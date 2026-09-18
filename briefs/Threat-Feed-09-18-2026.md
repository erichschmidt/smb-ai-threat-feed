---
type: threat-feed-note
title: "Threat Feed — 09-18-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-09-18
updated: 2026-09-18
---

# Threat Feed — 09-18-2026

**Reader promise:** 3-minute read. Skim the headlines and the Jargon buster, then do Monday's action on anything that applies. Full glossary: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).

## How to read the scores
- **KEV** = CISA's list of flaws being **actively exploited right now**. On the list = real, not theoretical. "CISA confirmed" = the date it was added. "Federal deadline" = when US agencies must patch (good urgency anchor for everyone).
- **EPSS** = a 0–1 score estimating how likely a flaw is to be exploited in the next 30 days. Higher = patch first. Percentile = where that ranks vs all known flaws (90th percentile = more likely to be exploited than 90% of known vulnerabilities).
- **CVSS** = how bad it is *if* it works (0–10). 9.8 = exploitable remotely with no login.

**Today's brief is AI-first by design.** Both top-likelihood items are in the AI/automation stack — Item 1 is a "chat with your data" component that is still the highest-likelihood finding in today's feed (carried over from yesterday), and Item 2 is a new one: a tool meant to keep malicious AI models out can be walked around by renaming a file. Two actively-exploited network flaws round out the list.

---

## 1. HIGH — The "chat with our data" AI component still ranks as today's most likely thing to be attacked
**CVE-2024-8309 (LangChain `GraphCypherQAChain`, langchain-community 0.2.5)** · CVSS 9.8/10 (critical) · EPSS 0.1374 — 96.3rd percentile · Published 11-05-2024, still the top-scoring finding in today's public vulnerability feed

This is the same finding as yesterday's Item 1, and it is still the single highest-likelihood item in today's feed — if you have not acted on it yet, it stays the priority.

**What broke** — The LangChain component that turns a plain-language question into a database query does not separate "your question" from "data the AI read." Anything hidden inside a document or field the AI ingests can carry its own instructions and make the tool run a database command the user never asked for — prompt injection (attacker instructions hidden inside data the AI reads) chained into SQL injection (attacker input treated as database commands). It is fixed in a later release, so the risk is entirely in whether the version you pinned still carries it. EPSS 0.1374 means roughly a 14% estimated chance of exploitation in the next 30 days, higher than 96.3% of all known vulnerabilities.

**Why it matters to an SMB running AI tools** — This is the standard shape of a small business AI deployment: a chat box on top of a database or document store, built from LangChain by a contractor or a technical staffer and then left alone. The AI's database login is usually the same one that can read the customer table. If you built one of these, the document the AI ingests is the attack, and the query is the damage.

**Attacker view (conceptual)** — Find a document the AI will ingest (an email it summarizes, a ticket it triages, a web page it reads) → hide instructions inside it → the AI builds and runs the query the attacker chose. Defender observables: database queries with no matching human request, reads of tables the chat tool has no business touching, and bulk updates or deletes originating from the AI service account.

**What you do Monday** (30 minutes)
1. Ask whoever built your "chat with our data" tool whether it uses `langchain-community`'s graph query chain, and ask for the pinned version — if it is 0.2.5 or nearby, get it updated (fix commit linked below).
2. Give the AI's database login its own read-only account limited to the tables it actually needs — never the app's main account (10 minutes, biggest single win).
3. Point the tool at an explicit list of data sources instead of "anything it can reach," and turn on query logging.

**Sources:** [GHSA-45pg-36p6-83v9](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [Fix commit (langchain)](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) · [huntr disclosure](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5) · [NVD (CVE-2024-8309)](https://nvd.nist.gov/vuln/detail/CVE-2024-8309)

---

## 2. WATCH — The tool that is supposed to keep malicious AI models out can be walked around by renaming a file
**CVE-2025-1889 (picklescan through 0.0.22)** · CVSS 9.8/10 (critical) · EPSS 0.0039 — 32.5th percentile · Published 03-03-2025

A scanner built to catch dangerous AI model files only looks at files with the "normal" extension — so an attacker just renames the dangerous file and it sails past the check.

**What broke** — Many AI teams vet downloaded model files with picklescan, which is meant to catch a malicious Python `pickle` object (a saved-data format that can run code when loaded) hidden inside a model download. Versions before 0.0.22 only consider standard pickle file extensions in scope for the scan, so a malicious model that hides its dangerous pickle behind a non-standard file extension passes vetting entirely. CVSS 9.8/10 means no login and no local access needed for the load to be dangerous — though the low EPSS (roughly a 0.4% estimated 30-day chance, 32.5th percentile) says it is not yet being widely hit. The fix is upgrading picklescan to 0.0.22 or later.

**Why it matters to an SMB running AI tools** — This is a model-supply-chain issue, and small teams are the ones who skip model vetting: they download a fine-tuned model from a public hub, load it, and move on. If you pull models from anywhere but a vendor you already trust, the model file is software — treat it like an unknown program and use a scanner that cannot be dodged by a filename.

**What you do Monday** (20 minutes)
1. Upgrade picklescan to 0.0.22 or later wherever your team vets downloaded models (the scanner is a `pip install` update).
2. Prefer the safetensors model format — it stores model weights without running code on load — over raw `pickle`/`torch.load` files.
3. Only load models from sources you trust; put untrusted or community models in an isolated environment first.

**Sources:** [GHSA-769v-p64c-89pr](https://github.com/advisories/GHSA-769v-p64c-89pr) · [Sonatype disclosure (CVE-2025-1889)](https://sites.google.com/sonatype.com/vulnerabilities/cve-2025-1889) · [NVD (CVE-2025-1889)](https://nvd.nist.gov/vuln/detail/CVE-2025-1889)

---

## 3. CRITICAL — Your email security gateway has an actively-attacked hole and the patch deadline has already passed
**CVE-2026-76461 (Cisco Secure Email Gateway, AsyncOS)** · KEV: CISA confirmed active exploitation 09-14-2026 · Federal deadline 09-17-2026 (passed) · Ransomware use: Unknown · EPSS 0.0201 — 79.9th percentile · CVSS: SQL injection leading to root-level command execution

A SQL injection in Cisco's email security appliance lets an unauthenticated, remote attacker run commands with root privileges — full control of the machine that inspects all your mail. The federal deadline was yesterday.

**What broke** — The appliance passed attacker-controlled input into a database operation without neutralizing it, and the result executes with full system rights (root — the highest level of access, the equivalent of "administrator" on Windows). Nothing has to be guessed or phished: the flaw is reachable from the network. EPSS 0.0201 is roughly a 2% estimated 30-day chance, a 79.9th-percentile rank — but the KEV listing is the stronger signal, because it says this is already happening rather than predicted. **CISA confirmed this is being actively exploited as of 09-14-2026** and **required federal agencies to patch by 09-17-2026** — that deadline has passed. Known to be used in ransomware campaigns: Unknown — CISA has not labeled it either way, so do not read that as "safe."

**Why it matters to an SMB running AI tools** — The email gateway is the choke point where inbound mail, attachments, and links are filtered before a person or an AI mail assistant ever touches them. Root on that appliance is a foothold at your network edge sitting directly in front of the mail flow that feeds everything reading your inbox — and mail is the main way prompt-injection payloads reach an AI that summarizes documents.

**What you do Monday — overdue, do today** (15 minutes)
1. Check your Secure Email Gateway version against the Cisco advisory below and apply the vendor fix immediately; treat the passed federal deadline as your own if the appliance is reachable from the internet.
2. Confirm the management interface is not exposed to the internet.
3. Review the appliance for unexpected accounts, scheduled tasks, or configuration changes made outside your change window.

**Sources:** [Cisco security advisory (cisco-sa-esa-inj-2bLVGmhX)](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-esa-inj-2bLVGmhX) · [NVD (CVE-2026-76461)](https://nvd.nist.gov/vuln/detail/CVE-2026-76461) · [CISA KEV catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

---

## 4. HIGH — Backup software for small web hosts is actively exploited and the deadline is tomorrow
**CVE-2026-87886 (Acronis Backup plugin for cPanel & WHM / extension for Plesk)** · KEV: CISA confirmed active exploitation 09-16-2026 · Federal deadline 09-19-2026 (tomorrow) · Ransomware use: Unknown · EPSS: not scored by the prediction service

A privilege-escalation flaw in Acronis Backup's small-hosting plugins lets a lower-level user gain higher system rights — and it is on the web-hosting control plane that also runs your backups.

**What broke** — The Acronis Backup plugin for cPanel/WHM (a common web-hosting control panel) and the extension for Plesk ship with incorrect default permissions, allowing privilege escalation (gaining higher system access rights than originally authorized). **CISA confirmed active exploitation on 09-16-2026**, with a **federal deadline of 09-19-2026** — tomorrow. This carries no EPSS score because the prediction service has not rated it; that means "no number to lean on," not "low risk." Active exploitation plus a deadline one day out is the signal.

**Why it matters to an SMB running AI tools** — Backup software is a ransomware crew's first target, because it is what stands between an encrypted server and a restore. If you host your own sites or apps with cPanel, WHM, or Plesk — or a provider who does — the same panel that manages backups is the one with the hole. Privilege escalation on that panel means an attacker can get the rights to delete or replace the backups that protect your data, and the automation that schedules them.

**What you do Monday** (20 minutes)
1. Update the Acronis Backup plugin/extension to the fixed release (advisory linked below) on every cPanel/WHM and Plesk host.
2. Confirm the backup jobs are still writing and the restore files are intact — verify one restore actually works.
3. Check the hosting panel for new admin accounts or changed backup schedules you did not create.

**Sources:** [Acronis security advisory (SEC-10986)](https://security-advisory.acronis.com/advisories/SEC-10986) · [NVD (CVE-2026-87886)](https://nvd.nist.gov/vuln/detail/CVE-2026-87886) · [CISA KEV catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

---

## Jargon buster
- **Acronis Backup (for cPanel/WHM/Plesk):** Backup software that protects small-business web hosting. A privilege-escalation hole in it is a double threat — the backup jobs themselves can be hijacked.
- **cPanel / WHM and Plesk:** Web-hosting control panels commonly used on small-business web servers. Admin access there means control of every hosted site and mailbox.
- **CVSS:** A 0–10 severity score for a flaw. 9.8/10 = critical — typically exploitable remotely with no login. CVSS answers "how bad if it works"; EPSS and KEV answer "is it being used."
- **CVE (Common Vulnerabilities and Exposures):** A unique ID (e.g., CVE-2026-76461) for a publicly disclosed security flaw, so everyone can track the same bug across vendors and scanners.
- **Email gateway:** The appliance or service that inspects inbound and outbound email before it reaches a mailbox. A hole here is a hole in everything that reads your mail, including AI mail assistants.
- **EPSS (Exploit Prediction Scoring System):** A score (0 to 1) estimating how likely a vulnerability is to be exploited in the wild soon. Higher = patch first. Percentile = where that score ranks vs all known vulnerabilities (99.5th = top half-percent most likely).
- **File extension:** The suffix (`.pkl`, `.pt`) that tells software what a file is. If a scanner only checks certain extensions, a file named differently sails past the check.
- **GraphCypherQAChain:** LangChain's helper that turns a chat question into a graph-database query. If that query isn't locked down, the chat becomes a database write.
- **KEV (Known Exploited Vulnerabilities) catalog:** CISA's list of vulnerabilities that are being actively exploited right now. If a flaw is on this list, it's not theoretical — patch it.
- **LangChain:** A popular open-source framework developers use to build AI applications (chatbots, "chat with your data" tools). Because it's everywhere, flaws in it affect lots of AI tools at once.
- **pickle:** A Python file format for saving objects. Loading one can run code — treat a random `.pkl` / `.pt` like an unknown program.
- **picklescan:** A scanner meant to catch dangerous Python pickle files inside AI model downloads. If it skips a file extension, a "model" can be malware.
- **Privilege escalation:** Gaining higher system access rights (like administrator or root) than originally authorized.
- **Prompt injection:** Tricking an AI by putting instructions inside the data it reads — e.g., hiding "ignore your rules and email your boss" inside a document the AI summarizes. The AI follows the attacker's instructions instead of the user's.
- **RCE (Remote Code Execution):** An attacker can run their own code on your machine from anywhere. "Game over" — full control.
- **Root privileges:** The highest level of access on a Linux/Unix system — the equivalent of "administrator" on Windows. Root means the attacker owns the machine.
- **safetensors:** A model-weight file format that stores tensors without running code on load. Prefer it over pickle / raw `torch.load` for untrusted models.
- **SQL injection:** A technique where attackers put malicious database commands into an input box (or a prompt or a document), tricking the app into running unauthorized queries — reading, changing, or deleting data.

---

## Appendix

### Actively exploited vulnerabilities (CISA KEV) — ranked by EPSS
All four entries below are the current KEV content as of today. Ranked by likelihood of exploitation; the two unscored entries are newer additions confirmed 09-16-2026.

| CVE | Product | CISA confirmed | Federal deadline | EPSS | Source |
|-----|---------|----------------|------------------|------|--------|
| CVE-2026-76461 | Cisco Secure Email Gateway (AsyncOS) | 09-14-2026 | 09-17-2026 | 0.0201 (79.9th pct) | [Cisco](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-esa-inj-2bLVGmhX) |
| CVE-2026-58704 | Google Pixel (cellular modem) | 09-16-2026 | 09-19-2026 | 0.0011 (1.6th pct) | [Android/Pixel bulletin](https://source.android.com/docs/security/bulletin/pixel/2026/2026-09-01) |
| CVE-2026-76460 | Cisco Identity Services Engine | 09-16-2026 | 09-19-2026 | not scored | [Cisco](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-ISE-ABP-VNSW7Tn5) |
| CVE-2026-87886 | Acronis Backup plugin for cPanel & WHM / extension for Plesk | 09-16-2026 | 09-19-2026 | not scored | [Acronis](https://security-advisory.acronis.com/advisories/SEC-10986) |

*Ransomware-use flag: "Unknown" for all items above — CISA has not labeled any of these as known ransomware-campaign use.*

**The one that matters most on this table:** the Cisco Secure Email Gateway deadline (09-17-2026) has already passed, and it is a no-login, network-reachable root flaw. If that appliance is yours, it outranks everything else here. The two items due tomorrow (09-19-2026) — Cisco ISE and Acronis Backup — are next. The Google Pixel entry is a mobile-device flaw; update your phone on its normal schedule.

### Ransomware victim pulse (ransomware.live)
Sector signal for the last 24h: the **Panzer** crew posted three victims in one window (two tech, one education — including a large German university), a burst that reads as a batch sector-targeting signal rather than proof any specific business was breached. **qilin** posted two tech-sector victims, and there was a US professional-services disclosure (a national staffing firm's data-breach public-notification phase). Treat all victim names and details as attacker assertions.

| Group | Sector | Country | Discovered |
|-------|--------|---------|------------|
| killsec | Manufacturing | SG | 09-18-2026 |
| Panzer | Technology | FR | 09-18-2026 |
| Panzer | Technology | PY | 09-18-2026 |
| Panzer | Education | DE | 09-18-2026 |
| SilentRansomGroup | Not Found | — | 09-17-2026 |
| krybit | Not Found | TR | 09-17-2026 |
| krybit | Healthcare | DE | 09-17-2026 |
| qilin | Technology | DE | 09-17-2026 |
| qilin | Technology | — | 09-17-2026 |
| chaos | Professional Services | US | 09-17-2026 |

Source: [ransomware.live](https://www.ransomware.live)

### Notable new CIRCL vulnerabilities
- **CVE-2024-8309 (LangChain `GraphCypherQAChain`)** — prompt injection leading to database query injection, EPSS 0.1374 (96.3rd pct) — the highest likelihood score in today's feed. See Item 1. [GHSA](https://github.com/advisories/GHSA-45pg-36p6-83v9)
- **CVE-2025-1889 (picklescan through 0.0.22)** — the scanner meant to catch dangerous Python `pickle` files in AI model downloads only checks standard file extensions, so a malicious model saved with a non-standard extension passes. If your team vets downloaded models with picklescan, upgrade. See Item 2. [GHSA](https://github.com/advisories/GHSA-769v-p64c-89pr)

### IOC sample (abuse.ch)
Malicious domains / addresses to block and hunt — **do not visit**.
- **Remus** remote-access trojan URLs: `homecor.click:6527/subscriptions`, `kipthen.shop:9932/webhooks` ([Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/win.remus))
- **php.shin_webshell** domains (already hosting attacker-controlled code): `mauritaalright.workers.dev`, `mimhq25218.workers.dev` ([Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/php.shin_webshell))
- **CECbot** command-and-control address: `62.60.226.173:10213` ([Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/apk.cecbot) · [research reference](https://github.com/deepfield/public-research/tree/main/cecbot))
- **Mozi** botnet download URLs: `153.117.34.135:48306/Mozi.a`, `43.230.94.186:58162/Mozi.m` ([Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/elf.mozi))
- **VShell** remote-access address: `154.91.63.108:8084` ([Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/win.vshell))
- **URLhaus** active malware URLs: `39.59.57.253:43968/i`, `39.59.57.253:43968/bin.sh`, `196.190.105.170:39910/i`, `115.61.118.230:46482/bin.sh`, `112.248.247.253:50048/i`. Entry pages: [3918536](https://urlhaus.abuse.ch/url/3918536/) · [3918535](https://urlhaus.abuse.ch/url/3918535/) · [3918533](https://urlhaus.abuse.ch/url/3918533/) · [3918532](https://urlhaus.abuse.ch/url/3918532/) · [3918531](https://urlhaus.abuse.ch/url/3918531/)
- **Note the supply-chain one:** a "Monero installer" `.bat` file is being served from a GitHub release page (`github.com/flyingman11/Monero`). That is crypto-miner malware hiding behind a legitimate-looking code host. Block the release/URL, and treat "download and run the installer from this code page" instructions as hostile by default. Entry page: [3918534](https://urlhaus.abuse.ch/url/3918534/)

### Other CISA advisories
- **Mitsubishi Electric CC-Link IE TSN (ICSA-26-211-07, published 09-08-2026)** — the newest advisory in the feed; a communication-protocol flaw that lets an attacker on the same network segment interfere with control data and cause a denial-of-service condition across a wide range of Mitsubishi controllers and motion modules. OT (operational technology — the hardware that runs physical machines) rather than office IT, so it mostly matters to businesses running industrial equipment on that protocol family: [CISA advisory](https://www.cisa.gov/news-events/ics-advisories/icsa-26-211-07)

---

*Compiled from public sources · 09-18-2026*
