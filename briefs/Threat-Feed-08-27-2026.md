---
type: threat-feed-note
title: "Threat Feed - 08-27-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-08-27
source: "cisa-kev, cisa-advisories, ransomware.live, circl, epss, threatfox, urlhaus"
related: "https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md"
---

# Threat Feed — 08-27-2026

> **Reader promise:** 3-minute read. Headlines alone tell you what to do. New term? Check the [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).
> **Lens:** threats that hit AI tools, automations, and small-business money.
> **Sources:** every finding links to its primary source. If you want to verify, click.

## How to read the scores (30 seconds)
- **EPSS (0–1):** a score estimating how likely this flaw is to be exploited in the next 30 days; higher = patch first. 0.78 ≈ 78% — patch first. 0.01 ≈ 1% — lower urgency. Percentile ranks it against every known flaw: 99.5th = more likely to be exploited than 99.5% of all known vulnerabilities.
- **CISA KEV:** CISA only adds a flaw after confirming it's being **actively exploited right now** — not theoretical. The date shown is when CISA confirmed it. The federal deadline is their urgency rating in date form.
- **Today's window:** CISA added **six** actively exploited flaws on **08-26-2026** ([alert](https://www.cisa.gov/news-events/alerts/2026/08/26/cisa-adds-six-known-exploited-vulnerabilities-catalog)). Oracle's federal clock is **today (08-27-2026)**. Gitea's is **tomorrow (08-28-2026)**. Citrix NetScaler and SQL Server are **08-29-2026**. Ajax.NET is **09-09-2026**. Three of the six new listings are old local Linux/Red Hat bugs — only urgent if you still run those hosts.

---

## 1. WATCH — The scanner you use to check downloaded AI models can miss a poisoned file
**CVE-2025-1889** · CIRCL / GHSA (not on CISA KEV) · **EPSS 0.0038 (30.9th percentile)** — below the 0.1 "patch first" flag · GHSA 5.3/10 = moderate for the scanner miss; the danger is what happens if you then load the model
**Sources:** [GHSA](https://github.com/advisories/GHSA-769v-p64c-89pr) · [Fix commit](https://github.com/mmaitre314/picklescan/commit/baf03faf88fece56a89534d12ce048e5ee36e50e) · [Sonatype](https://sites.google.com/sonatype.com/vulnerabilities/cve-2025-1889) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2025-1889)

**What broke:** **picklescan (a checker meant to catch dangerous Python pickle files inside AI model downloads)** at **0.0.21 and earlier** only looks at usual file endings (`.pkl`, `.pt`). A model archive can hide a second pickle under a weird name; the old scanner skips it, and **PyTorch (the common toolkit that loads those model files)** still runs it. You don't need the archive-format detail — if your "we scanned it" step is an old picklescan, that stamp is not proof. If you never download model files, you're done.

**Why it matters to an SMB running AI tools:** This is the on-lens item: the broken product *is* the model-safety scanner. Shops that fine-tune or "try a model from the internet" often treat picklescan as the gate. A leftover 0.0.21 install means a poisoned model can walk into the same notebook or pipeline that holds customer data and API keys.

**What you do Monday (10 minutes):**
1. On the machine that loads models: `pip show picklescan`. If it's missing or **0.0.21 or older**, continue.
2. Upgrade: `pip install -U 'picklescan>=0.0.22'`. Confirm with `pip show picklescan`.
3. Until that's done: do not load `.pt` / `.pkl` files from strangers. "The scanner said it's clean" is false if the scanner is old.

**CISA metrics:** this item is from CIRCL + FIRST EPSS, not CISA KEV. CISA has not listed it as actively exploited. Known ransomware-campaign use: not flagged. Treat the scanner version as the action, not the low EPSS score.

**Attacker view (conceptual):** Hide a second pickle inside a model file the scanner won't open → the victim loads the model → code runs in the data-science environment. Defender rule of thumb: unexpected network calls or new processes at model-load time; picklescan older than 0.0.22.

---

## 2. CRITICAL — An old .NET web library in leftover internal apps is being used to run attacker code
**CVE-2021-23758** · CISA confirmed active exploitation **08-26-2026** · federal patch deadline **09-09-2026** · **EPSS 0.891 (99.8th percentile)** — more likely to be exploited than 99.8% of known flaws · CVSS 8.1/10 = high — reachable over the network with no login (attack complexity rated high)
**Sources:** [GitHub advisory GHSA-6r7c-6w96-8pvw](https://github.com/michaelschwarz/Ajax.NET-Professional/security/advisories/GHSA-6r7c-6w96-8pvw) · [Fix commit](https://github.com/michaelschwarz/Ajax.NET-Professional/commit/b0e63be5f0bb20dfce507cb8a1a9568f6e73de57) · [Official NuGet: AjaxNetProfessional](https://www.nuget.org/packages/AjaxNetProfessional/) · [Snyk](https://security.snyk.io/vuln/SNYK-DOTNET-AJAXPRO2-1925971) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2021-23758) · [CISA alert 08-26-2026](https://www.cisa.gov/news-events/alerts/2026/08/26/cisa-adds-six-known-exploited-vulnerabilities-catalog) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** **Ajax.NET Professional / AjaxPro (an old library that lets a browser call server code without a full page reload)** will take attacker-controlled data and turn it into live .NET objects — **deserialization (turning a data blob back into a running program object)**. That can become remote code execution. The official **AjaxNetProfessional** package is patched at **21.11.29.1**. The **AjaxPro.2** NuGet line has no patch; CISA says the product may be end-of-life and to **stop using it**. If you have no old ASP.NET apps, you're done.

**Why it matters to an SMB running AI tools:** This is not a bug in Copilot or LangChain. It is the forgotten internal website those tools often read (intranet, quoting, inventory). Cisco Talos (08-20-2026) reported a tracked group using this CVE on web servers *and* using AI agents to speed the steps after they get in. Old library, modern follow-through — the chatbot that summarizes that intranet inherits whatever the attacker plants.

**What you do Monday (20 minutes):**
1. On app servers, search for `AjaxPro.dll`, NuGet `AjaxPro.2`, `AjaxNetProfessional`, or `Joint.AjaxPro`. If none, you're done.
2. If you found **AjaxNetProfessional**: upgrade to **21.11.29.1 or later** from [nuget.org/packages/AjaxNetProfessional](https://www.nuget.org/packages/AjaxNetProfessional/). If you found **AjaxPro.2** or a fork CISA treats as end-of-life: remove it or replace that AJAX layer — there is no safe leftover version.
3. Tell IT: *"CVE-2021-23758 is on CISA's actively-exploited list as of 08-26-2026. EPSS 0.891. Federal deadline 09-09-2026. Find AjaxPro.dll, upgrade AjaxNetProfessional to 21.11.29.1 or remove AjaxPro.2, and look for unexpected IIS app-pool processes."*

**CISA metrics:** CISA confirmed this is being actively exploited as of 08-26-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch by 09-09-2026. Required action: upgrade AjaxNetProfessional to 21.11.29.1 or discontinue AjaxPro.2 / end-of-life builds.

**Attacker view (conceptual):** Find a leftover AjaxPro endpoint on an old .NET site → send crafted serialized data → code runs as the web app. Defender rule of thumb: AjaxPro.dll you forgot you shipped; odd POSTs to `.ashx` handlers; new processes from the IIS app pool.

---

## 3. CRITICAL — Old SQL Server 2014/2016/2017 can still be taken over — federal deadline is 08-29
**CVE-2019-1068** · CISA confirmed active exploitation **08-26-2026** · federal patch deadline **08-29-2026** · **EPSS 0.4466 (98.7th percentile)** · CVSS 8.8/10 = high — network-reachable; a logged-in database user is enough
**Sources:** [Microsoft advisory CVE-2019-1068](https://portal.msrc.microsoft.com/en-US/security-guidance/advisory/CVE-2019-1068) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2019-1068) · [CISA alert 08-26-2026](https://www.cisa.gov/news-events/alerts/2026/08/26/cisa-adds-six-known-exploited-vulnerabilities-catalog) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** **Microsoft SQL Server 2014, 2016, and 2017** mishandle some internal functions so a connected database user can run code as the SQL Server engine account. You don't need the function-name detail — CISA says this 2019 bug is being used now. SQL Server 2019 and later are not on CISA's affected-product list. If you don't run 2014/2016/2017, you're done.

**Why it matters to an SMB running AI tools:** SQL Server is still the warehouse behind a lot of "chat with our data" tools, Power BI, and Copilot connectors. If the engine account is owned, the attacker is inside the same tables those assistants read — invoices, HR exports, customer lists.

**What you do Monday (20 minutes — do it before 08-29 if you still run 2014/2016/2017):**
1. In SQL Server Management Studio run `SELECT @@VERSION;`. If it says 2014, 2016, or 2017, continue. If 2019 or newer, you're outside this listing.
2. Install Microsoft's **July 9, 2019** SQL Server security update (GDR or the CU that includes CVE-2019-1068) from Windows Update or the Microsoft Update Catalog — or upgrade that instance to a currently supported SQL Server.
3. Tell IT: *"CVE-2019-1068 is on CISA's actively-exploited list as of 08-26-2026. Federal deadline is 08-29-2026. Patch SQL 2014/2016/2017 today and confirm the instance is not on the public internet."*

**CISA metrics:** CISA confirmed this is being actively exploited as of 08-26-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch by 08-29-2026. Required action: apply the July 2019 SQL Server security updates (or upgrade off 2014/2016/2017).

---

## 4. CRITICAL — Your Citrix VPN / gateway box can be knocked over — patch by 08-29
**CVE-2026-8452** · CISA confirmed active exploitation **08-26-2026** · federal patch deadline **08-29-2026** · EPSS 0.0104 (61.5th percentile) — **KEV is the signal, not EPSS** · CVSS 8.8/10 = high — no login required against a Gateway or AAA virtual server
**Sources:** [Citrix CTX696604](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX696604) · [CVE record](https://www.cve.org/CVERecord?id=CVE-2026-8452) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-8452) · [CISA alert 08-26-2026](https://www.cisa.gov/news-events/alerts/2026/08/26/cisa-adds-six-known-exploited-vulnerabilities-catalog) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** **NetScaler ADC / NetScaler Gateway (the box that is often your VPN and website front door)** has a memory-buffer bug if it is set up as a Gateway (SSL VPN, ICA Proxy, CVPN, RDP Proxy) **or** an AAA login virtual server. Result: unpredictable behavior and a crash of that front door. CISA's writeup is denial-of-service; the vendor score also flags high confidentiality impact. You don't need the memory-bug detail — if this appliance is internet-facing, treat it as patch-now. If you don't run NetScaler, you're done.

**Why it matters to an SMB running AI tools:** This is not an AI-product bug. It is the tunnel remote staff and many automations use to reach the office. If the gateway is down or misbehaving, Copilot/n8n/VPN-only data sources fail — and anything behind that box is in play. CISA's federal clock is two days.

**What you do Monday (30 minutes — do it before 08-29 if you run NetScaler):**
1. On the appliance: `show version`. In scope if you have a Gateway or AAA vserver (`show vpn vserver` / `show authentication vserver`). If no NetScaler, you're done.
2. Upgrade firmware to **14.1-72.61 or later**, or **13.1-63.18 or later**. FIPS: **14.1-72.61 FIPS** or **13.1-37.272**. Builds below those are affected.
3. Tell IT: *"CVE-2026-8452 is on CISA's actively-exploited list as of 08-26-2026. Federal deadline is 08-29-2026. Upgrade NetScaler to 14.1-72.61 or 13.1-63.18. If you cannot patch today, take Gateway/AAA off the public internet."*

**CISA metrics:** CISA confirmed this is being actively exploited as of 08-26-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch by 08-29-2026. Required action: install the CTX696604 firmware builds above.

---

## 5. CRITICAL — The front door in front of your Oracle apps can be fully owned — federal deadline is today
**CVE-2026-21962** · CISA confirmed active exploitation **08-24-2026** · federal patch deadline **08-27-2026 (today)** · **EPSS 0.4202 (98.6th percentile)** · CVSS 10.0/10 = critical — exploitable remotely with no authentication
**Sources:** [Oracle January 2026 Critical Patch Update](https://www.oracle.com/security-alerts/cpujan2026.html) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-21962) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** **Oracle HTTP Server** and the **WebLogic Server Proxy Plug-in (the forwarder that sits on Apache or IIS in front of WebLogic apps)** versions **12.2.1.4.0, 14.1.1.0.0, and 14.1.2.0.0** fail to check who is allowed to do what. An unauthorized network caller can create, change, or delete critical data — up to complete access to the component. You don't need the plug-in internals — CISA says this is being exploited, Oracle scored it a 10, and the federal clock hits today.

**Why it matters to an SMB running AI tools:** WebLogic is the engine room behind a lot of mid-size ERP, CRM, and portal stacks. Those same systems are the data sources Copilot and "chat with your business apps" tools read. If the HTTP front door is owned, the attacker is inside the records those assistants summarize.

**What you do Monday (30 minutes — do it today if you run these):**
1. Ask whoever owns ERP/CRM/intranet: *"Do we run Oracle HTTP Server or the WebLogic Server Proxy Plug-in? Which version?"* If no, you're done.
2. Apply Oracle's **January 2026 Critical Patch Update** from My Oracle Support for the Fusion Middleware / HTTP Server / Proxy Plug-in packages on 12.2.1.4.0, 14.1.1.0.0, or 14.1.2.0.0.
3. Tell IT: *"CVE-2026-21962 is on CISA's actively-exploited list as of 08-24-2026. Federal deadline is 08-27-2026. Apply the January 2026 CPU today. If this box is internet-facing, treat it as check-this-host, not patch-and-forget."*

**CISA metrics:** CISA confirmed this is being actively exploited as of 08-24-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch by 08-27-2026. Required action: apply the January 2026 Oracle Critical Patch Update for HTTP Server / WebLogic Proxy Plug-in.

---

## Jargon buster (terms used today)
- **CVE:** a unique ID for a security flaw, so everyone tracks the same bug (like a license plate).
- **RCE (Remote Code Execution):** attacker can run their own code on your machine — full control.
- **EPSS:** 0–1 score of how likely a flaw is to be exploited in the next 30 days. Higher = patch first.
- **Percentile:** where a score ranks — 99.8th = more likely to be exploited than 99.8% of known flaws.
- **KEV (Known Exploited Vulnerabilities):** CISA's list of flaws being actively exploited right now.
- **CVSS:** a 0–10 severity score. 8.8/10 = high; 10.0/10 = the top of the scale — typically exploitable remotely with no login.
- **picklescan:** a scanner meant to catch dangerous Python pickle files inside AI model downloads. If it skips a file, a "model" can be malware.
- **pickle:** a Python file format for saving objects. Loading one can run code — treat a random `.pkl` / `.pt` like an unknown program.
- **PyTorch:** a common toolkit for training and loading AI models. `torch.load` on an untrusted file is the danger, not the brand name.
- **Ajax.NET Professional / AjaxPro:** an old .NET library that lets a web page call server code without a full reload. Leftover copies are the risk.
- **Deserialization:** turning a saved data blob back into a live program object. If the blob is attacker-controlled, that "restore" can run their code.
- **SQL Server:** Microsoft's database engine. 2014/2016/2017 are the versions in today's listing.
- **NetScaler ADC / NetScaler Gateway:** Citrix's appliance that is often the VPN and website front door.
- **AAA virtual server:** the login/authentication vserver on a NetScaler — if you have one, CVE-2026-8452 is in scope.
- **Oracle HTTP Server / WebLogic Server Proxy Plug-in:** the front door in front of many Oracle business apps; the plug-in sits on Apache or IIS and forwards traffic to WebLogic.
- **Improper access control:** the product fails to check who is allowed to do what.
- **Gitea:** a self-hosted Git (source-code) server many small teams run instead of GitHub. Federal deadline tomorrow (08-28-2026).
- **LangChain:** a popular framework for building "chat with your data" apps. Flaws in it hit lots of AI tools at once.
- **GraphCypherQAChain:** LangChain's helper that turns a chat question into a graph-database query. If that query isn't locked down, the chat becomes a database write.
- **Prompt injection / SQL injection:** hiding instructions or database commands inside the data an AI or app reads.
- **Flowintel:** an open-source case-management app. Today's CIRCL note is about how it shows case titles in the browser.
- **Ransomware:** malware that locks your files and demands payment — the top small-business threat.
- **SilentRansomGroup / iah6477:** ransomware groups in today's victim disclosures. Treat the name as a sector-targeting signal, not a reason to pay.
- **ClearFake:** malware that pretends to be a browser or software update so a visitor infects themselves.
- **XMRIG:** a crypto-miner. In an IOC list it means someone is stealing CPU time, not running a legit miner.
- **IOC (Indicator of Compromise):** a trace of an attack (malicious IP/domain/file) to hunt for in logs.

Full plain-language library: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).

---

## Appendix — raw signals (for the technical reader)

### CISA KEV (last 7 days, ranked by EPSS — links to vendor advisories)
| CVE | Product | EPSS | CISA confirmed | Federal deadline | Ransomware use | Source |
|---|---|---|---|---|---|---|
| CVE-2021-23758 | Ajax.NET Professional (deserialization / RCE) | **0.891** | 08-26-2026 | 09-09-2026 | Unknown | [GHSA](https://github.com/michaelschwarz/Ajax.NET-Professional/security/advisories/GHSA-6r7c-6w96-8pvw) |
| CVE-2019-1068 | Microsoft SQL Server 2014/2016/2017 (RCE) | **0.4466** | 08-26-2026 | 08-29-2026 | Unknown | [MSRC](https://portal.msrc.microsoft.com/en-US/security-guidance/advisory/CVE-2019-1068) |
| CVE-2026-21962 | Oracle HTTP Server / WebLogic Proxy Plug-in (access control) | **0.4202** | 08-24-2026 | 08-27-2026 | Unknown | [Oracle Jan 2026 CPU](https://www.oracle.com/security-alerts/cpujan2026.html) |
| CVE-2015-3246 | Red Hat libuser (local race / passwd corruption) | 0.0709 | 08-26-2026 | 09-09-2026 | Unknown | [Red Hat](https://access.redhat.com/articles/1537873) |
| CVE-2022-0995 | Linux Kernel (local out-of-bounds write) | 0.0634 | 08-26-2026 | 09-09-2026 | Unknown | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2022-0995) |
| CVE-2015-5287 | Red Hat ABRT (local privilege escalation; likely EoL) | 0.0341 | 08-26-2026 | 09-09-2026 | Unknown | [Fix commit](https://github.com/abrt/abrt/commit/3c1b60cfa62d39e5fff5a53a5bc53dae189e740e) |
| CVE-2026-73570 | Synacor Zimbra ZCS (OS command injection via SMTP) | 0.0151 | 08-21-2026 | 08-24-2026 | Unknown | [Zimbra 10.1.20](https://blog.zimbra.com/2026/07/patch-release-update-zimbra-10-1-20/) |
| CVE-2026-8452 | Citrix NetScaler ADC / Gateway (memory buffer / DoS) | 0.0104 | 08-26-2026 | 08-29-2026 | Unknown | [CTX696604](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX696604) |
| CVE-2026-60004 | Gitea (code injection via patch API / Git hook) | n/a | 08-25-2026 | 08-28-2026 | Unknown | [GHSA](https://github.com/go-gitea/gitea/security/advisories/GHSA-rcr6-4jqh-j84m) |

Six added 08-26-2026: [CISA alert](https://www.cisa.gov/news-events/alerts/2026/08/26/cisa-adds-six-known-exploited-vulnerabilities-catalog).

### Ransomware.live — recent victims (10)
| Group | Sector | Country | Discovered | Source |
|---|---|---|---|---|
| SilentRansomGroup | Not Found (name redacted; disclosure timer) | — | 08-26-2026 | [Ransomware.live](https://www.ransomware.live) |
| SilentRansomGroup | Not Found (name redacted; disclosure timer) | — | 08-26-2026 | [Ransomware.live](https://www.ransomware.live) |
| SilentRansomGroup | Not Found (name redacted; disclosure timer) | — | 08-26-2026 | [Ransomware.live](https://www.ransomware.live) |
| SilentRansomGroup | Not Found (name redacted; disclosure timer) | — | 08-26-2026 | [Ransomware.live](https://www.ransomware.live) |
| SilentRansomGroup | Not Found (name redacted; disclosure timer) | — | 08-26-2026 | [Ransomware.live](https://www.ransomware.live) |
| SilentRansomGroup | Not Found (name redacted; disclosure timer) | — | 08-26-2026 | [Ransomware.live](https://www.ransomware.live) |
| SilentRansomGroup | Not Found (name redacted; disclosure timer) | — | 08-26-2026 | [Ransomware.live](https://www.ransomware.live) |
| iah6477 | Manufacturing | US | 08-26-2026 | [Ransomware.live](https://www.ransomware.live) |
| SilentRansomGroup | Not Found (name redacted; disclosure timer) | — | 08-26-2026 | [Ransomware.live](https://www.ransomware.live) |
| iah6477 | Manufacturing | US | 08-26-2026 | [Ransomware.live](https://www.ransomware.live) |

No leak-site or .onion links. Named pulse: two US manufacturing claims (iah6477; listed haul sizes 745.3 GiB and 148.2 GiB). The rest are SilentRansomGroup entries with company names still redacted.

### CIRCL — highest-signal new items (30 pulled; 27 empty/unparseable records skipped)
- **CVE-2024-8309 (EPSS 0.1374, 96.2nd pct)** — LangChain GraphCypherQAChain SQL injection via prompt injection; `langchain` patched at **0.2.0**, `langchain-community` patched at **0.2.19** — [GHSA](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [Fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) · [huntr](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5)
- **CVE-2025-1889 (EPSS 0.0038, 30.9th pct)** — picklescan missed non-standard pickle extensions in ML model files; upgrade picklescan to **0.0.22 or later** — [GHSA](https://github.com/advisories/GHSA-769v-p64c-89pr) · [Sonatype](https://sites.google.com/sonatype.com/vulnerabilities/cve-2025-1889)
- **CVE-2026-81814 (EPSS n/a, published 08-27-2026)** — Flowintel calendar titles rendered with innerHTML from case titles (script-capable content in the browser) — [CIRCL](https://vulnerability.circl.lu/advisories/cve-2026-81814)

### IOCs (ThreatFox 8 + URLhaus 6, newest — linked)
- **ClearFake domains:** `healthmetabolismreset.com`, `www.femmesdefoot.com`, `duo-theo-werni.ch`, `weddingstars.gr`, `cmp.mc` — [Malpedia: ClearFake](https://malpedia.caad.fkie.fraunhofer.de/details/js.clearfake)
- **Unknown malware domain:** `spiraldirect.ch` — [ThreatFox / Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/unknown)
- **XMRIG URLs:** `http://92.246.139.83/2` and `/3` — [Malpedia: XMRIG](https://malpedia.caad.fkie.fraunhofer.de/details/elf.xmrig)
- **URLhaus:** [62.60.226.140 YZvtV2H.exe (offline)](https://urlhaus.abuse.ch/url/3908964/) · [115.48.151.132:36550/i](https://urlhaus.abuse.ch/url/3908963/) · [119.116.34.176:47926/i](https://urlhaus.abuse.ch/url/3908962/) · [115.48.151.132:36550/bin.sh](https://urlhaus.abuse.ch/url/3908961/) · [182.126.124.161:50960/i](https://urlhaus.abuse.ch/url/3908960/) · [219.155.10.234:34322/i](https://urlhaus.abuse.ch/url/3908959/)

---

*Compiled from public sources · 08-27-2026 · Sources: CISA KEV, CISA Advisories, Ransomware.live, CIRCL, FIRST EPSS, ThreatFox, URLhaus*
