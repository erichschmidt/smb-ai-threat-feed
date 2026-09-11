---
type: threat-feed-note
title: "Threat Feed 09-11-2026"
status: published
tags: [threat-feed, daily, smb-ai-lens]
date: 09-11-2026
---

# Threat Feed — 09-11-2026

**Three-minute briefing:** Read the headlines and the [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md) entries to decide what needs attention today.

## How to read the scores

**EPSS** is a 0–1 score estimating how likely a flaw is to be exploited in the next 30 days; higher means patch first. Its percentile shows the rank against all known flaws: 99.5th percentile means more likely than 99.5% of them. **CVSS** is impact severity, not a prediction of active use. CISA KEV is the strongest signal here: it means active exploitation has been confirmed.

## 1. HIGH — Your LangChain database chatbot may let a prompt alter business data

**CVE-2024-8309 · LangChain GraphCypherQAChain · EPSS 0.1374 (96.28th percentile — more likely to be exploited than 96.28% of known flaws).**

**Sources:** [GitHub advisory](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) · [research disclosure](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5)

### What broke
A vulnerable LangChain component turns chat questions into database commands. Prompt injection (hidden instructions in text the AI reads) can steer it into SQL injection (tricking an app into running unauthorized database commands), allowing unauthorized changes, data exposure, or service disruption. The reported affected version is langchain-community 0.2.5.

**Attacker view, conceptually:** an attacker looks for a public-facing chat feature connected to a graph database, supplies a question that changes the generated query, then looks for unusual database writes or broad data reads.

### Why it matters to an SMB running AI tools
This is directly in the AI layer: a “chat with your data” tool linked to a graph database can become a path into the data store. The risk is higher where the chatbot has write permission instead of a read-only account.

### What you do Monday
1. **10 minutes:** In the project environment, run `pip show langchain-community` or check `requirements.txt` / `poetry.lock` for version 0.2.5.
2. If present, update to the vendor-fixed release identified in the [advisory](https://github.com/advisories/GHSA-45pg-36p6-83v9), rebuild the application, and run its normal chatbot test.
3. Change the chatbot database account to read-only unless writes are essential; review database audit logs for unexpected writes from the chatbot account.

## 2. CRITICAL — Your firewall control panel is being attacked; update it before the weekend

**CVE-2026-20079 · Cisco Secure Firewall Management Center and Security Cloud Control · EPSS 0.7470 (99.47th percentile — more likely to be exploited than 99.47% of known flaws).**

**Sources:** [Cisco advisory](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-onprem-fmc-authbypass-5JPp45V2) · [NVD record](https://nvd.nist.gov/vuln/detail/CVE-2026-20079)

### What broke
A login-bypass flaw lets an unauthenticated remote attacker reach functions in Cisco’s firewall-management products and execute script files. You do not need the implementation detail: if this management console is exposed or reachable by an attacker, it can become a route to changing the network controls that protect everything behind it.

### Why it matters to an SMB running AI tools
AI applications, model servers, and automation workers often sit behind firewall rules managed from this console. A compromise could expose internal AI endpoints, document stores, or service credentials by changing the boundaries around them.

### What you do Monday
1. **15 minutes:** Open the Cisco Secure Firewall Management Center → **System → Software Updates**; identify the installed release and compare it to the fixed release in the [Cisco advisory](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-onprem-fmc-authbypass-5JPp45V2).
2. Schedule the vendor update at the next approved maintenance window; if the console is internet-accessible, restrict its management access to the admin network first.
3. Ask the firewall owner: “Please confirm whether this console is internet-accessible, apply Cisco’s fix for CVE-2026-20079, and review recent administrator and configuration-change logs.”

**CISA active-exploitation signal:** CISA confirmed this is being actively exploited as of 09-09-2026. CISA requires federal agencies to patch by 09-12-2026. Known to be used in ransomware campaigns: Unknown.

## 3. CRITICAL — Your Citrix remote-access gateway has an active login bypass

**CVE-2026-19490 · Citrix NetScaler ADC and Gateway · EPSS 0.0600 (92.89th percentile — more likely to be exploited than 92.89% of known flaws).**

**Sources:** [Citrix advisory](https://support.citrix.com/external/article/CTX696939/netscaler-adc-and-netscaler-gateway-secu.html) · [NVD record](https://nvd.nist.gov/vuln/detail/CVE-2026-19490)

### What broke
A login bypass in the Citrix remote-access gateway can let a remote attacker reach protected functions without a valid login when certain gateway or authentication-server configurations are used. This is a front-door problem, not a theoretical browser bug.

### Why it matters to an SMB running AI tools
Remote staff and vendors may reach internal document systems and AI administration tools through this gateway. A gateway compromise can give an attacker a foothold before they try to reach the data sources or controls connected to those tools.

### What you do Monday
1. **10 minutes:** Sign in to the Citrix management console → **Configuration → System → Firmware** and record the installed build.
2. Match it against the fixed build in the [Citrix advisory](https://support.citrix.com/external/article/CTX696939/netscaler-adc-and-netscaler-gateway-secu.html), then install the update under the approved change process.
3. Review gateway login and administrator logs from 09-09-2026 onward for unexpected sessions; disable unneeded remote-access profiles.

**CISA active-exploitation signal:** CISA confirmed this is being actively exploited as of 09-09-2026. CISA requires federal agencies to patch by 09-12-2026. Known to be used in ransomware campaigns: Unknown.

## 4. HIGH — Your MikroTik router has two actively attacked paths to higher control

**CVE-2026-67277 and CVE-2026-86060 · MikroTik RouterOS · EPSS 0.0043 / 0.0040 (36.74th / 33.63rd percentile).**

**Sources:** [MikroTik September advisory](https://mikrotik.com/supportsec/september-2026-vulnerability/) · [CVE-2026-67277 NVD record](https://nvd.nist.gov/vuln/detail/CVE-2026-67277) · [CVE-2026-86060 NVD record](https://nvd.nist.gov/vuln/detail/CVE-2026-86060)

### What broke
One flaw lacks a required check before a sensitive RouterOS function; the other can let an attacker change a policy mask and gain higher privileges. Their EPSS scores are modest, but CISA has confirmed active exploitation, which outweighs a low prediction score for a specific exposed device.

### Why it matters to an SMB running AI tools
A router is the front door for cloud AI services, office networks, and automation devices. If it is compromised, an attacker can observe, redirect, or interrupt traffic between your people, data, and AI services.

### What you do Monday
1. **15 minutes:** Sign in to RouterOS → **System → Packages → Check For Updates**; install the current stable release specified by [MikroTik](https://mikrotik.com/supportsec/september-2026-vulnerability/).
2. In **IP → Services**, disable any management service not required and limit required services to known administrator IP addresses.
3. Review router administrator accounts and recent logins; remove unfamiliar accounts and rotate administrator passwords if anything is unexpected.

**CISA active-exploitation signal:** CISA confirmed both vulnerabilities are being actively exploited as of 09-10-2026. CISA requires federal agencies to patch both by 09-13-2026. Known to be used in ransomware campaigns: Unknown.

## Jargon buster

- **Firewall management console:** The control panel that sets and pushes firewall rules. If it is compromised, an attacker may be able to change the network boundaries that protect other systems.
- **LangChain:** A popular open-source framework developers use to build AI applications, including chatbots and “chat with your data” tools.
- **Login bypass:** A flaw that lets someone get past a login or permission check they should have had to pass.
- **Prompt injection:** Tricking an AI by putting instructions inside the data it reads, causing it to follow the attacker’s instructions instead of the user’s.
- **SQL injection:** Tricking an app into running unauthorized database commands through an input field or prompt.

## Appendix — raw signals

### CISA known-exploited vulnerabilities

| Rank by EPSS | Vulnerability | Product | EPSS / percentile | Added | Federal patch deadline | Ransomware use | Source |
|---:|---|---|---|---|---|---|---|
| 1 | CVE-2026-20079 | Cisco Secure Firewall Management | 0.7470 / 99.47th | 09-09-2026 | 09-12-2026 | Unknown | [Cisco](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-onprem-fmc-authbypass-5JPp45V2) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-20079) |
| 2 | CVE-2026-19490 | Citrix NetScaler | 0.0600 / 92.89th | 09-09-2026 | 09-12-2026 | Unknown | [Citrix](https://support.citrix.com/external/article/CTX696939/netscaler-adc-and-netscaler-gateway-secu.html) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-19490) |
| 3 | CVE-2026-75650 | Adobe Commerce and Magento | 0.0215 / 81.03rd | 09-08-2026 | 09-11-2026 | Unknown | [Adobe](https://helpx.adobe.com/security/products/magento/apsb26-146.html) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-75650) |
| 4 | CVE-2025-25249 | Fortinet products | 0.0170 / 75.79th | 09-09-2026 | 09-12-2026 | Unknown | [Fortinet](https://fortiguard.fortinet.com/psirt/FG-IR-25-084) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2025-25249) |
| 5 | CVE-2026-87491 | Chromium V8 | 0.0076 / 53.30th | 09-09-2026 | 09-23-2026 | Unknown | [Google](https://chromereleases.googleblog.com/2026/09/stable-channel-update-for-desktop_0808145027.html) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-87491) |
| 6 | CVE-2026-86218 | N-central | 0.0074 / 52.63rd | 09-08-2026 | 09-11-2026 | Unknown | [N-able](https://status.n-able.com/2026/09/06/n-central-2026-3-hotfix-4-cve-2026-86218/) · [advisory](https://me.n-able.com/s/security-advisory/aArVy0000002Ld3KAE/cve202686218-preauthentication-remote-code-execution) |
| 7 | CVE-2026-81963 | Microsoft Windows | 0.0063 / 48.19th | 09-08-2026 | 09-22-2026 | Unknown | [Microsoft](https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-81963) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-81963) |
| 8 | CVE-2026-85880 | Microsoft Windows | 0.0057 / 45.42nd | 09-08-2026 | 09-22-2026 | Unknown | [Microsoft](https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-85880) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-85880) |
| 9 | CVE-2026-67277 | MikroTik RouterOS | 0.0043 / 36.74th | 09-10-2026 | 09-13-2026 | Unknown | [MikroTik](https://mikrotik.com/supportsec/september-2026-vulnerability/) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-67277) |
| 10 | CVE-2026-86060 | MikroTik RouterOS | 0.0040 / 33.63rd | 09-10-2026 | 09-13-2026 | Unknown | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-86060) |

### Ransomware victim-claim pulse

| Group | Sector | Country | Discovered | Source |
|---|---|---|---|---|
| Panzer | Government & Defense | ES | 09-11-2026 | [Ransomware.live](https://www.ransomware.live) |
| Global Secret Group | Financial Services | IN | 09-10-2026 | [Ransomware.live](https://www.ransomware.live) |
| Vexy Ransomware | Technology | IN | 09-10-2026 | [Ransomware.live](https://www.ransomware.live) |
| play | Technology | Not listed | 09-10-2026 | [Ransomware.live](https://www.ransomware.live) |
| play | Manufacturing | CA | 09-10-2026 | [Ransomware.live](https://www.ransomware.live) |

Victim claims are attacker assertions, not independently verified incident reports.

### Notable CIRCL vulnerability signal

| Vulnerability | Product | EPSS / percentile | Why it stands out | Source |
|---|---|---|---|---|
| CVE-2024-8309 | LangChain GraphCypherQAChain | 0.1374 / 96.28th | AI database-chat prompt-to-query path; listed above | [GitHub advisory](https://github.com/advisories/GHSA-45pg-36p6-83v9) |

### IOC sample — block and hunt; do not visit

| Indicator | Type | Associated malware | Confidence | Seen | Source |
|---|---|---|---:|---|---|
| `escapeai.live` | Domain | AMOS | 100 | 09-11-2026 | [ThreatFox reference](https://malpedia.caad.fkie.fraunhofer.de/details/osx.amos) |
| `redirectwebpage.online` | Domain | ClearFake | 90 | 09-11-2026 | [ThreatFox reference](https://malpedia.caad.fkie.fraunhofer.de/details/js.clearfake) |
| `64.225.102.231:8080` | IP:port | Aisuru | 100 | 09-11-2026 | [ThreatFox reference](https://malpedia.caad.fkie.fraunhofer.de/details/elf.aisuru) |
| `http://117.95.20.161:56609/i` | URL | Not classified in packet | — | 09-11-2026 | [URLhaus entry](https://urlhaus.abuse.ch/url/3915287/) |

Compiled from public sources · 09-11-2026
