# PAI Tools Directory

This directory contains documentation for all Personal AI (PAI) tools that integrate with the TAM workflow system.

## Email Tools

### [pai-email-cli](pai-email-cli.md)
Full-featured command-line email client using NeoMutt and Notmuch.
- Interactive email reading and management
- Powerful search and filtering
- Unix-style pipe operations
- Integration with gmailieer

### [pai-email-search](pai-email-search.md)
Command-line email search with powerful query syntax.
```bash
email-search "from:customer.com AND subject:urgent"
```

### [pai-email-cat](pai-email-cat.md)
Extract email content to stdout for Unix processing.
```bash
email-cat "subject:case" | grep "Case Number"
```

### [pai-email-summary](pai-email-summary.md)
Daily email statistics and summary generator.
```bash
email-summary  # Shows counts and recent emails
```

## Task Management

### [pai-gtasks](pai-gtasks.md)
Google Tasks bidirectional sync with Taskwarrior.
- Syncs "To Do" list with 'work' tag
- Automatic sync every 15 minutes
- Full Taskwarrior CLI features

## Calendar Tools

### [pai-calendar](pai-calendar.md)
Google Calendar integration for meeting preparation and daily planning.
- OAuth authentication with Google Workspace
- Meeting preparation with attendee research
- Daily calendar summaries

## Workspace Tools

### [pai-workspace](pai-workspace.md)
Case management and workspace organization for TAM workflows.
- Red Hat case integration
- Account-based organization
- Knowledge base management

## Workflow Tools

### [pai-my-plate-v2](pai-my-plate-v2.md)
Daily briefing and task aggregation tool.
- Combines email, calendar, and task summaries
- Morning routine automation
- Comprehensive daily overview

## Helper Scripts

### Quick Setup Scripts
- `~/.claude/context/config/email/quickstart-neomutt.sh` - Email CLI setup
- `~/.local/bin/gtasks-setup-helper` - Google Tasks setup

### Email Utilities
- `email-search` - Search emails from command line
- `email-cat` - Output email to stdout
- `email-summary` - Daily email statistics

### Sync Scripts
- `~/.local/bin/sync-work-tasks.sh` - Google Tasks sync
- `gmi sync` - Email sync (via gmailieer)

## Integration Map

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────────┐
│   Google        │────▶│     Local    │────▶│      CLI        │
│   Workspace     │     │    Storage   │     │     Tools       │
└─────────────────┘     └──────────────┘     └─────────────────┘
       │                       │                      │
       │                       │                      │
┌──────┴────────┐      ┌──────┴────────┐    ┌───────┴────────┐
│ • Gmail       │      │ • Maildir     │    │ • neomutt      │
│ • Calendar    │      │ • .ics files  │    │ • gcalcli      │
│ • Tasks       │      │ • Task DB     │    │ • taskwarrior  │
└───────────────┘      └───────────────┘    └────────────────┘
```

## Common Workflows

### Morning Routine
```bash
# 1. Check email summary
email-summary

# 2. Review calendar
pai-calendar summary

# 3. Check tasks
task next tag:work

# 4. Full daily briefing
pai-my-plate-v2
```

### Case Management
```bash
# Search case emails
email-search "case 04123456"

# Extract case details
email-cat "case 04123456" | grep -A10 "Description"

# Create task from case
task add "Review case 04123456" +work +case
```

### Meeting Preparation
```bash
# Find meeting invites
email-search "filename:.ics"

# Prepare for meeting
pai-calendar prep "Customer Sync"

# Extract attendee emails
email-cat "subject:meeting" | grep -o '<.*@.*>'
```

## Configuration Locations

- **Email**: `~/.config/neomutt/`, `~/.notmuch-config`
- **Tasks**: `~/.taskrc`, `~/.config/syncall/`
- **Calendar**: `~/.config/gcalcli/`
- **PAI System**: `~/.claude/context/`

## Security Notes

All tools use separate OAuth clients for security:
- Email: gmailieer OAuth client
- Calendar: gcalcli OAuth client  
- Tasks: syncall OAuth client (ID: 604570179581-*)

## Quick Reference Cards

- [Email Quick Reference](~/Desktop/cli-email-quickref.txt)
- [Taskwarrior Quick Reference](~/Desktop/taskwarrior-quick-ref.txt)
- [Google Tasks Setup](~/Desktop/google-tasks-quick-setup.txt)
