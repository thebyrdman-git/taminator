# TAM RFE Report Scheduler

Schedule automated TAM reports and case summaries.

## Features

- ✅ Schedule reports using cron format
- ✅ Execute any RFE tool command
- ✅ Email delivery (planned)
- ✅ Multiple schedule management
- ✅ Manual execution for testing
- ⏸️ Daemon mode (future)

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

### 1. Add a Schedule

```bash
tam-rfe-schedule add "Westpac Weekly Summary" \
  --command "tam-rfe-chat 'Show Westpac cases from last 7 days'" \
  --frequency "0 8 * * 1" \
  --email jbyrd@redhat.com
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

### 4. Remove Schedule

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

## Commands Reference

### Add Schedule
```bash
tam-rfe-schedule add "Name" \
  --command "command to run" \
  --frequency "0 8 * * 1" \
  --email you@redhat.com \
  [--format text|html]
```

### List Schedules
```bash
tam-rfe-schedule list
```

### Run Schedule (Test)
```bash
tam-rfe-schedule run <schedule-id>
```

### Remove Schedule
```bash
tam-rfe-schedule remove <schedule-id>
```

### Check Status
```bash
tam-rfe-schedule status
```

### View Logs
```bash
tam-rfe-schedule logs [schedule-id]
```

## Configuration

Schedules are stored in: `~/.config/tam-rfe-scheduler/schedules.yaml`

Example configuration:
```yaml
schedules:
  - id: westpac-weekly
    name: "Westpac Weekly Summary"
    command: "tam-rfe-chat 'Show Westpac cases'"
    frequency: "0 8 * * 1"
    email: jbyrd@redhat.com
    format: text
    enabled: true
    created: 2025-10-16T12:00:00Z
```

## Integration with RFE Tools

Can schedule any RFE command:

### Intelligence Tools
```bash
--command "tam-rfe-chat 'natural language query'"
--command "tam-rfe-validate-intelligence"
--command "tam-rfe-discover-customers"
```

### Hydra Tools
```bash
--command "tam-rfe-hydra-api my-assignments"
--command "tam-rfe-hydra-api org NAPS"
--command "tam-rfe-discover-customers-hydra my-portfolio"
--command "tam-rfe-discover-customers-hydra geo APAC"
```

### Case Management
```bash
--command "tam-rfe-onboard-intelligent"  # Not recommended for scheduling
```

## Current Limitations

**Phase 1 (Current):**
- ✅ Schedule management (add/list/remove)
- ✅ Manual execution (run command)
- ✅ Cron format support
- ❌ No automatic execution (daemon not implemented)
- ❌ No email delivery yet
- ❌ No execution history/logs

**Phase 2 (Planned):**
- Daemon mode for automatic execution
- Email delivery via SMTP
- Execution history and logging
- HTML report formatting

**Phase 3 (Future):**
- Report templates
- Conditional scheduling
- Slack integration
- Web UI

## Manual Execution Workaround

Until daemon mode is implemented, use cron directly:

```bash
# Add to crontab
crontab -e

# Add line:
0 8 * * 1 $HOME/.local/bin/tam-rfe-schedule run westpac-weekly >> /tmp/tam-scheduler.log 2>&1
```

## Troubleshooting

### Schedule Not Found
```bash
❌ Schedule 'my-report' not found

# Check available schedules
tam-rfe-schedule list
```

### Command Fails
```bash
# Test command directly first
tam-rfe-chat 'your query'

# Then test via scheduler
tam-rfe-schedule run <schedule-id>
```

### Missing Configuration
```bash
# Config created automatically on first use
# Location: ~/.config/tam-rfe-scheduler/schedules.yaml
```

## Architecture

```
scheduler/
├── bin/
│   └── tam-rfe-schedule           # Main CLI (Sys Admin persona)
├── config/
│   └── ~/.config/tam-rfe-scheduler/schedules.yaml
└── install.sh                     # Setup script
```

**Command Aliases:**
- `tam-rfe-schedule` → Primary command
- `tam-rfe-scheduler` → Symlink
- `active-case-report-scheduler` → Symlink

All three execute the same tool.

## Communication Style

This tool follows **Sys Admin persona**:
- Direct, actionable output
- Clear error messages with fixes
- No unnecessary verbosity
- Professional status indicators

Example output:
```
✅ Schedule added
ID: westpac-weekly
Command: tam-rfe-chat 'Westpac summary'
Frequency: 0 8 * * 1 (cron format)
Email: jbyrd@redhat.com

Next: tam-rfe-schedule run westpac-weekly  # Test it
```

---

**Status:** Phase 1 MVP - Manual scheduling with test execution  
**Next:** Daemon mode + email delivery (Phase 2)

