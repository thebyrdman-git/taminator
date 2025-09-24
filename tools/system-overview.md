# PAI System Tools Overview

This directory contains documentation for all tools available in the Personal AI Infrastructure (PAI) system.

## Tool Categories

### PAI Core Tools
Tools created specifically for the PAI system:
- **[pai-my-plate](pai-my-plate.md)**: Daily TAM briefing generator
- **[pai-case-initial-screen](pai-case-initial-screen.md)**: Case screening document generator
- **[pai-case-initial-screen-v2](pai-case-initial-screen-v2.md)**: Enhanced case screening with AI analysis
- **[pai-services](pai-services.md)**: PAI infrastructure service manager
- **[pai-local-tool-inventory](pai-local-tool-inventory.md)**: Local tool and repository scanner
- **[pai-workspace](pai-workspace.md)**: Multi-specialty TAM workspace integration

### AI-Powered Analysis Tools
Tools for AI-augmented analysis and content processing:
- **[fabric](fabric.md)**: AI pattern-based analysis and content generation

### Red Hat Internal Tools
Official Red Hat tools for TAM work:
- **[rhcase](rhcase.md)**: Case management and lookups
- **[lefty2](lefty2.md)**: Case reporting and analytics
- **[supportshell-tool-scan](supportshell-tool-scan.md)**: SupportShell capability scanner

### SupportShell Environment
Remote analysis environment tools:
- **[Overview](supportshell/overview.md)**: SupportShell access and capabilities
- **[yank-ng](supportshell/yank-ng.md)**: Advanced log extraction and analysis

## Quick Reference

### Daily Workflow
```bash
# List all active cases across specialties
pai-workspace list

# Generate daily briefing
pai-my-plate

# Screen a new case with AI analysis
pai-workspace case 04056105 analyze

# Check cases for an account
rhcase list cibc
```

### Service Management
```bash
# Start PAI services
pai-services start

# Check service status
pai-services status

# View service logs
pai-services logs
```

### Remote Analysis
```bash
# Connect to SupportShell
ssh gvaughn@supportshell-1.sush-001.prod.us-west-2.aws.redhat.com

# Scan available tools
supportshell-tool-scan
```

### AI-Augmented Analysis
```bash
# Analyze case with fabric patterns
rhcase analyze 12345678 | fabric -p analyze_incident

# Extract insights from KCS articles
rhcase kcs search "performance issue" | fabric -p extract_wisdom

# Summarize long logs
yank-ng --case 12345 --pattern "error" | fabric -p analyze_logs
```

### Workspace Management
```bash
# Create new case structure
pai-workspace create bny 04123456

# Create case in specific specialty
pai-workspace create tam-ai cibc 04567890

# Find and analyze any case across specialties
pai-workspace case 04056105 info
pai-workspace case 04056105 analyze

# Sync PAI outputs to case directory
pai-workspace sync 04056105
```

## Tool Locations
- PAI tools: `~/.local/bin/pai-*`
- System tools: Various locations in PATH
- Config files: `~/.claude/pai/config/`
- Service data: `~/.claude/pai/services/*/data`

## Environment Setup
```fish
# Export API keys for model access
source ~/.claude/pai/config/export-model-keys.fish
```

## Integration Points
All tools are designed to work together:
1. **rhcase** feeds data to **pai-my-plate**
2. **pai-case-initial-screen** uses templates from TAM manual
3. **pai-services** provides infrastructure for all agents
4. **supportshell** tools analyze data that can't leave customer environment
