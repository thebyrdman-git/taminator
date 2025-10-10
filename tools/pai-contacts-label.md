# pai-contacts-label - Google Workspace Contact Labeling Tool

## Overview
The `pai-contacts-label` tool provides automated labeling capabilities for Google Workspace contacts using the Google People API. It enables batch processing of contact lists to apply organizational labels for improved contact management and workflow automation.

## Installation and Setup

### Prerequisites
- Google Cloud Project with People API and Contacts API enabled
- OAuth 2.0 credentials (Desktop application type)
- Python Google API libraries:
  ```bash
  pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
  ```

### Authentication Setup
1. **OAuth Credentials**: Place your `client_secret_*.json` file in `~/.claude/context/secrets/`
2. **First Run**: Tool opens browser for OAuth authorization automatically
3. **Token Storage**: Saves token to `~/.claude/context/secrets/google-contacts-token.json`
4. **Subsequent Runs**: Uses stored token automatically

### Required Google API Scopes
- `https://www.googleapis.com/auth/contacts` - Full contacts read/write access

## Core Functionality

### Single Contact Labeling
```bash
# Add single contact to label
pai-contacts-label --label "TAM-BNY" john.doe@company.com

# Example output:
# Processing: john.doe@company.com
# SUCCESS: Added john.doe@company.com to label 'TAM-BNY'
# LABELED: john.doe@company.com
```

### Batch Processing from Stdin
```bash
# Process email list from file
cat email_list.txt | pai-contacts-label --label "TAM-BNY"

# Process with pipeline
echo "user@domain.com" | pai-contacts-label --label "Strategic-Contacts"

# Example output:
# Processing: user1@domain.com
# SUCCESS: Added user1@domain.com to label 'TAM-BNY'
# Processing: user2@domain.com
# ERROR: Contact not found for user2@domain.com
# LABELED: user1@domain.com
# FAILED: user2@domain.com
# Summary: 1 successful, 1 failed
```

### Multiple Label Application
```bash
# Apply multiple labels to contacts
cat strategic_contacts.txt | pai-contacts-label --label "TAM-BNY" --label "Strategic" --label "OpenShift"

# Each contact gets all specified labels
```

## Advanced Usage Patterns

### TAM Workflow Integration
```bash
# Label customer contacts by account
cat bny_contacts.txt | pai-contacts-label --label "Customer-BNY"
cat cibc_contacts.txt | pai-contacts-label --label "Customer-CIBC"

# Label by role
grep "@redhat.com" team_list.txt | pai-contacts-label --label "TAM-Team"
grep -v "@redhat.com" team_list.txt | pai-contacts-label --label "Customer-Contacts"

# Label by engagement type
cat strategic_contacts.txt | pai-contacts-label --label "Strategic-Account"
cat escalation_contacts.txt | pai-contacts-label --label "Escalation-List"
```

### Contact Organization
```bash
# Project-based labeling
cat project_stakeholders.txt | pai-contacts-label --label "Project-Migration"

# Event-based labeling
cat meeting_attendees.txt | pai-contacts-label --label "Quarterly-Review-2025"

# Technology-based labeling
cat openshift_users.txt | pai-contacts-label --label "OpenShift-Users"
```

### Pipeline Processing with Error Handling
```bash
# Process with separate success/failure handling
cat contact_list.txt | pai-contacts-label --label "New-Label" 2>errors.log | \
  grep "LABELED" > successful_labels.txt

# Count results
echo "Successful: $(wc -l < successful_labels.txt)"
echo "Failed: $(grep "FAILED" errors.log | wc -l)"
```

## Label Management

### Automatic Label Creation
- **Auto-creation**: Labels are created automatically if they don't exist
- **Naming**: Use descriptive names like "TAM-BNY", "Strategic-Contacts", "Project-Alpha"
- **Organization**: Consider hierarchical naming (e.g., "TAM-BNY-Strategic", "TAM-CIBC-Technical")

### Label Strategy Best Practices
```bash
# Account-based labels
--label "Customer-BNY"
--label "Customer-CIBC"
--label "Customer-Discover"

# Role-based labels
--label "TAM-Team"
--label "Customer-Technical"
--label "Customer-Business"

# Engagement-based labels
--label "Strategic-Account"
--label "Escalation-Contacts"
--label "Executive-Stakeholders"

# Project-based labels
--label "Migration-Project"
--label "Upgrade-Planning"
--label "Performance-Review"
```

## Output Format and Processing

### Standard Output Format
- **Progress messages**: Sent to stderr (`Processing: email@domain.com`)
- **Success results**: Sent to stdout (`LABELED: email@domain.com`)
- **Failure results**: Sent to stdout (`FAILED: email@domain.com`)
- **Summary**: Sent to stderr (`Summary: X successful, Y failed`)

### Exit Codes
- **0**: All contacts successfully labeled
- **1**: One or more contacts failed to be labeled

### Pipeline-Friendly Design
```bash
# Extract only successful labelings
cat contacts.txt | pai-contacts-label --label "Test" | grep "LABELED"

# Extract only failures for follow-up
cat contacts.txt | pai-contacts-label --label "Test" | grep "FAILED"

# Count successful operations
cat contacts.txt | pai-contacts-label --label "Test" | grep "LABELED" | wc -l
```

## Error Handling

### Contact Not Found
```bash
pai-contacts-label --label "Test" nonexistent@example.com
# Output: FAILED: nonexistent@example.com
# Stderr: ERROR: Contact not found for nonexistent@example.com
```

### Authentication Issues
```bash
# Missing OAuth setup
pai-contacts-label --label "Test" user@domain.com
# Error: Google OAuth credentials file not found
# Expected location: ~/.claude/context/secrets/google-contacts-credentials.json
```

### API Quota/Rate Limiting
- **Built-in timeouts**: 10-second timeout per API call
- **Retry logic**: Automatically retries failed requests once
- **Rate limiting**: No built-in rate limiting (Google API handles this)

### Permission Issues
```bash
# Insufficient OAuth scopes
# Error: Failed to create/find contact group 'Label': insufficient permissions
```

## Google Workspace Integration

### Contact Group Management
- **Automatic creation**: Contact groups (labels) created if they don't exist
- **Membership management**: Adds contacts to existing groups
- **Duplicate handling**: Safe to run multiple times (won't create duplicates)

### API Endpoints Used
- `people().searchContacts()` - Find contacts by email
- `contactGroups().list()` - List existing contact groups
- `contactGroups().create()` - Create new contact groups
- `contactGroups().members().modify()` - Add contacts to groups

### OAuth Scope Requirements
```json
{
  "scopes": [
    "https://www.googleapis.com/auth/contacts"
  ]
}
```

## Real-World Use Cases

### Strategic Account Management
```bash
# Label all BNY strategic contacts
cat bny_strategic_contacts.txt | pai-contacts-label --label "Strategic-BNY"

# Label quarterly review attendees
cat q4_review_attendees.txt | pai-contacts-label --label "Q4-Review-2025"
```

### Project Stakeholder Management
```bash
# Label migration project stakeholders
cat migration_stakeholders.txt | pai-contacts-label --label "Migration-Project" --label "Technical-Contacts"

# Label by customer and engagement type
cat bny_technical_team.txt | pai-contacts-label --label "Customer-BNY" --label "Technical-Team"
```

### Event and Meeting Management
```bash
# Label conference attendees
cat red_hat_summit_contacts.txt | pai-contacts-label --label "Summit-2025"

# Label webinar participants
cat webinar_registrants.txt | pai-contacts-label --label "OpenShift-Webinar"
```

### Contact Segmentation
```bash
# Segment by role
grep "engineer\|architect" contacts.txt | pai-contacts-label --label "Technical-Contacts"
grep "manager\|director" contacts.txt | pai-contacts-label --label "Business-Contacts"

# Segment by company domain
grep "@bny.com" all_contacts.txt | pai-contacts-label --label "BNY-Contacts"
grep "@redhat.com" all_contacts.txt | pai-contacts-label --label "Red-Hat-Team"
```

## Troubleshooting

### OAuth Issues
```bash
# Re-run OAuth flow (delete token file)
rm ~/.claude/context/secrets/google-contacts-token.json
pai-contacts-label --label "Test" test@example.com
# Will trigger new OAuth flow
```

### API Quota Issues
- Google Contacts API has generous quotas for normal use
- If hitting limits, add delays between batch operations
- Monitor Google Cloud Console for quota usage

### Contact Matching Issues
- Tool uses exact email matching (case-insensitive)
- Contacts must exist in your Google Workspace
- Shared contacts vs. personal contacts may affect visibility

## Configuration and Customization

### Credential Locations
- **OAuth credentials**: `~/.claude/context/secrets/client_secret_*.json`
- **Access token**: `~/.claude/context/secrets/google-contacts-token.json`

### Integration Points
- **PAI audit system**: Could be added for operation logging
- **Error logging**: Stderr provides detailed error information
- **Success tracking**: Stdout provides machine-readable success indicators

## Tool Philosophy

### Design Principles
- **Focused purpose**: Contact labeling only, no other Google Workspace operations
- **Stdin/stdout**: Perfect for shell pipelines and automation scripts
- **Batch friendly**: Efficient processing of contact lists
- **Error transparency**: Clear success/failure indication for each contact
- **OAuth integration**: Leverages existing Google authentication

### Workflow Augmentation
This tool transforms manual contact organization into automated workflow components, enabling:
- **Automated contact segmentation** based on business relationships
- **Event-driven contact labeling** for meetings and projects
- **Pipeline integration** with other PAI tools for comprehensive contact management
- **Scalable organization** of large contact databases

The tool embodies the PAI principle of turning repetitive manual tasks into automated, reliable workflow components that enhance human productivity rather than replacing human judgment.