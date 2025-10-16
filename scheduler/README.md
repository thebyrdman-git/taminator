# TAM RFE Report Scheduler

Schedule automated TAM reports and case summaries.

## Features

### Phase 1 & 2 (Complete)
- ✅ Schedule reports using cron format
- ✅ Execute any RFE tool command
- ✅ Email delivery via SMTP
- ✅ Background daemon for automatic execution
- ✅ Multiple schedule management
- ✅ Manual execution for testing

### Phase 3 (Complete)
- ✅ **Report Templates** - Professional HTML emails (weekly digest, executive brief)
- ✅ **Conditional Execution** - Smart conditions (`sev1_count > 0`, `weekday`, etc.)
- ✅ **Slack Integration** - Post reports to Slack channels
- ✅ **Pre-check Commands** - Validate before execution

## Installation

```bash
cd scheduler
./install.sh
```

Creates three command aliases (all same tool):
- `tam-rfe-schedule` (primary, short)
- `tam-rfe-scheduler` (consistent naming)
- `active-case-report-scheduler` (descriptive)

## Quick Start

### 1. Add a Basic Schedule

```bash
tam-rfe-schedule add "Westpac Weekly Summary" \
  --command "tam-rfe-chat 'Show Westpac cases from last 7 days'" \
  --frequency "0 8 * * 1" \
  --email jbyrd@redhat.com
```

### 1b. Add a Schedule with Phase 3 Features

```bash
# With HTML template
tam-rfe-schedule add "Weekly Digest" \
  --command "tam-rfe-chat 'Weekly summary'" \
  --frequency "0 16 * * 5" \
  --email jbyrd@redhat.com \
  --template weekly_digest

# With condition (only if Sev 1 cases exist)
tam-rfe-schedule add "Sev 1 Alert" \
  --command "tam-rfe-chat 'Show Sev 1 cases'" \
  --frequency "0 * * * *" \
  --email jbyrd@redhat.com \
  --condition "sev1_count > 0" \
  --pre-check "tam-rfe-chat 'Count Sev 1'"

# With Slack integration
tam-rfe-schedule add "Team Update" \
  --command "tam-rfe-hydra-api my-assignments" \
  --frequency "0 9 * * 1-5" \
  --slack-webhook "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

### 2. List Schedules

```bash
tam-rfe-schedule list
```

Output:
```
Scheduled Reports
=================

✅ westpac-weekly-summary: Westpac Weekly Summary
   Command: tam-rfe-chat 'Show Westpac cases from last 7 days'
   Schedule: 0 8 * * 1
   Email: jbyrd@redhat.com
```

### 3. Test Execution

```bash
tam-rfe-schedule run westpac-weekly-summary
```

### 4. Start Background Daemon

```bash
tam-rfe-schedule start
```

Schedules now execute automatically in the background.

### 5. Check Status & Logs

```bash
tam-rfe-schedule status
tam-rfe-schedule logs
```

### 6. Remove Schedule

```bash
tam-rfe-schedule remove westpac-weekly-summary
```

## Cron Frequency Format

```
* * * * *
│ │ │ │ │
│ │ │ │ └─ Day of week (0-7, Sunday = 0 or 7)
│ │ │ └─── Month (1-12)
│ │ └───── Day of month (1-31)
│ └─────── Hour (0-23)
└───────── Minute (0-59)
```

### Common Schedules

```bash
# Every weekday at 8am
--frequency "0 8 * * 1-5"

# Every Monday at 9am
--frequency "0 9 * * 1"

# Every Friday at 4pm
--frequency "0 16 * * 5"

# Daily at 6am
--frequency "0 6 * * *"

# Every hour
--frequency "0 * * * *"
```

---

## Phase 3: Advanced Features

### Report Templates

Transform plain command output into professional HTML emails.

**Available Templates:**
- `plain` - Default text output
- `weekly_digest` - Professional weekly summary with statistics
- `executive_brief` - Red Hat branded executive report
- `custom:path/to/template.html` - Your own custom template

**Example:**
```bash
tam-rfe-schedule add "Weekly Digest" \
  --command "tam-rfe-chat 'Weekly customer summary'" \
  --frequency "0 16 * * 5" \
  --email jbyrd@redhat.com \
  --template weekly_digest
```

### Conditional Execution

Run reports only when specific conditions are met.

**Supported Conditions:**
- `always` - Always execute (default)
- `weekday` - Monday-Friday only
- `weekend` - Saturday-Sunday only
- `sev1_count > 0` - When Sev 1 cases exist
- `case_count > 5` - When total cases exceed threshold
- Any numeric comparison: `<`, `>`, `<=`, `>=`, `==`, `!=`

**Example:**
```bash
tam-rfe-schedule add "Sev 1 Alert" \
  --command "tam-rfe-chat 'Show all Sev 1 cases'" \
  --frequency "0 * * * *" \
  --email jbyrd@redhat.com \
  --condition "sev1_count > 0" \
  --pre-check "tam-rfe-chat 'Count Sev 1 cases'"
```

**How It Works:**
1. Pre-check command runs first
2. Output parsed for metrics (e.g., "Sev 1: 3 cases")
3. Condition evaluated with extracted context
4. Main command only runs if condition is true

### Slack Integration

Send reports directly to Slack channels.

**Setup:**
1. Create a Slack Incoming Webhook at: https://api.slack.com/messaging/webhooks
2. Add webhook URL to your schedule

**Example:**
```bash
tam-rfe-schedule add "Daily Standup" \
  --command "tam-rfe-hydra-api my-assignments" \
  --frequency "0 9 * * 1-5" \
  --slack-webhook "https://hooks.slack.com/services/T00/B00/xxx"
```

**Features:**
- Rich message formatting with Slack Blocks API
- Success/failure color coding
- Execution duration tracking
- Professional TAM branding
- Can combine with email delivery

---

## Usage Examples

### Morning Briefing

```bash
tam-rfe-schedule add "Morning TAM Brief" \
  --command "tam-rfe-hydra-api my-assignments" \
  --frequency "0 8 * * 1-5" \
  --email jbyrd@redhat.com
```

### Weekly Customer Review

```bash
tam-rfe-schedule add "Westpac Weekly Review" \
  --command "tam-rfe-chat 'Westpac cases updated last 7 days, grouped by SBR'" \
  --frequency "0 16 * * 5" \
  --email jbyrd@redhat.com
```

### Sev 1 Alert (Hourly)

```bash
tam-rfe-schedule add "Sev 1 Watch" \
  --command "tam-rfe-discover-customers-hydra my-portfolio" \
  --frequency "0 * * * *" \
  --email jbyrd@redhat.com
```

### Intelligence Validation

```bash
tam-rfe-schedule add "Config Health Check" \
  --command "tam-rfe-validate-intelligence" \
  --frequency "0 0 * * 1" \
  --email jbyrd@redhat.com
```

### Geographic Review

```bash
tam-rfe-schedule add "APAC Portfolio" \
  --command "tam-rfe-discover-customers-hydra geo APAC" \
  --frequency "0 9 * * 1" \
  --email jbyrd@redhat.com
```

### Phase 3: Conditional Sev 1 Alert

```bash
tam-rfe-schedule add "Urgent Sev 1 Alert" \
  --command "tam-rfe-chat 'Detailed Sev 1 analysis with root cause'" \
  --frequency "0 * * * *" \
  --email jbyrd@redhat.com \
  --condition "sev1_count > 0" \
  --pre-check "tam-rfe-chat 'Count Sev 1 cases'" \
  --template executive_brief
```

Only sends when Sev 1 cases exist, uses professional template.

### Phase 3: Slack Daily Standup

```bash
tam-rfe-schedule add "Team Standup" \
  --command "tam-rfe-hydra-api my-assignments" \
  --frequency "0 9 * * 1-5" \
  --slack-webhook "$SLACK_WEBHOOK_URL" \
  --condition weekday
```

Posts to Slack, weekdays only.

---

## Architecture

### File Structure

```
~/.config/tam-rfe-scheduler/
├── schedules.yaml              # Schedule configuration
└── logs/
    ├── daemon.log              # Daemon activity log
    ├── daemon.out              # Daemon stdout/stderr
    ├── daemon.pid              # Daemon process ID
    └── execution_history.jsonl # Execution logs (JSONL format)

~/.local/bin/
├── tam-rfe-schedule            # Main CLI
├── tam-rfe-scheduler           # Alias
├── active-case-report-scheduler # Alias
└── tam-rfe-scheduler-daemon    # Background daemon

scheduler/
├── bin/
│   ├── tam-rfe-schedule        # CLI script
│   └── tam-rfe-scheduler-daemon # Daemon script
├── lib/                        # Phase 3 modules
│   ├── template_engine.py      # Report templates
│   ├── conditional_executor.py # Conditional logic
│   └── slack_notifier.py       # Slack integration
├── templates/
│   ├── reports/                # Custom templates
│   └── slack/                  # Slack templates
├── config/
│   └── schedules.example.yaml  # Example configuration
├── install.sh                  # Installation script
└── README.md                   # This file
```

### Daemon Process

The daemon:
1. Loads schedules from `schedules.yaml`
2. Evaluates cron expressions for each schedule
3. Checks conditions (Phase 3)
4. Executes commands when scheduled
5. Renders templates (Phase 3)
6. Sends email notifications
7. Sends Slack notifications (Phase 3)
8. Logs all activity

### Phase 3 Execution Flow

```
1. Schedule time reached
2. Check condition (if specified)
   ├─ Run pre-check command
   ├─ Extract metrics from output
   └─ Evaluate condition
3. If condition met:
   ├─ Execute main command
   ├─ Capture output
   ├─ Render template (if specified)
   ├─ Send email
   └─ Send Slack notification (if configured)
4. Log execution result
```

---

## Daemon Management

### Start Daemon

```bash
tam-rfe-schedule start
```

Daemon runs in background, executes schedules automatically.

### Stop Daemon

```bash
tam-rfe-schedule stop
```

Graceful shutdown with 10-second timeout.

### Restart Daemon

```bash
tam-rfe-schedule restart
```

### Check Status

```bash
tam-rfe-schedule status
```

Shows:
- Running status
- PID
- Log file location
- Schedule count
- Next execution times

### View Logs

```bash
# View all execution history
tam-rfe-schedule logs

# View specific schedule logs
tam-rfe-schedule logs westpac-weekly

# View daemon logs directly
tail -f ~/.config/tam-rfe-scheduler/logs/daemon.log
```

---

## Configuration

### Schedule YAML Format

```yaml
schedules:
  - id: my-report
    name: "Human-readable name"
    command: "tam-rfe-chat 'Query here'"
    frequency: "0 8 * * 1"
    email: "you@redhat.com"
    format: "text"
    template: "weekly_digest"      # Phase 3
    condition: "sev1_count > 0"    # Phase 3
    pre_check_command: "..."       # Phase 3
    slack_webhook: "https://..."   # Phase 3
    enabled: true
    created: "2025-10-16T12:00:00"
    last_run: "2025-10-16T08:00:00"
```

### Environment Variables

- `SMTP_SERVER` - SMTP server (default: localhost)
- `SMTP_PORT` - SMTP port (default: 25)
- `SLACK_WEBHOOK_URL` - Default Slack webhook

---

## Troubleshooting

### Daemon not starting

```bash
# Check if already running
tam-rfe-schedule status

# View daemon logs
cat ~/.config/tam-rfe-scheduler/logs/daemon.log

# Remove stale PID file
rm ~/.config/tam-rfe-scheduler/daemon.pid
```

### Email not sending

1. Check SMTP server is running:
   ```bash
   systemctl status postfix
   ```

2. Test email delivery:
   ```bash
   echo "Test" | mail -s "Test" jbyrd@redhat.com
   ```

3. Check daemon logs for SMTP errors

### Slack not sending

1. Verify webhook URL is valid
2. Test webhook manually:
   ```bash
   curl -X POST -H 'Content-type: application/json' \
     --data '{"text":"Test"}' \
     YOUR_WEBHOOK_URL
   ```
3. Check daemon logs for errors

### Condition not working

1. Test pre-check command manually
2. Verify output contains expected metrics
3. Check daemon logs for condition evaluation
4. Example output format:
   ```
   Sev 1: 3 cases
   Total: 15 cases
   ```

---

## Development

### Adding Custom Templates

Create your own HTML template:

```html
<html>
<body>
  <h1>{{schedule_name}}</h1>
  <pre>{{output}}</pre>
  <p>Generated: {{timestamp}}</p>
</body>
</html>
```

Use it:

```bash
tam-rfe-schedule add "My Report" \
  --command "..." \
  --frequency "..." \
  --email you@redhat.com \
  --template "custom:/path/to/template.html"
```

### Template Variables

Available in all templates:
- `{{output}}` - Command output
- `{{schedule_name}}` - Schedule name
- `{{timestamp}}` - Execution time
- `{{duration}}` - Execution duration

Template-specific variables:
- Weekly Digest: `{{week_start}}`, `{{week_end}}`, `{{total_cases}}`
- Executive Brief: `{{report_date}}`, `{{summary}}`

---

## Sys Admin Notes

Built with directness and efficiency in mind. No bullshit, just working automation.

- Schedules persist across reboots
- Daemon auto-recovers from failures
- All operations logged for audit
- Email + Slack dual delivery supported
- Conditions prevent notification spam
- Templates make reports professional

Deploy this, set it, forget it. It'll handle your TAM reporting.

---

*TAM RFE Report Scheduler*  
*Part of the RFE Bug Tracker Automation Suite*  
*Sys Admin Persona - Direct, Efficient, Reliable*
