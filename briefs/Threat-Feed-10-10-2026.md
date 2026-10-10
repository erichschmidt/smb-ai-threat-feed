---
type: threat-feed-note
title: "Threat Feed - 10-10-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-10-10
updated: 2026-10-10
---

# Threat Feed — 10-10-2026

**The 3-minute read for small businesses running AI and automation.** Plain language in the headlines, deeper detail below. Every score and source is explained so you can act without a security degree. Full plain-English glossary: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md)

*AI-drafted from public data and published automatically. No one reviews each brief before it goes out. Check the linked source before you act.*

## How to read the scores

- **CISA KEV:** If a vulnerability is on this list, it is *being actively exploited right now*, not theoretical. "CISA confirmed" = the authoritative "patch fast" signal.
- **EPSS:** A 0–1 score estimating how likely a flaw is to be exploited in the next 30 days; higher = patch first. The percentile says where it ranks — 99th percentile means it's more likely to be exploited than 99% of all known vulnerabilities.
- **CVSS:** A 0–10 severity score. 9.8/10 = critical, typically exploitable remotely with no login. Answers "how bad if it works"; EPSS/KEV answer "is it actually being used."

---

## 1. HIGH — The AI "chat with your data" helper still tops the stack: a question over the network can become a database break-in

**CVE-2024-8309 — LangChain GraphCypherQAChain** · EPSS 0.137 (96th percentile — more likely to be exploited than 96% of all known vulnerabilities) · not in KEV, but EPSS crosses the exploitation-likelihood bar

**What broke.** LangChain — the open-source framework many developers use to build "chat with your data" AI apps — has a helper (GraphCypherQAChain) that turns a chat question into a database query. The flaw is a **SQL injection** (an attacker types malicious commands into an input or prompt, tricking the app into running unauthorized queries) that can be triggered through a prompt — so a crafted question or a poisoned chat source can make the tool read, change, or delete data it should never touch. CVSS 9.8/10 = critical, exploitable remotely with no login. This item resurfaced in today's vulnerability lookup with a fully documented proof-of-concept trail (a public bounty report plus the upstream fix commit), which is why it remains the standing AI-stack priority.

**Why it matters to an SMB running AI tools.** This is exactly the pattern small businesses are shipping: an AI assistant that answers questions about their own business data stored in a **graph database** (a database that stores records and their relationships as connected points). If that assistant is built on LangChain's GraphCypherQAChain and pulls from a graph store, an attacker who can get a prompt into the pipeline — a shared document, a support ticket, a form field — can write to the database instead of just reading it. It's the AI data-source layer itself, not a generic IT box; if you built on the affected helper at all, it's your highest-priority AI-layer fix.

**What you do Monday** (about 20 minutes):
1. Identify any AI chatbot or "talk to your data" tool built on LangChain that queries a graph database, and check the `langchain-community` / `langchain` version you're running.
2. Update to the patched release that fixes CVE-2024-8309 — check the fix commit below and confirm you're on a version that includes it.
3. Hardening that costs little now: connect the tool to the database with a read-only, least-privilege service account, and validate/restrict the queries it can generate.

**Sources:** [huntr bounty](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5) · [LangChain fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) · [GitHub advisory GHSA-45pg-36p6-83v9](https://github.com/advisories/GHSA-45pg-36p6-83v9)

---

## 2. WATCH — A batch of WordPress plugins disclosed holes today, including an unauthenticated database query and a login-recovery bypass that can take over accounts

**CVE-2026-87781 (LTL Freight Quotes) · CVE-2026-94257 / CVE-2026-94256 (SMS Alert) — disclosed 10-10-2026**

**What broke.** A cluster of WordPress plugin flaws landed today. LTL Freight Quotes has a **SQL injection** (an attacker types malicious database commands into an input, tricking the app into running unauthorized queries) exploitable by unauthenticated users — CVSS 9.8. SMS Alert has a pair of related flaws in its recovery flow: an attacker can reset a password on an account whose phone number they didn't actually verify (CVE-2026-94257), and can log in as any user whose phone number is stored — including an administrator (CVE-2026-94256). There's no evidence these are being exploited yet, which is why this is a WATCH rather than a HIGH, but the account-takeover pair is worth treating seriously.

**Why it matters to an SMB running AI tools.** General IT hygiene — no specific AI angle. WordPress is the most common way small businesses run their site, and these are flaws in plugins any of them might run. The account-takeover flaw is the sharp one: if someone can log in as your site administrator, any connected tools — analytics, forms, email, marketing automations that read site data — inherit that access. The best defense is simply updating the plugins, which is a few clicks once you own a plugin inventory.

**What you do Monday** (about 15 minutes):
1. In your WordPress admin: go to Plugins → Installed Plugins and write down which of these you run — the freight-quotes and SMS-alert plugins are the ones named, but treat today as "run a plugin update pass."
2. Update those plugins: Plugins → Installed Plugins → Update Now on anything with available updates.
3. Turn on email/push security alerts in WordPress or your host so you see login activity; if you suspect you were already hit, check for a new admin user you didn't create (Users → All Users).

**Sources:** [NVD — LTL Freight Quotes CVE-2026-87781](https://nvd.nist.gov/vuln/detail/CVE-2026-87781) · [NVD — SMS Alert CVE-2026-94257](https://nvd.nist.gov/vuln/detail/CVE-2026-94257) · [NVD — SMS Alert CVE-2026-94256](https://nvd.nist.gov/vuln/detail/CVE-2026-94256)

---

## 3. WATCH — A widely used analytics/data library opened several memory flaws at once — review it if your data or AI pipelines use sketches

**CVE-2026-103501, CVE-2026-103513, CVE-2026-103635, CVE-2026-103636 — Apache DataSketches C++ — disclosed 10-10-2026**

**What broke.** Apache DataSketches, a popular C++ library for approximate counting and statistical summaries (the "sketch" data structures used in many analytics and observability stacks), disclosed four deserialization flaws at once — memory bugs where software reads or writes past the space it allocated for data (heap buffer overflow and out-of-bounds read/write). The pattern across all four: feeding the library a maliciously crafted saved sketch can corrupt memory. No scores or exploitation evidence are published yet, so this is a WATCH — but the "four CVEs, same library, same trigger, same day" shape is the tell that vendors are cleaning house on a component they all share.

**Why it matters to an SMB running AI tools.** This is a data-pipeline library more than an AI product itself, but sketch structures (like HLL — HyperLogLog, a type of sketch used for counting unique items at scale) sit inside the telemetry and analytics path that your dashboards and monitoring — and, increasingly, the pipelines feeding AI features — rely on. The good news: this is not a "your website is exposed" bug. It needs a targeted data file or API response to exploit, so it's a library-update item for whoever runs the analytics stack behind your tools, not a fire-drill for the front office.

**What you do Monday** (about 15 minutes, only if you run DataSketches):
1. Check whether your analytics/observability stack or any service you run bundles Apache DataSketches (dependency lists, `pom.xml` for Java builds, or the equivalent package file).
2. Update DataSketches C++ to a release that includes the 10-10-2026 fuzz fixes.
3. If a vendor or analytics tool manages it for you, note it on your vendor patch list; there's no action until the fixed release lands from that vendor.

**Sources:** [NVD — CVE-2026-103501](https://nvd.nist.gov/vuln/detail/CVE-2026-103501) · [NVD — CVE-2026-103513](https://nvd.nist.gov/vuln/detail/CVE-2026-103513) · [NVD — CVE-2026-103635](https://nvd.nist.gov/vuln/detail/CVE-2026-103635) · [NVD — CVE-2026-103636](https://nvd.nist.gov/vuln/detail/CVE-2026-103636)

---

## 4. WATCH — No new actively-exploited flaws were added to CISA's list today — but the six already there are still being used, and their exploitation scores just moved

**No new CISA KEV additions in the last 24 hours.** The six already in the catalog remain actively exploited.

**What broke.** CISA added no new vulnerabilities to its Known Exploited Vulnerabilities (KEV) catalog today — the actively-exploited list is unchanged since the 10-08 batch (ProFTPD, Apache Struts, ISC BIND, ONLYOFFICE, Strapi) plus the older Citrix NetScaler entry. The important update: FIRST re-scored today and several exploitation-likelihood scores *rose* materially (ProFTPD to a 99.9th percentile, ONLYOFFICE from roughly the mid-90s to the 97th). That's a re-ranked watchlist, not new names — the same machines you were told to patch on 10-08 are the ones being attacked right now.

**Why it matters to an SMB running AI tools.** These are the servers underneath your stack — file-transfer and app servers your integrations and automations talk to, the DNS server your outbound calls depend on, the self-hosted office suite your AI reads to summarize files. A quiet KEV day is a good day; the risk is treating "nothing new was added" as permission to skip the patches you were already told about. The appendix below has the full table with updated scores.

**What you do Monday** (about 30 minutes):
1. If you haven't patched the 10-08 batch yet, treat that as today's task — it's the priority, not the "new" news: ProFTPD, Apache Struts, ISC BIND, ONLYOFFICE, Strapi.
2. Confirm you're covered against the Citrix NetScaler entry (CVE-2026-88779) if you run those appliances.
3. Cross off each one on your patch checklist and log the date; the appendix is your checklist.

**Sources:** [CISA KEV catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) · [CISA/BOD 26-04](https://www.cisa.gov/news-events/directives)

---

## Jargon buster

- **Denial of service (DoS):** The service stops answering, so nobody gets in — including you.
- **Deserialization:** Turning a saved data blob back into a live program object; if the blob is attacker-controlled, that "restore" can run their code.
- **Graph database:** A database that stores things and their relationships as connected points. AI tools may query it to answer questions about linked business records.
- **Heap buffer overflow / out-of-bounds read/write:** Memory bugs where software reads or writes past the space it allocated for data. Attackers use them to crash a service or, in the right conditions, run their own code.
- **Sketch (statistics):** A compact summary a library computes from large data (e.g., HyperLogLog for counting unique items) so it can answer questions without storing every record. A "sketch" fed a malicious saved file can be the injection point for these bugs.
- **SQL injection:** A technique where attackers type malicious database commands into an input box (or a prompt), tricking the app into running unauthorized queries — reading, changing, or deleting data.

*(All other terms used above — LangChain, GraphCypherQAChain, KEV, EPSS, CVSS, RCE, graph database, WordPress plugin, OTP — are in the [master glossary](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).)*

---

## Appendix

### CISA KEV — actively exploited, ranked by EPSS (most likely to be exploited first)

All still active; the first five were added 10-08-2026, Citrix 10-04-2026. Federal patch deadline for the 10-08 batch is 10-11-2026. Scores below are today's re-scored EPSS values.

| CVE | Product | Added | Fed deadline | EPSS | EPSS %ile | Source |
|---|---|---|---|---|---|---|
| CVE-2015-3306 | ProFTPD | 10-08-2026 | 10-11-2026 | 0.980 | 99.9th | [ProFTPD](http://www.proftpd.org/) |
| CVE-2016-3081 | Apache Struts | 10-08-2026 | 10-11-2026 | 0.945 | 99.8th | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2016-3081) |
| CVE-2015-5477 | ISC BIND (DoS) | 10-08-2026 | 10-11-2026 | 0.918 | 99.8th | [Red Hat](https://access.redhat.com/errata/RHSA-2015:1513.html) |
| CVE-2021-3199 | ONLYOFFICE Docs | 10-08-2026 | 10-11-2026 | 0.146 | 96.6th | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2021-3199) |
| CVE-2023-22894 | Strapi | 10-08-2026 | 10-11-2026 | 0.034 | 88.6th | [Strapi](https://github.com/strapi/strapi/releases) |
| CVE-2026-88779 | Citrix NetScaler (DoS) | 10-04-2026 | 10-07-2026 | 0.006 | 46.7th | [Citrix](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697174) |

CISA confirmed each is actively exploited as of its "Added" date. Known ransomware-campaign use: not flagged (Unknown) for all six. The low-EPSS rows (ONLYOFFICE, Strapi, Citrix) are still in the KEV, so they're being exploited — EPSS just says less likely to be widely automated than the top three.

### Ransomware victims, last 24h (sector pulse — treat as sector-targeting signal, not proof)

| Group | Sector | Country | Date |
|---|---|---|---|
| rhysida | Government & Defense | US | 10-09-2026 |
| chaos | Healthcare | US | 10-09-2026 |
| Deadlock | Not Found (machine-vision supplier) | US | 10-09-2026 |
| threeam | Transportation | US | 10-09-2026 |
| Deadlock | Healthcare (pharma) | ES | 10-09-2026 |
| safepay | Hospitality | CH | 10-09-2026 |
| safepay | Other (metal roofs & facades) | DE | 10-09-2026 |
| Panzer | Energy & Utilities | SG | 10-09-2026 |
| Panzer | Technology | — | 10-09-2026 |
| qilin | Not Found | SE | 10-09-2026 |

Four US posts in the last 24 hours — a government county, a healthcare provider, a machine-vision supplier, and a trucking/fleet company — plus a European pharma and hospitality string. Ransomware crews are not staying in one industry; the US sees healthcare and public-sector targets alongside small manufacturers and fleet operators. Source: [ransomware.live](https://www.ransomware.live)

### Notable vulnerabilities (CIRCL lookup)

- **WordPress plugin batch (10-10-2026):** beyond the two headline items, today's disclosures include stored XSS in LTL Freight Quotes (CVE-2026-87780), authorization bypasses that leak customer data / forge payments in Contact Form 7 PayPal (CVE-2026-105990, CVE-2026-105989), and a brute-forcible registration PIN (CVE-2026-107120). If you run WordPress, treat today as plugin-update day. Sources: [CVE-2026-87780](https://nvd.nist.gov/vuln/detail/CVE-2026-87780) · [CVE-2026-105990](https://nvd.nist.gov/vuln/detail/CVE-2026-105990)
- **Kendo UI chart libraries (10-10-2026):** KendoReact and Kendo UI for Vue chart tooltips render point values as raw HTML without encoding, enabling stored XSS in BI/dashboard components (CVE-2026-106138, CVE-2026-106139). If you build internal dashboards with Kendo, update. Sources: [CVE-2026-106138](https://nvd.nist.gov/vuln/detail/CVE-2026-106138) · [CVE-2026-106139](https://nvd.nist.gov/vuln/detail/CVE-2026-106139)

### CISA ICS advisory (Satel Netco Design, 09-27-2026)

Satel Netco Design, a building-communications design tool used in the communications sector, has XSS, denial-of-service, and path-traversal flaws (v3 CVSS 8.8 total); fix is v2.1.7. Low SMB relevance unless you work in telecom/building comms. Source: [ICSA-26-281-03](https://www.cisa.gov/news-events/ics-advisories/icsa-26-281-03)

### IOC sample (block-and-hunt signals — do not visit)

| Type | Value | Malware |
|---|---|---|
| domain | brigitte7.workers.dev | php.shin_webshell |
| domain | jp168amp-super.com | ClearFake |
| domain | google-proxy-66-102-8-168.google.com | php.shin_webshell |
| URL | http://105.184.158.253:37135/Mozi.m | Mozi |
| URL | http://144.48.130.194:47077/Mozi.m | Mozi |
| URL | http://125.40.153.124:36333/Mozi.a | Mozi |
| URL | http://117.134.206.218:41681/Mozi.m | Mozi |
| URL | http://139.135.40.51:47099/Mozi.m | Mozi |
| URL | http://94.154.43.26/main_arm7 | (URLhaus) |

A Mozi botnet spread cluster (several IPs serving Mozi binaries) plus fake-browser-update (ClearFake) and PHP-webshell domains are the day's signal. Host `94.154.43.26` is serving several architecture variants (x86_64, arm, mips, sh4, ppc, m68k) — a classic multi-platform botnet-drop host. Source: [ThreatFox](https://threatfox.abuse.ch/) (via [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/)) · [URLhaus](https://urlhaus.abuse.ch/)

---

*Compiled from public sources · 10-10-2026*
