# Vendor Reference Guide — VConfi Standard Equipment

## Fortinet (Firewall & Wireless)

### FortiGate Firewall Selection Guide

| Users | Recommended Model | Firewall Throughput | IPS Throughput | SSL Inspection | Interfaces |
|-------|-------------------|--------------------|----|----------------|------------|
| 1-50 | FortiGate 40F/60F | 5-10 Gbps | 1-1.4 Gbps | 0.3-0.7 Gbps | 5-10 GE |
| 50-150 | FortiGate 80F/100F | 10-20 Gbps | 1.4-2 Gbps | 0.7-1 Gbps | 12-22 GE |
| 150-500 | FortiGate 200F/400F | 27-68 Gbps | 3-8 Gbps | 3-7 Gbps | 16-18 GE + SFP |
| 500-2000 | FortiGate 600F/900G | 80-164 Gbps | 12-20 Gbps | 7-15 Gbps | Multiple GE + SFP+ |
| 2000+ | FortiGate 1800F/2600F | 198-450 Gbps | 20-55 Gbps | 20-45 Gbps | Multiple 10G/25G |

**Note:** Always verify current models and throughput on [Fortinet product page](https://www.fortinet.com/products/next-generation-firewall). Models refresh annually.

### FortiGuard License Bundles
- **UTP (Unified Threat Protection):** AV, IPS, Web Filtering, App Control, Antispam, FortiSandbox Cloud — **Minimum required**
- **ATP (Advanced Threat Protection):** UTP + FortiSandbox, FortiNDR, FortiDeceptor integration
- **Always get 3-year or 5-year bundles** — significant discount vs annual

### FortiAP Selection Guide

| Environment | Recommended Model | Standard | Max Clients | PoE Requirement |
|-------------|-------------------|----------|-------------|-----------------|
| Small office/room | FortiAP 231G | Wi-Fi 6E | 256 | 802.3at (PoE+) |
| Open office floor | FortiAP 431G | Wi-Fi 6E | 512 | 802.3at (PoE+) |
| High density (conference) | FortiAP 831F | Wi-Fi 6 | 1024 | 802.3bt (PoE++) |
| Outdoor | FortiAP 234G | Wi-Fi 6E | 256 | 802.3at (PoE+) |

**Note:** FortiGate acts as wireless controller — no separate controller cost.

### Wireless Security Standards
- **Corporate SSID:** WPA3-Enterprise, 802.1X with RADIUS (NPS on Windows Server or FortiAuthenticator)
- **Guest SSID:** WPA3-Personal or Open with captive portal, bandwidth limits, VLAN isolation
- **Management SSID:** Hidden, MAC filtering + 802.1X, restricted to IT devices only

### Official Documentation
- [FortiOS Admin Guide](https://docs.fortinet.com/product/fortigate/)
- [FortiAP Deployment Guide](https://docs.fortinet.com/product/fortiap/)
- [FortiGate Cookbook](https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/)

---

## HPE (Switches & Servers)

### HPE Aruba Switch Selection Guide

| Layer | Recommended Series | Features | Use Case |
|-------|--------------------|----------|----------|
| Access | Aruba CX 6100 | L2, PoE+, basic | Small deployments, access layer |
| Access | Aruba CX 6200 | L2+, PoE+, stacking | Medium deployments, access layer |
| Distribution | Aruba CX 6300 | L3, PoE++, VSX | Core/distribution, routing required |
| Core | Aruba CX 8100/8360 | L3, 10G/25G, VSX | Data center, large campus core |

- **GreenLake subscription:** OpEx model — pay-per-use with lifecycle management
- **VSX (Virtual Switching Extension):** HPE's HA solution — dual switches act as one

### HPE ProLiant Server Selection Guide

| Workload | Recommended Model | Typical Config |
|----------|-------------------|----------------|
| AD, DNS, DHCP | ProLiant DL20 Gen11 | Xeon E-2400, 32-64GB, 2x 480GB SSD RAID 1 |
| File server | ProLiant DL380 Gen11 | Xeon Silver/Gold, 64-128GB, RAID 5/6 SAS/SSD |
| Virtualization | ProLiant DL380 Gen11 | Xeon Gold, 128-512GB, NVMe + SAS RAID |
| Database | ProLiant DL380 Gen11 | Xeon Gold, 256-512GB, NVMe RAID 10 |
| HCI | ProLiant DX360 Gen11 | HPE dHCI with Alletra Storage |

- **iLO 6 (Integrated Lights-Out):** Out-of-band management — always include iLO Advanced license
- **HPE Foundation Care:** 24x7 support with 4-hour response — recommended for critical servers

### Official Documentation
- [HPE Aruba CX Switches](https://www.arubanetworks.com/products/switches/)
- [HPE ProLiant Servers](https://www.hpe.com/us/en/servers/proliant-dl-servers.html)
- [HPE GreenLake](https://www.hpe.com/us/en/greenlake.html)

---

## Cisco (Switches)

### Cisco Catalyst Switch Selection Guide

| Layer | Recommended Series | Features | Use Case |
|-------|--------------------|----------|----------|
| Access | Catalyst 9200 | L2+, PoE+, stacking | Small-medium access layer |
| Access/Dist | Catalyst 9300 | L3, PoE++, StackWise | Medium-large, distribution |
| Core | Catalyst 9400/9500 | L3, modular/fixed, 10G/25G | Campus core, data center |

- **DNA Essentials license:** Automation, monitoring, assurance, basic SD-Access
- **DNA Advantage license:** Full SD-Access, Cisco AI Analytics (if needed)
- **StackWise/StackWise Virtual:** Cisco's stacking and HA solution

### Official Documentation
- [Cisco Catalyst 9000 Series](https://www.cisco.com/c/en/us/products/switches/catalyst-9000.html)
- [Cisco DNA Center](https://www.cisco.com/c/en/us/products/cloud-systems-management/dna-center/index.html)

---

## Synology (NAS & Backup)

### Synology NAS Selection Guide

| Use Case | Recommended Model | Bays | Typical Config |
|----------|-------------------|------|----------------|
| Small backup target | DS923+ | 4 bay | 4x 4TB NAS HDD, RAID 5 |
| File server / medium backup | DS1823xs+ | 8 bay | 8x 8TB NAS HDD, RAID 6 |
| Large backup / surveillance | RS3621xs+ | 12 bay | 12x 16TB NAS HDD, RAID 6 |
| Enterprise backup target | HD6500 | 60 bay | High density, scale-out |

- **Synology Active Backup for Business:** Free — backs up VMs, PCs, servers, M365
- **Synology Surveillance Station:** 2 camera licenses free, additional licenses purchasable
- **Always use Synology-verified HDDs** (WD Red Plus, Seagate IronWolf, Synology HAT5300)

### Official Documentation
- [Synology Product Selector](https://www.synology.com/en-global/products)
- [Active Backup for Business](https://www.synology.com/en-global/dsm/feature/active-backup-business)

---

## UPS & Power

### APC by Schneider Electric

| Capacity | Model Series | Type | Use Case |
|----------|-------------|------|----------|
| 750-3000 VA | Smart-UPS SMT | Line-interactive | Small switch closets |
| 1-10 kVA | Smart-UPS SRT | Online double-conversion | Server rooms |
| 10-20 kVA | Smart-UPS SRT/VT | Online double-conversion | Medium data center |
| 20-500 kVA | Symmetra/Galaxy | Online double-conversion | Large data center |

### Vertiv (Liebert)

| Capacity | Model Series | Type | Use Case |
|----------|-------------|------|----------|
| 750-3000 VA | Liebert PSI5 | Line-interactive | Small setups |
| 1-10 kVA | Liebert GXT5 | Online double-conversion | Server rooms |
| 10-20 kVA | Liebert EXS | Online double-conversion | Medium data center |

### Eaton

| Capacity | Model Series | Type | Use Case |
|----------|-------------|------|----------|
| 750-3000 VA | 5PX Gen2 | Line-interactive | Small setups |
| 1-10 kVA | 9PX | Online double-conversion | Server rooms |
| 10-20 kVA | 93PS | Online double-conversion | Medium data center |

### UPS Sizing Formula
```
Required VA = (Total Watts of all devices) / Power Factor (typically 0.9)
Recommended VA = Required VA x 1.2 (20% headroom)
```

### SNMP Monitoring
- **APC:** AP9631 Network Management Card (NMC3)
- **Vertiv:** Liebert IntelliSlot Unity card
- **Eaton:** Gigabit Network Card (NETWORK-M3)
- All integrate with Zabbix via SNMP v3

---

## Backup Solutions

### Veeam Backup & Replication
- **Veeam Data Platform Foundation:** VM backup, instant recovery, NAS backup
- **Veeam Data Platform Advanced:** + monitoring, Veeam ONE analytics
- License: per-workload (VM, server, NAS) — get pricing from Veeam partner

### Backup Architecture (3-2-1 Rule)
```
[Production Servers]
    → Copy 1: Local backup (Veeam to local repo)
    → Copy 2: NAS backup (Veeam to Synology NAS)
    → Copy 3: Offsite (Veeam Cloud Connect or Synology C2)
```
