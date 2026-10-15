---
type: threat-feed-note
title: "Threat Feed - 10-15-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-10-15
updated: 2026-10-15
---

# Threat Feed — 10-15-2026

**The 3-minute read for small businesses running AI and automation.** Plain language in the headlines, deeper detail below. Full plain-English glossary: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md)

*AI-drafted from public data and published automatically. No one reviews each brief before it goes out. Check the linked source before you act.*

## How to read the scores

- **CISA KEV:** on this list means attackers are using the flaw right now.
- **EPSS:** a 0–1 estimate of how likely a flaw is to be exploited in the next 30 days; the percentile ranks it against all known flaws.
- **Severity:** CRITICAL, HIGH or WATCH, set by a fixed published rubric, not by tone.

---

**No new security advisories for common AI tools today.**

## 1. CRITICAL — Cisco Secure Email Gateway servers are under active attack with no login needed — patch now

**CVE-2026-76519 — Cisco Secure Email Gateway** · CISA confirmed active exploitation on 10-14-2026 · federal patch deadline 10-17-2026 · known ransomware use: Unknown · in CISA KEV · no login needed

**What broke.** Cisco Secure Email Gateway (an email gateway — the system that scans incoming and outgoing mail before it reaches mailboxes) contains a relative path traversal flaw, a trick where an attacker uses up-one-directory markers in a file path to place files where they shouldn't be able to. An unauthenticated (no login) remote attacker can write arbitrary files on the underlying operating system, and CISA added the flaw to its Known Exploited Vulnerabilities catalog on 10-14-2026, meaning it is being used in real attacks.

**Why it matters to an SMB running AI tools.** General IT hygiene — no specific AI angle. The gateway that filters your email often feeds the same mailboxes that AI assistants and automation read, so an attacker who can plant files on it is standing inside your communication chain. Treat this as a same-day patch item, not a routine monthly update.

**What you do Monday** (about 15 minutes):
1. Ask whoever manages your email: "Do we run Cisco Secure Email Gateway, and has CVE-2026-76519 been patched per Cisco's security advisory?"
2. If you run it, apply the fixed software listed in Cisco's advisory and confirm the appliance version now matches a fixed release.
3. If you cannot patch today, ask Cisco support which interim mitigations apply to your release and apply them the same day.

**Sources:** [Cisco security advisory](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-esa-afw-zqYJkjxp) · [NVD entry for CVE-2026-76519](https://nvd.nist.gov/vuln/detail/CVE-2026-76519)

---

## Jargon buster

- **Email gateway:** The system that scans business email before it reaches anyone's mailbox.
- **Path traversal:** Using up-one-directory markers in a file path to reach or write files you shouldn't.
- **Unauthenticated attacker:** Someone with no username or password, attacking from anywhere on the internet.

## Appendix

### CISA KEV — actively exploited, ranked by EPSS

| CVE | Product | CISA added | Federal deadline | EPSS | Ransomware use | Source |
|---|---|---|---|---|---|---|
| CVE-2026-104935 | Ivanti Connect Secure | 10-13-2026 | 10-16-2026 | 0.2598 | Unknown | [Ivanti advisory](https://forums.ivanti.com/s/article/Security-Advisory-Ivanti-Connect-Secure-CVE-2026-104935) |
| CVE-2026-105134 | Ahsay AhsayCBS | 10-14-2026 | 10-17-2026 | 0.0184 | Unknown | [Ahsay announcement](https://www.ahsay.com/en/company/announcements/patch-cve-105133-105134-update) |
| CVE-2026-96951 | Microsoft Windows | 10-13-2026 | 10-16-2026 | 0.0151 | Unknown | [Microsoft update guide](https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-96951) |
| CVE-2026-105133 | Ahsay AhsayCBS | 10-14-2026 | 10-17-2026 | 0.0038 | Unknown | [Ahsay announcement](https://www.ahsay.com/en/company/announcements/patch-cve-105133-105134-update) |
| CVE-2026-76519 | Cisco Secure Email Gateway | 10-14-2026 | 10-17-2026 | N/A | Unknown | [Cisco security advisory](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-esa-afw-zqYJkjxp) |

**Ransomware pulse:** 10 recent victim claims; most-hit sectors: Professional Services (3), Technology (1), Education (1); countries: US (3), NL (1), SG (1). · Source: [Ransomware.live](https://www.ransomware.live)

**Full data, including malware IOCs:** [latest.json](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/latest.json)

---

*Compiled from public sources · 10-15-2026*
