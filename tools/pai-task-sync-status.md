# pai-task-sync-status

## Purpose
Comprehensive monitoring and health dashboard for PAI task synchronization between PAI projects, Taskwarrior, and Google Tasks.

## Location
`~/.local/bin/pai-task-sync-status`

## Description
`pai-task-sync-status` provides real-time monitoring of the complete task integration ecosystem, showing sync health, statistics, error status, and automation status. Essential for maintaining the mobile-accessible task management workflow.

## Key Features
- **Real-time Statistics**: Task counts across all sync systems
- **Sync Health Monitoring**: Last successful sync tracking
- **Error Detection**: Identifies and reports sync failures
- **Cron Job Status**: Monitors automated sync scheduling
- **Next Sync Prediction**: Shows when next automatic sync will occur
- **Visual Dashboard**: Color-coded status indicators

## Usage

### Basic Command
```bash
pai-task-sync-status
```

### Complete Output Example
```
🔄 PAI Task Sync Status
==================================================
📊 Current Statistics
----------------------------------
PAI Tasks:
  Total: 15
  Pending: 12
  In-Progress: 2
  Completed: 1
  Blocked: 0

Taskwarrior PAI Tasks:
  Total: 15
  Pending: 14
  Completed: 1
  Waiting: 0
  Deleted: 0

📋 Recent Sync Activity
----------------------------------
Last 5 sync events:
  2025-09-17 21:08:11 - Starting automated PAI task sync
  🔄 Starting bidirectional sync...
  ✅ Synced 15 tasks from PAI to Taskwarrior
  ✅ Updated 2 PAI tasks from Taskwarrior
  2025-09-17 21:08:12 - Sync completed successfully

✅ Last successful sync: 2025-09-17 21:08:12

⚠️ Error Status
----------------------------------
✅ No errors

⏰ Cron Job Status
----------------------------------
✅ Cron job active (every 15 minutes)
  Schedule: */15 * * * * /home/grimm/.local/bin/pai-task-sync-cron >/dev/null 2>&1

⏭️ Next scheduled sync: 2025-09-17 21:23:11

==================================================
Commands:
  pai-task-sync bidirectional  # Manual sync
  pai-projects summary         # View projects
  tail -f /home/grimm/.claude/context/logs/pai-task-sync-cron.log # Watch live sync
```

## Status Indicators

### Color Coding
- **🔄 Blue**: Information and section headers
- **✅ Green**: Successful operations and healthy status
- **⚠️ Yellow**: Warnings and attention items
- **❌ Red**: Errors and failed operations

### Health Checks

#### Sync Health
- **✅ Healthy**: Recent successful sync within 20 minutes
- **⚠️ Warning**: No sync in 20-60 minutes
- **❌ Critical**: No sync in over 60 minutes

#### Error Status
- **✅ No errors**: Clean error log or no error log file
- **⚠️ Recent errors**: Errors within last 24 hours
- **❌ Critical errors**: Multiple recent errors indicating systemic issues

#### Cron Status
- **✅ Active**: Cron job found and properly scheduled
- **❌ Missing**: Cron job not found in crontab

## Data Sources

### PAI Projects Statistics
**Source**: `~/.claude/context/create/outputs/projects/projects.yaml`
**Metrics**:
- Total task count across all projects
- Breakdown by status (pending, in-progress, completed, blocked)
- Project category distribution

### Taskwarrior Statistics
**Source**: `task export` with PAI tag filtering
**Metrics**:
- Total PAI-tagged tasks in Taskwarrior
- Status distribution (pending, completed, waiting, deleted)
- Recent activity tracking

### Sync Activity
**Source**: `~/.claude/context/logs/pai-task-sync-cron.log`
**Tracking**:
- Sync operation timestamps
- Success/failure status
- Error messages and debugging info
- Performance metrics

### Error Monitoring
**Source**: `~/.claude/context/logs/pai-task-sync-error.log`
**Detection**:
- Sync operation failures
- Configuration issues
- Authentication problems
- System resource constraints

## Automation Monitoring

### Cron Job Verification
- **Schedule Check**: Verifies 15-minute interval is active
- **Command Validation**: Confirms correct script path
- **Execution Status**: Tracks recent cron runs

### Next Sync Prediction
- **Calculation**: Based on last sync timestamp + 15 minutes
- **Accuracy**: Accounts for system clock and cron timing
- **Display**: Human-readable next sync time

## Integration with Complete Ecosystem

### Mobile Workflow Monitoring
The status tool shows the complete mobile integration health:

1. **PAI → Taskwarrior**: Tracks how local changes reach Taskwarrior
2. **Taskwarrior → Google Tasks**: Monitored through existing sync logs
3. **Google Tasks → Mobile**: Real-time (outside monitoring scope)
4. **Mobile → PAI**: Tracks how phone changes reach PAI

### Performance Tracking
- **Sync Timing**: How long operations take
- **Task Throughput**: Number of tasks processed per sync
- **Error Rates**: Frequency of sync failures
- **System Load**: Impact on overall system performance

## Troubleshooting Integration

### Common Issues and Solutions

#### "No recent sync activity"
**Diagnosis**: Check if cron job is running
```bash
systemctl status crond
crontab -l | grep pai-task-sync
```

#### "PAI and Taskwarrior task counts don't match"
**Diagnosis**: Sync interruption or configuration issue
```bash
pai-task-sync push  # Force resync from PAI
task list +pai      # Verify Taskwarrior state
```

#### "Errors detected"
**Diagnosis**: Check error log for specific issues
```bash
tail -20 ~/.claude/context/logs/pai-task-sync-error.log
```

#### "Mobile changes not appearing in PAI"
**Diagnosis**: Check complete sync chain
```bash
# 1. Verify Google Tasks → Taskwarrior sync
tail -f ~/.local/share/syncall/sync.log

# 2. Force PAI update
pai-task-sync pull

# 3. Check PAI dashboard
pai-projects summary
```

## Related Commands

### Quick Health Check Sequence
```bash
# Full system health
pai-task-sync-status

# PAI project view
pai-projects summary

# Taskwarrior PAI tasks
task list +pai

# Google sync status
tail -5 ~/.local/share/syncall/sync.log

# Force full sync if needed
pai-task-sync bidirectional
```

### Emergency Recovery
```bash
# If sync is completely broken
pkill -f pai-task-sync          # Stop any running syncs
rm /tmp/pai-task-sync.lock      # Clear lock file
pai-task-sync push              # Rebuild from PAI
pai-task-sync-status            # Verify recovery
```

## Log Analysis

### Key Log Patterns
- **Success**: "Sync completed successfully"
- **Errors**: "ERROR:" prefix in error log
- **Lock Issues**: "Sync already running" messages
- **Performance**: "Sync stats:" with timing data

### Log Rotation
- **Automatic**: Logs grow but don't auto-rotate
- **Manual**: Periodically archive old logs: `gzip ~/.claude/context/logs/*.log`
- **Monitoring**: Watch disk usage in `~/.claude/context/logs/`

## Performance Benchmarks

### Typical Sync Times
- **15 PAI tasks**: 2-5 seconds
- **Status update only**: Under 1 second
- **Full ecosystem sync**: Under 30 seconds total

### Resource Impact
- **CPU**: Brief spike during sync only
- **Memory**: Under 50MB during operation
- **Disk**: Log files grow ~1KB per sync operation

---

**Purpose**: System health and performance monitoring
**Automation**: Works with 15-minute cron cycle
**Integration**: Complete mobile workflow tracking
**Reliability**: ✅ Production monitoring tool