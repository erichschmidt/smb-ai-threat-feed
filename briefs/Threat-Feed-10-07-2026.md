---
type: threat-feed-note
title: "Threat Feed - 10-07-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-10-07
updated: 2026-10-07
---

# Threat Feed — 10-07-2026

**The 3-minute read for small businesses running AI and automation.** Plain language in the headlines, deeper detail below. Every score and source is explained so you can act without a security degree. Full plain-English glossary: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md)

## How to read the scores

- **CISA KEV:** If a vulnerability is on this list, it is *being actively exploited right now*, not theoretical. "CISA confirmed" = the authoritative "patch fast" signal.
- **EPSS:** A 0–1 score estimating how likely a flaw is to be exploited in the next 30 days; higher = patch first. The percentile says where it ranks — 96th percentile means it's more likely to be exploited than 96% of all known vulnerabilities.
- **CVSS:** A 0–10 severity score. 9.8/10 = critical, typically exploitable remotely with no login. Answers "how bad if it works"; EPSS/KEV answer "is it actually being used."

---

## 1. HIGH — Chat-with-your-data AI tools can be tricked into running database commands — update your LangChain

**CVE-2024-8309** · EPSS 0.137 (96th percentile) · CVSS 9.8/10 critical

**What broke.** A flaw in a widely used AI-building framework lets an attacker slip malicious instructions into the conversation that turn into unauthorized database commands. Specifically, the framework's graph-database "answer my question about our records" helper (GraphCypherQAChain) doesn't lock down the query it builds, so an attacker can inject their own database command through a crafted message — a **prompt injection** (putting instructions inside the data the AI reads) that becomes a **SQL injection** (tricking software into running database commands that read, change, or delete data).

**Attacker view (conceptual).** Scan for a chatbot built on this framework → send a crafted question that plants an injection → the unchecked query builder runs it against the linked database → read entire tables or wipe data. Defender observables: unexpected full-table reads or write commands in the database's activity log, far outside normal question-answer traffic.

**Why it matters to an SMB running AI tools.** If your "chat with your data" assistant, support bot, or internal tool queries a graph or SQL database via LangChain, the data source itself becomes the attack surface. A malicious document or message poisons the pipeline, and the bot runs commands against your business records with its own access. This is exactly the RAG (retrieval-augmented-generation) pattern most AI assistants use to "know" your data.

**What you do Monday** (15–30 minutes):
1. Update `langchain-community` to the fixed version — the patch commit is [c2a3021](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255). Check your lockfile/dependency manifest for the version you actually run.
2. If you can't update immediately, add an allowlist so the query builder only ever runs a few pre-approved read-only queries.
3. Ask whoever runs your database to check today's activity log for large, abnormal reads — evidence of exploitation.

**Sources:** [huntr bounty](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5) · [GitHub Security Advisory GHSA-45pg-36p6-83v9](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [Fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255)

---

## 2. HIGH — Known to be exploited: your email-gateway appliance can be hijacked by crafted web requests — patch FortiMail now

**CVE-2026-104286** · EPSS 0.022 (82nd percentile) · CISA KEV: confirmed actively exploited 10-01-2026, federal patch deadline 10-04-2026

**What broke.** An email security gateway lets an attacker with no login write files anywhere on the appliance by sending specifically crafted web requests — a **path traversal** (typing file path tricks to reach files you shouldn't) plus a "missing character" bug. Writing a file onto the appliance can become the first step to running attacker code on it.

**Why it matters to an SMB running AI tools.** The email gateway sits in front of every inbox — including the mailbox your AI mail assistant reads and the alerts your automation sends. A hijacked gateway can intercept, modify, or stop that mail. It is often the box that routes email-to-ticket and notification automations, so a compromise there reaches the data feeding your workflows.

**What you do Monday** (about 30 minutes, plus any firmware update):
1. Update FortiMail to the patched firmware — vendor advisory [FG-IR-26-175](https://fortiguard.fortinet.com/psirt/FG-IR-26-175). Note CISA flagged this as *actively exploited*, so treat it as urgent, not routine.
2. Confirm the appliance's admin/management web interface is not exposed to the internet (restrict to your office or VPN).
3. Check the appliance's logs for recent strange file-write or outbound traffic if you have them.

**Sources:** [Fortinet PSIRT FG-IR-26-175](https://fortiguard.fortinet.com/psirt/FG-IR-26-175) · [NVD CVE-2026-104286](https://nvd.nist.gov/vuln/detail/CVE-2026-104286)

---

## 3. WATCH — AI models can hide malware behind a filename — the scanner meant to catch it can be bypassed

**CVE-2025-1889** · CVSS 9.8/10 critical (lower observed exploitation odds)

**What broke.** A scanning tool meant to catch malicious code hidden inside downloaded AI-model files only checks files with standard name endings. An attacker renames a malicious model file to a non-standard ending and it sails past the scan. If a program then **loads** that model, the hidden code runs on your machine — a model file treated like a normal program.

**Why it matters to an SMB running AI tools.** If your team downloads or loads public AI models (fine-tunes, image or speech models, demo checkpoints), a poisoned model is malware wearing a model's clothes. Loading untrusted models into any ML tool — from a chatbot to a document analyzer — is a way to run attacker code.

**What you do Monday** (15–20 minutes):
1. Upgrade the scanner to version 0.0.22 or later — [GitHub Advisory GHSA-769v-p64c-89pr](https://github.com/advisories/GHSA-769v-p64c-89pr).
2. Prefer the safer model format (Safetensors) or the safe "load data only, run no code" loading switch for Python models.
3. Treat any downloaded model from an unfamiliar source as untrusted — scan it, and don't load it in a place connected to production data.

**Sources:** [GitHub Security Advisory GHSA-769v-p64c-89pr](https://github.com/advisories/GHSA-769v-p64c-89pr) · [Sonatype advisory CVE-2025-1889](https://sites.google.com/sonatype.com/vulnerabilities/cve-2025-1889)

---

## 4. WATCH — Your helpdesk system is actively exploited — a login-trick paired with a privilege bug gives full server access

**CVE-2026-102489 + CVE-2026-102490** · CISA KEV: confirmed actively exploited 10-02-2026, federal patch deadline 10-05-2026

**What broke.** Two flaws in a self-hosted helpdesk/ticketing system chain together. The first is a **session fixation** (pinning a victim to a login session the attacker controls) that can let an attacker run code as the helpdesk user. The second is a privilege-escalation flaw that raises that access to **root** (the highest level of control on the server). Together: full takeover of the machine.

**Why it matters to an SMB running AI tools.** A helpdesk holds support conversations, tickets, and customer records, and often feeds email-to-ticket and support-AI automations. Take over that server and you get the customer data the automation reads and the accounts it uses. Both flaws are already being exploited now.

**What you do Monday** (about 15 minutes, plus any update):
1. Update Zammad to the latest release — vendor [releases page](https://zammad.com/en/product/releases/).
2. If you host it yourself, check whether the admin panel is reachable only from inside your network.
3. Confirm the server's backups are recent and test one restore — ransomware crew activity is elevated today (see appendix) and this chain hands over the machine.

**Sources:** [Zammad releases](https://zammad.com/en/product/releases/) · [Zammad community advisory for CVE-2026-102490](https://community.zammad.org/t/take-care-local-privilege-escalation-cve-2026-102490-is-reported-as-being-actively-exploited/21297/2) · [NVD CVE-2026-102489](https://nvd.nist.gov/vuln/detail/CVE-2026-102489) · [NVD CVE-2026-102490](https://nvd.nist.gov/vuln/detail/CVE-2026-102490)

---

## 5. WATCH — Known to be exploited: a Citrix remote-access flaw can knock your VPN offline — patch before today's deadline

**CVE-2026-88779** · CISA KEV: confirmed actively exploited 10-04-2026, federal patch deadline 10-07-2026

**What broke.** A memory-handling bug in a popular remote-access appliance can be triggered to stop answering — a **denial of service** (the service stops responding, so nobody gets in, including you). CISA has confirmed it is being actively exploited.

**Why it matters to an SMB running AI tools.** This appliance is often the remote-access front door staff and automations use to reach the office network from outside — including access to the servers that run AI workloads and the admin panels of your automation tools. An outage there takes your remote workers and remote automation offline at once.

**What you do Monday** (about 10 minutes, plus any appliance update):
1. Apply the vendor fix — Citrix advisory [CTX697174](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697174). Today is the federal deadline, so this one is due now.
2. Review the Citrix techzone guidance in the source link for the exact mitigation steps for your appliance model.

**Sources:** [Citrix KB CTX697174](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697174) · [Citrix techzone analysis](https://community.citrix.com/techzone-blogs/110_security-updates/understanding-and-addressing-cve-2026-88779-in-citrix-netscaler-adc-and-citrix-netscaler-gateway/)

---

## Jargon buster

- **Prompt injection:** Putting instructions inside the data an AI reads so the AI follows the attacker's orders instead of the user's.
- **SQL injection:** Tricking software into running database commands that read, change, or delete data.
- **LangChain:** A popular open-source framework for building AI apps (chatbots, "chat with your data"). Flaws in it affect lots of AI tools at once.
- **GraphCypherQAChain:** The LangChain helper that turns a chat question into a graph-database query — if it isn't locked down, chat becomes a database write.
- **RAG (Retrieval-Augmented Generation):** The standard way AI tools "know" your data — the AI retrieves relevant documents, then answers from them. Poison the documents, poison the answers.
- **Path traversal:** A trick where an attacker types `../` (or similar) in a file path to reach files they shouldn't; in a server product it can become full takeover.
- **Email gateway:** The appliance or service that inspects inbound/outbound email before it reaches a mailbox — a hole here is a hole in everything that reads your mail, including AI mail assistants.
- **Unauthenticated (attacker):** Someone with no login credentials, operating from anywhere on the network or internet.
- **Denial of service (DoS):** The service stops answering, so nobody gets in — including you.
- **pickle:** A Python file format for saving objects; loading one can run code, so treat a random model file like an unknown program.
- **picklescan:** A scanner meant to catch dangerous pickle files inside AI-model downloads; if it skips a filename ending, a "model" can be malware.
- **Safetensors:** A model-file format that loads data without running code — prefer it for untrusted models.
- **Session fixation:** Pinning a victim to a login session the attacker controls; when the victim signs in, the attacker inherits that session and its access.
- **Privilege escalation:** Gaining higher system access (like administrator or root) than originally authorized.
- **Root privileges:** The highest level of access on a Linux/Unix system — the "administrator" of the machine.
- **CISA KEV:** CISA's list of vulnerabilities being actively exploited right now — if it's on the list, patch it.
- **EPSS:** A 0–1 estimate of how likely a flaw is to be exploited in the next 30 days; higher = patch first. Percentile = where it ranks vs all known vulnerabilities.

---

## Appendix

### CISA KEV — actively exploited, ranked by EPSS (most likely to be exploited first)

| CVE | Product | Added | Fed deadline | EPSS | EPSS %ile | Source |
|---|---|---|---|---|---|---|
| CVE-2026-104286 | Fortinet FortiMail | 10-01-2026 | 10-04-2026 | 0.022 | 82nd | [Fortinet](https://fortiguard.fortinet.com/psirt/FG-IR-26-175) |
| CVE-2026-102489 | Zammad (session → code) | 10-02-2026 | 10-05-2026 | 0.014 | 72nd | [Zammad](https://zammad.com/en/product/releases/) |
| CVE-2026-102490 | Zammad (priv escalation) | 10-02-2026 | 10-05-2026 | 0.0063 | 48th | [Zammad](https://zammad.com/en/product/releases/) |
| CVE-2026-88779 | Citrix NetScaler | 10-04-2026 | 10-07-2026 | 0.0059 | 47th | [Citrix](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697174) |

All four are being actively exploited right now. The Zammad pair chains into full server control; FortiMail is the highest-risk single item.

### Ransomware victims, last 24h (sector pulse — treat as sector-targeting signal, not proof)

| Group | Sector | Country | Date |
|---|---|---|---|
| qilin | Professional Services | ES | 10-07-2026 |
| SilentRansomGroup | Professional Services | — | 10-06-2026 |
| UmBra | Education | EG | 10-06-2026 |
| Panzer | Manufacturing | — | 10-06-2026 |
| qilin | Financial Services | — | 10-06-2026 |
| qilin | Manufacturing | TR | 10-06-2026 |
| Vexy Ransomware | Retail & E-Commerce | AU | 10-06-2026 |
| Panzer | Professional Services | US | 10-06-2026 |
| incransom | Other | US | 10-06-2026 |
| Deadlock | Agriculture & Food | IT | 10-06-2026 |

Source: [ransomware.live](https://www.ransomware.live)

### Notable vulnerabilities (CIRCL lookup)

- **Obot (CVE-2026-105138 / CVE-2026-105139):** A self-hosted AI-assistant platform. One flaw lets a logged-in user read stored secrets on connected tool entries; another lets a user access components they were never granted. If you run this agent platform, update. Sources: [CVE-2026-105138](https://vulnerability.circl.lu/vuln/CVE-2026-105138) · [CVE-2026-105139](https://vulnerability.circl.lu/vuln/CVE-2026-105139)
- **Veeam Backup & Replication (CVE-2026-93026):** A restricted backup user can modify the master key and stored update credentials; a separate flaw (CVE-2026-58069) lets a tenant read arbitrary files on the host. Backup software is the last line of defense — patch and test restores. Source: [CVE-2026-93026](https://vulnerability.circl.lu/vuln/CVE-2026-93026)
- **Gitea (CVE-2026-96400):** A migration-URL check can let an internal-address request reach the cloud metadata service. Self-hosted Git users: review migration settings, keep all.local-networks checks on. Source: [CVE-2026-96400](https://vulnerability.circl.lu/vuln/CVE-2026-96400)
- **MISP (CVE-2026-107175):** A bug in the event-save flow stops correlation recalculation when sharing settings change — intel-sharing platforms may silently miss links between threats. Source: [CVE-2026-107175](https://vulnerability.circl.lu/vuln/CVE-2026-107175)

### IOC sample (block-and-hunt signals — do not visit)

| Type | Value | Malware |
|---|---|---|
| hashes | b0a61e0d…9df0 | AMOS | 
| URL | https://kb.3toto.com | Vidar |
| IP:port | 137.220.224.26:8151 | Unknown RAT |
| domain | sarmo.store | ClearFake |
| domain | cfcher.biz | Remus |
| domain | cryonex.sbs | Remus |
| domain | didi31.workers.dev | Shin webshell |

Source: [ThreatFox](https://threatfox.abuse.ch/) (via [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/))

---

*Compiled from public sources · 10-07-2026*
