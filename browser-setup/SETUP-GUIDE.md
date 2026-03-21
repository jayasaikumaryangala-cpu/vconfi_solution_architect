# VConfi Solution Architect — Claude AI Browser Setup Guide

## Prerequisites
- Claude Pro or Team plan (required for Projects and extended context)
- Web search enabled in your Claude account

## Step-by-Step Setup

### Step 1: Create a New Project
1. Go to **claude.ai**
2. Click the **Projects** icon in the left sidebar (folder icon)
3. Click **"+ Create project"**
4. Name it: **VConfi Solution Architect**
5. (Optional) Add a description: "IT infrastructure solution design with ISO 27001 compliance"

### Step 2: Add Project Instructions
1. Inside the project, click **"Set custom instructions"** (or the gear icon → Custom instructions)
2. Copy the ENTIRE contents of `project-instructions.md` (in this folder) and paste it into the instructions field
3. Click **Save**

### Step 3: Upload Knowledge Files
1. Inside the project, click **"Add content"** → **"Upload files"**
2. Upload these 5 files from the skill directory:

| File to Upload | Location in Skill Directory |
|---------------|----------------------------|
| `iso-27001-controls.md` | `references/iso-27001-controls.md` |
| `vendor-reference.md` | `references/vendor-reference.md` |
| `security-stress-test.md` | `references/security-stress-test.md` |
| `output-format.md` | `references/output-format.md` |
| `implementation-plan.html` | `templates/implementation-plan.html` |

These files load on-demand (only when Claude needs them), saving your 200K context window for actual document generation.

### Step 4: Enable Web Search
1. When you start a conversation, look for the **web search toggle** (globe icon) at the bottom of the chat input
2. Make sure it is **enabled** (toggled on)
3. This allows Claude to search for live pricing, current product models, and verify availability

### Step 5: Start Your First Engagement
1. Click **"Start chat"** within the project
2. Type your client brief, e.g.:
   - "New client: ABC Manufacturing, 200 users, new office in Pune"
   - "Design infrastructure for a healthcare company with 50 users"
   - Or simply say "Let's start" and Claude will begin with the discovery questions
3. Claude will automatically follow the VConfi Solution Architect workflow

## How It Works

```
You type client brief
        ↓
Claude asks Group 0-7 questions (one group at a time)
        ↓
Claude designs solution across 12 sections (with your approval)
        ↓
Claude generates "Design Decisions Summary" artifact (your safety net)
        ↓
Claude generates 7 HTML artifacts back-to-back (Parts 1-5, 6a, 6b)
        ↓
Claude auto-merges all parts into ONE final combined HTML artifact
        ↓
You print the single combined artifact to PDF
```

## Tips for Best Results

### Save Context
- Answer questions concisely — no need to repeat the question back
- When approving a part, just say "approved" or "looks good, next"
- Don't ask Claude to re-explain things already covered

### If Context Runs Low
If Claude warns about context limits mid-generation:
1. Download the "Design Decisions Summary" artifact (it was generated earlier)
2. Start a **new conversation** in the same project
3. Upload or paste the Design Decisions Summary
4. Tell Claude: "Continue from Part X. Here are the design decisions from our previous conversation."
5. Claude will pick up right where you left off

### Printing to PDF
After Claude generates all parts and the final combined artifact:
1. Click on the **final combined artifact** to open it in full view
2. Right-click → **Print** (or Ctrl+P / Cmd+P)
3. Select **"Save as PDF"** as the printer
4. Set paper size to **A4**, margins to **Default**
5. Click **Save** — you get one complete PDF with all parts

### Each Client = New Conversation
- Start a new conversation within the project for each client
- The project instructions and knowledge files persist across all conversations
- Previous conversation history does NOT carry over (which is good — clean context)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Claude doesn't follow the questioning workflow | Check that project instructions are saved correctly. Try: "Follow the VConfi Solution Architect workflow and start with Group 0 questions." |
| Artifact is cut off / incomplete | Say: "This artifact appears truncated. Please regenerate the complete Part X." |
| Web search not working | Make sure the globe icon is toggled on at the bottom of the chat input |
| Claude forgets earlier design decisions | This means context is running low. Start a new conversation with the Design Decisions Summary. |
| CSS/styling looks wrong in artifact | Make sure Claude included the full `<style>` block from the HTML template. Say: "The styling is missing. Please regenerate with the full CSS from the implementation-plan.html template." |
| Mermaid diagrams not rendering | The artifact needs the Mermaid CDN script tag. Say: "Please include the Mermaid.js CDN script and wrap diagrams in `<pre class='mermaid'>` tags." |
