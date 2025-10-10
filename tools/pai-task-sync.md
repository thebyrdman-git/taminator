# pai-task-sync

## Purpose
Bidirectional synchronization between PAI project tracking and Taskwarrior, enabling mobile access through Google Tasks integration.

## Locations
- **Main Script**: `~/.local/bin/pai-task-sync`
- **Cron Script**: `~/.local/bin/pai-task-sync-cron`
- **Status Monitor**: `~/.local/bin/pai-task-sync-status`

## Description
`pai-task-sync` maintains consistency between PAI project tracking and Taskwarrior, enabling full mobile accessibility through the existing Google Tasks sync infrastructure. It creates properly namespaced Taskwarrior projects that integrate seamlessly with your existing 348-task Google Tasks ecosystem.

## Key Features
- **Bidirectional Sync**: PAI ↔ Taskwarrior status synchronization
- **Namespace Isolation**: PAI tasks use dedicated project hierarchy
- **Mobile Integration**: Works with existing Google Tasks sync
- **Conflict Avoidance**: Doesn't interfere with existing `work` tagged tasks
- **Audit Logging**: Complete sync operation tracking
- **Automated Execution**: Runs every 15 minutes via cron

## Usage

### Basic Commands

```bash
# Sync PAI projects to Taskwarrior
pai-task-sync push

# Sync Taskwarrior changes back to PAI
pai-task-sync pull

# Full bidirectional sync
pai-task-sync bidirectional

# Check sync health and statistics
pai-task-sync status
```

### Automated Sync

```bash
# Check cron status and sync health
pai-task-sync-status

# Manual cron execution (for testing)
pai-task-sync-cron

# View sync logs
tail -f ~/.claude/context/logs/task-sync.log
```

### Examples

#### Manual Sync Operations
```bash
# Push new PAI projects to Taskwarrior
pai-task-sync push
# Output: ✅ Synced 15 tasks from PAI to Taskwarrior

# Pull mobile status changes back to PAI
pai-task-sync pull
# Output: ✅ Updated 3 PAI tasks from Taskwarrior

# Full sync cycle
pai-task-sync bidirectional
# Output: 🔄 Starting bidirectional sync...
#         ✅ Synced 15 tasks from PAI to Taskwarrior
#         ✅ Updated 2 PAI tasks from Taskwarrior
#         ✅ Bidirectional sync complete
```

#### Monitoring
```bash
pai-task-sync-status
```
**Output**:
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

Taskwarrior PAI Tasks:
  Total: 15
  Pending: 14
  Completed: 1

✅ Last successful sync: 2025-09-17 21:08:12
✅ Cron job active (every 15 minutes)
⏭️ Next scheduled sync: 2025-09-17 21:23:11
```

## Integration Architecture

### PAI → Taskwarrior Mapping

#### Project Names
PAI projects become Taskwarrior projects with clean mobile-friendly names:
- `bny` → `PAI-Customer-Bny`
- `cibc` → `PAI-Customer-Cibc`
- `discover` → `PAI-Customer-Discover`
- `tamlab-gpu` → `PAI-RedHat-TamlabGpu`
- `rh1` → `PAI-Personal-Rh1`

#### Task Descriptions
PAI tasks become descriptive Taskwarrior tasks:
```
PAI: project: cibc, task: Case 04245934, subtask: follow up with support
TW:  cibc: Case 04245934 → follow up with support
```

#### Tags and Metadata
- **Primary tag**: `pai` (identifies all PAI-originated tasks)
- **Project tag**: `pai-{project-name}` (e.g., `pai-cibc`)
- **Category tag**: `pai-customer`, `pai-redhat`, `pai-internal`, `pai-personal`
- **ID tag**: `pai-id-{task-id}` (maintains sync relationship)
- **Account attribute**: `account:999625` (for customer projects)

### Status Synchronization

#### PAI → Taskwarrior
| PAI Status | Taskwarrior Status | Additional Tags |
|------------|-------------------|-----------------|
| pending | pending | - |
| in-progress | pending | +ACTIVE |
| blocked | waiting | - |
| completed | completed | - |
| cancelled | deleted | - |

#### Taskwarrior → PAI
Changes made in Taskwarrior (including from mobile) sync back:
- **Completed tasks**: Auto-set completion date in PAI
- **Status changes**: Reflect mobile updates in PAI dashboard
- **Conflict resolution**: Taskwarrior status takes precedence

## Mobile Workflow

### Complete Task Flow
1. **Mobile Action**: Mark task complete in Google Tasks app
2. **Google → TW Sync**: Status syncs to Taskwarrior (≤15min)
3. **TW → PAI Sync**: Completion syncs to PAI (≤15min)
4. **PAI Dashboard**: Shows completed status with timestamp

### View Projects on Phone
Tasks appear in Google Tasks as organized project groups:
```
📱 Google Tasks - "To Do" List
├── PAI-Customer-Cibc
│   ├── Case 04245934 → follow up with support
│   ├── Case 04239021 → follow up with support
│   └── Dealservice application case
├── PAI-Customer-Discover
│   ├── Mahesh → architectural questions...
│   └── Mahesh → oc versioning follow up
└── PAI-RedHat-TamlabGpu
    └── IT-aligned Hardware Proposal → meet with Brian A.
```

## Configuration

### Automated Sync (Cron)
```bash
# Runs every 15 minutes
*/15 * * * * /home/grimm/.local/bin/pai-task-sync-cron >/dev/null 2>&1
```

### Sync Lock File
- **Location**: `/tmp/pai-task-sync.lock`
- **Purpose**: Prevents concurrent sync operations
- **Cleanup**: Automatic on process completion

### Logging
- **Sync Operations**: `~/.claude/context/logs/task-sync.log`
- **Cron Execution**: `~/.claude/context/logs/pai-task-sync-cron.log`
- **Error Tracking**: `~/.claude/context/logs/pai-task-sync-error.log`

## Integration Points

### PAI System Integration
- **Projects Data**: Uses PAI YAML structure
- **Audit System**: Integrates with PAI logging
- **Workflow**: Complements case management and calendar systems

### Taskwarrior Integration
- **Namespace**: Uses `PAI-*` project hierarchy
- **Tags**: Maintains `pai` tag family for identification
- **Compatibility**: Doesn't conflict with existing `work` tag system

### Google Tasks Integration
- **Passive Integration**: Works through existing Taskwarrior sync
- **List Compatibility**: Integrates with "To Do" list structure
- **Conflict Avoidance**: PAI namespace prevents task conflicts

## Troubleshooting

### Sync Not Working
```bash
# Check overall health
pai-task-sync-status

# Check if lock file is stuck
ls -la /tmp/pai-task-sync.lock

# Manual sync with error output
pai-task-sync bidirectional
```

### PAI Changes Not Appearing in Taskwarrior
```bash
# Force push from PAI
pai-task-sync push

# Check PAI data file
ls -la ~/.claude/context/create/outputs/projects/projects.yaml

# Verify PAI tasks in Taskwarrior
task list +pai
```

### Mobile Changes Not Updating PAI
```bash
# Check Google Tasks sync status
tail -f ~/.local/share/syncall/sync.log

# Force pull from Taskwarrior
pai-task-sync pull

# Verify Taskwarrior has updates
task list +pai status:completed
```

### Common Issues

#### Missing Tasks
- **Cause**: Sync timing or lock file issues
- **Solution**: Run `pai-task-sync bidirectional` manually

#### Duplicate Tasks
- **Cause**: Multiple sync attempts during development
- **Solution**: Use `task list +pai` to identify and `task {id} delete` duplicates

#### Status Conflicts
- **Cause**: Simultaneous updates on mobile and PAI
- **Solution**: Most recent change wins automatically

#### Permission Errors
- **Cause**: Log directory permissions
- **Solution**: `mkdir -p ~/.claude/context/logs && chmod 755 ~/.claude/context/logs`

## Advanced Usage

### Filtering PAI Tasks in Taskwarrior
```bash
# All PAI tasks
task list +pai

# PAI customer tasks only
task list +pai-customer

# Specific customer
task list project:PAI-Customer-Cibc

# High priority PAI tasks
task list +pai priority:H

# PAI tasks due soon
task list +pai due.before:tomorrow
```

### Bulk Operations
```bash
# Mark all PAI tasks for a project as done
task +pai-cibc modify status:completed

# Add due dates to customer tasks
task +pai-customer modify due:tomorrow

# Change priority for urgent items
task +pai project:PAI-Customer-Discover modify priority:H
```

## Security Considerations

### Data Privacy
- **Customer Data**: Account numbers included in Taskwarrior tasks
- **Mobile Sync**: Customer project names visible in Google Tasks
- **Audit Trail**: All sync operations logged with timestamps

### Access Control
- **Local Files**: PAI YAML files have standard user permissions
- **Sync Logs**: Audit logs accessible only to user account
- **Google Integration**: Uses existing OAuth authentication

### Best Practices
- **Regular Backups**: PAI YAML files should be backed up
- **Log Retention**: Monitor log file sizes for disk usage
- **Credential Security**: Don't share or commit sync configurations

## Performance

### Sync Timing
- **PAI → Taskwarrior**: ~2-5 seconds for 15 tasks
- **Status Updates**: Near-instantaneous for small changes
- **Full Sync Cycle**: Under 30 minutes worst case

### Resource Usage
- **Memory**: Minimal impact on system resources
- **CPU**: Brief spikes during sync operations only
- **Disk**: Logs rotate automatically, YAML files are small

### Scalability
- **Task Capacity**: Tested with 15 tasks, supports 100+ easily
- **Project Growth**: YAML structure scales well
- **Mobile Performance**: Google Tasks handles large lists efficiently

---

**Implementation**: 2025-09-17
**Status**: Production Active
**Automation**: ✅ 15-minute cron
**Mobile Ready**: ✅ Google Tasks integrated
**Customer Ready**: ✅ Account tracking active