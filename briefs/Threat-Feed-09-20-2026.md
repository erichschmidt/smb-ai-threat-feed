---
type: threat-feed-note
title: "Threat Feed — 09-20-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-09-20
updated: 2026-09-20
---

# Threat Feed — 09-20-2026

*Daily briefing for small businesses running AI and automation. 3-minute read: headlines plus the jargon buster at the bottom carry the gist. Plain terms explained inline; a term you don't know yet lives in the [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).*

## How to read the scores

Two numbers matter on each item:

- **EPSS** — a 0–1 estimate of how likely this flaw is to actually be exploited in the next 30 days. Higher = patch first. 0.14 = roughly 14% chance; its **percentile** tells you where that ranks against every known vulnerability (96th percentile = more likely to be exploited than 96% of all flaws).
- **CVSS** — a 0–10 severity score for how bad the flaw is *if* it works. 9.8/10 = critical — typically exploitable remotely with no login.

Rule of thumb: EPSS says "is it coming for you," CVSS says "how bad if it does." Patch the ones high on both.

---

## HIGH — The AI tool that drives your web browser can be hijacked by a malicious plugin

**CVE-2026-94111 · Tencent BrowserSkill · severity not yet rated**

**What broke**
BrowserSkill — a browser-control skill that lets an AI agent operate a real web browser (click, fill forms, read pages) — accepts connections from almost any browser extension. Its local control channel only checks that the caller is a "chrome-extension" with a code name of a certain length, not that it's actually yours (an **origin validation (origin validation — checking that an incoming connection really comes from where it claims to)** failure). A malicious browser extension, or a compromised page that loads one, can connect to the browser the AI is driving and take over the session.

**Why it matters to an SMB running AI tools**
If you run an AI agent that browses on your behalf — submitting forms, checking portals, filling invoices, scraping a vendor site — the tool is effectively a remote-control for a live, logged-in browser. Someone hijacking that control channel gains what the agent's browser session can do: read pages you're authenticated to, trigger actions with your session keys, and watch what the AI is doing. Most of the AI billing tools in the space now ship some kind of browser automation, so this is the class of tool to inventory and lock down.

**What you do Monday** (about 30 minutes)
1. List any browser-automation tool or AI agent your business uses and note its version. BrowserSkill through 0.3.0 is affected — check for an update past that.
2. Confirm the tool only accepts connections from your own browser profile / a loopback address (localhost), and that no random extension can attach.
3. Run browser automation inside a controlled machine where the browser profile holds only the minimum logins the agent needs — not your daily-driver account.

**Sources:**
- CIRCL advisory: https://vulnerability.circl.lu/vuln/CVE-2026-94111

---

## WATCH — Support-chat tool lets an attacker reuse a stolen one-time login code

**CVE-2026-94112 · ezBookkeeping · severity not yet rated**

**What broke**
ezBookkeeping (an open-source bookkeeping app) fails to invalidate **TOTP (TOTP — the rotating 6-digit code from your authenticator app, a time-based one-time password)** codes after they're used. An attacker who steals a login and captures a valid code can reuse that same code during its short validity window to get in again — and again. **Replay (replay — reusing a captured code instead of generating a fresh one)** defeats the whole point of the second factor.

**Why it matters to an SMB running AI tools**
A core defense for small businesses is multi-factor authentication (MFA) — "password plus a code from your phone." Any app that lets a used code be reused quietly weakens that defense for the accounts your team and your automation log into. Bookkeeping is exactly the kind of sensitive, money-touching system where a session compromise hurts.

**What you do Monday** (about 15 minutes)
1. If you run ezBookkeeping, update past 2.0.0 (contains the fix).
2. For any sensitive app, confirm a code works only once — a good health check is to try re-entering an old code after a successful login.
3. Keep MFA on for everything that touches money or client data, and treat "code reuse" as an app-quality red flag when you evaluate vendors.

**Sources:**
- CIRCL advisory: https://vulnerability.circl.lu/vuln/CVE-2026-94112

---

## WATCH — Your ERP's timesheet report lets staff see other people's data

**CVE-2026-94113 · Frappe ERPNext · severity not yet rated**

**What broke**
ERPNext — a popular open-source business software (ERP) that runs invoices, inventory, payroll, and HR — has an information-disclosure flaw in its timesheet endpoints. Authenticated staff can call report functions that fail to enforce what they're allowed to see, pulling timesheet data across the permission boundary.

**Why it matters to an SMB running AI tools**
If your ERP feeds your AI reporting or "ask it for a staff report" tools, a permissions hole in the ERP is a hole in what the AI can surface — and what a low-level user can quietly mine. Payroll and timesheet data are exactly the sensitive records you don't want visible across roles.

**What you do Monday** (about 15–30 minutes)
1. Update ERPNext to 15.121.0+ (or 16.34.0+ for the 16.x line) which fixes it.
2. Review which of your staff and automations can call timesheet/report endpoints; restrict to the people who actually need them.
3. If you route ERP data into AI tools, check that the AI service account has least-privilege access (least privilege — giving an account only the access it needs and no more), not admin.

**Sources:**
- CIRCL advisory: https://vulnerability.circl.lu/vuln/CVE-2026-94113

---

## WATCH — Media metadata library lets a crafted music file run commands on your machine

**CVE-2026-94108 · CVE-2026-94106 · getID3 lib · severity not yet rated**

**What broke**
getID3, a widely used library for reading tags from music and media files (artist, album, cover art), has two flaws disclosed together: an **XML external entity (XXE — XXE (XML External Entity): a trick where a crafted XML document makes a server fetch or reveal files it shouldn't)** issue and an **OS command injection (OS command injection — tricking software into running operating-system commands the attacker chose)** flaw. Both are triggered by malicious metadata hidden inside a media file — a filename or embedded XML that, when read, tells the machine to fetch files or run commands.

**Why it matters to an SMB running AI tools**
Media processing is a quiet corner of automation: audio transcription, podcast-to-notes, cover-art extraction for product feeds. Any pipeline that automatically ingests or tags media files — yours or a vendor's — is a place a crafted file lands. If getID3 is in that chain, an uploaded or synced media file becomes a way to run commands on the server.

**What you do Monday** (about 15 minutes)
1. Note whether any tool you run reads media metadata (transcription, tagging, ingestion). If yes, check the getID3 version — fix landed in 1.9.26.
2. Isolate media ingestion in a sandbox so a malicious file can't reach your main systems, and scan uploads.
3. Treat any media file from an outside source as untrusted until it's been through a safe parser.

**Sources:**
- CIRCL advisory (XXE): https://vulnerability.circl.lu/vuln/CVE-2026-94108
- CIRCL advisory (command injection): https://vulnerability.circl.lu/vuln/CVE-2026-94106

---

## WATCH — No new actively-exploited flaws added to CISA's list today — refresh the ones already due

**CVE-2026-76461 · CVE-2025-39964 · CVE-2026-53266 · CVE-2025-39682 · CVE-2026-87886 · CVE-2026-58704 · CVE-2026-76460 · KEV (Known Exploited Vulnerabilities) catalog**

**What broke**
No *new* vulnerabilities were added to CISA's actively-exploited KEV (KEV — CISA's list of flaws being actively exploited right now; a listing means it's real, not theoretical) catalog today. The currently listed set is carried over from the last several days: the Cisco Secure Email Gateway SQL-injection flaw (highest exploitation odds at the 79.9th percentile), the three Linux kernel flaws, and the Acronis backup, Google Pixel, and Cisco Identity Services Engine items. Quiet on the catalog is good news — but a quiet list doesn't mean your patches are done.

**Why it matters to an SMB running AI tools**
The exploited set includes Linux kernel flaws — relevant on any Linux host running your self-hosted AI models, automation agents, and databases — and the Cisco email gateway that fronts your mail and AI mail assistants. If those patches were deferred over the weekend, today is the day to close them.

**What you do Monday** (about 10–30 minutes per server)
1. On each Linux host run your package update (`sudo apt update && sudo apt upgrade` on Debian/Ubuntu, or the equivalent), then restart for the kernel to take effect.
2. Apply the Cisco Secure Email Gateway update if you run one — mine is the "patch first" choice here (highest exploitation odds).
3. If a host is customer- or AI-facing, schedule the reboot for a low-traffic window and confirm the new kernel is running afterward.

**CISA / vendor metrics:** confirmed actively exploited — Cisco SEG 09-14-2026, Linux trio 09-18-2026, Acronis/Pixel/ISE 09-16-2026 · federal patch deadlines 09-17 to 09-21-2026 · known ransomware campaign use: No.
**Sources:**
- Cisco advisory: https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-esa-inj-2bLVGmhX
- CVE-2025-39964 fix: https://git.kernel.org/stable/c/0f28c4adbc4a97437874c9b669fd7958a8c6d6ce
- CVE-2026-53266 fix: https://git.kernel.org/stable/c/bf84ad7c7a9ede46e31afaa41a1ba06a159e8c87
- CVE-2025-39682 fix: https://git.kernel.org/stable/c/2902c3ebcca52ca845c03182000e8d71d3a5196f

---

## Jargon buster

Every technical term used today, in one plain line each:

- **BrowserSkill:** An AI tool that lets an agent drive a real web browser — click, fill forms, read pages.
- **Origin validation:** Checking that an incoming connection really comes from where it claims to; a failure means a stranger can connect.
- **TOTP (time-based one-time password):** The rotating 6-digit code from your authenticator app — the second factor in MFA.
- **Replay:** Reusing a captured code instead of generating a fresh one, defeating the point of a one-time code.
- **Least privilege:** Giving an account only the access it needs for its job, and no more.
- **XXE (XML External Entity):** A trick where a crafted XML document makes a server fetch or reveal files and internal addresses it should not.
- **OS command injection:** Tricking software into running operating-system commands the attacker chose.
- **KEV (Known Exploited Vulnerabilities):** CISA's list of flaws being actively exploited right now — the "this is real, not theoretical" signal.
- **RCE (Remote Code Execution):** An attacker can run their own code on your machine from anywhere — full control.

## Appendix — raw signals

### Actively exploited (KEV) — ranked by exploitation likelihood (EPSS)

| CVE | Product | Added | Federal patch deadline | Ransom-ware use | EPSS (percentile) | Source |
|---|---|---|---|---|---|---|
| CVE-2026-76461 | Cisco Secure Email Gateway | 09-14-2026 | 09-17-2026 | No | 0.020 (79.9th) | [Cisco sb](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-esa-inj-2bLVGmhX) |
| CVE-2026-76460 | Cisco Identity Services Engine | 09-16-2026 | 09-19-2026 | No | 0.008 (54.5th) | [Cisco sb](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-ISE-ABP-VNSW7Tn5) |
| CVE-2025-39964 | Linux Kernel | 09-18-2026 | 09-21-2026 | No | 0.008 (54.7th) | [kernel fix](https://git.kernel.org/stable/c/0f28c4adbc4a97437874c9b669fd7958a8c6d6ce) |
| CVE-2025-39682 | Linux Kernel | 09-18-2026 | 09-21-2026 | No | 0.012 (66.7th) | [kernel fix](https://git.kernel.org/stable/c/2902c3ebcca52ca845c03182000e8d71d3a5196f) |
| CVE-2026-87886 | Acronis Backup (cPanel/Plesk) | 09-16-2026 | 09-19-2026 | No | 0.003 (17.4th) | [Acronis](https://security-advisory.acronis.com/advisories/SEC-10986) |
| CVE-2026-53266 | Linux Kernel | 09-18-2026 | 09-21-2026 | No | 0.003 (20.2nd) | [kernel fix](https://git.kernel.org/stable/c/bf84ad7c7a9ede46e31afaa41a1ba06a159e8c87) |
| CVE-2026-58704 | Google Pixel (cellular modem) | 09-16-2026 | 09-19-2026 | No | 0.002 (11.2th) | [Android](https://source.android.com/docs/security/bulletin/pixel/2026/2026-09-01) |

### New/disclosed today (CIRCL)
- **Tencent BrowserSkill (CVE-2026-94111)** — authentication bypass in the browser-control channel's origin check; a malicious extension can take over the browser an AI agent drives. [advisory](https://vulnerability.circl.lu/vuln/CVE-2026-94111)
- **ezBookkeeping (CVE-2026-94112)** — one-time login codes not invalidated after use; replay risk. [advisory](https://vulnerability.circl.lu/vuln/CVE-2026-94112)
- **Frappe ERPNext (CVE-2026-94113)** — timesheet endpoints bypass permissions, exposing cross-role data. [advisory](https://vulnerability.circl.lu/vuln/CVE-2026-94113)
- **openEQUELLA (CVE-2026-94109)** — unsandboxed FreeMarker template compiler allows remote code execution by authenticated users. [advisory](https://vulnerability.circl.lu/vuln/CVE-2026-94109)
- **NivoCart (CVE-2026-94104/94105/94107)** — arbitrary file upload, admin password-reset manipulation, and predictable password-reset tokens in a cart platform. [CVE-2026-94104](https://vulnerability.circl.lu/vuln/CVE-2026-94104) · [CVE-2026-94105](https://vulnerability.circl.lu/vuln/CVE-2026-94105) · [CVE-2026-94107](https://vulnerability.circl.lu/vuln/CVE-2026-94107)

Ransomware victim pulse: source feed unavailable this run (ransomware.live query failed) — recheck tomorrow.

### IOC sample (ThreatFox/URLhaus)
- **ClearFake (fake browser-update malware)** domains (block and hunt, don't visit): sddiadtu.gideonconstructioninc.com · 8cm45ib0.us-slimsplitsmethod.com · gideonconstructioninc.com ([Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/js.clearfake))
- **php.shin_webshell (webshell)** domains: rafytylu.workers.dev · cosygazo.workers.dev ([Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/php.shin_webshell))
- **Aisuru (botnet)** C2 IP:port addresses: 46.101.36.181:34567 · 144.126.224.25:8080 ([Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/elf.aisuru))
- Malicious URLs (block-list hits): http://210.208.110.21:59565/i ([URLhaus](https://urlhaus.abuse.ch/url/3919339/)) · http://61.52.45.235:56991/i ([URLhaus](https://urlhaus.abuse.ch/url/3919338/)) · http://182.126.103.176:51069/bin.sh ([URLhaus](https://urlhaus.abuse.ch/url/3919337/)) · http://115.55.7.153:58478/i ([URLhaus](https://urlhaus.abuse.ch/url/3919334/))

---

*Compiled from public sources · 09-20-2026*