#!/usr/bin/env python3
"""
SMB + AI Threat Feed — collector (deterministic source layer).
==============================================================
Fetches public, free, read-only threat intel sources and writes that day's
structured JSON packet (see ../SCHEMA.md). This is the same collection logic
the published feed runs each morning; no AI is involved in this step.

Sources: CISA KEV, ThreatFox, URLhaus, Ransomware.live, CIRCL Vulnerability
Lookup, GitHub-reviewed advisories for an AI tool watchlist (via OSV.dev),
FIRST EPSS enrichment.

It also picks what the brief covers (`brief_plan`): which findings, in what
order, at what severity, and which ones were already reported on earlier days.
That keeps selection and severity in deterministic code; the drafting step only
writes the prose.

Credentials: ABUSE_CH_KEY environment variable (or a local .env file). Optional;
only ThreatFox and URLhaus need it. The other sources are keyless.

Safety: public, read-only sources only. No secrets are printed. Each source is
isolated, so one failure never kills the run. Ransomware leak-site (.onion)
links are never emitted.
"""
import argparse
import collections
import datetime
import glob
import json
import os
import re

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
OSV_BATCH_URL = "https://api.osv.dev/v1/querybatch"
OSV_VULN_URL = "https://api.osv.dev/v1/vulns/"
OSV_ECOSYSTEMS = {"pip": "PyPI", "npm": "npm", "go": "Go"}

# AI and automation packages small businesses commonly run or build on, by
# ecosystem. Edit freely; the whole list is one OSV batch query.
AI_WATCHLIST = {
    "pip": ["langchain", "langchain-core", "langchain-community", "langgraph",
            "llama-index-core", "litellm", "open-webui", "transformers", "vllm",
            "gradio", "mlflow", "ray", "picklescan", "crewai", "mcp", "chromadb",
            "langflow"],
    "npm": ["n8n", "flowise", "langchain", "@langchain/core",
            "@modelcontextprotocol/sdk", "ai"],
    "go": ["github.com/ollama/ollama"],
}
# The subset most likely to be run directly by a small business; ranked first.
AI_SMB_COMMON = {"n8n", "flowise", "open-webui", "github.com/ollama/ollama",
                 "langchain", "langchain-core", "langchain-community",
                 "@langchain/core", "litellm", "mcp", "@modelcontextprotocol/sdk",
                 "langflow"}
# Words that mark a KEV/CIRCL entry as being about an AI or automation product.
AI_TERMS = re.compile(
    r"\b(llms?|large language models?|langchain|langgraph|llama[-_ ]?index|litellm|"
    r"open[- ]?webui|ollama|vllm|gradio|mlflow|picklescan|crewai|mcp|"
    r"model context protocol|chromadb|langflow|flowise|n8n|openai|anthropic|"
    r"copilot|chatgpt|gpt-\d|retrieval[- ]augmented|rag pipeline|prompt injection|"
    r"ai agents?|agentic|hugging ?face|pytorch|tensorflow)\b", re.I)

# Plain-language AI risks that have no CVE. One is covered each Monday, in order.
AI_RISK_TOPICS = [
    {"title": "Prompt injection through emails and documents",
     "scope": "Hidden instructions in an email, web page or shared file that an AI assistant reads and then follows."},
    {"title": "Sensitive data pasted into AI tools",
     "scope": "Staff pasting customer, financial or HR data into consumer AI tools that keep or train on it."},
    {"title": "AI integrations with too much access",
     "scope": "OAuth grants, API keys and MCP servers that give an AI tool more access than its job needs."},
    {"title": "Deepfake voice and video payment fraud",
     "scope": "Cloned voices or faces of a boss or vendor used to push an urgent payment or bank-detail change."},
    {"title": "AI-written phishing",
     "scope": "Polished, personalized phishing that no longer has the spelling mistakes people were taught to look for."},
    {"title": "Malicious models, extensions and packages",
     "scope": "Downloaded models, browser extensions and AI plugins that carry hidden code."},
    {"title": "Unapproved \"shadow AI\" tools",
     "scope": "AI apps staff sign up for on their own, outside any review of what data they can reach."},
    {"title": "AI agents that can act, not just answer",
     "scope": "Agents with write access to email, files or payments, and why a human approval step matters."},
]

SEVERITY_RANK = {"CRITICAL": 0, "HIGH": 1, "WATCH": 2}
GHSA_SEVERITY_RANK = {"critical": 0, "high": 1, "medium": 2, "moderate": 2, "low": 3}
NO_LOGIN = re.compile(
    r"\bunauthenticated\b|without (?:any )?(?:authentication|logging in|login|credentials)|"
    r"no authentication|pre-?auth(?:entication)?\b|does not require authentication", re.I)
RCE = re.compile(
    r"remote code execution|execute arbitrary (?:code|commands)|arbitrary code execution|"
    r"run arbitrary code|command injection|code injection", re.I)


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
                "links": [u.strip() for u in (v.get("notes") or "").split(";") if u.strip().startswith("http")][:2],
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


def cvss3_score(vector):
    """CVSS 3.x base score from a vector string, or None if it isn't a valid v3 vector."""
    try:
        m = dict(part.split(":") for part in vector.split("/")[1:])
        changed = m["S"] == "C"
        av = {"N": 0.85, "A": 0.62, "L": 0.55, "P": 0.2}[m["AV"]]
        ac = {"L": 0.77, "H": 0.44}[m["AC"]]
        pr = ({"N": 0.85, "L": 0.68, "H": 0.5} if changed else {"N": 0.85, "L": 0.62, "H": 0.27})[m["PR"]]
        ui = {"N": 0.85, "R": 0.62}[m["UI"]]
        cia = [{"H": 0.56, "L": 0.22, "N": 0.0}[m[k]] for k in ("C", "I", "A")]
    except (AttributeError, KeyError, ValueError):
        return None
    iss = 1 - (1 - cia[0]) * (1 - cia[1]) * (1 - cia[2])
    impact = 7.52 * (iss - 0.029) - 3.25 * (iss - 0.02) ** 15 if changed else 6.42 * iss
    if impact <= 0:
        return 0.0
    raw = min((1.08 if changed else 1) * (impact + 8.22 * av * ac * pr * ui), 10)
    n = round(raw * 100000)  # CVSS 3.1 Roundup
    return n / 100000 if n % 10000 == 0 else (n // 10000 + 1) / 10


def _osv_range(affected):
    """GitHub-style vulnerable range and first fixed version from an OSV `affected` entry."""
    events = [e for r in affected.get("ranges") or [] for e in r.get("events") or []]
    introduced = next((e["introduced"] for e in events if "introduced" in e), None)
    fixed = next((e["fixed"] for e in events if "fixed" in e), None)
    last = next((e["last_affected"] for e in events if "last_affected" in e), None)
    parts = [f">= {introduced}"] if introduced and introduced != "0" else []
    known = (affected.get("database_specific") or {}).get("last_known_affected_version_range")
    if known:
        parts.append(known)
    elif fixed:
        parts.append(f"< {fixed}")
    elif last:
        parts.append(f"<= {last}")
    return ", ".join(parts) or None, fixed


def fetch_ai_advisories(days=7, limit=15):
    """Recent GitHub-reviewed advisories for the AI tool watchlist, from OSV.dev (no auth).

    One batch query lists every advisory for the watched packages; only the
    ones modified inside the window are fetched in full. Failed fetches are
    reported in `_error` while the rest are kept.
    """
    since = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
    watched = {(OSV_ECOSYSTEMS[eco], p): eco for eco, pkgs in AI_WATCHLIST.items() for p in pkgs}
    queries = [{"package": {"name": name, "ecosystem": osv_eco}} for osv_eco, name in watched]
    try:
        r = requests.post(OSV_BATCH_URL, json={"queries": queries}, timeout=30)
        r.raise_for_status()
        results = r.json().get("results") or []
    except Exception as e:
        return {"count": 0, "items": [], "_error": f"osv: {type(e).__name__}: {e}"}
    ids = {v["id"] for res in results for v in res.get("vulns") or []
           if v.get("id", "").startswith("GHSA-") and (v.get("modified") or "")[:10] >= since}

    items, errors = [], []
    for ghsa in sorted(ids):
        a = _get(OSV_VULN_URL + ghsa, timeout=20)
        if a.get("_error"):
            errors.append(f"{ghsa}: {a['_error']}")
            continue
        db = a.get("database_specific") or {}
        if a.get("withdrawn") or not db.get("github_reviewed") or (a.get("published") or "")[:10] < since:
            continue
        hit = next((v for v in a.get("affected") or []
                    if ((v.get("package") or {}).get("ecosystem"), (v.get("package") or {}).get("name")) in watched), None)
        if not hit:
            continue
        pkg = hit["package"]
        affected, patched = _osv_range(hit)
        vector = next((s.get("score") for s in a.get("severity") or [] if s.get("type") == "CVSS_V3"), None)
        severity = str(db.get("severity") or "N/A").lower()
        items.append({
            "id": a["id"],
            "cve": next((x for x in a.get("aliases") or [] if x.startswith("CVE-")), None),
            "package": pkg["name"],
            "ecosystem": watched[(pkg["ecosystem"], pkg["name"])],
            "smb_common": pkg["name"] in AI_SMB_COMMON,
            "severity": "medium" if severity == "moderate" else severity,
            "cvss": cvss3_score(vector),
            "summary": (a.get("summary") or "")[:250],
            "details": (a.get("details") or "")[:400],
            "affected": affected,
            "patched": patched,
            "published": a["published"][:10],
            "links": [f"https://github.com/advisories/{a['id']}"],
        })
    items.sort(key=lambda x: x["published"], reverse=True)
    items.sort(key=lambda x: (GHSA_SEVERITY_RANK.get(x["severity"], 4), not x["smb_common"]))
    items = items[:limit]
    for x in items:
        x["published"] = iso_to_mmdd(x["published"])
    result = {"count": len(items), "items": items}
    if errors:
        result["_error"] = f"osv: {len(errors)} of {len(ids)} advisories failed to load ({errors[0]})"
    return result


def _parse_mmdd(value):
    try:
        return datetime.datetime.strptime(value, "%m-%d-%Y")
    except (TypeError, ValueError):
        return None


def _item_keys(item):
    keys = {item.get("cve"), item.get("id"), *(item.get("aliases") or [])}
    return {k for k in keys if k and k != "N/A"}


def load_prior_packets(paths, today):
    """Earlier daily packets, oldest first. Today's own file is skipped so re-runs are idempotent."""
    prior = []
    for path in paths:
        try:
            with open(path) as f:
                p = json.load(f)
        except Exception:
            continue
        day = _parse_mmdd(p.get("date") if isinstance(p, dict) else None)
        if day and p["date"] != today:
            prior.append((day, p))
    prior.sort(key=lambda x: x[0])
    return prior


def annotate_history(packet, prior):
    """Add `first_seen` and `prev_epss` to every KEV, CIRCL and AI advisory item.

    KEV is tracked on its own, so an old CVE that newly lands in KEV counts as new
    there. CIRCL and AI advisories share one history.
    """
    first = {"kev": {}, "vuln": {}}
    last_epss = {"kev": {}, "vuln": {}}
    for day, p in prior:
        for section in ("kev", "circl", "ai_advisories"):
            bucket = "kev" if section == "kev" else "vuln"
            for item in p.get(section) or []:
                for k in _item_keys(item):
                    first[bucket].setdefault(k, day)
                    last_epss[bucket][k] = item.get("epss")
    for section in ("kev", "circl", "ai_advisories"):
        bucket = "kev" if section == "kev" else "vuln"
        for item in packet.get(section) or []:
            keys = _item_keys(item)
            seen = [first[bucket][k] for k in keys if k in first[bucket]]
            item["first_seen"] = min(seen).strftime("%m-%d-%Y") if seen else packet["date"]
            item["prev_epss"] = next((last_epss[bucket][k] for k in keys if k in last_epss[bucket]), None)


def rate_severity(section, item):
    """The public severity rubric (README), as code. Returns (label, reason)."""
    text = " ".join(str(item.get(k) or "") for k in ("description", "details", "summary"))
    epss = item.get("epss") or 0
    pct = item.get("epss_percentile") or 0
    no_login = bool(NO_LOGIN.search(text))
    if section == "kev":
        if item.get("ransomware_use") == "Known":
            return "CRITICAL", "in CISA KEV · known ransomware use"
        if no_login:
            return "CRITICAL", "in CISA KEV · no login needed"
        return "HIGH", "in CISA KEV"
    if epss >= 0.1 or pct >= 0.95:
        return "HIGH", f"not in KEV · EPSS {epss} ({pct * 100:.0f}th percentile)"
    if no_login and RCE.search(text):
        return "HIGH", "not in KEV · remote code execution without a login"
    if item.get("epss") is None:
        return "WATCH", "not in KEV · no EPSS score yet"
    return "WATCH", f"not in KEV · low EPSS ({epss})"


def _is_ai(section, item):
    if section == "ai_advisories":
        return True
    text = " ".join(str(item.get(k) or "") for k in ("vendor", "product", "description", "id", "details"))
    return bool(AI_TERMS.search(text))


def ransomware_pulse(items, top=3):
    """One factual sentence on recent ransomware victim claims, for the brief to copy as-is."""
    if not items:
        return "No recent ransomware victim claims in the latest listing."
    skip = {"", "N/A", "Not Found", "Other", "Unknown"}
    sectors = collections.Counter(r.get("sector") for r in items if r.get("sector") not in skip)
    countries = collections.Counter(r.get("country") for r in items if r.get("country") not in skip)
    parts = [f"{len(items)} recent victim claims"]
    if sectors:
        parts.append("most-hit sectors: " + ", ".join(f"{s} ({n})" for s, n in sectors.most_common(top)))
    if countries:
        parts.append("countries: " + ", ".join(f"{c} ({n})" for c, n in countries.most_common(top)))
    return "; ".join(parts) + "."


def plan_brief(packet, max_findings=3, radar_days=14, radar_max=3):
    """Decide what the brief covers. The drafting step must follow this exactly.

    - Findings: at most `max_findings`. AI items first. An item qualifies if it is
      new today, or seen before but its EPSS crossed 0.1 since then. One finding
      per product. At most one non-AI item, and only a new CRITICAL KEV entry.
    - On the radar (one-line mentions): new AI items that didn't make the cut,
      plus AI items rated HIGH or CRITICAL first seen in the last `radar_days` days.
    - Quiet AI day: no AI finding today.
    - AI risk of the week: Mondays only, rotating through AI_RISK_TOPICS.
    """
    today = _parse_mmdd(packet["date"])
    candidates = {}
    for section in ("kev", "ai_advisories", "circl"):
        for item in packet.get(section) or []:
            severity, reason = rate_severity(section, item)
            ai = _is_ai(section, item)
            if section == "ai_advisories" and item.get("severity") == "low":
                continue
            new = item.get("first_seen") == packet["date"]
            prev, epss = item.get("prev_epss"), item.get("epss")
            escalated = not new and prev is not None and epss is not None and prev < 0.1 <= epss
            entry = {
                "section": section,
                "id": item.get("cve") if section == "kev" else item.get("id"),
                "cve": item.get("cve") or next((a for a in item.get("aliases") or [] if a.startswith("CVE-")), None),
                "severity": severity,
                "severity_reason": reason,
                "ai": ai,
                "selected_because": "new today" if new else ("EPSS crossed 0.1 since last seen" if escalated else None),
                "first_seen": item.get("first_seen"),
                "item": item,
            }
            key = entry["cve"] or entry["id"]
            have = candidates.get(key)
            # The same CVE can appear in several sources: keep the strongest rating.
            if not have or SEVERITY_RANK[severity] < SEVERITY_RANK[have["severity"]]:
                candidates[key] = entry

    def rank(e):
        return (SEVERITY_RANK[e["severity"]], GHSA_SEVERITY_RANK.get(str(e["item"].get("severity")).lower(), 4),
                not e["item"].get("smb_common", False), -(e["item"].get("epss") or 0))

    fresh = [e for e in candidates.values() if e["selected_because"]]
    other_pool = sorted([e for e in fresh if not e["ai"] and e["section"] == "kev" and e["severity"] == "CRITICAL"], key=rank)
    ai_slots = max_findings - min(1, len(other_pool))
    ai_findings, products = [], set()
    for e in sorted((e for e in fresh if e["ai"]), key=rank):
        # One finding per product; the rest can go on the radar.
        product = e["item"].get("package") or e["item"].get("product") or e["id"]
        if len(ai_findings) < ai_slots and product not in products:
            ai_findings.append(e)
            products.add(product)
    findings = ai_findings + other_pool[:1]

    chosen = {id(e) for e in findings}
    radar = []
    for e in sorted((e for e in candidates.values() if e["ai"] and id(e) not in chosen), key=rank):
        seen = _parse_mmdd(e["first_seen"])
        recent_high = e["severity"] in ("CRITICAL", "HIGH") and seen and (today - seen).days <= radar_days
        if e["selected_because"] or recent_high:
            radar.append({k: e[k] for k in ("section", "id", "cve", "severity", "severity_reason", "first_seen")}
                              | {"product": e["item"].get("package") or e["item"].get("product") or "",
                                 "links": e["item"].get("links") or []})
        if len(radar) == radar_max:
            break

    topic = None
    if today and today.weekday() == 0:
        topic = AI_RISK_TOPICS[today.isocalendar()[1] % len(AI_RISK_TOPICS)]

    return {
        "rules": "max 3 findings; AI first; repeats only on a stated change; at most one non-AI item (new CRITICAL KEV)",
        "findings": [{k: e[k] for k in ("section", "id", "cve", "severity", "severity_reason", "ai", "selected_because", "item")}
                     for e in findings],
        "on_the_radar": radar,
        "quiet_ai_day": not any(e["ai"] for e in findings),
        "ai_risk_topic": topic,
        "ransomware_pulse": ransomware_pulse(packet.get("ransomware") or []),
    }


def build_packet(prior_paths=()):
    kev = fetch_cisa_kev()
    tf = fetch_threatfox()
    uh = fetch_urlhaus()
    rl = fetch_ransomware_live()
    circl = fetch_circl()
    ai = fetch_ai_advisories()

    # EPSS enrichment: score all CVE ids seen in KEV, CIRCL aliases and AI advisories
    cve_ids = [v["cve"] for v in kev.get("items", [])]
    cve_ids += [a for v in circl.get("items", []) for a in v.get("aliases", [])]
    cve_ids += [v["cve"] for v in ai.get("items", []) if v.get("cve")]
    epss = fetch_epss(cve_ids)
    for v in kev.get("items", []) + ai.get("items", []):
        v["epss"] = epss.get(v.get("cve"), {}).get("epss")
        v["epss_percentile"] = epss.get(v.get("cve"), {}).get("percentile")
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
            "ai_advisories": {"status": "ok" if not ai.get("_error") else ai["_error"], "count": ai.get("count", 0)},
            "epss": {"status": f"ok ({len(epss)}/{len(set(cve_ids))} scored)" if epss else "no scores", "count": len(epss)},
        },
        "kev": kev.get("items", []),
        "threatfox": tf.get("items", []),
        "urlhaus": uh.get("items", []),
        "ransomware": rl.get("items", []),
        "circl": circl.get("items", []),
        "ai_advisories": ai.get("items", []),
    }
    packet["date"] = DATE_STR
    for v in packet["kev"]:
        v["added"] = iso_to_mmdd(v.get("added"))
        v["due"] = iso_to_mmdd(v.get("due"))
    annotate_history(packet, load_prior_packets(prior_paths, packet["date"]))
    packet["brief_plan"] = plan_brief(packet)
    return packet


def print_plan(plan):
    """The brief plan in plain text, for the drafting step's context."""
    print("\nBRIEF PLAN (follow exactly; do not add, drop, reorder or re-rate findings):")
    if not plan["findings"]:
        print("  No findings today.")
    for n, f in enumerate(plan["findings"], 1):
        item = f["item"]
        what = item.get("package") or " ".join(x for x in (item.get("vendor"), item.get("product")) if x) or item.get("id")
        print(f"  {n}. {f['severity']} | {f['section']} {f['id']}{' / ' + f['cve'] if f['cve'] and f['cve'] != f['id'] else ''}"
              f" | {what} | reason: {f['severity_reason']} | {'AI' if f['ai'] else 'not AI: open with General IT hygiene'}"
              f" | {f['selected_because']}")
    for r in plan["on_the_radar"]:
        print(f"  On the radar: {r['severity']} {r['id']} {r['product']} (first seen {r['first_seen']})")
    print(f"  Quiet AI day: {'yes' if plan['quiet_ai_day'] else 'no'}")
    topic = plan["ai_risk_topic"]
    print(f"  AI risk of the week: {topic['title'] if topic else 'none (Mondays only)'}")
    print(f"  Ransomware pulse (copy exactly): {plan['ransomware_pulse']}")


def main():
    ap = argparse.ArgumentParser(description="SMB + AI Threat Feed collector")
    ap.add_argument("--out", default=".", help="Output directory (default: current dir)")
    args = ap.parse_args()

    # Earlier packets in the output dir tell the planner what was already reported.
    prior = [p for p in glob.glob(os.path.join(args.out, "*.json"))
             if re.fullmatch(r"\d{2}-\d{2}-\d{4}\.json", os.path.basename(p))]
    packet = build_packet(prior)
    path = os.path.join(args.out, f"{packet['date']}.json")
    with open(path, "w") as f:
        json.dump(packet, f, indent=2)

    print(f"Wrote {path}")
    for name, meta in packet["sources"].items():
        print(f"  {name}: {meta['status']} ({meta['count']} items)")
    print_plan(packet["brief_plan"])
    print("\nQuick digest:")
    for v in packet["kev"][:5]:
        ep = f" | EPSS {v['epss']} (p{v['epss_percentile']})" if v.get("epss") is not None else ""
        print(f"  KEV {v['cve']} ({v['vendor']} {v['product']}, added {v['added']}){ep}")
    for v in packet["ransomware"][:5]:
        print(f"  RL group={v['group']} sector={v['sector']} country={v['country']} discovered={v['discovered']}")
    for v in packet["circl"][:5]:
        print(f"  CIRCL {v['id']} sev={v['severity']} aliases={','.join(v['aliases'][:2])}")
    for v in packet["ai_advisories"][:8]:
        seen = "new" if v["first_seen"] == packet["date"] else f"seen since {v['first_seen']}"
        print(f"  AI {v['id']} {v['package']} sev={v['severity']} cve={v['cve']} ({seen})")


if __name__ == "__main__":
    main()
