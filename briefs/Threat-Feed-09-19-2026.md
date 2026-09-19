---
type: threat-feed-note
title: "Threat Feed — 09-19-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-09-19
updated: 2026-09-19
---

# Threat Feed — 09-19-2026

*Daily briefing for small businesses running AI and automation. 3-minute read: headlines plus the jargon buster at the bottom carry the gist. Plain terms explained inline; a term you don't know yet lives in the [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).*

## How to read the scores

Two numbers matter on each item:

- **EPSS** — a 0–1 estimate of how likely this flaw is to actually be exploited in the next 30 days. Higher = patch first. 0.14 = roughly 14% chance; its **percentile** tells you where that ranks against every known vulnerability (96th percentile = more likely to be exploited than 96% of all flaws).
- **CVSS** — a 0–10 severity score for how bad the flaw is *if* it works. 9.8/10 = critical — typically exploitable remotely with no login.

Rule of thumb: EPSS says "is it coming for you," CVSS says "how bad if it does." Patch the ones high on both.

---

## HIGH — Your "chat with your data" tool can be tricked into leaking or rewriting your whole database

**PYSEC-2024-115 / CVE-2024-8309 · LangChain GraphCypherQAChain · CVSS 9.8/10 · EPSS 0.137 (96.3rd percentile)**

**What broke**
LangChain's GraphCypherQAChain — a helper that turns a typed question into a database query so your chatbot can answer from your records — allows **SQL injection (SQL injection — typing malicious database commands into an input, tricking the app into running unauthorized queries)** through **prompt injection (prompt injection — hiding instructions inside the data an AI reads, so it follows the attacker's orders instead of yours)**. An attacker who can get any text into the AI's context can run database commands the app never meant to allow: read data it shouldn't, change or delete records, or knock the service offline. CVSS 9.8/10 = critical — remotely exploitable with no login. It's on the 96th-percentile EPSS ranking, meaning it's more likely to be exploited than most known flaws.

**Why it matters to an SMB running AI tools**
If you built a "chat with your sales CRM / support tickets / order history" bot on LangChain — or your developer did — the graph-database step in that chain may accept attacker-controlled queries. The chat input stops being a question interface and starts being an unlocked door to whatever that database holds. Even a customer support bot that reads a public FAQ can still pass hostile text straight into the query builder.

Attacker view (conceptual): attacker finds your AI's data-knowledge endpoint → feeds a crafted string meant to look like a normal question → the chain converts it into an unauthorized database command → data is read or altered, logged as a normal conversation. Defender evidence: unexpected database queries, especially writes, from your AI service's service account (service account — a non-human login software uses to talk to other software).

**What you do Monday** (about 30–60 minutes)
1. Ask whoever maintains the bot: what LangChain version is deployed? Fix is in langchain commit `c2a3021` and patched releases after 0.2.5 — upgrade.
2. If you log in and find you run the affected version today, restrict that database account to read-only and the minimum tables the bot needs (least privilege — least privilege — giving an account only the access it needs for its job, and no more).
3. Get an example SQL-injection test string from a trusted advisory and confirm the fix blocks it before you consider it done.

**CISA / vendor metrics:** not in CISA KEV (no confirmed CISA active-exploitation listing — fix this proactively rather than waiting to be a victim).
**Sources:**
- Advisory (huntr): https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5
- Fix commit: https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255
- GitHub advisory (GHSA-45pg-36p6-83v9): https://github.com/advisories/GHSA-45pg-36p6-83v9

---

## HIGH — Fake AI model files can slip past the scanner meant to catch them

**PYSEC-2025-19 / CVE-2025-1889 · picklescan · CVSS 9.8/10 · EPSS 0.004 (32.7th percentile)**

**What broke**
The `picklescan` tool — a scanner designed to catch dangerous Python **pickle (pickle — a Python file format for saving objects; loading one can run code, so treat a random model file like an unknown program)** files hidden inside AI model downloads — only checked files with standard model extensions. Rename a malicious pickle to a less common suffix and the scan sails past it. An attacker can then ship a "model" that isn't a model at all: loading it runs their code on your machine. CVSS 9.8/10 = critical.

**Why it matters to an SMB running AI tools**
Any business that pulls open-source AI models for tasks like document analysis, image generation, or a local chatbot is loading third-party model files. This is exactly the attack that turns a downloaded "model" into a foothold on your server — which is why the scanner existed in the first place. If your tooling trusts picklescan to validate downloaded models, it is trusting a filter with a hole.

**What you do Monday** (about 15–30 minutes)
1. Update picklescan to 0.0.22 or later (the fix) wherever it's installed.
2. Prefer the **safetensors (safetensors — a model-weight format that stores data without running code on load)** format for untrusted models over pickle / raw `torch.load`.
3. Only load models from the publisher's official page, never from random links or paste-sites.

**Sources:**
- Sonatype advisory: https://sites.google.com/sonatype.com/vulnerabilities/cve-2025-1889
- GitHub advisory (GHSA-769v-p64c-89pr): https://github.com/advisories/GHSA-769v-p64c-89pr

---

## WATCH — Automation server leaks the AI-assistant login keys into plaintext logs

**CVE-2026-93982 · OpenPanel · severity not yet rated**

**What broke**
OpenPanel — a server-management panel some teams run to stand up and manage apps — writes **MCP (MCP / Model Context Protocol — MCP (Model Context Protocol): the plug-in standard that lets an AI assistant use extra tools and services)** authentication tokens from URL addresses straight into ordinary application logs without hiding (redacting) them. Plaintext logs (plaintext — stored so anyone can read it, with no encryption) are exactly where an attacker or an insider looks first.

**Why it matters to an SMB running AI tools**
If your automation panel connects to AI or database services via MCP and passes the token in the URL, that token now sits in your logs. Anyone who can open the log file — support staff, a monitoring service, an attacker who got a foothold — has the key to that AI service, no password needed.

**What you do Monday** (about 30 minutes)
1. Confirm which OpenPanel version you run; move to a build past the vulnerable commit `bad75bdd`.
2. Rotate (replace) the authentication tokens that were ever passed in a URL — treat them as compromised.
3. Check whether your log retention pipeline exposes these files; restrict read access to admin-only.

**Sources:**
- CIRCL advisory: https://vulnerability.circl.lu/vuln/CVE-2026-93982

---

## HIGH — Your email gateway has a hole that lets an outsider take it over completely

**CVE-2026-76461 · Cisco Secure Email Gateway (AsyncOS) · CVSS severity unrated on CISA record · EPSS 0.020 (79.9th percentile)**

**What broke**
Cisco's Secure Email Gateway — the appliance that inspects your inbound and outbound mail — has a **SQL injection** flaw in how it handles addresses. An unauthenticated, remote attacker (no login, from anywhere) can use it to execute commands as **root (root — the highest access level on a Linux/Unix system; root means the attacker owns the machine)**. Because it's not known to be used in ransomware campaigns (CISA flag: Unknown), but it **is** confirmed actively exploited.

**Why it matters to an SMB running AI tools**
Your email gateway is the front door for every message your business sends and receives — including the mailboxes your AI assistants summarize and the automation that reads inbound orders or support tickets. Full takeover of that appliance means the attacker sees your mail and can redirect, plant, or delete it. It has the highest exploitation-likelihood rank (79.9th percentile) of today's actively-exploited items.

**What you do Monday** (about 30–60 minutes)
1. Apply the Cisco update for Secure Email Gateway and/or AsyncOS as soon as you can — this one is confirmed exploited.
2. Check Cisco's advisory (source below) for the exact versions fixed and follow the upgrade path for your appliance.
3. While it updates, enable MFA (MFA — multi-factor authentication: a second proof of identity beyond a password) on any web admin access to the box.

**CISA / vendor metrics:** confirmed actively exploited as of 09-14-2026 · federal deadline to patch was 09-17-2026 (this one is urgent) · known ransomware campaign use: No.
**Sources:**
- Cisco advisory: https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-esa-inj-2bLVGmhX
- NVD: https://nvd.nist.gov/vuln/detail/CVE-2026-76461

---

## WATCH — Linux kernel is under active attack: three flaws just added to the exploited list

**CVE-2025-39964 · CVE-2026-53266 · CVE-2025-39682 · Linux Kernel · added 09-18-2026**

**What broke**
CISA confirmed three Linux kernel flaws are being actively exploited, all added to the KEV (KEV — CISA's list of vulnerabilities being actively exploited right now; a listing means it's real, not theoretical) catalog on 09-18-2026:
- **CVE-2025-39964** — a **race condition (race condition — two parts of a program writing the same data at the same time, letting an attacker feed in their own result)** that corrupts a network socket's internal state.
- **CVE-2026-53266** — an out-of-bounds write (out-of-bounds write — software writing past the space it allocated for data, letting attackers run code).
- **CVE-2025-39682** — a flaw in the TLS (secure internet traffic) receive path that mis-handles records.

Exploitation odds are individually low (EPSS 0.001–0.005, all under the 43rd percentile), but they're on the "confirmed real right now" list — that's the signal.

**Why it matters to an SMB running AI tools**
These are in the kernel that runs your Linux servers — the same class of host that runs your self-hosted AI models, automation agents, and databases. The patches ship through your normal OS update channel; there's no vendor-specific app to fix. The risk for a small business is the machines you forgot to keep patched, especially anything exposed to the internet.

**What you do Monday** (about 10–30 minutes per server)
1. On each Linux host: run your package update (e.g. `sudo apt update && sudo apt upgrade` on Debian/Ubuntu, or the equivalent on your distro), then restart.
2. If a host hosts a customer-facing or AI-facing service, schedule the reboot for a low-traffic window and confirm the kernel has the fix afterward.
3. If you don't know which hosts run Linux or aren't patched weekly, that's the gap to close first.

**CISA / vendor metrics:** confirmed actively exploited as of 09-18-2026 · federal deadline 09-21-2026 · known ransomware campaign use: Unknown.
**Sources:**
- CISA KEV alert: https://www.cisa.gov/news-events/alerts/2026/09/18/cisa-adds-two-known-exploited-vulnerabilities-catalog
- CVE-2025-39964 fix: https://git.kernel.org/stable/c/0f28c4adbc4a97437874c9b669fd7958a8c6d6ce
- CVE-2026-53266 fix: https://git.kernel.org/stable/c/bf84ad7c7a9ede46e31afaa41a1ba06a159e8c87
- CVE-2025-39682 fix: https://git.kernel.org/stable/c/2902c3ebcca52ca845c03182000e8d71d3a5196f

---

## Jargon buster

Every technical term used today, in one plain line each:

- **CVE (Common Vulnerabilities and Exposures):** A unique ID for a publicly disclosed security flaw, so everyone tracks the same bug — like a license plate for a vulnerability.
- **SQL injection:** Typing malicious database commands into an input box (or an AI prompt), tricking the app into running unauthorized queries — reading, changing, or deleting data.
- **Prompt injection:** Hiding instructions inside the data an AI reads so it follows the attacker's orders instead of the user's.
- **Pickle:** A Python file format for saving objects; loading one can run code, so treat a random model file like an unknown program.
- **Safetensors:** A model-weight file format that stores data without running code on load. Prefer it for untrusted models.
- **MCP (Model Context Protocol):** The plug-in standard that lets an AI assistant use extra tools and services. A hole in an MCP helper is a hole in what the assistant can reach.
- **Plaintext:** Stored so anyone can read it, with no encryption.
- **Root:** The highest access level on a Linux/Unix system; root means the attacker owns the machine.
- **KEV (Known Exploited Vulnerabilities):** CISA's list of flaws being actively exploited right now — the "this is real, not theoretical" signal.
- **Race condition:** Two parts of a program writing the same data at the same time, letting an attacker feed in their own result.
- **Out-of-bounds write:** Software writing past the space it allocated for data, which attackers can use to run code.
- **Least privilege:** Giving an account only the access it needs for its job, and no more.
- **Service account:** A non-human login that software uses to talk to other software.
- **MFA (Multi-Factor Authentication):** Requiring a second proof of identity (a code from your phone, a fingerprint) beyond a password.
- **RCE (Remote Code Execution):** An attacker can run their own code on your machine from anywhere — full control.

## Appendix — raw signals

### Actively exploited (KEV) — ranked by exploitation likelihood (EPSS)

| CVE | Product | Added | Federal patch deadline | Ransom-ware use | EPSS (percentile) | Source |
|---|---|---|---|---|---|---|
| CVE-2026-76461 | Cisco Secure Email Gateway | 09-14-2026 | 09-17-2026 | No | 0.020 (79.9th) | [Cisco sb](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-esa-inj-2bLVGmhX) |
| CVE-2026-76460 | Cisco Identity Services Engine | 09-16-2026 | 09-19-2026 | No | 0.008 (54.5th) | [Cisco sb](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-ISE-ABP-VNSW7Tn5) |
| CVE-2025-39682 | Linux Kernel | 09-18-2026 | 09-21-2026 | No | 0.005 (42.1st) | [kernel fix](https://git.kernel.org/stable/c/2902c3ebcca52ca845c03182000e8d71d3a5196f) |
| CVE-2025-39964 | Linux Kernel | 09-18-2026 | 09-21-2026 | No | 0.003 (25.6th) | [kernel fix](https://git.kernel.org/stable/c/0f28c4adbc4a97437874c9b669fd7958a8c6d6ce) |
| CVE-2026-87886 | Acronis Backup (cPanel/Plesk) | 09-16-2026 | 09-19-2026 | No | 0.003 (20.8th) | [Acronis](https://security-advisory.acronis.com/advisories/SEC-10986) |
| CVE-2026-58704 | Google Pixel (cellular modem) | 09-16-2026 | 09-19-2026 | No | 0.002 (11.2th) | [Android](https://source.android.com/docs/security/bulletin/pixel/2026/2026-09-01) |
| CVE-2026-53266 | Linux Kernel | 09-18-2026 | 09-21-2026 | No | 0.001 (2.2nd) | [kernel fix](https://git.kernel.org/stable/c/bf84ad7c7a9ede46e31afaa41a1ba06a159e8c87) |

### New/disclosed today (CIRCL)
- **OpenPanel (CVE-2026-93982)** — MCP auth tokens written to plaintext logs. [advisory](https://vulnerability.circl.lu/vuln/CVE-2026-93982)
- **OpenPanel (CVE-2026-93985)** — JavaScript sandbox escape in webhook template validator. [advisory](https://vulnerability.circl.lu/vuln/CVE-2026-93985)
- **OpenPanel (CVE-2026-93983)** — SQL injection via crafted filter names bypasses project isolation. [advisory](https://vulnerability.circl.lu/vuln/CVE-2026-93983)
- **rclone (CVE-2026-93986 / CVE-2026-93987)** — path traversal (path traversal — typecasting `../` in a file path to reach files the attacker shouldn't) in volume/object names, up to 1.75.0. [CVE-2026-93986](https://vulnerability.circl.lu/vuln/CVE-2026-93986) · [CVE-2026-93987](https://vulnerability.circl.lu/vuln/CVE-2026-93987)
- **hono (CVE-2026-93981)** — missing HTML escaping of rendered strings (injection class), before 4.13.7. [advisory](https://vulnerability.circl.lu/vuln/CVE-2026-93981)

Ransomware victim pulse: source feed unavailable this run (ransomware.live query failed) — recheck tomorrow.

### IOC sample (ThreatFox/URLhaus)
- **Aisuru (botnet)** C2 IP:port addresses (block and hunt, don't visit): 188.166.158.18:8001 · 209.38.218.95:8001 · 46.101.36.181:8001 · 138.68.168.41:8001 · 144.126.224.25:8001 · 144.126.234.230:8001 · 159.65.83.2:8001 · 167.71.45.235:8001. Malware reference: [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/elf.aisuru)
- Malicious URLs (block-list hits): http://113.228.135.163:49613/bin.sh ([URLhaus](https://urlhaus.abuse.ch/url/3919002/)) · http://110.139.18.164:33747/i ([URLhaus](https://urlhaus.abuse.ch/url/3919001/)) · http://45.233.94.135:39288/i ([URLhaus](https://urlhaus.abuse.ch/url/3919000/))

---

*Compiled from public sources · 09-19-2026*