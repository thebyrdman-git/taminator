# pai-my-plate-v2

Comprehensive daily TAM briefing system with case numbers and lifecycle management.

## Location
`~/.local/bin/pai-my-plate-v2`

## Description
Enhanced daily briefing generator that implements complete TAM workflow automation including case lifecycle management, rhcase integration for all accounts, and AI-enhanced briefing generation with specific case number references.

## Key Features
- **Case Number Tracking**: All briefing sections include specific case numbers
- **Multi-Specialty Support**: Covers tam-ocp, tam-ai, tam-sec
- **Case Lifecycle Management**: Automatically moves resolved cases to resolved/ directories
- **rhcase Integration**: Pulls live case data for each account (bny, cibc, citi, discover)
- **AI Enhancement**: Uses fabric patterns for intelligent briefing generation
- **Automated Scheduling**: Systemd timer support for daily generation

## Commands

### Basic Usage
```bash
pai-my-plate-v2                    # Generate today's briefing (default)
```

### Scheduling
```bash
pai-my-plate-v2 schedule 07:00     # Setup automated daily generation at 7 AM
pai-my-plate-v2 schedule 08:30     # Setup for 8:30 AM daily
```

### Management
```bash
pai-my-plate-v2 stats              # Show briefing statistics and automation status
pai-my-plate-v2 view 2025-01-06    # View briefing for specific date
```

## Output Structure

### Daily Briefing Sections
1. **AI-Generated Briefing**: Enhanced analysis with case numbers
2. **Case Summary by Specialty**: tam-ocp, tam-ai, tam-sec breakdown
3. **Active Case Numbers by Account**: Specific case lists for bny, cibc, citi, discover
4. **Case Lifecycle Management**: Shows cases moved to resolved today
5. **Tools and Resources**: Quick command references
6. **Quick Actions**: Ready-to-use commands for case work

### Example Output
```markdown
# Daily My Plate - 2025-01-07

## AI-Generated Briefing
**Executive Summary**: 3 high-priority cases require attention including Case 04056105 (BNY OpenShift networking) and Case 04123456 (CIBC security vulnerability).

## 🚨 Breach Risk / SBT Items
- Case 04056105 (BNY): OpenShift pods failing - Review cluster config
- Case 04123456 (CIBC): Security vulnerability - Apply patches

## Active Case Numbers by Account
### bny
- Case 04056105
- Case 04234567

### cibc  
- Case 04123456
- Case 04345678

## Case Lifecycle Management
**Cases moved to resolved today**: 2
- Case 04111222 (BNY)
- Case 04333444 (Discover)
```

## Integration Points

### Daily Workflow Integration
- **Called by morning routine**: Part of comprehensive daily workflow
- **Case processor integration**: Runs pai-case-processor for lifecycle management
- **rhcase data**: Pulls live case data with numbers for each account
- **Fabric enhancement**: Uses tam_daily_plate pattern for AI briefing

### Account Processing
Automatically processes these accounts:
- **BNY**: Account 729650 (tam-ocp)
- **CIBC**: Accounts 1216348, 5598345, 6587770 (tam-ocp)
- **Citi**: Account 411070 (tam-ocp)
- **Discover**: Account 999625 (tam-ocp)

### Output Locations
- **PAI Directory**: `~/.claude/context/create/outputs/briefs/daily/`
- **TAM Reports**: `~/Documents/rh/projects/reports/`
- **Naming**: `daily-YYYY-MM-DD.md`

## Automation Features

### Systemd Integration
```bash
# Setup daily automation
pai-my-plate-v2 schedule 07:00

# Check automation status  
systemctl --user status pai-daily-briefing.timer

# View automation logs
journalctl --user -u pai-daily-briefing.service
```

### Data Sources
1. **Case Workspace**: Scans ~/Documents/rh/projects/{tam-ocp,tam-ai,tam-sec}
2. **rhcase API**: Live case data for each account
3. **Audit Logs**: Case movement and analysis tracking
4. **Fabric AI**: Enhanced briefing generation

## Workflow Integration

### Morning Routine
```bash
# Generate comprehensive briefing
pai-my-plate-v2

# Review calendar
pai-calendar summary

# Process emails
pai-email-sync pull
```

### Case Management
```bash
# The briefing identifies cases needing attention
# Follow up with specific case analysis
pai-workspace case 04056105 analyze

# Or run comprehensive case processing
pai-case-processor all
```

## Security and Audit
- All briefing generation logged via pai-audit
- Case movements tracked with timestamps
- Sensitive data handling via redaction patterns
- Audit trail for all automated operations

## Environment Variables
- `DAILY_BRIEF_MODEL`: Model for briefing generation (default: gpt-4o)
- `FABRIC_MODEL`: Fallback model for fabric operations

## Comparison with Basic Version

| Feature | pai-my-plate | pai-my-plate-v2 |
|---------|--------------|-----------------|
| Case Numbers | ❌ No | ✅ Specific case references |
| Account Integration | ❌ Basic | ✅ rhcase live data |
| Lifecycle Management | ❌ No | ✅ Auto-move resolved cases |
| AI Enhancement | ❌ Template only | ✅ Fabric pattern generation |
| Automation | ❌ Manual | ✅ Systemd timer support |
| Multi-Specialty | ❌ No | ✅ tam-ocp/ai/sec support |
