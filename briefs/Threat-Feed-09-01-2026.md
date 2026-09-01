---
type: threat-feed-note
title: "Threat Feed - 09-01-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-09-01
source: "cisa-kev, cisa-advisories, ransomware.live, circl, epss, threatfox, urlhaus"
related: "https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md"
---

# Threat Feed — 09-01-2026

> **Reader promise:** 3-minute read. Headlines alone tell you what to do. New term? Check the [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).
> **Lens:** threats that hit AI tools, automations, and small-business money.
> **Sources:** every finding links to its primary source. If you want to verify, click.

## How to read the scores (30 seconds)
- **EPSS (0–1):** a score estimating how likely this flaw is to be exploited in the next 30 days; higher = patch first. 0.78 ≈ 78% — patch first. 0.01 ≈ 1% — lower urgency. Percentile ranks it against every known flaw: 99.5th = more likely to be exploited than 99.5% of all known vulnerabilities.
- **CISA KEV:** CISA only adds a flaw after confirming it's being **actively exploited right now** — not theoretical. The date shown is when CISA confirmed it. The federal deadline is their urgency rating in date form.
- **Today's window:** CISA added **two** actively exploited PaperCut NG/MF flaws on **08-31-2026** ([alert](https://www.cisa.gov/news-events/alerts/2026/08/31/cisa-adds-two-known-exploited-vulnerabilities-catalog)). Federal clock for both: **09-14-2026**. Overdue: SQL Server (**CVE-2019-1068**, EPSS **0.5284**) and Citrix NetScaler (**CVE-2026-8452**) **08-29-2026**; ownCloud (**CVE-2023-49105**, EPSS **0.4320**) and Linux IPv6 kernel (**CVE-2026-53362**) **08-30-2026**. Still open: Ajax.NET Professional (**CVE-2021-23758**, EPSS **0.8363**) **09-09-2026**; Linux kernel OOB write / libuser / ABRT **09-09-2026**; JFrog Artifactory (**CVE-2026-66384**) **09-10-2026**.

---

## 1. HIGH — Your chat-with-your-data tool can still be tricked into changing the database
**CVE-2024-8309** · CIRCL / GHSA (not on CISA KEV) · **EPSS 0.1374 (96.2nd percentile)** — above the 0.1 "patch first" flag; more likely to be exploited than 96.2% of known flaws · CIRCL lists CVSS 9.8/10 = critical if the chain is reachable — scored as exploitable remotely with no login
**Sources:** [GHSA-45pg-36p6-83v9](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [Fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) · [huntr](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2024-8309) · [CIRCL / PYSEC-2024-115](https://vulnerability.circl.lu/vuln/CVE-2024-8309)

**What broke:** LangChain's **GraphCypherQAChain (the piece that turns a chat question into a graph-database query)** in the 0.2.5-era packages can be steered by **prompt injection (hiding instructions inside the data the AI reads)** so the generated query becomes a database write, delete, or data grab. This is not a new CISA listing — scanners and CIRCL are still surfacing leftover 0.2.x installs. Patched: `langchain` **0.2.0**, `langchain-community` **0.2.19**. If you never used LangChain's graph-chat chain, you're done.

**Why it matters to an SMB running AI tools:** This is the on-lens item: the broken product is the "chat with your data" chain itself. A leftover GraphCypherQAChain next to customer records is not a code-review miss — the chat becomes a database write. CIRCL is still ranking this above the 0.1 EPSS flag, which is why it leads today even though the fix is from 2024.

**What you do Monday (15 minutes):**
1. Ask whoever built the chatbot: *"Do we use LangChain GraphCypherQAChain? What version is `langchain` / `langchain-community`?"* On the app host: `pip show langchain langchain-community`.
2. If `langchain` is below **0.2.0**, or `langchain-community` is **0.2.0 through 0.2.18**, upgrade (`pip install -U "langchain-community>=0.2.19"`). If the package is absent, you're outside this listing.
3. Until that's done: do not point that chain at a production graph database. Tell IT: *"CVE-2024-8309 — leftover LangChain GraphCypherQAChain can turn a chat question into a database write. EPSS 0.1374. Confirm langchain-community 0.2.19 or later."*

**Attacker view (conceptual):** Plant write/delete instructions in a document the assistant will retrieve → the chain turns that into a graph query → data changes without a login to the database. Defender rule of thumb: `GraphCypherQAChain` in the project; `langchain-community` below 0.2.19; unexpected CREATE/DELETE/DROP in the graph-database log.

---

## 2. CRITICAL — Your print server can be taken over without a login if the admin page is on the internet — patch today
**CVE-2026-81578** + **CVE-2026-82078** (chained) · CISA confirmed active exploitation **08-31-2026** · federal patch deadline **09-14-2026** · EPSS 0.0039 / 0.0046 (32nd–38th percentile) — **KEV is the signal, not EPSS**; these IDs are new · vendor CVSS 8.8 (auth bypass) and 9.4 (code execution)
**Sources:** [PaperCut urgent advisory (27 Aug 2026; Release 3 on 09-01-2026)](https://www.papercut.com/kb/Main/security-bulletin-27-aug-2026-urgent-security-advisory/) · [NVD CVE-2026-81578](https://nvd.nist.gov/vuln/detail/CVE-2026-81578) · [NVD CVE-2026-82078](https://nvd.nist.gov/vuln/detail/CVE-2026-82078) · [CISA alert 08-31-2026](https://www.cisa.gov/news-events/alerts/2026/08/31/cisa-adds-two-known-exploited-vulnerabilities-catalog) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** Self-hosted **PaperCut NG/MF (the print-management server many offices put in front of printers)** has two holes that chain. First, **missing authentication (the admin site ran a change before it finished checking who you are)** so a stranger can alter certain settings with no login (**CVE-2026-81578**). Second, **unsafe reflection (the server loads a Java class the attacker named)** in the database connector, which can run code as the PaperCut process (**CVE-2026-82078**). PaperCut confirmed customer incidents. All NG/MF versions are in scope. **Hive and Pocket are not.** You don't need the Java-class detail — CISA listed both because they are being used.

**Why it matters to an SMB running AI tools:** This is not a bug in the chatbot. It is the print server that often sits on the same network as file shares, scan-to-folder jobs, and the documents those AI tools summarize. A taken-over print server is a foothold next to that library. PaperCut published Emergency Patch **Release 3** today (09-01-2026); earlier emergency builds are not enough.

**What you do Monday (20 minutes — do the first step now if the admin page is internet-facing):**
1. If the PaperCut admin web UI is reachable from the public internet: firewall / network ACL it to office or VPN IPs only. PaperCut says do this even if you have seen nothing suspicious. Hive/Pocket customers can stop here.
2. PaperCut admin → version in the footer / About. You need Emergency Patch Release 3: **MF 26.0.4 / 25.0.12 / 24.1.9** or **NG 26.0.4 / 25.0.12 / 24.1.9**. Pre-v24: upgrade to current. Also patch Site Servers and secondary print servers (not Mobility Print / Print Deploy / the user client). Follow PaperCut's [upgrade steps](https://www.papercut.com/help/manuals/ng-mf/common/upgrade/).
3. Tell IT: *"CVE-2026-81578 and CVE-2026-82078 are on CISA's actively-exploited list as of 08-31-2026. Federal deadline 09-14-2026. Take the admin UI off the internet, install Release 3, and check server.log plus pc-app.exe child processes for compromise — not patch-and-forget if it was public."*

**CISA metrics:** CISA confirmed these are being actively exploited as of 08-31-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch by 09-14-2026. Required action: restrict the admin UI to trusted IPs and install PaperCut Emergency Patch Release 3 (or current NG/MF if you are pre-v24).

**Attacker view (conceptual):** Find an internet-facing PaperCut admin page → change config with no login → chain into code running as the PaperCut service. Defender rule of thumb: `pc-app.exe` launching `cmd.exe`; missing or truncated `server.log`; unexpected `.class` files under `server\lib`; new remote-support software on that host. Absence of those signs is not a clean bill of health.

---

## 3. CRITICAL — An old leftover .NET library is being used to run attacker code — federal deadline 09-09-2026
**CVE-2021-23758** · CISA confirmed active exploitation **08-26-2026** · federal patch deadline **09-09-2026** · **EPSS 0.8363 (99.7th percentile)** — more likely to be exploited than 99.7% of known flaws
**Sources:** [NVD](https://nvd.nist.gov/vuln/detail/CVE-2021-23758) · [Fix commit](https://github.com/michaelschwarz/Ajax.NET-Professional/commit/b0e63be5f0bb20dfce507cb8a1a9568f6e73de57) · [Official NuGet: AjaxNetProfessional](https://www.nuget.org/packages/AjaxNetProfessional/) · [CISA alert 08-26-2026](https://www.cisa.gov/news-events/alerts/2026/08/26/cisa-adds-six-known-exploited-vulnerabilities-catalog) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** **Ajax.NET Professional / AjaxPro (an old library that lets a browser call server code without a full page reload)** will take attacker-controlled data and turn it into live .NET objects — **deserialization (turning a data blob back into a running program object)**. That can become remote code execution. The official **AjaxNetProfessional** package is patched at **21.11.29.1**. The **AjaxPro.2** NuGet line has no patch; CISA says the product may be end-of-life and to **stop using it**. If you have no old ASP.NET apps, you're done.

**Why it matters to an SMB running AI tools:** This is not a bug in the assistant. It is the forgotten internal website those tools often read (intranet, quoting, inventory). Highest EPSS in today's KEV window, and the federal clock is **09-09-2026**. Whatever that intranet holds is what the chatbot will summarize next.

**What you do Monday (20 minutes):**
1. On app servers, search for `AjaxPro.dll`, NuGet `AjaxPro.2`, `AjaxNetProfessional`, or `Joint.AjaxPro`. If none, you're done.
2. If you found **AjaxNetProfessional**: upgrade to **21.11.29.1 or later** from [nuget.org/packages/AjaxNetProfessional](https://www.nuget.org/packages/AjaxNetProfessional/). If you found **AjaxPro.2** or a fork CISA treats as end-of-life: remove it or replace that AJAX layer — there is no safe leftover version.
3. Tell IT: *"CVE-2021-23758 is on CISA's actively-exploited list as of 08-26-2026. EPSS 0.8363. Federal deadline 09-09-2026. Find AjaxPro.dll, upgrade AjaxNetProfessional to 21.11.29.1 or remove AjaxPro.2, and look for unexpected IIS app-pool processes."*

**CISA metrics:** CISA confirmed this is being actively exploited as of 08-26-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch by 09-09-2026. Required action: upgrade AjaxNetProfessional to 21.11.29.1 or discontinue AjaxPro.2 / end-of-life builds.

---

## 4. CRITICAL — Old SQL Server 2014/2016/2017 can still be taken over — federal deadline already passed
**CVE-2019-1068** · CISA confirmed active exploitation **08-26-2026** · federal patch deadline **08-29-2026 (passed)** · **EPSS 0.5284 (98.9th percentile)** — more likely to be exploited than 98.9% of known flaws
**Sources:** [Microsoft advisory CVE-2019-1068](https://portal.msrc.microsoft.com/en-US/security-guidance/advisory/CVE-2019-1068) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2019-1068) · [CISA alert 08-26-2026](https://www.cisa.gov/news-events/alerts/2026/08/26/cisa-adds-six-known-exploited-vulnerabilities-catalog) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** **Microsoft SQL Server 2014, 2016, and 2017** mishandle some internal functions so a connected database user can run code as the SQL Server engine account. You don't need the function-name detail — CISA says this 2019 bug is being used now, and the federal clock passed **08-29-2026**. SQL Server 2019 and later are not on CISA's affected-product list. If you don't run 2014/2016/2017, you're done.

**Why it matters to an SMB running AI tools:** SQL Server is still the warehouse behind a lot of "chat with your data" tools, Power BI, and Copilot connectors. If the engine account is owned, the attacker is inside the same tables those assistants read — invoices, HR exports, customer lists. Second-highest EPSS in today's KEV window.

**What you do Monday (20 minutes — do it today if you still run 2014/2016/2017 unpatched):**
1. In SQL Server Management Studio run `SELECT @@VERSION;`. If it says 2014, 2016, or 2017, continue. If 2019 or newer, you're outside this listing.
2. Install Microsoft's **July 9, 2019** SQL Server security update (GDR or the CU that includes CVE-2019-1068) from Windows Update or the Microsoft Update Catalog — or upgrade that instance to a currently supported SQL Server.
3. Tell IT: *"CVE-2019-1068 is on CISA's actively-exploited list as of 08-26-2026. EPSS 0.5284. Federal deadline was 08-29-2026. Patch SQL 2014/2016/2017 today and confirm the instance is not on the public internet."*

**CISA metrics:** CISA confirmed this is being actively exploited as of 08-26-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch by 08-29-2026. Required action: apply the July 2019 SQL Server security updates (or upgrade off 2014/2016/2017).

---

## Jargon buster (terms used today)
- **CVE:** a unique ID for a security flaw, so everyone tracks the same bug (like a license plate).
- **EPSS:** 0–1 score of how likely a flaw is to be exploited in the next 30 days. Higher = patch first.
- **Percentile:** where a score ranks — 99.7th = more likely to be exploited than 99.7% of known flaws.
- **KEV (Known Exploited Vulnerabilities):** CISA's list of flaws being actively exploited right now.
- **CVSS:** a 0–10 severity score. 9.8/10 = critical — typically exploitable remotely with no login.
- **LangChain / GraphCypherQAChain:** a popular AI application framework and its graph-database query helper. Leftover 0.2.x installs are why this still leads.
- **Prompt injection:** hiding instructions inside the data an AI reads so it follows the attacker instead of you.
- **PaperCut NG/MF:** self-hosted print-management server. Hive/Pocket are not in this bulletin.
- **Missing authentication:** the product ran a sensitive action before checking that the caller was logged in.
- **Unsafe reflection:** tricking a Java app into loading a class the attacker named.
- **Ajax.NET Professional / AjaxPro:** an older .NET web library; federal deadline 09-09-2026, EPSS 0.8363.
- **Deserialization:** turning a saved data blob back into a live program object. If the blob is attacker-controlled, that restore can run their code.
- **SQL Server:** Microsoft's database engine. Versions 2014, 2016, and 2017 are the ones in the CVE-2019-1068 listing.
- **ownCloud:** self-hosted file-sync; federal deadline passed 08-30-2026.
- **JFrog Artifactory:** a repository manager for packages and Docker images used in AI pipelines; federal deadline 09-10-2026.
- **NetScaler ADC / NetScaler Gateway:** Citrix's appliance that is often the VPN and website front door.
- **Linux Kernel:** the core operating system software running Linux servers, containers, and VMs.
- **picklescan / pickle:** a scanner and a Python file format for AI models; outdated scanners can miss malicious model payloads.
- **print command (Samba):** a Samba setting that runs a program when someone prints. If it includes unescaped job text, a print job can become a command.
- **Ransomware:** malware that locks your files and demands payment — the top threat to small businesses.
- **ClearFake:** malware that pretends to be a browser or software update so a visitor infects themselves.
- **Shin webshell / php.shin_webshell:** a PHP webshell family. A domain listed with this name is already hosting attacker-controlled code — block and hunt, don't visit.
- **Loki Password Stealer (LokiPWS):** malware that steals saved passwords from browsers and apps.
- **IOC (Indicator of Compromise):** a trace of an attack (malicious IP/domain/file) to hunt for in network logs.

Full plain-language library: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).

---

## Appendix — raw signals (for the technical reader)

### CISA KEV (last 7 days, ranked by EPSS — links to vendor advisories)
| CVE | Product | EPSS | CISA confirmed | Federal deadline | Ransomware use | Source |
|---|---|---|---|---|---|---|
| CVE-2021-23758 | Ajax.NET Professional (deserialization / RCE) | **0.8363** | 08-26-2026 | 09-09-2026 | Unknown | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2021-23758) · [Fix commit](https://github.com/michaelschwarz/Ajax.NET-Professional/commit/b0e63be5f0bb20dfce507cb8a1a9568f6e73de57) |
| CVE-2019-1068 | Microsoft SQL Server 2014/2016/2017 (RCE) | **0.5284** | 08-26-2026 | 08-29-2026 | Unknown | [MSRC](https://portal.msrc.microsoft.com/en-US/security-guidance/advisory/CVE-2019-1068) |
| CVE-2023-49105 | ownCloud 10.6.0–10.13.0 (WebDAV auth bypass) | **0.4320** | 08-27-2026 | 08-30-2026 | Unknown | [ownCloud advisory](https://owncloud.com/security-advisories/webdav-api-authentication-bypass-using-pre-signed-urls/) |
| CVE-2022-0995 | Linux Kernel (local out-of-bounds write) | 0.0952 | 08-26-2026 | 09-09-2026 | Unknown | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2022-0995) |
| CVE-2015-3246 | Red Hat libuser (local race / passwd corruption) | 0.0880 | 08-26-2026 | 09-09-2026 | Unknown | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2015-3246) |
| CVE-2015-5287 | Red Hat ABRT (local privilege escalation; EoL) | 0.0496 | 08-26-2026 | 09-09-2026 | Unknown | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2015-5287) |
| CVE-2026-8452 | Citrix NetScaler ADC / Gateway (memory buffer / DoS) | 0.0161 | 08-26-2026 | 08-29-2026 | Unknown | [CTX696604](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX696604) |
| CVE-2026-66384 | JFrog Artifactory (Docker cache path traversal) | 0.0058 | 08-27-2026 | 09-10-2026 | Unknown | [JFrog advisories](https://docs.jfrog.com/releases/docs/jfrog-security-advisories) |
| CVE-2026-53362 | Linux Kernel IPv6 (local privilege escalation) | 0.0051 | 08-27-2026 | 08-30-2026 | Unknown | [Kernel commit](https://git.kernel.org/stable/c/14200d435af9a9eeb444f529fc2f689a236b7962) |
| CVE-2026-82078 | PaperCut NG/MF (unsafe reflection / code execution) | 0.0046 | 08-31-2026 | 09-14-2026 | Unknown | [PaperCut advisory](https://www.papercut.com/kb/Main/security-bulletin-27-aug-2026-urgent-security-advisory/) |
| CVE-2026-81578 | PaperCut NG/MF (missing authentication) | 0.0039 | 08-31-2026 | 09-14-2026 | Unknown | [PaperCut advisory](https://www.papercut.com/kb/Main/security-bulletin-27-aug-2026-urgent-security-advisory/) |

Two new KEV additions on 08-31-2026: [CISA alert](https://www.cisa.gov/news-events/alerts/2026/08/31/cisa-adds-two-known-exploited-vulnerabilities-catalog). Three added 08-27-2026: [CISA alert](https://www.cisa.gov/news-events/alerts/2026/08/27/cisa-adds-three-known-exploited-vulnerabilities-catalog). Six added 08-26-2026: [CISA alert](https://www.cisa.gov/news-events/alerts/2026/08/26/cisa-adds-six-known-exploited-vulnerabilities-catalog).

### Ransomware.live — recent victims
| Group | Sector | Country | Discovered | Source |
|---|---|---|---|---|
| — | — | — | — | [Ransomware.live](https://www.ransomware.live) (query failed today; 0 victims in packet) |

No leak-site or .onion links. Named pulse: unavailable — the ransomware.live API returned no rows on 09-01-2026. Do not treat the empty table as "ransomware stopped."

### CIRCL — highest-signal new items (30 pulled)
- **CVE-2026-4480 (EPSS 0.1393, 96.3rd pct)** — Samba `print command` with `%J` passes a client-controlled job description into a shell without escaping; only in play if you set a custom print command — [CIRCL](https://vulnerability.circl.lu/advisories/cve-2026-4480)
- **CVE-2024-8309 (EPSS 0.1374, 96.2nd pct, CVSS 9.8)** — LangChain GraphCypherQAChain SQL/Cypher injection via prompt injection; `langchain` patched at **0.2.0**, `langchain-community` at **0.2.19** — [GHSA](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [Fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) · [huntr](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5)
- **CVE-2026-4408 (EPSS 0.0250, 83.6th pct)** — Samba `check password script` with `%u` on file servers / classic DCs — [CIRCL](https://vulnerability.circl.lu/advisories/cve-2026-4408)
- **CVE-2025-1889 (EPSS 0.0038, 31.1st pct)** — picklescan missed non-standard pickle extensions in ML model files; upgrade picklescan to **0.0.22 or later** — [GHSA](https://github.com/advisories/GHSA-769v-p64c-89pr) · [Sonatype](https://sites.google.com/sonatype.com/vulnerabilities/cve-2025-1889)
- **CVE-2025-49796 (EPSS 0.0148, 72.1st pct)** — libxml2 memory corruption on crafted XML — [CIRCL](https://vulnerability.circl.lu/advisories/cve-2025-49796)
- **CVE-2026-10579 (EPSS 0.0030)** — PicketLink Federation SAML accepted forged assertions with no verification — [CIRCL](https://vulnerability.circl.lu/advisories/cve-2026-10579)

### IOCs (ThreatFox 8, URLhaus 6 — linked)
- **Shin webshell domains (confidence 50):** `lewisixo.workers.dev`, `hahynoci.workers.dev`, `wazaso.workers.dev`, `cyfidixa.workers.dev` — [Malpedia: php.shin_webshell](https://malpedia.caad.fkie.fraunhofer.de/details/php.shin_webshell)
- **ClearFake domains (confidence 90–100):** `exmyza.com`, `payload.moodec.ch`, `fuptae0y.shop-bellyflush.com` — [Malpedia: ClearFake](https://malpedia.caad.fkie.fraunhofer.de/details/js.clearfake)
- **Loki Password Stealer URL (confidence 100):** `http://worldatdoor.in/wapl/Panel/five/fre.php` — [Malpedia: LokiPWS](https://malpedia.caad.fkie.fraunhofer.de/details/win.lokipws)
- **URLhaus malware distribution URLs:** `http://125.45.25.114:44399/i` — [URLhaus 3910845](https://urlhaus.abuse.ch/url/3910845/) · `http://115.56.163.153:51027/i` — [URLhaus 3910844](https://urlhaus.abuse.ch/url/3910844/) · `http://60.19.217.253:46181/i` — [URLhaus 3910843](https://urlhaus.abuse.ch/url/3910843/) · `http://125.45.25.114:44399/bin.sh` — [URLhaus 3910842](https://urlhaus.abuse.ch/url/3910842/) · `http://115.56.163.153:51027/bin.sh` — [URLhaus 3910841](https://urlhaus.abuse.ch/url/3910841/) · `https://www.movy.bz/scripts/xyz.js` (offline) — [URLhaus 3910840](https://urlhaus.abuse.ch/url/3910840/)

### CISA advisories
Newest item in the CISA RSS is [CISA Adds Two Known Exploited Vulnerabilities to Catalog](https://www.cisa.gov/news-events/alerts/2026/08/31/cisa-adds-two-known-exploited-vulnerabilities-catalog) (pubDate 08-31-2026) — PaperCut NG/MF, folded into item 2. Next ICS item (ASE2000 test set, ICSA-26-239-04) is OT lab gear, not folded into today's top items.

---

*Compiled from public sources · 09-01-2026 · Sources: CISA KEV, CISA Advisories, Ransomware.live, CIRCL, FIRST EPSS, ThreatFox, URLhaus*
