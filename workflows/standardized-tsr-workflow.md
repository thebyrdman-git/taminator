---
title: "Standardized TSR Workflow"
category: "workflows"
created: "2025-09-08T16:45:00Z"
tags: [tsr, standardized, irt, official-data, 2025]
status: "production-ready"
version: "4.0"
---

# Standardized TSR Workflow - Official Salesforce Data

## Overview
Streamlined TSR methodology using standardized CSV naming and official Salesforce milestone data. Eliminates manual calculations in favor of official IRT (Initial Response Time) tracking.

## Standardized Data Sources

### **Required Files**
- `casedata.csv` - Salesforce case export with SLA Attainment data
- `irt.csv` - Salesforce IRT milestone export with Violation flags

### **Data Consistency**
- **Time Period**: Single year focus (2025) for accurate analysis
- **Official Metrics**: Salesforce SLA Attainment and IRT milestone data
- **Account Specific**: No cross-account data contamination

## Simplified 3-Step Workflow

### **Step 1: Data Preparation**
```bash
# Export from Salesforce:
# 1. Case report with SLA Attainment → save as casedata.csv
# 2. IRT milestone report with Violation flags → save as irt.csv

# Place in TSR directory:
cd ~/Documents/rh/projects/tam-ocp/[account]/strategic/tsr-initial/
```

### **Step 2: Chart Generation**
```bash
# Generate all charts with standardized data
standardized_chart_generator.py

# Output: 4 professional charts ready for customer presentation
```

### **Step 3: Customer Presentation**
```bash
# Charts ready in: analysis/charts/
# - severity distribution (2025 data)
# - SLA vs IRT comparison (official methodology)
# - SLA performance by severity
# - Executive dashboard summary
```

## Key Advantages Over Complex Workflow

### **Simplified Process**
- **2 CSV files** vs complex JSON processing
- **3 steps** vs 6-step workflow  
- **Official data** vs calculated estimates
- **5 minutes** vs 30 minutes setup time

### **Data Accuracy**
- **Salesforce IRT**: Official milestone methodology with business hours
- **SLA Attainment**: Official Salesforce tracking
- **No Calculations**: Uses official data vs error-prone timestamp parsing
- **Customer Credibility**: Same metrics customer sees in Salesforce

### **Professional Quality**
- **Executive Charts**: 300 DPI, proper formatting
- **Consistent Terminology**: IRT vs TTFR consistency
- **Official Metrics**: Salesforce methodology vs custom calculations
- **Clean Presentation**: Professional appearance for customer meetings

## IRT Methodology (Official Salesforce)

### **Salesforce IRT Formula**
```
IRT% = 100 × (1 - AVG(IS_VIOLATED))
```

### **Milestone-Based Calculation**
- **Start Date**: Milestone start (business rules applied)
- **Target Date**: SLA deadline with business hours/holidays
- **Completion Date**: When first response milestone completed
- **Violation Flag**: 1 if missed target, 0 if met

### **Business Logic Applied**
- **Business Hours**: Working hours only (excludes nights/weekends)
- **Holiday Calendar**: Company holidays excluded from SLA clock
- **Pause Conditions**: SLA paused during "Waiting on Customer"
- **Completion Criteria**: Official milestone completion events

## Discover Results with Standardized Data

### **Dataset (2025)**
- **Total Cases**: 130 cases (casedata.csv)
- **IRT Milestone Cases**: 129 cases (irt.csv)
- **Coverage**: 99.2% IRT data availability

### **Performance Metrics**
- **Overall IRT**: 90.7% (official Salesforce milestone methodology)
- **SLA Attainment**: 88-98% by severity (official Salesforce data)
- **Industry Comparison**: Above average performance levels

### **Customer Discussion**
- **Strong Foundation**: 90.7% IRT provides excellent baseline
- **Performance Enhancement**: TAM engagement to achieve 95%+ targets
- **Communication Improvement**: Address perception vs performance gaps

## Tool Deployment

### **Standardized Tool** (in ~/.local/bin/)
- `standardized_chart_generator.py` - Complete chart generation with official data

### **Documentation** (in ~/.claude/context/)
- **tools/standardized-chart-generator.md** - Tool documentation
- **workflows/standardized-tsr-workflow.md** - Complete workflow guide

## Replication for Any Account

### **Standard Setup**
```bash
# 1. Create TSR directory
mkdir -p ~/Documents/rh/projects/tam-ocp/[ACCOUNT]/strategic/tsr-initial

# 2. Export Salesforce data to standard names
# - Case report → casedata.csv
# - IRT milestone report → irt.csv

# 3. Generate charts
cd ~/Documents/rh/projects/tam-ocp/[ACCOUNT]/strategic/tsr-initial
standardized_chart_generator.py

# 4. Ready for customer presentation
ls analysis/charts/kickoff_*.png
```

### **Quality Assurance**
- **Data Validation**: Official Salesforce sources only
- **Time Period**: Consistent data period (typically current year)
- **Professional Standards**: Executive-ready chart quality
- **Terminology**: Consistent IRT vs TTFR usage

---

**This standardized workflow provides reliable, professional TSR analysis using official Salesforce data with minimal manual processing and maximum customer credibility.**