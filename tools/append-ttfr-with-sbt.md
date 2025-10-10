# append-ttfr-with-sbt

Append Time to First Response (TTFR) and Service Breach Time (SBT) data to Salesforce case reports.

## Location
`~/.local/bin/append_ttfr_with_sbt.py`

## Description
Data enhancement tool that extracts first public Red Hat comment timestamps and SBT values from case JSON files and appends them to Salesforce CSV reports for comprehensive response time analysis.

## Key Features
- **TTFR Calculation**: Precise time to first response using exact timestamps
- **SBT Extraction**: Service Breach Time values for SLA analysis
- **Clean Data Output**: Focused on timestamp and SBT data only
- **Red Hat SLA Validation**: Compliance checking against Premium SLA targets
- **Administrative Filter**: Excludes administrative comments from TTFR calculation

## SBT (Service Breach Time) Analysis
### SBT Value Interpretation
- **Positive SBT**: Minutes remaining before SLA breach (e.g., +120 = 2 hours left)
- **Negative SBT**: Minutes over SLA target (e.g., -60 = 1 hour past SLA)
- **Zero SBT**: Exactly at SLA boundary
- **Usage**: Provides precise SLA performance measurement

## Usage
```bash
# Run from TSR directory with Salesforce CSV and case JSON files
cd ~/Documents/rh/projects/tam-ocp/[account]/strategic/tsr-initial
append_ttfr_with_sbt.py

# Prerequisites:
# - [account]-long-sla-attainment.csv (Salesforce export)
# - cases/[case_number]/extracts/*.json (case data)
```

## Output Columns Added
- `First Comment Date` - ISO timestamp of first public Red Hat comment
- `TTFR Hours` - Calculated time to first response  
- `SBT Minutes` - Service Breach Time from comment
- `SBT Interpretation` - Human-readable SBT meaning
- `Met Red Hat SLA` - Yes/No compliance with Premium SLA
- `First Comment Author` - Red Hat associate name

## Administrative Comment Filtering
Excludes comments containing:
- "waiting for response"
- "closing this case" 
- "no response received"
- "please respond"
- "case has been created"
- Other administrative phrases

## Integration Points
### Input Sources
- **Salesforce CSV**: Official case and SLA data
- **Case JSON Files**: Precise timestamps and comment data
- **Red Hat SLA Standards**: Official Premium support targets

### Output Integration
- **correct_ttfr_calculation.py**: Uses this data for precise TTFR analysis
- **create_sla_vs_ttfr_chart.py**: Charts the TTFR vs SLA performance gap
- **Customer Presentations**: Direct data for response time discussions

This tool provides the foundational data layer for accurate TTFR analysis and customer responsiveness discussions based on precise, verifiable timestamps rather than estimates.