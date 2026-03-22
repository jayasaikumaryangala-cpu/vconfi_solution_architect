# Kimi Code CLI — Ultimate Optimization Guide
## Peak Performance Configuration v1.0

---

## 🎯 Executive Summary

This guide will configure Kimi Code CLI for **maximum capability**, including:
- **MCP Servers** for extended functionality
- **Everything-Claude-Code Plugin** for 28 agents + 116 skills
- **Web Search** always enabled globally
- **Context optimization** fixes
- **Best-in-class settings**

---

## Phase 1: Install Everything-Claude-Code Plugin

### Step 1: Add Marketplace

```bash
# In Kimi Code CLI, run:
/plugin marketplace add affaan-m/everything-claude-code
```

### Step 2: Install Plugin

```bash
/plugin install everything-claude-code@everything-claude-code
```

### Step 3: Install Rules (CRITICAL)

Rules cannot be auto-installed via plugins. Install manually:

```bash
# Clone the repository
git clone https://github.com/affaan-m/everything-claude-code.git

# Windows PowerShell
cd everything-claude-code
.\install.ps1 typescript python golang

# Or for all languages
.\install.ps1 typescript python golang swift php
```

This installs:
- ✅ 28 specialized agents
- ✅ 116 skills
- ✅ 59 slash commands
- ✅ Hooks for automation
- ✅ Coding rules and standards

---

## Phase 2: Configure MCP Servers

Create/edit: `~/.kimi/mcp-servers.json`

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_GITHUB_TOKEN"
      }
    },
    "web-search": {
      "command": "npx",
      "args": ["-y", "@mcp/server-web-search"]
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@mcp/server-fetch"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\saikumaryangala"]
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"]
    },
    "browser-tools": {
      "command": "npx",
      "args": ["-y", "@mcp/browser-tools-mcp"]
    },
    "supabase": {
      "command": "npx",
      "args": ["-y", "@supabase/mcp-server-supabase"],
      "env": {
        "SUPABASE_ACCESS_TOKEN": "YOUR_SUPABASE_TOKEN"
      }
    },
    "vercel": {
      "command": "npx",
      "args": ["-y", "@mcp/server-vercel"],
      "env": {
        "VERCEL_TOKEN": "YOUR_VERCEL_TOKEN"
      }
    }
  }
}
```

### Install MCP Dependencies

```bash
# Install Node.js if not already installed
# Then install MCP servers globally
npm install -g @modelcontextprotocol/server-github
npm install -g @mcp/server-web-search
npm install -g @mcp/server-fetch
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-sequential-thinking
npm install -g @modelcontextprotocol/server-memory
npm install -g @context7/mcp-server
npm install -g @mcp/browser-tools-mcp
```

---

## Phase 3: Global Settings Configuration

Create/edit: `~/.kimi/settings.json`

```json
{
  "model": "kimi-k2-0711-preview",
  "maxTokens": 8192,
  "temperature": 0.7,
  "topP": 0.9,
  
  "webSearch": {
    "enabled": true,
    "default": true
  },
  
  "mcp": {
    "enabled": true,
    "servers": [
      "github",
      "web-search",
      "fetch",
      "filesystem",
      "sequential-thinking",
      "memory",
      "context7",
      "browser-tools"
    ]
  },
  
  "plugins": {
    "enabled": true,
    "autoLoad": true,
    "marketplaces": [
      "affaan-m/everything-claude-code"
    ],
    "installed": [
      "everything-claude-code@everything-claude-code"
    ]
  },
  
  "skills": {
    "autoLoad": true,
    "directories": [
      "~/.kimi/skills",
      "~/.claude/skills",
      "~/.config/agents/skills"
    ]
  },
  
  "agents": {
    "autoLoad": true,
    "directories": [
      "~/.kimi/agents",
      "~/.claude/agents"
    ]
  },
  
  "commands": {
    "autoLoad": true,
    "directories": [
      "~/.kimi/commands",
      "~/.claude/commands"
    ]
  },
  
  "rules": {
    "autoLoad": true,
    "directories": [
      "~/.kimi/rules",
      "~/.claude/rules"
    ]
  },
  
  "hooks": {
    "enabled": true,
    "autoLoad": true
  },
  
  "context": {
    "maxSize": 200000,
    "warningThreshold": 150000,
    "autoCompact": true,
    "compactThreshold": 180000
  },
  
  "editor": {
    "autoSave": true,
    "formatOnSave": true,
    "defaultFormatter": "prettier"
  },
  
  "terminal": {
    "shell": "powershell",
    "integrateWithVSCode": true
  },
  
  "security": {
    "confirmDestructiveOperations": true,
    "confirmBashCommands": true,
    "allowGitOperations": true,
    "confirmBeforePush": true
  },
  
  "performance": {
    "parallelToolCalls": true,
    "maxParallelCalls": 5,
    "cacheResults": true,
    "cacheDuration": 3600
  },
  
  "logging": {
    "level": "info",
    "saveToFile": true,
    "logDirectory": "~/.kimi/logs"
  },
  
  "experimental": {
    "enableAIOps": true,
    "enablePredictiveMaintenance": true,
    "enableContinuousLearning": true
  }
}
```

---

## Phase 4: Context Window Optimization

### Fix Context Issues

Create: `~/.kimi/context-optimizer.json`

```json
{
  "contextManagement": {
    "strategy": "sliding-window",
    "maxTokens": 200000,
    "reserveTokens": 20000,
    
    "compression": {
      "enabled": true,
      "threshold": 150000,
      "method": "summarize",
      "preserveRecent": 10
    },
    
    "prioritization": {
      "systemPrompt": "highest",
      "currentFile": "highest",
      "recentHistory": "high",
      "projectContext": "high",
      "skills": "medium",
      "generalKnowledge": "low"
    },
    
    "cleanup": {
      "autoRemoveOld": true,
      "keepLastNMessages": 50,
      "summarizeBeforeRemove": true
    }
  },
  
  "memory": {
    "persistent": true,
    "storage": "~/.kimi/memory.db",
    "autoSave": true,
    "autoLoad": true,
    
    "keyValueStore": {
      "enabled": true,
      "maxEntries": 1000
    }
  },
  
  "subagents": {
    "forkContext": true,
    "inheritSkills": true,
    "maxConcurrent": 3
  }
}
```

### Strategic Compaction Rules

Create: `~/.kimi/rules/context-management.md`

```markdown
---
name: context-management
description: Optimize context window usage
---

## Context Management Rules

### When Context Exceeds 150K Tokens:
1. Summarize older conversation turns
2. Extract key decisions and actions
3. Remove redundant code snippets
4. Keep full content of current task

### When Context Exceeds 180K Tokens:
1. Compact aggressively
2. Archive completed work to files
3. Start new context with summary
4. Provide continuation reference

### Always Preserve:
- Current task requirements
- Recent error messages
- Active file contents
- User preferences from session

### Safe to Remove:
- Successful test outputs
- Old file listings
- Resolved error messages
- Superseded code versions
```

---

## Phase 5: Web Search Configuration

### Global Web Search Enable

Add to `~/.kimi/settings.json`:

```json
{
  "webSearch": {
    "enabled": true,
    "default": true,
    "autoSearch": true,
    "searchThreshold": 0.7,
    "maxResults": 10,
    "includeContent": true,
    "cacheResults": true,
    "cacheDuration": 3600
  }
}
```

### Web Search Triggers

Create: `~/.kimi/rules/web-search-triggers.md`

```markdown
---
name: web-search-triggers
description: Automatically trigger web search when needed
---

## Auto-Search Triggers

ALWAYS search web when:
- User asks about "latest", "newest", "recent"
- Question involves versions, releases, updates
- Pricing or availability questions
- Technical documentation lookup
- Best practices or comparisons
- Error messages or bug fixes
- Security vulnerabilities
- API changes or deprecations

NEVER search when:
- Working with local files only
- Code refactoring without external deps
- Pure logic or algorithm questions
- Already have current information
```

---

## Phase 6: Install Additional Tools

### Essential Global Tools

```bash
# Install via npm
npm install -g typescript
npm install -g @anthropic-ai/claude-code
npm install -g @modelcontextprotocol/server-github
npm install -g @mcp/server-web-search
npm install -g prettier
npm install -g eslint
npm install -g @vscode/vscode-languagedetection

# Install via pip
pip install python-dotenv
pip install requests
pip install beautifulsoup4
pip install PyPDF2
pip install python-docx
pip install openpyxl

# Install via winget (Windows)
winget install Git.Git
winget install Node.js
winget install Python.Python.3.11
winget install Microsoft.PowerShell
winget install Microsoft.WindowsTerminal
```

### VS Code Extensions (if using VS Code)

```json
{
  "recommendations": [
    "moonshot-ai.kimi-code",
    "ms-vscode.vscode-typescript-next",
    "ms-python.python",
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "ms-vscode.powershell",
    "github.copilot",
    "github.copilot-chat",
    "eamodio.gitlens",
    "christian-kohler.path-intellisense",
    "ms-vscode.vscode-json"
  ]
}
```

---

## Phase 7: Custom Skills Setup

### Create Global Skills Directory

```bash
# Create skills directories
mkdir -p ~/.kimi/skills
mkdir -p ~/.kimi/agents
mkdir -p ~/.kimi/commands
mkdir -p ~/.kimi/rules
mkdir -p ~/.kimi/hooks
mkdir -p ~/.kimi/logs
mkdir -p ~/.kimi/memory
```

### Install Your VConfi Skill Globally

```bash
# Copy your skill to global location
cp -r "c:\Users\saikumaryangala\Downloads\skills for vconfi\.claude\skills\vconfi-solution-architect" ~/.kimi/skills/

# Or create symlink
mklink /D "%USERPROFILE%\.kimi\skills\vconfi-solution-architect" "c:\Users\saikumaryangala\Downloads\skills for vconfi\.claude\skills\vconfi-solution-architect"
```

---

## Phase 8: Environment Variables

### Create: `~/.kimi/.env`

```bash
# API Keys (replace with your actual keys)
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key
GITHUB_TOKEN=your_github_token
SUPABASE_ACCESS_TOKEN=your_supabase_token
VERCEL_TOKEN=your_vercel_token

# Configuration
CLAUDE_PACKAGE_MANAGER=npm
CLAUDE_CODE_DEBUG=0
CLAUDE_CODE_ANALYTICS=1

# MCP Server Flags
ECC_HOOK_PROFILE=standard
ECC_DISABLED_HOOKS=""

# Performance
NODE_OPTIONS=--max-old-space-size=8192
PYTHONPATH="${HOME}/.kimi/python-lib"

# Paths
KIMI_HOME="${USERPROFILE}/.kimi"
KIMI_SKILLS_DIR="${KIMI_HOME}/skills"
KIMI_AGENTS_DIR="${KIMI_HOME}/agents"
KIMI_LOGS_DIR="${KIMI_HOME}/logs"
```

---

## Phase 9: Verification & Testing

### Verify Installation

Run these commands in Kimi Code CLI:

```bash
# Check plugin installation
/plugin list everything-claude-code@everything-claude-code

# Check MCP servers
/mcp list

# Check available commands
/help

# Check skills
/skill:list

# Test web search
/search "latest TypeScript version"

# Test everything-claude-code
/plan "Test feature implementation"
```

### Test Commands to Try

```bash
# TDD workflow
/tdd

# Code review
/code-review

# Security scan
/security-scan

# Plan implementation
/plan "Add user authentication"

# Learn from session
/learn

# Check instinct status
/instinct-status
```

---

## Phase 10: Troubleshooting

### Common Issues & Fixes

#### Issue: "Duplicate hooks file detected"
**Fix**: Don't add `"hooks"` field to plugin.json. Claude Code v2.1+ auto-loads hooks.

#### Issue: Context window shrinking
**Fix**: Disable unused MCP servers:
```json
{
  "disabledMcpServers": ["supabase", "railway", "vercel"]
}
```
Keep under 10 MCPs enabled.

#### Issue: Web search not working
**Fix**: Check environment variables and MCP server status:
```bash
/mcp status web-search
```

#### Issue: Skills not loading
**Fix**: Verify skill directories in settings.json and restart Kimi Code CLI.

#### Issue: Plugin commands not found
**Fix**: Use namespaced form:
```bash
/everything-claude-code:plan "feature"
```

---

## Summary: What You Get

After complete setup:

| Capability | Before | After |
|------------|--------|-------|
| **Agents** | 2 built-in | **30+ specialized agents** |
| **Skills** | Basic | **116+ production skills** |
| **Commands** | 10 | **60+ slash commands** |
| **MCP Servers** | 0 | **10+ integrated services** |
| **Web Search** | Manual | **Auto-triggered** |
| **Context** | 200K limit | **Optimized + auto-compact** |
| **Memory** | Session-only | **Persistent across sessions** |
| **Hooks** | None | **Auto-workflows** |
| **Rules** | None | **Coding standards enforced** |

---

## Quick Start Commands

After installation, these commands unlock peak performance:

```bash
# Planning & Architecture
/plan "Feature description"           # AI-powered planning
/architect "System design"            # Architecture decisions

# Development
/tdd                                  # Test-driven development
/code-review                          # Quality review
/security-scan                        # Security audit
/build-fix                            # Fix build errors

# Testing
/e2e                                  # E2E test generation
/test-coverage                        # Coverage analysis
/verify                               # Verification loop

# Operations
/learn                                # Extract patterns
/instinct-status                      # View learned patterns
/evolve                               # Cluster into skills
/sessions                             # Manage sessions

# Multi-agent
/orchestrate                          # Coordinate agents
/multi-plan                           # Collaborative planning
/multi-execute                        # Parallel execution
```

---

**Document Version**: 1.0  
**Last Updated**: March 2026  
**Author**: VConfi Solutions

---

**END OF GUIDE**

*This configuration transforms Kimi Code CLI from a basic coding assistant to a production-grade AI engineering platform.*
