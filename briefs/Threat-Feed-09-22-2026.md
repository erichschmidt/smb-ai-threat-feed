---
type: threat-feed-note
title: "Threat Feed - 09-22-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-09-22
updated: 2026-09-22
---

# Threat Feed — 09-22-2026

**3-minute read:** Skim the headlines, then the Jargon buster at the bottom. If a term is new, it's defined there. Full glossary lives at [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).

## How to read the scores
- **EPSS** is a 0-to-1 number estimating how likely a flaw is to be exploited in the next 30 days. Higher = patch first. The percentile tells you where it ranks: 96th percentile = more likely to be exploited than 96% of all known vulnerabilities.
- **CVSS** is a 0-to-10 severity score for "how bad if it works." 9.8/10 = critical — typically exploitable remotely with no login. CVSS says how bad; EPSS and the KEV list answer "is it actually being used."
- **KEV** is CISA's list of flaws being actively exploited right now. If a flaw is on it, it's not theoretical — patch it.

---

## Item 1 — WATCH — Your threat-intel sharing platform can be hijacked by a crafted link to run its analysis tools

**CVE-2026-95658** and **CVE-2026-95659** in MISP (an open-source platform teams use to share threat intelligence and indicators with each other). Both published 09-22-2026. CVSS not yet rated; not on the KEV list yet — treat as "patch on your own schedule," not an emergency.

**What broke:** Two separate flaws in MISP, the platform many security teams use to share and automate threat data:
- One lets a crafted web link inject a script into the analyst's own browser session (a reflected XSS — cross-site scripting — tricking a logged-in user's browser into running attacker code). The attacker doesn't break in; they get the *analyst's* browser to do something on their behalf.
- The other exposes MISP's workflow-execution action so the usual safety checks (CSRF — cross-site request forgery — the check that stops a random website from making your logged-in session do things) are disabled. An attacker can trigger MISP's analysis modules to run without a valid token.

**Why it matters to an SMB running AI tools:** If your team runs MISP to automate threat-intel ingestion or to feed indicators into your security automation, these are holes in that automation. The second flaw means someone who can reach your MISP can invoke its module/analysis workflows without authorization — a way to waste compute or abuse your automation. This is a "patch MISP when you next update" item, but a real one.

**Attacker view (conceptual):** Attacker finds your MISP instance → sends the analyst a link or gets a request that reaches the exposed workflow action → MISP runs its analysis module without the login check → the attacker gets the module's behavior (and any data it touches) as if they were an authorized operator.

**What you do Monday:**
1. Update MISP to the version that fixes CVE-2026-95658 and CVE-2026-95659. (30 minutes)
2. Confirm your MISP instance is not exposed to the internet — it should only be reachable from inside your network. (15 minutes)
3. If you have any doubts, ask your IT person: "Is our MISP patched for the two CVEs published 09-22-2026?" (10 minutes)

**Sources:** [CIRCL advisory CVE-2026-95659](https://vulnerability.circl.lu/vuln/CVE-2026-95659) · [CIRCL advisory CVE-2026-95658](https://vulnerability.circl.lu/vuln/CVE-2026-95658)

---

## Item 2 — HIGH — Your "chat with your data" AI can still be tricked into rewriting the database behind it

**CVE-2024-8309** in LangChain's GraphCypherQAChain (a helper that turns a chat question into a database query). CVSS 9.8/10 (critical — exploitable remotely with no login). EPSS 0.1374 — 96th percentile: more likely to be exploited than 96% of known vulnerabilities. This is the same finding flagged yesterday — if you haven't acted yet, today's the day, because it remains the single highest-likelihood AI-lens vulnerability in sight.

**What broke:** LangChain is one of the most-used frameworks for building AI tools that answer questions from your business data. Its GraphCypherQAChain (the component that translates a question into a query for a graph database — a database that stores records and their relationships as connected points) is vulnerable to SQL injection (tricking software into running unauthorized database commands) through prompt injection. An attacker hides instructions inside the data the AI reads, and the AI obediently runs a query that reads, changes, or deletes data it should never touch. You don't need the mechanism detail — just know the fix belongs to whoever built the tool, not to you as a user.

**Why it matters to an SMB running AI tools:** If you (or a vendor you use) built a "chat with your records" assistant on LangChain's graph-query chain, this is a direct hole in that assistant. The AI is the front door, and the database it reads is the prize. Because LangChain is everywhere, one flaw here touches a lot of AI tools at once.

**What you do Monday:**
1. Ask whoever built your AI assistant (vendor or in-house dev): "Are you on a patched LangChain that fixes CVE-2024-8309?" If no, ask them to update. (15 minutes)
2. If you run it yourself, update `langchain-community` to the patched version that includes the fix commit. (30 minutes)
3. Check that the AI's database account has least privilege — read-only for the tables the assistant answers from, no ability to delete. (30 minutes)

**Sources:** [GitHub advisory (GHSA-45pg-36p6-83v9)](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [huntr bounty report](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5) · [LangChain fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255)

---

## Item 3 — HIGH — Your office network switches have a hole CISA confirms is being actively exploited

**CVE-2026-7273** in Zyxel GS1900 Series network switches. EPSS 0.0032 (25th percentile). CISA added it to its known-exploited list on 09-21-2026; federal deadline 09-24-2026. Ransomware use: not flagged.

**What broke:** The GS1900 series switches have a stack-based buffer overflow (a memory bug in the switch's web-management CGI program) that a LAN-based, unauthenticated attacker (someone already on your network, needing no login) can trigger with a crafted HTTP request — potentially to execute operating-system commands on the switch. The important part for you: it requires the attacker to already be inside your network.

**Why it matters to an SMB running AI tools:** Your network switches are the plumbing that carries every connection — including to your AI services and the data stores they read. A switch that's been hijacked lets an attacker re-route, capture, or drop that traffic. Because this one needs a foothold inside your LAN, it's a follow-on move, but a nasty one once someone is in.

**Attacker view (conceptual):** Attacker already on your network → sends a crafted HTTP request to the switch's web-management port → stack-based buffer overflow runs their command → the switch now does what the attacker wants (reroute traffic, disable segmentation). Keep the management panel off the internet and off untrusted VLANs to deny the trigger point.

**What you do Monday:**
1. Check whether you run Zyxel GS1900 series switches. If yes, apply Zyxel's firmware fix for CVE-2026-7273. (30 minutes)
2. Confirm the switch's web-management interface is not reachable from the internet or from untrusted guest Wi-Fi — only from your admin network. (15 minutes)
3. If you don't know what switches you run, ask your IT person: "Do we run Zyxel GS1900 switches, and are they patched against CVE-2026-7273?" (10 minutes)

**Sources:** [Zyxel security advisory](https://www.zyxel.com/global/en/support/security-advisories/zyxel-security-advisory-for-stack-based-buffer-overflow-vulnerability-in-gs1900-series-switches-06-16-2026) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-7273) · [CISA KEV alert (09-21-2026)](https://www.cisa.gov/news-events/alerts/2026/09/21/cisa-adds-one-known-exploited-vulnerability-catalog)

---

## Item 4 — WATCH — Ransomware crew targets US manufacturing and a lending company this morning

**Ransomware.live, last 24 hours:** the "termite" group posted three US victims on 09-22-2026 — a Colorado cable-management manufacturer (Sealcon), a wholesale mortgage lender (theLender), and a real-estate investment firm (TruAmerica). A separate US professional-services posting (NAI Earle Furman real estate brokerage) also landed today. In all, 10 victim disclosures in the last day across the US, Uzbekistan, Brazil, Japan, and Finland.

**What broke:** These are attacker claims on leak sites, not confirmed incidents — but the cluster is a clear sector-targeting signal. The mortgage lender hit and the real-estate/professional-services hits point at firms that hold large volumes of financial and personal data. Financial Services and Professional Services are the sectors in the crosshairs today.

**Why it matters to an SMB running AI tools:** If you operate in financial services, professional services, or any business holding customer financial records, ransomware crews are actively fishing in that pond right now. Your AI assistants and automations read the same data these crews want to lock for ransom — so the backup-and-recovery hygiene that protects your data also protects what your AI depends on.

**What you do Monday:**
1. Test that your backups actually restore — don't assume. Run one real restore drill on a test machine. (45 minutes)
2. Confirm MFA is enforced on all admin and financial-system accounts (the single cheapest defense against stolen passwords). (20 minutes)
3. Make sure offline or remote-recovery backups exist for your most sensitive data — a threat actor can delete the online copies. (30 minutes)

**Sources:** [Ransomware.live](https://www.ransomware.live) (attacker claims only — do not visit linked leak sites)

---

## Item 5 — WATCH — Fake-update malware and remote-access trojans are the active threat stream this morning

**ThreatFox / URLhaus, last 24 hours:** ClearFake (malware that pretends to be a browser or software update) is live on the domain `morning-coffee-ritual.us` and via a fake-update URL. Remus (a remote-access trojan — malware that gives an attacker remote control of a machine) is reachable on two shop domains, and a PureLogs Stealer (malware that steals saved passwords and crypto-wallet files) is live on an IP:port. Six active malicious URLs are confirmed online.

**What broke:** This is the routine but active criminal stream: fake-update pages that try to infect visitors, and command posts for remote-control malware. ClearFake pages masquerade as legitimate update prompts; the other signals are addresses attackers use to control infected machines and exfiltrate stolen data.

**Why it matters to an SMB running AI tools:** Your team is the vector — the person who clicks a "your browser is out of date" prompt on a business machine, or opens an unsolicited attachment. A remote-access trojan on a machine that has access to your AI tools' data sources (document libraries, databases, CRM) turns into a path to everything those tools read.

**What you do Monday:**
1. Share one line with your team: fake "update your browser" pop-ups are the top attack right now — if it pops up, close the tab, don't click. (5 minutes)
2. Confirm browser auto-update is on so nobody is handed a fake-update prompt. (10 minutes)
3. If you use a blocklist-based filter on your firewall/DNS, confirm these listed IOC domains are blocked and add any that aren't. (15 minutes)

**Sources (block-and-hunt — do not visit):** [ClearFake (Malpedia)](https://malpedia.caad.fkie.fraunhofer.de/details/js.clearfake) · [Remus (Malpedia)](https://malpedia.caad.fkie.fraunhofer.de/details/win.remus) · [PureLogs Stealer (Malpedia)](https://malpedia.caad.fkie.fraunhofer.de/details/win.purelogs) · [URLhaus](https://urlhaus.abuse.ch/url/3920926/)

---

## Jargon buster
- **Reflected XSS (cross-site scripting):** A crafted link that makes a logged-in user's own browser run attacker-supplied script — so the attacker leverages the person's session without breaking in.
- **CSRF (cross-site request forgery):** The check that stops a random website or crafted link from making your already-logged-in session perform actions. Disabling it means an outsider can trigger actions as if they were you.
- **Stack-based buffer overflow:** A memory bug where software writes past the space it allocated on its call stack. Attackers use it to run their own code on the device.
- **Graph database / Cypher:** A graph database stores records and their relationships as connected points; Cypher is its query language. AI tools may query it to answer questions about linked business records.
- **SQL injection:** A technique where attackers type malicious database commands into an input box (or a prompt), tricking the app into running unauthorized queries — reading, changing, or deleting data.
- **Prompt injection:** Tricking an AI by putting instructions inside the data it reads — the AI follows the attacker's instructions instead of the user's.
- **Least privilege:** Giving a person or software account only the access it needs for its job, and no more.
- **RAT (Remote Access Trojan):** Malware that gives an attacker remote control of a machine, like a ghost at your keyboard.
- **IOC (Indicator of Compromise):** A trace left behind by an attack — a malicious IP address, domain, URL, or file hash. Finding one in your logs means something bad touched your network.
- **KEV / EPSS / CVSS:** See "How to read the scores" above.

---

## Appendix

### CISA KEV — ranked by EPSS (highest exploitation likelihood first)
| CVE | Product | CISA confirmed | Federal patch by | Ransomware use | EPSS | Source |
|-----|---------|----------------|------------------|----------------|------|--------|
| CVE-2025-39682 | Linux Kernel (TLS) | 09-18-2026 | 09-21-2026 | Unknown | 0.012 (67th pct) | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2025-39682) |
| CVE-2025-39964 | Linux Kernel (socket race) | 09-18-2026 | 09-21-2026 | Unknown | 0.0079 (55th pct) | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2025-39964) |
| CVE-2026-76460 | Cisco ISE | 09-16-2026 | 09-19-2026 | Unknown | 0.0078 (55th pct) | [Cisco](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-ISE-ABP-VNSW7Tn5) |
| CVE-2026-7273 | Zyxel GS1900 switches | 09-21-2026 | 09-24-2026 | Unknown | 0.0032 (25th pct) | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-7273) |
| CVE-2026-53266 | Linux Kernel (ebtables) | 09-18-2026 | 09-21-2026 | Unknown | 0.0028 (20th pct) | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-53266) |
| CVE-2026-87886 | Acronis Backup (cPanel/Plesk) | 09-16-2026 | 09-19-2026 | Unknown | 0.0025 (17th pct) | [Acronis](https://security-advisory.acronis.com/advisories/SEC-10986) |
| CVE-2026-58704 | Google Pixel (cellular modem) | 09-16-2026 | 09-19-2026 | Unknown | 0.0021 (11th pct) | [Android bulletin](https://source.android.com/docs/security/bulletin/pixel/2026/2026-09-01) |

*All KEV items: CISA confirmed active exploitation as of the "CISA confirmed" date. "Ransomware use: Unknown" means CISA has not flagged it as used in ransomware campaigns.*

### Ransomware sector pulse (Ransomware.live, last 24h)
- **termite** — US Manufacturing (Sealcon), US Financial Services (theLender mortgage), US real estate (TruAmerica)
- **secp0** — US Professional Services (real estate brokerage)
- **N0n** — Retail & E-Commerce (UZ retail vendor)
- **metaencryptor** — Manufacturing (JP automotive parts)
- **play** — Manufacturing (BR), Other (US)
- **SilentRansomGroup** — Professional Services (names partially redacted)

Sector signal: financial services, professional services, and US real estate in the crosshairs today — firms holding large volumes of financial and personal data. These are attacker claims, not proof of incidents — treat them as "this sector is being hunted" signals.

**Source:** [Ransomware.live](https://www.ransomware.live)

### Notable CIRCL findings (high-signal)
- **CVE-2024-8309** (LangChain GraphCypherQAChain SQL injection) — EPSS 0.1374, 96th percentile. Covered as Item 2. [GHSA](https://github.com/advisories/GHSA-45pg-36p6-83v9)
- **CVE-2026-95659 / 95658** (MISP threat-intel platform, published 09-22-2026) — reflected XSS and workflow CSRF bypass. Covered as Item 1. [CIRCL](https://vulnerability.circl.lu/vuln/CVE-2026-95659)
- **CVE-2025-1889** (picklescan model-scan bypass) — EPSS 0.0039. Still relevant for anyone downloading AI models. [GHSA](https://github.com/advisories/GHSA-769v-p64c-89pr)
- **CVE-2026-74849** (ManageEngine ADSelfService Plus remote code execution, published 09-22-2026) — for teams that run the tool. [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-74849)

### IOC sample (ThreatFox / URLhaus, last 24h)
- **ClearFake** (fake-update malware): domain `morning-coffee-ritual.us` — [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/js.clearfake)
- **ClearFake** (fake-update malware): `https://testingcf.jsdelivr.net/gh/e438e-1E-4/60-08-99-68-BE-7B/A84335-B692` — [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/js.clearfake)
- **Remus** (remote-access trojan): `http://bennep.shop:4883/webhooks` — [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/win.remus)
- **Remus** (remote-access trojan): `http://hkealop.shop:9932/reports` — [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/win.remus)
- **PureLogs Stealer**: `89.106.83.156:8799` — [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/win.purelogs)
- **php.shin_webshell** (webshell hosting): `t86gg19h5q.workers.dev`, `sodipo.workers.dev` — [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/php.shin_webshell)
- **URLhaus** (active malicious URLs, all online): e.g. `http://113.228.85.214:50311/bin.sh` and 5 others — [URLhaus](https://urlhaus.abuse.ch/url/3920926/)

*IOCs are block-and-hunt signals. Do not visit listed domains or URLs.*

---

*Compiled from public sources · 09-22-2026*