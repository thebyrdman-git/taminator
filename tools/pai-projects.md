# pai-projects

## Purpose
TAM Non-Case Project Tracker for managing customer commitments, internal initiatives, and personal tasks with full mobile integration.

## Location
`~/.local/bin/pai-projects`

## Description
`pai-projects` provides comprehensive project and task management for TAM workflows that fall outside of formal case management. It organizes work by customer accounts, internal Red Hat initiatives, and personal tasks with priority tracking and mobile accessibility through Taskwarrior/Google Tasks integration.

## Key Features
- **Customer Project Tracking**: Links projects to specific customer account numbers
- **Multi-Category Organization**: Customer, Red Hat Internal, Personal
- **Priority Management**: High, Medium, Low priority levels with visual indicators
- **Status Tracking**: pending, in-progress, blocked, completed, cancelled
- **Mobile Integration**: Automatic sync to Google Tasks via Taskwarrior
- **Audit Logging**: All changes tracked for accountability

## Usage

### Basic Commands

```bash
# Main dashboard view
pai-projects summary

# List all project names
pai-projects list

# View specific project details
pai-projects project --project discover

# Show only high priority tasks
pai-projects priority

# Update task status
pai-projects update --project cibc --task-id cibc-001 --status completed
```

### Command Options

#### Global Options
- `-h, --help`: Show help message

#### project Command
- `--project, -p <name>`: Project name to display details

#### update Command
- `--project, -p <name>`: Project name
- `--task-id, -t <id>`: Task ID to update
- `--status, -s <status>`: New status (pending, in-progress, blocked, completed, cancelled)

### Examples

#### Dashboard Overview
```bash
pai-projects summary
```
**Output**:
```
🎯 TAM Project Dashboard
==================================================
📊 Overview: 9 projects | 4 high priority
   Customer: 3 | Internal: 5 | Personal: 1

🏢 Customer Projects
------------------------------
   🔥 CIBC (Account: 1460290)
      ⏳ Case 04245934 → follow up with support
      ⏳ Case 04239021 → follow up with support
```

#### Project Details
```bash
pai-projects project --project discover
```
**Output**:
```
📋 Project: DISCOVER
==================================================
Category: customer
Priority: high
Status: active
Account: 999625

Tasks:
--------------------
ID: discover-001
Task: Mahesh
Subtask: architectural questions about scaling up pre-upgrade
Status: pending
```

#### Priority View
```bash
pai-projects priority
```
**Output**:
```
🔥 High Priority Tasks
==============================
   • cibc: Case 04245934 → follow up with support
   • discover: Mahesh → architectural questions...
   • tamlab-gpu: IT-aligned Hardware Proposal → meet with Brian A.
```

#### Update Task Status
```bash
pai-projects update --project cibc --task-id cibc-001 --status completed
```
**Output**:
```
✅ Updated task cibc-001 status: pending → completed
```

## Data Structure

### Projects File Location
`~/.claude/context/create/outputs/projects/projects.yaml`

### Project Schema
```yaml
projects:
  project-name:
    category: "customer|redhat-internal|personal"
    account: "account-number"  # For customer projects
    priority: "high|medium|low"
    status: "active|paused|completed"
    tasks:
      - id: "unique-task-id"
        task: "main task description"
        subtask: "optional subtask detail"
        status: "pending|in-progress|blocked|completed|cancelled"
        created: "YYYY-MM-DD"
        due: "YYYY-MM-DD"  # Optional
        completed: "YYYY-MM-DD"  # Auto-set when completed
        notes: "optional notes"
```

### Current Project Categories

#### Customer Projects
- **BNY** (729650): Cadence management, meeting coordination
- **CIBC** (1460290): Case follow-ups, application issues
- **Discover** (999625): Architecture consultations, version management

#### Red Hat Internal
- **AI TAM Committee**: Landing page development
- **TAMlab GPU**: Hardware proposals and meetings
- **Security TAM Committee**: Quarterly security reviews
- **TAM General**: CoE research, content creation
- **rhcase**: Tool integration projects

#### Personal
- **RH1**: Administrative tasks like travel booking

## Mobile Integration

### Google Tasks Sync
PAI projects automatically sync to Google Tasks through Taskwarrior:

1. **PAI tasks** → Taskwarrior (15-minute cron)
2. **Taskwarrior** → Google Tasks (15-minute cron)
3. **Google Tasks** → Mobile app (real-time)

### Mobile Project Names
Projects appear in Google Tasks with clean namespacing:
- `PAI-Customer-Cibc`: CIBC customer tasks
- `PAI-Customer-Discover`: Discover customer tasks
- `PAI-RedHat-TamlabGpu`: Internal TAMlab GPU project
- `PAI-Personal-Rh1`: Personal administrative tasks

### Mobile Workflow
- **View**: Open Google Tasks app to see organized project groups
- **Complete**: Tap to mark tasks done on phone
- **Add**: Create new tasks (though PAI is preferred for project structure)
- **Sync**: Changes flow back to PAI within 30 minutes

## Integration with PAI Ecosystem

### TAM Workflow Enhancement
- **Customer Focus**: Account-linked project tracking
- **Priority Management**: High-priority customer commitments highlighted
- **Meeting Preparation**: Task lists accessible during customer calls
- **Follow-up Tracking**: Ensures customer commitments aren't forgotten

### Audit and Compliance
- **Change Logging**: All project updates logged with timestamps
- **Status History**: Track progress on customer commitments
- **Account Traceability**: Customer tasks linked to account numbers
- **Mobile Accountability**: Phone updates tracked back to PAI

## Commands Quick Reference

| Task | Command |
|------|---------|
| View dashboard | `pai-projects summary` |
| Project details | `pai-projects project -p PROJECTNAME` |
| High priority only | `pai-projects priority` |
| Mark task done | `pai-projects update -p PROJECT -t TASKID -s completed` |
| View in Taskwarrior | `task list project.startswith:PAI` |
| Manual sync | `pai-task-sync bidirectional` |
| Check sync health | `pai-task-sync-status` |

## Best Practices

### Task Organization
- **Use subtasks** for multi-step customer commitments
- **Set priorities** based on customer impact and urgency
- **Update status** regularly to maintain accuracy
- **Add notes** for context and next actions

### Customer Project Management
- **Link to accounts**: Always include customer account numbers
- **Track commitments**: Use tasks for promises made to customers
- **Follow up promptly**: Mobile access ensures timely responses
- **Document outcomes**: Update notes with results

### Mobile Usage
- **Review during travel**: Check commitments before customer meetings
- **Quick updates**: Mark progress during or after customer calls
- **Accessibility**: All projects available offline on phone
- **Sync awareness**: Changes may take up to 30 minutes to propagate

## Troubleshooting

### Sync Issues
```bash
pai-task-sync-status    # Check overall health
tail -f ~/.claude/context/logs/task-sync.log    # Watch PAI sync
tail -f ~/.local/share/syncall/sync.log         # Watch Google sync
```

### Common Problems
- **PAI not syncing**: Check `pai-task-sync-status` for errors
- **Google sync broken**: Re-authenticate with `rm ~/.config/syncall/token.json`
- **Mobile not updating**: Wait 30 minutes for full sync cycle
- **Duplicates**: Use `task list +pai` to identify and clean up

### Recovery Procedures
- **PAI corruption**: Restore from Git (YAML files are versioned)
- **Taskwarrior issues**: Rebuild from PAI with `pai-task-sync push`
- **Google auth expired**: Re-authenticate following setup guide
- **Lost mobile access**: Check Google Tasks app settings and re-sync

## Performance

### Current Scale
- **9 projects** with 15 total tasks
- **348 existing tasks** from Google Tasks
- **15-minute sync cycles** for timely updates
- **Sub-30-second** PAI dashboard generation

### Scalability
- Designed for 50+ projects and 500+ tasks
- YAML storage is lightweight and fast
- Taskwarrior handles thousands of tasks efficiently
- Google Tasks supports unlimited task creation

---

**Created**: 2025-09-17
**Status**: Production Active
**Mobile Ready**: ✅
**Auto-Sync**: ✅
**Integration**: Complete