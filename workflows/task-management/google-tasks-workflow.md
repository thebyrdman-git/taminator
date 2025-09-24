# Google Tasks + Taskwarrior Workflow

Integrated task management workflow combining Google Tasks with local Taskwarrior CLI for Red Hat TAM work.

## Overview

This workflow enables bidirectional synchronization between Google Tasks (in your Red Hat workspace) and Taskwarrior, providing powerful CLI-based task management that stays in sync with your Google Workspace.

## Initial Setup (One-time)

1. **Run the setup helper**:
   ```bash
   gtasks-setup-helper
   ```

2. **Follow the interactive prompts** to:
   - Authenticate with Google (uses existing OAuth client)
   - Select Google Tasks list to sync
   - Configure Taskwarrior tags
   - Set up automatic synchronization

## Daily Task Management Workflow

### Morning Routine
```bash
# Review all work tasks
task list tag:work

# Check what needs attention today
task next tag:work

# View task burndown/statistics
task burndown.weekly tag:work
```

### Adding Tasks

#### From Command Line (syncs to Google)
```bash
# Quick task
task add "Review case 04123456" +work

# Task with priority
task add "Urgent: Customer escalation" +work priority:H due:today

# Task with project
task add "Update OpenShift docs" +work project:documentation
```

#### From Google Tasks (syncs to Taskwarrior)
- Add tasks via Google Tasks mobile app or web
- They appear in Taskwarrior after next sync (within 15 minutes)

### Working with Tasks

```bash
# Start working on a task
task 42 start

# Add notes to a task
task 42 annotate "Discussed with customer, needs follow-up"

# Complete a task
task 42 done

# Modify task details
task 42 modify priority:H due:friday
```

### Task Organization

#### By Status
```bash
task list tag:work status:pending     # Active tasks
task list tag:work status:completed   # Recently completed
task list tag:work status:waiting     # Blocked tasks
```

#### By Priority
```bash
task list tag:work priority:H         # High priority only
task list tag:work priority.not:L     # Exclude low priority
```

#### By Time
```bash
task list tag:work due:today          # Due today
task list tag:work due:week           # Due this week
task list tag:work entry:yesterday    # Created yesterday
```

### Advanced Filtering

```bash
# OpenShift-related urgent tasks
task list tag:work priority:H /OpenShift/

# Tasks modified in last 24 hours
task list tag:work modified:24h

# Overdue tasks
task list tag:work +OVERDUE

# Tasks without due dates
task list tag:work due:
```

## Integration with TAM Workflow

### Case Management
```bash
# Create task from case
task add "Case 04123456: Node drain issue" +work project:cases due:today

# Link tasks to accounts
task add "CIBC: Quarterly review prep" +work project:cibc due:friday
```

### Meeting Preparation
```bash
# Tasks from calendar events
task add "Prep for customer sync meeting" +work due:tomorrow +meeting

# Follow-up tasks
task add "Send meeting notes to customer" +work depends:88
```

### Escalation Tracking
```bash
# High-priority escalations
task add "ESCALATION: Production down" +work priority:H +escalation due:now

# View all escalations
task list tag:work +escalation
```

## Sync Management

### Automatic Sync
- Runs every 15 minutes via cron
- Bidirectional updates
- Conflict resolution: most recent wins

### Manual Sync
```bash
# Force immediate sync
tw_gtasks_sync -b work-tasks.yaml

# Check sync status
tail -f ~/.local/share/syncall/sync.log
```

### Multiple List Management
```bash
# Sync different Google Tasks lists
tw_gtasks_sync -l "Blocked" -t blocked --save-as blocked-tasks
tw_gtasks_sync -l "Doing" -t active --save-as active-tasks
```

## Reporting and Analytics

### Task Statistics
```bash
# Summary report
task summary tag:work

# Completed tasks this week
task completed tag:work end:week

# Time tracking report
task timesheet tag:work
```

### Productivity Metrics
```bash
# Task burndown chart
task burndown.daily tag:work

# History graph
task history.monthly tag:work

# Task calendar view
task calendar
```

## Tips and Best Practices

### Task Naming Conventions
- Start with account name for customer tasks: "CIBC: Update firewall rules"
- Use case numbers for support tasks: "Case 04123456: Investigation"
- Tag appropriately: +work, +escalation, +meeting

### Regular Review
```bash
# Weekly review - completed tasks
task completed tag:work end:week

# Identify stale tasks
task list tag:work modified.before:30d

# Clean up completed tasks
task purge
```

### Backup and Recovery
```bash
# Backup Taskwarrior data
cp -r ~/.task ~/.task.backup.$(date +%Y%m%d)

# Export tasks to JSON
task export tag:work > work-tasks-backup.json
```

## Troubleshooting

### Sync Issues
```bash
# Check last sync
grep "Sync completed" ~/.local/share/syncall/sync.log | tail -5

# Re-authenticate if needed
rm ~/.config/syncall/token.json
tw_gtasks_sync -b work-tasks.yaml
```

### Data Integrity
```bash
# Check for duplicates
task duplicates tag:work

# Verify task count matches Google
task count tag:work
```

## Related Tools
- [pai-calendar](../tools/pai-calendar.md) - Calendar integration
- [pai-workspace](../tools/pai-workspace.md) - Case management
- [gmailieer](../capture/email/) - Email integration
