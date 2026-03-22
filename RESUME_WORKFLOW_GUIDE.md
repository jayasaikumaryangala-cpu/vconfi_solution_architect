# VConfi Resume Workflow Guide — Conversation Break & Resume

## When to Use Resume Capability

### Scenario: Context Window Filling Up

You're generating a large implementation plan and hit the token limit:

```
[Generating Part 4 of 6...]
⚠️ Warning: Context at 120K tokens (limit: 200K)
⚠️ Slow response times detected
⚠️ Risk of truncation
```

**Solution:** Break conversation, save state, resume in fresh conversation.

---

## Step-by-Step Resume Workflow

### Phase 1: BREAK (Current Conversation)

#### Step 1: Save All State

```python
from scripts.context_manager import ContextManager

# Initialize (same session name as when you started)
cm = ContextManager("AcmeCorp_NetworkUpgrade")

# Save current design decisions
cm.save_decision("firewall_model", "FortiGate 200F", "firewall")
cm.save_decision("core_switch", "Aruba CX 6300", "network")
cm.save_decision("vlan_count", 8, "network")
cm.save_decision("user_count", 500, "network")
# ... save all recent decisions

# Update state
cm.update_state(phase="document_generation")
cm.mark_group_completed(0)  # Discovery
cm.mark_group_completed(1)  # Scope
cm.mark_group_completed(2)  # Network
# ... mark all completed groups

# Save conversation summary
cm.save_conversation_summary(
    """Generated Parts 1-3 successfully. 
    Part 1: Executive Summary + Architecture + ISO compliance (complete)
    Part 2: Network design + Wireless + Servers (complete)
    Part 3: DR/Backup + Monitoring + Power (complete)
    
    Now starting Part 4 (BOM). Context window filling up.""",
    phase="document_generation"
)
```

#### Step 2: Write Design Decisions File

```yaml
# Use Filesystem MCP to write complete design spec
filesystem-write_file:
  path: "Design_Decisions.md"
  content: |
    # Design Decisions Summary — AcmeCorp Network Upgrade
    
    ## Client Profile
    - **Company:** AcmeCorp Manufacturing
    - **Industry:** Manufacturing
    - **Users:** 500
    - **Sites:** 3 (Pune HQ, Mumbai Branch, Chennai DC)
    
    ## Architecture Decisions
    | Component | Model | Rationale |
    |-----------|-------|-----------|
    | Firewall | FortiGate 200F | 500 users, SSL inspection needed |
    | Core Switch | Aruba CX 6300 48G | PoE++, VSX stacking |
    | UPS | APC SRT10KRMXLI | 10kVA for 4hr runtime |
    
    ## Network Design
    - **VLANs:** 8 (10-Mgmt, 20-Users, 30-Servers, 40-Guest, 50-CCTV, 60-VoIP, 70-IoT, 80-DMZ)
    - **IP Scheme:** 10.10.0.0/16
    - **Redundancy:** HA with dual FortiGate, dual core switches
    
    ## Completed Parts
    - Part 1: ✓ Complete (saved as Part1_Executive_Architecture_ISO.md)
    - Part 2: ✓ Complete (saved as Part2_Network_Wireless_Server.md)
    - Part 3: ✓ Complete (saved as Part3_DR_Monitoring_Power.md)
    - Part 4: In Progress (BOM, Assets, Timeline)
    - Part 5: Pending (Security Stress Test)
    - Part 6: Pending (SOPs)
    
    ## Next Actions
    1. Complete Part 4 (BOM with pricing)
    2. Complete Part 5 (Security test)
    3. Complete Part 6 (SOPs)
    4. Render all diagrams
    5. Merge to DOCX
```

#### Step 3: Generate Resume Package

```python
# Generate resume prompt for user
resume_package = cm.generate_resume_prompt()
print(resume_package)
```

**Output:**

```markdown
# Resume Session: AcmeCorp_NetworkUpgrade

## Current Phase
document_generation

## Key Decisions Made

### firewall
- **firewall_model:** FortiGate 200F

### network
- **core_switch:** Aruba CX 6300
- **vlan_count:** 8
- **user_count:** 500

## Conversation History
# Conversation Summary

## [2026-03-22 14:30]
**Phase:** discovery

Group 0 complete. Client confirmed 500 users, 3 sites.

## [2026-03-22 14:45]
**Phase:** design

Finalized FortiGate 200F, Aruba CX 6300 core switches.

## [2026-03-22 15:00]
**Phase:** document_generation

Generated Parts 1-3 successfully. 
Part 1: Executive Summary + Architecture + ISO compliance (complete)
Part 2: Network design + Wireless + Servers (complete)
Part 3: DR/Backup + Monitoring + Power (complete)

Now starting Part 4 (BOM). Context window filling up.
```

#### Step 4: Provide Resume Instructions to User

```
⚠️ CONTEXT WINDOW FULL — CONVERSATION BREAK

I'm saving our progress. To resume:

1. DOWNLOAD these files from this conversation:
   - Design_Decisions.md
   - Part1_Executive_Architecture_ISO.md
   - Part2_Network_Wireless_Server.md
   - Part3_DR_Monitoring_Power.md
   - .context/AcmeCorp_NetworkUpgrade/ (entire folder)

2. START A NEW CONVERSATION

3. UPLOAD the files above

4. PASTE this resume summary:

---
[RESUME SUMMARY PASTE HERE]
---

I'll continue from Part 4 (BOM) with fresh context!
```

---

### Phase 2: RESUME (New Conversation)

#### Step 5: User Starts New Conversation

**User uploads:**
- Design_Decisions.md
- Part1_Executive_Architecture_ISO.md
- Part2_Network_Wireless_Server.md
- Part3_DR_Monitoring_Power.md
- .context/AcmeCorp_NetworkUpgrade/ folder

**User pastes:**
```markdown
Resume Session: AcmeCorp_NetworkUpgrade
[Full resume text from above]
```

#### Step 6: You Read State Files

```yaml
# Read the design decisions
filesystem-read_file: path="Design_Decisions.md"

# Read the saved state
filesystem-read_file: path=".context/AcmeCorp_NetworkUpgrade/decisions.json"
filesystem-read_file: path=".context/AcmeCorp_NetworkUpgrade/conversation_summary.md"
filesystem-read_file: path=".context/AcmeCorp_NetworkUpgrade/state.json"

# Verify completed parts exist
filesystem-list_directory: path="."
# Should see: Part1_Executive_Architecture_ISO.md, Part2_..., Part3_...
```

#### Step 7: Confirm Understanding & Resume

```
✓ Successfully resumed session: AcmeCorp_NetworkUpgrade

State Loaded:
- Client: AcmeCorp Manufacturing (500 users, 3 sites)
- Phase: Document Generation
- Completed: Parts 1, 2, 3
- In Progress: Part 4 (BOM, Assets, Timeline)
- Pending: Parts 5, 6

Key Decisions Confirmed:
- Firewall: FortiGate 200F
- Core Switch: Aruba CX 6300
- VLANs: 8

Resuming with fresh context! 🚀

Next: Continue Part 4 — BOM with INR pricing
```

#### Step 8: Continue Generation

```python
# Re-initialize ContextManager in new conversation
cm = ContextManager("AcmeCorp_NetworkUpgrade")

# Check what's already done
state = cm.load_state()
print(f"Completed groups: {state['state']['completed_groups']}")
print(f"Last phase: {state['state']['phase']}")

# Continue with Part 4
# Launch subagent for Part 4...
```

---

## Complete Code Example: Break & Resume

### File: `example_break_resume.py`

```python
#!/usr/bin/env python3
"""
Example: Breaking and Resuming a VConfi Engagement
"""

from scripts.context_manager import ContextManager
import os

def break_conversation():
    """Call this when context is filling up."""
    
    # 1. Initialize ContextManager
    cm = ContextManager("AcmeCorp_NetworkUpgrade")
    
    # 2. Save all current decisions
    decisions = {
        "firewall": {"model": "FortiGate 200F", "license": "UTP 3-year"},
        "network": {
            "core_switch": "Aruba CX 6300",
            "access_switches": "Aruba CX 6200",
            "vlan_count": 8,
            "user_count": 500
        },
        "servers": {
            "virtualization_host": "HPE DL380 Gen11",
            "nas": "Synology RS3621xs+",
            "count": 3
        },
        "wireless": {
            "ap_model": "FortiAP 431F",
            "ap_count": 12
        }
    }
    
    for category, items in decisions.items():
        for key, value in items.items():
            cm.save_decision(key, value, category)
    
    # 3. Mark completed work
    cm.mark_group_completed(0)  # Discovery
    cm.mark_group_completed(1)  # Scope
    cm.mark_group_completed(2)  # Network
    cm.mark_group_completed(3)  # Servers
    cm.mark_group_completed(4)  # Wireless
    cm.mark_group_completed(5)  # Security
    cm.mark_group_completed(6)  # Budget
    cm.mark_group_completed(7)  # Redundancy
    
    # 4. Update phase
    cm.update_state(
        phase="document_generation",
        current_part=4,
        total_parts=6,
        completed_parts=[1, 2, 3]
    )
    
    # 5. Save summary
    cm.save_conversation_summary(
        """Document generation in progress.
        
        COMPLETED:
        - Part 1: Executive Summary ✓
        - Part 2: Network Design ✓  
        - Part 3: DR/Monitoring/Power ✓
        
        IN PROGRESS:
        - Part 4: BOM (estimating costs)
        
        PENDING:
        - Part 5: Security Stress Test
        - Part 6: SOPs
        
        Context at 120K tokens. Breaking conversation.""",
        phase="document_generation"
    )
    
    # 6. Generate resume package for user
    resume = cm.generate_resume_prompt()
    
    print("\n" + "="*60)
    print("CONVERSATION BREAK — SAVE THESE FILES:")
    print("="*60)
    print("1. Design_Decisions.md")
    print("2. Part1_Executive_Architecture_ISO.md")
    print("3. Part2_Network_Wireless_Server.md")
    print("4. Part3_DR_Monitoring_Power.md")
    print("5. .context/AcmeCorp_NetworkUpgrade/ (folder)")
    print("\n" + "="*60)
    print("PASTE THIS IN NEW CONVERSATION:")
    print("="*60)
    print(resume)
    
    return resume

def resume_conversation():
    """Call this in the new conversation after user uploads files."""
    
    # 1. Re-initialize ContextManager (same session name)
    cm = ContextManager("AcmeCorp_NetworkUpgrade")
    
    # 2. Load state
    state = cm.load_state()
    
    print("\n" + "="*60)
    print("RESUMED SESSION:")
    print("="*60)
    print(f"Session: {cm.session_name}")
    print(f"Phase: {state['state']['phase']}")
    print(f"Completed Groups: {state['state']['completed_groups']}")
    
    print("\nKey Decisions:")
    for category, items in state['decisions'].items():
        print(f"\n  [{category}]")
        for key, data in items.items():
            print(f"    - {key}: {data['value']}")
    
    print("\n" + "="*60)
    print("READY TO CONTINUE!")
    print("="*60)
    
    # 3. Return state for continuing work
    return state

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "break":
        break_conversation()
    elif len(sys.argv) > 1 and sys.argv[1] == "resume":
        resume_conversation()
    else:
        print("Usage:")
        print("  python example_break_resume.py break")
        print("  python example_break_resume.py resume")
```

---

## Visual Workflow

```
CONVERSATION 1 (Filling Up)
============================
1. Generate Parts 1-3 ✓
2. Context at 120K ⚠️
3. BREAK SEQUENCE:
   ├── cm.save_decision() for all choices
   ├── cm.mark_group_completed(0-7)
   ├── cm.update_state(phase="doc_gen")
   ├── filesystem-write_file: Design_Decisions.md
   └── cm.generate_resume_prompt()
4. Give user files + resume text

[USER DOWNLOADS FILES]
[USER STARTS NEW CONVERSATION]

CONVERSATION 2 (Fresh Context)
=============================
1. User uploads files
2. User pastes resume text
3. YOU READ:
   ├── filesystem-read_file: Design_Decisions.md
   ├── filesystem-read_file: decisions.json
   └── filesystem-list_directory: verify parts exist
4. Confirm: "Resumed AcmeCorp session"
5. CONTINUE Part 4-6 ✓
6. Generate final DOCX ✓
```

---

## Files Created During Break

```
.context/
└── AcmeCorp_NetworkUpgrade/
    ├── decisions.json          # All decisions made
    ├── conversation_summary.md # Running history
    ├── state.json              # Current phase, completed groups
    └── resume_prompt.md        # Generated resume package

Design_Decisions.md              # Complete design specification
Part1_Executive_Architecture_ISO.md
Part2_Network_Wireless_Server.md
Part3_DR_Monitoring_Power.md
```

---

## Tips for Smooth Resume

### 1. Save Frequently

Don't wait until 150K tokens. Save at 100K:

```python
# During document generation
if estimated_tokens > 100000:
    cm.save_conversation_summary("Approaching limit, preparing break")
    # ... save everything
```

### 2. Name Sessions Clearly

```python
# Good naming
"AcmeCorp_NetworkUpgrade_March2026"
"GlobalTech_DRSetup_Q2_2026"

# Avoid
"project1"
"temp"
```

### 3. Include File List in Resume

Always tell user exactly which files to upload:

```
UPLOAD THESE FILES:
1. Design_Decisions.md
2. Part1_*.md (if generated)
3. Part2_*.md (if generated)
4. .context/[session]/ (folder)
```

### 4. Verify on Resume

Always read files to confirm state:

```yaml
filesystem-read_file: path="Design_Decisions.md"
filesystem-read_file: path=".context/AcmeCorp_NetworkUpgrade/state.json"
```

Then confirm back to user:
```
✓ Confirmed: 500 users, FortiGate 200F, 8 VLANs
✓ Completed: Parts 1-3
→ Continuing: Part 4 (BOM)
```

---

## Emergency: Context Overflowed

If context overflowed before you could save:

```python
# Try emergency save
filesystem-write_file: 
  path="EMERGENCY_SAVE.md"
  content=[what you remember of decisions]

# Create minimal resume
cm = ContextManager("AcmeCorp_NetworkUpgrade_Emergency")
cm.save_conversation_summary(
    "Context overflowed. Partial state recovered. "
    "User to provide Design_Decisions.md from local save."
)
```

Then in new conversation, ask user to provide what they have:
```
"Context overflowed. Please upload any files you downloaded 
from the previous conversation (Design_Decisions.md, completed parts)."
```

---

## Summary

| Step | Action | Code |
|------|--------|------|
| 1 | Initialize | `cm = ContextManager("SessionName")` |
| 2 | Save decisions | `cm.save_decision(key, value, category)` |
| 3 | Mark progress | `cm.mark_group_completed(n)` |
| 4 | Write file | `filesystem-write_file: Design_Decisions.md` |
| 5 | Generate resume | `cm.generate_resume_prompt()` |
| 6 | User uploads | In new conversation |
| 7 | Read state | `filesystem-read_file: decisions.json` |
| 8 | Continue | Launch subagents for remaining parts |

**Result:** Zero lost work, seamless continuation! 🚀
