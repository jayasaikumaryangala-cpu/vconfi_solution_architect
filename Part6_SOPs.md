# Part 6: Standard Operating Procedures (SOPs)
## B2H Studios IT Infrastructure Implementation Plan

---

**Document Information**
- **Client:** B2H Studios
- **Industry:** Media & Entertainment — Post-Production
- **Document Version:** 1.0
- **Date:** March 22, 2026
- **Prepared by:** VConfi Solutions
- **Classification:** CONFIDENTIAL — Internal Use Only

---

## Table of Contents

1. [SOP-001: Network Administration](#sop-001-network-administration)
2. [SOP-002: Monitoring System Management](#sop-002-monitoring-system-management)
3. [SOP-003: Server Administration](#sop-003-server-administration)
4. [SOP-004: Storage Administration](#sop-004-storage-administration)
5. [SOP-005: Backup Operations](#sop-005-backup-operations)
6. [SOP-006: Disaster Recovery](#sop-006-disaster-recovery)
7. [SOP-007: Security Operations](#sop-007-security-operations)
8. [SOP-008: Incident Response](#sop-008-incident-response)
9. [SOP-009: Change Management](#sop-009-change-management)
10. [SOP-010: User Access Management](#sop-010-user-access-management)
11. [SOP-011: Vendor Management](#sop-011-vendor-management)

---

# SOP-001: Network Administration

## Purpose
To establish standardized procedures for network infrastructure management, including VLAN administration, switch configuration, firmware maintenance, and troubleshooting for the B2H Studios HPE Aruba CX 6300M VSX infrastructure.

## Scope
This SOP applies to all network infrastructure including:
- HPE Aruba CX 6300M switches (SW1, SW2)
- FortiGate 120G firewalls
- VLAN configuration (VLAN 10, 20, 30, 40, 50)
- LACP aggregations and trunk ports
- ISL/VSX links

## Responsibility
| Role | Responsibility |
|------|----------------|
| Network Administrator | Day-to-day VLAN and switch management |
| Senior Network Engineer | Firmware upgrades, major configuration changes |
| IT Manager | Approval for changes affecting production |

## Prerequisites
- Administrative access to HPE Aruba CX switches
- FortiGate admin credentials
- Network documentation (IP schemes, VLAN assignments)
- Maintenance window for intrusive changes
- Configuration backup from previous day

## Procedure

### 1. VLAN Management

#### 1.1 Create New VLAN
```bash
# Connect to primary switch (SW1)
ssh admin@10.10.40.2

# Enter configuration mode
configure terminal

# Create new VLAN
vlan 60
  name NewProject_VLAN
  description "VLAN for new project team"
  exit

# Configure VLAN interface
interface vlan 60
  ip address 10.10.60.2/24
  exit

# Apply to VSX
vsx-sync vlan 60

# Save configuration
copy running-config startup-config

# Verify on both switches
show vlan 60
show vsx status
```

#### 1.2 Modify VLAN Membership
```bash
# Add port to VLAN (access mode)
interface 1/1/25
  no shutdown
  vlan access 20
  exit

# Configure trunk port
interface 1/1/26
  no shutdown
  vlan trunk native 1
  vlan trunk allowed 10,20,30,40,50
  exit

# Save and verify
copy running-config startup-config
show vlan port-config interface 1/1/26
```

### 2. Switch Configuration Backup and Restore

#### 2.1 Manual Backup
```bash
# Create timestamped backup
show running-config | tee running-config-$(date +%Y%m%d-%H%M%S).cfg

# Automated backup to TFTP server
copy running-config tftp://10.10.40.10/backups/sw1-running-$(date +%Y%m%d).cfg

# Verify backup integrity
show startup-config
```

#### 2.2 Scheduled Backup Configuration
```bash
# Configure automated daily backup
copy running-config startup-config

# Set up checkpoint schedule
checkpoint auto-save interval 1440  # Daily

# Configure remote backup via SCP
ssh-scp-server enable
```

#### 2.3 Configuration Restore
```bash
# WARNING: Restore will cause brief outage

# Method 1: Restore from startup-config
boot system goback  # Rollback to previous boot

# Method 2: Restore from file
copy tftp://10.10.40.10/backups/sw1-running-20260322.cfg running-config

# Method 3: Restore specific section
configure terminal
# Manually re-enter configuration sections
exit
copy running-config startup-config
```

### 3. Firmware Upgrade Procedure (ISSU)

#### 3.1 Pre-Upgrade Checklist
- [ ] Verify current firmware: `show firmware`
- [ ] Check VSX status: `show vsx status` (must be "in-sync")
- [ ] Verify no active alarms: `show alarms`
- [ ] Confirm backup exists
- [ ] Schedule maintenance window
- [ ] Notify stakeholders

#### 3.2 ISSU Upgrade Steps
```bash
# Step 1: Download firmware to primary switch (SW1)
copy tftp://10.10.40.10/firmware/ArubaOS-CX_10.13.swi primary

# Step 2: Verify image integrity
show firmware

# Step 3: Upgrade secondary switch first (SW2 via VSX)
vsx update-software secondary

# Step 4: Monitor upgrade progress (takes 5-10 minutes)
show vsx status

# Step 5: Failover to upgraded SW2
vsx switchover

# Step 6: Verify SW2 is now primary
show vsx status

# Step 7: Upgrade SW1 (now secondary)
vsx update-software secondary

# Step 8: Optional: Switch back to original primary
vsx switchover

# Step 9: Verify final state
show vsx status
show firmware
```

#### 3.3 Post-Upgrade Verification
```bash
# Verify all services operational
show running-config | include vlan
show lacp aggregates
show ip route

# Test connectivity
ping 10.10.30.10  # NAS
ping 10.10.20.1   # Gateway

# Monitor for 30 minutes
show interface counters
```

### 4. Troubleshooting Common Issues

#### 4.1 VSX Split-Brain Recovery
```bash
# Symptom: Both switches show "primary" status

# Step 1: Identify which switch has correct config
show running-config | include "vlan\|interface"

# Step 2: On incorrect switch, force standby
vsx restart

# Step 3: On correct switch, verify sync
show vsx status

# Step 4: If sync fails, reinitialize VSX
vsx peer-sync
```

#### 4.2 LACP Link Flapping
```bash
# Check LACP status
show lacp aggregates
show lacp interface

# Check physical layer
show interface 1/1/49-1/1/50
show interface transceiver

# Check for errors
show interface counters errors

# Reset LACP if necessary (maintenance window required)
interface lag 10
  no shutdown
  lacp port-priority 1
  exit
```

#### 4.3 VLAN Trunk Issues
```bash
# Verify trunk configuration
show vlan port-config
show vlan trunk

# Check allowed VLANs match on both ends
show interface 1/1/1 trunk

# Test VLAN connectivity
show mac-address-table vlan 30
```

#### 4.4 High CPU/Memory
```bash
# Identify process consuming resources
show system resource-utilization
show process cpu
show process memory

# Check for broadcast storms
show interface counters rates
show spanning-tree

# Collect diagnostic data
diagnostics
show tech
```

### 5. Port Security Procedures

#### 5.1 Enable Port Security
```bash
interface 1/1/25
  port-access authenticator
  port-access authenticator authentication-method dot1x
  exit
```

#### 5.2 MAC Lockdown
```bash
# Static MAC binding
mac-address-table static 00:11:22:33:44:55 vlan 20 interface 1/1/25

# Port security with MAC limit
interface 1/1/25
  port-security
  port-security maximum 1
  exit
```

## Verification
| Check | Command | Expected Result |
|-------|---------|-----------------|
| VSX Status | `show vsx status` | "in-sync", one primary, one secondary |
| VLAN Config | `show vlan` | All 5 VLANs present |
| LACP Status | `show lacp aggregates` | All members "bundled" |
| Interfaces | `show interface brief` | Critical ports "up/up" |
| Firmware | `show firmware` | Same version on both switches |

## Rollback
If issues occur post-change:
1. Identify last known good configuration
2. `boot system goback` to previous firmware (for ISSU)
3. Restore configuration from backup
4. Contact HPE TAC if unresolved

## Escalation Matrix
| Severity | Contact | Response Time |
|----------|---------|---------------|
| P1 - Critical (Total network outage) | Network Admin: +91-XXXXXXXXXX | 15 minutes |
| P2 - High (Degraded performance) | Senior Network Eng: +91-XXXXXXXXXX | 1 hour |
| P3 - Medium (Single link failure) | Network Admin | 4 hours |
| P4 - Low (Documentation updates) | IT Team | 1 business day |

| Vendor Escalation | Contact | SLA |
|-------------------|---------|-----|
| HPE Support | 1800-425-4333 | 4-hour response |
| Fortinet TAC | support.fortinet.com | 1-hour response (P1) |

## Related Documents
- SOP-002: Monitoring System Management
- SOP-006: Disaster Recovery
- Design_Decisions_Detailed.md (Section 3: Network Infrastructure)
- Part2_Enhanced_Network_Wireless_Server.md

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 22-Mar-2026 | VConfi | Initial release |

---

# SOP-002: Monitoring System Management

## Purpose
To define standardized procedures for Zabbix monitoring system administration, including daily health checks, alert management, dashboard maintenance, and performance reporting for the B2H Studios infrastructure.

## Scope
This SOP covers:
- Zabbix Server (VM on Dell R760)
- SNMP monitoring of network devices
- Agent-based server monitoring
- Alert acknowledgment and escalation
- Dashboard and report generation
- Threshold management

## Responsibility
| Role | Responsibility |
|------|----------------|
| Monitoring Administrator | Daily health checks, alert triage |
| System Administrator | Threshold adjustments, agent deployment |
| IT Manager | SLA reporting, escalation management |

## Prerequisites
- Zabbix web interface access (https://zabbix.b2h.local)
- Admin credentials for Zabbix
- SNMP read-only community strings
- Network access to all monitored devices
- Zabbix agent installed on servers

## Procedure

### 1. Daily Health Checks

#### 1.1 Morning Checklist (09:00 AM)
```bash
# Log into Zabbix web interface
# Navigate to: Monitoring → Dashboard

Checklist:
□ System status widget: All green (no red alerts)
□ Host availability: 100% for critical systems
□ Latest data review: No anomalous values
□ Trigger status: Review acknowledged vs unacknowledged alerts
□ Event history: Review overnight events
```

#### 1.2 Critical Systems Verification
| System | Check Method | Normal Value | Action if Abnormal |
|--------|--------------|--------------|-------------------|
| FortiGate 120G | ICMP ping + SNMP | <1ms latency | Check WAN connectivity |
| HD6500 NAS | SNMP + API | CPU <50% | Check for backup jobs |
| HPE Switches | SNMP | CPU <40% | Check for broadcast storm |
| Dell R760 | Zabbix Agent | CPU <70% | Check VM resource usage |
| UPS | SNMP | Load <80% | Verify power draw |

#### 1.3 Replication Health Check
```bash
# Access Synology DSM
ssh admin@10.10.30.10

# Check replication status
synoreplog --status

# Verify no errors
synoreplog --list

# Check RPO compliance (should be <15 minutes)
synoreplog --last-sync
```

### 2. Alert Acknowledgment Procedures

#### 2.1 Alert Triage Process
```
P1 (Critical - Red): Immediate action required
├── Site down, production stopped
├── Ransomware detection
└── Response: Page on-call engineer immediately

P2 (High - Orange): Action within 1 hour
├── Service degradation
├── Replication lag >1 hour
└── Response: Create ticket, assign engineer

P3 (Medium - Yellow): Action within 4 hours
├── Single component failure
├── Predictive disk failure
└── Response: Schedule maintenance

P4 (Low - Blue): Action within 24 hours
├── Informational only
└── Response: Log for review
```

#### 2.2 Acknowledgment Procedure
1. Log into Zabbix: `https://zabbix.b2h.local`
2. Navigate to: Monitoring → Problems
3. Click on alert to view details
4. Click "Acknowledge" button
5. Enter acknowledgment message:
   ```
   Acknowledged by: [Name]
   Time: [Timestamp]
   Action: [What you're doing]
   ETA Resolution: [When it will be fixed]
   ```
6. Select severity-appropriate options:
   - [ ] Close problem (only when resolved)
   - [ ] Acknowledge
   - [ ] Suppress notifications

#### 2.3 False Positive Management
```bash
# Temporarily disable problematic trigger (emergency only)
# Better approach: Adjust threshold

Configuration → Hosts → [Host] → Triggers → [Trigger]
# Click "Edit" and modify expression
# Example: Change CPU threshold from 80% to 85%

# Add maintenance window for planned work
Configuration → Maintenance → Create maintenance period
```

### 3. Dashboard Maintenance

#### 3.1 NOC Dashboard Components
```
┌─────────────────────────────────────────────────────────┐
│ TOP ROW - Executive Summary                               │
│ [System Health Score] [Uptime %] [Active Alerts] [SLA]    │
├─────────────────────────────────────────────────────────┤
│ LEFT COLUMN              │ RIGHT COLUMN                   │
│ Network Health           │ Storage Health                 │
│ - FortiGate Status       │ - HD6500 Capacity              │
│ - Bandwidth Utilization  │ - Replication Status           │
│ - VPN Sessions           │ - RAID Health                  │
│                          │                                │
│ Switch Status            │ Compute Health                 │
│ - VSX Stack State        │ - VM Resource Usage            │
│ - Port Utilization       │ - Top Processes                │
└─────────────────────────────────────────────────────────┘
```

#### 3.2 Creating Custom Dashboard
```bash
# Web interface steps:
1. Monitoring → Dashboards → Create dashboard
2. Name: "Site B DR Dashboard"
3. Add widgets:
   - Graph: Network bandwidth
   - Map: Network topology
   - Problems: Unresolved alerts
   - System info: Key metrics
4. Set refresh interval: 30 seconds
5. Share with appropriate users
```

#### 3.3 Widget Configuration Examples
```sql
-- CPU Utilization Graph (Zabbix SQL for custom reports)
SELECT itemid, clock, value
FROM history
WHERE itemid IN (
  SELECT itemid FROM items 
  WHERE name LIKE '%CPU utilization%'
  AND hostid = [R760_hostid]
)
AND clock > UNIX_TIMESTAMP(NOW() - INTERVAL 24 HOUR);
```

### 4. Threshold Adjustment Process

#### 4.1 Threshold Change Request
```
Change Request Form:
━━━━━━━━━━━━━━━━━━━━
Requested by: [Name]
Date: [Date]
Host/Item: [e.g., HD6500 - CPU Utilization]
Current Threshold: [Value]
Proposed Threshold: [Value]
Justification: [Why change is needed]
Risk Assessment: [Impact of false positives/missed alerts]
Approval: [IT Manager signature]
```

#### 4.2 Implementing Threshold Changes
```bash
# Navigate to Configuration → Hosts → [Host] → Items
# Find the item to modify (e.g., "CPU utilization")

# Edit trigger expression
# Original: {HD6500:system.cpu.util[all].last()}>80
# New:      {HD6500:system.cpu.util[all].last()}>85

# Add hysteresis to prevent flapping
# Original: >80
# New:      >85 and <75 (high threshold 85, recovery 75)
```

#### 4.3 Standard Thresholds Reference
| Metric | Warning | High | Critical | Notes |
|--------|---------|------|----------|-------|
| CPU Utilization | 70% | 80% | 90% | Sustained 5 min |
| Memory Usage | 75% | 85% | 95% | Available RAM |
| Disk Usage | 80% | 85% | 90% | Plan expansion at 80% |
| Network Utilization | 60% | 75% | 90% | Of link capacity |
| Temperature | 35°C | 40°C | 45°C | Ambient + component |
| Replication Lag | 15 min | 30 min | 60 min | RPO breach |

### 5. Report Generation

#### 5.1 Weekly Health Report
```bash
# Automated report generation
# Configure in Zabbix: Reports → Scheduled reports

Report Contents:
━━━━━━━━━━━━━━━
1. Executive Summary
   - Overall system health score
   - Uptime percentage by system
   - Critical incidents count

2. Capacity Trends
   - Storage utilization trend
   - Network bandwidth trend
   - VM resource growth

3. Incident Summary
   - All P1/P2 incidents
   - Mean Time To Resolution (MTTR)
   - Recurring issues

4. Compliance Status
   - Backup success rate
   - Patch compliance
   - Security alerts
```

#### 5.2 Monthly SLA Report
```sql
-- Uptime calculation query template
SELECT 
  h.name AS hostname,
  COUNT(CASE WHEN e.value = 1 THEN 1 END) * 100.0 / COUNT(*) AS uptime_pct
FROM hosts h
JOIN events e ON h.hostid = e.objectid
WHERE e.clock >= UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL 30 DAY))
GROUP BY h.hostid;
```

#### 5.3 Custom SNMP Template Updates
```bash
# For new device types, create SNMP template

1. Configuration → Templates → Create template
2. Template name: "Synology HD6500 Custom"
3. Add Items:
   - OID: 1.3.6.1.4.1.6574.1.1.0 (System Status)
   - OID: 1.3.6.1.4.1.6574.1.2.0 (Temperature)
   - OID: 1.3.6.1.4.1.6574.1.4.1.0 (RAID Status)
4. Create Triggers based on item values
5. Link template to host
```

## Verification
| Check | Method | Expected Result |
|-------|--------|-----------------|
| Zabbix Server | `systemctl status zabbix-server` | Active (running) |
| Database | `systemctl status mysql` | Active (running) |
| Agent Communication | `zabbix_get -s [host] -k agent.ping` | 1 (success) |
| Web Interface | Browse to zabbix.b2h.local | Login page loads |
| Alerting | Test trigger | Email/SMS received |

## Rollback
If monitoring changes cause issues:
1. Revert to previous template version
2. Restore original thresholds
3. Restart Zabbix services if needed:
   ```bash
   systemctl restart zabbix-server zabbix-agent
   ```

## Escalation Matrix
| Severity | Contact | Response Time |
|----------|---------|---------------|
| P1 - Critical | Monitoring Admin: +91-XXXXXXXXXX | 15 minutes |
| P2 - High | System Admin: +91-XXXXXXXXXX | 1 hour |
| P3 - Medium | IT Support: +91-XXXXXXXXXX | 4 hours |
| Zabbix Vendor | Zabbix Support Portal | 24 hours |

## Related Documents
- SOP-001: Network Administration
- SOP-004: Storage Administration
- SOP-008: Incident Response

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 22-Mar-2026 | VConfi | Initial release |

---

# SOP-003: Server Administration

## Purpose
To establish standardized procedures for VMware vSphere server management, VM provisioning, resource allocation, backup verification, and patch management for the B2H Studios Dell R760 infrastructure.

## Scope
This SOP covers:
- VMware vSphere 8 management
- VM lifecycle management
- Resource allocation and optimization
- Veeam backup verification
- OS and application patching

## Responsibility
| Role | Responsibility |
|------|----------------|
| System Administrator | VM provisioning, patching |
| Senior System Admin | Resource planning, capacity |
| IT Manager | Change approval, maintenance windows |

## Prerequisites
- vSphere Web Client access (https://vcenter.b2h.local)
- Administrative privileges on vCenter
- Veeam Backup & Replication console access
- VM templates prepared
- Maintenance windows scheduled

## Procedure

### 1. VMware vSphere Management

#### 1.1 Daily vCenter Health Check
```bash
# SSH to vCenter Server Appliance (VCSA)
ssh root@vcenter.b2h.local

# Check services status
service-control --status --all

# Expected running services:
# applmgmt, rbd, vmcam, vmonapi, vmware-analytics, vmware-cis-license
# vmware-cm, vmware-content-library, vmware-eam, vmware-imagebuilder
# vmware-mbcs, vmware-netdumper, vmware-perfcharts, vmware-rhttpproxy
# vmware-sca, vmware-sps, vmware-statsmonitor, vmware-sts-idmd
# vmware-stsd, vmware-updatemgr, vmware-vapi-endpoint, vmware-vmon
# vmware-vpostgres, vmware-vpxd, vmware-vpxd-svcs, vmware-vsan-health
# vmware-vsm, vsphere-client, vsphere-ui

# Check disk space
shell
df -h
# Alert if any filesystem >80%

# Check NTP synchronization
ntpq -p
```

#### 1.2 Host Health Verification
```bash
# Via ESXi console or SSH
ssh root@esxi01.b2h.local

# Check hardware health
esxcli hardware platform get
esxcli hardware memory get

# Check storage
esxcli storage filesystem list
esxcli storage core device list

# Check networking
esxcli network ip interface list
esxcli network nic list

# Check VM status
esxcli vm process list
```

### 2. VM Provisioning Procedure

#### 2.1 New VM Request Form
```
VM Provisioning Request
━━━━━━━━━━━━━━━━━━━━━━━
Requester: [Name]
Date: [Date]
Project: [Project name]

VM Specifications:
├── VM Name: [B2H-VM-XXX format]
├── Purpose: [Description]
├── Operating System: [Windows Server 2022/CentOS/etc]
├── vCPUs: [Number]
├── RAM: [GB]
├── Storage: [GB]
├── Network: [VLAN 10/20/30/40]
├── Backup Required: [Yes/No]
└── Monitoring Required: [Yes/No]

Approval: [IT Manager signature]
```

#### 2.2 VM Deployment from Template
```bash
# Via PowerCLI (preferred for consistency)
Connect-VIServer vcenter.b2h.local -Credential (Get-Credential)

# Deploy VM from template
New-VM -Name "B2H-VM-NEW" `
  -Template "Template-Win2022-Base" `
  -VMHost "esxi01.b2h.local" `
  -Datastore "R760-Datastore-01" `
  -Location "B2H Production"

# Configure resources
Set-VM -VM "B2H-VM-NEW" -NumCpu 4 -MemoryGB 16 -Confirm:$false

# Add network adapter
New-NetworkAdapter -VM "B2H-VM-NEW" `
  -NetworkName "VLAN20-Production" `
  -Type Vmxnet3

# Start VM
Start-VM -VM "B2H-VM-NEW"

# Disconnect
Disconnect-VIServer -Confirm:$false
```

#### 2.3 VM Configuration Standards
| Parameter | Standard Value | Notes |
|-----------|----------------|-------|
| VMware Tools | Latest version | Auto-update enabled |
| Disk Format | Thin Provision | Monitor capacity |
| Network Adapter | VMXNET3 | Best performance |
| SCSI Controller | LSI Logic SAS/PVSCSI | PVSCSI for high I/O |
| BIOS Boot Delay | 5000ms | For console access |
| Snapshot Reserve | 20% | Auto-cleanup after 3 days |

#### 2.4 Post-Deployment Checklist
```bash
□ VM powers on successfully
□ VMware Tools starts and reports "Running"
□ Network connectivity verified (ping gateway)
□ DNS registration successful
□ Joined to domain (B2H.LOCAL)
□ Antivirus agent installed (Kaspersky)
□ Monitoring agent installed (Zabbix)
□ Backup job configured (Veeam)
□ Documentation updated
```

### 3. Resource Allocation Adjustments

#### 3.1 Capacity Monitoring
```bash
# Check cluster resources
Get-Cluster "B2H-Cluster" | Select-Object `
  Name, @{N="CPU GHz Total";E={[math]::Round($_.ExtensionData.Summary.TotalCpu/1000,2)}}, `
  @{N="CPU GHz Used";E={[math]::Round($_.ExtensionData.Summary.UsedCpu/1000,2)}}, `
  @{N="Memory GB Total";E={[math]::Round($_.ExtensionData.Summary.TotalMemory/1GB,2)}}, `
  @{N="Memory GB Used";E={[math]::Round($_.ExtensionData.Summary.UsedMemory/1GB,2)}}

# Check for resource contention
Get-VMHost | Get-VM | Where-Object {$_.PowerState -eq 'PoweredOn'} | `
  Select-Object Name, @{N="CPU Usage";E={$_.ExtensionData.Summary.QuickStats.OverallCpuUsage}}, `
  @{N="Memory Usage";E={$_.ExtensionData.Summary.QuickStats.GuestMemoryUsage}}
```

#### 3.2 Resource Adjustment Process
```bash
# Hot-add CPU (requires VM shutdown if not enabled)
Shutdown-VMGuest -VM "B2H-VM-XXX" -Confirm:$false
Start-Sleep -Seconds 120
Set-VM -VM "B2H-VM-XXX" -NumCpu 8 -Confirm:$false
Start-VM -VM "B2H-VM-XXX"

# Hot-add Memory (if guest OS supports)
Set-VM -VM "B2H-VM-XXX" -MemoryGB 32 -Confirm:$false

# Expand disk
Get-HardDisk -VM "B2H-VM-XXX" | Where-Object {$_.Name -eq "Hard disk 1"} | `
  Set-HardDisk -CapacityGB 200 -Confirm:$false

# Extend within OS (Windows)
diskpart
select volume C
extend
exit
```

#### 3.3 Resource Reservation Guidelines
| VM Type | CPU Reservation | Memory Reservation | Notes |
|---------|-----------------|-------------------|-------|
| Production DB | 2000 MHz | 100% | Critical workloads |
| Domain Controller | 1000 MHz | 50% | Auth services |
| Zabbix Server | 1500 MHz | 75% | Monitoring critical |
| General Purpose | None | None | Burstable |

### 4. Backup Verification

#### 4.1 Daily Backup Status Check
```bash
# Access Veeam Console
# Connect to: https://veeam.b2h.local:9398

# PowerShell verification
Add-PSSnapin VeeamPSSnapin

# Check job status
Get-VBRJob | Select-Object Name, JobState, LastState, LastResult

# Expected: LastResult = "Success" for all jobs
```

#### 4.2 Backup Verification Test (Monthly)
```bash
# Instant VM Recovery Test
# 1. Open Veeam Backup & Replication console
# 2. Select backup job → Right-click → Instant VM Recovery
# 3. Select restore point (verify multiple points available)
# 4. Restore to isolated test network (VLAN 999)
# 5. Verify VM boots successfully
# 6. Verify data integrity (check file hashes)
# 7. Finalize recovery (or discard test)

# File-Level Recovery Test
# 1. Select VM backup → Restore → Guest files
# 2. Mount backup as virtual drive
# 3. Extract test file to temp location
# 4. Verify file checksum matches expected
# 5. Dismount backup

# Application Item Recovery Test (if applicable)
# 1. For Active Directory: Test user object restore
# 2. For SQL: Test database table recovery
# 3. For Exchange: Test mailbox item recovery
```

#### 4.3 Backup Verification Report
```
Backup Verification Report
━━━━━━━━━━━━━━━━━━━━━━━━━━
Date: [Date]
Verified by: [Name]

VM Backups:
┌────────────────────┬──────────────┬──────────┬────────────┐
│ VM Name            │ Last Backup  │ Status   │ Verified   │
├────────────────────┼──────────────┼──────────┼────────────┤
│ B2H-SIGNIANT-01    │ 2026-03-22   │ Success  │ ✓ Yes      │
│ B2H-FANALYZER-01   │ 2026-03-22   │ Success  │ ✓ Yes      │
│ B2H-FORTIAUTH-01   │ 2026-03-22   │ Success  │ ✓ Yes      │
│ B2H-VAULT-01       │ 2026-03-22   │ Success  │ ✓ Yes      │
│ B2H-EMS-01         │ 2026-03-22   │ Success  │ ✓ Yes      │
│ B2H-KASPERSKY-01   │ 2026-03-22   │ Success  │ ✓ Yes      │
│ B2H-ZABBIX-01      │ 2026-03-22   │ Success  │ ✓ Yes      │
└────────────────────┴──────────────┴──────────┴────────────┘

Issues Found: [None/Details]
Remediation: [Actions taken]
```

### 5. Patch Management Schedule

#### 5.1 Monthly Patching Window
```
Patching Schedule (Second Sunday of each month)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
00:00 - 01:00: Pre-patching verification
01:00 - 01:30: VMware Tools updates
01:30 - 03:00: Guest OS updates
03:00 - 03:30: Application updates
03:30 - 04:00: Post-patching verification
04:00 - 06:00: Extended testing period
06:00: Production release
```

#### 5.2 VMware Tools Update
```bash
# Update VMware Tools on all VMs
Get-VMHost | Get-VM | Where-Object {$_.PowerState -eq 'PoweredOn'} | `
  Where-Object {$_.ExtensionData.Guest.ToolsVersionStatus -ne 'guestToolsCurrent'} | `
  Update-Tools -NoReboot -RunAsync

# Schedule automatic upgrade
Get-VM | Set-VM -ToolsUpgradePolicy "UpgradeAtPowerCycle"
```

#### 5.3 Guest OS Patching (Windows)
```powershell
# Windows Update via PowerShell
# Run on each VM

# Check available updates
Install-Module PSWindowsUpdate -Force
Get-WUList

# Install all critical and security updates
Get-WUInstall -AcceptAll -AutoReboot

# Verify installed
Get-WUHistory | Select-Object -First 10
```

#### 5.4 Guest OS Patching (Linux)
```bash
# CentOS/RHEL
sudo yum update -y
sudo reboot

# Ubuntu
sudo apt update
sudo apt upgrade -y
sudo reboot

# Post-reboot verification
uname -r  # Verify new kernel
systemctl status [critical-services]
```

#### 5.5 Emergency Patching (Zero-Day)
```
Zero-Day Response Procedure:
━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Receive security advisory (CVE notification)
2. Assess applicability to B2H infrastructure
3. IT Manager approval for emergency patching
4. Schedule emergency maintenance window
5. Take VM snapshot before patching
6. Apply patch
7. Verify functionality
8. Remove snapshot after 48 hours stable
9. Document in change log
```

## Verification
| Check | Command/Method | Expected Result |
|-------|----------------|-----------------|
| vCenter Status | vSphere Client | All hosts connected, green status |
| VM Tools | `Get-VM | Get-VMGuest` | All "Running", "Current" version |
| Datastore Space | vSphere Client | <80% utilized |
| Backup Jobs | Veeam Console | All "Success" last run |
| Host Uptime | `uptime` | Since last planned maintenance |

## Rollback
If patch causes issues:
1. Revert to snapshot taken before patching
2. Document failure for next patch cycle
3. Contact vendor for remediation
4. Update exclude list if necessary

## Escalation Matrix
| Severity | Contact | Response Time |
|----------|---------|---------------|
| P1 - Critical (VM outage) | System Admin: +91-XXXXXXXXXX | 15 minutes |
| P2 - High (Performance issue) | Senior System Admin: +91-XXXXXXXXXX | 1 hour |
| P3 - Medium (Patch failure) | System Admin | 4 hours |
| VMware Support | support.vmware.com | 1 hour (P1) |

## Related Documents
- SOP-005: Backup Operations
- SOP-009: Change Management
- Part2_Enhanced_Network_Wireless_Server.md (Section 6)

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 22-Mar-2026 | VConfi | Initial release |

---

# SOP-004: Storage Administration

## Purpose
To establish standardized procedures for three-tier storage management including daily health checks, capacity monitoring, snapshot management, replication verification, and performance optimization for B2H Studios' Synology infrastructure.

## Scope
This SOP covers:
- Hot Tier: Synology RS2423RP+ HA (30TB)
- Warm Tier: Synology RS4021xs+ (468TB)
- Cold Tier: Wasabi Hot Cloud integration
- Snapshot management and retention
- Replication health monitoring

## Responsibility
| Role | Responsibility |
|------|----------------|
| Storage Administrator | Daily checks, snapshot management |
| Senior Storage Admin | Capacity planning, performance tuning |
| IT Manager | Budget approval for capacity expansion |

## Prerequisites
- DSM administrative access (https://10.10.30.10:5001)
- SSH access to Synology devices
- Understanding of BTRFS and RAID concepts
- Access to Wasabi cloud console

## Procedure

### 1. Hot Tier Daily Checks

#### 1.1 RS2423RP+ Health Verification
```bash
# SSH to primary NAS
ssh admin@10.10.30.10

# Check overall system status
synohealthcheck

# Check RAID status (should be "Healthy")
cat /proc/mdstat
# Expected: [UU] for all arrays

# Check disk health
smartctl -a /dev/sda  # Repeat for sdb, sdc, etc.
# Look for: "PASSED" in SMART status

# Check NVMe cache (if applicable)
nvme smart-log /dev/nvme0n1

# Check system temperature
sensors
# Alert if >45°C sustained

# Check memory usage
free -h
```

#### 1.2 Volume and Share Status
```bash
# Check volume usage
synofshare --enum

# Check BTRFS filesystem
btrfs filesystem df /volume1
btrfs filesystem show

# Check for errors
btrfs device stats /volume1
# All values should be 0
```

#### 1.3 High Availability Status
```bash
# Check HA cluster status
synoha --status

# Expected output:
# Status: Normal
# Role: Primary/Secondary
# Heartbeat: Connected
# Data Sync: Synchronized

# Check sync status
synoha --show
```

### 2. Warm Tier Capacity Monitoring

#### 2.1 RS4021xs+ Daily Checks
```bash
# SSH to warm tier NAS
ssh admin@10.10.30.20

# Check storage pools
synospace --meta -s

# Volume capacity check
synofshare --enum

# Expected thresholds:
# Warning: 75% full
# Critical: 85% full
# Emergency: 90% full
```

#### 2.2 Capacity Trend Analysis
```bash
# Historical usage (requires SNMP or API)
# Or manually log daily:

df -h >> /var/log/capacity-$(date +%Y%m).log

# Calculate daily growth rate
grep "volume1" /var/log/capacity-202603.log | \
  awk '{print $5}' | sed 's/%//' | \
  awk 'NR>1{print $1-p} {p=$1}'
```

#### 2.3 Capacity Planning Triggers
| Capacity Level | Action | Timeline |
|----------------|--------|----------|
| 70% | Monitor closely | Daily checks |
| 75% | Initiate capacity review | 1 week |
| 80% | Order expansion hardware | Immediate |
| 85% | Emergency expansion | Immediate |
| 90% | Critical - stop new projects | Immediate |

### 3. Snapshot Management

#### 3.1 Snapshot Schedule Verification
```bash
# Check snapshot schedules
synoreplicatool --list-local

# Verify retention policies
synoreplicatool --list-local --detail

# Expected schedules:
# - Every 2 hours (24 snapshots)
# - Daily at 00:00 (30 days)
# - Monthly at 1st (12 months)
```

#### 3.2 Snapshot Lock Verification
```bash
# List locked snapshots
synoreplicatool --list-local --locked

# Verify WORM compliance
# Locked snapshots should show:
# - Lock status: Locked
# - Retention: 7 years for deliverables
# - Cannot be deleted by admin
```

#### 3.3 Manual Snapshot Creation
```bash
# Create manual snapshot (before major changes)
synoreplicatool --create --name "pre-migration-$(date +%Y%m%d)"

# Lock snapshot for compliance
synoreplicatool --lock --id [snapshot_id] --retention 2555  # 7 years in days

# Verify lock applied
synoreplicatool --list-local --detail | grep -A5 [snapshot_name]
```

#### 3.4 Snapshot Cleanup (Non-Locked)
```bash
# List deletable snapshots
synoreplicatool --list-local --unlocked

# Delete specific snapshot (with confirmation)
synoreplicatool --delete --id [snapshot_id]

# Automatic cleanup per retention policy runs at 02:00 daily
```

### 4. Replication Health Verification

#### 4.1 RTRR (Real-Time Remote Replication) Check
```bash
# Check replication status
synoreplog --status

# Expected output:
# Status: Idle/Running
# Last Sync: [within 15 minutes]
# Errors: 0

# List recent replication logs
synoreplog --list --limit 10

# Check for errors
synoreplog --list | grep -i error
```

#### 4.2 Replication Performance Check
```bash
# Current replication throughput
synoreplog --detail --id [last_sync_id]

# Check for throttling
synoreplog --config
# Should show: throttle = off or configured limit
```

#### 4.3 Manual Replication Sync
```bash
# Force immediate sync (if needed)
synoreplicatool --sync-now --target [site_b_ip]

# Monitor progress
watch -n 5 'synoreplog --status'

# Cancel if running too long (maintenance window)
synoreplicatool --pause --target [site_b_ip]
```

### 5. Performance Monitoring

#### 5.1 IOPS and Latency Monitoring
```bash
# Check disk I/O statistics
iostat -x 5 3

# Look for:
# - %util < 80% (good)
# - await < 20ms (acceptable for HDD)
# - svctm < 10ms (good)

# Check network I/O (for NFS/SMB)
sar -n DEV 5 3
```

#### 5.2 SMB/NFS Performance
```bash
# Check current connections
smbstatus -S

# NFS exports and clients
showmount -a

# Check for connection limits
cat /proc/sys/net/core/somaxconn
```

#### 5.3 Cache Performance (NVMe SSD)
```bash
# Check SSD cache hit ratio
cat /proc/sys/fs/ssd_cache/stats

# If hit ratio < 80%, consider:
# - Expanding cache
# - Reviewing workload patterns
# - Adjusting cache policies
```

### 6. Cloud Tiering (Hybrid Share)

#### 6.1 Wasabi Sync Status
```bash
# Check cloud sync status
synocloudsync --status

# Verify bucket connectivity
synocloudsync --test-connection

# Check pending uploads
synocloudsync --queue
```

#### 6.2 Tiering Policy Verification
```bash
# Check file tiering status
synohacheck --verbose

# Files should tier after 90 days of inactivity
# Hot files (pinned) should remain local
```

## Verification
| Check | Command | Expected Result |
|-------|---------|-----------------|
| RAID Status | `cat /proc/mdstat` | [UU] all disks |
| Volume Health | `synohealthcheck` | "Healthy" |
| Replication | `synoreplog --status` | "Idle" or "Synced <15 min" |
| Snapshots | `synoreplicatool --list-local` | Expected count |
| Temperature | `sensors` | <45°C |

## Rollback
If snapshot restore needed:
```bash
# List available snapshots
synoreplicatool --list-local

# Restore from snapshot
synoreplicatool --restore --id [snapshot_id] --target [path]

# Verify restore
ls -la [path]
```

## Escalation Matrix
| Severity | Contact | Response Time |
|----------|---------|---------------|
| P1 - Critical (NAS down) | Storage Admin: +91-XXXXXXXXXX | 15 minutes |
| P2 - High (Degraded RAID) | Senior Storage Admin: +91-XXXXXXXXXX | 1 hour |
| P3 - Medium (Capacity >80%) | Storage Admin | 4 hours |
| Synology Support | support.synology.com | 4 hours |

## Related Documents
- SOP-005: Backup Operations
- SOP-006: Disaster Recovery
- Design_Decisions.md (Storage Architecture)

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 22-Mar-2026 | VConfi | Initial release |

---

# SOP-005: Backup Operations

## Purpose
To establish standardized procedures for backup verification, testing, air-gap operations, retention management, and remediation of failed backups to ensure B2H Studios' 3-2-1-1-0 backup strategy compliance.

## Scope
This SOP covers:
- Daily backup verification
- Weekly test restores
- Monthly air-gap backup procedure (LTO-9 tape)
- Backup retention management
- Failed backup remediation

## Responsibility
| Role | Responsibility |
|------|----------------|
| Backup Administrator | Daily verification, tape operations |
| Storage Administrator | Snapshot management |
| IT Manager | Offsite tape management, audit compliance |

## Prerequisites
- Access to Veeam Backup & Replication console
- Access to Synology DSM
- LTO-9 tape drive and tapes
- Access to fireproof safe and bank vault
- LTO barcode scanner (recommended)

## Procedure

### 1. Daily Backup Verification

#### 1.1 Morning Verification Checklist (09:00 AM)
```bash
# Access Veeam Console
# https://veeam.b2h.local:9398

# Check all job status
Get-VBRJob | Select-Object Name, JobType, ScheduleEnabled, LastResult, LastState

# Expected Results:
# LastResult = "Success" or "Warning" (investigate warnings)
# LastState = "Idle" or "Running"
```

#### 1.2 Backup Job Status Review
```
Daily Backup Status Review
━━━━━━━━━━━━━━━━━━━━━━━━━━
Date: ___________
Verified by: ___________

Veeam Backup Jobs:
┌─────────────────────┬──────────────┬──────────┬──────────┐
│ Job Name            │ Last Run     │ Duration │ Status   │
├─────────────────────┼──────────────┼──────────┼──────────┤
│ VM-Backup-Daily     │ ___________ │ ________ │ [ ] Pass │
│ VM-Backup-Weekly    │ ___________ │ ________ │ [ ] Pass │
│ Config-Backup       │ ___________ │ ________ │ [ ] Pass │
└─────────────────────┴──────────────┴──────────┴──────────┘

Synology Snapshots:
┌─────────────────────┬──────────────┬──────────┐
│ Snapshot Type       │ Last Created │ Count    │
├─────────────────────┼──────────────┼──────────┤
│ Hourly (2hr)        │ ___________ │ ____     │
│ Daily               │ ___________ │ ____     │
│ Monthly             │ ___________ │ ____     │
└─────────────────────┴──────────────┴──────────┘

Wasabi Cloud Sync:
┌─────────────────────┬──────────────┬──────────┐
│ Sync Job            │ Last Sync    │ Status   │
├─────────────────────┼──────────────┼──────────┤
│ Hot-Tier-Archive    │ ___________ │ [ ] Pass │
│ Warm-Tier-Archive   │ ___________ │ [ ] Pass │
└─────────────────────┴──────────────┴──────────┘

Issues: ___________________________________________
Actions: __________________________________________
```

#### 1.3 Verification Commands
```bash
# Check Veeam session details
Get-VBRBackupSession | Where-Object {$_.CreationTime -gt (Get-Date).AddDays(-1)} | `
  Select-Object JobName, Result, CreationTime, EndTime

# Verify backup file integrity (check for corruption)
Get-VBRBackup | ForEach-Object {
    $backup = $_
    $file = $backup.GetAllStorages() | Select-Object -First 1
    if ($file) {
        "Backup: $($backup.Name) - File: $($file.PartialPath)"
        "Size: $([math]::Round($file.Stats.BackupSize/1GB,2)) GB"
    }
}
```

### 2. Weekly Backup Test Restore

#### 2.1 Test Restore Schedule
```
Weekly Test Restore Rotation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Week 1: Zabbix Server VM
Week 2: FortiAnalyzer VM
Week 3: Random production file restore
Week 4: Disaster Recovery drill (monthly)
```

#### 2.2 VM Instant Recovery Test
```bash
# PowerShell via Veeam console
Add-PSSnapin VeeamPSSnapin

# Select backup and restore point
$backup = Get-VBRBackup -Name "VM-Backup-Daily"
$restorePoint = Get-VBRRestorePoint -Backup $backup | Sort-Object -Property CreationTime -Descending | Select-Object -First 1

# Perform Instant VM Recovery to isolated network
Start-VBRInstantRecovery -RestorePoint $restorePoint `
  -Server (Get-VBRServer -Name "esxi01.b2h.local") `
  -ResourcePool "Test-Recovery" `
  -VMName "TEST-RESTORE-$($restorePoint.VmName)" `
  -PowerUp $true

# Wait for VM to boot (5 minutes)
Start-Sleep -Seconds 300

# Test connectivity
Test-Connection -ComputerName "TEST-RESTORE-$($restorePoint.VmName)" -Count 4

# Verify services (customize per VM type)
# For Zabbix: Test web interface
Invoke-WebRequest -Uri "http://TEST-RESTORE-ZABBIX-01/zabbix"
```

#### 2.3 File-Level Restore Test
```bash
# From Veeam console:
# 1. Select backup → Restore → Guest files
# 2. Choose restore point (verify multiple available)
# 3. Mount backup as virtual drive
# 4. Select test file(s) to restore

# Generate checksum of original file (weekly)
sha256sum /volume1/projects/testfile.bin > /var/log/checksums-$(date +%Y%m%d).txt

# After restore, compare checksum
sha256sum /temp/restore/testfile.bin
diff /var/log/checksums-$(date +%Y%m%d).txt /temp/restore/checksum.txt

# Result should match exactly
```

#### 2.4 Test Restore Documentation
```
Test Restore Report
━━━━━━━━━━━━━━━━━━━
Date: ___________
Performed by: ___________

Test Type: [ ] VM Instant Recovery  [ ] File Restore  [ ] Application

Source: _________________________________
Restore Point: __________________________

Test Steps:
[ ] 1. Initiated restore at: _______
[ ] 2. Restore completed at: _______
[ ] 3. VM powered on: [ ] Yes  [ ] No
[ ] 4. Network connectivity verified: [ ] Yes  [ ] No
[ ] 5. Services started: [ ] Yes  [ ] No
[ ] 6. Data integrity verified: [ ] Yes  [ ] No

Results:
Duration: _______
Status: [ ] Pass  [ ] Fail

Issues: ___________________________________________
Remediation: _______________________________________

Finalized: [ ] Yes  Discarded: [ ] Yes
Verified by: ___________
```

### 3. Monthly Air-Gap Backup Procedure

#### 3.1 Pre-Backup Preparation
```
Air-Gap Backup Checklist (Monthly - 1st Sunday)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
□ Maintenance window confirmed (scheduled 8 hours)
□ LTO-9 tape library checked and cleaned
□ Blank tape(s) prepared and labeled: B2H-AG-[YYYYMM]
□ Fireproof safe opened and accessible
□ Previous month tape ready for bank vault rotation
□ Staff availability confirmed (2 people recommended)
```

#### 3.2 Air-Gap Backup Procedure
```bash
# STEP 1: Connect LTO Drive (09:00 AM)
# Physically connect LTO-9 drive to RS4021xs+ (warm tier)
# Power on drive, wait for ready status (green LED)

# Verify drive detection
lsscsi | grep tape
# Expected: [x:y:z:w]  tape    IBM      ULTRIUM-HH9 ...

# STEP 2: Initialize Tape (09:15 AM)
# Insert blank tape
mt -f /dev/st0 status

# Format tape (if new)
mt -f /dev/st0 rewind

# STEP 3: Perform Full Backup (09:30 AM - ~4 hours)
# Mount backup share
mkdir -p /mnt/backup-target

# Create tar archive with checksum
 tar -cvf /dev/st0 \
  --exclude='*.tmp' \
  --exclude='cache' \
  --exclude='@snapshot' \
  /volume1/projects/ \
  /volume1/deliverables/ \
  2>&1 | tee /var/log/airgap-$(date +%Y%m%d).log

# Alternative: Use Synology Hyper Backup
# Create backup task: "Monthly-AirGap"
# Target: USB/LTO Device
# Files: /volume1/projects, /volume1/deliverables
# Encryption: Yes (AES-256)

# STEP 4: Verify Backup (13:30 PM - ~1 hour)
# Rewind and verify
dd if=/dev/st0 of=/dev/null bs=1M count=100

# Check for read errors
dmesg | tail -20

# Generate tape checksum
sha256sum /dev/st0 > /var/log/tape-checksum-$(date +%Y%m%d).txt

# Compare file count
# Count source files
find /volume1/projects -type f | wc -l > /var/log/source-count.txt

# Count archived files (via tar -t)
tar -tvf /dev/st0 | wc -l > /var/log/archive-count.txt

# Compare counts
diff /var/log/source-count.txt /var/log/archive-count.txt

# STEP 5: Create Tape Index (14:30 PM)
tar -tvf /dev/st0 > /var/log/tape-index-$(date +%Y%m%d).txt

# Copy index to multiple locations
cp /var/log/tape-index-$(date +%Y%m%d).txt /volume1/tape-inventory/
cp /var/log/tape-index-$(date +%Y%m%d).txt /volumeUSB/tape-indexes/

# STEP 6: Physical Disconnection (CRITICAL - 15:00 PM)
# Eject tape
eject /dev/st0

# Physically disconnect LTO drive from NAS
# Store cable in secure location
# Update asset tracking: Drive status = "Disconnected"

# STEP 7: Tape Storage (15:15 PM)
# Label tape: B2H-AG-[YYYYMM]
# Place in anti-static case
# Store in fireproof safe at primary site
# Update tape inventory log

echo "$(date '+%Y-%m-%d %H:%M:%S'),B2H-AG-$(date +%Y%m),Fireproof-Safe,Monthly-Backup" \
  >> /volume1/admin/tape-inventory.csv

# STEP 8: Quarterly Bank Vault Rotation
# If quarter-end:
# - Retrieve tape from 3 months ago (B2H-AG-[YYYY-3M])
# - Transport to bank vault
# - Retrieve oldest vault tape for destruction/reuse
# - Update chain of custody log
```

#### 3.3 Air-Gap Backup Verification
```bash
# Monthly verification commands

# Verify drive disconnected
lsscsi | grep tape
# Should return nothing

# Verify tape catalog exists
ls -la /volume1/tape-inventory/tape-index-$(date +%Y%m --date='last month')*.txt

# Verify checksum files
cat /var/log/tape-checksum-$(date +%Y%m --date='last month').txt

# Update air-gap compliance report
cat > /volume1/admin/airgap-compliance-$(date +%Y%m).txt << EOF
Air-Gap Backup Compliance Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Period: $(date +%B-%Y)
Generated: $(date)

Backup Status: COMPLETED
Tape Label: B2H-AG-$(date +%Y%m)
Backup Size: $(du -sh /volume1/projects /volume1/deliverables | awk '{sum+=$1} END {print sum}')
Verification: PASSED
Tape Location: Fireproof Safe
Drive Status: DISCONNECTED

Retention: 7 Years (Per ISO 27001)
Next Tape Rotation: $(date -d '+3 months' +%B-%Y)

Signed: ____________________
Date: ____________________
EOF
```

### 4. Backup Retention Management

#### 4.1 Retention Policy Enforcement
```
Backup Retention Matrix
━━━━━━━━━━━━━━━━━━━━━━━
Backup Type          Retention    Media        Location
─────────────────────────────────────────────────────────
VM Daily Backups     30 days      Disk (Veeam) Site A
VM Weekly Backups    12 weeks     Disk (Veeam) Site A, B
VM Monthly Backups   12 months    Disk (Veeam) Site A, B
Snapshots (Hourly)   48 hours     BTRFS        Site A
Snapshots (Daily)    30 days      BTRFS        Site A, B
Snapshots (Monthly)  12 months    BTRFS        Site A
LTO Air-Gap          7 years      Tape         Bank Vault
Cloud (Wasabi)       7 years      Object       Wasabi
```

#### 4.2 Automated Cleanup Verification
```bash
# Check Veeam retention cleanup
Get-VBRBackup | ForEach-Object {
    $backup = $_
    $sessions = Get-VBRBackupSession -Backup $backup
    $restorePoints = Get-VBRRestorePoint -Backup $backup
    Write-Host "$($backup.Name): $($restorePoints.Count) restore points"
}

# Check Synology snapshot retention
synoreplicatool --list-local | grep -c "snapshot"

# Verify count matches retention policy
```

### 5. Failed Backup Remediation

#### 5.1 Failure Classification and Response
| Failure Type | Symptoms | Response Time | Action |
|--------------|----------|---------------|--------|
| Transient | Network timeout | Immediate | Retry job |
| Storage | Disk full | 1 hour | Free space/expand |
| Permission | Access denied | 30 min | Fix credentials |
| Corruption | Checksum fail | 2 hours | New full backup |
| Hardware | Drive failure | 4 hours | Replace hardware |

#### 5.2 Remediation Procedure
```bash
# STEP 1: Identify failure cause
# Check Veeam logs
cat "C:\ProgramData\Veeam\Backup\[JobName]\Job.[JobName].log" | Select-String -Pattern "Error"

# Check Synology logs
synolog --show | grep -i error
cat /var/log/synoreplog.log | tail -50

# STEP 2: Common fixes

# Fix 1: Retry job (transient issues)
Start-VBRJob -Job "VM-Backup-Daily" -RetryBackup

# Fix 2: Free up storage space
# Delete old temporary files
find /volume1/@tmp -type f -mtime +7 -delete

# Expand volume if needed (requires unallocated space)
# DSM → Storage Manager → Storage Pool → Action → Expand

# Fix 3: Restart services
# Veeam
Restart-Service -Name "VeeamBackupSvc"
Restart-Service -Name "VeeamBrokerSvc"

# Synology
synoservice --restart pkgctl-HyperBackup

# Fix 4: Repair backup chain (corruption)
# Veeam: Right-click backup → Properties → Maintenance → Quick Backup Verification
# Then run Active Full backup if needed

# STEP 3: Run test backup
Start-VBRJob -Job "VM-Backup-Daily" -FullBackup

# Monitor until completion
while ((Get-VBRJob -Name "VM-Backup-Daily").LastState -eq "Working") {
    Start-Sleep -Seconds 60
    Write-Host "Backup in progress..."
}

# Verify success
Get-VBRJob -Name "VM-Backup-Daily" | Select-Object LastResult
```

#### 5.3 Post-Remediation Documentation
```
Backup Failure Report
━━━━━━━━━━━━━━━━━━━━━━
Date/Time: ___________
Reported by: ___________

Failure Details:
Job Name: _________________________________
Failure Time: ___________
Error Message: ____________________________
__________________________________________

Root Cause: [ ] Transient  [ ] Storage  [ ] Permission
            [ ] Corruption  [ ] Hardware  [ ] Other: ____

Remediation:
[ ] Issue identified
[ ] Fix applied: __________________________
[ ] Backup retried
[ ] Backup completed successfully

Prevention:
__________________________________________

Verified by: ___________ Date: ___________
```

## Verification
| Check | Method | Expected Result |
|-------|--------|-----------------|
| Daily Backup | Veeam Console | All jobs "Success" |
| Weekly Test | Restore Report | All tests "Pass" |
| Air-Gap Tape | Physical check | Labeled, in safe |
| Drive Status | lsscsi | Not connected |
| Retention | Restore point count | Matches policy |

## Rollback
If backup corruption detected:
1. Isolate affected backup chain
2. Initiate new full backup immediately
3. Verify new backup integrity
4. Document for audit trail

## Escalation Matrix
| Severity | Contact | Response Time |
|----------|---------|---------------|
| P1 - Critical (All backups failing) | Backup Admin: +91-XXXXXXXXXX | 15 minutes |
| P2 - High (Single job failure) | Storage Admin: +91-XXXXXXXXXX | 1 hour |
| P3 - Medium (Warning state) | Backup Admin | 4 hours |
| Veeam Support | support.veeam.com | 4 hours |

## Related Documents
- SOP-004: Storage Administration
- SOP-006: Disaster Recovery
- Design_Decisions.md (Backup Strategy)

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 22-Mar-2026 | VConfi | Initial release |

---

# SOP-006: Disaster Recovery

## Purpose
To establish standardized procedures for DR site readiness checks, failover execution, and failback operations to ensure B2H Studios can achieve RTO of 10 minutes and RPO of 15 minutes as per business requirements.

## Scope
This SOP covers:
- DR site readiness verification
- Failover decision tree and procedures
- Hot tier failover (<30 seconds)
- Warm tier failover (10 minutes)
- Complete site failover
- Failback procedures

## Responsibility
| Role | Responsibility |
|------|----------------|
| DR Coordinator | Overall DR execution, stakeholder communication |
| Network Administrator | Network failover, VPN/ZTNA updates |
| Storage Administrator | NAS promotion, replication management |
| System Administrator | VM startup, service verification |
| IT Manager | Decision authority for failover declaration |

## Prerequisites
- VPN/ZTNA access to Site B
- Administrative access to all Site B systems
- DR runbook printed and accessible offline
- Current contact list with phone tree
- Pre-staged credentials in sealed envelope (CISO safe)

## Procedure

### 1. DR Site Readiness Checks

#### 1.1 Daily Readiness Verification (Automated)
```bash
# Script: /opt/dr-scripts/daily-readiness-check.sh

#!/bin/bash
# Daily DR Readiness Check Script

REPORT="/var/log/dr-readiness-$(date +%Y%m%d).log"
echo "=== DR Readiness Check: $(date) ===" > $REPORT

# Check 1: Site B NAS accessibility
echo -n "Site B NAS: " >> $REPORT
if ping -c 3 10.10.30.110 > /dev/null 2>&1; then
    echo "REACHABLE" >> $REPORT
else
    echo "UNREACHABLE" >> $REPORT
fi

# Check 2: Replication status
echo -n "Replication Lag: " >> $REPORT
ssh admin@10.10.30.10 "synoreplog --status" >> $REPORT 2>&1

# Check 3: Site B VMs status
echo -n "Site B vCenter: " >> $REPORT
if curl -sk https://10.10.40.111/sdk > /dev/null 2>&1; then
    echo "REACHABLE" >> $REPORT
else
    echo "UNREACHABLE" >> $REPORT
fi

# Check 4: Site B FortiGate
echo -n "Site B FortiGate: " >> $REPORT
if ping -c 3 10.10.40.112 > /dev/null 2>&1; then
    echo "REACHABLE" >> $REPORT
else
    echo "UNREACHABLE" >> $REPORT
fi

# Email report
cat $REPORT | mail -s "DR Readiness Check $(date +%Y-%m-%d)" admin@b2h.local
```

#### 1.2 Weekly Manual Verification
```
Weekly DR Readiness Checklist
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Week of: ___________
Verified by: ___________

Site B Infrastructure:
[ ] NAS accessible (DSM login successful)
[ ] Replication lag <15 minutes
[ ] Available capacity >30%
[ ] No hardware alarms

Site B Network:
[ ] FortiGate accessible
[ ] WAN links operational (both ISPs)
[ ] VSX stack synchronized
[ ] ZTNA gateway responding

Site B Compute:
[ ] ESXi host responding
[ ] DR VMs powered off (standby mode)
[ ] Sufficient resources for failover
[ ] vCenter accessible

Documentation:
[ ] Contact list current
[ ] Procedures accessible
[ ] Credentials accessible (CISO)
[ ] Vendor contacts confirmed

Issues: ___________________________________________
Actions: __________________________________________
```

### 2. Failover Decision Tree

```
Incident Detected at Site A
━━━━━━━━━━━━━━━━━━━━━━━━━━

                    ┌─────────────────────┐
                    │   Site A Incident   │
                    │      Detected       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Severity Assessment│
                    └──────────┬──────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
    ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
    │    Minor     │   │    Major     │   │   Critical   │
    │ Single Service│   │ Multi-Service│   │Complete Site │
    └──────┬───────┘   └──────┬───────┘   └──────┬───────┘
           │                  │                   │
           ▼                  ▼                   ▼
    ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
    │  Wait for    │   │  Verify Site │   │ Immediate    │
    │  Recovery    │   │  A Status    │   │ Assessment   │
    │  (Monitor)   │   │  (5 min)     │   │ (2 min)      │
    └──────┬───────┘   └──────┬───────┘   └──────┬───────┘
           │                  │                   │
           │                  ▼                   │
           │         ┌──────────────┐            │
           │         │ False Alarm? │            │
           │         └──────┬───────┘            │
           │                │                     │
           │       ┌────────┴────────┐            │
           │       │                 │            │
           │       ▼                 ▼            │
           │  ┌──────────┐    ┌──────────┐        │
           │  │   Yes    │    │    No    │◄───────┘
           │  │ Return   │    │          │
           │  │ Normal   │    │          │
           │  └──────────┘    └────┬─────┘
           │                       │
           │                       ▼
           │              ┌─────────────────────┐
           │              │  DECLARE DISASTER   │
           │              │ (IT Manager Auth)   │
           │              └──────────┬──────────┘
           │                         │
           │                         ▼
           │              ┌─────────────────────┐
           │              │  INITIATE FAILOVER  │
           │              └─────────────────────┘
           │                         │
           └─────────────────────────┘
```

### 3. Hot Tier Failover Procedure (<30 seconds)

#### 3.1 RS2423RP+ HA Failover
```bash
# Automatic failover if primary fails
# Manual trigger procedure:

# SSH to secondary NAS
ssh admin@10.10.30.11  # Site A secondary

# Check current role
synoha --status
# If showing "Secondary", proceed:

# Force takeover (emergency only)
synoha --takeover

# Verify takeover
synoha --status
# Expected: "Primary"

# Verify services
synofshare --enum
cat /proc/mdstat

# Update monitoring
# Notify team of manual intervention
```

#### 3.2 Verification After Hot Failover
```bash
# Connectivity test
ping 10.10.30.10  # Virtual IP should respond

# Service test
smbclient -L //10.10.30.10 -N
showmount -e 10.10.30.10

# Performance test
dd if=/dev/zero of=/volume1/test-$(date +%s).bin bs=1M count=100
rm /volume1/test-*.bin
```

### 4. Warm Tier Failover Procedure (10 minutes)

#### 4.1 Site B NAS Promotion
```bash
# STEP 1: Pause Replication (0:00)
# On Site B NAS
synoreplicatool --pause --target site_a_ip

# STEP 2: Verify Last Sync (0:02)
synoreplog --last-sync
# Note timestamp for RPO calculation

# STEP 3: Promote Replica to Primary (0:03)
synoreplicatool --promote --share Projects
synoreplicatool --promote --share Deliverables

# STEP 4: Verify Promotion (0:05)
synofshare --enum
# Shares should show as Read-Write

# STEP 5: Update Share Permissions (0:07)
synoacltool -get /volume1/Projects
# Verify user/group permissions intact

# STEP 6: Enable Services (0:08)
synoservice --start pkgctl-NFS
synoservice --start pkgctl-SMBService

# STEP 7: Test Access (0:10)
smbclient -L //10.10.30.110 -N
showmount -e 10.10.30.110
```

### 5. Complete Site Failover Procedure (10 minutes)

#### 5.1 Failover Execution Timeline
```
Complete Site Failover Runbook
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RTO Target: 10 minutes

Minute  Action                              Responsible        Verification
────────────────────────────────────────────────────────────────────────────
0:00    Declare disaster, page team          IT Manager         Team assembled
0:01    Pause replication to Site B          Storage Admin      synoreplog --pause
0:02    Verify Site A unavailable            Network Admin      Ping/telnet fail
0:03    Convene incident team                DR Coordinator     All roles present
0:04    Promote Site B NAS to primary        Storage Admin      RW access confirmed
0:05    Update ZTNA profiles                 Network Admin      FortiClient redirected
0:06    Start DR VMs                         System Admin       VMs powered on
0:07    Update DNS/ZTNA records              Network Admin      nslookup confirms
0:08    Verify services online               System Admin       All green status
0:09    Notify employees                     DR Coordinator     Email/Slack sent
0:10    Production resumed                   DR Coordinator     Monitoring green
────────────────────────────────────────────────────────────────────────────
```

#### 5.2 Detailed Failover Steps
```bash
# STEP 1: Site B NAS Promotion (Minutes 1-4)
# (As detailed in section 4.1)

# STEP 2: ZTNA Profile Update (Minutes 5-7)
# Via FortiGate CLI or GUI

config system ztna
    edit "ZTNA-NAS-Access"
        set primary-gateway "10.10.40.112"  # Site B
        set secondary-gateway "10.10.40.12" # Site A (down)
    next
end

# Or via FortiClient EMS
# Update endpoint profiles to use Site B gateway

# STEP 3: VM Startup (Minutes 6-8)
# Via PowerCLI
Connect-VIServer vcenter-siteb.b2h.local

$drVMs = @("B2H-ZABBIX-02", "B2H-FANALYZER-02")
foreach ($vm in $drVMs) {
    Start-VM -VM $vm -RunAsync
}

# Wait for VMware Tools
Start-Sleep -Seconds 120

# Verify VM health
Get-VM | Where-Object {$_.PowerState -eq 'PoweredOn'} | `
    Select-Object Name, @{N="ToolsStatus";E={$_.Guest.ToolsStatus}}

# STEP 4: Service Verification (Minutes 8-10)
# Test critical services

# Zabbix
curl -s http://10.10.40.115/zabbix | grep -q "Zabbix" && echo "OK" || echo "FAIL"

# DNS resolution
nslookup nas.b2h.local

# SMB access
smbclient -L //10.10.30.110 -N
```

### 6. Failback Procedures

#### 6.1 Failback Decision
```
Failback Decision Criteria
━━━━━━━━━━━━━━━━━━━━━━━━━━
Do NOT fail back if:
- Site A status uncertain
- Data divergence suspected
- Network instability persists
- Less than 4 hours on Site B

DO fail back when:
- Site A fully operational (confirmed)
- All services tested and verified
- Maintenance window available (after hours)
- Data sync completed
```

#### 6.2 Failback Execution
```bash
# STEP 1: Pre-Failback Checks (Day before)
# Verify Site A operational
ssh admin@site-a-nas "synohealthcheck"
ping -c 4 site-a-firewall

# STEP 2: Sync Data from Site B to Site A (Hours 1-4)
# Reverse replication direction

# On Site A NAS (now secondary)
synoreplicatool --add --source site_b_ip --target /volume1/Projects

# Initial sync will take hours depending on change volume
# Monitor progress:
watch -n 30 'synoreplog --status'

# STEP 3: Verify Data Consistency (Hour 5)
# Compare file counts and sizes
ssh admin@site-a-nas "du -sh /volume1/Projects"
ssh admin@site-b-nas "du -sh /volume1/Projects"

# STEP 4: Schedule Maintenance Window (Hour 6)
# Notify users of brief outage
# Schedule during low-activity period

# STEP 5: Execute Failback (Maintenance Window)
# 5a. Stop services on Site B
synoreplicatool --pause --target site_a_ip
synoservice --stop pkgctl-NFS
synoservice --stop pkgctl-SMBService

# 5b. Final sync
synoreplicatool --sync-now --target site_a_ip

# 5c. Promote Site A back to primary
ssh admin@site-a-nas "synoreplicatool --promote --share Projects"

# 5d. Update ZTNA back to Site A
config system ztna
    edit "ZTNA-NAS-Access"
        set primary-gateway "10.10.40.12"  # Site A
        set secondary-gateway "10.10.40.112" # Site B
    next
end

# 5e. Restart services on Site A
ssh admin@site-a-nas "synoservice --start pkgctl-NFS"

# 5f. Test and verify
smbclient -L //10.10.30.10 -N

# 5g. Resume normal replication
ssh admin@site-a-nas "synoreplicatool --resume"

# STEP 6: Post-Failback
# - Verify all systems normal
# - Document lessons learned
# - Update DR runbook if needed
# - Schedule next DR drill
```

## Verification
| Check | Method | Expected Result |
|-------|--------|-----------------|
| DR Readiness | Daily script | All items "REACHABLE" |
| NAS Promotion | synoreplicatool --status | "Primary" role |
| ZTNA Redirect | nslookup | Points to Site B |
| VM Startup | PowerCLI | All VMs "PoweredOn" |
| Service Health | curl/smbclient | All respond OK |

## Rollback
If failover fails:
1. Document failure point
2. Remain on Site B if operational
3. Escalate to vendor support
4. Consider manual recovery procedures

## Escalation Matrix
| Severity | Contact | Response Time |
|----------|---------|---------------|
| P1 - Critical (DR declared) | DR Coordinator: +91-XXXXXXXXXX | Immediate |
| P2 - High (Failover issues) | IT Manager: +91-XXXXXXXXXX | 15 minutes |
| Vendor Support (Synology) | support.synology.com | 4 hours |
| Vendor Support (VMware) | support.vmware.com | 1 hour |

## Related Documents
- SOP-004: Storage Administration
- SOP-005: Backup Operations
- SOP-008: Incident Response
- Part3_Enhanced_DR_Monitoring_Power.md

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 22-Mar-2026 | VConfi | Initial release |

---

# SOP-007: Security Operations

## Purpose
To establish standardized procedures for security monitoring, log analysis, firewall management, access review, and incident response for the B2H Studios security infrastructure.

## Scope
This SOP covers:
- Daily security log review
- FortiGate rule change process
- ZTNA access review
- Certificate renewal
- Security incident initial response

## Responsibility
| Role | Responsibility |
|------|----------------|
| Security Administrator | Daily log review, rule updates |
| CISO/Security Lead | Incident response, policy enforcement |
| IT Manager | Change approval, compliance oversight |

## Prerequisites
- FortiGate admin access
- FortiAnalyzer access (https://fanalyzer.b2h.local)
- Splunk access (https://splunk.b2h.local)
- ZTNA policy documentation
- Certificate inventory

## Procedure

### 1. Daily Security Log Review

#### 1.1 Morning Security Checklist (09:00 AM)
```bash
# Access FortiAnalyzer
# https://fanalyzer.b2h.local

Checklist:
□ Review overnight security events
□ Check for high-severity alerts (P1/P2)
□ Review failed authentication attempts
□ Check for blocked threats (IPS/AV)
□ Review VPN/ZTNA access logs
□ Check for anomalous traffic patterns
```

#### 1.2 Automated Log Analysis
```bash
# FortiAnalyzer CLI for automated reports

# Get threat summary
diagnose test application forticldd 1

# Check IPS events
diagnose test application ipsmonitor 1

# Review AV detections
diagnose test application scanunitd 1
```

#### 1.3 Key Security Metrics to Review
| Metric | Normal Range | Action if Abnormal |
|--------|--------------|-------------------|
| Failed logins/hour | <5 | Investigate source IPs |
| Blocked threats/day | 10-100 | Normal range varies |
| VPN connections | 15-25 | Verify legitimacy |
| High-risk events | 0 | Immediate investigation |
| SSL inspection failures | <10/day | Check certificate issues |

### 2. FortiGate Rule Change Process

#### 2.1 Change Request Form
```
FortiGate Rule Change Request
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Requester: ________________________
Date: ________________________

Change Details:
Rule Name: ________________________
Source: ________________________
Destination: ________________________
Service/Port: ________________________
Action: [ ] Allow  [ ] Deny  [ ] Modify  [ ] Delete

Business Justification:
________________________________________________
________________________________________________

Security Review:
[ ] Risk assessment completed
[ ] Least privilege verified
[ ] Logging enabled
[ ] No conflicts with existing rules

Approved by: ________________________
Date: ________________________
```

#### 2.2 Rule Implementation
```bash
# SSH to FortiGate
ssh admin@10.10.40.1

# Enter configuration mode
config firewall policy

# Add new rule (example: allow new service)
edit 0  # Auto-assign next ID
    set name "Allow-NewService-DMZ-to-Internal"
    set srcintf "port3"  # DMZ
    set dstintf "port4"  # Internal
    set srcaddr "DMZ_Servers"
    set dstaddr "Internal_Servers"
    set action accept
    set schedule "always"
    set service "HTTP" "HTTPS"
    set logtraffic all
    set comments "[Ticket#12345] Approved by [Name] on [Date]"
next
end

# Move rule to correct position (before deny)
config firewall policy
move 106 before 200
end

# Verify configuration
show firewall policy | grep -A10 "Allow-NewService"

# Test rule
# From source: telnet destination port
# Check logs: diagnose debug enable
```

#### 1.3 Post-Change Verification
```bash
# Verify rule hit count
diagnose ipstat filter
get firewall policy | grep -A5 [RuleName]

# Check for any unintended blocks
diagnose debug flow filter [source-ip]
diagnose debug flow trace start 100

# Review logs for 24 hours
diagnose test application forticldd 3
```

### 3. ZTNA Access Review

#### 3.1 Weekly ZTNA Review
```bash
# FortiGate CLI
ssh admin@10.10.40.1

# Review ZTNA access logs
diagnose wad user list

# Check device posture compliance
diagnose endpoint record list

# Review denied access attempts
diagnose wad debug filter category ztna
diagnose debug enable
```

#### 3.2 Quarterly Access Review
```
ZTNA Access Review - Quarterly
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Quarter: Q__ 20__
Reviewed by: ________________________

User Access Review:
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ User         │ Last Access  │ Device Status│ Action       │
├──────────────┼──────────────┼──────────────┼──────────────┤
│ user1@b2h    │ ____________ │ Compliant    │ [ ] Keep     │
│              │              │              │ [ ] Revoke   │
├──────────────┼──────────────┼──────────────┼──────────────┤
│ user2@b2h    │ ____________ │ Non-compliant│ [ ] Remediate│
│              │              │              │ [ ] Revoke   │
└──────────────┴──────────────┴──────────────┴──────────────┘

Inactive Users (>30 days):
[ ] Notified: ________________________
[ ] Access suspended: ________________________

Device Posture Violations:
[ ] Missing patches: ________________________
[ ] AV not running: ________________________
[ ] Encryption disabled: ________________________

Remediation Actions:
________________________________________________
```

### 4. Certificate Renewal

#### 4.1 Certificate Inventory
| Certificate | Location | Expiry Date | Renewal Due | Owner |
|-------------|----------|-------------|-------------|-------|
| b2hstudios.com | FortiGate | [Date] | 30 days before | NetOps |
| wildcard.b2hstudios.com | FortiGate | [Date] | 30 days before | NetOps |
| nas.b2h.local | Synology | [Date] | 30 days before | Storage |
| vcenter.b2h.local | vCenter | [Date] | 30 days before | SysOps |
| zabbix.b2h.local | Zabbix | [Date] | 30 days before | SysOps |

#### 4.2 Certificate Renewal Procedure
```bash
# FortiGate Certificate Renewal

# Step 1: Generate CSR
config vpn certificate local
edit "b2h-wildcard-new"
    set password [encrypt-password]
    set comments "Wildcard cert renewal 2026"
    set certificate "-----BEGIN CERTIFICATE REQUEST-----"
    # Paste CSR content
    "-----END CERTIFICATE REQUEST-----"
next
end

# Step 2: Submit to CA, receive certificate

# Step 3: Import certificate
config vpn certificate local
edit "b2h-wildcard-new"
    set certificate "-----BEGIN CERTIFICATE-----"
    # Paste certificate content
    "-----END CERTIFICATE-----"
    set private-key "-----BEGIN ENCRYPTED PRIVATE KEY-----"
    # Paste key content
    "-----END ENCRYPTED PRIVATE KEY-----"
next
end

# Step 4: Update references
config system global
    set admin-server-cert "b2h-wildcard-new"
end

config firewall ssl-ssh-profile
edit "certificate-inspection"
    set ca-certificate "b2h-wildcard-new"
next
end

# Step 5: Test
curl -v https://firewall.b2h.local
# Verify certificate chain

# Step 6: Schedule old cert deletion (30 days)
```

### 5. Security Incident Initial Response

#### 5.1 Incident Detection Categories
| Category | Indicators | Severity |
|----------|------------|----------|
| Malware | AV detection, suspicious files | P1 |
| Intrusion | Failed logins, lateral movement | P1 |
| Data Exfiltration | Large uploads, unusual access | P1 |
| Ransomware | File encryption, ransom notes | P1 |
| Policy Violation | Unauthorized access attempts | P2 |

#### 5.2 Initial Response Actions
```bash
# STEP 1: Isolate (if malware/ransomware suspected)
# Block source IP immediately
config firewall address
edit "Block-Threat-[IP]"
    set subnet [IP] 255.255.255.255
next
end

config firewall policy
edit 0
    set name "Block-Threat-[IP]"
    set srcintf "any"
    set dstintf "any"
    set srcaddr "Block-Threat-[IP]"
    set dstaddr "all"
    set action deny
    set schedule "always"
    set service "ALL"
    set logtraffic all
next
end

# STEP 2: Capture evidence
diagnose sniffer packet any 'host [suspicious-ip]' 4 1000 l
# Save output to file

# STEP 3: Disable compromised account (if applicable)
config user local
edit [username]
    set status disable
next
end

# STEP 4: Revoke ZTNA access
diagnose wad user clear [username]

# STEP 5: Notify security team
# Create P1 ticket
# Page CISO
```

## Verification
| Check | Method | Expected Result |
|-------|--------|-----------------|
| Firewall Rules | `show firewall policy` | Rules in correct order |
| ZTNA Status | `diagnose wad user list` | Users compliant |
| Certificates | `show vpn certificate local` | All valid, not expiring |
| Security Logs | FortiAnalyzer | No critical alerts |

## Rollback
If rule causes issues:
```bash
# Delete or disable rule immediately
config firewall policy
delete [rule-id]
# OR
edit [rule-id]
    set status disable
next
end
```

## Escalation Matrix
| Severity | Contact | Response Time |
|----------|---------|---------------|
| P1 - Critical (Security breach) | CISO: +91-XXXXXXXXXX | 15 minutes |
| P2 - High (Policy violation) | Security Admin: +91-XXXXXXXXXX | 1 hour |
| Fortinet Support | support.fortinet.com | 1 hour (P1) |

## Related Documents
- SOP-008: Incident Response
- SOP-010: User Access Management
- Part5_Enhanced_Security_Stress_Test.md

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 22-Mar-2026 | VConfi | Initial release |

---

# SOP-008: Incident Response

## Purpose
To establish standardized procedures for security incident classification, response coordination, containment, evidence preservation, and post-incident review to minimize impact and prevent recurrence.

## Scope
This SOP covers:
- Incident classification (P1/P2/P3/P4)
- Response team roles and responsibilities
- Communication plan
- Containment procedures
- Evidence preservation
- Post-incident review

## Responsibility
| Role | Responsibility |
|------|----------------|
| Incident Commander | Overall coordination, decision authority |
| Technical Lead | Technical investigation, containment |
| Communications Lead | Stakeholder updates, external comms |
| Documentation Lead | Evidence collection, timeline, reporting |
| Legal/Compliance | Regulatory requirements, legal hold |

## Prerequisites
- Incident Response Plan (IRP) document
- Contact tree with alternates
- Forensic tools (FTK, Autopsy, etc.)
- Evidence storage (write-protected)
- War room/conference bridge access

## Procedure

### 1. Incident Classification

#### 1.1 Severity Classification Matrix
| Severity | Definition | Examples | Response Time |
|----------|------------|----------|---------------|
| **P1 - Critical** | Complete service outage or active breach | Ransomware, data breach, site down | 15 minutes |
| **P2 - High** | Significant service degradation | Major system failure, malware detection | 1 hour |
| **P3 - Medium** | Limited impact, workaround available | Single system failure, minor policy violation | 4 hours |
| **P4 - Low** | Minimal impact, cosmetic | Non-critical alert, documentation error | 24 hours |

#### 1.2 Incident Type Categories
| Category | Description | Primary Response |
|----------|-------------|------------------|
| Security | Malware, intrusion, data loss | SOP-007 + this SOP |
| Availability | System downtime, network outage | SOP-006 + this SOP |
| Performance | Degradation, resource exhaustion | SOP-002 + this SOP |
| Data | Corruption, loss, unauthorized access | SOP-005 + this SOP |

### 2. Response Team Roles

#### 2.1 Incident Response Team Structure
```
                    ┌─────────────────┐
                    │  Incident       │
                    │  Commander      │
                    │  (IT Manager)   │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Technical      │  │  Communications │  │  Documentation  │
│  Lead           │  │  Lead           │  │  Lead           │
│  (Senior Admin) │  │  (IT Admin)     │  │  (Any available)│
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

#### 2.2 Role Responsibilities
| Role | Key Responsibilities |
|------|---------------------|
| Incident Commander | Declare/close incident, resource allocation, major decisions |
| Technical Lead | Technical containment, evidence collection, root cause analysis |
| Communications Lead | Status updates, stakeholder notification, external communications |
| Documentation Lead | Timeline recording, evidence chain of custody, final report |

### 3. Communication Plan

#### 3.1 Internal Communication Tree
```
T+0    P1 Incident Detected
       └── Page On-Call Engineer
T+15   Engineer Acknowledges
       └── Page Incident Commander
T+30   Incident Commander Convenes Team
       ├── Technical Lead → Technical resources
       ├── Communications Lead → Stakeholder notifications
       └── Documentation Lead → War room setup

T+1h   First Status Update
       └── All stakeholders notified
T+2h   Subsequent updates every 30 min (P1) or 1 hour (P2)
       └── Until resolution or downgrade
```

#### 3.2 Communication Templates
```
INCIDENT NOTIFICATION - P1
━━━━━━━━━━━━━━━━━━━━━━━━━━
Incident ID: INC-2026-XXX
Severity: P1 - Critical
Time Detected: [Timestamp]
Status: ACTIVE

Summary:
[Brief description of incident]

Impact:
[What is affected, who is impacted]

Actions Taken:
[What has been done so far]

Next Update:
[When next communication will be sent]

Contact:
Incident Commander: [Name] [Phone]
```

#### 3.3 External Communication
| Stakeholder | When to Notify | Who Notifies |
|-------------|----------------|--------------|
| Customers | Confirmed data breach | Communications Lead |
| Vendors | If their systems involved | Technical Lead |
| Regulators | As required by law | Legal/Compliance |
| Media | Only if public impact | CISO/Executive |

### 4. Containment Procedures

#### 4.1 Short-Term Containment (Immediate)
```bash
# Network Isolation (if malware suspected)
# FortiGate - Block suspicious IPs
config firewall address
edit "IOC-[IP]"
    set subnet [IP] 255.255.255.255
    set comment "Incident INC-2026-XXX"
next
end

# Disable compromised accounts
config user local
edit [compromised-user]
    set status disable
next
end

# Isolate VM (if compromised)
# vCenter - disconnect NIC or move to isolated VLAN
```

#### 4.2 System Isolation Decision Tree
```
System Compromised?
        │
        ▼
┌───────────────────┐
│ Critical System?  │
└─────────┬─────────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
┌───────┐   ┌───────────┐
│  Yes  │   │    No     │
└───┬───┘   └─────┬─────┘
    │             │
    ▼             ▼
┌───────────┐ ┌───────────┐
│ Isolate   │ │ Disconnect│
│ NIC only  │ │ from net  │
│ (maintain │ │ (full     │
│  uptime)  │ │  quarantine)
└───────────┘ └───────────┘
```

#### 4.3 Long-Term Containment
- Backup compromised systems (forensic image)
- Patch vulnerabilities
- Rotate credentials
- Implement additional monitoring
- Deploy compensating controls

### 5. Evidence Preservation

#### 5.1 Evidence Collection Checklist
```
Evidence Collection
━━━━━━━━━━━━━━━━━━━
Incident ID: INC-2026-XXX
Collected by: ________________________
Date/Time: ________________________

[ ] Memory dump (if system compromised)
    Tool: Magnet RAM Capture / FTK Imager
    Location: /evidence/INC-2026-XXX/memory/

[ ] Disk image (if system compromised)
    Tool: dd / FTK Imager
    Format: E01 (compressed)
    Hash: SHA-256 calculated

[ ] Log files
    Sources: FortiGate, Synology, Windows Event Logs
    Time range: [Start] to [End]
    Location: /evidence/INC-2026-XXX/logs/

[ ] Network captures
    Tool: tcpdump / Wireshark
    Filters: host [IP] or port [Port]
    Location: /evidence/INC-2026-XXX/pcap/

Chain of Custody:
┌──────────────┬──────────────┬──────────────────────┐
│ Date/Time    │ Custodian    │ Action               │
├──────────────┼──────────────┼──────────────────────┤
│ ____________ │ ____________ │ Collected            │
│ ____________ │ ____________ │ Transferred to       │
│ ____________ │ ____________ │ Analyzed by          │
│ ____________ │ ____________ │ Archived             │
└──────────────┴──────────────┴──────────────────────┘
```

#### 5.2 Forensic Imaging Procedure
```bash
# Create forensic image of compromised system
# Boot from forensic Linux (Helix/Kali)

# Identify source disk
fdisk -l

# Create image with hash verification
dd if=/dev/sda of=/mnt/evidence/INC-2026-XXX-sda.img bs=4M conv=noerror,sync status=progress

# Calculate SHA-256
sha256sum /mnt/evidence/INC-2026-XXX-sda.img > /mnt/evidence/INC-2026-XXX-sha256.txt

# Verify hash
cat /mnt/evidence/INC-2026-XXX-sha256.txt
sha256sum -c /mnt/evidence/INC-2026-XXX-sha256.txt

# Set immutable on evidence files
chattr +i /mnt/evidence/INC-2026-XXX-*
```

### 6. Post-Incident Review

#### 6.1 Post-Incident Review Meeting
```
Post-Incident Review
━━━━━━━━━━━━━━━━━━━━
Incident ID: INC-2026-XXX
Date: ___________
Facilitator: ___________

Timeline Review:
┌──────────┬──────────────────────────────────────┐
│ Time     │ Event                                │
├──────────┼──────────────────────────────────────┤
│ T+0      │ Incident detected                    │
│ ________ │ ____________________________________ │
│ ________ │ ____________________________________ │
│ ________ │ ____________________________________ │
│ ________ │ Resolution                           │
└──────────┴──────────────────────────────────────┘

Root Cause Analysis:
5 Whys:
1. Why did incident occur? _______________________________
2. Why? ___________________________________________________
3. Why? ___________________________________________________
4. Why? ___________________________________________________
5. Why? ___________________________________________________

Root Cause: _________________________________________________

Corrective Actions:
┌──────────┬──────────────────────────────┬────────┬──────────┐
│ Priority │ Action                       │ Owner  │ Due Date │
├──────────┼──────────────────────────────┼────────┼──────────┤
│ High     │ ____________________________ │ ______ │ ________ │
│ Medium   │ ____________________________ │ ______ │ ________ │
│ Low      │ ____________________________ │ ______ │ ________ │
└──────────┴──────────────────────────────┴────────┴──────────┘

Lessons Learned:
What went well: _____________________________________________
What could be improved: ______________________________________
Process changes needed: ______________________________________

Approved by: ________________________ Date: __________________
```

#### 6.2 Incident Closure Criteria
- [ ] Root cause identified
- [ ] All corrective actions assigned
- [ ] Evidence properly archived
- [ ] Stakeholders notified of resolution
- [ ] Post-incident review completed
- [ ] Documentation updated

## Verification
| Check | Method | Expected Result |
|-------|--------|-----------------|
| Team Assembly | Time tracking | <30 minutes for P1 |
| Evidence Chain | Chain of custody form | Complete, unbroken |
| Root Cause | 5 Whys analysis | True root identified |
| Lessons Learned | Post-incident review | Actions assigned |

## Rollback
Not applicable - incident response is not reversible

## Escalation Matrix
| Severity | Contact | Response Time |
|----------|---------|---------------|
| P1 - Critical | Incident Commander: +91-XXXXXXXXXX | Immediate |
| P2 - High | Technical Lead: +91-XXXXXXXXXX | 1 hour |
| External IR Firm | [Contracted IR firm] | 4 hours |

## Related Documents
- SOP-007: Security Operations
- SOP-009: Change Management
- Part5_Enhanced_Security_Stress_Test.md

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 22-Mar-2026 | VConfi | Initial release |

---

# SOP-009: Change Management

## Purpose
To establish standardized procedures for managing changes to the IT infrastructure, ensuring minimal disruption to services while maintaining security and compliance.

## Scope
This SOP covers:
- Change request submission and approval
- Change categorization (Standard, Normal, Emergency)
- CAB (Change Advisory Board) process
- Emergency change procedure
- Rollback procedures

## Responsibility
| Role | Responsibility |
|------|----------------|
| Change Requester | Submit requests, test changes |
| Change Manager | Review, schedule, track changes |
| CAB Members | Approve significant changes |
| IT Manager | Final approval, emergency changes |

## Prerequisites
- Change request form
- Current configuration documentation
- Test environment access
- Rollback plan prepared
- Maintenance window scheduled

## Procedure

### 1. Change Request Process

#### 1.1 Change Request Form
```
CHANGE REQUEST FORM
━━━━━━━━━━━━━━━━━━━━
CR Number: CR-2026-XXX
Date Submitted: ___________
Requester: ___________

Change Details:
Title: __________________________________________________
Description: ____________________________________________
________________________________________________________

Justification:
[ ] Security patch
[ ] Performance improvement
[ ] Capacity expansion
[ ] Bug fix
[ ] New feature/service
[ ] Other: ___________

Business Impact:
[ ] No impact
[ ] Minor impact (limited users)
[ ] Major impact (all users)
[ ] Critical impact (business halt)

Affected Systems:
[ ] Network (FortiGate, Switches)
[ ] Storage (Synology NAS)
[ ] Servers (VMware)
[ ] Security (ZTNA, certificates)
[ ] Applications (Zabbix, etc.)
[ ] Other: ___________

Implementation Plan:
Proposed Date/Time: ___________
Duration: ___________
Backout Plan: __________________________________________
________________________________________________________

Testing:
[ ] Tested in lab environment
[ ] Tested in staging
[ ] Unable to test (explain): __________________________

Approvals:
Requester: ___________ Date: _______
Change Manager: ___________ Date: _______
CAB: ___________ Date: _______
IT Manager: ___________ Date: _______
```

#### 1.2 Change Submission Process
1. Complete change request form
2. Attach supporting documentation
3. Submit to Change Manager
4. Receive CR number (CR-2026-XXX)
5. Await review and scheduling
6. Implement as scheduled
7. Complete post-implementation review

### 2. Change Categorization

#### 2.1 Change Types
| Type | Definition | Approval Required | Lead Time |
|------|------------|-------------------|-----------|
| **Standard** | Low risk, pre-approved procedure | Change Manager | 48 hours |
| **Normal** | Moderate risk, requires assessment | CAB | 1 week |
| **Major** | High risk, significant impact | CAB + IT Manager | 2 weeks |
| **Emergency** | Critical fix, bypass normal process | IT Manager | Immediate |

#### 2.2 Standard Change Examples
- Routine patch deployment (tested procedure)
- User account provisioning
- Monitor threshold adjustments
- Certificate renewals (standard process)
- Backup verification tests

#### 2.3 Normal/Major Change Examples
- Firmware upgrades
- Hardware replacement
- Network reconfiguration
- Storage expansion
- Major software updates

### 3. CAB (Change Advisory Board) Process

#### 3.1 CAB Composition
| Role | Department | Responsibility |
|------|------------|----------------|
| Chair | IT Manager | Final approval, conflict resolution |
| Member | Network Team | Network impact assessment |
| Member | Storage Team | Storage impact assessment |
| Member | Security Team | Security risk assessment |
| Member | Applications Team | Application impact |

#### 3.2 CAB Meeting Agenda
```
CAB Meeting Agenda
━━━━━━━━━━━━━━━━━━
Date: ___________
Attendees: ________________________________

Review Queue:
1. Changes pending approval
   - CR-2026-XXX: [Description] - Decision: [Approve/Defer/Reject]
   - CR-2026-XXX: [Description] - Decision: [Approve/Defer/Reject]

2. Changes scheduled for next window
   - Review prerequisites, confirm readiness

3. Changes implemented since last meeting
   - Post-implementation review results
   - Any issues encountered

4. Change calendar review
   - Conflict identification
   - Resource availability

5. Process improvements
   - Feedback, metrics review
```

#### 3.3 CAB Decision Matrix
| Risk Level | Impact | Approval Authority |
|------------|--------|-------------------|
| Low | Low | Change Manager |
| Low | Medium | Change Manager |
| Medium | Low | CAB |
| Medium | Medium | CAB |
| High | Any | CAB + IT Manager |
| Any | High | CAB + IT Manager |

### 4. Emergency Change Procedure

#### 4.1 Emergency Change Criteria
Emergency changes are only for:
- Security vulnerabilities requiring immediate patching
- Critical system failures needing immediate fix
- Regulatory compliance issues
- Natural disaster recovery

NOT for:
- Convenience
- Poor planning
- "While we're here" additions

#### 4.2 Emergency Change Process
```
Emergency Change Process
━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: IT Manager Authorization (Phone/Verbal OK)
├── Declare emergency
├── Document reason
└── Obtain verbal approval

Step 2: Implement with Minimal Testing
├── Follow documented procedure if exists
├── Or implement best-practice fix
└── Document all steps taken

Step 3: Post-Implementation
├── Notify CAB of emergency change
├── Submit retrospective change request
├── Conduct post-implementation review
└── Update documentation

Step 4: Review
├── CAB reviews emergency change within 48 hours
├── Validates appropriateness
├── Identifies prevention opportunities
└── Updates standard procedures if applicable
```

#### 4.3 Emergency Change Documentation
```
EMERGENCY CHANGE - RETROSPECTIVE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ECR Number: ECR-2026-XXX
Date Implemented: ___________
Authorized by: ___________

Emergency Justification:
[ ] Security vulnerability (CVE: _________)
[ ] Critical system failure
[ ] Compliance requirement
[ ] Disaster recovery

Description of Change:
________________________________________________________
________________________________________________________

Steps Taken:
1. ____________________________________________________
2. ____________________________________________________
3. ____________________________________________________

Testing Performed:
[ ] Limited testing (explain): __________________________
[ ] No testing (explain): ______________________________

Outcome:
[ ] Successful
[ ] Issues encountered (describe): _____________________

Post-Implementation Actions Required:
[ ] Update standard procedures
[ ] Schedule full testing
[ ] Additional documentation
[ ] Training required

CAB Review Date: ___________
Approved for Retrospective: [ ] Yes  [ ] No (requires remediation)
```

### 5. Rollback Procedures

#### 5.1 Rollback Decision Criteria
Rollback if ANY of the following:
- Service degradation >25%
- Security vulnerability introduced
- Data integrity concerns
- User impact exceeds acceptable threshold
- Failed acceptance criteria

#### 5.2 Rollback Procedure
```bash
# Generic rollback steps - customize per change type

# STEP 1: Assess impact
# Determine scope of rollback needed

# STEP 2: Notify stakeholders
# "Initiating rollback of CR-2026-XXX due to [reason]"

# STEP 3: Execute rollback
# Configuration rollback example (FortiGate):
config system global
    # Revert to previous config
    restore config from tftp [server] [file]
end

# VM snapshot rollback (VMware):
Get-Snapshot -VM [VM-Name] | Where-Object {$_.Name -eq "Pre-Change-CRXXX"} | `
    Restore-VMSnapshot -Confirm:$false

# STEP 4: Verify rollback
# Confirm service restoration
# Test critical functions

# STEP 5: Document
# Record rollback reason
# Update change record
# Schedule post-mortem if needed
```

#### 5.3 Rollback Testing
```bash
# Pre-change snapshot/backup verification
date > /tmp/rollback-test-start.txt

# Make test change
[apply test configuration]

# Verify rollback works
[execute rollback procedure]

# Confirm restoration
diff /tmp/rollback-test-start.txt /tmp/rollback-test-end.txt

# If test passes, proceed with actual change
```

## Verification
| Check | Method | Expected Result |
|-------|--------|-----------------|
| CR Tracking | Change log | All changes documented |
| CAB Minutes | Meeting records | Decisions recorded |
| Implementation | Post-review | Matches approved plan |
| Rollback | Test results | Successful within SLA |

## Escalation Matrix
| Issue | Contact | Response Time |
|-------|---------|---------------|
| CAB Conflict | IT Manager | Immediate |
| Emergency Authorization Needed | IT Manager | 15 minutes |
| Rollback Failure | Technical Lead | Immediate |

## Related Documents
- All technical SOPs for specific rollback procedures
- SOP-008: Incident Response

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 22-Mar-2026 | VConfi | Initial release |

---

# SOP-010: User Access Management

## Purpose
To establish standardized procedures for user onboarding, offboarding, access reviews, and privileged access management to ensure appropriate access controls and compliance with ISO 27001 requirements.

## Scope
This SOP covers:
- User onboarding procedure
- User offboarding procedure
- Quarterly access review
- Password reset procedure
- Privileged access management

## Responsibility
| Role | Responsibility |
|------|----------------|
| HR Representative | Initiate onboarding/offboarding requests |
| IT Administrator | Account provisioning/deprovisioning |
| System Owners | Access approval, periodic review |
| IT Manager | Privileged access approval |
| Security Administrator | Compliance monitoring |

## Prerequisites
- HR system access for employee status
- Active Directory administrative access
- FortiAuthenticator admin access
- Current organizational chart
- Access matrix documentation

## Procedure

### 1. User Onboarding Procedure

#### 1.1 New User Request Form
```
NEW USER ACCESS REQUEST
━━━━━━━━━━━━━━━━━━━━━━━
Request Date: ___________
Requested by (HR): ___________

Employee Details:
Full Name: ________________________________
Employee ID: ________________________________
Department: ________________________________
Manager: ________________________________
Start Date: ________________________________
Location: [ ] Site A  [ ] Site B  [ ] Remote

Access Requirements:
┌─────────────────────┬────────┬───────────────┐
│ System              │ Access │ Business Just │
├─────────────────────┼────────┼───────────────┤
│ Windows Domain      │ [ ] Y  │               │
│ Email (Office 365)  │ [ ] Y  │               │
│ ZTNA (Remote)       │ [ ] Y  │               │
│ NAS Shares          │ [ ] Y  │ Which: _______│
│ Zabbix              │ [ ] Y  │               │
│ FortiClient EMS     │ [ ] Y  │               │
│ Other: ____________ │ [ ] Y  │               │
└─────────────────────┴────────┴───────────────┘

Manager Approval: ___________ Date: _______
IT Manager Approval: ___________ Date: _______
```

#### 1.2 Account Provisioning Steps
```bash
# STEP 1: Create Active Directory Account
# PowerShell on Domain Controller

$UserParams = @{
    Name = "jdoe"
    GivenName = "John"
    Surname = "Doe"
    DisplayName = "John Doe"
    SamAccountName = "jdoe"
    UserPrincipalName = "jdoe@b2h.local"
    Path = "OU=Users,OU=Production,DC=b2h,DC=local"
    Enabled = $true
    AccountPassword = (ConvertTo-SecureString -String "TempPass123!" -AsPlainText -Force)
    ChangePasswordAtLogon = $true
}

New-ADUser @UserParams

# Add to groups based on role
Add-ADGroupMember -Identity "Production-Users" -Members "jdoe"
Add-ADGroupMember -Identity "ZTNA-Editors" -Members "jdoe"

# STEP 2: Create Email Account (Office 365)
# Connect to Exchange Online
Connect-ExchangeOnline

Enable-Mailbox -Identity "jdoe" -Alias "jdoe"
Set-Mailbox -Identity "jdoe" -MaxSendSize 100MB -MaxReceiveSize 100MB

# STEP 3: Configure FortiAuthenticator (ZTNA/MFA)
# Via FortiAuthenticator GUI or API
# Add user to ZTNA user group
# Assign FortiToken for MFA

# STEP 4: Configure NAS Access
# SSH to Synology
synoacltool -add /volume1/Projects [username] allow Read

# STEP 5: Configure Zabbix Access
# SQL or GUI
INSERT INTO users (username, name, surname, passwd, roleid)
VALUES ('jdoe', 'John', 'Doe', '[hashed_password]', 2);

# STEP 6: Notify user
# Send welcome email with:
# - Username
# - Temporary password
# - ZTNA download link
# - MFA setup instructions
# - Acceptable use policy
```

#### 1.3 Onboarding Checklist
```
New User Onboarding Checklist
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Employee: ___________ Start Date: ___________

Account Creation:
[ ] Active Directory account created
[ ] Email account enabled
[ ] ZTNA/FortiAuthenticator configured
[ ] MFA token assigned/activated
[ ] NAS share permissions configured
[ ] Zabbix account created
[ ] Added to appropriate security groups

Hardware:
[ ] Laptop/desktop assigned
[ ] Mobile device (if applicable)
[ ] FortiClient installed and configured
[ ] Kaspersky installed

Access Verification:
[ ] User can log into Windows domain
[ ] Email access verified
[ ] ZTNA connection successful
[ ] NAS shares accessible
[ ] Zabbix login successful

Training:
[ ] Security awareness briefing completed
[ ] Acceptable use policy signed
[ ] ZTNA/MFA training completed
[ ] Emergency contacts provided

Completed by: ___________ Date: _______
```

### 2. User Offboarding Procedure

#### 2.1 Termination Request Form
```
USER TERMINATION REQUEST
━━━━━━━━━━━━━━━━━━━━━━━━
Request Date: ___________
Requested by (HR): ___________
Termination Date: ___________
Termination Type: [ ] Voluntary  [ ] Involuntary

Employee Details:
Name: ________________________________
Employee ID: ________________________________
Manager: ________________________________

Access Revocation Requirements:
[ ] Immediate (security concern)
[ ] End of business day
[ ] End of notice period (___ days)

Data Handover:
[ ] Data transferred to: ________________________________
[ ] Project files location documented
[ ] Email delegation configured

Manager: ___________ Date: _______
HR: ___________ Date: _______
IT Manager: ___________ Date: _______
```

#### 2.2 Account Deprovisioning Steps
```bash
# STEP 1: Disable AD Account (Immediate for involuntary)
Disable-ADAccount -Identity "jdoe"

# STEP 2: Revoke ZTNA Access (Immediate)
# FortiAuthenticator
config user local
edit "jdoe"
    set status disable
next
end

# Clear active sessions
diagnose wad user clear jdoe

# STEP 3: Email Handling
# Exchange Online
# Set auto-reply
Set-MailboxAutoReplyConfiguration -Identity "jdoe" `
    -AutoReplyState Enabled `
    -InternalMessage "This employee is no longer with B2H Studios..." `
    -ExternalMessage "This employee is no longer with B2H Studios..."

# Grant manager access
Add-MailboxPermission -Identity "jdoe" -User "manager" -AccessRights FullAccess

# STEP 4: Backup and Archive Data
# Export mailbox to PST
New-MailboxExportRequest -Mailbox "jdoe" -FilePath "\\backup\email\jdoe.pst"

# Archive NAS home directory
tar -czf /volume1/archive/users/jdoe-$(date +%Y%m%d).tar.gz /volume1/homes/jdoe

# STEP 5: Remove Permissions
# Remove from all groups
Get-ADGroup -Filter * | Where-Object { (Get-ADGroupMember $_ | Where-Object {$_.SamAccountName -eq "jdoe"}) } | `
    ForEach-Object { Remove-ADGroupMember -Identity $_ -Members "jdoe" -Confirm:$false }

# Remove Zabbix access
# SQL: DELETE FROM users WHERE username='jdoe';

# STEP 6: Hardware Recovery
# Document returned items
# Wipe device if applicable

# STEP 7: Final Account Deletion (30 days post-termination)
# After grace period for data recovery
Remove-ADUser -Identity "jdoe" -Confirm:$false
```

### 3. Quarterly Access Review

#### 3.1 Access Review Process
```
Quarterly Access Review - Q_ 20__
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Review Period: ___________
Completed by: ___________

System: Active Directory
Reviewer: Department Managers

┌──────────────┬──────────────┬──────────────┬──────────────┐
│ User         │ Department   │ Last Login   │ Action       │
├──────────────┼──────────────┼──────────────┼──────────────┤
│ jdoe         │ Production   │ 2026-03-15   │ [ ] Keep     │
│              │              │              │ [ ] Modify   │
│              │              │              │ [ ] Remove   │
├──────────────┼──────────────┼──────────────┼──────────────┤
│ [Continue...]│              │              │              │
└──────────────┴──────────────┴──────────────┴──────────────┘

Privileged Accounts Review:
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Account      │ Owner        │ Last Used    │ Justification│
├──────────────┼──────────────┼──────────────┼──────────────┤
│ admin        │ IT Manager   │ 2026-03-20   │ Required     │
│ root         │ SysAdmin     │ 2026-03-19   │ Required     │
└──────────────┴──────────────┴──────────────┴──────────────┘

Service Accounts Review:
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Account      │ Purpose      │ Status       │ Action       │
├──────────────┼──────────────┼──────────────┼──────────────┤
│ svc-backup   │ Veeam        │ Active       │ [ ] Keep     │
│ svc-monitor  │ Zabbix       │ Active       │ [ ] Keep     │
└──────────────┴──────────────┴──────────────┴──────────────┘

Findings: ___________________________________________
Remediation: ________________________________________
Completed: ___________
```

#### 3.2 Stale Account Identification
```bash
# PowerShell - Find inactive accounts
Search-ADAccount -AccountInactive -TimeSpan 90.00:00:00 | `
    Where-Object {$_.Enabled -eq $true} | `
    Select-Object Name, LastLogonDate, DistinguishedName | `
    Export-CSV "Stale-Accounts-$(Get-Date -Format 'yyyyMMdd').csv"

# Email accounts inactive >90 days
Get-Mailbox -ResultSize Unlimited | `
    Get-MailboxStatistics | `
    Where-Object {$_.LastLogonTime -lt (Get-Date).AddDays(-90)} | `
    Select-Object DisplayName, LastLogonTime
```

### 4. Password Reset Procedure

#### 4.1 Self-Service Password Reset
```
Users can reset via:
1. Azure AD Self-Service Password Reset (SSPR)
   - https://passwordreset.microsoftonline.com
   - Requires pre-registered authentication methods

2. IT Help Desk (if SSPR fails)
   - Call: XXX-XXXX-XXXX
   - Verify identity via employee ID + manager confirmation
```

#### 4.2 Admin-Initiated Password Reset
```bash
# Active Directory
Set-ADAccountPassword -Identity "jdoe" -Reset -NewPassword (ConvertTo-SecureString -AsPlainText "TempPass123!" -Force)
Set-ADUser -Identity "jdoe" -ChangePasswordAtLogon $true

# FortiAuthenticator
diagnose test application forticldd 1
# Reset via GUI or API

# Notify user via SMS or manager
Send-MailMessage -To "jdoe@b2h.local" -Subject "Password Reset" `
    -Body "Your password has been reset. Temporary password: TempPass123!"
```

### 5. Privileged Access Management

#### 5.1 Privileged Account Inventory
| Account | System | Purpose | Owner | Last Review |
|---------|--------|---------|-------|-------------|
| admin | FortiGate | Firewall administration | IT Manager | [Date] |
| root | Synology | NAS administration | Storage Admin | [Date] |
| Administrator | Windows | Domain admin | IT Manager | [Date] |
| root | ESXi | Virtualization host | System Admin | [Date] |

#### 5.2 Privileged Access Controls
```bash
# Just-in-Time (JIT) elevation for domain admin
# Use temporary group membership

Add-ADGroupMember -Identity "Domain Admins" -Members "admin-temp" -MemberTimeToLive (New-TimeSpan -Hours 4)

# Automatic removal after 4 hours

# Session recording for privileged access
# Enable via FortiAuthenticator or PAM solution

# Break-glass accounts (emergency only)
# Store credentials in sealed envelope in CISO safe
# Audit all usage
```

## Verification
| Check | Method | Expected Result |
|-------|--------|-----------------|
| Account Creation | AD Users & Computers | Account exists, enabled |
| ZTNA Access | FortiAuthenticator | User in correct groups |
| Offboarding | AD Users & Computers | Account disabled |
| Access Review | Review documentation | Completed quarterly |
| Password Policy | Group Policy | Complexity enforced |

## Rollback
If wrong access granted:
1. Immediately revoke incorrect permissions
2. Document incident
3. Grant correct access
4. Review process for improvement

## Escalation Matrix
| Issue | Contact | Response Time |
|-------|---------|---------------|
| Urgent access needed | IT Manager | 30 minutes |
| Offboarding issue | Security Admin | 1 hour |
| Privileged access request | IT Manager | 4 hours |

## Related Documents
- SOP-007: Security Operations
- SOP-009: Change Management
- ISO 27001 Access Control Policy

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 22-Mar-2026 | VConfi | Initial release |

---

# SOP-011: Vendor Management

## Purpose
To establish standardized procedures for vendor relationship management, support escalation, hardware RMA, and license tracking to ensure timely resolution of issues and compliance with contractual obligations.

## Scope
This SOP covers:
- Vendor contact directory
- Escalation procedures per vendor
- Support ticket creation
- Hardware RMA process
- License renewal tracking

## Responsibility
| Role | Responsibility |
|------|----------------|
| Vendor Manager | Relationship management, escalations |
| Technical Lead | Technical support engagement |
| Procurement | RMA coordination, license renewals |
| IT Manager | Contract negotiation, major escalations |

## Prerequisites
- Vendor contract documentation
- Support entitlement verification
- Asset inventory
- License inventory
- Escalation contact list

## Procedure

### 1. Vendor Contact Directory

#### 1.1 Critical Vendor Contacts
```
VENDOR CONTACT DIRECTORY
━━━━━━━━━━━━━━━━━━━━━━━━
Last Updated: ___________

NETWORK & SECURITY
──────────────────
Fortinet (FortiGate, ZTNA, FortiClient)
├─ Technical Support: support.fortinet.com
├─ Phone (India): +91-000-000-0000
├─ Account Manager: ________________________
├─ TAC Priority: P1=1hr, P2=4hr, P3=1day
└─ Contract #: ________________________

HPE Aruba (Switches)
├─ Technical Support: 1800-425-4333
├─ Support Portal: support.hpe.com
├─ Account Manager: ________________________
├─ Serial Numbers: SW1: _________ SW2: _________
└─ Contract #: ________________________

STORAGE & SERVERS
─────────────────
Synology (NAS)
├─ Technical Support: support.synology.com
├─ Phone (Global): +886-2-2955-3888
├─ Local Partner: ________________________
├─ Serial Numbers: See asset inventory
└─ Warranty: 5-Year

Dell (PowerEdge R760)
├─ Technical Support: 1800-425-4026
├─ Support Portal: dell.com/support
├─ ProSupport Contract: ________________________
├─ Service Tag: ________________________
└─ Warranty: 5-Year ProSupport

VMware (vSphere)
├─ Technical Support: support.vmware.com
├─ Phone: 000-800-040-1563
├─ License Keys: See license inventory
└─ Support Level: Production

SOFTWARE & SERVICES
───────────────────
Veeam (Backup)
├─ Technical Support: support.veeam.com
├─ Phone: Check regional numbers
├─ License: ________________________
└─ Support Level: Standard

Wasabi (Cloud Storage)
├─ Technical Support: wasabi.com/help
├─ Account ID: ________________________
└─ Billing: ________________________

Zabbix (Monitoring)
├─ Technical Support: zabbix.com/support
├─ Enterprise Contract: ________________________
└─ License: Open Source (Commercial Support)

Kaspersky (Endpoint Protection)
├─ Technical Support: support.kaspersky.com
├─ License: ________________________
└─ Admin Console: ________________________
```

### 2. Escalation Procedures

#### 2.1 Support Escalation Matrix
| Vendor | L1 (Initial) | L2 (Escalation) | L3 (Management) |
|--------|--------------|-----------------|-----------------|
| Fortinet | Web ticket | Phone P1 | Account Manager |
| HPE | Phone 1800# | Technical PM | Account Manager |
| Synology | Web ticket | Phone +886 | Local partner |
| Dell | Web/Phone | ProSupport | TAM |
| VMware | Web SR | Phone P1 | Account Team |

#### 2.2 Escalation Timeline
```
Support Escalation Timeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━
T+0    Incident reported to vendor
T+1h   No response → Escalate to phone
T+4h   No resolution → Escalate to manager
T+8h   Critical issue unresolved → Executive escalation
T+24h  Any P1 unresolved → Contract review
```

### 3. Support Ticket Creation

#### 3.1 Ticket Creation Best Practices
```
SUPPORT TICKET TEMPLATE
━━━━━━━━━━━━━━━━━━━━━━━━
Subject: [B2H Studios] [Severity] [Brief Description]

Customer Info:
Company: B2H Studios
Contract #: ___________
Serial/Service Tag: ___________

Issue Description:
[Clear, concise description of the problem]

Environment:
- Hardware Model: ___________
- Firmware/Software Version: ___________
- Configuration: [Brief relevant config]
- Network Topology: [If applicable]

Steps to Reproduce:
1. ________________________________
2. ________________________________
3. ________________________________

Expected Result:
______________________________

Actual Result:
______________________________

Logs/Diagnostics Attached:
[ ] Configuration backup
[ ] Log files
[ ] Error screenshots
[ ] Network captures
[ ] Other: ___________

Business Impact:
[ ] Production down
[ ] Service degraded
[ ] Non-production issue

Contact:
Primary: ___________ Phone: ___________
Secondary: ___________ Phone: ___________
```

#### 3.2 Ticket Tracking
```bash
# Maintain ticket log
cat >> /var/log/vendor-tickets.csv << EOF
$(date +%Y-%m-%d),[Vendor],[Ticket#],[Description],[Status],[Owner]
EOF

# Weekly ticket review
# - Check for stale tickets (>7 days)
# - Verify no P1/P2 tickets unresolved
# - Escalate as needed
```

### 4. Hardware RMA Process

#### 4.1 RMA Decision Tree
```
Hardware Failure Detected
        │
        ▼
┌───────────────────┐
│ Under Warranty?   │
└─────────┬─────────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
┌───────┐   ┌───────────┐
│  Yes  │   │    No     │
└───┬───┘   └─────┬─────┘
    │             │
    ▼             ▼
┌───────────┐ ┌───────────┐
│ Initiate  │ │ Procure   │
│ RMA       │ │ New HW    │
│ (below)   │ │           │
└───────────┘ └───────────┘
```

#### 4.2 RMA Procedure
```
HARDWARE RMA CHECKLIST
━━━━━━━━━━━━━━━━━━━━━━
Failed Component: ________________________
Serial Number: ________________________
Failure Date: ________________________

Step 1: Gather Information
[ ] Exact error messages
[ ] Diagnostic output
[ ] Asset tag/serial number
[ ] Purchase date/warranty status

Step 2: Open Support Case
Vendor: ________________________
Ticket #: ________________________
Opened: ________________________

Step 3: Remote Diagnostics
[ ] Completed vendor diagnostics
[ ] Uploaded log files
[ ] Confirmed hardware failure

Step 4: RMA Approval
[ ] RMA number received: ___________
[ ] Advance replacement approved: [ ] Yes [ ] No
[ ] Cross-ship date: ___________

Step 5: Replacement
[ ] Replacement received: ___________
[ ] Installed and tested: ___________
[ ] Failed unit returned: ___________
[ ] RMA closed: ___________

Step 6: Update Records
[ ] Asset inventory updated
[ ] Warranty status updated
[ ] Spare parts inventory updated

Completed by: ___________ Date: _______
```

#### 4.3 Critical Spares Inventory
```
CRITICAL SPARES INVENTORY
━━━━━━━━━━━━━━━━━━━━━━━━━
Location: ________________________
Last Verified: ________________________

┌─────────────────────┬──────────┬──────────┬──────────────┐
│ Item                │ Quantity │ Location │ Expiry/Refresh│
├─────────────────────┼──────────┼──────────┼──────────────┤
│ HPE CX 6300M PSU    │    1     │ Shelf A  │ N/A          │
│ FortiGate 120G PSU  │    1     │ Shelf A  │ N/A          │
│ 10GbE SFP+ (HPE)    │    4     │ Bin 1    │ N/A          │
│ Cat6a Patch (3m)    │   10     │ Bin 2    │ N/A          │
│ LTO-9 Tapes         │    5     │ Safe     │ 2028-12-31   │
└─────────────────────┴──────────┴──────────┴──────────────┘

Note: Verify quarterly
```

### 5. License Renewal Tracking

#### 5.1 License Inventory
```
SOFTWARE LICENSE INVENTORY
━━━━━━━━━━━━━━━━━━━━━━━━━━
Last Updated: ___________

┌─────────────────┬──────────────┬──────────────┬──────────────┐
│ Product         │ License Key  │ Expiry Date  │ Renew Date   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ FortiGate UTP   │ XXXX-XXXX    │ 2027-03-22   │ 2027-02-22   │
│ VMware vSphere  │ XXXX-XXXX    │ 2027-03-22   │ 2027-02-22   │
│ Veeam Backup    │ XXXX-XXXX    │ 2027-03-22   │ 2027-02-22   │
│ Zabbix Support  │ ENT-XXXX     │ 2027-03-22   │ 2027-02-22   │
│ Signiant Jet    │ XXXX-XXXX    │ 2027-03-22   │ 2027-02-22   │
│ Splunk SIEM     │ XXXX-XXXX    │ 2027-03-22   │ 2027-02-22   │
│ Wasabi (200TB)  │ WAS-XXXX     │ Monthly      │ Auto         │
│ Kaspersky EP    │ KL-XXXX      │ 2027-03-22   │ 2027-02-22   │
└─────────────────┴──────────────┴──────────────┴──────────────┘

Renewal Reminder Schedule:
- 90 days before: Initial reminder
- 60 days before: Budget request
- 30 days before: PO submission
- 14 days before: Escalation if not ordered
- 7 days before: Emergency procurement
```

#### 5.2 Renewal Procedure
```
LICENSE RENEWAL CHECKLIST
━━━━━━━━━━━━━━━━━━━━━━━━━
Product: ________________________
Current Expiry: ________________________

Step 1: 90-Day Review
[ ] Verify current usage vs entitlement
[ ] Check for upgrade opportunities
[ ] Confirm budget availability
[ ] Initiate renewal quote request

Step 2: 60-Day Quote
[ ] Receive vendor quote
[ ] Compare pricing (3-year vs annual)
[ ] Verify contract terms
[ ] Obtain approval

Step 3: 30-Day Procurement
[ ] Submit PO
[ ] Receive license/key
[ ] Apply/update license
[ ] Verify activation

Step 4: Documentation
[ ] Update license inventory
[ ] Store license documentation
[ ] Update calendar for next renewal
[ ] Archive old licenses

Completed: ___________
```

## Verification
| Check | Method | Expected Result |
|-------|--------|-----------------|
| Contact Directory | Review | All vendors listed |
| Tickets | Ticket log | No stale tickets |
| RMA Status | Vendor portals | All closed |
| Licenses | Inventory | 60+ days until expiry |

## Rollback
Not applicable - vendor management is administrative

## Escalation Matrix
| Issue | Contact | Response Time |
|-------|---------|---------------|
| Vendor not responding | IT Manager | Immediate |
| License expired | Procurement | 4 hours |
| RMA delayed | Vendor Manager | 1 hour |

## Related Documents
- Vendor contracts
- Asset inventory
- License documentation
- Part4_Enhanced_BOM_Assets_Timeline.md

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 22-Mar-2026 | VConfi | Initial release |

---

# Document Control

## Version History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 22-Mar-2026 | VConfi | Initial release of all 11 SOPs |

## Approval
| Role | Name | Signature | Date |
|------|------|-----------|------|
| Solutions Architect | VConfi Solutions | [Digital] | March 22, 2026 |
| IT Manager | B2H Studios | _________________ | _______________ |
| Security Lead | VConfi Solutions | [Digital] | March 22, 2026 |

## Distribution List
| Role | Organization | Purpose |
|------|--------------|---------|
| IT Director | B2H Studios | Primary operational reference |
| Network Administrator | B2H Studios | SOP-001, SOP-002 |
| System Administrator | B2H Studios | SOP-003, SOP-004, SOP-005 |
| Storage Administrator | B2H Studios | SOP-004, SOP-005, SOP-006 |
| Security Administrator | B2H Studios | SOP-007, SOP-008 |
| IT Manager | B2H Studios | All SOPs |

---

*End of Part 6: Standard Operating Procedures*
*Document Version: 1.0*
*Classification: CONFIDENTIAL*
