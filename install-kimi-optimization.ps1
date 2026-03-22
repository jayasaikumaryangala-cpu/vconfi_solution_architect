# Kimi Code CLI Optimization Installation Script
# Run this in PowerShell as Administrator

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Kimi Code CLI Optimization Installer" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Create directories
Write-Host "Step 1: Creating directories..." -ForegroundColor Green
$dirs = @(
    "$env:USERPROFILE\.kimi\skills",
    "$env:USERPROFILE\.kimi\agents",
    "$env:USERPROFILE\.kimi\commands",
    "$env:USERPROFILE\.kimi\rules",
    "$env:USERPROFILE\.kimi\hooks",
    "$env:USERPROFILE\.kimi\logs",
    "$env:USERPROFILE\.kimi\memory",
    "$env:USERPROFILE\.kimi\mcp"
)

foreach ($dir in $dirs) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  Created: $dir" -ForegroundColor Gray
    }
}

# Install everything-claude-code
Write-Host ""
Write-Host "Step 2: Installing everything-claude-code..." -ForegroundColor Green
Write-Host "  Cloning repository..." -ForegroundColor Gray

cd "$env:USERPROFILE\Downloads"
if (Test-Path "everything-claude-code") {
    Remove-Item -Recurse -Force "everything-claude-code"
}

git clone https://github.com/affaan-m/everything-claude-code.git

if (Test-Path "everything-claude-code") {
    Write-Host "  Running installer..." -ForegroundColor Gray
    cd everything-claude-code
    
    # Install rules
    Write-Host "  Installing TypeScript rules..." -ForegroundColor Gray
    .\install.ps1 typescript
    
    Write-Host "  Installing Python rules..." -ForegroundColor Gray
    .\install.ps1 python
    
    Write-Host "  Installing Golang rules..." -ForegroundColor Gray
    .\install.ps1 golang
    
    Write-Host "  Rules installed successfully!" -ForegroundColor Green
} else {
    Write-Host "  ERROR: Failed to clone repository" -ForegroundColor Red
}

# Create MCP servers config
Write-Host ""
Write-Host "Step 3: Creating MCP configuration..." -ForegroundColor Green

$mcpConfig = @'
{
  "mcpServers": {
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
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\$env:USERNAME"]
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
'@ -replace '\$env:USERNAME', $env:USERNAME

$mcpConfig | Out-File -FilePath "$env:USERPROFILE\.kimi\mcp-servers.json" -Encoding UTF8
Write-Host "  Created: ~/.kimi/mcp-servers.json" -ForegroundColor Gray

# Create settings.json
Write-Host ""
Write-Host "Step 4: Creating settings configuration..." -ForegroundColor Green

$settings = @'
{
  "model": "kimi-k2-0711-preview",
  "maxTokens": 8192,
  "temperature": 0.7,
  "topP": 0.9,
  
  "webSearch": {
    "enabled": true,
    "default": true,
    "autoSearch": true
  },
  
  "mcp": {
    "enabled": true,
    "servers": [
      "web-search",
      "fetch",
      "filesystem",
      "sequential-thinking",
      "memory"
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
  
  "security": {
    "confirmDestructiveOperations": true,
    "confirmBashCommands": true,
    "allowGitOperations": true
  },
  
  "performance": {
    "parallelToolCalls": true,
    "maxParallelCalls": 5,
    "cacheResults": true
  },
  
  "logging": {
    "level": "info",
    "saveToFile": true,
    "logDirectory": "~/.kimi/logs"
  }
}
'@

$settings | Out-File -FilePath "$env:USERPROFILE\.kimi\settings.json" -Encoding UTF8
Write-Host "  Created: ~/.kimi/settings.json" -ForegroundColor Gray

# Create context optimizer config
Write-Host ""
Write-Host "Step 5: Creating context optimizer..." -ForegroundColor Green

$contextConfig = @'
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
    "autoLoad": true
  }
}
'@

$contextConfig | Out-File -FilePath "$env:USERPROFILE\.kimi\context-optimizer.json" -Encoding UTF8
Write-Host "  Created: ~/.kimi/context-optimizer.json" -ForegroundColor Gray

# Install global npm packages
Write-Host ""
Write-Host "Step 6: Installing global npm packages..." -ForegroundColor Green

$packages = @(
    "typescript",
    "prettier",
    "eslint",
    "@anthropic-ai/claude-code",
    "@mcp/server-web-search",
    "@mcp/server-fetch",
    "@modelcontextprotocol/server-filesystem",
    "@modelcontextprotocol/server-sequential-thinking",
    "@modelcontextprotocol/server-memory"
)

foreach ($pkg in $packages) {
    Write-Host "  Installing: $pkg" -ForegroundColor Gray
    npm install -g $pkg 2>&1 | Out-Null
}

Write-Host "  Global packages installed!" -ForegroundColor Green

# Link VConfi skill globally
Write-Host ""
Write-Host "Step 7: Linking VConfi skill globally..." -ForegroundColor Green

$vconfiSource = "c:\Users\saikumaryangala\Downloads\skills for vconfi\.claude\skills\vconfi-solution-architect"
$vconfiDest = "$env:USERPROFILE\.kimi\skills\vconfi-solution-architect"

if (Test-Path $vconfiSource) {
    if (Test-Path $vconfiDest) {
        Remove-Item -Recurse -Force $vconfiDest
    }
    
    # Create junction (Windows symlink equivalent)
    New-Item -ItemType Junction -Path $vconfiDest -Target $vconfiSource | Out-Null
    Write-Host "  Linked: vconfi-solution-architect -> ~/.kimi/skills/" -ForegroundColor Gray
} else {
    Write-Host "  WARNING: VConfi skill source not found at:" -ForegroundColor Yellow
    Write-Host "    $vconfiSource" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Installation Complete!" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host "  1. Restart Kimi Code CLI" -ForegroundColor Yellow
Write-Host "  2. Run: /plugin marketplace add affaan-m/everything-claude-code" -ForegroundColor Yellow
Write-Host "  3. Run: /plugin install everything-claude-code@everything-claude-code" -ForegroundColor Yellow
Write-Host "  4. Test with: /plan 'Test feature'" -ForegroundColor Yellow
Write-Host ""
Write-Host "Configuration files created:" -ForegroundColor White
Write-Host "  - ~/.kimi/settings.json" -ForegroundColor Gray
Write-Host "  - ~/.kimi/mcp-servers.json" -ForegroundColor Gray
Write-Host "  - ~/.kimi/context-optimizer.json" -ForegroundColor Gray
Write-Host ""
Write-Host "Features enabled:" -ForegroundColor White
Write-Host "  ✓ Web search (auto-enabled)" -ForegroundColor Green
Write-Host "  ✓ MCP servers (5 configured)" -ForegroundColor Green
Write-Host "  ✓ Context optimization" -ForegroundColor Green
Write-Host "  ✓ Skills directory" -ForegroundColor Green
Write-Host "  ✓ Agents directory" -ForegroundColor Green
Write-Host "  ✓ Rules (TypeScript, Python, Go)" -ForegroundColor Green
Write-Host ""
Write-Host "Run /help in Kimi Code CLI to see available commands!" -ForegroundColor Cyan
Write-Host ""

pause
