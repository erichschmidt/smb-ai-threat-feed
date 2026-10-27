---
type: threat-feed-note
title: "Threat Feed - 10-27-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-10-27
updated: 2026-10-27
---

# Threat Feed — 10-27-2026

**The 3-minute read for small businesses running AI and automation.** Plain language in the headlines, deeper detail below. Full plain-English glossary: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md)

*AI-drafted from public data and published automatically. No one reviews each brief before it goes out. Check the linked source before you act.*

## How to read the scores

- **CISA KEV:** on this list means attackers are using the flaw right now.
- **EPSS:** a 0–1 estimate of how likely a flaw is to be exploited in the next 30 days; the percentile ranks it against all known flaws.
- **Severity:** CRITICAL, HIGH or WATCH, set by a fixed published rubric, not by tone.

---

**No new security advisories for common AI tools today.**

## 1. CRITICAL — Attackers are exploiting a PHP flaw that lets strangers run code on web servers — patch immediately

**CVE-2026-109619 — PHP** · EPSS 1.0 (99.99th percentile — more likely to be exploited than 99.99% of known flaws) · CISA confirmed active exploitation on 10-26-2026 · federal patch deadline 10-29-2026 · known ransomware use: Unknown · in CISA KEV · no login needed

**What broke.** PHP (the web-scripting language behind many websites and business portals) holds internal request state (leftover working data from earlier web requests) and a flaw lets a crafted request reuse stale state it should not touch. That mistake lets an attacker run their own code on the server with no login, which CISA confirms is happening now in the wild.

**Why it matters to an SMB running AI tools.** General IT hygiene — no specific AI angle. PHP is common in small-business web stacks — CMS sites, form handlers, customer portals, and the login pages in front of automation dashboards — so a takeover here exposes the same servers that can hold AI service keys and integration credentials.

**What you do Monday** (about 20 minutes):
1. Ask your web host or IT person which of your servers run PHP and whether the current patch for CVE-2026-109619 is applied; if the answer is "I don't know," assume any unchecked PHP site is exposed until verified.
2. Have them upgrade PHP to the vendor's patched release on any internet-facing server, and reboot/reload the web service so the fix actually takes effect.
3. Say this to them: "CISA added CVE-2026-109619, an unauthenticated remote-code-execution flaw in PHP, to its actively-exploited list on 10-26-2026 with a 10-29-2026 deadline — please confirm each server running PHP is patched and show me the version output."

**Sources:** [CISA alert](https://www.cisa.gov/news-events/alerts/2026/10/21/critical-vulnerabilities-php-require-immediate-patching) · [NVD record](https://nvd.nist.gov/vuln/detail/CVE-2026-109619) · [PHP project](https://www.php.net/)

---

## Jargon buster

- **PHP:** The web-scripting language behind many websites, forms, and business portals, including common content systems.
- **Stale request state:** Leftover internal data a server keeps from earlier requests; reusing it by mistake can let outsiders act through it.
- **Remote code execution:** An attacker runs their own program on your server from anywhere — full control of that machine.

## Appendix

### CISA KEV — actively exploited, ranked by EPSS

| CVE | Product | CISA added | Federal deadline | EPSS | Ransomware use | Source |
|---|---|---|---|---|---|---|
| CVE-2026-109619 | PHP Group PHP | 10-26-2026 | 10-29-2026 | 1.0 | Unknown | [CISA](https://www.cisa.gov/news-events/alerts/2026/10/21/critical-vulnerabilities-php-require-immediate-patching) |
| CVE-2026-109618 | PHP Group PHP | 10-26-2026 | 10-29-2026 | 0.9998 | Unknown | [CISA](https://www.cisa.gov/news-events/alerts/2026/10/21/critical-vulnerabilities-php-require-immediate-patching) |
| CVE-2026-110447 | Collabora Online – Built-in CODE Server | 10-23-2026 | 10-26-2026 | 0.1233 | Unknown | [Nextcloud](https://help.nextcloud.com/t/to-collabora-built-in-user-update-asap/250516) |
| CVE-2026-114625 | Arista VeloCloud Orchestrator | 10-23-2026 | 10-26-2026 | 0.0103 | Unknown | [Arista](https://www.arista.com/en/support/advisories-notices/security-advisory/24838-security-advisory-0199) |

**Ransomware pulse:** 10 recent victim claims; most-hit sectors: Technology (3), Manufacturing (2), Healthcare (2); countries: IT (2), PH (1), SG (1). · Source: [Ransomware.live](https://www.ransomware.live)

**Full data, including malware IOCs:** [latest.json](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/latest.json)

---

*Compiled from public sources · 10-27-2026*
