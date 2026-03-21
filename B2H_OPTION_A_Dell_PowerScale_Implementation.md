# B2H Studios — OPTION A Implementation Plan
## Dell PowerScale F710 All-NVMe Architecture

---

**Document Control**

| Field | Detail |
|-------|--------|
| Client | B2H Studios |
| Solution | Option A — Dell PowerScale F710 |
| Architecture | All-NVMe, High-Performance |
| Version | 1.0 |
| Date | March 2026 |
| Prepared By | VConfi Solutions Team |
| Classification | CONFIDENTIAL |

---

## Executive Summary

Option A delivers the **highest performance tier** for B2H Studios using Dell PowerScale F710 all-NVMe storage. This is the "no-compromise" solution for media studios requiring real-time 8K RAW editing with zero latency.

### When to Choose Option A

- **Maximum performance** is non-negotiable
- Budget allows for **premium infrastructure**
- Future-proofing for **8K/12K workflows**
- Preference for **Dell enterprise support**

---

## Architecture Overview

### Core Components

```
┌─────────────────────────────────────────────────────────────────┐
│              OPTION A — DELL POWERSCALE ARCHITECTURE            │
│                    All-NVMe Performance Tier                    │
└─────────────────────────────────────────────────────────────────┘

Storage Layer (All-NVMe):
├─ Dell PowerScale F710 (Site A)
│  ├─ 4 nodes × 46TB NVMe = 184TB usable
│  ├─ OneFS 9.x distributed filesystem
│  ├─ Sub-millisecond latency
│  └─ 25GbE/100GbE connectivity
│
├─ Dell PowerScale F710 (Site B DR)
│  ├─ 2 nodes × 46TB NVMe = 92TB usable
│  ├─ SyncIQ replication from Site A
│  └─ Hot-standby configuration
│
Network Layer:
├─ HPE Aruba CX 8360 (25GbE/100GbE core)
├─ 25GbE to editor workstations
└─ 100GbE to PowerScale backend

Security Layer:
├─ FortiGate 120G HA (ZTNA)
├─ FortiAuthenticator (MFA)
└─ FortiAnalyzer (centralized logging)

Cloud Tier:
└─ Dell CloudPools → Wasabi Hot Cloud
```

### Performance Specifications

| Metric | Specification |
|--------|--------------|
| **Raw Capacity** | 184TB per site |
| **Usable Capacity** | ~165TB (80% efficiency) |
| **Latency** | <0.5ms read, <1ms write |
| **Throughput** | 15+ GB/s aggregate |
| **IOPS** | 1,000,000+ mixed workload |
| **Concurrent 4K Streams** | 50+ |
| **Concurrent 8K Streams** | 25+ |

---

## Detailed Component Design

### 1.1 Dell PowerScale F710 Configuration

**Hardware Specs (Per Node):**

```yaml
Node Configuration:
  Model: Dell PowerScale F710
  Form Factor: 1U half-width (4 nodes = 2U)
  
  NVMe Drives:
    - 8x 7.68TB NVMe SSD per node
    - Total per node: 61.44TB raw
    
  Performance per Node:
    - Sequential Read: 4 GB/s
    - Sequential Write: 2.5 GB/s
    - Random Read (4K): 250K IOPS
    - Random Write (4K): 100K IOPS
    
  Network:
    - 2x 25GbE SFP28 (frontend)
    - 2x 100GbE QSFP28 (backend)
    
  Redundancy:
    - N+1 node redundancy
    - RAID equivalent: OneFS protection (2x)
```

**Cluster Configuration (Site A):**

```bash
# OneFS Cluster Setup
Cluster Name: B2H-PROD-PS
Node Count: 4
Total Raw: 245.76TB
Protection: +2d:1n (2 drives + 1 node)
Usable: ~165TB

# SmartPools Policies
SmartPool: FAST
  - NVMe SSD tier only
  - Data access pattern: Hot
  - Run jobs: Always

# CloudPools (Tiering)
CloudPool: ARCHIVE
  - Target: Wasabi Hot Cloud
  - Policy: Files >90 days inactive
  - Compression: LZ4
  - Encryption: AES-256
```

### 1.2 Network Architecture

**HPE Aruba CX 8360 Configuration:**

```bash
! Core Switch Configuration for PowerScale
hostname CORE-SW-A

! 100GbE Uplinks to PowerScale
interface 1/1/1-1/1/4
    description "PowerScale-Backend-100GbE"
    no shutdown
    mtu 9198
    
interface 1/1/5-1/1/28
    description "Editor-Workstations-25GbE"
    no shutdown
    mtu 9198
    
! LACP to PowerScale
interface lag 10
    description "PowerScale-Aggregate"
    trunk mode
    vlan trunk allowed 30
    lacp mode active
```

**VLAN Design:**

| VLAN | Purpose | Subnet | Notes |
|------|---------|--------|-------|
| 10 | Management | 10.0.10.0/24 | OOB management |
| 20 | Editors | 10.0.20.0/24 | 25 workstations |
| 30 | Storage | 10.0.30.0/24 | PowerScale access |
| 40 | Infrastructure | 10.0.40.0/24 | VMs, monitoring |

### 1.3 OneFS Configuration

**Access Zones:**

```bash
# Create Access Zones
isi zone zones create \
    --name=PRODUCTION \
    --path=/ifs/production \
    --allocation-state=COMPLY

# SMB Share for Windows Editors
isi smb shares create \
    --name=projects_active \
    --path=/ifs/production/active \
    --description="Active Projects — NVMe Tier"

# NFS Export for Linux/Mac
isi nfs exports create \
    --paths=/ifs/production/active \
    --clients=@10.0.20.0/24 \
    --read-write \
    --root-clients=@10.0.40.10

# Quotas per project
isi quota quotas create \
    --path=/ifs/production/active/project_a \
    --type=directory \
    --hard-threshold=10TB \
    --advisory-threshold=8TB
```

**CloudPools Integration:**

```bash
# Configure Wasabi as cloud tier
isi cloud accounts create \
    --name=wasabi_b2h \
    --type=S3 \
    --endpoint=s3.ap-southeast-1.wasabisys.com \
    --key-id=$WASABI_KEY \
    --secret-key=$WASABI_SECRET

# CloudPool policy
isi cloud pools create \
    --name=archive_tier \
    --account=wasabi_b2h \
    --bucket=b2h-powerscale-archive

# Filepool policy (auto-tier)
isi filepool policies create \
    --name=archive_old_projects \
    --template=ARCHIVE \
    --condition="(accessed >= 90 days)"
```

---

## Security Implementation

### 2.1 ZTNA Configuration

```bash
# FortiGate ZTNA for PowerScale Access
config firewall policy
    edit 100
        set name "ZTNA-PowerScale-Access"
        set srcintf "ssl-vpn"
        set dstintf "port3"
        set srcaddr "ZTNA-Editors"
        set dstaddr "PowerScale-NFS"
        set action accept
        set schedule "always"
        set service "NFS" "SMB"
        set utm-status enable
        set ssl-ssh-profile "deep-inspection"
        set ips-sensor "media-studio-default"
        set logtraffic all
        set nat disable
    next
end

# Device posture checks
config endpoint forticlient-ems
    set address "10.0.40.20"
    set admin-username "fortigate"
    set admin-password ENC AK1L9...
end
```

### 2.2 OneFS Security Hardening

```bash
# Disable insecure protocols
isi services nfs disable --node-type=all
isi services nfs3 disable --node-type=all
isi services smb1 disable --node-type=all

# Enable SMB signing
isi smb settings global modify \
    --support-signing=true \
    --reject-unencrypted-access=true

# Antivirus integration (ICAP)
isi antivirus icap settings modify \
    --enabled=true \
    --server=10.0.40.30 \
    --port=1344

# Audit logging
isi audit settings modify \
    --enabled=true \
    --syslog-forwarding-enabled=true \
    --syslog-server=10.0.40.10
```

---

## Disaster Recovery

### 3.1 SyncIQ Configuration

```bash
# Create replication policy
isi sync policies create \
    --name=PROD_TO_DR \
    --source-root-path=/ifs/production \
    --target-host=B2H-DR-PS.lab.local \
    --target-path=/ifs/dr_replica \
    --schedule="every 5 minutes" \
    --snapshot-sync-existing=true

# Enable sync failover
isi sync failover create \
    --policy=PROD_TO_DR \
    --name=ACTIVE_DR \
    --mode=manual

# Test failover procedure
isi sync failover test PROD_TO_DR
```

### 3.2 Failover Process

| Step | Action | Duration |
|------|--------|----------|
| 1 | Detect site failure | 30 seconds |
| 2 | Promote DR to writable | 2 minutes |
| 3 | Update DNS records | 1 minute |
| 4 | ZTNA reconnection | 2 minutes |
| 5 | Editor validation | 3 minutes |
| **Total RTO** | | **<10 minutes** |

---

## Implementation Timeline

### Phase 1: Site Preparation (Weeks 1-2)

| Task | Owner | Deliverable |
|------|-------|-------------|
| Rack installation | Facilities | 4x racks ready |
| Power installation | Electrical | 2x 16A circuits |
| Cooling verification | HVAC | <25°C ambient |
| Network cabling | Network team | CAT8/fiber installed |

### Phase 2: PowerScale Deployment (Weeks 3-6)

| Week | Activity | Deliverable |
|------|----------|-------------|
| 3 | Hardware delivery | F710 nodes on-site |
| 3-4 | Node installation | 4 nodes racked |
| 4 | OneFS installation | Cluster online |
| 5 | Network configuration | 25GbE/100GbE active |
| 5 | Access zones setup | SMB/NFS exports ready |
| 6 | Performance testing | Baseline established |

### Phase 3: DR Site (Weeks 7-10)

| Week | Activity | Deliverable |
|------|----------|-------------|
| 7-8 | Site B hardware install | 2-node cluster |
| 9 | SyncIQ configuration | Replication active |
| 9 | Failover testing | DR validated |
| 10 | Documentation | Runbooks complete |

### Phase 4: Security & Integration (Weeks 9-12)

| Week | Activity | Deliverable |
|------|----------|-------------|
| 9 | ZTNA integration | Secure remote access |
| 10 | CloudPools setup | Wasabi tier active |
| 11 | Monitoring setup | Zabbix + OneFS insights |
| 12 | Security hardening | Audit passed |

### Phase 5: Go-Live (Weeks 13-14)

| Week | Activity | Deliverable |
|------|----------|-------------|
| 13 | Data migration | Production data migrated |
| 13 | User training | Editors trained |
| 14 | Production cutover | Live operations |
| 14 | Hypercare | 24/7 support |

---

## Bill of Materials

### Hardware Costs

| Component | Specification | Qty | Unit Cost | Total |
|-----------|--------------|-----|-----------|-------|
| **Site A — Primary** | | | | |
| Dell PowerScale F710 | 4-node NVMe cluster | 1 | 4,85,00,000 | 4,85,00,000 |
| HPE Aruba CX 8360 | 25GbE/100GbE switch | 2 | 8,50,000 | 17,00,000 |
| **Site B — DR** | | | | |
| Dell PowerScale F710 | 2-node NVMe cluster | 1 | 2,42,50,000 | 2,42,50,000 |
| HPE Aruba CX 8360 | 25GbE/100GbE switch | 2 | 8,50,000 | 17,00,000 |
| **Network** | | | | |
| 25GbE NICs (editors) | Mellanox ConnectX-5 | 25 | 22,000 | 5,50,000 |
| DAC cables | 25GbE/100GbE | 50 | 5,000 | 2,50,000 |
| **Security** | | | | |
| FortiGate 120G | HA pair | 2 | 8,50,000 | 17,00,000 |
| FortiAuthenticator | MFA server | 1 | 2,50,000 | 2,50,000 |
| FortiAnalyzer | Log management | 1 | 3,50,000 | 3,50,000 |
| FortiClient EMS | Endpoint management | 1 | 1,50,000 | 1,50,000 |
| **Power** | | | | |
| 10kVA UPS | APC Smart-UPS | 4 | 3,50,000 | 14,00,000 |
| ATS | Auto-transfer switch | 2 | 75,000 | 1,50,000 |
| **Software** | | | | |
| OneFS licenses | Enterprise features | 1 | 15,00,000 | 15,00,000 |
| Dell ProSupport | 5-year 4-hour | 1 | 8,50,000 | 8,50,000 |
| **Services** | | | | |
| Implementation | 14-week deployment | 1 | 45,00,000 | 45,00,000 |
| Training | Admin + user training | 1 | 5,00,000 | 5,00,000 |
| **Subtotal** | | | | **8,72,50,000** |
| **GST (18%)** | | | | **1,57,05,000** |
| **TOTAL** | | | | **Rs. 10,29,55,000** |

### 5-Year TCO

| Year | Cost Component | Amount |
|------|---------------|--------|
| Year 1 | Initial deployment | 10.30 Cr |
| Year 2 | Support + maintenance | 85L |
| Year 3 | Expansion (if needed) | 1.5 Cr |
| Year 4 | Support + maintenance | 95L |
| Year 5 | Support + maintenance | 1.05 Cr |
| **5-Year Total** | | **14.6 Cr** |

*Note: Wasabi cloud storage costs additional ~Rs. 3L/year*

---

## Operational Runbooks

### SOP-PS-001: PowerScale Health Check

```bash
#!/bin/bash
# Daily health check script

echo "=== PowerScale Health Check ==="
date

# Cluster status
isi status -q

# Drive health
isi devices -q | grep -i "bad\|dead"

# Network health
isi network interfaces list | grep -i "down"

# Quota usage
isi quota list --format=csv | awk -F, '$3 > 90 {print "WARNING: " $1 " at " $3 "%"}'

# SyncIQ status
isi sync jobs list

# Alert summary
isi email settings view
```

### SOP-PS-002: Node Failure Response

1. **Detection**: Zabbix alert "PowerScale Node Down"
2. **Verify**: `isi status` confirms node offline
3. **Assess**: Check if protection level at risk
4. **Response**:
   - If N+1 still valid: No immediate action, log ticket
   - If at risk: Initiate emergency replacement
5. **Replacement**:
   - Dell ProSupport: 4-hour response
   - Swap node: <30 minutes
   - Auto-join cluster and rebalance

---

## Acceptance Criteria

### Pre-Go-Live Checklist

- [ ] All 4 nodes online and healthy
- [ ] SyncIQ replication active (RPO <5 min)
- [ ] 25GbE connectivity to all editors
- [ ] ZTNA authentication working
- [ ] CloudPools tiering active
- [ ] Backup verification passed
- [ ] Performance benchmarks met (>10GB/s)
- [ ] DR failover tested successfully
- [ ] Documentation complete
- [ ] Staff training completed

### Performance Benchmarks

| Test | Target | Actual | Pass/Fail |
|------|--------|--------|-----------|
| Sequential Read | >10 GB/s | ___ | |
| Sequential Write | >6 GB/s | ___ | |
| Random Read (4K) | >500K IOPS | ___ | |
| Latency (avg) | <1ms | ___ | |
| 25x 4K Streams | No drops | ___ | |

---

## Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Node hardware failure | Medium | Medium | N+1 redundancy, 4hr support |
| Network outage | Low | High | Dual switches, redundant paths |
| SyncIQ lag | Low | Medium | Bandwidth reservation, monitoring |
| Cost overrun | Medium | High | Fixed-price contract |
| Skill gap | Medium | Medium | Dell training, VConfi handover |

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | March 2026 | VConfi Team | Initial release |

---

**End of Document**

*VConfi Solutions — Enterprise Infrastructure*
