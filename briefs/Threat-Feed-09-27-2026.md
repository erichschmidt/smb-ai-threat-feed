---
type: threat-feed-note
title: "Threat Feed — 09-27-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
date: 09-27-2026
---

# Threat Feed — 09-27-2026

*Threat intel for people deploying AI and automation in small businesses. 3-minute read: skim the headlines, then check the [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md) if a term is new.*

## How to read the scores
- **EPSS:** a 0–1 score estimating how likely a flaw is to be exploited in the next 30 days; higher = patch first. The percentile (e.g. "97th") is how that score ranks against every known vulnerability.
- **CISA KEV:** a flaw on this list is being actively exploited right now (not theoretical); the federal deadline is the "patch by" anchor.
- **CVSS:** a 0–10 severity score; 9.8/10 is critical, typically exploitable remotely with no login.

---

## Items

### 1. HIGH — Your design tool's AI (MCP) plugin leaves an unauthenticated door open on your network
**CVE-2026-100868 · Penpot < 2.18.0 · single-user mode**

Penpot is an open-source design platform many small teams run to prototype product UI. In single-user mode it binds its **MCP** (Model Context Protocol — the standard way AI tools hook into other software) server plugin WebSocket bridge to *all* network interfaces with **no authentication**. Anyone on an adjacent network can connect to that port and impersonate the Penpot browser session. For a small business running Penpot on a shared office or home LAN, that means a non-technical attacker on the same network can hijack the design/editor session and the AI tooling wired into it.

**Do:** check your Penpot version and upgrade past 2.18.0; if you run it in single-user mode on a shared network, upgrade now and keep the instance off exposed interfaces. **Do not:** leave single-user Penpot reachable beyond your trusted network.

**Sources:** [CIRCL advisory](https://vulnerability.circl.lu/)

---

### 2. CRITICAL — WordPress core has a remote file-inclusion bug — and it's already on the actively-exploited list
**CVE-2026-87902 · WordPress Core · added to CISA KEV 09-25-2026 · EPSS 0.1817 (97th percentile)**

A remote file-inclusion flaw in WordPress core lets an **unauthenticated** attacker make page-template resolution pull in a chosen readable local `.php` file from outside the active theme directories — a path that can lead to remote code execution. It's new on the CISA KEV list (federal patch deadline **09-28-2026**) with a 97th-percentile EPSS, so expect real-world exploitation now. For the huge share of SMBs running WordPress for their site, this is a patch-this-week emergency.

**What you do Monday** — 1. Update WordPress core to the patched release via the admin dashboard (or your host's updater). ~10 minutes. 2. If you don't know your version, check `wp-admin` → Dashboard and update. 3. After patching, look for any unexpected files or themes dropped in `wp-content/` as a tamper check.

**Sources:** [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-87902)

---

### 3. CRITICAL — Adobe Commerce/Magento flaw is the single most-likely-to-be-exploited item on today's list
**CVE-2026-71362 · Adobe Commerce & Magento · added to CISA KEV 09-24-2026 · EPSS 0.8751 (99th percentile)**

An incorrect authorization flaw in Adobe Commerce and Magento is sitting at an **0.8751 EPSS — the 99th percentile**, the highest exploitation likelihood on today's feed. If your store runs on Adobe Commerce/Magento, this is effectively a "they will target you" signal. Federal deadline **09-27-2026** (today).

**What you do Monday** — 1. Apply the Adobe security update from APSB26-92 today. ~30–60 minutes with a maintenance window. 2. If you run it on a managed host, confirm the patch is deployed before assuming coverage. 3. Check for any unexpected admin/API changes afterward as a tamper check.

**Sources:** [Adobe advisory APSB26-92](https://helpx.adobe.com/security/products/magento/apsb26-92.html) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

---

### 4. WATCH — Your terminal AI cheatsheet tool can be tricked into running commands
**CVE-2026-101032 · navi (terminal cheatsheet/CLI assistant) · EPSS n/a**

`navi` is a terminal tool many devs/AI workflows use to look up and run cheatsheet commands. It fails to properly escape cheatsheet variable values when substituting them into shell commands, so an attacker who controls a crafted file name in a suggestion command directory can inject shell metacharacters and execute arbitrary commands. In a small shop, this is a local/tooling risk rather than a network emergency — but it's exactly the kind of AI-adjacent CLI tool an automation setup might trust.

**Do:** update navi; don't run it against untrusted suggestion directories. **Do not:** treat terminal-assistant output as safe to blindly execute.

**Sources:** [CIRCL advisory](https://vulnerability.circl.lu/)

---

## Jargon buster
- **MCP (Model Context Protocol):** the standard way AI tools connect to other software; a plugin exposing it unauthenticated is a real gap.
- **Remote file inclusion:** forcing an app to load and run a file the attacker chose.
- **EPSS:** a 0–1 model score for "how likely is this to be exploited soon."

*(Growing glossary: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).)*

---

## Appendix — CISA KEV (actively exploited), ranked by EPSS

| CVE | Product | EPSS (percentile) | Federal deadline |
|---|---|---|---|
| CVE-2026-71362 | Adobe Commerce/Magento | 0.8751 (99th) | 09-27-2026 |
| CVE-2026-93616 | Check Point Security Gateway | 0.1965 (97th) | 09-25-2026 |
| CVE-2026-87902 | WordPress Core | 0.1817 (97th) | 09-28-2026 |
| CVE-2026-7273 | Zyxel GS1900 switches | 0.0250 (84th) | 09-24-2026 |
| CVE-2026-94127 | F5 BIG-IP APM | 0.0223 (82nd) | 09-25-2026 |
| CVE-2026-65660 | Microsoft SharePoint | 0.0210 (80th) | 09-28-2026 |
| CVE-2026-67279 | MikroTik RouterOS | 0.0103 (62nd) | 09-28-2026 |
| CVE-2026-85102 | Check Point VPN | 0.0099 (61st) | 09-25-2026 |
| CVE-2026-93952 | Arista VeloCloud | 0.0089 (58th) | 09-25-2026 |
| CVE-2026-5430 | WSO2 | 0.0059 (46th) | 09-27-2026 |

*Compiled from public sources · 09-27-2026*
