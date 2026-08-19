---
type: threat-feed-note
title: "Threat Feed - 08-19-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-08-19
source: "cisa-kev, cisa-advisories, ransomware.live, circl, epss, threatfox, urlhaus"
related: "[GLOSSARY.md](GLOSSARY.md)"
---

# Threat Feed — 08-19-2026

> **Reader promise:** 3-minute read. Headlines alone tell you what to do. New term? Check the [GLOSSARY.md](GLOSSARY.md).
> **Lens:** threats that hit AI tools, automations, and small-business money.
> **Sources:** every finding links to its primary source. If you want to verify, click.

## How to read the scores (30 seconds)
- **EPSS (0–1):** the odds this flaw gets exploited in the next 30 days. 0.78 ≈ 78% — patch first. 0.01 ≈ 1% — lower urgency. Percentile ranks it against every known flaw: 99.5th = more likely to be exploited than 99.5% of all known vulnerabilities.
- **CISA KEV:** CISA only adds a flaw after confirming it's being **actively exploited right now** — not theoretical. The date shown is when CISA confirmed it. The CISA deadline is their urgency rating in date form.

---

## 1. CRITICAL — Your Windows VPN has a hole that's being actively attacked — patch it today
**CVE-2026-33824** · CISA confirmed active exploitation **08-18-2026** · federal patch deadline **08-21-2026** · **EPSS 0.78 (99.5th percentile)**
**Sources:** [Microsoft advisory](https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-33824) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-33824) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**What broke:** A flaw in the VPN service built into Windows lets an attacker **execute code remotely (RCE — run their own programs on your machine)** without ever touching your keyboard. You don't need the memory-bug detail — just know: it's being exploited right now.

**Why it matters to you:** Your VPN is the front door to your whole business — remote workers, backup agents, automation tools. A hole in the front door is a hole in everything behind it, including the data your AI tools read.

**What you do Monday (10 minutes):**
1. On every Windows machine: **Settings → Windows Update → Check for updates** — install and restart.
2. If a machine won't update (old version), call your IT person and say: *"We need the August Windows security update — CVE-2026-33824."*
3. That's it. This one's a patch, not a project.

**CISA metrics:** Active exploitation confirmed 08-18-2026 · federal deadline 08-21-2026 (3 days — CISA's "urgent" rating) · not flagged for known ransomware campaigns.

---

## 2. HIGH — "Chat with your data" AI tools built on LangChain may have a back door
**CVE-2024-8309** · **EPSS 0.14 (96th percentile)** · not yet on CISA's actively-exploited list — fix proactively
**Sources:** [GitHub Advisory GHSA-45pg-36p6-83v9](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [Fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) · [Original report (huntr)](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5)

**What broke:** LangChain (a popular framework for building AI assistants) has a flaw where an attacker can hide instructions inside a document — **prompt injection (tricking the AI by putting commands in the data it reads)** — that turn into **SQL injection (malicious database commands)**. Result: the attacker can read, change, or delete your data *through your own AI assistant*.

**Why it matters to you:** If you or a vendor built a "chat with your data" tool — document Q&A, support bot, inventory chat — your employees' question box is a potential door. The AI is the unwitting middleman between the attacker and your database.

**What you do Monday (20 minutes):**
1. Ask your AI vendors: *"Do you use LangChain or any 'ask your data' pattern? Is it patched past version 0.2.5?"* (The fix has existed since 2024 — most vendors have it; the question finds the stragglers.)
2. Whatever AI reads your database, confirm it uses a **read-only account** with access only to what it needs — an AI never needs permission to delete anything.
3. Make it a standing rule for any future AI tool: *read-only, least privilege.*

**CISA metrics:** not in KEV (no confirmed active exploitation yet) — EPSS says exploitation is likely, so patching now beats patching after a breach.

---

## 3. HIGH — Attackers are using AI to break into factory equipment — check yours isn't online
**CISA Advisory AA26-231A** (joint NSA/CISA/FBI warning, published 08-06-2026, still current)
**Source:** [CISA Advisory AA26-231A](https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-231a)

**What broke:** Active attacks on Siemens S7 **PLCs (Programmable Logic Controllers — the rugged little computers that run factory machines, pumps, and valves)**. Attackers use **AI-generated scripts disguised as normal monitoring tools** to find PLCs connected to the internet and take them over. Targets: manufacturing, water, food, energy, chemical plants.

**Why it matters to you:** Two lessons. (1) AI isn't just defense — attackers use it to make exploitation easier, so "we're too small to be a target" is dead. (2) Even if you don't own a factory, vendors and integrators with remote access to any equipment are a supply-chain door into your network.

**What you do Monday (15 minutes):**
1. Ask whoever runs your facilities/equipment: *"Are any PLCs or control devices reachable from the internet? They shouldn't be."*
2. If yes: disconnect them, put them on a separate network, and change default passwords.
3. Note for your own planning: AI-assisted attacks are now the norm — basic hygiene is the defense.

**CISA metrics:** a CISA advisory (joint NSA/FBI), not a KEV entry — a campaign warning rather than a single software flaw. The mitigations are the point.

---

## 4. HIGH — Ransomware is hitting businesses like yours right now — check your backups actually restore
**Ransomware.live, last 24h:** Healthcare (2), Technology (2), Financial Services (1), Professional Services (1), Manufacturing (1) — groups: direwolf, SilentRansomGroup
**Source:** [Ransomware.live](https://www.ransomware.live)

**What it means:** Small and mid-size firms in these sectors are being hit *today*. Ransomware groups pick by sector, and the path of least resistance is usually the business with new AI tools and nobody watching the perimeter.

**What you do Monday (30 minutes):**
1. **Test one backup restore.** Not "check the backup ran" — actually restore one folder to a spare machine. If you can't, that's the real finding.
2. Any AI or automation tool added this year: confirm it has **MFA (multi-factor authentication — password plus a second proof like a phone code)** and limited access. Attackers go through the new stuff first.
3. If you run or support IT for a business in one of the sectors above, use this as your own checklist — the same steps apply whether it's your business or one you support.

**CISA metrics:** this section comes from Ransomware.live (victim disclosures), not CISA — no KEV entry applies. It's the "who's getting hit" signal to pair with the patch list above.

---

## Jargon buster (terms used today)
- **CVE:** a unique ID for a security flaw, so everyone tracks the same bug (like a license plate).
- **RCE (Remote Code Execution):** attacker can run their own code on your machine — full control.
- **Double-free:** a memory bug attackers use to inject code. Mechanism not required — just patch.
- **EPSS:** 0–1 score of how likely a flaw is to be exploited soon. Higher = patch first.
- **Percentile:** where a score ranks — 96th percentile = more likely to be exploited than 96% of known flaws.
- **KEV (Known Exploited Vulnerabilities):** CISA's list of flaws being actively exploited right now.
- **Prompt injection:** hiding commands inside data so an AI follows the attacker, not you.
- **SQL injection:** typing malicious database commands into an input/prompt to read or destroy data.
- **LangChain:** popular framework for building AI assistants; flaws in it affect many AI tools.
- **PLC (Programmable Logic Controller):** the computer that runs factory machines, pumps, valves.
- **Ransomware:** malware that locks your files and demands payment — the top small-business threat.
- **MFA (Multi-Factor Authentication):** password plus a second proof (phone code). Cheapest real defense.
- **IOC (Indicator of Compromise):** a trace of an attack (malicious IP/domain/file) to hunt for in logs.
- **C2 (Command-and-Control):** the attacker's server that infected machines report to.
- **Cobalt Strike / Remcos / Remus / ScreenConnect:** tool names seen in today's IOC list — Cobalt Strike and ScreenConnect are legitimate tools attackers abuse; Remcos/Remus are remote-access trojans.

Full plain-language library: [GLOSSARY.md](GLOSSARY.md).

---

## Appendix — raw signals (for the technical reader)

### CISA KEV (last 7 days, ranked by EPSS — links to vendor advisories)
| CVE | Product | EPSS | CISA confirmed | Federal deadline | Ransomware use | Source |
|---|---|---|---|---|---|---|
| CVE-2026-33824 | Microsoft IKE (RCE) | **0.779** | 08-18-2026 | 08-21-2026 | Not flagged | [MSRC](https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-33824) |
| CVE-2026-55040 | Microsoft SharePoint (auth bypass) | 0.055 | 08-18-2026 | 08-21-2026 | Not flagged | [MSRC](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-55040) |
| CVE-2026-59310 | VMware vCenter (path traversal → RCE) | 0.024 | 08-18-2026 | 08-21-2026 | Not flagged | [Broadcom](https://support.broadcom.com/web/ecx/support-content-notification/-/external/content/SecurityAdvisories/0/38017) |
| CVE-2025-62593 | Ray-Project Ray (code injection → RCE) | 0.010 | 08-17-2026 | 08-20-2026 | Not flagged | [GitHub GHSA](https://github.com/ray-project/ray/security/advisories/GHSA-q279-jhrf-cc6v) |
| CVE-2026-65400 | Apple macOS Screen Sharing (auth bypass) | 0.007 | 08-18-2026 | 08-21-2026 | Not flagged | [Apple](https://support.apple.com/en-us/148170) |

### Ransomware.live — recent victims (10)
| Group | Sector | Country | Discovered |
|---|---|---|---|
| direwolf | Healthcare | SE | 08-19-2026 |
| direwolf | Financial Services | — | 08-19-2026 |
| direwolf | Technology | US | 08-19-2026 |
| direwolf | Healthcare | US | 08-19-2026 |
| SilentRansomGroup | Professional Services | US | 08-18-2026 |

### CIRCL — highest-EPSS new items (30 pulled, EPSS-enriched, linked)
- **CVE-2024-8309 (EPSS 0.137, 96th pct)** — LangChain SQLi via prompt injection — [GHSA](https://github.com/advisories/GHSA-45pg-36p6-83v9)
- CVE-2026-75984 (0.013) — TRENDnet TEW-823DRU router — [CIRCL](https://vulnerability.circl.lu/advisories/cve-2026-75984)
- CVE-2026-19500 (0.005) — Brainstorm Force SureForms — [CIRCL](https://vulnerability.circl.lu/advisories/cve-2026-19500)
- CVE-2026-61263 / 61271 (Oracle E-Business Suite) — [CIRCL](https://vulnerability.circl.lu/advisories/cve-2026-61263)
- CVE-2026-21711 — Node.js Permission Model network enforcement gap — [CIRCL](https://vulnerability.circl.lu/advisories/cve-2026-21711)

### IOCs (ThreatFox 8 + URLhaus 6, newest — linked)
- **Cobalt Strike C2:** `38.76.183.197:8082`
- **Remcos RAT C2:** `107.175.88.92:2404`
- **Remus RAT panel URLs:** `zxdaone.click:6432/*`, `zakuiru.shop:9048/settings` — [Malpedia: Remus](https://malpedia.caad.fkie.fraunhofer.de/details/win.remus)
- **Live malware hosts:** `125.43.38.255:44908/bin.sh`, `2.58.56.49/ConnectProAgentSetup.msi`, `192.142.53.225` (ScreenConnect client masquerades — [URLhaus entry](https://urlhaus.abuse.ch/url/3905846/)), `hypercorevector5.lol`

---

*Compiled from public sources · 08-19-2026 · Sources: CISA KEV, CISA Advisories, Ransomware.live, CIRCL, FIRST EPSS, ThreatFox, URLhaus*
