---
type: threat-feed-note
title: "Threat Feed - 08-20-2026"
status: active
created: 2026-08-20
tags: [threat-feed, daily, smb-ai-lens]
source: "cisa-kev, cisa-advisories, ransomware.live, circl, epss, threatfox, urlhaus"
related: "https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md"
---

# Threat Feed — 08-20-2026

> **Reader promise:** 3-minute read. Headlines alone tell you what to do. New term? Check the [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md).
> **Lens:** threats that hit AI tools, automations, and small-business money.
> **Sources:** every finding links to its primary source. If you want to verify, click.

## How to read the scores (30 seconds)
- **EPSS (0–1):** the odds this flaw gets exploited in the next 30 days. 0.78 ≈ 78% — patch first. 0.01 ≈ 1% — lower urgency. Percentile ranks it against every known flaw: 99.5th = more likely to be exploited than 99.5% of all known vulnerabilities.
- **CISA KEV:** CISA only adds a flaw after confirming it's being **actively exploited right now** — not theoretical. The date shown is when CISA confirmed it. The CISA deadline is their urgency rating in date form.

---

## 1. CRITICAL — Actively exploited flaw in Microsoft Internet Key Exchange (IKE) Service Extensions
**CVE-2026-33824** · CISA confirmed active exploitation **2026-08-18** · federal patch deadline **2026-08-21** · **EPSS 0.78 (1.0th percentile)**
**Sources:** [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-33824)

**What broke:** Microsoft Internet Key Exchange (IKE) Service Extensions contains a double free vulnerability that could enable remote code execution.

**Why it matters to you:** This is on CISA's actively-exploited list — attackers are using it right now. If your business runs this product, patch it today.

**What you do (10–20 minutes):**
1. Check whether your business runs **Microsoft Internet Key Exchange (IKE) Service Extensions**. If yes, apply the vendor patch for **CVE-2026-33824** now.
2. If you use an IT provider, tell them: *"We need the patch for {cve} applied — it's being actively exploited."*
3. Confirm your backups restore, in case a machine is already hit.

**CISA metrics:** Active exploitation confirmed 2026-08-18 · federal deadline 2026-08-21.

---

## 2. HIGH — Actively exploited flaw in Microsoft SharePoint
**CVE-2026-55040** · CISA confirmed active exploitation **2026-08-18** · federal patch deadline **2026-08-21** · **EPSS 0.05 (0.9th percentile)**
**Sources:** [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-55040)

**What broke:** Microsoft SharePoint contains a weak authentication vulnerability which allows an unauthorized attacker to bypass a security feature over a network.

**Why it matters to you:** This is on CISA's actively-exploited list — attackers are using it right now. If your business runs this product, patch it today.

**What you do (10–20 minutes):**
1. Check whether your business runs **Microsoft SharePoint**. If yes, apply the vendor patch for **CVE-2026-55040** now.
2. If you use an IT provider, tell them: *"We need the patch for {cve} applied — it's being actively exploited."*
3. Confirm your backups restore, in case a machine is already hit.

**CISA metrics:** Active exploitation confirmed 2026-08-18 · federal deadline 2026-08-21.

---

## 3. HIGH — Actively exploited flaw in Broadcom VMware vCenter
**CVE-2026-59310** · CISA confirmed active exploitation **2026-08-18** · federal patch deadline **2026-08-21** · **EPSS 0.02 (0.8th percentile)**
**Sources:** [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-59310)

**What broke:** Broadcom VMware vCenter contains a path traversal vulnerability which could allow a threat actor with network access to vCenter to execute arbitrary code.

**Why it matters to you:** This is on CISA's actively-exploited list — attackers are using it right now. If your business runs this product, patch it today.

**What you do (10–20 minutes):**
1. Check whether your business runs **Broadcom VMware vCenter**. If yes, apply the vendor patch for **CVE-2026-59310** now.
2. If you use an IT provider, tell them: *"We need the patch for {cve} applied — it's being actively exploited."*
3. Confirm your backups restore, in case a machine is already hit.

**CISA metrics:** Active exploitation confirmed 2026-08-18 · federal deadline 2026-08-21.

---

## 4. HIGH — Actively exploited flaw in MLflow MLflow
**CVE-2026-64849** · CISA confirmed active exploitation **2026-08-19** · federal patch deadline **2026-09-02** · **EPSS 0.01 (0.6th percentile)**
**Sources:** [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-64849)

**What broke:** MLflow contains a server-side request forgery vulnerability that can allow attackers to reach internal or cloud metadata services and receive response_status and response_body.

**Why it matters to you:** This is on CISA's actively-exploited list — attackers are using it right now. If your business runs this product, patch it today.

**What you do (10–20 minutes):**
1. Check whether your business runs **MLflow MLflow**. If yes, apply the vendor patch for **CVE-2026-64849** now.
2. If you use an IT provider, tell them: *"We need the patch for {cve} applied — it's being actively exploited."*
3. Confirm your backups restore, in case a machine is already hit.

**CISA metrics:** Active exploitation confirmed 2026-08-19 · federal deadline 2026-09-02.

---

## 5. HIGH — Actively exploited flaw in Ray-Project Ray
**CVE-2025-62593** · CISA confirmed active exploitation **2026-08-17** · federal patch deadline **2026-08-20** · **EPSS 0.01 (0.6th percentile)**
**Sources:** [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2025-62593)

**What broke:** Ray-Project Ray contains a code injection vulnerability that could allow remote code execution. Developers using Ray as a development tool may be exposed to this vulnerability exploitable through Firefox and Safari.

**Why it matters to you:** This is on CISA's actively-exploited list — attackers are using it right now. If your business runs this product, patch it today.

**What you do (10–20 minutes):**
1. Check whether your business runs **Ray-Project Ray**. If yes, apply the vendor patch for **CVE-2025-62593** now.
2. If you use an IT provider, tell them: *"We need the patch for {cve} applied — it's being actively exploited."*
3. Confirm your backups restore, in case a machine is already hit.

**CISA metrics:** Active exploitation confirmed 2026-08-17 · federal deadline 2026-08-20.

---

## 6. HIGH — Actively exploited flaw in Apple macOS
**CVE-2026-65400** · CISA confirmed active exploitation **2026-08-18** · federal patch deadline **2026-08-21** · **EPSS 0.01 (0.5th percentile)**
**Sources:** [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-65400)

**What broke:** Apple macOS contains an improper authentication vulnerability that could allow an attacker on the network to authenticate to Screen Sharing without valid credentials.

**Why it matters to you:** This is on CISA's actively-exploited list — attackers are using it right now. If your business runs this product, patch it today.

**What you do (10–20 minutes):**
1. Check whether your business runs **Apple macOS**. If yes, apply the vendor patch for **CVE-2026-65400** now.
2. If you use an IT provider, tell them: *"We need the patch for {cve} applied — it's being actively exploited."*
3. Confirm your backups restore, in case a machine is already hit.

**CISA metrics:** Active exploitation confirmed 2026-08-18 · federal deadline 2026-08-21.

---

## Ransomware is hitting businesses like yours right now — check your backups actually restore
**Ransomware.live, last 24h:** 10 victim disclosure(s). Groups: Deadlock, Helix, everest, krybit, qilin, xpl0itrs
**Source:** [Ransomware.live](https://www.ransomware.live)

**What it means:** Small and mid-size firms in these sectors are being hit today. Ransomware groups pick by sector, and the path of least resistance is usually the business with new AI tools and nobody watching the perimeter.

**What you do (30 minutes):**
1. **Test one backup restore.** Not "check the backup ran" — actually restore one folder to a spare machine. If you can't, that's the real finding.
2. Any AI or automation tool added this year: confirm it has **MFA** and limited access. Attackers go through the new stuff first.
3. If you run or support IT for a business in one of the sectors above, use this as your own checklist.

---

## IOCs (ThreatFox + URLhaus, newest)
- **ip:port:** `143.246.216.114:38990`
- **url:** `https://guirreiro.lol/api/v1/status`
- **url:** `https://guirreiro.lol/api/v1/session`
- **url:** `https://guirreiro.lol/api/v1/verify`
- **domain:** `guirreiro.lol`
- **ip:port:** `80.190.77.86:2222`
- **ip:port:** `202.61.130.163:8888`
- **domain:** `bdwjk37712.workers.dev`
- **URL:** `http://85.108.86.149:50272/bin.sh`
- **URL:** `http://182.126.248.10:58244/bin.sh`
- **URL:** `https://github.com/atilabyte/golang/raw/refs/heads/master/scripts/install.sh`
- **URL:** `http://5.182.210.174/9a3160`
- **URL:** `http://5.182.210.174/b97872`
- **URL:** `http://5.182.210.174/f287aa`

---

_Compiled from public sources · 2026-08-20 · Sources: CISA KEV, CISA Advisories, Ransomware.live, CIRCL, FIRST EPSS, ThreatFox, URLhaus_
Free · daily · open source

### Follow the briefing
Subscribe via RSS, browse the archive and raw data on GitHub, or run the collector yourself.
[Subscribe via RSS](https://erichschmidt.com/feed.xml) · [View on GitHub](https://github.com/erichschmidt/smb-ai-threat-feed)
