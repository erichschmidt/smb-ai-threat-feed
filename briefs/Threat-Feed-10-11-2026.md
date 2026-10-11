---
type: threat-feed-note
title: "Threat Feed - 10-11-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-10-11
updated: 2026-10-11
---

# Threat Feed — 10-11-2026

**The 3-minute read for small businesses running AI and automation.** Plain language in the headlines, deeper detail below. Every score and source is explained so you can act without a security degree. Full plain-English glossary: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md)

*AI-drafted from public data and published automatically. No one reviews each brief before it goes out. Check the linked source before you act.*

## How to read the scores

- **CISA KEV:** If a vulnerability is on this list, it is *being actively exploited right now*, not theoretical. "CISA confirmed" = the authoritative "patch fast" signal.
- **EPSS:** A 0–1 score estimating how likely a flaw is to be exploited in the next 30 days; higher = patch first. The percentile says where it ranks — 99th percentile means it's more likely to be exploited than 99% of all known vulnerabilities.
- **CVSS:** A 0–10 severity score. 9.8/10 = critical, typically exploitable remotely with no login. Answers "how bad if it works"; EPSS/KEV answer "is it actually being used."

---

## 1. HIGH — The AI "chat with your data" helper is still your top AI-layer fix: a question over the network can become a database break-in

**CVE-2024-8309 — LangChain GraphCypherQAChain** · EPSS 0.137 (96th percentile — more likely to be exploited than 96% of all known vulnerabilities) · not in KEV, but EPSS crosses the exploitation-likelihood bar

**What broke.** LangChain — the open-source framework many developers use to build "chat with your data" AI apps — has a helper (GraphCypherQAChain) that turns a chat question into a database query. The flaw is a **SQL injection** (an attacker types malicious commands into an input or prompt, tricking the app into running unauthorized queries), triggered through a prompt, that works against a **graph database** (a database that stores records and their relationships as connected points). A crafted question or a poisoned chat source can make the tool read, change, or delete data it should never touch. CVSS 9.8/10 = critical — exploitable remotely with no login. This item reappears in today's vulnerability lookup with a fully documented trail (a public bounty report plus the upstream fix commit), which is why it remains the standing AI-stack priority.

*Conceptual attacker view:* attacker gets a prompt into the pipeline — a shared document, a support ticket, a form field — laced with a hidden instruction; the helper builds a database query from it; if the query isn't locked down, the attacker's clause executes against your data. Defender observables: unexpected or generated SQL/Cypher statements and reads/writes hitting your database at odd times.

**Why it matters to an SMB running AI tools.** This is exactly the pattern small businesses are shipping: an AI assistant that answers questions about their own business data. If that assistant is built on LangChain's GraphCypherQAChain and pulls from a graph store, an attacker who can get a prompt into the pipeline can write to the database instead of just reading it. It's the AI data-source layer itself, not a generic IT box, so if you built on the affected helper at all, it's your highest-priority AI-layer fix.

**What you do Monday** (about 20 minutes):
1. Identify any AI chatbot or "talk to your data" tool built on LangChain that queries a graph database, and check the `langchain-community` / `langchain` version you're running.
2. Update to the patched release that fixes CVE-2024-8309 — confirm against the fix commit below.
3. Hardening that costs little now: connect the tool to the database through a read-only, least-privilege service account, and restrict the queries it can generate.

**Sources:** [huntr bounty](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5) · [LangChain fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) · [GitHub advisory GHSA-45pg-36p6-83v9](https://github.com/advisories/GHSA-45pg-36p6-83v9)

---

## 2. WATCH — A tool that checks downloaded AI models for hidden code can be fooled by a renamed file — verify your model-loading rules

**CVE-2025-1889 — picklescan (before 0.0.22)** · EPSS 0.004 (low — needs an attacker to get a model file into your pipeline, so not widely automated) · not in KEV

**What broke.** picklescan is a safety scanner teams use to inspect downloaded AI model files for embedded malicious code before loading them. Versions before 0.0.22 only looked in scope at files with the standard **pickle** (the Python file format used to save and reload data objects — and a classic loading place for attacker code) **extension** (the letters after the dot in a file name, like `.pkl` or `.pt`). An attacker could craft a malicious model saved under a non-standard extension and it would sail past the scan.

**Why it matters to an SMB running AI tools.** If you download and load third-party or vendor-supplied model files (from a model hub or an integration that pulls models down), this is a supply-chain weak point: a hidden executable bundled inside a "model" that your pipeline happily loads. Loading it runs attacker code on the machine running your AI stack. If the tool you use to defend against that very risk can be named around, the risk you thought you closed is not actually closed.

**What you do Monday** (about 15 minutes, if you scan models before loading):
1. Check the version you run in your model-loading pipeline: `pip show picklescan`.
2. Upgrade to 0.0.22 or later.
3. Add a rule that any model file that enters production passes picklescan — regardless of its file extension — before it is loaded.

**Sources:** [Sonatype advisory](https://sites.google.com/sonatype.com/vulnerabilities/cve-2025-1889) · [GitHub advisory GHSA-769v-p64c-89pr](https://github.com/advisories/GHSA-769v-p64c-89pr)

---

## 3. WATCH — An AI gateway that fronts all your model keys has flaws around stored keys and spend logs — tighten who reaches the admin screens

**CVE-2026-108575 / CVE-2026-108574 — BerriAI LiteLLM (up to 1.94.0 / 1.95.0)** · low CVSS (not scored this run) · no exploitation evidence yet · not in KEV

**What broke.** LiteLLM is a popular **gateway** (a single service that sits in front of many AI model providers, managing keys, usage, and access so teams don't hardcode credentials everywhere) teams self-host to centralize how they call AI models. Two flaws landed: one in how it resolves stored credentials mis-handles an **API key** (a stored secret an app uses to call an AI service) so a lower-privileged role can reach a key it shouldn't (CVE-2026-108575); the other lets a lower-privileged user view other users' session spend logs (CVE-2026-108574). Both are limited in scope — low severity — but they sit in a control point for credentials.

**Why it matters to an SMB running AI tools.** An AI gateway is where the keys to the AI tools you pay for all live. Because it centralizes credentials, it's worth treating as a serious host even when the individual flaws look small: a low-impact hole in the credential hub matters more than the same score in a random web app. If you run LiteLLM (or a similar gateway) as your API-key manager, this is a version check and an access review, not a fire drill.

**What you do Monday** (about 20 minutes, if you run LiteLLM):
1. Check your LiteLLM version.
2. Upgrade past 1.95.0 so both fixes are included.
3. Review which roles/accounts can see the spend-tracking and secret-facing admin pages, and trim to least privilege.

**Sources:** [NVD — CVE-2026-108575](https://nvd.nist.gov/vuln/detail/CVE-2026-108575) · [NVD — CVE-2026-108574](https://nvd.nist.gov/vuln/detail/CVE-2026-108574)

---

## 4. CRITICAL — Old Apache Struts web apps (they're still out there) have a remote-code hole CISA says is being actively attacked — find them and patch now

**CVE-2016-3081 — Apache Struts** · EPSS 0.961 (99.8th percentile — among the most likely flaws in existence to be exploited) · in CISA KEV — reason for CRITICAL: actively exploited · remote code execution without a login

**What broke.** Apache Struts 2 (a Java web framework) has a **command injection** (a way to make the app run commands on the server) flaw reachable through its **dynamic method invocation** (a setting that lets a URL pick which method the app runs) feature. An attacker can send a crafted URL and get the server to execute their own code. CISA added this to its actively-exploited list on 10-08-2026.

**Why it matters to an SMB running AI tools.** General IT hygiene — the AI angle is not special here. An AI and automation stack usually sits in front of, or beside, older web apps. If any of your line-of-business apps (or one a vendor hosts for you) is Struts-based, this is a path an attacker uses to get a foothold on your network — and once they're in, they can move toward the AI servers and the data they touch. Struts is old enough that the honest question is "do we still run it," not "is it new."

**What you do Monday** (about 30 minutes):
1. Ask whoever runs your web apps whether any of them is built on Apache Struts 2 (a Java web framework).
2. If yes, ensure dynamic method invocation is off and apply the available Struts updates.
3. If you're not sure, have IT run a scan of web-facing and internal apps for a Struts fingerprint.

**CISA metrics:** Confirmed being actively exploited as of 10-08-2026. Federal agencies must patch by **10-11-2026** (the CISA/BOD deadline — the urgency anchor). Known ransomware-campaign use: not flagged.

**Sources:** [NVD — CVE-2016-3081](https://nvd.nist.gov/vuln/detail/CVE-2016-3081) · [Apache advisory S2-032](https://cwiki.apache.org/confluence/display/WW/S2-032)

---

## 5. CRITICAL — The network-address software at the core of the internet is being actively hit with a remote crash bug — if you run your own DNS, patch today

**CVE-2015-5477 — ISC BIND** · EPSS 0.994 (99.9th percentile — among the most likely flaws in existence to be exploited) · in CISA KEV — reason for CRITICAL: actively exploited · remote, no login needed

**What broke.** BIND is the most widely used name-server (DNS) software on the internet — it's what translates a site name into an address. A data-processing bug lets a specially crafted TKEY query crash the server — a **denial of service** (the service stops answering, so nobody gets in — including you) that can take a DNS server offline remotely with no login. CISA added it to its actively-exploited list on 10-08-2026.

**Why it matters to an SMB running AI tools.** General IT hygiene — no specific AI angle beyond "your outbound calls depend on it." If you or a vendor run your own BIND-based DNS (your domain's name resolution, sometimes your internal network lookups), a crash here takes domains and servers offline for customers — and your AI integrations, email, and web all stop resolving. Most small businesses use their registrar or ISP for DNS and are not affected; this is aimed at whoever runs BIND servers directly.

**What you do Monday** (about 20 minutes, only if you run BIND):
1. Confirm whether any server you run is a BIND DNS server (`named` process / version check).
2. If yes, patch BIND to the fixed release — this flaw's fixes are in the standard vendor errata.
3. If a vendor or registrar manages DNS for you (most common), no action — confirm they do, and move on.

**CISA metrics:** Confirmed being actively exploited as of 10-08-2026. Federal agencies must patch by **10-11-2026**. Known ransomware-campaign use: not flagged.

**Sources:** [Red Hat errata RHSA-2015:1513](https://access.redhat.com/errata/RHSA-2015:1513.html) · [ISC advisory](https://web.archive.org/web/20150729014733/https://kb.isc.org/article/AA-01272)

---

## Jargon buster

- **API key:** A stored secret an app uses to call an AI (or another) service. A gateway that holds many of them is a concentration of keys worth protecting.
- **Command injection:** Tricking software into running operating-system commands the attacker chose.
- **Denial of service (DoS):** The service stops answering, so nobody gets in — including you.
- **Dynamic method invocation:** A Struts setting that lets a URL pick which method the app runs; when enabled, it opens the command-injection path.
- **Gateway (AI):** A single service that sits in front of many AI providers, managing keys, usage, and access — a controlled front door for all your AI calls.
- **Graph database:** A database that stores things and their relationships as connected points. AI tools may query it to answer questions about linked business records.
- **SQL injection:** A technique where attackers type malicious database commands into an input box (or a prompt), tricking the app into running unauthorized queries — reading, changing, or deleting data.

*(All other terms used above — LangChain, GraphCypherQAChain, KEV, EPSS, CVSS, RCE, prompt injection, pickle, file extension, CISA, BOD 26-04, path traversal, XSS — are in the [master glossary](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).)*

---

## Appendix

### CISA KEV — actively exploited, ranked by EPSS (most likely to be exploited first)

No new KEV additions today — the catalog still lists the 10-08 batch below, all being actively exploited, federal patch deadline 10-11-2026.

| CVE | Product | Added | Fed deadline | EPSS | EPSS %ile | Source |
|---|---|---|---|---|---|---|
| CVE-2015-3306 | ProFTPD | 10-08-2026 | 10-11-2026 | 0.995 | 99.9th | [ProFTPD](http://www.proftpd.org/) |
| CVE-2015-5477 | ISC BIND (DoS) | 10-08-2026 | 10-11-2026 | 0.994 | 99.9th | [Red Hat](https://access.redhat.com/errata/RHSA-2015:1513.html) |
| CVE-2016-3081 | Apache Struts | 10-08-2026 | 10-11-2026 | 0.961 | 99.8th | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2016-3081) |
| CVE-2021-3199 | ONLYOFFICE Docs | 10-08-2026 | 10-11-2026 | 0.194 | 97.3rd | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2021-3199) |
| CVE-2023-22894 | Strapi | 10-08-2026 | 10-11-2026 | 0.036 | 89.2nd | [Strapi releases](https://github.com/strapi/strapi/releases) |

CISA confirmed each is being actively exploited as of its "Added" date. Known ransomware-campaign use: not flagged (Unknown) for all five. The low-EPSS rows (ONLYOFFICE, Strapi) are still in the KEV, so they're being exploited — EPSS just says less likely to be widely automated than the top three.

### Ransomware victims, last 24h (sector pulse — treat as sector-targeting signal, not proof)

| Group | Sector | Country | Date |
|---|---|---|---|
| qilin | Energy & Utilities | CO | 10-11-2026 |
| rhysida | Professional Services (law firm) | US | 10-10-2026 |
| exitium | Manufacturing | JP | 10-10-2026 |
| Redact | Healthcare (medical equipment) | US | 10-10-2026 |
| dragonforce | Manufacturing | TW | 10-10-2026 |
| thegentlemen | Government & Defense | TH | 10-10-2026 |
| UmBra | Education | EG | 10-10-2026 |
| qilin | Hospitality | US | 10-10-2026 |

Two stand out for a small-business audience. The **rhysida** post describes a US law firm with banking details, SSNs, client signatures, and tax forms among the claimed haul — a reminder that professional-services firms (accountants, lawyers, bookkeepers) hold exactly the data exfiltrators want, and that reaching that data in a practice's email is often the goal. The **exitium** post against a Japanese manufacturer carries an ultimatum (data sale unless contacted by 10-13-2026) and claims 5.8 TB spanning contracts and confidential files. Source: [ransomware.live](https://www.ransomware.live)

### Notable vulnerabilities (CIRCL lookup)

- **BerriAI LiteLLM (10-11-2026):** the AI-gateway pair featured in item 3 (credential/secret handling and spend-log access), plus a related low-severity spend-log issue. Sources: [CVE-2026-108575](https://nvd.nist.gov/vuln/detail/CVE-2026-108575) · [CVE-2026-108574](https://nvd.nist.gov/vuln/detail/CVE-2026-108574)
- **WordPress plugin batch (10-11-2026):** a large cluster of unauthenticated SQL injection, stored-XSS, and option-overwrite flaws across many plugins (Post Voting System CVE-2026-89302, WpCues quiz CVE-2026-89214, Site Setup Wizard CVE-2026-89195, AI Content Generator Marketing CVE-2026-85118, Piotnet Forms unauthenticated file-upload RCE CVE-2026-96227, and others). If you run WordPress, treat today as plugin-update day. Source samples: [CVE-2026-96227](https://nvd.nist.gov/vuln/detail/CVE-2026-96227) · [CVE-2026-85118](https://nvd.nist.gov/vuln/detail/CVE-2026-85118)
- **Casdoor (10-11-2026):** self-hosted login server, server-side request forgery in proxy validation (CVE-2026-108572). Server-side request forgery means a crafted request can make the identity server reach internal services. If you run Casdoor, update. Source: [CVE-2026-108572](https://nvd.nist.gov/vuln/detail/CVE-2026-108572)

### CISA ICS advisory (Satel Netco Design, 10-08-2026)

Satel Netco Design, a building-communications / security-automation design tool, has XSS, denial-of-service, and path-traversal flaws (one path-traversal case can reach arbitrary code execution under certain conditions; v3 CVSS up to 8.8); fix is v2.1.7, no known public exploitation yet. Low SMB relevance unless you or a security integrator programs/builds Satel systems with it — then ask them to confirm they're on v2.1.7. Source: [ICSA-26-281-03](https://www.cisa.gov/news-events/ics-advisories/icsa-26-281-03)

### IOC sample (block-and-hunt signals — do not visit)

| Type | Value | Malware |
|---|---|---|
| URL | http://crownsquareproductions.com:4219 | Remus (RAT) |
| URL | http://tyxa.today:4894 | Remus (RAT) |
| domain | antimalwarediagnostics.st (api/* endpoints) | Unknown malware |
| URL | http://115.53.220.37:43200/i | (URLhaus) |
| URL | http://91.92.242.236/files-129312398/.../file_4aa3e284d0ae6318.exe | (URLhaus) |
| URL | http://221.235.139.104:57238/bin.sh | (URLhaus) |

Remus is a remote-access trojan family — a URL hosting its drop is a block-and-hunt signal. `antimalwarediagnostics.st` is a freshly-registered-looking fake "scan/upload" domain (several malicious API paths) worth treating as active. The URLhaus rows are live content/drop hosts serving binaries and scripts. Source: [ThreatFox](https://threatfox.abuse.ch/) (via [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/)) · [URLhaus](https://urlhaus.abuse.ch/)

---

*Compiled from public sources · 10-11-2026*
