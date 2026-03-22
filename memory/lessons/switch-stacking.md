# Lesson: Switch Stacking Cabling

- **Date:** 2026-03-22
- **Severity:** Medium
- **Category:** Switch Configuration

## The Lesson

**Stacking cables must be ordered SEPARATELY — they are never included.**

## What Happened

- **Client:** Education institution with 3-floor campus
- **Mistake:** Assumed HPE Aruba CX 6200 stacking modules included cables
- **Reality:** Stacking modules = empty slots; cables cost extra 15,000 INR each
- **Result:** Installation delayed 1 week waiting for cables

## What We Now Know

### HPE Aruba Stacking Requirements

| Component | Included? | Cost (INR) |
|-----------|-----------|------------|
| CX 6200 Switch | Yes | Base price |
| Stacking Module (JL677A) | No | ~25,000 |
| 0.5m Stacking Cable (JL678A) | No | ~8,000 |
| 1m Stacking Cable (JL679A) | No | ~10,000 |
| 3m Stacking Cable (JL680A) | No | ~15,000 |

### Cisco Stacking (for comparison)

| Component | Included? | Cost (INR) |
|-----------|-----------|------------|
| Catalyst 9200 | Yes | Base price |
| StackWise Cable | Yes (in box) | — |
| StackWise Adapter | No | ~18,000 |

## Best Practice

1. **Always ask:** "What's the distance between switch racks?"
2. **Add to BOM:** Stacking module + cable per switch pair
3. **Add spare:** One extra cable (they get damaged)
4. **Document:** Cable lengths in the implementation plan

## Template BOM Entry

```
HPE Aruba CX 6200 48G CL4 Switch    Qty: 2    @ 2,10,000 = 4,20,000
HPE Stacking Module (JL677A)        Qty: 2    @ 25,000   = 50,000
HPE 3m Stacking Cable (JL680A)      Qty: 2    @ 15,000   = 30,000
HPE 3m Stacking Cable (spare)       Qty: 1    @ 15,000   = 15,000
                                                        ———————————
Stacking Total: 5,15,000 INR
```
