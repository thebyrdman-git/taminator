# pai-email-cli

Command-line email management using NeoMutt and Notmuch for TAM workflows.

## Location
- **Helper Scripts**: `~/.local/bin/email-*`
- **Email Client**: `neomutt`
- **Search Engine**: `notmuch`
- **Configuration**: `~/.config/neomutt/neomuttrc`

## Description
Provides powerful CLI-based email management with Unix-style operations, search, and processing capabilities. Works with existing gmailieer setup for Red Hat workspace email.

## Setup
```bash
# One-time setup
~/.claude/context/config/email/quickstart-neomutt.sh

# Manual setup:
sudo dnf install -y neomutt notmuch notmuch-mutt urlview w3m
notmuch setup  # Point to ~/.claude/context/capture/email/gmail-gvaughn/mail
notmuch new    # Initial index
```

## Daily Workflow Integration

### Email Management
```bash
# Sync and open email
mutt  # Alias that syncs with gmailieer first

# Quick email summary
email-summary

# Search from command line
email-search "from:customer.com"
email-search "subject:case AND date:7d.."
email-search "tag:unread AND tag:important"

# Extract email to stdout
email-cat "subject:urgent" | grep -i "deadline"
email-cat "from:john" > ~/tmp/john-email.txt
```

### Unix-Style Operations
```bash
# Count emails by sender
notmuch search --output=messages '*' | \
  xargs -I{} notmuch show --format=json {} | \
  jq -r '.[][][0].headers.From' | sort | uniq -c | sort -nr

# Extract all URLs from today's emails
notmuch search --output=files date:today | \
  xargs grep -ho 'https://[^"]*' | sort -u

# Find case numbers in emails
notmuch search --output=files "case" | \
  xargs grep -ho "[Cc]ase.* [0-9]\{8\}" | sort -u

# Export emails matching criteria
notmuch show --format=mbox tag:important > important.mbox
```

## Commands

### Helper Scripts
- `email-summary` - Show email statistics and recent emails
- `email-search <query>` - Search emails with summary
- `email-cat <query>` - Output first matching email to stdout
- `mutt` - Sync and open NeoMutt (alias)

### Notmuch Search Syntax
```bash
# Basic searches
from:user@example.com
to:me@example.com
subject:"important topic"
date:today
date:yesterday
date:7d..  # Last 7 days
tag:unread
tag:flagged

# Complex searches
from:redhat.com AND subject:case AND date:30d..
tag:unread AND NOT from:noreply
(from:customer1.com OR from:customer2.com) AND tag:important
```

### NeoMutt Key Bindings
- `/` - Search emails
- `Enter` - Open email
- `q` - Quit
- `r` - Reply
- `f` - Forward
- `d` - Delete/Archive
- `s` - Save message
- `|` - Pipe to command
- `Ctrl+O` - Save to /tmp/email.txt
- `Ctrl+U` - Extract URLs
- `?` - Help

## Email Processing Features

### Task Creation
```bash
# Function for ~/.bashrc
email2task() {
  local query="$1"
  local subject=$(email-cat "$query" | grep "^Subject:" | cut -d: -f2-)
  local from=$(email-cat "$query" | grep "^From:" | sed 's/.*<\(.*\)>.*/\1/')
  task add "Email from $from: $subject" +email +work
}

# Usage
email2task "subject:urgent"
```

### Case Analysis
```bash
# Extract case-related emails
case_emails() {
  local case_num="$1"
  notmuch search --output=files "case $case_num" | \
    xargs -I{} cp {} ~/tmp/case-$case_num/
}

# Get case timeline
case_timeline() {
  local case_num="$1"
  notmuch search --format=json "case $case_num" | \
    jq -r '.[] | "\(.date_relative) | \(.authors) | \(.subject)"' | \
    sort
}
```

### Meeting Extraction
```bash
# Find calendar invites
notmuch search --output=files has:attachment filename:.ics | \
  while read email; do
    munpack -C /tmp "$email" 2>/dev/null
  done
gcalcli import /tmp/*.ics

# Extract meeting details
meeting_info() {
  notmuch search --output=files "meeting AND has:attachment" | \
    xargs grep -h "SUMMARY:\|DTSTART:\|LOCATION:"
}
```

## Integration Points

### With pai-gtasks
```bash
# Convert flagged emails to tasks
notmuch search --format=json tag:flagged AND tag:unread | \
  jq -r '.[] | "task add \"Email: \(.subject)\" +email +work due:tomorrow"' | \
  bash

# Email tasks sync with Google Tasks via taskwarrior
```

### With pai-calendar
```bash
# Extract meeting requests
notmuch search --output=files filename:.ics date:7d.. | \
  xargs -I{} sh -c 'munpack -C /tmp {} && gcalcli import /tmp/*.ics'
```

### With pai-workspace
```bash
# Link emails to cases
link_email_to_case() {
  local email_id="$1"
  local case_num="$2"
  notmuch tag +case-$case_num -- id:$email_id
}

# Search by account
notmuch search from:@bankofny.com OR to:@bankofny.com
```

## Output Formats

### JSON Export
```bash
# Export email metadata as JSON
notmuch show --format=json "from:important.com" | \
  jq '.[] | {
    subject: .[0][0].headers.Subject,
    from: .[0][0].headers.From,
    date: .[0][0].headers.Date,
    id: .[0][0].id
  }'
```

### CSV Export
```bash
# Export email list as CSV
notmuch search --format=json '*' | \
  jq -r '.[] | [.date_relative, .authors, .subject] | @csv' > emails.csv
```

### Plain Text Reports
```bash
# Daily email report
daily_email_report() {
  echo "=== Email Report for $(date +%Y-%m-%d) ==="
  echo "Total: $(notmuch count '*')"
  echo "Unread: $(notmuch count tag:unread)"
  echo "Today: $(notmuch count date:today)"
  echo
  echo "=== By Sender ==="
  notmuch search --output=messages date:today | \
    xargs -I{} notmuch show --format=json {} | \
    jq -r '.[][][0].headers.From' | sort | uniq -c | sort -nr | head -10
}
```

## Advanced Features

### Email Threading
```bash
# Show full thread
notmuch show --entire-thread=true "subject:discussion"

# Thread statistics
thread_stats() {
  notmuch search --output=threads "$@" | \
    xargs -I{} sh -c 'echo -n "{}: "; notmuch count {}'
}
```

### Attachment Handling
```bash
# Find large attachments
find ~/.claude/context/capture/email/gmail-gvaughn/mail -size +5M -name "*.pdf"

# Extract all attachments
extract_attachments() {
  local output_dir="${1:-/tmp/attachments}"
  mkdir -p "$output_dir"
  notmuch search --output=files has:attachment | \
    xargs -I{} munpack -C "$output_dir" {}
}
```

### Email Backup
```bash
# Backup important emails
notmuch show --format=mbox tag:important OR tag:archive > \
  ~/backup/emails-$(date +%Y%m%d).mbox

# Incremental backup
notmuch search --output=files date:yesterday.. | \
  tar -czf ~/backup/emails-incremental-$(date +%Y%m%d).tar.gz -T -
```

## Security and Privacy
- All email remains local after gmailieer sync
- Search operations are performed locally
- No data sent to external services
- OAuth tokens managed by gmailieer

## Troubleshooting

### Common Issues
```bash
# Reindex if search not working
notmuch new --verbose

# Check database integrity
notmuch compact

# Fix sync issues
cd ~/.claude/context/capture/email/gmail-gvaughn
gmi sync --force

# Clear search cache
notmuch reindex '*'
```

### Performance Tuning
```bash
# Optimize database
notmuch compact --backup=/tmp/notmuch.backup

# Exclude large folders
echo "search.exclude_tags=spam;trash;deleted" >> ~/.notmuch-config
```

## Requirements
- gmailieer (already configured)
- neomutt
- notmuch
- jq (for JSON processing)
- urlview or extract_url
- w3m or lynx (for HTML email)
