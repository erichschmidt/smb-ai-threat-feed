---
type: threat-feed-note
title: "Threat Feed - 08-26-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-08-26
source: "cisa-kev, cisa-advisories, ransomware.live, circl, epss, threatfox, urlhaus"
related: "https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md"
---

# Threat Feed — 08-26-2026

> **Reader promise:** 3-minute read. Headlines alone tell you what to do. New term? Check the [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).
> **Lens:** threats that hit AI tools, automations, and small-business money.
> **Sources:** every finding links to its primary source. If you want to verify, click.

## How to read the scores (30 seconds)
- **EPSS (0–1):** a score estimating how likely this flaw is to be exploited in the next 30 days; higher = patch first. 0.78 ≈ 78% — patch first. 0.01 ≈ 1% — lower urgency. Percentile ranks it against every known flaw: 99.5th = more likely to be exploited than 99.5% of all known vulnerabilities.
- **CISA KEV:** CISA only adds a flaw after confirming it's being **actively exploited right now** — not theoretical. The date shown is when CISA confirmed it. The federal deadline is their urgency rating in date form.
- **Today's window:** no new actively-exploited vulnerabilities were added to CISA KEV on 08-26-2026. Five entries remain in the last 7 days. Newest is Gitea (added 08-25-2026). Oracle's federal clock hits **tomorrow (08-27-2026)**; Gitea's hits **08-28-2026**. Zimbra and one TrueConf hole already missed their deadlines.

---

## 1. HIGH — Your LangChain chat-with-data chain can still be tricked into rewriting the database
**CVE-2024-8309** · CIRCL / GHSA (not on CISA KEV) · **EPSS 0.1374 (96.2nd percentile)** — above the 0.1 "patch first" flag · CVSS 9.8/10 = critical — scored as exploitable remotely with no login
**Sources:** [GHSA](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [Fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) · [huntr](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2024-8309)

**What broke:** LangChain's **GraphCypherQAChain (the piece that turns a chat question into a graph-database query)** in the 0.2.5-era packages can be steered by **prompt injection (hiding instructions inside the data the AI reads)** so the generated query becomes a database write, delete, or data grab. This is not a new CISA listing — scanners and CIRCL are still surfacing leftover 0.2.x installs. If you never used LangChain's graph-chat chain, you're done.

**Why it matters to an SMB running AI tools:** This is the on-lens item: the broken product *is* the AI framework. "Chat with the knowledge graph" tools often sit on customer, inventory, or ticket data. A leftover unpatched chain means a crafted document or chat turn can become a database change — and anything Copilot-style that reads that graph inherits the poison.

**What you do Monday (15 minutes):**
1. Ask whoever built the chatbot: *"Do we use LangChain GraphCypherQAChain? What version is `langchain` / `langchain-community`?"* (`pip show langchain langchain-community`)
2. If `langchain` is below **0.2.0**, or `langchain-community` is below **0.2.19**, upgrade today. Current 0.3.x builds are past this hole.
3. Until patched: do not let that chain run write queries, and keep the graph database off the public internet.

**CISA metrics:** this item is from CIRCL + FIRST EPSS, not CISA KEV. CISA has not listed it as actively exploited. Known ransomware-campaign use: not flagged. Treat EPSS 0.1374 (more likely than 96.2% of known flaws) as the prioritization signal, then verify the package version.

**Attacker view (conceptual):** Hide instructions in a document the chatbot is allowed to read → the chain turns them into a graph-database change → customer or inventory records move. Defender rule of thumb: unexpected CREATE/DELETE queries from the chatbot's database account are the tell.

---

## 2. CRITICAL — Your self-hosted Git server can be taken over by anyone who can write to a repo — CISA just confirmed it's being used
**CVE-2026-60004** · CISA confirmed active exploitation **08-25-2026** · federal patch deadline **08-28-2026** · EPSS not scored yet · CVSS 9.8/10 = critical — scored as exploitable remotely with no login
**Sources:** [Gitea advisory GHSA-rcr6-4jqh-j84m](https://github.com/go-gitea/gitea/security/advisories/GHSA-rcr6-4jqh-j84m) · [CISA alert 08-25-2026](https://www.cisa.gov/news-events/alerts/2026/08/25/cisa-adds-one-known-exploited-vulnerability-catalog) · [CVE record](https://www.cve.org/CVERecord?id=CVE-2026-60004) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-60004) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** **Gitea (a self-hosted Git / source-code server)** from 1.17 up to but not including **1.27.1** will accept a malicious patch through its patch API and plant a **Git hook (a script Git runs automatically on a repo event)** that then runs shell commands as the Gitea service account. You don't need the patch-format detail — just know write access to a repo is enough, and if sign-up is left open a stranger can create that access themselves. If you don't run Gitea, you're done.

**Why it matters to an SMB running AI tools:** This is not an AI-product bug. It is the box that often holds the prompts, agent code, n8n workflows, and API keys your automations pull from. If Gitea is owned, the attacker is inside the same repos your CI and AI tools clone.

**What you do Monday (20 minutes):**
1. Ask whoever owns source control: *"Do we run Gitea? What version?"* Check **Site Administration → Configuration**, or run `gitea --version` on the host. If no Gitea, you're done.
2. Upgrade to **Gitea 1.27.1 or later**. If you cannot patch today: turn **open registration off** and take the server off the public internet (VPN or private network only).
3. Tell IT: *"CVE-2026-60004 is on CISA's actively-exploited list as of 08-25-2026. Federal deadline is 08-28-2026. Upgrade Gitea to 1.27.1, disable public sign-up, and look for unexpected Git hooks or new admin users."*

**CISA metrics:** CISA confirmed this is being actively exploited as of 08-25-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch by 08-28-2026. Required action: upgrade to Gitea 1.27.1 (and stop exposing an open-registration instance to the internet).

**Attacker view (conceptual):** Get write access to a repo (open sign-up, or a leftover token) → send a crafted patch to the server's patch API → a hook runs as the Gitea account. Defender rule of thumb: public registration you forgot was on; unexpected hooks or new repos; the Gitea service account doing work you didn't schedule.

---

## 3. CRITICAL — The front door in front of your Oracle apps can be fully owned — federal deadline is tomorrow
**CVE-2026-21962** · CISA confirmed active exploitation **08-24-2026** · federal patch deadline **08-27-2026 (tomorrow)** · **EPSS 0.4202 (98.6th percentile)** · CVSS 10.0/10 = critical — exploitable remotely with no authentication
**Sources:** [Oracle January 2026 Critical Patch Update](https://www.oracle.com/security-alerts/cpujan2026.html) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-21962) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** **Oracle HTTP Server** and the **WebLogic Server Proxy Plug-in (the forwarder that sits on Apache or IIS in front of WebLogic apps)** versions **12.2.1.4.0, 14.1.1.0.0, and 14.1.2.0.0** fail to check who is allowed to do what. An unauthorized network caller can create, change, or delete critical data — up to complete access to the component. You don't need the plug-in internals — CISA says this is being exploited, and Oracle scored it a 10.

**Why it matters to an SMB running AI tools:** WebLogic is the engine room behind a lot of mid-size ERP, CRM, and portal stacks. Those same systems are the data sources Copilot and "chat with your business apps" tools read. If the HTTP front door is owned, the attacker is inside the records those assistants summarize.

**What you do Monday (30 minutes — do it today if you run these):**
1. Ask whoever owns ERP/CRM/intranet: *"Do we run Oracle HTTP Server or the WebLogic Server Proxy Plug-in? Which version?"* If no, you're done.
2. Apply Oracle's **January 2026 Critical Patch Update** from My Oracle Support for the Fusion Middleware / HTTP Server / Proxy Plug-in packages on 12.2.1.4.0, 14.1.1.0.0, or 14.1.2.0.0.
3. Tell IT: *"CVE-2026-21962 is on CISA's actively-exploited list as of 08-24-2026. Federal deadline is 08-27-2026. Apply the January 2026 CPU today. If this box is internet-facing, treat it as check-this-host, not patch-and-forget."*

**CISA metrics:** CISA confirmed this is being actively exploited as of 08-24-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch by 08-27-2026. Required action: apply the January 2026 Oracle Critical Patch Update for HTTP Server / WebLogic Proxy Plug-in.

---

## 4. HIGH — Your self-hosted email server is still exposed after CISA's deadline
**CVE-2026-73570** · CISA confirmed active exploitation **08-21-2026** · federal patch deadline **08-24-2026 (missed)** · EPSS 0.0151 (72.4th percentile) — **KEV is the signal, not EPSS**
**Sources:** [Zimbra security advisories](https://wiki.zimbra.com/wiki/Zimbra_Security_Advisories) · [Zimbra 10.1.20 patch notes](https://blog.zimbra.com/2026/07/patch-release-update-zimbra-10-1-20/) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-73570) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** **Zimbra Collaboration Suite (self-hosted email and calendar)** before **10.1.20** will run an attacker-chosen operating-system command as the Zimbra user if the optional **SNMP (the "tell the monitoring box that mail arrived")** package is installed and notifications are on. The trigger is a specially crafted incoming mail — no login required. If you don't run Zimbra, you're done.

**Why it matters to an SMB running AI tools:** Inbox, calendar, and attachment stores are the default data source for Copilot and every "summarize my email" automation. If the mail server is owned, the attacker is inside the same stream those tools read — invoices, password resets, customer threads, and anything an assistant is allowed to see. CISA's federal clock already passed.

**What you do Monday (15 minutes — do it today if you still run unpatched Zimbra):**
1. On the Zimbra host: `yum update` or `apt update` and install **ZCS 10.1.20 or later**. Confirm the version in the admin console.
2. If you cannot patch today: turn **SNMP notifications off** and remove the `zimbra-snmp` package until 10.1.20 is on.
3. Tell IT: *"CVE-2026-73570 is on CISA's actively-exploited list as of 08-21-2026. Federal deadline was 08-24-2026. Upgrade Zimbra to 10.1.20 and check the host for unexpected zimbra-user processes."*

**CISA metrics:** CISA confirmed this is being actively exploited as of 08-21-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch by 08-24-2026. Required action: upgrade to Zimbra 10.1.20 (or disable SNMP notifications until you can).

---

## 5. WATCH — Ransomware crews posted manufacturing, schools, clinics, and small US shops — test a restore
**Ransomware.live sector pulse, 08-25-2026 to 08-26-2026:** 10 recent victim disclosures in this run. **qilin** posted three (manufacturing in GB and RO; US education). **chaos** posted three (Netherlands "other," US professional services, and a US primary-care clinic listed under a mismatched country field). **Global Secret Group** posted two US small shops (construction / paving and a car dealer). Also in the batch: **safepay** (KR manufacturing) and **AuditTeam** (RU, sector not given).
**Sources:** [Ransomware.live](https://www.ransomware.live)

**What broke:** Nothing new in your software, necessarily — these are victim disclosures. The pattern is the point: manufacturing is in the dump again, a US school is in it, a clinic is in it, and two of the named US targets are the size of a real small business (dozens of employees, not a Fortune 500).

**Why it matters to an SMB running AI tools:** New AI connectors (inbox, drive, CRM, clinic or accounting export) are often the least-watched door. Ransomware crews do not need a clever AI exploit if the shop PC or file server has never had a restore test and the new automation has no MFA. If your assistant reads those systems, a ransomed shop or clinic export is an AI data-source problem.

**What you do Monday (30 minutes):**
1. **Test one backup restore.** Not "check the job ran" — restore one folder to a spare machine. If you can't, that is the finding.
2. Any AI or automation added this year: turn on **MFA (multi-factor authentication — password plus a phone code or key)** and cut its access to only the folders it needs.
3. If you are in manufacturing, education, healthcare, construction, auto retail, or professional services, tell IT: *"Ransomware.live showed a qilin manufacturing/education dump plus chaos clinic/services claims and two small US shop claims on 08-25-2026 / 08-26-2026. Walk the backup restore and the new AI connectors today."*

**CISA metrics:** this section is from Ransomware.live (victim disclosures), not CISA KEV. No single CVE applies. Pair it with the patch list above.

---

## Jargon buster (terms used today)
- **CVE:** a unique ID for a security flaw, so everyone tracks the same bug (like a license plate).
- **RCE (Remote Code Execution):** attacker can run their own code on your machine — full control.
- **EPSS:** 0–1 score of how likely a flaw is to be exploited in the next 30 days. Higher = patch first.
- **Percentile:** where a score ranks — 98.6th = more likely to be exploited than 98.6% of known flaws.
- **KEV (Known Exploited Vulnerabilities):** CISA's list of flaws being actively exploited right now.
- **CVSS:** a 0–10 severity score. 9.8/10 = critical; 10.0/10 = the top of the scale — typically exploitable remotely with no login.
- **LangChain:** a popular framework for building "chat with your data" apps. Flaws in it hit lots of AI tools at once.
- **GraphCypherQAChain:** LangChain's helper that turns a chat question into a graph-database query. If that query isn't locked down, the chat becomes a database write.
- **Prompt injection / SQL injection:** hiding instructions or database commands inside the data an AI or app reads.
- **Gitea:** a self-hosted Git (source-code) server many small teams run instead of GitHub.
- **Git hook:** a small script Git runs automatically when something happens in a repo. If an attacker plants one, it runs with the Git server's own permissions.
- **Code injection:** tricking software into running attacker-supplied commands as if they were part of the program.
- **Oracle HTTP Server / WebLogic Server Proxy Plug-in:** the front door in front of many Oracle business apps; the plug-in sits on Apache or IIS and forwards traffic to WebLogic.
- **Improper access control:** the product fails to check who is allowed to do what.
- **Zimbra / ZCS:** a self-hosted email and calendar suite used by many schools, governments, and small orgs.
- **SNMP:** a simple monitoring protocol devices use to report "I'm up / something broke." Wired into email notifications, a crafted message can become a command.
- **Command injection:** tricking software into running operating-system commands the attacker chose.
- **SMTP:** the internet's send-mail protocol. "Crafted SMTP" here means a specially built incoming email.
- **TrueConf:** an on-premises video-meeting server. A hole here is a hole in the meeting room and often the recordings.
- **Isolated environment / sandbox:** a cage meant to contain a program. A "breakout" means the attacker escaped onto the real machine.
- **Ransomware:** malware that locks your files and demands payment — the top small-business threat.
- **MFA (Multi-Factor Authentication):** password plus a second proof (phone code). Cheapest real defense.
- **qilin / chaos / safepay / AuditTeam / Global Secret Group:** ransomware groups in today's victim disclosures.
- **picklescan:** a scanner meant to catch dangerous Python pickle files inside AI model downloads. If it skips a file, a "model" can be malware.
- **IOC (Indicator of Compromise):** a trace of an attack (malicious IP/domain/file) to hunt for in logs.
- **Lumma Stealer:** malware that steals saved passwords, cookies, and wallet files from a Windows PC.
- **XMRIG:** a crypto-miner. In an IOC list it means someone is stealing CPU time, not running a legit miner.
- **RAT (Remote Access Trojan):** malware that gives an attacker remote control of a machine.
- **Webshell:** a small script planted on a hacked website so the attacker can come back and run commands later.

Full plain-language library: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).

---

## Appendix — raw signals (for the technical reader)

### CISA KEV (last 7 days, ranked by EPSS — links to vendor advisories)
| CVE | Product | EPSS | CISA confirmed | Federal deadline | Ransomware use | Source |
|---|---|---|---|---|---|---|
| CVE-2026-21962 | Oracle HTTP Server / WebLogic Proxy Plug-in (access control) | **0.4202** | 08-24-2026 | 08-27-2026 | Unknown | [Oracle Jan 2026 CPU](https://www.oracle.com/security-alerts/cpujan2026.html) |
| CVE-2026-72530 | TrueConf Server (code injection / breakout) | 0.0183 | 08-20-2026 | 09-03-2026 | Unknown | [Kaspersky](https://ics-cert.kaspersky.com/advisories/2026/08/11/trueconf-server-breakout-from-isolated-environment/) |
| CVE-2026-72529 | TrueConf Server (missing authentication) | 0.0155 | 08-20-2026 | 08-23-2026 | Unknown | [Kaspersky](https://ics-cert.kaspersky.com/advisories/2026/08/11/trueconf-server-missing-authentication-for-critical-function/) |
| CVE-2026-73570 | Synacor Zimbra ZCS (OS command injection via SMTP) | 0.0151 | 08-21-2026 | 08-24-2026 | Unknown | [Zimbra 10.1.20](https://blog.zimbra.com/2026/07/patch-release-update-zimbra-10-1-20/) |
| CVE-2026-60004 | Gitea (code injection via patch API / Git hook) | n/a | 08-25-2026 | 08-28-2026 | Unknown | [GHSA](https://github.com/go-gitea/gitea/security/advisories/GHSA-rcr6-4jqh-j84m) |

### Ransomware.live — recent victims (10)
| Group | Sector | Country | Discovered | Source |
|---|---|---|---|---|
| qilin | Manufacturing | GB | 08-26-2026 | [Ransomware.live](https://www.ransomware.live) |
| qilin | Education | US | 08-25-2026 | [Ransomware.live](https://www.ransomware.live) |
| AuditTeam | Not Found | RU | 08-25-2026 | [Ransomware.live](https://www.ransomware.live) |
| safepay | Manufacturing | KR | 08-25-2026 | [Ransomware.live](https://www.ransomware.live) |
| chaos | Other | NL | 08-25-2026 | [Ransomware.live](https://www.ransomware.live) |
| chaos | Professional Services | US | 08-25-2026 | [Ransomware.live](https://www.ransomware.live) |
| chaos | Not Found | CN | 08-25-2026 | [Ransomware.live](https://www.ransomware.live) |
| qilin | Manufacturing | RO | 08-25-2026 | [Ransomware.live](https://www.ransomware.live) |
| Global Secret Group | Transportation | US | 08-25-2026 | [Ransomware.live](https://www.ransomware.live) |
| Global Secret Group | Retail & E-Commerce | US | 08-25-2026 | [Ransomware.live](https://www.ransomware.live) |

No leak-site or .onion links.

### CIRCL — highest-signal new items (30 pulled; 28 empty/unparseable records skipped)
- **CVE-2024-8309 (EPSS 0.1374, 96.2nd pct)** — LangChain GraphCypherQAChain SQL injection via prompt injection; `langchain` patched at **0.2.0**, `langchain-community` patched at **0.2.19** — [GHSA](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [Fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) · [huntr](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5)
- **CVE-2025-1889 (EPSS 0.0038, 30.9th pct)** — picklescan missed non-standard pickle extensions in ML model files; upgrade picklescan to **0.0.22 or later** — [GHSA](https://github.com/advisories/GHSA-769v-p64c-89pr) · [Sonatype](https://sites.google.com/sonatype.com/vulnerabilities/cve-2025-1889)

### IOCs (ThreatFox 8 + URLhaus 6, newest — linked)
- **Lumma Stealer URLs:** `idealvgtrens.com/cloud/x/6157/` and `.../server.php` — [Malpedia: Lumma](https://malpedia.caad.fkie.fraunhofer.de/details/win.lumma)
- **Unknown RAT URLs:** `ivahook.online/api/clients/ping`, `ivahook.online/api/clients/exfiltrate` — [ANY.RUN task](https://app.any.run/tasks/2b95e84b-5f3a-453f-b846-a32959d3845b)
- **XMRIG:** domain `cyberknull.com`; `47.238.196.189:33333`; `103.30.194.78:80`; URL `cta.edu.pe/wp-content/plugins/linux.bin` — [Malpedia: XMRIG](https://malpedia.caad.fkie.fraunhofer.de/details/elf.xmrig)
- **URLhaus droppers (all online):** [124.94.144.192:55986/bin.sh](https://urlhaus.abuse.ch/url/3908500/) · [115.48.26.110:42240/bin.sh](https://urlhaus.abuse.ch/url/3908499/) · [asdsocial.pt/WINWORD.zip](https://urlhaus.abuse.ch/url/3908498/) · [103.249.199.5:39552/bin.sh](https://urlhaus.abuse.ch/url/3908497/) · [cta.edu.pe http linux.bin](https://urlhaus.abuse.ch/url/3908495/) · [cta.edu.pe https linux.bin](https://urlhaus.abuse.ch/url/3908496/)

---

*Compiled from public sources · 08-26-2026 · Sources: CISA KEV, CISA Advisories, Ransomware.live, CIRCL, FIRST EPSS, ThreatFox, URLhaus*
