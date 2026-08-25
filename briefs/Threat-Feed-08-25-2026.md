---
type: threat-feed-note
title: "Threat Feed - 08-25-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-08-25
source: "cisa-kev, cisa-advisories, circl, epss"
related: "https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md"
---

# Threat Feed — 08-25-2026

> **Reader promise:** 3-minute read. Headlines alone tell you what to do. New term? Check the [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).
> **Lens:** threats that hit AI tools, automation, and small-business money.
> **Sources:** CISA KEV, CISA advisories, CIRCL, FIRST EPSS.

## How to read the scores (30 seconds)
- **CISA KEV:** the federal "known exploited" list — someone is attacking this *right now*. Patch before the federal deadline.
- **EPSS:** 0–1 odds a flaw gets exploited in the wild in the next 30 days. Percentile ranks it against every known flaw. 95th+ percentile = treat as urgent.
- **CVSS:** 0–10 severity. 7+ is serious, but a high CVSS with low EPSS can wait; a KEV listing always beats a high score.

## 1. ON-LENS LEAD — MLflow (CVE-2026-64849): still hot, no change, deadline still running
**Finding:** MLflow server-side request forgery (SSRF). This is still the only actively exploited AI-tooling flaw in the current KEV window.
- KEV added 08-19; federal patch deadline **09-02-2026**.
- EPSS **0.1641 (96.7th percentile)** — very likely to be used in the wild.
**What changed today:** nothing new — but the clock hasn't stopped. If yesterday's answer was "we don't run MLflow," you're done. If you run it: confirm the webhook fix (PR 24258) is installed and it's not on the public internet.
**Do:** keep the 09-02 date on your calendar; re-check the fix is in place.

## 2. CRITICAL — NEW: Oracle HTTP Server / WebLogic Proxy Plug-in (CVE-2026-21962)
**Finding:** improper access control in Oracle HTTP Server and Oracle WebLogic Server Proxy Plug-in. An unauthorized user can create, read, change, or delete data they shouldn't touch — up to complete compromise of the component.
- Added to KEV **08-24-2026**; federal deadline **08-27-2026 (48 hours)**.
- EPSS **0.4323 (98.6th percentile)** — among the most likely-to-be-exploited flaws known right now.
**Why it matters to an SMB:** WebLogic is the app server behind a lot of mid-size ERP/CRM/portal stacks; Oracle HTTP Server fronts web apps. If you run either, this is the "patch now" item of the day.
**Do:** apply Oracle's security patch immediately. If you're not sure whether you run these, ask whoever owns your ERP/CRM before Friday.

## 3. WATCH — NEW CISA advisory: Johnson Controls Simplex Incident Manager (CVE-2026-27875)
**Finding:** the fire-alarm / incident-management system stores user passwords and login tokens in plaintext in memory. A local attacker with low privileges can pull them out and get into the system and things it connects to. CVSS 5.8 (medium); needs local access; no known exploitation yet.
- CISA advisory ICSA-26-232-01 published **08-20-2026**.
**Why it matters to an SMB:** mostly commercial buildings and facilities with a Simplex fire-alarm panel. Not remotely exploitable — don't panic.
**Do:** if you have one, ask your alarm vendor for the patched release; restrict who can sit at a local workstation on that system.

## Still on your plate (KEV window, last 7 days)
| CVE | Product | Added | EPSS (pct) | Fed deadline | Status |
|---|---|---|---|---|---|
| CVE-2026-64849 | MLflow (SSRF) | 08-19 | 0.1641 (96.7%) | 09-02 | open — lead item |
| CVE-2026-21962 | Oracle HTTP Server / WebLogic Proxy | 08-24 | 0.4323 (98.6%) | 08-27 | **patch now** |
| CVE-2026-73570 | Zimbra | 08-21 | 0.0151 (72.4%) | 08-24 | deadline passed — if unpatched, still exposed |
| CVE-2026-72530 | TrueConf Server | 08-20 | 0.0183 (77.2%) | 09-03 | open — patch from vendor if you run it |
| CVE-2026-72529 | TrueConf Server | 08-20 | 0.0155 (73.2%) | 08-23 | deadline passed — if unpatched, still exposed |

## Jargon buster (new terms today)
- **Improper access control:** a software flaw where the product fails to check who is allowed to do what — letting an unauthorized user create, read, change, or delete data they shouldn't touch. (Oracle item.)
- **Oracle WebLogic Server:** a common application server behind ERP/CRM/portal systems — the "engine room" that serves business apps to browsers. (Oracle item.)

*Compiled 08-25-2026 from CISA KEV, CISA advisories, CIRCL, FIRST EPSS.*
