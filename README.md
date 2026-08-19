# smb-ai-threat-feed

Daily threat intelligence for **small businesses deploying AI and automation**.

Plain-language briefs, EPSS-prioritized vulnerabilities, ransomware sector pulse, and IOCs — compiled every day from free public sources.

## Why this feed exists

Most threat intelligence is written for enterprise SOCs: full of jargon, and useless if you run a 20-person company that just added an AI assistant. This feed answers three questions for every finding:

1. **What broke** — in plain language.
2. **Why it matters to a small business running AI tools** — the translation layer.
3. **What you do Monday** — literal next steps, not vendor boilerplate.

## What's here

| Path | What it is |
|---|---|
| `briefs/MM-DD-YYYY.md` | Human-readable daily brief (the 3-minute read) |
| `data/YYYY-MM-DD.json` | Structured machine-readable data for each day |
| `latest.json` | Always points at today's structured data — poll this URL for automation |
| `GLOSSARY.md` | Plain-language definitions of every term used |
| `collector/` | The open-source generator — run it yourself, verify the feed |

## Consuming the data

The structured feed is in `data/YYYY-MM-DD.json` (mirrored to `latest.json`). Shape:

```json
{
  "date": "2026-08-19",
  "sources": { "cisa_kev": {"status": "ok", "count": 5}, "...": "..." },
  "kev": [ { "cve": "CVE-2026-33824", "product": "...", "epss": 0.779, "epss_percentile": 0.995, "links": ["..."] } ],
  "ransomware": [ { "group": "...", "sector": "...", "country": "...", "discovered": "..." } ],
  "circl": [ { "id": "...", "aliases": ["CVE-..."], "severity": "...", "details": "...", "links": ["..."] } ],
  "threatfox": [ { "value": "...", "ioc_type": "...", "malware": "...", "links": ["..."] } ],
  "urlhaus": [ { "value": "...", "status": "...", "links": ["..."] } ]
}
```

Full field documentation: [SCHEMA.md](SCHEMA.md).

**Prioritization:** each CVE carries an EPSS score (0–1, likelihood of exploitation in the next 30 days) plus a percentile ranking. Sort by `epss` descending to build your patch order.

## Sources (all public, free, read-only)

- **CISA KEV** — actively exploited vulnerabilities (prioritization anchor)
- **CISA Advisories** — joint NSA/CISA/FBI campaign warnings
- **FIRST EPSS** — exploitation-likelihood scoring
- **Ransomware.live** — victim disclosures and sector targeting
- **CIRCL Vulnerability Lookup** — current CVE coverage
- **ThreatFox / URLhaus (abuse.ch)** — malware IOCs

Every finding links to its primary source. No link, no claim.

## Running the collector yourself

```bash
cd collector
pip install -r requirements.txt
export ABUSE_CH_KEY=your_abuse_ch_key   # optional — only ThreatFox/URLhaus need it
python collector.py --out ../data
```

## License

CC-BY-4.0 — reuse freely with attribution. Data is compiled from public sources (see their respective terms); source attribution for each finding is embedded in the feed itself.
