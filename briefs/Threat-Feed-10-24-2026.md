---
type: threat-feed-note
title: "Threat Feed - 10-24-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-10-24
updated: 2026-10-24
---

# Threat Feed — 10-24-2026

**The 3-minute read for small businesses running AI and automation.** Plain language in the headlines, deeper detail below. Full plain-English glossary: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md)

*AI-drafted from public data and published automatically. No one reviews each brief before it goes out. Check the linked source before you act.*

## How to read the scores

- **CISA KEV:** on this list means attackers are using the flaw right now.
- **EPSS:** a 0–1 estimate of how likely a flaw is to be exploited in the next 30 days; the percentile ranks it against all known flaws.
- **Severity:** CRITICAL, HIGH or WATCH, set by a fixed published rubric, not by tone.

---

## 1. WATCH — Self-hosted MLflow servers with file storage may let outsiders place files where they shouldn't

**CVE-2026-53995 — MLflow** · EPSS 0.0056 (46th percentile — more likely to be exploited than 46% of known flaws) · CVSS 8.2/10 = high · affected <= 3.17.1 · fixed in 3.17.2 · not in KEV · low EPSS (0.0056)

**What broke.** MLflow, an open-source tracker teams use for AI experiments and model runs, has a path traversal flaw (a trick where special characters in a field point the software at folders it shouldn't touch) in its FileStore backend, which saves records as plain files. An attacker with no login can submit a crafted trace label (an ID for a saved AI run) to the traces API, and the server writes its record files to paths the attacker controls instead of the intended folder.

**Why it matters to an SMB running AI tools.** A self-hosted MLflow box often sits close to training data, model files, and cloud credentials, so a file-write hole there is a doorway into the AI workspace itself. If your team runs MLflow with the file-based backend and its tracking API is reachable beyond a locked-down internal network, the update is worth doing before this gets wider attention.

**What you do Monday** (about 20 minutes):
1. Upgrade mlflow to 3.17.2 or later (`pip install -U mlflow` on the server that runs it).
2. If someone else manages your servers, say exactly this: "Please upgrade our MLflow server to version 3.17.2 or later and confirm whether it uses the file-based store."
3. Check that MLflow's tracking API is not reachable from the public internet.

**Sources:** [GitHub advisory GHSA-wqmh-qccw-pqwf](https://github.com/advisories/GHSA-wqmh-qccw-pqwf)

---

## 2. WATCH — Public vLLM AI servers can be knocked offline by oversized image and video requests

**CVE-2026-114055 — vLLM** · EPSS 0.0034 (27th percentile — more likely to be exploited than 27% of known flaws) · CVSS 7.5/10 = high · affected >= 0.7.3, < 0.31.0 · fixed in 0.31.0 · not in KEV · low EPSS (0.0034)

**What broke.** vLLM is open-source software for running large AI models on your own servers, including ones that accept images and video. Remote clients could attach per-request settings that control image size, patch count, or frame count, and those values were passed along without limits — so one crafted request could make the server burn so much memory or time that it stalls or crashes.

**Why it matters to an SMB running AI tools.** If your business exposes a vLLM endpoint to customers or the public, one visitor can take your AI service offline for everyone — an outage lever rather than a data-theft lever. Teams self-hosting an image-capable AI chatbot or document analyzer on vLLM should treat this as a scheduled update, not an emergency.

**What you do Monday** (about 15 minutes):
1. Upgrade vllm to 0.31.0 or later (`pip install -U vllm`, or rebuild the container image).
2. If someone else manages it, say exactly this: "Please update our vLLM inference server to version 0.31.0 or later."
3. Confirm the vLLM API is behind authentication or an internal network, not open to the internet.

**Sources:** [GitHub advisory GHSA-gx7p-2j49-hfq4](https://github.com/advisories/GHSA-gx7p-2j49-hfq4)

---

## Also on the radar

- **vLLM** — Crafted image requests could crash the whole AI engine. (WATCH, GHSA-p92p-rxj5-7p2x) · [source](https://github.com/advisories/GHSA-p92p-rxj5-7p2x)
- **MLflow** — An open server could be tricked into fetching internal web addresses. (WATCH, GHSA-2wqp-q3c6-ccj5) · [source](https://github.com/advisories/GHSA-2wqp-q3c6-ccj5)

## Jargon buster

- **Path traversal:** Sneaking special characters into a field to reach folders outside the intended one.
- **MLflow:** Open-source tool teams use to track AI experiments, runs, and models.
- **vLLM:** Open-source software that runs large AI models on your own hardware.
- **Denial of service (DoS):** An attack that crashes or stalls a service so nobody can use it.

## Appendix

### CISA KEV — actively exploited, ranked by EPSS

| CVE | Product | CISA added | Federal deadline | EPSS | Ransomware use | Source |
|---|---|---|---|---|---|---|
| CVE-2026-110447 | Collabora Online – Built-in CODE Server | 10-23-2026 | 10-26-2026 | 0.0123 | Unknown | [source](https://help.nextcloud.com/t/to-collabora-built-in-user-update-asap/250516) |
| CVE-2026-106931 | EG Secure Solutions SiteGuard Server Edition | 10-20-2026 | 10-23-2026 | 0.0117 | Unknown | [source](https://www.eg-secure.co.jp/siteguard/news/alert-202610-1) |
| CVE-2026-96656 | Plex Media Server | 10-20-2026 | 10-23-2026 | 0.0082 | Unknown | [source](https://forums.plex.tv/t/important-security-update-for-plex-media-server-v1-43-2-and-earlier/942319) |
| CVE-2026-114625 | Arista VeloCloud Orchestrator | 10-23-2026 | 10-26-2026 | 0.0056 | Unknown | [source](https://www.arista.com/en/support/advisories-notices/security-advisory/24838-security-advisory-0199) |
| CVE-2026-96654 | Plex Media Server | 10-20-2026 | 10-23-2026 | 0.0046 | Unknown | [source](https://forums.plex.tv/t/important-security-update-for-plex-media-server-v1-43-2-and-earlier/942319) |

**Ransomware pulse:** No recent ransomware victim claims in the latest listing. · Source: [Ransomware.live](https://www.ransomware.live)

**Full data, including malware IOCs:** [latest.json](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/latest.json)

---

*Compiled from public sources · 10-24-2026*
