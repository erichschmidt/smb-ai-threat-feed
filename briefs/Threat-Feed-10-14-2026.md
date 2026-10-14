---
type: threat-feed-note
title: "Threat Feed - 10-14-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-10-14
updated: 2026-10-14
---

# Threat Feed — 10-14-2026

**The 3-minute read for small businesses running AI and automation.** Plain language in the headlines, deeper detail below. Full plain-English glossary: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md)

*AI-drafted from public data and published automatically. No one reviews each brief before it goes out. Check the linked source before you act.*

## How to read the scores

- **CISA KEV:** on this list means attackers are using the flaw right now.
- **EPSS:** a 0–1 estimate of how likely a flaw is to be exploited in the next 30 days; the percentile ranks it against all known flaws.
- **Severity:** CRITICAL, HIGH or WATCH, set by a fixed published rubric, not by tone.

---

**No new security advisories for common AI tools today.**

Nothing new landed in the AI tool watchlist in the last day, and no other item met the bar for a numbered finding. That is not an all-clear: the actively exploited list below still needs patching, and the ransomware picture is busy. If your business runs self-hosted AI builders like Langflow or Flowise, this is a good quiet window to confirm they are on the latest fixed versions.

## Appendix

### CISA KEV — actively exploited, ranked by EPSS

| CVE | Product | CISA added | Federal deadline | EPSS | Ransomware use | Source |
|---|---|---|---|---|---|---|
| CVE-2015-3306 | ProFTPD | 10-08-2026 | 10-11-2026 | 0.995 | Unknown | [Debian advisory](https://lists.debian.org/debian-security-announce/2015/msg00154.html) |
| CVE-2015-5477 | ISC BIND | 10-08-2026 | 10-11-2026 | 0.9941 | Unknown | [Red Hat errata](https://access.redhat.com/errata/RHSA-2015:1513.html) |
| CVE-2016-3081 | Apache Struts | 10-08-2026 | 10-11-2026 | 0.9605 | Unknown | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2016-3081) |
| CVE-2021-3199 | ONLYOFFICE Docs | 10-08-2026 | 10-11-2026 | 0.1935 | Unknown | [ONLYOFFICE changelog](https://github.com/ONLYOFFICE/DocumentServer/blob/903fe5ab7a275bd69c3c3346af2d21cf87ebeabf/CHANGELOG.md#563) |
| CVE-2023-22894 | Strapi | 10-08-2026 | 10-11-2026 | 0.0361 | Unknown | [Strapi releases](https://github.com/strapi/strapi/releases) |

**Ransomware pulse:** 10 recent victim claims; most-hit sectors: Manufacturing (2), Healthcare (2), Professional Services (2); countries: SE (6), US (1), BR (1). · Source: [Ransomware.live](https://www.ransomware.live)

**Full data, including malware IOCs:** [latest.json](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/latest.json)

---

*Compiled from public sources · 10-14-2026*
