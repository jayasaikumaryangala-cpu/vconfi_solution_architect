# Security Stress Testing — Red Team Your Own Design

After the implementation plan is finalized, you MUST perform a security stress test on the design. Act as a penetration tester / red team operator and attempt to find weaknesses in the solution you just designed. This is a defensive exercise to harden the solution before deployment.

## Phase 1: Attack Surface Analysis
Identify every entry point in the designed solution:
- Internet-facing services and ports
- VPN endpoints
- Wireless SSIDs (corporate, guest, management)
- Remote management interfaces (iLO, FortiGate admin, SSH, SNMP)
- Physical access points (console ports, USB)
- User endpoints connecting to the network
- DR site connectivity
- Backup infrastructure exposure

## Phase 2: Simulated Attack Scenarios
For EACH attack vector, think like an attacker and document:

### External Attacks
- **Perimeter breach** — Can the FortiGate be bypassed? Are there exposed services? Is SSL inspection properly configured? Any default credentials?
- **DDoS resilience** — Can the ISP links be saturated? Is there rate limiting? SD-WAN failover under attack?
- **VPN attacks** — Brute force on VPN credentials? Weak encryption? Split tunneling risks?
- **DNS attacks** — DNS poisoning, tunneling, exfiltration via DNS?

### Internal Attacks (Assume attacker is on the network)
- **Lateral movement** — Can an attacker move between VLANs? Are inter-VLAN firewall rules tight enough? Is east-west traffic inspected?
- **Privilege escalation** — Can a standard user reach admin interfaces? Are management VLANs truly isolated? Is 802.1X bypassable?
- **Credential theft** — Is LDAP traffic encrypted (LDAPS)? Are admin passwords stored securely? Is MFA enforced on all admin access?
- **Rogue devices** — Can an unauthorized device join the network? Is NAC/802.1X enforced on all ports? What about rogue APs?
- **Data exfiltration** — Can sensitive data leave the network undetected? Is DLP configured? Are USB ports disabled on servers?

### Wireless Attacks
- **Evil twin AP** — Is rogue AP detection enabled on FortiGate? Can the RADIUS be spoofed?
- **Deauth attacks** — Is 802.11w (Management Frame Protection) enabled?
- **Guest network breakout** — Can a guest SSID user reach internal VLANs? Is the captive portal bypassable?

### Backup & DR Attacks
- **Ransomware resilience** — Can backups be encrypted by ransomware? Are backup repos air-gapped or immutable? Can Veeam credentials be compromised?
- **DR site compromise** — Is the VPN between primary and DR hardened? Can DR be used as a pivot point?

### Social Engineering & Human Factors
- **Phishing readiness** — Does the solution include email security (FortiMail or equivalent)? Are users trained?
- **Insider threat** — Can a rogue admin wipe logs? Are admin actions logged to a separate, tamper-proof system?

## Phase 3: Vulnerability Report
Generate a report with:

| # | Attack Vector | Severity | Current Mitigation | Gap Found | Recommended Fix |
|---|--------------|----------|-------------------|-----------|-----------------|

Severity levels: **Critical** / **High** / **Medium** / **Low** / **Informational**

## Phase 4: Hardening Recommendations
For every gap found, provide:
1. **What to fix** — Specific configuration change or addition
2. **How to fix** — Step-by-step instructions or config snippet
3. **Cost impact** — Does the fix require additional hardware/licenses? If so, add to BOM
4. **Priority** — Must-fix-before-go-live vs post-deployment hardening

## Phase 5: Update the Implementation Plan
After the security stress test:
1. Update the implementation plan document with all hardening recommendations
2. Add a new section: **"Security Stress Test Results"** with the vulnerability report
3. Update the BOM if additional hardware/licenses are needed
4. Update the timeline if hardening tasks add deployment time
5. Present findings to the user: *"I've stress-tested the design as an attacker. Here are the gaps I found and how to fix them. Review and confirm before we finalize."*

## Mandatory Testing Standard
- NEVER skip the security stress test
- NEVER deliver a plan without testing it against these attack scenarios
- If ANY Critical or High severity gap is found, the plan MUST be updated before delivery
- Document all findings even if no gaps are found (proves due diligence for auditors)
