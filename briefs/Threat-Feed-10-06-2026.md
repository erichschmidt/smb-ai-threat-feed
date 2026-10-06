---
type: threat-feed-note
title: "Threat Feed - 10-06-2026"
status: published
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-10-06
updated: 2026-10-06
---

# SMB + AI Threat Feed — 10-06-2026

**Reader promise (3-minute read):** Adversaries are harder and AI tools are here to stay. Read the headlines — each is one plain sentence with a fix. If a term is new, [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md) explains it in one line. No jargon required.

## How to read the scores

- **EPSS** is a 0–1 score estimating how likely a flaw is to be exploited in the next 30 days. Higher = patch first. The **percentile** shows where it ranks vs all known flaws: 96th percentile means it's in the top 4% most likely to be exploited.
- **CISA KEV** = CISA confirmed the flaw is being actively exploited right now. If it's on this list, it's not theoretical — patch it.
- **CVSS** is a 0–10 "how bad if it works" severity. 9.8/10 = critical, exploitable remotely with no login.

---

## 1. HIGH — The AI "chat with your data" framework remains your top AI-stack risk — verify your version today

**CVE-2024-8309** · EPSS 0.1374 (96.4th percentile — the highest exploit-likelihood score in today's data; in the top ~4% of all known flaws) · CVSS 9.8/10 (critical, remote, no login)

**What broke.** LangChain (a widely used open-source framework for building AI apps that answer questions from your own data) has a flaw in its graph-database query helper. An attacker who can ask the AI a question — through your chatbot, your support widget, or any "chat with your files" tool built on this library — can plant **SQL injection** (type malicious database commands into the prompt) that reads, changes, or deletes data the chat was never meant to touch. This scores the highest exploit likelihood of anything in the feed today, so it's worth re-confirming even if you looked at it recently.

**Why it matters to an SMB running AI tools.** If you run any RAG (Retrieval-Augmented Generation — the standard way AI tools answer from your own files) app built on LangChain's graph helper, the "talk to your business data" feature is the attack surface. A malicious prompt buried in a document or typed into the chat can reach the database the model answers from — your customers, orders, and records. One framework flaw maps to every chat tool that uses it.

**What you do Monday.**
1. Find which LangChain packages your AI apps use: run `pip freeze` or open your app's dependency list and look for `langchain-community`. (10 minutes)
2. If you're on `langchain-community` 0.2.5 or earlier, update to the patched version that includes the fix commit. (20 minutes)
3. Restrict the graph-database account your AI uses to read-only, so even a successful injection can't write or delete. (15 minutes)

**Sources:** [huntr advisory](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5) · [GitHub Security Advisory](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [Fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255)

---

## 2. HIGH — Your SD-WAN orchestrator lets an outsider in as admin with no login — patch now

**CVE-2026-76504** · EPSS 0.0158 (74.6th percentile — more likely to be exploited than ~75% of known flaws) · CISA confirmed actively exploited as of **09-30-2026** · CISA requires federal agencies to patch by **10-03-2026**

**What broke.** Cisco Catalyst SD-WAN Manager (the control panel that configures and routes traffic between your office and branch sites) has a **hex encoding** flaw (a way web addresses are encoded as 0–9,A–F characters; when the server mis-decodes it, an attacker can smuggle past checks). An **unauthenticated attacker** (no login at all) can reach the system with admin privileges by crafting a web request. It's on CISA's actively-exploited list.

**Why it matters to an SMB running AI tools.** If you route branch-office traffic through SD-WAN, this panel controls every link your remote staff — and the AI/automation dashboards they reach — travel over. Administrator access here lets an attacker read or reroute that traffic, tamper with what reaches your tools, or plant a foothold beside them. The command-and-control surface for your whole network sits behind this login.

**What you do Monday.**
1. Check your Catalyst SD-WAN Manager version against the advisory; apply the fixed release. (1–2 hours)
2. If you can't patch immediately, restrict admin access to trusted networks / VPN only. (20 minutes)
3. Review the orchestrator's admin-account and configuration-change logs for the past week. (30 minutes)

**Sources:** [Cisco advisory cisco-sa-sdwan-webauth](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-sdwan-webauth-xr8beuuU) · [NVD entry](https://nvd.nist.gov/vuln/detail/CVE-2026-76504)

---

## 3. WATCH — Your automation management suite can be fed bad data that skips the checks you count on

**CVE-2026-56596** · no score yet (recently published)

**What broke.** HCL BigFix Service Management (a tool teams use to automate and manage IT endpoint tasks) has an **input validation** flaw (it doesn't properly check the data coming in). An attacker can feed it unexpected or malformed input that causes processing errors and slips past normal business logic. This is an "inspect before you build automations on it" item rather than a confirmed live wildfire.

**Why it matters to an SMB running AI tools.** If BigFix drives your patch, deployment, or endpoint automations, a flaw that lets malformed data skip logic checks is a flaw in the trust your automation pipeline places in it — the same class as a poisoned input to an AI workflow. An out-of-spec command that runs anyway is exactly how an automated "safe" action turns into an unintended change.

**What you do Monday.**
1. Confirm whether you run HCL BigFix Service Management and on which version. (10 minutes)
2. If you do, watch for a patched release from HCL and subscribe to its security updates. (10 minutes)
3. In any automation you manage, pin input validation at the boundary so malformed data fails closed, not open. (30 minutes)

**Sources:** [CIRCL advisory CVE-2026-56596](https://vulnerability.circl.lu/vuln/CVE-2026-56596)

---

## Jargon buster

- **EPSS:** A 0–1 score estimating how likely a flaw is to be exploited in the next 30 days; higher = patch first. Percentile = where it ranks vs all known vulnerabilities.
- **KEV / CISA KEV:** CISA's list of vulnerabilities confirmed to be actively exploited right now — not theoretical.
- **SQL injection:** Typing malicious database commands into an input (or a prompt), tricking the app into running unauthorized queries.
- **Prompt injection:** Tricking an AI by putting instructions inside the data it reads; it follows the attacker's instructions instead of the user's.
- **RAG (Retrieval-Augmented Generation):** The standard way AI tools answer from your own files — it retrieves relevant documents, then answers from them.
- **LangChain:** A popular open-source framework for building AI chat apps that answer from your data. Because it's everywhere, a flaw in it affects many AI tools at once.
- **GraphCypherQAChain:** LangChain's helper that turns a chat question into a graph-database query; if the query isn't locked down, the chat becomes a database write.
- **CVSS:** A 0–10 severity score; 9.8/10 = critical, exploitable remotely with no login.
- **SD-WAN:** A software-defined network that routes traffic between office and branch sites over software instead of dedicated hardware; its manager is the control panel for all those links.
- **Hex encoding:** A way of encoding web-address characters as 0–9,A–F. When a server mis-decodes it, an attacker can smuggle past checks to reach admin functions.
- **Unauthenticated (attacker):** Someone with no login credentials.
- **Input validation:** Software checking that the data coming in is the right shape; a flaw here means bad data gets processed anyway.
- **Business logic:** The rules that define what an app is supposed to do; a bypass means those rules are skipped.

---

## Appendix

### Active exploits added or updated this week (CISA KEV), ranked by EPSS

| CVE | Product | EPSS (percentile) | CISA added | Federal deadline | Ransomware used | Source |
|---|---|---|---|---|---|---|
| CVE-2026-104286 | Fortinet FortiMail | 0.022 (81.9) | 10-01-2026 | 10-04-2026 | Unknown | [Fortinet](https://fortiguard.fortinet.com/psirt/FG-IR-26-175) |
| CVE-2026-76504 | Cisco Catalyst SD-WAN Manager | 0.0158 (74.6) | 09-30-2026 | 10-03-2026 | Unknown | [Cisco](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-sdwan-webauth-xr8beuuU) |
| CVE-2026-102489 | Zammad | 0.014 (71.5) | 10-02-2026 | 10-05-2026 | Unknown | [Zammad](https://zammad.com/en/product/releases/) |
| CVE-2026-102490 | Zammad | 0.0063 (48.3) | 10-02-2026 | 10-05-2026 | Unknown | [Zammad](https://zammad.com/en/product/releases/) |
| CVE-2026-88779 | Citrix NetScaler | 0.0053 (43.1) | 10-04-2026 | 10-07-2026 | Unknown | [Citrix](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697174) |

*EPSS = likelihood of exploitation in the next 30 days; percentile = rank vs all known flaws. "Ransomware used: Unknown" means no confirmed ransomware-campaign link is on record.*

### Ransomware victims — latest disclosures

| Group | Sector | Country | Discovered | Source |
|---|---|---|---|---|
| SilentRansomGroup | Professional Services | US | 10-05-2026 | [Ransomware.live](https://www.ransomware.live) |
| qilin | Professional Services | US | 10-05-2026 | [Ransomware.live](https://www.ransomware.live) |
| safepay | Technology | CZ | 10-05-2026 | [Ransomware.live](https://www.ransomware.live) |
| safepay | Retail & E-Commerce | CH | 10-05-2026 | [Ransomware.live](https://www.ransomware.live) |
| safepay | Professional Services | DE | 10-05-2026 | [Ransomware.live](https://www.ransomware.live) |
| safepay | Professional Services | IT | 10-05-2026 | [Ransomware.live](https://www.ransomware.live) |
| safepay | Retail & E-Commerce | US | 10-05-2026 | [Ransomware.live](https://www.ransomware.live) |
| safepay | Technology | DE | 10-05-2026 | [Ransomware.live](https://www.ransomware.live) |

*Victim names are attacker self-disclosures, not confirmed incidents. Use this as a "which sectors are being hunted right now" signal.*

### Notable CIRCL advisories (beyond the top findings)

- **CVE-2025-1889 (picklescan):** A scanner meant to catch dangerous Python `pickle` files inside AI model downloads only checked standard file extensions, so a renamed malicious model sails past. Update to 0.0.22+ and prefer the `safetensors` format. [GitHub Advisory](https://github.com/advisories/GHSA-769v-p64c-89pr)
- **CVE-2026-59357 (Cloud Foundry UAA):** An authentication-code check in the OIDC login flow can be skipped, letting an authenticated user establish a session without the proper exchange. [CIRCL detail](https://vulnerability.circl.lu/vuln/CVE-2026-59357)
- **CVE-2026-106016 (Firefox):** A mitigation bypass in the file-handling component, fixed in Firefox 157.0.1 — update your browser. [CIRCL detail](https://vulnerability.circl.lu/vuln/CVE-2026-106016)
- **CVE-2026-82531 (Smarty):** A code-injection bug in the PHP template engine's multi-component template inheritance; update Smarty to 4.5.8+ / 5.8.5+. [CIRCL detail](https://vulnerability.circl.lu/vuln/CVE-2026-82531)

### IOC sample (block-and-hunt; do not visit)

- **ClearFake (fake-update malware):** domains `samruby.vn`, `pixel-ninjas.de`, `pchtaxadvisors.com` · [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/js.clearfake)
- **Vidar (info-stealer):** URL `https://hi.333vip.org/` · domain `hi.333vip.org` · [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/win.vidar)
- **XWorm (remote-access trojan):** C2 addresses `31.56.209.48:7007`, `84.38.133.22:1012` · [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/win.xworm)
- **SmartApeSG (fake-browser malware):** domain `sunstonejetty.info` · [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/js.smartapesg)
- **Fake ScreenConnect installer (malware in disguise):** `https://omskin.org/lnvoice/ScreenConnect.ClientSetup.msi` · [URLhaus](https://urlhaus.abuse.ch/url/3943736/)

---

*Compiled from public sources · 10-06-2026*
