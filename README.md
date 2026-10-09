# SMB + AI Threat Feed

A plain-language threat briefing for **small businesses running AI and automation**. EPSS-prioritized vulnerabilities, a ransomware sector pulse, and IOCs, compiled from free public sources and published most mornings.

**Read it:** [erichschmidt.com/briefing](https://erichschmidt.com/briefing/) · **RSS:** [erichschmidt.com/feed.xml](https://erichschmidt.com/feed.xml) · Built by [Erich Schmidt](https://erichschmidt.com)

## Why this feed exists

Most threat intelligence is written for enterprise security teams. It's full of jargon, and it's useless if you run a 20-person company that just added an AI assistant. Every finding in this feed answers three questions:

1. **What broke**, in plain language.
2. **Why it matters to a small business running AI tools.**
3. **What you do Monday**: concrete next steps, not vendor boilerplate.

## How this is made

This feed is written with AI, and here's exactly how:

1. **Collect (deterministic code).** [`collector/collector.py`](collector/collector.py) pulls from the public sources listed below and writes that day's structured data to `data/MM-DD-YYYY.json`. There's no AI in this step. Each source is isolated, so one failing source never kills the run.
2. **Draft (AI).** An AI model writes the brief from that day's collected data, in the fixed format above, with a source link for every finding.
3. **Publish (automatic).** The brief, data and RSS are committed here automatically. **No one reviews each brief before it goes out.**

So treat it the way you'd treat a sharp but junior analyst's morning notes: useful for knowing *what to look at*, never the final word. Every claim links to its source, so check it and your vendor's advisory before you change anything. If you spot an error, [open an issue](https://github.com/erichschmidt/smb-ai-threat-feed/issues).

## Not advice

This is general information, not security, legal or professional advice, and it comes with no warranty. Commands and steps in the briefs are examples. Confirm them against your vendor's documentation and your own environment before running them.

## What's here

| Path | What it is |
|---|---|
| `briefs/Threat-Feed-MM-DD-YYYY.md` | The day's brief (the 3-minute read) |
| `data/MM-DD-YYYY.json` | Structured, machine-readable data for that day |
| `latest.json` | The most recent day's data. Poll this URL for automation. |
| `feed.xml` | Atom feed of the briefs |
| `GLOSSARY.md` | Plain-language definitions of every term used |
| `collector/` | The open-source collector. Run it yourself and check the data. |

## Consuming the data

Each day's data is in `data/MM-DD-YYYY.json`, mirrored to `latest.json`. Shape:

```json
{
  "date": "08-19-2026",
  "sources": { "cisa_kev": {"status": "ok", "count": 5}, "...": "..." },
  "kev": [ { "cve": "CVE-2026-33824", "product": "...", "epss": 0.779, "epss_percentile": 0.995, "links": ["..."] } ],
  "ransomware": [ { "group": "...", "sector": "...", "country": "...", "discovered": "..." } ],
  "circl": [ { "id": "...", "aliases": ["CVE-..."], "severity": "...", "details": "...", "links": ["..."] } ],
  "threatfox": [ { "value": "...", "ioc_type": "...", "malware": "...", "links": ["..."] } ],
  "urlhaus": [ { "value": "...", "status": "...", "links": ["..."] } ]
}
```

Full field documentation: [SCHEMA.md](SCHEMA.md).

**Prioritization:** each CVE carries an EPSS score (0–1, the likelihood of exploitation in the next 30 days) and a percentile rank. Sort by `epss`, highest first, to build a patch order.

## Sources (all public, free, read-only)

- **CISA KEV:** vulnerabilities confirmed as actively exploited (the prioritization anchor)
- **FIRST EPSS:** exploitation-likelihood scoring
- **Ransomware.live:** victim disclosures and sector targeting (leak-site links are deliberately excluded)
- **CIRCL Vulnerability Lookup:** current CVE coverage
- **ThreatFox / URLhaus (abuse.ch):** malware IOCs

Every finding links to its source. No link, no claim.

## Running the collector yourself

```bash
cd collector
pip install -r requirements.txt
export ABUSE_CH_KEY=your_abuse_ch_key   # optional: only ThreatFox/URLhaus need it
python collector.py --out ../data
```

## License

- **Briefs and data:** [CC BY 4.0](LICENSE). Reuse freely with attribution to *SMB + AI Threat Feed / Erich Schmidt*. Findings are compiled from public sources that keep their own terms, and each finding carries its source attribution.
- **Collector code** (`collector/`): [MIT](collector/LICENSE).
