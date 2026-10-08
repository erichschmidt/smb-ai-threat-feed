---
type: threat-feed-note
title: "Threat Feed - 10-08-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-10-08
updated: 2026-10-08
---

# Threat Feed — 10-08-2026

**The 3-minute read for small businesses running AI and automation.** Plain language in the headlines, deeper detail below. Every score and source is explained so you can act without a security degree. Full plain-English glossary: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md)

## How to read the scores

- **CISA KEV:** If a vulnerability is on this list, it is *being actively exploited right now*, not theoretical. "CISA confirmed" = the authoritative "patch fast" signal.
- **EPSS:** A 0–1 score estimating how likely a flaw is to be exploited in the next 30 days; higher = patch first. The percentile says where it ranks — 99th percentile means it's more likely to be exploited than 99% of all known vulnerabilities.
- **CVSS:** A 0–10 severity score. 9.8/10 = critical, typically exploitable remotely with no login. Answers "how bad if it works"; EPSS/KEV answer "is it actually being used."

---

## 1. HIGH — The tool that ships your software may let a user reach deployment rights they were never granted

**CVE-2026-102488 — Octopus Server** · published 10-08-2026

**What broke.** A widely used deployment-automation platform (the tool that schedules and pushes your software to servers) checks its permission settings incorrectly in some configurations. The result: a highly-privileged account can gain **deployment** rights — control over what gets shipped to production — beyond what it was actually granted. It's a permissions bug, not a remote break-in.

**Why it matters to an SMB running AI tools.** If you auto-deploy your apps, AI chatbots, or automation pipelines through Octopus Server, your deployment pipeline is one of the most sensitive pieces of infrastructure you run — it's what pushes code (and the secrets it needs) to production. A user who wasn't meant to deploy now can. Because this is a deployment tool, mistakes and misuse here land directly on your live systems, and audit logs are the only evidence you'll have.

**What you do Monday** (about 20 minutes):
1. Update Octopus Server to the latest release that fixes CVE-2026-102488 — check your version against the vendor's release notes and upgrade.
2. Review which users and teams hold deployment permission and trim it to the shortest list you actually need.
3. If you can't patch immediately, treat deployment rights as critical and review your audit log for unexpected privilege changes.

**Sources:** [CIRCL vulnerability entry CVE-2026-102488](https://vulnerability.circl.lu/vuln/CVE-2026-102488)

---

## 2. HIGH — The remote-access protocol nearly every server uses can be knocked offline by a single crafted ping

**CVE-2025-26466 — OpenSSH** · EPSS 0.41 (99th percentile — more likely to be exploited than 99% of all known vulnerabilities)

**What broke.** A long-standing bug in OpenSSH — the encrypted remote-login software behind most Linux servers — lets an unauthenticated attacker send a crafted ping that makes the server hold messages in memory until the login handshake finishes. A malicious client can repeat this to exhaust memory and crash the service — a **denial of service** (the service stops answering, so nobody gets in, including you). It requires no login and no password.

**Why it matters to an SMB running AI tools.** Almost every self-hosted AI server, database, and automation host answers on SSH. A remote permanent outage there takes your whole stack offline at once — including the servers running your models and the job schedulers that keep automations alive. At the 99th-percentile exploitation likelihood, this is one of the highest-signal items today.

**What you do Monday** (about 15 minutes, plus any package update):
1. Update the OpenSSH package on any Linux/Unix server you run (Ubuntu/Debian: `sudo apt update && sudo apt upgrade openssh-server`; Rocky/CentOS: `sudo dnf update openssh-server`).
2. Confirm password-based SSH login is disabled and only key-based logins are allowed, to shrink the attack surface.
3. Limit direct SSH access from the internet to your VPN or office IPs.

**Sources:** [CIRCL vulnerability entry CVE-2025-26466](https://vulnerability.circl.lu/vuln/CVE-2025-26466)

---

## 3. HIGH — Your mail server got 17 flaws at once, including a memory-bug path — update now

**CVE-2026-107570 / CVE-2026-107580 (and ~15 more) — hMailServer** · published 10-08-2026

**What broke.** hMailServer — a self-hosted Windows mail server used by many small businesses instead of renting hosted email — had a large batch of flaws disclosed at once. The most serious is a **heap buffer overflow** (a memory bug where software writes past the space it allocated, which attackers can turn into running their own code) triggered by a crafted email header. The others are mostly **denial-of-service** bugs where specially-crafted mail, filters, or network messages make the mail services stop answering. Several of the crashes need no login at all.

**Why it matters to an SMB running AI tools.** Your mail server gates every inbox your team and your AI tools touch — the mailbox your AI mail assistant reads, the email-to-ticket rules, the alerts your automation sends. A mail server that can be crashed remotely stops that flow, and a memory bug in the same product is a potential foothold into the machine that holds all your mail and the accounts that read it.

**What you do Monday** (about 30 minutes, plus any update):
1. Update hMailServer to the latest patched version — check the vendor's release notes for the fix for CVE-2026-107570 and the batch.
2. Confirm the mail server's admin interface is not exposed to the internet, and requires a strong admin account.
3. If remote access to that box is needed at all, require a VPN and treat the server as high-value when backing it up.

**Sources:** [CIRCL CVE-2026-107570](https://vulnerability.circl.lu/vuln/CVE-2026-107570) · [CIRCL CVE-2026-107580](https://vulnerability.circl.lu/vuln/CVE-2026-107580)

---

## 4. WATCH — A login-token library used by apps can mis-handle expiry settings, leaving sessions valid longer than intended

**CVE-2026-107275 — @fastify/jwt** · published 10-08-2026

**What broke.** A popular **JSON Web Token** (JWT — a signed digital credential an app presents to prove who it is) plugin for the Fastify web framework has a parsing bug. When a developer sets a token's expiry (`expiresIn`) or similar time settings using a format the parser can't read (like a compound span or a duration in an ISO 8601 format), the setting is mishandled — which can mean a token designed to expire doesn't expire when it should. It's a configuration/parsing flaw, not a remote break-in.

**Why it matters to an SMB running AI tools.** JWTs are how many apps and automation handlers authenticate — a machine-to-machine "key card" that grants access. If the expiry is mishandled, a session that should have ended stays alive longer than designed, widening the window a stolen token is good for. If any of your API-backed apps or integrations use this plugin, this is worth a version check.

**What you do Monday** (about 10 minutes):
1. Check whether any Fastify-based app or API you run uses the `@fastify/jwt` plugin, and which version.
2. If affected, update to the patched version and set token lifetimes explicitly in a format the plugin reads (seconds or integer milliseconds).

**Sources:** [CIRCL vulnerability entry CVE-2026-107275](https://vulnerability.circl.lu/vuln/CVE-2026-107275)

---

## Jargon buster

- **Deployment automation:** A tool that schedules and pushes your software to servers automatically. Compromise here means control over what ships to production.
- **Denial of service (DoS):** The service stops answering, so nobody gets in — including you.
- **Heap buffer overflow:** A memory bug where software writes past the space it allocated — attackers can turn it into running their own code.
- **JSON Web Token (JWT):** A signed digital credential an app or automation presents to prove who it is — a temporary key card.
- **OpenSSH:** The standard encrypted remote-login software behind most Linux/Unix servers.
- **EPSS:** A 0–1 estimate of how likely a flaw is to be exploited in the next 30 days; higher = patch first. Percentile = where it ranks vs all known vulnerabilities.
- **CISA KEV:** CISA's list of vulnerabilities being actively exploited right now — if it's on the list, patch it.

---

## Appendix

### CISA KEV — actively exploited, ranked by EPSS (most likely to be exploited first)

| CVE | Product | Added | Fed deadline | EPSS | EPSS %ile | Source |
|---|---|---|---|---|---|---|
| CVE-2026-102489 | Zammad (session → code) | 10-02-2026 | 10-05-2026 | 0.014 | 72nd | [Zammad](https://zammad.com/en/product/releases/) |
| CVE-2026-102490 | Zammad (priv escalation) | 10-02-2026 | 10-05-2026 | 0.0063 | 48th | [Zammad](https://zammad.com/en/product/releases/) |
| CVE-2026-88779 | Citrix NetScaler | 10-04-2026 | 10-07-2026 | 0.0059 | 47th | [Citrix](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697174) |

All three remain actively exploited. The Zammad pair chains into full server control and its federal deadline has passed — if you run a self-hosted helpdesk, patch it now. Citrix NetScaler's federal deadline was yesterday; if it's your remote-access front door, apply the vendor fix.

### Ransomware victims, last 24h (sector pulse — treat as sector-targeting signal, not proof)

| Group | Sector | Country | Date |
|---|---|---|---|
| qilin | Agriculture & Food Production | ES | 10-07-2026 |
| interlock | Healthcare | US | 10-07-2026 |
| Panzer | Education | DE | 10-07-2026 |
| dragonforce | Energy & Utilities | BR | 10-07-2026 |
| dragonforce | Technology | FR | 10-07-2026 |
| UmBra | Technology | EG | 10-07-2026 |
| anubis | Manufacturing | DE | 10-07-2026 |
| qilin | Other | QA | 10-07-2026 |

Ransomware crews hit healthcare, education, and energy/food sectors in the past day — a reminder these groups don't stay inside one industry. Source: [ransomware.live](https://www.ransomware.live)

### Notable vulnerabilities (CIRCL lookup)

- **Foxit PDF Editor/Reader (CVE-2026-91805):** A crafted PDF can trigger a **use-after-free** (accessing a piece of memory that's been released) in the page-tree handler, leading to memory corruption. If staff open PDFs on Foxit, update. Source: [CVE-2026-91805](https://vulnerability.circl.lu/vuln/CVE-2026-91805)
- **RESTEasy (CVE-2026-89059):** A Java web framework's image-handler decodes attacker-supplied images with no limit on declared dimensions, so an unauthenticated attacker can send one tiny image that exhausts server memory (denial of service). EPSS 0.0079 (55th). Source: [CVE-2026-89059](https://vulnerability.circl.lu/vuln/CVE-2026-89059)
- **LangChain (CVE-2024-8309) & picklescan (CVE-2025-1889):** The two AI on-lens items from yesterday's brief remain relevant and unpatched for many readers — a graph-database query-injection helper and a model-scan bypass. See the [10-07-2026 brief](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/briefs/Threat-Feed-10-07-2026.md).

### IOC sample (block-and-hunt signals — do not visit)

| Type | Value | Malware |
|---|---|---|
| domain | www.mariusbroeders.nl | ClearFake |
| domain | www.espacesante-suisse.ch | ClearFake |
| domain | 1c6pukow.sadis.store | ClearFake |
| IP:port | 95.168.180.123:24042 | Remcos |
| hash | 0322622e705bc…4b08b | AMOS |
| URL | http://112.246.228.19:33953/bin.sh | (URLhaus) |

Source: [ThreatFox](https://threatfox.abuse.ch/) (via [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/)) · [URLhaus](https://urlhaus.abuse.ch/)

---

*Compiled from public sources · 10-08-2026*
