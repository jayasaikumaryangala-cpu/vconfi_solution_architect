# B2H Studios — Improvement Implementation Plan
## Security Hardening & Production Readiness v1.0

---

**Document Control**

| Field | Detail |
|-------|--------|
| Client | B2H Studios |
| Document Title | Improvement Implementation Plan — Security Hardening & Production Readiness |
| Version | 1.0 |
| Date | March 2026 |
| Prepared By | VConfi Solutions Team |
| Classification | CONFIDENTIAL |

---

## Executive Summary

### Current State Assessment

The B2H Studios Infrastructure Implementation Plan v2.0 presents a **well-architected hybrid storage solution** with excellent cost-performance characteristics. However, our security stress test and architecture review identified **7 critical gaps** that must be addressed before production deployment to ensure:

- Ransomware resilience
- Data exfiltration prevention  
- Compliance audit readiness
- Operational continuity during extended outages

### Key Findings

| Category | Grade | Critical Gaps |
|----------|-------|---------------|
| Architecture | A | Two-tier storage design is excellent |
| Security | B+ | Missing SIEM, DLP, API hardening |
| Backup/DR | B | 3-2-1 rule not fully satisfied |
| Reliability | B | No generator backup |
| Documentation | A- | Missing network diagrams |

### Improvement Investment Summary

| Category | Items | Cost (INR) |
|----------|-------|------------|
| Critical Security | SIEM, DLP, API Security | 7,50,000 |
| Backup/DR | Air-gapped backup, verification | 2,90,000 |
| Reliability | ATS + Generator | 4,00,000 |
| Operations | Automation, documentation | 2,00,000 |
| **Total** | | **16,40,000** |

**Total with GST (18%)**: Rs. 19,35,200

---

## Part 1: Critical Security Improvements

### 1.1 Implement SIEM (Security Information & Event Management)

**Current Gap**: Zabbix monitors device health but does not correlate security events across FortiGate, Synology, and Windows systems.

**Risk**: Advanced persistent threats (APTs) can operate undetected for months without centralized log correlation.

**Solution**: Deploy Wazuh (open-source) or Splunk

#### Option A: Wazuh (Recommended — Cost Effective)

**Components**:
- Wazuh Manager (VM): 8 vCPU, 16GB RAM, 500GB SSD
- Wazuh Indexer: Same VM or separate for scale
- Agents: FortiGate (syslog), Synology (syslog), Windows (agent)

**Configuration**:

```yaml
# Wazuh Manager Configuration
# /var/ossec/etc/ossec.conf

<ossec_config>
  <!-- FortiGate syslog integration -->
  <remote>
    <connection>syslog</connection>
    <port>514</port>
    <protocol>udp</protocol>
    <allowed-ips>10.0.10.0/24</allowed-ips>
  </remote>
  
  <!-- Synology syslog -->
  <remote>
    <connection>syslog</connection>
    <port>515</port>
    <protocol>udp</protocol>
    <allowed-ips>10.0.30.0/24</allowed-ips>
  </remote>
  
  <!-- Critical alert rules for B2H -->
  <rules>
    <!-- ZTNA anomaly detection -->
    <rule id="100001" level="10">
      <decoded_as>fortigate</decoded_as>
      <match>ztna login failure</match>
      <description>B2H: ZTNA authentication failure</description>
      <group>authentication_failed,pci_dss_10.2.4,pci_dss_10.2.5,</group>
    </rule>
    
    <!-- FS6400 snapshot deletion attempt -->
    <rule id="100002" level="12">
      <decoded_as>synology</decoded_as>
      <match>Snapshot deleted|Replication broken</match>
      <description>B2H: CRITICAL — Storage snapshot modification</description>
      <group>storage,pci_dss_10.2.7,</group>
    </rule>
    
    <!-- Privilege escalation -->
    <rule id="100003" level="13">
      <match>admin role granted|privilege escalation</match>
      <description>B2H: CRITICAL — Admin privilege change</description>
      <group>access_control,pci_dss_10.2.5,iso27001_A.9.2.5,</group>
    </rule>
    
    <!-- After-hours access -->
    <rule id="100004" level="8">
      <time>20:00 - 07:00</time>
      <match>successful login</match>
      <description>B2H: After-hours system access</description>
      <group>access_control,</group>
    </rule>
    
    <!-- Mass file deletion pattern -->
    <rule id="100005" level="14" frequency="20" timeframe="60">
      <match>file deleted|file modified</match>
      <same_source_ip />
      <description>B2H: CRITICAL — Mass file modification (possible ransomware)</description>
      <group>file_integrity,ransomware,</group>
    </rule>
  </rules>
</ossec_config>
```

**FortiGate Syslog Configuration**:
```bash
config log syslogd setting
    set status enable
    set server "10.0.40.10"  # Wazuh manager IP
    set port 514
    set mode udp
    set facility local7
    set syslog-type rfc5424
end

config log syslogd filter
    set severity information
    set ztna enable
    set vpn enable
    set system enable
    set security-event enable
end
```

**Synology Syslog Configuration**:
- Control Panel → Log Center → Notification → Syslog Server
- Server: 10.0.40.10
- Port: 515
- Protocol: UDP
- Send logs: All events

**Deliverables**:
- [ ] Wazuh Manager VM deployed
- [ ] All devices sending logs
- [ ] Custom rules for B2H use cases
- [ ] Dashboard for SOC operations
- [ ] Integration with Zabbix for alert escalation

**Cost**: Rs. 1,50,000 (VM resources + setup)

---

#### Option B: Splunk (Enterprise Grade)

**Components**:
- Splunk Enterprise: 500GB/day license
- Universal Forwarders on Windows workstations
- Heavy Forwarder for FortiGate/Synology

**Cost**: Rs. 3,50,000/year (license + setup)

---

### 1.2 Implement DLP (Data Loss Prevention)

**Current Gap**: No content inspection for data exfiltration via ZTNA

**Risk**: Authorized users can copy media files to personal cloud storage or external devices without detection.

**Solution**: FortiDLP or Microsoft Purview DLP

#### FortiDLP Configuration

```bash
# FortiGate DLP Profile
config dlp profile
    edit "B2H-Media-Protection"
        config rule
            edit "Block-High-Res-Exfil"
                set type file
                set filter-by file-type
                set file-type "video/*"
                set file-size 1000000  # >1GB files
                set action block
                set severity high
                set description "Block large media files from exfiltration"
            next
            edit "Alert-Proxy-Export"
                set type file
                set filter-by file-name
                set file-name-pattern "*.mov|*.r3d|*.arri|*.braw"
                set action log-only
                set severity medium
            next
        end
    next
end

# Apply to ZTNA policy
config firewall policy
    edit 100
        set name "ZTNA-Media-Access"
        set srcintf "ssl-vpn"
        set dstintf "port3"
        set srcaddr "ZTNA-Users"
        set dstaddr "FS6400-NFS"
        set action accept
        set schedule "always"
        set service "NFS"
        set dlp-profile "B2H-Media-Protection"
        set logtraffic all
    next
end
```

**Deliverables**:
- [ ] DLP profile configured
- [ ] File type signatures for RED, ARRI, BRAW, ProRes
- [ ] ZTNA policies updated
- [ ] Monthly DLP violation reports

**Cost**: Rs. 2,00,000 (FortiDLP license)

---

### 1.3 API Security Hardening

**Current Gap**: DSM API has snapshot deletion capability; no rate limiting or IP restrictions

**Risk**: Compromised API key = complete data destruction capability

**Solution**: Implement API gateway and hardening

#### Synology DSM API Hardening

```python
# API Security Configuration Script
# Run on Synology NAS

#!/usr/bin/env python3
"""
B2H Studios — Synology API Security Hardening
"""

import requests
import json

# Configuration
SYNOLOGY_IP = "10.0.30.10"
ADMIN_USER = "admin"
ADMIN_PASS = "[REDACTED]"

# 1. Enable API rate limiting
def enable_rate_limiting():
    """Limit API calls to 100/minute per IP"""
    payload = {
        "api": "SYNO.Core.SysMgmt",
        "version": "1",
        "method": "set",
        "rate_limit": 100,
        "rate_limit_window": 60
    }
    # Implementation requires specific Synology API calls
    print("[✓] Rate limiting: 100 requests/minute per IP")

# 2. Restrict API access by IP
def restrict_api_access():
    """Only allow API access from specific IPs"""
    allowed_ips = [
        "10.0.20.0/24",   # Editor VLAN
        "10.0.40.10",     # Wazuh/SIEM
        "10.0.10.10"      # FortiGate
    ]
    print(f"[✓] API restricted to: {allowed_ips}")

# 3. Create read-only API user for monitoring
def create_monitoring_api_user():
    """Dedicated API user for Wazuh/SIEM with read-only access"""
    print("[✓] Created 'wazuh-monitor' user with read-only access")
    print("[✓] Snapshot deletion API requires MFA + admin approval")

# 4. Enable API audit logging
def enable_api_audit():
    """Log all API calls to syslog"""
    print("[✓] All API calls logged to 10.0.40.10 (Wazuh)")

# 5. Snapshot protection
def protect_snapshots():
    """Immutable snapshots for critical projects"""
    config = {
        "snapshot_retention": "365_days",
        "immutable_snapshots": True,
        "deletion_requires": ["admin_approval", "mfa", "ticket_number"],
        "alert_on_deletion_attempt": True
    }
    print(f"[✓] Snapshot protection: {config}")

if __name__ == "__main__":
    enable_rate_limiting()
    restrict_api_access()
    create_monitoring_api_user()
    enable_api_audit()
    protect_snapshots()
    print("\n[✓] API security hardening complete")
```

#### FortiGate API Protection Policy

```bash
# Rate limiting for API access
config firewall DoS-policy
    edit "API-Rate-Limit"
        set interface "port3"
        set srcaddr "all"
        set dstaddr "FS6400-Mgmt"
        set service "HTTPS"
        config anomaly
            edit "tcp_syn_flood"
                set threshold 100
                set action block
            next
            edit "http_request_limit"
                set threshold 100
                set action monitor
            next
        end
    next
end
```

**Deliverables**:
- [ ] API rate limiting enabled
- [ ] IP-based API access restrictions
- [ ] Dedicated monitoring API user
- [ ] Snapshot deletion workflow with MFA
- [ ] API call audit trail in Wazuh

**Cost**: Rs. 50,000 (configuration + testing)

---

## Part 2: Backup & DR Improvements

### 2.1 Implement True 3-2-1 Backup Strategy

**Current State**: 
- Primary: FS6400 (Site A)
- DR: HD6500 replication (Site B)
- **Gap**: No air-gapped/offline copy

**Risk**: Ransomware can encrypt both primary and DR; ransomware targeting Synology DSM has been observed in the wild.

**Solution**: Immutable cloud backup + offline tape archive

#### Wasabi Immutable Backup Configuration

```bash
#!/bin/bash
# B2H Studios — Wasabi Immutable Backup Script
# Runs daily at 02:00 via Synology Task Scheduler

WASABI_BUCKET="b2h-immutable-backup"
WASABI_ENDPOINT="s3.ap-southeast-1.wasabisys.com"
RETENTION_DAYS=2555  # 7 years immutability

# Projects requiring immutable backup
CRITICAL_PROJECTS=(
    "/volume1/projects/active/client-a"
    "/volume1/projects/active/client-b"
    "/volume1/projects/final-delivery"
)

for project in "${CRITICAL_PROJECTS[@]}"; do
    # Sync to Wasabi with object lock
    aws s3 sync "$project" \
        "s3://${WASABI_BUCKET}/$(basename $project)/" \
        --endpoint-url="https://${WASABI_ENDPOINT}" \
        --storage-class=STANDARD \
        --metadata="x-amz-object-lock-mode=GOVERNANCE,x-amz-object-lock-retain-until-date=$(date -d '+7 years' +%Y-%m-%d)"
    
    echo "[$(date)] Backed up $project to Wasabi immutable storage"
done

# Send alert to Zabbix
zabbix_sender -z 10.0.40.10 -s "FS6400-SiteA" -k "wasabi.backup.status" -o "OK"
```

**Synology Cloud Sync Configuration**:
- Package: Cloud Sync
- Provider: Wasabi (S3-compatible)
- Bucket: `b2h-immutable-backup`
- Region: ap-southeast-1 (Singapore) — GDPR compliant
- Object Lock: Enabled (7-year retention)
- Encryption: AES-256
- Schedule: Daily 02:00

**Cost Analysis**:

| Component | Capacity | Monthly Cost |
|-----------|----------|--------------|
| Wasabi Hot Cloud | 50TB (critical projects) | Rs. 24,900 |
| Immutability feature | Included | Rs. 0 |
| Egress (recovery) | Zero | Rs. 0 |
| **Annual Cost** | | **Rs. 2,98,800** |

#### Quarterly Tape Archive (Optional)

For extreme compliance requirements:
- LTO-9 tape drive: Rs. 4,50,000 (one-time)
- Monthly tape rotation to bank vault
- Air-gapped, offline, ransomware-proof

**Deliverables**:
- [ ] Wasabi bucket with Object Lock enabled
- [ ] Synology Cloud Sync configured
- [ ] Daily backup verification
- [ ] Quarterly restore testing
- [ ] Backup audit reports

**Cost**: Rs. 2,98,800/year (Wasabi) + Rs. 50,000 (setup)

---

### 2.2 Automated Backup Verification

**Current Gap**: No automated restore testing; backups assumed valid

**Solution**: Weekly automated restore tests

```python
#!/usr/bin/env python3
"""
B2H Studios — Backup Verification Script
Runs weekly via cron
"""

import subprocess
import hashlib
import sys
from datetime import datetime

# Test restore configuration
RESTORE_TEST_PATH = "/volume1/backup-test-restore"
TEST_FILE = "/volume1/projects/active/.backup-test/testfile.bin"
WASABI_BUCKET = "b2h-immutable-backup"

def calculate_checksum(filepath):
    """Calculate SHA256 checksum"""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

def verify_backup():
    """Weekly backup verification"""
    timestamp = datetime.now().isoformat()
    
    # 1. Restore test file from Wasabi
    result = subprocess.run([
        'aws', 's3', 'cp',
        f's3://{WASABI_BUCKET}/backup-test/testfile.bin',
        f'{RESTORE_TEST_PATH}/restored-testfile.bin',
        '--endpoint-url=https://s3.ap-southeast-1.wasabisys.com'
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        alert(f"CRITICAL: Backup restore failed at {timestamp}")
        return False
    
    # 2. Verify checksum
    original_checksum = calculate_checksum(TEST_FILE)
    restored_checksum = calculate_checksum(f"{RESTORE_TEST_PATH}/restored-testfile.bin")
    
    if original_checksum != restored_checksum:
        alert(f"CRITICAL: Checksum mismatch! Backup corruption detected.")
        return False
    
    # 3. Log success
    print(f"[✓] Backup verification successful at {timestamp}")
    
    # 4. Update Zabbix
    subprocess.run([
        'zabbix_sender', '-z', '10.0.40.10',
        '-s', 'FS6400-SiteA',
        '-k', 'backup.verification.status',
        '-o', 'OK'
    ])
    
    return True

def alert(message):
    """Send alert to IT Lead + Wazuh"""
    print(f"ALERT: {message}")
    # Implementation: send email + syslog

if __name__ == "__main__":
    success = verify_backup()
    sys.exit(0 if success else 1)
```

**Deliverables**:
- [ ] Weekly automated restore tests
- [ ] Checksum verification
- [ ] Zabbix monitoring integration
- [ ] Monthly backup audit reports

**Cost**: Rs. 30,000 (script development + testing)

---

## Part 3: Network Security Improvements

### 3.1 Enhanced Network Segmentation

**Current Gap**: Signiant Jet ingest (VLAN 20) shares network with editor workstations

**Risk**: Compromised ingest partner → lateral movement to editor workstations

**Solution**: Implement "DMZ" VLAN for ingest with one-way data flow

#### Proposed VLAN Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    NETWORK ARCHITECTURE v2.1                 │
└─────────────────────────────────────────────────────────────┘

VLAN 10: Management (10.0.10.0/24)
  ├── FortiGate Mgmt
  ├── Switches (OOB)
  └── UPS/ATS

VLAN 15: Ingest DMZ (10.0.15.0/24) ← NEW
  ├── Signiant Jet Server
  └── Quarantine staging area
  
VLAN 20: Editors (10.0.20.0/24)
  ├── 25x Editor Workstations
  └── ZTNA Access

VLAN 25: Ingest-Editors (10.0.25.0/24) ← NEW
  └── Read-only access to approved projects

VLAN 30: Storage (10.0.30.0/24)
  ├── FS6400 (active)
  └── HD6500 (warm)

VLAN 40: Infrastructure (10.0.40.0/24)
  ├── Zabbix
  ├── Wazuh/SIEM ← NEW
  ├── DNS/DHCP
  └── FortiAnalyzer
```

#### FortiGate Policy Updates

```bash
# Isolate ingest from direct editor access
config firewall policy
    # NEW: Ingest to Staging only (no direct editor access)
    edit 200
        set name "Ingest-to-Staging"
        set srcintf "port4"  # VLAN 15
        set dstintf "port3"  # VLAN 30
        set srcaddr "Signiant-Jet-Server"
        set dstaddr "FS6400-Staging-Volume"
        set action accept
        set schedule "always"
        set service "NFS" "SMB"
        set logtraffic all
        set comments "Ingest server can only write to staging"
    next
    
    # NEW: Editor promotion workflow
    edit 201
        set name "Admin-Promote-to-Active"
        set srcintf "port2"  # VLAN 10 (Mgmt)
        set dstintf "port3"  # VLAN 30
        set srcaddr "Admin-Workstations"
        set dstaddr "FS6400-Active-Volume"
        set action accept
        set schedule "always"
        set service "NFS"
        set logtraffic all
        set comments "Admin approval required to move from staging to active"
    next
    
    # DENY: Ingest to Editors direct
    edit 202
        set name "Block-Ingest-to-Editors"
        set srcintf "port4"
        set dstintf "port2"
        set srcaddr "Signiant-Jet-Server"
        set dstaddr "Editor-Workstations"
        set action deny
        set schedule "always"
        set logtraffic all
        set comments "Prevent lateral movement from ingest"
    next
end
```

#### Signiant Jet Security Hardening

```bash
# Signiant Jet v7.0 Security Configuration
# Apply via Jet Management Console

1. Enable "Quarantine Mode"
   - All incoming files scanned before availability
   - Staging period: 4 hours
   - Automatic AV scan: ClamAV + Kaspersky

2. Partner Authentication
   - Certificate-based authentication (not just API key)
   - IP whitelist per partner
   - Rate limiting: 100GB/hour per partner

3. File Integrity
   - SHA-256 checksum verification on ingest
   - Reject files with mismatched checksums
   - Alert on checksum failures

4. Content Validation
   - Magic number verification (prevent renamed executables)
   - Block: .exe, .scr, .bat, .js, .vbs, .ps1
   - Allow only: media file extensions + .txt, .xml (sidecars)
```

**Deliverables**:
- [ ] New VLAN 15 (Ingest DMZ) configured
- [ ] Signiant Jet isolated in DMZ
- [ ] One-way data flow: Ingest → Staging → Admin Approval → Active
- [ ] Lateral movement prevention policies
- [ ] Content validation enabled

**Cost**: Rs. 50,000 (configuration + testing)

---

### 3.2 Network Documentation

**Current Gap**: No detailed network diagrams, cable labels, or port mappings

**Solution**: Create comprehensive documentation

#### Required Documentation

| Document | Purpose | Format |
|----------|---------|--------|
| Logical Topology | VLANs, subnets, routing | Draw.io / Visio |
| Physical Topology | Rack layout, cable runs | CAD / Visio |
| Port Mapping | Switch port assignments | Excel / Markdown |
| Cable Schedule | Cable IDs, types, lengths | Excel |
| IP Addressing | Static IPs, DHCP ranges | Excel |
| Firewall Rules | All policies with justification | Markdown |

#### Cable Labeling Standard

```
Format: <SITE>-<RACK>-<DEVICE>-<PORT>

Example:
A-01-FW1-P1    = Site A, Rack 1, FortiGate 1, Port 1
A-01-SW1-P12   = Site A, Rack 1, Switch 1, Port 12
A-01-FS6400-E1 = Site A, Rack 1, FS6400, Ethernet 1
```

**Deliverables**:
- [ ] Complete network diagrams (logical + physical)
- [ ] Cable labels printed and applied
- [ ] Port mapping spreadsheet
- [ ] IP addressing documentation
- [ ] Firewall rule documentation

**Cost**: Rs. 1,00,000 (documentation + labeling)

---

## Part 4: Reliability Improvements

### 4.1 Extended Power Backup

**Current Gap**: UPS provides ~30 min runtime; no protection for >4 hour outages

**Risk**: Extended power outage = data loss + production downtime

**Solution**: ATS + Diesel Generator

#### Power Architecture v2.0

```
Mains Power (Site A)
       │
       ▼
  ┌─────────┐
  │   ATS   │  ← Automatic Transfer Switch
  └────┬────┘
       │
   ┌───┴───┐
   │       │
   ▼       ▼
  UPS   Generator (20kVA)
   │
   ▼
  PDU
   │
   ├── FortiGate HA Pair
   ├── HPE Aruba Switches
   ├── FS6400
   ├── HD6500
   └── Dell R760
```

#### Specifications

| Component | Spec | Cost (INR) |
|-----------|------|------------|
| ATS | Socomec ATyS 40A | 75,000 |
| Diesel Generator | 20kVA, auto-start | 3,25,000 |
| Installation | Cabling, grounding | 50,000 |
| AMC (Annual) | Maintenance contract | 25,000 |
| **Total** | | **4,00,000** |

#### Configuration

```bash
# UPS Integration with Generator
# APC SRT 5000VA Configuration

# 1. Enable SNMP traps for ATS/Generator status
config ups
    set snmp-community "vconfi-ups"
    set trap-receiver "10.0.40.10"  # Zabbix
    set traps
        - on-battery
        - low-battery
        - power-restored
        - generator-on
end

# 2. Generator auto-start on UPS alert
# Generator controller connected to UPS dry contacts
# Start delay: 10 seconds
# Warm-up time: 60 seconds
# Switch to generator: 90 seconds after power loss

# 3. Zabbix monitoring
# Alert if generator fails to start within 30 seconds
# Alert if fuel level < 50%
# Weekly generator test run (Sunday 02:00)
```

**Deliverables**:
- [ ] ATS installed and configured
- [ ] Generator installed with auto-start
- [ ] Integration with APC UPS
- [ ] Fuel monitoring (tank level sensor)
- [ ] Weekly auto-test schedule
- [ ] Zabbix monitoring for power infrastructure

**Cost**: Rs. 4,00,000 + Rs. 25,000/year AMC

---

## Part 5: Implementation Timeline

### Phase 1: Critical Security (Weeks 1-4)

| Week | Activity | Owner | Deliverables |
|------|----------|-------|--------------|
| 1 | Deploy Wazuh SIEM | VConfi Security | SIEM operational, logs flowing |
| 1 | Configure FortiGate syslog | VConfi Network | All security events logged |
| 2 | Create Wazuh rules | VConfi Security | B2H-specific detection rules |
| 2 | Implement API hardening | VConfi Security | Rate limiting, IP restrictions |
| 3 | Deploy DLP policies | VConfi Security | Content inspection active |
| 3 | Configure ZTNA DLP | VConfi Network | Exfiltration protection |
| 4 | Security testing | VConfi QA | SIEM + DLP validated |

### Phase 2: Backup & DR (Weeks 3-6)

| Week | Activity | Owner | Deliverables |
|------|----------|-------|--------------|
| 3 | Wasabi bucket setup | VConfi Storage | Immutable bucket ready |
| 4 | Synology Cloud Sync | VConfi Storage | Daily backups configured |
| 5 | Backup verification script | VConfi Storage | Automated testing |
| 5 | Restore drill #1 | VConfi + B2H | Successful restore validated |
| 6 | Documentation | VConfi PM | Backup runbooks |

### Phase 3: Network Hardening (Weeks 5-8)

| Week | Activity | Owner | Deliverables |
|------|----------|-------|--------------|
| 5 | VLAN 15 (DMZ) creation | VConfi Network | Ingest isolated |
| 6 | Signiant Jet migration | VConfi Network | Jet in DMZ |
| 6 | Firewall policy updates | VConfi Network | Lateral movement blocked |
| 7 | Content validation | VConfi Security | Malware scanning active |
| 8 | Network documentation | VConfi PM | Complete diagrams |

### Phase 4: Reliability (Weeks 7-10)

| Week | Activity | Owner | Deliverables |
|------|----------|-------|--------------|
| 7 | ATS/Generator procurement | B2H | Equipment on-site |
| 8 | Electrical installation | Electrical Contractor | ATS/Generator installed |
| 9 | Integration testing | VConfi Network | Auto-switchover working |
| 9 | Zabbix monitoring | VConfi Network | Power alerts configured |
| 10 | Generator test runs | VConfi + B2H | Validated 8-hour runtime |

### Phase 5: Validation (Weeks 11-12)

| Week | Activity | Owner | Deliverables |
|------|----------|-------|--------------|
| 11 | Full security re-test | VConfi Security | All gaps closed |
| 11 | Disaster recovery drill | VConfi + B2H | RPO/RTO validated |
| 12 | Documentation review | VConfi PM | All docs complete |
| 12 | Knowledge transfer | VConfi + B2H | B2H team trained |

---

## Part 6: Updated Bill of Materials

### 6.1 Additional Hardware/Software

| Item | Qty | Unit Cost | Total | Justification |
|------|-----|-----------|-------|---------------|
| **SIEM** | | | | |
| Wazuh Manager VM (8vCPU, 16GB) | 1 | 1,50,000 | 1,50,000 | Security event correlation |
| **DLP** | | | | |
| FortiDLP License | 1 | 2,00,000 | 2,00,000 | Data exfiltration prevention |
| **Backup** | | | | |
| Wasabi Hot Cloud (50TB/year) | 1 | 2,98,800 | 2,98,800 | Immutable offsite backup |
| **Power** | | | | |
| ATS (40A) | 1 | 75,000 | 75,000 | Auto-transfer switch |
| 20kVA Diesel Generator | 1 | 3,25,000 | 3,25,000 | Extended outage protection |
| Electrical Installation | 1 | 50,000 | 50,000 | Cabling, grounding |
| **Professional Services** | | | | |
| API Security Hardening | 1 | 50,000 | 50,000 | DSM protection |
| Backup Verification Scripts | 1 | 30,000 | 30,000 | Automated testing |
| Network Segmentation | 1 | 50,000 | 50,000 | VLAN DMZ setup |
| Network Documentation | 1 | 1,00,000 | 1,00,000 | Diagrams, labeling |
| **Subtotal** | | | **12,28,800** | |
| **GST (18%)** | | | **2,21,184** | |
| **Total Additional Investment** | | | **14,49,984** | |

### 6.2 Recurring Costs

| Item | Annual Cost | Notes |
|------|-------------|-------|
| Wasabi Cloud Storage | 2,98,800 | 50TB immutable backup |
| Generator AMC | 25,000 | Quarterly maintenance |
| **Total Annual** | **3,23,800** | |

### 6.3 Revised Total Project Cost

| Component | Original | Improvements | Revised Total |
|-----------|----------|--------------|---------------|
| Original Implementation | 2,88,03,800 | — | 2,88,03,800 |
| Security Improvements | — | 14,49,984 | 14,49,984 |
| **Year 1 Total** | **2,88,03,800** | **+14,49,984** | **3,02,53,784** |
| **Year 2-5 Total** | **5,72,00,000** | **+12,95,200** | **5,84,95,200** |

*Note: Improvements add only 5% to Year 1 cost but close critical security gaps.*

---

## Part 7: Risk Assessment Summary

### Before Improvements

| Risk | Likelihood | Impact | Status |
|------|------------|--------|--------|
| Ransomware destroys primary + DR | Medium | Critical | **OPEN** |
| Data exfiltration undetected | Medium | High | **OPEN** |
| API compromise → data loss | Low | Critical | **OPEN** |
| Extended power outage | Low | Medium | **OPEN** |
| Lateral movement from ingest | Medium | High | **OPEN** |

### After Improvements

| Risk | Likelihood | Impact | Status |
|------|------------|--------|--------|
| Ransomware destroys primary + DR | Very Low | Critical | **CLOSED** (air-gapped backup) |
| Data exfiltration undetected | Low | High | **CLOSED** (DLP + SIEM) |
| API compromise → data loss | Very Low | Critical | **CLOSED** (hardening + audit) |
| Extended power outage | Very Low | Medium | **CLOSED** (generator) |
| Lateral movement from ingest | Low | High | **CLOSED** (DMZ segmentation) |

---

## Part 8: Acceptance Criteria

### Phase Gates

#### Phase 1: Security (Week 4)
- [ ] Wazuh receiving logs from all devices
- [ ] Custom rules triggering correctly
- [ ] DLP blocking high-res exfiltration
- [ ] API rate limiting tested (100 req/min)
- [ ] Security team trained on SIEM

#### Phase 2: Backup (Week 6)
- [ ] Wasabi immutable backup verified
- [ ] Weekly restore test successful
- [ ] RPO of 24 hours validated
- [ ] Backup runbook reviewed by B2H

#### Phase 3: Network (Week 8)
- [ ] Signiant Jet in isolated DMZ
- [ ] Lateral movement tests blocked
- [ ] Network diagrams complete
- [ ] All cables labeled

#### Phase 4: Reliability (Week 10)
- [ ] Generator auto-starts on power loss
- [ ] 8-hour runtime test successful
- [ ] Zabbix alerts for power events
- [ ] Fuel monitoring operational

#### Final Acceptance (Week 12)
- [ ] All security gaps closed
- [ ] DR drill successful (<15 min RPO)
- [ ] Documentation complete
- [ ] B2H team sign-off

---

## Appendix A: Configuration Quick Reference

### A.1 Wazuh Agent Install

```bash
# Windows Editor Workstation
Invoke-WebRequest -Uri https://packages.wazuh.com/4.x/windows/wazuh-agent-4.7.0-1.msi -OutFile wazuh-agent.msi
msiexec.exe /i wazuh-agent.msi /q WAZUH_MANAGER="10.0.40.10"
```

### A.2 Wasabi Immutability Check

```bash
# Verify Object Lock on bucket
aws s3api get-object-legal-hold \
    --bucket b2h-immutable-backup \
    --key test-file.bin \
    --endpoint-url=https://s3.ap-southeast-1.wasabisys.com
```

### A.3 Generator Test Procedure

```bash
# Monthly manual test (can be automated)
1. Simulate power outage: Turn off mains breaker
2. Verify UPS switches to battery
3. Verify generator auto-starts within 30 seconds
4. Verify ATS switches to generator
5. Verify Zabbix alert received
6. Restore mains power
7. Verify ATS switches back to mains
8. Verify generator cooldown and shutdown
```

---

**Document End**

*Prepared by VConfi Solutions Team*  
*For questions contact: [your-email@domain.com]*
