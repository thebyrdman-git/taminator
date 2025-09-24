# pai-supportshell

SupportShell remote analysis with OADP handling and AI troubleshooting.

## Location
`~/.local/bin/pai-supportshell`

## Description
Comprehensive tool for executing secure analysis on SupportShell environment. Handles OADP approval requirements, file naming with prepended counts, and provides AI-assisted troubleshooting for failed commands.

## Key Features
- **OADP Approval Handling**: Detects and alerts for approval requirements
- **File Naming Awareness**: Handles prepended counts (0010-must-gather.tar.gz)
- **AI Troubleshooting**: Analyzes failures and suggests fixes
- **Multiple Analysis Tools**: yank, insights, etc-ocp-diag.py, omc
- **Security Focused**: No data exfiltration, summaries only

## Essential Workflow
```bash
# 1. Pull case attachments (may require OADP approval)
pai-supportshell pull 04056105

# 2. Understand file structure and naming
pai-supportshell tree 04056105

# 3. Run comprehensive analysis
pai-supportshell analyze-all 04056105
```

## Commands

### Case Management
- `pai-supportshell pull <case>` - Pull attachments with yank -y (watch for OADP approval)
- `pai-supportshell tree <case>` - Show directory structure with tree -L 3
- `pai-supportshell files <case>` - List available files

### Analysis Tools
- `pai-supportshell analyze-all <case>` - Run all analyses with auto-troubleshoot
- `pai-supportshell insights <case>` - Red Hat Insights analysis
- `pai-supportshell etcd <case>` - etc-ocp-diag.py analysis on must-gather
- `pai-supportshell omc <case>` - OMC (OpenShift Must-gather Collector) analysis
- `pai-supportshell logs <case> [pattern]` - Log analysis with pattern matching

### Troubleshooting
- `pai-supportshell troubleshoot <case> <cmd> <error>` - AI-assisted problem solving
- `pai-supportshell check` - Test connectivity and available tools
- `pai-supportshell run <command>` - Execute arbitrary SupportShell command

## OADP Approval Process
When running `pai-supportshell pull` for the first time on a case:

1. **Tool alerts**: "🚨 OADP APPROVAL REQUIRED 🚨"
2. **Output shown**: Complete pull result with any approval links
3. **User action**: Complete approval process via provided links
4. **Retry**: Run pull command again after approval

## File Naming Conventions
SupportShell extracts attachments with prepended submission counts:
- Original: `must-gather.tar.gz`
- Extracted: `0010-must-gather.tar.gz` (10th attachment)

The tool automatically handles both naming conventions.

## AI Troubleshooting
When commands fail, the tool:
1. **Gathers context**: Current directory, case structure, available tools
2. **AI analysis**: Uses fabric patterns to diagnose the failure
3. **Suggests fixes**: Corrected commands and alternative approaches
4. **Documents issues**: Saves troubleshooting analysis for future reference

## Security Features
- **No data download**: Only analysis summaries returned
- **Audit logging**: All operations logged via pai-audit
- **Fabric integration**: AI analysis uses secure model routing
- **Output location**: ~/.claude/context/create/outputs/supportshell/

## Integration Examples
```bash
# Complete case analysis workflow
pai-supportshell pull 04056105
pai-supportshell tree 04056105
pai-supportshell analyze-all 04056105

# Add results to knowledge base
pai-search add cases "Case 04056105 SupportShell Analysis" "$(cat latest_analysis.md)"

# Include in daily briefing
pai-my-plate-v2  # Automatically includes recent SupportShell analyses
```
