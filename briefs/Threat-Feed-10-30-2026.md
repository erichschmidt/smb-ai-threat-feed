---
type: threat-feed-note
title: "Threat Feed - 10-30-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-10-30
updated: 2026-10-30
---

# Threat Feed — 10-30-2026

**The 3-minute read for small businesses running AI and automation.** Plain language in the headlines, deeper detail below. Full plain-English glossary: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md)

*AI-drafted from public data and published automatically. No one reviews each brief before it goes out. Check the linked source before you act.*

## How to read the scores

- **CISA KEV:** on this list means attackers are using the flaw right now.
- **EPSS:** a 0–1 estimate of how likely a flaw is to be exploited in the next 30 days; the percentile ranks it against all known flaws.
- **Severity:** CRITICAL, HIGH or WATCH, set by a fixed published rubric, not by tone.

---

## 1. WATCH — A flaw in n8n's Databricks connector can let outsiders reach data endpoints they should not

**CVE-2026-119557 — n8n** · affected n8n 2.14.0 through 2.46.3 · not in KEV · no EPSS score yet

**What broke.** n8n versions 2.14.0 through 2.46.3 contain a path traversal flaw (an input trick that makes software look past the location it intended) in the node that connects to Databricks, a cloud data platform. An unauthenticated attacker can inject `../` sequences into a resource identifier and make the n8n server call arbitrary Databricks API endpoints using the connection saved on that server.

**Why it matters to an SMB running AI tools.** n8n is a common way small businesses wire chatbots, model calls, and SaaS tools into automated workflows, and a saved Databricks connection means stored warehouse credentials. If the connector is reachable, an outsider can use your own automation server as a bridge into your data.

**What you do Monday** (about 10 minutes):
1. Check your n8n version; if it is between 2.14.0 and 2.46.3, plan the upgrade when a fixed release is available.
2. Confirm the n8n instance is not reachable from the open internet without a login.
3. Review recent activity in your Databricks access logs for calls you did not make.

**Sources:** [CIRCL advisory record](https://vulnerability.circl.lu/vuln/CVE-2026-119557)

---

## 2. CRITICAL — GitLab servers are being exploited now through a flaw in pipeline configuration checks

**CVE-2026-97229 — GitLab Community Edition and Enterprise Edition** · EPSS 0.1843 (97th percentile — more likely to be exploited than 97% of known flaws) · CISA confirmed active exploitation on 10-29-2026 · federal patch deadline 11-01-2026 · known ransomware use: Unknown · in CISA KEV · no login needed

**What broke.** GitLab Community and Enterprise Editions contain an integer overflow flaw (a counting error that makes software misjudge the size of data) in the component that compiles regular expressions (short patterns used to match text) inside CI/CD pipeline configurations. An unauthenticated attacker can submit a pipeline config with a crafted pattern and execute arbitrary code on the GitLab server.

**Why it matters to an SMB running AI tools.** General IT hygiene — no specific AI angle. Teams often keep deploy keys, API tokens, and source code in GitLab, and AI tooling increasingly reads from those same repositories. A taken-over GitLab server hands an attacker that code and the secrets the pipelines hold.

**What you do Monday** (about 15 minutes):
1. Patch self-hosted GitLab to version 19.4.2 or later per the vendor advisory below.
2. If patching cannot finish before 11-01-2026, at least block internet access to the GitLab server until it is done.
3. Check recent CI/CD pipeline configuration changes for edits nobody recognizes.

**Sources:** [GitLab patch release](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-4-2-released/) · [NVD record](https://nvd.nist.gov/vuln/detail/CVE-2026-97229)

---

## Also on the radar

- **mlflow** — Flaw lets unauthenticated HTTP callers run code on self-hosted MLflow servers. (HIGH, GHSA-26p8-2jq9-3vq9) · [source](https://github.com/advisories/GHSA-26p8-2jq9-3vq9)

## Jargon buster

- **Path traversal:** Input trick using `../` sequences to look beyond where software intends.
- **Integer overflow:** Counting error where a value wraps around and the software misjudges size.
- **Regular expression:** Compact text pattern software uses to search or match input.
- **CI/CD pipeline:** Automated system that tests and ships code changes.

## Appendix

### CISA KEV — actively exploited, ranked by EPSS

| CVE | Product | CISA added | Federal deadline | EPSS | Ransomware use | Source |
|---|---|---|---|---|---|---|
| CVE-2026-109618 | PHP | 10-26-2026 | 10-29-2026 | 1.0 | Unknown | [CISA alert on PHP patching](https://www.cisa.gov/news-events/alerts/2026-10-21/critical-vulnerabilities-php-require-immediate-patching) |
| CVE-2026-109619 | PHP | 10-26-2026 | 10-29-2026 | 1.0 | Unknown | [CISA alert on PHP patching](https://www.cisa.gov/news-events/alerts/2026-10-21/critical-vulnerabilities-php-require-immediate-patching) |
| CVE-2026-111497 | Google Brotli | 10-27-2026 | 11-10-2026 | 0.8264 | Unknown | [NVD record](https://nvd.nist.gov/vuln/detail/CVE-2026-111497) |
| CVE-2026-48356 | Adobe Commerce and Magento | 10-27-2026 | 11-10-2026 | 0.4458 | Unknown | [Adobe security bulletin](https://www.adobe.com/trust/security/products/commerce/apsb26-73.html) |
| CVE-2026-97229 | GitLab Community Edition and Enterprise Edition | 10-29-2026 | 11-01-2026 | 0.1843 | Unknown | [GitLab patch release](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-4-2-released/) |

**Ransomware pulse:** 10 recent victim claims; most-hit sectors: Professional Services (2), Healthcare (2), Energy & Utilities (1); countries: US (2), GB (1). · Source: [Ransomware.live](https://www.ransomware.live)

**Full data, including malware IOCs:** [latest.json](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/latest.json)

---

*Compiled from public sources · 10-30-2026*
