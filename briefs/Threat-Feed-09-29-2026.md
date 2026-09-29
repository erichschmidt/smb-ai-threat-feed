---
type: threat-feed-note
title: "Threat Feed — 09-29-2026"
status: published
date: 09-29-2026
tags: [threat-feed, daily, smb-ai-lens]
---

# Threat Feed — 09-29-2026

*Threat intel for people deploying AI and automation in small businesses.* Every headline is written to stand alone; every term is defined in the [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md). This is the ~3-minute read.

## How to read the scores

- **KEV** (CISA's Known Exploited Vulnerabilities) = "this is being exploited for real right now, not theoretical." If a flaw is on this list, patch it.
- **EPSS** = a 0–1 score estimating how likely a flaw is to be exploited in the next 30 days (higher = patch first), plus a percentile showing where it ranks against every known vulnerability (99th percentile = more likely to be exploited than 99% of all flaws). No new EPSS data was returned for today's reading, so this edition ranks by active-exploitation status and severity instead.
- **CVSS** = a 0–10 severity score. **CVSS 9.8/10 is critical** — typically exploitable from anywhere with no login.
- **BOD 26-04 deadline** = the date CISA requires federal agencies to patch; a useful urgency anchor for everyone.

---

## Items

### 1. CRITICAL — A common AI "chat with your data" framework lets a carefully-worded question run database commands

**CVE-2024-8309** (LangChain `GraphCypherQAChain`) · CVSS 9.8/10 (critical) · on-lens

**Sources:** [huntr bounty](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5) · [upstream fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) · [GHSA-45pg-36p6-83v9 advisory](https://github.com/advisories/GHSA-45pg-36p6-83v9)

**What broke.** LangChain is one of the most-used open-source frameworks for building AI apps (chatbots, "ask your documents" tools). Its `GraphCypherQAChain` helper turns a chat question into a query against a graph database. A bug in how it builds that query lets a carefully-worded prompt inject its own database commands — an SQL injection (tricking software into running database commands the attacker chose) triggered purely through chat text. No login needed. Rated critical, CVSS 9.8/10, because it's exploitable from anywhere and can read, change, or delete the data behind the AI.

**Why it matters to an SMB running AI tools.** If you build or run any LangChain-based assistant that interviews your business data (even through a vendor's product), this bug means the chatbot's own data source is the attack surface. An attacker doesn't need to hack your website — they just phrase a question that smuggles a database command past the AI. Worst case it silently copies data (data exfiltration) or shuts down the database. This is a supply-chain warning: an AI framework we don't maintain can open the apps built on it.

**What you do Monday** (30–45 minutes).
1. Check your AI stack's dependency list for `langchain-community` versions at or below **0.2.5**. `pip list | grep langchain`
2. Upgrade `langchain-community` to the patched version and redeploy: `pip install -U langchain-community`
3. If you can't patch today, restrict `GraphCypherQAChain` to read-only queries and put the underlying database behind a least-privilege account — never let the AI connect as a database admin.

---

### 2. HIGH — Apache Airflow's connection logic strings untrusted input and cloud keys into commands

**CVE-2026-86843, CVE-2026-81930, CVE-2026-81914, CVE-2026-81862** (Apache Airflow providers) · on-lens

**Sources:** [CVE-2026-86843 (Teradata compute-cluster DAG)](https://vulnerability.circl.lu/vuln/CVE-2026-86843) · [CVE-2026-81930 (Snowflake provider)](https://vulnerability.circl.lu/vuln/CVE-2026-81930) · [CVE-2026-81914 (Google provider)](https://vulnerability.circl.lu/vuln/CVE-2026-81914) · [CVE-2026-81862 (Teradata cloud credentials)](https://vulnerability.circl.lu/vuln/CVE-2026-81862)

**What broke.** Apache Airflow is a popular open-source orchestrator (the software that schedules and manages data and machine-learning jobs) — the traffic cop for your automated pipelines. Four new advisories (published 09-29-2026) hit its "providers," the connectors that talk to specific clouds and databases. The Teradata, Snowflake, and Google connectors build their commands by pasting in data that isn't sanitized first, so a crafted input can inject its own instructions. Two of them also embed cloud storage credentials directly into SQL statements — as plaintext inside a command. That means if any log or error message captures the command, it captures your cloud keys too.

**Why it matters to an SMB running AI tools.** If you automate AI or data work with Airflow — or a managed service built on it — these connectors are the pipes between your data and your models. "Injection on the pipe" is exactly the kind of flaw that turns a bad file name into a command, and plaintext credentials turn a single log line into a cloud compromise. If you don't run Airflow yourself, your ML vendor probably does, so it's worth asking them their patch status.

**What you do Monday** (20 minutes).
1. Update your Airflow provider packages: Teradata, Snowflake (SQL API), and Google providers to the versions in the respective advisories above. `pip install -U apache-airflow-providers-google apache-airflow-providers-snowflake apache-airflow-providers-teradata`
2. Rotate any cloud credentials those pipelines touch, since an injected command or leaked log may have exposed them.
3. If you rely on a vendor's Airflow-based service, ask: "Have you patched the 09-29-2026 Airflow provider advisories, and have you rotated the underlying cloud keys?"

---

### 3. CRITICAL — Your Citrix remote-access gateway has two holes being attacked worldwide right now — patch today

**CVE-2026-88771 / CVE-2026-88772** (Citrix NetScaler ADC & Gateway) · zero-day · in CISA KEV, added 09-27-2026

**Sources:** [CISA alert](https://www.cisa.gov/news-events/alerts/2026/09/27/critical-zero-day-vulnerabilities-exploited-citrix-netscaler-adc-gateway) · [Citrix Security Bulletin CTX697096](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697096) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) · [Steps to take if NetScaler is compromised](https://support.citrix.com/external/article/CTX694799/steps-to-take-if-netscaler-adc-is-suspec.html)

**What broke.** Citrix NetScaler ADC and Gateway — the appliance many businesses use as their VPN (the encrypted remote-access "tunnel" workers log into from home) and website front door — has two critical holes, both zero-day (a flaw that was unknown and unpatched when attackers started using it). CVE-2026-88771 lets an unauthenticated attacker (someone with no login) execute arbitrary commands; CVE-2026-88772 is a memory-buffer bug that can also lead to remote code execution. CISA's alert (09-27-2026) confirms threat actors are exploiting these worldwide, and CISA has added both to its KEV catalog — the authoritative "this is real right now" list. Federal agencies must patch by 09-30-2026 (BOD 26-04).

**Why it matters to an SMB running AI tools.** This is the front door your staff and your AI/automation services use to reach the office network. A remote-access gateway that's actively exploited means an attacker walks in through the same tunnel your people use — and once inside, they're on the network that also runs your Copilot data sources, document stores, and automation. It's not an AI bug, but it puts the AI's home network at risk.

**What you do Monday** (1–2 hours; plan for brief downtime).
1. Run the indicators of compromise Citrix published (via NetScaler Console) to check whether you've already been hit *before* you patch — patching can erase forensic evidence.
2. Apply Citrix's update for CVE-2026-88771 through CVE-2026-88778 per [CTX697096](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697096).
3. If patching is delayed, review Citrix's temporary mitigations and keep NetScaler off the public internet where you can; watch logs for the published IOCs afterward.

---

### 4. HIGH — A malicious AI model can hide malware behind a renamed file and run code when you load it

**CVE-2025-1889** (picklescan) · CVSS 9.8/10 (critical) · on-lens

**Sources:** [Sonatype advisory](https://sites.google.com/sonatype.com/vulnerabilities/cve-2025-1889) · [GHSA-769v-p64c-89pr](https://github.com/advisories/GHSA-769v-p64c-89pr)

**What broke.** When you load an AI model, you're often loading a pickle — a Python file format that can run code while it loads. picklescan is a tool teams use to scan downloaded models for dangerous pickle files before trusting them. But before version 0.0.22, it only looked at standard model file extensions (like `.pkl` or `.pt`), so an attacker could rename a malicious pickle to a non-standard extension and sail it past the scan. Load it and the "model" runs attacker code on the machine.

**Why it matters to an SMB running AI tools.** Your RAG (Retrieval-Augmented Generation — the standard way AI tools "know" your data) and other model-based automations pull weights and model files from places you may not fully control. A "model" is effectively an unknown program — and if the scanner meant to catch it has a blind spot, one bad download becomes code running inside your AI infrastructure.

**What you do Monday** (15 minutes).
1. Upgrade picklescan to **0.0.22 or later** in any pipeline that scans model files: `pip install -U picklescan`
2. Prefer `safetensors` format (a safe model format that doesn't run code on load) for any model you can — especially models you didn't train yourself.
3. When a fix isn't possible, only load models from sources you control and trust; treat every new model file like an unknown installer.

---

## Jargon buster

Plain-language definitions for terms used in today's note. Full living glossary: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).

- **Apache Airflow:** An open-source orchestrator — software that schedules and manages data and machine-learning jobs. Its "providers" are the connectors to specific clouds and databases.
- **BOD 26-04:** A CISA directive requiring federal agencies to patch actively-exploited flaws by a set deadline — a good urgency signal for everyone.
- **CVSS:** A 0–10 severity score for a flaw. 9.8/10 = critical — typically exploitable remotely with no login.
- **Data exfiltration:** Silently copying data out of your systems to the attacker.
- **Denial of service (DoS):** The service stops answering, so nobody gets in — including you.
- **EPSS:** A 0–1 score estimating how likely a flaw is to be exploited in the next 30 days; higher = patch first. Percentile = where it ranks vs every known vulnerability.
- **KEV (Known Exploited Vulnerabilities) catalog:** CISA's list of vulnerabilities being actively exploited right now. On the list = not theoretical, patch it.
- **LangChain:** A popular open-source framework for building AI applications (chatbots, "chat with your data"). Flaws in it affect lots of AI tools at once.
- **Orchestrator / orchestration:** The software that schedules and manages AI and data workloads across machines and services.
- **pickle:** A Python file format for saving objects. Loading one can run code — treat a random `.pkl` / `.pt` like an unknown program.
- **picklescan:** A scanner meant to catch dangerous Python pickle files inside AI model downloads. If it skips a file extension, a "model" can be malware.
- **Provider (in Airflow):** A connector package that lets Airflow talk to a specific service (Snowflake, Google Cloud, Teradata). A flaw here is a flaw in the pipe.
- **Prompt injection:** Tricking an AI by putting instructions inside the data it reads — e.g., hiding "ignore your rules" inside a document the AI summarizes.
- **RAG (Retrieval-Augmented Generation):** The standard way AI tools "know" your business data — retrieve relevant documents, then answer from them. Poison the source, poison the answer.
- **RCE (Remote Code Execution):** An attacker can run their own code on your machine from anywhere. Full control.
- **SQL injection:** Tricking software into running database commands the attacker chose, via a crafted input (or prompt).
- **Unauthenticated (attacker):** Someone with no login credentials, operating from anywhere.
- **VPN (Virtual Private Network):** The encrypted "tunnel" remote workers use to reach the office network.
- **Zero-day:** A flaw that was unknown and unpatched when it started being exploited — the most dangerous kind.

---

## Appendix

### Actively-exploited vulnerabilities added to CISA KEV in the last 7 days

Ranked by active-exploitation status and recency (no EPSS scores returned for today's reading). **Rank** is by how urgent patching is.

| Rank | CVE | Product | CISA confirmed | Federal deadline (BOD 26-04) | Ransomware use | Source |
|---|---|---|---|---|---|---|
| 1 | CVE-2026-88771 | Citrix NetScaler (RCE, no login) | 09-27-2026 | 09-30-2026 | Unknown | [Citrix CTX697096](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697096) |
| 1 | CVE-2026-88772 | Citrix NetScaler (RCE/DoS) | 09-27-2026 | 09-30-2026 | Unknown | [Citrix CTX697096](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697096) |
| 3 | CVE-2026-67279 | MikroTik RouterOS (unauthenticated exec) | 09-25-2026 | 09-28-2026 | Unknown | [MikroTik](https://mikrotik.com/supportsec/september-2026-vulnerability/) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-67279) |
| 3 | CVE-2026-65660 | Microsoft SharePoint (code injection) | 09-25-2026 | 09-28-2026 | Unknown | [MSRC](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-65660) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-65660) |
| 3 | CVE-2026-87902 | WordPress Core (remote file inclusion → RCE) | 09-25-2026 | 09-28-2026 | Unknown | [GHSA-7hp8-65ch-5whp](https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-7hp8-65ch-5whp) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-87902) |
| 6 | CVE-2026-5430 | WSO2 API products (path traversal → RCE) | 09-24-2026 | 09-27-2026 | Unknown | [WSO2 advisory](https://security.docs.wso2.com/en/latest/security-announcements/security-advisories/2026/WSO2-2026-5328/) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-5430) |
| 6 | CVE-2026-71362 | Adobe Commerce / Magento (authorization bypass) | 09-24-2026 | 09-27-2026 | Unknown | [Adobe APSB26-92](https://helpx.adobe.com/security/products/magento/apsb26-92.html) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-71362) |

- **CISA confirmed** = the date CISA confirmed active exploitation (KEV = real right now, not theoretical).
- **Federal deadline** = the date CISA requires federal agencies to patch (BOD 26-04). Treat as "this is urgent."
- **Ransomware use** = "Known to be used in ransomware campaigns: Yes / Unknown." All unknowns today — still patch, but no ransomware-gang signal attached.

**SMB Monday watch:** Besides the items above, update **Microsoft SharePoint** and **WordPress** cores (both KEV, both exploitable to run code), **MikroTik RouterOS** if you run MikroTik hardware, and **Adobe Commerce/Magento** if you run an online store. The WSO2 API platform path-traversal is a hole in an integration layer that often sits right next to the data your automation and AI tools read.

### Ransomware claims (Ransomware.live, 09-28-2026)

Leading a violent ransomware sector pulse: **threeam** posted a batch of victims across manufacturing (GB, AR), healthcare (CO — a health-insurance provider serving millions), technology (US x2, incl. a managed-IT firm), professional services (DE accounting), and education (AU school). **qilin** claimed a US victim; **netrunner** claimed one in MY; **Doommageddon** listed an upcoming transportation victim (deadline 10-05-2026).

[Source: ransomware.live](https://www.ransomware.live)

**SMB takeaway:** The threeam batch confirms the pattern that small construction, manufacturing, and service firms are being targeted, and a healthcare-sector hit means the healthcare supply chain is in their sights. Backups that are offline and tested, plus MFA on every remote entry, remain the work that matters — it's not the victim's failing, it's the criminals' volume.

### Notable vulnerabilities (CIRCL, newest first)

An AI/automation-heavy day beyond the items above — worth checking if you run the stack:

- **CVE-2026-81862, CVE-2026-81914, CVE-2026-81930, CVE-2026-86843** — Apache Airflow providers (see Item 2). [CIRCL](https://vulnerability.circl.lu/vuln/CVE-2026-86843)
- **CVE-2025-1889** — picklescan model-scan bypass (see Item 4). [CIRCL GHSA](https://github.com/advisories/GHSA-769v-p64c-89pr)
- **CVE-2026-95520** — heap buffer overflow in `rpm` (package manager); parsing a crafted package can cause a crash. [CIRCL](https://vulnerability.circl.lu/vuln/CVE-2026-95520)
- **CVE-2026-85520** — unauthenticated arbitrary file write in the PrestaShop Google Merchant Center module (`gmfeed`). [CIRCL](https://vulnerability.circl.lu/vuln/CVE-2026-85520)
- **CVE-2026-73593 / 73594 / 73595** — Dell Secure Connect Gateway Policy Manager: active debug code, certificate-validation gap, and code download without integrity check. [CIRCL](https://vulnerability.circl.lu/vuln/CVE-2026-73595)
- **CVE-2026-76719** — HPE OneView remote session hijacking / data-theft risk. [CIRCL](https://vulnerability.circl.lu/vuln/CVE-2026-76719)
- **CVE-2026-102495 / 102496 / 102497** — Apache XmlSchema stack-overflow denial-of-service on crafted schemas. [CIRCL](https://vulnerability.circl.lu/vuln/CVE-2026-102497)

Rocky Linux patched Python, Ruby, coreutils, libxml2, the kernel, and FreeIPA this week — if you run Rocky Enterprise Software Foundation distros, apply the September errata (e.g. [RLSA-2026:72279 FreeIPA](https://errata.rockylinux.org/RLSA-2026:72279), [RLSA-2026:71586 libxml2](https://errata.rockylinux.org/RLSA-2026:71586)).

### Sample IOCs (seen today — block and hunt these; don't visit them)

ThreatFox (abuse.ch), 100% confidence unless noted:
- **ClearFake** (fake update / drive-by): `https://cdn.jsdelivr.net/gh/52-7aa5/40ab-5bb6-d1f9b0-9634a4-e30/1-ac1b-9c-b` — [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/js.clearfake)
- Loader-related domains (75%): `zsp18.poznan.pl`, `zadelboetiek.nl`, `yawangstore.shop`, `winssensekermiskoers.nl`, `wimedyou.com`, `vpnlandw5.com`, `void-athletics.com` — [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/unknown_loader)

URLhaus (abuse.ch), online at reading time — likely botnet/malware download hosts:
- `http://107.172.209.126/img/3.jpg` — [URLhaus](https://urlhaus.abuse.ch/url/3924979/)
- `http://172.245.209.150/60/IefSebk.txt` — [URLhaus](https://urlhaus.abuse.ch/url/3924978/)
- `http://182.127.84.1:54511/i` — [URLhaus](https://urlhaus.abuse.ch/url/3924977/)
- `http://115.57.254.244:47288/i` — [URLhaus](https://urlhaus.abuse.ch/url/3924975/)
- `http://113.230.80.220:59429/bin.sh` — [URLhaus](https://urlhaus.abuse.ch/url/3924976/)
- `https://reinigung-kosanke.de/wp-includes/theme-compat/qmxythi/baw1uqm/dvwqpnh/myCRYPTED_STUB.ps1` — [URLhaus](https://urlhaus.abuse.ch/url/3924974/)

---

*Compiled from public sources · 09-29-2026*
