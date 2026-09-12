---
type: threat-feed-note
title: "Threat Feed — 09-12-2026"
status: published
tags: [threat-feed, daily, smb-ai-lens]
date: 09-12-2026
---

# Threat Feed — 09-12-2026

A three-minute security brief for people deploying AI and automation in small businesses. Read the headlines for the actions; use the [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md) when a term is new.

## How to read the scores

- **CISA KEV** means CISA has confirmed active exploitation; it is a real-now signal, not a theoretical bug.
- **EPSS** is a 0–1 score estimating how likely a flaw is to be exploited in the next 30 days; higher means patch first. Its percentile shows the rank against known flaws: 99.5th percentile means more likely to be exploited than 99.5% of them.
- **CVSS** is impact severity: 9.8/10 is critical and usually means remote exploitation without a login. CVSS says how bad; KEV and EPSS help decide what to fix first.

## 1. HIGH — A chatbot connected to your graph database can be tricked into changing or exposing business data

**CVE / metrics:** CVE-2024-8309 · CVSS 9.8/10 = critical — exploitable remotely with no authentication · EPSS 0.1374 (96.28th percentile: more likely to be exploited than 96.28% of known vulnerabilities in the next 30 days).

**Sources:** [research disclosure](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5) · [fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) · [GitHub advisory](https://github.com/advisories/GHSA-45pg-36p6-83v9)

**What broke:** LangChain Community 0.2.5's GraphCypherQAChain can turn a hostile prompt into SQL injection (malicious database commands smuggled through an input), allowing unauthorized data changes, data exposure, or service disruption. This is a prompt-injection path, not a normal chatbot mistake: the unsafe input reaches the database-query layer.

**Why it matters to an SMB running AI tools:** This is directly in the AI stack. A chat-with-your-data tool connected to Neo4j or another graph database can become a route from untrusted text to business records if it runs this affected component with broad database permissions.

**Attacker view, conceptually:** An attacker looks for a public or shared chatbot, supplies instructions that alter the generated query, then watches for unusual query failures, unexpected writes, or bulk reads.

**What you do Monday (20 minutes):**
1. In the code repository, search for `GraphCypherQAChain` and `langchain-community==0.2.5`; list every deployed chatbot that uses either.
2. Update the affected LangChain component using the [vendor fix](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255), then run the existing test suite before deployment.
3. In the graph-database console, give that chatbot a read-only, least-privilege account and review recent write/query logs for unexpected bulk reads or writes.

## 2. CRITICAL — Your AI model and software package warehouse has two actively attacked permission holes

**CVE / metrics:** CVE-2026-42016 and CVE-2026-42018 · CISA confirmed active exploitation as of 09-11-2026 · EPSS 0.0027 / 0.0035 (18.40th / 28.04th percentile; exploitation likelihood estimate, not a reason to defer an actively exploited flaw).

**Sources:** [JFrog security advisories](https://docs.jfrog.com/releases/docs/jfrog-security-advisories) · [JFrog self-managed releases](https://docs.jfrog.com/releases/docs/artifactory-self-managed-releases) · [CISA alert](https://www.cisa.gov/news-events/alerts/2026/09/11/cisa-adds-three-known-exploited-vulnerabilities-catalog)

**What broke:** Two JFrog Artifactory flaws let an attacker abuse authorization checks: one can raise permissions by presenting a token outside its intended access boundary, and the other can expose an internal anonymous-user token even when anonymous access is disabled. You do not need the token-detail mechanics; CISA says these flaws are being exploited now.

**Why it matters to an SMB running AI tools:** Artifactory commonly stores the packages, containers, and model dependencies that AI pipelines pull during builds and deployment. A compromised repository can expose private artifacts or contaminate what automated jobs download.

**What you do Monday (30 minutes):**
1. Ask the person who owns build systems: “Do we run self-hosted JFrog Artifactory, and what version is in production?”
2. If yes, open the [JFrog release page](https://docs.jfrog.com/releases/docs/artifactory-self-managed-releases), install the vendor's current fixed release for that deployment, and restart only in the approved maintenance window.
3. Rotate repository access tokens that can read or publish production packages, then review administrator and anonymous-access settings.

**CISA status:** CISA confirmed active exploitation as of 09-11-2026. Known to be used in ransomware campaigns: No (the KEV entries do not identify ransomware use). CISA requires federal agencies to patch by 09-25-2026; that deadline is a practical urgency anchor, though it applies directly to federal agencies.

## 3. CRITICAL — A firewall control panel being actively attacked can let an outsider run files on the management server

**CVE / metrics:** CVE-2026-20079 · CISA confirmed active exploitation as of 09-09-2026 · EPSS 0.7575 (99.49th percentile: more likely to be exploited than 99.49% of known vulnerabilities in the next 30 days).

**Sources:** [Cisco advisory](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-onprem-fmc-authbypass-5JPp45V2) · [NVD record](https://nvd.nist.gov/vuln/detail/CVE-2026-20079)

**What broke:** Cisco Secure Firewall Management Center and Security Cloud Control Firewall Management have an authentication bypass (a flaw that lets someone get past a login check) that can let an unauthenticated remote attacker execute script files on the management system.

**Why it matters to an SMB running AI tools:** This is not an AI product, but it protects the network boundary around systems that hold automation credentials, document stores, and AI service connectors. A compromised firewall manager can give an attacker a better route to those systems.

**What you do Monday (15 minutes):**
1. In the Cisco management console, open **System → About** and record the product and version; confirm whether it is reachable from the public internet.
2. Match the version to the [Cisco advisory](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-onprem-fmc-authbypass-5JPp45V2) and install Cisco's fixed release using the documented upgrade path.
3. Restrict the management interface to VPN or named administrator IP addresses, then review administrator logins and script-file activity since 09-09-2026.

**CISA status:** CISA confirmed active exploitation as of 09-09-2026. Known to be used in ransomware campaigns: No (the KEV entry does not identify ransomware use). CISA requires federal agencies to patch by 09-12-2026; that deadline is today.

## 4. WATCH — Ransomware crews are claiming technology and manufacturing victims, so test recovery for the systems your automations depend on

**Sources:** [Ransomware.live recent-victim tracker](https://www.ransomware.live)

**What broke:** Recent attacker claims include manufacturing organizations in the United States and Bulgaria and technology organizations in the United States, Sweden, India, and an unspecified location. These are claims from criminal groups, not independently verified incident reports.

**Why it matters to an SMB running AI tools:** Automation often concentrates access: a single service account may reach documents, cloud storage, databases, and deployment systems. Ransomware disruption can stop those workflows even if the AI application itself is not the initial entry point.

**What you do Monday (25 minutes):**
1. Pick one automation that handles business documents and identify its source data, credentials, and recovery owner.
2. Restore one non-sensitive test file from its backup to a separate folder; confirm it opens and the automation can safely read it.
3. Tell the IT owner: “Please verify that our backup restore works for the document store and database used by this automation, not just that the backup job reports success.”

## Jargon buster

- **Authentication bypass:** A flaw that lets someone get past a login or permission check they should have had to pass.
- **CISA:** The US federal agency that tracks exploited vulnerabilities and publishes guidance.
- **CVE:** A unique ID for a publicly disclosed security flaw.
- **CVSS:** A 0–10 severity score for a flaw; it describes potential impact.
- **EPSS:** A 0–1 estimate of how likely a vulnerability is to be exploited soon; higher means patch first.
- **GraphCypherQAChain:** LangChain's helper that turns a chat question into a graph-database query.
- **KEV:** CISA's list of vulnerabilities being actively exploited right now.
- **Prompt injection:** Instructions hidden in content that try to make an AI ignore its intended rules.
- **SQL injection:** Malicious database commands inserted through an input so an application runs unauthorized queries.

## Appendix

### CISA Known Exploited Vulnerabilities

| CVE | Product | Added | Federal patch deadline | EPSS | Ransomware use | Source |
|---|---|---:|---:|---:|---|---|
| CVE-2026-20079 | Cisco Secure Firewall Management | 09-09-2026 | 09-12-2026 | 0.7575 (99.49th) | No identified use | [Cisco advisory](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-onprem-fmc-authbypass-5JPp45V2) |
| CVE-2026-19490 | Citrix NetScaler | 09-09-2026 | 09-12-2026 | 0.0560 (92.44th) | No identified use | [Citrix advisory](https://support.citrix.com/external/article/CTX696939/netscaler-adc-and-netscaler-gateway-secu.html) |
| CVE-2025-25249 | Fortinet products | 09-09-2026 | 09-12-2026 | 0.0240 (83.09th) | No identified use | [Fortinet advisory](https://fortiguard.fortinet.com/psirt/FG-IR-25-084) |
| CVE-2026-75650 | Adobe Commerce / Magento | 09-08-2026 | 09-11-2026 | 0.0215 (81.05th) | No identified use | [Adobe advisory](https://helpx.adobe.com/security/products/magento/apsb26-146.html) |
| CVE-2026-87491 | Chromium V8 | 09-09-2026 | 09-23-2026 | 0.0086 (56.37th) | No identified use | [Google advisory](https://chromereleases.googleblog.com/2026/09/stable-channel-update-for-desktop_0808145027.html) |
| CVE-2026-67277 | MikroTik RouterOS | 09-10-2026 | 09-13-2026 | 0.0075 (52.79th) | No identified use | [MikroTik advisory](https://mikrotik.com/supportsec/september-2026-vulnerability/) |
| CVE-2026-86218 | N-able N-central | 09-08-2026 | 09-11-2026 | 0.0074 (52.67th) | No identified use | [N-able advisory](https://status.n-able.com/2026/09/06/n-central-2026-3-hotfix-4-cve-2026-86218/) |
| CVE-2026-86060 | MikroTik RouterOS | 09-10-2026 | 09-13-2026 | 0.0069 (50.74th) | No identified use | [NVD record](https://nvd.nist.gov/vuln/detail/CVE-2026-86060) |
| CVE-2026-81963 | Microsoft Windows Update Stack | 09-08-2026 | 09-22-2026 | 0.0063 (48.22nd) | No identified use | [Microsoft advisory](https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-81963) |
| CVE-2026-85880 | Microsoft Windows ALPC | 09-08-2026 | 09-22-2026 | 0.0057 (45.46th) | No identified use | [Microsoft advisory](https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-85880) |
| CVE-2026-84869 | ConnectWise ScreenConnect | 09-11-2026 | 09-14-2026 | 0.0038 (31.64th) | No identified use | [ConnectWise bulletin](https://www.connectwise.com/company/trust/security-bulletins/2026-09-08-screenconnect-bulletin) |
| CVE-2026-42018 | JFrog Artifactory | 09-11-2026 | 09-25-2026 | 0.0035 (28.04th) | No identified use | [JFrog advisory](https://docs.jfrog.com/releases/docs/jfrog-security-advisories) |
| CVE-2026-42016 | JFrog Artifactory | 09-11-2026 | 09-25-2026 | 0.0027 (18.40th) | No identified use | [JFrog advisory](https://docs.jfrog.com/releases/docs/jfrog-security-advisories) |
| CVE-2026-85706 | GitLab CE / EE | 09-11-2026 | 09-14-2026 | Not scored | No identified use | [GitLab advisory](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-3-2-released/) |

### Ransomware victim-sector pulse

| Group | Sector | Country | Discovered | Source |
|---|---|---|---:|---|
| securotrop | Manufacturing | US | 09-12-2026 | [Ransomware.live](https://www.ransomware.live) |
| safepay | Technology | US | 09-11-2026 | [Ransomware.live](https://www.ransomware.live) |
| direwolf | Transportation | MY | 09-11-2026 | [Ransomware.live](https://www.ransomware.live) |
| fulcrumsec | Technology | SE | 09-11-2026 | [Ransomware.live](https://www.ransomware.live) |
| Panzer | Manufacturing | BG | 09-11-2026 | [Ransomware.live](https://www.ransomware.live) |
| Panzer | Government & Defense | ES | 09-11-2026 | [Ransomware.live](https://www.ransomware.live) |
| qilin | Healthcare | US | 09-11-2026 | [Ransomware.live](https://www.ransomware.live) |
| Global Secret Group | Financial Services | IN | 09-10-2026 | [Ransomware.live](https://www.ransomware.live) |
| Vexy Ransomware | Technology | IN | 09-10-2026 | [Ransomware.live](https://www.ransomware.live) |
| play | Technology | Unspecified | 09-10-2026 | [Ransomware.live](https://www.ransomware.live) |

### Notable CIRCL findings

| Finding | Product | Severity / EPSS | Source |
|---|---|---|---|
| CVE-2024-8309 | LangChain Community GraphCypherQAChain | CVSS 9.8/10 · 0.1374 (96.28th) | [GitHub advisory](https://github.com/advisories/GHSA-45pg-36p6-83v9) |
| CVE-2025-1889 | picklescan | CVSS 9.8/10 · 0.0039 (32.20th) | [GitHub advisory](https://github.com/advisories/GHSA-769v-p64c-89pr) |

### IOC sample — block and hunt; do not visit

| Indicator | Type | Associated malware | Seen | Source |
|---|---|---|---:|---|
| `172u1sfd.diero.store` | Domain | ClearFake | 09-12-2026 | [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/js.clearfake) |
| `diero.store` | Domain | ClearFake | 09-12-2026 | [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/js.clearfake) |
| `silvacheck.com` | Domain | Agent Tesla | 09-12-2026 | [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/win.agent_tesla) |
| `91.92.242.236/files-129312398/files/file_ddc6c6aa8ace95a7.ps1` | URL | Not classified | 09-12-2026 | [URLhaus entry](https://urlhaus.abuse.ch/url/3915605/) |
| `59.96.140.97:54883/i` | URL | Not classified | 09-12-2026 | [URLhaus entry](https://urlhaus.abuse.ch/url/3915604/) |

Compiled from public sources · 09-12-2026
