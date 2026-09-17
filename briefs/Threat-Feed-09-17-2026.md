---
type: threat-feed-note
title: "Threat Feed — 09-17-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-09-17
updated: 2026-09-17
---

# Threat Feed — 09-17-2026

**Reader promise:** 3-minute read. Skim the headlines and the Jargon buster, then do Monday's action on anything that applies. Full glossary: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).

## How to read the scores
- **KEV** = CISA's list of flaws being **actively exploited right now**. On the list = real, not theoretical. "CISA confirmed" = the date it was added. "Federal deadline" = when US agencies must patch (good urgency anchor for everyone).
- **EPSS** = a 0–1 score estimating how likely a flaw is to be exploited in the next 30 days. Higher = patch first. Percentile = where that ranks vs all known flaws (90th percentile = more likely to be exploited than 90% of known vulnerabilities).
- **CVSS** = how bad it is *if* it works (0–10). 9.8 = exploitable remotely with no login.

**CISA added three actively-exploited vulnerabilities on 09-16-2026** (Cisco Identity Services Engine, Acronis Backup, Google Pixel) and the Cisco email-gateway patch deadline is **today, 09-17-2026** — that is Item 2 below. The highest-likelihood item in today's feed is an AI pipeline component, Item 1.

---

## 1. HIGH — A "chat with our database" AI tool will run an attacker's instructions instead of yours
**CVE-2024-8309 (LangChain `GraphCypherQAChain`, langchain-community 0.2.5)** · CVSS 9.8/10 (critical) · EPSS 0.1374 — 96.3rd percentile · Published 11-05-2024, resurfaced in today's public vulnerability feed

The LangChain component that turns a plain-language question into a database query does not separate "your question" from "data the AI read." Anything hidden inside a document or field the AI ingests can carry its own instructions and make the tool run a database command the user never asked for.

**What broke** — This is prompt injection (attacker instructions hidden inside data the AI reads) chained into SQL injection (attacker input treated as database commands). The `GraphCypherQAChain` class builds a query from the model's output and runs it without confining what that query may touch, so a poisoned source document — a support ticket, a wiki page, a competitor's PDF — becomes a database read, write, or delete. It is a fixed issue: a correction commit exists and it affects langchain-community 0.2.5 and neighbors, so the risk is entirely in whether the version you pinned still carries it. CVSS 9.8/10 means an attacker needs no login and no local access. EPSS 0.1374 is the highest likelihood score in today's feed — roughly a 14% estimated chance of exploitation in the next 30 days, higher than 96.3% of all known vulnerabilities.

**Why it matters to an SMB running AI tools** — This is the standard shape of a small business AI deployment: a chat box on top of a database or document store, built from LangChain by a contractor or a technical staffer and then left alone. The AI's database account is usually the same one that can read the customer table, because that was easiest. Prompt injection is the top risk in every AI deployment assessment right now, and this is the concrete version of it — the document is the attack, and the query is the damage.

**Attacker view (conceptual)** — Find a document the AI will ingest (an email it summarizes, a ticket it triages, a web page it reads) → hide instructions inside it → the AI builds and runs the query the attacker chose → the answer comes back in the chat window or the damage simply lands in the database. Defender observables: database queries with no matching human request, reads of tables the chat tool has no business touching, bulk updates or deletes originating from the AI service account, and sudden jumps in how often the tool queries.

**What you do Monday** (30 minutes)
1. Ask whoever built your "chat with our data" tool whether it uses `langchain-community`'s graph query chain, and ask for the pinned version — if it is 0.2.5 or nearby, get it updated (link to the fix below).
2. Give the AI's database login its own read-only account limited to the tables it actually needs — never the app's main account (10 minutes, biggest single win).
3. Point the tool at an explicit list of data sources instead of "anything it can reach," and turn on query logging so you can see what it asks for.

**Sources:** [GHSA-45pg-36p6-83v9](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [Fix commit (langchain)](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) · [huntr disclosure](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5) · [NVD (CVE-2024-8309)](https://nvd.nist.gov/vuln/detail/CVE-2024-8309)

---

## 2. CRITICAL — Your email security gateway has an actively-attacked hole and the patch deadline is today
**CVE-2026-76461 (Cisco Secure Email Gateway, AsyncOS)** · KEV: CISA confirmed active exploitation 09-14-2026 · Federal deadline 09-17-2026 · Ransomware use: Unknown · EPSS 0.0201 — 79.9th percentile · CVSS: SQL injection leading to root-level command execution

A SQL injection in Cisco's email security appliance lets an unauthenticated, remote attacker run commands with root privileges — full control of the machine that inspects all your mail. The federal deadline is today.

**What broke** — The appliance passed attacker-controlled input into a database operation without neutralizing it, and the result executes with full system rights. Nothing has to be guessed or phished: the flaw is reachable from the network. EPSS 0.0201 means roughly a 2% estimated chance of exploitation in the next 30 days, a 79.9th-percentile rank — but the KEV listing is the stronger signal, because it says this is already happening rather than predicted. **CISA confirmed this is being actively exploited as of 09-14-2026** and **requires federal agencies to patch by 09-17-2026**. Known to be used in ransomware campaigns: Unknown — CISA has not labeled it either way, so do not read that as "safe."

**Why it matters to an SMB running AI tools** — The email gateway is the choke point where inbound mail, attachments, and links are filtered before a person or an AI mail assistant ever touches them. Root on that appliance is a foothold at your network edge sitting directly in front of the mail flow that feeds everything reading your inbox — and mail is the main way prompt-injection payloads reach an AI that summarizes documents.

**What you do Monday — actually today** (15 minutes)
1. Check your Secure Email Gateway version against the Cisco advisory below and apply the vendor fix; treat today's deadline as your own if the appliance is reachable from the internet.
2. Confirm the management interface is not exposed to the internet.
3. Review the appliance for unexpected accounts, scheduled tasks, or configuration changes made outside your change window.

**Sources:** [Cisco security advisory (cisco-sa-esa-inj-2bLVGmhX)](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-esa-inj-2bLVGmhX) · [NVD (CVE-2026-76461)](https://nvd.nist.gov/vuln/detail/CVE-2026-76461) · [CISA KEV catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

---

## 3. HIGH — Anyone on the internet can read files off your code server without logging in
**CVE-2026-85706 (GitLab Community Edition and Enterprise Edition)** · KEV: CISA confirmed active exploitation 09-11-2026 · Federal deadline 09-14-2026 (passed) · Ransomware use: Unknown · EPSS 0.1196 — 95.9th percentile

GitLab's repository commits API lets an unauthenticated user read arbitrary files from the server by walking the file path — no login, no account, no invitation. Fixed in GitLab 19.3.2.

**What broke** — Path traversal (an attacker types `../` in a file path to climb out of the folder they are supposed to be limited to) in a GitLab API endpoint, combined with a missing authentication check. The impact is "read any file the GitLab service can read" — which on a self-hosted code server means configuration files, tokens, database credentials, and customer data, not just source code. **CISA confirmed this is being actively exploited as of 09-11-2026.** EPSS 0.1196 is the highest KEV score in the catalog today: about a 12% estimated chance of exploitation in the next 30 days, higher than 95.9% of all known flaws. The federal deadline passed on 09-14-2026 — three days ago — and it is a network-reachable, no-login flaw, so it is the most urgent item on this list after Item 2.

**Why it matters to an SMB running AI tools** — Self-hosted GitLab is where small teams keep code, deployment scripts, and the API keys their automations run on. It is also, increasingly, where AI tooling pulls from — a repository the AI can read is a repository whose secrets the AI's own queries can surface. File-read flaws look harmless next to ransomware, but the files are the point: one readable configuration file is the whole cloud account.

**What you do Monday** (20 minutes)
1. Check your GitLab version — Help → check the version badge, or ask whoever manages it — and upgrade to 19.3.2 or later if you are behind.
2. If you cannot patch immediately, restrict access to GitLab to your office network or VPN rather than leaving it internet-facing.
3. Assume secrets were reachable: rotate the tokens and database passwords stored on that server, starting with anything the deployment pipeline uses.

**Sources:** [GitLab patch release 19.3.2](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-3-2-released/) · [NVD (CVE-2026-85706)](https://nvd.nist.gov/vuln/detail/CVE-2026-85706) · [CISA KEV catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

---

## 4. HIGH — Two holes in the package warehouse your builds and AI pipelines pull from
**CVE-2026-42016 and CVE-2026-42018 (JFrog Artifactory)** · KEV: CISA confirmed active exploitation 09-11-2026 · Federal deadline 09-25-2026 · Ransomware use: Unknown · EPSS 0.0089 (57.5th pct) and 0.0092 (58.5th pct)

JFrog Artifactory is the internal warehouse where software packages, container images, and AI model files are stored and pulled from during a build. Two flaws let someone who should be locked out act as a trusted user: one checks a token's signature but not what the token is allowed to do, and the other hands an internal anonymous-user token to an unauthenticated caller even when anonymous access is switched off.

**What broke** — CVE-2026-42016 is an authorization failure: the product validates that a token is genuine but never validates its scope, so a low-privilege token can be used to perform privileged actions. CVE-2026-42018 is an authentication failure: with anonymous access disabled, a request still receives an internal anonymous-user token, exposing resources that were supposed to require a login. Both are **confirmed by CISA as actively exploited as of 09-11-2026**, with a **federal deadline of 09-25-2026**. The EPSS scores are modest (roughly a 1% estimated 30-day chance each, around the 58th percentile) — the active-exploitation flag is what raises them.

**Why it matters to an SMB running AI tools** — Artifactory is a supply-chain chokepoint: it is where the dependencies, images, and model artifacts your product and your AI pipelines consume are stored. If a low-privilege token can act privileged, an attacker who obtains one — from a build log, a CI/CD variable, or a developer laptop — can push a poisoned package that every downstream machine, including your model-serving box, pulls by design. Self-hosted copies should be treated as production, not a lab toy.

**What you do Monday** (30 minutes)
1. Ask your platform or DevOps person whether Artifactory is self-hosted and which version it runs; get the vendor fix for both CVEs applied (advisories linked below).
2. Confirm anonymous access is genuinely off and audit who holds admin tokens — remove any token that can do more than the job it belongs to needs.
3. Check the artifact repository's access and upload logs for pushes you cannot attribute to a build you recognize.

**Sources:** [JFrog security advisories](https://docs.jfrog.com/releases/docs/jfrog-security-advisories) · [JFrog Artifactory self-managed releases](https://docs.jfrog.com/releases/docs/artifactory-self-managed-releases) · [NVD (CVE-2026-42016)](https://nvd.nist.gov/vuln/detail/CVE-2026-42016) · [NVD (CVE-2026-42018)](https://nvd.nist.gov/vuln/detail/CVE-2026-42018) · [CISA KEV catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

---

## 5. WATCH — The system that decides which devices may join your network can be bypassed without a login
**CVE-2026-76460 (Cisco Identity Services Engine and ISE Passive Identity Connector)** · KEV: CISA confirmed active exploitation 09-16-2026 · Federal deadline 09-19-2026 · Ransomware use: Unknown · EPSS: not scored by the prediction service

Cisco Identity Services Engine is the appliance that answers "is this laptop, phone, or guest allowed on the network, and what may it reach?" An unauthenticated, remote attacker can bypass its web management interface and gain unauthorized access to the box — **CISA confirmed active exploitation on 09-16-2026**, with a **federal deadline of 09-19-2026** (two days out).

**What broke** — The product uses privileged internal interfaces without properly checking who is calling them, so the web management interface can be walked around entirely. That interface is where network access policies live — which segments exist, what a guest may reach, where your AI infrastructure sits relative to everything else. This carries no EPSS score because the prediction service has not rated it yet; that means "no number to lean on," not "low risk." Active exploitation plus a deadline two days out is the signal.

**Why it matters to an SMB running AI tools** — Network access control is the boundary that keeps a compromised laptop, a vendor's device, or a stray IoT box away from the servers hosting your internal AI models and the data they are allowed to read. Bypass the box that enforces that boundary and the "AI data stays on our network" assumption gets weaker in a way nothing else in this brief touches. It is also a common target because it sits in front of everything, and the attacker does not need a credential to reach it.

**What you do Monday** (20 minutes)
1. Find out whether you run Cisco ISE or ISE-PIC at all (ask your network vendor or IT provider — if you do not, skip this item) and get the version checked against the Cisco advisory below.
2. Confirm the management interface is not reachable from the internet — this flaw is specifically about that interface.
3. Review the appliance for new admin accounts, policy changes, or role changes you cannot attribute to your own team.

**Sources:** [Cisco security advisory (cisco-sa-ISE-ABP-VNSW7Tn5)](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-ISE-ABP-VNSW7Tn5) · [NVD (CVE-2026-76460)](https://nvd.nist.gov/vuln/detail/CVE-2026-76460) · [CISA KEV catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

---

## Jargon buster
- **Access token / assertion:** The signed digital credential an app or automation presents to prove who it is — a temporary key card. A stolen token lets an attacker act as your service without knowing any password.
- **Authorization bypass:** A flaw that lets someone who *is* logged in do things they were never granted permission to do. Different from breaking in — they walk through the wrong door.
- **cPanel / WHM and Plesk:** Web-hosting control panels commonly used on small-business web servers. Admin access there means control of every hosted site and mailbox.
- **CVSS:** A 0–10 severity score for a flaw. 9.8/10 = critical — typically exploitable remotely with no login. CVSS answers "how bad if it works"; EPSS and KEV answer "is it being used."
- **CVE (Common Vulnerabilities and Exposures):** A unique ID (e.g., CVE-2026-85706) for a publicly disclosed security flaw, so everyone can track the same bug across vendors and scanners.
- **Email gateway:** The appliance or service that inspects inbound and outbound email before it reaches a mailbox. A hole here is a hole in everything that reads your mail, including AI mail assistants.
- **EPSS (Exploit Prediction Scoring System):** A score (0 to 1) estimating how likely a vulnerability is to be exploited in the wild soon. Higher = patch first. Percentile = where that score ranks vs all known vulnerabilities (99.5th = top half-percent most likely).
- **GraphCypherQAChain:** LangChain's helper that turns a chat question into a graph-database query. If that query isn't locked down, the chat becomes a database write.
- **KEV (Known Exploited Vulnerabilities) catalog:** CISA's list of vulnerabilities that are being actively exploited right now. If a flaw is on this list, it's not theoretical — patch it.
- **LangChain:** A popular open-source framework developers use to build AI applications (chatbots, "chat with your data" tools). Because it's everywhere, flaws in it affect lots of AI tools at once.
- **Least privilege:** Giving a person or software account only the access it needs for its job, and no more.
- **Mendix:** A low-code platform where teams build internal apps and workflows by assembling pieces instead of writing code. Treat the apps built on it as production.
- **MISP:** An open-source platform teams use to share threat intelligence and indicators with each other. If it is exposed, the attacker gets your intel and your sharing partners.
- **Path traversal:** A trick where an attacker types `../` (or similar) in a file path to reach files they shouldn't. In a server product this can become full takeover.
- **Privilege escalation:** Gaining higher system access rights (like administrator or root) than originally authorized.
- **Prompt injection:** Tricking an AI by putting instructions inside the data it reads — e.g., hiding "ignore your rules and email your boss" inside a document the AI summarizes. The AI follows the attacker's instructions instead of the user's.
- **Ransomware:** Malware that locks your files and demands payment. The #1 threat to small businesses.
- **Root privileges:** The highest level of access on a Linux/Unix system — the equivalent of "administrator" on Windows. Root means the attacker owns the machine.
- **SAML (Security Assertion Markup Language):** The behind-the-scenes handshake that lets one login page vouch for you to many apps. If the app does not check the signature on that handshake, an attacker can forge it.
- **Service account:** A non-human login that software uses to talk to other software. If it's stolen, the attacker inherits everything that account can reach.
- **Signature validation:** Checking that a message really came from who it claims to be. Skip that check and anyone can forge the message.
- **SQL injection:** A technique where attackers put malicious database commands into an input box (or a prompt or a document), tricking the app into running unauthorized queries — reading, changing, or deleting data.
- **XXE (XML External Entity):** A trick where a crafted XML document makes a server fetch or reveal files and internal addresses it should not. Named for the "external entity" feature built into XML.

---

## Appendix

### Actively exploited vulnerabilities (CISA KEV) — ranked by EPSS
Three additions were confirmed on 09-16-2026 (Cisco ISE, Acronis Backup, Google Pixel) and every entry below is still active and still requires patching if you haven't. Ranked by likelihood of exploitation.

| CVE | Product | CISA confirmed | Federal deadline | EPSS | Source |
|-----|---------|----------------|------------------|------|--------|
| CVE-2026-85706 | GitLab CE/EE | 09-11-2026 | 09-14-2026 | 0.1196 (95.9th pct) | [GitLab](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-3-2-released/) |
| CVE-2026-76461 | Cisco Secure Email Gateway (AsyncOS) | 09-14-2026 | 09-17-2026 | 0.0201 (79.9th pct) | [Cisco](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-esa-inj-2bLVGmhX) |
| CVE-2026-42018 | JFrog Artifactory | 09-11-2026 | 09-25-2026 | 0.0092 (58.5th pct) | [JFrog](https://docs.jfrog.com/releases/docs/jfrog-security-advisories) |
| CVE-2026-42016 | JFrog Artifactory | 09-11-2026 | 09-25-2026 | 0.0089 (57.5th pct) | [JFrog](https://docs.jfrog.com/releases/docs/jfrog-security-advisories) |
| CVE-2026-84869 | ConnectWise ScreenConnect | 09-11-2026 | 09-14-2026 | 0.0069 (51.1st pct) | [ConnectWise](https://www.connectwise.com/company/trust/security-bulletins/2026-09-08-screenconnect-bulletin) |
| CVE-2026-58704 | Google Pixel (cellular modem) | 09-16-2026 | 09-19-2026 | 0.0011 (1.6th pct) | [Android/Pixel bulletin](https://source.android.com/docs/security/bulletin/pixel/2026/2026-09-01) |
| CVE-2026-76460 | Cisco Identity Services Engine | 09-16-2026 | 09-19-2026 | not scored | [Cisco](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-ISE-ABP-VNSW7Tn5) |
| CVE-2026-87886 | Acronis Backup plugin for cPanel & WHM / extension for Plesk | 09-16-2026 | 09-19-2026 | not scored | [Acronis](https://security-advisory.acronis.com/advisories/SEC-10986) |

*Ransomware-use flag: "Unknown" for all items above — CISA has not labeled any of these as known ransomware-campaign use.*

**Also worth a look this week:** CVE-2026-84869 (ConnectWise ScreenConnect) lets an attacker move and execute files through an active remote-support session without host confirmation — a remote-support tool that can push files is a remote-support tool that can push anything. The two older-deadline items (GitLab 09-14-2026, ConnectWise 09-14-2026) are overdue and unauthenticated-adjacent; if either is yours, they outrank the newer additions.

**New KEV addition worth knowing about even if the score is low: CVE-2026-87886 (Acronis Backup for cPanel & WHM / Plesk)** — incorrect default permissions allowing privilege escalation on the hosting control plane that also runs your backups. Backup software is a ransomware crew's first target because it is what stands between an encrypted server and a restore. Fixed releases are available from Acronis; the advisory is linked in the table above.

### Ransomware victim pulse (ransomware.live)
Sector signal for the last 24h: **Financial Services** led on data volume (one lending and brokerage claim at 9.3TB covering financials, HR, client private data, and PII/PHI records), with **Manufacturing**, **Education**, and IT/computer-services claims behind it. The **qilin** crew posted three victims in one window and **emperador** two — a burst like that is a sector-targeting signal, not proof any specific business was breached. One US commercial-property manager claim carried a hard negotiation deadline and direct contact addresses; treat those details as attacker assertions.

| Group | Sector | Country | Discovered |
|-------|--------|---------|------------|
| shinyhunters | Not Found | — | 09-17-2026 |
| ShadowByt3$ | Other | US | 09-16-2026 |
| emperador | Manufacturing | IT | 09-16-2026 |
| blacknevas | Financial Services | — | 09-16-2026 |
| emperador | Not Found | CZ | 09-16-2026 |
| qilin | Not Found | AU | 09-16-2026 |
| qilin | Other | CA | 09-16-2026 |
| Wallstreet | Manufacturing | IR | 09-16-2026 |
| Wallstreet | Education | US | 09-16-2026 |
| qilin | Other | AU | 09-16-2026 |

Source: [ransomware.live](https://www.ransomware.live)

### Notable new CIRCL vulnerabilities
- **CVE-2024-8309 (LangChain `GraphCypherQAChain`)** — prompt injection leading to database query injection, EPSS 0.1374 (96.3rd pct) — the highest likelihood score in today's feed. See Item 1. [GHSA](https://github.com/advisories/GHSA-45pg-36p6-83v9)
- **CVE-2025-1889 (picklescan through 0.0.22)** — the scanner meant to catch dangerous Python `pickle` files in AI model downloads only checks standard file extensions, so a malicious model saved with a non-standard extension passes. If your team vets downloaded models with picklescan, upgrade. [GHSA](https://github.com/advisories/GHSA-769v-p64c-89pr)
- **CVE-2026-92932 (MISP / CakePHP `Xml::build()`)** — a logic error in the condition that gates network-based XML fetching lets crafted XML reach out from the server (an XML external entity class flaw). If you run MISP or any CakePHP-based app, patch on your normal cycle. [CIRCL](https://vulnerability.circl.lu/vuln/CVE-2026-92932)
- **CVE-2026-81475 (Dell OpenManage Server Administrator, before 11.1.0.3)** — missing authentication for a critical function: an unauthenticated attacker with remote access can potentially execute code. This agent runs with deep system access on Dell servers, so it is worth a version check. [CIRCL](https://vulnerability.circl.lu/vuln/CVE-2026-81475)

### IOC sample (abuse.ch)
Malicious domains / addresses to block and hunt — **do not visit**.
- **ClearFake** (fake browser-update malware) domains: `usalo.store`, `me7wszz7.usalo.store`, `sensa138pg.it.com` ([Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/js.clearfake))
- **Jackskid** command-and-control addresses: `43.156.82.233:443`, `129.226.82.94:443` ([Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/elf.jackskid) · [research reference](https://github.com/deepfield/public-research/tree/main/jackskid))
- **Mozi** botnet download URL: `175.107.2.57:40845/Mozi.a` ([Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/elf.mozi))
- **Remus** remote-access trojan URLs: `fuarnpp.shop:5627/collections`, `teculse.click:9210/users` ([Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/win.remus))
- **URLhaus** active malware URLs: `119.114.152.239:34836/i`, `119.116.251.152:58006/i`, `27.96.93.32:54541/i`, `182.126.102.26:41130/i`, `119.180.62.17:32897/i`. Entry pages: [3917983](https://urlhaus.abuse.ch/url/3917983/) · [3917982](https://urlhaus.abuse.ch/url/3917982/) · [3917981](https://urlhaus.abuse.ch/url/3917981/) · [3917980](https://urlhaus.abuse.ch/url/3917980/) · [3917978](https://urlhaus.abuse.ch/url/3917978/)
- **Note the cloud-hosted one:** a malware bundle (`bundle.zip`) is being served from a legitimate Dropbox share link, first seen 09-17-2026 11:24 UTC. Blocking by domain will not help here — block or alert on the full URL, and treat "download the file from this cloud link" instructions as hostile by default. Entry page: [3917979](https://urlhaus.abuse.ch/url/3917979/)

### Other CISA advisories
- **Siemens Mendix SAML (ICSA-26-258-06, published 09-15-2026)** — the Mendix SAML module does not properly validate the SAML response signature, letting an unauthenticated remote attacker hijack an account session in certain single-sign-on configurations. CVSS 8.7/10 (high). Affected: Mendix 9.24 builds below 3.6.27, and Mendix 10 and 11 builds below 4.2.3. If your team builds internal apps or automations on Mendix and signs in through single sign-on, this is the fix release to take: [CISA advisory](https://www.cisa.gov/news-events/ics-advisories/icsa-26-258-06) · [CVE-2026-80465](https://www.cve.org/CVERecord?id=CVE-2026-80465) · [Mendix component](https://marketplace.mendix.com/link/component/1174)
- **CISA decoy guidance (published 09-16-2026)** — CISA published guidance on using cyber decoys to strengthen detection and response: cheap, believable fake systems that exist only to be touched, so that any interaction is a signal. Relevant to small teams because it is one of the few detection approaches that does not require a full analyst team: [CISA resource](https://www.cisa.gov/resources-tools/resources/using-cyber-decoys-strengthen-detection-and-response)

---

*Compiled from public sources · 09-17-2026*
