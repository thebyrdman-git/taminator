# PAI Tools Context Documentation

## Available Tools and Their Usage

### Core PAI Tools
Located in `~/.local/bin/` and integrated with TAM workflows:

#### pai-workspace
**Purpose**: Multi-specialty TAM workspace management
**Usage**: 
- `pai-workspace list` - Show all accounts by specialty with case counts
- `pai-workspace case <number> info` - Find case across all specialties
- `pai-workspace case <number> analyze` - Run AI analysis on case
- `pai-workspace create <account> <case>` - Create new case structure

#### pai-case-initial-screen-v2
**Purpose**: Enhanced case screening with AI analysis
**Usage**:
- `pai-case-initial-screen-v2 -a -c 04056105` - AI analysis (auto-detects case location)
- `pai-case-initial-screen-v2` - Template mode for manual completion

#### pai-my-plate-v2
**Purpose**: Comprehensive daily TAM briefing with case numbers
**Usage**:
- `pai-my-plate-v2` - Generate comprehensive daily briefing
- `pai-my-plate-v2 schedule 07:00` - Setup automated daily generation
- `pai-my-plate-v2 stats` - Show briefing statistics

#### pai-case-processor
**Purpose**: Automated case lifecycle and comprehensive analysis
**Usage**:
- `pai-case-processor all` - Process all accounts across specialties
- `pai-case-processor account <specialty> <account>` - Process specific account
- `pai-case-processor case <specialty> <account> <case>` - Analyze specific case
- `pai-case-processor report` - Generate daily case analysis report

#### pai-supportshell
**Purpose**: SupportShell remote analysis with OADP handling
**Usage**:
- `pai-supportshell pull <case>` - Pull case attachments with yank -y
- `pai-supportshell tree <case>` - Show case structure with tree -L 3
- `pai-supportshell analyze-all <case>` - Comprehensive analysis with auto-troubleshoot
- `pai-supportshell insights <case>` - Red Hat Insights analysis
- `pai-supportshell etcd <case>` - etc-ocp-diag.py analysis
- `pai-supportshell omc <case>` - OMC analysis
- `pai-supportshell troubleshoot <case> <cmd> <error>` - AI-assisted troubleshooting

#### pai-hydra
**Purpose**: Red Hat Hydra API ad-hoc query tool for contact and case lookups
**Usage**:
- `pai-hydra email <email>` - Look up SSO username by email address
- `pai-hydra sso <username>` - Look up contact details by SSO username
- `pai-hydra case <case_number>` - Get case information from Hydra
- `pai-hydra contacts <account_number>` - List contacts for an account
- `pai-hydra auth` - Test Hydra API authentication status
- `pai-hydra --format json <command>` - Output results in JSON format

#### pai-email-to-sso
**Purpose**: Convert email addresses to SSO usernames for portal integration
**Usage**:
- `pai-email-to-sso <email>` - Look up SSO username by email address
- `echo "user@domain.com" | pai-email-to-sso` - Process email from stdin
- `cat email_list.txt | pai-email-to-sso` - Batch process email list

#### pai-contacts-label
**Purpose**: Add labels to Google Workspace contacts via People API
**Usage**:
- `pai-contacts-label --label "TAM-BNY" <email>` - Add label to single contact
- `cat email_list.txt | pai-contacts-label --label "TAM-BNY"` - Process emails from stdin
- `pai-contacts-label --label "TAM" --label "OpenShift" <email>` - Apply multiple labels
- First run requires OAuth setup with Google Cloud Console credentials

#### pai-servicenow
**Purpose**: ServiceNow ticket reporting and analysis integration
**Usage**:
- `pai-servicenow auth --instance <instance> --user <username>` - Configure ServiceNow authentication
- `pai-servicenow tickets --group "<assignment_group>" [--days <N>]` - Query tickets by assignment group
- `pai-servicenow tickets --assignee "<user>" [--state <state>]` - Query tickets by assignee
- `pai-servicenow tickets --priority <level> [--days <N>]` - Query tickets by priority level
- `pai-servicenow report daily --group "<group>" [--format <format>]` - Generate daily ticket reports
- `pai-servicenow report sla --assignee "<user>" --days <N>` - Generate SLA analysis reports
- `pai-servicenow export --query "<query>" --format <csv|json|md>` - Export filtered ticket data
- `pai-servicenow status` - Check authentication and connectivity status
- `pai-servicenow sync --days <N>` - Sync tickets to PAI knowledge base

#### pai-search
**Purpose**: Markdown knowledge base search and management
**Usage**:
- `pai-search search <query>` - Full text search
- `pai-search search <query> smart` - AI-enhanced search with fabric
- `pai-search add <category> <title> <content>` - Add knowledge entry
- `pai-search stats` - Show knowledge base statistics

#### pai-audit
**Purpose**: Security, audit logging, and secrets management
**Usage**:
- `pai-audit log <type> <details>` - Manual audit logging
- `pai-audit show-log [filter] [lines]` - View audit logs
- `pai-audit secret {set|get|list|delete} <name>` - Encrypted secrets management
- `pai-audit fabric <pattern> <model> <data>` - Secure fabric calls with auto-redaction
- `pai-audit status` - Security status and metrics

#### pai-email-processor
**Purpose**: Email intelligence and contact research
**Usage**:
- `pai-email-processor process [days] [max]` - Process recent emails
- `pai-email-processor issues [days]` - Identify potential issues
- `pai-email-processor contact <email> [name]` - Research contact dossier
- `pai-email-processor summary [days]` - Email summary for briefings
- `pai-email-processor discover [days]` - Generate Discover-specific email summary
- `pai-email-processor search <query> [days]` - Search emails and create summary

#### pai-hydra-processor
**Purpose**: Hydra notification processing and case extraction
**Usage**:
- `pai-hydra-processor` - Process recent Hydra notifications
- `pai-hydra-processor --days <N>` - Process N days of notifications
- `pai-hydra-processor --list` - List processed notifications

#### pai-gmail-sync
**Purpose**: Direct Gmail API sync (replaces gmailieer)
**Usage**:
- `pai-gmail-sync` - Sync last 7 days (200 emails max)
- Uses custom OAuth with refresh tokens for automation
- Saves emails to maildir format for notmuch integration

#### pai-email-sync
**Purpose**: Automated email synchronization and processing
**Usage**:
- `pai-email-sync pull` - Manual email sync (now uses pai-gmail-sync)
- `pai-email-sync setup [interval]` - Setup automation (default: 15min)
- `pai-email-sync status` - Check automation status

#### pai-email-cron-status
**Purpose**: Monitor automated email sync health
**Usage**:
- `pai-email-cron-status` - Check cron job status, OAuth tokens, sync logs
- Shows total email count, recent activity, connectivity status
- Monitor logs: `tail -f ~/.claude/context/logs/email-sync.log`

#### pai-slack-query
**Purpose**: Automated Slack message extraction and search (uses slackdump)
**Usage**:
- `pai-slack-query setup` - One-time authentication setup (EZ-Login 3000)
- `pai-slack-query search <query> [days]` - Search Slack messages
- `pai-slack-query channels [days] [max]` - Extract recent channel messages
- `pai-slack-query dms [days]` - Extract direct message conversations
- `pai-slack-query status` - Check system status and authentication
- `pai-slack-query test` - Test authentication and connectivity

#### pai-slack-processor (created by pai-slack-query)
**Purpose**: Slack message analysis and TAM relevance scoring
**Usage**:
- `pai-slack-processor analyze [days]` - Analyze Slack messages for TAM relevance
- `pai-slack-processor search <query> [days]` - Search and analyze results
- `pai-slack-processor summary [days]` - Generate Slack activity summary

#### pai-calendar
**Purpose**: Google Calendar integration and meeting preparation
**Usage**:
- `pai-calendar today [date]` - Show meetings for date
- `pai-calendar summary [date]` - Daily calendar summary with prep status
- `pai-calendar prep <meeting_title>` - Generate meeting preparation
- `pai-calendar agenda [days]` - Show upcoming agenda

#### pai-fabric
**Purpose**: Fabric + LiteLLM integration wrapper
**Usage**:
- `pai-fabric redact` - Redact sensitive data using custom pattern
- `pai-fabric analyze` - Case analysis using TAM methodology
- `pai-fabric research` - Online research with Perplexity
- `pai-fabric models` - List available models

#### pai-update-pattern-docs
**Purpose**: Automatic pattern documentation generator
**Usage**:
- `pai-update-pattern-docs` - Update documentation
- `pai-update-pattern-docs test <pattern>` - Test specific pattern

### Red Hat Internal Tools

#### rhcase
**Purpose**: Case management and knowledge base access
**Usage**:
- `rhcase analyze <case_number>` - Analyze specific case
- `rhcase kcs search "<terms>"` - Search knowledge base
- `rhcase jira search "<terms>"` - Search JIRA issues
- `rhcase list <account>` - List cases for account

#### lefty2
**Purpose**: Case reporting and analytics
**Usage**: Advanced reporting capabilities for TAM metrics

### AI-Powered Analysis

#### fabric
**Purpose**: Pattern-based AI analysis via LiteLLM proxy
**Working Models**: gpt-4o, gemini-pro, perplexity-sonar-large, remote-local-granite-3-2-8b-instruct
**Custom Patterns**:
- `redact_tam_data` - ✅ Working redaction pattern
- `analyze_case` - Case analysis following workflow.md
- `tam_case_screen` - ✅ Working case screening
- `tam_daily_plate` - Daily briefing generation
- Standard patterns: `summarize`, `analyze_incident`, `extract_wisdom`

**Usage Examples**:
```bash
# Redact sensitive data
echo "Account 1216348..." | fabric -p redact_tam_data -m gpt-4o

# Analyze case data
cat case.json | fabric -p tam_case_screen -m gpt-4o

# Research topics
echo "OpenShift 4.17 issues" | fabric -p extract_wisdom -m perplexity-sonar-large
```

### SupportShell Tools

#### sushe / supportshell-tool-scan
**Purpose**: Access SupportShell environment for secure analysis
**Usage**: 
- `sushe` - Connect to SupportShell
- `supportshell-tool-scan` - List available tools in SupportShell

#### yank-ng (SupportShell)
**Purpose**: Advanced log extraction and analysis
**Usage**: `yank-ng --case <number> --pattern "error"`

### System Tools

#### pai-local-tool-inventory
**Purpose**: Inventory all available tools and repositories
**Usage**: `pai-local-tool-inventory` - Lists tools and repos

#### pai-services
**Purpose**: Manage PAI infrastructure services
**Usage**:
- `pai-services start` - Start services
- `pai-services status` - Check service status
- `pai-services logs` - View service logs

## Tool Integration Workflows

### Complete Daily TAM Workflow
```bash
# 1. Comprehensive daily briefing with case numbers
pai-my-plate-v2

# 2. Calendar preparation
pai-calendar summary

# 3. Process all account cases
pai-case-processor all

# 4. Email intelligence
pai-email-sync pull

# 5. Slack intelligence (on-demand)
pai-slack-query search "discover" 1    # Daily customer mentions
pai-slack-query dms 1                  # Today's important DMs

# 6. Case analysis
pai-workspace case 04056105 analyze

# 7. SupportShell analysis
pai-supportshell pull 04056105
pai-supportshell analyze-all 04056105
```

### Case Analysis Workflow
```bash
# 1. Find and analyze case
pai-workspace case 04056105 info
pai-workspace case 04056105 analyze

# 2. Research related issues
rhcase kcs search "relevant terms"
rhcase jira search "issue keywords"

# 3. SupportShell analysis
pai-supportshell pull 04056105
pai-supportshell insights 04056105

# 4. Add to knowledge base
pai-search add cases "Case Analysis" "$(cat analysis.md)"
```

### Email and Calendar Workflow
```bash
# 1. Process recent emails
pai-email-processor process 1 20

# 2. Generate calendar summary
pai-calendar summary

# 3. Prepare for specific meeting
pai-calendar prep "Customer Sync Meeting"

# 4. Research contacts
pai-email-processor contact "john@company.com" "John Smith"
```

## Model Selection Guidelines
- **Redaction**: Use gpt-4o (tested working with custom patterns)
- **Analysis**: Use gpt-4o, gemini-pro, or remote-local-granite-3-2-8b-instruct
- **Research**: Use perplexity-sonar-large for current information
- **Reasoning**: Use gpt-5-reasoning (o3) for complex problems

## Security Notes
- Always redact sensitive data before using external models
- All operations logged via pai-audit
- Customer data stays in designated directories
- Automated case lifecycle management