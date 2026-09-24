---
type: threat-feed-note
title: "Threat-Feed-09-24-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-09-24
---

# Threat-Feed-09-24-2026

**Threat intel for people deploying AI and automation in small businesses.**
One fully working "What to do Monday" per item. Headlines alone carry the gist. Full plain-language definitions for every term are at the bottom and in the public [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).

**How to read the scores**
- **EPSS** is a 0-to-1 score estimating how likely this flaw is to be exploited in the next 30 days; higher = patch first. Percentile says where that ranks: 96th percentile = more likely to be exploited than 96% of all known vulnerabilities.
- **CISA KEV** means "confirmed actively exploited right now" — not theoretical.
- **CVSS** is a 0–10 severity score for "how bad if it works"; EPSS/KEV answer "is it being used."

---

## Item 1 — HIGH — Your AI "chat with your data" assistant can be tricked into reading, changing, or deleting records in your database by a single crafted question

**CVE-2024-8309 (GraphCypherQAChain in langchain-community 0.2.5) · EPSS 0.1374 (96th percentile — top few percent most likely to be exploited)**

**What broke:** The `GraphCypherQAChain` helper in LangChain (a popular framework for building AI apps) turns a chat question into a database query. Because the query it builds is not locked down, a question can carry hidden instructions that escape "asking" and become "acting" — a combination of **SQL injection** (tricking an app into running unauthorized database commands) and **prompt injection** (hiding instructions inside data the AI reads). The AI then executes the attacker's commands against the database it is connected to.

**Why it matters to an SMB running AI tools:** Any "ask your data" assistant built on LangChain that is wired to a **graph database** (a database storing connected records, often used for customer/product/relationship data) is a potential door into that data. A malicious user — or a poisoned document a tool reads — could pull records out, change them, or in worst cases drop the data.

**What you do Monday:**
1. If you or a vendor built an assistant with `GraphCypherQAChain`, check your `langchain-community` package version and update to a fixed release (5–15 min).
2. Give the AI a **read-only, least-privilege database account** — it should never authenticate to the production database with write rights (15–30 min).
3. Test it yourself: ask your "chat with your data" tool something like "what tables exist?" and "can you add a record?" — if it acts instead of refuses, fix it before an attacker finds it (5 min).

**Sources:** [Huntr bounty](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5) · [LangChain fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) · [GitHub Advisory GHSA-45pg-36p6-83v9](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [CIRCL record](https://vulnerability.circl.lu/vuln/)

---

## Item 2 — HIGH — Your AI model scanner can miss a poisoned model file if it has a slightly unusual file name

**CVE-2025-1889 (picklescan before 0.0.22) · EPSS 0.0039**

**What broke:** `picklescan` is a scanner meant to catch dangerous **pickle** files (a Python format that can run code when loaded) inside downloaded AI models. Versions before 0.0.22 only looked at files with *standard* pickle file extensions. An attacker can rename a malicious model file with a non-standard extension and it sails straight past the check — the "scanned" model then runs attacker code when loaded.

**Why it matters to an SMB running AI tools:** If your AI pipeline downloads models — from Hugging Face, a vendor, or anywhere — and `picklescan` was your only model-safety check, a renamed poison file bypasses it. A malicious model can execute code on the machine that loads it, giving an attacker access to whatever that server can reach.

**What you do Monday:**
1. Upgrade `picklescan` to 0.0.22 or later (2 min).
2. Do not rely on file-extension checks alone — treat any downloaded model like an unknown program; load untrusted models in the `safetensors` format instead of raw pickle (15–30 min).
3. Only download models from sources you already trust; pin the exact version you use.

**Sources:** [GitHub Advisory GHSA-769v-p64c-89pr](https://github.com/advisories/GHSA-769v-p64c-89pr) · [Sonatype advisory](https://sites.google.com/sonatype.com/vulnerabilities/cve-2025-1889) · [CIRCL record](https://vulnerability.circl.lu/vuln/)

---

## Item 3 — CRITICAL — Your remote-access VPN gateway (F5 BIG-IP APM) has an actively exploited hole that lets an attacker run code with no login — patch today

**CVE-2026-94127 · CISA confirmed actively exploited as of 09-22-2026 · CISA requires federal agencies to patch by 09-25-2026 · EPSS 0.0139 (71st percentile)**

**What broke:** A **heap buffer overflow** (a memory bug where software writes past the space it allocated) in F5 BIG-IP's APM module. When the access policy and an OAuth profile (a saved configuration for delegating login) are both set on a virtual server, an unauthenticated remote attacker can pull off **Remote Code Execution** — running their own code on the gateway with no login at all.

**Why it matters to an SMB running AI tools:** This is the remote-access front door many employees (and AI agents/tools) use to reach the office network. An attacker with code-running access here is inside the perimeter — able to reach the servers, file shares, and databases your automation stack depends on. CISA classified this as real, active exploitation.

**What you do Monday:**
1. Apply the vendor-provided temporary **iRule** mitigation immediately (10 min).
2. Then install the final vendor patch as soon as it is available — the iRule is a stopgap, not the fix.
3. Watch login/access logs for unexpected APM sessions while you patch (30 min).

**Sources:** [F5 advisory K000162605](https://my.f5.com/manage/s/article/K000162605) · [NVD CVE-2026-94127](https://nvd.nist.gov/vuln/detail/CVE-2026-94127)

---

## Item 4 — HIGH — Your Check Point firewall management box can be taken over by an attacker with no login who uploads and runs their own scripts

**CVE-2026-93616 (path traversal) + CVE-2026-85102 (certificate validation) · Check Point multiple products · CISA confirmed actively exploited as of 09-22-2026 · deliver by 09-25-2026**

**What broke:** Two flaws in Check Point security products are being actively exploited:
- **CVE-2026-93616:** A **path traversal** (a trick where an attacker types `../` in a path to reach files they shouldn't) in the Security Management Server and related products lets an unauthenticated attacker upload and run arbitrary scripts.
- **CVE-2026-85102:** An improper certificate validation flaw in the Check Point Security Gateway and its small-business firewall line's remote-access VPN lets an unauthenticated remote attacker run code on the gateway.

**Why it matters to an SMB running AI tools:** The Check Point firewall management console *sets the rules that protect your network* — including the network your AI and automation workloads live on. Compromising it lets an attacker rewrite the perimeter, add back doors, and see traffic that flows to and from your AI services.

**What you do Monday:**
1. Apply the Check Point patches for [SK1000171](https://support.checkpoint.com/results/sk/sk1000171/) and [SK1000117](https://support.checkpoint.com/results/sk/sk1000117) (30–60 min, plan a maintenance window).
2. If you run a Check Point gateway with Site-to-Site or Remote Access VPN, treat it as urgent — do not wait.
3. Check management-console logs for unrecognized uploads or rule changes in the last two weeks (30 min).

**Sources:** [Check Point SK1000171](https://support.checkpoint.com/results/sk/sk1000171/) · [Check Point SK1000117](https://support.checkpoint.com/results/sk/sk1000117) · [NVD CVE-2026-93616](https://nvd.nist.gov/vuln/detail/CVE-2026-93616) · [NVD CVE-2026-85102](https://nvd.nist.gov/vuln/detail/CVE-2026-85102)

---

## Item 5 — HIGH — Arista VeloCloud Orchestrator (the manager for your SD-WAN links) is being exploited to reach privileged internal functions

**CVE-2026-93952 · Arista VeloCloud Orchestrator · CISA confirmed actively exploited as of 09-22-2026 · deliver by 09-25-2026 · EPSS 0.0074**

**What broke:** An improper input validation flaw in the on-premises Arista VeloCloud Orchestrator (VCO — the controller managing an **SD-WAN**, a software-defined wide-area network that routes traffic between branch offices) lets a remote attacker reach privileged internal functionality and compromise the orchestrator host. That can hit confidentiality, integrity, and availability of everything it orchestrates.

**Why it matters to an SMB running AI tools:** SD-WAN is how a small business usually connects branch offices to the cloud — including the cloud where your AI services, data, and automation run. Compromise the orchestrator and an attacker can quietly reroute or intercept branch traffic, including traffic to your AI/cloud workloads.

**What you do Monday:**
1. Apply the mitigations in [Arista advisories/security-advisory-0183](https://www.arista.com/en/support/advisories-notices/security-advisory/24765-security-advisory-0183) (target your VCO admins, 15 min).
2. Confirm the on-prem VCO is not exposed to the public internet; restrict it to management network only (15 min).
3. Review VCO logs for unexpected configuration or routing changes (20 min).

**Sources:** [Arista advisory 0183](https://www.arista.com/en/support/advisories-notices/security-advisory/24765-security-advisory-0183) · [NVD CVE-2026-93952](https://nvd.nist.gov/vuln/detail/CVE-2026-93952) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

---

## Jargon buster

Terms used today, one line each (living master list in [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md)):

- **SQL injection:** A technique where attackers type malicious database commands into an input box (or a prompt), tricking the app into running unauthorized queries — reading, changing, or deleting data.
- **Prompt injection:** Tricking an AI by putting instructions inside the data it reads — the AI follows the attacker's instructions instead of the user's.
- **Graph database:** A database that stores things and their relationships as connected points. AI tools may query it to answer questions about linked business records.
- **Least privilege:** Giving a person or software account only the access it needs for its job, and no more.
- **Pickle:** A Python file format for saving objects. Loading one can run code — treat a random `.pkl`/`.pt` like an unknown program.
- **Heap buffer overflow:** A memory bug where software writes past the space it allocated for data. Attackers use it to crash a service or, in the right conditions, run their own code.
- **Remote Code Execution (RCE):** An attacker can run their own code on your machine from anywhere. "Game over" — full control.
- **Unauthenticated (attacker):** Someone with no login credentials, operating from anywhere on the network or internet.
- **OAuth profile:** A saved configuration an access server uses to delegate login to an external identity service.
- **Path traversal:** A trick where an attacker types `../` in a file path to reach files they shouldn't. In a server product this can become full takeover.
- **Certificate validation:** Checking that a digital certificate on a connection really is who it claims to be. If the check is skipped, a stranger can present a fake certificate and the system trusts it.
- **SD-WAN:** A software-defined wide-area network that manages and routes traffic between branch offices over software instead of dedicated hardware.
- **ACR Stealer:** Malware that steals saved data (passwords, cookies) from Windows. A listed domain is a block-and-hunt signal; do not visit it.

---

## Appendix

### CISA KEV — actively exploited, ranked by EPSS (most likely to be exploited first)

| CVE | Product | CISA confirmed | Federal due | EPSS | Source |
|---|---|---|---|---|---|
| CVE-2026-93616 | Check Point Management/Log servers | 09-22-2026 | 09-25-2026 | 0.0242 | [Check Point](https://support.checkpoint.com/results/sk/sk1000171/) |
| CVE-2026-7273 | Zyxel GS1900 switches | 09-21-2026 | 09-24-2026 | 0.0241 | [Zyxel](https://www.zyxel.com/global/en/support/security-advisories/zyxel-security-advisory-for-stack-based-buffer-overflow-vulnerability-in-gs1900-series-switches-06-16-2026) |
| CVE-2025-39682 | Linux Kernel (TLS receive) | 09-18-2026 | 09-21-2026 | 0.0203 | [kernel commit](https://git.kernel.org/stable/c/2902c3ebcca52ca845c03182000e8d71d3a5196f) |
| CVE-2026-94127 | F5 BIG-IP APM | 09-22-2026 | 09-25-2026 | 0.0139 | [F5](https://my.f5.com/manage/s/article/K000162605) |
| CVE-2025-39964 | Linux Kernel (AF_ALG) | 09-18-2026 | 09-21-2026 | 0.0079 | [kernel commit](https://git.kernel.org/stable/c/0f28c4adbc4a97437874c9b669fd7958a8c6d6ce) |
| CVE-2026-93952 | Arista VeloCloud Orchestrator | 09-22-2026 | 09-25-2026 | 0.0074 | [Arista](https://www.arista.com/en/support/advisories-notices/security-advisory/24765-security-advisory-0183) |
| CVE-2026-85102 | Check Point Gateways | 09-22-2026 | 09-25-2026 | 0.0066 | [Check Point](https://support.checkpoint.com/results/sk/sk1000117) |
| CVE-2026-53266 | Linux Kernel (ebtables SNAT) | 09-18-2026 | 09-21-2026 | 0.0028 | [kernel commit](https://git.kernel.org/stable/c/bf84ad7c7a9ede46e31afaa41a1ba06a159e8c87) |

*Zyxel GS1900 (CVE-2026-7273) federal due date is **today**, 09-24-2026.* Linux Kernel items are patched by your OS vendor's update channel — update your servers; Do not hand-patch kernel source unless you maintain it.

### CIRCL — notable AI/software findings (ranked by EPSS)

| Finding | Issue | EPSS | Source |
|---|---|---|---|
| CVE-2024-8309 (langchain-community) | GraphCypherQAChain SQL injection via prompt injection | 0.1374 | [Huntr](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5) / [GHSA](https://github.com/advisories/GHSA-45pg-36p6-83v9) |
| CVE-2025-1889 (picklescan) | Model safety scan skips non-standard file extensions | 0.0039 | [GHSA](https://github.com/advisories/GHSA-769v-p64c-89pr) |

### ThreatFox / URLhaus — IOC sample (block-and-hunt signals; do not visit)

- **AMOS** (Apple-data stealer) — URLs/domain `delta-canvas.com`, host `104.248.194.193`. [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/osx.amos)
- **ACR Stealer** (Windows) — domain `media.hazelnook.cc`. [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/win.acr_stealer)
- **Remcos** (remote-access trojan) — `84.38.133.167:7474`. [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/win.remcos)
- **URLhaus** fresh payloads — [ficus.in](https://urlhaus.abuse.ch/url/3922088/), [198macros.org](https://urlhaus.abuse.ch/url/3922080/), [noamaddons.com](https://urlhaus.abuse.ch/url/3922084/). Especially note the `.jar` payloads (198-Macros, NoamAddons) — fake/bundled Java downloads are a common way malware gets launched.

Keep blockers current on these domains/IPs and check your edge logs for outbound contact.

### Ransomware

No fresh ransomware victim data was available this run (the source was unavailable this morning) — so no sector pulse to report today. Standard advice stands: verify backups are tested and offline, and patch the networking/VPN items above, since those are the doors ransomware crews walk through.

### CISA advisories

CISA published a fact sheet, *Considerations for Critical Infrastructure Operators Working With Third-Party ICS Integrators* (09-23-2026), on the risk of giving third-party industrial-control integrators broad access — enforce least privilege, inventory what they can reach, and monitor their remote access. Read it [here](https://www.cisa.gov/resources-tools/resources/considerations-critical-infrastructure-operators-working-third-party-ics-integrators). The same principle applies to any SMB vendor/integrator with access to your systems.

---

*Compiled from public sources · 09-24-2026*
