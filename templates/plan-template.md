# Implementation Plan Template — VConfi

## Document Control

| Field | Value |
|-------|-------|
| Project Name | [Project Name] |
| Client | [Client Name] |
| Location | [Site Location] |
| Version | 1.0 |
| Date | [Date] |
| Prepared By | VConfi Solutions Team |
| Reviewed By | [Reviewer] |
| Approved By | [Approver] |

### Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | VConfi | Initial draft |

---

## Table of Contents

1. Executive Summary
2. Scope & Requirements
3. Architecture Overview & Diagram
4. ISO 27001 Compliance Mapping
5. Network Infrastructure Design
   - 5.1 Firewall (Fortinet FortiGate)
   - 5.2 Switches (HPE Aruba / Cisco Catalyst)
   - 5.3 Cabling (Cat 6 / CommScope Fiber)
   - 5.4 Network Redundancy Design
6. Wireless Infrastructure (FortiAP)
7. Server Infrastructure
8. Disaster Recovery & Backup Strategy
   - 8.1 Backup Topology (3-2-1)
   - 8.2 DR Site Planning
9. Monitoring, Alerting & SIEM
   - 9.1 Zabbix Network Monitoring
   - 9.2 Splunk SIEM
   - 9.3 Log Retention Policy
10. Power & Environmental
    - 10.1 Power Load Calculation
    - 10.2 UPS Recommendation
    - 10.3 ATS Configuration
    - 10.4 SNMP Monitoring
11. Asset Lifecycle & Warranty Management
12. SOP Documents & Training Plan
13. Bill of Materials (BOM) — INR
14. Implementation Timeline
15. Acceptance Criteria
16. Appendices
    - A. Network Diagram (Detailed)
    - B. IP Address Scheme
    - C. VLAN Design
    - D. Firewall Policy Matrix
    - E. Backup Schedule
    - F. DR Runbook
    - G. SOP Documents

---

## 1. Executive Summary

[Brief overview of the project, objectives, and key design decisions. 1-2 paragraphs.]

---

## 2. Scope & Requirements

### 2.1 In Scope
- [List all deliverables]

### 2.2 Out of Scope
- Physical security (biometric, CCTV, access control) — client responsibility
- [Other exclusions]

### 2.3 Requirements Summary

| Requirement | Details |
|-------------|---------|
| Users/Endpoints | [Number] |
| Floors/Buildings | [Number] |
| Deployment Type | Greenfield / Brownfield |
| Internet Bandwidth | [Current → Required] |
| ISP Links | [Number] |
| VPN | [Site-to-site / Remote access / None] |
| Redundancy | Scenario A (HA) / Scenario B (Non-HA) |
| DR Requirement | Yes — [Cold/Warm/Hot] site |
| Budget Range | INR [Amount] |
| Timeline | [Duration] |

---

## 3. Architecture Overview & Diagram

### 3.1 High-Level Architecture

[Insert Mermaid or ASCII diagram showing full topology]

### 3.2 Design Principles
- [List key design decisions and their rationale]

---

## 4. ISO 27001 Compliance Mapping

| ISO Control | Requirement | Implementation | Status |
|-------------|-------------|----------------|--------|
| A.8.3 | Information access restriction | VLAN segmentation + firewall ACLs | Planned |
| A.8.5 | Secure authentication | 802.1X + RADIUS + WPA3-Enterprise | Planned |
| A.8.7 | Malware protection | FortiGate UTM (AV + IPS + Sandbox) | Planned |
| A.8.13 | Information backup | 3-2-1 rule with Veeam + Synology | Planned |
| A.8.14 | Redundancy | [Scenario A or B details] | Planned |
| A.8.15 | Logging | Splunk SIEM + 90d/1y/3y retention | Planned |
| A.8.20 | Network security | FortiGate zones + UTM policies | Planned |
| A.8.22 | Network segregation | VLAN design per function | Planned |
<!-- Add all applicable ISO controls — every row must be fully populated -->

---

## 5. Network Infrastructure Design

### 5.1 Firewall — Fortinet FortiGate

| Item | Details |
|------|---------|
| Model | FortiGate [Model] |
| Quantity | [1 or 2 for HA] |
| HA Mode | [Active-Passive / Active-Active / N/A] |
| License | [UTP / ATP] — [Duration] |
| Key Features | SD-WAN, UTM, SSL Inspection, VPN |

#### Firewall Zones
| Zone | Purpose | Interfaces |
|------|---------|------------|
| WAN | Internet connectivity | [ports] |
| LAN | Internal network | [ports] |
| DMZ | Public-facing services | [ports] |
| Management | Device management | [ports] |

### 5.2 Switches

[Repeat per switch type]

| Item | Details |
|------|---------|
| Model | [Model] |
| Quantity | [Number] |
| Port Count | [X GE + Y SFP+] |
| PoE Budget | [Watts] |
| Layer | L2 / L3 |
| Stacking | Yes / No |
| License | [GreenLake / DNA Essentials] |

### 5.3 Cabling

| Type | Standard | Use Case | Quantity |
|------|----------|----------|----------|
| Copper | Cat 6 / Cat 6A | Horizontal runs, endpoint to patch panel | [X runs] |
| Fiber | CommScope OM4 | Inter-floor backbone, switch-to-switch | [X strands] |
| Fiber | CommScope OS2 | Building-to-building (if applicable) | [X strands] |

### 5.4 Network Redundancy

[Detail Scenario A or B based on user selection]

---

## 6. Wireless Infrastructure — FortiAP

| Location | AP Model | Quantity | Clients | SSID | Security |
|----------|----------|----------|---------|------|----------|
| [Floor/Area] | FortiAP [Model] | [X] | [Y] | Corporate | WPA3-Enterprise + 802.1X |
| [Floor/Area] | FortiAP [Model] | [X] | [Y] | Guest | Captive Portal |

**RADIUS Configuration:**
- Server: [Windows NPS / FortiAuthenticator]
- Authentication: EAP-TLS / PEAP-MSCHAPv2

---

## 7. Server Infrastructure

| Role | Model | CPU | RAM | Storage | RAID | OS | License |
|------|-------|-----|-----|---------|------|----|---------|
| [AD/DNS] | HPE DL[XX] | [Xeon] | [GB] | [Drives] | [Level] | [OS] | [License] |
| [File Server] | HPE DL[XX] | [Xeon] | [GB] | [Drives] | [Level] | [OS] | [License] |
| [Backup NAS] | Synology [Model] | [Embedded] | [GB] | [Drives] | [Level] | DSM | Included |

---

## 8. Disaster Recovery & Backup

### 8.1 Backup Topology (3-2-1)

| Copy | Location | Media | Software | Schedule |
|------|----------|-------|----------|----------|
| Copy 1 | Local repository | SSD/HDD | Veeam | Daily incremental, weekly full |
| Copy 2 | Synology NAS | NAS HDD | Veeam backup copy | Daily, 4h after primary |
| Copy 3 | Offsite/Cloud | Cloud/DR site | Veeam Cloud Connect | Daily |

### 8.2 RPO/RTO Targets

| System | RPO | RTO | Backup Frequency |
|--------|-----|-----|-------------------|
| [Critical system] | [Hours] | [Hours] | [Schedule] |

### 8.3 DR Site Plan

| Item | Details |
|------|---------|
| DR Location | [Location] |
| DR Tier | Cold / Warm / Hot |
| Replication Method | [Sync / Async] |
| Failover Procedure | See Appendix F |
| Testing Schedule | Quarterly |

---

## 9. Monitoring, Alerting & SIEM

### 9.1 Zabbix

| Item | Details |
|------|---------|
| Zabbix Server VM | [CPU/RAM/Storage] |
| Monitored Devices | [Total count] |
| Protocol | SNMP v3 |
| Alert Method | Email + [Slack/Teams/SMS] |

### 9.2 Splunk

| Item | Details |
|------|---------|
| License Tier | [Free/Enterprise] |
| Daily Ingestion | [X GB/day] |
| Log Sources | FortiGate, Switches, Servers, AD |
| Retention | 90d hot / 1y warm / 3y cold |

### 9.3 Key Correlation Rules
- [ ] Brute force detection (>5 failed logins in 5 min)
- [ ] Unauthorized access attempts
- [ ] Admin login from unusual IP
- [ ] Anomalous traffic volume
- [ ] Policy violation alerts

---

## 10. Power & Environmental

### 10.1 Power Load Calculation

| Device | Model | Qty | Power (W) | Total (W) |
|--------|-------|-----|-----------|-----------|
| Firewall | [Model] | [X] | [W] | [Total] |
| Switches | [Model] | [X] | [W] | [Total] |
| Servers | [Model] | [X] | [W] | [Total] |
| NAS | [Model] | [X] | [W] | [Total] |
| APs (PoE) | [Model] | [X] | [W] | [Total] |
| **Total Load** | | | | **[Total W]** |
| **+ 20% Headroom** | | | | **[Adjusted W]** |
| **Required VA** | | | | **[VA at 0.9 PF]** |

### 10.2 UPS Recommendation

| UPS | Model | Capacity | Runtime | Price (INR) |
|-----|-------|----------|---------|-------------|
| Primary | [Brand Model] | [kVA] | [min] | [INR] |
| Redundant | [Brand Model] | [kVA] | [min] | [INR] |

### 10.3 ATS
- Model: [ATS Model]
- Configuration: [Mains → UPS1 → UPS2 / Generator]

### 10.4 SNMP Monitoring (via Zabbix)
- Monitored metrics: Battery health, load %, voltage, temperature, runtime

---

## 11. Asset Lifecycle & Warranty

| # | Device | Model | Serial | Warranty | EOL Date | AMC (INR/yr) | Renewal |
|---|--------|-------|--------|----------|----------|--------------|---------|
| 1 | [Device] | [Model] | [TBD] | [Period] | [Date] | [INR] | [Notes] |

### Total Cost of Ownership

| Year | Hardware | Licenses | AMC | Support | Total (INR) |
|------|----------|----------|-----|---------|-------------|
| Year 1 | [INR] | [INR] | — | [INR] | [INR] |
| Year 2 | — | [INR] | [INR] | [INR] | [INR] |
| Year 3 | — | [INR] | [INR] | [INR] | [INR] |
| **3-Year TCO** | | | | | **[INR]** |
| Year 4 | — | [INR] | [INR] | [INR] | [INR] |
| Year 5 | — | [INR] | [INR] | [INR] | [INR] |
| **5-Year TCO** | | | | | **[INR]** |

---

## 12. SOP Documents & Training

### Deliverable SOPs

| SOP # | Title | Audience | Pages |
|-------|-------|----------|-------|
| SOP-NET-001 | FortiGate Daily Operations | Network Admin | — |
| SOP-NET-002 | Switch Management | Network Admin | — |
| SOP-NET-003 | FortiAP Wireless Management | Network Admin | — |
| SOP-MON-001 | Zabbix Monitoring & Alert Response | Network Admin | — |
| SOP-SRV-001 | Server Patching & Maintenance | System Admin | — |
| SOP-BKP-001 | Backup & Restore Procedures | System Admin | — |
| SOP-DR-001 | DR Failover & Failback | System Admin | — |
| SOP-SEC-001 | Splunk SIEM Review | IT Manager/CISO | — |
| SOP-SEC-002 | Incident Response Workflow | IT Manager/CISO | — |
| SOP-SEC-003 | ISO 27001 Audit Prep Checklist | IT Manager/CISO | — |
| SOP-USR-001 | Wi-Fi & VPN Access Guide | End Users | — |

---

## 13. Bill of Materials — INR

| # | Category | Item | Model | Qty | Unit (INR) | Total (INR) | Warranty |
|---|----------|------|-------|-----|------------|-------------|----------|
| | **Firewall** | | | | | | |
| 1 | | FortiGate | [Model] | [X] | [INR] | [INR] | [Period] |
| 2 | | FortiGuard License | [Bundle] | [X] | [INR] | [INR] | [Period] |
| | **Switches** | | | | | | |
| 3 | | [Switch] | [Model] | [X] | [INR] | [INR] | [Period] |
| | **Wireless** | | | | | | |
| 4 | | FortiAP | [Model] | [X] | [INR] | [INR] | [Period] |
| | **Servers** | | | | | | |
| 5 | | HPE Server | [Model] | [X] | [INR] | [INR] | [Period] |
| | **Storage** | | | | | | |
| 6 | | Synology NAS | [Model] | [X] | [INR] | [INR] | [Period] |
| | **UPS & Power** | | | | | | |
| 7 | | UPS | [Model] | [X] | [INR] | [INR] | [Period] |
| 8 | | ATS | [Model] | [X] | [INR] | [INR] | [Period] |
| | **Cabling** | | | | | | |
| 9 | | Cat 6 Cable | [Brand] | [X runs] | [INR] | [INR] | — |
| 10 | | CommScope Fiber | [Type] | [X strands] | [INR] | [INR] | — |
| | **Software** | | | | | | |
| 11 | | [License] | [Product] | [X] | [INR] | [INR] | [Period] |
| | **Services** | | | | | | |
| 12 | | Implementation | Labor | [Days] | [INR/day] | [INR] | — |
| 13 | | AMC (Year 2+) | Annual | 1 | [INR] | [INR] | Annual |

| | | | |
|---|---|---|---|
| **Subtotal** | | | **[INR]** |
| **GST (18%)** | | | **[INR]** |
| **Grand Total** | | | **[INR]** |

### Year 1 vs Recurring Costs

| | Year 1 (INR) | Year 2-5 Annual (INR) |
|---|---|---|
| Capital (Hardware) | [INR] | — |
| Licenses | [INR] | [INR] |
| AMC | — | [INR] |
| Support | [INR] | [INR] |
| **Total** | **[INR]** | **[INR/year]** |

---

## 14. Implementation Timeline

| Phase | Activities | Duration | Dependencies | Owner |
|-------|-----------|----------|--------------|-------|
| 1 | Site survey & requirement finalization | Week 1-2 | — | VConfi |
| 2 | Procurement & staging | Week 3-5 | Phase 1 sign-off | VConfi |
| 3 | Cabling & physical setup | Week 4-6 | Materials arrival | VConfi + Cabling vendor |
| 4 | Network deployment | Week 5-7 | Phase 3 | VConfi Network Team |
| 5 | Server deployment | Week 6-8 | Phase 4 | VConfi Server Team |
| 6 | Wireless deployment | Week 7-8 | Phase 4 | VConfi Network Team |
| 7 | Monitoring & SIEM | Week 8-9 | Phase 4, 5 | VConfi |
| 8 | DR & backup config | Week 8-9 | Phase 5 | VConfi Server Team |
| 9 | Testing & validation | Week 9-10 | All phases | VConfi QA |
| 10 | Documentation & training | Week 10-11 | Phase 9 | VConfi |
| 11 | Go-live & hypercare | Week 11-12 | Phase 10 | VConfi |

---

## 15. Acceptance Criteria

- [ ] All devices deployed and accessible
- [ ] Network connectivity verified across all VLANs
- [ ] Firewall policies tested and documented
- [ ] Wireless coverage validated (heat map)
- [ ] Servers operational with applications running
- [ ] Backup jobs completing successfully
- [ ] DR failover test completed
- [ ] Monitoring dashboards live with alerts working
- [ ] SIEM collecting and correlating logs
- [ ] All SOPs delivered and training completed
- [ ] BOM reconciled with deployed equipment
- [ ] Client sign-off obtained

---

## Appendices

### Appendix A: Network Diagram (Detailed)
[Full topology diagram]

### Appendix B: IP Address Scheme
| VLAN | Name | Subnet | Gateway | DHCP Range | Description |
|------|------|--------|---------|------------|-------------|

### Appendix C: VLAN Design
| VLAN ID | Name | Purpose | Allowed Destinations |
|---------|------|---------|---------------------|

### Appendix D: Firewall Policy Matrix
| # | Source Zone | Dest Zone | Service | Action | Log | Comment |
|---|-----------|----------|---------|--------|-----|---------|

### Appendix E: Backup Schedule
| System | Type | Schedule | Retention | Target |
|--------|------|----------|-----------|--------|

### Appendix F: DR Runbook
[Step-by-step failover and failback procedures]

### Appendix G: SOP Documents
[Individual SOP documents attached]
