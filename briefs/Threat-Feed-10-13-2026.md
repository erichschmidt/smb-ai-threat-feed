---
type: threat-feed-note
title: "Threat Feed - 10-13-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-10-13
updated: 2026-10-13
---

# Threat Feed — 10-13-2026

**The 3-minute read for small businesses running AI and automation.** Plain language in the headlines, deeper detail below. Full plain-English glossary: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md)

*AI-drafted from public data and published automatically. No one reviews each brief before it goes out. Check the linked source before you act.*

## How to read the scores

- **CISA KEV:** on this list means attackers are using the flaw right now.
- **EPSS:** a 0–1 estimate of how likely a flaw is to be exploited in the next 30 days; the percentile ranks it against all known flaws.
- **Severity:** CRITICAL, HIGH or WATCH, set by a fixed published rubric, not by tone.

---

**No new security advisories for common AI tools today.**

## 1. CRITICAL — Ivanti Connect Secure VPN gateways can be taken over without a login — apply the vendor fix immediately

**CVE-2026-104935 — Ivanti Connect Secure** · CISA confirmed active exploitation on 10-13-2026 · federal patch deadline 10-16-2026 · known ransomware use: Unknown · in CISA KEV · no login needed

**What broke.** Ivanti Connect Secure, a VPN gateway appliance, contains an authentication bypass by spoofing (a flaw that lets someone get past a login check they should have had to pass by faking identity signals). A remote attacker with no credentials can execute arbitrary commands on the device, and CISA added the flaw to its Known Exploited Vulnerabilities catalog on 10-13-2026, meaning it is being used in real attacks.

**Why it matters to an SMB running AI tools.** General IT hygiene — no specific AI angle. A VPN gateway is the front door to the whole office network, so a takeover there exposes every system and file behind it, including any self-hosted tools. Treat this as a same-day patch item, not a routine monthly update.

**What you do Monday** (about 20 minutes):
1. Ask whoever manages your VPN: "Do we run Ivanti Connect Secure, and has CVE-2026-104935 been patched per the Ivanti security advisory?"
2. If it runs in front of your network, apply the vendor's mitigations from the advisory immediately and check for signs of compromise.
3. Confirm the fix landed by checking the appliance version against the advisory's fixed-version list.

**Sources:** [Ivanti security advisory](https://forums.ivanti.com/s/article/Security-Advisory-Ivanti-Connect-Secure-CVE-2026-104935) · [NVD entry for CVE-2026-104935](https://nvd.nist.gov/vuln/detail/CVE-2026-104935)

---

## Jargon buster

- **Authentication bypass:** A flaw that lets someone get past a login or permission check.
- **Spoofing:** Faking identity signals so a system trusts an attacker as if they were legitimate.
- **VPN gateway:** The encrypted tunnel remote workers use to reach the office network.

## Appendix

### CISA KEV — actively exploited, ranked by EPSS

| CVE | Product | CISA added | Federal deadline | EPSS | Ransomware use | Source |
|---|---|---|---|---|---|---|
| CVE-2015-3306 | ProFTPD | 10-08-2026 | 10-11-2026 | 0.995 | Unknown | [Debian advisory](https://lists.debian.org/debian-security-announce/2015/msg00154.html) |
| CVE-2015-5477 | ISC BIND | 10-08-2026 | 10-11-2026 | 0.9941 | Unknown | [Red Hat errata](https://access.redhat.com/errata/RHSA-2015:1513.html) |
| CVE-2016-3081 | Apache Struts | 10-08-2026 | 10-11-2026 | 0.9605 | Unknown | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2016-3081) |
| CVE-2021-3199 | ONLYOFFICE Docs | 10-08-2026 | 10-11-2026 | 0.1935 | Unknown | [ONLYOFFICE changelog](https://github.com/ONLYOFFICE/DocumentServer/blob/903fe5ab7a275bd69c3c3346af2d21cf87ebeabf/CHANGELOG.md#563) |
| CVE-2023-22894 | Strapi | 10-08-2026 | 10-11-2026 | 0.0361 | Unknown | [Strapi releases](https://github.com/strapi/strapi/releases) |

**Ransomware pulse:** 10 recent victim claims; most-hit sectors: Professional Services (4), Healthcare (2), Manufacturing (1); countries: SE (9), DE (1). · Source: [Ransomware.live](https://www.ransomware.live)

**Full data, including malware IOCs:** [latest.json](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/latest.json)

---

*Compiled from public sources · 10-13-2026*
