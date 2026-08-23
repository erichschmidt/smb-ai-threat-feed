---
type: threat-feed-note
title: "Threat Feed - 08-23-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-08-23
source: "cisa-kev, cisa-advisories, ransomware.live, circl, epss, threatfox, urlhaus"
related: "https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md"
---

# Threat Feed — 08-23-2026

> **Reader promise:** 3-minute read. Headlines alone tell you what to do. New term? Check the [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).
> **Lens:** threats that hit AI tools, automations, and small-business money.
> **Sources:** every finding links to its primary source. If you want to verify, click.

## How to read the scores (30 seconds)
- **EPSS (0–1):** a score estimating how likely this flaw is to be exploited in the next 30 days; higher = patch first. 0.78 ≈ 78% — patch first. 0.01 ≈ 1% — lower urgency. Percentile ranks it against every known flaw: 99.5th = more likely to be exploited than 99.5% of all known vulnerabilities.
- **CISA KEV:** CISA only adds a flaw after confirming it's being **actively exploited right now** — not theoretical. The date shown is when CISA confirmed it. The federal deadline is their urgency rating in date form.
- **Today's window:** no new actively-exploited vulnerabilities were added to CISA KEV on 08-23-2026. The nine entries below are the last 7 days. Deadlines that land this weekend are the story.

---

## 1. HIGH — Your AI experiment-tracking tool is still being used to steal cloud keys
**CVE-2026-64849** · CISA confirmed active exploitation **08-19-2026** · federal patch deadline **09-02-2026** · **EPSS 0.0815 (94.4th percentile)**
**Sources:** [Fix pull request](https://github.com/mlflow/mlflow/pull/24258) · [Issue (webhook SSRF)](https://github.com/mlflow/mlflow/issues/24179) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-64849) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** **MLflow (the popular tracker for AI experiments, models, and deployments)** will call a webhook URL you configure. Attackers abuse **SSRF (server-side request forgery — tricking your server into fetching internal URLs for them)** so the tracker reaches cloud metadata or other internal services and hands back the response. You don't need the DNS-rebinding detail — just know an internet-reachable MLflow can be turned into a proxy into your cloud, and CISA still says that is happening.

**Why it matters to an SMB running AI tools:** This is the on-lens item: the broken product *is* the AI stack. MLflow often sits next to training data, model registries, and cloud credentials. Copilot/RAG pipelines that pull from the same cloud account inherit the blast radius. No new KEV today does not mean this cooled off — the federal clock still runs to 09-02-2026.

**What you do Monday (20 minutes):**
1. Ask whoever runs AI/ML: *"Do we run MLflow? Is it on the internet? Has the CVE-2026-64849 webhook fix (PR 24258) landed?"* If no MLflow, you're done.
2. If it exists: take it off the public internet (VPN or private network only), apply the patched build, and disable unused webhooks.
3. If it was reachable from the internet, rotate the cloud keys on that machine, then confirm the metadata endpoint is not reachable from the app.

**CISA metrics:** CISA confirmed this is being actively exploited as of 08-19-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch by 09-02-2026. Required action: apply the MLflow webhook fix and stop exposing the tracker to the internet.

**Attacker view (conceptual):** Scan for an internet-reachable experiment tracker → point a webhook at an internal or cloud-metadata address → read the response. Defender rule of thumb: MLflow should not be on the public internet; unexpected outbound webhook destinations from that host are the tell.

---

## 2. CRITICAL — Your video-meeting server's missing-login patch is due today
**CVE-2026-72529** (missing login check) and **CVE-2026-72530** (code injection / sandbox breakout) · CISA confirmed active exploitation **08-20-2026** · federal deadlines **08-23-2026 (today)** and **09-03-2026** · EPSS 0.0078 / 0.0097 — **KEV is the signal, not EPSS**
**Sources:** [TrueConf advisories](https://trueconf.com/blog/news/security-fixes-updates-and-advisories) · [Kaspersky: missing authentication](https://ics-cert.kaspersky.com/advisories/2026/08/11/trueconf-server-missing-authentication-for-critical-function/) · [Kaspersky: isolated-environment breakout](https://ics-cert.kaspersky.com/advisories/2026/08/11/trueconf-server-breakout-from-isolated-environment/) · [NVD CVE-2026-72529](https://nvd.nist.gov/vuln/detail/CVE-2026-72529) · [NVD CVE-2026-72530](https://nvd.nist.gov/vuln/detail/CVE-2026-72530)

**What broke:** TrueConf Server (an on-premises video-meeting product) has two holes on port **4307/TCP**. One lets a stranger call a powerful function with **no login**. The other lets them **break out of the isolated environment (the sandbox meant to contain the meeting software)** and run code on the real machine. Affected: all versions before 5.3, plus 5.3.x before 5.3.9, 5.4.x before 5.4.9, and 5.5.x before 5.5.5. If you don't run TrueConf, you're done.

**Why it matters to an SMB running AI tools:** Meeting servers sit on the same network as file shares, calendars, and the transcript/recording pipelines that AI tools summarize. If the meeting box is owned, recordings and chat become an AI data-source problem — poisoned transcripts, stolen decks, and a foothold into whatever the bot can read.

**What you do Monday (15 minutes — do it today if you run TrueConf):**
1. On the TrueConf host: update to **5.3.9, 5.4.9, or 5.5.5** (vendor installer / server admin update).
2. At the firewall: confirm **port 4307/TCP is not open to the internet**. If it is, close it until the patch is on.
3. Tell IT: *"TrueConf CVE-2026-72529 and CVE-2026-72530 are on CISA's actively-exploited list as of 08-20-2026. Missing-login deadline is 08-23-2026. Patch, pull 4307 off the internet, and scan the host."*

**CISA metrics:** CISA confirmed active exploitation as of 08-20-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch CVE-2026-72529 by 08-23-2026 and CVE-2026-72530 by 09-03-2026. Required action: vendor update to 5.3.9 / 5.4.9 / 5.5.5, then isolate port 4307.

---

## 3. CRITICAL — Your self-hosted email server can be owned by a crafted incoming message — patch by tomorrow
**CVE-2026-73570** · CISA confirmed active exploitation **08-21-2026** · federal patch deadline **08-24-2026 (Monday)** · EPSS 0.0104 (61.5th percentile) — **KEV is the signal, not EPSS** · CVSS 8.9/10 = high — remote, no login, but only when SNMP notifications are on
**Sources:** [CISA alert 08-21-2026](https://www.cisa.gov/news-events/alerts/2026/08/21/cisa-adds-one-known-exploited-vulnerability-catalog) · [Zimbra security advisories](https://wiki.zimbra.com/wiki/Zimbra_Security_Advisories) · [Zimbra 10.1.20 patch notes](https://blog.zimbra.com/2026/07/patch-release-update-zimbra-10-1-20/) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-73570) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** **Zimbra Collaboration Suite (self-hosted email and calendar, used by a lot of schools and small orgs)** before **10.1.20** will run an attacker-chosen operating-system command as the Zimbra user if the optional **SNMP (the "tell the monitoring box that mail arrived")** package is installed and notifications are enabled. The trigger is a specially crafted incoming mail (SMTP) — no login required. If you don't run Zimbra, you're done.

**Why it matters to an SMB running AI tools:** Inbox, calendar, and attachment stores are the default data source for Copilot and every "summarize my email" automation. If the mail server is owned, the attacker is inside the same stream those tools read — invoices, password resets, customer threads, and anything an assistant is allowed to see.

**What you do Monday (15 minutes — do it today if you run Zimbra):**
1. On the Zimbra host: `yum update` or `apt update` and install **ZCS 10.1.20 or later**. Confirm the version in the admin console.
2. If you cannot patch today: turn **SNMP notifications off** and remove the `zimbra-snmp` package until 10.1.20 is on.
3. Tell IT: *"CVE-2026-73570 is on CISA's actively-exploited list as of 08-21-2026. Federal deadline is 08-24-2026. Upgrade Zimbra to 10.1.20 and check the host for unexpected zimbra-user processes."*

**CISA metrics:** CISA confirmed this is being actively exploited as of 08-21-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch by 08-24-2026. Required action: upgrade to Zimbra 10.1.20 (or disable SNMP notifications until you can).

**Attacker view (conceptual):** Find a Zimbra box that still talks SNMP → send mail that trips a notification → the notification path runs a command as the mail user. Defender rule of thumb: SNMP notifications you didn't know were on, plus unexpected processes owned by the zimbra user after inbound SMTP.

---

## 4. CRITICAL — Your Windows VPN hole is still being attacked — the patch deadline already passed
**CVE-2026-33824** · CISA confirmed active exploitation **08-18-2026** · federal patch deadline **08-21-2026 (missed)** · **EPSS 0.779 (99.5th percentile)**
**Sources:** [Microsoft advisory](https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-33824) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-33824) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** A memory bug (double-free — the program frees the same memory twice) in the Windows **IKE (Internet Key Exchange — the handshake that sets up a VPN tunnel)** service can let an attacker run their own code on the machine from the network. You don't need the memory-bug detail — just know it is being exploited right now, and CISA's federal deadline was 08-21-2026.

**Why it matters to an SMB running AI tools:** The VPN is the front door for remote staff, backup agents, and the automations that feed Copilot / "chat with your files" tools. If the tunnel service is owned, everything behind it is in play — including the document stores those tools read.

**What you do Monday (10 minutes — do it today if you haven't):**
1. On every Windows PC and server: **Settings → Windows Update → Check for updates** — install the August security update and restart.
2. If a machine won't update, tell your IT person: *"Apply the Microsoft patch for CVE-2026-33824 today — CISA says it's being exploited and the federal deadline was 08-21-2026."*
3. After the restart, confirm VPN users can still connect; if a box was internet-facing on IKE/VPN ports, treat it as "check this host" not "patch and forget."

**CISA metrics:** CISA confirmed this is being actively exploited as of 08-18-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch by 08-21-2026. Required action: install the Microsoft security update (Windows Update path above).

---

## 5. WATCH — Healthcare and clinic software is getting dumped in bunches today — test a restore
**Ransomware.live sector pulse, 08-23-2026:** 39 victim disclosures today. Top sectors: Healthcare (14), Manufacturing (7), Technology (5). Top groups: **kazu**, **metaencryptor**, **Storm**. US-heavy (20 of 39). The API feed failed this run; counts are from the public site (updated 08-23-2026 12:50 UTC).
**Sources:** [Ransomware.live](https://www.ransomware.live)

**What broke:** Nothing new in your software, necessarily — these are victim disclosures. The pattern is the point: one crew is posting a batch of healthcare and clinic-software claims, not a single hospital headline. Practice-management, telemedicine, and clinic tools sit in the same "small office with patient or customer records" world a lot of SMBs actually occupy.

**Why it matters to an SMB running AI tools:** New AI connectors (inbox, drive, clinic or accounting export) are often the least-watched door. Ransomware crews do not need a clever AI exploit if the practice-management box has never had a restore test and the new automation has no MFA. If your assistant reads those systems, a ransomed clinic or office platform is an AI data-source problem.

**What you do Monday (30 minutes):**
1. **Test one backup restore.** Not "check the job ran" — restore one folder to a spare machine. If you can't, that is the finding.
2. Any AI or automation added this year: turn on **MFA (multi-factor authentication — password plus a phone code or key)** and cut its access to only the folders it needs.
3. If you are in healthcare, manufacturing, or a small tech shop, tell IT: *"Ransomware.live showed a healthcare-heavy dump on 08-23-2026. Walk the backup restore and the new AI connectors today."*

**CISA metrics:** this section is from Ransomware.live (victim disclosures), not CISA KEV. No single CVE applies. Pair it with the patch list above.

---

## Jargon buster (terms used today)
- **CVE:** a unique ID for a security flaw, so everyone tracks the same bug (like a license plate).
- **RCE (Remote Code Execution):** attacker can run their own code on your machine — full control.
- **EPSS:** 0–1 score of how likely a flaw is to be exploited in the next 30 days. Higher = patch first.
- **Percentile:** where a score ranks — 99.5th = more likely to be exploited than 99.5% of known flaws.
- **KEV (Known Exploited Vulnerabilities):** CISA's list of flaws being actively exploited right now.
- **CVSS:** a 0–10 severity score. 8.9/10 = high; 9.8/10 = critical — typically exploitable remotely with no login.
- **MLflow:** open-source tracker for AI experiments, models, and deployments — often sits next to cloud keys.
- **SSRF (Server-Side Request Forgery):** tricking a server into fetching internal or cloud URLs on the attacker's behalf.
- **Webhook:** an automated HTTP callback one system sends another when something happens (e.g. "a model was logged").
- **Cloud metadata:** the internal cloud "who am I" page that holds machine keys. If an app can fetch it, attackers steal credentials.
- **RAG / Copilot data source:** the files an AI is allowed to read. If those files (or the system that holds them) are owned, the AI is owned.
- **TrueConf:** an on-premises video-meeting server. A hole here is a hole in the meeting room and often the recordings.
- **Code injection:** tricking software into running attacker-supplied commands as if they were part of the program.
- **Isolated environment / sandbox:** a cage meant to contain a program; a breakout means the attacker reached the real machine.
- **Zimbra / ZCS:** a self-hosted email and calendar suite used by many schools, governments, and small orgs.
- **SNMP:** a simple monitoring protocol devices use to report "I'm up / something broke." Wired into email notifications, a crafted message can become a command.
- **Command injection:** tricking software into running operating-system commands the attacker chose.
- **SMTP:** the internet's send-mail protocol. "Crafted SMTP" here means a specially built incoming email.
- **Double-free:** a memory bug attackers use to inject code. Mechanism not required — just patch.
- **IKE (Internet Key Exchange):** the Windows service that sets up a VPN tunnel. A hole here is a hole in the front door.
- **Ransomware:** malware that locks your files and demands payment — the top small-business threat.
- **MFA (Multi-Factor Authentication):** password plus a second proof (phone code). Cheapest real defense.
- **kazu / metaencryptor / Storm:** ransomware groups in today's victim disclosures.
- **LangChain:** a popular framework for building "chat with your data" apps. Flaws in it hit lots of AI tools at once.
- **Prompt injection / SQL injection:** hiding instructions or database commands inside the data an AI or app reads.
- **picklescan:** a scanner meant to catch dangerous Python pickle files inside AI model downloads. If it skips a file, a "model" can be malware.
- **IOC (Indicator of Compromise):** a trace of an attack (malicious IP/domain/file) to hunt for in logs.
- **ClearFake:** malware that pretends to be a browser or software update so a visitor infects themselves.
- **Shin webshell:** a PHP webshell family. Seeing it on a domain means a site is already hosting attacker-controlled code.
- **Webshell:** a small script planted on a hacked website so the attacker can come back and run commands later.
- **Ray:** open-source tool that runs AI jobs across machines. Developers often leave its dashboard on a laptop with no login.

Full plain-language library: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).

---

## Appendix — raw signals (for the technical reader)

### CISA KEV (last 7 days, ranked by EPSS — links to vendor advisories)
| CVE | Product | EPSS | CISA confirmed | Federal deadline | Ransomware use | Source |
|---|---|---|---|---|---|---|
| CVE-2026-33824 | Microsoft IKE Service Extensions (RCE) | **0.779** | 08-18-2026 | 08-21-2026 | Unknown | [MSRC](https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-33824) |
| CVE-2026-64849 | MLflow (SSRF → cloud metadata) | 0.0815 | 08-19-2026 | 09-02-2026 | Unknown | [Fix PR](https://github.com/mlflow/mlflow/pull/24258) |
| CVE-2026-55040 | Microsoft SharePoint (auth bypass) | 0.0549 | 08-18-2026 | 08-21-2026 | Unknown | [MSRC](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-55040) |
| CVE-2026-59310 | Broadcom VMware vCenter (path traversal → RCE) | 0.024 | 08-18-2026 | 08-21-2026 | Unknown | [Broadcom](https://support.broadcom.com/web/ecx/support-content-notification/-/external/content/SecurityAdvisories/0/38017) |
| CVE-2026-73570 | Synacor Zimbra ZCS (OS command injection via SMTP) | 0.0104 | 08-21-2026 | 08-24-2026 | Unknown | [Zimbra 10.1.20](https://blog.zimbra.com/2026/07/patch-release-update-zimbra-10-1-20/) |
| CVE-2025-62593 | Ray-Project Ray (code injection → RCE) | 0.01 | 08-17-2026 | 08-20-2026 | Unknown | [GitHub GHSA](https://github.com/ray-project/ray/security/advisories/GHSA-q279-jhrf-cc6v) |
| CVE-2026-72530 | TrueConf Server (code injection / breakout) | 0.0097 | 08-20-2026 | 09-03-2026 | Unknown | [Kaspersky](https://ics-cert.kaspersky.com/advisories/2026/08/11/trueconf-server-breakout-from-isolated-environment/) |
| CVE-2026-72529 | TrueConf Server (missing authentication) | 0.0078 | 08-20-2026 | 08-23-2026 | Unknown | [Kaspersky](https://ics-cert.kaspersky.com/advisories/2026/08/11/trueconf-server-missing-authentication-for-critical-function/) |
| CVE-2026-65400 | Apple macOS Screen Sharing (auth bypass) | 0.0075 | 08-18-2026 | 08-21-2026 | Unknown | [Apple](https://support.apple.com/en-us/148170) |

### Ransomware.live — recent victims
Ransomware.live API query failed this run (0 victims in the packet). Public-site pulse (updated 08-23-2026 12:50 UTC): **39 disclosures today** — Healthcare 14, Manufacturing 7, Technology 5. Top groups: kazu, metaencryptor, Storm. US 20 / Chile 3 / Mexico 2. No leak-site or .onion links. Source: [Ransomware.live](https://www.ransomware.live)

### CIRCL — highest-signal new items (30 pulled; 28 empty/unparseable records skipped)
- **CVE-2024-8309 (EPSS 0.1374, 96.2nd pct)** — LangChain GraphCypherQAChain SQL injection via prompt injection; patch `langchain-community` past the 0.2.5-era chain (fixed line is the 0.3 series / GHSA below) — [GHSA](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [Fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) · [huntr](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5)
- **CVE-2025-1889 (EPSS 0.0038, 31.5th pct)** — picklescan missed non-standard pickle extensions in ML model files; upgrade picklescan to **0.0.22 or later** — [GHSA](https://github.com/advisories/GHSA-769v-p64c-89pr) · [Sonatype](https://sites.google.com/sonatype.com/vulnerabilities/cve-2025-1889)

### IOCs (ThreatFox 8 + URLhaus 6, newest — linked)
- **ClearFake domains:** `eng-usa-heroup.com`, `steffpro.ch`, `talerent.com`, `eng-en-thebrainsong.com`, `aolmqkxl.eng--puraboost.com` — [Malpedia: ClearFake](https://malpedia.caad.fkie.fraunhofer.de/details/js.clearfake)
- **Shin webshell domains:** `kekenuri.workers.dev`, `cisonagi.workers.dev`, `candacemale.workers.dev` — [Malpedia: php.shin_webshell](https://malpedia.caad.fkie.fraunhofer.de/details/php.shin_webshell)
- **URLhaus live droppers:** [59.96.139.68:54390/bin.sh](https://urlhaus.abuse.ch/url/3907231/) · [113.230.83.154:45105/i](https://urlhaus.abuse.ch/url/3907230/) · [125.45.57.136:34620/i](https://urlhaus.abuse.ch/url/3907229/) · [24.54.95.49:35344/bin.sh](https://urlhaus.abuse.ch/url/3907228/) · [77.230.168.62:51199/i](https://urlhaus.abuse.ch/url/3907227/) · [123.12.234.38:40280/i](https://urlhaus.abuse.ch/url/3907226/)

---

*Compiled from public sources · 08-23-2026 · Sources: CISA KEV, CISA Advisories, Ransomware.live, CIRCL, FIRST EPSS, ThreatFox, URLhaus*
