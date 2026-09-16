---
type: threat-feed-note
title: "Threat Feed — 09-16-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-09-16
updated: 2026-09-16
---

# Threat Feed — 09-16-2026

**Reader promise:** 3-minute read. Skim the headlines and the Jargon buster, then do Monday's action on anything that applies. Full glossary: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).

## How to read the scores
- **KEV** = CISA's list of flaws being **actively exploited right now**. On the list = real, not theoretical. "CISA confirmed" = the date it was added. "Federal deadline" = when US agencies must patch (good urgency anchor for everyone).
- **EPSS** = a 0–1 score estimating how likely a flaw is to be exploited in the next 30 days. Higher = patch first. Percentile = where that ranks vs all known flaws (90th percentile = more likely to be exploited than 90% of known vulnerabilities).
- **CVSS** = how bad it is *if* it works (0–10). 9.8 = exploitable remotely with no login.

**No new actively-exploited vulnerabilities were added to CISA's KEV list today.** The items on the list this week stay on it until patched, and the Cisco email-gateway deadline is tomorrow — it is Item 2 below.

---

## 1. HIGH — Anyone with a back-office login can take every sales lead, delete your approval steps, and read the audit trail
**CVE-2026-92456 and six related CVEs (yshop-crm through 2.1.3)** · CVSS 4.3–6.5/10 (medium) · Published 09-16-2026

Seven authorization bugs in one CRM release. A logged-in back-office user with an ordinary account — not an administrator — can claim unassigned sales leads, delete approval workflow steps, list every user in the system, read the installation-wide audit trail, and change product sale status.

**What broke** — None of these are break-ins. Every one is a missing permission check on an admin-side endpoint (an authorization failure — the software lets someone who *is* logged in do things they were never granted). The lead-claim endpoint (`receiveCustomer`) never verified the caller had sales-lead permission; the workflow endpoint let any back-office account delete approval steps; the user-list check was literally commented out in the code (`@PreAuthorize` disabled); and the operation-log endpoint handed the entire audit trail to any authenticated user. Version 2.1.3 and earlier are affected — check the vendor for a fixed release.

**Why it matters to an SMB running AI tools** — A CRM is the system your lead-routing and approval automations read and write. If the permissions under those automations are wrong, your pipeline acts on tampered records: leads quietly reassigned, approval steps removed so work moves forward that was never signed off, and the audit trail you would use to prove what happened readable by everyone. The least-privileged accounts here are usually the service accounts your automation runs as — exactly the account class that inherits these functions.

**Attacker view (conceptual)** — Get any single staff or contractor credential (leaked, shared, or an old account nobody disabled) → call the admin API endpoints directly instead of using the web screens → claim leads, delete workflow steps, pull the user list and the audit log → the web interface never shows a thing. Defender observables: admin-API calls made by low-privilege accounts, bursts of user-list or operation-log queries, lead-assignment changes with no matching sales activity, and deleted approval steps.

**What you do Monday** (20 minutes)
1. Find out whether you run yshop-crm and on which version — ask your CRM vendor or whoever set it up, and ask for their patch status for the CVEs below.
2. Pull your back-office account list and remove lead-claim, workflow-delete, and audit-log access from anyone who doesn't need it — including the service account your CRM automation uses.
3. Review the operation log for lead claims and deleted workflow steps you can't attribute, especially over the last 30 days.

**Sources:** [GHSA-qwxr-xhwf-5r52 (lead claiming)](https://github.com/advisories/GHSA-qwxr-xhwf-5r52) · [GHSA-h72m-g9jg-f5vg (workflow deletion)](https://github.com/advisories/GHSA-h72m-g9jg-f5vg) · [GHSA-fxr9-cwrf-jj7v (user enumeration)](https://github.com/advisories/GHSA-fxr9-cwrf-jj7v) · [NVD (CVE-2026-92459)](https://nvd.nist.gov/vuln/detail/CVE-2026-92459) · [NVD (CVE-2026-92460)](https://nvd.nist.gov/vuln/detail/CVE-2026-92460)

---

## 2. CRITICAL — Your email security gateway still has a hole being attacked right now, and the patch deadline is tomorrow
**CVE-2026-76461 (Cisco Secure Email Gateway, AsyncOS)** · KEV: CISA confirmed active exploitation 09-14-2026 · Federal deadline 09-17-2026 · Ransomware use: Unknown · EPSS 0.0216 (81st percentile)

A SQL injection (a flaw where attacker input is treated as database commands) in Cisco's email security appliance lets an unauthenticated, remote attacker run commands with root privileges — full control — on the machine that inspects all your mail. CISA's deadline is 09-17-2026, which is tomorrow.

**What broke** — The appliance passed attacker-controlled input into a database operation without neutralizing it, and the result executes with full system rights. Nothing needs to be guessed or phished: the flaw is reachable from the network. EPSS 0.0216 means roughly a 2% estimated chance of exploitation in the next 30 days — an 81st-percentile rank among all known vulnerabilities, so higher-likelihood than four out of five. But the KEV listing is the stronger signal: this is already being used, not predicted.

**Why it matters to an SMB running AI tools** — The email gateway is the choke point where inbound mail, attachments, and links are filtered before a person or an AI mail assistant ever touches them. A gateway at root level is a foothold on your network edge, sitting in front of the mail flow that feeds everything reading your inbox.

**What you do Monday** (15 minutes)
1. Check your Secure Email Gateway version against the Cisco advisory below and apply the vendor fix — treat tomorrow's deadline as your own if the appliance is internet-reachable.
2. Confirm the management interface is not reachable from the internet.
3. Review the appliance for unexpected accounts, scheduled tasks, or config changes made outside your change window.

**Sources:** [Cisco security advisory](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-esa-inj-2bLVGmhX) · [NVD (CVE-2026-76461)](https://nvd.nist.gov/vuln/detail/CVE-2026-76461)

---

## 3. HIGH — Anyone on your office Wi-Fi can pull the saved settings out of your 5G internet box without a password
**CVE-2026-40856 and CVE-2026-58147 (WNC T-Mobile 5G Box IDU router)** · Published 09-16-2026

A backup-internet / fixed-wireless 5G router has a diagnostic web endpoint (`wnc_maccheck.cgi`) reachable with no login that returns sensitive configuration data, including stored credentials. A second flaw lets a logged-in user inject operating-system commands through the password-change page.

**What broke** — Improper access control: the diagnostic CGI page was written to be called without authentication checks, so a device on the same network can simply request it and get back configuration details it should never expose. The second issue is command injection (attacker input runs as an operating-system command) in the portal's password-change handler. Both are adjacent-network flaws — someone on your Wi-Fi or office LAN, not necessarily from the internet. If the box's admin password is still the factory default, the command-injection path becomes much easier to reach.

**Why it matters to an SMB running AI tools** — These boxes are often plugged in as "just backup internet" and treated as nothing, then sit on the flat internal network next to your file server and your self-hosted AI endpoints. Unauthenticated access to stored configuration is how the box's own credentials, your Wi-Fi credentials, or a provider login end up in someone else's hands — and then reused against everything you own. A cheap edge device with a weak login is a quiet path to the inside of your network.

**What you do Monday** (20 minutes)
1. Identify whether you have a WNC 5G IDU router (check the label or ask your internet provider) and ask the provider for the current firmware and any fix for these two CVEs.
2. Put the 5G box on its own network segment or guest VLAN rather than the same network as servers, and change the admin password from the default.
3. If you can't isolate it or patch it, turn off its remote and local web management where the provider allows it.

**Sources:** [NVD (CVE-2026-40856)](https://nvd.nist.gov/vuln/detail/CVE-2026-40856) · [NVD (CVE-2026-58147)](https://nvd.nist.gov/vuln/detail/CVE-2026-58147) · [CIRCL lookup record](https://vulnerability.circl.lu/vuln/CVE-2026-40856)

---

## 4. WATCH — If your local AI runs on a server cluster, the cluster's internal messaging service has a memory bug
**CVE-2026-81665 (Corosync Totem process group)** · EPSS 0.0021 (11.6th percentile) · Published 09-04-2026

Corosync — the messaging service that keeps the nodes of a server cluster in sync — has a heap buffer overflow when it reassembles fragmented multicast messages. The buffer that reassembles the pieces has no runtime bounds check in release builds, so a machine on the cluster's network can send a crafted message and trigger memory corruption.

**What broke** — A heap buffer overflow is a memory bug where software writes past the end of the space it allocated; attackers use these to crash a service or, in the right conditions, run their own code. You don't need the memory-bug detail, just this: the flaw is reachable by another machine on the same network segment, needs no login, and it is in the service that keeps your cluster alive. EPSS 0.0021 is low — an 11.6th-percentile chance of exploitation in the next 30 days — so this is "patch at your next maintenance window," not "drop everything." Published 09-04-2026.

**Why it matters to an SMB running AI tools** — This is where self-hosted AI actually lives for a lot of small teams: a cluster of one or two machines (Proxmox VE and similar) running local models, a vector database, or an inference service. If the clustering service on those hosts can be corrupted by a nearby machine, the thing hosting your private models is the thing at risk — even though your models never touch the internet.

**What you do Monday** (20 minutes)
1. Ask whoever manages your hosts whether Corosync is running — it's present on clustered Proxmox VE setups and Pacemaker clusters. Single-machine installs are not affected.
2. Apply your distribution's Corosync update at the next maintenance window (check your package updates: `apt list --upgradable` on most setups shows it).
3. Keep cluster heartbeat traffic on a private segment or dedicated link that other devices can't reach.

**Sources:** [CIRCL lookup record (CVE-2026-81665)](https://vulnerability.circl.lu/vuln/CVE-2026-81665) · [NVD (CVE-2026-81665)](https://nvd.nist.gov/vuln/detail/CVE-2026-81665)

---

## 5. WATCH — New official guidance on the tokens your automations log in with, because that's what attackers are stealing now
**CISA / NIST interagency report IR 8587** · Published 09-15-2026

CISA and NIST published final guidance on protecting the access tokens and identity assertions that modern cloud logins depend on — the signed credentials behind single sign-on, federation, and API access. The agencies' framing: adversaries target these tokens for forgery, theft, and misuse to move sideways across networks and reach data without breaking a password.

**What broke** — Nothing broke; this is a defensive posture statement, and it matches what we're seeing in the field. Modern automation doesn't log in with a password. It holds a token — a signed credential valid until it expires — and if that token is copied out of a config file, a log, a wiki page, or a compromised laptop, the attacker becomes your automation. No password reset stops them; the token is still valid. The report's guidance covers validation, secrets management, and detection at scale.

**Why it matters to an SMB running AI tools** — Your AI automations and integration jobs are token-based service accounts, and they usually get the broadest permissions in the house because "the automation needs it." A stolen token doesn't need to guess anything, doesn't trigger a failed-login alert, and acts with the full authority of the job it belongs to. This is also the quiet version of last week's mass-extraction story: API credentials are the currency.

**What you do Monday** (20 minutes)
1. List the service accounts and API keys your automations use, write down what each one can reach, and revoke anything you can't explain.
2. Move secrets out of config files, notes, and shared docs into a secret manager or at least an environment store with restricted access — and prefer short-lived tokens over keys that never expire.
3. Check your sign-in logs for the same token or service account in use from two places or two countries at once; that's the tell for a stolen token.

**Sources:** [CISA — Protecting Tokens and Assertions from Forgery, Theft, and Misuse](https://www.cisa.gov/resources-tools/resources/protecting-tokens-and-assertions-forgery-theft-and-misuse-implementation-recommendations-agencies) · [NIST IR 8587 (final)](https://csrc.nist.gov/pubs/ir/8587/final)

---

## Jargon buster
- **Access token / assertion:** The signed digital credential an app or automation presents to prove who it is — a temporary key card. A stolen token lets an attacker act as your service without knowing any password.
- **Approval workflow:** A defined chain of steps a request must pass through for sign-off. If steps can be deleted, approvals happen that never should have.
- **Audit trail / operation log:** The record of who did what in a system, and your evidence when something goes wrong. If every logged-in user can read it, it stops being evidence.
- **Authorization bypass:** A flaw that lets someone who *is* logged in do things they were never granted permission to do. Different from breaking in — they walk through the wrong door.
- **Back-office:** The admin side of a business system, where staff manage customers, leads, orders, and settings.
- **Command injection / OS command injection:** Tricking software into running operating-system commands the attacker chose.
- **Corosync:** The messaging service that keeps the nodes of a server cluster in sync (used by Proxmox VE and similar). A hole here can affect every node in the cluster.
- **CVE (Common Vulnerabilities and Exposures):** A unique ID (e.g., CVE-2026-92459) for a publicly disclosed security flaw, so everyone can track the same bug across vendors and scanners.
- **CVSS:** A 0–10 severity score for a flaw. 9.8/10 = critical — typically exploitable remotely with no login. Medium (4–6.9) usually means the attacker needs an account or local access first. CVSS answers "how bad if it works"; EPSS and KEV answer "is it being used."
- **Email gateway:** The appliance or service that inspects inbound and outbound email before it reaches a mailbox. A hole here is a hole in everything that reads your mail, including AI mail assistants.
- **EPSS (Exploit Prediction Scoring System):** A score (0 to 1) estimating how likely a vulnerability is to be exploited in the wild soon. Higher = patch first. Percentile = where that score ranks vs all known vulnerabilities (99.5th = top half-percent most likely).
- **Heap buffer overflow:** A memory bug where software writes past the space it allocated for data. Attackers use it to crash a service or, in the right conditions, run their own code.
- **Improper access control:** A software flaw where the product fails to check who is allowed to do what — letting an unauthorized user create, read, change, or delete data they shouldn't touch.
- **KEV (Known Exploited Vulnerabilities) catalog:** CISA's list of vulnerabilities that are being actively exploited right now. If a flaw is on this list, it's not theoretical — patch it.
- **Least privilege:** Giving a person or software account only the access it needs for its job, and no more.
- **Proxmox VE:** A popular open-source virtualization platform for running many virtual machines on your own hardware — a common home for self-hosted AI servers.
- **Root privileges:** The highest level of access on a Linux/Unix system — the equivalent of "administrator" on Windows. Root means the attacker owns the machine.
- **Ransomware:** Malware that locks your files and demands payment. The #1 threat to small businesses.
- **SQL injection:** A technique where attackers type malicious database commands into an input box (or a request), tricking the app into running unauthorized queries — reading, changing, or deleting data.
- **Service account:** A non-human login that software uses to talk to other software. If it's stolen, the attacker inherits everything that account can reach.
- **5G fixed wireless (IDU):** A 5G internet box used as primary or backup office internet. Treat it as an untrusted edge device — it is a computer on your network.

---

## Appendix

### Actively exploited vulnerabilities (CISA KEV) — ranked by EPSS
No new additions to the KEV catalog since 09-14-2026; every entry below is still active and still requires patching if you haven't. Ranked by likelihood of exploitation.

| CVE | Product | CISA confirmed | Federal deadline | EPSS | Source |
|-----|---------|----------------|------------------|------|--------|
| CVE-2026-85706 | GitLab CE/EE | 09-11-2026 | 09-14-2026 | 0.1196 (95.9th pct) | [GitLab](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-3-2-released/) |
| CVE-2026-76461 | Cisco Secure Email Gateway (AsyncOS) | 09-14-2026 | 09-17-2026 | 0.0216 (81.2nd pct) | [Cisco](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-esa-inj-2bLVGmhX) |
| CVE-2026-86060 | MikroTik RouterOS | 09-10-2026 | 09-13-2026 | 0.0106 (62.6th pct) | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-86060) |
| CVE-2026-42018 | JFrog Artifactory | 09-11-2026 | 09-25-2026 | 0.0092 (58.4th pct) | [JFrog](https://docs.jfrog.com/releases/docs/jfrog-security-advisories) |
| CVE-2026-42016 | JFrog Artifactory | 09-11-2026 | 09-25-2026 | 0.0089 (57.3rd pct) | [JFrog](https://docs.jfrog.com/releases/docs/jfrog-security-advisories) |
| CVE-2026-67277 | MikroTik RouterOS | 09-10-2026 | 09-13-2026 | 0.0087 (56.8th pct) | [MikroTik](https://mikrotik.com/supportsec/september-2026-vulnerability/) |
| CVE-2026-84869 | ConnectWise ScreenConnect | 09-11-2026 | 09-14-2026 | 0.0069 (50.9th pct) | [ConnectWise](https://www.connectwise.com/company/trust/security-bulletins/2026-09-08-screenconnect-bulletin) |

*Ransomware-use flag: "Unknown" for all items above — CISA has not labeled any of these as known ransomware-campaign use.*

**Still-unpatched watch:** GitLab CE/EE has the highest likelihood score on the list today (EPSS 0.1196 — a 12% estimated chance of exploitation in the next 30 days, higher than 95.9% of all known flaws), it is an unauthenticated file-read flaw on your code server, and its federal deadline passed on 09-14-2026. The two JFrog Artifactory flaws (deadline 09-25-2026) and both MikroTik flaws (deadline 09-13-2026) are also live. If any of those four systems are yours and unpatched, they outrank everything else here.

### Ransomware victim pulse (ransomware.live)
Sector signal for the last 24h: **Manufacturing** and **Healthcare** were hit hardest, with Retail and Technology behind them. The **safepay** crew posted a batch across five countries in one window — a burst like that is a sector-targeting signal, not proof any specific business was breached.

| Group | Sector | Country | Discovered |
|-------|--------|---------|------------|
| safepay | Manufacturing | US | 09-15-2026 |
| safepay | Manufacturing | DE | 09-15-2026 |
| safepay | Healthcare | US | 09-15-2026 |
| safepay | Retail & E-Commerce | MX | 09-15-2026 |
| safepay | Retail & E-Commerce | CH | 09-15-2026 |
| safepay | Technology | DE | 09-15-2026 |
| safepay | Not Found | JP | 09-15-2026 |
| dragonforce | Healthcare | GB | 09-16-2026 |
| dragonforce | Other | US | 09-16-2026 |
| qilin | Manufacturing | SE | 09-16-2026 |

Source: [ransomware.live](https://www.ransomware.live)

### Notable new CIRCL vulnerabilities
- **CVE-2026-40856 / CVE-2026-58147 (WNC 5G Box IDU router)** — unauthenticated configuration disclosure and command injection in the password-change page. See Item 3. [CIRCL](https://vulnerability.circl.lu/vuln/CVE-2026-40856)
- **CVE-2026-81665 (Corosync)** — heap overflow in Totem message reassembly; EPSS 0.0021 (11.6th pct). See Item 4. [CIRCL](https://vulnerability.circl.lu/vuln/CVE-2026-81665)
- **CVE-2026-92356 (a2ui 0.9/0.9.1)** — a toolkit AI agents use to build and update user-interface components; a crafted `updateComponents` call leads to resource consumption (a denial-of-service class flaw). Low severity, but if you build agent-driven interfaces, patch on your normal cycle. [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-92356)
- **CVE-2026-73163 / CVE-2026-73164 / CVE-2026-19535 (Advantech EKI-1242IEIMS, firmware V1.06.01)** — command injection and cross-site request forgery in the web management interface of an industrial gateway. Relevant if any shop-floor or building equipment sits on your network. [CIRCL](https://vulnerability.circl.lu/vuln/CVE-2026-73164)
- **CVE-2026-65369 (macOS Gatekeeper)** — a malicious application may bypass Gatekeeper checks; fixed in macOS Sequoia 15.8, macOS Tahoe 26.7, and newer. Confirm your Macs are on a current release. [CIRCL](https://vulnerability.circl.lu/vuln/CVE-2026-65369)
- **CVE-2024-8309 (LangChain `GraphCypherQAChain`) and CVE-2025-1889 (picklescan)** — both surfaced again in today's feed at EPSS 0.1374 (96.3rd pct) and 0.0039 respectively. Already covered in this week's briefs; if you haven't checked your RAG pipeline and your model scanner since, that action is still open.

### IOC sample (abuse.ch)
Malicious domains / addresses to block and hunt — **do not visit**.
- **ClearFake** (fake browser-update malware) domain: `somageneva.ch` ([Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/js.clearfake))
- **PHP webshell** hosts: `gagymo.workers.dev`, `ybkjz19142.workers.dev` ([Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/php.shin_webshell))
- **Mozi** botnet download URLs: `103.174.243.207:53259/Mozi.m`, `110.38.8.126:39702/Mozi.a` ([Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/elf.mozi))
- **Unknown malware** domains seen in click-fix style campaigns: `fullynsure.com`, `davariyabrothers.com`, `docucentercentral.live` ([ClickFix reference](https://clickfix.carsonww.com/domains/fullynsure.com) · [sandbox report](https://www.virustotal.com/gui/file/05b976a4dfe18bbe53785588f8fc862d18d562bf317facd7e051b0f6ef6675f4))
- **URLhaus** active malicious download URLs: `1.70.76.88:49433/bin.sh`, `94.154.43.37/.Sx86`, `94.154.43.37/.Sx86_64`, `94.154.43.37/.Smpsl`, `94.154.43.37/.Sarm5`, `176.65.139.231/client.exe`. Entry pages: [3917771](https://urlhaus.abuse.ch/url/3917771/) · [3917767](https://urlhaus.abuse.ch/url/3917767/) · [3917768](https://urlhaus.abuse.ch/url/3917768/) · [3917769](https://urlhaus.abuse.ch/url/3917769/) · [3917770](https://urlhaus.abuse.ch/url/3917770/) · [3917766](https://urlhaus.abuse.ch/url/3917766/)

### Other CISA advisories
- **Digital Watchdog VMAX DVR and NVR product lineups (ICSA-26-258-01, published 09-03-2026)** — successful exploitation could grant full administrative control of the recorder: live and recorded surveillance, configuration changes, and use of the device as a network pivot. CISA reported no known public exploitation at the time of publication. If you have cameras with one of these recorders on your network, it is worth a firmware check: [CISA advisory](https://www.cisa.gov/news-events/ics-advisories/icsa-26-258-01)

---

*Compiled from public sources · 09-16-2026*
