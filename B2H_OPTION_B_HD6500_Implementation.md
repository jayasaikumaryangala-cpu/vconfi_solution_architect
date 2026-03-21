# B2H Studios — OPTION B Implementation Plan
## Synology HD6500 High-Capacity Architecture

---

**Document Control**

| Field | Detail |
|-------|--------|
| Client | B2H Studios |
| Solution | Option B — Synology HD6500 |
| Architecture | High-Capacity HDD, Cost-Optimized |
| Version | 1.0 |
| Date | March 2026 |
| Prepared By | VConfi Solutions Team |
| Classification | CONFIDENTIAL |

---

## Executive Summary

Option B delivers **maximum capacity at minimum cost** using Synology HD6500 high-density HDD storage. This solution is ideal for B2H Studios if:

- **Budget is constrained** (lowest upfront cost)
- **Proxy workflow** is acceptable (editors work locally)
- **Archive-heavy** use case (infrequently accessed footage)
- **Administrative simplicity** is valued (DSM vs OneFS)

### Important Limitations

⚠️ **Critical Constraint**: HD6500 cannot deliver real-time 4K/8K RAW editing. Editors MUST work on proxies stored locally.

---

## Architecture Overview

### Core Components

```
┌─────────────────────────────────────────────────────────────────┐
│              OPTION B — SYNOLOGY HD6500 ARCHITECTURE            │
│                   High-Capacity HDD Tier                        │
└─────────────────────────────────────────────────────────────────┘

Storage Layer (HDD-Based):
├─ Synology HD6500 (Site A Primary)
│  ├─ 60x 18TB SAS HDD = 1,080TB raw
│  ├─ RAID 6 = ~936TB usable
│  ├─ 4x 10GbE connectivity
│  └─ ~8-12ms latency (HDD typical)
│
├─ Synology HD6500 (Site B DR)
│  ├─ 60x 18TB SAS HDD = 1,080TB raw
│  ├─ Async replication from Site A
│  └─ Cold standby (manual failover)
│
SSD Cache:
├─ 4x 3.84TB NVMe SSD (read cache)
└─ Improves metadata operations only

Network Layer:
├─ HPE Aruba CX 6300M (10GbE core)
├─ 10GbE to editor workstations
└─ 10GbE storage network

Security:
├─ FortiGate 120G HA (ZTNA)
└─ DSM built-in firewall

Cloud Tier:
└─ Synology Hybrid Share → Wasabi
```

### Performance Specifications

| Metric | Specification | Note |
|--------|--------------|------|
| **Raw Capacity** | 1,080TB per site | Largest in class |
| **Usable Capacity** | ~936TB (RAID 6) | 2-drive fault tolerance |
| **Latency** | 8-12ms typical | HDD limitation |
| **Sequential Throughput** | 1.5-2 GB/s | 4x 10GbE aggregate |
| **IOPS** | ~500 (random 4K) | Not suitable for random workloads |
| **Concurrent 4K Streams** | 2-3 direct | Requires proxy workflow |
| **Editor Workflow** | Proxy-based | Local editing, NAS stores originals |

---

## Detailed Component Design

### 1.1 Synology HD6500 Configuration

**Hardware Specifications:**

```yaml
Synology HD6500 (Site A):
  Form Factor: 4U, 60-bay
  Drive Configuration:
    - 60x Seagate Exos X18 18TB SAS HDD
    - 4x 3.84TB NVMe SSD (read cache only)
    - RAID 6: 56 data + 4 parity drives
    - Hot spares: 2 drives (auto-rebuild)
    
  Usable Capacity:
    Raw: 1,080TB
    After RAID 6: ~936TB
    After filesystem: ~900TB
    
  Connectivity:
    - 4x 10GbE RJ45 (front-end)
    - 2x 25GbE SFP28 (replication/back-end)
    - LACP: 40 Gbps aggregate (4x 10GbE)
    
  Performance:
    Sequential Read: 1,800 MB/s
    Sequential Write: 1,500 MB/s
    Random Read: ~500 IOPS (HDD limitation)
    Latency: 8-12ms (seek time)
    
  Redundancy:
    - Dual PSU (2+2)
    - Dual fans (N+1)
    - RAID 6 (2-drive failure tolerance)
    - Battery-backed cache (BBU)
```

**Volume Design:**

```bash
# DSM Volume Configuration
Volume 1 (Active Projects):
  - RAID: 6 (56+4)
  - Size: ~400TB
  - Shared Folders:
    - /volume1/projects/active/
    - /volume1/projects/review/
    
Volume 2 (Archive):
  - RAID: 6 (same drive pool)
  - Size: ~500TB
  - Shared Folders:
    - /volume1/archive/
    - /volume1/deliverables/
    
SSD Cache:
  - Mode: Read-only
  - Size: 4x 3.84TB RAID 1 = ~7.5TB
  - Benefit: Metadata acceleration only
  - NOT suitable for file data caching
```

### 1.2 Network Architecture

**HPE Aruba CX 6300M Configuration:**

```bash
! VSX Stack Configuration
vsx
    system-mac 02:01:00:00:01:00
    inter-switch-link lag 256
    role primary

! HD6500 LACP Trunk
interface lag 1
    description "HD6500-Storage"
    lacp mode active
    vlan trunk native 1
    vlan trunk allowed 30
    spanning-tree port-type admin-edge
    mtu 9000

interface 1/1/49,1/1/50,2/1/49,2/1/50
    lag 1
```

**VLAN Design:**

| VLAN | Purpose | Subnet | Notes |
|------|---------|--------|-------|
| 10 | Management | 10.0.10.0/24 | OOB, switches, UPS |
| 20 | Editors | 10.0.20.0/24 | 25 workstations, 1GbE/10GbE |
| 30 | Storage | 10.0.30.0/24 | HD6500 access |
| 40 | Infrastructure | 10.0.40.0/24 | VMs, monitoring |

### 1.3 DSM Configuration

**Shared Folder Setup:**

```yaml
DSM Control Panel → Shared Folder:

projects_active:
  - Location: Volume 1
  - Purpose: Current production projects
  - Quota: None (monitor at volume level)
  - Snapshot: Every 2 hours, 24 copies
  - Replication: Real-time to Site B
  
archive:
  - Location: Volume 2
  - Purpose: Completed projects, deliverables
  - Quota: None
  - Snapshot: Daily, 30 copies
  - Hybrid Share: Enable (tier to Wasabi)
  
ingest:
  - Location: Volume 1
  - Purpose: Signiant Jet landing zone
  - Permissions: Signiant SDCX VM only
  - Cleanup: Auto-delete after 7 days
```

**Snapshot Configuration:**

```bash
# DSM Snapshot Replication
Snapshot Schedule:
  projects_active:
    - Every 2 hours
    - Retention: 24 snapshots (2 days)
    - Plus: Daily × 30 days
    - Plus: Monthly × 12 months
    
  archive:
    - Daily at 02:00
    - Retention: 30 snapshots
    - Lock critical snapshots (WORM)
```

---

## Workflow Design (Proxy-Based)

### 2.1 Editor Workflow (IMPORTANT)

```
┌─────────────────────────────────────────────────────────────┐
│              EDITOR WORKFLOW (PROXY-BASED)                   │
└─────────────────────────────────────────────────────────────┘

Step 1: Project Setup
  ├─ Editor downloads proxy files from NAS
  ├─ Proxies stored on local NVMe workstation
  └─ Full resolution files remain on HD6500

Step 2: Editing (Local)
  ├─ Editor works on local proxies (real-time)
  ├─ No network dependency during editing
  └─ Edit decision list (EDL) saved locally

Step 3: Conform/Finish
  ├─ Editor reconnects to NAS
  ├─ Project conforms to full-res originals
  └─ Color grade, VFX, final output

Step 4: Archive
  ├─ Final deliverables copied to NAS
  ├─ Project moves to archive tier
  └─ Local proxies deleted (auto-cleanup)

Latency Impact: MINIMAL (local proxies)
Capacity Impact: HIGH (duplicates on every workstation)
```

### 2.2 Proxy Generation Strategy

```bash
# Automated Proxy Generation
# Runs on Dell R760 application server

Source: /volume1/projects/active/[project]/originals/
Destination: /volume1/projects/active/[project]/proxies/

Proxy Formats:
  - ProRes 422 Proxy (editing)
  - H.264 1080p (review/dailies)
  
Automation:
  - Trigger: New file in ingest folder
  - Tool: FFmpeg or Adobe Media Encoder
  - Schedule: Continuous (queue-based)
  - Notification: Editor slack when ready
```

---

## Security Implementation

### 3.1 DSM Security Hardening

```bash
# DSM Security Advisor Checklist

1. Admin Account:
   [✓] Disable default 'admin' account
   [✓] Create named admin accounts
   [✓] Enable 2FA (TOTP or Secure SignIn)
   [✓] Admin sessions timeout: 15 minutes

2. Network Access:
   [✓] DSM management: VLAN 40 only
   [✓] SMB/NFS: VLAN 20 only
   [✓] No internet access to DSM

3. Firewall Rules:
   [✓] Enable DSM Firewall
   [✓] Allow SMB (445) from VLAN 20
   [✓] Allow NFS (2049, 111) from VLAN 20
   [✓] Deny all other inbound
   
4. Snapshot Protection:
   [✓] Enable Snapshot Replication
   [✓] Lock critical snapshots
   [✓] 30-day retention minimum
   
5. Encryption:
   [✓] Shared folder encryption (sensitive projects)
   [✓] AES-256 encryption keys in Vault
```

### 3.2 ZTNA Configuration

```bash
# FortiGate ZTNA for HD6500

config firewall policy
    edit 100
        set name "ZTNA-HD6500-Access"
        set srcintf "ssl-vpn"
        set dstintf "port3"
        set srcaddr "ZTNA-Editors"
        set dstaddr "HD6500-NAS"
        set action accept
        set schedule "always"
        set service "SMB" "NFS"
        set logtraffic all
        
        # DLP: Block high-res downloads
        config dlp sensor
            edit "block-high-res"
                config filter
                    edit 1
                        set type file-type
                        set file-type "video/*"
                        set action log-only
                    next
                end
            next
        end
    next
end
```

---

## Disaster Recovery

### 4.1 Synology Replication Manager

```bash
# Site A to Site B Replication

Replication Task 1: projects_active
  - Source: Site A HD6500
  - Destination: Site B HD6500
  - Mode: Real-time (5-minute intervals)
  - Compression: Enabled
  - Encryption: AES-256
  - Bandwidth throttle: 80% during business hours
  
Replication Task 2: archive
  - Source: Site A HD6500
  - Destination: Site B HD6500
  - Mode: Daily at 02:00
  - Incremental only
```

### 4.2 Failover Process (Manual)

| Step | Action | Duration | Owner |
|------|--------|----------|-------|
| 1 | Detect Site A failure | 5 min | Zabbix |
| 2 | IT Lead notification | 2 min | Automated |
| 3 | Promote Site B (DSM) | 5 min | IT Admin |
| 4 | Update ZTNA profiles | 5 min | IT Admin |
| 5 | DNS update | 2 min | IT Admin |
| 6 | Editor reconnection | 5 min | End users |
| **Total RTO** | | **~25 minutes** | |

⚠️ **Note**: Failover is MANUAL (not automatic) in Option B

---

## Implementation Timeline

### Phase 1: Site Preparation (Weeks 1-2)

| Task | Owner | Deliverable |
|------|-------|-------------|
| Rack preparation | Facilities | 42U rack space |
| Power installation | Electrical | 2x 16A circuits |
| Cooling check | HVAC | <28°C ambient |
| Network cabling | Network | CAT6A/fiber ready |

### Phase 2: HD6500 Deployment (Weeks 3-8)

| Week | Activity | Deliverable |
|------|----------|-------------|
| 3 | Hardware delivery | HD6500 on-site |
| 3-4 | Drive installation | 60 drives installed |
| 4 | DSM installation | System online |
| 5 | RAID initialization | Volume ready (~48 hours) |
| 5-6 | Network config | 10GbE active |
| 6 | Shared folders | SMB/NFS exports |
| 7 | Snapshot config | Replication active |
| 8 | Performance test | Baseline established |

### Phase 3: DR Site (Weeks 7-10)

| Week | Activity | Deliverable |
|------|----------|-------------|
| 7-8 | Site B hardware | HD6500 installed |
| 9 | Replication setup | Site A → Site B |
| 9 | Failover test | DR validated |
| 10 | Documentation | Runbooks complete |

### Phase 4: Integration (Weeks 9-12)

| Week | Activity | Deliverable |
|------|----------|-------------|
| 9 | Signiant Jet setup | Ingest working |
| 10 | ZTNA integration | Remote access |
| 11 | Wasabi Hybrid Share | Cloud tier active |
| 11 | Monitoring setup | Zabbix + DSM |
| 12 | Proxy workflow | Editor training |

### Phase 5: Go-Live (Weeks 13-14)

| Week | Activity | Deliverable |
|------|----------|-------------|
| 13 | Data migration | Production data |
| 13 | User training | Editors trained |
| 14 | Production cutover | Live operations |
| 14 | Hypercare | 24/7 support |

---

## Bill of Materials

### Hardware Costs

| Component | Specification | Qty | Unit Cost | Total |
|-----------|--------------|-----|-----------|-------|
| **Site A — Primary** | | | | |
| Synology HD6500 | 60-bay chassis | 1 | 6,50,000 | 6,50,000 |
| Seagate Exos X18 | 18TB SAS HDD | 60 | 42,000 | 25,20,000 |
| Synology SAT5210 | 3.84TB NVMe SSD | 4 | 65,000 | 2,60,000 |
| **Site B — DR** | | | | |
| Synology HD6500 | 60-bay chassis | 1 | 6,50,000 | 6,50,000 |
| Seagate Exos X18 | 18TB SAS HDD | 60 | 42,000 | 25,20,000 |
| Synology SAT5210 | 3.84TB NVMe SSD | 4 | 65,000 | 2,60,000 |
| **Network** | | | | |
| HPE Aruba CX 6300M | 48x10GbE + 4x25GbE | 4 | 3,50,000 | 14,00,000 |
| 10GbE NICs (editors) | Intel X550-T2 | 25 | 12,000 | 3,00,000 |
| DAC cables | 10GbE/25GbE | 50 | 3,500 | 1,75,000 |
| **Security** | | | | |
| FortiGate 120G | HA pair | 2 | 8,50,000 | 17,00,000 |
| FortiAuthenticator | MFA server | 1 | 2,50,000 | 2,50,000 |
| FortiAnalyzer | Log management | 1 | 3,50,000 | 3,50,000 |
| **Application Server** | | | | |
| Dell PowerEdge R760 | Signiant + VMs | 1 | 4,50,000 | 4,50,000 |
| **Power** | | | | |
| 10kVA UPS | APC Smart-UPS | 2 | 3,50,000 | 7,00,000 |
| **Services** | | | | |
| Implementation | 14-week deployment | 1 | 28,00,000 | 28,00,000 |
| Training | Admin + user training | 1 | 3,00,000 | 3,00,000 |
| **Subtotal** | | | | **1,54,55,000** |
| **GST (18%)** | | | | **27,81,900** |
| **TOTAL** | | | | **Rs. 1,82,36,900** |

### 5-Year TCO

| Year | Cost Component | Amount |
|------|---------------|--------|
| Year 1 | Initial deployment | 1.82 Cr |
| Year 2 | Support + maintenance | 35L |
| Year 3 | Drive replacements (predicted) | 25L |
| Year 4 | Support + maintenance | 40L |
| Year 5 | Support + maintenance | 45L |
| **5-Year Total** | | **3.27 Cr** |

*Note: Wasabi cloud storage costs additional ~Rs. 3L/year*

---

## Operational Runbooks

### SOP-HD-001: Daily Health Check

```bash
#!/bin/bash
# DSM Health Check Script

echo "=== HD6500 Health Check ==="
date

# System status
echo "System Status:"
synosystemctl status

# Drive health
echo -e "\nDrive Health:"
cat /proc/mdstat
smartctl -a /dev/sda | grep -E "(Reallocated|Current_Pending|Offline_Uncorrectable)"

# Volume usage
echo -e "\nVolume Usage:"
df -h | grep volume

# Network status
echo -e "\nNetwork:"
ip addr show | grep -E "(eth|bond)"

# Replication status
echo -e "\nReplication:"
synoreplicatool --status

# Temperature
echo -e "\nTemperature:"
cat /sys/class/thermal/thermal_zone*/temp
```

### SOP-HD-002: Drive Failure Response

1. **Detection**: DSM alert "Degraded Mode" or Zabbix alert
2. **Verify**: Storage Manager → HDD/SSD → check failed drive bay
3. **Response**:
   - Hot-swap failed drive (no downtime)
   - RAID rebuild starts automatically
4. **Monitor**: Rebuild progress in Storage Manager
5. **Timeline**: 18-24 hours for 18TB drive rebuild
6. **Order**: Replacement drive from vendor

---

## Acceptance Criteria

### Pre-Go-Live Checklist

- [ ] All 60 drives healthy and RAID synchronized
- [ ] Replication to Site B active
- [ ] 10GbE connectivity validated
- [ ] ZTNA authentication working
- [ ] Hybrid Share to Wasabi active
- [ ] Proxy generation workflow tested
- [ ] Snapshot verification passed
- [ ] DR failover tested (manual process)
- [ ] Documentation complete
- [ ] Staff training completed

### Performance Benchmarks

| Test | Target | Actual | Pass/Fail |
|------|--------|--------|-----------|
| Sequential Read | >1.5 GB/s | ___ | |
| Sequential Write | >1.2 GB/s | ___ | |
| Latency (avg) | <12ms | ___ | |
| Replication RPO | <15 min | ___ | |

---

## Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Performance unsatisfactory | Medium | High | Set expectations (proxy workflow) |
| Drive failure during rebuild | Low | Medium | RAID 6 (2-drive tolerance) |
| Long rebuild times | High | Medium | Hot spares, 18TB = 18-24 hours |
| Manual DR failover | Medium | High | Documented runbook, training |
| Proxy storage overflow | Medium | High | Local storage monitoring |

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | March 2026 | VConfi Team | Initial release |

---

**End of Document**

*VConfi Solutions — Cost-Optimized Infrastructure*
