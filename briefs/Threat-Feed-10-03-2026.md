---
type: threat-feed-note
title: "Threat Feed - 10-03-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-10-03
updated: 2026-10-03
---

# Threat Feed - 10-03-2026

Plain-language cyber threat briefing for small businesses running artificial intelligence (AI) and automation. Headlines alone are the 3-minute read. A term is unfamiliar? It's defined right where it appears, and every term is spelled out in plain language in the [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md) at the bottom.

## How to read the scores

- **EPSS:** a 0-1 score estimating a vulnerability's odds of being exploited in the next 30 days. Higher = patch first. Percentile (e.g. 96th) = where that score ranks against all known vulnerabilities - 96th means it's more likely to be exploited than 96% of everything known.
- **KEV (Known Exploited Vulnerabilities catalog):** CISA's authoritative list of flaws actually being attacked right now - if it's there, it is not theoretical. CISA confirms an item's actual exploitation as of its "confirmed" date, and sets a federal-agency patch deadline (due date).
- **CVSS:** a 0-10 severity score for a flaw. 9.8/10 = critical - typically exploitable remotely with no login. "How bad if it works", while EPSS/KEV answer "is it actually being used".

---

## 1. HIGH - A popular "chat with your data" building block can be tricked into running database commands straight from a prompt - and the odds it's attacked soon are sky-high.

**CVE-2024-8309 - LangChain GraphCypherQAChain (langchain-community) - EPSS 0.1374 (96th percentile - higher exploitation likelihood than 96% of all known flaws)**

**What broke:** LangChain is a very widely used open-source toolkit for building AI applications, including "ask your database" assistants. One of its helpers, GraphCypherQAChain, turns a plain-English question into a query against a graph database (a database that stores records and their relationships as connected points - the kind many AI apps use to answer questions about linked business records). Because of how it builds that query, an attacker can hide instructions inside the text a user or a document feeds the AI, and the chain will run a malicious database query the developer never intended - altering, deleting, or copying out data it was never supposed to touch (SQL injection through prompt injection).

**Why it matters to an SMB running AI tools:** If your team built - or a vendor built for you - an AI assistant that answers questions by querying your customer or product data, this helper may be the engine under it. The danger is that the attack travels through the normal input path: a poisoned prompt in a document, a message, a web form. One crafted question turns your "chat with the data" tool into a tool that leaks or destroys that same data. At 96th-percentile exploitation likelihood, this is the thing to check first.

*Attacker view (conceptual):* an attacker targets an exposed assistant, finds where a user-supplied or document-supplied value flows into the database query, and injects a crafted snippet that changes what the query does - then asks the assistant to run it, reading or writing records well beyond their permission. The observables are unusually shaped database queries and audit-log entries on the graph database. A safe lab test with a disposable database is the right way to confirm your own exposure.

**What you do Monday:**
1. Check your AI project dependencies for `langchain-community` and confirm the version (the affected line is 0.2.5 and nearby builds): in your project, run `pip show langchain-community` or search `requirements.txt` (15 minutes).
2. Update to a patched release that fixes the query construction, and re-test the assistant against a throwaway copy of your data, never production (1 hour).
3. Limit the database account this chain connects with to read-only where possible - least privilege - so even a successful injected query can't change or delete records (30 minutes).

**Sources:** [GitHub advisory GHSA-45pg-36p6-83v9](https://github.com/advisories/GHSA-45pg-36p6-83v9) - [Huntr report](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5) - [Fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255)

---

## 2. HIGH - Your self-hosted customer-support tool has two flaws already being attacked - one lets an outsider escalate all the way to full server control.

**CVE-2026-102489 & CVE-2026-102490 - Zammad - added to CISA KEV 10-02-2026 - federal patch deadline 10-05-2026 - actively exploited per CISA - EPSS 0.0058 (46th) and 0.0026 (16th)**

**What broke:** Zammad is an open-source customer-support / helpdesk system that many small businesses run on their own server to manage support tickets. Two flaws were added to CISA's exploited list together. One is a session-fixation bug - an attacker can pin a victim to a login session the attacker controls, so when the victim signs in the attacker inherits that session - which can lead to remote code execution (the attacker runs their own code on the machine) as the "zammad" user. The second is an improper-privilege-management flaw that lets that same account escalate to root (the highest, full-control level of a Linux system). Chained, they're a step-by-step path from a poisoned login to total server takeover.

**Why it matters to an SMB running AI tools:** Your helpdesk holds every support conversation, customer record, and often the attachments and email threads your team shares. If you run email-to-ticket automation or have started an AI assistant that reads tickets to draft answers, this inbox is also a data source your AI reads. An attacker with root on this box reads all of it, and can quietly alter what your support AI sees before it answers. Note the lesson here: EPSS says "maybe soon," but KEV says "already today" - when CISA confirms active exploitation, EPSS no longer matters; patch now.

**What you do Monday:**
1. Follow Zammad's upgrade instructions to the patched release containing both fixes (60-90 minutes). You'll find the releases page and the community advisory linked in Sources below.
2. After upgrading, change the account password and rotate any API tokens that authenticating through the web portal may have been exposed to (30 minutes).
3. Review Zammad's logs for logins or changes in the window before you patched, so you catch it if the box was already hit (30-45 minutes).

**Sources:** [CISA alert - two KEV additions](https://www.cisa.gov/news-events/alerts/2026/10/02/cisa-adds-two-known-exploited-vulnerabilities-catalog) - [Zammad releases](https://zammad.com/en/product/releases/) - [Zammad community advisory](https://community.zammad.org/t/take-care-local-privilege-escalation-cve-2026-102490-is-reported-as-being-actively-exploited/21297/2)

---

## 3. HIGH - The console that routes your branch sites to your cloud tools must be patched by today - unauthenticated full admin access.

**CVE-2026-76504 - Cisco Catalyst SD-WAN Manager - added to CISA KEV 09-30-2026 - federal patch deadline 10-03-2026 (today) - EPSS 0.0158 (75th percentile)**

**What broke:** Cisco Catalyst SD-WAN Manager - the control console that configures and routes traffic across a company's wide-area network links - mishandles hex encoding in an HTTP request. That lets an unauthenticated remote attacker reach the system with the privileges of the admin user, i.e. full control of your WAN routing, no login needed.

**Why it matters to an SMB running AI tools:** SD-WAN is the pipe your office traffic rides on - including the connections between your staff, your cloud apps, and your AI/automation tooling. Whoever owns this console can reroute, intercept, or cut that traffic. A hole in the console is a hole between your people and the AIs they depend on. Today's federal deadline means this one is treated as urgent.

**What you do Monday:**
1. In SD-WAN Manager → System → Software Update, apply the latest patch (1 hour).
2. If you can't patch today, restrict internet-facing access to the Manager console to trusted admin IPs only (30 minutes).
3. If you have branch sites, confirm the update reaches every manager, not just the primary one (30 minutes).

**Sources:** [Cisco advisory](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-sdwan-webauth-xr8beuuU) - [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-76504)

---

## 4. WATCH - If you did not patch your mail-appliance hole yesterday, it is still being exploited and the deadline is tomorrow.

**CVE-2026-104286 - Fortinet FortiMail - added to CISA KEV 10-01-2026 - federal patch deadline 10-04-2026 (tomorrow) - EPSS 0.0178 (77th percentile - highest in today's exploited list)**

**What broke:** FortiMail is the appliance many offices use to filter and route their business email. A bundled pair of flaws - a path traversal (a request that climbs out of the folder it should stay in) plus poor NULL-byte handling - lets an unauthenticated attacker write arbitrary files onto the underlying server via crafted HTTP/HTTPS requests. No login required, and it's the most-likely-to-be-exploited item on today's list.

**Why it matters to an SMB running AI tools:** Email is the front door for prompt injection and automation poisoning. Your AI inbox/summarizer bots and "mail → CRM/document" automations read whatever ends up in that mailbox. An attacker who can plant files on the mail appliance is one step from feeding your AI pipeline attacker-controlled content - and from hijacking the box your team depends on every day.

**What you do Monday:**
1. In your FortiMail console, apply the vendor's recommended mitigation / hotfix per FG-IR-26-175 (30-60 minutes).
2. If it still can't be patched, keep the management interface off the public internet (admin-IP-only access) until it is (30 minutes).
3. Run Fortinet's supplied indicators of compromise on the appliance to check whether it was already hit (15 minutes).

**Sources:** [Fortinet advisory FG-IR-26-175](https://fortiguard.fortinet.com/psirt/FG-IR-26-175) - [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-104286)

---

## Jargon buster

- **Arbitrary code execution:** Running attacker-supplied code as if it were part of the program - effectively taking over the machine.
- **EPSS (Exploit Prediction Scoring System):** a 0-1 score estimating how likely a vulnerability is to be exploited in the next 30 days. Higher = patch first.
- **Graph database:** a database that stores things and their relationships as connected points. AI tools may query it to answer questions about linked business records.
- **GraphCypherQAChain:** LangChain's helper that turns a chat question into a graph-database query. If that query isn't locked down, the chat becomes a database write.
- **KEV (Known Exploited Vulnerabilities):** CISA's authoritative list of flaws actually being exploited right now - it's the "real right now" signal, not theory.
- **Language model / LangChain:** the open-source framework developers use to build AI chat and "chat with your data" tools; LangChain is one of the most common, so flaws in it affect many AI apps at once.
- **Least privilege:** giving a software account only the access it needs for its job, and no more.
- **Path traversal:** a flaw where a request with special ".." paths lets an attacker escape the intended folder and touch files elsewhere on the system.
- **Privilege escalation:** gaining higher system access rights (like administrator or root) than originally authorized.
- **Prompt injection:** an attack that slips instructions into data the AI reads, so the AI acts on the attacker's text as if it were a legitimate command.
- **Remote code execution (RCE):** an attacker can run their own code on the machine from anywhere - "game over," full control.
- **Root:** the highest level of access on a Linux/Unix system - the equivalent of "administrator" on Windows. Root means the attacker owns the machine.
- **SD-WAN:** software-defined wide-area network - the technology offices use to route traffic between branch sites and the cloud.
- **Session fixation:** an attacker pins a victim to a login session the attacker controls; when the victim signs in, the attacker inherits that session.
- **SQL injection:** a technique where attackers type malicious database commands into an input (or a prompt), tricking the app into running unauthorized queries - reading, changing, or deleting data.
- **Zammad:** an open-source customer-support / helpdesk ticketing system some small businesses run on their own server; it holds support conversations and tickets.

---

## Appendix

### A. KEV catalog this week (ranked by EPSS - highest exploitation likelihood first)

| CVE | Product | CISA confirmed | Federal patch by | EPSS (percentile) | Ransomware use | Source |
|---|---|---|---|---|---|---|
| CVE-2026-104286 | Fortinet FortiMail | 10-01-2026 | 10-04-2026 | 0.0178 (77th) | Unknown | [Fortinet](https://fortiguard.fortinet.com/psirt/FG-IR-26-175) |
| CVE-2026-76504 | Cisco Catalyst SD-WAN Manager | 09-30-2026 | 10-03-2026 | 0.0158 (75th) | Unknown | [Cisco](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-sdwan-webauth-xr8beuuU) |
| CVE-2026-88772 | Citrix NetScaler ADC / Gateway | 09-27-2026 | 09-30-2026 | 0.013 (69th) | Unknown | [Citrix](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697096) |
| CVE-2026-86950 | Apple iOS/macOS/iPadOS CoreGraphics | 09-29-2026 | 10-02-2026 | 0.0124 (68th) | Unknown | [Apple](https://support.apple.com/en-us/149226) |
| CVE-2026-88771 | Citrix NetScaler Gateway | 09-27-2026 | 09-30-2026 | 0.0106 (63rd) | Unknown | [Citrix](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697096) |
| CVE-2026-102489 | Zammad (session fixation / RCE) | 10-02-2026 | 10-05-2026 | 0.0058 (46th) | Unknown | [CISA alert](https://www.cisa.gov/news-events/alerts/2026/10/02/cisa-adds-two-known-exploited-vulnerabilities-catalog) |
| CVE-2026-102490 | Zammad (privilege escalation) | 10-02-2026 | 10-05-2026 | 0.0026 (16th) | Unknown | [CISA alert](https://www.cisa.gov/news-events/alerts/2026/10/02/cisa-adds-two-known-exploited-vulnerabilities-catalog) |

### B. Ransomware sector pulse
- **rhysida** claimed a Vietnamese cloud-hosting / domain-registrar (Technology sector) and a Swedish industrial-furnace maker (Energy & Utilities, with 2.55 TB of SolidWorks CAD designs claimed stolen). Shows the "hosting provider" and "manufacturing" angles hitting SMB-scale operations. [Ransomware.live](https://www.ransomware.live)
- **qilin** appeared against a transportation firm in Thailand and a German manufacturer. **Spirals** claimed a UAE maritime/ship-supplies group (Transportation). [Ransomware.live](https://www.ransomware.live)
- **Booba Project** posted a batch including US higher-education (344 GB), plus US/CA healthcare and a medical-device firm - a reminder that education and medical records stay prime targets. [Ransomware.live](https://www.ransomware.live)

*Treat all victim claims as unverified attacker assertions - useful as "this sector is being hunted" signals, not as confirmed incidents.*

### C. Notable CIRCL findings (higher EPSS first / on-lens first)
- **LangChain GraphCypherQAChain (CVE-2024-8309)** - SQL injection through prompt injection; the strongest on-lens item of the day. EPSS 0.1374 (96th). Covered as item 1. [GitHub advisory](https://github.com/advisories/GHSA-45pg-36p6-83v9)
- **Picklescan (CVE-2025-1889)** - AI model-file scanner bypass via non-standard file extension; covered 10-02 as item 1. Still worth confirming your scanner is 0.0.22+. EPSS 0.004 (31st). [GitHub advisory](https://github.com/advisories/GHSA-769v-p64c-89pr)
- The rest of today's CIRCL feed is dominated by low-EPSS Linux-kernel hardening fixes (pmem, mt76 wifi firmware, nvme-rdma, btrfs, Bluetooth, etc.) - patching signal for server admins, not SMB-priority items.

### D. IOC sample (block-and-hunt signals - do not visit)
- **ClearFake** (fake browser-update malware): domains `9d24355d.pattysole.com`, `6b2e76df.pattysole.com` - [Malpedia ClearFake](https://malpedia.caad.fkie.fraunhofer.de/details/js.clearfake)
- **Mirai** (camera/router botnet): seven captured SHA-256 file hashes on today's feed, including `b917460b2f8c5ccc99d24bef30b04011618c75ee9563bd3f5fed003ac90be065` - [Malpedia Mirai](https://malpedia.caad.fkie.fraunhofer.de/details/elf.mirai)
- **URLhaus recent payload URLs** (block, do not visit): `http://45.183.184.74:49148/i` - [URLhaus 3927649](https://urlhaus.abuse.ch/url/3927649/) | `http://222.137.144.228:57187/i` - [URLhaus 3927644](https://urlhaus.abuse.ch/url/3927644/)

---

*Compiled from public sources · 10-03-2026*
