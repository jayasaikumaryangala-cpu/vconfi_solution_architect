# Lesson: Backup RTO Reality Check

- **Date:** 2026-03-22
- **Severity:** Critical
- **Category:** Disaster Recovery

## The Lesson

**Never promise RTO without testing restore speed from actual backup media.**

## What Happened

- **Client:** Healthcare clinic (50 beds)
- **Requirement:** RTO 4 hours, RPO 1 hour for patient database
- **Design:** Veeam backup to Synology NAS, nightly replication to offsite
- **Mistake:** Assumed 4-hour RTO was achievable based on Veeam specs
- **Reality:** First restore test took 14 hours due to:
  - Slow NAS read speeds (HDD-based)
  - Large VM size (2 TB) with random I/O
  - Network bandwidth to offsite (100 Mbps)
- **Result:** Clinic could not access patient records for full day — compliance violation

## Root Cause Analysis

| Factor | Assumed | Reality |
|--------|---------|---------|
| NAS Read Speed | 200 MB/s | 80 MB/s (RAID 6 penalty) |
| Network (offsite) | 1 Gbps | 100 Mbps shared |
| VM Size | 500 GB | 2 TB (underestimated growth) |
| Concurrent Restores | 1 VM | 5 VMs (dependencies) |

## Correction Applied

### New Sizing Formula

```
Restore Time = (Data Size) / (Restore Throughput)

Where Restore Throughput = MIN(Source Read, Network, Target Write) × 0.7 (overhead)
```

### For 2TB VM with 4-hour RTO:

| Requirement | Calculation |
|-------------|-------------|
| Required throughput | 2 TB / 4 hr = 512 GB/hr = 142 MB/s |
| With overhead | 142 MB/s / 0.7 = 203 MB/s sustained |
| **Solution needed** | SSD-based backup target or Instant VM Recovery |

## Best Practice

1. **Always test:** Restore one full VM during design phase
2. **Size backup target:** Use SSDs for critical VMs (not just HDD)
3. **Use Instant VM Recovery:** For critical systems — boot from backup instantly
4. **Document actual RTO:** After first successful restore test
5. **Set expectations:** "Target RTO: 4 hours, Validated RTO: TBD after testing"

## Updated Design Pattern

| Tier | RTO | Technology | Cost Impact |
|------|-----|------------|-------------|
| Critical (Tier 1) | < 1 hour | Veeam Instant VM Recovery + SSD | +40% |
| Important (Tier 2) | 4-8 hours | Standard restore from SSD NAS | +20% |
| Standard (Tier 3) | 24+ hours | Restore from HDD NAS | Base |

## Reference

- Veeam RTO calculator: https://www.veeam.com/resources/calculator.html
