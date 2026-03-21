# Output Format — Multi-Part Document Generation

This document covers **Mode A (Claude Code)** — generating 6 markdown parts merged into `.docx` via Python. For **Mode B (Claude Browser)**, use the HTML template at `templates/implementation-plan.html` to generate a single HTML Artifact with all parts inline.

To avoid token limits and ensure NO details are compressed or lost, generate the implementation plan in **6 separate parts**, then merge them into one final `.docx`.

## Part Structure

| Part | File Name | Contents |
|------|-----------|----------|
| Part 1 | `Part1_Executive_Architecture_ISO.md` | Document Control, Executive Summary, Architecture Overview with diagrams (Mermaid/ASCII), VLAN design table, IP scheme table, ISO 27001 compliance mapping with full control table |
| Part 2 | `Part2_Network_Wireless_Server.md` | Firewall design (model, zones, policies, HA config), Switch design (model, ports, PoE, stacking), Cabling schedule, Redundancy scenario details, Wireless design (AP placement, SSID config, RADIUS, heat map recommendation), Server specs (CPU, RAM, storage, RAID, OS for each server), Virtualization plan |
| Part 3 | `Part3_DR_Monitoring_Power.md` | Backup topology (3-2-1 with diagram), RPO/RTO targets table, DR site plan (location, tier, replication, failover runbook), Zabbix setup (VM sizing, monitored devices, thresholds, dashboard), Splunk SIEM (license, ingestion, log sources, correlation rules), Log retention policy table, UPS power load calculation table, UPS recommendation with comparison, ATS config, SNMP monitoring setup |
| Part 4 | `Part4_BOM_Assets_Timeline.md` | Complete BOM table in INR (every device, license, cable, service), Category subtotals, GST calculation, Grand total, Year 1 vs Year 2-5 breakdown, Asset lifecycle table (warranty, EOL, AMC for every device), 3-year and 5-year TCO table, Phase-wise implementation timeline, Acceptance criteria checklist |
| Part 5 | `Part5_Security_Stress_Test.md` | Attack surface analysis, External attack scenarios and findings, Internal attack scenarios and findings, Wireless attack scenarios and findings, Backup/DR attack scenarios and findings, Social engineering assessment, Full vulnerability report table (every finding with severity, gap, fix), Hardening recommendations with config snippets, Updated BOM items (if any), Priority matrix (pre-go-live vs post-deployment) |
| Part 6 | `Part6_SOPs.md` | SOP-NET-001: FortiGate Daily Operations, SOP-NET-002: Switch Management, SOP-NET-003: FortiAP Wireless Management, SOP-MON-001: Zabbix Monitoring & Alert Response, SOP-SRV-001: Server Patching & Maintenance, SOP-BKP-001: Backup & Restore Procedures, SOP-DR-001: DR Failover & Failback, SOP-SEC-001: Splunk SIEM Review, SOP-SEC-002: Incident Response Workflow, SOP-SEC-003: ISO 27001 Audit Prep Checklist, SOP-USR-001: Wi-Fi & VPN Access Guide. Each SOP must have: purpose, scope, step-by-step procedures, escalation matrix, reference links |

## Diagram Requirements — MANDATORY in Every Part

**NEVER skip diagrams.** Every part must include relevant diagrams:

- **Part 1:** Full network topology diagram (Mermaid), VLAN segmentation diagram, firewall zone diagram
- **Part 2:** Switch stacking/interconnect diagram, wireless AP placement diagram (floor-by-floor), server rack layout diagram
- **Part 3:** Backup flow diagram (3-2-1 visual), DR replication diagram (primary ↔ DR site), monitoring architecture diagram (what monitors what), UPS power distribution diagram (mains → ATS → UPS → PDU → devices)
- **Part 4:** Implementation timeline Gantt chart (Mermaid), cost breakdown pie chart (text-based)
- **Part 5:** Attack surface diagram, attack path diagrams for critical findings
- **Part 6:** Escalation flow diagrams, incident response flowchart, backup/restore decision tree

Use **Mermaid syntax** for diagrams. Example:
```
graph TD
    ISP1[ISP 1] --> FW1[FortiGate Primary]
    ISP2[ISP 2] --> FW1
    FW1 --> |HA| FW2[FortiGate Secondary]
    FW1 --> CS1[Core Switch 1]
    FW2 --> CS2[Core Switch 2]
    CS1 --> |LACP| CS2
    CS1 --> AS1[Access Switch Floor 1]
    CS2 --> AS2[Access Switch Floor 2]
```

If Mermaid is not renderable in the output, use ASCII box diagrams as fallback.

## Generation Process

1. Generate each part as a separate `.md` file in the user's project directory
2. After ALL 6 parts are generated, merge them into one final document using the generate_docx.py script in this skill's `scripts/` directory:
   ```bash
   python3 scripts/generate_docx.py merge --parts Part1_*.md Part2_*.md Part3_*.md Part4_*.md Part5_*.md Part6_*.md --output "VConfi_Implementation_Plan_<ClientName>_<Date>.docx" --client "<ClientName>" --project "<ProjectName>"
   ```
3. The merged `.docx` will have:
   - Professional cover page with VConfi branding
   - Table of Contents
   - All 6 parts in order with proper section numbering
   - All diagrams rendered
   - Styled tables, headings, and formatting
   - Page numbers and confidential footer
4. Confirm the final `.docx` path to the user

## Zero Compression Rule

**NEVER compress, summarize, abbreviate, or skip ANY of the following:**
- Every row in every table must be fully populated — no "[Add more as applicable]" placeholders
- Every device in the BOM must have actual model numbers and pricing (use WebSearch for current prices)
- Every ISO control must have a specific implementation mapping — not generic text
- Every SOP must have complete step-by-step procedures — not just topic headers
- Every stress test attack must have a specific finding — not just "check this"
- Every diagram must be complete — not "see appendix" or "to be added"
- If a section needs more space, use MORE space — never truncate to save tokens

If you are running low on output tokens while generating a part, STOP and tell the user: *"I need to continue this part in the next message to ensure no details are lost."* Then continue in the next response. NEVER silently cut content.

**Proactive splitting:** If a part will clearly exceed ~4,000 words (e.g., 11 SOPs, 100+ BOM rows), split it BEFORE you start writing — not after you run out of space. It is always better to have more smaller artifacts than to risk truncation.

**Prerequisites:** `python-docx` must be installed (`pip install python-docx`). Before running the script, verify it is installed by running `python3 -c "import docx"`. If it fails, run `pip install python-docx` first.

If the user asks for revisions, regenerate only the affected part(s) and re-merge.

## Mermaid Diagrams in DOCX

Note: The DOCX generator renders Mermaid diagrams as formatted code blocks. For visual rendering, the user should:
1. Open the `.docx` and copy Mermaid code blocks
2. Render them using [mermaid.live](https://mermaid.live) or a local Mermaid CLI
3. Paste the rendered images back into the document
4. Alternatively, use a Mermaid-to-image tool before merging
