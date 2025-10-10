# pai-email-sync

Automated email synchronization and processing with systemd integration.

## Location
`~/.local/bin/pai-email-sync`

## Description
Automated email synchronization system that pulls Gmail emails via lieer, processes Hydra notifications, and provides systemd timer-based automation for continuous email monitoring.

## Key Features
- **Automated Gmail sync**: Uses lieer (gmi) for OAuth-authenticated email pulling
- **Hydra processing**: Automatic processing of Hydra notifications
- **Systemd integration**: Timer-based automation every 15 minutes
- **Comprehensive logging**: All operations logged to dedicated log file
- **Error handling**: Graceful failure handling with audit logging

## Commands

### Manual Operations
```bash
pai-email-sync pull                 # Pull emails and process Hydra notifications once
```

### Automation Management
```bash
pai-email-sync setup [interval]     # Setup automated sync
pai-email-sync status               # Check automation status and recent activity
pai-email-sync disable             # Disable automation

# Examples:
pai-email-sync setup 15min         # Every 15 minutes (default)
pai-email-sync setup 10min         # Every 10 minutes
pai-email-sync setup 30min         # Every 30 minutes
```

## Automation Features

### Systemd Timer Integration
- **Service**: `pai-email-sync.service` (oneshot execution)
- **Timer**: `pai-email-sync.timer` (configurable intervals)
- **Persistent**: Runs even if system was down during scheduled time
- **Logging**: Integrated with systemd journal

### Default Schedule
- **Interval**: Every 15 minutes
- **Persistence**: Yes (catches up missed runs)
- **Error handling**: Continues on failure, logs errors

### Timer Management
```bash
# Check timer status
systemctl --user status pai-email-sync.timer

# View timer schedule
systemctl --user list-timers pai-email-sync.timer

# Manual timer control
systemctl --user start pai-email-sync.timer
systemctl --user stop pai-email-sync.timer
```

## Email Processing Workflow

### Pull Process
1. **Gmail Authentication**: Uses existing OAuth credentials
2. **Email Pulling**: `gmi pull` to sync new emails
3. **Hydra Processing**: Runs pai-hydra-processor for notifications
4. **Logging**: All activities logged to email-sync.log
5. **Audit Trail**: Security logging via pai-audit

### Hydra Notification Processing
- **Pattern Detection**: Identifies "Hydra: Case XXXXXXXX" subjects
- **Metadata Extraction**: Case numbers, severity, account info
- **Markdown Conversion**: Structured output with YAML frontmatter
- **Case Integration**: Links to pai-workspace for case analysis

## Logging and Monitoring

### Log Files
- **Email sync log**: `~/.claude/context/logs/email-sync.log`
- **Audit log**: `~/.claude/context/logs/pai-audit.log` (via pai-audit)
- **Systemd journal**: Standard systemd logging

### Log Format
```
[2025-01-07T12:00:00Z] Starting email pull...
[2025-01-07T12:00:05Z] Email pull completed successfully
[2025-01-07T12:00:06Z] Processing Hydra notifications...
[2025-01-07T12:00:08Z] Hydra processing completed
```

### Status Monitoring
```bash
pai-email-sync status
```

Shows:
- **Automation status**: Enabled/disabled
- **Next run time**: When next sync will occur
- **Recent activity**: Last 5 log entries
- **Processed notifications**: Recent Hydra notifications

## Integration Points

### Daily Workflow Integration
- **Automated background sync**: Runs every 15 minutes
- **pai-my-plate-v2**: Includes email intelligence in daily briefings
- **pai-hydra-processor**: Processes case notifications automatically

### Security Integration
- **pai-audit logging**: All operations tracked
- **OAuth security**: Secure Gmail API access
- **No data retention**: Only processes, doesn't store email content

### Error Recovery
- **Graceful failures**: Continues operation despite individual failures
- **Audit logging**: All errors tracked for analysis
- **Retry capability**: Manual retry via pai-email-sync pull

## Configuration

### Email Configuration
- **Gmail repo**: `~/.claude/context/capture/email/gmail-gvaughn/`
- **OAuth credentials**: Stored by lieer in .gmailieer.json
- **Notmuch database**: `~/.claude/context/capture/email/`

### Systemd Configuration
- **Service file**: `~/.config/systemd/user/pai-email-sync.service`
- **Timer file**: `~/.config/systemd/user/pai-email-sync.timer`
- **Working directory**: Gmail repo directory

## Troubleshooting

### Common Issues
- **OAuth expiration**: Re-authenticate with `gmi auth`
- **Timer not running**: Check `systemctl --user status pai-email-sync.timer`
- **Processing failures**: Check logs with `pai-email-sync status`
- **Permission issues**: Verify directory permissions

### Debug Commands
```bash
# Check email sync status
pai-email-sync status

# Manual email pull to test
pai-email-sync pull

# Check systemd logs
journalctl --user -u pai-email-sync.service

# View recent audit events
pai-audit show-log "EMAIL_SYNC" 10
```

## Performance
- **Lightweight operation**: Minimal resource usage
- **Background processing**: Non-blocking automation
- **Efficient sync**: Only processes new emails
- **Batch processing**: Handles multiple notifications efficiently

## Security Considerations
- **OAuth security**: Secure Google API access
- **Local processing**: No external data transmission
- **Audit compliance**: Complete operation logging
- **Error containment**: Failures don't expose data
