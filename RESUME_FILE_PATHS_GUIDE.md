# Resume File Paths — Exact Paths to Tell the User

## ⚠️ CRITICAL: Give Users Exact File Paths

When breaking a conversation, always provide the **exact file paths** the user needs to download and upload. This prevents confusion.

---

## 📋 Standard File Path Template

### When Breaking Conversation, Tell User:

```
⚠️ CONTEXT WINDOW FULL — CONVERSATION BREAK REQUIRED

To continue in a new conversation, you MUST download these files:

═══════════════════════════════════════════════════════════
📁 FILES TO DOWNLOAD (Save to your computer):
═══════════════════════════════════════════════════════════

1.  Design_Decisions.md
    → Located in: Current working directory
    
2.  Part1_Executive_Architecture_ISO.md
    → Located in: Current working directory
    
3.  Part2_Network_Wireless_Server.md
    → Located in: Current working directory (if generated)
    
4.  Part3_DR_Monitoring_Power.md
    → Located in: Current working directory (if generated)
    
5.  .context/AcmeCorp_NetworkUpgrade/decisions.json
    → Located in: .context/AcmeCorp_NetworkUpgrade/
    
6.  .context/AcmeCorp_NetworkUpgrade/state.json
    → Located in: .context/AcmeCorp_NetworkUpgrade/
    
7.  .context/AcmeCorp_NetworkUpgrade/conversation_summary.md
    → Located in: .context/AcmeCorp_NetworkUpgrade/

═══════════════════════════════════════════════════════════
📋 HOW TO DOWNLOAD:
═══════════════════════════════════════════════════════════

In VS Code:
1. Right-click on each file in Explorer sidebar
2. Select "Download" or "Reveal in File Explorer"
3. Save to a folder (e.g., Desktop/AcmeCorp_Resume/)

OR

Use terminal:
cd [your project directory]
cp Design_Decisions.md ~/Desktop/AcmeCorp_Resume/
cp Part1_*.md ~/Desktop/AcmeCorp_Resume/
cp Part2_*.md ~/Desktop/AcmeCorp_Resume/
cp Part3_*.md ~/Desktop/AcmeCorp_Resume/
cp -r .context/AcmeCorp_NetworkUpgrade ~/Desktop/AcmeCorp_Resume/

═══════════════════════════════════════════════════════════
▶️ START NEW CONVERSATION:
═══════════════════════════════════════════════════════════

1. Start a NEW chat with me
2. UPLOAD these files by dragging them into the chat:
   - Design_Decisions.md
   - Part1_Executive_Architecture_ISO.md
   - Part2_Network_Wireless_Server.md (if exists)
   - Part3_DR_Monitoring_Power.md (if exists)
   - .context/AcmeCorp_NetworkUpgrade/ (upload entire folder)

3. PASTE this resume summary:

---
[RESUME SUMMARY WILL BE HERE]
---

═══════════════════════════════════════════════════════════
```

---

## 🎯 Practical Example

### Scenario: Breaking After Part 3

**You say to user:**

```
⚠️ CONTEXT AT 120K TOKENS — BREAKING CONVERSATION

I've generated Parts 1-3 successfully. To continue with Parts 4-6,
we need to start fresh (new context window).

═══════════════════════════════════════════════════════════
📁 DOWNLOAD THESE FILES (7 files total):
═══════════════════════════════════════════════════════════

From your project folder (c:\Users\Mukund Neeli\OneDrive\Desktop\VSC-KIMI\~\.config\agents\skills\vconfi-solution-architect):

1.  Design_Decisions.md
    Full path: c:\Users\...\vconfi-solution-architect\Design_Decisions.md
    
2.  Part1_Executive_Architecture_ISO.md
    Full path: c:\Users\...\vconfi-solution-architect\Part1_Executive_Architecture_ISO.md
    
3.  Part2_Network_Wireless_Server.md
    Full path: c:\Users\...\vconfi-solution-architect\Part2_Network_Wireless_Server.md
    
4.  Part3_DR_Monitoring_Power.md
    Full path: c:\Users\...\vconfi-solution-architect\Part3_DR_Monitoring_Power.md

From .context folder:

5.  .context/AcmeCorp_NetworkUpgrade/decisions.json
    Full path: c:\Users\...\vconfi-solution-architect\.context\AcmeCorp_NetworkUpgrade\decisions.json
    
6.  .context/AcmeCorp_NetworkUpgrade/state.json
    Full path: c:\Users\...\vconfi-solution-architect\.context\AcmeCorp_NetworkUpgrade\state.json
    
7.  .context/AcmeCorp_NetworkUpgrade/conversation_summary.md
    Full path: c:\Users\...\vconfi-solution-architect\.context\AcmeCorp_NetworkUpgrade\conversation_summary.md

═══════════════════════════════════════════════════════════
📂 SAVE LOCATION:
═══════════════════════════════════════════════════════════

Create this folder structure on your Desktop:

Desktop/
└── AcmeCorp_Resume/
    ├── Design_Decisions.md
    ├── Part1_Executive_Architecture_ISO.md
    ├── Part2_Network_Wireless_Server.md
    ├── Part3_DR_Monitoring_Power.md
    └── .context/
        └── AcmeCorp_NetworkUpgrade/
            ├── decisions.json
            ├── state.json
            └── conversation_summary.md

═══════════════════════════════════════════════════════════
▶️ IN NEW CONVERSATION:
═══════════════════════════════════════════════════════════

1. Start new chat with me
2. Upload ALL files from Desktop/AcmeCorp_Resume/
3. Also paste this summary:

---
# Resume Session: AcmeCorp_NetworkUpgrade

## Current Phase
document_generation

## Progress
- Part 1: ✓ Complete (Executive Summary, Architecture, ISO)
- Part 2: ✓ Complete (Network, Wireless, Servers)
- Part 3: ✓ Complete (DR, Monitoring, Power)
- Part 4: Next (BOM, Assets, Timeline)
- Part 5: Pending (Security Stress Test)
- Part 6: Pending (SOPs)

## Key Decisions
- Firewall: FortiGate 200F
- Core Switch: Aruba CX 6300
- VLANs: 8
- Users: 500
- Sites: 3

## Files Attached
- Design_Decisions.md (complete design spec)
- Part1_*.md, Part2_*.md, Part3_*.md (completed parts)
- .context/AcmeCorp_NetworkUpgrade/ (session state)
---

═══════════════════════════════════════════════════════════
```

---

## 🔍 Visual: What User Sees in VS Code

```
VS Code Explorer Sidebar:

📁 VCONFI-SOLUTION-ARCHITECT/
├── 📄 Design_Decisions.md          ← DOWNLOAD THIS
├── 📄 Part1_Executive_...md        ← DOWNLOAD THIS
├── 📄 Part2_Network_...md          ← DOWNLOAD THIS
├── 📄 Part3_DR_...md               ← DOWNLOAD THIS
├── 📄 Part4_BOM_...md              (in progress)
├── 📄 SKILL.md
├── 📁 .context/                    ← EXPAND THIS FOLDER
│   └── 📁 AcmeCorp_NetworkUpgrade/  ← DOWNLOAD THIS FOLDER
│       ├── 📄 decisions.json       ← (inside folder)
│       ├── 📄 state.json           ← (inside folder)
│       └── 📄 conversation_summary.md  ← (inside folder)
├── 📁 scripts/
├── 📁 memory/
└── 📁 templates/
```

**User right-clicks each file → "Download" or "Reveal in File Explorer"**

---

## 📤 Visual: What User Uploads in New Chat

```
New Chat Window:

[User drags files here]

Uploading:
✓ Design_Decisions.md (156 KB)
✓ Part1_Executive_Architecture_ISO.md (234 KB)
✓ Part2_Network_Wireless_Server.md (189 KB)
✓ Part3_DR_Monitoring_Power.md (167 KB)
✓ decisions.json (12 KB)
✓ state.json (3 KB)
✓ conversation_summary.md (45 KB)

[User pastes resume summary]
```

---

## ✅ Checklist: What User Must Upload

### Minimum Required (3 files):
- [ ] `Design_Decisions.md` — Contains complete design spec
- [ ] `.context/[session]/decisions.json` — Structured decisions
- [ ] `.context/[session]/state.json` — Current phase

### Recommended (6+ files):
- [ ] `Design_Decisions.md`
- [ ] `Part1_Executive_Architecture_ISO.md` — If generated
- [ ] `Part2_Network_Wireless_Server.md` — If generated
- [ ] `Part3_DR_Monitoring_Power.md` — If generated
- [ ] `.context/[session]/decisions.json`
- [ ] `.context/[session]/state.json`
- [ ] `.context/[session]/conversation_summary.md`

---

## 🚫 Common Mistakes to Avoid

### Mistake 1: Vague Paths
❌ **BAD:** "Download the files"
✅ **GOOD:** "Download Design_Decisions.md from root folder"

### Mistake 2: Missing .context Folder
❌ **BAD:** Only mentioning markdown files
✅ **GOOD:** Explicitly listing .context/[session]/ folder

### Mistake 3: Wrong Folder Depth
❌ **BAD:** ".context/decisions.json"
✅ **GOOD:** ".context/AcmeCorp_NetworkUpgrade/decisions.json"

### Mistake 4: Forgetting Part Files
❌ **BAD:** Only Design_Decisions.md
✅ **GOOD:** All Part*.md files that were completed

---

## 📝 Template: Copy-Paste Message to User

```markdown
⚠️ CONTEXT FULL — SAVE & RESUME REQUIRED

🛑 Download these files NOW:

From your project folder:
1. Design_Decisions.md
2. Part1_Executive_Architecture_ISO.md
3. Part2_Network_Wireless_Server.md
4. Part3_DR_Monitoring_Power.md

From .context/ folder:
5. .context/AcmeCorp_NetworkUpgrade/decisions.json
6. .context/AcmeCorp_NetworkUpgrade/state.json
7. .context/AcmeCorp_NetworkUpgrade/conversation_summary.md

💾 Save to: Desktop/AcmeCorp_Resume/

▶️ Then start NEW conversation and:
1. Upload all files above
2. Paste this summary:

---
RESUME: AcmeCorp_NetworkUpgrade
Phase: document_generation
Progress: Parts 1-3 ✓ | Part 4-6 pending
Key: 500 users, FortiGate 200F, 8 VLANs
Files: [all files listed above attached]
---

I'll resume immediately with fresh context!
```

---

## 🎯 Verification: Confirm User Has All Files

**In new conversation, after user uploads, verify:**

```yaml
filesystem-list_directory: path="."
# Should see: Design_Decisions.md, Part1_*.md, Part2_*.md, etc.

filesystem-list_directory: path=".context/AcmeCorp_NetworkUpgrade"
# Should see: decisions.json, state.json, conversation_summary.md
```

**Then confirm:**
```
✓ Verified files uploaded:
  - Design_Decisions.md ✓
  - Part1_Executive_Architecture_ISO.md ✓
  - Part2_Network_Wireless_Server.md ✓
  - Part3_DR_Monitoring_Power.md ✓
  - decisions.json ✓
  - state.json ✓
  
✓ Resuming AcmeCorp_NetworkUpgrade
✓ Continuing Part 4 (BOM)
```

---

## 📂 Complete File Tree for User

```
USER'S COMPUTER:
│
└── Desktop/
    └── AcmeCorp_Resume/           ← CREATE THIS FOLDER
        │
        ├── Design_Decisions.md    ← DOWNLOAD FROM PROJECT ROOT
        │
        ├── Part1_Executive_       ← DOWNLOAD FROM PROJECT ROOT
        │   Architecture_ISO.md
        │
        ├── Part2_Network_         ← DOWNLOAD FROM PROJECT ROOT
        │   Wireless_Server.md
        │
        ├── Part3_DR_Monitoring_   ← DOWNLOAD FROM PROJECT ROOT
        │   Power.md
        │
        └── .context/              ← CREATE THIS FOLDER
            └── AcmeCorp_NetworkUpgrade/   ← DOWNLOAD ENTIRE FOLDER
                ├── decisions.json
                ├── state.json
                └── conversation_summary.md
```

---

## ✅ Summary

| What | Exact Path |
|------|-----------|
| Design Spec | `Design_Decisions.md` |
| Completed Part 1 | `Part1_Executive_Architecture_ISO.md` |
| Completed Part 2 | `Part2_Network_Wireless_Server.md` |
| Completed Part 3 | `Part3_DR_Monitoring_Power.md` |
| Decisions Data | `.context/[session]/decisions.json` |
| State Data | `.context/[session]/state.json` |
| History | `.context/[session]/conversation_summary.md` |

**Always give exact paths. Never assume user knows where to look.**
