# correct-ttfr-calculation

Calculate accurate Time to First Response using precise case creation and comment timestamps.

## Location
`~/.local/bin/correct_ttfr_calculation.py`

## Description
Precise TTFR calculation tool that uses exact case creation timestamps from JSON files rather than Salesforce date-only fields. Essential for accurate response time analysis and customer SLA discussions.

## Key Features
- **Precise Timestamp Parsing**: Uses exact ISO timestamps from case JSON files
- **Timezone Handling**: Proper UTC timezone parsing for accurate calculations
- **SBT Integration**: Extracts Service Breach Time (SBT) values from comments
- **Red Hat SLA Validation**: Compares against official Red Hat Premium SLA targets
- **Clean Data Output**: Minimal columns focused on TTFR analysis

## Technical Implementation
### Timestamp Sources
- **Case Creation**: Uses `case_details.createdDate` from JSON (precise to seconds)
- **First Comment**: Uses `case_comments[].createdDate` from first public Red Hat comment
- **Timezone**: All timestamps parsed as UTC for consistent calculation

### SBT (Service Breach Time) Extraction
- **Field**: `sbt` or `sbr` from first Red Hat comment
- **Interpretation**: 
  - Positive value = minutes remaining before SLA breach
  - Negative value = minutes over SLA (breach duration)
  - Used for detailed SLA performance analysis

## Usage
```bash
# Run from TSR directory containing case JSON files
cd ~/Documents/rh/projects/tam-ocp/[account]/strategic/tsr-initial
correct_ttfr_calculation.py

# Prerequisites:
# - discover-long-sla-attainment.csv (Salesforce export)
# - cases/[case_number]/extracts/*.json (case data)
```

## Outputs
- **File**: `discover-sla-ttfr-corrected.csv`
- **Columns Added**:
  - `Case Created (Precise)` - Exact case creation timestamp
  - `First Comment Date` - Timestamp of first public Red Hat comment
  - `TTFR Hours (Corrected)` - Accurate time to first response
  - `SBT Minutes` - Service Breach Time from comment
  - `Met Red Hat SLA` - Yes/No against Premium SLA targets
  - `TTFR Category` - Performance categorization

## Red Hat Premium SLA Compliance
### Official Targets
- Severity 1: 1 hour
- Severity 2: 2 hours
- Severity 3: 4 business hours  
- Severity 4: 8 business hours

### Typical Results
- **Average TTFR**: ~5-50 hours (varies by account)
- **Compliance Rate**: 20-70% (varies by account performance)
- **Best Cases**: Sub-hour response for urgent issues
- **Worst Cases**: Multi-day delays on lower priority

## Customer Meeting Applications
### Addressing Responsiveness Concerns
- **Precise Data**: Exact response times, not estimates
- **SLA Validation**: Against official Red Hat commitments
- **Performance Gaps**: Specific areas needing TAM improvement
- **Accountability**: Real data for honest performance discussions

### TAM Improvement Planning
- **Baseline Metrics**: Current TTFR performance for tracking
- **Target Setting**: Specific TTFR improvements through TAM engagement  
- **Progress Tracking**: Monthly TTFR performance reviews
- **Customer Communication**: Regular TTFR reporting and transparency

This tool provides the accurate foundation for customer discussions about response time performance and TAM engagement improvements.