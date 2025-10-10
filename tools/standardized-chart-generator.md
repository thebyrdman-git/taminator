# standardized-chart-generator

Generate professional TSR charts using standardized data sources (casedata.csv + irt.csv).

## Location
`~/.local/bin/standardized_chart_generator.py`

## Description
Streamlined chart generation tool for TSR analysis using standardized CSV file naming and consistent data periods. Uses official Salesforce IRT milestone data for accurate initial response performance analysis.

## Key Features
- **Standardized Inputs**: Uses consistent casedata.csv + irt.csv naming convention
- **Official IRT Data**: Salesforce milestone methodology with business hours/holidays
- **2025 Data Focus**: Consistent time period for accurate analysis
- **Professional Quality**: Executive-ready charts with proper formatting
- **Complete Chart Suite**: 4 essential charts for customer presentations

## Standardized Data Sources
### **casedata.csv** (Salesforce case export)
- Contains: Case Number, SLA Attainment, Severity, Status, Problem Statement
- Purpose: Overall case performance and volume analysis

### **irt.csv** (Salesforce IRT milestone export)  
- Contains: Case Number, Violation flag, Milestone dates
- Purpose: Official first-response performance using Salesforce methodology
- Formula: IRT% = 100 × (1 - AVG(IS_VIOLATED))

## Usage
```bash
# Run from TSR directory containing standardized CSV files
cd ~/Documents/rh/projects/tam-ocp/[account]/strategic/tsr-initial
standardized_chart_generator.py

# Prerequisites:
# - casedata.csv (Salesforce case export)
# - irt.csv (Salesforce IRT milestone export)
```

## Charts Generated
1. **kickoff_01_severity_distribution.png** - Case volume by severity (2025)
2. **sla_vs_irt_comparison.png** - Critical SLA vs IRT performance comparison
3. **kickoff_05_executive_dashboard.png** - Executive summary dashboard
4. **kickoff_02_sla_performance.png** - Clean SLA attainment by severity

## Key Improvements
- **Official IRT Data**: Uses Salesforce milestone methodology (not calculated estimates)
- **Consistent Time Period**: 2025 data only for standardized analysis
- **Proper Terminology**: IRT (Initial Response Time) vs TTFR terminology
- **Data Accuracy**: Official Salesforce exports vs manual calculations

## Integration Benefits
- **Reliable Data**: Official Salesforce milestone tracking
- **Consistent Results**: Standardized inputs produce consistent outputs
- **Customer Credibility**: Uses same metrics customer sees in Salesforce
- **Simplified Workflow**: Two input files vs complex JSON processing

This tool provides the foundation for standardized, replicable TSR analysis using official Salesforce data sources and consistent time periods.