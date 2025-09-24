# run-tsr-analysis

Complete automated Technical Service Review workflow.

## Location
`~/.local/bin/run-tsr-analysis.sh`

## Description
Comprehensive automation script that orchestrates the complete Technical Service Review process. Combines case extraction, SLA analysis, pattern recognition, and executive report generation into a single, streamlined workflow for TAM account assessments.

## Key Features
- **End-to-End Automation**: Complete TSR process from data extraction to final reports
- **Error Handling**: Robust error handling with graceful degradation
- **Progress Tracking**: Real-time progress indication throughout analysis
- **Deliverable Organization**: Automatically organizes outputs for presentation
- **Quality Assurance**: Validates outputs at each step

## Commands

### Basic Usage
```bash
run-tsr-analysis.sh <account_name>                      # Complete TSR with defaults
run-tsr-analysis.sh <account_name> <months>             # Specify analysis period
```

### Examples
```bash
# Complete Discover TSR analysis
run-tsr-analysis.sh discover

# Analyze last 24 months of CIBC cases
run-tsr-analysis.sh cibc 24

# Quick 6-month analysis for urgent review
run-tsr-analysis.sh citi 6
```

## Workflow Steps

### Step 1: Case Data Extraction
- **Tool**: `tsr-case-extractor.py`
- **Purpose**: Extract comprehensive case history from rhcase
- **Output**: Raw case data in JSON format
- **Validation**: Confirms case count and data completeness

### Step 2: SLA Performance Analysis  
- **Tool**: `tsr-sla-analyzer.py`
- **Purpose**: Calculate detailed SLA adherence metrics
- **Output**: SLA performance report and metrics CSV
- **Validation**: Confirms metric calculation and report generation

### Step 3: Pattern Recognition Analysis
- **Tool**: `tsr-pattern-analyzer.py`  
- **Purpose**: Identify recurring issues and case categorization
- **Output**: Pattern analysis report and categorized data
- **Validation**: Confirms pattern detection and categorization

### Step 4: Executive Report Generation
- **Tool**: `tsr-report-generator.py`
- **Purpose**: Create comprehensive executive summary
- **Output**: Executive report combining all analyses
- **Validation**: Confirms report completeness and formatting

### Step 5: Deliverable Organization
- **Purpose**: Organize outputs for easy access and presentation
- **Actions**: Copy key files to summary directory
- **Output**: Consolidated deliverables folder
- **Validation**: Confirms all required files present

## Output Structure

```
analysis/
├── reports/                    # Executive reports
│   ├── {account}_tsr_sla_report.md
│   ├── {account}_pattern_analysis.md
│   └── {account}_tsr_executive_summary.md
├── summary/                    # Key deliverables
│   ├── {account}_tsr_sla_report.md
│   ├── {account}_pattern_analysis.md
│   └── {account}_sla_metrics.csv
└── processed/                  # Analysis data
    ├── {account}_tsr_summary.json
    └── {account}_pattern_analysis.json

extract/
├── raw_data/                   # Original case data
│   └── case_{number}_data.json
└── processed/                  # Structured metrics
    └── {account}_sla_metrics.csv
```

## Integration Points

### TAM Workflow Integration
- **Pre-Meeting Prep**: Complete analysis before customer meetings
- **Quarterly Reviews**: Regular performance assessment automation
- **Account Onboarding**: New account assessment and baseline establishment
- **Issue Investigation**: Rapid analysis for problem investigation

### PAI System Integration
- **pai-audit**: Logs all TSR activities for compliance tracking
- **pai-search**: Stores insights in knowledge base
- **fabric**: Enhances analysis with AI-powered insights
- **pai-workspace**: Links with account case management

## Quality Assurance

### Validation Checks
- **Data Completeness**: Verifies required data files exist
- **Metric Accuracy**: Cross-validates SLA calculations
- **Report Integrity**: Confirms all report sections generated
- **File Organization**: Ensures proper directory structure

### Error Recovery
- **Graceful Degradation**: Continues analysis despite individual step failures
- **Partial Results**: Generates reports with available data
- **Clear Error Messages**: Specific guidance for troubleshooting
- **Resume Capability**: Can restart from failed steps

## Performance Characteristics

### Execution Time
- **Small Accounts** (<50 cases): 2-5 minutes
- **Medium Accounts** (50-200 cases): 5-15 minutes  
- **Large Accounts** (200+ cases): 15-30 minutes

### Resource Usage
- **Memory**: Efficiently handles large case datasets
- **CPU**: Optimized for batch processing
- **Disk**: Temporary storage for intermediate results
- **Network**: Minimal - works with local rhcase cache

## Customization Options

### Analysis Scope
```bash
# Include closed cases for comprehensive history
run-tsr-analysis.sh discover 12 --include-closed

# Focus on specific severity levels
run-tsr-analysis.sh discover 12 --severity 1,2

# Exclude certain issue types
run-tsr-analysis.sh discover 12 --exclude performance,monitoring
```

### Output Customization
```bash
# Generate presentation-ready format
run-tsr-analysis.sh discover 12 --format presentation

# Include detailed case examples
run-tsr-analysis.sh discover 12 --include-examples

# Create customer-specific recommendations
run-tsr-analysis.sh discover 12 --customer-focus
```

## Use Cases

### Account Onboarding
- **New TAM Assignment**: Complete account assessment for new TAM
- **Baseline Establishment**: Create performance baseline for future comparison
- **Issue History**: Understand historical support challenges
- **Relationship Planning**: Data-driven customer engagement strategy

### Performance Reviews
- **Quarterly Reviews**: Regular account performance assessment
- **Annual Planning**: Strategic planning input and metrics
- **Process Improvement**: Support process optimization insights
- **Team Performance**: TAM and support team effectiveness measurement

### Customer Meetings
- **Executive Briefings**: Data-driven customer presentations
- **Technical Reviews**: Detailed technical discussion materials
- **Strategic Planning**: Customer strategic planning input
- **Issue Resolution**: Historical context for current problems

## Success Metrics

### Process Efficiency
- **Analysis Time**: Reduced from days to hours
- **Report Quality**: Consistent, professional output
- **Data Accuracy**: Validated metrics and calculations
- **Actionability**: Clear, specific recommendations

### Business Impact
- **Customer Satisfaction**: Improved through data-driven insights
- **Issue Prevention**: Proactive identification of potential problems
- **Strategic Value**: Enhanced TAM strategic contribution
- **Competitive Advantage**: Superior support analytics capability

## Troubleshooting

### Common Issues
- **rhcase Configuration**: Ensure rhcase tool properly configured
- **Python Dependencies**: Verify pandas and required libraries installed
- **File Permissions**: Check write permissions for output directories
- **Case Data Format**: Validate case data structure and format

### Debug Mode
```bash
# Run with detailed debugging
run-tsr-analysis.sh discover 12 --debug

# Verbose output for troubleshooting
run-tsr-analysis.sh discover 12 --verbose

# Test individual components
tsr-case-extractor.py discover --test
```