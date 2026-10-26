---
type: threat-feed-note
title: "Threat Feed - 10-26-2026"
status: active
tags: [threat-feed, daily, smb-ai-lens]
created: 2026-10-26
updated: 2026-10-26
---

# Threat Feed — 10-26-2026

**The 3-minute read for small businesses running AI and automation.** Plain language in the headlines, deeper detail below. Full plain-English glossary: [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md)

*AI-drafted from public data and published automatically. No one reviews each brief before it goes out. Check the linked source before you act.*

## How to read the scores

- **CISA KEV:** on this list means attackers are using the flaw right now.
- **EPSS:** a 0–1 estimate of how likely a flaw is to be exploited in the next 30 days; the percentile ranks it against all known flaws.
- **Severity:** CRITICAL, HIGH or WATCH, set by a fixed published rubric, not by tone.

---

## 1. WATCH — Self-hosted Frappe Builder lets any logged-in user run its built-in text-generation feature without a permission check

**CVE-2026-115718 — Frappe Builder** · published 10-26-2026 · not in KEV · no EPSS score yet

**What broke.** Frappe Builder versions 1.33.0 up to 1.36.0 include an "improve prompt" endpoint that sends text to a connected large language model so the tool can rewrite it more clearly. The endpoint checks that a user is logged in, but not whether that user was ever granted permission to use the feature, so any non-Guest account can trigger model calls.

**Why it matters to an SMB running AI tools.** Frappe Builder sits inside self-hosted Frappe and ERPNext installations that small manufacturers, retailers, and service firms use as their back office. A bookkeeper, temp, or vendor with a basic login could burn paid AI quota or reach a model connection the owner meant to keep restricted.

**What you do Monday** (about 20 minutes):
1. If you run Frappe Builder, upgrade to 1.36.0 or later.
2. List accounts with non-Guest access and remove any that no longer need it.
3. Check your AI provider's billing page for usage spikes you can't attribute.

**Sources:** [CIRCL advisory record](https://vulnerability.circl.lu/vuln/CVE-2026-115718)

---

## AI risk of the week: AI-written phishing

Attackers now use AI writing tools to produce phishing emails that are grammatically clean and tailored to each recipient. At a small business, that means a message can name your real vendors, reference an actual invoice, and read like it came from a coworker — with none of the spelling mistakes people were taught to spot. The defense is no longer reading for typos; it is verifying the request itself. This week, pick one payment or credential change you've received by email recently and confirm it by phone through a number you already had on file, not one the message provided.

## Jargon buster

- **Frappe Builder:** A self-hosted drag-and-drop web page tool in the Frappe/ERPNext business-software stack.
- **LLM (large language model):** The AI text engine behind chatbots and automatic writing tools.
- **Phishing:** Fraudulent messages that trick you into clicking a link or surrendering a password.
- **Prompt:** The text you type when asking an AI tool to do or write something.

## Appendix

### CISA KEV — actively exploited, ranked by EPSS

| CVE | Product | CISA added | Federal deadline | EPSS | Ransomware use | Source |
|---|---|---|---|---|---|---|
| CVE-2026-110447 | Collabora Collabora Online – Built-in CODE Server | 10-23-2026 | 10-26-2026 | 0.1233 | Unknown | [source](https://help.nextcloud.com/t/to-collabora-built-in-user-update-asap/250516) |
| CVE-2026-106931 | EG Secure Solutions SiteGuard Server Edition | 10-20-2026 | 10-23-2026 | 0.0253 | Unknown | [source](https://www.eg-secure.co.jp/siteguard/news/alert-202610-1) |
| CVE-2026-96654 | Plex Media Server | 10-20-2026 | 10-23-2026 | 0.0195 | Unknown | [source](https://forums.plex.tv/t/important-security-update-for-plex-media-server-v1-43-2-and-earlier/942319) |
| CVE-2026-96652 | Plex Media Server | 10-20-2026 | 11-03-2026 | 0.0182 | Unknown | [source](https://forums.plex.tv/t/important-security-update-for-plex-media-server-v1-43-2-and-earlier/942319) |
| CVE-2026-96656 | Plex Media Server | 10-20-2026 | 10-23-2026 | 0.0179 | Unknown | [source](https://forums.plex.tv/t/important-security-update-for-plex-media-server-v1-43-2-and-earlier/942319) |

**Ransomware pulse:** 10 recent victim claims; most-hit sectors: Professional Services (3), Government & Defense (2), Retail & E-Commerce (1); countries: US (5), DE (3), AR (1). · Source: [Ransomware.live](https://www.ransomware.live)

**Full data, including malware IOCs:** [latest.json](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/latest.json)

---

*Compiled from public sources · 10-26-2026*
