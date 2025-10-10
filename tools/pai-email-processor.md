# pai-email-processor

Email intelligence and contact research for TAM workflows.

## Location
`~/.local/bin/pai-email-processor`

## Description
Comprehensive email analysis tool that processes emails for TAM relevance, identifies potential issues, researches contacts for relationship building, and generates intelligence summaries for daily briefings.

## Core Features
- **TAM Relevance Analysis**: Identifies emails related to customers, cases, and technical issues
- **Issue Detection**: Finds potential problems mentioned in emails
- **Contact Intelligence**: Researches external contacts for relationship building
- **Dossier Creation**: Builds professional profiles for meeting preparation
- **Integration Ready**: Designed for daily briefing inclusion

## Commands

### Email Processing
```bash
pai-email-processor process [days] [max]    # Process recent emails
# Examples:
pai-email-processor process 1 20           # Last 1 day, max 20 emails
pai-email-processor process 3 50           # Last 3 days, max 50 emails
```

### Issue Identification
```bash
pai-email-processor issues [days]          # Identify potential issues from emails
# Examples:
pai-email-processor issues 1               # Issues from last day
pai-email-processor issues 7               # Issues from last week
```

### Contact Research
```bash
pai-email-processor contact <email> [name] # Research contact and create dossier
# Examples:
pai-email-processor contact "john@company.com" "John Smith"
pai-email-processor contact "jane.doe@enterprise.com"
```

### Reporting
```bash
pai-email-processor summary [days]         # Generate email summary for briefings
# Example:
pai-email-processor summary 1              # Daily email summary
```

## Email Analysis Process

### TAM Relevance Detection
Analyzes emails for:
- **Customer mentions**: BNY, CIBC, Citi, Discover, other companies
- **Technical issues**: Problems, errors, failures, outages
- **Case references**: Case numbers or support ticket mentions
- **Escalations**: Urgent items or priority issues
- **Product mentions**: OpenShift, RHEL, AI tools, security products
- **Meeting requests**: Calendar items and scheduling

### Issue Classification
Identifies potential issues by looking for:
- **Problem indicators**: "problem", "issue", "error", "failure", "down", "outage"
- **Urgency markers**: "urgent", "critical", "immediate", "asap"
- **Customer impact**: Business impact statements
- **Technical failures**: System or application problems

## Contact Research Features

### Automatic Research
For external contacts (non-@redhat.com), researches:
- **Current role and company**
- **Technical background and expertise**
- **Professional history**
- **Social media/professional profiles**
- **Recent publications or presentations**
- **Areas of technical interest**
- **Collaboration opportunities**

### Dossier Creation
Creates structured contact profiles:
```markdown
---
title: Contact Dossier - John Smith
email: john@company.com
name: John Smith
researched: 2025-01-07T12:00:00Z
tags: [contact, research, dossier]
---

# Contact Dossier - John Smith

## Research Results
[AI-generated professional profile]

## TAM Notes
[Manual observations and interaction history]

## Relationship Status
- [ ] Initial contact
- [ ] Active engagement
- [x] Regular communication
- [ ] Strategic relationship
```

## Output Locations

### Email Analysis
- **Daily emails**: `~/.claude/context/create/outputs/email/daily/`
- **Filename**: `email-{hash}-{date}.md`

### Contact Dossiers
- **Directory**: `~/.claude/context/create/outputs/email/contacts/`
- **Filename**: `{email-sanitized}-{date}.md`

### Issue Reports
- **Directory**: `~/.claude/context/create/outputs/email/issues/`
- **Filename**: `issues-{date}.md`

## Integration with Daily Briefings

### Email Summary Generation
```bash
pai-email-processor summary 1
```

Provides structured summary:
```markdown
## Email Intelligence Summary

### Processing Stats
- **Total emails processed**: 15
- **TAM-relevant emails**: 8
- **Analysis period**: Last 1 day(s)

### Potential Issues Identified
- Customer reported OpenShift networking problems
- Escalation request for case 04056105

### Contact Research
- 3 new contacts researched and added to dossier system
- External contacts automatically profiled for relationship building
```

## AI Enhancement

### Fabric Pattern Integration
- **Email analysis**: Uses fabric patterns for content analysis
- **Contact research**: Perplexity for up-to-date professional information
- **Issue detection**: AI-powered problem identification
- **Summary generation**: Intelligent briefing creation

### Model Usage
- **Analysis**: gpt-4o for email content analysis
- **Research**: perplexity-sonar-large for contact intelligence
- **Classification**: fabric patterns for TAM relevance

## Security and Privacy

### Data Handling
- **Email content**: Processed but not permanently stored
- **Contact research**: Only publicly available information
- **Privacy compliance**: No personal data collection
- **Audit logging**: All processing activities tracked

### Redaction Integration
- **Sensitive data**: Automatic redaction before external research
- **Customer data**: Protected via pai-audit integration
- **Contact privacy**: Research limited to professional information

## Performance Features
- **Batch processing**: Handles multiple emails efficiently
- **Deduplication**: Avoids reprocessing same emails
- **Selective processing**: Focuses on TAM-relevant content
- **Resource efficient**: Minimal system impact

## Workflow Examples

### Morning Email Review
```bash
# Process overnight emails
pai-email-processor process 1 30

# Check for issues
pai-email-processor issues 1

# Include in daily briefing
pai-email-processor summary 1
```

### Meeting Preparation
```bash
# Research meeting attendees
pai-email-processor contact "attendee@company.com" "Attendee Name"

# Check for related email context
pai-email-processor process 7 100 | grep -i "company"
```

### Issue Tracking
```bash
# Daily issue monitoring
pai-email-processor issues 1

# Weekly issue trends
pai-email-processor issues 7
```
