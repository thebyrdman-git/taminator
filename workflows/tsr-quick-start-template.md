---
title: "TSR Quick Start Template"
category: "templates"
created: "2025-09-08T15:45:00Z"
tags: [tsr, template, quick-start, replicable]
status: "production-ready"
version: "1.0"
---

# TSR Quick Start Template - Replicable for Any Account

## 🚀 **30-Minute TSR Setup for Any Account**

### **Prerequisites**
- Account case data in JSON format: `cases/[case_number]/extracts/*.json`
- Salesforce SLA report: `[account]-long-sla-attainment.csv`

### **Quick Setup Commands**
```bash
# 1. Create account TSR structure
mkdir -p ~/Documents/rh/projects/tam-ocp/[ACCOUNT]/strategic/tsr-initial
cd ~/Documents/rh/projects/tam-ocp/[ACCOUNT]/strategic/tsr-initial

# 2. Core analysis (5 minutes)
extract_case_csv.py                    # Extract all case data
correct_ttfr_calculation.py           # Calculate precise TTFR
quick_sla_summary.py                  # Official SLA summary

# 3. Generate charts (10 minutes)
simple_chart_generator.py             # Create 5 core charts
create_sla_vs_ttfr_chart.py          # Critical comparison chart
fix_chart_formatting.py              # Fix formatting issues

# 4. Ready for customer meeting (15 minutes total)
ls analysis/charts/kickoff_*.png     # Verify charts
ls analysis/charts/sla_vs_ttfr_comparison.png    # Verify comparison
```

## 📊 **Standard Deliverables Created**

### **Customer Presentation Charts**
1. **Severity Distribution** - Case volume by priority with proper colors
2. **SLA Performance** - Official Salesforce SLA attainment data
3. **Technical Patterns** - Issue categorization from case analysis
4. **Case Complexity** - Complexity distribution analysis
5. **Executive Dashboard** - 4-panel summary for leadership
6. **SLA vs TTFR Comparison** - Critical performance gap analysis

### **Data Files for Analysis**
- `[account]_cases_aggregate.csv` - Complete case dataset
- `[account]-sla-ttfr-corrected.csv` - TTFR and SBT data
- `analysis/reports/sla_vs_ttfr_analysis.md` - Performance gap analysis

## 🎯 **Customer Meeting Framework**

### **Data-Driven Opening**
*"I analyzed all [X] of your cases using official Salesforce data and precise response time calculations. Here's what I found..."*

### **Key Discussion Points**
1. **Overall Performance**: Salesforce SLA attainment scores
2. **Initial Response Reality**: TTFR compliance with Red Hat targets
3. **Performance Gap**: Why good overall scores feel like poor responsiveness
4. **TAM Solution**: Specific improvements through TAM engagement

### **Specific Metrics to Present**
- **Total Cases Analyzed**: Complete dataset coverage
- **SLA Attainment**: Official Salesforce performance scores  
- **TTFR Compliance**: Actual response time performance
- **Performance Gap**: Percentage difference by severity level

## 🔧 **Customization Points for Different Accounts**

### **SLA Targets by Support Level**
```python
# Premium Support (most enterprise accounts)
premium_sla = {'1': 1, '2': 2, '3': 4, '4': 8}  # hours

# Standard Support
standard_sla = {'1': 2, '2': 4, '3': 8, '4': 16}  # hours
```

### **Performance Thresholds by Customer**
```python
# High-expectation customers
excellence_threshold = 95
good_threshold = 85

# Standard customers
excellence_threshold = 90
good_threshold = 75
```

### **Chart Branding**
```python
# Customer-specific colors
CUSTOMER_COLORS = {
    '1': '#customer_urgent',
    '2': '#customer_high', 
    '3': '#customer_medium',
    '4': '#customer_low'
}
```

## 📈 **Success Metrics**

### **Process Efficiency** 
- **Setup Time**: 30 minutes from raw data to customer presentation
- **Accuracy**: Precise timestamps and official SLA data
- **Professional Quality**: Executive-ready charts and analysis
- **Replicability**: Consistent results across different accounts

### **Customer Impact**
- **Transparency**: Honest, data-driven approach builds trust
- **Issue Validation**: Direct addressing of customer concerns with data
- **TAM Value**: Clear demonstration of TAM engagement benefits
- **Strategic Foundation**: Baseline for ongoing performance improvement

## 🔍 **Quality Assurance Checklist**

### **Before Customer Meeting**
- [ ] All 6 charts generated without formatting errors
- [ ] TTFR calculations use precise JSON timestamps
- [ ] SLA data sourced from official Salesforce reports
- [ ] Performance gap analysis explains customer concerns
- [ ] Charts follow severity color standards (1=Red, 2=Orange, 3=Green, 4=Blue)

### **Data Validation**
- [ ] TTFR values are realistic (minutes/hours, not days for most cases)
- [ ] SLA attainment matches Salesforce official data
- [ ] Case coverage >90% for both SLA and TTFR metrics
- [ ] No cross-account data contamination

### **Professional Standards**
- [ ] Charts suitable for executive presentation
- [ ] Clear, readable text without overlaps
- [ ] Consistent color scheme and formatting
- [ ] Complete dataset analysis (no sampling)

---

**This template enables any TAM to create professional, accurate TSR analysis in 30 minutes with customer-ready presentation materials and data-driven insights for account engagement discussions.**