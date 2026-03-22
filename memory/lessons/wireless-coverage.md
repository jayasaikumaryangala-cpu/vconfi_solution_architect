# Lesson: Wireless AP Density Underestimation

- **Date:** 2026-03-22
- **Severity:** Medium
- **Category:** Wireless Design

## The Lesson

**The "2,000 sq ft per AP" rule is for open space only. Walls halve this.**

## What Happened

- **Client:** Corporate office with cubicles and meeting rooms
- **Design:** 6 APs for 12,000 sq ft (following 2,000 sq ft/AP rule)
- **Reality:** Poor coverage in conference rooms, dead spots in corners
- **Root Cause:** Drywall + glass partitions attenuate signal 3-6 dB; meeting rooms need dedicated APs
- **Result:** Added 3 more APs post-installation — additional cost 1,20,000 INR

## Attenuation Reference

| Obstacle | Signal Loss | Impact on Coverage |
|----------|-------------|-------------------|
| Open air | 0 dB | 2,000 sq ft |
| Drywall | 3 dB | ~1,400 sq ft |
| Glass/window | 3-6 dB | ~1,000 sq ft |
| Concrete wall | 10-15 dB | ~500 sq ft |
| Elevator shaft | 20+ dB | Dead zone |

## Design Rules We Now Use

### Base Calculation

```
APs Needed = (Total Area / Coverage Per AP) + (High-Density Areas × 2)
```

### Coverage Per AP by Environment

| Environment | Sq Ft per AP | Max Clients | Example |
|-------------|--------------|-------------|---------|
| Open office | 1,500 | 50 | Software company floor |
| Cubicle office | 1,000 | 40 | Call center |
| Conference rooms | 1 per room | 30 | Boardroom needs dedicated AP |
| Classroom | 800 | 35 | Education |
| Warehouse | 2,500 | 30 | Open space, high ceilings |
| Healthcare | 1,200 | 25 | EMI from medical equipment |

## High-Density Multiplier

Add extra APs for:
- **Conference rooms:** +1 AP per room >200 sq ft
- **Auditoriums:** +2-3 APs (high concurrent users)
- **Cafeterias:** +1-2 APs (BYOD density)
- **Warehouse aisles:** +1 AP per aisle if racking >10 ft

## Pre-Deployment Checklist

- [ ] Site walk with floor plan (if possible)
- [ ] Identify wall materials
- [ ] Count conference rooms/meeting spaces
- [ ] Identify high-density zones
- [ ] Plan for 20% growth in client count
- [ ] Budget for 10% extra APs (future proofing)

## Tools

- **Ekahau HeatMapper:** Free for basic planning
- **FortiPlanner:** Free, FortiAP-specific
- **Site survey:** Mandatory for >50 AP deployments
