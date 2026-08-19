# Schema — smb-ai-threat-feed structured data

Version: 1.0 · Each daily file lives at `data/YYYY-MM-DD.json` and is mirrored to `latest.json`.

## Top level

| Field | Type | Description |
|---|---|---|
| `generated` | string (ISO-8601) | UTC timestamp when the packet was collected |
| `date` | string `YYYY-MM-DD` | Feed date |
| `sources` | object | Per-source status and item count (`status`: `ok` or error string; `count`: int) |
| `kev` | array | CISA Known Exploited Vulnerabilities added in the last 7 days |
| `ransomware` | array | Recent Ransomware.live victim disclosures |
| `circl` | array | Recent CIRCL Vulnerability Lookup entries |
| `threatfox` | array | Recent ThreatFox IOCs |
| `urlhaus` | array | Recent URLhaus URLs |

## `kev[]`

| Field | Type | Description |
|---|---|---|
| `cve` | string | CVE identifier (e.g. `CVE-2026-33824`) |
| `added` | string `YYYY-MM-DD` | Date CISA added the entry (confirmed active exploitation) |
| `vendor` / `product` | string | Affected vendor/product |
| `description` | string | Plain description of the flaw (truncated) |
| `action` | string | CISA required action (truncated) |
| `due` | string `YYYY-MM-DD` | CISA federal patch deadline |
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

## `threatfox[]` / `urlhaus[]`

| Field | Type | Description |
|---|---|---|
| `value` | string | The IOC (domain, IP:port, URL) |
| `ioc_type` / `status` | string | Type / online status |
| `malware` / `host` | string | Malware family / host |
| `confidence` | number | ThreatFox confidence level |
| `seen` | string | First-seen timestamp |
| `links` | array<string> | Malpedia / URLhaus entry page |
