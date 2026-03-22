# Lesson: Firewall Sizing Mistakes

- **Date:** 2026-03-22
- **Severity:** High
- **Category:** Firewall Sizing

## The Lesson

**Always size firewalls by SSL Inspection throughput, not firewall throughput.**

## What Happened

- **Client:** Mid-size financial services firm (200 users)
- **Mistake:** Recommended FortiGate 100F based on 200 users (fits the chart)
- **Reality:** Heavy SSL inspection + 50 VPN users caused bottleneck
- **Result:** Had to upgrade to 200F within 6 months — client unhappy

## Root Cause

Firewall datasheets show "Firewall Throughput" (raw packets) which is 10x higher than "SSL Inspection Throughput" (decrypted traffic).

| Spec | FortiGate 100F | FortiGate 200F |
|------|----------------|----------------|
| Firewall Throughput | 20 Gbps | 68 Gbps |
| **SSL Inspection** | **1 Gbps** | **7 Gbps** |
| IPS Throughput | 2 Gbps | 8 Gbps |

With 200 users + SSL inspection + VPN, the 100F's 1 Gbps SSL throughput was saturated.

## Correction Applied

Now we use this sizing formula:
```
Required SSL Throughput = (Number of Users × 5 Mbps) × 1.5 (headroom)

Example: 200 users × 5 Mbps = 1 Gbps × 1.5 = 1.5 Gbps needed
→ Minimum: FortiGate 200F (7 Gbps SSL)
```

## Checklist

- [ ] Ask: "Do you need SSL inspection?" (compliance usually requires yes)
- [ ] Ask: "How many VPN users concurrently?"
- [ ] Calculate SSL throughput needed
- [ ] Size up one model if budget allows
- [ ] Document the calculation in the proposal

## Reference

- Fortinet sizing guide: https://www.fortinet.com/resources/sizing-guides
