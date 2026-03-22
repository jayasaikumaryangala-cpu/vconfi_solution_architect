# VConfi MCP Quick Reference Cheat Sheet

One-page reference for using MCPs with the VConfi skill.

---

## 🚀 3-Step Fast Workflow

```
Step 1: MCP Discovery (2 min)
   filesystem-read_file → memory/memory_index.md
   web-search → [industry-specific requirements]
   sequentialthinking → [complex architecture decisions]

Step 2: Write Design Decisions (1 min)
   filesystem-write_file → Design_Decisions.md

Step 3: Parallel Generation (10 min)
   Task × 3 (Batch 1) → wait → Task × 3 (Batch 2) → wait
   Shell → python scripts/generate_docx.py merge ...
```

**Total: ~13 minutes**

---

## 📋 MCP Command Patterns

### Filesystem MCP

```yaml
# Read memory files
filesystem-read_file:
  path: "memory/memory_index.md"

filesystem-list_directory:
  path: "memory/clients"

# Write design decisions
filesystem-write_file:
  path: "Design_Decisions.md"
  content: "# Design Decisions\n\n..."

# Check generated parts
filesystem-list_directory:
  path: "."
```

### Sequential Thinking MCP

```yaml
# Break down complex decisions
sequentialthinking:
  thought: "Analyzing 500-user multi-site requirements..."
  thoughtNumber: 1
  totalThoughts: 5
  nextThoughtNeeded: true

# Continue until thoughtNumber == totalThoughts
```

### Web Search MCP

```yaml
# Live pricing
web-search:
  query: "FortiGate 200F price India INR 2026"

# Product specs
web-search:
  query: "HPE DL380 Gen11 specs datasheet"

# Best practices
web-search:
  query: "ISO 27001 manufacturing industry controls 2026"
```

### Task (Subagent Launcher)

```yaml
# Launch parallel document generation
Task:
  description: "Generate Part 1: Executive Summary"
  subagent_name: "coder"
  prompt: |
    You are a VConfi Solutions Architect...
    
    READ FIRST: Design_Decisions.md
    
    YOUR TASK: Write Part 1...
    
    WRITE OUTPUT TO: Part1_Executive_Architecture_ISO.md
```

---

## 🔄 Subagent Batch Sequence

```
┌─────────────────────────────────────────────────────────────┐
│ BATCH 1 (Launch 3 at once)                                  │
├─────────────────────────────────────────────────────────────┤
│ Task A → Part1_Executive_Architecture_ISO.md                │
│ Task B → Part2_Network_Wireless_Server.md                   │
│ Task C → Part3_DR_Monitoring_Power.md                       │
└─────────────────────────────────────────────────────────────┘
                          ↓
                    [Wait for all 3]
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ BATCH 2 (Launch 3 at once)                                  │
├─────────────────────────────────────────────────────────────┤
│ Task D → Part4_BOM_Assets_Timeline.md                       │
│ Task E → Part5_Security_Stress_Test.md                      │
│ Task F → Part6_SOPs.md                                      │
└─────────────────────────────────────────────────────────────┘
                          ↓
                    [Wait for all 3]
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ MERGE                                                       │
├─────────────────────────────────────────────────────────────┤
│ Shell: python scripts/generate_docx.py merge ...            │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Key Files to Read

| When | File | Via |
|------|------|-----|
| Start | `memory/memory_index.md` | Filesystem MCP |
| Start | `memory/pricing/*.md` | Filesystem MCP |
| Start | `memory/clients/[client].md` | Filesystem MCP (if exists) |
| Design | `references/vendor-reference.md` | Filesystem MCP |
| Part 1 | `references/iso-27001-controls.md` | Subagent reads |
| Part 5 | `references/security-stress-test.md` | Subagent reads |

---

## ⚠️ Zero Compression Checklist

Before finishing each part, verify via Filesystem MCP:

```python
filesystem-read_file: path="PartX_*.md"

# Check for these forbidden patterns:
# - "[Add more"
# - "TODO"
# - "TBD"
# - "..."
# - "etc."
# - "as applicable"

# Verify:
# - All VLANs present (count them)
# - All devices in BOM
# - All SOPs complete
# - All diagrams rendered
```

---

## 💡 Pro Tips

### 1. Let Subagents Read Files
Don't paste Design_Decisions.md content into subagent prompts. Just tell them:
```
READ FIRST: filesystem-read_file: path="Design_Decisions.md"
```

### 2. Use Sequential Thinking for Complex Sizing
```yaml
sequentialthinking:
  thought: "500 users × 5 Mbps = 2.5 Gbps needed"
  thoughtNumber: 1
  totalThoughts: 3
  nextThoughtNeeded: true
```

### 3. Check Pricing First
```yaml
filesystem-read_file: path="memory/pricing/fortinet-firewalls.md"
# Fall back to web-search only if price not found
```

### 4. Parallel = Speed
Sequential: 30 minutes  
Parallel (6 subagents): 10 minutes  
**3× faster**

### 5. Filesystem MCP for Verification
```yaml
filesystem-list_directory: path="."
# Check all Part*.md files exist before merging
```

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Subagent times out | Split part into smaller chunks |
| Missing pricing | web-search for current prices |
| Context running low | Write Design_Decisions.md, start fresh chat |
| Part file incomplete | Regenerate just that part |
| DOCX generation fails | Check python-docx installed: `python -c "import docx"` |

---

## 📊 Time Comparison

| Approach | Discovery | Design | Doc Gen | Verify | **Total** |
|----------|-----------|--------|---------|--------|-----------|
| Old (Sequential) | 10 min | 15 min | 30 min | 10 min | **65 min** |
| MCP-Optimized | 5 min | 3 min | 10 min | 5 min | **23 min** |
| **Savings** | **50%** | **80%** | **67%** | **50%** | **65%** |

---

## 🎯 One-Liner Commands

### Check Memory
```
filesystem-read_file: path="memory/memory_index.md"
filesystem-list_directory: path="memory/clients"
```

### Get Pricing
```
filesystem-read_file: path="memory/pricing/fortinet-firewalls.md"
web-search: "FortiGate 200F latest price India"
```

### Launch Batch 1
```
Task(description="Part 1", subagent_name="coder", prompt="...")
Task(description="Part 2", subagent_name="coder", prompt="...")
Task(description="Part 3", subagent_name="coder", prompt="...")
```

### Verify & Merge
```
filesystem-list_directory: path="."
Shell: python scripts/generate_docx.py merge --parts Part*.md --output Final.docx
```

---

*Keep this cheat sheet handy for every engagement!*
