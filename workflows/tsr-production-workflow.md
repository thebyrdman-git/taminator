---
title: "TSR Production Workflow - Complete Process"
category: "workflows" 
created: "2025-09-08T15:00:00Z"
tags: [tsr, production, replicable, tam, kickoff-meetings]
status: "production-ready"
version: "2.0"
---

# TSR Production Workflow - Complete Replicable Process

## Overview
Production-ready Technical Service Review workflow proven with Discover Financial Services. Processes 320+ cases, integrates official Salesforce SLA data, and generates customer-ready presentations.

## Complete Tool Suite (All in ~/.local/bin/)

### **Data Processing Tools**
- `extract_case_csv.py` - Extract all case JSON data to structured CSV
- `quick_sla_summary.py` - Analyze official Salesforce SLA attainment data
- `analyze_sf_sla_data.py` - Advanced Salesforce data processing
- `discover_case_processor.py` - Comprehensive Discover-specific analysis
- `analyze_abandoned_solutions.py` - Abandoned cases solution analysis

### **Chart Generation Tools**
- `simple_chart_generator.py` - Generate 5 core presentation charts
- `regenerate_corrected_charts.py` - Apply corrections and proper colors
- `fix_sla_chart.py` - Fix SLA charts with official data
- `fix_chart_formatting.py` - Fix formatting and readability issues

### **Workflow Orchestration**
- `tsr-workflow-orchestrator` - Master workflow coordination (legacy)

## Standard Execution Process

### **STEP 1: Account Setup**
```bash
# Create account TSR directory
mkdir -p ~/Documents/rh/projects/tam-ocp/[ACCOUNT]/strategic/tsr-initial
cd ~/Documents/rh/projects/tam-ocp/[ACCOUNT]/strategic/tsr-initial

# Create required subdirectories
mkdir -p {scripts,analysis/{charts,reports,processed},cases,agent-responses}
```

### **STEP 2: Data Preparation**
```bash
# Ensure case data structure exists
# Required: cases/[case_number]/extracts/*.json files

# Import Salesforce SLA report (critical for accuracy)
# Required: [account]-long-sla-attainment.csv with "SLA Attainment" column
```

### **STEP 3: Core Analysis**
```bash
# Extract complete case dataset to CSV
extract_case_csv.py
# Creates: analysis/processed/[account]_cases_aggregate.csv

# Analyze official Salesforce SLA performance
quick_sla_summary.py  
# Provides: Real SLA metrics, not calculated estimates
```

### **STEP 4: Chart Generation**
```bash
# Generate initial charts
simple_chart_generator.py
# Creates: analysis/charts/kickoff_*.png

# Apply color corrections (Sev 1=Red, 2=Orange, 3=Green, 4=Blue)
regenerate_corrected_charts.py

# Fix specific formatting issues
fix_chart_formatting.py
# Final output: 5 professional, customer-ready charts
```

### **STEP 5: Validation and Completion**
```bash
# Verify all charts exist and are properly formatted
ls -la analysis/charts/kickoff_*.png

# Verify tools are in PATH for future use
which extract_case_csv.py quick_sla_summary.py simple_chart_generator.py

# Ready for customer presentation
```

## Key Success Factors

### **Data Accuracy**
- **Official Salesforce SLA data** takes priority over calculations
- **Complete dataset** analysis (all available cases)
- **Cross-validation** between multiple data sources
- **Mathematical precision** for customer-facing metrics

### **Professional Quality**
- **Executive-ready charts** with proper formatting
- **Standard color schemes** for consistency
- **Clear data visualization** without overlapping text
- **Professional presentation** suitable for C-level discussions

### **Customer Focus**
- **Address stated concerns** directly with data
- **Present from strength** when performance is good
- **Honest assessment** of improvement areas
- **TAM value proposition** based on concrete improvements

## Proven Results - Discover Case Study

### **Dataset Processed**
- **320 total cases** (complete account history)
- **323 cases** with official SLA tracking
- **January 2024 - Present** (complete recent history)

### **Key Findings**
- **96.0% SLA** for Severity 1 (Urgent) cases
- **88.0% SLA** for Severity 2 (High) cases  
- **94.0% SLA** for Severity 3 (Medium) cases
- **98.1% SLA** for Severity 4 (Low) cases

### **Customer Impact**
- **Data-driven approach** addressed responsiveness concerns
- **Transparent presentation** built customer trust
- **TAM value demonstration** through performance analysis
- **Strategic partnership** foundation established

## Replication for Future Accounts

### **Account-Specific Customization**
1. **Pattern Keywords**: Modify for account-specific technologies
2. **SLA Targets**: Adjust for premium vs standard support levels
3. **Chart Styling**: Customize colors for customer branding
4. **Analysis Focus**: Tailor to specific customer concerns

### **Tool Deployment**
```bash
# All tools ready in PATH for immediate use on any account
cd ~/Documents/rh/projects/tam-ocp/[NEW_ACCOUNT]/strategic/tsr-initial

# Standard workflow execution
extract_case_csv.py                    # Step 1: Data extraction
quick_sla_summary.py                   # Step 2: SLA analysis  
simple_chart_generator.py              # Step 3: Chart generation
fix_chart_formatting.py               # Step 4: Final formatting
```

### **Quality Assurance**
- **Reviewer agent verification** following Grimm System Protocol
- **Data accuracy validation** against official sources
- **Professional presentation standards** for customer meetings
- **Complete documentation** for methodology replication

## Documentation Integration

### **PAI Context Integration**
- **Workflows**: Complete methodology in ~/.claude/context/workflows/
- **Tools**: Individual tool documentation in ~/.claude/context/tools/
- **Knowledge Base**: Lessons learned and best practices stored

### **Tool Availability**
- **PATH Integration**: All tools available from command line
- **Executable Scripts**: Proper permissions and error handling
- **Dependency Management**: Minimal external requirements
- **Cross-Platform**: Compatible across development environments

---

**This workflow is now production-ready and proven for accurate, professional TSR delivery that addresses customer concerns while demonstrating TAM value through data-driven transparency.**