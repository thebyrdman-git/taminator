# Red Hat Work Email Organization System

## 🎯 Overview

This document describes the complete Gmail organization system for your Red Hat work email (`jbyrd@redhat.com`), designed to parallel the existing personal email system while maintaining full Red Hat AI policy compliance.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                Red Hat Work Email Organization System                │
└─────────────────────────────────────────────────────────────────────┘
                                      │
                ┌─────────────────────┼─────────────────────┐
                │                     │                     │
        ┌───────▼──────┐    ┌────────▼────────┐   ┌──────▼──────┐
        │   Gmail API   │    │   Notmuch       │   │ Red Hat     │
        │   Sync        │    │   Search &      │   │ Compliance  │
        │               │    │   Tagging       │   │ (Granite)   │
        └───────┬──────┘    └────────┬────────┘   └──────┬──────┘
                │                    │                   │
        ┌───────▼──────────────────────▼───────────────────▼──────┐
        │              Local Email Storage                        │
        │         ~/.claude/context/capture/email/               │
        │              gmail-jbyrd-redhat/                       │
        └───────┬──────────────────────┬────────────────────────┘
                │                      │
        ┌───────▼──────┐      ┌───────▼────────┐
        │   Reports &   │      │   Automation   │
        │   Analytics   │      │   (systemd)    │
        └──────────────┘      └────────────────┘
```

## 🚀 Quick Start

### One-Command Setup
```bash
pai-work-email-setup
```

This single command handles:
- ✅ Prerequisites checking
- ✅ Directory structure creation  
- ✅ OAuth authentication setup
- ✅ Email organization configuration
- ✅ Initial sync and tagging
- ✅ Automation setup (30-minute intervals)
- ✅ Quick reference creation

### Manual Setup (if needed)
```bash
# 1. Authenticate with Red Hat Gmail
pai-gmail-work-auth

# 2. Set up organization system  
pai-email-work-organizer setup

# 3. Run initial sync
pai-email-work-organizer sync

# 4. Enable automation
pai-email-work-processor setup
```

## 🛠️ Core Tools

### 1. `pai-gmail-work-sync`
- **Purpose**: Direct Gmail API sync for jbyrd@redhat.com
- **Features**: 
  - Red Hat compliance focused
  - Secure OAuth2 authentication
  - Automated refresh token handling
  - Audit logging
- **Usage**: `pai-gmail-work-sync`

### 2. `pai-gmail-work-auth`
- **Purpose**: Authentication setup and management
- **Features**:
  - Interactive OAuth setup
  - Token validation and refresh
  - Red Hat account verification
- **Usage**: 
  - Setup: `pai-gmail-work-auth`
  - Test: `pai-gmail-work-auth test`

### 3. `pai-email-work-processor`
- **Purpose**: Intelligent email processing for TAM workflows
- **Features**:
  - Red Hat approved AI models only
  - Case extraction and tracking
  - Team communication analysis
  - Daily briefing generation
- **Usage**:
  - Full processing: `pai-email-work-processor process`
  - Daily only: `pai-email-work-processor daily`
  - Cases only: `pai-email-work-processor cases`

### 4. `pai-email-work-organizer`
- **Purpose**: Email organization, tagging, and search
- **Features**:
  - Red Hat-specific tagging patterns
  - Notmuch integration for fast search
  - Automated categorization
  - Reporting and analytics
- **Usage**:
  - Full cycle: `pai-email-work-organizer sync`
  - Search: `pai-email-work-organizer search 'tag:urgent'`
  - Reports: `pai-email-work-organizer report`

### 5. `pai-work-email-setup`
- **Purpose**: Complete system setup and management
- **Features**:
  - One-command setup
  - System testing
  - Configuration reset
- **Usage**:
  - Setup: `pai-work-email-setup`
  - Test: `pai-work-email-setup test`
  - Reset: `pai-work-email-setup reset`

## 🏷️ Email Tagging System

The system automatically applies Red Hat-specific tags:

### Business Tags
- **`cases`**: Support case emails, SupportShell notifications
- **`customers`**: External customer communications
- **`tam_team`**: TAM team discussions and updates
- **`urgent`**: High-priority, escalated, or P1 issues
- **`security`**: CVEs, security advisories, RHSA notifications

### Operational Tags
- **`announcements`**: Company-wide announcements
- **`training`**: Learning materials, certifications
- **`internal`**: Internal-only communications
- **`archived`**: Older emails (auto-applied after 1 month)

### Search Tags
- **`unread`**: Unprocessed emails
- **`inbox`**: Active inbox items
- **`work`**: Work-related (applied to all)

## 📊 Reports and Analytics

### Daily Reports
- **Location**: `~/.claude/context/create/outputs/email/work/daily/`
- **Content**:
  - Email volume and distribution
  - High-priority items
  - New cases identified
  - Customer communications
  - Action items and follow-ups

### Organization Reports
- **Tag statistics and trends**
- **Unread message summaries**
- **Urgent item alerts**
- **Customer communication tracking**

## 🔍 Search and Discovery

### Command-Line Search
```bash
# Load work email aliases
source ~/.config/pai/work-email-aliases.sh

# Quick searches
work-email-urgent          # Show urgent emails
work-email-cases           # Show case-related emails
work-email-customers       # Show customer emails
work-email-today           # Show today's emails
work-email-summary         # Show overview

# Advanced searches
pai-email-work-organizer search 'tag:urgent and date:7d..'
pai-email-work-organizer search 'from:customer.com'
pai-email-work-organizer search 'subject:case and tag:unread'
```

### Search Patterns
```bash
# Date filters
date:today                 # Today's emails
date:yesterday             # Yesterday's emails  
date:7d..                  # Last 7 days
date:2024-09-01..2024-09-30  # Date range

# Tag combinations
tag:urgent and tag:unread  # Urgent unread emails
tag:cases and date:today   # Today's case emails
tag:customer and not tag:archived  # Active customer emails

# Content search
subject:escalation         # Subject contains "escalation"
from:*@customer.com        # From customer domain
body:"case number"         # Body contains phrase
```

## 🤖 Automation

### Systemd Services
- **Service**: `pai-email-work-processor.service`
- **Timer**: `pai-email-work-processor.timer` (30-minute intervals)
- **Logs**: `journalctl --user -u pai-email-work-processor.service`

### Management Commands
```bash
# Check status
systemctl --user status pai-email-work-processor.timer

# Stop automation
systemctl --user stop pai-email-work-processor.timer

# Start automation  
systemctl --user start pai-email-work-processor.timer

# View logs
journalctl --user -u pai-email-work-processor.service -f
```

## 🔒 Red Hat Compliance

### AI Model Usage
- **Approved Models**: Granite family only (`granite-3-2-8b-instruct`)
- **Data Processing**: Local processing with approved models
- **External APIs**: Blocked for customer data
- **Audit Logging**: All operations logged via `pai-audit`

### Security Features
- **OAuth2**: Secure authentication with refresh tokens
- **Encrypted Storage**: Credentials stored in `~/.config/pai/secrets/`
- **Audit Trail**: Complete operation logging
- **No External AI**: Customer data never leaves Red Hat infrastructure

### Data Handling
- **Customer Emails**: Processed locally only
- **Internal Communications**: Standard Red Hat handling
- **Sensitive Data**: Flagged and protected
- **Compliance Verification**: Built-in compliance checks

## 📁 Directory Structure

```
~/.claude/context/
├── capture/
│   └── email/
│       └── gmail-jbyrd-redhat/           # Work email storage
│           ├── mail/                     # Email files (maildir format)
│           └── .notmuch/                 # Search database
├── create/
│   └── outputs/
│       └── email/
│           └── work/                     # Work email outputs
│               ├── daily/                # Daily reports
│               ├── cases/                # Case extractions
│               ├── contacts/             # Contact analysis
│               └── projects/             # Project tracking
└── logs/                                 # System logs

~/.config/
├── pai/
│   ├── secrets/                          # OAuth credentials (encrypted)
│   ├── work-email-aliases.sh            # Search aliases
│   └── work-email-quickref.md           # Quick reference
└── notmuch/
    └── work-config                       # Notmuch configuration
```

## 🔧 Troubleshooting

### Authentication Issues
```bash
# Test authentication
pai-gmail-work-auth test

# Re-authenticate
rm ~/.config/pai/secrets/gmail_jbyrd_redhat_token.pickle
pai-gmail-work-auth
```

### Sync Problems
```bash
# Manual sync
pai-gmail-work-sync

# Check network and permissions
curl -s https://www.googleapis.com/gmail/v1/users/me/profile

# Rebuild notmuch database
pai-email-work-organizer setup
```

### Missing Tags
```bash
# Reapply all tags
pai-email-work-organizer tag

# Check notmuch database
export NOTMUCH_CONFIG=~/.config/notmuch/work-config
notmuch new
```

### Automation Not Running
```bash
# Check timer status
systemctl --user status pai-email-work-processor.timer

# Check service logs
journalctl --user -u pai-email-work-processor.service --since "1 hour ago"

# Restart automation
systemctl --user restart pai-email-work-processor.timer
```

## 🔄 Integration with Existing PAI Tools

### Case Management
- **`pai-case-processor`**: Processes extracted cases
- **`pai-supportshell`**: SupportShell integration
- **`pai-hydra`**: Case notification processing

### Communication Tools
- **`pai-email-processor`**: Enhanced with work context
- **`pai-contact-intelligence`**: Contact analysis
- **`pai-meeting-prep`**: Meeting preparation with work emails

### Workflow Integration
- **`pai-my-plate-v3`**: Daily briefings include work email summary
- **`pai-brief-generate`**: Work email insights in daily briefs
- **`pai-audit`**: All work email operations logged

## 📚 Quick Reference

### Daily Workflow
```bash
# 1. Morning email check
work-email-summary

# 2. Review urgent items
work-email-urgent

# 3. Check new cases  
pai-email-work-organizer search 'tag:cases and date:today'

# 4. Process unread emails
work-email-unread | head -20
```

### Weekly Maintenance
```bash
# 1. Generate weekly report
pai-email-work-processor process

# 2. Clean up archived items
pai-email-work-organizer sync

# 3. Review automation logs
journalctl --user -u pai-email-work-processor.service --since "1 week ago"
```

### File Locations
- **Quick Reference**: `~/.config/pai/work-email-quickref.md`
- **Search Aliases**: `~/.config/pai/work-email-aliases.sh`
- **Daily Reports**: `~/.claude/context/create/outputs/email/work/daily/`
- **System Config**: `~/.config/notmuch/work-config`

---

## 🎉 Success!

Your Red Hat work email organization system is now fully configured and integrated with the existing PAI infrastructure. The system provides:

- ✅ **Automated email sync** every 30 minutes
- ✅ **Intelligent tagging** for Red Hat workflows  
- ✅ **Powerful search** with notmuch integration
- ✅ **Daily reporting** and analytics
- ✅ **Full compliance** with Red Hat AI policies
- ✅ **Seamless integration** with existing PAI tools

The system mirrors your personal email organization while maintaining strict Red Hat compliance and security standards.
