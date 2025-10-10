# pai-calendar

Google Calendar integration and meeting preparation for TAM workflows.

## Location
`~/.local/bin/pai-calendar`

## Description
Integrates Google Workspace calendar with PAI system to provide meeting preparation, attendee research, and calendar awareness for daily TAM workflows.

## Setup
```bash
# One-time setup
pai-calendar auth
# Opens browser for Google OAuth authentication
```

## Daily Workflow Integration

### Morning Routine
```bash
# Get today's meeting overview
pai-calendar summary

# Generate preparation for specific meeting
pai-calendar prep "Customer Sync Meeting"

# Include in daily briefing
pai-my-plate-v2  # Automatically includes calendar summary
```

## Commands

### Calendar Access
- `pai-calendar today [date]` - Show meetings for specific date (default: today)
- `pai-calendar agenda [days]` - Show upcoming meetings (default: 7 days)
- `pai-calendar summary [date]` - Generate daily calendar summary with prep status

### Meeting Preparation
- `pai-calendar prep <meeting_title>` - Generate comprehensive meeting preparation
- Includes:
  - Meeting analysis for TAM relevance
  - Attendee research using perplexity
  - Technical preparation checklist
  - Relevant case numbers and account context
  - Quick command references

### Authentication
- `pai-calendar auth` - Setup Google Calendar OAuth (one-time)

## Meeting Preparation Features

### Automatic Analysis
For each meeting, generates:
1. **Meeting type identification** (customer call, internal sync, escalation)
2. **Attendee research** (roles, companies, technical expertise)
3. **Account context** (relevant cases, technical history)
4. **Preparation checklist** with specific action items
5. **Quick commands** for gathering relevant information

### Example Preparation Output
```markdown
# Meeting Preparation: Customer Technical Review

## Meeting Analysis
- Type: Customer technical review
- Account: BNY Bank
- Technical focus: OpenShift networking issues
- Priority: High (production impact)

## Attendee Research
### john.smith@bnybank.com
- Role: Senior Infrastructure Engineer
- Expertise: Kubernetes, OpenShift, networking
- Decision authority: Technical implementation

## Preparation Checklist
- [ ] Review cases 04056105, 04123456 (OpenShift networking)
- [ ] Prepare KCS articles on OpenShift SDN troubleshooting
- [ ] Gather recent cluster health data
- [ ] Review account technical history

## Quick Commands
pai-workspace case 04056105 info
rhcase kcs search "OpenShift networking"
```

## Integration Points

### Daily Briefing Integration
- Called by `pai-my-plate-v2` for calendar awareness
- Meeting prep status included in daily briefings
- Automatic identification of customer vs internal meetings

### TAM Workflow Integration
- Links meeting topics to relevant cases
- Suggests account-specific preparation materials
- Integrates with knowledge base for meeting context

### AI Enhancement
- Uses fabric patterns for meeting analysis
- Perplexity research for attendee intelligence
- Contact dossier creation for relationship building

## Output Locations
- **Daily summaries**: ~/.claude/context/create/outputs/calendar/daily/
- **Meeting prep**: ~/.claude/context/create/outputs/calendar/prep/
- **Meeting analysis**: ~/.claude/context/create/outputs/calendar/meetings/

## Security and Privacy
- Only accesses calendar metadata and meeting details
- Attendee research uses publicly available information only
- All research activities logged via pai-audit
- No personal or sensitive calendar data stored permanently

## Requirements
- Google Workspace account access
- gcalcli installed (automatically done)
- OAuth authentication (browser-based, one-time)
- Internet access for attendee research
