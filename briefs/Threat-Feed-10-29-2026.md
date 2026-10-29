---
type: threat-feed-note
title: "Threat Feed - 10-29-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-10-29
updated: 2026-10-29
---

# Threat Feed — 10-29-2026

**The 3-minute read for small businesses running AI and automation.** Plain language in the headlines, deeper detail below. Full plain-English glossary: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md)

*AI-drafted from public data and published automatically. No one reviews each brief before it goes out. Check the linked source before you act.*

## How to read the scores

- **CISA KEV:** on this list means attackers are using the flaw right now.
- **EPSS:** a 0–1 estimate of how likely a flaw is to be exploited in the next 30 days; the percentile ranks it against all known flaws.
- **Severity:** CRITICAL, HIGH or WATCH, set by a fixed published rubric, not by tone.

---

## 1. WATCH — Self-hosted vLLM servers that accept image files can route them through a vulnerable document converter

**CVE-2026-115915 (GHSA-h3rc-j82p-2c3h) — vLLM** · CVSS 8.1/10 = high · EPSS 0.0063 (50th percentile — more likely to be exploited than 50% of known flaws) · affected < 0.32.0 · fixed in 0.32.0 · not in KEV · low EPSS (0.0063)

**What broke.** vLLM passes caller-supplied image bytes through a format detector without restricting which formats are accepted, so a request labeled as a PNG can carry a different file type underneath. A crafted EPS file (an image built from document instructions) can then reach the server's Ghostscript converter (a program that turns documents into images), where a known Ghostscript flaw (CVE-2024-29510) can crash the service or, on an affected host, run attacker code.

**Why it matters to an SMB running AI tools.** A small business serving images or scanned documents through a self-hosted vLLM endpoint is decoding those files on the server itself, before the model ever sees them. How bad it gets depends on the host's setup, so the upgrade matters even when the realistic worst case is only an outage.

**What you do Monday** (about 15 minutes):
1. Upgrade vllm to 0.32.0 or later (`pip install -U "vllm>=0.32.0"`).
2. Update Ghostscript on the same host to a build that fixes CVE-2024-29510, or block EPS input if your image pipeline has no reason to convert documents.
3. If you do not patch it yourself, say: "Please upgrade our vLLM server to 0.32.0 or later and check its Ghostscript install against CVE-2024-29510."

**Sources:** [GitHub advisory GHSA-h3rc-j82p-2c3h](https://github.com/advisories/GHSA-h3rc-j82p-2c3h)

---

## Also on the radar

- **mlflow** — Unauthenticated MLflow servers let remote callers run their own code. (HIGH, GHSA-26p8-2jq9-3vq9) · [source](https://github.com/advisories/GHSA-26p8-2jq9-3vq9)
- **vllm** — A crafted request can push attacker-built data into vLLM's code-loading step. (WATCH, GHSA-6757-hggm-hp2w) · [source](https://github.com/advisories/GHSA-6757-hggm-hp2w)
- **vllm** — One ordinary image request can crash vLLM servers running OCR models. (WATCH, GHSA-gq5q-89c7-vhvx) · [source](https://github.com/advisories/GHSA-gq5q-89c7-vhvx)

## Jargon buster

- **EPS:** An image file built from document instructions, not just pixels.
- **Ghostscript:** A free program servers use to convert documents into images.

## Appendix

### CISA KEV — actively exploited, ranked by EPSS

| CVE | Product | CISA added | Federal deadline | EPSS | Ransomware use | Source |
|---|---|---|---|---|---|---|
| CVE-2026-109618 | PHP Group PHP | 10-26-2026 | 10-29-2026 | 1.0 | Unknown | [CISA alert](https://www.cisa.gov/news-events/alerts/2026-10-21/critical-vulnerabilities-php-require-immediate-patching) |
| CVE-2026-109619 | PHP Group PHP | 10-26-2026 | 10-29-2026 | 1.0 | Unknown | [CISA alert](https://www.cisa.gov/news-events/alerts/2026-10-21/critical-vulnerabilities-php-require-immediate-patching) |
| CVE-2026-111497 | Google Brotli | 10-27-2026 | 11-10-2026 | 0.8799 | Unknown | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-111497) |
| CVE-2026-48356 | Adobe Commerce and Magento | 10-27-2026 | 11-10-2026 | 0.5908 | Unknown | [Adobe APSB26-73](https://www.adobe.com/trust/security/products/commerce/apsb26-73.html) |
| CVE-2026-46300 | Linux Kernel | 10-28-2026 | 10-31-2026 | 0.1019 | Unknown | [Kernel commit](https://git.kernel.org/stable/c/3599e6b3cc1ada96883d496a50a210d3afbb6987) |

**Ransomware pulse:** 10 recent victim claims; most-hit sectors: Professional Services (2), Healthcare (1), Financial Services (1); countries: US (4), MX (1), SG (1). · Source: [Ransomware.live](https://www.ransomware.live)

**Full data, including malware IOCs:** [latest.json](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/latest.json)

---

*Compiled from public sources · 10-29-2026*
