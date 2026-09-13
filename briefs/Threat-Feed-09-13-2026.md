---
type: threat-feed-note
title: "Threat Feed - 09-13-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-09-13
updated: 2026-09-13
---

# Threat Feed - 09-13-2026

A plain-language, 3-minute read on what broke, why it matters to a small business running AI and automation tools, and exactly what to do Monday. Full glossary of every term used here: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md)

## How to read the scores

- **EPSS** (0 to 1) estimates how likely a flaw is to be exploited in the next 30 days. Higher = patch first.
- **EPSS percentile** shows where that score ranks — 99th percentile means it is more likely to be exploited than 99% of all known vulnerabilities.
- **CISA KEV** = CISA has confirmed a flaw is being actively exploited *right now*, not theoretical. The added date is "CISA confirmed it's being used today"; the due date is when federal agencies must patch by.
- **CVSS** (0–10) says how severe a flaw is *if* it works. 9.8/10 = critical, typically exploitable remotely with no login.
- **Severity prefixes:** CRITICAL, HIGH, or WATCH. No emojis, ever.

---

## Items

### 1. HIGH — A "chat with your data" AI helper can be tricked into rewriting your database — update LangChain

**CVE-2024-8309** · EPSS 0.1374 (96.3rd percentile — top 4% most likely to be exploited) · CVSS 9.8/10

**What broke:** A common open-source AI framework (LangChain) has a helper, GraphCypherQAChain, that turns a chat question into a database query. A trick called **prompt injection** (hiding instructions inside the data the AI reads) lets an attacker turn that chat input into a live database command — an **SQL injection** (a way to read, change, or delete data the attacker shouldn't touch). One malicious line inside a document or message can reach your data.

**Why it matters to an SMB running AI tools:** This is exactly where AI meets business data. If you (or a tool you use) run any "ask your data" assistant that queries a customer, inventory, or orders database through a graph or relational database, this flaw sits in your stack. It ranks in the top 4% of known vulnerabilities by exploitation likelihood — and it lands directly on your AI-to-database path.

**What you do Monday:**
1. Ask whoever built your "chat with your data" tool whether it uses LangChain's GraphCypherQAChain, and confirm the underlying package is patched to langchain-community 0.2.6 or newer. ~15 min.
2. If you self-host the chain, upgrade the langchain-community package and make sure the chain only runs read-only queries, never writes. ~30 min.
3. Set a rule: no AI tool may write to a live business database without a human review step. ~5 min.

**Sources:** [huntr advisory](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5) · [GitHub fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) · [GitHub advisory (GHSA-45pg-36p6-83v9)](https://github.com/advisories/GHSA-45pg-36p6-83v9)

---

### 2. HIGH — Malicious "AI model" files can run code on your machine — only load models from trusted sources

**CVE-2026-90777** · published 09-13-2026

**What broke:** A widely used open-source speech-AI toolkit (ESPnet) loads downloaded model files in a way that can execute code while the file is being opened — an unsafe **deserialization** (restoring a saved file into a live program, and running whatever is inside it). A poisoned model file acts like a program, not like a passive data file.

**Why it matters to an SMB running AI tools:** Anything that pulls model files — speech, translation, image tools — and loads them without confirming they're trusted inherits this risk. If an attacker swaps a model file in a shared pipeline or an unofficial download mirror, every machine that loads it is compromised. Model files are not inert; they are executable.

**What you do Monday:**
1. If you run ESPnet or any Python AI that uses PyTorch's `torch.load` on downloaded models, upgrade and switch to safe loading (`weights_only=True`). ~20 min.
2. Pull models only from the official source or registry; treat unofficial model downloads as untrusted. ~10 min.
3. Audit for any already-downloaded `.pt` / `.pkl` model files that didn't come from a source you trust. ~15 min.

**Sources:** [CIRCL advisory](https://vulnerability.circl.lu/advisories/cve-2026-90777)

---

### 3. WATCH — The scanner that checks AI models for malware can be dodged with a file-extension trick

**CVE-2025-1889** · CVSS 9.8/10

**What broke:** **picklescan** (a scanner built to flag dangerous Python **pickle** files hidden inside AI model downloads) only checks standard file extensions. Rename a malicious file to an unexpected extension and the scanner walks straight past it — the poison gets through the gate you rely on.

**Why it matters to an SMB running AI tools:** picklescan is exactly the kind of safety check a small team runs before loading a model someone shared. Knowing it has a blind spot matters because the whole point of the tool is to be the thing that catches the poison before it reaches your stack.

**What you do Monday:**
1. Update picklescan to version 0.0.22 or newer. ~5 min.
2. Don't rely on it alone — load models only from trusted sources and prefer the safer `safetensors` model format when available. ~10 min.
3. Re-scan any model files you've brought in recently with the updated scanner. ~10 min.

**Sources:** [Sonatype advisory](https://sites.google.com/sonatype.com/vulnerabilities/cve-2025-1889) · [GitHub advisory (GHSA-769v-p64c-89pr)](https://github.com/advisories/GHSA-769v-p64c-89pr)

---

### 4. CRITICAL — Attackers are breaking into the panel that manages your firewall — patch now

**CVE-2026-20079** · EPSS 0.7575 (99.5th percentile — top half-percent most likely to be exploited) · CISA confirmed actively exploited 09-09-2026 · federal patch deadline 09-12-2026

**What broke:** Cisco's central firewall-management console (Secure Firewall Management Center and Security Cloud Control) has an **authentication bypass** (a flaw that skips the login check). An unauthenticated remote attacker can bypass sign-in and run scripts on the appliance. This is the single most likely-to-be-exploited flaw in today's feed, and it is on CISA's actively-exploited list.

**Why it matters to an SMB running AI tools:** Your firewall is the front door protecting everything your AI tools touch — models, data sources, APIs, integrations. An attacker inside the management console can rewrite the network rules that keep your whole stack safe, then lock you out of your own perimeter.

**What you do Monday:**
1. If you use Cisco FMC or Security Cloud Control, apply the vendor update immediately. ~20 min.
2. Restrict access to the management console to a small admin-only network — never expose it to the internet. ~15 min.
3. After patching, audit the console for unauthorized logins or rule changes. ~15 min.

**Sources:** [Cisco advisory](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-onprem-fmc-authbypass-5JPp45V2) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-20079)

---

### 5. CRITICAL — Your remote-support tool has a hole being actively attacked — update ScreenConnect

**CVE-2026-84869** · CISA confirmed actively exploited 09-11-2026 · federal patch deadline 09-14-2026 (tomorrow)

**What broke:** ConnectWise ScreenConnect, the remote-support tool many small IT teams use to fix computers, lets an attacker take over an active remote session without authorization — transferring files and running commands on a machine you thought you were in control of.

**Why it matters to an SMB running AI tools:** Remote-support and remote-desktop tools are among the highest-value targets in the chain — whoever controls them controls every machine in the business, including the ones running AI automations and connected to your data. This is being actively exploited today, and the federal patch deadline is tomorrow.

**What you do Monday:**
1. Update ScreenConnect to the patched build from the vendor's 09-08-2026 security bulletin. ~30 min.
2. Check any machine you've remotely supported this week for signs of a rogue session you didn't start. ~20 min.
3. If you can't patch immediately, restrict ScreenConnect access to your admin network only. ~10 min.

**Sources:** [ConnectWise security bulletin](https://www.connectwise.com/company/trust/security-bulletins/2026-09-08-screenconnect-bulletin) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-84869)

---

## Jargon buster

- **Authentication bypass:** a flaw that lets someone get past a login or permission check they should have had to pass.
- **Checkpoint (model):** a saved snapshot of a trained AI model's settings. Loading one from an untrusted source can run attacker code — treat model files like unknown programs.
- **CISA:** the US federal agency that tracks exploited vulnerabilities. Its "known exploited" list is the closest thing to "this is real right now."
- **CVE:** a unique ID for a publicly disclosed security flaw, so everyone can track the same bug.
- **CVSS:** a 0–10 severity score. 9.8/10 = critical, typically exploitable remotely with no login.
- **Deserialization:** turning a saved data blob back into a live program. If the blob is attacker-controlled, that "restore" can run their code.
- **EPSS:** a 0–1 score estimating how likely a flaw is to be exploited in the next 30 days; higher = patch first. Percentile = where that score ranks vs all known vulnerabilities.
- **ESPnet:** an open-source toolkit for AI speech processing (recognition, synthesis). It loads model files with a loader that can run code if the file is untrusted.
- **FMC / Firewall Management Center:** Cisco's centralized panel for managing many firewalls. A hole here lets an attacker rewrite the rules that protect your network.
- **Graph database:** a database that stores things and their relationships as connected points; AI tools may query it to answer questions about linked business records.
- **GraphCypherQAChain:** LangChain's helper that turns a chat question into a graph-database query. If that query isn't locked down, the chat becomes a database write.
- **KEV (Known Exploited Vulnerabilities) catalog:** CISA's list of vulnerabilities being actively exploited right now. If a flaw is on it, it's not theoretical — patch it.
- **LangChain:** a popular open-source framework for building AI applications. Because it's everywhere, flaws in it affect lots of AI tools at once.
- **pickle:** a Python file format for saving objects. Loading one can run code — treat a random `.pkl` / `.pt` file like an unknown program.
- **picklescan:** a scanner meant to catch dangerous pickle files inside AI model downloads. If it skips a file extension, a "model" can be malware.
- **Prompt injection:** tricking an AI by putting instructions inside the data it reads, so the AI follows the attacker's orders instead of the user's.
- **PyTorch:** a common toolkit for training and loading AI models. `torch.load` on an untrusted file is the danger.
- **RCE (Remote Code Execution):** an attacker can run their own code on your machine from anywhere — full control.
- **safetensors:** a model-weight file format that stores data without running code on load. Prefer it over raw `torch.load` for untrusted models.
- **ScreenConnect:** a legitimate remote-support tool attackers increasingly abuse — a fake installer or a rogue session is often malware in disguise.
- **SQL injection:** a technique where attackers type malicious database commands into an input box (or a prompt), tricking the app into running unauthorized queries.
- **weights_only:** the safe "load data only, run no code" switch for PyTorch's `torch.load`. Old code that omits it will run code from a malicious model file.

---

## Appendix

### KEV catalog (ranked by EPSS) — all actively exploited, added 09-08 to 09-11-2026

Ransomware campaign use: **Unknown** for every item in today's listing (CISA has not flagged any as ransomware-associated).

| CVE | Product | EPSS | CISA added | Federal due | Source |
| --- | --- | --- | --- | --- | --- |
| CVE-2026-20079 | Cisco Secure FMC / SCC | 0.7575 | 09-09 | 09-12 | [Cisco](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-onprem-fmc-authbypass-5JPp45V2) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-20079) |
| CVE-2026-19490 | Citrix NetScaler | 0.056 | 09-09 | 09-12 | [Citrix](https://support.citrix.com/external/article/CTX696939/netscaler-adc-and-netscaler-gateway-secu.html) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-19490) |
| CVE-2025-25249 | Fortinet (FortiOS) | 0.024 | 09-09 | 09-12 | [Fortinet](https://fortiguard.fortinet.com/psirt/FG-IR-25-084) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2025-25249) |
| CVE-2026-75650 | Adobe Commerce / Magento | 0.0215 | 09-08 | 09-11 | [Adobe](https://helpx.adobe.com/security/products/magento/apsb26-146.html) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-75650) |
| CVE-2026-85706 | GitLab CE / EE | 0.0115 | 09-11 | 09-14 | [GitLab](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-3-2-released/) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-85706) |
| CVE-2026-86060 | MikroTik RouterOS | 0.0102 | 09-10 | 09-13 | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-86060) |
| CVE-2026-42018 | JFrog Artifactory | 0.0092 | 09-11 | 09-25 | [JFrog](https://docs.jfrog.com/releases/docs/jfrog-security-advisories) |
| CVE-2026-42016 | JFrog Artifactory | 0.0089 | 09-11 | 09-25 | [JFrog](https://docs.jfrog.com/releases/docs/jfrog-security-advisories) |
| CVE-2026-87491 | Chromium V8 (Chrome/Edge) | 0.0086 | 09-09 | 09-23 | [Chrome](https://chromereleases.googleblog.com/2026/09/stable-channel-update-for-desktop_0808145027.html) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-87491) |
| CVE-2026-67277 | MikroTik RouterOS | 0.0086 | 09-10 | 09-13 | [MikroTik](https://mikrotik.com/supportsec/september-2026-vulnerability/) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-67277) |
| CVE-2026-86218 | N-able N-central | 0.0074 | 09-08 | 09-11 | [N-able](https://status.n-able.com/2026/09/06/n-central-2026-3-hotfix-4-cve-2026-86218/) |
| CVE-2026-84869 | ConnectWise ScreenConnect | 0.0069 | 09-11 | 09-14 | [ConnectWise](https://www.connectwise.com/company/trust/security-bulletins/2026-09-08-screenconnect-bulletin) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-84869) |
| CVE-2026-81963 | Microsoft Windows Update Stack | 0.0063 | 09-08 | 09-22 | [Microsoft](https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-81963) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-81963) |
| CVE-2026-85880 | Microsoft Windows ALPC | 0.0057 | 09-08 | 09-22 | [Microsoft](https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-85880) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-85880) |

### Ransomware sector pulse (discovered 09-12 to 09-13)

The **krybit** crew posted a large batch (6 victims) spanning hospitality, healthcare, transportation, and government-adjacent targets in one day — a "every sector is being hunted" signal.

| Group | Sector | Country | Note | Discovered |
| --- | --- | --- | --- | --- |
| Doommageddon | Other | India | — | 09-13 |
| Vexy Ransomware | Technology | UK | Hosting / managed-IT provider | 09-12 |
| rhysida | Professional Services | — | Electronics firm | 09-12 |
| unsafe | Technology | US | — | 09-12 |
| krybit | Hospitality | Georgia | Boutique hotel | 09-12 |
| krybit | Healthcare | Bangladesh | Non-profit trust | 09-12 |
| krybit | Transportation | India | Logistics firm | 09-12 |
| krybit | Hospitality | Morocco | Hotel group | 09-12 |

### CIRCL high-signal advisories

- **CVE-2024-8309** — LangChain GraphCypherQAChain SQL injection via prompt injection. EPSS 0.1374 (96.3rd percentile). [Sources](https://github.com/advisories/GHSA-45pg-36p6-83v9)
- **CVE-2026-90777** — ESPnet unsafe model deserialization, arbitrary code execution. Published today. [Source](https://vulnerability.circl.lu/advisories/cve-2026-90777)
- **CVE-2026-90776** — Nodemailer (a Node.js email library) quadratic-time parsing flaw in address parsing. [Source](https://vulnerability.circl.lu/advisories/cve-2026-90776)
- **CVE-2025-1889** — picklescan file-extension scan bypass. EPSS 0.0039. [Source](https://github.com/advisories/GHSA-769v-p64c-89pr)

### IOC sample (block-and-hunt signals — do not visit)

- **ClearFake** (fake browser/update malware) domains: `bvr3nwx8.kapkan.store`, `kapkan.store`, `kamaks.store`. [Source: Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/js.clearfake)
- **Mozi** (router botnet) payload URLs: `http://72.255.3.252:42908/Mozi.a`, `http://139.135.40.99:36040/Mozi.m`, `http://42.229.169.27:32848/Mozi.m`. [Source: Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/elf.mozi)
- **Aisuru** (botnet) C2 IP:ports: `137.184.75.185:8080`, `167.172.147.77:8080`. [Source: Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/elf.aisuru)
- **URLhaus** malicious URLs (active): `http://120.84.215.148:43711/i`, `http://58.47.106.225:37250/bin.sh`, `http://45.194.88.27:50386/i`. [Source: URLhaus](https://urlhaus.abuse.ch/url/3915941/)

---

*Compiled from public sources · 09-13-2026*
