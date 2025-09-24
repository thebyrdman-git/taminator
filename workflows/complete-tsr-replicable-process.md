---
title: "Complete TSR Replicable Process"
category: "workflows"
created: "2025-09-08T15:30:00Z"
updated: "2025-09-08T15:30:00Z"
tags: [tsr, replicable, ttfr, sla-analysis, tam, customer-meetings]
status: "production-ready"
version: "3.0"
author: "TAM Workflow System"  
priority: "critical"
---

# Complete TSR (Technical Service Review) Replicable Process

## Overview
Production-ready, comprehensive Technical Service Review methodology proven with Discover Financial Services. Processes complete case datasets, integrates official Salesforce SLA data, calculates precise Time to First Response (TTFR), and generates professional customer presentation materials.

## Complete Tool Suite (All in ~/.local/bin/)

### **Core Data Processing**
- `extract_case_csv.py` - Extract all case JSON data to structured CSV
- `correct_ttfr_calculation.py` - Calculate precise TTFR with timezone handling
- `quick_sla_summary.py` - Analyze official Salesforce SLA attainment data
- `append_ttfr_with_sbt.py` - Add TTFR and SBT data to Salesforce CSV

### **Chart Generation & Formatting**
- `simple_chart_generator.py` - Generate 5 core presentation charts
- `create_sla_vs_ttfr_chart.py` - Critical SLA vs TTFR comparison chart
- `fix_chart_formatting.py` - Fix text overlap and formatting issues
- `final_sla_chart_fix.py` - Apply final chart corrections
- `fix_dashboard_final.py` - Executive dashboard with proper formatting

### **Comprehensive Analysis**
- `discover_case_processor.py` - Complete case pattern analysis
- `analyze_abandoned_solutions.py` - Abandoned cases solution identification
- `analyze_sf_sla_data.py` - Advanced Salesforce data processing

### **Workflow Orchestration**
- `tsr-workflow-orchestrator` - Master workflow coordination

## Standard 6-Step Replication Process

### **STEP 1: Account Setup**
```bash
# Create TSR directory structure
mkdir -p ~/Documents/rh/projects/tam-ocp/[ACCOUNT]/strategic/tsr-initial/{scripts,analysis/{charts,reports,processed},cases,agent-responses}

cd ~/Documents/rh/projects/tam-ocp/[ACCOUNT]/strategic/tsr-initial
```

### **STEP 2: Data Collection**
```bash
# Required data sources:
# 1. Case JSON files: cases/[case_number]/extracts/*.json
# 2. Salesforce SLA report: [account]-long-sla-attainment.csv (with SLA Attainment column)
```

### **STEP 3: Core Data Processing**
```bash
# Extract all case data to structured CSV
extract_case_csv.py
# Output: analysis/processed/[account]_cases_aggregate.csv

# Calculate precise TTFR with official SLA validation
correct_ttfr_calculation.py  
# Output: [account]-sla-ttfr-corrected.csv

# Quick SLA summary from official data
quick_sla_summary.py
# Output: Console summary of real SLA performance
```

### **STEP 4: Chart Generation**
```bash
# Generate core presentation charts
simple_chart_generator.py
# Output: analysis/charts/kickoff_01-05_*.png

# Create critical SLA vs TTFR comparison
create_sla_vs_ttfr_chart.py
# Output: analysis/charts/sla_vs_ttfr_comparison.png

# Apply final formatting corrections
fix_chart_formatting.py && final_sla_chart_fix.py && fix_dashboard_final.py
# Output: Professional, customer-ready charts
```

### **STEP 5: Comprehensive Analysis** (Optional for detailed reports)
```bash
# Complete pattern analysis
discover_case_processor.py
# Output: analysis/reports/[account]_complete_tsr_analysis.md

# Abandoned cases solution analysis
analyze_abandoned_solutions.py
# Output: analysis/reports/[account]_abandoned_cases_analysis.md
```

### **STEP 6: Validation & Documentation**
```bash
# Verify all deliverables
ls analysis/charts/kickoff_*.png    # Should show 5 charts
ls analysis/charts/sla_vs_ttfr_comparison.png    # Critical comparison chart
ls [account]-sla-ttfr-corrected.csv    # TTFR data for analysis

# Ready for customer presentation
```

## Critical Success Factors Learned from Discover

### **1. Use Precise Timestamps**
- **Problem**: Salesforce date-only fields cause calculation errors
- **Solution**: Extract exact ISO timestamps from case JSON files
- **Result**: Accurate TTFR calculations (minutes vs false hours)

### **2. Official SLA Data Priority**
- **Problem**: Calculated SLA estimates can be wrong
- **Solution**: Always use Salesforce "SLA Attainment" field when available
- **Result**: Credible metrics for customer discussion

### **3. TTFR vs SLA Attainment Gap**
- **Discovery**: Customers feel "unresponsive" despite good overall SLA scores
- **Root Cause**: Initial response time (TTFR) vs overall case satisfaction gap
- **Solution**: Present both metrics and address TTFR specifically

### **4. Professional Chart Quality**
- **Problem**: Overlapping text, incorrect target lines, poor formatting
- **Solution**: Multiple chart correction scripts for professional presentation
- **Result**: Executive-ready materials suitable for C-level presentations

## Deliverable Standards

### **For Customer Kickoff Meeting**
- **6 Professional Charts**: Including critical SLA vs TTFR comparison
- **Precise TTFR Data**: Accurate response time analysis
- **Official SLA Metrics**: Credible Salesforce data integration
- **Performance Gap Analysis**: Explains customer experience vs reported metrics

### **For TAM Ongoing Work**
- **Baseline Performance**: Established TTFR and SLA baselines
- **Improvement Targets**: Specific areas for TAM enhancement
- **Customer Context**: Complete understanding of customer experience
- **Tracking Framework**: Monthly performance review capability

### **For Future Account Replication**
- **Complete Tool Suite**: All scripts tested and documented
- **Standard Process**: 6-step replicable workflow
- **Quality Assurance**: Proven methodology with validation steps
- **Professional Standards**: Executive-ready deliverable quality

## Key Metrics Framework

### **TTFR Analysis Standards**
- **Data Source**: Precise JSON timestamps, not Salesforce date-only fields
- **SLA Targets**: Official Red Hat Premium SLA commitments
- **Performance Categories**: Excellent, Good, Acceptable, Delayed, Poor
- **Customer Impact**: Address initial response perception issues

### **SLA Attainment Integration**
- **Official Source**: Salesforce SLA Attainment field
- **Cross-Validation**: Compare with TTFR calculations for accuracy
- **Performance Baseline**: Overall case satisfaction metrics
- **Gap Analysis**: Identify perception vs performance disconnects

## Proven Results - Discover Case Study

### **Dataset Processed**
- **323 cases** with official SLA tracking
- **292 cases** with precise TTFR calculations (90.4% coverage)
- **271 cases** with SBT data (83.9% coverage)
- **Complete analysis** from January 2024 - Present

### **Key Performance Gaps Identified**
- **Severity 1**: 96% SLA Attainment vs 69% TTFR Compliance (-27% gap)
- **Severity 2**: 88% SLA Attainment vs 48% TTFR Compliance (-40% gap)
- **Severity 3**: 94% SLA Attainment vs 43% TTFR Compliance (-51% gap)
- **Severity 4**: 98% SLA Attainment vs 37% TTFR Compliance (-61% gap)

### **Customer Experience Insights**
- **Overall Satisfaction**: Good (88-98% SLA attainment)
- **Initial Response**: Poor (37-69% TTFR compliance)
- **Customer Concern**: Validated by TTFR data, not contradicted by SLA data
- **TAM Opportunity**: Close the performance gap through enhanced initial response

## Customization for Different Accounts

### **Account-Specific Adjustments**
```python
# Modify SLA targets for different support levels
premium_targets = {'1': 1, '2': 2, '3': 4, '4': 8}     # Premium Support
standard_targets = {'1': 2, '2': 4, '3': 8, '4': 16}   # Standard Support

# Customize performance categories
excellent_threshold = 90  # Premium accounts
good_threshold = 75      # Standard accounts
```

### **Chart Customization**
```python
# Company branding colors
CUSTOM_COLORS = {'1': '#brand_red', '2': '#brand_orange', '3': '#brand_green', '4': '#brand_blue'}

# Performance thresholds
excellence_line = 95     # Industry leading
target_line = 90        # Good performance
minimum_line = 75       # Acceptable performance
```

## Quality Assurance Standards

### **Data Accuracy Requirements**
- **Timestamp Precision**: Use exact ISO timestamps, not date-only fields
- **SLA Target Validation**: Against official Red Hat SLA documentation
- **Cross-Metric Validation**: Compare TTFR with SLA attainment for consistency
- **Customer Data Integrity**: Account-specific analysis only

### **Professional Presentation Standards**
- **Chart Quality**: 300 DPI resolution for crisp presentation
- **Text Readability**: No overlapping labels or obscured data
- **Color Standards**: Consistent severity color scheme across all charts
- **Executive Ready**: Suitable for C-level customer presentations

---

**This process transforms ad-hoc TSR work into systematic, replicable methodology that consistently delivers accurate, customer-ready assessments addressing both perception and performance realities through TAM engagement.**