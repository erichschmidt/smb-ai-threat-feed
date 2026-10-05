---
type: threat-feed-note
title: "Threat Feed - 10-05-2026"
status: published
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-10-05
updated: 2026-10-05
---

# SMB + AI Threat Feed — 10-05-2026

**Reader promise (3-minute read):** Adversaries are harder and AI tools are here to stay. Read the headlines — each is one plain sentence with a fix. If a term is new, [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md) explains it in one line. No jargon required.

## How to read the scores

- **EPSS** is a 0–1 score estimating how likely a flaw is to be exploited in the next 30 days. Higher = patch first. The **percentile** shows where it ranks vs all known flaws: 96th percentile means it's in the top 4% most likely to be exploited.
- **CISA KEV** = CISA confirmed the flaw is being actively exploited right now. If it's on this list, it's not theoretical — patch it.
- **CVSS** is a 0–10 "how bad if it works" severity. 9.8/10 = critical, exploitable remotely with no login.

---

## 1. HIGH — A bug in a popular AI chat framework lets a crafted question reach into your database

**CVE-2024-8309** · EPSS 0.1374 (96.4th percentile — in the top ~4% most likely to be exploited) · CVSS 9.8/10 (critical, remote, no login)

**What broke.** LangChain (a widely used open-source framework for building AI apps that answer questions from your data) shipped a flaw in its graph-database query helper. An attacker who can ask the AI a question — through your chatbot, your support widget, or any "chat with your data" tool built on this library — can plant SQL injection (type malicious database commands into the input) that reads, changes, or deletes data the chat was never meant to touch.

**Why it matters to an SMB running AI tools.** If you run any RAG (Retrieval-Augmented Generation — the standard way AI tools answer from your own files) app built on LangChain's graph helper, the "talk to your business data" feature is the attack surface. A malicious prompt buried in a document or submitted to the chat can reach the database the model answers from — the customers, orders, and records feeding your AI.

**What you do Monday.**
1. Find which LangChain packages your AI apps use: check `pip freeze` or your app's dependency list for `langchain-community`. (10 minutes)
2. If you're on `langchain-community` 0.2.5 or earlier, update to the patched version that includes the fix commit. (20 minutes)
3. Restrict the graph-database account your AI uses to read-only, so even a successful injection can't write or delete.

**Sources:** [huntr advisory](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5) · [GitHub Security Advisory](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [Fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255)

---

## 2. WATCH — Your AI model safety scanner silently skips files that don't end in the standard extension

**CVE-2025-1889** · EPSS 0.004 (low likelihood of wide exploitation — a development-tool gap, not a live wildfire) · CVSS 9.8/10 (critical "if it works")

**What broke.** picklescan (a scanner that checks downloaded AI model files for dangerous code before you load them) only looked at files with standard model extensions. An attacker can rename a malicious model file with a non-standard extension, and the scanner skips it entirely. Loading it can run the attacker's code on your machine. This is a deserialization class risk.

**Why it matters to an SMB running AI tools.** If your team pulls open-source AI models — from Hugging Face or elsewhere — and scans them before loading, this gap means the scan can be a false sense of security. A renamed malicious model is exactly the kind of software supply chain ambush (a poisoned third-party package) you put the scanner in place to stop.

**What you do Monday.**
1. Update the `picklescan` package to 0.0.22 or later, which scans all files regardless of extension. (10 minutes)
2. In your model-download workflow, prefer the `safetensors` file format, which doesn't run code on load. (30 minutes)
3. Only load models from sources you trust; treat any `.pkl` / `.pt` file like an unknown program.

**Sources:** [GitHub Security Advisory](https://github.com/advisories/GHSA-769v-p64c-89pr) · [Sonatype advisory](https://sites.google.com/sonatype.com/vulnerabilities/cve-2025-1889)

---

## 3. HIGH — Your Citrix remote-access gateway has a hole under active attack — patch it this week

**CVE-2026-88779** · EPSS 0.0028 (low odds score — but it's already on the actively-exploited list) · CISA confirmed actively exploited as of **10-04-2026** · CISA requires federal agencies to patch by **10-07-2026**

**What broke.** Citrix NetScaler ADC / Gateway (the appliance many businesses use as the VPN and web front door for remote workers) has a memory-handling flaw that lets an attacker crash the service or disrupt access. CISA added it to its Known Exploited Vulnerabilities list because attackers are already using it.

**Why it matters to an SMB running AI tools.** NetScaler sits in front of everything remote users reach — and that now includes your AI tools, chat-with-data apps, and automation consoles that staff access from home. If an attacker knocks out the gateway or gets a foothold beside it, the door to those remote-access surfaces weakens. Treat the actively-exploited confirmation as "patch now," not "keep an eye on it."

**What you do Monday.**
1. Check your Citrix NetScaler version against the vendor advisory (KB article CTX697174). (15 minutes)
2. Apply the vendor patch — Citrix lists the fixed builds in the advisory; if you can't patch immediately, apply the vendor's interim mitigation. (1–2 hours)
3. Review VPN and remote-access logs for odd logins or dropped sessions in the past week. (30 minutes)

**Sources:** [Citrix KB CTX697174](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697174) · [Citrix tech-zone analysis](https://community.citrix.com/techzone-blogs/110_security-updates/understanding-and-addressing-cve-2026-88779-in-citrix-netscaler-adc-and-citrix-netscaler-gateway/)

---

## 4. HIGH — Your email security gateway lets an outsider write files onto its server — patch now

**CVE-2026-104286** · EPSS 0.022 (81.9th percentile — more likely to be exploited than ~82% of known flaws) · CISA confirmed actively exploited as of **10-01-2026** · CISA requires federal agencies to patch by **10-04-2026**

**What broke.** Fortinet FortiMail (an email security gateway many SMBs put in front of their mail server) contains a path traversal (a trick where an attacker types `../` in a file path to reach files they shouldn't) plus a null-byte handling flaw. Together they let an **unauthenticated attacker** (no login) write arbitrary files to the underlying system via crafted web requests — a step toward full takeover.

**Why it matters to an SMB running AI tools.** FortiMail inspects your inbound and outbound email — the same mail your AI assistants and notification automations read and file. If an attacker writes files onto the gateway, they can plant backdoors, tamper with the mail the AI trusts, or pivot to the mailboxes it serves. An email gateway hole is a hole in everything that reads your mail, including AI mail tools.

**What you do Monday.**
1. Check your FortiMail version against the advisory FG-IR-26-175; apply the fixed firmware. (1 hour)
2. If you can't patch immediately, restrict or block untrusted HTTPS access to the FortiMail management/HTTP interface. (20 minutes)
3. Verify email-gateway logs for unexpected web requests or file writes in the past week. (30 minutes)

**Sources:** [Fortinet advisory FG-IR-26-175](https://fortiguard.fortinet.com/psirt/FG-IR-26-175) · [NVD entry](https://nvd.nist.gov/vuln/detail/CVE-2026-104286)

---

## 5. HIGH — Your helpdesk tool can be taken over and give attackers full server control — update today

**CVE-2026-102489 + CVE-2026-102490** · EPSS 0.014 (71.5th percentile) / 0.0063 (48th percentile) · CISA confirmed actively exploited as of **10-02-2026** · CISA requires federal agencies to patch by **10-05-2026**

**What broke.** Zammad (an open-source helpdesk / customer-support ticketing system some small businesses run on their own server) has a pair of flaws that work together: a **session fixation** attack (pinning a victim to a login session the attacker controls) that leads to remote code execution as the app user, chained with a privilege escalation (gaining higher system access rights) that lifts the attacker to **root** (full server control). CISA added both to its actively-exploited list.

**Why it matters to an SMB running AI tools.** Zammad holds your support conversations, tickets, and customer records — and often feeds email-to-ticket and support-AI automations. Give an attacker root on that box and they own the support history, the customers in it, and whatever the helpdesk's AI integrations can reach.

**What you do Monday.**
1. Go to your Zammad install and update to the latest release: the vendor's fix is in the current release notes. (30 minutes)
2. Confirm no local account was added and no odd support-'admin' account exists after the update. (15 minutes)
3. Rotate any passwords or tokens the helpdesk holds if you suspect it was exposed. (30 minutes)

**Sources:** [Zammad releases](https://zammad.com/en/product/releases/) · [Zammad community advisory](https://community.zammad.org/t/take-care-local-privilege-escalation-cve-2026-102490-is-reported-as-being-actively-exploited/21297/2)

---

## Jargon buster

- **EPSS:** A 0–1 score estimating how likely a flaw is to be exploited in the next 30 days; higher = patch first. Percentile = where it ranks vs all known vulnerabilities.
- **Kev / CISA KEV:** CISA's list of vulnerabilities confirmed to be actively exploited right now — not theoretical.
- **SQL injection:** Typing malicious database commands into an input (or a prompt), tricking the app into running unauthorized queries.
- **Prompt injection:** Tricking an AI by putting instructions inside the data it reads; it follows the attacker's instructions instead of the user's.
- **RAG (Retrieval-Augmented Generation):** The standard way AI tools answer from your own files — it retrieves relevant documents, then answers from them.
- **Deserialization:** Turning a saved data blob back into a live program object; if the blob is attacker-controlled, that "restore" can run their code.
- **Software supply chain:** The code packages and services you depend on; a problem in one can affect every application that pulls from it.
- **Path traversal:** A trick where an attacker types `../` in a file path to reach files they shouldn't.
- **Unauthenticated (attacker):** Someone with no login credentials.
- **Session fixation:** Pinning a victim to a login session the attacker controls; when the victim signs in, the attacker inherits that session.
- **Privilege escalation:** Gaining higher system access rights than originally authorized.
- **Root:** The highest level of access on a Linux/Unix system — full control.
- **RCE (Remote Code Execution):** An attacker can run their own code on your machine from anywhere.
- **CVSS:** A 0–10 severity score; 9.8/10 = critical, exploitable remotely with no login.
- **DoS (Denial of service):** The service stops answering so nobody gets in — including you.
- **Graph database:** A database storing things and their relationships as connected points; AI tools may query it to answer questions about linked records.
- **GraphCypherQAChain:** LangChain's helper that turns a chat question into a graph-database query; if the query isn't locked down, the chat becomes a database write.
- **picklescan:** A scanner meant to catch dangerous Python model files in AI downloads.
- **NetScaler ADC / Gateway:** Citrix's appliance that is often the VPN and website front door.
- **FortiMail:** Fortinet's email security gateway.
- **Zammad:** An open-source customer-support / helpdesk ticketing system some small businesses self-host.

---

## Appendix

### Active exploits added or updated this week (CISA KEV), ranked by EPSS

| CVE | Product | EPSS (percentile) | CISA added | Federal deadline | Ransomware used | Source |
|---|---|---|---|---|---|---|
| CVE-2026-104286 | Fortinet FortiMail | 0.022 (81.9) | 10-01-2026 | 10-04-2026 | Unknown | [Fortinet](https://fortiguard.fortinet.com/psirt/FG-IR-26-175) |
| CVE-2026-76504 | Cisco Catalyst SD-WAN Manager | 0.0158 (74.6) | 09-30-2026 | 10-03-2026 | Unknown | [Cisco](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-sdwan-webauth-xr8beuuU) |
| CVE-2026-102489 | Zammad | 0.014 (71.5) | 10-02-2026 | 10-05-2026 | Unknown | [Zammad](https://zammad.com/en/product/releases/) |
| CVE-2026-86950 | Apple iOS/macOS/iPadOS | 0.0124 (68.2) | 09-29-2026 | 10-02-2026 | Unknown | [Apple](https://support.apple.com/en-us/149226) |
| CVE-2026-102490 | Zammad | 0.0063 (48.3) | 10-02-2026 | 10-05-2026 | Unknown | [Zammad](https://zammad.com/en/product/releases/) |
| CVE-2026-88779 | Citrix NetScaler | 0.0028 (18.2) | 10-04-2026 | 10-07-2026 | Unknown | [Citrix](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697174) |

*EPSS = likelihood of exploitation in the next 30 days; percentile = rank vs all known flaws. "Ransomware used: Unknown" means no confirmed ransomware-campaign link is on record.*

### Ransomware victims — latest disclosures

| Group | Sector | Country | Discovered | Source |
|---|---|---|---|---|
| play | Agriculture and Food Production | US | 10-04-2026 | [Ransomware.live](https://www.ransomware.live) |
| play | Manufacturing | US | 10-04-2026 | [Ransomware.live](https://www.ransomware.live) |
| emperador | Manufacturing | TR | 10-04-2026 | [Ransomware.live](https://www.ransomware.live) |
| qilin | Manufacturing | AU | 10-04-2026 | [Ransomware.live](https://www.ransomware.live) |
| qilin | Manufacturing | ES | 10-04-2026 | [Ransomware.live](https://www.ransomware.live) |
| direwolf | Technology (Software) | BR | 10-04-2026 | [Ransomware.live](https://www.ransomware.live) |
| Storm | Healthcare | CA | 10-04-2026 | [Ransomware.live](https://www.ransomware.live) |
| krybit | Technology (IT integrator) | FR | 10-04-2026 | [Ransomware.live](https://www.ransomware.live) |
| krybit | Retail & E-Commerce | CO | 10-04-2026 | [Ransomware.live](https://www.ransomware.live) |

*Victim names are attacker self-disclosures, not confirmed incidents. Use this as a "which sectors are being hunted right now" signal.*

### Notable CIRCL advisories (beyond the top findings)

- **CVE-2026-63266 / -63267 / -63268 / -63269 / -63270 / -63277 (LibreOffice Calc & friends):** A batch of linked-data and media handling bugs. Opening a crafted spreadsheet or document can read local files, run code from a remote location, or exfiltrate settings. Update LibreOffice. [CIRCL detail](https://vulnerability.circl.lu/vuln/CVE-2026-63277)
- **CVE-2026-105396 (Heym, an AI agent tool):** Token leakage lets an unauthenticated attacker redirect human-in-the-loop review links and trigger anonymous workflows. [CIRCL detail](https://vulnerability.circl.lu/vuln/CVE-2026-105396)
- **CVE-2026-105307 (Casdoor):** Missing authentication in the API-filter endpoint, exploitable remotely. [CIRCL detail](https://vulnerability.circl.lu/vuln/CVE-2026-105307)
- **CVE-2026-59785 (Zabbix):** Host search lets a user read stored IPMI and PSK credentials by guessing and observing the result. [CIRCL detail](https://vulnerability.circl.lu/vuln/CVE-2026-59785)

### IOC sample (block-and-hunt; do not visit)

- **IClickFix / ClearFake (fake-update malware):** domains `cdn.quickdelivr.com`, `test.veveycorseauxplage.ch`, `toutmonmateriel.fr` · [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/js.iclickfix)
- **Drifter (ELF malware):** C2 IPs `93.152.221.232:32505`, `45.146.91.241:23004`, `45.146.91.234:32505`, `171.22.130.121:25632` · [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/elf.drifter)
- **Mozi (router botnet) payloads:** `http://120.28.215.116:57223/Mozi.m`, `http://113.94.58.233:7431/Mozi.m` · [URLhaus](https://urlhaus.abuse.ch/url/3929214/)

---

*Compiled from public sources · 10-05-2026*
