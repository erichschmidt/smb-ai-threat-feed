---
type: threat-feed-note
title: "Threat Feed — 09-14-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-09-14
updated: 2026-09-14
---

# Threat Feed — 09-14-2026

**Reader promise:** 3-minute read. Skim the headlines and the Jargon buster, then do Monday's action on anything that applies. Full glossary: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).

## How to read the scores
- **KEV** = CISA's list of flaws being **actively exploited right now**. On the list = real, not theoretical. "CISA confirmed" = the date it was added. "Federal deadline" = when US agencies must patch (good urgency anchor for everyone).
- **EPSS** = a 0–1 score estimating how likely a flaw is to be exploited in the next 30 days. Higher = patch first. Percentile = where that ranks vs all known flaws (90th percentile = more likely to be exploited than 90% of known vulnerabilities).
- **CVSS** = how bad it is *if* it works (0–10). 9.8 = exploitable remotely with no login.

---

## 1. HIGH — The AI toolkit that answers questions from your data can be tricked into changing or stealing your database
**CVE-2024-8309** · EPSS 0.1374 (96.3rd percentile) · CVSS 9.8/10

A popular open-source AI framework (LangChain) had a flaw in a helper that turns a chat question into a database lookup. An attacker can hide instructions inside a document the AI reads so that answering a question also runs their database commands.

**What broke** — LangChain's `GraphCypherQAChain` (a piece that lets a chatbot query a graph database — a database that stores things as connected points, like customers and their orders) didn't lock down the query it builds from your question. Because the query is built from data the AI reads, an attacker can inject a malicious prompt (a "prompt injection" — instructions hidden in text the AI processes) that turns a normal chat into a read, change, or delete against your database.

**Why it matters to an SMB running AI tools** — This is exactly the pattern behind "chat with your business data" products. If your AI assistant answers questions about your customer or order database through a RAG pipeline (retrieval-augmented generation — the AI grabs relevant documents/data, then answers), and any part of that stack is built on LangChain's graph helper, the documents and records you feed the AI are an attack surface. It's not just a library bug — it's a hole in the automation that talks to your data.

**What you do Monday** (30 minutes)
1. Ask whoever built your "chat with your data" tool whether it uses LangChain's `GraphCypherQAChain` — share the CVE and the GHSA link below.
2. If yes, update `langchain-community` to the patched version (fix commit: c2a3021) and re-test your chat tool against a safe copy of your data.
3. Check that your graph or SQL database is read-only for the AI's service account, so even a successful injection can't change or delete records.

**Sources:** [GitHub Security Advisory (GHSA-45pg-36p6-83v9)](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [Fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) · [huntr report](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5) · [NVD (CVE-2024-8309)](https://nvd.nist.gov/vuln/detail/CVE-2024-8309)

---

## 2. CRITICAL — Attackers can break into the warehouse that stores your software and AI models
**CVE-2026-42016, CVE-2026-42018 (JFrog Artifactory)** · KEV: CISA confirmed active exploitation 09-11-2026 · Federal deadline 09-25-2026 · Ransomware use: Unknown

JFrog Artifactory (the software/package warehouse many teams run to hold the programs, containers, and AI models their systems depend on) has two actively-exploited login flaws. One lets an attacker pass a token check and climb to higher privileges; the other can hand out an internal anonymous-user token when anonymous access is supposed to be off.

**What broke** — Both are authorization/authentication holes: the product checked that a security token looked valid but not whether it was allowed to do what it was doing, letting an unauthorized caller gain elevated access to the packages and models stored inside. CISA confirms both are being actively exploited right now.

**Why it matters to an SMB running AI tools** — Artifactory is a hub in your software supply chain (the chain of code, packages, and build systems your software depends on). The same warehouse often holds the model files and dependencies your AI pipelines pull. If an attacker takes over the warehouse, they can plant a poisoned package or model that then flows into every application and AI tool that downloads from it. One warehouse, many downstream systems.

**What you do Monday** (20 minutes)
1. Check your Artifactory version against the JFrog security advisory and patch the affected self-managed release (link below).
2. Turn on audit logging for login and token events, and review logins over the last 30 days for unknown users.
3. After patching, rotate the tokens your build/CI/CD pipelines use to pull from Artifactory.

**Sources:** [JFrog Security Advisories](https://docs.jfrog.com/releases/docs/jfrog-security-advisories) · [Artifactory Self-Managed Releases](https://docs.jfrog.com/releases/docs/artifactory-self-managed-releases) · [CISA alert](https://www.cisa.gov/news-events/alerts/2026/09/11/cisa-adds-three-known-exploited-vulnerabilities-catalog)

---

## 3. CRITICAL — Anyone on the internet can read files from your code server without a login
**CVE-2026-85706 (GitLab CE/EE)** · KEV: CISA confirmed active exploitation 09-11-2026 · Federal deadline 09-14-2026 · Ransomware use: Unknown

A hole in GitLab (a self-hosted code platform many teams run instead of GitHub) lets an unauthenticated attacker read arbitrary files from the server by exploiting a path in its repository-commit tool. "Path traversal" (a trick where an attacker types `../` in a file path to reach files they shouldn't) combined with a missing login check means no password is needed.

**What broke** — In the repository commits API, GitLab failed to keep file paths inside the repo and failed to require a login. An attacker with no account can read arbitrary files on the server — which on a code server can mean source code, configuration, and secrets.

**Why it matters to an SMB running AI tools** — GitLab is where your code, build pipelines (CI/CD — automated build-and-deploy), and often the data sources your AI tools read all live. If it's self-hosted and exposed, a file read here can expose the credentials and source that your automation and AI models are built on. And the federal deadline to patch is today.

**What you do Monday** (10 minutes)
1. Update GitLab to the fixed release — [patch release 19.3.2](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-3-2-released/) — today.
2. Confirm your GitLab instance is not exposed to the public internet without a VPN in front of it.
3. If it may have been exposed, rotate the credentials and tokens stored in GitLab CI/CD after patching.

**Sources:** [GitLab patch release notes](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-3-2-released/) · [NVD (CVE-2026-85706)](https://nvd.nist.gov/vuln/detail/CVE-2026-85706) · [CISA alert](https://www.cisa.gov/news-events/alerts/2026/09/11/cisa-adds-one-known-exploited-vulnerability-catalog)

---

## 4. CRITICAL — The remote-support tool on your machines can be hijacked to push files and run commands
**CVE-2026-84869 (ConnectWise ScreenConnect)** · KEV: CISA confirmed active exploitation 09-11-2026 · Federal deadline 09-14-2026 · Ransomware use: Unknown

ScreenConnect (a remote-support tool — an RMM, remote monitoring and management — used to log into and fix office computers) has a flaw where someone can use an active remote session to transfer files and run things without authorization or the user's confirmation.

**What broke** — Because of a missing permission check, an attacker can abuse an already-open remote-support session to push files onto and execute commands inside the machine — without the host person approving it. Remote-support tools are a favorite target because one compromised tool reaches every computer it manages. CISA confirms this is actively exploited, with a federal patch deadline of today.

**Why it matters to an SMB running AI tools** — If you or your IT support vendor use ScreenConnect, it can see and control every workstation it connects to — including the machines where your AI tools and the data sources they read live. A takeover here is a door into your whole office network, not just one computer.

**What you do Monday** (10 minutes)
1. Update every ScreenConnect instance to the patched version from the [ConnectWise security bulletin](https://www.connectwise.com/company/trust/security-bulletins/2026-09-08-screenconnect-bulletin).
2. Enable two-factor / strong auth on the ScreenConnect server and require host confirmation before any session.
3. If you use an IT provider for this, send them this link and ask: "Are we on the patched ScreenConnect release?"

**Sources:** [ConnectWise ScreenConnect bulletin](https://www.connectwise.com/company/trust/security-bulletins/2026-09-08-screenconnect-bulletin) · [NVD (CVE-2026-84869)](https://nvd.nist.gov/vuln/detail/CVE-2026-84869) · [CISA alert](https://www.cisa.gov/news-events/alerts/2026/09/11/cisa-adds-three-known-exploited-vulnerabilities-catalog)

---

## 5. WATCH — A safety scanner can miss malicious code hidden inside an AI model download
**CVE-2025-1889 (picklescan)** · CVSS 9.8/10

picklescan is a tool meant to catch dangerous Python files (pickle files — a Python format that can run code when loaded) inside AI model downloads. It only checked standard file extensions, so an attacker could name a malicious model file with a non-standard extension and the scan would skip it.

**What broke** — A common AI-safety check that scans model downloads for malware can be bypassed simply by giving the malicious file an unexpected name. This matters because loading a model file can run code — treat a random model download like an unknown program.

**Why it matters to an SMB running AI tools** — If you (or a tool you rely on) download AI models from the internet, your main protection against a malicious model is scanning the download. A scanner that can be silently skipped weakens that protection — which matters most when you're pulling open-source models into your automation or vendor stack.

**What you do Monday** (15 minutes)
1. Update picklescan to 0.0.22 or newer (the fixed version).
2. If you or your vendors download AI models, confirm the scan also covers non-standard file extensions and archives before a model is loaded.
3. Prefer model-weight formats that don't run code on load (like safetensors) for untrusted downloads.

**Sources:** [GitHub Security Advisory (GHSA-769v-p64c-89pr)](https://github.com/advisories/GHSA-769v-p64c-89pr) · [Sonatype advisory](https://sites.google.com/sonatype.com/vulnerabilities/cve-2025-1889) · [NVD (CVE-2025-1889)](https://nvd.nist.gov/vuln/detail/CVE-2025-1889)

---

## Jargon buster
- **CI/CD (Continuous Integration / Continuous Delivery):** Automated build-and-deploy — code changes are tested, built, and shipped automatically. The pipeline that turns your code into running software.
- **Graph database:** A database that stores things and their relationships as connected points (customers, orders, suppliers). AI tools may query it to answer questions about linked business records.
- **RAG (Retrieval-Augmented Generation):** The standard way AI tools "know" your business data — the AI retrieves relevant documents/data, then answers from them. The data source becomes an attack surface.
- **RMM (Remote Monitoring and Management):** Software that lets IT support log into and manage computers remotely. One compromised RMM tool reaches every machine it manages.
- **Path traversal:** A trick where an attacker types `../` in a file path to reach files they shouldn't.
- **picklescan:** A scanner meant to catch dangerous Python pickle files inside AI model downloads.
- **Software supply chain:** The code packages, build systems, repositories, and services your software depends on. A problem in one affects every application that pulls from it.
- **Prompt injection:** Tricking an AI by putting instructions inside the data it reads — the AI follows the attacker's instructions instead of the user's.
- **SQL injection:** A technique where attackers type malicious database commands into an input box (or a prompt), tricking the app into running unauthorized queries.
- **safetensors:** A model-weight file format that stores tensors without running code on load. Prefer it over pickle for untrusted models.

---

## Appendix

### Actively exploited vulnerabilities (CISA KEV) — ranked by EPSS
Ranked by likelihood of exploitation; CISA confirmed each is being actively used.

| CVE | Product | CISA confirmed | Federal deadline | EPSS | Source |
|-----|---------|----------------|------------------|------|--------|
| CVE-2026-20079 | Cisco Secure Firewall Mgmt (FMC/SCC) | 09-09-2026 | 09-12-2026 | 0.7575 | [Cisco](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-onprem-fmc-authbypass-5JPp45V2) |
| CVE-2026-19490 | Citrix NetScaler ADC/Gateway | 09-09-2026 | 09-12-2026 | 0.056 | [Citrix](https://support.citrix.com/external/article/CTX696939/netscaler-adc-and-netscaler-gateway-secu.html) |
| CVE-2025-25249 | Fortinet FortiOS / FortiSwitchManager | 09-09-2026 | 09-12-2026 | 0.024 | [Fortinet](https://fortiguard.fortinet.com/psirt/FG-IR-25-084) |
| CVE-2026-75650 | Adobe Commerce / Magento | 09-08-2026 | 09-11-2026 | 0.0215 | [Adobe](https://helpx.adobe.com/security/products/magento/apsb26-146.html) |
| CVE-2026-85706 | GitLab CE/EE | 09-11-2026 | 09-14-2026 | 0.0116 | [GitLab](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-3-2-released/) |
| CVE-2026-86060 | MikroTik RouterOS | 09-10-2026 | 09-13-2026 | 0.0102 | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-86060) |
| CVE-2026-42018 | JFrog Artifactory | 09-11-2026 | 09-25-2026 | 0.0092 | [JFrog](https://docs.jfrog.com/releases/docs/jfrog-security-advisories) |
| CVE-2026-42016 | JFrog Artifactory | 09-11-2026 | 09-25-2026 | 0.0089 | [JFrog](https://docs.jfrog.com/releases/docs/jfrog-security-advisories) |
| CVE-2026-67277 | MikroTik RouterOS | 09-10-2026 | 09-13-2026 | 0.0086 | [MikroTik](https://mikrotik.com/supportsec/september-2026-vulnerability/) |
| CVE-2026-87491 | Chromium V8 (Chrome/Edge) | 09-09-2026 | 09-23-2026 | 0.0086 | [Chrome releases](https://chromereleases.googleblog.com/2026/09/stable-channel-update-for-desktop_0808145027.html) |
| CVE-2026-86218 | N-able N-central | 09-08-2026 | 09-11-2026 | 0.0074 | [N-able](https://status.n-able.com/2026/09/06/n-central-2026-3-hotfix-4-cve-2026-86218/) |
| CVE-2026-84869 | ConnectWise ScreenConnect | 09-11-2026 | 09-14-2026 | 0.0069 | [ConnectWise](https://www.connectwise.com/company/trust/security-bulletins/2026-09-08-screenconnect-bulletin) |
| CVE-2026-81963 | Microsoft Windows Update Stack | 09-08-2026 | 09-22-2026 | 0.0063 | [MSRC](https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-81963) |
| CVE-2026-85880 | Microsoft Windows ALPC | 09-08-2026 | 09-22-2026 | 0.0057 | [MSRC](https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-85880) |

*Ransomware-use flag: "Unknown" for all items above — CISA has not labeled any of today's new KEV entries as known ransomware-campaign use.*

### Ransomware victim pulse (ransomware.live)
Sector signal for the last 24h: **Manufacturing** and **Transportation** were hit hardest.

| Group | Sector | Country | Discovered |
|-------|--------|---------|------------|
| Panzer | Manufacturing | — | 09-13-2026 |
| qilin | Manufacturing | GB | 09-13-2026 |
| qilin | Agriculture & Food | FR | 09-13-2026 |
| emperador | Transportation | — | 09-13-2026 |
| AuditTeam | Transportation | IN | 09-13-2026 |
| shinyhunters | Manufacturing | US | 09-13-2026 |
| krybit | Fashion/Retail | — | 09-13-2026 |
| AuditTeam | — | RU | 09-13-2026 |
| AuditTeam | — | DE | 09-13-2026 |
| Doommageddon | Other | IN | 09-13-2026 |

Source: [ransomware.live](https://www.ransomware.live)

### Notable new CIRCL vulnerabilities
- **CVE-2024-8309 (LangChain GraphCypherQAChain)** — SQL injection via prompt injection; EPSS 0.1374 (96.3rd percentile). On-lens, see Item 1.
- **CVE-2025-1889 (picklescan)** — malicious pickle files with non-standard extensions skip the scan; EPSS 0.0039. See Item 5.
- **Large CONPROSYS industrial/OT batch (CVE-2026-82772 … 82790+)** — a cluster of 20+ controller, PAC, M2M gateway, and I/O coupler flaws published 09-14-2026, including unauthenticated command injection and directory-listing exposures. Relevant to any manufacturing operation running these controllers; see the [CIRCL listing](https://vulnerability.circl.lu) for your model.
- **CVE-2026-9812 / CVE-2026-8821 (Mattermost)** — run-property and permission validation gaps in a self-hosted team-messaging server. [CIRCL](https://vulnerability.circl.lu/advisories/cve-2026-9812)

### IOC sample (abuse.ch)
Malicious domains / addresses to block and hunt — **do not visit**.
- **Quasar RAT** command domain: `goldieslot.co` ([Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/win.quasar_rat))
- **Aisuru** C2 IP:port: `165.227.142.229:34567` ([Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/elf.aisuru))
- **ClearFake** (fake browser-update malware): `3c-solutions-finance.fr` ([Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/js.clearfake))
- **GCleaner / Venus Stealer** hashes — see packet; family details: [GCleaner](https://malpedia.caad.fkie.fraunhofer.de/details/win.gcleaner) · [Venus Stealer](https://malpedia.caad.fkie.fraunhofer.de/details/py.venus_stealer)
- **URLhaus:** active malicious download URLs — `bunnyview.b-cdn.net/img_093703.png`, `112.248.155.16:37235/i`, `130.12.209.147:59643/bin.sh`, two Google-Drive-hosted payloads. Entry pages: [3916434](https://urlhaus.abuse.ch/url/3916434/) · [3916433](https://urlhaus.abuse.ch/url/3916433/) · [3916432](https://urlhaus.abuse.ch/url/3916432/) · [3916430](https://urlhaus.abuse.ch/url/3916430/)

---

*Compiled from public sources · 09-14-2026*
