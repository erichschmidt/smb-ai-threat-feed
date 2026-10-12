# Schema — smb-ai-threat-feed structured data

Version: 1.2 · Each daily file lives at `data/MM-DD-YYYY.json` and is mirrored to `latest.json`.

1.2 (10-12-2026) adds `ai_advisories`, the history fields `first_seen` and `prev_epss`, and `brief_plan`. Files before 10-12-2026 don't have them.

## Top level

| Field | Type | Description |
|---|---|---|
| `generated` | string (ISO-8601) | UTC timestamp when the packet was collected |
| `date` | string `MM-DD-YYYY` | Feed date |
| `sources` | object | Per-source status and item count (`status`: `ok` or error string; `count`: int) |
| `kev` | array | CISA Known Exploited Vulnerabilities added in the last 7 days |
| `ransomware` | array | Recent Ransomware.live victim disclosures |
| `circl` | array | Recent CIRCL Vulnerability Lookup entries |
| `ai_advisories` | array | GitHub-reviewed advisories from the last 7 days for a watchlist of common AI and automation tools |
| `threatfox` | array | Recent ThreatFox IOCs |
| `urlhaus` | array | Recent URLhaus URLs |
| `brief_plan` | object | What the day's brief covers, decided by the collector (see below) |

## `kev[]`

| Field | Type | Description |
|---|---|---|
| `cve` | string | CVE identifier (e.g. `CVE-2026-33824`) |
| `added` | string `MM-DD-YYYY` | Date CISA added the entry (confirmed active exploitation) |
| `vendor` / `product` | string | Affected vendor/product |
| `description` | string | Plain description of the flaw (truncated) |
| `action` | string | CISA required action (truncated) |
| `due` | string `MM-DD-YYYY` | CISA federal patch deadline |
| `ransomware_use` | string | Known ransomware campaign use flag |
| `notes` | string | Vendor advisory text/link (truncated) |
| `links` | array<string> | Vendor advisory + NVD URLs |
| `epss` | number (0–1) | EPSS exploitation likelihood; `null` if unscored |
| `epss_percentile` | number (0–1) | EPSS percentile rank; `null` if unscored |

## `ransomware[]`

| Field | Type | Description |
|---|---|---|
| `group` | string | Ransomware group name |
| `sector` | string | Victim sector/activity (may be `Not Found`) |
| `country` | string | Two-letter country code or empty |
| `description` | string | Victim description (truncated) |
| `discovered` | string | Discovery timestamp (UTC, truncated) |
| `links` | array<string> | Ransomware.live site reference (leak-site links deliberately excluded) |

## `circl[]`

| Field | Type | Description |
|---|---|---|
| `id` | string | Advisory ID (e.g. `PYSEC-2024-115` or CVE) |
| `aliases` | array<string> | CVE aliases (may be empty) |
| `severity` | string/array | CVSS data (may be `N/A`) |
| `published` | string | Publication date (truncated) |
| `details` | string | Description (truncated) |
| `epss` / `epss_percentile` | number/null | EPSS enrichment when a CVE alias exists |
| `links` | array<string> | GHSA / huntr / fix commit / CIRCL advisory page |

## `ai_advisories[]`

| Field | Type | Description |
|---|---|---|
| `id` | string | GitHub advisory ID (e.g. `GHSA-cf6m-vc3m-7cgm`) |
| `cve` | string/null | CVE identifier, if assigned |
| `package` / `ecosystem` | string | Affected package and its ecosystem (`pip`, `npm`, `go`) |
| `smb_common` | boolean | The package is one small businesses commonly run directly (ranked first) |
| `severity` | string | GitHub severity (`critical`, `high`, `medium`, `low`) |
| `cvss` | number/null | CVSS score |
| `summary` / `details` | string | Advisory summary and description (truncated) |
| `affected` / `patched` | string/null | Vulnerable version range / first fixed version |
| `published` | string `MM-DD-YYYY` | Advisory publication date |
| `epss` / `epss_percentile` | number/null | EPSS enrichment; `null` if unscored |
| `links` | array<string> | GitHub advisory page |

## History fields (`kev[]`, `circl[]`, `ai_advisories[]`)

| Field | Type | Description |
|---|---|---|
| `first_seen` | string `MM-DD-YYYY` | First daily file containing this vulnerability (today if new). KEV is tracked separately, so a CVE that newly enters KEV is new there. |
| `prev_epss` | number/null | EPSS in the most recent earlier file that contained it |

## `brief_plan`

Selection and severity are deterministic code (`plan_brief` and `rate_severity` in the collector). The drafting step writes prose for exactly these items.

| Field | Type | Description |
|---|---|---|
| `findings` | array | Up to 3, AI tools first, one per product. Each has `section`, `id`, `cve`, `severity` (CRITICAL/HIGH/WATCH), `severity_reason`, `ai`, `selected_because` (`new today` or `EPSS crossed 0.1 since last seen`) and `item` (the full source record). At most one non-AI finding, and only a new CRITICAL KEV entry. |
| `on_the_radar` | array | Up to 3 one-line mentions: new AI items that didn't make the cut, or recent HIGH/CRITICAL ones |
| `ai_advisories_checked` | boolean | The AI advisory source loaded fully today (`sources.ai_advisories.status` is `"ok"`) |
| `quiet_ai_day` | boolean | No AI finding today, and `ai_advisories_checked` is true. A failed check is never a quiet day. |
| `ai_risk_topic` | object/null | Mondays only: `{title, scope}` for a plain-language AI risk with no CVE, rotating weekly |
| `ransomware_pulse` | string | One factual sentence: recent victim count, most-hit sectors and countries |

## `threatfox[]` / `urlhaus[]`

| Field | Type | Description |
|---|---|---|
| `value` | string | The IOC (domain, IP:port, URL) |
| `ioc_type` / `status` | string | Type / online status |
| `malware` / `host` | string | Malware family / host |
| `confidence` | number | ThreatFox confidence level |
| `seen` | string | First-seen timestamp |
| `links` | array<string> | Malpedia / URLhaus entry page |
