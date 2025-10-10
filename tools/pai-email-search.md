# pai-email-search

Command-line email search tool using notmuch for fast, powerful email queries.

## Location
`~/.local/bin/email-search`

## Description
Search Red Hat workspace emails from the command line with powerful query syntax. Returns formatted results with counts.

## Usage
```bash
email-search <search-query>
```

## Examples

### Basic Searches
```bash
# Search by sender
email-search "from:john.doe@redhat.com"
email-search "from:customer.com"

# Search by subject
email-search "subject:urgent"
email-search "subject:'case 04123456'"

# Search by date
email-search "date:today"
email-search "date:yesterday"
email-search "date:7d.."        # Last 7 days
email-search "date:2025-09-01..2025-09-10"

# Search by status
email-search "tag:unread"
email-search "tag:flagged"
email-search "is:unread"       # Alias for tag:unread
```

### Advanced Searches
```bash
# Combine criteria with AND
email-search "from:redhat.com AND subject:case AND date:30d.."

# Use OR for alternatives
email-search "from:customer1.com OR from:customer2.com"

# Exclude with NOT
email-search "tag:unread AND NOT from:noreply"

# Complex queries with parentheses
email-search "(from:cibc.com OR from:bny.com) AND subject:escalation"

# Search with attachments
email-search "has:attachment AND from:customer.com"
email-search "filename:pdf AND date:week.."
```

### TAM-Specific Searches
```bash
# Find case-related emails
email-search "case 04123456"
email-search "subject:case AND tag:unread"

# Find escalations
email-search "subject:escalation OR subject:urgent"

# Find by account
email-search "from:@bankofny.com OR to:@bankofny.com"

# Find meeting invites
email-search "filename:.ics"

# Find from specific Red Hat teams
email-search "from:tam-list@redhat.com"
email-search "from:support@redhat.com"
```

## Search Syntax Reference

### Fields
- `from:` - Sender email or domain
- `to:` - Recipient email or domain  
- `subject:` - Email subject line
- `date:` - Date ranges
- `tag:` - Email tags/labels
- `folder:` - Gmail folder/label
- `filename:` - Attachment filename
- `body:` - Search in email body

### Date Formats
- `today`, `yesterday`
- `7d..` - Last 7 days
- `..7d` - Older than 7 days
- `week`, `month`, `year`
- `2025-09-01..2025-09-10` - Date range

### Operators
- `AND` - Both conditions (default)
- `OR` - Either condition
- `NOT` - Exclude condition
- `()` - Group conditions

## Integration with Other Tools

### Pipe to Task Creation
```bash
# Create tasks from search results
email-search "tag:flagged" | \
  awk -F' -- ' '{print $2}' | \
  xargs -I{} task add "Review: {}" +email

# Create task from specific email
email-search "from:customer subject:urgent" | \
  head -1 | \
  awk -F' -- ' '{print "task add \"" $2 "\" +email priority:H"}' | \
  bash
```

### Export Results
```bash
# Export to CSV
email-search "date:month.." | \
  awk -F' -- ' '{print "\"" $1 "\",\"" $2 "\""}' > emails.csv

# Count by sender
email-search '*' | \
  awk '{print $3}' | \
  sort | uniq -c | sort -nr
```

### Archive Operations
```bash
# Find and archive old emails
email-search "date:..90d" | \
  awk '{print $1}' | \
  xargs -I{} notmuch tag +archive -inbox -- {}
```

## Output Format
```
=== Email Search Results ===
thread:0000000000012345   2025-09-10 [1/1] John Doe; Important Subject (inbox unread)
thread:0000000000012346   2025-09-09 [3/3] Jane Smith; Re: Case 04123456 (inbox)
...

Total matches: 42
```

## Tips
- Use quotes for multi-word searches: `"subject:urgent case"`
- Wildcards supported: `from:*@redhat.com`
- Case insensitive by default
- Results limited to 20 for readability (edit script to change)

## See Also
- [pai-email-cat](pai-email-cat.md) - Extract email content
- [pai-email-summary](pai-email-summary.md) - Email statistics
- [pai-email-cli](pai-email-cli.md) - Full email client
