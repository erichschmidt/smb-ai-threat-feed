---
type: threat-feed-note
title: "Threat Feed - 08-21-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-08-21
source: "cisa-kev, cisa-advisories, ransomware.live, circl, epss, threatfox, urlhaus"
related: "https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md"
---

# Threat Feed — 08-21-2026

> **Reader promise:** 3-minute read. Headlines alone tell you what to do. New term? Check the [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).
> **Lens:** threats that hit AI tools, automations, and small-business money.
> **Sources:** every finding links to its primary source. If you want to verify, click.

## How to read the scores (30 seconds)
- **EPSS (0–1):** a score estimating how likely this flaw is to be exploited in the next 30 days; higher = patch first. 0.78 ≈ 78% — patch first. 0.01 ≈ 1% — lower urgency. Percentile ranks it against every known flaw: 99.5th = more likely to be exploited than 99.5% of all known vulnerabilities.
- **CISA KEV:** CISA only adds a flaw after confirming it's being **actively exploited right now** — not theoretical. The date shown is when CISA confirmed it. The federal deadline is their urgency rating in date form.

---

## 1. CRITICAL — Your Windows VPN hole is being actively attacked and today's the patch deadline
**CVE-2026-33824** · CISA confirmed active exploitation **08-18-2026** · federal patch deadline **08-21-2026 (today)** · **EPSS 0.779 (99.5th percentile)**
**Sources:** [Microsoft advisory](https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-33824) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-33824) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** A memory bug (double-free — the program frees the same memory twice) in the Windows **IKE (Internet Key Exchange — the handshake that sets up a VPN tunnel)** service can let an attacker run their own code on the machine from the network. You don't need the memory-bug detail — just know it is being exploited right now, and CISA's federal deadline is today.

**Why it matters to an SMB running AI tools:** The VPN is the front door for remote staff, backup agents, and the automations that feed Copilot / "chat with your files" tools. If the tunnel service is owned, everything behind it is in play — including the document stores those AI tools read.

**What you do Monday (10 minutes — do it today if you haven't):**
1. On every Windows PC and server: **Settings → Windows Update → Check for updates** — install the August security update and restart.
2. If a machine won't update, tell your IT person: *"Apply the Microsoft patch for CVE-2026-33824 today — CISA says it's being exploited and the federal deadline is 08-21-2026."*
3. After the restart, confirm VPN users can still connect; if a box was internet-facing on IKE/VPN ports, treat it as "check this host" not "patch and forget."

**CISA metrics:** CISA confirmed this is being actively exploited as of 08-18-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch by 08-21-2026. Required action: install the Microsoft security update (Windows Update path above).

**Attacker view (conceptual):** Scan for internet-reachable VPN/IKE → hit the handshake service (no login needed) → crash/control the process → land on the host. Defender rule of thumb: unexpected IKE/VPN crashes or new processes on VPN servers after 08-18-2026 are worth a look; patching is the control.

---

## 2. CRITICAL — Your video-meeting server can be taken over by anyone who can reach it — update this weekend
**CVE-2026-72529** (missing login check, CVSS 9.8/10 = critical — exploitable remotely with no authentication) and **CVE-2026-72530** (code injection / sandbox breakout) · CISA confirmed active exploitation **08-20-2026** · federal deadlines **08-23-2026** and **09-03-2026** · EPSS still low (0.003 / 0.003) because the listing is new — **KEV is the signal, not EPSS**
**Sources:** [CISA alert 08-20-2026](https://www.cisa.gov/news-events/alerts/2026/08/20/cisa-adds-two-known-exploited-vulnerabilities-catalog) · [TrueConf advisories](https://trueconf.com/blog/news/security-fixes-updates-and-advisories) · [Kaspersky: missing authentication](https://ics-cert.kaspersky.com/advisories/2026/08/11/trueconf-server-missing-authentication-for-critical-function/) · [Kaspersky: isolated-environment breakout](https://ics-cert.kaspersky.com/advisories/2026/08/11/trueconf-server-breakout-from-isolated-environment/) · [NVD CVE-2026-72529](https://nvd.nist.gov/vuln/detail/CVE-2026-72529) · [NVD CVE-2026-72530](https://nvd.nist.gov/vuln/detail/CVE-2026-72530)

**What broke:** TrueConf Server (an on-premises video-meeting product) has two holes on port **4307/TCP**. One lets a stranger call a powerful function with **no login**. The other lets them **break out of the isolated environment (the sandbox meant to contain the meeting software)** and run code on the real machine. Affected: all versions before 5.3, plus 5.3.x before 5.3.9, 5.4.x before 5.4.9, and 5.5.x before 5.5.5. Researchers report this class of hole has already been used to plant malware that then reaches people who join the meeting.

**Why it matters to an SMB running AI tools:** Meeting servers sit on the same network as file shares, calendars, and the transcript/recording pipelines that AI tools summarize. If the meeting box is owned, recordings and chat become an AI data-source problem — poisoned transcripts, stolen decks, and a foothold into whatever the bot can read.

**What you do Monday (15 minutes — this weekend if you run TrueConf):**
1. On the TrueConf host: update to **5.3.9, 5.4.9, or 5.5.5** (vendor installer / server admin update). If you don't run TrueConf, you're done.
2. At the firewall: confirm **port 4307/TCP is not open to the internet**. If it is, close it until the patch is on.
3. Tell IT: *"TrueConf CVE-2026-72529 and CVE-2026-72530 are on CISA's actively-exploited list as of 08-20-2026. Patch, pull 4307 off the internet, and scan the host."*

**CISA metrics:** CISA confirmed active exploitation as of 08-20-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch CVE-2026-72529 by 08-23-2026 and CVE-2026-72530 by 09-03-2026. Required action: vendor update to 5.3.9 / 5.4.9 / 5.5.5, then isolate port 4307.

---

## 3. HIGH — Your AI experiment-tracking tool can be tricked into stealing cloud keys
**CVE-2026-64849** · CISA confirmed active exploitation **08-19-2026** · federal patch deadline **09-02-2026** · **EPSS 0.0815 (94.4th percentile)**
**Sources:** [Fix pull request](https://github.com/mlflow/mlflow/pull/24258) · [Issue (webhook SSRF)](https://github.com/mlflow/mlflow/issues/24179) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-64849) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** **MLflow (the popular tracker for AI experiments, models, and deployments)** will call a webhook URL you configure. Attackers abuse **SSRF (server-side request forgery — tricking your server into fetching internal URLs for them)** so the tracker reaches cloud metadata or other internal services and hands back the response. You don't need the DNS-rebinding detail — just know an internet-reachable MLflow can be turned into a proxy into your cloud.

**Why it matters to an SMB running AI tools:** MLflow often sits next to training data, model registries, and cloud credentials. Copilot/RAG pipelines that pull from the same cloud account inherit the blast radius. This is not a "data-science-only" bug — it is a cloud-key bug that happens to live in the AI stack.

**What you do Monday (20 minutes):**
1. Ask whoever runs AI/ML: *"Do we run MLflow? Is it on the internet? Has CVE-2026-64849 / the webhook fix landed?"* If no MLflow, you're done.
2. If it exists: take it off the public internet (VPN or private network only), apply the patched build, and disable unused webhooks.
3. If it was reachable from the internet, rotate the cloud keys on that machine, then confirm the metadata endpoint is not reachable from the app.

**CISA metrics:** CISA confirmed this is being actively exploited as of 08-19-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch by 09-02-2026. Required action: apply the MLflow webhook fix and stop exposing the tracker to the internet.

---

## 4. HIGH — SharePoint's login check is being bypassed in the wild — patch today
**CVE-2026-55040** · CISA confirmed active exploitation **08-18-2026** · federal patch deadline **08-21-2026 (today)** · **EPSS 0.0549 (92.2nd percentile)**
**Sources:** [Microsoft advisory](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-55040) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-55040) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** SharePoint has a **weak authentication (the login/ticket check can be skipped)** flaw that lets an unauthorized attacker bypass a security feature over the network. CISA has confirmed it is being used in the wild. You don't need the protocol detail — patch the farm.

**Why it matters to an SMB running AI tools:** SharePoint is the default document brain for Microsoft 365 Copilot and a lot of "chat with our files" setups. If an attacker bypasses SharePoint auth, they are inside the same library your AI reads — theft, tampering, and prompt-poisoned documents.

**What you do Monday (15 minutes — today):**
1. Microsoft 365 / SharePoint admin: **Microsoft 365 admin center → Health → Message center / SharePoint admin center → apply the security update for CVE-2026-55040**. On-prem farm: install the matching SharePoint security update and run the config wizard.
2. Tell IT: *"CVE-2026-55040 is being exploited and CISA's deadline is 08-21-2026. Patch SharePoint today and review recent anonymous/unusual access."*
3. Confirm Copilot / any bot that reads SharePoint still uses least-privilege accounts — never a farm admin.

**CISA metrics:** CISA confirmed this is being actively exploited as of 08-18-2026. Known to be used in ransomware campaigns: Unknown. CISA requires federal agencies to patch by 08-21-2026. Required action: apply the Microsoft SharePoint security update (admin-center / farm patch path above).

---

## 5. WATCH — Ransomware groups hit healthcare, schools, and small-business accounting overnight — test a restore
**Ransomware.live, last 24h:** 10 victim disclosures. **anubis** (Healthcare, US) plus a **direwolf** cluster across Education, Financial Services (DK), Transportation (US), Manufacturing (US), Hospitality (MX), Technology (US), and retail. One listed target is cloud accounting software aimed at small and mid-size firms.
**Sources:** [Ransomware.live](https://www.ransomware.live)

**What broke:** Nothing new in your software, necessarily — these are victim disclosures. The pattern is the point: groups are hitting the same sectors small businesses actually occupy, including accounting and education platforms, not only hospitals and factories.

**Why it matters to an SMB running AI tools:** New AI connectors (inbox, drive, accounting export) are often the least-watched door. Ransomware crews don't need a clever AI exploit if your backup has never been restored and the new automation has no MFA.

**What you do Monday (30 minutes):**
1. **Test one backup restore.** Not "check the job ran" — restore one folder to a spare machine. If you can't, that is the finding.
2. Any AI or automation added this year: turn on **MFA (multi-factor authentication — password plus a phone code or key)** and cut its access to only the folders it needs.
3. If you are in healthcare, education, accounting, transport, or hospitality, tell IT: *"Ransomware.live showed new victims in our sector on 08-21-2026. Walk the backup restore and the new AI connectors today."*

**CISA metrics:** this section is from Ransomware.live (victim disclosures), not CISA KEV. No single CVE applies. Pair it with the patch list above.

---

## Friday companion — this week's top 3

1. **Windows VPN/IKE (CVE-2026-33824)** — highest-likelihood exploited flaw of the week (EPSS 0.779, 99.5th percentile). CISA deadline is **08-21-2026**. If the Monday update didn't land, it is late.
2. **AI platforms are now on the actively-exploited list** — Ray (CVE-2025-62593, listed 08-17-2026) and MLflow (CVE-2026-64849, listed 08-19-2026). Treat experiment trackers and job orchestrators as production: not on the internet, patched, keys rotated if they were exposed.
3. **TrueConf meeting servers (CVE-2026-72529 / CVE-2026-72530)** — added 08-20-2026. Missing-auth deadline **08-23-2026**. Video meetings are a malware-delivery path, not just a downtime issue.

Same-week also-patch (all CISA-confirmed, several due 08-21-2026): SharePoint CVE-2026-55040, VMware vCenter CVE-2026-59310, Apple Screen Sharing CVE-2026-65400.

---

## Jargon buster (terms used today)
- **CVE:** a unique ID for a security flaw, so everyone tracks the same bug (like a license plate).
- **RCE (Remote Code Execution):** attacker can run their own code on your machine — full control.
- **Double-free:** a memory bug attackers use to inject code. Mechanism not required — just patch.
- **IKE (Internet Key Exchange):** the Windows service that sets up a VPN tunnel. A hole here is a hole in the front door.
- **EPSS:** 0–1 score of how likely a flaw is to be exploited in the next 30 days. Higher = patch first.
- **Percentile:** where a score ranks — 99.5th = more likely to be exploited than 99.5% of known flaws.
- **KEV (Known Exploited Vulnerabilities):** CISA's list of flaws being actively exploited right now.
- **CVSS:** a 0–10 severity score. 9.8/10 = critical — exploitable remotely with no login.
- **Code injection:** tricking software into running attacker-supplied commands as if they were part of the program.
- **Isolated environment / sandbox:** a cage meant to contain a program; a breakout means the attacker reached the real machine.
- **SSRF (Server-Side Request Forgery):** tricking a server into fetching internal or cloud URLs on the attacker's behalf.
- **MLflow:** open-source tracker for AI experiments, models, and deployments — often sits next to cloud keys.
- **Webhook:** an automated HTTP callback one system sends another when something happens (e.g. "a model was logged").
- **Cloud metadata:** the internal cloud "who am I" page that holds machine keys. If an app can fetch it, attackers steal credentials.
- **SharePoint:** Microsoft's document intranet; often the library Copilot and other AI tools read.
- **RAG / Copilot data source:** the files an AI is allowed to read. If those files (or the system that holds them) are owned, the AI is owned.
- **Ransomware:** malware that locks your files and demands payment — the top small-business threat.
- **MFA (Multi-Factor Authentication):** password plus a second proof (phone code). Cheapest real defense.
- **IOC (Indicator of Compromise):** a trace of an attack (malicious IP/domain/file) to hunt for in logs.
- **C2 (Command-and-Control):** the attacker's server that infected machines report to.
- **ClearFake / Mozi / VShell / Cobalt Strike / Remus:** names on today's IOC list — ClearFake fakes browser updates; Mozi hits internet-connected gadgets; VShell and Remus are remote-control malware; Cobalt Strike is a legitimate test tool attackers also use.
- **anubis / direwolf:** ransomware groups in today's victim disclosures.

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
| CVE-2025-62593 | Ray-Project Ray (code injection → RCE) | 0.0101 | 08-17-2026 | 08-20-2026 | Unknown | [GitHub GHSA](https://github.com/ray-project/ray/security/advisories/GHSA-q279-jhrf-cc6v) |
| CVE-2026-65400 | Apple macOS Screen Sharing (auth bypass) | 0.0075 | 08-18-2026 | 08-21-2026 | Unknown | [Apple](https://support.apple.com/en-us/148170) |
| CVE-2026-72530 | TrueConf Server (code injection / breakout) | 0.0034 | 08-20-2026 | 09-03-2026 | Unknown | [Kaspersky](https://ics-cert.kaspersky.com/advisories/2026/08/11/trueconf-server-breakout-from-isolated-environment/) |
| CVE-2026-72529 | TrueConf Server (missing authentication) | 0.0028 | 08-20-2026 | 08-23-2026 | Unknown | [Kaspersky](https://ics-cert.kaspersky.com/advisories/2026/08/11/trueconf-server-missing-authentication-for-critical-function/) |

### Ransomware.live — recent victims (10)
| Group | Sector | Country | Discovered | Source |
|---|---|---|---|---|
| anubis | Healthcare | US | 08-21-2026 | [Ransomware.live](https://www.ransomware.live) |
| direwolf | Education | — | 08-21-2026 | [Ransomware.live](https://www.ransomware.live) |
| direwolf | Financial Services | DK | 08-21-2026 | [Ransomware.live](https://www.ransomware.live) |
| direwolf | Other (building materials) | AE | 08-21-2026 | [Ransomware.live](https://www.ransomware.live) |
| direwolf | Transportation | US | 08-21-2026 | [Ransomware.live](https://www.ransomware.live) |
| direwolf | Manufacturing | US | 08-21-2026 | [Ransomware.live](https://www.ransomware.live) |
| direwolf | Education | US | 08-21-2026 | [Ransomware.live](https://www.ransomware.live) |
| direwolf | Hospitality | MX | 08-21-2026 | [Ransomware.live](https://www.ransomware.live) |
| direwolf | Other (jewelry / watch retail) | — | 08-21-2026 | [Ransomware.live](https://www.ransomware.live) |
| direwolf | Technology | US | 08-21-2026 | [Ransomware.live](https://www.ransomware.live) |

### CIRCL — highest-signal new items (30 pulled; skip empty records)
- **CVE-2024-8309 (EPSS 0.1374, 96.2nd pct)** — LangChain GraphCypherQAChain SQL injection via prompt injection — [GHSA](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [Fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) · [huntr](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5)
- **CVE-2026-77775** — Headroom LLM proxy lets a client pick the upstream with the `x-headroom-base-url` header (your AI gateway can be pointed at an attacker-controlled server) — [CIRCL](https://vulnerability.circl.lu/advisories/cve-2026-77775) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-77775)
- **CVE-2025-1889 (EPSS 0.0038)** — picklescan missed non-standard pickle extensions in ML model files — [GHSA](https://github.com/advisories/GHSA-769v-p64c-89pr) · [Sonatype](https://sites.google.com/sonatype.com/vulnerabilities/cve-2025-1889)
- **CVE-2026-55674 (EPSS 0.0034)** — unauthenticated Discourse HTML injection via a crafted `color_scheme_id` cookie — [CIRCL](https://vulnerability.circl.lu/advisories/bit-discourse-2026-55674)
- WordPress plugin cluster (SMB-relevant, published 08-21-2026): ProfilePress CVE-2026-19848 · Limit Login Attempts Reloaded CVE-2026-18356 · Passster CVE-2026-17559 · Charitable CVE-2026-16650 · myCred CVE-2026-15150 · LitExtension CVE-2026-15046 · Eventin CVE-2026-13176 — [CIRCL index](https://vulnerability.circl.lu/advisories/cve-2026-19848)

### IOCs (ThreatFox 8 + URLhaus 6, newest — linked)
- **ClearFake domains:** `5zh0a5l5.en-flashburnn.com`, `en-flashburnn.com` — [Malpedia: ClearFake](https://malpedia.caad.fkie.fraunhofer.de/details/js.clearfake)
- **php.shin webshell:** `xorajahy.workers.dev` — [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/php.shin_webshell)
- **Mozi URLs:** `http://113.228.208.46:56903/Mozi.a`, `http://46.227.184.199:36141/Mozi.m` — [Malpedia: Mozi](https://malpedia.caad.fkie.fraunhofer.de/details/elf.mozi) · [URLhaus](https://urlhaus.abuse.ch/url/3906601/)
- **Cobalt Strike C2:** `36.140.162.173:8082` — [Malpedia: Cobalt Strike](https://malpedia.caad.fkie.fraunhofer.de/details/win.cobalt_strike)
- **VShell:** `43.134.100.72:4444` — [Malpedia: VShell](https://malpedia.caad.fkie.fraunhofer.de/details/win.vshell)
- **Remus:** `http://zakuiru.shop:9048/reviews` — [Malpedia: Remus](https://malpedia.caad.fkie.fraunhofer.de/details/win.remus)
- **URLhaus live droppers:** [59.180.144.211:51836/bin.sh](https://urlhaus.abuse.ch/url/3906602/) · [222.142.244.196:59371/bin.sh](https://urlhaus.abuse.ch/url/3906600/) · [182.116.20.246:39870/bin.sh](https://urlhaus.abuse.ch/url/3906598/) · [163.142.94.220:54475/i](https://urlhaus.abuse.ch/url/3906597/) · offline: [178.16.54.109/spamget.exe](https://urlhaus.abuse.ch/url/3906599/)

---

*Compiled from public sources · 08-21-2026 · Sources: CISA KEV, CISA Advisories, Ransomware.live, CIRCL, FIRST EPSS, ThreatFox, URLhaus*
