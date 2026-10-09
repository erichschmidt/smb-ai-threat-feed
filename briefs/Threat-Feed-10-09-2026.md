---
type: threat-feed-note
title: "Threat Feed - 10-09-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-10-09
updated: 2026-10-09
---

# Threat Feed — 10-09-2026

**The 3-minute read for small businesses running AI and automation.** Plain language in the headlines, deeper detail below. Every score and source is explained so you can act without a security degree. Full plain-English glossary: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md)

*AI-drafted from public data and published automatically. No one reviews each brief before it goes out. Check the linked source before you act.*

## How to read the scores

- **CISA KEV:** If a vulnerability is on this list, it is *being actively exploited right now*, not theoretical. "CISA confirmed" = the authoritative "patch fast" signal.
- **EPSS:** A 0–1 score estimating how likely a flaw is to be exploited in the next 30 days; higher = patch first. The percentile says where it ranks — 99th percentile means it's more likely to be exploited than 99% of all known vulnerabilities.
- **CVSS:** A 0–10 severity score. 9.8/10 = critical, typically exploitable remotely with no login. Answers "how bad if it works"; EPSS/KEV answer "is it actually being used."

---

## 1. HIGH — A popular "chat with your data" AI tool lets a question become a database break-in over the network

**CVE-2024-8309 — LangChain GraphCypherQAChain** · EPSS 0.137 (96th percentile — more likely to be exploited than 96% of all known vulnerabilities)

**What broke.** LangChain — the open-source framework many developers use to build "chat with your data" AI apps — has a helper (GraphCypherQAChain) that turns a chat question into a database query. The CVE text confirms a **SQL injection** (an attacker types malicious commands into an input or prompt, tricking the app into running unauthorized queries) that can be triggered through a prompt — meaning a crafted question or a poisoned chat source can make the tool read, change, or delete data it should never touch. CVSS 9.8/10 = critical, exploitable remotely with no login.

**Why it matters to an SMB running AI tools.** This is exactly the pattern small businesses are shipping: an AI assistant that answers questions about their own business data stored in a graph database (a database that stores records and their relationships as connected points). If that assistant is built on LangChain's GraphCypherQAChain and pulls from a graph store, an attacker who can get a prompt into the pipeline — via a shared document, a support ticket, or a form field — can write to the database instead of just reading it. It's the AI data-source layer itself, not a generic IT box.

**What you do Monday** (about 20 minutes):
1. Identify any AI chatbot or "talk to your data" tool built on LangChain that queries a graph database, and check the `langchain-community` / `langchain` version you're running.
2. Update to the patched `langchain-community` release that fixes CVE-2024-8309 (the fix landed in a 2024 commit, so this is much more about confirming you're current than hunting an old app).
3. Hardening that costs little now: connect the tool to the database with a read-only, least-privilege service account, and validate/restrict the queries it can generate.

**Sources:** [huntr bounty](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5) · [LangChain fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) · [GitHub advisory GHSA-45pg-36p6-83v9](https://github.com/advisories/GHSA-45pg-36p6-83v9)

---

## 2. CRITICAL — A common file-transfer server lets outsiders read and write any file on the machine — now confirmed actively exploited

**CVE-2015-3306 — ProFTPD** · EPSS 0.968 (99.9th percentile) · in CISA KEV · no login needed

**What broke.** ProFTPD — a widely used file-transfer (FTP) server on Linux servers — has a flaw from 2015 that lets a remote attacker use two special FTP commands to read **and write** arbitrary files on the server, no password or account required. CISA added it to the **KEV** list on 10-08-2026, meaning it is being actively exploited in the wild right now.

**Why it matters to an SMB running AI tools.** Many small businesses still run FTP or FTPS servers to exchange files with partners, vendors, and file-watcher automations. An unauthenticated "read and write any file" hole on that box turns it into a staging ground: attackers can plant files where your automation picks them up, or read the credentials and data your AI/automation pipelines pull. It's the pipe your integrations use, and it's wide open without a login.

**What you do Monday** (about 15 minutes):
1. Find any ProFTPD server you run and check its version — anything before the 2015 fix is exposed.
2. Update ProFTPD to the latest patched release (package update: Ubuntu/Debian `sudo apt update && sudo apt upgrade proftpd-*`).
3. If FTP isn't strictly needed, replace it with SFTP (which runs over SSH); if it must stay, block it from the internet and require the office VPN.

**Sources:** [Debian security announcement](https://lists.debian.org/debian-security-announce/2015/msg00154.html) · [openSUSE update](https://lists.opensuse.org/archives/list/updates@lists.opensuse.org/message/WE6YZRG5UVXMGQ7IVDRYBPIWV4M6UUGM/)

---

## 3. HIGH — Actively exploited flaws in Java app servers and the software behind many office tools — CISA added a batch today

**CVE-2016-3081 (Apache Struts) · CVE-2015-5477 (ISC BIND) · CVE-2021-3199 (ONLYOFFICE)** · all added to CISA KEV 10-08-2026 · EPSS 0.934 / 0.913 / 0.082

**What broke.** CISA added a cluster of older-but-still-active flaws to its actively-exploited list all at once. Highlights: Apache Struts — a Java framework many internal business apps are built on — has a **command injection** flaw (tricking software into running operating-system commands the attacker chose) that can execute code when a specific setting is on; ISC BIND (the DNS server that resolves names on your network) can be knocked offline by a crafted query (**denial of service** — the service stops answering); and ONLYOFFICE Docs, a self-hosted office suite some teams run, has a path-traversal hole that can lead to code execution.

**Why it matters to an SMB running AI tools.** These are the "old faithfuls" sitting underneath your stack: the Java app server running your internal tools and integrations, the DNS server your whole office (and your automation's outbound calls) depend on, and the office-doc suite your AI reads to summarize files. The message is the pattern: **old software that has been on the internet for years is being actively targeted right now.** Your AI tools are only as trustworthy as the servers that feed them.

**What you do Monday** (about 20 minutes):
1. Patch Apache Struts: find any Java app using it and update to the fixed release. Settings → application server config → update the Struts/package version.
2. Update ISC BIND on any DNS server you run: Ubuntu/Debian `sudo apt update && sudo apt upgrade bind9`.
3. Update ONLYOFFICE Docs to the version that fixes CVE-2021-3199 (check the [ONLYOFFICE changelog](https://github.com/ONLYOFFICE/DocumentServer/blob/903fe5ab7a275bd69c3c3346af2d21cf87ebeabf/CHANGELOG.md#563)).

**Sources:** [Struts — NVD](https://nvd.nist.gov/vuln/detail/CVE-2016-3081) & [Apache wiki S2-032](https://cwiki.apache.org/confluence/display/WW/S2-032) · [BIND — Red Hat](https://access.redhat.com/errata/RHSA-2015:1513.html) & [Juniper](https://supportportal.juniper.net/s/article/2016-01-Security-Bulletin-Junos-Vulnerability-in-ISC-BIND-named-CVE-2015-5477) · [ONLYOFFICE — NVD](https://nvd.nist.gov/vuln/detail/CVE-2021-3199) & [changelog](https://github.com/ONLYOFFICE/DocumentServer/blob/903fe5ab7a275bd69c3c3346af2d21cf87ebeabf/CHANGELOG.md#563)

---

## 4. HIGH — Your remote-access front door is the target of active zero-day attacks — CISA and Citrix are both warning

**Citrix NetScaler ADC / NetScaler Gateway — CISA Alert (09-27-2026) + CVE-2026-88779** · in CISA KEV · actively exploited

**What broke.** CISA issued an alert because serious **zero-day** (flaws that were unknown and unpatched when exploitation started) vulnerabilities in Citrix NetScaler ADC and NetScaler Gateway — the appliances many businesses use as their **VPN** (the encrypted "tunnel" remote workers use to reach the office network) and remote-access front door — are being actively attacked. It's the same product family as confirmed-in-KEV CVE-2026-88779 (a memory-buffer DoS), and the effect is the same: this is your front door, and it's being hit right now.

**Why it matters to an SMB running AI tools.** If you use a NetScaler appliance as your VPN/remote-access gateway, everything remote workers touch — including your internal AI chat tools, dashboards, and the admin panels of your automation — sits behind it. A compromise there gives an attacker the same doorway your staff use, so your tools and their data stop being private. Even if you don't run NetScaler, treat this as the reminder to check that whatever remote-access box you *do* use is patched, because these appliances get targeted relentlessly.

**What you do Monday** (about 15 minutes, plus reboot/downtime for the fix):
1. Check your Citrix NetScaler ADC/Gateway versions against the [Citrix security bulletin](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697174).
2. Apply the vendor fix — note this can require downtime/maintenance windows; plan it.
3. Check Citrix's indicators of compromise (published via NetScaler Console) before patching, and preserve evidence if you suspect a breach — patching can remove the traces.

**Sources:** [CISA Alert — Zero-Day Vulnerabilities in Citrix NetScaler ADC, Gateway](https://www.cisa.gov/news-events/alerts/2026/09/27/critical-zero-day-vulnerabilities-exploited-citrix-netscaler-adc-gateway) · [Citrix KB CTX697174](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697174)

---

## 5. WATCH — A headless website platform leaks customer data — and it's now end-of-life, so update before you're stuck

**CVE-2023-22894 — Strapi** · in CISA KEV · EPSS 0.017 (76th percentile)

**What broke.** Strapi — a popular **headless CMS** (a content system that serves website content to apps via an API) many SMBs use to run their sites — stores sensitive user details in **cleartext** (stored so anyone who can read the file can see it, with no encryption) and exposes them through a query filter when someone has admin-panel access. CISA flagged it as actively exploited. The catch: the affected line can be **end-of-life** (at the end of vendor support), so waiting risks being left with no fix at all.

**Why it matters to an SMB running AI tools.** If your website or a data feed your marketing AI reads is served by Strapi, this is a data-exposure entry point: an admin with access can pull customer details that have been stored unencrypted. And because it's end-of-life, the practical fix is likely an upgrade/migration to a supported Strapi release rather than a one-line patch — the kind of thing that needs planning, not just clicking update.

**What you do Monday** (about 15 minutes):
1. If you run Strapi, confirm whether you're on the affected, end-of-life release (check your version against the [Strapi releases page](https://github.com/strapi/strapi/releases)).
2. Upgrade to a supported release — or, if you're on the EoL line, plan the migration and block it as a priority.
3. Confirm sensitive customer fields are stored encrypted / tokenized (this is a data-at-rest problem).

**Sources:** [Strapi security disclosure](https://strapi.io/blog/security-disclosure-of-vulnerabilities-cve) · [NVD — CVE-2023-22894](https://nvd.nist.gov/vuln/detail/CVE-2023-22894)

---

## Jargon buster

- **Command injection:** Tricking software into running operating-system commands the attacker chose.
- **Denial of service (DoS):** The service stops answering, so nobody gets in — including you.
- **End-of-life (EoL):** A product the vendor has stopped supporting, so no more security fixes — any new flaw is permanent.
- **Graph database:** A database that stores things and their relationships as connected points. AI tools may query it to answer questions about linked business records.
- **Headless CMS:** A content system that serves website content to apps via an API, instead of rendering a page itself.
- **SQL injection:** A technique where attackers type malicious database commands into an input box (or a prompt), tricking the app into running unauthorized queries — reading, changing, or deleting data.
- **Zero-day:** A flaw that was unknown (and unpatched) when it started being exploited — the most dangerous kind.

*(All other terms used above — LangChain, GraphCypherQAChain, KEV, EPSS, CVSS, RCE, path traversal, cleartext, VPN, prompt injection — are in the [master glossary](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).)*

---

## Appendix

### CISA KEV — actively exploited, ranked by EPSS (most likely to be exploited first)

All added 10-08-2026 unless noted; federal patch deadline for the new batch is 10-11-2026.

| CVE | Product | Added | Fed deadline | EPSS | EPSS %ile | Source |
|---|---|---|---|---|---|---|
| CVE-2015-3306 | ProFTPD | 10-08-2026 | 10-11-2026 | 0.968 | 99.9th | [ProFTPD](http://www.proftpd.org/) |
| CVE-2016-3081 | Apache Struts | 10-08-2026 | 10-11-2026 | 0.934 | 99.8th | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2016-3081) |
| CVE-2015-5477 | ISC BIND (DoS) | 10-08-2026 | 10-11-2026 | 0.913 | 99.8th | [Red Hat](https://access.redhat.com/errata/RHSA-2015:1513.html) |
| CVE-2021-3199 | ONLYOFFICE Docs | 10-08-2026 | 10-11-2026 | 0.082 | 94.8th | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2021-3199) |
| CVE-2023-22894 | Strapi | 10-08-2026 | 10-11-2026 | 0.017 | 75.9th | [Strapi](https://github.com/strapi/strapi/releases) |
| CVE-2026-88779 | Citrix NetScaler (DoS) | 10-04-2026 | 10-07-2026 | 0.006 | 46.6th | [Citrix](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697174) |

CISA confirmed each is actively exploited as of its "Added" date. Known ransomware-campaign use: not flagged (Unknown) for all six. The low-EPSS rows (ONLYOFFICE, Strapi, Citrix) are still in the KEV, so they're being exploited — EPSS just says less likely to be widely automated than the top three.

### Ransomware victims, last 24h (sector pulse — treat as sector-targeting signal, not proof)

| Group | Sector | Country | Date |
|---|---|---|---|
| netrunner | Healthcare | US | 10-08-2026 |
| Barracuda | Agriculture & Food Production | HR | 10-09-2026 |
| SilentRansomGroup | Professional Services (US law firms) | US | 10-08-2026 |
| qilin | Technology | MX | 10-08-2026 |
| UmBra | Education | IN | 10-08-2026 |
| payload | Retail & E-Commerce | FR | 10-08-2026 |

A US healthcare provider and US law firms sit alongside the agriculture/food and retail hits — evidence that ransomware crews are spreading across every sector, not staying inside one industry. Source: [ransomware.live](https://www.ransomware.live)

### Notable vulnerabilities (CIRCL lookup)

- **WordPress plugin batch (many, incl. CVE-2026-89235, CVE-2026-96539, CVE-2026-96331):** a large cluster of WordPress plugin flaws disclosed 10-09-2026 — SQL injection, privilege escalation, and blind SQL injection across testimonial, membership, and search plugins. If you run WordPress and any of these plugins (Testimonials by BestWebSoft, Ultimate Member, Ajax Search Pro, etc.), check your plugin-update page: Settings → Plugins → Update.
- **picklescan (CVE-2025-1889):** the AI model-scan tool can be bypassed if a malicious model file uses a non-standard extension, so the "safe" scan skips it. Reminder: treat downloaded AI model files like unknown programs. EPSS 0.004 (32nd). Source: [GHSA-769v-p64c-89pr](https://github.com/advisories/GHSA-769v-p64c-89pr).

### IOC sample (block-and-hunt signals — do not visit)

| Type | Value | Malware |
|---|---|---|
| IP:port | 207.154.219.20:8080 | Aisuru |
| IP:port | 217.60.242.27:12345 | Aisuru |
| domain | mars-uae.com | ClearFake |
| domain | 48ypnsgk.porel.store | ClearFake |
| hash | deba43734e342776a2724c6cf12557aa7bbbd93200a4f2bfa8f2e7f7ef1b56a8 | AMOS (macOS) |
| URL | http://139.135.59.180:50268/Mozi.m | Mozi |
| URL | http://222.140.156.6:45408/bin.sh | (URLhaus) |

Source: [ThreatFox](https://threatfox.abuse.ch/) (via [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/)) · [URLhaus](https://urlhaus.abuse.ch/)

---

*Compiled from public sources · 10-09-2026*
