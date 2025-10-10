# pai-email-summary

Daily email statistics and summary generator for TAM workflows.

## Location
`~/.local/bin/email-summary`

## Description
Provides a quick overview of email statistics including counts, recent emails, and daily activity. Perfect for morning routines and status checks.

## Usage
```bash
email-summary
```

## Output Example
```
=== Email Summary ===
Total emails: 15,234
Unread: 42
Today: 18
This week: 127

=== Recent Emails ===
today     | John Doe <john@example.com> | Re: Case 04123456 - Urgent
today     | Alert System | Production Alert: Node Down
yesterday | Jane Smith | Meeting notes from sync
...
```

## Daily Workflow Integration

### Morning Routine
```bash
# Add to daily startup script
morning_briefing() {
  echo "=== Good morning! ==="
  date
  echo
  email-summary
  echo
  task list tag:work due:today
  echo
  gcalcli agenda
}
```

### Email Metrics
```bash
# Extended summary with trends
email_metrics() {
  echo "=== Email Metrics ==="
  echo "Today: $(notmuch count date:today)"
  echo "Yesterday: $(notmuch count date:yesterday)"
  echo "This week: $(notmuch count date:7d..)"
  echo "Last week: $(notmuch count date:14d..7d)"
  echo
  echo "=== By Status ==="
  echo "Unread: $(notmuch count tag:unread)"
  echo "Flagged: $(notmuch count tag:flagged)"
  echo "Archived: $(notmuch count tag:archive)"
}
```

### Account-Specific Summaries
```bash
# Summary by customer account
customer_email_summary() {
  for domain in "cibc.com" "bny.com" "discover.com" "citi.com"; do
    echo "$domain: $(notmuch count from:$domain OR to:$domain)"
  done
}

# Red Hat internal summary
internal_summary() {
  echo "=== Red Hat Internal ==="
  echo "From TAMs: $(notmuch count from:tam-list@redhat.com)"
  echo "From Support: $(notmuch count from:support@redhat.com)"
  echo "From Management: $(notmuch count from:manager@redhat.com)"
}
```

## Customization

### Add to ~/.bashrc
```bash
# Enhanced email summary function
email_summary_enhanced() {
  email-summary
  echo
  echo "=== Top Senders Today ==="
  notmuch search --output=messages date:today | \
    xargs -I{} notmuch show --format=json {} | \
    jq -r '.[][][0].headers.From' | \
    grep -o '<.*>' | tr -d '<>' | \
    sort | uniq -c | sort -nr | head -5
  echo
  echo "=== Urgent/Flagged ==="
  notmuch search tag:flagged AND tag:unread | head -5
}
```

### Time-based Summaries
```bash
# Hourly email rate
hourly_email_rate() {
  for hour in {00..23}; do
    count=$(notmuch count "date:today AND date:${hour}:00..${hour}:59")
    printf "%s:00 - %3d emails\n" "$hour" "$count"
  done | grep -v " 0 emails"
}

# Weekly summary
weekly_summary() {
  for i in {0..6}; do
    date=$(date -d "$i days ago" +%Y-%m-%d)
    count=$(notmuch count date:$date)
    printf "%s: %4d emails\n" "$date" "$count"
  done
}
```

## Integration Examples

### With pai-gtasks
```bash
# Summary with pending email tasks
email_task_summary() {
  email-summary
  echo
  echo "=== Email Tasks ==="
  task list tag:email status:pending | head -10
}
```

### With pai-calendar
```bash
# Summary with meeting invites
meeting_email_summary() {
  email-summary
  echo
  echo "=== Meeting Invitations ==="
  notmuch search filename:.ics date:7d.. | head -5
}
```

### With pai-workspace
```bash
# Case-related email summary
case_email_summary() {
  email-summary
  echo
  echo "=== Case-Related Emails ==="
  notmuch search "case" date:7d.. | grep -o "Case [0-9]\+" | sort | uniq -c
}
```

## Automation

### Cron Job for Daily Report
```bash
# Add to crontab
0 8 * * * /home/grimm/.local/bin/email-summary > /home/grimm/tmp/daily-email-$(date +\%Y\%m\%d).txt
```

### Slack/Chat Integration
```bash
# Post summary to chat
post_email_summary() {
  local summary=$(email-summary | sed ':a;N;$!ba;s/\n/\\n/g')
  curl -X POST -H 'Content-type: application/json' \
    --data "{\"text\":\"$summary\"}" \
    "$SLACK_WEBHOOK_URL"
}
```

### Email Report Generator
```bash
# Generate weekly email report
generate_email_report() {
  local report_file="/tmp/email-report-$(date +%Y%m%d).txt"
  {
    echo "Weekly Email Report - $(date)"
    echo "================================"
    echo
    weekly_summary
    echo
    echo "Top Senders:"
    notmuch search --output=messages date:7d.. | \
      xargs -I{} notmuch show --format=json {} | \
      jq -r '.[][][0].headers.From' | \
      sort | uniq -c | sort -nr | head -20
    echo
    echo "Important Threads:"
    notmuch search tag:important date:7d..
  } > "$report_file"
  
  echo "Report saved to: $report_file"
}
```

## Output Format
- Statistics section with counts
- Recent emails with relative date, sender, and subject
- Sorted by date (newest first)
- Limited to 10 recent emails for readability

## Tips
- Run first thing in the morning for daily overview
- Combine with other tools for comprehensive status
- Customize output by editing the script
- Use with `watch` for real-time monitoring: `watch -n 300 email-summary`

## See Also
- [pai-email-search](pai-email-search.md) - Search emails
- [pai-email-cat](pai-email-cat.md) - Extract email content
- [pai-email-cli](pai-email-cli.md) - Full email client
- [pai-my-plate-v2](pai-my-plate-v2.md) - Daily briefing tool
