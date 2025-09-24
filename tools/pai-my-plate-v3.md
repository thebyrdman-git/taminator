# pai-my-plate-v3

Enhanced daily TAM briefing system with CLI email integration and intelligent case sync tracking.

## Location
`~/.local/bin/pai-my-plate-v3`

## Description
Next-generation daily briefing generator that builds on v2 with:
- **Native CLI email tools**: Uses notmuch, email-search, email-cat for 10x faster email processing
- **Smart sync tracking**: Prevents redundant case syncs within 30-minute windows
- **Enhanced email metrics**: Detailed email statistics and customer communication tracking
- **Improved performance**: Faster email searches and better error handling

## Key Enhancements Over v2

| Feature | v2 | v3 |
|---------|----|----|
| Email Processing | pai-email-processor | notmuch + CLI tools |
| Search Speed | ~5-10s | <1s |
| Sync Tracking | ❌ Always syncs | ✅ Smart 30-min cache |
| Email Metrics | ❌ Basic | ✅ Comprehensive stats |
| Customer Email Tracking | ❌ Limited | ✅ Full sender analysis |
| Error Handling | ⚠️ Some unbound vars | ✅ Fixed and robust |

## Commands

### Basic Usage
```bash
pai-my-plate-v3                    # Generate today's briefing
pai-my-plate-v3 help              # Show all commands and options
```

### Sync Management
```bash
pai-my-plate-v3 stats             # Show statistics and sync status
pai-my-plate-v3 force-sync        # Force case sync regardless of time
pai-my-plate-v3 quick             # Quick mode - skip all syncing
```

### Scheduling & Viewing
```bash
pai-my-plate-v3 schedule 07:00    # Setup automated daily generation
pai-my-plate-v3 view 2025-01-06   # View briefing for specific date
pai-my-plate-v3 test              # Test mode - minimal processing
```

## Case Sync Tracking

### How It Works
- Tracks last sync time in `~/.claude/context/state/last-case-sync.timestamp`
- Automatically skips sync if run within 30 minutes
- Saves significant time when running multiple times
- Force sync available when needed

### Sync Behavior
```
First run:       Full sync → Updates tracker
Within 30 min:   Skip sync → Use cached data
After 30 min:    Full sync → Updates tracker
Force sync:      Always sync → Updates tracker
```

## Enhanced Email Features

### Email Search Integration
```bash
# Direct case search from briefing
email-search "case 04056105"

# Find urgent customer emails
email-search "date:today AND urgent AND from:@bny.com"

# Extract email content
email-cat "case 04056105" | grep -A10 "problem"
```

### Email Metrics Section
- Total emails (7-day window)
- Unread count with visual indicators
- Today's email volume
- Customer email breakdown
- Top customer contacts
- Case-related email tracking
- Flagged/urgent email alerts

### Customer Email Analysis
- High-priority customer emails with action items
- Case number extraction from email bodies
- Sender identification and tracking
- Action item extraction
- SLA warning for old unread emails

## Output Enhancements

### New Sections in Daily Briefing
1. **📊 Email Metrics**: Comprehensive email statistics
2. **🔴 High Priority Customer Emails**: Urgent customer communications
3. **🟡 Internal Collaboration**: Team emails requiring attention
4. **🚀 Quick Email Actions**: Ready-to-use email commands
5. **Case Sync Status**: Shows if sync was skipped

### Example Enhanced Output
```markdown
## 📊 Email Metrics (Last 7 Days)
- **Total Emails**: 1,234
- **Unread**: 42
- **Today**: 18
- **Customer Emails**: 127

### Top Customer Contacts
- john.doe@bny.com: 15 emails
- jane.smith@cibc.com: 12 emails

## 🔴 High Priority Customer Emails

### Re: Case 04056105 - Network Outage
- **From**: john.doe@bny.com
- **Date**: today
- **Cases**: 04056105
- **Actions Required**:
  - Please provide update on cluster status
  - Need ETA for resolution

## Case Sync Status
(Using cached data - last sync 15 minutes ago)
```

## Integration with New Email Tools

### Helper Scripts Used
- `email-search`: Fast notmuch-based email search
- `email-cat`: Extract email content to stdout
- `email-summary`: Generate email statistics

### Prerequisites
```bash
# Install email CLI tools
~/.claude/context/config/email/quickstart-neomutt.sh

# Ensure gmailieer is syncing
gmi sync
```

## Performance Improvements

### Sync Optimization
- Case sync: ~2-5 minutes → Cached (0 seconds)
- Prevents redundant rhcase API calls
- Reduces file system operations
- Maintains accuracy with 30-minute window

### Email Processing
- Search time: 5-10s → <1s
- Direct notmuch queries vs subprocess calls
- Streaming processing vs full email loads
- Indexed search vs linear scan

## Cron Job Updates

The cron job at 8am Eastern (13:00 UTC) now uses v3:
```cron
# PAI Daily Plate (8am Eastern - 1 hour before workday)
0 13 * * * /home/grimm/.local/bin/pai-my-plate-v3
```

Benefits:
- Morning run uses fresh sync
- Subsequent manual runs use cache
- Saves time during work hours

## Troubleshooting

### Sync Not Working
```bash
# Check sync status
pai-my-plate-v3 stats

# Force sync if needed
pai-my-plate-v3 force-sync

# Remove tracker to reset
rm ~/.claude/context/state/last-case-sync.timestamp
```

### Email Metrics Missing
```bash
# Ensure notmuch database is initialized
notmuch setup
notmuch new

# Check email sync
gmi sync
```

### Performance Issues
```bash
# Use quick mode for testing
pai-my-plate-v3 quick

# Check what's taking time
time pai-my-plate-v3 test
```

## Environment Variables
- `DAILY_BRIEF_MODEL`: Model for briefing generation (default: gpt-4o)
- `FABRIC_MODEL`: Fallback model for fabric operations
- `OPEN_EDITOR`: Set to "true" to auto-open briefing in editor

## Migration from v2

1. **Update cron**: Already updated to use v3
2. **Install email tools**: Run quickstart script
3. **First run**: Will create sync tracker automatically
4. **Backwards compatible**: All v2 features still work

## Future Enhancements

Potential improvements:
- Configurable sync timeout (currently 30 min)
- Per-account sync tracking
- Email template responses
- Case priority scoring
- Meeting extraction from .ics files
- Slack/Teams integration
