# ISO 27001:2022 Controls Reference — VConfi Implementation Mapping

## Relevant Controls for IT Infrastructure

### A.5 — Organizational Controls
| Control | Description | VConfi Mapping |
|---------|-------------|----------------|
| A.5.1 | Policies for information security | Document security policies for all deployed systems |
| A.5.2 | Information security roles | Define roles: Network Admin, Sys Admin, IT Manager, CISO |
| A.5.3 | Segregation of duties | Separate firewall admin from server admin roles |

### A.6 — People Controls
| Control | Description | VConfi Mapping |
|---------|-------------|----------------|
| A.6.3 | Information security awareness | End-user training SOPs, security awareness basics |
| A.6.5 | Responsibilities after termination | AD account disable procedures in SOP |

### A.7 — Physical Controls
| Control | Description | VConfi Mapping |
|---------|-------------|----------------|
| A.7.1 | Physical security perimeters | Server room physical boundaries (out of scope but document) |
| A.7.4 | Physical security monitoring | Note: Physical security is outside VConfi scope — client responsibility |
| A.7.8 | Equipment siting and protection | Rack placement, UPS, environmental controls |
| A.7.9 | Security of assets off-premises | DR site security requirements |
| A.7.10 | Storage media | Backup media handling and disposal procedures |
| A.7.11 | Supporting utilities | UPS, ATS, power redundancy design |
| A.7.12 | Cabling security | Cat 6/CommScope fiber standards |
| A.7.13 | Equipment maintenance | AMC, warranty tracking, preventive maintenance schedule |

### A.8 — Technological Controls
| Control | Description | VConfi Mapping |
|---------|-------------|----------------|
| A.8.1 | User endpoint devices | Endpoint security policies via FortiGate |
| A.8.2 | Privileged access rights | Admin accounts, RBAC on all devices |
| A.8.3 | Information access restriction | VLAN segmentation, firewall rules, ACLs |
| A.8.4 | Access to source code | Not applicable for infra deployments |
| A.8.5 | Secure authentication | 802.1X, RADIUS, WPA3-Enterprise, MFA for admin access |
| A.8.6 | Capacity management | Switch port headroom (40%), server sizing (30% headroom) |
| A.8.7 | Protection against malware | FortiGate AV, IPS, sandboxing (if ATP license) |
| A.8.8 | Management of technical vulnerabilities | FortiGuard updates, firmware management procedures |
| A.8.9 | Configuration management | Baseline configs documented for all devices |
| A.8.10 | Information deletion | Data sanitization procedures for decommissioned equipment |
| A.8.12 | Data leakage prevention | FortiGate DLP policies, application control |
| A.8.13 | Information backup | 3-2-1 backup rule, Veeam/Synology backup strategy |
| A.8.14 | Redundancy of information processing | HA scenarios (Scenario A), DR site planning |
| A.8.15 | Logging | Zabbix monitoring, Splunk SIEM, log retention policies |
| A.8.16 | Monitoring activities | Zabbix dashboards, Splunk correlation rules, alert escalation |
| A.8.20 | Network security | Firewall zones, VLAN segmentation, UTM policies |
| A.8.21 | Security of network services | ISP SLA verification, SD-WAN configuration |
| A.8.22 | Segregation of networks | VLAN design, inter-VLAN routing policies |
| A.8.23 | Web filtering | FortiGuard web filtering categories |
| A.8.24 | Use of cryptography | VPN encryption (IPSec/SSL), TLS policies |
| A.8.25 | Secure development lifecycle | Not applicable for infra deployments |
| A.8.26 | Application security requirements | WAF if web servers are in scope |
| A.8.28 | Secure coding | Not applicable for infra deployments |

## Log Retention Policy — ISO 27001 Guidance

### Minimum Requirements
| Log Type | Hot Storage (Searchable) | Warm Storage (Archived) | Cold Storage (Compliance) |
|----------|------------------------|------------------------|--------------------------|
| Firewall logs | 90 days | 1 year | 3 years |
| Authentication logs | 90 days | 1 year | 3 years |
| VPN logs | 90 days | 1 year | 3 years |
| Server event logs | 90 days | 1 year | 3 years |
| Switch/AP logs | 30 days | 6 months | 1 year |
| Backup job logs | 90 days | 1 year | 3 years |
| Admin change logs | 90 days | 1 year | 5 years |

### Requirements
- Logs must be **tamper-proof** (write-once or hash-verified)
- Log access must be **restricted** to authorized personnel only
- Log **integrity checks** must be performed regularly
- Log **retention exceptions** must be documented with justification
- Time synchronization (**NTP**) must be configured on all devices for accurate timestamps

## Audit Preparation Checklist

Before any ISO 27001 audit, verify:

- [ ] All devices inventoried with serial numbers, locations, and owners
- [ ] Network diagrams are current and match actual topology
- [ ] Firewall rules are documented and reviewed (last review date recorded)
- [ ] Backup restore tests completed (with documented results)
- [ ] DR test completed within last quarter (with documented results)
- [ ] All user access reviews completed (quarterly)
- [ ] Vulnerability scans completed (monthly) with remediation records
- [ ] Log retention verified across all systems
- [ ] SOP documents are current and signed off
- [ ] Change management records are complete for all recent changes
- [ ] Incident response procedures tested (tabletop or simulation)
- [ ] AMC/warranty status verified for all devices
