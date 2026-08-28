---
type: threat-feed-note
title: "Threat Feed - 08-28-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-08-28
source: "cisa-kev, cisa-advisories, ransomware.live, circl, epss, threatfox, urlhaus"
related: "https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md"
---

# Threat Feed — 08-28-2026

> **Reader promise:** 3-minute read. Headlines alone tell you what to do. New term? Check the [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).
> **Lens:** threats that hit AI tools, automations, and small-business money.
> **Sources:** every finding links to its primary source. If you want to verify, click.

## How to read the scores (30 seconds)
- **EPSS (0–1):** a score estimating how likely this flaw is to be exploited in the next 30 days; higher = patch first. 0.78 ≈ 78% — patch first. 0.01 ≈ 1% — lower urgency. Percentile ranks it against every known flaw: 99.5th = more likely to be exploited than 99.5% of all known vulnerabilities.
- **CISA KEV:** CISA only adds a flaw after confirming it's being **actively exploited right now** — not theoretical. The date shown is when CISA confirmed it. The federal deadline is their urgency rating in date form.
- **Today's window:** CISA added **three** actively exploited flaws on **08-27-2026** ([alert](https://www.cisa.gov/news-events/alerts/2026/08/27/cisa-adds-three-known-exploited-vulnerabilities-catalog)). Gitea's federal clock is **today (08-28-2026)**. SQL Server and Citrix NetScaler are **08-29-2026**. ownCloud and the new Linux IPv6 kernel bug are **08-30-2026**. JFrog Artifactory is **09-10-2026**. Oracle's **08-27-2026** deadline has already passed.

---

## 1. HIGH — The warehouse that stores your Docker images and AI packages has a hole that's being actively attacked
**CVE-2026-66384** · CISA confirmed active exploitation **08-27-2026** · federal patch deadline **09-10-2026** · EPSS 0.0026 (17.9th percentile) — **KEV is the signal, not EPSS** · CVSS 5.3/10 = medium — a logged-in user, under specific remote-repository conditions
**Sources:** [JFrog advisory CVE-2026-66384](https://docs.jfrog.com/releases/docs/jfrog-security-advisories#cve-2026-66384---authenticated-users-may-write-data-outside-the-intended-docker-cache-path) · [Artifactory self-managed releases](https://docs.jfrog.com/releases/docs/artifactory-self-managed-releases) · [CVE record](https://www.cve.org/CVERecord?id=CVE-2026-66384) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-66384) · [CISA alert 08-27-2026](https://www.cisa.gov/news-events/alerts/2026/08/27/cisa-adds-three-known-exploited-vulnerabilities-catalog) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** **JFrog Artifactory (the warehouse for software packages and Docker images)** will let a logged-in user write files **outside** the intended Docker cache folder when a remote repository is set up a certain way — **path traversal (using a crafted file path to land outside the allowed directory)**. You don't need the cache-path detail — CISA says this is being used now. JFrog cloud is already patched. If you don't run self-hosted Artifactory, you're done.

**Why it matters to an SMB running AI tools:** This is the on-lens item: the broken product *is* the package/model warehouse. Training jobs, n8n/LangChain workers, and "pull this image / this wheel" steps often trust whatever Artifactory serves. A write outside the Docker cache is a planted file in the next build. CISA's enrichment for this CVE points at OpenAI's public Hugging Face / Artifactory write-up (agents treating the warehouse as a side channel). You don't need that saga — if this box is in your AI pipeline, treat it as production.

**What you do Monday (15 minutes):**
1. Ask whoever runs builds/AI: *\"Do we self-host JFrog Artifactory? Which version?\"* If you only use JFrog cloud, JFrog says you're already patched. If no Artifactory, you're done.
2. Self-hosted: upgrade to **7.146.35** or **7.161.16** (match your release branch) from [Artifactory self-managed releases](https://docs.jfrog.com/releases/docs/artifactory-self-managed-releases).
3. Tell IT: *\"CVE-2026-66384 is on CISA's actively-exploited list as of 08-27-2026. Federal deadline 09-10-2026. Upgrade self-hosted Artifactory to 7.146.35 or 7.161.16, and look for unexpected files outside the Docker cache directory.\"*

**CISA metrics:** CISA confirmed this is being actively exploited as of 08-27-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch by 09-10-2026. Required action: upgrade self-hosted Artifactory to 7.146.35 or 7.161.16 (cloud already fortified).

**Attacker view (conceptual):** Get a normal Artifactory login (or a leaked token) → abuse a remote Docker repository so a write lands outside the cache folder → a later build trusts that file. Defender rule of thumb: self-hosted Artifactory below 7.146.35 / 7.161.16; unexpected files outside the Docker cache; this product should not be on the public internet.

---

## 2. CRITICAL — Your self-hosted code server can be taken over — federal deadline is today
**CVE-2026-60004** · CISA confirmed active exploitation **08-25-2026** · federal patch deadline **08-28-2026 (today)** · **EPSS 0.824 (99.6th percentile)** — more likely to be exploited than 99.6% of known flaws · CVSS 9.8/10 = critical — exploitable over the network
**Sources:** [GitHub advisory GHSA-rcr6-4jqh-j84m](https://github.com/go-gitea/gitea/security/advisories/GHSA-rcr6-4jqh-j84m) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-60004) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** **Gitea (a self-hosted Git / source-code server)** will take a crafted patch on the `diffpatch` API and plant a **Git hook (a script Git runs automatically on an event)**. That script runs as the Gitea service account — secrets, repos, and whatever that account can reach. Affected: **1.17 through 1.27.0**. Fixed: **1.27.1**. If open sign-up is on, a stranger can register, create a repo, and get the write access this needs. If you don't run Gitea, you're done.

**Why it matters to an SMB running AI tools:** This is not a bug in Copilot. It is the repo those automations clone — prompts, n8n workflows, RAG loaders, API keys in `.env` files someone committed. If Gitea is owned, the next pipeline run is the attacker's.

**What you do Monday (20 minutes — do it today if you run Gitea):**
1. On the Gitea host: `gitea --version` (or Site Administration → Configuration). If **1.27.1 or later**, you're outside this listing. If no Gitea, you're done.
2. Upgrade to **1.27.1 or later**. Until that's done, turn **off** open registration (Site Administration → Authentication / Register).
3. Tell IT: *\"CVE-2026-60004 is on CISA's actively-exploited list as of 08-25-2026. EPSS 0.824. Federal deadline is today, 08-28-2026. Upgrade Gitea to 1.27.1, disable open sign-up, and look for unexpected Git hooks and new processes as the Gitea user.\"*

**CISA metrics:** CISA confirmed this is being actively exploited as of 08-25-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch by 08-28-2026. Required action: upgrade Gitea to 1.27.1 or later.

---

## 3. CRITICAL — Anyone who knows a username can read, change, or delete files on your private file server
**CVE-2023-49105** · CISA confirmed active exploitation **08-27-2026** · federal patch deadline **08-30-2026** · **EPSS 0.1107 (95.6th percentile)** — above the 0.1 "patch first" flag · CVSS 9.8/10 = critical — exploitable remotely with no authentication
**Sources:** [ownCloud advisory](https://owncloud.com/security-advisories/webdav-api-authentication-bypass-using-pre-signed-urls/) · [ownCloud security](https://owncloud.org/security) · [CVE record](https://www.cve.org/CVERecord?id=CVE-2023-49105) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2023-49105) · [CISA alert 08-27-2026](https://www.cisa.gov/news-events/alerts/2026/08/27/cisa-adds-three-known-exploited-vulnerabilities-catalog) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** **ownCloud 10.6.0 through 10.13.0** will accept a **pre-signed URL (a file link that's supposed to prove you were allowed in)** even when the owner never set a signing key — which is the default. If the attacker knows the username, they can read, change, or delete that person's files with **no login**. Fixed in **10.13.1**. If you don't run ownCloud 10.x, you're done.

**Why it matters to an SMB running AI tools:** ownCloud is often the private Dropbox Copilot, RAG loaders, and "chat with our files" tools read. Unauthenticated file access is not just a leak — it's a poison-the-library problem. Whatever the assistant summarizes next may be attacker-written.

**What you do Monday (20 minutes — do it before 08-30 if you run ownCloud 10.x):**
1. In ownCloud: Settings → Admin (or the version string on the login page). If it's **10.13.1 or later**, you're outside this listing. If you run Infinite Scale / ownCloud Online instead of 10.x, this listing does not apply.
2. Upgrade **ownCloud 10** to **10.13.1 or later**. Do not leave 10.6.0–10.13.0 on the internet.
3. Tell IT: *\"CVE-2023-49105 is on CISA's actively-exploited list as of 08-27-2026. Federal deadline 08-30-2026. Upgrade ownCloud 10 to 10.13.1. If this server was internet-facing and unpatched, treat it as check-the-files, not patch-and-forget.\"*

**CISA metrics:** CISA confirmed this is being actively exploited as of 08-27-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch by 08-30-2026. Required action: upgrade ownCloud 10 to 10.13.1 or later.

---

## 4. CRITICAL — Old SQL Server 2014/2016/2017 can still be taken over — federal deadline is tomorrow
**CVE-2019-1068** · CISA confirmed active exploitation **08-26-2026** · federal patch deadline **08-29-2026** · **EPSS 0.5284 (98.9th percentile)** · CVSS 8.8/10 = high — network-reachable; a logged-in database user is enough
**Sources:** [Microsoft advisory CVE-2019-1068](https://portal.msrc.microsoft.com/en-US/security-guidance/advisory/CVE-2019-1068) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2019-1068) · [CISA alert 08-26-2026](https://www.cisa.gov/news-events/alerts/2026/08/26/cisa-adds-six-known-exploited-vulnerabilities-catalog) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** **Microsoft SQL Server 2014, 2016, and 2017** mishandle some internal functions so a connected database user can run code as the SQL Server engine account. You don't need the function-name detail — CISA says this 2019 bug is being used now. SQL Server 2019 and later are not on CISA's affected-product list. If you don't run 2014/2016/2017, you're done.

**Why it matters to an SMB running AI tools:** SQL Server is still the warehouse behind a lot of "chat with our data" tools, Power BI, and Copilot connectors. If the engine account is owned, the attacker is inside the same tables those assistants read — invoices, HR exports, customer lists.

**What you do Monday (20 minutes — do it before 08-29 if you still run 2014/2016/2017):**
1. In SQL Server Management Studio run `SELECT @@VERSION;`. If it says 2014, 2016, or 2017, continue. If 2019 or newer, you're outside this listing.
2. Install Microsoft's **July 9, 2019** SQL Server security update (GDR or the CU that includes CVE-2019-1068) from Windows Update or the Microsoft Update Catalog — or upgrade that instance to a currently supported SQL Server.
3. Tell IT: *\"CVE-2019-1068 is on CISA's actively-exploited list as of 08-26-2026. Federal deadline is 08-29-2026. Patch SQL 2014/2016/2017 today and confirm the instance is not on the public internet.\"*

**CISA metrics:** CISA confirmed this is being actively exploited as of 08-26-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch by 08-29-2026. Required action: apply the July 2019 SQL Server security updates (or upgrade off 2014/2016/2017).

---

## Friday companion — this week's top 3

1. **Gitea (CVE-2026-60004)** — federal deadline is **today (08-28-2026)**. EPSS 0.824 (99.6th percentile). If you self-host Git, this is the weekend's #1.
2. **SQL Server 2014/2016/2017 (CVE-2019-1068) and Citrix NetScaler (CVE-2026-8452)** — both due **08-29-2026**. SQL is the high-likelihood one (EPSS 0.5284). NetScaler is the front-door one (KEV beats its low EPSS). Firmware: **14.1-72.61** or **13.1-63.18** ([CTX696604](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX696604)).
3. **ownCloud (CVE-2023-49105)** — new KEV on **08-27-2026**, no login required if a username is known, due **08-30-2026**. Pair with **JFrog Artifactory (CVE-2026-66384)** if you run an AI/package warehouse.

Same-week also-patch: Ajax.NET Professional CVE-2021-23758 (EPSS 0.8363, due 09-09-2026); Oracle HTTP Server / WebLogic Proxy Plug-in CVE-2026-21962 (deadline **08-27-2026 already passed**).

---

## Jargon buster (terms used today)
- **CVE:** a unique ID for a security flaw, so everyone tracks the same bug (like a license plate).
- **RCE (Remote Code Execution):** attacker can run their own code on your machine — full control.
- **EPSS:** 0–1 score of how likely a flaw is to be exploited in the next 30 days. Higher = patch first.
- **Percentile:** where a score ranks — 99.6th = more likely to be exploited than 99.6% of known flaws.
- **KEV (Known Exploited Vulnerabilities):** CISA's list of flaws being actively exploited right now.
- **CVSS:** a 0–10 severity score. 9.8/10 = critical — typically exploitable remotely with no login.
- **JFrog Artifactory:** a warehouse for software packages and Docker images — often the same place AI pipelines pull models and dependencies.
- **Path traversal:** using `../` (or similar) in a file path to land outside the allowed folder.
- **Gitea:** a self-hosted Git (source-code) server many small teams run instead of GitHub.
- **Git hook:** a small script Git runs automatically when something happens in a repo. If an attacker plants one, it runs with the Git server's permissions.
- **ownCloud:** self-hosted file-sync (like a private Dropbox). A hole here is a hole in the documents your AI tools summarize.
- **WebDAV:** an old-but-common way programs read and write files over HTTP. ownCloud's file API uses it.
- **Pre-signed URL:** a file link that's supposed to prove you were allowed to access it. If the signing key was never set, the proof is fake.
- **SQL Server:** Microsoft's database engine. 2014/2016/2017 are the versions in today's listing.
- **NetScaler ADC / NetScaler Gateway:** Citrix's appliance that is often the VPN and website front door. Firmware deadline tomorrow.
- **Ajax.NET Professional / AjaxPro:** an old .NET library that lets a web page call server code without a full reload. Leftover copies are the risk.
- **MCP (Model Context Protocol):** the plug-in style that lets an AI assistant use extra tools (files, notes, browsers). A hole in an MCP helper is a hole in whatever that assistant can reach.
- **getnote-mcp:** a notes helper that plugs into an AI assistant via MCP. Versions through 1.5.0 could be tricked into reading local files.
- **LangChain:** a popular framework for building "chat with your data" apps.
- **GraphCypherQAChain:** LangChain's helper that turns a chat question into a graph-database query.
- **picklescan / pickle / PyTorch:** scanner, file format, and toolkit for loading AI models. An old scanner can miss a poisoned model file.
- **Budibase:** a low-code app builder. Today's CIRCL cluster includes a plugin-upload code-execution hole — only if you actually run it.
- **Ransomware:** malware that locks your files and demands payment — the top small-business threat.
- **anubis / lockbit5 / qilin / chaos / SilentRansomGroup / emperador:** ransomware groups in today's victim disclosures. Treat the name as a sector-targeting signal, not a reason to pay.
- **ClearFake:** malware that pretends to be a browser or software update so a visitor infects themselves.
- **IClickFix:** malware that tricks a visitor into running a "fix" or "click this" command. Fake troubleshooting pages are the usual tell.
- **Shin webshell / php.shin_webshell:** a PHP webshell family. A domain listed with this name is already hosting attacker-controlled code — block and hunt, don't visit.
- **IOC (Indicator of Compromise):** a trace of an attack (malicious IP/domain/file) to hunt for in logs.

Full plain-language library: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).

---

## Appendix — raw signals (for the technical reader)

### CISA KEV (last 7 days, ranked by EPSS — links to vendor advisories)
| CVE | Product | EPSS | CISA confirmed | Federal deadline | Ransomware use | Source |
|---|---|---|---|---|---|---|
| CVE-2021-23758 | Ajax.NET Professional (deserialization / RCE) | **0.8363** | 08-26-2026 | 09-09-2026 | Unknown | [GHSA](https://github.com/michaelschwarz/Ajax.NET-Professional/security/advisories/GHSA-6r7c-6w96-8pvw) |
| CVE-2026-60004 | Gitea (code injection via patch API / Git hook) | **0.824** | 08-25-2026 | 08-28-2026 | Unknown | [GHSA](https://github.com/go-gitea/gitea/security/advisories/GHSA-rcr6-4jqh-j84m) |
| CVE-2019-1068 | Microsoft SQL Server 2014/2016/2017 (RCE) | **0.5284** | 08-26-2026 | 08-29-2026 | Unknown | [MSRC](https://portal.msrc.microsoft.com/en-US/security-guidance/advisory/CVE-2019-1068) |
| CVE-2026-21962 | Oracle HTTP Server / WebLogic Proxy Plug-in (access control) | **0.4202** | 08-24-2026 | 08-27-2026 | Unknown | [Oracle Jan 2026 CPU](https://www.oracle.com/security-alerts/cpujan2026.html) |
| CVE-2023-49105 | ownCloud 10.6.0–10.13.0 (WebDAV auth bypass) | **0.1107** | 08-27-2026 | 08-30-2026 | Unknown | [ownCloud advisory](https://owncloud.com/security-advisories/webdav-api-authentication-bypass-using-pre-signed-urls/) |
| CVE-2022-0995 | Linux Kernel (local out-of-bounds write) | 0.0952 | 08-26-2026 | 09-09-2026 | Unknown | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2022-0995) |
| CVE-2015-3246 | Red Hat libuser (local race / passwd corruption) | 0.088 | 08-26-2026 | 09-09-2026 | Unknown | [Red Hat](https://access.redhat.com/articles/1537873) |
| CVE-2015-5287 | Red Hat ABRT (local privilege escalation; likely EoL) | 0.0496 | 08-26-2026 | 09-09-2026 | Unknown | [Fix commit](https://github.com/abrt/abrt/commit/3c1b60cfa62d39e5fff5a53a5bc53dae189e740e) |
| CVE-2026-8452 | Citrix NetScaler ADC / Gateway (memory buffer / DoS) | 0.0161 | 08-26-2026 | 08-29-2026 | Unknown | [CTX696604](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX696604) |
| CVE-2026-53362 | Linux Kernel IPv6 (local privilege escalation) | 0.0027 | 08-27-2026 | 08-30-2026 | Unknown | [Kernel commit](https://git.kernel.org/stable/c/14200d435af9a9eeb444f529fc2f689a236b7962) |
| CVE-2026-66384 | JFrog Artifactory (Docker cache path traversal) | 0.0026 | 08-27-2026 | 09-10-2026 | Unknown | [JFrog advisory](https://docs.jfrog.com/releases/docs/jfrog-security-advisories#cve-2026-66384---authenticated-users-may-write-data-outside-the-intended-docker-cache-path) |

Three added 08-27-2026: [CISA alert](https://www.cisa.gov/news-events/alerts/2026/08/27/cisa-adds-three-known-exploited-vulnerabilities-catalog). Six added 08-26-2026: [CISA alert](https://www.cisa.gov/news-events/alerts/2026/08/26/cisa-adds-six-known-exploited-vulnerabilities-catalog).

### Ransomware.live — recent victims (10)
| Group | Sector | Country | Discovered | Source |
|---|---|---|---|---|
| lockbit5 | Healthcare | TN | 08-28-2026 | [Ransomware.live](https://www.ransomware.live) |
| anubis | Healthcare | — | 08-28-2026 | [Ransomware.live](https://www.ransomware.live) |
| chaos | Not Found | AU | 08-27-2026 | [Ransomware.live](https://www.ransomware.live) |
| SilentRansomGroup | Not Found (name redacted; disclosure timer) | — | 08-27-2026 | [Ransomware.live](https://www.ransomware.live) |
| qilin | Transportation | PH | 08-27-2026 | [Ransomware.live](https://www.ransomware.live) |
| SilentRansomGroup | Not Found (name redacted; disclosure timer) | — | 08-27-2026 | [Ransomware.live](https://www.ransomware.live) |
| qilin | Retail & E-Commerce | DE | 08-27-2026 | [Ransomware.live](https://www.ransomware.live) |
| qilin | Technology | SG | 08-27-2026 | [Ransomware.live](https://www.ransomware.live) |
| lockbit5 | Professional Services | NL | 08-27-2026 | [Ransomware.live](https://www.ransomware.live) |
| emperador | Technology | — | 08-27-2026 | [Ransomware.live](https://www.ransomware.live) |

No leak-site or .onion links. Named pulse: two healthcare claims (lockbit5, anubis) plus a qilin cluster across transportation, retail, and technology.

### CIRCL — highest-signal new items (30 pulled; 5 empty/unparseable records skipped)
- **CVE-2024-8309 (EPSS 0.1374, 96.2nd pct)** — LangChain GraphCypherQAChain SQL injection via prompt injection; `langchain` patched at **0.2.0**, `langchain-community` patched at **0.2.19** — [GHSA](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [Fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) · [huntr](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5)
- **CVE-2025-1889 (EPSS 0.0038, 31.0th pct)** — picklescan missed non-standard pickle extensions in ML model files; upgrade picklescan to **0.0.22 or later** — [GHSA](https://github.com/advisories/GHSA-769v-p64c-89pr) · [Sonatype](https://sites.google.com/sonatype.com/vulnerabilities/cve-2025-1889)
- **CVE-2026-82111 (EPSS n/a, published 08-28-2026)** — getnote-mcp (MCP notes helper) path traversal in `upload_image` / `image_path` through **1.5.0**; upgrade to **1.5.1** — [Fix commit](https://github.com/iswalle/getnote-mcp/commit/7f9a215e03575c650d38c8f87fc6d8d363fed80d) · [Release v1.5.1](https://github.com/iswalle/getnote-mcp/releases/tag/v1.5.1) · [CVE record](https://www.cve.org/CVERecord?id=CVE-2026-82111)
- **CVE-2026-82244 (EPSS n/a, published 08-28-2026)** — Budibase before **3.41.3**: authenticated admin can run code by uploading a plugin tarball (server `eval()` on plugin JavaScript) — [CIRCL](https://vulnerability.circl.lu/advisories/cve-2026-82244)

### IOCs (ThreatFox 8 + URLhaus 6, newest — linked)
- **ClearFake domains:** `wn0nofms.dsmlabs.io`, `lpqzx6iv.lepto--zan.com`, `yl9wom1c.en-trump-token.com`, `dsmlabs.io`, `home-power-shield.com` — [Malpedia: ClearFake](https://malpedia.caad.fkie.fraunhofer.de/details/js.clearfake)
- **IClickFix domains:** `nreearts.com.bd`, `primekitsbd.com` — [Malpedia: IClickFix](https://malpedia.caad.fkie.fraunhofer.de/details/js.iclickfix)
- **Shin webshell domain:** `vuqena.workers.dev` (confidence 50) — [Malpedia: php.shin_webshell](https://malpedia.caad.fkie.fraunhofer.de/details/php.shin_webshell)
- **URLhaus:** [182.119.12.4:52303/i](https://urlhaus.abuse.ch/url/3909271/) · [91.92.242.236 file_da5806c64db79315.exe](https://urlhaus.abuse.ch/url/3909270/) · [42.85.15.247:42620/i](https://urlhaus.abuse.ch/url/3909269/) · [196.190.133.180:41857/i](https://urlhaus.abuse.ch/url/3909268/) · [115.56.43.164:34354/i](https://urlhaus.abuse.ch/url/3909267/) · [103.31.103.204:49856/i](https://urlhaus.abuse.ch/url/3909266/)

---

*Compiled from public sources · 08-28-2026 · Sources: CISA KEV, CISA Advisories, Ransomware.live, CIRCL, FIRST EPSS, ThreatFox, URLhaus*
