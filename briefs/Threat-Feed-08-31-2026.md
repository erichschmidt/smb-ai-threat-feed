---
type: threat-feed-note
title: "Threat Feed - 08-31-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-08-31
source: "cisa-kev, cisa-advisories, ransomware.live, circl, epss, threatfox, urlhaus"
related: "https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md"
---

# Threat Feed — 08-31-2026

> **Reader promise:** 3-minute read. Headlines alone tell you what to do. New term? Check the [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).
> **Lens:** threats that hit AI tools, automations, and small-business money.
> **Sources:** every finding links to its primary source. If you want to verify, click.

## How to read the scores (30 seconds)
- **EPSS (0–1):** a score estimating how likely this flaw is to be exploited in the next 30 days; higher = patch first. 0.78 ≈ 78% — patch first. 0.01 ≈ 1% — lower urgency. Percentile ranks it against every known flaw: 99.5th = more likely to be exploited than 99.5% of all known vulnerabilities.
- **CISA KEV:** CISA only adds a flaw after confirming it's being **actively exploited right now** — not theoretical. The date shown is when CISA confirmed it. The federal deadline is their urgency rating in date form.
- **Today's window:** No new actively exploited vulnerabilities were added to CISA KEV on **08-31-2026**. Overdue federal deadlines: Gitea (**CVE-2026-60004**, EPSS **0.8455**) **08-28-2026**; SQL Server (**CVE-2019-1068**, EPSS **0.5284**) and Citrix NetScaler (**CVE-2026-8452**) **08-29-2026**; ownCloud (**CVE-2023-49105**, EPSS **0.4320**) and Linux IPv6 kernel (**CVE-2026-53362**) **08-30-2026**. Still open: Ajax.NET Professional (**CVE-2021-23758**, EPSS **0.8363**) **09-09-2026**; Linux kernel OOB write / libuser / ABRT **09-09-2026**; JFrog Artifactory (**CVE-2026-66384**) **09-10-2026**.

---

## 1. HIGH — Unreviewed GitHub pull requests could run in your Google cloud build pipeline — Google already patched it; check your trigger history
**CVE-2026-19410** · published **08-31-2026** (CIRCL) · Google service-side fix **06-24-2026**, disclosed **08-24-2026** · not on CISA KEV · EPSS not scored · CVSS 9.4 (CVSS v4) = critical impact if it worked — unreviewed code in the build environment · CISA SSVC: exploitation none
**Sources:** [CIRCL / CVE-2026-19410](https://vulnerability.circl.lu/vuln/CVE-2026-19410) · [Google Cloud Build release notes (08-24-2026)](https://docs.cloud.google.com/build/docs/release-notes#August_24_2026) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-19410)

**What broke:** **Cloud Build (Google's managed service that builds, tests, and deploys your code)** has a GitHub pull-request trigger with **comment control (a gate that is supposed to require a repo collaborator to comment before an untrusted pull request is built)**. Before 06-24-2026, that gate could be beaten with webhook suppression so unreviewed code still ran in the build environment — including whatever secrets and deploy keys that trigger holds. Google patched the service on 06-24-2026 and says no customer patch is required. If you do not use Cloud Build GitHub PR triggers, you're done.

**Why it matters to an SMB running AI tools:** This is the on-lens item: the broken product is the automation pipeline itself. Cloud Build is a common path for model deploys, RAG app releases, and "push to GitHub → ship the bot." A poisoned PR that still runs is not a code-review miss — it is unreviewed code executing next to your cloud keys, model registry credentials, and production deploy targets.

**What you do Monday (15 minutes):**
1. Google Cloud Console → Cloud Build → Triggers. Open each GitHub **pull request** trigger and confirm Comment Control is on (collaborator comment required before building forks / untrusted PRs).
2. Cloud Build → History. Filter the last 90 days for PR-triggered builds from forks. If any ran without a maintainer comment, treat that trigger's secrets as exposed and rotate them (Cloud Build → the trigger → substitution variables / Secret Manager bindings).
3. Google's note: the service-side fix landed 06-24-2026; there is nothing to install. If a contractor copied a homegrown "comment to run CI" gate, do not assume it is safe — that pattern is what broke here.

**Attacker view (conceptual):** Open a pull request from a fork → interfere with the webhook so the "maintainer already approved this commit" check and the commit that actually builds are not the same → unreviewed code runs with the pipeline's secrets. Defender rule of thumb: comment-control must bind to the exact commit SHA that is built; hunt PR builds that have no matching collaborator comment.

---

## 2. HIGH — Your AI-model scanner can give a clean bill of health to a malicious model file
**CVE-2025-1889** · published **03-03-2025** (active in CIRCL index) · not on CISA KEV · **EPSS 0.0038 (31.1st percentile)** — below the 0.1 "patch first" flag; you are here because the broken thing is an AI supply-chain control, not because EPSS is high · CIRCL lists CVSS 9.8/10 for code execution if a bad model is loaded; the scanner-bypass itself is rated Medium by the vendor
**Sources:** [GHSA-769v-p64c-89pr](https://github.com/advisories/GHSA-769v-p64c-89pr) · [Sonatype advisory](https://sites.google.com/sonatype.com/vulnerabilities/cve-2025-1889) · [CIRCL / PYSEC-2025-19](https://vulnerability.circl.lu/vuln/CVE-2025-1889) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2025-1889)

**What broke:** **picklescan (a scanner meant to catch dangerous Python pickle files inside AI model downloads)** versions through **0.0.21** only inspects files with expected extensions (`.pkl`, `.pt`, and similar). A model archive can hide a second pickle under a non-standard name; the scanner skips it, **PyTorch (the common toolkit that loads those models)** still loads it, and that load can run attacker code. Fixed in **picklescan 0.0.22**. If you do not download or scan third-party model files, you're done.

**Why it matters to an SMB running AI tools:** This is on-lens: the hole is in the control that is supposed to make "chat with this model" safe. Hugging Face downloads, vendor "starter" weights, and intern-dropped `.pt` files often get a picklescan pass, then `torch.load`, then a production assistant. A clean scan on 0.0.21 is not a safety result.

**What you do Monday (10 minutes):**
1. On every host that scans or loads models: `pip show picklescan`. You need **0.0.22 or later**. If the package is missing, you are not scanning — treat untrusted models as untrusted programs.
2. Upgrade: `pip install -U "picklescan>=0.0.22"`. Re-scan anything you accepted on an older scanner.
3. Do not `torch.load` untrusted files. Prefer **safetensors** (or `weights_only=True` on trusted files). Tell IT: *"CVE-2025-1889 — picklescan before 0.0.22 can miss a malicious pickle with a weird extension. Upgrade the scanner and stop loading random .pt files."*

---

## 3. CRITICAL — Your self-hosted code server can still be taken over — federal deadline passed 08-28-2026
**CVE-2026-60004** · CISA confirmed active exploitation **08-25-2026** · federal patch deadline **08-28-2026 (passed)** · **EPSS 0.8455 (99.7th percentile)** — more likely to be exploited than 99.7% of known flaws · CVSS 9.8/10 = critical — network-reachable code execution
**Sources:** [Gitea advisory GHSA-rcr6-4jqh-j84m](https://github.com/go-gitea/gitea/security/advisories/GHSA-rcr6-4jqh-j84m) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-60004) · [CISA alert 08-25-2026](https://www.cisa.gov/news-events/alerts/2026/08/25/cisa-adds-one-known-exploited-vulnerability-catalog) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** **Gitea (a self-hosted Git / source-code server)** will take a crafted patch on the `diffpatch` API and plant a **Git hook (a script Git runs automatically on an event)**. That script runs as the Gitea service account — repos, secrets, and whatever that account can reach. Affected: **1.17 through 1.27.0**. Fixed: **1.27.1**. If open sign-up is on, a stranger can register, create a repo, and get the write access this needs. If you don't run Gitea, you're done.

**Why it matters to an SMB running AI tools:** This is not a bug in the chatbot. It is the repo those automations clone — prompts, n8n workflows, RAG loaders, API keys in `.env` files someone committed. If Gitea is owned, the next pipeline run is the attacker's. Highest EPSS in this week's KEV window, and the federal deadline is already three days past.

**What you do Monday (20 minutes — do it today if you still run Gitea before 1.27.1):**
1. On the Gitea host: `gitea --version` (or Site Administration → Configuration). If **1.27.1 or later**, you're outside this listing. If no Gitea, you're done.
2. Upgrade to **1.27.1 or later**. Until that's done, turn **off** open registration (Site Administration → Authentication / Register).
3. Tell IT: *"CVE-2026-60004 is on CISA's actively-exploited list as of 08-25-2026. EPSS 0.8455. Federal deadline was 08-28-2026. Upgrade Gitea to 1.27.1, disable open sign-up, and look for unexpected Git hooks and new processes as the Gitea user."*

**CISA metrics:** CISA confirmed this is being actively exploited as of 08-25-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch by 08-28-2026. Required action: upgrade Gitea to 1.27.1 or later.

---

## 4. HIGH — Your package warehouse can be tricked into writing files outside the Docker cache — federal deadline 09-10-2026
**CVE-2026-66384** · CISA confirmed active exploitation **08-27-2026** · federal patch deadline **09-10-2026** · EPSS 0.0058 (45.3rd percentile) — **KEV is the authoritative signal, not EPSS** · vendor severity Medium (authenticated path write)
**Sources:** [JFrog security advisories](https://docs.jfrog.com/releases/docs/jfrog-security-advisories) · [Artifactory self-managed releases](https://docs.jfrog.com/releases/docs/artifactory-self-managed-releases) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-66384) · [CISA alert 08-27-2026](https://www.cisa.gov/news-events/alerts/2026/08/27/cisa-adds-three-known-exploited-vulnerabilities-catalog) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** Self-hosted **JFrog Artifactory (the warehouse for packages and Docker images — often the same place AI pipelines pull models and dependencies)** lets an authenticated user write data **outside** the intended Docker cache path under specific remote-repository conditions (**path traversal — using a crafted path to reach files the product should not write**). You don't need the cache-path detail: CISA confirmed this is being exploited. JFrog patched **7.146.35** and the **7.161.16** line. If you only use JFrog's SaaS and they have already rolled the fix, confirm with your admin; this listing is aimed at self-managed Artifactory.

**Why it matters to an SMB running AI tools:** Artifactory is where build pipelines and model runners pull "trusted" images. A write outside the cache is a foothold next to those artifacts — poison an image once, every GPU box that pulls it inherits the problem. KEV listing plus a still-open 09-10-2026 federal deadline is the urgency, even with a low EPSS.

**What you do Monday (15 minutes):**
1. Artifactory UI → Administration → check version (or the version string on the login/footer). If you are on SaaS only, ask the vendor/admin whether 7.146.35 / 7.161.16 (or later) is live. If you do not run Artifactory, you're done.
2. Self-managed: if version is **below 7.146.35**, or **7.161.0 through 7.161.15**, upgrade to **7.146.35** or **7.161.16 or later** per the JFrog advisory table.
3. Tell IT: *"CVE-2026-66384 is on CISA KEV as of 08-27-2026. Federal deadline 09-10-2026. Upgrade self-hosted Artifactory to 7.146.35 or 7.161.16+ and review Docker remote-repo cache paths for unexpected files."*

**CISA metrics:** CISA confirmed this is being actively exploited as of 08-27-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch by 09-10-2026. Required action: apply vendor mitigations; upgrade Artifactory to the patched releases above.

---

## Jargon buster (terms used today)
- **CVE:** a unique ID for a security flaw, so everyone tracks the same bug (like a license plate).
- **EPSS:** 0–1 score of how likely a flaw is to be exploited in the next 30 days. Higher = patch first.
- **Percentile:** where a score ranks — 99.7th = more likely to be exploited than 99.7% of known flaws.
- **KEV (Known Exploited Vulnerabilities):** CISA's list of flaws being actively exploited right now.
- **CVSS:** a 0–10 severity score. 9.8/10 = critical — typically exploitable remotely with no login.
- **Cloud Build:** Google's managed service that builds, tests, and deploys code from GitHub and similar.
- **Comment control:** a Cloud Build / GitHub setting that is supposed to require a collaborator comment before an untrusted pull request is built.
- **picklescan / pickle:** a scanner and a Python file format for AI models; outdated scanners can miss malicious model payloads.
- **PyTorch:** a common toolkit for training and loading AI models. `torch.load` on an untrusted file is the danger.
- **safetensors:** a safer model-weight format that does not run code on load the way pickle can.
- **Gitea:** a self-hosted Git server; federal deadline passed 08-28-2026, still the highest-EPSS item in this window (0.8455).
- **Git hook:** a small script Git runs automatically on an event (commit, push). If an attacker plants one, it runs with the Git server's permissions.
- **JFrog Artifactory:** a repository manager for packages and Docker images used in AI pipelines.
- **Path traversal:** using `../` or a crafted path to write or read files outside the intended folder.
- **ownCloud:** self-hosted file-sync; federal deadline passed 08-30-2026.
- **Ajax.NET Professional / AjaxPro:** an older .NET web library; federal deadline 09-09-2026, EPSS 0.8363.
- **SQL Server:** Microsoft's database engine; federal patch deadline passed 08-29-2026.
- **NetScaler ADC / NetScaler Gateway:** Citrix's appliance that is often the VPN and website front door.
- **Linux Kernel:** the core operating system software running Linux servers, containers, and VMs.
- **LangChain / GraphCypherQAChain:** a popular AI application framework and its graph-database query helper (still in CIRCL; EPSS 0.1374).
- **WINS:** an old Windows name-lookup service. Samba's WINS hook is the high-EPSS CIRCL item today — only in play if you turned it on.
- **Ransomware:** malware that locks your files and demands payment — the top threat to small businesses.
- **ClearFake:** malware that pretends to be a browser or software update so a visitor infects themselves.
- **DanaBot:** malware that steals banking and browser data and gives the attacker a foothold on a Windows PC.
- **Aisuru:** a botnet / malware family seen in today's IOC list — treat the IP:port as a block-and-hunt address.
- **Shin webshell / php.shin_webshell:** a PHP webshell family. A domain listed with this name is already hosting attacker-controlled code — block and hunt, don't visit.
- **Mozi:** malware that infects internet-connected gadgets (routers, cameras) and turns them into a botnet.
- **IOC (Indicator of Compromise):** a trace of an attack (malicious IP/domain/file) to hunt for in network logs.

Full plain-language library: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).

---

## Appendix — raw signals (for the technical reader)

### CISA KEV (last 7 days, ranked by EPSS — links to vendor advisories)
| CVE | Product | EPSS | CISA confirmed | Federal deadline | Ransomware use | Source |
|---|---|---|---|---|---|---|
| CVE-2026-60004 | Gitea (code injection via diffpatch API / Git hook) | **0.8455** | 08-25-2026 | 08-28-2026 | Unknown | [GHSA](https://github.com/go-gitea/gitea/security/advisories/GHSA-rcr6-4jqh-j84m) |
| CVE-2021-23758 | Ajax.NET Professional (deserialization / RCE) | **0.8363** | 08-26-2026 | 09-09-2026 | Unknown | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2021-23758) · [Fix commit](https://github.com/michaelschwarz/Ajax.NET-Professional/commit/b0e63be5f0bb20dfce507cb8a1a9568f6e73de57) |
| CVE-2019-1068 | Microsoft SQL Server 2014/2016/2017 (RCE) | **0.5284** | 08-26-2026 | 08-29-2026 | Unknown | [MSRC](https://portal.msrc.microsoft.com/en-US/security-guidance/advisory/CVE-2019-1068) |
| CVE-2023-49105 | ownCloud 10.6.0–10.13.0 (WebDAV auth bypass) | **0.4320** | 08-27-2026 | 08-30-2026 | Unknown | [ownCloud advisory](https://owncloud.com/security-advisories/webdav-api-authentication-bypass-using-pre-signed-urls/) |
| CVE-2022-0995 | Linux Kernel (local out-of-bounds write) | 0.0952 | 08-26-2026 | 09-09-2026 | Unknown | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2022-0995) |
| CVE-2015-3246 | Red Hat libuser (local race / passwd corruption) | 0.0880 | 08-26-2026 | 09-09-2026 | Unknown | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2015-3246) |
| CVE-2015-5287 | Red Hat ABRT (local privilege escalation; EoL) | 0.0496 | 08-26-2026 | 09-09-2026 | Unknown | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2015-5287) |
| CVE-2026-8452 | Citrix NetScaler ADC / Gateway (memory buffer / DoS) | 0.0161 | 08-26-2026 | 08-29-2026 | Unknown | [CTX696604](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX696604) |
| CVE-2026-66384 | JFrog Artifactory (Docker cache path traversal) | 0.0058 | 08-27-2026 | 09-10-2026 | Unknown | [JFrog advisories](https://docs.jfrog.com/releases/docs/jfrog-security-advisories) |
| CVE-2026-53362 | Linux Kernel IPv6 (local privilege escalation) | 0.0051 | 08-27-2026 | 08-30-2026 | Unknown | [Kernel commit](https://git.kernel.org/stable/c/14200d435af9a9eeb444f529fc2f689a236b7962) |

No new KEV additions on 08-31-2026 or 08-30-2026. Three added 08-27-2026: [CISA alert](https://www.cisa.gov/news-events/alerts/2026/08/27/cisa-adds-three-known-exploited-vulnerabilities-catalog). Six added 08-26-2026: [CISA alert](https://www.cisa.gov/news-events/alerts/2026/08/26/cisa-adds-six-known-exploited-vulnerabilities-catalog). One added 08-25-2026: [CISA alert](https://www.cisa.gov/news-events/alerts/2026/08/25/cisa-adds-one-known-exploited-vulnerability-catalog).

### Ransomware.live — recent victims
| Group | Sector | Country | Discovered | Source |
|---|---|---|---|---|
| — | — | — | — | [Ransomware.live](https://www.ransomware.live) (query failed today; 0 victims in packet) |

No leak-site or .onion links. Named pulse: unavailable — the ransomware.live API returned no rows on 08-31-2026. Do not treat the empty table as "ransomware stopped."

### CIRCL — highest-signal new items (30 pulled)
- **CVE-2025-10230 (EPSS 0.3965, 98.5th pct)** — Samba WINS hook command injection on an AD DC with `wins support` + `wins hook` set; default is off; upgrade Samba 4.23.2 / 4.22.5 / 4.21.9 or unset `wins hook` — [Samba advisory](https://www.samba.org/samba/security/CVE-2025-10230.html) · [CIRCL](https://vulnerability.circl.lu/advisories/cve-2025-10230)
- **CVE-2024-8309 (EPSS 0.1374, 96.2nd pct, CVSS 9.8)** — LangChain GraphCypherQAChain SQL/Cypher injection via prompt injection; upgrade `langchain-community` — [GHSA](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [Fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) · [huntr](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5)
- **CVE-2026-19410** — Google Cloud Build GitHub comment-control bypass (item 1); patched 06-24-2026, CVE published 08-31-2026 — [CIRCL](https://vulnerability.circl.lu/vuln/CVE-2026-19410) · [Google release notes](https://docs.cloud.google.com/build/docs/release-notes#August_24_2026)
- **CVE-2025-1889 (EPSS 0.0038, 31.1st pct)** — picklescan missed non-standard pickle extensions in ML model files; upgrade picklescan to **0.0.22 or later** — [GHSA](https://github.com/advisories/GHSA-769v-p64c-89pr) · [Sonatype](https://sites.google.com/sonatype.com/vulnerabilities/cve-2025-1889)
- **Apache Wicket cluster (published 08-31-2026):** CVE-2026-76982, CVE-2026-75802, CVE-2026-71378, CVE-2026-71257, CVE-2026-70449 — markup escaping / CSRF / upload-limit / file-read issues; if you ship a Wicket app, read the CIRCL pages today — [CVE-2026-70449](https://vulnerability.circl.lu/advisories/cve-2026-70449)
- **CVE-2026-82691 / CVE-2026-82690** — D-Link DNS-320L/327L/340L/345 CGI command injection (published 08-31-2026); if those NAS boxes are on your network, isolate and replace — [CVE-2026-82691](https://vulnerability.circl.lu/advisories/cve-2026-82691)

### IOCs (ThreatFox 8, URLhaus 6 — linked)
- **DanaBot C2 (confidence 100):** `142.11.244.124:443` — [Malpedia: DanaBot](https://malpedia.caad.fkie.fraunhofer.de/details/win.danabot) · [tria.ge](https://tria.ge/260831-n5mezs1djc/behavioral1)
- **Aisuru C2 (confidence 100):** `43.129.180.120:5555` — [Malpedia: Aisuru](https://malpedia.caad.fkie.fraunhofer.de/details/elf.aisuru)
- **ClearFake domains/URLs (confidence 90–100):** `earl.afghankabobgrill.com`, `www.groupe-elemen.com`, `https://raw.githubusercontent.com/Christa6547/davidrun/refs/heads/main/pull2395` — [Malpedia: ClearFake](https://malpedia.caad.fkie.fraunhofer.de/details/js.clearfake)
- **Shin webshell domains (confidence 50):** `nylefe.workers.dev`, `qylofihi.workers.dev` — [Malpedia: php.shin_webshell](https://malpedia.caad.fkie.fraunhofer.de/details/php.shin_webshell)
- **URLhaus malware distribution URLs:** `http://124.94.244.212:33038/Mozi.a` (offline) — [URLhaus 3910520](https://urlhaus.abuse.ch/url/3910520/) · `http://196.188.135.20:48063/i` — [URLhaus 3910519](https://urlhaus.abuse.ch/url/3910519/) · `http://103.203.210.102:46614/i` — [URLhaus 3910518](https://urlhaus.abuse.ch/url/3910518/) · `http://196.188.135.20:48063/bin.sh` — [URLhaus 3910517](https://urlhaus.abuse.ch/url/3910517/) · `http://175.148.87.144:40832/i` — [URLhaus 3910516](https://urlhaus.abuse.ch/url/3910516/) · `http://175.148.87.144:40832/bin.sh` — [URLhaus 3910515](https://urlhaus.abuse.ch/url/3910515/)

### CISA advisories
Newest item in the CISA RSS remains [Rockwell Automation OTTO Fleet Manager (ICSA-26-239-03)](https://www.cisa.gov/news-events/ics-advisories/icsa-26-239-03) (pubDate 08-13-2026) — outside the ~2-week window, not folded into today's top items.

---

*Compiled from public sources · 08-31-2026 · Sources: CISA KEV, CISA Advisories, Ransomware.live, CIRCL, FIRST EPSS, ThreatFox, URLhaus*
