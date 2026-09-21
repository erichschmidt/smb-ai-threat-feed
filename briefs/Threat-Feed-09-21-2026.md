---
type: threat-feed-note
title: "Threat Feed - 09-21-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-09-21
updated: 2026-09-21
---

# Threat Feed — 09-21-2026

**3-minute read:** Skim the headlines, then the Jargon buster at the bottom. If a term is new, it's defined there. Full glossary lives at [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).

## How to read the scores
- **EPSS** is a 0-to-1 number estimating how likely a flaw is to be exploited in the next 30 days. Higher = patch first. The percentile tells you where it ranks: 96th percentile = more likely to be exploited than 96% of all known vulnerabilities.
- **CVSS** is a 0-to-10 severity score for "how bad if it works." 9.8/10 = critical — typically exploitable remotely with no login. CVSS says how bad; EPSS and the KEV list answer "is it actually being used."
- **KEV** is CISA's list of flaws being actively exploited right now. If a flaw is on it, it's not theoretical — patch it.

---

## Item 1 — HIGH — Your "chat with your data" AI can be tricked into rewriting the database behind it

**CVE-2024-8309** in LangChain's GraphCypherQAChain (a helper that turns a chat question into a database query). CVSS 9.8/10 (critical — exploitable remotely with no login). EPSS 0.1374 — 96th percentile: more likely to be exploited than 96% of known vulnerabilities.

**What broke:** LangChain is one of the most-used frameworks for building AI tools that answer questions from your business data. Its GraphCypherQAChain (the component that translates a question into a query for a graph database — a database that stores records and their relationships as connected points) is vulnerable to SQL injection (tricking software into running unauthorized database commands) through prompt injection. An attacker can hide instructions inside the data the AI reads, and the AI obediently runs a query that reads, changes, or deletes data it should never touch. You don't need the mechanism detail — just know that a chatbot built on this component can be turned into a way in to its database.

**Why it matters to an SMB running AI tools:** If you (or a vendor you use) built a "chat with your records" assistant on LangChain's graph-query chain, this is a direct hole in that assistant. The AI is the front door, and the database it reads is the prize. Because LangChain is everywhere, one flaw here touches a lot of AI tools at once — and the fix belongs to whoever built the tool, not to you as a user.

**What you do Monday:**
1. Ask whoever built your AI assistant (vendor or in-house dev): "Are you on a patched LangChain that fixes CVE-2024-8309?" If yes, confirm the version. If no, ask them to update. (15 minutes)
2. If you run it yourself, update `langchain-community` to the patched version that includes the fix commit. (30 minutes)
3. Check that the AI's database account has least privilege — read-only for the tables the assistant answers from, no ability to delete. (30 minutes)

**Sources:** [GitHub advisory (GHSA-45pg-36p6-83v9)](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [huntr bounty report](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5) · [LangChain fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255)

---

## Item 2 — WATCH — The tool that scans downloaded AI models can be fooled by renaming the file

**CVE-2025-1889** in picklescan, a scanner meant to catch dangerous files inside AI model downloads. CVSS 9.8/10 (critical). EPSS 0.0039 — low; not yet widely exploited, but the bypass is trivial.

**What broke:** picklescan only checks files with standard pickle extensions (pickle is a Python file format for saving objects — loading one can run code). An attacker can craft a malicious model that includes a dangerous pickle file with a non-standard file extension, and the scanner walks right past it. The "safety scan" gives a false all-clear.

**Why it matters to an SMB running AI tools:** If you or your team download AI models from the internet and rely on picklescan to check them before loading, that check can be silently skipped. Loading a malicious model file is like running an unknown program — it can execute attacker code on your machine. This is the second day in a row this scanner family has shown up in the feed; treat model files like unknown programs, not trusted data.

**What you do Monday:**
1. Update picklescan to version 0.0.22 or later (the fix). (10 minutes)
2. Prefer the safetensors format (a model-weight format that stores data without running code on load) over raw pickle files for any model you download. (30 minutes)
3. Load any downloaded model in an isolated environment (a sandbox — a cage meant to contain a program) before touching production. (1 hour)

**Sources:** [GitHub advisory (GHSA-769v-p64c-89pr)](https://github.com/advisories/GHSA-769v-p64c-89pr) · [Sonatype advisory](https://sites.google.com/sonatype.com/vulnerabilities/cve-2025-1889)

---

## Item 3 — HIGH — Your Linux servers have three actively-exploited holes — patch today

**CVE-2025-39964**, **CVE-2026-53266**, **CVE-2025-39682** in the Linux kernel. CISA added all three to its known-exploited list on 09-18-2026 and requires federal agencies to patch by 09-21-2026 (today). EPSS 0.012 / 0.0079 / 0.0028 — moderate to low, but CISA confirms active exploitation.

**What broke:** Three separate kernel flaws, all confirmed being actively exploited right now:
- A race condition (two parts of a program writing the same data at the same time) that lets concurrent writes to the same network socket get interleaved and corrupt the socket's internal state.
- An out-of-bounds write (a memory bug where software writes past the space it allocated) in the firewall address-rewrite path.
- A flaw in the encrypted-connection (TLS) receive path that lets a crafted zero-length record bypass normal handling and corrupt how later records are processed.

You don't need the memory-bug detail — just know these are real, being exploited, and the fix is a kernel update.

**Why it matters to an SMB running AI tools:** Your AI/automation stack — model servers, RAG pipelines (the standard way AI tools "know" your business data), ML orchestration — almost certainly runs on Linux. These are kernel-level flaws, meaning they're in the operating system under everything. If you self-host any AI service on Linux, this is a patch-your-hosts item.

**What you do Monday:**
1. On every Linux server: `sudo apt update && sudo apt upgrade` (or your distro's equivalent), then reboot to load the new kernel. (30 minutes per server)
2. Confirm the new kernel is running: `uname -r` and check it matches your distro's patched version. (5 minutes)
3. If you can't reboot immediately, check with your hosting provider or IT person whether the patched kernel is staged. Give them this exact sentence: "CISA added three Linux kernel flaws to its actively-exploited list on 09-18-2026 — I need the patched kernel applied." (15 minutes)

**Sources:** [CISA KEV alert (09-18-2026)](https://www.cisa.gov/news-events/alerts/2026/09/18/cisa-adds-two-known-exploited-vulnerabilities-catalog) · [CVE-2025-39964 (NVD)](https://nvd.nist.gov/vuln/detail/CVE-2025-39964) · [CVE-2026-53266 (NVD)](https://nvd.nist.gov/vuln/detail/CVE-2026-53266) · [CVE-2025-39682 (NVD)](https://nvd.nist.gov/vuln/detail/CVE-2025-39682)

---

## Item 4 — HIGH — Cisco's network-access control box has an unauthenticated hole being actively exploited

**CVE-2026-76460** in Cisco Identity Services Engine (ISE) and its Passive Identity Connector. CVSS not listed; EPSS 0.0078 (55th percentile). CISA added it to the known-exploited list on 09-16-2026, federal deadline 09-19-2026 (passed).

**What broke:** ISE (Identity Services Engine — the Cisco appliance that decides who and what is allowed on your network) has a flaw where an unauthenticated, remote attacker (someone with no login, from anywhere) can bypass the web-based management interface and gain unauthorized access to the device.

**Why it matters to an SMB running AI tools:** ISE is the gatekeeper that controls which devices and users get onto your network — including the servers that run your AI and automation. An attacker who gets into the gatekeeper can often reach everything behind it. If you run Cisco ISE, this is a "patch now" item; if you don't, it's a "good thing we don't run that" item.

**What you do Monday:**
1. If you run Cisco ISE or ISE-PIC, apply Cisco's patch for cisco-sa-ISE-ABP-VNSW7Tn5. (1 hour)
2. If you're not sure whether you run ISE, ask your IT person: "Do we run Cisco Identity Services Engine?" If yes, it needs patching. (10 minutes)
3. Check whether the ISE management interface is exposed to the internet — it should only be reachable from inside your network. (15 minutes)

**Sources:** [Cisco security advisory](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-ISE-ABP-VNSW7Tn5) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-76460)

---

## Item 5 — WATCH — Your web-hosting backup plugin can be hijacked to gain admin access

**CVE-2026-87886** in Acronis Backup for cPanel/WHM and Plesk (web-hosting control panels). EPSS 0.0025 (17th percentile). CISA added it to the known-exploited list on 09-16-2026, federal deadline 09-19-2026 (passed).

**What broke:** The Acronis Backup plugin used on common web-hosting control panels has an incorrect-default-permissions flaw that allows privilege escalation (gaining higher system access rights than you're supposed to have). Someone with a foothold on the server can leverage it to reach admin-level access.

**Why it matters to an SMB running AI tools:** If you host websites or self-host services using cPanel/WHM or Plesk with Acronis Backup, this is a double threat — the backup jobs themselves can be hijacked. And if your AI tools read from those hosted sites or databases, the backup compromise is a path to the data your AI depends on. For most SMBs, this is: check if you run it, patch if you do.

**What you do Monday:**
1. If you use Acronis Backup with cPanel/WHM or Plesk, apply the fix from Acronis advisory SEC-10986. (30 minutes)
2. If you don't know, ask your hosting provider: "Is Acronis Backup running on our cPanel/Plesk server, and is it patched against CVE-2026-87886?" (10 minutes)

**Sources:** [Acronis advisory SEC-10986](https://security-advisory.acronis.com/advisories/SEC-10986) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-87886)

---

## Jargon buster
- **Cypher / graph database:** A graph database stores records and their relationships as connected points; Cypher is its query language. AI tools may query it to answer questions about linked business records.
- **SQL injection:** A technique where attackers type malicious database commands into an input box (or a prompt), tricking the app into running unauthorized queries — reading, changing, or deleting data.
- **Prompt injection:** Tricking an AI by putting instructions inside the data it reads — the AI follows the attacker's instructions instead of the user's.
- **pickle / picklescan:** Pickle is a Python file format for saving objects; loading one can run code. picklescan is a scanner meant to catch dangerous pickle files inside AI model downloads. If it skips a file extension, a "model" can be malware.
- **safetensors:** A model-weight file format that stores data without running code on load. Prefer it over pickle for untrusted models.
- **Race condition:** Two parts of a program writing the same data at the same time, letting an attacker feed in their own result.
- **Out-of-bounds write:** A memory bug where software writes past the space it allocated for data. Attackers use it to crash a service or, in the right conditions, run their own code.
- **RAG (Retrieval-Augmented Generation):** The standard way AI tools "know" your business data — the AI retrieves relevant documents, then answers from them. The data source becomes an attack surface.
- **ISE (Identity Services Engine):** Cisco's appliance that decides who and what is allowed on your network.
- **Unauthenticated (attacker):** Someone with no login credentials, operating from anywhere.
- **Privilege escalation:** Gaining higher system access rights (like administrator or root) than originally authorized.
- **Least privilege:** Giving a person or software account only the access it needs for its job, and no more.
- **cPanel/WHM and Plesk:** Web-hosting control panels commonly used on small-business web servers. Admin access there means control of every hosted site and mailbox.
- **Sandbox:** A cage meant to contain a program. A "breakout" means the attacker escaped onto the real machine.
- **KEV / EPSS / CVSS:** See "How to read the scores" above.

---

## Appendix

### CISA KEV — ranked by EPSS (highest exploitation likelihood first)
| CVE | Product | CISA confirmed | Federal patch by | Ransomware use | EPSS | Source |
|-----|---------|----------------|------------------|----------------|------|--------|
| CVE-2025-39682 | Linux Kernel (TLS) | 09-18-2026 | 09-21-2026 | Unknown | 0.012 (67th pct) | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2025-39682) |
| CVE-2025-39964 | Linux Kernel (socket race) | 09-18-2026 | 09-21-2026 | Unknown | 0.0079 (55th pct) | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2025-39964) |
| CVE-2026-76460 | Cisco ISE | 09-16-2026 | 09-19-2026 | Unknown | 0.0078 (55th pct) | [Cisco](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-ISE-ABP-VNSW7Tn5) |
| CVE-2026-53266 | Linux Kernel (ebtables) | 09-18-2026 | 09-21-2026 | Unknown | 0.0028 (20th pct) | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-53266) |
| CVE-2026-87886 | Acronis Backup (cPanel/Plesk) | 09-16-2026 | 09-19-2026 | Unknown | 0.0025 (17th pct) | [Acronis](https://security-advisory.acronis.com/advisories/SEC-10986) |
| CVE-2026-58704 | Google Pixel (cellular modem) | 09-16-2026 | 09-19-2026 | Unknown | 0.0021 (11th pct) | [Android bulletin](https://source.android.com/docs/security/bulletin/pixel/2026/2026-09-01) |

*All KEV items: CISA confirmed active exploitation as of the "CISA confirmed" date. "Ransomware use: Unknown" means CISA has not flagged it as used in ransomware campaigns.*

### Ransomware sector pulse (Ransomware.live, last 24h)
- **incransom** — Hospitality (ES), real estate (US orthodontics)
- **emperador** — Healthcare (US women's health), Professional Services (IT notary)
- **krybit** — Technology (TR)
- **qilin** — Manufacturing (TR), Retail & E-Commerce (TH), Transportation (CH)
- **bravox** — Technology (US surveying/LiDAR/GIS)

Sector signal: healthcare and professional services continue to be targeted. These are attacker claims, not proof of incidents — treat them as "this sector is being hunted" signals.

**Source:** [Ransomware.live](https://www.ransomware.live)

### Notable CIRCL findings (high-signal)
- **CVE-2024-8309** (LangChain GraphCypherQAChain SQL injection) — EPSS 0.1374, 96th percentile. Covered as Item 1. [GHSA](https://github.com/advisories/GHSA-45pg-36p6-83v9)
- **CVE-2025-1889** (picklescan bypass) — EPSS 0.0039. Covered as Item 2. [GHSA](https://github.com/advisories/GHSA-769v-p64c-89pr)
- **CVE-2026-94379 / 94381 / 94383** (MISP threat-intel platform, published 09-21-2026) — login method validation, API-key privilege issue, and blocklist filename injection. For teams running MISP. [CIRCL](https://vulnerability.circl.lu/vuln/CVE-2026-94379)

### IOC sample (ThreatFox / URLhaus, last 24h)
- **Mirai** (IoT botnet): `http://94.154.43.176/x64` — [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/elf.mirai)
- **Mozi** (IoT botnet): `http://72.255.37.168:56495/Mozi.m` — [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/elf.mozi)
- **AMOS** (macOS stealer): hash `aacf8388...` — [bazaar](https://bazaar.abuse.ch/sample/aacf8388643245011a2b5edc472fafa48277e33b7b7e4de23ba62b1a8e919558/)
- **Quasar RAT** (Windows remote access): `217.69.9.252:3252` — [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/win.quasar_rat)
- **ClearFake** (fake-update malware): `76ocm7az.en-us-glycofree.com` — [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/js.clearfake)
- **URLhaus** (active malicious URLs, all online): `http://196.189.69.192:48199/i` and 5 others — [URLhaus](https://urlhaus.abuse.ch/url/3919983/)

*IOCs are block-and-hunt signals. Do not visit listed domains or URLs.*

---

*Compiled from public sources · 09-21-2026*