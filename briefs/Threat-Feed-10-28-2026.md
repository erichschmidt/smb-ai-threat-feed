---
type: threat-feed-note
title: "Threat Feed - 10-28-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-10-28
updated: 2026-10-28
---

# Threat Feed — 10-28-2026

**The 3-minute read for small businesses running AI and automation.** Plain language in the headlines, deeper detail below. Full plain-English glossary: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md)

*AI-drafted from public data and published automatically. No one reviews each brief before it goes out. Check the linked source before you act.*

## How to read the scores

- **CISA KEV:** on this list means attackers are using the flaw right now.
- **EPSS:** a 0–1 estimate of how likely a flaw is to be exploited in the next 30 days; the percentile ranks it against all known flaws.
- **Severity:** CRITICAL, HIGH or WATCH, set by a fixed published rubric, not by tone.

---

## 1. HIGH — MLflow servers that skip login checks let remote callers run their own code

**CVE-2026-116692 (GHSA-26p8-2jq9-3vq9) — MLflow** · CVSS 9.8/10 = critical · affected >= 3.12.0rc0, < 3.17.0 · fixed in 3.17.0 · not in KEV · remote code execution without a login

**What broke.** MLflow added a way to register third-party scoring tools, and when the server loads one it follows a module path chosen by the caller instead of code that was reviewed and approved. Combined with how MLflow stores files, a remote caller can leave that module in place first and get their own code running on a server that does not require a login.

**Why it matters to an SMB running AI tools.** MLflow is the kind of tracker that sits next to AI training data and cloud keys, so a takeover reaches well past one server. If a small business self-hosts MLflow with no login screen, anyone who can reach that port is a potential admin.

**What you do Monday** (about 20 minutes):
1. Upgrade mlflow to 3.17.0 or later (`pip install -U "mlflow>=3.17.0"`).
2. Turn on authentication for every MLflow server that is reachable from outside the team.
3. If no one runs MLflow for you, forward the advisory to whoever manages your AI stack and ask them to confirm the version in use.

**Sources:** [GitHub advisory GHSA-26p8-2jq9-3vq9](https://github.com/advisories/GHSA-26p8-2jq9-3vq9)

---

## 2. WATCH — Self-hosted LiteLLM gateways can let ordinary users climb to admin

**CVE-2026-114612 (GHSA-7hp6-4w63-5g45) — LiteLLM** · CVSS 9.9/10 = critical · EPSS 0.0032 (25th percentile — more likely to be exploited than 25% of known flaws) · affected >= 1.91.0, < 1.100.4 · fixed in 1.100.4 · not in KEV · low EPSS (0.0032)

**What broke.** LiteLLM uses one encryption key for two jobs: protecting stored secrets and issuing session tokens. A logged-in ordinary user can ask the server to encrypt a forged admin credential as if it were a stored secret, and get back something the proxy accepts as admin access, with remote code execution reachable from there.

**Why it matters to an SMB running AI tools.** A LiteLLM gateway holds the keys to every AI service it fronts, so admin there means admin over your whole AI traffic and its billing. The climb requires an already-logged-in user, so the risk concentrates on gateways that hand accounts to many staff or contractors.

**What you do Monday** (about 15 minutes):
1. Upgrade litellm to 1.100.4 or later.
2. List who holds ordinary user accounts on the proxy and remove the ones that are not needed.
3. If you do not patch it yourself, say: "Our LiteLLM proxy is vulnerable to CVE-2026-114612 — please upgrade it to 1.100.4 or later."

**Sources:** [GitHub advisory GHSA-7hp6-4w63-5g45](https://github.com/advisories/GHSA-7hp6-4w63-5g45)

---

## 3. CRITICAL — A flaw in the Brotli compression used across the web is being exploited now

**CVE-2026-111497 — Google Brotli** · EPSS 0.5548 (99th percentile — more likely to be exploited than 99% of known flaws) · CISA confirmed active exploitation on 10-27-2026 · federal patch deadline 11-10-2026 · known ransomware use: Unknown · in CISA KEV · no login needed

**What broke.** Google's Brotli compression library shrinks web content so browsers and apps load it faster, and it contains an unchecked return value bug (the decoder ignores a failure signal and keeps working with corrupted data). A remote attacker with no login can send a crafted compressed stream that corrupts memory, discloses sensitive memory contents, crashes the software, or potentially runs their own code.

**Why it matters to an SMB running AI tools.** General IT hygiene — no specific AI angle. Brotli ships inside popular browsers and many backend and document tools, so the fix arrives through ordinary app updates from each software vendor rather than one patch you apply yourself.

**What you do Monday** (about 10 minutes):
1. Update browsers and any software that fetches web content to the latest vendor builds.
2. Ask your IT person: "Does anything we run use Google's Brotli library, and has it been updated to Brotli 1.2.1 or a patched build that bundles it?"
3. Treat the federal deadline of 11-10-2026 as the yardstick: patch everything reachable before then.

**Sources:** [NVD — CVE-2026-111497](https://nvd.nist.gov/vuln/detail/CVE-2026-111497) · [Brotli v1.2.1 release](https://github.com/google/brotli/releases/tag/v1.2.1)

---

## Also on the radar

- **LiteLLM** — A logged-in user could read local files they shouldn't. (WATCH, GHSA-g5ff-637f-6q2m) · [source](https://github.com/advisories/GHSA-g5ff-637f-6q2m)
- **@modelcontextprotocol/sdk** — A public MCP server can be knocked offline by oversized requests. (WATCH, GHSA-f897-62hf-6gxq) · [source](https://github.com/advisories/GHSA-f897-62hf-6gxq)
- **vLLM** — vLLM can run attacker-chosen code when set to trust remote code. (WATCH, CVE-2026-114053) · [source](https://github.com/advisories/GHSA-h3rc-6mm3-gc2m)

## Jargon buster

- **Brotli:** Google's open-source compression library that shrinks web content for faster loading.
- **Unchecked return value:** Software ignores a failure signal and keeps running on bad data.
- **Deserialization:** Rebuilding saved data into live program objects; attacker-built data can run code.
- **Session token:** A string a server hands out to recognize a returning user.

## Appendix

### CISA KEV — actively exploited, ranked by EPSS

| CVE | Product | CISA added | Federal deadline | EPSS | Ransomware use | Source |
|---|---|---|---|---|---|---|
| CVE-2026-109618 | PHP Group PHP | 10-26-2026 | 10-29-2026 | 1.0 | Unknown | [CISA alert](https://www.cisa.gov/news-events/alerts/2026-10-21/critical-vulnerabilities-php-require-immediate-patching) |
| CVE-2026-109619 | PHP Group PHP | 10-26-2026 | 10-29-2026 | 1.0 | Unknown | [CISA alert](https://www.cisa.gov/news-events/alerts/2026-10-21/critical-vulnerabilities-php-require-immediate-patching) |
| CVE-2026-111497 | Google Brotli | 10-27-2026 | 11-10-2026 | 0.5548 | Unknown | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-111497) |
| CVE-2026-48356 | Adobe Commerce and Magento | 10-27-2026 | 11-10-2026 | 0.3058 | Unknown | [Adobe APSB26-73](https://www.adobe.com/trust/security/products/commerce/apsb26-73.html) |
| CVE-2026-110447 | Collabora Online – Built-in CODE Server | 10-23-2026 | 10-26-2026 | 0.1163 | Unknown | [Nextcloud forum](https://help.nextcloud.com/t/to-collabora-built-in-user-update-asap/250516) |

**Ransomware pulse:** 10 recent victim claims; most-hit sectors: Transportation (2), Technology (1), Retail & E-Commerce (1); countries: US (4), DE (1), BE (1). · Source: [Ransomware.live](https://www.ransomware.live)

**Full data, including malware IOCs:** [latest.json](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/latest.json)

---

*Compiled from public sources · 10-28-2026*
