# pai-hydra-processor

Hydra notification processing and case metadata extraction.

## Location
`~/.local/bin/pai-hydra-processor`

## Description
Specialized processor for Hydra email notifications that extracts case metadata, identifies accounts, and converts notifications to structured markdown format for integration with TAM workflows.

## Key Features
- **Pattern Recognition**: Identifies Hydra notifications by subject patterns
- **Case Extraction**: Extracts case numbers from various formats
- **Account Detection**: Automatically identifies customer accounts
- **Metadata Parsing**: Extracts severity, dates, and other case metadata
- **Markdown Conversion**: Creates structured output with YAML frontmatter

## Commands

### Processing
```bash
pai-hydra-processor                 # Process recent Hydra notifications (default: 7 days)
pai-hydra-processor --days 3        # Process last 3 days
pai-hydra-processor --days 14       # Process last 2 weeks
```

### Management
```bash
pai-hydra-processor --list          # List processed notifications (last 30 days)
pai-hydra-processor --case 04056105 # Process specific case (future feature)
```

## Hydra Notification Patterns

### Subject Pattern Recognition
- **Primary**: `Hydra: Case 04056105` 
- **Variations**: `Hydra Case 04056105`, `Hydra - Case: 04056105`
- **Fallback**: Searches email body for 8-digit case numbers

### Account Detection
Automatically identifies accounts based on content patterns:
- **BNY**: `bny`, `bank.*new.*york`, `mellon`
- **CIBC**: `cibc`, `canadian.*imperial`  
- **Citi**: `citi`, `citigroup`, `citibank`
- **Discover**: `discover`, `discover.*financial`

### Severity Extraction
Recognizes severity indicators:
- **Numeric**: Severity 1, 2, 3, 4
- **Text**: Low, Medium, High, Critical
- **Case context**: Extracts from notification body

## Output Format

### Markdown Structure
```markdown
---
title: "Hydra Notification - Case 04056105"
case_id: "04056105"
account: "bny"
severity: "High"
notification_type: "hydra"
from: "hydra@redhat.com"
date: "2025-01-07T12:00:00Z"
processed: "2025-01-07T12:05:00Z"
tags: [hydra, case04056105, bny]
---

# Hydra Notification - Case 04056105

## Extracted Metadata
- **Case Number**: 04056105
- **Account**: bny
- **Severity**: High

## Action Items
- [ ] Review case in Salesforce/Hydra
- [ ] Run case analysis: `pai-workspace case 04056105 analyze`
- [ ] Check for related cases: `rhcase list bny`

## Related Commands
```bash
pai-workspace case 04056105 analyze
rhcase analyze 04056105
```
```

### Output Location
- **Directory**: `~/.claude/context/capture/hydra/`
- **Filename**: `hydra-case-{case_number}-{date}.md`
- **Example**: `hydra-case-04056105-20250107.md`

## Processing Logic

### Email Source
- **Email directory**: `~/.claude/context/capture/email/gmail-gvaughn/`
- **Search method**: Uses notmuch to find Hydra-related emails
- **Time range**: Configurable days lookback (default: 7)

### Deduplication
- **Check existing**: Avoids reprocessing same case notifications
- **Filename pattern**: Uses case number and date for uniqueness
- **Skip processed**: Reports already processed cases

### Error Handling
- **Missing case numbers**: Logs and skips malformed notifications
- **Account detection failure**: Uses "Unknown" as fallback
- **Severity parsing**: Defaults to "Unknown" if not found
- **Email access errors**: Graceful handling with error logging

## Integration Points

### Daily Workflow Integration
- **Called by pai-email-sync**: Automatic processing every 15 minutes
- **pai-my-plate-v2**: Hydra notifications included in daily briefings
- **Case linking**: Provides case numbers for workspace integration

### TAM Workflow Integration
- **Case analysis trigger**: Notifications can trigger case analysis
- **Account mapping**: Links to existing account structures
- **Workspace integration**: Compatible with pai-workspace commands

### Security Integration
- **pai-audit logging**: All processing logged for compliance
- **No data retention**: Processes notifications without storing email content
- **Metadata only**: Extracts only necessary case metadata

## Example Processing Flow

### Input: Hydra Email
```
Subject: Hydra: Case 04056105 - High Severity
From: hydra-notifications@redhat.com
Body: Case 04056105 for BNY Bank has been escalated to High severity...
```

### Output: Structured Markdown
```markdown
---
title: "Hydra Notification - Case 04056105"
case_id: "04056105"
account: "bny"
severity: "High"
---

# Hydra Notification - Case 04056105

[Structured analysis and action items]
```

## Performance
- **Fast processing**: Regex-based pattern matching
- **Efficient search**: Uses notmuch for email queries
- **Minimal overhead**: Only processes new notifications
- **Batch capable**: Handles multiple notifications efficiently

## Monitoring and Analytics

### Processing Statistics
```bash
pai-hydra-processor --list
```

Shows:
- **Case numbers processed**: With timestamps
- **Processing dates**: When each case was handled
- **Account distribution**: Which accounts are most active

### Integration with Reporting
- **Daily briefings**: Processed notifications included
- **Case analysis**: Triggers for comprehensive case review
- **Trend analysis**: Pattern identification across notifications

## Future Enhancements
- **Case-specific processing**: Direct case number processing
- **Advanced pattern recognition**: ML-based notification classification
- **Workflow triggers**: Automatic case analysis initiation
- **Escalation detection**: Priority-based notification handling
