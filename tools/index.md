# PAI Context Tools Index

## Documentation Files

### Core Documentation
- **[CLAUDE.md](CLAUDE.md)** - Main context system overview and architecture
- **[pai-tools.md](pai-tools.md)** - Complete PAI tools documentation
- **[fabric-patterns.md](fabric-patterns.md)** - Fabric patterns for TAM workflows

### Tool Categories

#### PAI Core Tools
- pai-workspace - Multi-specialty TAM workspace management
- pai-case-initial-screen-v2 - Enhanced case screening with AI
- pai-fabric - Fabric + LiteLLM integration wrapper  
- pai-my-plate-v2 - Comprehensive daily briefing with case numbers
- pai-case-processor - Automated case lifecycle and analysis
- pai-search - Markdown knowledge base search and management
- pai-supportshell - SupportShell remote analysis with OADP handling
- pai-audit - Security, audit logging, and secrets management
- pai-email-processor - Email intelligence and contact research
- pai-hydra-processor - Hydra notification processing
- pai-email-sync - Automated email synchronization
- pai-calendar - Google Calendar integration and meeting prep
- pai-update-pattern-docs - Pattern documentation updater

#### Red Hat Internal Tools
- rhcase - Case management, KCS, and JIRA operations
- lefty2 - Case reporting and analytics

#### AI-Powered Analysis
- fabric - Pattern-based AI analysis via LiteLLM proxy
- Custom TAM patterns for specialized workflows

#### SupportShell Tools
- sushe - Secure SupportShell access
- supportshell-tool-scan - Remote tool inventory
- SupportShell environment tools (yank-ng, insights-client, etc.)

## Quick Reference

### Daily Workflow Commands
```bash
pai-my-plate-v2                       # Comprehensive daily briefing with case numbers
pai-calendar summary                  # Daily calendar with meeting prep status
pai-workspace list                    # List all cases by specialty
pai-case-processor all                # Ensure all cases analyzed
pai-email-sync pull                   # Manual email sync
pai-workspace case 04056105 analyze   # Analyze specific case
```

### Case Analysis Commands
```bash
pai-workspace case 04056105 info      # Get case details
echo "issue description" | fabric -p tam_case_screen -m gpt-4o  # Screen case
rhcase kcs search "terms" | fabric -p extract_wisdom -m gpt-4o  # Research
```

### Data Security Commands
```bash
cat sensitive_data.txt | fabric -p redact_tam_data -m gpt-4o  # Redact before sharing
pai-fabric redact < input.txt > redacted_output.txt          # Simplified redaction
```

## Maintenance Commands
```bash
pai-update-pattern-docs              # Update pattern documentation
pai-local-tool-inventory            # Refresh tool inventory
pai-fabric check                    # Verify litellm proxy status
```

## Integration Points
- **TAM Workspace**: ~/Documents/rh/projects/{tam-ocp,tam-ai,tam-sec}
- **PAI Context**: ~/.claude/context/ (Miessler-aligned structure)
- **Fabric Patterns**: ~/.config/fabric/custom_patterns/
- **LiteLLM Proxy**: http://localhost:4000

## Status Dashboard
- ✅ Workspace integration across all TAM specialties
- ✅ Fabric + LiteLLM connectivity working
- ✅ Custom redaction pattern functional
- ✅ Case analysis patterns available
- ✅ Email ingestion and Hydra processing automated
- ✅ SupportShell remote analysis with OADP handling
- ✅ Calendar integration and meeting preparation
- ✅ Security and audit system operational
- ✅ Automated case lifecycle management
- ⚠️ Internal Red Hat Mistral models need debugging (Granite working)

## Update Instructions
This documentation is automatically maintained. After adding new tools or patterns:

1. **Add new patterns**: Create in ~/.config/fabric/custom_patterns/
2. **Update documentation**: Run `pai-update-pattern-docs`
3. **Test functionality**: Use `pai-update-pattern-docs test <pattern>`
4. **Commit changes**: Document in version control if needed
