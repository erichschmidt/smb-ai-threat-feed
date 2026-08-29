---
type: threat-feed-note
title: "Threat Feed - 08-29-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-08-29
source: "cisa-kev, cisa-advisories, ransomware.live, circl, epss, threatfox, urlhaus"
related: "https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md"
---

# Threat Feed — 08-29-2026

> **Reader promise:** 3-minute read. Headlines alone tell you what to do. New term? Check the [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).
> **Lens:** threats that hit AI tools, automations, and small-business money.
> **Sources:** every finding links to its primary source. If you want to verify, click.

## How to read the scores (30 seconds)
- **EPSS (0–1):** a score estimating how likely this flaw is to be exploited in the next 30 days; higher = patch first. 0.78 ≈ 78% — patch first. 0.01 ≈ 1% — lower urgency. Percentile ranks it against every known flaw: 99.5th = more likely to be exploited than 99.5% of all known vulnerabilities.
- **CISA KEV:** CISA only adds a flaw after confirming it's being **actively exploited right now** — not theoretical. The date shown is when CISA confirmed it. The federal deadline is their urgency rating in date form.
- **Today's window:** No new actively exploited vulnerabilities were added to CISA KEV on **08-29-2026**. SQL Server (**CVE-2019-1068**) and Citrix NetScaler (**CVE-2026-8452**) federal clocks are **today (08-29-2026)**. ownCloud and the Linux IPv6 kernel bug are **08-30-2026**. Gitea's **08-28-2026** deadline has already passed (still the highest-EPSS item in this window). Ajax.NET Professional is **09-09-2026**. JFrog Artifactory is **09-10-2026**. Oracle's **08-27-2026** deadline has already passed.

---

## 1. HIGH — Your AI browser agent can run attacker code from a poisoned workflow prompt
**CVE-2026-82447** · published **08-29-2026** · not on CISA KEV · EPSS not yet scored · CVSS 8.8/10 = high — network-reachable; a logged-in user is enough
**Sources:** [CIRCL / CVE-2026-82447](https://vulnerability.circl.lu/vuln/CVE-2026-82447) · [VulnCheck advisory](https://www.vulncheck.com/advisories/skyvern-before-1.0.45-sandbox-escape-via-textpromptblock) · [Fix commit](https://github.com/Skyvern-AI/skyvern/commit/d723de621d5b3a340f3cc4d5b46bfe40a9a3124e) · [Skyvern repo](https://github.com/Skyvern-AI/skyvern) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-82447)

**What broke:** **Skyvern (an AI agent that fills forms and clicks through websites for you)** will template a TextPromptBlock twice — first inside a **sandbox (a cage meant to stop templates from running real code)**, then again without the cage. If an attacker can set a workflow parameter or feed output from a previous step, leftover template tags run as the Skyvern server itself. Affected: **0.2.1 through 1.0.44**. Fixed: **1.0.45** (GitHub is already at **v1.0.51**). You don't need the double-render detail — just know anything below 1.0.45 is in scope. If you don't run Skyvern, you're done.

**Why it matters to an SMB running AI tools:** This is the on-lens item: the broken product *is* the AI automation. Skyvern often has live browser sessions into CRMs, billing portals, and vendor sites — plus API keys in the same process. A poisoned workflow parameter is a poisoned agent. This is not on CISA's actively-exploited list yet; treat it as "patch the AI box you actually run," not a generic Windows footnote.

**What you do Monday (15 minutes):**
1. Ask whoever runs automations: *"Do we self-host Skyvern? What version?"* On the host: `pip show skyvern` (or check the Docker image tag). If no Skyvern, you're done. If you only use Skyvern cloud, ask the vendor whether **1.0.45 or later** is deployed.
2. Self-hosted below 1.0.45: upgrade to **1.0.45 or later** (`pip install -U "skyvern>=1.0.45"` or pull the current image).
3. Tell IT: *"CVE-2026-82447 is a high-severity sandbox escape in Skyvern before 1.0.45. Upgrade today. Don't let untrusted web content become workflow input, and look for unexpected processes as the Skyvern user."*

**Attacker view (conceptual):** Get a Skyvern login (or a workflow that accepts untrusted parameters) → plant template tags in a parameter or upstream block output → the second render runs outside the cage → code runs as the Skyvern process. Defender rule of thumb: Skyvern below 1.0.45; unexpected processes as that service account; untrusted page content should never be trusted workflow input.

---

## 2. CRITICAL — Old SQL Server 2014/2016/2017 can still be taken over — patch deadline is today
**CVE-2019-1068** · CISA confirmed active exploitation **08-26-2026** · federal patch deadline **08-29-2026 (today)** · **EPSS 0.5284 (98.9th percentile)** · CVSS 8.8/10 = high — network-reachable; a logged-in database user is enough
**Sources:** [Microsoft advisory CVE-2019-1068](https://portal.msrc.microsoft.com/en-US/security-guidance/advisory/CVE-2019-1068) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2019-1068) · [CISA alert 08-26-2026](https://www.cisa.gov/news-events/alerts/2026/08/26/cisa-adds-six-known-exploited-vulnerabilities-catalog) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** **Microsoft SQL Server 2014, 2016, and 2017** mishandle some internal functions so a connected database user can run code as the SQL Server engine account. You don't need the function-name detail — CISA says this 2019 bug is being used now. SQL Server 2019 and later are not on CISA's affected-product list. If you don't run 2014/2016/2017, you're done.

**Why it matters to an SMB running AI tools:** SQL Server is still the warehouse behind a lot of "chat with our data" tools, Power BI, and Copilot connectors. If the engine account is owned, the attacker is inside the same tables those assistants read — invoices, HR exports, customer lists.

**What you do Monday (20 minutes — do it today if you still run 2014/2016/2017):**
1. In SQL Server Management Studio run `SELECT @@VERSION;`. If it says 2014, 2016, or 2017, continue. If 2019 or newer, you're outside this listing.
2. Install Microsoft's **July 9, 2019** SQL Server security update (GDR or the CU that includes CVE-2019-1068) from Windows Update or the Microsoft Update Catalog — or upgrade that instance to a currently supported SQL Server.
3. Tell IT: *"CVE-2019-1068 is on CISA's actively-exploited list as of 08-26-2026. Federal deadline is today, 08-29-2026. Patch SQL 2014/2016/2017 today and confirm the instance is not on the public internet."*

**CISA metrics:** CISA confirmed this is being actively exploited as of 08-26-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch by 08-29-2026. Required action: apply the July 2019 SQL Server security updates (or upgrade off 2014/2016/2017).

---

## 3. HIGH — Your Citrix VPN/front door can be knocked offline — patch deadline is today
**CVE-2026-8452** · CISA confirmed active exploitation **08-26-2026** · federal patch deadline **08-29-2026 (today)** · EPSS 0.0161 (73.7th percentile) — **KEV is the signal, not EPSS**
**Sources:** [Citrix CTX696604](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX696604) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-8452) · [CISA alert 08-26-2026](https://www.cisa.gov/news-events/alerts/2026/08/26/cisa-adds-six-known-exploited-vulnerabilities-catalog) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** **Citrix NetScaler ADC / NetScaler Gateway (the appliance that is often the VPN and website front door)** has a memory-buffer bug that can take the box down — **denial of service (the service stops answering, so nobody gets in)**. You don't need the buffer detail — CISA says this is being used now. If you don't run NetScaler, you're done.

**Why it matters to an SMB running AI tools:** The VPN is the front door for remote staff, backup agents, and the automations that feed Copilot / "chat with your files" tools. If the tunnel appliance is down or owned, everything behind it is in play — including the document stores those tools read. Low EPSS does not cancel a KEV listing with a deadline of today.

**What you do Monday (20 minutes — do it today if you run NetScaler):**
1. On the NetScaler: System → Settings → or the version string on the login page. Confirm whether you are on a build **at or above** the fixed firmware in [CTX696604](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX696604) (**14.1-72.61** or **13.1-63.18** on the branches Citrix listed). If no NetScaler, you're done.
2. Upgrade firmware to the fixed build for your branch. Don't leave an internet-facing NetScaler on a pre-fix build over the weekend.
3. Tell IT: *"CVE-2026-8452 is on CISA's actively-exploited list as of 08-26-2026. Federal deadline is today, 08-29-2026. Upgrade NetScaler to 14.1-72.61 or 13.1-63.18 (match the branch) and confirm the management interface is not on the public internet."*

**CISA metrics:** CISA confirmed this is being actively exploited as of 08-26-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch by 08-29-2026. Required action: apply the Citrix firmware in CTX696604.

---

## 4. CRITICAL — Anyone who knows a username can read, change, or delete files on your private file server
**CVE-2023-49105** · CISA confirmed active exploitation **08-27-2026** · federal patch deadline **08-30-2026** · **EPSS 0.4119 (98.6th percentile)** — jumped from 0.11 yesterday; above the 0.1 "patch first" flag · CVSS 9.8/10 = critical — exploitable remotely with no authentication
**Sources:** [ownCloud advisory](https://owncloud.com/security-advisories/webdav-api-authentication-bypass-using-pre-signed-urls/) · [ownCloud security](https://owncloud.org/security) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2023-49105) · [CISA alert 08-27-2026](https://www.cisa.gov/news-events/alerts/2026/08/27/cisa-adds-three-known-exploited-vulnerabilities-catalog) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** **ownCloud 10.6.0 through 10.13.0** will accept a **pre-signed URL (a file link that's supposed to prove you were allowed in)** even when the owner never set a signing key — which is the default. If the attacker knows the username, they can read, change, or delete that person's files with **no login**. Fixed in **10.13.1**. If you don't run ownCloud 10.x, you're done.

**Why it matters to an SMB running AI tools:** ownCloud is often the private Dropbox Copilot, RAG loaders, and "chat with our files" tools read. Unauthenticated file access is not just a leak — it's a poison-the-library problem. Whatever the assistant summarizes next may be attacker-written. The overnight EPSS jump is the "this is getting more likely" signal; the federal clock is tomorrow.

**What you do Monday (20 minutes — do it before 08-30 if you run ownCloud 10.x):**
1. In ownCloud: Settings → Admin (or the version string on the login page). If it's **10.13.1 or later**, you're outside this listing. If you run Infinite Scale / ownCloud Online instead of 10.x, this listing does not apply.
2. Upgrade **ownCloud 10** to **10.13.1 or later**. Do not leave 10.6.0–10.13.0 on the internet.
3. Tell IT: *"CVE-2023-49105 is on CISA's actively-exploited list as of 08-27-2026. Federal deadline 08-30-2026. Upgrade ownCloud 10 to 10.13.1. If this server was internet-facing and unpatched, treat it as check-the-files, not patch-and-forget."*

**CISA metrics:** CISA confirmed this is being actively exploited as of 08-27-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch by 08-30-2026. Required action: upgrade ownCloud 10 to 10.13.1 or later.

---

## Jargon buster (terms used today)
- **CVE:** a unique ID for a security flaw, so everyone tracks the same bug (like a license plate).
- **RCE (Remote Code Execution):** attacker can run their own code on your machine — full control.
- **EPSS:** 0–1 score of how likely a flaw is to be exploited in the next 30 days. Higher = patch first.
- **Percentile:** where a score ranks — 98.9th = more likely to be exploited than 98.9% of known flaws.
- **KEV (Known Exploited Vulnerabilities):** CISA's list of flaws being actively exploited right now.
- **CVSS:** a 0–10 severity score. 9.8/10 = critical — typically exploitable remotely with no login. 8.8/10 = high — usually needs a login, still game-over if it works.
- **Skyvern:** an AI agent that fills forms and clicks through websites for you. A hole here is a hole in those browser sessions and the keys on that box.
- **Sandbox / sandbox escape:** a cage meant to stop templates from running real code. Escape means the cage failed and code ran on the real machine.
- **Jinja:** a template language used to fill in variables in text. Leftover template tags can become code if they are rendered unsandboxed.
- **SQL Server:** Microsoft's database engine. 2014/2016/2017 are the versions in today's listing.
- **NetScaler ADC / NetScaler Gateway:** Citrix's appliance that is often the VPN and website front door.
- **Denial of service:** the service stops answering, so nobody gets in — including you.
- **ownCloud:** self-hosted file-sync (like a private Dropbox). A hole here is a hole in the documents your AI tools summarize.
- **Pre-signed URL:** a file link that's supposed to prove you were allowed to access it. If the signing key was never set, the proof is fake.
- **WebDAV:** an old-but-common way programs read and write files over HTTP. ownCloud's file API uses it.
- **RAG / Copilot data source:** the files an AI is allowed to read. If those files (or the system that holds them) are owned, the AI is owned.
- **Gitea:** a self-hosted Git (source-code) server. Federal deadline was yesterday; still the highest-EPSS KEV in this window.
- **JFrog Artifactory:** a warehouse for software packages and Docker images — often the same place AI pipelines pull models and dependencies.
- **Ajax.NET Professional / AjaxPro:** an old .NET library that lets a web page call server code without a full reload. Leftover copies are the risk.
- **Ransomware:** malware that locks your files and demands payment — the top small-business threat.
- **ShadowByt3$ / incransom / shinyhunters / Doommageddon / lockbit5 / qilin / chaos:** ransomware groups in today's victim disclosures. Treat the name as a sector-targeting signal, not a reason to pay.
- **ClearFake:** malware that pretends to be a browser or software update so a visitor infects themselves.
- **Shin webshell / php.shin_webshell:** a PHP webshell family. A domain listed with this name is already hosting attacker-controlled code — block and hunt, don't visit.
- **IOC (Indicator of Compromise):** a trace of an attack (malicious IP/domain/file) to hunt for in logs.
- **LangChain / GraphCypherQAChain:** a popular AI-app framework and its graph-database helper. Old 0.2.x community packages still show up in scanners.
- **picklescan / pickle:** a scanner and a Python file format for AI models. An old scanner can miss a poisoned model file.

Full plain-language library: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).

---

## Appendix — raw signals (for the technical reader)

### CISA KEV (last 7 days, ranked by EPSS — links to vendor advisories)
| CVE | Product | EPSS | CISA confirmed | Federal deadline | Ransomware use | Source |
|---|---|---|---|---|---|---|
| CVE-2026-60004 | Gitea (code injection via patch API / Git hook) | **0.8455** | 08-25-2026 | 08-28-2026 | Unknown | [GHSA](https://github.com/go-gitea/gitea/security/advisories/GHSA-rcr6-4jqh-j84m) |
| CVE-2021-23758 | Ajax.NET Professional (deserialization / RCE) | **0.8363** | 08-26-2026 | 09-09-2026 | Unknown | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2021-23758) · [Fix commit](https://github.com/michaelschwarz/Ajax.NET-Professional/commit/b0e63be5f0bb20dfce507cb8a1a9568f6e73de57) |
| CVE-2019-1068 | Microsoft SQL Server 2014/2016/2017 (RCE) | **0.5284** | 08-26-2026 | 08-29-2026 | Unknown | [MSRC](https://portal.msrc.microsoft.com/en-US/security-guidance/advisory/CVE-2019-1068) |
| CVE-2026-21962 | Oracle HTTP Server / WebLogic Proxy Plug-in (access control) | **0.4202** | 08-24-2026 | 08-27-2026 | Unknown | [Oracle Jan 2026 CPU](https://www.oracle.com/security-alerts/cpujan2026.html) |
| CVE-2023-49105 | ownCloud 10.6.0–10.13.0 (WebDAV auth bypass) | **0.4119** | 08-27-2026 | 08-30-2026 | Unknown | [ownCloud advisory](https://owncloud.com/security-advisories/webdav-api-authentication-bypass-using-pre-signed-urls/) |
| CVE-2022-0995 | Linux Kernel (local out-of-bounds write) | 0.0952 | 08-26-2026 | 09-09-2026 | Unknown | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2022-0995) |
| CVE-2015-3246 | Red Hat libuser (local race / passwd corruption) | 0.088 | 08-26-2026 | 09-09-2026 | Unknown | [Red Hat](https://access.redhat.com/articles/1537873) |
| CVE-2015-5287 | Red Hat ABRT (local privilege escalation; likely EoL) | 0.0496 | 08-26-2026 | 09-09-2026 | Unknown | [Fix commit](https://github.com/abrt/abrt/commit/3c1b60cfa62d39e5fff5a53a5bc53dae189e740e) |
| CVE-2026-8452 | Citrix NetScaler ADC / Gateway (memory buffer / DoS) | 0.0161 | 08-26-2026 | 08-29-2026 | Unknown | [CTX696604](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX696604) |
| CVE-2026-66384 | JFrog Artifactory (Docker cache path traversal) | 0.0054 | 08-27-2026 | 09-10-2026 | Unknown | [JFrog advisories](https://docs.jfrog.com/releases/docs/jfrog-security-advisories) |
| CVE-2026-53362 | Linux Kernel IPv6 (local privilege escalation) | 0.0051 | 08-27-2026 | 08-30-2026 | Unknown | [Kernel commit](https://git.kernel.org/stable/c/14200d435af9a9eeb444f529fc2f689a236b7962) |

No new KEV additions on 08-29-2026. Three added 08-27-2026: [CISA alert](https://www.cisa.gov/news-events/alerts/2026/08/27/cisa-adds-three-known-exploited-vulnerabilities-catalog). Six added 08-26-2026: [CISA alert](https://www.cisa.gov/news-events/alerts/2026/08/26/cisa-adds-six-known-exploited-vulnerabilities-catalog).

### Ransomware.live — recent victims (10)
| Group | Sector | Country | Discovered | Source |
|---|---|---|---|---|
| ShadowByt3$ | Retail & E-Commerce | US | 08-29-2026 | [Ransomware.live](https://www.ransomware.live) |
| incransom | Energy & Utilities | US | 08-29-2026 | [Ransomware.live](https://www.ransomware.live) |
| lockbit5 | Not Found | MX | 08-29-2026 | [Ransomware.live](https://www.ransomware.live) |
| shinyhunters | Healthcare | US | 08-28-2026 | [Ransomware.live](https://www.ransomware.live) |
| Doommageddon | Transportation | TR | 08-28-2026 | [Ransomware.live](https://www.ransomware.live) |
| Doommageddon | Other | TR | 08-28-2026 | [Ransomware.live](https://www.ransomware.live) |
| shinyhunters | Healthcare | SE | 08-28-2026 | [Ransomware.live](https://www.ransomware.live) |
| shinyhunters | Financial Services | US | 08-28-2026 | [Ransomware.live](https://www.ransomware.live) |
| qilin | Professional Services | ES | 08-28-2026 | [Ransomware.live](https://www.ransomware.live) |
| chaos | Manufacturing | US | 08-28-2026 | [Ransomware.live](https://www.ransomware.live) |

No leak-site or .onion links. Named pulse: US retail, energy, healthcare, financial services, and manufacturing claims in the last 24 hours (ShadowByt3$, incransom, shinyhunters, chaos), plus a shinyhunters healthcare cluster (US + SE).

### CIRCL — highest-signal new items (30 pulled)
- **CVE-2026-82447 (EPSS n/a, published 08-29-2026, CVSS 8.8)** — Skyvern before **1.0.45**: TextPromptBlock sandbox escape via a second unsandboxed Jinja render; upgrade to **1.0.45 or later** — [CIRCL](https://vulnerability.circl.lu/vuln/CVE-2026-82447) · [VulnCheck](https://www.vulncheck.com/advisories/skyvern-before-1.0.45-sandbox-escape-via-textpromptblock) · [Fix commit](https://github.com/Skyvern-AI/skyvern/commit/d723de621d5b3a340f3cc4d5b46bfe40a9a3124e)
- **CVE-2024-8309 (EPSS 0.1374, 96.3rd pct)** — LangChain GraphCypherQAChain SQL injection via prompt injection; `langchain-community` patched past the 0.2.5-era chain — [GHSA](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [Fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) · [huntr](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5)
- **CVE-2025-1889 (EPSS 0.0038, 30.9th pct)** — picklescan missed non-standard pickle extensions in ML model files; upgrade picklescan to **0.0.22 or later** — [GHSA](https://github.com/advisories/GHSA-769v-p64c-89pr) · [Sonatype](https://sites.google.com/sonatype.com/vulnerabilities/cve-2025-1889)
- **CVE-2026-14494 (EPSS n/a, published 08-29-2026, CVSS 9.8)** — WordPress plugin Sigma Forms Pro through **1.4.5**: remote code execution via form submission (`unfiltered_upload` granted too broadly) — [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-14494) · [CIRCL](https://vulnerability.circl.lu/advisories/cve-2026-14494)
- **MAL-2026-15566 / MAL-2026-14587 (published 08-29 / 08-28)** — malicious PyPI packages: install-time theft of environment variables/files, and a `setup.py` that forks a daemon during `pip install` — [MAL-2026-15566](https://vulnerability.circl.lu/advisories/mal-2026-15566) · [MAL-2026-14587](https://vulnerability.circl.lu/advisories/mal-2026-14587)

### IOCs (ThreatFox 8, newest — linked)
- **ClearFake domains/URLs (confidence 90):** `luckywheels.world`, `fish-planet.online`, `https://fish-planet.online`, `https://online-park.online` — [Malpedia: ClearFake](https://malpedia.caad.fkie.fraunhofer.de/details/js.clearfake)
- **Shin webshell domains (confidence 50):** `linywahe.workers.dev`, `lulugyqi.workers.dev`, `bbxi4lykw4.workers.dev`, `c75aknnyxf.workers.dev` — [Malpedia: php.shin_webshell](https://malpedia.caad.fkie.fraunhofer.de/details/php.shin_webshell)

URLhaus collector failed this run (expired TLS certificate on `urlhaus-api.abuse.ch`) — 0 URLhaus rows.

### CISA advisories (newest in feed, 08-27-2026)
- [Rockwell Automation OTTO Fleet Manager (ICSA-26-239-03)](https://www.cisa.gov/news-events/ics-advisories/icsa-26-239-03) — ICS warehouse-robot manager, weak password hashing (CVE-2026-75112). Not an SMB AI-stack issue unless you run OTTO. Fixed in 2.36.3.

---

*Compiled from public sources · 08-29-2026 · Sources: CISA KEV, CISA Advisories, Ransomware.live, CIRCL, FIRST EPSS, ThreatFox, URLhaus*
