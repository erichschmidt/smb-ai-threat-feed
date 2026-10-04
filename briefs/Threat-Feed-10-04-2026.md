---
type: threat-feed-note
title: "Threat Feed - 10-04-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-10-04
updated: 2026-10-04
---

# Threat Feed - 10-04-2026

Plain-language cyber threat briefing for small businesses running artificial intelligence (AI) and automation. Headlines alone are the 3-minute read. A term is unfamiliar? It's defined right where it appears, and every term is spelled out in plain language in the [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md) at the bottom.

## How to read the scores

- **EPSS:** a 0-1 score estimating a vulnerability's odds of being exploited in the next 30 days. Higher = patch first. Percentile (e.g. 82nd) = where that score ranks against all known vulnerabilities - 82nd means it's more likely to be exploited than 82% of everything known.
- **KEV (Known Exploited Vulnerabilities catalog):** CISA's authoritative list of flaws actually being attacked right now - if it's there, it is not theoretical. CISA confirms an item's actual exploitation as of its "confirmed" date, and sets a federal-agency patch deadline (due date).
- **CVSS:** a 0-10 severity score for a flaw. 9.8/10 = critical - typically exploitable remotely with no login. "How bad if it works", while EPSS/KEV answer "is it actually being used".

---

## 1. HIGH - The AI build-blocks already in today's feed are still live: a "chat with your data" helper that can run database commands from a prompt, and a model-scan check that can be sailed past. Verify both this week.

**CVE-2024-8309 - LangChain GraphCypherQAChain (langchain-community), EPSS 0.1374 (96th percentile - more likely to be exploited than 96% of all known flaws); CVE-2025-1889 - picklescan (before 0.0.22), EPSS 0.004 (31st)**

**What broke:** Two AI-specific holes keep re-appearing at the top of the feed, and both deserve a concrete check, not another skim. LangChain is the widely used open-source toolkit for building AI assistants, including "ask your database" tools. One helper, GraphCypherQAChain, turns a plain-English question into a query against a graph database (a database that stores records and their relationships as connected points). It reads attacker-supplied text from a prompt or document and can let that text turn into a malicious database query the developer never intended - reading, changing, or deleting data without authorization (SQL injection through prompt injection). Separately, picklescan is a scanner meant to catch dangerous Python pickle files (a file format that can run code when loaded) hidden inside AI model downloads. Before version 0.0.22, it only scanned standard file extensions, so a malicious model using a non-standard filename sailed past the check.

**Why it matters to an SMB running AI tools:** These are the two most likely places "your AI is the weak link" shows up for a small team. If you or a vendor built an assistant that answers questions from your customer, product, or document data, GraphCypherQAChain may be the engine under it - and the attack rides the normal input path (a poisoned prompt inside a message, a web form, or a document the AI reads). And a model-download scanner that can be bypassed means your team's "we scan the models we download" confidence may be false. Both are still on the feed because they're widespread and still exploitable.

**What you do Monday:**
1. Check your dependencies for the affected line: in your project, run `pip show langchain-community` (fix is in patched releases past 0.2.5) to confirm the version; and confirm your picklescan is 0.0.22 or newer with `pip show picklescan` (15 minutes).
2. For any GraphCypherQAChain assistant, connect it to the database with a read-only account - least privilege - so even a successful injected query can't change or delete records (30 minutes).
3. If your team loads AI models directly (not through a scanner), load them with pickled/`torch.load` guards or switch to `safetensors` (a model format that stores data without running code on load) and re-test against a throwaway copy (1 hour).

**Sources:** [GitHub advisory GHSA-45pg-36p6-83v9 (LangChain)](https://github.com/advisories/GHSA-45pg-36p6-83v9) - [Fix commit (LangChain)](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) - [GitHub advisory GHSA-769v-p64c-89pr (picklescan)](https://github.com/advisories/GHSA-769v-p64c-89pr) - [CVSS records](https://www.cve.org/CVERecord?id=CVE-2025-1889)

---

## 2. HIGH - Your iPhones, Macs, and iPads carry a flaw that is actively being attacked - and the federal deadline to patch has already passed. Update today.

**CVE-2026-86950 - Apple iOS / macOS / iPadOS (CoreGraphics) - added to CISA KEV 09-29-2026 - federal patch deadline 10-02-2026 (passed) - actively exploited per CISA - EPSS 0.0124 (68th percentile)**

**What broke:** CoreGraphics is the engine inside Apple devices that draws everything on screen. A flaw in it - an out-of-bounds write, a memory bug where software writes past the space it reserved for data, which attackers use to run their own code - could let an attacker run code on your iPhone, Mac, or iPad. It's being exploited in the wild, so this is not a theoretical risk. It affects iOS, macOS, and iPadOS at once because they share the same graphics engine.

**Why it matters to an SMB running AI tools:** Phones, Macs, and tablets are how your team reaches your cloud apps, shared drives, and AI workers every day - and often the device that holds the login to them. A compromised personal or work device is a foothold an attacker can use to reach the same data your AI tools read. Because the deadline is already here and it's confirmed exploited, this is a "do it today" item, not a "plan it" item.

**What you do Monday:**
1. On each device open **Settings → General → Software Update** (iPhone/iPad) or **System Settings → General → Software Update** (Mac) and install the current release (10-20 minutes per device).
2. After updating, confirm no apps are still running an old OS by checking **About → iOS/macOS Version** (10 minutes).
3. For any device you cannot update (too old, unsupported), treat it as high-risk: move it off work logins and cloud access until it can be replaced (30 minutes).

**Sources:** [Apple support advisory (iOS/macOS/iPadOS)](https://support.apple.com/en-us/149226) - [Apple support advisory](https://support.apple.com/en-us/149228) - [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-86950)

---

## 3. WATCH - If you have not patched your mail-appliance hole, today is CISA's deadline. It is still being exploited and it is the most-likely-to-be-hit item on this week's list.

**CVE-2026-104286 - Fortinet FortiMail - added to CISA KEV 10-01-2026 - federal patch deadline 10-04-2026 (today) - actively exploited per CISA - EPSS 0.022 (82nd percentile - the highest on this week's exploited list)**

**What broke:** FortiMail is the appliance many offices use to filter and route business email. A bundled pair of flaws - a path traversal (a request that climbs out of the folder it should stay in to reach files elsewhere) plus poor NULL-byte handling - lets an unauthenticated attacker write arbitrary files onto the underlying server via crafted HTTP/HTTPS requests. No login required, and it is the item most likely to be exploited this week.

**Why it matters to an SMB running AI tools:** Email is the front door for prompt injection and automation poisoning: your AI inbox assistants and "mail to CRM/document" automations read whatever lands in the mailbox. An attacker who can plant files on the mail appliance is one step from feeding your AI pipeline attacker-controlled content - and from taking over the box your team depends on every single day.

**What you do Monday:**
1. In your FortiMail console, apply the vendor's recommended mitigation / hotfix from FG-IR-26-175 (30-60 minutes).
2. If it still cannot be patched today, keep the management interface off the public internet - admin-IP-only access - until it is (30 minutes).
3. Run Fortinet's supplied indicators of compromise on the appliance to check whether it was already hit before you patch (15 minutes).

**Sources:** [Fortinet advisory FG-IR-26-175](https://fortiguard.fortinet.com/psirt/FG-IR-26-175) - [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-104286)

---

## 4. WATCH - The controllers that run your building's heating, cooling, and lights send login credentials in cleartext (unencrypted) - an attacker on the network can read them.

**CISA advisory ICSA-26-274-05 - Johnson Controls EasyIO Neo Series EC and CW Controllers (CVE-2026-64893) - advised 09-22-2026**

**What broke:** EasyIO Neo controllers are the edge devices that manage HVAC, lighting, and energy in commercial buildings through a web interface. They transmit login credentials and session data in cleartext - meaning anyone who can intercept the traffic, including someone already on the same network, can read them. Cleartext is the opposite of encrypted: the data is sent as-is, so a network sniffer sees the password. Fixed firmware exists; older versions (EC V3.3b62/b63, CW V3.3b24/b25) are affected.

**Why it matters to an SMB running AI tools:** Building automation rarely gets the same security attention as your servers, but these controllers sit on your office network alongside the systems your AI and automation tools depend on - and their credentials are readable in transit. If you outsource facility management, the contractor who connects to these controls is a supply-chain point of contact worth confirming is patched. HTTP is the problem; HTTPS is the fix.

**What you do Monday:**
1. If you manage the building yourself, upgrade the controllers to the fixed firmware (EC V3.3b64 or later, CW V3.3b26 or later) per Johnson Controls' guidance; otherwise ask your facility contractor to confirm this is scheduled (1-2 hours).
2. Enable and enforce HTTPS/TLS for all management access and disable HTTP entirely (30 minutes).
3. Make sure these controllers are on a network segment isolated from your business PCs and AI servers, behind a firewall (1 hour).

**Sources:** [CISA advisory ICSA-26-274-05](https://www.cisa.gov/news-events/ics-advisories/icsa-26-274-05) - [CVE details](https://www.cve.org/CVERecord?id=CVE-2026-64893)

---

## Jargon buster

- **Building automation controller:** the edge device that manages a commercial building's HVAC, lighting, and energy systems through a web interface.
- **Cleartext:** data sent or stored unencrypted, so anyone who intercepts it can read it - the opposite of encrypted.
- **CoreGraphics:** Apple's graphics engine that renders what appears on screen, shared across iPhone, Mac, and iPad.
- **EPSS (Exploit Prediction Scoring System):** a 0-1 score estimating how likely a vulnerability is to be exploited in the next 30 days. Higher = patch first.
- **Graph database:** a database that stores things and their relationships as connected points. AI tools may query it to answer questions about linked business records.
- **GraphCypherQAChain:** LangChain's helper that turns a chat question into a graph-database query. If that query isn't locked down, the chat becomes a database write.
- **KEV (Known Exploited Vulnerabilities):** CISA's authoritative list of flaws actually being exploited right now - the "real right now" signal, not theory.
- **Least privilege:** giving a software account only the access it needs for its job, and no more.
- **Out-of-bounds write:** a memory bug where software writes past the space it allocated for data. Attackers use it to crash a service or, in the right conditions, run their own code.
- **Path traversal:** a flaw where a request with special ".." paths lets an attacker escape the intended folder and touch files elsewhere on the system.
- **pickle / picklescan:** pickle is a Python file format for saving objects; loading one can run code. picklescan is a scanner meant to catch dangerous pickle files inside AI model downloads. If it skips a file extension, a "model" can be malware.
- **Prompt injection:** an attack that slips instructions into data the AI reads, so the AI acts on the attacker's text as if it were a legitimate command.
- **Safetensors:** a model-weight file format that stores data without running code on load. Prefer it over pickle/raw `torch.load` for untrusted models.
- **SQL injection:** a technique where attackers type malicious database commands into an input (or a prompt), tricking the app into running unauthorized queries - reading, changing, or deleting data.
- **Vidar:** malware that steals saved passwords, browser cookies, and crypto-wallet files from a Windows PC and sends them to the attacker.

---

## Appendix

### A. KEV catalog this week (ranked by EPSS - highest exploitation likelihood first)

| CVE | Product | CISA confirmed | Federal patch by | EPSS (percentile) | Ransomware use | Source |
|---|---|---|---|---|---|---|
| CVE-2026-104286 | Fortinet FortiMail | 10-01-2026 | 10-04-2026 | 0.022 (82nd) | Unknown | [Fortinet](https://fortiguard.fortinet.com/psirt/FG-IR-26-175) |
| CVE-2026-76504 | Cisco Catalyst SD-WAN Manager | 09-30-2026 | 10-03-2026 | 0.0158 (75th) | Unknown | [Cisco](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-sdwan-webauth-xr8beuuU) |
| CVE-2026-102489 | Zammad (session fixation / RCE) | 10-02-2026 | 10-05-2026 | 0.014 (71st) | Unknown | [CISA alert](https://www.cisa.gov/news-events/alerts/2026/10/02/cisa-adds-two-known-exploited-vulnerabilities-catalog) |
| CVE-2026-86950 | Apple iOS/macOS/iPadOS CoreGraphics | 09-29-2026 | 10-02-2026 | 0.0124 (68th) | Unknown | [Apple](https://support.apple.com/en-us/149226) |
| CVE-2026-102490 | Zammad (privilege escalation to root) | 10-02-2026 | 10-05-2026 | 0.0063 (48th) | Unknown | [CISA alert](https://www.cisa.gov/news-events/alerts/2026/10/02/cisa-adds-two-known-exploited-vulnerabilities-catalog) |

### B. Ransomware sector pulse (victim-claim signals from 10-03-2026)
- **Wallstreet** claimed a US nonprofit healthcare system (St. Francis Healthcare System of Hawaii, Healthcare) and a Middle-East construction consortium building the Jeddah World Cup 2034 stadium (Other). Healthcare remains a steady target - and the Jeddah hit shows major-event infrastructure in the crosshairs. [Ransomware.live](https://www.ransomware.live)
- **qilin** claimed a US Financial Services victim - a sector that is prime AI/automation territory and a reminder that finance records attract direct attention. **netrunner** claimed a US marine-construction firm (Transportation). [Ransomware.live](https://www.ransomware.live)
- **rhysida** had a busy day: a Vietnamese cloud-hosting / domain-registrar (Technology - directly relevant to the SMB AI/IT supply chain), a Swedish industrial-furnace maker (Energy & Utilities, 2.55 TB of SolidWorks CAD designs claimed stolen), and a Lebanese fabric firm (Other). **akira** claimed a Mexican architecture-college body; **Spirals** claimed a UAE maritime-supplies group (Transportation). [Ransomware.live](https://www.ransomware.live)

*Treat all victim claims as unverified attacker assertions - useful as "this sector is being hunted" signals, not as confirmed incidents.*

### C. Notable CIRCL findings (higher EPSS first / on-lens first)
- **LangChain GraphCypherQAChain (CVE-2024-8309)** - SQL injection through prompt injection; the strongest on-lens item of the feed, EPSS 0.1374 (96th). Covered as item 1. [GitHub advisory](https://github.com/advisories/GHSA-45pg-36p6-83v9)
- **Picklescan (CVE-2025-1889)** - AI model-file scanner bypass via non-standard file extension. Covered as item 1; confirm your scanner is 0.0.22+. EPSS 0.004 (31st). [GitHub advisory](https://github.com/advisories/GHSA-769v-p64c-89pr)
- The rest of the CIRCL feed is dominated by low-EPSS Rocky/Red Hat patch errata (libpcap, FreeRDP, Ghostscript, Expat, OpenSSH, kernel, Node.js, Thunderbird, libxml2, unbound RCE) - server-admin patching signal, not SMB-priority top items.

### D. IOC sample (block-and-hunt signals - do not visit)
- **Vidar** (info-stealer): today's feed lists the domain `kh.333pwk.org` and `kh.396zk.net` as active drop/distribution points - block them at your firewall and hunt for contact in logs. [Malpedia Vidar](https://malpedia.caad.fkie.fraunhofer.de/details/win.vidar)
- **Mirai** (camera/router botnet): three captured SHA-256 file hashes on today's feed, including `a29c5b31347714fd1e7470ade9d5fffc183ff86029969dcf313729fe7292f310` - block-and-hunt signals for IoT botnet spread. [Malpedia Mirai](https://malpedia.caad.fkie.fraunhofer.de/details/elf.mirai)
- **URLhaus recent payload URLs** (IoT "Hilix" botnet binaries from a single re-using server; block, do not visit): `http://176.65.148.144/bins/Hilix.ppc` - [URLhaus 3928537](https://urlhaus.abuse.ch/url/3928537/) | `http://176.65.148.144/bins/Hilix.arm5` - [URLhaus 3928538](https://urlhaus.abuse.ch/url/3928538/) | `http://176.65.148.144/bins/Hilix.mpsl` - [URLhaus 3928533](https://urlhaus.abuse.ch/url/3928533/)

---

*Compiled from public sources · 10-04-2026*
