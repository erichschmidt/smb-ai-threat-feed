---
type: reference-glossary
title: "Threat Feed Glossary"
status: active
tags: [threat-feed, glossary, plain-language]
created: 2026-08-19
updated: 2026-10-08
related: "briefs/Threat-Feed-10-08-2026.md"
---

# Threat Feed Glossary

Plain-language definitions for every term used in the daily feed. **Living note — add new terms as they first appear; never remove.** One line each; if a term needs more, it's not glossary material, it's a topic for the feed itself.

## How to use
- Readers: skim this when a term in the feed is new. Repeat readers will stop needing it.
- Feed generation: every term used in a day's note MUST appear here; add it on first use.

## A–Z

### A
- **API (Application Programming Interface):** The software bridge one program uses to talk to another — how your apps, SaaS tools, and automation exchange data. An insecure API is an unlocked door to the systems it connects.
- **Apache Airflow:** An open-source orchestrator — software that schedules and manages data and machine-learning jobs. Its "providers" are the connectors to specific clouds and databases; a flaw in a provider is a flaw in the pipe between your data and your models.
- **ACR Stealer:** Malware that steals saved passwords, browser cookies, and saved data from a Windows PC, then sends them to the attacker. A listed domain is a block-and-hunt signal; do not visit it.
- **AMOS:** Malware that targets Apple computers and steals browser data, passwords, and cryptocurrency-wallet information. A listed domain is a block-and-hunt signal; do not visit it.
- **Agent Tesla:** Malware that steals passwords and other data from Windows systems. A listed domain is a block-and-hunt signal; do not visit it.
- **ALPC (Advanced Local Procedure Call):** A Windows internal messaging component. A flaw here generally requires someone to already have a foothold on the computer.
- **Arbitrary code execution:** Running attacker-supplied code as if it were part of the program — effectively taking over the machine.
- **AAA virtual server:** The login/authentication virtual server on a Citrix NetScaler. If you have one, some NetScaler memory bugs (including CVE-2026-8452) are in scope.
- **Ansible:** A common automation tool that runs "playbooks" — lists of steps that configure servers and deploy software. Its job settings often hold the passwords those steps need.
- **Authentication bypass:** A flaw that lets someone get past a login or permission check they should have had to pass.
- **Authorization bypass:** A flaw that lets someone who *is* logged in do things they were never granted permission to do. Different from breaking in — they walk through the wrong door.
- **Ajax.NET Professional / AjaxPro:** An old .NET library that lets a web page call server code without a full reload. Leftover `AjaxPro.dll` / `AjaxPro.2` packages are the risk; the official patched line is AjaxNetProfessional 21.11.29.1+.
- **Aisuru:** A botnet / malware family. An IP:port listed with this name is a command-and-control address to block and hunt — don't visit it.
- **anubis:** A ransomware group. Seeing the name in a victim list means that crew claimed a breach — treat it as a "this sector is being hunted" signal, not a reason to pay.
- **Apache Wicket:** A Java web-app framework. A cluster of Wicket CVEs in the feed is a "if you ship a Wicket app, read the advisories" signal, not a generic Windows patch.
- **APT (Advanced Persistent Threat):** A well-funded, organized hacking group (often state-sponsored) that stays inside networks for long periods. The "big boys" of cybercrime — usually not the first thing a small business needs to worry about.
- **AuditTeam:** A ransomware group. Seeing the name in a victim list means that crew claimed a breach — treat it as a sector-targeting signal, not a reason to pay.
- **a2ui:** An open-source toolkit that lets AI agents build and update user-interface components. A flaw in its component-update function can be used to exhaust resources (a denial-of-service class bug).
- **Access token / assertion:** The signed digital credential an app or automation presents to prove who it is — a temporary key card. A stolen token lets an attacker act as your service without knowing any password.
- **Approval workflow:** A defined chain of steps a request must pass through for sign-off. If steps can be deleted, approvals happen that never should have.
- **Acronis Backup (for cPanel/WHM/Plesk):** Backup software that protects small-business web hosting. A privilege-escalation hole in it is a double threat — the backup jobs themselves can be hijacked.
- **Audit trail / operation log:** The record of who did what in a system, and your evidence when something goes wrong. If every logged-in user can read it, it stops being evidence.

### B
- **Building automation controller:** The edge device that manages a commercial building's HVAC, lighting, and energy systems through a web interface. A hole here is a hole in the systems that keep the office running and their readable credentials are a supply-chain weak point.
- **Buffer overflow:** A memory bug where software writes past the space it reserved for data. Attackers use it to crash a service or, in the right conditions, run their own code. (Heap and stack are two flavors of the same bug.)
- **Back-office:** The admin side of a business system, where staff manage customers, leads, orders, and settings.
- **BOD 26-04:** A CISA directive requiring federal agencies to patch actively-exploited flaws by a set deadline — a good "how urgent is this" signal for everyone.
- **Botnet:** A network of hacked internet-connected devices (routers, cameras) that attackers control and use together.
- **BrowserSkill:** An AI tool that lets an agent drive a real web browser — click, fill forms, read pages.
- **Budibase:** A low-code app builder. A hole in plugin upload or data-source URLs is a hole in the apps and automations built on it.

### C
- **Cleartext:** Data sent or stored unencrypted, so anyone who intercepts it can read it — the opposite of encrypted. A password sent in cleartext is effectively handed to anyone sniffing the network.
- **CoreGraphics:** Apple's graphics engine that renders on-screen images. A flaw here can affect iPhones, Macs, and iPads at once.
- **Certificate validation:** Checking that a digital certificate on a connection really is who it claims to be. If the check is skipped, a stranger can present a fake certificate and the system trusts it.
- **Check Point (firewalls / security gateways):** A major firewall and security-appliance vendor common at the edge of business networks. A hole here is a hole in the front door that all traffic — including AI app traffic — passes through.
- **CI/CD (Continuous Integration / Continuous Delivery):** Automated build-and-deploy — code changes are tested, built, and shipped automatically. The pipeline that turns your code into running software, and a place tokens and secrets often live.
- **clop:** A ransomware group. A claim under this name is an unverified attacker assertion; treat it as a sector-targeting signal, not proof of an incident or a reason to pay.
- **C2 / Command-and-Control server:** A server attackers control; infected machines "phone home" to it to get instructions or steal data. When analysts see C2 traffic, they know a machine is compromised.
- **Casdoor:** A self-hosted login/identity server that other apps check with to confirm who a user is. Treat it as production, not a side project.
- **CISA (Cybersecurity and Infrastructure Security Agency):** The US federal agency that tracks exploited vulnerabilities and publishes guidance. Their "known exploited" list is the closest thing to an authoritative "this is real right now" signal.
- **chaos (ransomware group):** A ransomware crew name in victim disclosures. Different from everyday "chaos." Treat it as a "this sector is being hunted" signal, not a reason to pay.
- **CIRCL:** A European security team that runs a free vulnerability database (Vulnerability Lookup) — one of the feed's sources for "what vulnerabilities exist."
- **ClearFake:** Malware that pretends to be a browser or software update so a visitor infects themselves. Fake "update Chrome" pages are the usual tell.
- **Cloud metadata service:** The internal cloud page a virtual machine uses to fetch its own keys and identity. If an app can be tricked into reading it, attackers steal cloud credentials.
- **Cisco Catalyst SD-WAN Manager:** The central control panel for Cisco's SD-WAN — it configures and routes traffic between offices. Admin access here means control of every link and what travels over it.
- **Cloud Foundry UAA:** The identity/login component of Cloud Foundry (a platform for running cloud apps). A flaw in its login handshake can let someone establish a session without the proper check.
- **Cobalt Strike:** A legitimate security-testing tool that attackers also use to control hacked machines. Seeing it in the wild = real attackers, not a false alarm.
- **Cloud Build / Google Cloud Build:** Google's managed service that builds, tests, and deploys code from GitHub and similar. A hole in a GitHub trigger is a hole in that deploy path and its secrets.
- **coinbasecartel:** A ransomware group. Seeing the name in a victim list means that crew claimed a breach — treat it as a sector-targeting signal, not a reason to pay.
- **Comment control:** A Cloud Build / GitHub setting that is supposed to require a collaborator comment before an untrusted pull request is built. If the gate and the commit that actually builds can diverge, unreviewed code runs.
- **Code injection:** Tricking software into running attacker-supplied commands as if they were part of the program.
- **Command injection / OS command injection:** Tricking software into running operating-system commands the attacker chose. Cousin of code injection, but aimed at the machine's shell.
- **Corosync:** The messaging service that keeps the nodes of a server cluster in sync (used by Proxmox VE and similar). A hole here can affect every node in the cluster.
- **CVE (Common Vulnerabilities and Exposures):** A unique ID (e.g., CVE-2026-33824) for a publicly disclosed security flaw, so everyone can track the same bug across vendors and scanners. Like a license plate for a vulnerability.
- **cPanel / WHM and Plesk:** Web-hosting control panels commonly used on small-business web servers. Admin access there means control of every hosted site and mailbox — including the backup jobs that protect them.
- **CVSS:** A 0–10 severity score for a flaw. 9.8/10 = critical — typically exploitable remotely with no login. Useful for "how bad if it works"; EPSS/KEV answer "is it being used."
- **Checkpoint (model):** A saved snapshot of a trained AI model's settings. Loading one from an untrusted source can run attacker code — treat model files like unknown programs.
- **Chromium V8:** The JavaScript engine inside Chrome, Edge, and other browsers. A hole here usually means "update your browser."
- **Cypher:** The query language for graph databases (like Neo4j). LangChain's GraphCypherQAChain turns a chat question into a Cypher query — if that query isn't locked down, the chat becomes a database write.
- **CSRF (cross-site request forgery):** The check that stops a random website or crafted link from making your already-logged-in session perform actions. If it's disabled, an outsider can trigger actions as if they were you.

### D
- **DanaBot:** Malware that steals banking and browser data and gives the attacker a foothold on a Windows PC. An IP:port listed with this name is a command-and-control address to block and hunt.
- **Deployment automation:** A tool that schedules and pushes your software to servers automatically. Compromise here means control over what ships to production.
- **Deadlock:** A ransomware group. A claim under this name is an attacker assertion; use it as a sector-targeting signal, not proof of an incident.
- **Denial of service (DoS):** The service stops answering, so nobody gets in — including you. Different from ransomware (which locks files); this one just knocks the door down.
- **Deserialization:** Turning a saved data blob back into a live program object. If the blob is attacker-controlled, that "restore" can run their code.
- **Data exfiltration:** Silently copying data out of your systems to the attacker.
- **direwolf:** A ransomware group. A cluster of claims in one day usually means they posted a batch of victims — useful as a sector-targeting signal.
- **Doommageddon:** A ransomware group. Seeing the name in a victim list means that crew claimed a breach — treat it as a sector-targeting signal, not a reason to pay.
- **Drifter:** A family of malware that gives an attacker remote control of hacked machines. An IP:port listed with this name is a command-and-control address to block and hunt — don't visit it.
- **Double-free:** A memory bug where software deletes the same piece of memory twice, which attackers exploit to run their own code. You don't need the mechanism — just know it's a real, exploitable flaw.
- **dragonforce:** A ransomware group. Seeing the name in a victim list means that crew claimed a breach — treat it as a sector-targeting signal, not a reason to pay.
- **DVR / NVR:** Digital video recorders and network video recorders — the boxes behind security cameras. Full admin control of one means an attacker can watch, rewind, and pivot deeper into your network.
- **Dell OpenManage Server Administrator:** Dell's management agent for its servers. It runs with deep system access, so an unauthenticated flaw there is effectively a server takeover path.

### E
- **emperador:** A ransomware group. Seeing the name in a victim list means that crew claimed a breach — treat it as a sector-targeting signal, not a reason to pay.
- **ESPnet:** An open-source toolkit for AI speech processing (recognition, synthesis). It loads model files with a loader that can run code if the file is untrusted.
- **Email gateway:** The appliance or service that inspects inbound and outbound email before it reaches a mailbox. A hole here is a hole in everything that reads your mail, including AI mail assistants.
- **Environment variables (in automation tools):** The saved settings a job runs with — often cloud keys, database passwords, and API keys. If they're stored as plaintext, anyone who can read the job can read the keys.
- **EPSS (Exploit Prediction Scoring System):** A score (0 to 1) estimating how likely a vulnerability is to be exploited in the wild soon. Higher = patch first. 0.78 means "very likely to be exploited"; 0.01 means "probably not for a while." Percentile = where that score ranks vs all known vulnerabilities (99.5th = top half-percent most likely).
- **Exploit:** The actual code or technique attackers use to take advantage of a flaw.
- **Flowintel:** An open-source case-management / intel-sharing app. A hole in how it shows case titles is a hole in the analyst browser session, not in your production AI stack unless you actually run it.

### F
- **F5 BIG-IP APM (Access Policy Manager):** The remote-access / VPN edge of F5's BIG-IP appliance line, often the tunnel remote workers use to reach the office network.
- **File extension:** The suffix (`.pkl`, `.pt`) that tells software what a file is. If a scanner only checks certain extensions, a file named differently sails past the check.
- **Firewall management console:** The control panel that sets and pushes firewall rules. If it is compromised, an attacker may be able to change the network boundaries that protect other systems.
- **FMC / Firewall Management Center:** Cisco's centralized panel for managing many firewalls. A hole here lets an attacker rewrite the rules that protect your network.
- **FortiOS:** The operating system inside Fortinet firewalls. A hole here is a hole in the front door of your network.
- **FortiMail:** Fortinet's email security gateway. It inspects inbound/outbound mail and often sits in front of the mail server — a hole here is a hole in everything that reads your mail, including AI mail assistants.

### G
- **Gitea:** A self-hosted Git (source-code) server that many small teams run instead of GitHub. A hole here is a hole in your code, secrets, and the automations that pull from those repos.
- **Gatekeeper (macOS):** Apple's check that a downloaded app is signed and safe before it runs. A bypass means a malicious app can run without the usual warning.
- **Graph database:** A database that stores things and their relationships as connected points. AI tools may query it to answer questions about linked business records.
- **getnote-mcp:** A notes helper that plugs into an AI assistant via MCP. Versions through 1.5.0 could be tricked into reading local files; 1.5.1 is the fix.
- **GitLab:** A self-hosted code-hosting platform many teams run instead of GitHub. A hole here is a hole in your code, CI/CD pipelines, and the AI tools that read those repos.
- **Git hook:** A small script Git runs automatically when something happens in a repo (a commit, a push). If an attacker plants one, it runs with the Git server's own permissions.
- **Global Secret Group:** A ransomware group. Recent claims have included small US construction and auto-retail shops — treat the name as a sector-targeting signal, not a reason to pay.
- **GraphCypherQAChain:** LangChain's helper that turns a chat question into a graph-database query. If that query isn't locked down, the chat becomes a database write.

### H
- **Hex encoding:** A way of encoding web-address characters into hexadecimal (0–9,A–F) form. If a server mis-decodes it, an attacker can smuggle past checks and reach admin functions.
- **HCL BigFix Service Management:** A tool used to automate and manage IT endpoint tasks (patch, deploy, update). A flaw here is a flaw in the trust your automation pipeline places in it.
- **HypeAgent:** A remote-access malware family. Seeing it in an IOC list means a machine is being told what to do by an attacker's server.
- **Heap buffer overflow:** A memory bug where software writes past the space it allocated for data. Attackers use it to crash a service or, in the right conditions, run their own code.
- **Out-of-bounds write:** A memory bug where software writes past the space it allocated for data. Attackers use it to crash a service or, in the right conditions, run their own code.
- **Octopus Server:** A self-hosted deployment-automation platform that schedules and pushes software to servers. A flaw here is a flaw in whatever ships to production.
- **OpenPanel:** A server-management panel some teams run to stand up and manage apps and services. A hole here is a hole in the automation and AI-service connections it manages.

### I
- **iRule:** A configuration snippet on F5 appliances used as a temporary stop from a vulnerability while a full patch is built and installed.
- **iah6477:** A ransomware group. Recent claims in this feed have been US manufacturing — treat the name as a sector-targeting signal, not a reason to pay.
- **IKE (Internet Key Exchange):** The Windows service that sets up a VPN tunnel. A hole here is a hole in the front door.
- **Identity provider (IdP) / single sign-on (SSO):** The service that holds user accounts and tells other apps "this person is who they say they are." Compromise it and you compromise every app that trusts it.
- **Improper access control:** A software flaw where the product fails to check who is allowed to do what — letting an unauthorized user create, read, change, or delete data they shouldn't touch.
- **IClickFix:** Malware that tricks a visitor into running a "fix" or "click this" command. Fake troubleshooting pages are the usual tell.
- **incransom:** A ransomware group. Seeing the name in a victim list means that crew claimed a breach — treat it as a sector-targeting signal, not a reason to pay.
- **IOC (Indicator of Compromise):** A trace left behind by an attack — a malicious IP address, domain, file hash, or URL. If you find an IOC in your logs, something bad touched your network.
- **Info-stealer:** Malware that harvests saved passwords, browser cookies, and wallet files and sends them to the attacker.
- **ISE (Identity Services Engine):** Cisco's appliance that decides who and what is allowed on your network — the network-access gatekeeper.
- **Isolated environment / sandbox:** A cage meant to contain a program. A "breakout" means the attacker escaped onto the real machine.

### J
- **JSON Web Token (JWT):** A signed digital credential an app or automation presents to prove who it is — a temporary key card. A stolen token lets an attacker act as your service without knowing any password.
- **JFrog Artifactory:** A warehouse for software packages and Docker images — often the same place AI pipelines pull models and dependencies. Treat self-hosted copies as production, not a lab toy.
- **Jinja:** A template language used to fill in variables in text. Leftover template tags can become code if they are rendered without a sandbox.

### K
- **kazu:** A ransomware group. Today's dump was healthcare-heavy — treat the name as a "this sector is being hunted" signal, not a reason to pay.
- **KEV (Known Exploited Vulnerabilities) catalog:** CISA's list of vulnerabilities that are being actively exploited right now. If a flaw is on this list, it's not theoretical — patch it.
- **killsec:** A ransomware group. Seeing the name in a victim list means that crew claimed a breach — treat it as a sector-targeting signal, not a reason to pay.
- **Knowledge distillation (in AI):** Training a new model to imitate another model's answers by feeding it huge volumes of the original model's outputs. Legitimate as a technique; abusive when it's mass extraction against a provider's terms.
- **krybit:** A ransomware group. Seeing the name in a victim list means that crew claimed a breach — treat it as a sector-targeting signal, not a reason to pay.

### L
- **LangChain:** A popular open-source framework developers use to build AI applications (chatbots, "chat with your data" tools). Because it's everywhere, flaws in it affect lots of AI tools at once.
- **Least privilege:** Giving a person or software account only the access it needs for its job, and no more.
- **Login bypass:** A flaw that lets someone get past a login or permission check they should have had to pass. Also called authentication bypass.
- **libxml2:** A standard software library for parsing XML files. Vulnerabilities here can allow code execution when processing untrusted XML data.
- **lockbit / lockbit5:** A ransomware group (lockbit5 is the current name in victim dumps). Treat the name as a "this sector is being hunted" signal, not a reason to pay.
- **Loki Password Stealer / LokiPWS:** Malware that steals saved passwords from browsers and apps, then sends them to the attacker. A URL listed with this name is a drop or panel to block and hunt — don't visit it.
- **Lumma Stealer:** Malware that steals saved passwords, browser cookies, and crypto-wallet files from a Windows PC, then sends them to the attacker.

### M
- **m3rx:** A ransomware group. Seeing the name in a victim list means that crew claimed a breach — treat it as a sector-targeting signal, not a reason to pay.
- **MCP (Model Context Protocol):** The plug-in style that lets an AI assistant use extra tools (files, notes, browsers). A hole in an MCP helper is a hole in whatever that assistant can reach.
- **Missing authentication:** The product ran a sensitive action before checking that the caller was logged in. Cousin of improper access control.
- **MFA (Multi-Factor Authentication):** Requiring a second proof of identity (a code from your phone, a fingerprint) beyond a password. The single cheapest defense against stolen passwords.
- **Malware:** Malicious software — viruses, ransomware, remote-access trojans, etc.
- **MLflow:** Popular open-source tracker for AI experiments, models, and deployments. Often sits next to training data and cloud keys — treat it as production, not a lab toy.
- **Magento / Adobe Commerce:** Adobe's e-commerce platform. A hole here is a hole in your storefront and customer data.
- **MikroTik RouterOS:** The operating system inside MikroTik routers. A hole here is a hole in the router that runs your office internet.
- **Mirai:** A botnet that infects internet-connected cameras and routers, and turns them into attack tools. A captured file hash of Mirai in an IOC list means someone's botnet is spreading via your network.
- **Mozi:** Malware that infects internet-connected gadgets (routers, cameras) and turns them into a botnet.
- **metaencryptor:** A ransomware group. Seeing the name in a victim list means that crew claimed a breach — treat it as a sector-targeting signal, not a reason to pay.
- **Mendix:** A low-code platform where teams build internal apps and workflows by assembling pieces instead of writing code. Treat the apps built on it as production, not prototypes.
- **MISP:** An open-source platform teams use to share threat intelligence and indicators with each other. If it is exposed, the attacker gets your intel and your sharing partners.

### N
- **N-able N-central:** A remote-monitoring / managed-IT tool. A hole here is a hole in every computer it manages.
- **NetScaler ADC / NetScaler Gateway:** Citrix's appliance that is often the VPN and website front door. A hole here is a hole in remote access and anything behind it.
- **Nodemailer:** A Node.js library apps use to send email. A parsing flaw here lets a crafted email header slow or stall the sending service.
- **OpenSSH:** The standard encrypted remote-login software behind most Linux/Unix servers. A flaw here is a flaw in how you reach every machine you manage.

### O
- **OAuth profile:** A saved configuration an access server uses to delegate login to an external identity service. A bug that triggers when it's set means the setup itself — not a one-off config — is the vulnerable state.
- **Obot:** A self-hosted platform for building and running AI assistants (including via the MCP plug-in standard, and vMCP agent profiles). Treat it as production — a flaw here is a hole in whatever the assistant can reach.
- **OIDC (OpenID Connect):** The standard login handshake where one service asks another to vouch for a user's identity. A flaw that skips a step in that handshake lets someone establish a session without the proper check.
- **Origin validation:** Checking that an incoming connection really comes from where it claims to; a failure means a stranger can connect.
- **Oracle HTTP Server / WebLogic Server Proxy Plug-in:** The front door in front of many Oracle business apps. The proxy plug-in sits on Apache or IIS and forwards traffic to WebLogic.
- **ownCloud:** Self-hosted file-sync (like a private Dropbox). A hole here is a hole in the documents your AI tools summarize.
- **Oracle WebLogic Server:** A common application server behind ERP/CRM/portal systems — the "engine room" that serves business apps to browsers.
- **OT (Operational Technology):** The hardware/software that runs physical things — factory machines, PLCs, water systems, HVAC. Different world from office IT, and often less protected.
- **Orchestration (in AI):** The software that schedules and manages AI workloads (training, inference) across machines. Ray is a famous example. Most SMBs never see it — it runs inside their vendors' stacks.

### P
- **Panzer:** A ransomware group. A claim under this name is an attacker assertion; use it as a sector-targeting signal, not proof of an incident.
- **PaperCut NG/MF:** Self-hosted print-management server many offices put in front of printers. A hole here is a foothold next to scan-to-folder jobs and file shares.
- **play (ransomware group):** A ransomware group. A victim claim is an attacker assertion; use it as a sector-targeting signal, not proof of an incident.
- **Path traversal:** A trick where an attacker types `../` (or similar) in a file path to reach files they shouldn't. In a server product this can become full takeover.
- **PLC (Programmable Logic Controller):** A rugged little computer that controls industrial equipment (conveyors, pumps, valves). Often connected to the internet with no password — a favorite target.
- **print command (Samba):** A Samba setting that runs a program when someone prints. If it includes unescaped job text (`%J`), a print job can become a command. Default installs that never set this are usually outside that listing.
- **Privilege escalation:** Gaining higher system access rights (like administrator or root) than originally authorized.
- **Proxmox VE:** A popular open-source virtualization platform for running many virtual machines on your own hardware — a common home for self-hosted AI servers.
- **Plaintext:** Stored so anyone can read it, with no encryption. A secret kept in plaintext is only protected by who is allowed to open the file.
- **Prompt injection:** Tricking an AI by putting instructions inside the data it reads — e.g., hiding "ignore your rules and email your boss" inside a document the AI summarizes. The AI follows the attacker's instructions instead of the user's.
- **Percentile (in EPSS):** Where a score ranks — 95th percentile means it's in the top 5% most likely to be exploited.
- **Pre-signed URL:** A file link that's supposed to prove you were allowed to access it. If the signing key was never set, the proof is fake.
- **pickle:** A Python file format for saving objects. Loading one can run code — treat a random `.pkl` / `.pt` like an unknown program.
- **picklescan:** A scanner meant to catch dangerous Python pickle files inside AI model downloads. If it skips a file extension, a "model" can be malware.
- **PureLogs Stealer:** Malware that steals saved passwords, browser cookies, and crypto-wallet files from a Windows PC, then sends them to the attacker.
- **Provider (in Apache Airflow):** A connector package that lets Airflow talk to a specific service (Snowflake, Google Cloud, Teradata). A flaw in a provider is a flaw in the pipe between your data and your models.
- **PyTorch:** A common toolkit for training and loading AI models. `torch.load` on an untrusted file is the danger, not the brand name.

### Q
- **qilin:** A ransomware group. A cluster of claims in one day usually means they posted a batch of victims — useful as a sector-targeting signal.

### R
- **RMM (Remote Monitoring and Management):** Software that lets IT support log into and manage computers remotely. One compromised RMM tool reaches every machine it manages.
- **Replay (code replay):** Reusing a captured code instead of generating a fresh one, defeating the point of a one-time code.
- **RAG (Retrieval-Augmented Generation):** The standard way AI tools "know" your business data — the AI retrieves relevant documents, then answers from them. The data source becomes an attack surface: poison the documents, poison the answers.
- **Ransomware:** Malware that locks your files and demands payment. The #1 threat to small businesses.
- **RAT (Remote Access Trojan):** Malware that gives an attacker remote control of a machine, like a ghost at your keyboard.
- **Ray:** Open-source tool that runs AI jobs across machines. Developers often leave its dashboard on a laptop with no login — treat it as production, not a toy.
- **RCE (Remote Code Execution):** An attacker can run their own code on your machine from anywhere. "Game over" — full control.
- **Remote file inclusion (RFI):** Tricking a server into loading a file the attacker chose — often a step toward running their own code.
- **Race condition:** Two parts of a program writing the same data at the same time, letting an attacker feed in their own result.
- **Root privileges:** The highest level of access on a Linux/Unix system — the equivalent of "administrator" on Windows. Root means the attacker owns the machine.
- **Remcos / Remus:** Names of remote-access trojans (RATs) — specific malware families seen in the feed.

### S
- **SD-WAN:** A software-defined wide-area network that manages and routes traffic between branch offices over software instead of dedicated hardware. Its orchestrator manages all the links, so a compromise there can reroute traffic.
- **safepay:** A ransomware group. Seeing the name in a victim list means that crew claimed a breach — treat it as a sector-targeting signal, not a reason to pay.
- **Software supply chain:** The code packages, build systems, repositories, and services a business depends on to make and run software. A problem in one can affect every application that pulls from it.
- **SAML (Security Assertion Markup Language):** The behind-the-scenes handshake that lets one login page vouch for you to many apps. If the app does not check the signature on that handshake, an attacker can forge it.
- **Signature validation:** Checking that a message really came from who it claims to be. Skip that check and anyone can forge the message — including onto someone else's account.
- **Sandbox escape:** Breaking out of a cage that was supposed to stop untrusted code or templates from touching the real machine.
- **ScreenConnect:** A legitimate remote-support tool that attackers increasingly abuse — a fake "ScreenConnect installer" is often malware in disguise.
- **Semaphore UI:** A self-hosted control panel that runs scheduled automation jobs, often Ansible playbooks. It stores the credentials those jobs use.
- **ShadowByt3$:** A ransomware group. Seeing the name in a victim list means that crew claimed a breach — treat it as a sector-targeting signal, not a reason to pay.
- **SharePoint:** Microsoft's document intranet. Often the library Copilot and other "chat with your files" tools read — a hole here is a hole in the AI's data source.
- **shinyhunters:** A ransomware / data-extortion group. Recent claims have included CRM / Salesforce-record hauls — treat the name as a "lock down the CRM connector" signal, not a reason to pay.
- **SilentRansomGroup:** A ransomware group. Seeing the name in a victim list means that crew claimed a breach — treat it as a sector-targeting signal, not a reason to pay. Victim names are sometimes redacted until a disclosure timer expires.
- **Shin webshell / php.shin_webshell:** A PHP webshell family. A domain listed with this name is already hosting attacker-controlled code — block and hunt, don't visit.
- **Skyvern:** An AI agent that fills forms and clicks through websites for you. A hole here is a hole in those browser sessions and the keys on that box.
- **SQL Server:** Microsoft's database engine. Versions 2014, 2016, and 2017 are the ones in the CVE-2019-1068 listing.
- **SMTP:** The internet's send-mail protocol. "Crafted SMTP" means a specially built incoming email, not a normal message from a coworker.
- **Storm (ransomware group):** A ransomware crew name in victim disclosures. Different from weather, and different from similarly named malware families — treat it as a "this sector is being hunted" signal.
- **SmartApeSG:** A fake-update malware family. A domain listed with this name is already hosting attacker-controlled code — block and hunt, don't visit it.
- **Smarty:** A popular PHP template language used to build web pages. A code-injection bug here can let an attacker run code on sites built with it.
- **SnappyClient:** A remote-access malware family. An IP:port listed with this name is a command-and-control address to block and hunt.
- **SNMP:** A simple monitoring protocol devices use to report "I'm up / something broke." If it's wired into email notifications, a crafted message can become a command.
- **SQL injection:** A technique where attackers type malicious database commands into an input box (or a prompt), tricking the app into running unauthorized queries — reading, changing, or deleting data.
- **SSH (Secure Shell):** A standard encrypted way to log into a server, router, or device and run commands on it from another computer. It's the secure replacement for older, unencrypted remote login.
- **Stack-based buffer overflow:** A memory bug where software writes past the space it allocated on its call stack. Attackers use it to run their own code on the device.
- **SSRF (Server-Side Request Forgery):** Tricking a server into fetching internal or cloud URLs on the attacker's behalf — often used to reach services the attacker could not hit directly.
- **Safetensors:** A model-weight file format that stores tensors without running code on load. Prefer it over pickle / raw `torch.load` for untrusted models.
- **Service account:** A non-human login that software uses to talk to other software. If it's stolen, the attacker inherits everything that account can reach.
- **Session fixation:** An attack where the attacker pins a victim to a login session the attacker controls; when the victim signs in, the attacker inherits that session and its access.
- **5G fixed wireless (IDU):** A 5G internet box used as primary or backup office internet. Treat it as an untrusted edge device — it is a computer on your network.

### T
- **ThreatFox / URLhaus:** Free abuse.ch databases of malicious IPs, domains, URLs, and malware. The feed's IOC sources.
- **TOTP (time-based one-time password):** The rotating 6-digit code from your authenticator app — the second factor in MFA.
- **TrueConf:** An on-premises video-meeting server. A hole here is a hole in the meeting room and often the recordings.
- **Transfer station (AI API proxy):** A gray-market reseller of access to AI model APIs that hides the real customer and bypasses regional restrictions and usage limits. Often runs on leaked or purchased API keys.

### U
- **Unauthenticated (attacker):** Someone with no login credentials, operating from anywhere on the network or internet.
- **UmBra:** A ransomware group. Seeing the name in a victim list means that crew claimed a breach — treat it as a sector-targeting signal, not a reason to pay.
- **Unsafe reflection:** Tricking a Java (or similar) app into loading a class the attacker named. Combined with a missing login check, it can become full takeover.

### V
- **Vexy Ransomware:** A ransomware group. A victim claim is an attacker assertion; use it as a sector-targeting signal, not proof of an incident.
- **Veeam Backup & Replication:** Backup software many businesses use to protect their servers and data. Because it holds pre-attack copies of everything, flaws here are a double threat — patch and test restores.
- **Vidar:** Malware that steals saved passwords, browser cookies, and wallet files from a Windows PC, then sends them to the attacker. A listed domain is a block-and-hunt signal; do not visit it.
- **VPN (Virtual Private Network):** The encrypted "tunnel" remote workers use to reach the office network. If the VPN software has a hole, attackers get in through the front door.
- **VShell:** A remote-access tool attackers use to control a hacked machine.
- **Vulnerability:** A flaw in software that attackers can use. (CVE = its ID; exploit = the use.)

### W
- **Webhook:** An automated HTTP callback one system sends another when something happens (e.g. "a new model was logged"). If the destination isn't locked down, it becomes an SSRF path.
- **WebDAV:** An old-but-common way programs read and write files over HTTP. ownCloud's file API uses it.
- **Webshell:** A small script planted on a hacked website so the attacker can come back later and run commands. If you see one in an IOC list, the site is already compromised.
- **weights_only:** The safe "load data only, run no code" switch for PyTorch's `torch.load`. Old code that omits it will run code from a malicious model file.
- **WSO2 (API Manager / API platform):** Software many teams use as an integration layer — the API gateway that ferries data between apps, SaaS tools, and automation pipelines. A hole here is a hole in every connection it manages, including the data your AI tools read and write.
- **WINS:** An old Windows name-lookup service. Samba's WINS hook is only dangerous if you turned WINS support on and set a `wins hook` on a domain controller — default is off.
- **WNC T-Mobile 5G Box IDU router:** A 5G internet box whose web management pages have carried unauthenticated configuration-disclosure and command-injection flaws. Treat it as an untrusted edge device.

### X
- **XSS (cross-site scripting):** A crafted link or input that makes a user's own browser run attacker-supplied script — so the attacker leverages the person's logged-in session without breaking in.
- **XWorm:** A remote-access trojan (RAT) that gives an attacker remote control of a Windows machine. An IP:port listed with this name is a command-and-control address to block and hunt.
- **XMRIG:** A crypto-miner. In an IOC list it means someone is stealing CPU time, not running a legit miner.
- **XXE (XML External Entity):** A trick where a crafted XML document makes a server fetch or reveal files and internal addresses it should not. Named for the "external entity" feature built into XML.

### Z
- **Zammad:** An open-source customer-support / helpdesk ticketing system some small businesses run on their own server; it holds support conversations, tickets, and customer records and often feeds email-to-ticket and support-AI automations.
- **Zimbra / ZCS (Zimbra Collaboration Suite):** A self-hosted email and calendar suite used by many schools, governments, and small orgs instead of Microsoft 365. A hole here is a hole in the inbox your AI tools summarize.
- **Zyxel GS1900 Series:** A line of managed network switches common in small businesses. A hole in their web management lets anyone already on the network run commands on the switch.
- **Zero-day:** A flaw that was unknown (and unpatched) when it started being exploited — the most dangerous kind because there's no fix yet.

---

*Glossary v1 — 2026-08-19. Add one line per new term on first use. Last extended 10-08-2026.*
