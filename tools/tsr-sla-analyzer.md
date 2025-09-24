# tsr-sla-analyzer

Calculate SLA adherence metrics and generate comprehensive performance reports.

## Location
`~/.local/bin/tsr-sla-analyzer.py`

## Description
Advanced SLA performance analysis tool for Technical Service Reviews. Processes case data extracted by tsr-case-extractor to calculate detailed SLA adherence metrics, identify performance trends, and generate executive-ready reports.

## Key Features
- **SLA Calculation Engine**: Comprehensive response time analysis by severity level
- **Trend Analysis**: Identifies performance improvements or degradation over time
- **Statistical Analysis**: Mean, median, standard deviation, and percentile calculations
- **Breach Detection**: Identifies and analyzes SLA violations
- **Executive Reporting**: Professional reports suitable for customer presentation

## Commands

### Basic Usage
```bash
tsr-sla-analyzer.py <account_name>                      # Analyze SLA performance
tsr-sla-analyzer.py <account_name> --data-dir /path     # Custom data directory
```

### Examples
```bash
# Analyze Discover SLA performance
tsr-sla-analyzer.py discover

# Analyze with custom data location
tsr-sla-analyzer.py cibc --data-dir /custom/analysis/data

# Generate report for quarterly review
tsr-sla-analyzer.py citi --output-dir quarterly-reports/
```

## Analysis Components

### First Response Analysis
- **Average Response Time**: Mean time to first Red Hat response
- **Median Response Time**: 50th percentile response time (less affected by outliers)
- **Response Range**: Fastest and slowest response times
- **Standard Deviation**: Consistency measurement of response times

### SLA Adherence Calculation
- **By Severity Level**: Individual analysis for each severity category
- **Overall Adherence Rate**: Aggregate SLA performance across all cases
- **Breach Analysis**: Detailed analysis of SLA violations
- **Target vs Actual**: Comparison of SLA targets to actual performance

### Performance Trends
- **Temporal Analysis**: Response time trends over the analysis period
- **Improvement Detection**: Identifies whether performance is improving or degrading
- **Volume Correlation**: Correlates case volume with response performance
- **Seasonal Patterns**: Identifies patterns related to time periods

## SLA Standards

### Red Hat SLA Targets
```
Severity 1 (Urgent)    : 1 hour
Severity 2 (High)      : 4 hours  
Severity 3 (Medium)    : 8 hours
Severity 4 (Low)       : 24 hours
```

### TAM Enhanced Targets
```
Severity 1 (Urgent)    : 30 minutes
Severity 2 (High)      : 1 hour
Severity 3 (Medium)    : 2 hours  
Severity 4 (Low)       : 4 hours
```

## Report Outputs

### Executive Summary Report
- **Performance Overview**: High-level SLA adherence summary
- **Severity Breakdown**: Detailed analysis by case severity
- **Trend Analysis**: Performance trends and trajectory
- **Recommendations**: Specific improvement actions
- **Customer Presentation**: Professional format suitable for executive review

### Performance Metrics
- **Adherence Rates**: Percentage of cases meeting SLA targets
- **Average Response Times**: By severity and overall
- **Breach Analysis**: Number and severity of SLA violations
- **Comparative Analysis**: Performance vs industry standards

## Integration Points

### Input Sources
- **tsr-case-extractor**: Requires processed case data from extractor
- **CSV Metrics**: Analyzes structured SLA metrics file
- **JSON Summary**: Uses case summary data for context

### Output Integration
- **Business Reports**: Executive-ready markdown reports
- **Data Analysis**: CSV exports for further statistical analysis
- **Dashboard Integration**: JSON data for business intelligence tools
- **Presentation Materials**: Charts and graphs for customer meetings

## Technical Implementation

### Statistical Methods
- **Robust Statistics**: Uses median and IQR to handle outliers
- **Confidence Intervals**: Statistical confidence in reported metrics
- **Trend Analysis**: Time series analysis for performance trends
- **Correlation Analysis**: Identifies factors affecting response times

### Performance Considerations
- **Memory Efficient**: Processes large case datasets without memory issues
- **Optimized Calculations**: Vectorized operations for fast analysis
- **Scalable**: Handles accounts with hundreds of cases efficiently

## Report Customization

### Severity Focus
```bash
# Focus on high-severity cases only
tsr-sla-analyzer.py discover --severity 1,2

# Exclude low-priority cases from analysis  
tsr-sla-analyzer.py discover --exclude-severity 4
```

### Time Period Analysis
```bash
# Compare quarters
tsr-sla-analyzer.py discover --compare-periods Q1,Q2,Q3

# Year-over-year comparison
tsr-sla-analyzer.py discover --compare-years 2024,2025
```

## Use Cases

### TAM Account Assessment
- **New Account Onboarding**: Baseline SLA performance assessment
- **Problem Investigation**: Validate customer concerns about responsiveness
- **Improvement Tracking**: Measure TAM engagement impact on SLA performance

### Customer Meetings
- **Quarterly Reviews**: Present SLA performance trends and improvements
- **Executive Briefings**: High-level performance summaries for leadership
- **Problem Resolution**: Data-driven discussion of support experience

### Internal Reviews
- **Process Improvement**: Identify systemic issues affecting SLA performance
- **Resource Planning**: Understand support load and response capacity
- **Best Practice Sharing**: Identify successful approaches for replication

## Advanced Features

### Comparative Analysis
- **Benchmark Against Portfolio**: Compare account performance to TAM portfolio average
- **Industry Standards**: Compare to published industry SLA benchmarks
- **Historical Comparison**: Track improvement over time periods

### Predictive Elements
- **Trend Projection**: Project future performance based on current trends
- **Risk Identification**: Flag accounts at risk of SLA degradation
- **Improvement Forecasting**: Estimate impact of process improvements