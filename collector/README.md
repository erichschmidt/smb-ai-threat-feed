# Collector — smb-ai-threat-feed

Deterministic source layer for the daily feed. Fetches public, free, read-only APIs and emits a structured JSON packet (see [SCHEMA.md](../SCHEMA.md)).

## Sources

1. CISA KEV — actively exploited vulnerabilities (prioritization anchor)
2. ThreatFox (abuse.ch) — recent malware IOCs
3. URLhaus (abuse.ch) — recent malicious URLs
4. Ransomware.live — victim disclosures + sector targeting
5. CIRCL Vulnerability Lookup — current CVE coverage
6. FIRST EPSS — exploitation-likelihood enrichment for all CVE IDs found

Each source is isolated: one failure never kills the run.

## Requirements

- Python 3.9+
- `requests`, `python-dotenv`
- Optional: `ABUSE_CH_KEY` env var (only ThreatFox/URLhaus require it; the other four sources are keyless)

## Usage

```bash
pip install -r requirements.txt
export ABUSE_CH_KEY=your_abuse_ch_key   # optional
python collector.py --out ../data
```

Writes `YYYY-MM-DD.json` (and prints a digest to stdout). Idempotent — safe to run multiple times per day.

## Safety

- Public-source/read-only only. No exploit instructions, payloads, or public-target scanning.
- No secrets in code; credentials come from environment variables only.
- Leak-site (`.onion`) links are deliberately excluded from output — compliance-sensitive.
- Each finding links to its primary source.
