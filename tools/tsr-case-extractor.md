# tsr-case-extractor

Extract and process case details for Technical Service Review analysis.

## Location
`~/.local/bin/tsr-case-extractor.py`

## Description
Comprehensive case data extraction tool for Technical Service Reviews (TSR). Extracts case history from rhcase, processes case details, comments, and attachments, and calculates initial SLA metrics for TAM account assessments.

## Key Features
- **rhcase Integration**: Leverages rhcase tool for comprehensive case data extraction
- **SLA Calculation**: Automatically calculates first response times and SLA adherence
- **Data Processing**: Structures raw case data for analysis workflows
- **Multiple Formats**: Outputs both JSON and CSV for different analysis needs
- **Batch Processing**: Handles large case volumes efficiently

## Commands

### Basic Usage
```bash
tsr-case-extractor.py <account_name>                    # Extract last 12 months
tsr-case-extractor.py <account_name> --months 24        # Extract last 24 months
tsr-case-extractor.py <account_name> --output-dir /path # Custom output location
```

### Examples
```bash
# Extract Discover case history for TSR
tsr-case-extractor.py discover --months 12

# Extract comprehensive history for major account review
tsr-case-extractor.py cibc --months 24 --output-dir analysis/data

# Quick extraction for recent issues
tsr-case-extractor.py citi --months 3
```

## Output Structure

### Raw Data Directory
- `{output-dir}/raw_data/case_{number}_data.json` - Individual case files
- Contains: case details, comments, attachments metadata
- Preserves original rhcase data structure

### Processed Data Directory  
- `{account}_tsr_summary.json` - Overall analysis summary
- `{account}_sla_metrics.csv` - SLA metrics for spreadsheet analysis
- Structured data ready for downstream analysis tools

## SLA Metrics Calculated

### Response Time Analysis
- **First Response Time**: Hours from case creation to first Red Hat response
- **Total Response Count**: Number of Red Hat responses in case
- **Customer Wait Times**: Time between Red Hat responses and customer follow-ups
- **Red Hat Response Times**: Time between customer updates and Red Hat responses

### SLA Targets by Severity
- **Severity 1 (Urgent)**: 1 hour target
- **Severity 2 (High)**: 4 hour target
- **Severity 3 (Medium)**: 8 hour target
- **Severity 4 (Low)**: 24 hour target

### Breach Detection
- Automatically flags cases exceeding SLA targets
- Calculates breach duration and impact
- Identifies patterns in SLA adherence

## Integration Points

### TAM Workflow Integration
- **Input for tsr-sla-analyzer**: Provides structured data for comprehensive SLA analysis
- **Input for tsr-pattern-analyzer**: Raw case data for pattern recognition
- **pai-audit Integration**: Logs all extractions for compliance tracking

### Downstream Tools
- **Excel/CSV Analysis**: Direct import of SLA metrics CSV
- **Business Intelligence**: JSON data for dashboard integration
- **Report Generation**: Structured input for automated report tools

## Technical Details

### Data Sources
- **rhcase tool**: Primary source for case data extraction
- **Case Details**: Basic case information (severity, dates, status)
- **Comments Timeline**: Complete comment history with timestamps
- **Attachments Index**: Attachment metadata and types

### Performance
- **Batch Processing**: Processes multiple cases efficiently
- **Rate Limiting**: Respects rhcase API limits
- **Error Handling**: Continues processing despite individual case errors
- **Progress Tracking**: Real-time progress indication for large extractions

## Error Handling

### Common Issues
- **Account Not Found**: Verify account name in rhcase configuration
- **API Timeouts**: Reduce batch size or extend timeout
- **Permission Issues**: Ensure rhcase authentication is configured
- **Data Format Changes**: Tool adapts to different rhcase output formats

### Troubleshooting
```bash
# Test rhcase connectivity
rhcase list {account} --months 1

# Debug mode for detailed error information
tsr-case-extractor.py {account} --debug

# Verify output directory permissions
ls -la {output-dir}
```

## Use Cases

### TAM Account Onboarding
- Extract complete case history for new account assessment
- Identify historical patterns and recurring issues
- Calculate baseline SLA performance metrics

### Quarterly Business Reviews  
- Generate case volume and response time trends
- Compare SLA performance across time periods
- Identify improvement areas and success stories

### Customer Concern Investigation
- Rapid extraction of relevant case data for specific time periods
- Detailed analysis of response patterns and customer experience
- Evidence-based discussion materials for customer meetings

## Future Enhancements
- **Real-time Monitoring**: Integration with case creation events
- **Predictive Analysis**: Machine learning for pattern prediction
- **Customer Portal Integration**: Direct case portal data access
- **Automated Alerts**: SLA breach notifications and escalations