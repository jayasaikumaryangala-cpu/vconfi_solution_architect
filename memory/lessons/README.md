# Lessons Learned — VConfi Solution Architect

This directory contains institutional knowledge from past projects. Each lesson documents:
- What went wrong (or what worked well)
- Root cause analysis
- How to avoid/prevent in future
- Templates or checklists where applicable

## Lesson Index

| File | Topic | Severity | Category |
|------|-------|----------|----------|
| [firewall-sizing.md](firewall-sizing.md) | Size by SSL throughput, not firewall throughput | High | Firewall |
| [switch-stacking.md](switch-stacking.md) | Stacking cables are not included | Medium | Switches |
| [backup-rto.md](backup-rto.md) | Never promise RTO without testing | Critical | DR/Backup |
| [wireless-coverage.md](wireless-coverage.md) | AP density rules by environment | Medium | Wireless |

## Adding New Lessons

When something unexpected happens on a project:

1. **Create a new markdown file** named `<topic>.md`
2. **Follow this template:**

```markdown
# Lesson: [Brief Title]

- **Date:** YYYY-MM-DD
- **Severity:** Critical/High/Medium/Low
- **Category:** [Firewall/Switch/Wireless/Server/DR/Backup/etc.]

## The Lesson

[One-line summary]

## What Happened

- **Client:** [Industry/size]
- **Mistake:** [What we did wrong]
- **Result:** [Impact]

## Root Cause

[Why it happened]

## Correction Applied

[How we fixed it / new process]

## Checklist

- [ ] Item 1
- [ ] Item 2

## Reference

[Links to docs]
```

3. **Update this README** with the new lesson entry

## Categories

- `firewall` — FortiGate, policies, sizing, VPN
- `switch` — HPE/Cisco switches, stacking, VLANs
- `wireless` — FortiAP, coverage, density
- `server` — HPE ProLiant, virtualization, sizing
- `backup` — Veeam, Synology, retention
- `dr` — Disaster recovery, RTO/RPO, failover
- `monitoring` — Zabbix, Splunk, alerting
- `power` — UPS, ATS, PDU
- `cabling` — Fiber, copper, standards
- `compliance` — ISO 27001, audit prep
