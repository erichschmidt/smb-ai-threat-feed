---
type: threat-feed-note
title: "Threat Feed - 10-12-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-10-12
updated: 2026-10-12
---

# Threat Feed — 10-12-2026

**The 3-minute read for small businesses running AI and automation.** Plain language in the headlines, deeper detail below. Full plain-English glossary: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md)

*AI-drafted from public data and published automatically. No one reviews each brief before it goes out. Check the linked source before you act.*

## How to read the scores

- **CISA KEV:** on this list means attackers are using the flaw right now.
- **EPSS:** a 0–1 estimate of how likely a flaw is to be exploited in the next 30 days; the percentile ranks it against all known flaws.
- **Severity:** CRITICAL, HIGH or WATCH, set by a fixed published rubric, not by tone.

---

## 1. HIGH — A self-hosted AI app can let an outsider run its flows with no login — update Langflow now

**CVE-2026-8505 — Langflow** · CVSS 9.8/10 = critical · EPSS 0.0072 (53rd percentile) · affected >=1.7.0, <=1.9.0 · fixed in 1.9.1 · not in KEV · remote code execution without a login

**What broke.** Langflow, a popular open-source tool for building AI flows, verifies its webhook (an automated callback one system sends another) callers with an API key — but when the webhook-auth setting is turned off, it skips that check entirely. A remote attacker who knows a flow's address can then run that flow as if they owned it, which can end in code execution on the server.

**Why it matters to an SMB running AI tools.** Langflow is exactly the kind of self-hosted AI plumbing small businesses stand up to prototype flows and connect to their data. If a flow can run code or touch internal tools, an unauthenticated trigger is a door straight into your AI stack — upgrade to the patched release first.

**What you do Monday** (about 15 minutes):
1. Check your Langflow version (any 1.7.0 through 1.9.0 is affected).
2. Upgrade Langflow to 1.9.1 or later.
3. Keep webhook authentication enabled (`WEBHOOK_AUTH_ENABLE` on) in the meantime.

**Sources:** [GitHub advisory GHSA-cf6m-vc3m-7cgm](https://github.com/advisories/GHSA-cf6m-vc3m-7cgm)

---
## 2. WATCH — An AI server's file-analysis agents can be coaxed into sending your data out — update Flowise

**CVE-2026-73487 — Flowise** · EPSS 0.0096 (60th percentile) · affected <=3.1.2 · fixed in 3.1.3 · not in KEV · low EPSS (0.0096)

**What broke.** Flowise, an open-source tool for building AI workflows, lets its CSV and Airtable agents run code that a safety filter is supposed to block. A crafted prompt can slip past that filter and make the agent send the loaded data to an external server or reach internal services.

**Why it matters to an SMB running AI tools.** This is a prompt-injection risk on a tool small teams use to connect AI to spreadsheets and records. If a Flowise agent handles customer data, a well-crafted prompt can exfiltrate it — upgrade to 3.1.3 or later.

**What you do Monday** (about 15 minutes, if you run Flowise):
1. Check your Flowise version (3.1.2 and earlier are affected).
2. Upgrade Flowise to 3.1.3 or later.
3. Avoid connecting sensitive files to agent-exposed CSV or Airtable nodes until patched.

**Sources:** [GitHub advisory GHSA-w7x8-q2gp-5cgg](https://github.com/advisories/GHSA-w7x8-q2gp-5cgg)

---
## 3. WATCH — The plug-in layer for AI assistants can hand your login credentials to the wrong server — update the SDK

**CVE-2026-104850 — MCP TypeScript SDK** · CVSS 7.5/10 = high · EPSS 0.0018 (7th percentile) · affected >=1.12.0, <1.31.0 · fixed in 1.31.0 · not in KEV · low EPSS (0.0018)

**What broke.** The MCP (Model Context Protocol — the plug-in standard that lets an AI assistant use extra tools) TypeScript SDK has a flaw in its OAuth login flow: it lets the remote server name its own authorization server, and sends that server the stored refresh token and client secret with no user action. A malicious or compromised MCP server can therefore collect the credentials meant for services you trust.

**Why it matters to an SMB running AI tools.** Small businesses increasingly connect AI assistants to their tools through MCP servers — databases, files, cloud services. If one of those servers is malicious it can capture the stored credentials your assistant uses, so upgrade any app built on the affected SDK and re-check which MCP servers you are connected to.

**What you do Monday** (about 20 minutes):
1. Identify AI assistants or apps built on the MCP TypeScript SDK in versions 1.12.0 through 1.30.x.
2. Upgrade the SDK to 1.31.0 or later.
3. Consider re-issuing credentials for any assistant you have connected to third-party MCP servers.

**Sources:** [GitHub advisory GHSA-6qxp-vccf-f47h](https://github.com/advisories/GHSA-6qxp-vccf-f47h)

---
## Also on the radar

- **Langflow** — Python interpreter runs unsandboxed code, so an insider can take over the server (WATCH, GHSA-8qpj-27x8-pwpq) · [source](https://github.com/advisories/GHSA-8qpj-27x8-pwpq)
- **Flowise** — sandbox can be escaped to read files or run code (WATCH, GHSA-9gvv-qjj3-2p6g) · [source](https://github.com/advisories/GHSA-9gvv-qjj3-2p6g)
- **Langflow** — a crafted MCP config can run operating-system commands (WATCH, GHSA-w794-rj3p-xv45) · [source](https://github.com/advisories/GHSA-w794-rj3p-xv45)

## AI risk of the week: AI integrations with too much access

The risk is that an AI tool is connected with more access than its job needs — an OAuth grant, an API key, or an MCP server that can read, write, or reach far more than a single task requires. At a small business this looks like an assistant connected to all of email, a chatbot holding a database write key, or a broker granted broad access across every business app. This week, list every AI tool you have connected and write down the narrowest access each one actually needs, then revoke any grant or key that goes beyond it. Start with the highest-value data (finance, customer records, HR) and add a quick access review whenever a new integration is requested.

## Jargon buster

- **MCP server:** The plug-in that lets an AI assistant reach a tool or service.
- **Authorization server:** The login service that approves an app's access and holds its credentials.
- **Webhook:** An automated callback one system sends another.
- **Prompt injection:** Tricking an AI by hiding instructions inside the data it reads.

## Appendix

### CISA KEV — actively exploited, ranked by EPSS

| CVE | Product | CISA added | Federal deadline | EPSS | Ransomware use | Source |
|---|---|---|---|---|---|---|
| CVE-2015-3306 | ProFTPD | 10-08-2026 | 10-11-2026 | 0.995 | Unknown | [Debian advisory](https://lists.debian.org/debian-security-announce/2015/msg00154.html) |
| CVE-2015-5477 | ISC BIND | 10-08-2026 | 10-11-2026 | 0.994 | Unknown | [Red Hat errata](https://access.redhat.com/errata/RHSA-2015:1513.html) |
| CVE-2016-3081 | Apache Struts | 10-08-2026 | 10-11-2026 | 0.961 | Unknown | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2016-3081) |
| CVE-2021-3199 | ONLYOFFICE Docs | 10-08-2026 | 10-11-2026 | 0.194 | Unknown | [ONLYOFFICE changelog](https://github.com/ONLYOFFICE/DocumentServer/blob/903fe5ab7a275bd69c3c3346af2d21cf87ebeabf/CHANGELOG.md) |
| CVE-2023-22894 | Strapi | 10-08-2026 | 10-11-2026 | 0.036 | Unknown | [Strapi releases](https://github.com/strapi/strapi/releases) |

**Ransomware pulse:** 10 recent victim claims; most-hit sectors: Energy & Utilities (1), Transportation (1); countries: US (2), CA (1). · Source: [Ransomware.live](https://www.ransomware.live)

**Full data, including malware IOCs:** [latest.json](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/latest.json)

---

*Compiled from public sources · 10-12-2026*
