# PAI Tools Documentation

## Overview
Complete documentation of all PAI tools, their usage, and integration points.

## Core PAI Tools
Located in `~/.local/bin/pai-*`

### pai-workspace
**Purpose**: Multi-specialty TAM workspace management
**Location**: ~/.local/bin/pai-workspace
**Integration**: Links PAI with existing TAM directory structure

**Commands**:
- `pai-workspace list` - Show all accounts by specialty with case counts
- `pai-workspace case <number> info` - Find case across specialties  
- `pai-workspace case <number> open` - Navigate to case directory
- `pai-workspace case <number> analyze` - Run AI analysis
- `pai-workspace create <account> <case>` - Create new case structure
- `pai-workspace create <specialty> <account> <case>` - Create in specific specialty
- `pai-workspace link <account>` - Create symbolic links
- `pai-workspace sync <case>` - Sync PAI outputs to case directory

**TAM Specialties**:
- **tam-ocp**: OpenShift Container Platform TAM
- **tam-ai**: Red Hat AI Portfolio TAM
- **tam-sec**: Security TAM (all products)

### pai-case-initial-screen-v2
**Purpose**: Enhanced case screening with AI analysis
**Location**: ~/.local/bin/pai-case-initial-screen-v2
**Integration**: Auto-detects cases across all TAM specialties

**Usage**:
- `pai-case-initial-screen-v2` - Template mode
- `pai-case-initial-screen-v2 -a -c 04056105` - AI analysis mode
- `pai-case-initial-screen-v2 -a -c 04056105 -v` - Verbose mode

**Features**:
- Auto-detects case location across tam-ocp/tam-ai/tam-sec
- Uses Granite 3.2 for AI analysis (when working)
- Follows workflow.md methodology
- Outputs to both PAI and case directories

### pai-fabric
**Purpose**: Fabric + LiteLLM integration wrapper
**Location**: ~/.local/bin/pai-fabric
**Integration**: Simplifies fabric pattern usage with model routing

**Commands**:
- `pai-fabric redact` - Redact sensitive data
- `pai-fabric analyze` - Case analysis
- `pai-fabric research` - Online research
- `pai-fabric brief` - Generate summaries
- `pai-fabric logs` - Log analysis
- `pai-fabric models` - List available models
- `pai-fabric patterns` - List available patterns
- `pai-fabric check` - Check litellm proxy status

### pai-my-plate
**Purpose**: Daily TAM briefing generator
**Location**: ~/.local/bin/pai-my-plate
**Integration**: Creates structured daily briefings

**Usage**: `pai-my-plate`
**Output**: ~/.claude/context/create/outputs/briefs/daily/YYYY-MM-DD.md

### pai-update-pattern-docs
**Purpose**: Automatic pattern documentation generator
**Location**: ~/.local/bin/pai-update-pattern-docs
**Integration**: Scans and documents all fabric patterns

**Usage**:
- `pai-update-pattern-docs` - Update documentation
- `pai-update-pattern-docs test <pattern>` - Test specific pattern

### pai-search
**Purpose**: Markdown knowledge base search and management
**Location**: ~/.local/bin/pai-search
**Integration**: Git-versioned knowledge base with fabric-enhanced search

**Commands**:
- `pai-search search <query>` - Full text search
- `pai-search search <query> smart` - AI-enhanced search with fabric
- `pai-search search <query> tags` - Search by YAML tags
- `pai-search search <query> files` - Search by filename
- `pai-search add <category> <title> <content>` - Add knowledge entry
- `pai-search update <filepath> <content>` - Update existing entry
- `pai-search list [category]` - List entries
- `pai-search stats` - Show knowledge base statistics

### pai-supportshell
**Purpose**: SupportShell remote analysis with OADP handling
**Location**: ~/.local/bin/pai-supportshell
**Integration**: Remote analysis without data exfiltration, AI troubleshooting

**Commands**:
- `pai-supportshell pull <case>` - Pull case attachments with yank -y
- `pai-supportshell tree <case>` - Show case structure with tree -L 3
- `pai-supportshell analyze-all <case>` - Comprehensive analysis with auto-troubleshoot
- `pai-supportshell insights <case>` - Red Hat Insights analysis
- `pai-supportshell etcd <case>` - etc-ocp-diag.py analysis
- `pai-supportshell omc <case>` - OMC analysis
- `pai-supportshell logs <case>` - Log analysis with patterns
- `pai-supportshell troubleshoot <case> <cmd> <error>` - AI-assisted troubleshooting

### pai-audit
**Purpose**: Security, audit logging, and secrets management
**Location**: ~/.local/bin/pai-audit
**Integration**: Comprehensive security layer for all PAI operations

**Commands**:
- `pai-audit log <type> <details>` - Manual audit logging
- `pai-audit show-log [filter] [lines]` - View audit logs
- `pai-audit secret {set|get|list|delete} <name>` - Encrypted secrets management
- `pai-audit fabric <pattern> <model> <data>` - Secure fabric calls with auto-redaction
- `pai-audit status` - Security status and metrics
- `pai-audit cleanup [days]` - Data retention cleanup

### pai-case-processor
**Purpose**: Automated case lifecycle and comprehensive analysis
**Location**: ~/.local/bin/pai-case-processor
**Integration**: Implements workflow.md methodology across all accounts

**Commands**:
- `pai-case-processor all` - Process all accounts across specialties
- `pai-case-processor account <specialty> <account>` - Process specific account
- `pai-case-processor case <specialty> <account> <case>` - Analyze specific case
- `pai-case-processor report` - Generate daily case analysis report

### pai-email-processor
**Purpose**: Email intelligence and contact research
**Location**: ~/.local/bin/pai-email-processor
**Integration**: TAM-focused email analysis with contact dossiers

**Commands**:
- `pai-email-processor process [days] [max]` - Process recent emails
- `pai-email-processor issues [days]` - Identify potential issues
- `pai-email-processor contact <email> [name]` - Research contact dossier
- `pai-email-processor summary [days]` - Email summary for briefings

### pai-hydra-processor
**Purpose**: Hydra notification processing and case extraction
**Location**: ~/.local/bin/pai-hydra-processor
**Integration**: Converts Hydra emails to structured markdown with case metadata

**Commands**:
- `pai-hydra-processor` - Process recent Hydra notifications
- `pai-hydra-processor --days <N>` - Process N days of notifications
- `pai-hydra-processor --list` - List processed notifications

### pai-email-sync
**Purpose**: Automated email synchronization and processing
**Location**: ~/.local/bin/pai-email-sync
**Integration**: Systemd timer-based automation every 15 minutes

**Commands**:
- `pai-email-sync pull` - Manual email sync
- `pai-email-sync setup [interval]` - Setup automation (default: 15min)
- `pai-email-sync status` - Check automation status
- `pai-email-sync disable` - Disable automation

### pai-calendar
**Purpose**: Google Calendar integration and meeting preparation
**Location**: ~/.local/bin/pai-calendar
**Integration**: Meeting prep with attendee research and TAM context

**Commands**:
- `pai-calendar auth` - Setup Google Calendar OAuth
- `pai-calendar today [date]` - Show meetings for date
- `pai-calendar summary [date]` - Daily calendar summary with prep status
- `pai-calendar prep <meeting_title>` - Generate meeting preparation
- `pai-calendar agenda [days]` - Show upcoming agenda

### pai-local-tool-inventory
**Purpose**: Inventory all available tools and repositories
**Location**: ~/.local/bin/pai-local-tool-inventory

**Usage**: `pai-local-tool-inventory`
**Output**: Lists tools in ~/.local/bin and repos in coding directories

## Red Hat Internal Tools

### rhcase
**Purpose**: Case management, KCS, and JIRA operations
**Location**: ~/.local/bin/rhcase
**Integration**: Primary data source for PAI workflows

**Key Commands**:
- `rhcase analyze <case>` - Analyze specific case
- `rhcase kcs search "<terms>"` - Search knowledge base
- `rhcase kcs fetch <kcs_id>` - Fetch KCS article
- `rhcase jira search "<terms>"` - Search JIRA issues
- `rhcase jira fetch <issue_id>` - Fetch JIRA issue
- `rhcase list <account>` - List cases for account

### lefty2
**Purpose**: Case reporting and analytics
**Location**: System PATH
**Integration**: Provides reporting capabilities for TAM metrics

## SupportShell Tools

### sushe / supportshell-tool-scan
**Purpose**: Secure access to SupportShell environment
**Location**: ~/.local/bin/supportshell-tool-scan
**Integration**: Remote analysis without data exfiltration

**Usage**:
- `sushe` - Connect to SupportShell
- `supportshell-tool-scan` - List available tools

### SupportShell Environment Tools
**Access**: Via sushe SSH connection
- **yank-ng**: Advanced log extraction
- **insights-client**: Red Hat Insights analysis
- **sosreport**: System diagnostic collection
- **oc**: OpenShift CLI
- **must-gather-explorer**: OpenShift diagnostics

## Fabric Integration

### Model Access
**Via LiteLLM Proxy**: http://localhost:4000
**Working Models**:
- gpt-4o (recommended for patterns)
- gemini-pro (large context)
- perplexity-sonar-large (research)

**Models Under Investigation**:
- remote-local-granite-3-2-8b-instruct (math responses issue)
- remote-local-mistral-7b-instruct (math responses issue)

### Custom Patterns
**Directory**: ~/.config/fabric/custom_patterns/
**Current Patterns**:
- redact_tam_data (✅ working)
- analyze_case (✅ available)
- tam_case_screen (✅ working)
- tam_daily_brief (✅ available)

## Workflow Examples

### Daily TAM Workflow
```bash
# 1. List all active cases
pai-workspace list

# 2. Generate daily briefing
pai-my-plate | fabric -p tam_daily_brief -m gpt-4o

# 3. Screen new cases
pai-workspace case 04056105 analyze

# 4. Research emerging issues
echo "OpenShift 4.17 issues" | fabric -p extract_wisdom -m perplexity-sonar-large
```

### Case Analysis Workflow
```bash
# 1. Find case across specialties
pai-workspace case 04056105 info

# 2. Run comprehensive analysis
pai-workspace case 04056105 analyze

# 3. Research related issues
rhcase kcs search "relevant terms" | fabric -p extract_wisdom -m gpt-4o
rhcase jira search "issue keywords" | fabric -p analyze_claims -m gpt-4o

# 4. Generate redacted summary for sharing
cat analysis.md | fabric -p redact_tam_data -m gpt-4o
```

### Multi-Specialty Workflow
```bash
# Find case regardless of specialty
pai-workspace case 04056105 info
# Output shows: Specialty: tam-ocp, Account: bny

# Create case in specific specialty
pai-workspace create tam-ai newclient 04567890

# Link specialty for easy access
pai-workspace link tam-sec discover
```

### Knowledge Base Workflow
```bash
# Search knowledge base
pai-search search "OpenShift networking"
pai-search search "case analysis" smart

# Add case analysis to knowledge base
pai-search add cases "Case 04056105 Analysis" "$(cat analysis.md)"

# Search by category
pai-search list cases
pai-search stats

# AI-enhanced knowledge extraction
rhcase kcs fetch 123456 | fabric -p extract_wisdom -m gpt-4o | pai-search add docs "KCS 123456 Insights" "$(cat -)"
```

## Configuration Files

### workspace.yaml
**Location**: ~/.claude/context/config/workspace.yaml
**Purpose**: Maps TAM specialties, accounts, and directory structures

### fabric-integration.yaml
**Location**: ~/.claude/context/config/fabric-integration.yaml
**Purpose**: Fabric + LiteLLM configuration for PAI

## Maintenance

### Pattern Documentation Updates
Run after adding new patterns or modifying existing ones:
```bash
pai-update-pattern-docs
```

### Tool Inventory Updates
Run to refresh tool and repository listings:
```bash
pai-local-tool-inventory
```

### Pattern Testing
Test specific patterns during development:
```bash
pai-update-pattern-docs test pattern_name
```

## Security Considerations
- Always use redact_tam_data before external model access
- Customer data stays in TAM workspace directories
- PAI outputs are temporary and should be synced to case directories
- Audit logging for all AI operations via pai-fabric wrapper
