---
type: threat-feed-note
title: "Threat Feed — 09-30-2026"
status: published
date: 09-30-2026
tags: [threat-feed, daily, smb-ai-lens]
---

# Threat Feed — 09-30-2026

*Threat intel for people deploying AI and automation in small businesses.* Every headline is written to stand alone; every term is defined in the [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md). This is the ~3-minute read.

## How to read the scores

- **KEV** (CISA's Known Exploited Vulnerabilities) = "this is being exploited for real right now, not theoretical." If a flaw is on this list, patch it.
- **EPSS** = a 0–1 score estimating how likely a flaw is to be exploited in the next 30 days (higher = patch first), plus a percentile showing where it ranks against every known vulnerability. Today's example: **EPSS 0.875, 99.75th percentile** = more likely to be exploited than 99.75% of all known vulnerabilities — patch that one first.
- **CVSS** = a 0–10 severity score. **CVSS 9.8/10 is critical** — typically exploitable from anywhere with no login.
- **BOD 26-04 deadline** = the date CISA requires federal agencies to patch; a useful urgency anchor for everyone.

---

## Items

### 1. HIGH — Your AI "chat with your data" tool can still be tricked into running its own database commands — confirm you've patched

**CVE-2024-8309** (LangChain `GraphCypherQAChain`) · CVSS 9.8/10 (critical) · on-lens

**Sources:** [huntr bounty](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5) · [upstream fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) · [GHSA-45pg-36p6-83v9 advisory](https://github.com/advisories/GHSA-45pg-36p6-83v9)

**What broke.** LangChain is one of the most-used open-source frameworks for building AI apps — chatbots and "ask your documents" assistants. Its `GraphCypherQAChain` helper turns a chat question into a query against a graph database, and a bug in how it builds that query lets a carefully-worded prompt inject its own database commands — an **SQL injection** (tricking software into running database commands the attacker chose) triggered purely through chat text. No login needed. This was flagged earlier this week; it is the only on-lens finding in today's reading, so if your AI stack runs LangChain, this is the check to prioritize.

**Why it matters to an SMB running AI tools.** If you run any LangChain-based assistant that interviews your business data — even through a vendor's product — the chatbot's own data source is the attack surface. An attacker doesn't need to hack your website; they just phrase a question that smuggles a database command past the AI. Worst case it silently copies data or shuts the database down. This is the classic supply-chain warning: an AI framework you don't maintain can open the apps built on it.

**What you do Monday** (20–30 minutes).
1. Check your AI stack for `langchain-community` at or below **0.2.5**: `pip list | grep langchain`
2. Upgrade and redeploy: `pip install -U langchain-community`
3. If you can't patch today, restrict `GraphCypherQAChain` to read-only queries and connect the database with a least-privilege account — never let the AI connect as a database admin.

> **Conceptual attacker view (no exploit detail):** scan path → a user with the least amount of access can reach the chat input; injection point → the natural-language question, which becomes database query text; observables → unexpected or malformed queries hitting the graph database, unusual read volume, or query errors in app logs. Detection rule of thumb: alert on database queries that originate from the AI service account and contain syntax typical of an injected command, and cap that account's rights so the blast radius stays small.

---

### 2. CRITICAL — Adobe Commerce / Magento online stores have the single most-exploitable flaw in the catalog this week — a bypass that needs no login or interaction

**CVE-2026-71362** (Adobe Commerce & Magento) · EPSS 0.875 · p99.75 · in CISA KEV, added 09-24-2026

**Sources:** [Adobe APSB26-92 advisory](https://helpx.adobe.com/security/products/magento/apsb26-92.html) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-71362)

**What broke.** Adobe Commerce and Magento are e-commerce platforms many small stores run on. This flaw is an **incorrect authorization** issue — a check that lets someone do things they were never granted permission to do — letting an attacker reach sensitive resources with elevated access and **no user interaction** (no click, no login). It tops today's whole catalog on exploitation likelihood: EPSS 0.875 means roughly 87.5% odds of being exploited in the next 30 days, and the 99.75th percentile means it's more likely to be exploited than 99.75% of all known vulnerabilities. CISA added it to KEV (active-exploitation confirmed) on 09-24; federal agencies have until 09-27 to patch.

**Why it matters to an SMB running AI tools.** To be plain: this is not an AI-tool bug. It matters to you because small storefronts increasingly bolt on AI — product-recommendation widgets, support chatbots, review assistants — and the customer and payment data those AI tools read sits behind the same store. Break the store's authorization and you reach the data layer underneath. Patch the storefront and you protect the data source the AI reads, even though Adobe didn't break the AI itself.

**What you do Monday** (30–45 minutes).
1. Confirm whether you run Adobe Commerce / Magento (check your hosting panel or ask your platform provider).
2. Apply Adobe's [APSB26-92](https://helpx.adobe.com/security/products/magento/apsb26-92.html) patch, or ask your vendor: "Have you applied the Adobe Security Bulletin APSB26-92 patch?"
3. After patching, tighten store account roles to least-privilege so any compromised login can't reach admin functions.

---

### 3. CRITICAL — A hole in how iPhones and Macs draw images is being attacked right now — update every Apple device

**CVE-2026-86950** (Apple iOS, macOS, iPadOS — CoreGraphics) · in CISA KEV, added 09-29-2026

**Sources:** [Apple support 149226](https://support.apple.com/en-us/149226) · [Apple support 149228](https://support.apple.com/en-us/149228)

**What broke.** Apple's iOS (iPhone), macOS (Mac), and iPadOS all share a bug in CoreGraphics — Apple's graphics engine that draws on-screen images. It's an **out-of-bounds write** (a memory bug where software writes past the space it reserved for data, which attackers can abuse to run their own code) that can lead to arbitrary code execution — meaning an attacker can run their own software on the device. CISA added it to KEV on 09-29, confirming active exploitation is happening for real. Federal agencies must patch by 10-02.

**Why it matters to an SMB running AI tools.** This isn't about your AI stack — it's the devices your people actually use every day: the phones and laptops staff use to reach AI assistants, company email, VPNs, and corporate apps. Wherever a staff member carries their work life on an iPhone or Mac, a device-takeover path is a path into your network. Consumer-grade patching is exactly the "Monday" work that matters.

**What you do Monday** (10–20 minutes, per device).
1. On each iPhone/iPad: **Settings → General → Software Update** → install the available update.
2. On each Mac: **System Settings (or System Preferences) → General → Software Update** → install.
3. If you manage devices, push the update through your device-management (MDM) console so unmanaged personal devices aren't carrying company access.

---

### 4. CRITICAL — The Citrix remote-access gateway holes attacked worldwide are still open and the federal patch deadline is today

**CVE-2026-88771 / CVE-2026-88772** (Citrix NetScaler ADC & Gateway) · zero-day · in CISA KEV, added 09-27-2026

**Sources:** [Citrix Security Bulletin CTX697096](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697096) · [Steps to take if NetScaler is compromised](https://support.citrix.com/external/article/CTX694799/steps-to-take-if-netscaler-adc-is-suspec.html)

**What broke.** Still active from this week's bulletin: Citrix NetScaler ADC and Gateway — the appliance many businesses use as their **VPN** (the encrypted "tunnel" remote workers log into from home) and website front door — has two critical, already-exploited holes. One lets an unauthenticated attacker (no login) execute arbitrary commands; the other is a memory-buffer bug that can lead to remote code execution. CISA's KEV lists both, and the federal patch deadline is **today, 09-30**. If you haven't acted on this week's advisory yet, this is the day.

**Why it matters to an SMB running AI tools.** This is the front door your staff and your AI/automation services use to reach the office network. An actively-exploited remote-access gateway means an attacker walks in through the same tunnel your people use and lands on the network that also runs your document stores, Copilot-style data sources, and automation. It's not an AI bug, but it puts the AI's home network at risk.

**What you do Monday** (1–2 hours; plan for brief downtime).
1. If you haven't already, run the indicators of compromise Citrix published (via NetScaler Console) to check whether you were hit *before* patching — patching can erase forensic evidence.
2. Apply Citrix's update for these CVEs per [CTX697096](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697096).
3. If patching is delayed, keep NetScaler off the public internet where you can and watch logs for the published IOCs afterward.

---

### 5. HIGH — WordPress sites can be remotely controlled through a theme-file trick — update the core

**CVE-2026-87902** (WordPress Core) · EPSS 0.198 · p97.32 · in CISA KEV, added 09-25-2026

**Sources:** [WordPress GHSA-7hp8-65ch-5whp advisory](https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-7hp8-65ch-5whp) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-87902)

**What broke.** WordPress Core has a **remote file inclusion** flaw — a trick where an attacker gets a server to load a file they chose — that lets an unauthenticated attacker make WordPress's page-template loader include a chosen readable local `.php` file outside the allowed theme folders. That can lead to remote code execution (running their own code on your server). It's the second-highest exploitation likelihood in today's KEV list at EPSS 0.198 (97th percentile), with CISA confirming active exploitation on 09-25.

**Why it matters to an SMB running AI tools.** Millions of small businesses run WordPress, and plenty bolt on AI — chatbots, AI-written content, booking and lead automations. A take-over of the WordPress server means an attacker controls the host that runs your site and the automations touching it. An actively-exploited CMS hole is a "patch the core now" event.

**What you do Monday** (15–20 minutes).
1. Log in to WordPress admin → **Updates** → apply the latest core update (and any pending security patches).
2. After updating, scan for unexpected plugins or users in **Users** and **Plugins**, since compromise often plants a backdoor.
3. If you use a managed host, ask: "Is my WordPress core up to date against CVE-2026-87902?"

---

## Jargon buster

Plain-language definitions for terms used in today's note. Full living glossary: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).

- **Authorization bypass:** A flaw that lets someone who *is* in the system do things they were never granted permission to do — they walk through the wrong door.
- **BOD 26-04:** A CISA directive requiring federal agencies to patch actively-exploited flaws by a set deadline — a good urgency signal for everyone.
- **CoreGraphics:** Apple's graphics engine that renders on-screen images. A flaw here can affect iPhones, Macs, and iPads at once.
- **CVSS:** A 0–10 severity score for a flaw. 9.8/10 = critical — typically exploitable remotely with no login.
- **EPSS:** A 0–1 score estimating how likely a flaw is to be exploited in the next 30 days; higher = patch first. Percentile = where it ranks vs every known vulnerability.
- **KEV (Known Exploited Vulnerabilities) catalog:** CISA's list of vulnerabilities being actively exploited right now. On the list = not theoretical, patch it.
- **LangChain:** A popular open-source framework for building AI applications (chatbots, "chat with your data"). Flaws in it affect lots of AI tools at once.
- **Out-of-bounds write:** A memory bug where software writes past the space it reserved for data. Attackers use it to crash a service or run their own code.
- **Remote file inclusion (RFI):** Tricking a server into loading a file the attacker chose — often a step toward running their own code.
- **RCE (Remote Code Execution):** An attacker can run their own code on your machine from anywhere. Full control.
- **SQL injection:** Tricking software into running database commands the attacker chose, via a crafted input (or prompt).
- **Unauthenticated (attacker):** Someone with no login credentials, operating from anywhere.
- **VPN (Virtual Private Network):** The encrypted "tunnel" remote workers use to reach the office network.

---

## Appendix

### Actively-exploited vulnerabilities added to CISA KEV in the last 7 days (ranked by EPSS)

Confidence + likelihood: highest EPSS / percentile = patch first. **KEV already means "real right now"; EPSS tells you the order.**

| Rank | CVE | Product | EPSS (percentile) | CISA confirmed | Federal deadline | Ransomware use | Source |
|---|---|---|---|---|---|---|---|
| 1 | CVE-2026-71362 | Adobe Commerce / Magento (authorization bypass) | 0.875 | 09-24-2026 | 09-27-2026 | Unknown | [Adobe APSB26-92](https://helpx.adobe.com/security/products/magento/apsb26-92.html) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-71362) |
| 2 | CVE-2026-87902 | WordPress Core (remote file inclusion → RCE) | 0.198 (p97.32) | 09-25-2026 | 09-28-2026 | Unknown | [GHSA-7hp8-65ch-5whp](https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-7hp8-65ch-5whp) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-87902) |
| 3 | CVE-2026-65660 | Microsoft SharePoint (code injection) | 0.021 (p80.98) | 09-25-2026 | 09-28-2026 | Unknown | [MSRC](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-65660) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-65660) |
| 4 | CVE-2026-88772 | Citrix NetScaler (RCE/DoS) | 0.013 (p69.33) | 09-27-2026 | 09-30-2026 | Unknown | [Citrix CTX697096](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697096) |
| 5 | CVE-2026-88771 | Citrix NetScaler (RCE, no login) | 0.011 (p63.29) | 09-27-2026 | 09-30-2026 | Unknown | [Citrix CTX697096](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697096) |
| 6 | CVE-2026-67279 | MikroTik RouterOS (unauthenticated exec) | 0.010 (p62.21) | 09-25-2026 | 09-28-2026 | Unknown | [MikroTik](https://mikrotik.com/supportsec/september-2026-vulnerability/) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-67279) |
| 7 | CVE-2026-86950 | Apple iOS/macOS/iPadOS (CoreGraphics OOB write) | 0.008 (p55.30) | 09-29-2026 | 10-02-2026 | Unknown | [Apple 149226](https://support.apple.com/en-us/149226) |
| 8 | CVE-2026-5430 | WSO2 API products (path traversal → unrestricted upload → RCE) | 0.006 (p46.01) | 09-24-2026 | 09-27-2026 | Unknown | [WSO2 advisory](https://security.docs.wso2.com/en/latest/security-announcements/security-advisories/2026/WSO2-2026-5328/) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-5430) |

- **CISA confirmed** = the date CISA confirmed active exploitation (KEV = real right now, not theoretical).
- **Federal deadline** = the date CISA requires federal agencies to patch (BOD 26-04). Treat as "this is urgent."
- **Ransomware use** = "Known to be used in ransomware campaigns: Yes / Unknown." All unknowns today — still patch, but no ransomware-gang signal attached.

**SMB Monday watch:** besides the items above, patch **Microsoft SharePoint** (about the same likelihood as the Citrix holes; it's the document library Copilot-style tools often read — a hole here is a hole in an AI data source), **MikroTik RouterOS** if you run MikroTik hardware (the router is the office internet front door), and **WSO2 API platform** if you run it — its path traversal sits in an integration layer right next to the data your automation and AI tools read. Note: CISA also published a new **MikroTik ICS advisory** (ICSA-26-272-06, CVE-2026-84411, RouterOS below 7.24, CVSS 9.8) — another reason to update that router firmware.

### Ransomware claims (Ransomware.live, 09-30-2026)

Today's sector pulse is dominated by **Storm**, which posted a batch of small US victims across professional services (a NY-area facility/janitorial firm, a property-management company), hospitality (a property-management firm), and a well-known New York studio. Also this reading: **m3rx** claimed a Polish technology/software firm, **Wallstreet** hit a community hospital in Illinois (healthcare), **thegentlemen** claimed a Puerto Rico pulmonary-services group, **interlock** listed a Utah defense contractor, and **chaos** posted a Taiwan manufacturer.

[Source: ransomware.live](https://www.ransomware.live)

**SMB takeaway:** the mix confirms the standing pattern — small facility-services, property-management, and hospitality firms are squarely in the crosshairs, alongside healthcare (two claims this reading). These are the businesses whose downtime hurts most and whose backups aren't always tested. Offline, tested backups and multi-factor authentication on every remote entry remain the work that matters — not the victims' failing, but the criminals' volume.

### Notable vulnerabilities (CIRCL)

Two AI-relevant records appeared in today's reading; both were already covered in this week's brief, so they're flagged here for continuity rather than re-dumped:

- **CVE-2024-8309** — LangChain `GraphCypherQAChain` SQL injection via prompt injection (see Item 1). [GHSA-45pg-36p6-83v9](https://github.com/advisories/GHSA-45pg-36p6-83v9)
- **CVE-2025-1889** — picklescan model-scan bypass (a malicious model saved with a non-standard file extension sails past the scanner). If your pipeline loads downloaded models, confirm this week's `picklescan` upgrade to **0.0.22+** landed. [GHSA-769v-p64c-89pr](https://github.com/advisories/GHSA-769v-p64c-89pr)

### Sample IOCs (seen today — block and hunt these; don't visit them)

ThreatFox (abuse.ch), 100% confidence unless noted:
- **Mirai** botnet samples (multiple `sha256` hashes seen 09-30-2026) — [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/elf.mirai)
- **Bashlite** botnet sample — [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/elf.bashlite)
- **ClearFake** (fake-update / drive-by) domain: `cognitiveenhancementcentre.ch` (90%) — [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/js.clearfake)

URLhaus (abuse.ch), online at reading time — likely malware-download / botnet hosts:
- `http://94.154.43.28/run.sh` — [URLhaus](https://urlhaus.abuse.ch/url/3925538/)
- `https://tk-1464303226.cos.ap-guangzhou.myqcloud.com/tk.y` — [URLhaus](https://urlhaus.abuse.ch/url/3925537/)
- `http://113.229.54.12:38270/bin.sh` — [URLhaus](https://urlhaus.abuse.ch/url/3925533/)

---

*Compiled from public sources · 09-30-2026*
