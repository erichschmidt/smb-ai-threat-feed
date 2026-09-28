---
type: threat-feed-note
title: "Daily Threat Feed — 09-28-2026"
status: published
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-09-28
---

# Daily Threat Feed — 09-28-2026

**Reader promise:** 3-minute read. Headlines + Jargon buster carry the gist; the appendix has the raw signals. New here? The plain-language glossary lives at [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).

**How to read the scores:** EPSS is a 0–1 estimate of how likely a flaw is to be exploited in the next 30 days — higher means patch first (percentile = where it ranks vs all known flaws; 97th percentile = more likely than 97% of them). KEV = CISA confirms it's being actively exploited right now. CVSS = how severe it is if it works.

---

## 1. HIGH — Your "chat with your data" AI tool can be tricked into running database commands

**CVE-2024-8309 · LangChain GraphCypherQAChain · EPSS 0.1374 (96th percentile)**

**What broke:** LangChain's GraphCypherQAChain (a helper that turns a chat question into a graph-database query) has a SQL injection (tricking a program into running unauthorized database commands) flaw reachable through prompt injection (hiding instructions inside the data the AI reads). An attacker who can talk to the chatbot can make it read, change, or delete data it shouldn't touch, or knock the service offline.

**Why it matters to an SMB running AI tools:** LangChain sits behind a huge share of "chat with your business data" tools. If your chatbot queries a graph database and the query isn't locked down, the chat box becomes a database write — the exact thing a small business can't afford to happen to its customer records.

**What you do Monday:**
1. Find which langchain-community version your chatbot uses and upgrade past 0.2.5 (10 minutes).
2. If you use GraphCypherQAChain, restrict the database account it runs under to read-only, least-privilege.
3. Ask your AI vendor whether their chatbot surfaces a graph database and whether queries are validated.

**Sources:** [huntr bounty](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5) · [GHSA-45pg-36p6-83v9](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255)

---

## 2. CRITICAL — Your Citrix remote-access gateway has two actively-exploited holes — patch today

**CVE-2026-88771 + CVE-2026-88772 · Citrix NetScaler ADC/Gateway · KEV added 09-27-2026 · federal deadline 09-30-2026**

**What broke:** Two zero-day (previously unknown and unpatched) flaws in Citrix NetScaler — the appliance many businesses use as the VPN/front door for remote workers. One lets an unauthenticated (no login needed) attacker run arbitrary commands; the other allows remote code execution (RCE — an attacker can run their own code on your machine). CISA confirms both are being actively exploited globally right now.

**Why it matters to an SMB running AI tools:** NetScaler is the front door for remote access — and the same appliance often fronts the internal apps your AI tools read and write. A takeover here means an attacker is inside your network, with access to the same data sources your AI assistants pull from. If you run NetScaler, this is the highest-priority item today.

**What you do Monday:**
1. Apply Citrix's patch to NetScaler ADC and Gateway immediately (CTX697096) — plan for downtime.
2. If you can't patch instantly, run Citrix's published indicators-of-compromise checks in the NetScaler console to look for signs of exploitation (30 minutes).
3. If you find evidence of compromise, do forensic triage per CISA's BOD 26-04 guidance before reconnecting.

**Sources:** [CISA advisory](https://www.cisa.gov/news-events/alerts/2026/09/27/critical-zero-day-vulnerabilities-exploited-citrix-netscaler-adc-gateway) · [Citrix CTX697096](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697096) · [Citrix triage steps](https://support.citrix.com/external/article/CTX694799/steps-to-take-if-netscaler-adc-is-suspec.html)

---

## 3. HIGH — Your WordPress site can be hijacked by a single crafted request

**CVE-2026-87902 · WordPress Core · EPSS 0.1817 (97th percentile) · KEV added 09-25-2026 · federal deadline 09-28-2026**

**What broke:** A remote file inclusion (RFI — tricking a site into loading a file the attacker chose) flaw in WordPress Core. An unauthenticated attacker can make the page-template system load a chosen readable local .php file, which leads to remote code execution — full control of the site.

**Why it matters to an SMB running AI tools:** WordPress is the backbone of countless small-business sites — and often the place where marketing AI agents, chatbots, and content tools plug in. A hijacked site can serve malicious content to visitors and to the AI tools that read it.

**What you do Monday:**
1. Go to wp-admin → Updates and update WordPress Core to the patched release (10 minutes).
2. If you can't update immediately, check whether any custom theme or page-template code is exposed.

**Sources:** [GHSA-7hp8-65ch-5whp](https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-7hp8-65ch-5whp) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-87902)

---

## 4. HIGH — Your e-commerce storefront has a hole that needs no login and no click

**CVE-2026-71362 · Adobe Commerce / Magento · EPSS 0.8751 (99.75th percentile) · KEV added 09-24-2026 · federal deadline 09-27-2026**

**What broke:** An incorrect authorization (the product failed to check who's allowed to do what) flaw in Adobe Commerce and Magento. An attacker can gain elevated access to sensitive resources with no user interaction — the highest exploitation likelihood of anything in today's feed.

**Why it matters to an SMB running AI tools:** If you run an online store, this is your customer-data and order surface — and the data your AI marketing and support tools rely on. A compromise here puts customer records and order history at risk.

**What you do Monday:**
1. Apply Adobe's security patch APSB26-92 (10 minutes).
2. Check for any unexpected admin accounts or changes in your store's admin panel.

**Sources:** [Adobe APSB26-92](https://helpx.adobe.com/security/products/magento/apsb26-92.html) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-71362)

---

## 5. WATCH — AI model scanners can be fooled by a file's name — a "model" can be malware

**CVE-2025-1889 · picklescan · EPSS 0.004 (31st percentile)**

**What broke:** picklescan — a scanner meant to catch dangerous Python pickle files inside AI model downloads — only checks standard file extensions. An attacker can craft a malicious model using a non-standard extension and sail past the scan. Pickle (a Python data format) loading can run code, so an unsuspicious "model" file can be malware.

**Why it matters to an SMB running AI tools:** If your team downloads AI models or your pipeline scans them before use, a scanner that can be bypassed by renaming a file means untrusted model code can still run. Model files should be treated like unknown programs, not trusted documents.

**What you do Monday:**
1. Upgrade picklescan to 0.0.22 or later (5 minutes).
2. For any model you load, prefer the safetensors format or PyTorch's safe weights_only switch.

**Sources:** [GHSA-769v-p64c-89pr](https://github.com/advisories/GHSA-769v-p64c-89pr) · [Sonatype advisory](https://sites.google.com/sonatype.com/vulnerabilities/cve-2025-1889)

---

## Jargon buster

- **BOD 26-04:** A CISA directive requiring federal agencies to patch actively-exploited flaws by a set deadline — a good "how urgent is this" signal for everyone.
- **Botnet:** A network of hacked internet-connected devices (routers, cameras) that attackers control and use together.
- **Info-stealer:** Malware that harvests saved passwords, browser cookies, and wallet files and sends them to the attacker.
- **Remote file inclusion (RFI):** Tricking a server into loading a file the attacker chose — often a step toward running their own code.
- **Zero-day:** A flaw that was unknown (and unpatched) when it started being exploited — the most dangerous kind because there's no fix yet.
- GraphCypherQAChain, LangChain, SQL injection, prompt injection, graph database, NetScaler, RCE, unauthenticated, EPSS, KEV, CVSS, picklescan, pickle, safetensors — all in the [glossary](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).

## Appendix

### KEV table (ranked by EPSS)

| CVE | Product | Added | Federal deadline | EPSS (percentile) | Source |
|---|---|---|---|---|---|
| CVE-2026-71362 | Adobe Commerce/Magento | 09-24-2026 | 09-27-2026 | 0.8751 (99.8th) | [Adobe](https://helpx.adobe.com/security/products/magento/apsb26-92.html) |
| CVE-2026-93616 | Check Point Management | 09-22-2026 | 09-25-2026 | 0.1965 (97.3rd) | [Check Point](https://support.checkpoint.com/results/sk/sk1000171/) |
| CVE-2026-87902 | WordPress Core | 09-25-2026 | 09-28-2026 | 0.1817 (97.1st) | [GHSA](https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-7hp8-65ch-5whp) |
| CVE-2026-94127 | F5 BIG-IP APM | 09-22-2026 | 09-25-2026 | 0.0223 (82.0th) | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-94127) |
| CVE-2026-65660 | Microsoft SharePoint | 09-25-2026 | 09-28-2026 | 0.0210 (81.0th) | [Microsoft](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-65660) |
| CVE-2026-93952 | Arista VeloCloud | 09-22-2026 | 09-25-2026 | 0.0106 (63.2nd) | [Arista](https://www.arista.com/en/support/advisories-notices/security-advisory/24765-security-advisory-0183) |
| CVE-2026-67279 | MikroTik RouterOS | 09-25-2026 | 09-28-2026 | 0.0103 (62.2nd) | [MikroTik](https://mikrotik.com/supportsec/september-2026-vulnerability/) |
| CVE-2026-85102 | Check Point Gateway | 09-22-2026 | 09-25-2026 | 0.0099 (61.0th) | [Check Point](https://support.checkpoint.com/results/sk/sk1000117) |
| CVE-2026-5430 | WSO2 API platform | 09-24-2026 | 09-27-2026 | 0.0059 (46.0th) | [WSO2](https://security.docs.wso2.com/en/latest/security-announcements/security-advisories/2026/WSO2-2026-5328/) |
| CVE-2026-88772 | Citrix NetScaler | 09-27-2026 | 09-30-2026 | n/a | [Citrix](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697096) |
| CVE-2026-88771 | Citrix NetScaler | 09-27-2026 | 09-30-2026 | n/a | [Citrix](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697096) |

### Ransomware victims (last 24h)

| Group | Sector | Country | Source |
|---|---|---|---|
| emperador | Manufacturing | SE | [Ransomware.live](https://www.ransomware.live) |
| emperador | Hospitality | — | [Ransomware.live](https://www.ransomware.live) |
| Panzer | Healthcare | — | [Ransomware.live](https://www.ransomware.live) |
| incransom | Government & Defense | US | [Ransomware.live](https://www.ransomware.live) |
| incransom | IT consulting | US | [Ransomware.live](https://www.ransomware.live) |
| Panzer | Professional Services | FR | [Ransomware.live](https://www.ransomware.live) |
| qilin | Technology | CA / ES | [Ransomware.live](https://www.ransomware.live) |

Sector pulse: healthcare, government/defense, and manufacturing victims again today — the same sectors that keep appearing. If you operate in one, verify your backups and test a restore.

### CIRCL high-EPSS

- **CVE-2024-8309** (LangChain GraphCypherQAChain) — EPSS 0.1374 (96th) — [GHSA](https://github.com/advisories/GHSA-45pg-36p6-83v9)
- **CVE-2025-1889** (picklescan) — EPSS 0.004 (31st) — [GHSA](https://github.com/advisories/GHSA-769v-p64c-89pr)

### IOC sample (last 24h)

- **Mozi botnet** (router/camera botnet): http://202.47.49.0:42751/Mozi.m · http://180.252.82.152:40061/Mozi.m · http://101.108.97.215:48064/Mozi.m — [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/elf.mozi)
- **Remcos RAT**: 180.93.236.78:80 — [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/win.remcos)
- **Vidar info-stealer**: https://accountz.msdos.ru/login · tr.v-panel.asia — [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/win.vidar)
- **AMOS** (macOS stealer): 193.233.210.226:80 — [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/osx.amos)
- **KongTuke** (JS): ssmpson.top — [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/js.kongtuke)
- **Fake browser installers** (URLhaus): https://moniquejhingon.com/Chrome.exe · https://moniquejhingon.com/google.exe — [URLhaus](https://urlhaus.abuse.ch/url/3924352/)

---

*Compiled from public sources · 09-28-2026*