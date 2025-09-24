# pai-servicenow - ServiceNow Ticket Reporting and Analysis Tool

## Overview
The `pai-servicenow` tool provides comprehensive ServiceNow integration for TAM workflows, enabling ticket querying, reporting, and analysis. Built on the proven `servicenow-api` library with PAI infrastructure integration.

## Installation and Setup

### Prerequisites
- Python 3.11+
- ServiceNow instance access (redhat.service-now.com or dev instances)
- Valid ServiceNow credentials (username/password or API token)

### Configuration
```bash
# Set up authentication (interactive)
pai-servicenow auth --instance redhat --user your-username

# Or configure via environment variables
export SNOW_USER="your-username"
export SNOW_PASSWORD="your-password"
export SNOW_INSTANCE="redhat"  # or dev300177 for development
```

### Authentication Methods
- **Basic Auth**: Username and password (most common)
- **Token Auth**: Personal Access Token (recommended for automation)
- **Kerberos**: Automatic SSO for Red Hat employees (web interface only)

## Core Functionality

### Ticket Querying

#### By Assignment Group
```bash
# Query TAM-related tickets
pai-servicenow tickets --group "Technical Account Management"

# Query Product Security tickets
pai-servicenow tickets --group "Product Security" --days 7

# Query with state filter
pai-servicenow tickets --group "OpenShift Support" --state "In Progress"
```

#### By Assignee
```bash
# Your own tickets
pai-servicenow tickets --assignee "jihoon.kim"

# Another user's tickets
pai-servicenow tickets --assignee "jane.doe" --state "New,In Progress"

# Recent tickets only
pai-servicenow tickets --assignee "me" --days 14
```

#### By Priority and Filters
```bash
# High priority tickets
pai-servicenow tickets --priority "High" --days 3

# Critical incidents
pai-servicenow tickets --priority "Critical" --state "New"

# Custom query
pai-servicenow tickets --query "state=open^priority=1^assignment_group=TAM"
```

### Report Generation

#### Daily Reports
```bash
# Daily team summary
pai-servicenow report daily --group "Technical Account Management"

# Daily personal summary
pai-servicenow report daily --assignee "me" --format markdown

# Daily priority report
pai-servicenow report daily --priority "High,Critical" --format json
```

#### SLA Analysis Reports
```bash
# Personal SLA metrics
pai-servicenow report sla --assignee "me" --days 30

# Team SLA performance
pai-servicenow report sla --group "TAM" --days 90

# Priority ticket SLA tracking
pai-servicenow report sla --priority "Critical" --days 7
```

#### Custom Reports
```bash
# Ticket aging report
pai-servicenow report aging --group "TAM" --threshold 14

# Resolution time analysis
pai-servicenow report resolution --assignee "me" --days 60

# Weekly summary for management
pai-servicenow report weekly --group "Technical Support" --format csv
```

### Data Export and Integration

#### Export Options
```bash
# Export to CSV for spreadsheet analysis
pai-servicenow export --query "state=resolved^resolved_at>30_days_ago" --format csv

# Export to JSON for further processing
pai-servicenow export --assignee "me" --format json > my_tickets.json

# Export to markdown for documentation
pai-servicenow export --group "TAM" --format markdown > team_tickets.md
```

#### PAI Knowledge Base Integration
```bash
# Sync ticket summaries to knowledge base
pai-servicenow sync --days 7 --category "tickets"

# Sync resolved tickets for knowledge capture
pai-servicenow sync --state "resolved" --days 30 --category "solutions"
```

## Advanced Features

### Fabric Pattern Integration
```bash
# Analyze ticket trends with AI
pai-servicenow tickets --group "TAM" --days 30 | pai-fabric analyze_trends

# Generate ticket summaries
pai-servicenow export --assignee "me" --format json | pai-fabric summarize_tickets

# Extract insights from ticket patterns
pai-servicenow report weekly --group "Support" | pai-fabric extract_insights
```

### Monitoring and Alerts
```bash
# Check for SLA violations
pai-servicenow monitor sla --group "TAM" --alert-threshold 4h

# Monitor high-priority tickets
pai-servicenow monitor priority --level "Critical" --notify email

# Status dashboard
pai-servicenow dashboard --group "Technical Support"
```

### Bulk Operations
```bash
# Bulk ticket updates (with confirmation)
pai-servicenow update --query "state=new^assignment_group=TAM" --field "priority=Medium"

# Bulk export for analysis
pai-servicenow bulk-export --groups "TAM,Support,Engineering" --days 90
```

## Output Formats

### Standard Output Formats
- **JSON**: Machine-readable for further processing
- **CSV**: Spreadsheet-compatible for data analysis
- **Markdown**: Human-readable reports for documentation
- **Table**: Terminal-friendly tabular display

### Report Templates
- **Daily Summary**: New, in-progress, resolved ticket counts
- **SLA Analysis**: Response times, resolution times, violation tracking
- **Aging Report**: Tickets by age buckets (0-7, 7-14, 14+ days)
- **Priority Breakdown**: Distribution by priority levels
- **Assignment Analysis**: Workload distribution across team members

## Configuration Options

### Query Parameters
- **Date Ranges**: `--days N`, `--since YYYY-MM-DD`, `--until YYYY-MM-DD`
- **States**: `New`, `In Progress`, `On Hold`, `Resolved`, `Closed`
- **Priorities**: `Critical`, `High`, `Medium`, `Low`
- **Fields**: Custom field selection for focused queries

### Output Customization
- **Format**: `json`, `csv`, `markdown`, `table`
- **Fields**: Select specific fields for export
- **Sorting**: Sort by any field (created, updated, priority, etc.)
- **Filtering**: Complex query building with ServiceNow syntax

### Integration Settings
- **PAI Sync**: Automatic knowledge base integration
- **Fabric Integration**: AI analysis pipeline configuration
- **Notification**: Email/Slack alerts for monitoring
- **Caching**: Response caching for performance

## Security and Authentication

### Credential Management
- **Environment Variables**: Secure credential storage
- **Token Rotation**: Support for API token refresh
- **Role-Based Access**: Respects ServiceNow permissions
- **Audit Logging**: Track API usage and access patterns

### Data Handling
- **PII Protection**: Automatic redaction of sensitive data
- **Data Retention**: Configurable local cache retention
- **Access Logging**: Track data access for compliance
- **Encryption**: Secure storage of cached credentials

## Integration with PAI Workflow

### Daily TAM Workflow Enhancement
```bash
# Enhanced daily briefing with ServiceNow tickets
pai-my-plate-v2 && pai-servicenow report daily --group "TAM"

# Combined case and ticket analysis
pai-case-processor report && pai-servicenow report sla --days 30

# Knowledge base enrichment
pai-servicenow sync --state "resolved" --days 7
pai-search search "servicenow tickets" smart
```

### Case Correlation
```bash
# Find related ServiceNow tickets for a case
pai-servicenow search --text "04223764" --days 90

# Cross-reference case numbers
pai-servicenow tickets --query "description~=case_number" --format json
```

## Example Use Cases

### TAM Daily Operations
1. **Morning briefing**: Check overnight tickets and priorities
2. **SLA monitoring**: Track response time performance
3. **Workload balancing**: Analyze assignment distribution
4. **Escalation tracking**: Identify tickets requiring attention

### Management Reporting
1. **Weekly metrics**: Team performance and ticket volumes
2. **Trend analysis**: Identify patterns in ticket types and resolution times
3. **Resource planning**: Workload forecasting and capacity analysis
4. **Customer satisfaction**: Response time and resolution quality metrics

### Integration Benefits
- **Unified workflow**: Single interface for case management and ServiceNow
- **Automated reporting**: Reduces manual report generation time
- **Data correlation**: Links ServiceNow tickets with case management data
- **AI enhancement**: Leverages fabric patterns for intelligent analysis

## Error Handling and Troubleshooting

### Common Issues
- **Authentication failures**: Check credentials and instance URL
- **Query timeouts**: Reduce query scope or add pagination
- **Permission errors**: Verify ServiceNow role assignments
- **API rate limits**: Implement backoff and retry mechanisms

### Diagnostic Commands
```bash
# Test connectivity
pai-servicenow status

# Validate authentication
pai-servicenow auth --test

# Debug query issues
pai-servicenow tickets --debug --group "TAM" --limit 5
```

## Development and Customization

### Configuration Files
- `~/.claude/context/config/servicenow.yaml` - Main configuration
- `~/.claude/context/config/servicenow-queries.yaml` - Predefined queries
- `~/.claude/context/logs/servicenow.log` - Activity logging

### Extension Points
- **Custom report templates**: Add new report types
- **Query builders**: Create complex query patterns
- **Output formatters**: Develop specialized output formats
- **Integration hooks**: Connect with other PAI tools

This tool provides comprehensive ServiceNow integration while maintaining the PAI architecture principles of security, automation, and knowledge management.