#!/usr/bin/env python3
"""
SMB + AI Threat Feed — collector (deterministic source layer).
==============================================================
Fetches public, free, read-only threat intel sources and writes that day's
structured JSON packet (see ../SCHEMA.md). This is the same collection logic
the published feed runs each morning; no AI is involved in this step.

Sources: CISA KEV, ThreatFox, URLhaus, Ransomware.live, CIRCL Vulnerability
Lookup, FIRST EPSS enrichment.

Credentials: ABUSE_CH_KEY environment variable (or a local .env file). Optional;
only ThreatFox and URLhaus need it. The other sources are keyless.

Safety: public, read-only sources only. No secrets are printed. Each source is
isolated, so one failure never kills the run. Ransomware leak-site (.onion)
links are never emitted.
"""
import argparse
import datetime
import json
import os

import requests

try:  # optional: load ABUSE_CH_KEY from a local .env
    import dotenv
    dotenv.load_dotenv()
except ImportError:
    pass

DATE_STR = datetime.datetime.now().strftime("%m-%d-%Y")
ABUSE_CH_KEY = os.getenv("ABUSE_CH_KEY")
ABUSE_HEADERS = {"Auth-Key": ABUSE_CH_KEY} if ABUSE_CH_KEY else {}


def iso_to_mmdd(value):
    """Date-only YYYY-MM-DD → MM-DD-YYYY. Leave timestamps/other strings alone."""
    if not value or not isinstance(value, str):
        return value
    s = value.strip()
    if len(s) >= 10 and s[4] == "-" and s[7] == "-" and s[:4].isdigit():
        y, m, d = s[:10].split("-")
        return f"{m}-{d}-{y}" + s[10:]
    return value

CISA_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
THREATFOX_URL = "https://threatfox-api.abuse.ch/api/v1/"
URLHAUS_URL = "https://urlhaus-api.abuse.ch/api/v1/"
RL_URL = "https://api.ransomware.live/v1/recentvictims"
CIRCL_URL = "https://vulnerability.circl.lu/api/last"
EPSS_URL = "https://api.first.org/data/v1/epss"


def fetch_epss(cve_ids, batch=100):
    """EPSS exploitation-likelihood scores (FIRST, free API, no auth).

    Batch query by CVE id. Returns {cve: {"epss": float, "percentile": float}}.
    Missing CVEs are skipped by the API. Isolated failures return {}.
    """
    cves = [c for c in dict.fromkeys(cve_ids) if c and c.startswith("CVE-")]
    scores = {}
    if not cves:
        return scores
    for i in range(0, len(cves), batch):
        chunk = cves[i:i + batch]
        try:
            r = requests.get(EPSS_URL, params={"cve": ",".join(chunk)}, timeout=20)
            r.raise_for_status()
            for entry in r.json().get("data", []):
                scores[entry["cve"]] = {
                    "epss": round(float(entry.get("epss", 0)), 4),
                    "percentile": round(float(entry.get("percentile", 0)), 4),
                }
        except Exception:
            continue
    return scores


def _get(url, timeout=15, **kwargs):
    try:
        r = requests.get(url, timeout=timeout, **kwargs)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"_error": f"{type(e).__name__}: {e}"}


def _post(url, payload, timeout=15):
    try:
        r = requests.post(url, json=payload, timeout=timeout, headers=ABUSE_HEADERS)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"_error": f"{type(e).__name__}: {e}"}


def fetch_cisa_kev(days=7):
    """KEV entries added in the last N days, newest first."""
    data = _get(CISA_URL)
    if not isinstance(data, dict) or "vulnerabilities" not in data:
        return {"_error": "no KEV data", "items": []}
    threshold = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)
    items = []
    for v in data["vulnerabilities"]:
        try:
            added = datetime.datetime.strptime(v["dateAdded"], "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc)
        except Exception:
            continue
        if added >= threshold:
            items.append({
                "cve": v.get("cveID"),
                "added": v.get("dateAdded"),
                "vendor": v.get("vendorProject"),
                "product": v.get("product"),
                "description": v.get("shortDescription", "")[:300],
                "action": v.get("requiredAction", "")[:200],
                "due": v.get("dueDate"),
                "ransomware_use": v.get("knownRansomwareCampaignUse", "Unknown"),
                "notes": v.get("notes", "")[:300],
                "links": [u for u in (v.get("notes") or "").split(";") if u.strip().startswith("http")][:2],
            })
    items.sort(key=lambda x: x["added"], reverse=True)
    return {"count": len(items), "items": items}


def fetch_threatfox(limit=8):
    """Recent malware-linked IOCs (ThreatFox API v1, Auth-Key header, get_iocs)."""
    data = _post(THREATFOX_URL, {"query": "get_iocs", "days": 7})
    if not isinstance(data, dict) or data.get("query_status") != "ok":
        return {"_error": "threatfox query failed", "items": []}
    raw = data.get("data", [])
    raw = sorted(raw, key=lambda x: x.get("first_seen", ""), reverse=True)[:limit]
    items = [{
        "type": "IOC",
        "value": e.get("ioc", "N/A"),
        "ioc_type": e.get("ioc_type", "N/A"),
        "malware": e.get("malware_printable", "N/A"),
        "confidence": e.get("confidence_level", "N/A"),
        "seen": e.get("first_seen", DATE_STR),
        "links": [u for u in [e.get("reference"), e.get("malware_malpedia")] if u],
    } for e in raw]
    return {"count": len(items), "items": items}


def fetch_urlhaus(limit=6):
    """Recent malicious URLs (URLhaus API v1 GET, Auth-Key header)."""
    url = f"https://urlhaus-api.abuse.ch/v1/urls/recent/limit/{limit}/"
    try:
        r = requests.get(url, timeout=15, headers=ABUSE_HEADERS)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        return {"_error": f"{type(e).__name__}: {e}", "items": []}
    if not isinstance(data, dict) or data.get("query_status") != "ok":
        return {"_error": "urlhaus query failed", "items": []}
    items = [{
        "type": "URL",
        "value": e.get("url", "N/A"),
        "host": e.get("host", "N/A"),
        "status": e.get("url_status", "N/A"),
        "seen": e.get("date_added", DATE_STR),
        "links": [u for u in [e.get("urlhaus_reference")] if u],
    } for e in data.get("urls", [])[:limit]]
    return {"count": len(items), "items": items}


def fetch_ransomware_live(limit=10):
    data = _get(RL_URL)
    if not isinstance(data, list):
        return {"_error": "ransomware.live query failed", "items": []}
    items = [{
        "group": e.get("group_name", "N/A"),
        "sector": e.get("activity", "N/A"),
        "country": e.get("country", "N/A"),
        "description": (e.get("description") or "N/A")[:200],
        "discovered": (e.get("discovered") or "N/A")[:19],
        "links": ["https://www.ransomware.live"] + ([e.get("post_url")] if (e.get("post_url") or "").startswith("https://www.ransomware.live") else []),
    } for e in data[:limit]]
    return {"count": len(items), "items": items}


def fetch_circl(limit=30):
    """Recent vuln coverage (CIRCL Vulnerability Lookup /api/last).

    The endpoint returns a mixed list: OSV-style records (id/aliases/details)
    and raw CVE 5.2 records (cveMetadata/containers). Normalize both shapes.
    """
    data = _get(CIRCL_URL)
    if not isinstance(data, list):
        return {"_error": "circl query failed", "items": []}
    items = []
    for e in data[:limit]:
        if isinstance(e, dict) and e.get("dataType") == "CVE_RECORD":
            meta = e.get("cveMetadata", {})
            cve_id = meta.get("cveId", "N/A")
            descs = (e.get("containers", {}).get("cna", {}).get("descriptions") or [])
            details = next((d.get("value", "") for d in descs if (d.get("lang") or "").lower().startswith("en")), "")
            items.append({
                "id": cve_id,
                "aliases": [cve_id],
                "severity": "N/A",
                "published": (meta.get("datePublished") or "N/A")[:10],
                "details": details[:250],
                "links": [f"https://vulnerability.circl.lu/vuln/{cve_id}"],
            })
        elif isinstance(e, dict):
            refs = [(r.get("type"), r.get("url")) for r in (e.get("references") or []) if r.get("url")]
            items.append({
                "id": e.get("id", "N/A"),
                "aliases": [a for a in e.get("aliases", []) if a.startswith("CVE-")][:3],
                "severity": e.get("severity", "N/A"),
                "published": (e.get("published") or "N/A")[:10],
                "details": (e.get("details") or "N/A")[:250],
                "links": [u for t, u in refs if t in ("ADVISORY", "FIX", "EVIDENCE")][:3] or [f"https://vulnerability.circl.lu/vuln/{e.get('id','')}"],
            })
    return {"count": len(items), "items": items}


def build_packet():
    kev = fetch_cisa_kev()
    tf = fetch_threatfox()
    uh = fetch_urlhaus()
    rl = fetch_ransomware_live()
    circl = fetch_circl()

    # EPSS enrichment: score all CVE ids seen in KEV + CIRCL aliases
    cve_ids = [v["cve"] for v in kev.get("items", [])]
    cve_ids += [a for v in circl.get("items", []) for a in v.get("aliases", [])]
    epss = fetch_epss(cve_ids)
    for v in kev.get("items", []):
        v["epss"] = epss.get(v["cve"], {}).get("epss")
        v["epss_percentile"] = epss.get(v["cve"], {}).get("percentile")
    for v in circl.get("items", []):
        hit = next((epss.get(a) for a in v.get("aliases", []) if a in epss), None)
        if hit:
            v["epss"] = hit["epss"]
            v["epss_percentile"] = hit["percentile"]

    # Build into a variable (not `return {...}`) so the date normalization below
    # actually runs — KEV added/due must be MM-DD-YYYY per SCHEMA.md.
    packet = {
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "date": DATE_STR,
        "sources": {
            "cisa_kev": {"status": "ok" if not kev.get("_error") else kev["_error"], "count": kev.get("count", 0)},
            "threatfox": {"status": "ok" if not tf.get("_error") else tf["_error"], "count": tf.get("count", 0)},
            "urlhaus": {"status": "ok" if not uh.get("_error") else uh["_error"], "count": uh.get("count", 0)},
            "ransomware_live": {"status": "ok" if not rl.get("_error") else rl["_error"], "count": rl.get("count", 0)},
            "circl": {"status": "ok" if not circl.get("_error") else circl["_error"], "count": circl.get("count", 0)},
            "epss": {"status": f"ok ({len(epss)}/{len(set(cve_ids))} scored)" if epss else "no scores", "count": len(epss)},
        },
        "kev": kev.get("items", []),
        "threatfox": tf.get("items", []),
        "urlhaus": uh.get("items", []),
        "ransomware": rl.get("items", []),
        "circl": circl.get("items", []),
    }
    packet["date"] = DATE_STR
    for v in packet["kev"]:
        v["added"] = iso_to_mmdd(v.get("added"))
        v["due"] = iso_to_mmdd(v.get("due"))
    return packet


def main():
    ap = argparse.ArgumentParser(description="SMB + AI Threat Feed collector")
    ap.add_argument("--out", default=".", help="Output directory (default: current dir)")
    args = ap.parse_args()

    packet = build_packet()
    path = os.path.join(args.out, f"{packet['date']}.json")
    with open(path, "w") as f:
        json.dump(packet, f, indent=2)

    print(f"Wrote {path}")
    for name, meta in packet["sources"].items():
        print(f"  {name}: {meta['status']} ({meta['count']} items)")
    print("\nQuick digest:")
    for v in packet["kev"][:5]:
        ep = f" | EPSS {v['epss']} (p{v['epss_percentile']})" if v.get("epss") is not None else ""
        print(f"  KEV {v['cve']} ({v['vendor']} {v['product']}, added {v['added']}){ep}")
    for v in packet["ransomware"][:5]:
        print(f"  RL group={v['group']} sector={v['sector']} country={v['country']} discovered={v['discovered']}")
    for v in packet["circl"][:5]:
        print(f"  CIRCL {v['id']} sev={v['severity']} aliases={','.join(v['aliases'][:2])}")


if __name__ == "__main__":
    main()
