---
type: threat-feed-note
title: "Threat Feed 09-02-2026"
status: published
tags: [threat-feed, daily, smb-ai-lens]
created: 09-02-2026
updated: 09-02-2026
---

# Threat Feed — 09-02-2026

**Three-minute read:** the headlines and [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md) give you the practical priority; the appendix preserves the evidence.

## How to read the scores

**EPSS** is a 0–1 score estimating how likely a flaw is to be exploited in the next 30 days; higher means patch first. Its percentile shows the rank against known vulnerabilities: 96.2nd percentile means more likely than 96.2% of them. **CVSS** measures impact if a flaw is used: 9.8/10 is critical and typically remotely exploitable without a login. CISA KEV means CISA has confirmed active exploitation, not a theoretical risk.

## 1. CRITICAL — A chat feature can be tricked into changing the database behind your AI tool

**CVE-2024-8309 · LangChain community 0.2.5 · CVSS 9.8/10 = critical — remotely exploitable with no authentication · EPSS 0.1374 (96.2nd percentile)**

**Sources:** [advisory](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) · [research record](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5)

### What broke

The affected LangChain GraphCypherQAChain version can turn hostile text in a chat prompt into unauthorized database commands. This is prompt injection (hidden instructions in data that make an AI follow the attacker's direction) crossing into SQL injection (tricking an app into running unauthorized database queries). The technical mechanism is an untrusted question reaching a graph query path without enough restrictions. Current signal: this is a published high-impact flaw with an EPSS score in the 96.2nd percentile; the packet does not establish confirmed active exploitation.

**Attacker view, conceptually:** an attacker looks for a public or lightly protected chat interface attached to a graph database, supplies a question designed to steer the generated query, and then watches for unusual reads, writes, or errors in database and application logs. Do not test this against production systems.

### Why it matters to an SMB running AI tools

This is directly in an AI application framework. A chatbot that can query customer, inventory, or internal knowledge graphs can become a path to alter or extract that data if the chain is exposed or given write-capable credentials.

### What you do Monday

1. **10 minutes:** In your dependency file, search for `langchain-community` and `GraphCypherQAChain`; identify every deployed app using it.
2. Update the affected package to the vendor-fixed release, rebuild the application, and deploy through your normal change process.
3. In the database console, review the application's account: make it read-only unless writes are truly required; inspect recent query and error logs for unexpected bulk reads or changes.

## 2. HIGH — Your private file server may already be a target, and its data may feed your AI search

**CVE-2023-49105 · ownCloud · EPSS 0.4320 (98.6th percentile)**

**Sources:** [ownCloud security page](https://owncloud.org/security) · [vendor advisory](https://owncloud.com/security-advisories/webdav-api-authentication-bypass-using-pre-signed-urls/)

### What broke

ownCloud can allow someone to access, change, or delete files without logging in when they know a username and the affected account has no signing key configured. This is an authentication bypass (getting past a login or permission check). You do not need the file-API detail: CISA confirmed this is being actively exploited as of 08-27-2026.

### Why it matters to an SMB running AI tools

Self-hosted file stores often supply the documents indexed by AI search and RAG (an AI pattern that retrieves business documents before answering). If that store is exposed, the attacker may reach the same source material the AI tool can retrieve, poison, or summarize.

### What you do Monday

1. **15 minutes:** Ask the owner of file storage, “Do we run ownCloud, and are all instances patched or mitigated for CVE-2023-49105?”
2. If yes, use the [ownCloud security advisory](https://owncloud.com/security-advisories/webdav-api-authentication-bypass-using-pre-signed-urls/) to apply its mitigation or supported update; remove public exposure until that is complete.
3. Review ownCloud access logs from 08-27-2026 onward for unfamiliar file reads, edits, deletes, and pre-signed-link activity; rotate affected integration credentials if activity is found.

### CISA metrics

- CISA confirmed active exploitation as of **08-27-2026**.
- Known to be used in ransomware campaigns: **Unknown**.
- CISA requires federal agencies to patch by **08-30-2026**; that deadline has passed.
- Required action translated: apply the vendor mitigation or supported update, then perform the access-log review above.
- Technical detail: [vendor advisory](https://owncloud.com/security-advisories/webdav-api-authentication-bypass-using-pre-signed-urls/).

## 3. HIGH — Patch the office print server before it becomes a way into your file shares

**CVE-2026-82078 and CVE-2026-81578 · PaperCut NG/MF · EPSS 0.0093 / 0.0077**

**Sources:** [PaperCut urgent advisory](https://www.papercut.com/kb/Main/security-bulletin-27-aug-2026-urgent-security-advisory/) · [CVE-2026-82078 record](https://nvd.nist.gov/vuln/detail/CVE-2026-82078) · [CVE-2026-81578 record](https://nvd.nist.gov/vuln/detail/CVE-2026-81578)

### What broke

PaperCut NG/MF has two flaws that can be chained: one lets an unauthenticated remote attacker change sensitive configuration, while the other can lead the server to run attacker-controlled Java code. Unsafe reflection (tricking a Java application into loading a class chosen by an attacker) is the load-bearing technical detail. CISA confirmed both are being actively exploited as of 08-31-2026.

### Why it matters to an SMB running AI tools

This is not an AI-tool flaw, but print servers commonly sit beside scan-to-folder workflows and shared document stores. Those documents can later enter an AI search or automation pipeline; a compromised print server is a foothold near that data path.

### What you do Monday

1. **10 minutes:** On the PaperCut server, open **About** and record the NG/MF version; identify every server at each site.
2. Follow the [PaperCut urgent advisory](https://www.papercut.com/kb/Main/security-bulletin-27-aug-2026-urgent-security-advisory/) to apply the specified update or mitigation before **09-14-2026**.
3. Restrict the PaperCut administration interface to the internal management network and review server logs for unexpected configuration changes or service restarts since 08-31-2026.

### CISA metrics

- CISA confirmed active exploitation as of **08-31-2026**.
- Known to be used in ransomware campaigns: **Unknown**.
- CISA requires federal agencies to patch by **09-14-2026**.
- Required action translated: install PaperCut's specified security update or mitigation, then perform the configuration and log checks above.
- Technical detail: [PaperCut advisory](https://www.papercut.com/kb/Main/security-bulletin-27-aug-2026-urgent-security-advisory/).

## 4. HIGH — Your package warehouse needs the same patch discipline as the AI apps that pull from it

**CVE-2026-66384 · JFrog Artifactory · EPSS 0.0058 (45.4th percentile)**

**Sources:** [JFrog security advisories](https://docs.jfrog.com/releases/docs/jfrog-security-advisories) · [Artifactory releases](https://docs.jfrog.com/releases/docs/artifactory-self-managed-releases)

### What broke

An authenticated Artifactory user can write data outside the intended Docker cache directory under certain remote-repository conditions. This is a path-control failure, not a confirmed public takeover by itself. CISA nevertheless confirmed active exploitation as of 08-27-2026.

### Why it matters to an SMB running AI tools

Artifactory is part of the software supply chain (the code packages, build systems, and repositories used to make and run software). AI applications may pull containers, libraries, or model-serving dependencies from it; an altered package warehouse can spread bad components into builds.

### What you do Monday

1. **10 minutes:** In Artifactory, open **Administration → System Information** and record the version; list remote repositories and users allowed to deploy or manage them.
2. Apply the applicable supported release from the [JFrog release guidance](https://docs.jfrog.com/releases/docs/artifactory-self-managed-releases) before **09-10-2026**.
3. Review audit logs for unusual cache-path writes, repository configuration changes, and unexpected package downloads since 08-27-2026; rotate affected automation tokens if activity is found.

### CISA metrics

- CISA confirmed active exploitation as of **08-27-2026**.
- Known to be used in ransomware campaigns: **Unknown**.
- CISA requires federal agencies to patch by **09-10-2026**.
- Required action translated: install the supported JFrog update, restrict repository-management access, and review the audit events above.
- Technical detail: [JFrog security advisories](https://docs.jfrog.com/releases/docs/jfrog-security-advisories).

## 5. WATCH — Ransomware claims include professional services, financial services, and manufacturing

**Signal date: 09-01-2026 to 09-02-2026 · victim disclosures are claims, not independently verified incident reports**

**Sources:** [Ransomware.live recent-victim tracking](https://www.ransomware.live)

### What broke

Public ransomware claim tracking recorded recent alleged victims in financial services, professional services, manufacturing, transportation, and business services. This is sector pressure, not proof that a named organization was breached or that a particular technical weakness was used.

### Why it matters to an SMB running AI tools

AI and automation systems concentrate business documents, workflow credentials, and service connections. During ransomware events, those connections can widen the operational impact even when the original access path was an ordinary endpoint or remote service.

### What you do Monday

1. **20 minutes:** Restore one noncritical file from your backup to a separate folder and confirm it opens correctly.
2. In your AI or automation tool, list integrations that can write to shared drives, email, or production systems; remove write access that is not needed.
3. Tell staff: “Do not approve unexpected sign-in prompts or browser ‘fix’ instructions; report them through the normal security channel.”

## Jargon buster

- **Authentication bypass:** A flaw that lets someone get past a login or permission check they should have had to pass.
- **CISA:** The US federal agency that tracks exploited vulnerabilities and publishes guidance.
- **CVE:** A unique public ID for a security flaw.
- **CVSS:** A 0–10 severity score for a flaw; it measures impact if the flaw is used.
- **EPSS:** A 0–1 score estimating the chance a flaw will be exploited in the next 30 days; higher means patch first.
- **KEV:** CISA's catalog of vulnerabilities confirmed as actively exploited.
- **LangChain:** A framework used to build AI applications, including chat and data-query tools.
- **ownCloud:** Self-hosted file-sync software; a private alternative to a shared cloud drive.
- **PaperCut NG/MF:** Self-hosted print-management software used in many offices.
- **Prompt injection:** Hidden instructions in data that make an AI follow the attacker's direction.
- **RAG:** An AI pattern that retrieves relevant business documents before answering.
- **Ransomware:** Malware that locks files or steals data for extortion.
- **Software supply chain:** The code packages, build systems, repositories, and services used to make and run software.
- **SQL injection:** Tricking an application into running unauthorized database queries.
- **Unsafe reflection:** Tricking a Java application into loading a class chosen by an attacker.

## Appendix

### CISA Known Exploited Vulnerabilities

| Rank by EPSS | CVE | Product | CISA added | Federal patch due | EPSS / percentile | Ransomware use | Source |
|---:|---|---|---|---|---|---|---|
| 1 | CVE-2023-49105 | ownCloud | 08-27-2026 | 08-30-2026 | 0.4320 / 98.6th | Unknown | [Vendor advisory](https://owncloud.com/security-advisories/webdav-api-authentication-bypass-using-pre-signed-urls/) |
| 2 | CVE-2026-82078 | PaperCut NG/MF | 08-31-2026 | 09-14-2026 | 0.0093 / 58.0th | Unknown | [Vendor advisory](https://www.papercut.com/kb/Main/security-bulletin-27-aug-2026-urgent-security-advisory/?lid=2oneu2wt0ct4) |
| 3 | CVE-2026-81578 | PaperCut NG/MF | 08-31-2026 | 09-14-2026 | 0.0077 / 53.1st | Unknown | [Vendor advisory](https://www.papercut.com/kb/Main/security-bulletin-27-aug-2026-urgent-security-advisory/) |
| 4 | CVE-2026-66384 | JFrog Artifactory | 08-27-2026 | 09-10-2026 | 0.0058 / 45.4th | Unknown | [JFrog advisory](https://docs.jfrog.com/releases/docs/jfrog-security-advisories) |
| 5 | CVE-2026-53362 | Linux Kernel | 08-27-2026 | 08-30-2026 | 0.0051 / 41.5th | Unknown | [Fix reference](https://git.kernel.org/stable/c/14200d435af9a9eeb444f529fc2f689a236b7962) |

### Ransomware sector pulse

| Group | Sector | Country | Discovered | Source |
|---|---|---|---|---|
| anubis | Financial Services | GB | 09-02-2026 | [Ransomware.live](https://www.ransomware.live) |
| SilentRansomGroup | Professional Services | US | 09-01-2026 | [Ransomware.live](https://www.ransomware.live) |
| direwolf | Manufacturing | ID | 09-01-2026 | [Ransomware.live](https://www.ransomware.live) |
| fulcrumsec | Transportation | GB | 09-01-2026 | [Ransomware.live](https://www.ransomware.live) |
| direwolf | Business Services | BR | 09-01-2026 | [Ransomware.live](https://www.ransomware.live) |

### Notable CIRCL vulnerability signals

| ID | Product / issue | Published | EPSS / percentile | Source |
|---|---|---|---|---|
| CVE-2024-8309 | LangChain GraphCypherQAChain prompt-to-query injection | 11-05-2024 | 0.1374 / 96.2nd | [GHSA](https://github.com/advisories/GHSA-45pg-36p6-83v9) |
| CVE-2025-1889 | picklescan misses nonstandard malicious model-file extensions | 03-03-2025 | 0.0038 / 31.1st | [GHSA](https://github.com/advisories/GHSA-769v-p64c-89pr) |
| CVE-2026-78657 | SigmaForms Pro AI Generated Forms file-deletion flaw | 09-02-2026 | Not scored | [CIRCL advisory](https://vulnerability.circl.lu/advisories/cve-2026-78657) |

### IOC sample — block and hunt; do not visit

| Indicator | Type | Associated signal | Seen | Source |
|---|---|---|---|---|
| `gate.albaikmenuonline.com` | Domain | IClickFix / ClearFake | 09-02-2026 | [Malpedia: IClickFix](https://malpedia.caad.fkie.fraunhofer.de/details/js.iclickfix) |
| `relais-montagnard.org` | Domain | ClearFake | 09-02-2026 | [Malpedia: ClearFake](https://malpedia.caad.fkie.fraunhofer.de/details/js.clearfake) |
| `kynequ.workers.dev` | Domain | Shin webshell | 09-02-2026 | [Malpedia: Shin webshell](https://malpedia.caad.fkie.fraunhofer.de/details/php.shin_webshell) |
| `munihuacho.gob.pe/documentos/newMSI_PRO.png` | URL | Online URLhaus entry | 09-02-2026 | [URLhaus entry](https://urlhaus.abuse.ch/url/3911372/) |
| `182.126.84.3:60500/bin.sh` | URL | Online URLhaus entry | 09-02-2026 | [URLhaus entry](https://urlhaus.abuse.ch/url/3911368/) |

Compiled from public sources · 09-02-2026
