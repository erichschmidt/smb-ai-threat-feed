---
type: threat-feed-note
title: "Threat Feed — 09-26-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
date: 09-26-2026
---

# Threat Feed — 09-26-2026

*Threat intel for people deploying AI and automation in small businesses. 3-minute read: skim the headlines, then the [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md) if a term is new.*

## How to read the scores
- **EPSS:** a 0–1 score estimating how likely a flaw is to be exploited in the next 30 days; higher = patch first. The percentile (e.g. "96th") is how that score ranks against every other known vulnerability.
- **CISA KEV:** a flaw on this list is being actively exploited right now (not theoretical), and the federal deadline is the "patch by" anchor.
- **CVSS:** a 0–10 severity score for a flaw — 9.8/10 means critical, typically exploitable remotely with no login.

---

## Items

### 1. HIGH — Your "chat with our data" AI tool can be tricked into running raw database commands
**CVE-2024-8309 · GraphCypherQAChain (langchain-community ≤ 0.2.5) · CVSS 9.8/10 · EPSS 0.1374 (96th percentile) · still actively exploited**

**What broke** — A component of LangChain, the most popular framework for building AI chatbots, lets a cleverly phrased user question smuggle in a raw database command. Specifically, `GraphCypherQAChain` — the part that turns a plain-English question into a database query — is vulnerable to SQL injection (typing malicious database commands into a prompt so the app runs unauthorized queries) via a prompt-injection trick. The database query becomes a door for an attacker to read, change, or delete records the chat was never meant to touch. This remains one of the highest-likelihood exploited flaws in the AI stack today.

**Why it matters to an SMB running AI tools** — If you've built or bought a "chat with our CRM/inventory/support data" feature, and it sits on a graph database or queries business records, this is the plumbing under it. An attacker who can reach your chat box can reach your data. For every SMB running LLM apps over their own data, this is the class of bug that turns a helpful assistant into a data exfiltration path.

*Attacker view (conceptual): scan for exposed chatbot/chat-with-data endpoints → probe with a question that includes a database command → observe whether the chat runs it and returns results. Defender observables: abnormal database queries or a spike in records read, especially from the chat service's credentials.*

**What you do Monday**
1. Update `langchain-community` to a version newer than 0.2.5 (`pip install --upgrade langchain-community`, then restart your app). ~10 minutes.
2. Give the database account that the chat tool uses read-only access. It should never be able to change or delete rows. ~20 minutes.
3. If you used a no-code builder with LLM chat over your data, check its release notes or ask the vendor whether the fix landed — then upgrade. ~15 minutes.

**Sources:** [Huntr bounty](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5) · [GitHub advisory GHSA-45pg-36p6-83v9](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [Fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255)

---

### 2. HIGH — Microsoft SharePoint lets an approved user run code — and it's the folder Copilot reads
**CVE-2026-65660 · Microsoft SharePoint · added to CISA KEV 09-25-2026 · EPSS 0.0122 (67th percentile)**

**What broke** — Microsoft SharePoint has a code-injection flaw (a bug that lets attacker-controlled code run as part of the application) that an *authorized* user — someone who legitimately has access to the site — can use to execute code over the network. CISA added it to its actively-exploited list today/yesterday, meaning real-world attackers are already using it. The vendor previously labeled it lower-severity spoofing; researchers found it goes deeper, enabling remote code execution (RCE — an attacker runs their own code on your machine).

**Why it matters to an SMB running AI tools** — SharePoint is the library Copilot and other "chat with your files" tools read to answer questions about your business. It is often the data source behind an AI assistant — which makes it both a target and a springboard: an attacker who compromises SharePoint can both steal the documents your AI summarizes and pivot to other internal systems from a legitimate-looking account. The bar ("authorized user only") is lower than it sounds because inside a company many people have some SharePoint access.

**What you do Monday**
1. Install the Microsoft patch from Windows Update / the MSRC Update Guide. Treat any SharePoint you run (or your Microsoft 365 tenant) as exposed. ~30 minutes.
2. Audit which accounts have write access to SharePoint sites that feed your AI/tools, and trim to the people who actually need it. ~30 minutes.
3. If an online Microsoft 365 tenant, confirm "instant updates" / patch status is current for SharePoint on the admin portal before assuming you're covered. ~10 minutes.

**Sources:** [CVE record (cve.org)](https://www.cve.org/CVERecord?id=CVE-2026-65660) · [Microsoft MSRC Update Guide](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-65660) · [NVD CVE-2026-65660](https://nvd.nist.gov/vuln/detail/CVE-2026-65660) · [CISA advisory](https://www.cisa.gov/news-events/alerts/2026/09/25/cisa-adds-two-known-exploited-vulnerabilities-catalog)

---

### 3. HIGH — Your MikroTik router is being attacked right now — patch by 09-28
**CVE-2026-67279 · MikroTik RouterOS · added to CISA KEV 09-25-2026 · due 09-28-2026 · EPSS 0.0071 (52nd percentile)**

**What broke** — A flaw in MikroTik RouterOS (the operating system inside tens of thousands of office and home routers) lets an unauthenticated remote attacker take control over an SSH connection before the user ever logs in. European national CERTs and MikroTik themselves have confirmed these routers are being actively targeted and compromised in the wild, sometimes in ways that survive a normal update — so responding to this one means an update plus a check for tampering.

**Why it matters to an SMB running AI tools** — Everything your AI tools send and receive — the API calls, the model queries, the synced business data — travels through your office router. A router that's been silently taken over can redirect traffic, intercept credentials, and watch every request, including the traffic to your AI providers. This is a patch-the-front-door emergency.

**What you do Monday**
1. Update RouterOS via Winbox/SSH/web to a fixed release: **7.24.2**, 7.23.4, or 6.49.21. US federal deadline is **09-28-2026**. ~30–60 minutes.
2. After updating, look for signs of compromise — unexpected admin user accounts, config changes, or devices "flagged" in the new boot log. Go to the manufacturer/security guidance and follow the recommended checks. ~15 minutes.
3. If internet access exposes the router's admin/SSH port to the outside world, close it now (manage the router only from inside the office network). ~10 minutes.

**Sources:** [MikroTik September 2026 advisory](https://mikrotik.com/supportsec/september-2026-vulnerability/) · [CERT Polska warning](https://cert.pl/en/posts/2026/09/vulnerabilities-in-mikrotik-routeros-actively-exploited/) · [NVD CVE-2026-67279](https://nvd.nist.gov/vuln/detail/CVE-2026-67279) · [CISA KEV catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

---

### 4. WATCH — Your API integration platform has a file-path trick that leads to full server control
**CVE-2026-5430 · WSO2 API Manager, API Control Plane, Traffic Manager, Universal Gateway · added to CISA KEV 09-24-2026 · EPSS 0.0037 (29th percentile)**

**What broke** — WSO2's API products have a path-traversal flaw (a `../` trick in a file path to reach files that should be out of reach) combined with an unrestricted file upload, and together they can lead to remote code execution (RCE — an attacker runs their own code on your machine, i.e. full control). CISA confirms this is being actively exploited.

**Why it matters to an SMB running AI tools** — WSO2 API Manager is the software many teams use to ferry data between their apps, SaaS tools, and automation pipelines — exactly the kind of integration layer an SMB leans on to stitch AI features into the business. A hole in the API gateway is a hole in every connection it manages, including the data your AI tools read and write.

**What you do Monday**
1. Apply the vendor patch. The US federal deadline is **09-27-2026** — treat this as urgent, not "someday." ~30–60 minutes plus a maintenance window.
2. If you don't know whether you run any WSO2 products, search your server list for "WSO2" / "API Manager" before assuming you're unaffected. ~10 minutes.

**Sources:** [WSO2 security advisory WSO2-2026-5328](https://security.docs.wso2.com/en/latest/security-announcements/security-advisories/2026/WSO2-2026-5328/) · [NVD CVE-2026-5430](https://nvd.nist.gov/vuln/detail/CVE-2026-5430)

---

## Jargon buster
- **API:** the software bridge one program uses to talk to another — how your apps and automation exchange data.
- **Code injection:** tricking software into running attacker-supplied commands as if they were part of the program.
- **CVSS:** a 0–10 severity score for a flaw; 9.8/10 is critical, typically exploitable remotely with no login.
- **GraphCypherQAChain:** LangChain's helper that turns a chat question into a graph-database query.
- **Path traversal:** a trick where an attacker types `../` (or similar) in a file path to reach files they shouldn't, which in a server product can become full takeover.
- **Prompt injection:** tricking an AI by putting instructions inside the data it reads — the AI follows the attacker's instructions instead of the user's.
- **RCE (remote code execution):** an attacker can run their own code on your machine from anywhere — full control.
- **SQL injection:** typing malicious database commands into an input box or prompt so the app runs unauthorized queries.
- **SSH:** a standard encrypted way to log into a server or device and run commands on it.

*(See the growing [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md) for the full list.)*

---

## Appendix

### CISA KEV — actively exploited (ranked by EPSS)
| CVE | Product | EPSS (percentile) | CISA added | Federal deadline | Source |
|---|---|---|---|---|---|
| CVE-2026-93616 | Check Point Multiple Products | 0.0242 (83rd) | 09-22-2026 | 09-25-2026 | [Check Point](https://support.checkpoint.com/results/sk/sk1000171/) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-93616) |
| CVE-2026-71362 | Adobe Commerce / Magento | 0.0233 (83rd) | 09-24-2026 | 09-27-2026 | [Adobe](https://helpx.adobe.com/security/products/magento/apsb26-92.html) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-71362) |
| CVE-2026-94127 | F5 BIG-IP APM | 0.0129 (69th) | 09-22-2026 | 09-25-2026 | [F5](https://my.f5.com/manage/s/article/K000162605) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-94127) |
| CVE-2026-7273 | Zyxel GS1900 Series Switches | 0.0129 (69th) | 09-21-2026 | 09-24-2026 | [Zyxel](https://www.zyxel.com/global/en/support/security-advisories/zyxel-security-advisory-for-stack-based-buffer-overflow-vulnerability-in-gs1900-series-switches-06-16-2026) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-7273) |
| CVE-2026-65660 | Microsoft SharePoint | 0.0122 (67th) | 09-25-2026 | — | [Microsoft](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-65660) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-65660) |
| CVE-2026-85102 | Check Point (VPN) | 0.0099 (61st) | 09-22-2026 | 09-25-2026 | [Check Point](https://support.checkpoint.com/results/sk/sk1000117) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-85102) |
| CVE-2026-93952 | Arista VeloCloud Orchestrator | 0.0089 (58th) | 09-22-2026 | 09-25-2026 | [Arista](https://www.arista.com/en/support/advisories-notices/security-advisory/24765-security-advisory-0183) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-93952) |
| CVE-2026-67279 | MikroTik RouterOS | 0.0071 (52nd) | 09-25-2026 | 09-28-2026 | [MikroTik](https://mikrotik.com/supportsec/september-2026-vulnerability/) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-67279) |
| CVE-2026-5430 | WSO2 API Platform | 0.0037 (29th) | 09-24-2026 | 09-27-2026 | [WSO2](https://security.docs.wso2.com/en/latest/security-announcements/security-advisories/2026/WSO2-2026-5328/) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-5430) |

### Notable CIRCL findings
- **CVE-2024-8309** — GraphCypherQAChain (LangChain) SQL injection via prompt injection. EPSS 0.1374 (96th percentile), CVSS 9.8. **[Source: Huntr](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5)**
- **CVE-2025-1889** — picklescan skips non-standard pickle file extensions. EPSS 0.0039. **[Source: GitHub](https://github.com/advisories/GHSA-769v-p64c-89pr)**

### Ransomware sector pulse
- No new ransomware victim disclosures were returned by the source today (data feed unavailable for this run). No ransomware-sector signal to report.

### IOC sample (ThreatFox / URLhaus)
- **Remus RAT (remote-access trojan)** — C2 `137.184.108.14:3546`. [Source: Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/win.remus)
- **Shin webshell** — hosting domains `sapphiremallory.workers.dev`, `jh10s83825.workers.dev`. [Source: Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/php.shin_webshell)
- **Mozi botnet** — distribution servers `103.213.112.230`, `223.123.124.122`, `153.117.41.26`, `203.128.24.233`, `111.92.157.232`. [Source: Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/elf.mozi)
- **URLhaus (recently reported malicious URLs)** — `163.142.94.23:36474/bin.sh`, `187.45.95.254:48143/bin.sh`, `221.15.9.146:46601/bin.sh` and two more. [Source: URLhaus](https://urlhaus.abuse.ch/url/3922588/)

*IOCs are block-and-hunt signals, not things to visit.*

---

*Compiled from public sources · 09-26-2026*
