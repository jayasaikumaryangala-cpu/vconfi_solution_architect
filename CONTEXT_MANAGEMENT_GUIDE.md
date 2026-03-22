# VConfi Context Management Guide — Prevent Context Window Overflow

## The Problem

Claude has a 200K token context window. A full implementation plan can consume 50K-80K tokens during questioning + design. When generating 6 parts, later parts (4, 5, 6) risk truncation.

## The Solution: File-Based Context Management

Instead of keeping everything in active context, **write to files immediately** and reference by filename.

---

## 🧠 Core Strategy: "Write Early, Reference Often"

### Pattern 1: Immediate File Writes

❌ **OLD (Context Heavy):**
```
User: "We need 500 users"
[Keep in context]
User: "8 VLANs"
[Keep in context]
User: "FortiGate 200F"
[Keep in context]
...
[Context fills up with all requirements]
```

✅ **NEW (Context Light):**
```
User: "We need 500 users"
→ filesystem-write_file: path=".context/decisions.json" 
  content='{"user_count": 500}'
[Reference only: "See decisions.json"]
```

### Pattern 2: Summarized Context

❌ **OLD:**
```
Full conversation history kept in context...
(User said X, I said Y, user said Z...)
```

✅ **NEW:**
```
Current Phase: Design Decisions
Last Action: Confirmed firewall model
Key File: Design_Decisions.md
Summary: 500 users, 8 VLANs, FortiGate 200F...
[Full details in files, not context]
```

---

## 📁 Context Manager Tool

Use `scripts/context_manager.py` to manage state:

```python
from scripts.context_manager import ContextManager

# Initialize for this engagement
cm = ContextManager("AcmeCorp_NetworkUpgrade")

# Save each decision immediately
cm.save_decision("user_count", 500, category="network")
cm.save_decision("firewall_model", "FortiGate 200F", category="firewall")
cm.save_decision("vlan_count", 8, category="network")

# Save conversation summaries
cm.save_conversation_summary(
    "Discussed network requirements. Client confirmed 8 VLANs needed.",
    phase="discovery"
)

# Mark completed questioning groups
cm.mark_group_completed(0)  # Group 0 done
cm.mark_group_completed(1)  # Group 1 done

# When context runs low, generate resume prompt
resume_text = cm.generate_resume_prompt()
# Paste this into a new conversation
```

---

## 🔄 Conversation Break Strategy

### When to Break (Warning Signs)

| Sign | Action |
|------|--------|
| Token count > 100K | Prepare to break |
| Token count > 150K | Break immediately after current task |
| Response generation slows | Context is full |
| "Continue from where we left off" | Break and resume |

### How to Break Gracefully

**Step 1: Save State**
```
filesystem-write_file: path="Design_Decisions.md" 
  content=[full design decisions]

[Use ContextManager to save all decisions]
```

**Step 2: Generate Resume Package**
```
[Generate summary with ContextManager]

Resume Package Contains:
1. Design_Decisions.md (full spec)
2. .context/[session]/decisions.json (structured data)
3. .context/[session]/conversation_summary.md (history)
4. This summary:

---
## SESSION RESUME PACKAGE
**Client:** AcmeCorp
**Project:** Network Upgrade
**Last Phase:** Design Decisions Complete
**Next Phase:** Document Generation

**Key Decisions:**
- Users: 500
- Firewall: FortiGate 200F
- VLANs: 8 (list in Design_Decisions.md)
- Servers: 3x HPE DL380

**Files to Read:**
- Design_Decisions.md
- .context/AcmeCorp_NetworkUpgrade/decisions.json

**Status:** Ready for parallel document generation
---
```

**Step 3: New Conversation**
```
User pastes resume package

I read:
- filesystem-read_file: path="Design_Decisions.md"
- filesystem-read_file: path=".context/AcmeCorp_NetworkUpgrade/decisions.json"

[Continue from where we left off with fresh context]
```

---

## 📊 Token Budget per Phase

| Phase | Target Tokens | Strategy |
|-------|---------------|----------|
| **Discovery** | 20K | Ask questions, save answers to file immediately |
| **Design** | 25K | Use Sequential Thinking MCP, write decisions to file |
| **Doc Gen** | 5K (main) + 20K per subagent | Main agent just coordinates, subagents do work |
| **Verification** | 10K | Filesystem MCP checks files |

**Total Main Agent:** ~60K tokens (safe margin)

---

## 🛠️ MCP Tools for Context Management

### Filesystem MCP — Your Best Friend

```yaml
# Write decisions immediately
filesystem-write_file:
  path: "decisions/network.json"
  content: '{"vlan_count": 8, "user_count": 500}'

# Read only when needed
filesystem-read_file:
  path: "decisions/network.json"

# Check what files exist
filesystem-list_directory:
  path: "decisions"
```

### Sequential Thinking MCP — For Complex Decisions

```yaml
# Break down complex sizing without filling context
sequentialthinking:
  thought: "Step 1: 500 users × 5 Mbps = 2.5 Gbps required"
  thoughtNumber: 1
  totalThoughts: 4
  nextThoughtNeeded: true

# Result: Final decision only kept in context
# Intermediate thoughts discarded
```

### Task (Subagents) — Parallel = Context Efficient

Each subagent gets **fresh context** — no accumulation!

```yaml
# Launch 3 subagents — each has independent context
Task: [Part 1]  # 20K tokens used
Task: [Part 2]  # 20K tokens used (parallel, not added)
Task: [Part 3]  # 20K tokens used (parallel, not added)

# Main agent context: Only coordination (~5K)
```

---

## 📋 Context-Saving Checklist

### Before Starting
- [ ] Initialize ContextManager: `cm = ContextManager("Client_Project")`
- [ ] Create `.context/` directory

### During Discovery
- [ ] After each question group, save summary to file
- [ ] Mark completed groups: `cm.mark_group_completed(0)`
- [ ] Keep only group numbers in context, not full answers

### During Design
- [ ] Use Sequential Thinking MCP for complex calculations
- [ ] Save each decision: `cm.save_decision(key, value, category)`
- [ ] Write Design_Decisions.md incrementally

### During Doc Gen
- [ ] Main agent only coordinates (minimal context)
- [ ] Subagents read Design_Decisions.md independently
- [ ] Each part written to file, not kept in context

### Before Breaking Conversation
- [ ] Save all decisions with ContextManager
- [ ] Write complete Design_Decisions.md
- [ ] Generate resume prompt: `cm.generate_resume_prompt()`
- [ ] List all files user needs to upload to new conversation

---

## 🚨 Emergency Context Recovery

### If Context Suddenly Fills

**Immediate Actions:**
1. Stop current generation
2. Save what you have:
   ```
   filesystem-write_file: path="EMERGENCY_SAVE.md" content=[what was generated]
   ```
3. Generate minimal resume package
4. Tell user: "Context full. Starting fresh conversation. Upload these files: [list]"

### Resume in New Conversation

```
User: [pastes resume package]

I:
1. Read Design_Decisions.md
2. Read any completed part files
3. Check .context/ directory
4. Resume from where we left off
```

---

## 💡 Pro Tips

### 1. Never Keep Full Tables in Context

❌ **Bad:**
```
| VLAN | Subnet | Gateway | ... [8 rows] |
```

✅ **Good:**
```
VLAN scheme: See Design_Decisions.md section "Network Design"
[Only reference in context]
```

### 2. Use Incremental Writes

Instead of building full document in context:

```python
# Write sections as they're ready
filesystem-write_file: path="Part1_Section1.md" content=[section]
filesystem-write_file: path="Part1_Section2.md" content=[section]

# At end, merge
Shell: cat Part1_Section*.md > Part1_Final.md
```

### 3. Subagent Chaining

If a part is too big for one subagent:

```
Subagent A: Part 1 Section 1 → Writes to Part1_Sec1.md
Subagent B: Part 1 Section 2 → Writes to Part1_Sec2.md
[Wait]
Subagent C: Merges Part1_Sec*.md → Writes Part1_Final.md
```

### 4. Diagram References

Keep diagram **code** in files, not rendered images in context:

```
Diagram: See diagrams/network_topology.mmd
[Subagent renders to PNG when generating document]
```

---

## 📁 File Organization for Context Management

```
.context/
├── AcmeCorp_NetworkUpgrade/
│   ├── decisions.json          # Structured decisions
│   ├── conversation_summary.md # Running summary
│   ├── state.json              # Current phase, completed groups
│   └── resume_prompt.md        # Generated resume package
├── Design_Decisions.md         # Master design spec
diagrams/
├── network_topology.mmd        # Mermaid source
├── network_topology.png        # Rendered (generated)
└── ...
```

---

## 🎯 Summary

| Instead of... | Do this... |
|---------------|------------|
| Keeping answers in context | Write to file immediately |
| Full conversation history | Summaries only |
| Building docs in context | Subagents write to files |
| Tables in context | File references |
| One long conversation | Break at 100K, resume fresh |

**Result:** Never hit context limit again!

---

*Use this guide with `scripts/context_manager.py` for bulletproof context management.*
