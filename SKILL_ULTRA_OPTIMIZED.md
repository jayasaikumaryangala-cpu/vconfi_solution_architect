---
 name: vconfi-solution-architect
 description: Design and plan secure, optimized IT infrastructure solutions for VConfi. Optimized for MCP tools, parallel subagents, context management, and perfect diagram rendering. Generates professional implementation plans with embedded diagrams, all priced in INR.
 argument-hint: "client name or project brief"
 disable-model-invocation: true
 ---
 
 # VConfi Solution Architect — Ultra-Optimized Edition
 
 > **🚀 ULTRA-OPTIMIZED:** Context-aware, parallel subagents, perfect diagrams, 5× faster than sequential.
 
 ## ⚡ Ultra-Fast Workflow Summary
 
 | Phase | Time | Key Optimization |
 |-------|------|------------------|
 | Discovery | 3 min | ContextManager + Filesystem MCP |
 | Design | 5 min | Sequential Thinking + incremental file writes |
 | Doc Gen | 8 min | 6 subagents in 2 parallel batches |
 | Diagram Render | 2 min | Pre-render to PNG, embed in DOCX |
 | Merge | 1 min | Automated DOCX assembly |
 | **TOTAL** | **19 min** | **vs 90+ min traditional** |
 
 ---
 
 ## 🧠 Context Management Strategy (CRITICAL)
 
 ### The Problem: Context Window Overflow
 
 Claude has 200K tokens. Traditional approach fills it by:
 - Keeping all answers in conversation
 - Building documents in context
 - Storing full tables/diagrams in memory
 
 ### The Solution: "Write Early, Reference Often"
 
 **Use ContextManager (`scripts/context_manager.py`)**
 
 ```python
 # Initialize at start
cm = ContextManager("AcmeCorp_NetworkUpgrade")

# Save EVERY decision immediately
cm.save_decision("user_count", 500, "network")
cm.save_decision("firewall_model", "FortiGate 200F", "firewall")
cm.save_decision("vlan_count", 8, "network")

# Keep only this in context:
# "Decisions saved to .context/AcmeCorp_NetworkUpgrade/decisions.json"
```
 
 **When Context Fills (Warning at 100K tokens):**
 
 1. Save state:
    ```
    filesystem-write_file: path="Design_Decisions.md"
    cm.generate_resume_prompt()
    ```
 
 2. Generate Resume Package:
    ```
    ---
    ## SESSION RESUME
    **Client:** AcmeCorp | **Phase:** Design Complete | **Next:** Doc Gen
    
    **Files Required:**
    - Design_Decisions.md
    - .context/AcmeCorp_NetworkUpgrade/decisions.json
    
    **Key Decisions:** [summary]
    ---
    ```
 
 3. New conversation → Read files → Continue seamlessly
 
 ---
 
 ## 🎨 Perfect Diagrams Strategy (CRITICAL)
 
 ### The Problem: Mermaid Code in DOCX
 
 Clients see code blocks instead of professional diagrams.
 
 ### The Solution: Pre-Render to PNG
 
 **Pipeline:**
 ```
 Markdown with Mermaid
        ↓
 scripts/render_diagrams.py
        ↓
 PNG Images (1200×800px, white background)
        ↓
 scripts/generate_docx_with_diagrams.py
        ↓
 DOCX with Embedded Professional Diagrams
 ```
 
 **Commands:**
 ```bash
 # After subagents generate parts:
 
 # Render all diagrams
 python scripts/render_diagrams.py Part1.md --external
 python scripts/render_diagrams.py Part2.md --external
 ...
 
 # Generate DOCX with embedded images
 python scripts/generate_docx_with_diagrams.py \
     --parts Part*.md \
     --output VConfi_Plan.docx
 ```
 
 **Diagram Quality Checklist:**
 - [ ] 1200×800px minimum
 - [ ] White background
 - [ ] VConfi colors (#007ACC primary)
 - [ ] Readable text (16px minimum)
 - [ ] No cut-offs or overlaps
 
 ---
 
 ## 🔄 Complete Ultra-Optimized Workflow
 
 ### Phase 1: Discovery (3 minutes)
 
 ```yaml
 # Step 1: Check memory (Filesystem MCP)
 filesystem-read_file: path="memory/memory_index.md"
 filesystem-list_directory: path="memory/clients"
 
 # Step 2: Initialize ContextManager
 [Initialize: cm = ContextManager("Client_Project")]
 
 # Step 3: Ask Group 0 questions
 [User answers]
 
 # Step 4: Save immediately
 cm.save_decision("client_name", "AcmeCorp")
 cm.save_decision("industry", "Manufacturing")
 cm.save_conversation_summary("Group 0 complete", phase="discovery")
 
 # Step 5: Research (Web Search MCP)
 web-search: "manufacturing network best practices 2026"
 
 # Step 6: Sequential Thinking for complex sizing
 sequentialthinking:
   thought: "Analyzing 500 users across 3 sites..."
   thoughtNumber: 1
   totalThoughts: 5
 ```
 
 ### Phase 2: Design Decisions (5 minutes)
 
 ```yaml
 # Write incremental decisions
 cm.save_decision("firewall_model", "FortiGate 200F", "firewall")
 cm.save_decision("core_switch", "Aruba CX 6300", "network")
 
 # Final write to Design_Decisions.md
 filesystem-write_file:
   path: "Design_Decisions.md"
   content: [complete design spec]
 
 cm.update_state(phase="document_generation")
 ```
 
 ### Phase 3: Parallel Document Generation (8 minutes)
 
 **BATCH 1 — Launch 3 Subagents:**
 
 ```yaml
 # All 3 launched simultaneously
 Task(description="Part 1", subagent_name="coder", prompt=|
   READ: filesystem-read_file: path="Design_Decisions.md"
   WRITE: Part1_Executive_Architecture_ISO.md
   Include: 3 Mermaid diagrams (topology, VLANs, zones)
 )
 
 Task(description="Part 2", subagent_name="coder", prompt=|
   READ: filesystem-read_file: path="Design_Decisions.md"
   WRITE: Part2_Network_Wireless_Server.md
   Include: 3 Mermaid diagrams (stacking, wireless, rack)
 )
 
 Task(description="Part 3", subagent_name="coder", prompt=|
   READ: filesystem-read_file: path="Design_Decisions.md"
   WRITE: Part3_DR_Monitoring_Power.md
   Include: 4 Mermaid diagrams (backup, DR, monitoring, power)
 )
 
 # WAIT for all 3 to complete
 ```
 
 **BATCH 2 — Launch 3 Subagents:**
 
 ```yaml
 Task(description="Part 4", ...)
 Task(description="Part 5", ...)
 Task(description="Part 6", ...)
 
 # WAIT for all 3 to complete
 ```
 
 ### Phase 4: Diagram Rendering (2 minutes)
 
 ```bash
 # Shell command to render all diagrams
 for file in Part*.md; do
   python scripts/render_diagrams.py "$file" --external
done

# Verify all rendered
ls diagrams/*.png | wc -l  # Should be 15-20 diagrams
```

### Phase 5: DOCX Generation (1 minute)

```bash
# Merge with embedded diagrams
python scripts/generate_docx_with_diagrams.py \
    --parts Part*.md \
    --output "VConfi_AcmeCorp_NetworkUpgrade_$(date +%Y%m%d).docx" \
    --client "AcmeCorp" \
    --project "Network Upgrade"

# Verify file created
ls -lh *.docx
```

---

## 📋 Subagent Prompts with Diagram Instructions

### Part 1: Executive Summary (With Diagrams)

```
You are a VConfi Solutions Architect writing Part 1.

READ: filesystem-read_file: path="Design_Decisions.md"

YOUR TASK:
Write Part1_Executive_Architecture_ISO.md

REQUIRED MERMAID DIAGRAMS:
1. Network Topology (graph TD):
   ```mermaid
   graph TD
       ISP1[ISP 1 - Airtel] --> FW1[FortiGate Primary]
       ISP2[ISP 2 - Jio] --> FW1
       FW1 --> |HA| FW2[FortiGate Secondary]
       FW1 --> CORE1[Core Switch 1]
       FW2 --> CORE2[Core Switch 2]
       CORE1 <-->|LACP| CORE2
   ```

2. VLAN Segmentation (graph LR with subgraphs):
   ```mermaid
   graph LR
       subgraph "Core Network"
           FW[FortiGate]
       end
       subgraph "VLANs"
           FW --> VLAN10[VLAN 10<br/>Mgmt]
           FW --> VLAN20[VLAN 20<br/>Users]
           FW --> VLAN30[VLAN 30<br/>Servers]
       end
   ```

3. Firewall Zones (graph TB):
   ```mermaid
   graph TB
       subgraph "Trust Zone"
           USERS[User VLANs]
           SERVERS[Server VLAN]
       end
       subgraph "Untrust Zone"
           INTERNET[Internet]
       end
       subgraph "DMZ Zone"
           DMZ[DMZ Servers]
       end
       FW[FortiGate] --- USERS
       FW --- SERVERS
       FW --- INTERNET
       FW --- DMZ
   ```

WRITE OUTPUT TO: Part1_Executive_Architecture_ISO.md

ZERO COMPRESSION RULES:
- All tables fully populated
- NO placeholders
- Include all 8 VLANs if 8 were decided
```

### Part 2: Network Design (With Diagrams)

```
REQUIRED DIAGRAMS:
1. Switch Stacking (graph TB):
   Show physical stacking connections

2. Wireless Coverage (flowchart):
   Floor-by-floor AP placement

3. Server Rack Layout (graph LR or ASCII art):
   RU positions for each device
```

### Part 3: DR/Monitoring (With Diagrams)

```
REQUIRED DIAGRAMS:
1. Backup 3-2-1 Flow (graph LR)
2. DR Replication (graph TB with Primary ↔ DR)
3. Monitoring Architecture (graph TD showing Zabbix → Devices)
4. Power Distribution (graph TD: Mains → ATS → UPS → PDU)
```

---

## 🛠️ Required Diagrams Checklist

| Part | Diagram | Type | Size |
|------|---------|------|------|
| 1 | Network Topology | graph TD | 1200×800 |
| 1 | VLAN Segmentation | graph LR | 1000×600 |
| 1 | Firewall Zones | graph TB | 800×600 |
| 2 | Switch Stacking | graph TB | 1000×600 |
| 2 | Wireless Coverage | flowchart | 1200×800 |
| 2 | Server Rack | graph LR | 600×800 |
| 3 | Backup 3-2-1 | graph LR | 1000×600 |
| 3 | DR Replication | graph TB | 1000×600 |
| 3 | Monitoring | graph TD | 1000×600 |
| 3 | Power Dist | graph TD | 1000×600 |
| 4 | Gantt Timeline | gantt | 1200×600 |
| 5 | Attack Surface | graph TD | 1000×600 |
| 6 | Escalation Flow | flowchart | 800×600 |

**Total: 15 diagrams minimum**

---

## 📊 Context Budget Management

| Component | Token Budget | File Offload Strategy |
|-----------|--------------|----------------------|
| Discovery Q&A | 15K | Save answers to decisions.json |
| Design Discussion | 20K | Incremental writes to Design_Decisions.md |
| Main Agent Coordination | 10K | Only file references, no content |
| Per Subagent | 25K | Fresh context per subagent |
| **Total Main Agent** | **~45K** | **Safe 75K buffer** |

---

## 🚨 Break Conversation Protocol

### When to Break

- Token count > 100K (warning)
- Token count > 150K (immediate action)
- User requests break

### Break Procedure

1. **Save Everything:**
   ```
   filesystem-write_file: path="Design_Decisions.md"
   cm.save_conversation_summary("Breaking conversation", phase="design")
   resume = cm.generate_resume_prompt()
   ```

2. **Provide Resume Package:**
   ```
   ## SESSION BREAK — RESUME PACKAGE
   
   **Status:** Conversation break requested
   **Last Phase:** [phase]
   **Files Required:**
   - Design_Decisions.md
   - .context/[session]/decisions.json
   
   **Upload these files to new conversation and paste:**
   [paste resume text]
   ```

3. **In New Conversation:**
   ```
   User uploads files
   → I read: Design_Decisions.md
   → I read: decisions.json
   → Continue seamlessly
   ```

---

## ✅ Quality Assurance Checklist

### Before Client Delivery

**Context Management:**
- [ ] All decisions saved to files
- [ ] No placeholders in any part
- [ ] Can resume from any point

**Diagrams:**
- [ ] All 15+ diagrams rendered to PNG
- [ ] 1200×800px minimum resolution
- [ ] White backgrounds
- [ ] Professional appearance
- [ ] Embedded in DOCX (not code blocks)

**Content:**
- [ ] All tables fully populated
- [ ] All 11 SOPs complete
- [ ] BOM accurate with pricing
- [ ] ISO 27001 mapping complete
- [ ] Security stress test performed

**Technical:**
- [ ] DOCX generates without errors
- [ ] File size < 50MB (for email)
- [ ] All diagrams visible
- [ ] Page numbers correct

---

## 📚 Reference Files

| File | Purpose |
|------|---------|
| `CONTEXT_MANAGEMENT_GUIDE.md` | Detailed context management |
| `DIAGRAM_RENDERING_GUIDE.md` | Diagram rendering workflow |
| `MCP_CHEAT_SHEET.md` | Quick MCP command reference |
| `templates/subagent-prompts.md` | Ready-to-use subagent prompts |
| `scripts/context_manager.py` | Context management tool |
| `scripts/render_diagrams.py` | Diagram rendering tool |
| `scripts/generate_docx_with_diagrams.py` | Enhanced DOCX generator |

---

## 🎯 Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Total Time | < 25 minutes | From discovery to DOCX |
| Context Usage | < 75K tokens | Main agent only |
| Diagram Quality | Client-ready | Visual inspection |
| Resume Success | 100% | Can resume from break |

---

*This ultra-optimized workflow ensures professional deliverables without context overflow.*
