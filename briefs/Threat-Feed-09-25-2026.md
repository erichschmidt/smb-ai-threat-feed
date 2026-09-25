---
type: threat-feed-note
title: "Threat Feed — 09-25-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
date: 09-25-2026
---

# Threat Feed — 09-25-2026

*Threat intel for people deploying AI and automation in small businesses. 3-minute read: skim the headlines, then the [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md) if a term is new.*

## How to read the scores
- **EPSS:** a 0–1 score estimating how likely a flaw is to be exploited in the next 30 days; higher = patch first. The percentile (e.g. "83rd") is how that score ranks against every other known vulnerability.
- **CISA KEV:** a flaw on this list is being actively exploited right now (not theoretical), and the federal deadline is the "patch by" anchor.
- **CVSS:** a 0–10 severity score for a flaw — 9.8/10 means critical, typically exploitable remotely with no login.

---

## Items

### 1. HIGH — Your "chat with our data" AI tool can be tricked into running raw database commands
**CVE-2024-8309 · GraphCypherQAChain (langchain-community ≤ 0.2.5) · CVSS 9.8/10 · EPSS 0.1374 (96th percentile) · added to CISA KEV 09-24-2026**

**What broke** — A component of LangChain, the most popular framework for building AI chatbots, lets a cleverly phrased user question smuggle in a raw database command. Specifically, `GraphCypherQAChain` — the part that turns a plain-English question into a database query — is vulnerable to SQL injection (typing malicious database commands into a prompt so the app runs unauthorized queries) via a prompt-injection trick. The database query becomes a door for an attacker to read, change, or delete records the chat was never meant to touch. This is being actively exploited.

**Why it matters to an SMB running AI tools** — If you've built or bought a "chat with our CRM/inventory/support data" feature, and it sits on a graph database or queries business records, this is the plumbing under it. An attacker who can reach your chat box can reach your data. For every SMB running LLM apps over their own data, this is the class of bug that turns a helpful assistant into a data exfiltration path.

*Attacker view (conceptual): scan for exposed chatbot/chat-with-data endpoints → probe with a question that includes a database command → observe whether the chat runs it and returns results. Defender observables: abnormal database queries or a spike in records read, especially from the chat service's credentials.*

**What you do Monday**
1. Update `langchain-community` to a version newer than 0.2.5 (`pip install --upgrade langchain-community`, then restart your app). ~10 minutes.
2. Give the database account that the chat tool uses read-only access. It should never be able to change or delete rows. ~20 minutes.
3. If you used a no-code builder with LLM chat over your data, check its release notes or ask the vendor whether the fix landed — then upgrade. ~15 minutes.

**Sources:** [Huntr bounty](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5) · [GitHub advisory GHSA-45pg-36p6-83v9](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [Fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255)

---

### 2. WATCH — AI model scanner can be bypassed by renaming the malicious file
**CVE-2025-1889 · picklescan < 0.0.22 · CVSS 9.8/10**

**What broke** — `picklescan`, the tool meant to catch dangerous Python *pickle* (a format for saving objects that can run code when loaded) files inside AI model downloads, only checked files with standard extension names. An attacker who hides the malicious file behind a non-standard extension sails straight past the scanner. The scan gives false confidence on any model pulled from a suspicious source.

**Why it matters to an SMB running AI tools** — Downloading a pre-trained model (from a marketplace, a vendor, or just somewhere online) is a normal part of shipping an AI feature. If the tool that's supposed to inspect every model before it runs silently skips certain files, a malicious "model" can load with your own project's permissions and run attacker-supplied code. It's the security check on your model-supply-chain front door.

**What you do Monday**
1. Update `picklescan` to version 0.0.22 or newer. ~5 minutes.
2. Rather than trusting extension names, treat an untrusted model as an unknown program: prefer the `safetensors` format when the model offers it, and load anything else only after a scan in an isolated environment. ~15 minutes.

**Sources:** [GitHub advisory GHSA-769v-p64c-89pr](https://github.com/advisories/GHSA-769v-p64c-89pr) · [Sonatype advisory](https://sites.google.com/sonatype.com/vulnerabilities/cve-2025-1889)

---

### 3. HIGH — Your API integration platform has a file-path trick that leads to full server control
**CVE-2026-5430 · WSO2 API Manager, API Control Plane, Traffic Manager, Universal Gateway · added to CISA KEV 09-24-2026 · EPSS 0.0037 (29th percentile)**

**What broke** — WSO2's API products have a path-traversal flaw (a `../` trick in a file path to reach files that should be out of reach) combined with an unrestricted file upload, and together they can lead to remote code execution (RCE — an attacker runs their own code on your machine, i.e. full control). CISA confirms this is being actively exploited.

**Why it matters to an SMB running AI tools** — WSO2 API Manager is the software many teams use to ferry data between their apps, SaaS tools, and automation pipelines — exactly the kind of integration layer an SMB leans on to stitch AI features into the business. A hole in the API gateway is a hole in every connection it manages, including the data your AI tools read and write.

**What you do Monday**
1. Apply the vendor patch. The US federal deadline is **09-27-2026**, so treat this as urgent, not "someday." ~30–60 minutes plus a maintenance window.
2. If you don't know whether you run any WSO2 products, search your server list for "WSO2" / "API Manager" before assuming you're unaffected. ~10 minutes.

**Sources:** [WSO2 security advisory WSO2-2026-5328](https://security.docs.wso2.com/en/latest/security-announcements/security-advisories/2026/WSO2-2026-5328/) · [NVD CVE-2026-5430](https://nvd.nist.gov/vuln/detail/CVE-2026-5430)

---

### 4. HIGH — Check Point firewalls, two ways to take over your front door
**CVE-2026-93616 & CVE-2026-85102 · Check Point Security Management Server and firewalls · added to CISA KEV 09-22-2026 · EPSS 0.0242 (83rd percentile)**

**What broke** — Check Point has two actively exploited flaws in its firewall and security-management products. One is a path-traversal bug that lets someone with no login credentials upload and run arbitrary scripts on the management servers. The other is a certificate-validation failure (the check that a digital certificate on a connection really is who it claims) in the VPN path that lets a remote attacker run code on the gateway. Together they mean an outsider can take control of the security devices that guard your network.

**Why it matters to an SMB running AI tools** — All the traffic your AI tools send and receive — the app data, the API calls, the model queries — flows through your firewall. If the firewall itself is owned, the attacker sees and controls that traffic and everything behind it. This is a patch-the-front-door situation, not a footnote.

**What you do Monday**
1. Update the affected Check Point products per the vendor advisories. The US federal deadline is **09-25-2026 — today** — so do this now. ~30–60 minutes.
2. If your Check Point VPN is internet-facing, prioritize it first; remote-access VPN is a direct exposure. ~10 minutes.

**Sources:** [Check Point advisory sk1000171](https://support.checkpoint.com/results/sk/sk1000171/) · [Check Point advisory sk1000117](https://support.checkpoint.com/results/sk/sk1000117) · [NVD CVE-2026-93616](https://nvd.nist.gov/vuln/detail/CVE-2026-93616)

---

### 5. HIGH — F5 VPN gateway can be taken over without any login
**CVE-2026-94127 · F5 BIG-IP APM · added to CISA KEV 09-22-2026 · EPSS 0.0129 (69th percentile)**

**What broke** — F5 BIG-IP's remote-access module (the VPN many remote workers use to reach the office) has a heap-based buffer overflow — a memory bug where software writes past the space it allocated, which an attacker can use to run code. It's exploitable by someone with no login, and CISA confirms active exploitation. A temporary vendor "iRule" (a configuration snippet) is available while the final patch is installed.

**Why it matters to an SMB running AI tools** — If your team connects to the office — or to the internal systems your AI automation runs on — through F5 remote access, this is how outsiders could slip past that gateway unauthenticated and into your internal tools. Another patch-your-VPN situation.

**What you do Monday**
1. Install the final vendor patch, or apply the vendor's temporary iRule now to buy time. The US federal deadline is **09-25-2026 — today**. ~30 minutes.
2. Update your remote users after the fix; confirm the VPN re-connects cleanly. ~15 minutes.

**Sources:** [F5 article K000162605](https://my.f5.com/manage/s/article/K000162605) · [NVD CVE-2026-94127](https://nvd.nist.gov/vuln/detail/CVE-2026-94127)

---

## Jargon buster
- **API:** the software bridge one program uses to talk to another — how your apps and automation exchange data.
- **Buffer overflow:** a memory bug where software writes past the space it reserved; attackers use it to crash a service or run their own code.
- **Certificate validation:** checking that a digital certificate on a connection really is who it claims to be.
- **CVSS:** a 0–10 severity score for a flaw; 9.8/10 is critical, typically exploitable remotely with no login.
- **GraphCypherQAChain:** LangChain's helper that turns a chat question into a graph-database query.
- **iRule:** a configuration snippet on F5 appliances that temporarily shuts a hole while a full patch is installed.
- **Pickle:** a Python file format for saving objects; loading one can run code, so a random `.pkl` / `.pt` should be treated like an unknown program.
- **Prompt injection:** tricking an AI by putting instructions inside the data it reads — the AI follows the attacker's instructions instead of the user's.
- **RCE (remote code execution):** an attacker can run their own code on your machine from anywhere — full control.
- **SQL injection:** typing malicious database commands into an input box or prompt so the app runs unauthorized queries.
- **safetensors:** a model-weight file format that stores data without running code on load — safer than pickle for untrusted models.

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
| CVE-2026-85102 | Check Point (VPN) | 0.0099 (61st) | 09-22-2026 | 09-25-2026 | [Check Point](https://support.checkpoint.com/results/sk/sk1000117) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-85102) |
| CVE-2026-93952 | Arista VeloCloud Orchestrator | 0.0089 (58th) | 09-22-2026 | 09-25-2026 | [Arista](https://www.arista.com/en/support/advisories-notices/security-advisory/24765-security-advisory-0183) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-93952) |
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

*Compiled from public sources · 09-25-2026*