# pai-email-to-sso - Email to SSO Username Conversion Tool

## Overview
The `pai-email-to-sso` tool provides a focused stdin/stdout utility for converting email addresses to SSO usernames. It queries the Red Hat Hydra API to find the actual SSO username that should be used for portal integrations and user management.

## Core Purpose
This tool solves the critical problem where email addresses don't always match SSO usernames, especially for:
- **Red Hat employees**: `gvaughn@redhat.com` → `rhn-support-gvaughn`
- **External contacts**: Email format varies and must be looked up in Hydra API
- **Portal integration**: Exact username required for adding users to Red Hat portals

## Installation and Authentication

### Prerequisites
- Red Hat authentication credentials in environment variables:
  - `REDHAT_USERNAME` - Your Red Hat username
  - `REDHAT_PASSWORD` - Your Red Hat password
- Network access to Red Hat Hydra API

### Dependencies
- Python 3.6+ (uses only standard library)
- `requests` library for HTTP calls

## Usage Patterns

### Command Line Usage
```bash
# Single email lookup
pai-email-to-sso john.doe@company.com

# Output: john.doe@company.com
# (or rhn-support-jdoe for Red Hat employees)
```

### Stdin Processing (Primary Use Case)
```bash
# Process from file
cat email_list.txt | pai-email-to-sso

# Process with pipeline
echo "user@domain.com" | pai-email-to-sso

# Process and capture results
cat emails.txt | while read email; do
    sso=$(echo "$email" | pai-email-to-sso 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo "$email -> $sso"
    else
        echo "$email -> NOT_FOUND"
    fi
done
```

### Batch Processing Examples
```bash
# Generate username list for portal
cat cadence-invitees | pai-email-to-sso > portal-usernames.txt

# Process with error handling
cat contact_list.txt | pai-email-to-sso 2>errors.log > usernames.txt

# Filter only found usernames
cat emails.txt | pai-email-to-sso 2>/dev/null | grep -v "NOT_FOUND"
```

## Output Format

### Success Output (stdout)
Returns the exact SSO username as stored in the Hydra API:
- **External contacts**: Email address as stored in API (e.g., `john.doe@company.com`)
- **Red Hat employees**: Standard SSO format (e.g., `rhn-support-username`)

### Error Output (stderr + stdout)
When contact not found:
```
NOT_FOUND:email@domain.com
```
This format allows you to identify exactly which email addresses need portal accounts created.

### Exit Codes
- **0**: Contact found, SSO username returned
- **1**: Contact not found or error occurred

## API Behavior and Logic

### Lookup Process
1. **Search BNY Account (729650)** for the contact using `/v1/accounts/729650/contacts`
2. **Match email address** exactly (case-insensitive comparison)
3. **Extract username** from API response (prefers `username` field, falls back to `ssoUserName`)
4. **Return exact API value** - no modification or generation

### Red Hat Employee Handling
For `@redhat.com` addresses:
- Converts `gvaughn@redhat.com` → `rhn-support-gvaughn`
- Uses standard Red Hat SSO naming convention
- Bypasses external account search

### External Contact Handling
For non-Red Hat addresses:
- Searches Hydra API for actual contact record
- Returns email **exactly as stored in Hydra**
- Preserves case and domain format that works in portals
- Returns `NOT_FOUND:email` if contact doesn't exist

## Integration with PAI Workflow

### Portal User Management
```bash
# Generate portal invitation list
cat stakeholders.txt | pai-email-to-sso > portal_users.txt

# Identify missing portal accounts
cat emails.txt | pai-email-to-sso | grep "NOT_FOUND" | cut -d: -f2
```

### Contact Validation
```bash
# Verify all meeting invitees have portal access
cat meeting_invitees.txt | pai-email-to-sso | tee usernames.txt | wc -l
grep "NOT_FOUND" usernames.txt | wc -l
```

### Red Hat Team Identification
```bash
# Separate Red Hat vs external contacts
cat mixed_contacts.txt | pai-email-to-sso | grep "rhn-support-" > redhat_team.txt
cat mixed_contacts.txt | pai-email-to-sso | grep -v "rhn-support-\|NOT_FOUND" > external_contacts.txt
```

## Account Coverage

### TAM Account Numbers
The tool searches these primary TAM accounts:
- **729650** - BNY Mellon (primary for external contacts)
- **999625** - Discover Financial Services
- **1460290** - CIBC
- **1212328** - Citi

### Account Search Strategy
- **Single Account Focus**: Primarily searches BNY (729650) for performance
- **Contact Matching**: Exact email match in Hydra API contact records
- **API Response Preservation**: Returns exactly what Hydra provides

## Error Handling

### Common Scenarios

#### Contact Not Found
```bash
pai-email-to-sso nonexistent@company.com
# Output: NOT_FOUND:nonexistent@company.com
# Exit code: 1
```

#### Authentication Issues
```bash
# Missing credentials
pai-email-to-sso user@domain.com
# Error: Missing REDHAT_USERNAME or REDHAT_PASSWORD
```

#### API Connectivity Issues
- Network timeouts: 15-second timeout per API call
- Authentication failures: Clear error messages
- API errors: HTTP status codes and response details

### Troubleshooting Commands
```bash
# Test authentication
env | grep REDHAT_

# Test API connectivity
curl -s -u "$REDHAT_USERNAME:$REDHAT_PASSWORD" \
  "https://access.redhat.com/hydra/rest/v1/businesshours?timezone=UTC"

# Verify account access
pai-hydra contacts 729650 | head -5
```

## Performance Characteristics

### Speed Considerations
- **Single API call** per email lookup
- **15-second timeout** per request
- **Sequential processing** (no parallel API calls)
- **Estimated time**: ~3-5 seconds per email lookup

### Optimization for Batch Processing
```bash
# For large lists, consider processing in chunks
split -l 10 large_email_list.txt chunk_
for chunk in chunk_*; do
    cat "$chunk" | pai-email-to-sso >> all_results.txt 2>>all_errors.log
    sleep 5  # Rate limiting
done
```

## Security and Compliance

### Authentication Security
- **Environment variables only**: No credential storage in files
- **Basic auth over HTTPS**: Secure credential transmission
- **No credential caching**: Fresh authentication for each execution

### Data Handling
- **Read-only operations**: Only queries existing data
- **Minimal data exposure**: Returns only SSO username
- **Audit integration**: All lookups logged via PAI audit system
- **Privacy compliance**: No persistent storage of contact data

### Audit Trail
Every lookup generates audit log entries:
- **Timestamp**: When lookup occurred
- **Action**: Type of lookup performed
- **Target**: Email address searched
- **Result**: Success/failure status

## Real-World Use Cases

### Portal User Management
**Scenario**: Adding customer contacts to Red Hat Customer Portal
```bash
# Process meeting attendee list
cat quarterly_review_attendees.txt | pai-email-to-sso > portal_usernames.txt

# Identify who needs portal accounts
grep "NOT_FOUND" portal_usernames.txt | cut -d: -f2 > needs_portal_accounts.txt
```

### Case Collaboration
**Scenario**: Identifying stakeholders for case escalation
```bash
# Find SSO usernames for case notification list
pai-hydra case 04245934 | grep -o "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" | \
  pai-email-to-sso > case_stakeholder_ssos.txt
```

### Strategic Account Management
**Scenario**: Creating contact groups for account management
```bash
# Process strategic contact list
cat strategic_contacts_bny.txt | pai-email-to-sso | \
  grep -v "NOT_FOUND" > confirmed_bny_portal_users.txt

# Generate invitation list
grep "NOT_FOUND" strategic_contacts_bny.txt | \
  cut -d: -f2 > invite_to_portal.txt
```

## Tool Philosophy

### Design Principles
- **Single purpose**: Email to SSO username conversion only
- **Stdin/stdout**: Perfect for shell pipelines and automation
- **API accuracy**: Returns exactly what Hydra API provides
- **Error clarity**: Clear indication of which emails need attention
- **Integration friendly**: Works seamlessly with other PAI tools

### Workflow Integration
This tool bridges the gap between human-readable email addresses and system-required SSO usernames, enabling seamless integration between contact management, portal administration, and case collaboration workflows.

The tool embodies the PAI principle of augmenting human capability - it handles the tedious API lookups automatically while providing exactly the information needed for the next step in your workflow.