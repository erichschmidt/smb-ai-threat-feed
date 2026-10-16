---
type: threat-feed-note
title: "Threat Feed - 10-16-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-10-16
updated: 2026-10-16
---

# Threat Feed — 10-16-2026

**The 3-minute read for small businesses running AI and automation.** Plain language in the headlines, deeper detail below. Full plain-English glossary: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md)

*AI-drafted from public data and published automatically. No one reviews each brief before it goes out. Check the linked source before you act.*

## How to read the scores

- **CISA KEV:** on this list means attackers are using the flaw right now.
- **EPSS:** a 0–1 estimate of how likely a flaw is to be exploited in the next 30 days; the percentile ranks it against all known flaws.
- **Severity:** CRITICAL, HIGH or WATCH, set by a fixed published rubric, not by tone.

---

## 1. WATCH — Self-hosted servers built with the MCP Python SDK can run out of memory because sessions never expire

**CVE-2026-59951 (GHSA-84m7-p3x7-pcfv) — mcp (MCP Python SDK, pip package)** · CVSS 7.5/10 (advisory rated medium) · EPSS 0.0046 (38th percentile — more likely to be exploited than 38% of known flaws) · affected >= 1.8.0, < 1.30.0 · fixed in 1.30.0 · not in KEV · low EPSS (0.0046)

**What broke.** In its default stateful mode (the server keeps a saved record, called a session, for each connected client), a server built with the MCP Python SDK never reclaimed those records: sessions did not expire, a client's disconnect request left the session registered, and a session refused on its first request stayed registered with a running task. The number of sessions was unlimited and each kept its parsed setup data, so accumulated sessions can push the server until it runs out of memory.

**Why it matters to an SMB running AI tools.** Many small businesses self-host MCP servers — the standard plug-in points that let an AI assistant reach their files, customer records, and automations — and this SDK is a common way those servers are built. No data is stolen here; the risk is an AI connector that degrades or stops answering under session buildup, so it is a patch-soon item rather than an emergency.

**What you do Monday** (about 10 minutes):
1. Upgrade the package: `pip install -U "mcp>=1.30.0"`, then restart any server built on it.
2. Ask whoever maintains your AI tools: "Do we run any self-hosted servers built on the MCP Python SDK, and are they on version 1.30.0 or later?"
3. After upgrading, restart the server and confirm versions of 1.30.0 or later are all that remains.

**Sources:** [GitHub advisory GHSA-84m7-p3x7-pcfv](https://github.com/advisories/GHSA-84m7-p3x7-pcfv)

---

## Jargon buster

- **SDK:** A toolbox of prewritten code developers use to build software.
- **Self-hosted server:** Software running on your own machines instead of the vendor's cloud.
- **Session:** A saved record of one connection between a client and a server.
- **Stateful:** A server that remembers each client between requests, instead of treating every request as new.

## Appendix

### CISA KEV — actively exploited, ranked by EPSS

| CVE | Product | CISA added | Federal deadline | EPSS | Ransomware use | Source |
|---|---|---|---|---|---|---|
| CVE-2026-104935 | Ivanti Connect Secure | 10-13-2026 | 10-16-2026 | 0.2598 | Unknown | [Ivanti advisory](https://forums.ivanti.com/s/article/Security-Advisory-Ivanti-Connect-Secure-CVE-2026-104935) |
| CVE-2026-105134 | Ahsay AhsayCBS | 10-14-2026 | 10-17-2026 | 0.0324 | Unknown | [Ahsay announcement](https://www.ahsay.com/en/company/announcements/patch-cve-105133-105134-update) |
| CVE-2026-21589 | Atlassian Multiple Products | 10-15-2026 | 10-18-2026 | 0.0278 | Unknown | [Atlassian security page](https://confluence.atlassian.com/security/cve-2026-21589-arbitrary-file-access-vulnerability-impacts-multiple-products-1870495748.html?ref=labs.watchtowr.com) |
| CVE-2026-76519 | Cisco Secure Email Gateway | 10-14-2026 | 10-17-2026 | 0.0174 | Unknown | [Cisco security advisory](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-esa-afw-zqYJkjxp) |
| CVE-2026-96951 | Microsoft Windows | 10-13-2026 | 10-16-2026 | 0.0151 | Unknown | [Microsoft update guide](https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-96951) |

**Ransomware pulse:** 10 recent victim claims; most-hit sectors: Financial Services (2), Healthcare (1), Technology (1); countries: US (6), PL (1), CR (1). · Source: [Ransomware.live](https://www.ransomware.live)

**Full data, including malware IOCs:** [latest.json](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/latest.json)

---

*Compiled from public sources · 10-16-2026*
