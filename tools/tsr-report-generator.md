# tsr-report-generator

Generate executive summary reports combining SLA analysis and pattern recognition.

## Location
`~/.local/bin/tsr-report-generator.py`

## Description
Executive report generation tool for Technical Service Reviews. Combines SLA analysis, pattern recognition, and customer context to create comprehensive reports suitable for customer presentations, executive briefings, and strategic planning discussions.

## Key Features
- **Executive Summary Generation**: Professional reports for leadership consumption
- **Multi-Source Integration**: Combines SLA metrics, patterns, and business context
- **Customer Presentation Ready**: Formatted for direct customer sharing
- **Action Plan Generation**: Specific, actionable recommendations
- **Strategic Insights**: Business-focused analysis and implications

## Commands

### Basic Usage
```bash
tsr-report-generator.py <account_name>                  # Generate executive summary
tsr-report-generator.py <account_name> --output-dir path # Custom output location
```

### Examples
```bash
# Generate Discover executive summary
tsr-report-generator.py discover

# Create quarterly review report
tsr-report-generator.py cibc --output-dir quarterly-reviews/

# Generate customer presentation
tsr-report-generator.py citi --format presentation
```

## Report Components

### Executive Summary
- **Key Findings**: High-level insights for executive consumption
- **SLA Performance**: Overall adherence rates and trends
- **Business Impact**: Revenue and operational impact assessment
- **Strategic Recommendations**: Business-aligned improvement actions

### Detailed Analysis Sections
- **SLA Performance Assessment**: Comprehensive response time analysis
- **Issue Pattern Analysis**: Recurring problems and root causes
- **Customer Experience Evaluation**: Support quality and satisfaction indicators
- **Trend Analysis**: Performance trajectory and future projections

### Action Planning
- **Immediate Actions**: Quick wins and urgent improvements
- **Strategic Initiatives**: Long-term improvement programs
- **Resource Requirements**: Staffing and tool recommendations
- **Success Metrics**: Measurable outcomes and KPIs

## Report Formats

### Executive Brief Format
```markdown
# Technical Service Review - [Account]

## Executive Summary
- SLA Adherence: 92.3% overall
- Primary Issues: Authentication (31%), Networking (24%)
- Trend: 15% improvement over last quarter

## Key Recommendations
1. Implement proactive auth monitoring
2. Establish TAM escalation path
3. Create customer-specific runbooks
```

### Detailed Analysis Format
- **Comprehensive Metrics**: Full statistical analysis
- **Case Examples**: Specific cases illustrating patterns
- **Root Cause Analysis**: Deep dive into recurring issues
- **Implementation Roadmap**: Step-by-step improvement plan

### Customer Presentation Format
- **Visual Elements**: Charts and graphs (when tools available)
- **Professional Layout**: Clean, executive-ready formatting
- **Action-Oriented**: Focus on customer value and improvements
- **Discussion Points**: Framework for productive customer dialogue

## Integration Points

### Input Sources
- **tsr-sla-analyzer**: SLA performance data and metrics
- **tsr-pattern-analyzer**: Issue patterns and categorization
- **Account Context**: Customer-specific business context
- **Historical Data**: Previous TSR reports for trend analysis

### Output Integration
- **Customer Meetings**: Direct presentation materials
- **Business Planning**: Strategic planning input data
- **Process Improvement**: Support process enhancement recommendations
- **Account Planning**: TAM account strategy development

## Customization Options

### Report Scope
```bash
# Focus on specific time periods
tsr-report-generator.py discover --period Q3-2025

# Include only high-severity cases
tsr-report-generator.py discover --severity 1,2

# Compare multiple time periods
tsr-report-generator.py discover --compare Q1,Q2,Q3
```

### Audience Customization
```bash
# Executive summary for leadership
tsr-report-generator.py discover --audience executive

# Technical deep-dive for engineers
tsr-report-generator.py discover --audience technical

# Customer presentation format
tsr-report-generator.py discover --audience customer
```

## Key Metrics Generated

### SLA Performance Indicators
- **Overall Adherence Rate**: Percentage meeting all SLA targets
- **Severity-Specific Rates**: Adherence by case severity level
- **Response Time Distribution**: Statistical distribution of response times
- **Breach Analysis**: Detailed SLA violation assessment

### Customer Experience Metrics
- **First Impression Score**: First response time performance
- **Consistency Rating**: Standard deviation and reliability metrics
- **Improvement Trajectory**: Performance trend over analysis period
- **Satisfaction Indicators**: Proxy metrics for customer satisfaction

### Business Impact Assessment
- **Critical Issue Frequency**: Business-critical case occurrence
- **Resolution Efficiency**: Time to resolution for different issue types
- **Escalation Patterns**: Cases requiring management intervention
- **Cost Impact**: Resource utilization and efficiency metrics

## Strategic Applications

### TAM Account Planning
- **Engagement Strategy**: Data-driven approach to customer engagement
- **Resource Allocation**: Optimize support resource assignment
- **Proactive Planning**: Prevent issues based on identified patterns
- **Relationship Building**: Use insights to strengthen customer relationships

### Customer Success
- **Value Demonstration**: Quantify support value and improvements
- **Issue Prevention**: Proactive measures based on pattern analysis
- **Strategic Alignment**: Align support with business objectives
- **Continuous Improvement**: Ongoing optimization of support experience

### Business Development
- **Reference Accounts**: Identify satisfied customers for references
- **Success Stories**: Document support excellence examples
- **Competitive Advantage**: Demonstrate superior support capabilities
- **Account Growth**: Use excellent support to drive account expansion

## Report Distribution

### Internal Stakeholders
- **TAM Management**: Performance review and strategic planning
- **Support Leadership**: Process improvement and resource planning
- **Account Teams**: Customer engagement and relationship building
- **Product Teams**: Feedback on product issues and improvement opportunities

### Customer Stakeholders  
- **Executive Leadership**: Business impact and strategic alignment
- **Technical Teams**: Technical patterns and improvement opportunities
- **IT Management**: Support process optimization and efficiency
- **Procurement**: Support value demonstration and ROI analysis