---
title: "TSR Replicable Workflow"
category: "workflows"
created: "2025-09-08T14:45:00Z"
tags: [tsr, replicable, tam, sla-analysis, customer-meetings]
status: "production-ready"
version: "2.0"
---

# TSR (Technical Service Review) Replicable Workflow

## Overview
Complete, replicable methodology for Technical Service Reviews proven with Discover Financial Services (320 cases, official Salesforce SLA data integration).

## Tools Available in PATH (~/.local/bin/)

### **Core TSR Tools**
- `extract_case_csv.py` - Extract all case data to structured CSV
- `quick_sla_summary.py` - Rapid official Salesforce SLA analysis  
- `simple_chart_generator.py` - Professional presentation charts
- `regenerate_corrected_charts.py` - Chart updates with corrections
- `fix_sla_chart.py` - SLA chart fixes with official data
- `analyze_abandoned_solutions.py` - Abandoned cases solution analysis
- `discover_case_processor.py` - Comprehensive case analysis
- `analyze_sf_sla_data.py` - Advanced Salesforce data processing

### **Workflow Orchestration**
- `tsr-workflow-orchestrator` - Master workflow coordination

## Standard Execution for Any Account

### **Step 1: Setup Account TSR Directory**
```bash
# Create directory structure
mkdir -p ~/Documents/rh/projects/tam-ocp/[ACCOUNT]/strategic/tsr-initial/{scripts,analysis/{charts,reports,processed},cases}

# Navigate to working directory
cd ~/Documents/rh/projects/tam-ocp/[ACCOUNT]/strategic/tsr-initial
```

### **Step 2: Data Preparation**
```bash
# Ensure case data is available in: cases/[case_number]/extracts/*.json
# Get official Salesforce SLA report: [account]-long-sla-attainment.csv
```

### **Step 3: Core Analysis**
```bash
# Extract all case data to CSV
extract_case_csv.py
# Output: analysis/processed/[account]_cases_aggregate.csv

# Analyze official SLA performance 
quick_sla_summary.py
# Output: Official SLA metrics and performance assessment
```

### **Step 4: Chart Generation**
```bash
# Generate professional presentation charts
simple_chart_generator.py
# Output: analysis/charts/kickoff_*.png (5 charts)

# Apply corrections and custom styling
regenerate_corrected_charts.py
# Output: Corrected charts with proper colors and official data
```

### **Step 5: Executive Deliverables**
```bash
# Charts ready for customer presentation
ls analysis/charts/kickoff_*.png

# Key deliverables:
# - kickoff_01_severity_distribution.png (Sev 1=Red, 2=Orange, 3=Green, 4=Blue)
# - kickoff_02_sla_performance.png (Official Salesforce SLA data)
# - kickoff_03_technical_patterns.png (Issue categorization)
# - kickoff_04_case_complexity.png (Complexity distribution)
# - kickoff_05_executive_dashboard.png (Complete summary)
```

## Key Methodology Principles

### **1. Official Data Priority**
- Always use Salesforce SLA Attainment field when available
- Script calculations only for backup/validation
- Cross-validate metrics against official sources

### **2. Complete Dataset Analysis**  
- Process ALL available cases, never sample
- Include abandoned/closed cases for complete picture
- Validate data completeness and quality

### **3. Customer-Specific Focus**
- Address stated customer concerns directly
- Tailor analysis to specific account context
- Present from strength when data supports it

## Customization for Different Accounts

### **Pattern Keywords (Modify for Account Context)**
```python
# Standard OpenShift patterns
patterns = {
    'upgrade': ['upgrade', 'update', 'migration'],
    'performance': ['performance', 'slow', 'cpu', 'memory'],
    'networking': ['network', 'dns', 'connectivity'],
    'storage': ['storage', 'pvc', 'volume']
}

# Add account-specific patterns
patterns['customer_specific'] = ['specific_technology', 'custom_app']
```

### **Chart Styling (Company Branding)**
```python
# Modify colors for customer branding
CUSTOM_COLORS = {
    '1': '#company_red',
    '2': '#company_orange', 
    '3': '#company_green',
    '4': '#company_blue'
}
```

### **SLA Targets (Support Level)**
```python
# Premium support targets
premium_sla_targets = {'1': 0.5, '2': 2, '3': 4, '4': 8}

# Standard support targets  
standard_sla_targets = {'1': 1, '2': 4, '3': 8, '4': 24}
```

## Success Criteria

### **For Tomorrow's Meeting**
- [x] 5 professional charts with correct colors and data
- [x] Official Salesforce SLA metrics (not estimates)
- [x] Complete 320-case analysis
- [x] Customer-ready presentation materials

### **For Future Accounts**
- [x] Replicable 5-step workflow
- [x] All tools in PATH for easy execution
- [x] Documentation in PAI context system
- [x] Proven methodology for customer meetings

## Deliverables Summary

**Charts** (analysis/charts/):
1. Severity Distribution (proper color order)
2. SLA Performance (official Salesforce data)  
3. Technical Patterns
4. Case Complexity
5. Executive Dashboard (actual resolution patterns)

**Data** (analysis/processed/):
- Complete case CSV with 26 metrics per case
- Official SLA performance validation
- Pattern analysis and complexity scoring

**Reports** (analysis/reports/):
- Executive summary addressing customer concerns
- Factual analysis based on complete dataset
- TAM engagement recommendations

This workflow is now production-ready and replicable for any TAM account assessment.