# pai-gtasks

Google Tasks bidirectional synchronization with Taskwarrior for TAM workflows.

## Location
- **Sync script**: `~/.local/bin/sync-work-tasks.sh`
- **Helper script**: `~/.local/bin/gtasks-setup-helper`
- **Configuration**: `~/.config/syncall/`

## Description
Provides bidirectional synchronization between Google Tasks in your Red Hat workspace and local Taskwarrior task management. Enables CLI-based task management with automatic sync to Google Tasks.

## Setup

### One-time OAuth Setup
```bash
# Run the interactive setup helper
gtasks-setup-helper

# Or manual setup:
# 1. Place Google OAuth credentials
cp /path/to/client_secret.json ~/.config/syncall/google_client_secret.json
chmod 600 ~/.config/syncall/google_client_secret.json

# 2. Initial authentication (opens browser)
tw_gtasks_sync -l "To Do" -t work --google-secret ~/.config/syncall/google_client_secret.json
```

### Saved Configurations
- **work-tasks**: Syncs "To Do" list with 'work' tag

## Daily Workflow Integration

### Task Management
```bash
# View all work tasks
task list tag:work

# Add a new task (syncs to Google)
task add "Review case 04123456" +work priority:H

# Complete a task
task 42 done

# View next actionable task
task next tag:work

# Search tasks
task list tag:work /OpenShift/
```

### Manual Sync
```bash
# Use saved configuration
tw_gtasks_sync -b work-tasks.yaml

# Check sync logs
tail -f ~/.local/share/syncall/sync.log
```

## Commands

### Taskwarrior Commands
- `task add <description> +tag` - Add new task with tag
- `task list tag:<tag>` - List tasks with specific tag
- `task <id> done` - Mark task as complete
- `task <id> modify <changes>` - Update task details
- `task next` - Show next actionable task

### Syncall Commands
- `tw_gtasks_sync -l "<list>" -t <tag>` - Sync specific list with tag
- `tw_gtasks_sync -b <config>` - Use saved configuration
- `tw_gtasks_sync --save-as <name>` - Save current config

## Integration Features

### Bidirectional Sync
- Tasks created in Google Tasks appear in Taskwarrior
- Tasks created in Taskwarrior appear in Google Tasks
- Status updates sync both ways
- Automatic conflict resolution (most recent wins)

### Tag-based Organization
- Each Google Tasks list can map to a Taskwarrior tag
- Multiple lists can be synced with different tags
- Maintains task relationships and dependencies

### Automation
- Cron job runs every 15 minutes
- Automatic OAuth token refresh
- Detailed sync logging

## Configuration

### OAuth Credentials
```yaml
# Stored in ~/.config/syncall/
google_client_secret.json  # OAuth client credentials
token.json                 # Auto-refreshing access token
```

### Saved Sync Configurations
```yaml
# Example: work-tasks.yaml
tw_filter: ""
tw_tags: ["work"]
tw_project: null
gtasks_list: "To Do"
resolution_strategy: "MostRecentRS"
```

### Cron Schedule
```bash
*/15 * * * * ~/.local/bin/sync-work-tasks.sh
```

## Available Google Tasks Lists
- **To Do** - Main work tasks (synced with 'work' tag)
- **Blocked** - Tasks waiting on others
- **Doing** - Currently active tasks
- **Maybe** - Potential future tasks
- **TBR** - To Be Read items

## Security and Privacy
- Uses separate OAuth client from email/calendar
- Credentials stored with 600 permissions
- Only accesses Google Tasks API scope
- All sync activity logged locally

## Troubleshooting

### Authentication Issues
```bash
# Re-authenticate
rm ~/.config/syncall/token.json
tw_gtasks_sync -b work-tasks.yaml
```

### Sync Conflicts
- Default: Most recent modification wins
- Alternative strategies: AlwaysFirstRS (Taskwarrior wins), AlwaysSecondRS (Google wins)

### Check Sync Status
```bash
# View recent sync activity
tail -n 50 ~/.local/share/syncall/sync.log

# Count synced tasks
task count tag:work
```

## Requirements
- Google Workspace account (Red Hat)
- Taskwarrior (`task`) installed
- syncall with Google/Taskwarrior support
- Google Tasks API enabled in Cloud Console
- OAuth 2.0 credentials (Desktop app type)
