#!/usr/bin/env python3
"""
Daily Threat Feed Collector — public version.
=============================================
Fetches public/free/read-only threat intel sources and emits a structured
JSON packet. See README.md and ../SCHEMA.md for details.

Sources: CISA KEV, ThreatFox, URLhaus, Ransomware.live, CIRCL, FIRST EPSS.
Credentials: ABUSE_CH_KEY env var only (optional; ThreatFox/URLhaus need it).
"""
import argparse
import datetime
import json
import os

import requests

ABUSE_HEADERS = {}
if os.getenv("ABUSE_CH_KEY"):
    ABUSE_HEADERS = {"Auth-Key": os.getenv("ABUSE_CH_KEY")}

CISA_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
THREATFOX_URL = "https://threatfox-api.abuse.ch/api/v1/"
URLHAUS_RECENT = "https://urlhaus-api.abuse.ch/v1/urls/recent/limit/{n}/"
RL_URL = "https://api.ransomware.live/v1/recentvictims"
CIRCL_URL = "https://vulnerability.circl.lu/api/last"
EPSS_URL = "https://api.first.org/data/v1/epss"


def _get(url, timeout=15):
    try:
        r = requests.get(url, timeout=timeout)
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
    data = _post(THREATFOX_URL, {"query": "get_iocs", "days": 7})
    if not isinstance(data, dict) or data.get("query_status") != "ok":
        return {"_error": "threatfox query failed", "items": []}
    raw = sorted(data.get("data", []), key=lambda x: x.get("first_seen", ""), reverse=True)[:limit]
    items = [{
        "type": "IOC",
        "value": e.get("ioc", "N/A"),
        "ioc_type": e.get("ioc_type", "N/A"),
        "malware": e.get("malware_printable", "N/A"),
        "confidence": e.get("confidence_level", "N/A"),
        "seen": e.get("first_seen", ""),
        "links": [u for u in [e.get("reference"), e.get("malware_malpedia")] if u],
    } for e in raw]
    return {"count": len(items), "items": items}


def fetch_urlhaus(limit=6):
    try:
        r = requests.get(URLHAUS_RECENT.format(n=limit), timeout=15, headers=ABUSE_HEADERS)
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
        "seen": e.get("date_added", ""),
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
        "links": ["https://www.ransomware.live"],
    } for e in data[:limit]]
    return {"count": len(items), "items": items}


def fetch_circl(limit=30):
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
                "links": [f"https://vulnerability.circl.lu/advisories/{cve_id.lower()}"],
            })
        elif isinstance(e, dict):
            refs = [(r.get("type"), r.get("url")) for r in (e.get("references") or []) if r.get("url")]
            items.append({
                "id": e.get("id", "N/A"),
                "aliases": [a for a in e.get("aliases", []) if a.startswith("CVE-")][:3],
                "severity": e.get("severity", "N/A"),
                "published": (e.get("published") or "N/A")[:10],
                "details": (e.get("details") or "N/A")[:250],
                "links": [u for t, u in refs if t in ("ADVISORY", "FIX", "EVIDENCE")][:3]
                or [f"https://vulnerability.circl.lu/advisories/{e.get('id', '').lower()}"],
            })
    return {"count": len(items), "items": items}


def fetch_epss(cve_ids, batch=100):
    cves = [c for c in dict.fromkeys(cve_ids) if c and c.startswith("CVE-")]
    scores = {}
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


def build_packet():
    kev = fetch_cisa_kev()
    tf = fetch_threatfox()
    uh = fetch_urlhaus()
    rl = fetch_ransomware_live()
    circl = fetch_circl()

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

    return {
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
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


def main():
    ap = argparse.ArgumentParser(description="Daily threat feed collector")
    ap.add_argument("--out", default=".", help="Output directory (default: current dir)")
    args = ap.parse_args()

    packet = build_packet()
    fname = f"{packet['date']}.json"
    path = os.path.join(args.out, fname)
    with open(path, "w") as f:
        json.dump(packet, f, indent=2)

    print(f"Wrote {path}")
    for name, meta in packet["sources"].items():
        print(f"  {name}: {meta['status']} ({meta['count']} items)")


if __name__ == "__main__":
    main()
