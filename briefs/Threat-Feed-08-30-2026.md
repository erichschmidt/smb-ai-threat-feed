---
type: threat-feed-note
title: "Threat Feed - 08-30-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-08-30
source: "cisa-kev, cisa-advisories, ransomware.live, circl, epss, threatfox, urlhaus"
related: "https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md"
---

# Threat Feed — 08-30-2026

> **Reader promise:** 3-minute read. Headlines alone tell you what to do. New term? Check the [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).
> **Lens:** threats that hit AI tools, automations, and small-business money.
> **Sources:** every finding links to its primary source. If you want to verify, click.

## How to read the scores (30 seconds)
- **EPSS (0–1):** a score estimating how likely this flaw is to be exploited in the next 30 days; higher = patch first. 0.78 ≈ 78% — patch first. 0.01 ≈ 1% — lower urgency. Percentile ranks it against every known flaw: 99.5th = more likely to be exploited than 99.5% of all known vulnerabilities.
- **CISA KEV:** CISA only adds a flaw after confirming it's being **actively exploited right now** — not theoretical. The date shown is when CISA confirmed it. The federal deadline is their urgency rating in date form.
- **Today's window:** No new actively exploited vulnerabilities were added to CISA KEV on **08-30-2026**. ownCloud (**CVE-2023-49105**, EPSS **0.4320**) and the Linux IPv6 kernel bug (**CVE-2026-53362**) federal patch deadlines are **today (08-30-2026)**. SQL Server (**CVE-2019-1068**, EPSS **0.5284**) and Citrix NetScaler (**CVE-2026-8452**) federal deadlines passed **yesterday (08-29-2026)**. Gitea's **08-28-2026** deadline has passed (still the highest-EPSS item in this window at **0.8455**). Ajax.NET Professional (**CVE-2021-23758**, EPSS **0.8363**) is **09-09-2026**. JFrog Artifactory (**CVE-2026-66384**) is **09-10-2026**. Oracle's **08-27-2026** deadline has passed.

---

## 1. HIGH — Your LangChain "chat with database" assistant can be hijacked via prompt injection
**CVE-2024-8309** · published **11-05-2024** (active in CIRCL index) · not on CISA KEV · **EPSS 0.1374 (96.3rd percentile)** — above the 0.1 "patch first" flag · CVSS 9.8/10 = critical — network-reachable without authentication
**Sources:** [GHSA-45pg-36p6-83v9](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [Fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) · [huntr bounty report](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5) · [CIRCL / PYSEC-2024-115](https://vulnerability.circl.lu/vuln/CVE-2024-8309) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2024-8309)

**What broke:** The **GraphCypherQAChain (LangChain's helper that turns natural language questions into graph database queries)** in `langchain-community` version 0.2.5 accepts user prompts and converts them into queries without isolating malicious instructions. An attacker using **prompt injection (tricking an AI by embedding malicious instructions inside input data)** can force the chain to generate unauthorized **Cypher (the query language for graph databases)** statements, resulting in unauthorized data modification, database wiping, or data theft. Fixed in `langchain-community` updates beyond 0.2.5. If you don't run LangChain graph-QA chains, you're done.

**Why it matters to an SMB running AI tools:** This is the on-lens item: the vulnerable component is the AI application framework itself. Many small businesses use LangChain to connect customer-facing bots or internal assistants directly to company knowledge graphs and Neo4j databases. If an untrusted user prompt (from a web chat, contact form, or customer email) feeds into this chain, the attacker gains direct query execution on your database. EPSS 0.1374 places this flaw in the top 3.7% of all known vulnerabilities for exploitation likelihood.

**What you do Monday (15 minutes):**
1. Check your AI environment dependencies: run `pip list | grep langchain` on all hosts running custom chatbots or RAG pipelines.
2. Upgrade `langchain-community` to the latest release (`pip install -U langchain-community`).
3. Ensure all database credentials used by LangChain agents have strictly read-only permissions on graph stores to prevent data modification even if a prompt is manipulated.

**Attacker view (conceptual):** Identify a chatbot connected to a graph database → submit a prompt containing structured Cypher syntax instructions (e.g., instructing the LLM to ignore prior constraints and output `DELETE` or `MATCH ... RETURN` queries) → the chain blindly executes the generated query against the database → data exfiltrated or corrupted. Defender rule of thumb: validate and parameterize all LLM-generated queries; never grant write/delete privileges to an LLM service account.

---

## 2. CRITICAL — Anyone who knows a username can read, change, or delete files on your private file server — patch deadline is today
**CVE-2023-49105** · CISA confirmed active exploitation **08-27-2026** · federal patch deadline **08-30-2026 (today)** · **EPSS 0.4320 (98.7th percentile)** — above the 0.1 "patch first" flag · CVSS 9.8/10 = critical — exploitable remotely with no authentication
**Sources:** [ownCloud advisory](https://owncloud.com/security-advisories/webdav-api-authentication-bypass-using-pre-signed-urls/) · [ownCloud security](https://owncloud.org/security) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2023-49105) · [CISA alert 08-27-2026](https://www.cisa.gov/news-events/alerts/2026/08/27/cisa-adds-three-known-exploited-vulnerabilities-catalog) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** **ownCloud (a self-hosted file-sync platform like a private Dropbox)** versions 10.6.0 through 10.13.0 will accept a **pre-signed URL (a file link that is supposed to prove access was authorized)** even when the system has no signing key configured (the default setting). If an attacker knows or guesses a valid username, they can access, alter, or delete all of that user's files with **no login**. Fixed in **10.13.1**. If you don't self-host ownCloud 10.x, you're done.

**Why it matters to an SMB running AI tools:** ownCloud is frequently deployed as the central document repository that internal AI assistants, RAG pipelines, and Copilot tools index. An unauthenticated attacker can silently overwrite trusted business documents, planting malicious prompt injections or falsified data that your AI tools will summarize as truth. CISA's federal patch deadline is today (08-30-2026) and EPSS is 0.4320 (top 1.3% exploitation risk).

**What you do Monday (20 minutes — do it today if you run ownCloud 10.x):**
1. In ownCloud, navigate to Settings → Admin (or check the login footer) to verify the version. If running **10.13.1 or later**, or if using ownCloud Infinite Scale, you are safe.
2. If running 10.6.0–10.13.0, upgrade immediately to **10.13.1 or later**. Do not leave vulnerable instances exposed to the internet.
3. Tell IT: *"CVE-2023-49105 is on CISA KEV with a federal deadline of today, 08-30-2026. Upgrade ownCloud to 10.13.1 immediately and inspect WebDAV access logs for unauthorized pre-signed URL requests."*

**CISA metrics:** CISA confirmed this is being actively exploited as of 08-27-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch by 08-30-2026. Required action: apply vendor mitigations and upgrade ownCloud 10 to 10.13.1 or later.

---

## 3. CRITICAL — Attackers are exploiting legacy Ajax.NET web components to run unauthorized code on servers
**CVE-2021-23758** · CISA confirmed active exploitation **08-26-2026** · federal patch deadline **09-09-2026** · **EPSS 0.8363 (99.7th percentile)** — top 0.3% exploitation probability · CVSS 9.8/10 = critical — remote code execution without login
**Sources:** [NVD](https://nvd.nist.gov/vuln/detail/CVE-2021-23758) · [Fix commit](https://github.com/michaelschwarz/Ajax.NET-Professional/commit/b0e63be5f0bb20dfce507cb8a1a9568f6e73de57) · [CISA alert 08-26-2026](https://www.cisa.gov/news-events/alerts/2026/08/26/cisa-adds-six-known-exploited-vulnerabilities-catalog) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** **Ajax.NET Professional / AjaxPro (an older .NET web library that handles background server calls)** contains an untrusted **deserialization (turning saved data back into active program objects)** vulnerability. By sending crafted JSON payloads to the AjaxPro handler, an attacker can trigger arbitrary .NET class execution, achieving complete **RCE (remote code execution — running attacker code on your server)** with no authentication. Fixed in AjaxNetProfessional 21.11.29.1+. If your web apps do not use AjaxPro, you're done.

**Why it matters to an SMB running AI tools:** Legacy .NET libraries often linger inside custom customer portals, internal dashboards, and ERP wrappers. If an attacker compromises a web server via AjaxPro, they gain an initial foothold on the local network where internal API keys, database credentials, and AI automation servers reside. With an EPSS score of 0.8363 (99.7th percentile), automated scanners and threat actors are actively hunting and exploiting exposed endpoints.

**What you do Monday (15 minutes):**
1. Search web application directories and build packages for `AjaxPro.dll` or `AjaxPro.2.dll`.
2. If found, upgrade to version **21.11.29.1 or later** via NuGet, or replace the legacy AjaxPro handlers with modern API endpoints.
3. Tell IT: *"CVE-2021-23758 is actively exploited on CISA KEV (EPSS 0.8363). Audit all public-facing .NET web servers for AjaxPro.dll and update or decommission vulnerable handlers."*

**CISA metrics:** CISA confirmed this is being actively exploited as of 08-26-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch by 09-09-2026. Required action: apply vendor mitigations or discontinue use / transition to supported software.

---

## 4. HIGH — Linux kernel IPv6 networking flaw allows local privilege escalation — patch deadline is today
**CVE-2026-53362** · CISA confirmed active exploitation **08-27-2026** · federal patch deadline **08-30-2026 (today)** · EPSS 0.0051 (41.3th percentile) — **KEV is the authoritative signal, not EPSS**
**Sources:** [Linux Kernel Commit 14200d4](https://git.kernel.org/stable/c/14200d435af9a9eeb444f529fc2f689a236b7962) · [Linux Kernel Commit 65fb14c](https://git.kernel.org/stable/c/65fb14cbebb0cd0eff903a22d33537ddc8b95769) · [CISA alert 08-27-2026](https://www.cisa.gov/news-events/alerts/2026/08/27/cisa-adds-three-known-exploited-vulnerabilities-catalog) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** The **Linux Kernel (the core operating system software running Linux servers)** contains a vulnerability in its IPv6 networking subsystem that allows an unprivileged local user or process to gain elevated administrative (root) privileges — **privilege escalation (gaining higher access rights than authorized)**. You don't need the networking subsystem details — CISA confirmed this flaw is being actively exploited in the wild.

**Why it matters to an SMB running AI tools:** Most small-business AI infrastructure — including Docker containers, Python AI scripts, local vector databases, and model runners — operates on Linux hosts. If an attacker achieves initial low-privilege access to a container or automation worker, they can exploit this kernel bug to break out, seize root control of the host machine, and extract all hosted model weights, customer data, and environment secrets.

**What you do Monday (15 minutes — patch today if running affected Linux servers):**
1. Check your kernel version on active Linux servers: run `uname -r`.
2. Apply distribution security updates: on Ubuntu/Debian run `sudo apt update && sudo apt upgrade -y`, or on RHEL/Rocky run `sudo dnf update -y kernel`.
3. Tell IT: *"CVE-2026-53362 is on CISA KEV with a federal patch deadline of today, 08-30-2026. Patch and reboot all production Linux hosts running AI workloads and container hosts."*

**CISA metrics:** CISA confirmed this is being actively exploited as of 08-27-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch by 08-30-2026. Required action: apply vendor patches in accordance with CISA BOD 26-04.

---

## Jargon buster (terms used today)
- **CVE:** a unique ID for a security flaw, so everyone tracks the same bug (like a license plate).
- **RCE (Remote Code Execution):** attacker can run their own code on your machine — full control.
- **EPSS:** 0–1 score of how likely a flaw is to be exploited in the next 30 days. Higher = patch first.
- **Percentile:** where a score ranks — 98.7th = more likely to be exploited than 98.7% of known flaws.
- **KEV (Known Exploited Vulnerabilities):** CISA's list of flaws being actively exploited right now.
- **CVSS:** a 0–10 severity score. 9.8/10 = critical — typically exploitable remotely with no login.
- **LangChain / GraphCypherQAChain:** a popular AI application framework and its graph database query helper.
- **Prompt injection:** tricking an AI by embedding malicious instructions inside input data to bypass constraints.
- **Cypher:** the query language used by graph databases (like Neo4j) to retrieve or modify data.
- **ownCloud:** self-hosted file-sync platform (like a private Dropbox). A hole here is a hole in documents your AI tools summarize.
- **Pre-signed URL:** a file link that is supposed to prove access was authorized without requiring a password.
- **WebDAV:** an HTTP-based file transfer protocol used by ownCloud for file syncing.
- **Ajax.NET Professional / AjaxPro:** an older .NET web library that handles background server calls.
- **Deserialization:** converting saved data back into live program objects; unsafe handling can run attacker code.
- **Linux Kernel:** the core operating system software running Linux servers, containers, and VMs.
- **Privilege escalation:** gaining higher system access rights (such as administrator or root) than authorized.
- **Gitea:** a self-hosted Git server; federal deadline passed 08-28-2026, still high EPSS (0.8455).
- **JFrog Artifactory:** a repository manager for software packages and Docker images used in AI pipelines.
- **SQL Server:** Microsoft's database engine; federal patch deadline passed 08-29-2026.
- **NetScaler ADC / NetScaler Gateway:** Citrix's appliance that is often the VPN and website front door.
- **Ransomware:** malware that locks your files and demands payment — the top threat to small businesses.
- **qilin / shinyhunters / emperador / m3rx / ShadowByt3$ / incransom:** ransomware groups in recent victim disclosures. Treat the name as a sector-targeting signal, not a reason to pay.
- **ClearFake:** malware that pretends to be a browser or software update to trick visitors into infecting themselves.
- **IOC (Indicator of Compromise):** a trace of an attack (malicious IP/domain/file) to hunt for in network logs.
- **picklescan / pickle:** a scanner and a Python file format for AI models; outdated scanners can miss malicious model payloads.
- **libxml2:** a standard software library for parsing XML files; buffer overflow patches in recent Linux advisories.

Full plain-language library: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).

---

## Appendix — raw signals (for the technical reader)

### CISA KEV (last 7 days, ranked by EPSS — links to vendor advisories)
| CVE | Product | EPSS | CISA confirmed | Federal deadline | Ransomware use | Source |
|---|---|---|---|---|---|---|
| CVE-2026-60004 | Gitea (code injection via diffpatch API / Git hook) | **0.8455** | 08-25-2026 | 08-28-2026 | Unknown | [GHSA](https://github.com/go-gitea/gitea/security/advisories/GHSA-rcr6-4jqh-j84m) |
| CVE-2021-23758 | Ajax.NET Professional (deserialization / RCE) | **0.8363** | 08-26-2026 | 09-09-2026 | Unknown | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2021-23758) · [Fix commit](https://github.com/michaelschwarz/Ajax.NET-Professional/commit/b0e63be5f0bb20dfce507cb8a1a9568f6e73de57) |
| CVE-2019-1068 | Microsoft SQL Server 2014/2016/2017 (RCE) | **0.5284** | 08-26-2026 | 08-29-2026 | Unknown | [MSRC](https://portal.msrc.microsoft.com/en-US/security-guidance/advisory/CVE-2019-1068) |
| CVE-2023-49105 | ownCloud 10.6.0–10.13.0 (WebDAV auth bypass) | **0.4320** | 08-27-2026 | 08-30-2026 | Unknown | [ownCloud advisory](https://owncloud.com/security-advisories/webdav-api-authentication-bypass-using-pre-signed-urls/) |
| CVE-2026-21962 | Oracle HTTP Server / WebLogic Proxy Plug-in (access control) | **0.4202** | 08-24-2026 | 08-27-2026 | Unknown | [Oracle Jan 2026 CPU](https://www.oracle.com/security-alerts/cpujan2026.html) |
| CVE-2022-0995 | Linux Kernel (local out-of-bounds write) | 0.0952 | 08-26-2026 | 09-09-2026 | Unknown | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2022-0995) |
| CVE-2015-3246 | Red Hat libuser (local race / passwd corruption) | 0.0880 | 08-26-2026 | 09-09-2026 | Unknown | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2015-3246) |
| CVE-2015-5287 | Red Hat ABRT (local privilege escalation; EoL) | 0.0496 | 08-26-2026 | 09-09-2026 | Unknown | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2015-5287) |
| CVE-2026-8452 | Citrix NetScaler ADC / Gateway (memory buffer / DoS) | 0.0161 | 08-26-2026 | 08-29-2026 | Unknown | [CTX696604](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX696604) |
| CVE-2026-66384 | JFrog Artifactory (Docker cache path traversal) | 0.0058 | 08-27-2026 | 09-10-2026 | Unknown | [JFrog advisories](https://docs.jfrog.com/releases/docs/jfrog-security-advisories) |
| CVE-2026-53362 | Linux Kernel IPv6 (local privilege escalation) | 0.0051 | 08-27-2026 | 08-30-2026 | Unknown | [Kernel commit](https://git.kernel.org/stable/c/14200d435af9a9eeb444f529fc2f689a236b7962) |

No new KEV additions on 08-30-2026. Three added 08-27-2026: [CISA alert](https://www.cisa.gov/news-events/alerts/2026/08/27/cisa-adds-three-known-exploited-vulnerabilities-catalog). Six added 08-26-2026: [CISA alert](https://www.cisa.gov/news-events/alerts/2026/08/26/cisa-adds-six-known-exploited-vulnerabilities-catalog).

### Ransomware.live — recent victims (10)
| Group | Sector | Country | Discovered | Source |
|---|---|---|---|---|
| shinyhunters | Agriculture and Food Production | US | 08-29-2026 | [Ransomware.live](https://www.ransomware.live) |
| qilin | Other | US | 08-29-2026 | [Ransomware.live](https://www.ransomware.live) |
| qilin | Professional Services | US | 08-29-2026 | [Ransomware.live](https://www.ransomware.live) |
| emperador | Other | BR | 08-29-2026 | [Ransomware.live](https://www.ransomware.live) |
| qilin | Manufacturing | AR | 08-29-2026 | [Ransomware.live](https://www.ransomware.live) |
| qilin | Retail & E-Commerce | AU | 08-29-2026 | [Ransomware.live](https://www.ransomware.live) |
| qilin | Retail & E-Commerce | FR | 08-29-2026 | [Ransomware.live](https://www.ransomware.live) |
| qilin | Healthcare | MY | 08-29-2026 | [Ransomware.live](https://www.ransomware.live) |
| m3rx | Manufacturing | AT | 08-29-2026 | [Ransomware.live](https://www.ransomware.live) |
| qilin | Manufacturing | US | 08-29-2026 | [Ransomware.live](https://www.ransomware.live) |

No leak-site or .onion links. Named pulse: major multi-country wave by qilin hitting US professional services, manufacturing, retail, and healthcare; shinyhunters targeting US food/agriculture; and m3rx targeting European manufacturing.

### CIRCL — highest-signal new items (30 pulled)
- **CVE-2024-8309 (EPSS 0.1374, 96.3rd pct, CVSS 9.8)** — LangChain GraphCypherQAChain SQL/Cypher injection via prompt injection; upgrade `langchain-community` — [GHSA](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [Fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) · [huntr](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5)
- **CVE-2025-1889 (EPSS 0.0038, 30.9th pct)** — picklescan missed non-standard pickle extensions in ML model files; upgrade picklescan to **0.0.22 or later** — [GHSA](https://github.com/advisories/GHSA-769v-p64c-89pr) · [Sonatype](https://sites.google.com/sonatype.com/vulnerabilities/cve-2025-1889)
- **CVE-2026-11979 (RLSA-2026:60394)** — libxml2 arbitrary code execution via buffer overflow in xmlcatalog utility — [Rocky Linux](https://errata.rockylinux.org/RLSA-2026:60394) · [Red Hat](https://access.redhat.com/errata/RHSA-2026:60394)
- **CVE-2026-33818 (RLSA-2026:60306)** — Go standard library `encoding/asn1` denial of service via excessive recursion in Unmarshal — [Rocky Linux](https://errata.rockylinux.org/RLSA-2026:60306)
- **CVE-2026-74983 (RLSA-2026:58899)** — Mozilla Firefox / Thunderbird Data Loss Prevention mitigation bypass — [Rocky Linux](https://errata.rockylinux.org/RLSA-2026:58899)

### IOCs (ThreatFox 8, URLhaus 6 — linked)
- **ClearFake domains/URLs (confidence 90–100):** `eq7rkug7.shop-alphastreamplus.us`, `glucotrust-bites.us.com`, `shop-alphastreamplus.us`, `84pa4isp.retinaclearofficials.com`, `retinaclearofficials.com`, `lbsa.nova-dev.ch`, `woodfield.global`, `https://raw.githubusercontent.com/Kath19634/ural3495/refs/heads/main/fds5412` — [Malpedia: ClearFake](https://malpedia.caad.fkie.fraunhofer.de/details/js.clearfake)
- **URLhaus malware distribution URLs (online):** `http://91.184.241.245/bins/psh4`, `http://91.184.241.245/bins/pmips`, `http://91.184.241.245/bins/parm6`, `http://91.184.241.245/bins/pm68k`, `http://91.184.241.245/bins/px86` — [URLhaus 3910110](https://urlhaus.abuse.ch/url/3910110/) · `http://196.189.130.28:40073/i` — [URLhaus 3910105](https://urlhaus.abuse.ch/url/3910105/)

### CISA advisories (newest in feed, 08-13-2026)
- [Rockwell Automation OTTO Fleet Manager (ICSA-26-239-03)](https://www.cisa.gov/news-events/ics-advisories/icsa-26-239-03) — Industrial mobile robot manager weak password hashing work factor (CVE-2026-75112). Affects OTTO Fleet Manager <=V2.36.2; fixed in 2.36.3.

---

*Compiled from public sources · 08-30-2026 · Sources: CISA KEV, CISA Advisories, Ransomware.live, CIRCL, FIRST EPSS, ThreatFox, URLhaus*
