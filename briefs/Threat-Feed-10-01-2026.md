---
type: threat-feed-note
title: "Threat Feed - 10-01-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-10-01
updated: 2026-10-01
---

# Threat Feed - 10-01-2026

Plain-language cyber threat briefing for small businesses running artificial intelligence (AI) and automation. Headlines alone are the 3-minute read. A term is unfamiliar? It's defined right where it appears,and every term is spelled out in plain language in the [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md)at the bottom.



## How to read the scores

- **EPSS**:a 0-1 score estimating a vulnerability's odds of being exploited in the next 30 days. Higher = patch first. Percentile(e.g. 97th) = where that score ranks against all known vulnerabilities - 97th means it's more likely to be exploited than 97% of everything known.
- **KEV (Known Exploited Vulnerabilities) catalog**:CISA's authoritative list of flaws actually being attacked right now - if it's there,it is not theoretical. CISA confirms an item's actual exploitation as of its"confirmed" date,and setsa federal-agency patch deadline(due date..
- **CVSS**:a 0-10 severity score fora flaw. 9.8/10 = critical - typically exploitable remotely with no login. "How bad if it works",while EPSS/KEV answer "is it actually being used".



---

## 1. HIGH - An AI "chat with your data" tool can be tricked into running malicious database commands.



**CVE-2024-8309 - LangChain GraphCypherQAChain - published 2024-11-05 - EPSS 0.1274(96th percentile)**

**What broke:** A popular building block for AI assistants leaks a way to smuggle attacker commands into its database queries. Specifically,a helper in the widely used LangChain framework converts a chat question into a database search. If the conversation or data it digests contains malicious SQL(a prompt injection attack,that search can become an unauthorized read,change,or delete of your records.



**Why it matters to an SMB running AI tools:** If your AI assistant uses LangChain's graph-database helper(GraphCypherQAChain)to answer questions fromyour business records,an attacker whocan get malicious text into whatthe AI reads(e.g. insidea document,email,or chat message)can turn that assistant intoa channel intoyour database. This is squarely in the"AI is the attack surface" class - not the AI just summarizing,butthe AI directly wired intoyour data store.



**What you do Monday:**
1. Update the LangChain / LangChain-community library toa fixed release per vendor instructions:`pip install -U langchain-community`(10 minutes..2. Ifyou can't update today,disconnectthe graph-database query helper from untrusted inputs,and only let vetted,staff-approved data reach it(30 minutes..3. Ask your developer or AI-vendor to confirm which LangChain version your chatbot deployments use(15 minutes..



**Sources:** [GitHub advisory(GHSA-45pg-36p6-83v9)](https://github.com/advisories/GHSA-45pg-36p6-83v9) - [Fix commit in LangChain](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c258) - [Huntr report](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5)



---

## 2. CRITICAL - Your website's engine hasa hole that lets attackers run their own code - patch it today.



**CVE-2026-87902 - WordPress Core - CISA confirmed 09-25-2026 - federal patch deadline 09-28-2026 - EPSS 0.1976(97th percentile - more likely to be exploited than 97% of known flaws)**

**What broke:** A remote file inclusion flaw in WordPress Core - the engine behind a large share of small-business websites - lets an unauthenticated attacker make the site load a chosen readable file,and then run its code,effectively gaining remote code execution(RCE - an attacker can run their own code on your machine)possession of the server.



**Why it matters to an SMB running AI tools:** So many micro-businesses run their site,online store,and AI-driven web chatbot / search widget from WordPress. If an attacker takes over the site,the code the AI tools scrape"read" is now attacker-controlled - poisoned content thatyour AI assistant will then quoteback to you and customers as if it were trustworthy.



**What you do Monday:**
1. In your WordPress dashboard:Dashboard - Updates - Update Now(or via wp-admin - Update Core.. If your host manages core,request it(10 minutes..2. Confirm core is on the latest version:Dashboard - Updates(5 minutes..3. If you're not certain you run WordPress,ask your web host"Has WordPress Core CVE-2026-87902 been patched?"(10 minutes..



**Sources:** [WordPress security advisory(GHSA-7hp8-65ch-5whp)](https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-7hp8-65ch-5whp) - [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-87902)



---

## 3. HIGH - Your remote-access appliance hastwo holes attackers are actively using - update it now.



**CVE-2026-88772 & CVE-2026-88771 - Citrix NetScaler ADC / NetScaler Gateway - CISA confirmed 09-27-2026 - federal patch deadline 09-30-2026 - EPSS 0.013and 0.0106**

**What broke:** Citrix NetScaler - the appliance many offices use as their VPN and website front door - carries two actively exploited flaws: one lets an unauthenticated remote attacker run their own code or knock the service offline(a remote code execution / denial of service bug,and another lets an unauthenticated attacker execute arbitrary commands on the box.



**Why it matters to an SMB running AI tools:** NetScaler oftenfrontsthe appsyour remote workers-and AI assistants- reachto get at business systems. A hole here isa holein the front door of everything behind it:your customer records,your file vault,the connectors and databasesyour AI stack readsand writes. Patch this box before it becomesa doorway.



**What you do Monday:**
1. Log intothe NetScaler management console and apply Citrix's latest recommended hotfix(see Sources below - 30-60 minutes..2. If it can't be patched immediately,at minimum ensurethe appliance isnot exposed directlytothe internet - put it behinda firewall / restrict source IPs(30 minutes..3. Run Citrix's published indicators-of-compromise commandson the console to check forprior intrusion(15 minutes..



**Sources:** [Citrix support article(CTX697096)](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697096) - [Citrix NetScaler intrusion steps](https://support.citrix.com/external/article/CTX694799/steps-to-take-if-netscaler-adc-is-suspec.html)



---

## 4. HIGH - The console that manages your branch-office network can be taken overbyan unauthenticated attacker..



**CVE-2026-76504 - Cisco Catalyst SD-WAN Manager - CISA confirmed 09-30-2026 - federal patch deadline 10-03-2026**

**What broke:** Cisco's Catalyst SD-WAN Manager -the console that configuresand routes traffic acrossan office's wide-area-network links - hasa hex-decoding flaw that letsun unauthenticated remote attacker reachthe system withthe rights of its admin user. Gainingthat level of controlmeans doing whateverthe admin can do.



**Why it matters to an SMB running AI tools:** The SD-WAN control plane handsand reroutesthe trafficyour office relieson - includingthe connections between your staff,your cloud apps,andyour AI / automation tooling. Compromise it,andan attacker can reroute or intercept that traffic,standing betweenyour peopleandthe AIs they dependon.



**What you do Monday:**
1. In the SD-WAN Manager Dashboard - System - Software Update - applythe available patch(1 hour..2. If you can't patch immediately,restrictany internet-facing accesstothe Manager console to trusted admin IPs only(30 minutes..3. If you have multiple branch sites,confirmthe update rollsout to all managers,not justthe primaryone(30 minutes..



**Sources:** [Cisco advisory](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-sdwan-webauth-xr8beuuU) - [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-76504)



---

## 5. WATCH - Your Macs and iPhones havea graphics bug that's being exploited - update Apple devices.



**CVE-2026-86950 - Apple iOS / macOS / iPadOS CoreGraphics - CISA confirmed 09-29-2026 - federal patch deadline 10-02-2026 - EPSS 0.0081(45th percentile)**

**What broke:** An out-of-bounds write flaw in CoreGraphics - Apple's graphics engine that draws what's on your screen - can be turned into arbitrary code execution(running attacker code on the device. It spans iPhones,Macs,and iPads at once.



**Why it matters to an SMB running AI tools:** Your AI assistants - Copilot,notebooks,and"ask your files" tools - run onthese very devices. If device is compromised,an attacker can tap the data your assistant readsandthe conversationsyou typeto it. Device compromise is assistant compromise.



**What you do Monday:**
1. iPhone/iPad:Settings - General - Software Update - Update Now(20 minutes..2. Mac:System Settings - General - Software Update - Update Now(20 minutes..3. If you managea device fleet,push the update via your management tool as soon as user availability allows(30-60 minutes..



**Sources:** [Apple support(149226)](https://support.apple.com/en-us/149226) - [Apple support(149228)](https://support.apple.com/en-us/149228) - [Apple support(149229)](https://support.apple.com/en-us/149229)



---

## Jargon buster

- **Arbitrary code execution:** Running attacker-supplied code as if it were part of the program - effectively taking over the machine..
- **Denial of service(DoS):** The service stops answering,so nobody gets in - including you. Different from ransomware;this one just knocks the door down..
- **EPSS(Exploit Prediction Scoring System):** a 0-1 score estimating how likely a flaw is to be exploited soon. Higher = patch first..
- **Remote file inclusion(RFI):** Tricking a server into loading a file the attacker chose - often a step toward running their own code..
- **NetScaler ADC / NetScaler Gateway:** Citrix's appliance that is often the VPN and website front door. A hole here is a hole in remote access and anything behind it..
- **Out-of-bounds write:** A memory bug where software writes past the space it allocated for data. Attackers use it to crash a service or,in the right conditions,run their own code..



---

## Appendix

### A. KEV actively-exploited vulnerabilities this week(ranked by EPSS - highest exploitation likelihood first)

| CVE | Product | EPSS(percentile |CISA confirmed |Federal patch by |Source |
|---|---|---|---|---|---|
| CVE-2026-87902 | WordPress Core |0.1976(97th|09-25-2026 |09-28-2026 |[Advisory](https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-7hp8-65ch-5whp)|
| CVE-2026-65660 | Microsoft SharePoint |0.021(81st|09-25-2026 |09-28-2026 |[MSRC](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-65660)|
| CVE-2026-88772 | Citrix NetScaler |0.013(69th|09-27-2026 |09-30-2026 |[Citrix](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697096)|
| CVE-2026-88771 | Citrix NetScaler |0.0106(63rd|09-27-2026 |09-30-2026 |[Citrix](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697096)|
| CVE-2026-67279 | MikroTik RouterOS |0.0103(62nd|09-25-2026 |09-28-2026 |[MikroTik](https://mikrotik.com/supportsec/september-2026-vulnerability/)|
| CVE-2026-86950 | Apple CoreGraphics |0.0081(45th|09-29-2026 |10-02-2026 |[Apple](https://support.apple.com/en-us/149226)|
| CVE-2026-76504 | Cisco Catalyst SD-WAN Manager |n/a |09-30-2026 |10-03-2026 |[Cisco](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-sdwan-webauth-xr8beuuU)|

SharePoint(CVE-2026-65660):a code-injection flaw lettingan authorized attacker executecode overa network - ifyour business livesin Microsoft's document intranet,patch it,because it's often the libraryyour"chat withyour files" Copilot-style tools read..



### B. Ransomware sector pulse

No new ransomware-victim data was retrievable today -the source query failed. Treat thisasa gapin visibility,nota clean billof health..



### C. Notable CIRCL findings(higher EPSS first)



| ID | What it is | EPSS |
|---|---|---|---|
| PYSEC-2024-115(CVE-2024-8309)|LangChain graph-database query helper SQL-injection via prompt injection - coveredas item 1|0.1374(96th|
| PYSEC-2025-19(CVE-2025-1889)|A scan tool for catching malicious Python model files(picklescan)was incomplete - malicious model fileswith unusual extensions could slip past it. Ifyou load AI model files from outside,weigh this when choosing a model-safety scanner.|0.004(31st|



### D. IOC sample(block-and-hunt signals - do not visit)

- **ClearFake** fake-update malware:domain`brambly.world` - [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/js.clearfake).
- **Mirai** botnet:5 file hashes captured this run - [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/elf.mirai.
..
- **Botnet payload URLs**(URLhaus:`http://94.154.43.84/mips`,`http://42.54.144.76:56600/bin.sh`,`http://60.23.237.178:53274/bin.sh` - [URLhaus](https://urlhaus.abuse.ch/url/3926300/),[URLhaus](https://urlhaus.abuse.ch/url/3926302/..



---

*Compiled from public sources - 10-01-2026*