---
type: threat-feed-note
title: "Threat Feed - 10-18-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-10-18
updated: 2026-10-18
---

# Threat Feed — 10-18-2026

**The 3-minute read for small businesses running AI and automation.** Plain language in the headlines, deeper detail below. Full plain-English glossary: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md)

*AI-drafted from public data and published automatically. No one reviews each brief before it goes out. Check the linked source before you act.*

## How to read the scores

- **CISA KEV:** on this list means attackers are using the flaw right now.
- **EPSS:** a 0–1 estimate of how likely a flaw is to be exploited in the next 30 days; the percentile ranks it against all known flaws.
- **Severity:** CRITICAL, HIGH or WATCH, set by a fixed published rubric, not by tone.

---

## 1. WATCH — Shared chats in self-hosted Open WebUI can run hidden code in a coworker's browser

**CVE-2026-109291 — Open WebUI** · EPSS 0.0028 (19th percentile — more likely to be exploited than 19% of known flaws) · not in KEV · low EPSS (0.0028)

**What broke.** Open WebUI versions from 0.6.33 before 0.11.4 let a signed-in user plant browser code inside the citation data of a chat — a javascript: link, which is text a browser runs as instructions instead of treating it as an address. A coworker who opens the crafted shared chat then runs that code inside their own logged-in session, a flaw called cross-site scripting (XSS).

**Why it matters to an SMB running AI tools.** Teams running self-hosted Open WebUI usually share chat links freely, so one malicious or compromised account can hijack a colleague's session and act with that person's access, including whatever the AI chat interface can reach. It is a prompt to limit who holds accounts and who may share chats, not just to patch.

**What you do Monday** (about 15 minutes):
1. Upgrade Open WebUI to 0.11.4 or later.
2. Review the account list and turn off public chat sharing for users who do not need it.
3. If someone else maintains the server, say: "Please upgrade our Open WebUI instance to version 0.11.4 or later to fix CVE-2026-109291."

**Sources:** [CIRCL vulnerability record](https://vulnerability.circl.lu/vuln/CVE-2026-109291)

---

## 2. WATCH — AI model connections disabled in self-hosted Open WebUI can stay reachable to signed-in users

**CVE-2026-109296 — Open WebUI** · EPSS 0.0027 (19th percentile — more likely to be exploited than 19% of known flaws) · not in KEV · low EPSS (0.0027)

**What broke.** Open WebUI versions before 0.11.4 do not fully block access to model provider backends — the saved connections to outside AI services — that an admin has disabled. A signed-in user can name the backend's position number directly, in a web address or a request parameter, and still reach it.

**Why it matters to an SMB running AI tools.** A connection you switched off because it was unapproved, retired, or too expensive may still answer prompts, quietly sending business questions to a provider you thought was out of the loop and possibly running up charges. The same gap defeats guardrails, such as routing sensitive questions only through an approved model.

**What you do Monday** (about 10 minutes):
1. Upgrade Open WebUI to 0.11.4 or later.
2. List the configured model connections and confirm disabled ones are unreachable by any signed-in user.
3. Check provider billing and usage logs for traffic you did not expect.

**Sources:** [CIRCL vulnerability record](https://vulnerability.circl.lu/vuln/CVE-2026-109296)

---

## Jargon buster

- **XSS (cross-site scripting):** A trap that makes your own logged-in browser run an attacker's code.
- **Backend:** A behind-the-scenes server service that does the work, like a saved AI model connection.
- **Authorization bypass:** A logged-in user reaches actions they were never granted permission to use.
- **Self-hosted server:** Software running on your own machines instead of the vendor's cloud.

## Appendix

### CISA KEV — actively exploited, ranked by EPSS

| CVE | Product | CISA added | Federal deadline | EPSS | Ransomware use | Source |
|---|---|---|---|---|---|---|
| CVE-2026-104935 | Ivanti Connect Secure | 10-13-2026 | 10-16-2026 | 0.2598 | Unknown | [Ivanti advisory](https://forums.ivanti.com/s/article/Security-Advisory-Ivanti-Connect-Secure-CVE-2026-104935) |
| CVE-2026-21589 | Atlassian Multiple Products | 10-15-2026 | 10-18-2026 | 0.1271 | Unknown | [Atlassian security page](https://confluence.atlassian.com/security/cve-2026-21589-arbitrary-file-access-vulnerability-impacts-multiple-products-1870495748.html?ref=labs.watchtowr.com) |
| CVE-2026-105134 | Ahsay AhsayCBS | 10-14-2026 | 10-17-2026 | 0.0478 | Unknown | [Ahsay announcement](https://www.ahsay.com/en/company/announcements/patch-cve-105133-105134-update) |
| CVE-2026-76519 | Cisco Secure Email Gateway | 10-14-2026 | 10-17-2026 | 0.0157 | Unknown | [Cisco security advisory](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-esa-afw-zqYJkjxp) |
| CVE-2026-96951 | Microsoft Windows | 10-13-2026 | 10-16-2026 | 0.0151 | Unknown | [Microsoft update guide](https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-96951) |

**Ransomware pulse:** 10 recent victim claims; most-hit sectors: Manufacturing (3), Professional Services (2), Energy & Utilities (1); countries: US (8), NL (1). · Source: [Ransomware.live](https://www.ransomware.live)

**Full data, including malware IOCs:** [latest.json](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/latest.json)

---

*Compiled from public sources · 10-18-2026*
