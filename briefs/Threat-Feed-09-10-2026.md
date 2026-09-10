---
type: threat-feed-note
title: "Threat Feed — 09-10-2026"
status: published
tags: [threat-feed, daily, smb-ai-lens]
created: 09-10-2026
---

# Threat Feed — 09-10-2026

A three-minute security brief for small businesses deploying AI and automation. Read the headlines and [GLOSSARY.md](https://github.com/erichschmidt/smb-ai-threat-feed/blob/main/GLOSSARY.md) to get the decision; use the appendix to verify the signals.

## How to read the scores

- **EPSS** is a 0–1 score estimating how likely a flaw is to be exploited in the next 30 days; higher means patch first. Its percentile shows rank among known flaws: 99.5th percentile means more likely to be exploited than 99.5% of them.
- **CVSS** measures technical severity, not whether attackers are using it. A 9.8/10 is critical: remotely exploitable with no login.
- **CISA KEV** means CISA has confirmed active exploitation, not a theoretical risk.

## 1. HIGH — Your LangChain graph chatbot can be tricked into changing or exposing database data

**CVE / metrics:** CVE-2024-8309 (PYSEC-2024-115) — CVSS 9.8/10: critical, remotely exploitable with no login. EPSS 0.1374 (96.28th percentile): a 0–1 estimate of exploitation likelihood in the next 30 days; this ranks above 96.28% of known flaws.

**Sources:** [GitHub advisory](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [fix commit](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) · [research disclosure](https://huntr.com/bounties/8f4ad910-7fdc-4089-8f0a-b5df5f32e7c5)

### What broke

LangChain Community 0.2.5's GraphCypherQAChain could turn hostile text in a chat prompt into **SQL injection** (malicious input that makes a database run an unauthorized query). The issue is prompt injection: untrusted text can influence the query the chatbot sends to its graph database. The practical point is simple: a chatbot connected to a writable database must not treat user language as a safe database command.

**Attacker view, conceptual:** an attacker finds a public or lightly authenticated chatbot, submits instructions aimed at its database-query step, then looks for unexpected queries, reads, or changes. Defenders should look for unusual query volume, failed authorization events, and database writes originating from the chatbot service account.

### Why it matters to an SMB running AI tools

This is directly in the AI stack. Any internal knowledge assistant that converts questions into graph-database queries can inherit the problem if it uses the affected component or grants its chatbot database write access. A successful abuse could expose business data, alter records, or make the assistant unavailable.

### What you do Monday

1. In the repository or deployment inventory, search for `langchain-community` and `GraphCypherQAChain`; identify any version 0.2.5 deployment (15 minutes).
2. Update to the vendor-fixed release identified in the [GitHub advisory](https://github.com/advisories/GHSA-45pg-36p6-83v9), then run the existing chatbot test suite before release (30 minutes).
3. In the database console, make the chatbot account read-only unless a documented workflow truly requires writes; review its query log for unexpected writes (20 minutes).

## 2. CRITICAL — Your firewall manager has a heavily targeted hole that can skip its login

**CVE / metrics:** CVE-2026-20079 — EPSS 0.7470 (99.47th percentile): a 0–1 estimate of exploitation likelihood in the next 30 days; this ranks above 99.47% of known flaws.

**Sources:** [Cisco advisory](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-onprem-fmc-authbypass-5JPp45V2) · [NVD record](https://nvd.nist.gov/vuln/detail/CVE-2026-20079)

### What broke

Cisco Secure Firewall Management Center and Security Cloud Control Firewall Management have an **authentication bypass** (a flaw that lets someone get past a login check). An unauthenticated remote attacker may be able to execute script files on the appliance. You do not need the implementation detail: this is a network-control system with a publicly confirmed active-exploitation signal.

### Why it matters to an SMB running AI tools

AI services and automation workers depend on reliable network boundaries, cloud connections, and secrets. If the system managing those boundaries is compromised, an attacker can disrupt the routes and controls that protect AI data sources and service accounts. This is not an AI-product flaw; it is urgent infrastructure risk around the stack.

### What you do Monday

1. Sign in to Cisco Secure Firewall Management Center or Security Cloud Control and open **System → Updates**; compare the installed release with the [Cisco advisory](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-onprem-fmc-authbypass-5JPp45V2) (10 minutes).
2. Apply Cisco's fixed release or mitigation in a scheduled maintenance window, then confirm administrator login and policy deployment still work (30–60 minutes).
3. Ask the firewall owner: “Please confirm whether CVE-2026-20079 is present, patched, or mitigated, and send the change record.”

**CISA metrics:** CISA confirmed this is being actively exploited as of 09-09-2026. CISA requires federal agencies to patch by 09-12-2026. Known to be used in ransomware campaigns: Unknown. CISA's required action is to apply the vendor mitigation; use the Cisco update path above and the linked advisory for the exact supported release.

## 3. HIGH — Your remote-access gateway may let an outsider in without a password

**CVE / metrics:** CVE-2026-19490 — EPSS 0.0600 (92.89th percentile): a 0–1 estimate of exploitation likelihood in the next 30 days; this ranks above 92.89% of known flaws.

**Sources:** [Citrix advisory](https://support.citrix.com/external/article/CTX696939/netscaler-adc-and-netscaler-gateway-secu.html) · [NVD record](https://nvd.nist.gov/vuln/detail/CVE-2026-19490)

### What broke

Citrix NetScaler ADC and NetScaler Gateway can have an authentication bypass when configured as a remote-access gateway or AAA virtual server. An unauthenticated remote attacker may bypass the login path. The important detail is not the alternate-path mechanism: if your NetScaler handles VPN or remote app access, treat it as an exposed front door.

### Why it matters to an SMB running AI tools

Remote workers and automation administrators often use the same gateway to reach private AI dashboards, model stores, document systems, and supporting servers. Compromise of that gateway can put the systems feeding an AI assistant within reach. This is infrastructure risk, not a flaw in the AI tool itself.

### What you do Monday

1. In NetScaler, open **Configuration → System → Software Images** and record the installed build; compare it with the [Citrix advisory](https://support.citrix.com/external/article/CTX696939/netscaler-adc-and-netscaler-gateway-secu.html) (10 minutes).
2. Apply Citrix's listed mitigation or fixed build, then test one approved VPN or remote-app login (30–60 minutes).
3. Review gateway authentication and administrator logs from 09-09-2026 onward for unfamiliar successful sessions; preserve suspicious entries before clearing anything (20 minutes).

**CISA metrics:** CISA confirmed this is being actively exploited as of 09-09-2026. CISA requires federal agencies to patch by 09-12-2026. Known to be used in ransomware campaigns: Unknown. CISA's required action is to apply the vendor mitigation; follow the Citrix advisory above for the exact configuration and build steps.

## 4. WATCH — Manufacturing and professional-services organizations appeared repeatedly in new ransomware claims

**CVE / metrics:** No CVE applies. This is a sector pulse from public victim claims, not proof of a breach at any particular business.

**Sources:** [Ransomware.live recent-victims tracker](https://www.ransomware.live)

### What broke

Recent claims include two US manufacturing organizations attributed to clop and a US professional-services organization attributed to ShadowByt3$. Public claim boards are unverified adversary assertions; use them as a signal of who may be under pressure, not as confirmed incident reporting.

### Why it matters to an SMB running AI tools

Manufacturing and professional-services firms increasingly connect document stores, scheduling, quoting, and operational data to AI assistants and automations. Ransomware pressure makes access control and recoverability around those connected data sources more important, especially where one compromised identity can reach many systems.

### What you do Monday

1. Open the backup console and verify the last successful backup for your document store and the systems that host AI-connected data; write down the restore-test date (15 minutes).
2. Open the identity provider's **Users → Sign-in activity** and review administrator accounts for unfamiliar locations or new MFA methods since 09-01-2026 (15 minutes).
3. Tell your IT owner: “Please confirm we can restore one AI-connected document folder and that administrator MFA is enforced.”

## Jargon buster

- **Authentication bypass:** A flaw that lets someone get past a login or permission check they should have had to pass.
- **CISA KEV:** CISA's list of vulnerabilities it knows attackers are actively exploiting.
- **ClearFake:** Malware that uses fake browser or software-update pages to trick a visitor into infecting themselves.
- **clop:** A ransomware group; a claim under this name is an unverified attacker assertion, not proof of an incident.
- **CVE:** A shared ID for a publicly disclosed security flaw.
- **CVSS:** A 0–10 technical severity score; it does not show whether a flaw is being attacked.
- **EPSS:** A 0–1 estimate of a flaw's likelihood of exploitation in the next 30 days; higher means patch first.
- **Firewall management console:** The control panel that sets and pushes firewall rules.
- **GraphCypherQAChain:** A LangChain helper that converts a chat question into a graph-database query.
- **IClickFix:** Malware that tricks a visitor into running a fake fix or click-this command.
- **LangChain:** A framework used to build AI applications and chat-with-your-data tools.
- **Ransomware:** Malicious software that locks files or steals data to extort payment.
- **SQL injection:** Malicious input that tricks an application into running unauthorized database queries.

## Appendix

### CISA KEV — ranked by EPSS

| CVE | Product | Added | EPSS | Federal patch deadline | Ransomware use | Source |
|---|---|---|---:|---|---|---|
| CVE-2026-20079 | Cisco Secure Firewall Management Center / Security Cloud Control | 09-09-2026 | 0.7470 (99.47th) | 09-12-2026 | Unknown | [Cisco](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-onprem-fmc-authbypass-5JPp45V2) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-20079) |
| CVE-2026-19490 | Citrix NetScaler | 09-09-2026 | 0.0600 (92.89th) | 09-12-2026 | Unknown | [Citrix](https://support.citrix.com/external/article/CTX696939/netscaler-adc-and-netscaler-gateway-secu.html) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-19490) |
| CVE-2026-75650 | Adobe Commerce and Magento | 09-08-2026 | 0.0215 (81.03rd) | 09-11-2026 | Unknown | [Adobe](https://helpx.adobe.com/security/products/magento/apsb26-146.html) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-75650) |
| CVE-2025-25249 | Fortinet products | 09-09-2026 | 0.0170 (75.79th) | 09-12-2026 | Unknown | [Fortinet](https://fortiguard.fortinet.com/psirt/FG-IR-25-084) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2025-25249) |
| CVE-2026-85046 | Google Chromium V8 | 09-04-2026 | 0.0126 (67.85th) | 09-18-2026 | Unknown | [Google](https://chromereleases.googleblog.com/2026/09/stable-channel-update-for-desktop_01882797386.html) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-85046) |
| CVE-2026-87491 | Google Chromium V8 | 09-09-2026 | 0.0076 (53.30th) | 09-23-2026 | Unknown | [Google](https://chromereleases.googleblog.com/2026/09/stable-channel-update-for-desktop_0808145027.html) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-87491) |
| CVE-2026-86218 | N-able N-central | 09-08-2026 | 0.0074 (52.63th) | 09-11-2026 | Unknown | [Vendor status](https://status.n-able.com/2026/09/06/n-central-2026-3-hotfix-4-cve-2026-86218/) · [advisory](https://me.n-able.com/s/security-advisory/aArVy0000002Ld3KAE/cve202686218-preauthentication-remote-code-execution) |
| CVE-2026-81963 | Microsoft Windows Update Stack | 09-08-2026 | 0.0063 (48.19th) | 09-22-2026 | Unknown | [Microsoft](https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-81963) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-81963) |
| CVE-2026-85880 | Microsoft Windows | 09-08-2026 | 0.0057 (45.42th) | 09-22-2026 | Unknown | [Microsoft](https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-85880) · [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-85880) |

### Ransomware sector pulse

| Group | Sector | Country | Discovered | Source |
|---|---|---|---|---|
| clop | Manufacturing | US | 09-10-2026 | [Ransomware.live](https://www.ransomware.live) |
| clop | Manufacturing | US | 09-10-2026 | [Ransomware.live](https://www.ransomware.live) |
| ShadowByt3$ | Professional Services | US | 09-10-2026 | [Ransomware.live](https://www.ransomware.live) |
| Global Secret Group | Manufacturing | US | 09-09-2026 | [Ransomware.live](https://www.ransomware.live) |
| embargo | Agriculture and Food Production | US | 09-09-2026 | [Ransomware.live](https://www.ransomware.live) |

### CIRCL high-EPSS candidates

| Advisory | CVE | Summary | EPSS | Source |
|---|---|---|---:|---|
| PYSEC-2024-115 | CVE-2024-8309 | LangChain graph-query prompt injection / SQL injection | 0.1374 (96.28th) | [GitHub advisory](https://github.com/advisories/GHSA-45pg-36p6-83v9) · [fix](https://github.com/langchain-ai/langchain/commit/c2a3021bb0c5f54649d380b42a0684ca5778c255) |

### IOC sample — do not visit these addresses

| Type | Indicator | Family / status | Seen | Source |
|---|---|---|---|---|
| Domain | `luwpywz1.web-enerflow.com` | ClearFake, confidence 100 | 09-10-2026 | [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/js.clearfake) |
| Domain | `www.zago.it` | IClickFix, confidence 100 | 09-10-2026 | [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/details/js.iclickfix) |
| URL | `http://101.74.52.251:15884/i` | online | 09-10-2026 | [URLhaus entry](https://urlhaus.abuse.ch/url/3915015/) |
| URL | `http://3.133.139.254/tiny_bot.arm` | online | 09-10-2026 | [URLhaus entry](https://urlhaus.abuse.ch/url/3915014/) |

Compiled from public sources · 09-10-2026
