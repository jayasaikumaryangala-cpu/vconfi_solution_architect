# VConfi Memory Index

Institutional knowledge repository for the VConfi Solution Architect skill.

---

## 📁 Directory Structure

```
memory/
├── memory_index.md          # This file — master index
├── clients/                 # Client profiles and preferences
│   ├── README.md
│   ├── TEMPLATE.md         # Use this to create new client profiles
│   └── Sample-Manufacturing-Corp.md  # Example client profile
├── pricing/                 # Actual pricing from vendors/distributors
│   ├── README.md
│   ├── fortinet-firewalls.md
│   ├── hpe-aruba-switches.md
│   ├── hpe-servers.md
│   ├── synology-nas.md
│   └── ups-power.md
├── lessons/                 # Lessons learned from past projects
│   ├── README.md           # Index of all lessons
│   ├── firewall-sizing.md
│   ├── switch-stacking.md
│   ├── backup-rto.md
│   └── wireless-coverage.md
└── projects/                # Completed project records
    └── README.md
```

---

## 💰 Pricing Data

| Vendor | File | Last Updated | Coverage |
|--------|------|--------------|----------|
| Fortinet | [fortinet-firewalls.md](pricing/fortinet-firewalls.md) | 2026-03-22 | Firewalls, FortiAPs, licensing |
| HPE | [hpe-aruba-switches.md](pricing/hpe-aruba-switches.md) | 2026-03-22 | CX 6100/6200/6300/8360, transceivers |
| HPE | [hpe-servers.md](pricing/hpe-servers.md) | 2026-03-22 | ProLiant DL20/DL380, options, support |
| Synology | [synology-nas.md](pricing/synology-nas.md) | 2026-03-22 | NAS units, drives, software |
| APC/Vertiv/Eaton | [ups-power.md](pricing/ups-power.md) | 2026-03-22 | UPS, ATS, PDU pricing |

### Quick Pricing Reference

**Firewall (with UTP 3-year bundle):**
- 50 users: FortiGate 60F — ~1,12,000 INR
- 100 users: FortiGate 80F — ~2,15,000 INR
- 200 users: FortiGate 100F — ~3,80,000 INR
- 500 users: FortiGate 200F — ~7,50,000 INR

**Switch (entry-level):**
- 24-port L2: Aruba CX 6100 — ~75,000 INR
- 48-port L2+ stacking: Aruba CX 6200 — ~2,10,000 INR
- 48-port L3 PoE++: Aruba CX 6300 — ~4,15,000 INR

**Server (typical config):**
- Entry: DL20 Gen11 — ~1,45,000-2,35,000 INR
- Virtualization: DL380 Gen11 — ~4,85,000-8,75,000 INR

**UPS (online double-conversion):**
- 1.5kVA rackmount: ~72,000-82,000 INR
- 3kVA rackmount: ~1,35,000-1,55,000 INR
- 10kVA rackmount: ~4,85,000-5,25,000 INR

---

## 👤 Client Profiles

| Client | Industry | Location | File |
|--------|----------|----------|------|
| Sample Manufacturing Corp | Manufacturing | Pune, MH | [Sample-Manufacturing-Corp.md](clients/Sample-Manufacturing-Corp.md) |

### Template

Use [TEMPLATE.md](clients/TEMPLATE.md) to create new client profiles.

---

## 📚 Lessons Learned

| Lesson | Severity | Category | Key Takeaway |
|--------|----------|----------|--------------|
| [Firewall Sizing](lessons/firewall-sizing.md) | 🔴 High | Firewall | Size by SSL throughput, not firewall throughput |
| [Switch Stacking](lessons/switch-stacking.md) | 🟡 Medium | Switches | Stacking cables/modules are never included |
| [Backup RTO](lessons/backup-rto.md) | 🔴 Critical | DR/Backup | Never promise RTO without testing restore |
| [Wireless Coverage](lessons/wireless-coverage.md) | 🟡 Medium | Wireless | "2,000 sq ft/AP" is for open space only |

See [lessons/README.md](lessons/README.md) for full index and how to add new lessons.

---

## 🔍 When to Use Memory

### At Project Start
1. Check [pricing/](pricing/) for current rates before WebSearch
2. Check [clients/](clients/) for returning clients
3. Review [lessons/](lessons/) for relevant warnings

### During Design
- Reference pricing to validate BOM accuracy
- Check lessons for common mistakes in that category
- Use client preferences to guide vendor selection

### After Project Completion
1. Update pricing if you received new quotes
2. Add client profile (if new client)
3. Document any lessons learned

---

## 📝 Maintenance

- **Pricing:** Update quarterly or when significant changes occur
- **Clients:** Update after each engagement
- **Lessons:** Add immediately after an incident or insight
- **This Index:** Update when adding new files or categories

---

*Last updated: 2026-03-22*
