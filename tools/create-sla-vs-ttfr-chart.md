# create-sla-vs-ttfr-chart

Create comparison chart showing Salesforce SLA Attainment vs actual TTFR (Time to First Response) compliance.

## Location
`~/.local/bin/create_sla_vs_ttfr_chart.py`

## Description
Critical analysis tool that reveals the performance gap between Salesforce SLA metrics and actual initial response time performance. Essential for understanding customer responsiveness concerns and explaining perception vs reality gaps.

## Key Features
- **Dual Metric Comparison**: Side-by-side comparison of SLA Attainment vs TTFR Compliance
- **Performance Gap Analysis**: Quantifies the difference between overall and initial response performance
- **Red Hat SLA Validation**: Compares against official Red Hat Premium SLA targets
- **Executive Visualization**: Professional charts for customer discussion
- **Detailed Analytics**: Comprehensive performance breakdown by severity

## Official Red Hat Premium SLA Targets
- **Severity 1 (Urgent)**: 1 hour
- **Severity 2 (High)**: 2 hours  
- **Severity 3 (Normal)**: 4 business hours
- **Severity 4 (Low)**: 8 business hours

## Usage
```bash
# Run from TSR directory with corrected TTFR data
cd ~/Documents/rh/projects/tam-ocp/[account]/strategic/tsr-initial
create_sla_vs_ttfr_chart.py

# Prerequisites:
# - discover-sla-ttfr-corrected.csv (from correct_ttfr_calculation.py)
```

## Outputs
- **Chart**: `analysis/charts/sla_vs_ttfr_comparison.png`
- **Analysis Report**: `analysis/reports/sla_vs_ttfr_analysis.md`

## Key Insights Revealed
- **Performance Gap**: Difference between overall satisfaction and initial responsiveness
- **Customer Perception**: Why customers feel unresponsive despite good overall SLA
- **TAM Opportunity**: Specific areas where TAM engagement improves customer experience
- **Metric Clarity**: Explains different between Salesforce tracking and customer experience

## Chart Components
### Left Panel: Salesforce SLA Attainment
- Shows reported overall case performance
- Typically shows good performance (85-98%)
- Measures complete case lifecycle satisfaction

### Right Panel: TTFR Compliance  
- Shows actual initial response time performance
- Often shows lower performance (37-69%)
- Measures customer's first impression of responsiveness

## Customer Meeting Applications
### Explaining Responsiveness Concerns
**"Your concerns are valid - while overall case satisfaction is high, initial response time performance has gaps. Here's the data that explains your experience."**

### TAM Value Demonstration
- **Specific Problem**: TTFR compliance gaps
- **TAM Solution**: Direct escalation and enhanced initial response
- **Measurable Improvement**: Target TTFR compliance to match SLA attainment levels

This tool provides the foundation for honest, data-driven customer discussions about response time performance and TAM engagement value.