# Resume Capability — Quick Reference

## ⚠️ When to Break (Warning Signs)

- Token count > 100K (start preparing)
- Token count > 150K (break immediately)
- Slow response times
- "Continue from where we left off" request

---

## 🛑 BREAK (Current Conversation)

### Step 1: Save State (Use in chat)

```python
from scripts.context_manager import ContextManager
cm = ContextManager("AcmeCorp_NetworkUpgrade")

# Save recent decisions
cm.save_decision("firewall_model", "FortiGate 200F", "firewall")
cm.save_decision("core_switch", "Aruba CX 6300", "network")
cm.save_decision("vlan_count", 8, "network")

# Mark completed work
cm.mark_group_completed(0)
cm.mark_group_completed(1)
# ... mark all completed
cm.update_state(phase="document_generation")

# Save summary
cm.save_conversation_summary(
    "Parts 1-3 complete. Starting Part 4.",
    phase="document_generation"
)
```

### Step 2: Write Design Decisions File

```yaml
filesystem-write_file:
  path: "Design_Decisions.md"
  content: |
    # Design Decisions — AcmeCorp
    
    ## Client
    - Name: AcmeCorp Manufacturing
    - Users: 500
    - Sites: 3
    
    ## Decisions
    - Firewall: FortiGate 200F
    - Core Switch: Aruba CX 6300
    - VLANs: 8 (list them)
    
    ## Status
    - Parts Complete: 1, 2, 3
    - Current: Part 4 (BOM)
    - Pending: Parts 5, 6
```

### Step 3: Generate Resume Package

```python
resume = cm.generate_resume_prompt()
print(resume)
```

### Step 4: Tell User

```
⚠️ CONTEXT FULL — CONVERSATION BREAK

Download these files from this conversation:
1. Design_Decisions.md
2. Part1_Executive_Architecture_ISO.md
3. Part2_Network_Wireless_Server.md  
4. Part3_DR_Monitoring_Power.md
5. .context/AcmeCorp_NetworkUpgrade/ (folder)

Start NEW conversation, upload files, paste:

---
[PASTE RESUME TEXT HERE]
---
```

---

## ▶️ RESUME (New Conversation)

### Step 5: User Uploads Files

User uploads:
- Design_Decisions.md
- Part1_*.md, Part2_*.md, Part3_*.md
- .context/AcmeCorp_NetworkUpgrade/ folder

User pastes resume summary.

### Step 6: You Read State

```yaml
# Read design spec
filesystem-read_file: path="Design_Decisions.md"

# Read saved state  
filesystem-read_file: path=".context/AcmeCorp_NetworkUpgrade/decisions.json"
filesystem-read_file: path=".context/AcmeCorp_NetworkUpgrade/state.json"

# Check completed parts
filesystem-list_directory: path="."
```

### Step 7: Confirm & Resume

```
✓ Resumed: AcmeCorp_NetworkUpgrade

Confirmed:
- 500 users, FortiGate 200F, 8 VLANs
- Parts 1-3: Complete
- Part 4: In Progress (BOM)

Fresh context! Continuing... 🚀
```

### Step 8: Continue Work

```python
# Re-initialize
cm = ContextManager("AcmeCorp_NetworkUpgrade")

# Continue Part 4-6
# Launch subagents...
```

---

## 📁 Files Created

```
.context/AcmeCorp_NetworkUpgrade/
├── decisions.json          # All decisions
├── conversation_summary.md # History
├── state.json              # Phase, completed groups
└── resume_prompt.md        # Resume text

Design_Decisions.md          # Master spec
Part1_*.md                   # Completed parts
Part2_*.md
Part3_*.md
```

---

## 🔑 Key Commands

### Save Decision
```python
cm.save_decision("key", "value", "category")
```

### Mark Complete
```python
cm.mark_group_completed(0)  # Group 0 done
cm.update_state(phase="design")
```

### Generate Resume
```python
cm.generate_resume_prompt()  # Returns text to paste
```

### Load State (in new conversation)
```python
cm = ContextManager("SessionName")
state = cm.load_state()
```

---

## ⚡ One-Liner Break

```python
# Quick break sequence
cm = ContextManager("SessionName")
cm.save_conversation_summary("Breaking at 120K tokens", "document_generation")
print(cm.generate_resume_prompt())
```

---

**Result:** Zero lost work, seamless continuation! 🎯
