# pai-email-cat

Extract email content to stdout for Unix-style processing.

## Location
`~/.local/bin/email-cat`

## Description
Outputs the raw content of the first email matching a search query to stdout. Perfect for piping, grepping, and Unix-style text processing.

## Usage
```bash
email-cat <search-query>
```

## Examples

### Basic Usage
```bash
# Output email to terminal
email-cat "subject:urgent"

# Save email to file
email-cat "from:john@example.com" > email.txt

# View in pager
email-cat "subject:report" | less
```

### Extract Specific Parts
```bash
# Get subject line
email-cat "from:customer" | grep "^Subject:" | cut -d: -f2-

# Get sender
email-cat "tag:unread" | grep "^From:" | sed 's/.*<\(.*\)>.*/\1/'

# Get date
email-cat "subject:meeting" | grep "^Date:"

# Get message body (skip headers)
email-cat "from:boss" | sed '1,/^$/d'
```

### Search Email Content
```bash
# Find URLs in email
email-cat "subject:newsletter" | grep -o 'https://[^"]*'

# Find email addresses
email-cat "subject:contact" | grep -o '[a-zA-Z0-9._%+-]\+@[a-zA-Z0-9.-]\+\.[a-zA-Z]\{2,\}'

# Find case numbers
email-cat "from:support" | grep -o "[Cc]ase.* [0-9]\{8\}"

# Find phone numbers
email-cat "subject:contact" | grep -E '\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
```

### TAM Workflow Examples
```bash
# Extract case details
extract_case_info() {
  local case_num="$1"
  email-cat "case $case_num" | grep -E "Subject:|From:|Date:|[Cc]ase.* [0-9]"
}

# Get customer email from case
get_customer_email() {
  local case_num="$1"
  email-cat "case $case_num" | grep "^From:" | grep -o '<.*>' | tr -d '<>'
}

# Extract meeting details
get_meeting_time() {
  email-cat "subject:meeting invitation" | grep -A5 "When:"
}
```

### Processing Attachments
```bash
# Check for attachments
email-cat "from:vendor" | grep -c "Content-Disposition: attachment"

# Extract attachment names
email-cat "has:attachment" | grep "filename=" | sed 's/.*filename="\([^"]*\)".*/\1/'

# Extract base64 content
email-cat "subject:document" | sed -n '/^Content-Transfer-Encoding: base64/,/^--/p'
```

### Integration Examples

#### Create Task from Email
```bash
# Extract and create task
email_to_task() {
  local query="$1"
  local subject=$(email-cat "$query" | grep "^Subject:" | cut -d: -f2- | xargs)
  local from=$(email-cat "$query" | grep "^From:" | grep -o '<.*>' | tr -d '<>')
  
  echo "Creating task: $subject from $from"
  task add "Email: $subject" +email +work annotate "From: $from"
}
```

#### Generate Email Summary
```bash
# Quick email summary
email_summary() {
  local query="$1"
  echo "=== Email Summary ==="
  email-cat "$query" | grep -E "^(From|Subject|Date):"
  echo "=== Preview ==="
  email-cat "$query" | sed '1,/^$/d' | head -10
}
```

#### Extract Action Items
```bash
# Find action items in email
find_actions() {
  email-cat "$1" | \
    grep -i -E "(action|todo|task|please|need|required|must|should):" | \
    sed 's/^[ \t]*/- /'
}
```

## Output Format
Raw email format (RFC 2822) including:
- Headers (From, To, Subject, Date, etc.)
- Blank line separator
- Body (plain text or MIME encoded)
- Attachments (MIME encoded)

## Common Patterns

### Email Headers
```bash
From: sender@example.com
To: recipient@example.com
Subject: Email subject line
Date: Mon, 10 Sep 2025 10:30:00 -0500
Message-ID: <unique-id@example.com>
```

### MIME Boundaries
```bash
--===============1234567890==
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: 7bit
```

## Tips
- First matching email is returned (use `email-search` to preview)
- Pipe to `head -50` to see just headers and beginning
- Use `| sed '1,/^$/d'` to skip headers
- Combine with other Unix tools for powerful processing

## Error Handling
```bash
# Check if email exists
if email-cat "subject:nonexistent" 2>/dev/null | grep -q "Subject:"; then
  echo "Email found"
else
  echo "No email matching query"
fi
```

## See Also
- [pai-email-search](pai-email-search.md) - Search emails
- [pai-email-summary](pai-email-summary.md) - Email statistics
- [pai-email-cli](pai-email-cli.md) - Full email client
