# pai-confluence

Red Hat internal Confluence integration for accessing development resources, product documentation, and business unit information.

## Location
`~/.local/bin/pai-confluence`

## Description
Command-line tool for accessing Red Hat's internal Confluence system (spaces.redhat.com) with features for searching, retrieving pages as markdown, and integrating with the PAI knowledge base. Supports non-interactive operation for automation and scripting.

## Features
- **Non-Interactive Authentication**: Personal Access Token support with secure storage
- **Content Search**: Full-text and space-specific search with CQL support
- **Markdown Export**: Automatic HTML to markdown conversion with pandoc
- **Scriptable Output**: Quiet mode and stdout support for pipelines
- **Space Navigation**: List and explore Confluence spaces
- **PDF Processing**: Extract content from downloaded Confluence PDFs
- **Knowledge Base Integration**: Sync content to PAI knowledge base
- **AI Enhancement**: Smart search with fabric integration

## Installation & Setup

### First-Time Setup
```bash
# Non-interactive authentication with token
pai-confluence auth "YOUR_PERSONAL_ACCESS_TOKEN"

# Or interactive setup
pai-confluence auth

# Verify access
pai-confluence spaces
```

### Getting Your Personal Access Token
1. Go to https://spaces.redhat.com
2. Click your profile picture (top right) → Profile
3. Go to Settings → Personal Access Token
4. Click "Create Token"
5. Name it (e.g., "PAI Integration")
6. Set expiration (optional but recommended)
7. Click Create and save the token

## Usage

### Command Syntax
```bash
pai-confluence [global-flags] <command> [options]

Global Flags:
  -q, --quiet         # Suppress informational output
  -o, --output-stdout # Output to stdout instead of files
```

### Basic Search
```bash
# Human-readable search
pai-confluence search "OpenShift 4.17"

# Machine-readable output (tab-separated: ID, type, space, title)
pai-confluence -q search "etcd backup"

# Search in specific space
pai-confluence search "monitoring" OCPSUP

# Extract just page IDs
pai-confluence -q search "security" | cut -f1
```

### Download Pages
```bash
# Download page to file (default behavior)
pai-confluence get 123456789

# Output page to stdout
pai-confluence -o get 123456789 > page.md

# Quiet mode with stdout (no progress messages)
pai-confluence -q -o get 123456789 > page.md

# Get page in different formats
pai-confluence get 123456789 storage    # Raw storage format
pai-confluence get 123456789 export_view # Clean export format
```

### Pipeline Examples
```bash
# Search and download all matching pages
pai-confluence -q search "OpenShift security" | \
  cut -f1 | \
  xargs -I{} pai-confluence -q get {}

# Filter by space and download
pai-confluence -q search "troubleshooting" | \
  awk -F'\t' '$3=="OCPSUP" {print $1}' | \
  xargs -I{} pai-confluence -o get {} > troubleshooting-guide.md

# Process with AI
pai-confluence -q search "customer issue" | \
  head -5 | cut -f1 | \
  xargs -I{} pai-confluence -q -o get {} | \
  fabric -p extract_wisdom -m gpt-4o

# Create knowledge base entries
pai-confluence -q search "best practices" TAMKB | \
  cut -f1 | \
  while read id; do
    pai-confluence -q -o get "$id" | \
    pai-search add confluence "Page $id" "$(cat)"
  done
```

### Space Operations
```bash
# List all spaces (human-readable)
pai-confluence spaces

# List spaces (machine-readable: key<TAB>name)
pai-confluence -q spaces

# Filter spaces
pai-confluence -q spaces | grep -i openshift

# Export space structure
pai-confluence tree TAMKB
```

### PDF Processing
```bash
# Process downloaded Confluence PDF
pai-confluence process-pdf ~/Downloads/confluence-export.pdf

# Process and auto-sync to knowledge base
pai-confluence process-pdf ~/Downloads/guide.pdf --sync
```

### Recent Updates
```bash
# Show updates from last 7 days
pai-confluence recent

# Show updates in specific space
pai-confluence recent OCPSUP 14

# Pipeline recent updates
pai-confluence -q recent TAMKB 7 | \
  cut -f1 | \
  xargs -I{} pai-confluence get {}
```

## Configuration

Configuration file: `~/.claude/context/config/confluence.yaml`

```yaml
confluence:
  url: "https://spaces.redhat.com"
  default_space: ""
  results_limit: 20
  spaces:
    - key: "OCPSTRAT"
      name: "OpenShift Strategy"
    - key: "OCPSUP"
      name: "OpenShift Support"
    - key: "TAMKB"
      name: "TAM Knowledge Base"
    - key: "RHAIDOCS"
      name: "Red Hat AI Documentation"
  search_defaults:
    type: "page"
    include_archived: false
    include_attachments: true
```

### Key Configuration Options
- **url**: Red Hat Confluence URL (spaces.redhat.com)
- **default_space**: Default space for searches
- **results_limit**: Maximum search results (default: 20)
- **spaces**: Quick reference for common spaces

## Output Locations
- **Captures**: `~/.claude/context/capture/confluence/`
- **Knowledge Base**: `~/.claude/context/knowledge/confluence/`
- **Logs**: `~/.claude/context/logs/confluence-YYYYMMDD.log`
- **Auth Storage**: Encrypted via `pai-audit secret`

## Practical Examples

### TAM Case Research
```bash
# Find known issues for a specific OpenShift version
pai-confluence -q search "OpenShift 4.16 etcd corruption" | \
  awk -F'\t' '$3=="OCPSUP" {print $1}' | \
  xargs -I{} pai-confluence -o get {} | \
  fabric -p extract_wisdom -m gpt-4o > etcd-issues.md

# Research customer-specific issues
pai-confluence search "CIBC networking" TAMKB

# Build case knowledge base
case_num="04123456"
pai-confluence -q search "case $case_num" | \
  cut -f1 | \
  xargs -I{} pai-confluence -q -o get {} | \
  pai-search add cases "Case $case_num Research" "$(cat)"
```

### Product Documentation Pipeline
```bash
# Download all security best practices
pai-confluence -q search "security best practices" | \
  grep -E "(OCPSUP|RHAISEC)" | \
  cut -f1 | \
  xargs -I{} pai-confluence get {}

# Create consolidated security guide
pai-confluence -q search "hardening guide" | \
  cut -f1 | \
  xargs -I{} pai-confluence -q -o get {} | \
  pandoc -f markdown -t html -o security-guide.html
```

### Automated Weekly Sync
```bash
#!/bin/bash
# Save as ~/bin/confluence-weekly-sync.sh

SPACES="TAMKB OCPSUP OCPSTRAT"
DAYS=7

for space in $SPACES; do
  echo "Syncing $space updates from last $DAYS days..."
  
  pai-confluence -q recent $space $DAYS | \
    cut -f1 | \
    while read page_id; do
      echo "Fetching page $page_id..."
      pai-confluence -q get "$page_id"
    done
done

# Sync to knowledge base
find ~/.claude/context/capture/confluence -name "*.md" -mtime -$DAYS | \
  xargs -I{} pai-confluence sync {} confluence
```

### Integration with Other PAI Tools
```bash
# Combine with pai-workspace for case documentation
case_num="04250846"
pai-confluence -q search "$case_num" | \
  cut -f1 | \
  xargs -I{} pai-confluence -o get {} > \
  ~/Documents/rh/projects/tam-ocp/cibc/casework/active/$case_num/confluence-research.md

# Use with pai-fabric for analysis
pai-confluence -q search "root cause analysis" TAMKB | \
  head -10 | cut -f1 | \
  xargs -I{} pai-confluence -q -o get {} | \
  pai-fabric analyze

# Feed into pai-case-processor
pai-confluence -q search "escalation procedures" | \
  cut -f1 | \
  xargs -I{} pai-confluence -q -o get {} > \
  ~/.claude/context/knowledge/procedures/escalation-guide.md
```

## Advanced Features

### CQL (Confluence Query Language) Support
The search function uses CQL for queries. While the tool builds CQL automatically, understanding the syntax helps:
```bash
# Text contains (default behavior)
pai-confluence search "etcd backup"  # Becomes: text ~ "etcd backup"

# Space-specific search
pai-confluence search "security" OCPSUP  # Becomes: text ~ "security" AND space = "OCPSUP"

# Note: Complex CQL queries should be constructed manually in the tool if needed
```

### Handling Large Result Sets
```bash
# Process results in batches
pai-confluence -q search "OpenShift" | \
  split -l 10 -a 3 - batch_ && \
  for batch in batch_*; do
    cat "$batch" | cut -f1 | \
    xargs -I{} pai-confluence -q get {}
    sleep 2  # Be nice to the API
  done

# Download with progress tracking
total=$(pai-confluence -q search "security" | wc -l)
pai-confluence -q search "security" | cut -f1 | \
  nl | \
  while read num id; do
    echo "Processing $num/$total: $id"
    pai-confluence -q get "$id"
  done
```

### Smart Search with Fabric
```bash
# AI-enhanced search (requires fabric setup)
pai-confluence smart-search "troubleshooting etcd" OCPSUP

# Custom fabric pattern processing
pai-confluence -q -o get 123456789 | \
  fabric -p redact_tam_data | \
  fabric -p extract_wisdom -m gpt-4o
```

## Output Formats

### Page Metadata Structure
Each downloaded page includes YAML frontmatter:
```yaml
---
title: "Page Title"
space: "SPACE_KEY"
page_id: "123456789"
version: 1
confluence_url: "https://spaces.redhat.com/spaces/SPACE_KEY/pages/123456789"
captured: 2024-12-11T10:30:00-05:00
format: "view"
---
```

### Search Output Format (Quiet Mode)
Tab-separated values: `PAGE_ID<TAB>TYPE<TAB>SPACE<TAB>TITLE`
```
123456789    page    OCPSUP    Troubleshooting Guide
987654321    page    TAMKB     Best Practices
```

## Security Considerations
- **Token Storage**: Personal Access Tokens stored encrypted via `pai-audit secret`
- **API Logging**: All API calls logged to `~/.claude/context/logs/`
- **Data Handling**: Downloaded content may contain sensitive information
- **Network Security**: All API calls use HTTPS
- **Token Rotation**: Regularly rotate Personal Access Tokens
- **Permissions**: Only access spaces/pages your account has permission to view

## Troubleshooting

### Authentication Issues
```bash
# Verify token is stored
pai-audit secret get confluence-token

# Re-authenticate
pai-confluence auth --force

# Test API access directly
curl -s -H "Authorization: Bearer $(pai-audit secret get confluence-token)" \
  "https://spaces.redhat.com/rest/api/space?limit=1" | jq .
```

### Empty or No Results
```bash
# Check if search returns results
pai-confluence search "common term"

# Verify space exists
pai-confluence -q spaces | grep -i "SPACENAME"

# Try broader search terms
pai-confluence search "OpenShift"  # Instead of specific version
```

### Network/Connectivity Issues
```bash
# Test basic connectivity
curl -I https://spaces.redhat.com

# Check for proxy settings
env | grep -i proxy

# Increase curl timeout (edit script if needed)
# Change curl timeout from default to 30 seconds
```

### PDF Processing Issues
```bash
# Ensure pdftotext is installed
which pdftotext || sudo dnf install -y poppler-utils

# Process PDF manually if needed
pdftotext input.pdf output.txt
```

## Best Practices

### 1. **Efficient Searching**
- Use specific search terms to reduce result sets
- Always specify space when known
- Use quiet mode (`-q`) for scripting

### 2. **API Rate Limiting**
- Add delays between bulk operations
- Process in batches for large result sets
- Cache frequently accessed pages locally

### 3. **Content Management**
- Regularly sync important pages to local knowledge base
- Use consistent naming for downloaded files
- Implement version tracking for critical documentation

### 4. **Integration Patterns**
```bash
# Standard pipeline pattern
pai-confluence -q search "SEARCH_TERM" | \
  cut -f1 | \
  xargs -I{} pai-confluence -q -o get {} | \
  PROCESS_COMMAND > output.md

# Knowledge base pattern
pai-confluence -q -o get PAGE_ID | \
  pai-search add CATEGORY "TITLE" "$(cat)"
```

## Dependencies
- **curl**: API communication
- **jq**: JSON parsing
- **yq**: YAML configuration
- **pandoc** (optional): HTML to markdown conversion
- **pdftotext** (optional): PDF text extraction

## See Also
- [pai-search](pai-search.md) - Knowledge base management
- [pai-fabric](pai-fabric.md) - AI pattern processing  
- [pai-audit](pai-audit.md) - Security and secrets management
- [pai-workspace](pai-workspace.md) - TAM workspace integration
- [pai-case-processor](pai-case-processor.md) - Case analysis automation
