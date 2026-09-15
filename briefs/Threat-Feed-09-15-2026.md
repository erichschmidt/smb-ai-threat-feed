---
type: threat-feed-note
title: "Threat Feed — 09-15-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-09-15
updated: 2026-09-15
---

# Threat Feed — 09-15-2026

**Reader promise:** 3-minute read. Skim the headlines and the Jargon buster, then do Monday's action on anything that applies. Full glossary: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).

## How to read the scores
- **KEV** = CISA's list of flaws being **actively exploited right now**. On the list = real, not theoretical. "CISA confirmed" = the date it was added. "Federal deadline" = when US agencies must patch (good urgency anchor for everyone).
- **EPSS** = a 0–1 score estimating how likely a flaw is to be exploited in the next 30 days. Higher = patch first. Percentile = where that ranks vs all known flaws (90th percentile = more likely to be exploited than 90% of known vulnerabilities).
- **CVSS** = how bad it is *if* it works (0–10). 9.8 = exploitable remotely with no login.

---

## 1. CRITICAL — One password from any app you've connected can make an attacker the admin of every account on your login server
**CVE-2026-91998 (Casdoor)** · CVSS 9.9/10 · Published 09-15-2026

Casdoor (a self-hosted login/identity server — the system other apps check with to confirm who a user is) mishandled its `/api/mcp` connector endpoint. Any application's client ID and secret was accepted as proof of authority to administer users across **all** organizations on that server.

**What broke** — It's an authorization failure, not a password guess: the server checked that the caller held an application credential, then let that credential manage any user, in any organization, including creating new admins. `/api/mcp` is the connector endpoint AI assistants and agents use to reach other systems — the same style of plug-in access that now sits inside lots of internal tooling. All versions up to and including 4.4.0 are affected.

**Why it matters to an SMB running AI tools** — Self-hosted identity servers are the front gate for internal apps, dashboards, and increasingly for AI helpers that authenticate as a service account. If a helper's credential sits in a shared config, a wiki, an old contractor's laptop, or a public repo, that single key becomes a master key to every account on the server — including the accounts your automation runs as.

**Attacker view (conceptual)** — Find an internet-reachable Casdoor instance → obtain *any* legitimately issued app credential (leaked config, shared secret, or a low-value integration account) → call the `/api/mcp` endpoint to create or take over an admin → use that admin to reach everything the login server protects. Defender observables: new or renamed admin users, `/api/mcp` calls in web logs, app-credential use from unfamiliar IPs, and changes to application registrations.

**What you do Monday** (20 minutes)
1. If you run Casdoor, update to a release newer than 4.4.0 as soon as it is available, and check the advisory links below for the fix release.
2. Rotate every application client secret in Casdoor, then review the user list for admin accounts nobody recognizes.
3. Do not expose the identity server's API to the open internet — put it behind your VPN or a reverse proxy that requires its own login.

**Sources:** [VulnCheck advisory](https://www.vulncheck.com/advisories/casdoor-through-4.4.0-cross-organization-user-administration-via-api-mcp) · [Researcher writeup (geo-chen/oss)](https://github.com/geo-chen/oss/blob/main/casdoor.md) · [CIRCL lookup record](https://vulnerability.circl.lu/vuln/CVE-2026-91998) · [NVD (CVE-2026-91998)](https://nvd.nist.gov/vuln/detail/CVE-2026-91998)

---

## 2. HIGH — Read-only users on your automation server can read every password your jobs use
**CVE-2026-91994 (Semaphore UI)** · CVSS 7.1/10 · Published 09-15-2026

Semaphore UI (a self-hosted control panel that runs scheduled automation jobs, often Ansible) skipped permission checks on read requests. A project member with the lowest possible role — guest, or task-runner — could read the project's full environment settings, including plaintext secrets, credentials, and passwords.

**What broke** — The permission middleware (the code that decides who may see what) exempted GET and HEAD requests from checks. So an account that was supposed to be able to *do nothing* could simply *read* the job configuration. Anything stored as plaintext — cloud keys, database passwords, API keys your jobs use — came back in the response. All versions up to and including 2.19.12 are affected.

**Why it matters to an SMB running AI tools** — This is the keys-to-the-automation problem. Semaphore holds the credentials your scheduled jobs use: cloud API keys, model-provider API keys, database passwords, deployment tokens. Anyone with read access inherits your automation's authority without needing to break anything — and the lowest-privilege accounts are usually the ones handed to contractors, interns, or "view-only" stakeholders.

**What you do Monday** (25 minutes)
1. Update Semaphore to a release newer than 2.19.12.
2. Rotate every credential stored in Semaphore environments after patching — assume anything readable may have been read.
3. Review project membership: remove guest and task-runner accounts that don't need to exist, and check server logs for read requests to the environment endpoint from those accounts.

**Sources:** [Maintainer issue (semaphoreui/semaphore #4150)](https://github.com/semaphoreui/semaphore/issues/4150) · [VulnCheck advisory](https://www.vulncheck.com/advisories/semaphore-ui-through-2.19.12-missing-authorization-on-get-and-head-requests) · [CIRCL lookup record](https://vulnerability.circl.lu/vuln/CVE-2026-91994) · [NVD (CVE-2026-91994)](https://nvd.nist.gov/vuln/detail/CVE-2026-91994)

---

## 3. WATCH — Foreign AI firms are mass-extracting answers from US AI models to train their own, and they hide behind proxy accounts
**CISA/NSA/FBI joint advisory AA26-251A** · Published 09-08-2026

US agencies warned that AI companies in China have run industrial-scale distillation campaigns against US frontier models since at least late 2024 — extracting model behavior through millions of API calls, then using those answers to train their own models.

**What broke** — Nothing broke; this is an abuse pattern. The agencies say the campaigns route requests through multiple paths — direct API accounts, cloud providers, third-party aggregators that strip identifying information, and a gray market of API proxies the advisory calls "transfer stations" that resell access and bypass regional restrictions and usage limits. Recommended countermeasures include detecting anomalous usage, altering responses for suspected distillation attempts, and sharing intelligence across providers.

**Why it matters to an SMB running AI tools** — The transfer-station market runs on credentials, and shared or leaked business API keys are its raw material. If your business shares one model API key across staff and contractors, a key that leaks can be resold and burned at industrial volume — on your card and under your name. This is also a vendor question: if you build on a model from a supplier whose own model was built by extracting a competitor's, you carry the legal and continuity risk of their dispute.

**What you do Monday** (15 minutes)
1. Stop sharing one API key across people. Issue a separate key per user or per automation, with a spend cap, and revoke unused ones.
2. Open your model-provider usage dashboard and look for any day where token volume doesn't match your business activity — a resold key shows up as sudden overnight bulk usage.
3. When you build a product on someone else's model API, read their abuse-monitoring and acceptable-use terms, because that is where your account can be suspended from.

**Sources:** [CISA joint advisory AA26-251A](https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-251a)

---

## 4. CRITICAL — Your email security gateway has a hole attackers are using right now, and the patch deadline is 09-17-2026
**CVE-2026-76461 (Cisco Secure Email Gateway, AsyncOS)** · KEV: CISA confirmed active exploitation 09-14-2026 · Federal deadline 09-17-2026 · Ransomware use: Unknown

Cisco's email security appliance has a SQL injection (a flaw where malicious input is treated as database commands) that lets an unauthenticated, remote attacker run commands with root privileges on the appliance's underlying operating system. No EPSS score yet — it was added to CISA's exploited list yesterday, which is the stronger signal anyway.

**What broke** — The appliance failed to neutralize attacker input before passing it to a database operation, and the result runs with full system rights. Because this is an email gateway — the box that inspects every inbound message — think of it as "one crafted request away from total control of the machine that reads all your mail."

**Why it matters to an SMB running AI tools** — Your email gateway is the choke point where inbound mail is filtered and where attachments and links are handled before a person or an AI mail assistant ever sees them. A gateway with root-level exposure is a foothold on the edge of your network, and it also sees the mail flow that feeds mail-reading AI tools. CISA requires federal agencies to patch by 09-17-2026.

**What you do Monday** (15 minutes)
1. Check your Cisco Secure Email Gateway version against the Cisco advisory below and apply the vendor fix — do this before 09-17-2026 if the appliance has any internet exposure.
2. Confirm the gateway's management interface is not reachable from the internet.
3. Review the appliance for unexpected accounts, scheduled tasks, or configuration changes made outside your change windows.

**Sources:** [Cisco security advisory](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-esa-inj-2bLVGmhX) · [NVD (CVE-2026-76461)](https://nvd.nist.gov/vuln/detail/CVE-2026-76461) · [CISA alert — one KEV addition](https://www.cisa.gov/news-events/alerts/2026/09/14/cisa-adds-one-known-exploited-vulnerability-catalog)

---

## 5. CRITICAL — The console that manages your firewalls can be reached without a login, and it tops today's likelihood ranking
**CVE-2026-20079 (Cisco Secure Firewall Management Center / Security Cloud Control)** · KEV: CISA confirmed active exploitation 09-09-2026 · Federal deadline 09-12-2026 · Ransomware use: Unknown · EPSS 0.7575 (99.5th percentile)

An authentication bypass (a flaw that gets you past a login you should have had to pass) in Cisco's firewall management software and its cloud firewall-management service lets an unauthenticated remote attacker execute script files. EPSS 0.7575 means roughly a 76% estimated chance of exploitation in the next 30 days — higher than 99.5% of all known vulnerabilities — and the federal patch deadline has already passed.

**What broke** — The management software accepted requests through an alternate path that skipped the authentication check. This is the console that writes the rules for every firewall it manages, so a bypass here means an attacker can change the boundaries that protect everything behind them — not just read something.

**Why it matters to an SMB running AI tools** — Firewall rules are what keep your internal AI services, model endpoints, and automation dashboards off the public internet. If the management console can be reached without a login, the rules are attacker-editable. It also sits high in the likelihood ranking for a reason: this class of Cisco management console gets scanned widely.

**What you do Monday** (20 minutes)
1. Apply the Cisco fix for your Secure Firewall Management Center / Security Cloud Control version — treat this as overdue since the deadline was 09-12-2026.
2. Restrict management access to the console to an internal management network or VPN only.
3. Review admin login and configuration-change logs since early September for activity you can't attribute.

**Sources:** [Cisco security advisory](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-onprem-fmc-authbypass-5JPp45V2) · [NVD (CVE-2026-20079)](https://nvd.nist.gov/vuln/detail/CVE-2026-20079) · [CISA alert — four KEV additions](https://www.cisa.gov/news-events/alerts/2026/09/09/cisa-adds-four-known-exploited-vulnerabilities-catalog)

---

## Jargon buster
- **Ansible:** A common automation tool that runs "playbooks" — lists of steps that configure servers and deploy software. Its job settings often hold the passwords those steps need.
- **Authentication bypass:** A flaw that lets someone get past a login or permission check they should have had to pass.
- **Authorization bypass:** A flaw that lets someone who *is* logged in do things they were never granted permission to do. Different from breaking in — they walk through the wrong door.
- **Casdoor:** A self-hosted login/identity server that other apps check with to confirm who a user is. Treat it as production, not a side project.
- **CI/CD (Continuous Integration / Continuous Delivery):** Automated build-and-deploy — code changes are tested, built, and shipped automatically. The pipeline that turns your code into running software, and a place tokens and secrets often live.
- **CISA (Cybersecurity and Infrastructure Security Agency):** The US federal agency that tracks exploited vulnerabilities and publishes guidance. Their "known exploited" list is the closest thing to an authoritative "this is real right now" signal.
- **CVE (Common Vulnerabilities and Exposures):** A unique ID (e.g., CVE-2026-91998) for a publicly disclosed security flaw, so everyone can track the same bug across vendors and scanners. Like a license plate for a vulnerability.
- **CVSS:** A 0–10 severity score for a flaw. 9.8/10 = critical — typically exploitable remotely with no login. Useful for "how bad if it works"; EPSS/KEV answer "is it being used."
- **EPSS (Exploit Prediction Scoring System):** A score (0 to 1) estimating how likely a vulnerability is to be exploited in the wild soon. Higher = patch first. Percentile = where that score ranks vs all known vulnerabilities (99.5th = top half-percent most likely).
- **Email gateway:** The appliance or service that inspects inbound and outbound email before it reaches a mailbox. A hole here is a hole in everything that reads your mail, including AI mail assistants.
- **Environment variables (in automation tools):** The saved settings a job runs with — often cloud keys, database passwords, and API keys. If they're stored as plaintext, anyone who can read the job can read the keys.
- **FMC / Firewall Management Center:** Cisco's centralized panel for managing many firewalls. A hole here lets an attacker rewrite the rules that protect your network.
- **Identity provider (IdP) / single sign-on (SSO):** The service that holds user accounts and tells other apps "this person is who they say they are." Compromise it and you compromise every app that trusts it.
- **KEV (Known Exploited Vulnerabilities) catalog:** CISA's list of vulnerabilities that are being actively exploited right now. If a flaw is on this list, it's not theoretical — patch it.
- **Knowledge distillation (in AI):** Training a new model to imitate another model's answers by feeding it huge volumes of the original model's outputs. Legitimate as a technique; abusive when it's mass extraction against a provider's terms.
- **MCP (Model Context Protocol):** The plug-in style that lets an AI assistant use extra tools (files, notes, browsers, databases). A hole in an MCP endpoint is a hole in whatever that assistant can reach.
- **Plaintext:** Stored so anyone can read it, with no encryption. A secret kept in plaintext is only protected by who is allowed to open the file.
- **Root privileges:** The highest level of access on a Linux/Unix system — the equivalent of "administrator" on Windows. Root means the attacker owns the machine.
- **Semaphore UI:** A self-hosted control panel that runs scheduled automation jobs, often Ansible playbooks. It stores the credentials those jobs use.
- **SQL injection:** A technique where attackers type malicious database commands into an input box (or a request), tricking the app into running unauthorized queries — reading, changing, or deleting data.
- **Transfer station (AI API proxy):** A gray-market reseller of access to AI model APIs that hides the real customer and bypasses regional restrictions and usage limits. Often runs on leaked or purchased API keys.

---

## Appendix

### Actively exploited vulnerabilities (CISA KEV) — ranked by EPSS
Ranked by likelihood of exploitation; CISA confirmed each is being actively used.

| CVE | Product | CISA confirmed | Federal deadline | EPSS | Source |
|-----|---------|----------------|------------------|------|--------|
| CVE-2026-20079 | Cisco Secure Firewall Mgmt (FMC/SCC) | 09-09-2026 | 09-12-2026 | 0.7575 | [Cisco](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-onprem-fmc-authbypass-5JPp45V2) |
| CVE-2026-85706 | GitLab CE/EE | 09-11-2026 | 09-14-2026 | 0.1111 | [GitLab](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-3-2-released/) |
| CVE-2026-19490 | Citrix NetScaler ADC/Gateway | 09-09-2026 | 09-12-2026 | 0.056 | [Citrix](https://support.citrix.com/external/article/CTX696939/netscaler-adc-and-netscaler-gateway-secu.html) |
| CVE-2025-25249 | Fortinet FortiOS / FortiSwitchManager | 09-09-2026 | 09-12-2026 | 0.024 | [Fortinet](https://fortiguard.fortinet.com/psirt/FG-IR-25-084) |
| CVE-2026-86060 | MikroTik RouterOS | 09-10-2026 | 09-13-2026 | 0.0102 | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-86060) |
| CVE-2026-42018 | JFrog Artifactory | 09-11-2026 | 09-25-2026 | 0.0092 | [JFrog](https://docs.jfrog.com/releases/docs/jfrog-security-advisories) |
| CVE-2026-42016 | JFrog Artifactory | 09-11-2026 | 09-25-2026 | 0.0089 | [JFrog](https://docs.jfrog.com/releases/docs/jfrog-security-advisories) |
| CVE-2026-67277 | MikroTik RouterOS | 09-10-2026 | 09-13-2026 | 0.0086 | [MikroTik](https://mikrotik.com/supportsec/september-2026-vulnerability/) |
| CVE-2026-87491 | Chromium V8 (Chrome/Edge) | 09-09-2026 | 09-23-2026 | 0.0086 | [Chrome releases](https://chromereleases.googleblog.com/2026/09/stable-channel-update-for-desktop_0808145027.html) |
| CVE-2026-84869 | ConnectWise ScreenConnect | 09-11-2026 | 09-14-2026 | 0.0069 | [ConnectWise](https://www.connectwise.com/company/trust/security-bulletins/2026-09-08-screenconnect-bulletin) |
| CVE-2026-76461 | Cisco Secure Email Gateway (AsyncOS) | 09-14-2026 | 09-17-2026 | not yet scored | [Cisco](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-esa-inj-2bLVGmhX) |

*Ransomware-use flag: "Unknown" for all items above — CISA has not labeled any of today's KEV entries as known ransomware-campaign use.*

### Ransomware victim pulse (ransomware.live)
Sector signal for the last 24h: **Manufacturing** and **Professional Services** were hit hardest, with Technology and Transportation behind them.

| Group | Sector | Country | Discovered |
|-------|--------|---------|------------|
| Panzer | Manufacturing | PE | 09-15-2026 |
| iah6477 | Manufacturing | US | 09-15-2026 |
| ShadowByt3$ | Other | US | 09-15-2026 |
| anubis | Professional Services | — | 09-14-2026 |
| unsafe | Technology | US | 09-14-2026 |
| qilin | Manufacturing | US | 09-14-2026 |
| qilin | Professional Services | US | 09-14-2026 |
| qilin | Transportation | US | 09-14-2026 |
| qilin | Other | — | 09-14-2026 |
| insomnia | Professional Services | US | 09-14-2026 |

Source: [ransomware.live](https://www.ransomware.live)

### Notable new CIRCL vulnerabilities
- **CVE-2026-91998 (Casdoor)** — application-credential authorization bypass in the `/api/mcp` endpoint; cross-organization user administration. See Item 1.
- **CVE-2026-91994 (Semaphore UI)** — missing authorization on GET/HEAD; guest and task-runner roles can read plaintext job secrets. CVSS 7.1. See Item 2.
- **CVE-2026-91997 (evolution-api)** — the IP-allowlist check for the `/metrics` endpoint fails, so unauthenticated callers can read the metrics endpoint. Relevant if you run self-hosted messaging-automation platforms. [CIRCL](https://vulnerability.circl.lu/vuln/CVE-2026-91997)
- **CVE-2026-89308 (PHP `ping.php` endpoint)** — unauthenticated OS command injection leading to remote code execution. Published 09-15-2026; check the vendor advisory in the CIRCL record before exposing any diagnostic page. [CIRCL](https://vulnerability.circl.lu/vuln/CVE-2026-89308)
- **CVE-2026-42508 (certificate-authority key revocation)** — a revoked signing key was not checked correctly during certificate validation; EPSS 0.0731 (94th percentile), the highest-scoring non-item CIRCL entry today. [CIRCL](https://vulnerability.circl.lu/vuln/CVE-2026-42508)
- **CVE-2026-91994/91996/91993 family (self-hosted ops tools)** — the same batch includes `lamp-cloud` (unauthenticated JVM property disclosure) and `Jpom` (cross-workspace repository access). Worth a scan if you run any of these internally. [CIRCL](https://vulnerability.circl.lu/recent)

### IOC sample (abuse.ch)
Malicious domains / addresses to block and hunt — **do not visit**.
- **ClearFake** (fake browser-update malware) domain: `botcheck-cf.top` ([Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/js.clearfake))
- **PHP webshell** host: `86roaaiuf2.workers.dev` ([Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/php.shin_webshell))
- **Aisuru** botnet C2 IP:port: `161.35.197.52:8443` ([Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/elf.aisuru))
- **Jackskid** C2 IP:port set: `31.58.171.101:443`, `31.58.171.10:443`, `31.58.171.61:443` ([Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/elf.jackskid) · [research repo](https://github.com/deepfield/public-research/tree/main/jackskid))
- **Unknown malware** C2 IP:port: `45.155.69.81:8070`, `45.155.69.81:8090` ([sandbox report](https://tria.ge/260914-zarl1avtfv/behavioral1))
- **URLhaus** active malicious download URLs: `27.215.55.48:39346/bin.sh`, `www.2bxvrc1.com/load915`, `222.137.4.182:59398/i`, `61.52.158.123:45471/Mozi.m`, `49.73.228.94:3588/i`. Entry pages: [3917019](https://urlhaus.abuse.ch/url/3917019/) · [3917018](https://urlhaus.abuse.ch/url/3917018/) · [3917017](https://urlhaus.abuse.ch/url/3917017/) · [3917016](https://urlhaus.abuse.ch/url/3917016/) · [3917014](https://urlhaus.abuse.ch/url/3917014/)

---

*Compiled from public sources · 09-15-2026*
