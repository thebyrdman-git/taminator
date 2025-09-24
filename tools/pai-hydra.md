# pai-hydra - Red Hat Hydra API Query Tool

## Overview
The `pai-hydra` tool provides ad-hoc query capabilities against the Red Hat Hydra API for TAM workflows. It enables quick lookups of cases, contacts, and account information without needing to navigate the web interface or write custom API calls.

## Installation and Setup

### Prerequisites
- Red Hat authentication credentials in environment variables:
  - `REDHAT_USERNAME` - Your Red Hat username
  - `REDHAT_PASSWORD` - Your Red Hat password
- Network access to `access.redhat.com/hydra/rest`

### Authentication
The tool uses basic authentication with your Red Hat credentials and integrates with the PAI audit logging system for security tracking.

## Core Functionality

### Contact Lookups

#### Email to SSO Username Lookup
```bash
# Look up SSO username by email address
pai-hydra email john.doe@company.com

# Example output:
# 🔍 Looking up SSO username for email: john.doe@company.com
#    Searching in account 999625...
#    Searching in account 1460290...
#    ✅ Found in account 729650
#
# 📋 Found 1 matching contact(s):
#    Account: 729650
#    SSO Username: John.Doe@company.com
#    Name: John Doe
#    Contact Type: Customer
```

#### SSO Username to Contact Details
```bash
# Look up contact details by SSO username
pai-hydra sso rhn-support-gvaughn

# Example output:
# 📋 Contact details for rhn-support-gvaughn:
#    Name: Grimm Greysson
#    Email: gvaughn@redhat.com
#    Phone: 1-919-754-4950
#    Country: N/A
#    Company: N/A
#    Contact Type: N/A
```

### Case Information Lookup

#### Case Details
```bash
# Get case information from Hydra
pai-hydra case 04245934

# Example output:
# 📋 Case 04245934 details:
#    Summary: Unable to get AWS Load Balancer Operator working
#    Status: Waiting on Red Hat
#    Severity: 3 (Normal)
#    Product: OpenShift Container Platform
#    Owner: Jihoon Kim
#    Account: 999625
#    Created: 2025-08-08T14:52:10Z
#    Updated: 2025-09-12T20:06:14Z
```

### Account Management

#### List Account Contacts
```bash
# List all contacts for an account
pai-hydra contacts 729650

# Example output:
# 📋 Found 179 contact(s) for account 729650:
#    SSO: N/A
#    Name: John Doe
#    Email: john.doe@company.com
#    Type: Customer
#    ---
#    [... continues for all contacts]
```

### System Diagnostics

#### Authentication Test
```bash
# Test Hydra API authentication and connectivity
pai-hydra auth

# Example output:
# 🔐 Testing Hydra API authentication...
#    Username: rhn-support-gvaughn
#    Password: ***********
#
# 🧪 Testing API access...
# ✅ Authentication and API access confirmed
```

## Output Formats

### Text Format (Default)
Human-readable output with emojis and formatting for terminal display.

### JSON Format
Machine-readable JSON output for further processing:

```bash
# Get JSON output for any command
pai-hydra --format json sso rhn-support-gvaughn
pai-hydra --format json case 04245934
pai-hydra --format json contacts 729650
```

## Account Coverage

The tool searches across common TAM account numbers:
- **999625** - Discover Financial Services
- **1460290** - CIBC
- **729650** - BNY Mellon
- **1212328** - Citi

Additional accounts can be added by modifying the tool's account list.

## Integration with PAI Workflow

### Daily TAM Operations
```bash
# Quick contact lookup during case work
pai-hydra email customer@company.com

# Verify case ownership and status
pai-hydra case 04123456

# Account relationship verification
pai-hydra contacts 999625 | grep -i "technical.*contact"
```

### Case Analysis Workflow
```bash
# Contact information for case stakeholders
cat stakeholder_emails.txt | while read email; do
    echo "=== $email ==="
    pai-hydra email "$email"
done

# Case details for strategic analysis
for case in 04123456 04789012; do
    pai-hydra --format json case "$case" > "case_${case}_details.json"
done
```

### Account Intelligence
```bash
# Export all account contacts for analysis
pai-hydra --format json contacts 729650 > bny_contacts.json

# Find technical contacts
pai-hydra contacts 729650 | grep -A5 -B5 -i "engineer\|architect\|technical"
```

## Error Handling and Troubleshooting

### Common Issues

#### Authentication Failures
- **Symptom**: "Unable to authenticate user"
- **Solution**: Verify `REDHAT_USERNAME` and `REDHAT_PASSWORD` environment variables
- **Test**: Run `pai-hydra auth` to validate credentials

#### Contact Not Found
- **Symptom**: "No SSO username found for email"
- **Cause**: Contact may not exist in searched accounts or no access permissions
- **Solution**: Verify email address and account access

#### API Timeouts
- **Symptom**: Request timeouts or connection errors
- **Solution**: Check network connectivity to `access.redhat.com`
- **Retry**: API calls are safe to retry

### Diagnostic Commands
```bash
# Test authentication
pai-hydra auth

# Verify account access
pai-hydra contacts 999625 | head -10

# Check specific contact exists
pai-hydra email known-contact@company.com
```

## Security and Audit

### Audit Logging
All API operations are logged to the PAI audit system:
- `email_lookup_success/failed` - Email to SSO lookups
- `sso_lookup_success/failed` - SSO to contact details
- `case_lookup_success/failed` - Case information queries
- `account_contacts_success/failed` - Account contact listings
- `auth_test_success/failed` - Authentication tests

### Data Handling
- **Credentials**: Environment variables only, never stored in files
- **API Responses**: Cached in memory during execution only
- **Personal Data**: Contact information handled according to Red Hat privacy policies
- **Access Logging**: All API calls tracked for compliance

## API Endpoints Used

### Contact Endpoints
- `GET /contacts/sso/{ssoUsername}` - Get contact by SSO username
- `GET /v1/accounts/{accountNumber}/contacts` - List account contacts
- `GET /v1/accounts/{accountNumber}/notifyees/{searchString}` - Search account contacts

### Case Endpoints
- `GET /v1/cases/{caseNumber}` - Get case details

### System Endpoints
- `GET /v1/businesshours?timezone=UTC` - System connectivity test

## Integration Examples

### Pipeline Processing
```bash
# Process email list and generate contact report
cat customer_emails.txt | while read email; do
    echo -n "$email -> "
    pai-hydra email "$email" 2>/dev/null | grep "SSO Username:" | cut -d: -f2 | xargs
done

# Find all contacts for multiple accounts
for account in 999625 729650 1460290; do
    echo "=== Account $account ==="
    pai-hydra --format json contacts "$account" | jq -r '.[] | "\(.firstName) \(.lastName) - \(.email)"'
done
```

### Case Management
```bash
# Quick case status check
pai-hydra case 04245934 | grep -E "(Status|Owner|Severity)"

# Export case details for analysis
pai-hydra --format json case 04245934 | jq '{
    summary: .summary,
    status: .status,
    owner: .ownerId,
    account: .accountNumberRef,
    updated: .lastModifiedDate
}'
```

## Configuration and Customization

### Environment Setup
```bash
# Set credentials (add to ~/.bashrc or ~/.zshrc)
export REDHAT_USERNAME="your-username"
export REDHAT_PASSWORD="your-password"
```

### Account Configuration
The tool currently searches these accounts by default. To add additional accounts, modify the accounts list in the tool:

```python
accounts = ["999625", "1460290", "729650", "1212328", "NEW_ACCOUNT"]
```

### Output Customization
- **Text Format**: Human-readable with emojis and formatting
- **JSON Format**: Machine-readable for further processing
- **Error Output**: Sent to stderr, success to stdout

This tool provides comprehensive Hydra API access while maintaining the PAI architecture principles of security, auditability, and workflow integration.