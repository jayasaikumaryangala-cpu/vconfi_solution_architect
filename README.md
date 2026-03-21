# VConfi Solution Architect

An AI-powered IT infrastructure solution design skill for [Kimi Code CLI](https://github.com/MoonshotAI/kimi-cli), Claude Code, and compatible AI coding agents.

## Overview

**VConfi Solution Architect** is a specialized skill that helps IT solutions architects design secure, optimized, and scalable infrastructure solutions that pass security audits and follow industry best practices.

### Key Features

- **Comprehensive Solution Design**: Network architecture, server deployments, firewall configurations
- **ISO 27001 Compliance**: Built-in compliance mapping and documentation
- **Security-First Approach**: Audit-ready designs from day one
- **Vendor-Specific Guidance**: Fortinet, HPE, Cisco, and more
- **Complete Documentation**: Auto-generates implementation plans with BOMs, diagrams, and SOPs
- **Memory System**: Persistent knowledge across client engagements
- **Priced in INR**: All cost estimates in Indian Rupees

## Installation

### Prerequisites

- [Kimi Code CLI](https://github.com/MoonshotAI/kimi-cli) OR [Claude Code](https://code.claude.com/) OR compatible AI agent
- Python 3.8+ (for DOCX generation)
- `python-docx` library: `pip install python-docx`

### Method 1: Quick Install (Terminal)

#### For Kimi Code CLI / Claude Code

```bash
# Clone to user-level skills directory (recommended)
git clone https://github.com/jayasaikumaryangala-cpu/vconfi_solution_architect.git ~/.config/agents/skills/vconfi-solution-architect

# Or clone to .claude/skills/ in your project directory
git clone https://github.com/jayasaikumaryangala-cpu/vconfi_solution_architect.git .claude/skills/vconfi-solution-architect
```

#### Alternative Paths (Kimi Code CLI will auto-detect)

```bash
# Option 1: ~/.config/agents/skills/ (RECOMMENDED - works across all projects)
git clone https://github.com/jayasaikumaryangala-cpu/vconfi_solution_architect.git ~/.config/agents/skills/vconfi-solution-architect

# Option 2: ~/.agents/skills/
git clone https://github.com/jayasaikumaryangala-cpu/vconfi_solution_architect.git ~/.agents/skills/vconfi-solution-architect

# Option 3: ~/.kimi/skills/
git clone https://github.com/jayasaikumaryangala-cpu/vconfi_solution_architect.git ~/.kimi/skills/vconfi-solution-architect

# Option 4: ~/.claude/skills/
git clone https://github.com/jayasaikumaryangala-cpu/vconfi_solution_architect.git ~/.claude/skills/vconfi-solution-architect
```

### Method 2: Project-Specific Install

```bash
# Navigate to your project directory
cd your-project

# Create .claude/skills directory if it doesn't exist
mkdir -p .claude/skills

# Clone the skill
git clone https://github.com/jayasaikumaryangala-cpu/vconfi_solution_architect.git .claude/skills/vconfi-solution-architect
```

### Method 3: Download ZIP

1. Download ZIP from: `https://github.com/jayasaikumaryangala-cpu/vconfi_solution_architect/archive/refs/heads/main.zip`
2. Extract to `~/.config/agents/skills/vconfi-solution-architect/` or `.claude/skills/vconfi-solution-architect/`

## Usage

### Invocation Methods

#### Method 1: Auto-Trigger (Recommended)

The skill auto-detects when you mention relevant keywords. Just type:

```
I need to design an IT infrastructure solution for Acme Corp
```

Or:

```
Create a network implementation plan with Fortinet firewall and ISO 27001 compliance
```

**Trigger keywords**: VConfi, implementation plan, network design, IT infrastructure, Fortinet, HPE, Cisco, ISO 27001

#### Method 2: Explicit Skill Invocation

**Kimi Code CLI:**
```
/skill:vconfi-solution-architect "Client Name"
```

**Claude Code:**
```
/vconfi-solution-architect "Client Name"
```

#### Method 3: Direct Request

```
Use the vconfi-solution-architect skill to help me design a secure network
```

### Workflow

Once invoked, the skill will guide you through:

1. **Client Discovery** (Group 0): Company info, industry, goals, non-negotiables
2. **Requirements Gathering** (Groups 1-7): Scope, network, servers, wireless, security, budget, timeline
3. **Solution Design**: Architecture, ISO mapping, vendor selection
4. **Document Generation**: 6-part implementation plan with BOMs, diagrams, SOPs
5. **Security Stress Test**: Red-team analysis and hardening recommendations

### Output Formats

| Platform | Output Format | Command |
|----------|---------------|---------|
| Kimi Code CLI | `.docx` (Word document) | Auto-generated via `scripts/generate_docx.py` |
| Claude.ai Browser | HTML Artifacts | Copy-paste into project |

## Directory Structure

```
vconfi-solution-architect/
├── SKILL.md                      # Main skill file (required)
├── README.md                     # This file
├── references/                   # Reference documentation
│   ├── iso-27001-controls.md     # ISO 27001 control mappings
│   ├── vendor-reference.md       # Vendor model selection guides
│   ├── security-stress-test.md   # Security testing methodology
│   └── output-format.md          # Document generation guide
├── templates/                    # Output templates
│   ├── implementation-plan.html  # HTML template for browser
│   └── plan-template.md          # Markdown template
├── scripts/                      # Utility scripts
│   └── generate_docx.py          # DOCX generator for Kimi Code CLI
├── memory/                       # Persistent memory (auto-created)
│   ├── clients/                  # Client profiles
│   ├── projects/                 # Project records
│   ├── pricing/                  # Pricing data
│   ├── lessons/                  # Lessons learned
│   └── memory_index.md           # Memory index
└── browser-setup/                # Browser setup guide
    ├── SETUP-GUIDE.md
    └── project-instructions.md
```

## Platform-Specific Setup

### Kimi Code CLI (VS Code Extension)

1. Install the skill using Method 1 or 2 above
2. Install Python dependency: `pip install python-docx`
3. Restart VS Code if needed
4. Invoke with keywords or `/skill:vconfi-solution-architect`

### Claude.ai Browser

1. Create a new Project at [claude.ai](https://claude.ai)
2. Copy content from `SKILL.md` into **Project Instructions**
3. Upload reference files as **Project Knowledge**:
   - `references/iso-27001-controls.md`
   - `references/vendor-reference.md`
   - `references/security-stress-test.md`
   - `references/output-format.md`
   - `templates/implementation-plan.html`
4. Enable **Web Search** in project settings
5. Start a conversation to begin

See [browser-setup/SETUP-GUIDE.md](browser-setup/SETUP-GUIDE.md) for detailed browser setup.

## Skill Features

### Core Capabilities

- **Network Design**: VLAN segmentation, firewall zones, redundancy planning
- **Vendor Recommendations**: Fortinet (firewall), HPE/Cisco (switches), FortiAP (wireless)
- **Server Infrastructure**: HPE ProLiant, Synology NAS, virtualization
- **Security & Compliance**: ISO 27001 mapping, stress testing, hardening
- **Disaster Recovery**: 3-2-1 backup rule, DR site planning
- **Monitoring**: Zabbix (network monitoring), Splunk (SIEM)
- **Power & UPS**: Load calculations, ATS configuration
- **Documentation**: Complete BOM, SOPs, timeline, TCO analysis

### Memory System

The skill maintains persistent knowledge across engagements:

- **Client Profiles**: Preferences, non-negotiables, vendor history
- **Project Records**: Past designs, decisions, outcomes
- **Pricing Data**: Recent vendor pricing for accurate BOMs
- **Lessons Learned**: Improvements from previous projects

### Document Generation

**6-Part Implementation Plan:**

1. **Part 1**: Executive Summary, Architecture & ISO Compliance
2. **Part 2**: Network, Wireless & Server Design
3. **Part 3**: DR/Backup, Monitoring/SIEM & Power/UPS
4. **Part 4**: BOM, Asset Lifecycle & Timeline
5. **Part 5**: Security Stress Test Results
6. **Part 6**: Standard Operating Procedures (SOPs)

**Key Features:**
- All pricing in INR
- Mermaid diagrams
- Complete BOM with GST calculations
- TCO analysis (3-year, 5-year)
- Phase-wise implementation timeline
- 11 comprehensive SOPs

## Troubleshooting

### Skill Not Detected

**Kimi Code CLI:**
1. Verify skill is in correct location: `ls ~/.config/agents/skills/`
2. Restart VS Code
3. Check for skill conflicts (duplicate names)

**Claude Code:**
1. Ensure `.claude/skills/` is in project root
2. Check SKILL.md has valid YAML frontmatter
3. Restart Claude Code

### DOCX Generation Fails

```bash
# Install required dependency
pip install python-docx

# Verify installation
python -c "import docx; print('OK')"
```

### Reference Files Not Found

Ensure relative paths in SKILL.md match your directory structure. All references should be one level deep from SKILL.md.

## Requirements

- Kimi Code CLI 1.23.0+ OR Claude Code
- Python 3.8+ (for DOCX generation)
- python-docx library
- Internet access (for web search and pricing research)

## License

[Specify your license here]

## Contributing

Contributions welcome! Please ensure:
- SKILL.md stays under 500 lines
- Reference files are properly linked
- Examples are concrete, not abstract
- Test with real usage before submitting

## Author

**VConfi Solutions**  
IT Infrastructure Solutions

## Support

For issues or questions:
- GitHub Issues: [github.com/jayasaikumaryangala-cpu/vconfi_solution_architect/issues](https://github.com/jayasaikumaryangala-cpu/vconfi_solution_architect/issues)
- Email: [your-email@vconfi.com]

---

**Note**: This skill generates infrastructure designs for educational and professional use. Always validate designs with certified professionals before production deployment.
