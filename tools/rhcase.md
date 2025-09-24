# rhcase

TAMScripts - AI-powered Red Hat support case analysis tool.

## Location
`~/.local/bin/rhcase`

## Description
Command-line tool for interacting with Red Hat support cases, knowledge base articles (KCS), Jira issues, and CVEs. Provides comprehensive case management capabilities for TAMs with AI-powered analysis features.

## Initial Setup
```bash
# Quick configuration - enter credentials and go!
rhcase config setup
```

## Core Commands

### Case Operations

#### Analyze a Single Case
```bash
rhcase analyze <case_number>
# Example:
rhcase analyze 12345678
```

#### List Cases by Account
```bash
rhcase list <account_name>
# Example:
rhcase list cibc
rhcase list yourcompany
```

#### Search Cases
```bash
rhcase case search [options]
# Search support cases across accounts
```

#### Manage Attachments
```bash
rhcase attachments [options]
# List or download case attachments
```

### KCS (Knowledge-Centered Support) Operations

#### Search KCS Articles
```bash
rhcase kcs search <terms>
# Examples:
rhcase kcs search "OpenShift Update Service logging"
rhcase kcs search "OLM InstallPlan" --product "OpenShift" --limit 20
rhcase kcs search "authselect RHEL CoreOS" --verbose

# Options:
#   --product PRODUCT     Filter by Red Hat product name
#   --version VERSION     Filter by product version
#   --limit LIMIT         Max results (default: 10, max: 500)
#   --format {table,json,csv}  Output format
#   --verbose            Include summaries and detailed info
```

#### Fetch KCS Article
```bash
rhcase kcs fetch <kcs_id>
# Example:
rhcase kcs fetch 5431091
# Fetches and converts KCS article to markdown
```

### Jira Operations

#### Search Jira Issues
```bash
rhcase jira search <query>
# Examples:
rhcase jira search "Update Service DEBUG logging"
rhcase jira search "project = OCP AND summary ~ 'authselect'"

# Uses JQL (Jira Query Language) or text queries
```

#### Fetch Jira Issue
```bash
rhcase jira fetch <issue_id>
# Examples:
rhcase jira fetch RFE-8101
rhcase jira fetch OTA-169
rhcase jira fetch RHEL-12345
```

#### List Jira Projects
```bash
rhcase jira projects
# Lists all Jira projects accessible to your account
```

### CVE Operations
```bash
rhcase cve <cve_number>
# Example:
rhcase cve CVE-2023-5366
```

### System Management

#### Health Check
```bash
rhcase doctor
# Run comprehensive system diagnostics and health checks
```

#### Update TAMScripts
```bash
rhcase update
# Update TAMScripts to latest version
```

## Key Features
- AI-powered case analysis
- Pattern analysis across multiple cases
- Rich terminal output with formatting
- Multiple output formats (table, JSON, CSV)
- Integration with Red Hat support systems
- Attachment management
- Configurable timeouts and proxies

## Account Mappings
- CIBC: Account numbers 1216348, 5598345, 6587770
- BNY: Account number 729650
- Discover: Account number 999625
- Citi: Account number 411070

## Example Workflows

### Complete Case Analysis
```bash
# 1. Quick setup (first time only)
rhcase config setup

# 2. Analyze a specific case
rhcase analyze 04056105

# 3. List all cases for an account
rhcase list bny

# 4. Search for relevant KCS articles
rhcase kcs search "missing authselect RPMs" --verbose

# 5. Fetch specific KCS article
rhcase kcs fetch 5431091

# 6. Search for related Jira issues
rhcase jira search "authselect CoreOS"

# 7. Fetch specific Jira issue
rhcase jira fetch RHCOS-1234
```

### KCS Research Workflow
```bash
# Search with filters
rhcase kcs search "OLM InstallPlan" --product "OpenShift Container Platform" --version "4.13"

# Get verbose output with summaries
rhcase kcs search "Update Service logging" --verbose --limit 20

# Output in different formats
rhcase kcs search "pod security" --format json > pod-security-kcs.json
rhcase kcs search "etcd backup" --format csv > etcd-backup-kcs.csv
```

### Pattern Analysis
```bash
# Analyze patterns from CSV file
rhcase patterns <csv_file>
# Useful for identifying trends across multiple cases
```

## Integration Points
- Used by PAI agents for case data retrieval
- Feeds into daily "My Plate" briefings
- Source for case initial screening
- Integrates with workflow documentation
- CVE tracking for security issues

## Notes
- Requires Red Hat internal network access
- Uses API tokens for authentication (configured during setup)
- Supports proxy configurations for corporate environments
- The workflow.md example shows saving fetched content with `-o` flag, but current help doesn't show this option