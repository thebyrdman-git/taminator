# tsr-workflow-orchestrator

Comprehensive TSR workflow orchestration leveraging existing PAI tools and new TSR analysis capabilities.

## Location
`~/.local/bin/tsr-workflow-orchestrator`

## Description
Master orchestration tool for Technical Service Review workflows. Integrates factual script-based analysis with AI-enhanced insights using existing PAI infrastructure. Coordinates multiple analysis approaches to ensure accurate, comprehensive TSR reports.

## Key Features
- **PAI Tool Integration**: Leverages existing pai-audit, pai-search, fabric tools
- **Factual Analysis First**: Script-based processing for mathematical accuracy
- **AI Enhancement**: Uses fabric patterns for intelligent pattern recognition
- **Quality Assurance**: Multi-step validation and verification
- **Audit Compliance**: Full audit trail using pai-audit logging
- **Knowledge Management**: Automatic pai-search knowledge base updates

## Commands

### Basic Usage
```bash
# Run complete TSR workflow from TSR directory
cd ~/Documents/rh/projects/tam-ocp/discover/strategic/tsr-initial
tsr-workflow-orchestrator discover

# Run with custom TSR directory
tsr-workflow-orchestrator discover --tsr-dir /path/to/tsr/directory
```

## Workflow Steps

### Step 1: Environment Verification
- **Tools Check**: Verifies all required PAI and TSR tools available
- **Data Validation**: Confirms case data directory and file structure
- **Audit Setup**: Initializes pai-audit logging for compliance
- **Progress Tracking**: Establishes progress monitoring

### Step 2: Factual Analysis (Script-Based)
- **Tool**: `tsr-discover-analyzer`
- **Method**: Mathematical processing of ALL case data
- **Output**: Verified SLA metrics, case distributions, statistical summaries
- **Validation**: Cross-checking with source data for accuracy

### Step 3: AI Enhancement (fabric Integration)
- **Tool**: `fabric` with analyze_case pattern
- **Method**: AI pattern recognition on factual analysis results
- **Purpose**: Intelligent insights into technical patterns and root causes
- **Model**: gpt-4o for consistent, reliable analysis

### Step 4: Executive Briefing Generation
- **Method**: Combines factual metrics with AI insights
- **Format**: Customer-presentation ready markdown
- **Content**: Data-driven recommendations and action plans
- **Validation**: Cross-references factual data for accuracy

### Step 5: PAI Knowledge Base Integration
- **Tool**: `pai-search`
- **Purpose**: Store TSR findings for future reference
- **Integration**: Links with existing account knowledge
- **Searchability**: Makes TSR insights available for ongoing work

## PAI Tool Leveraging

### Existing PAI Tools Used
- **pai-audit**: Comprehensive audit logging of all TSR activities
- **pai-search**: Knowledge base storage and retrieval
- **fabric**: AI-powered pattern analysis using proven patterns
- **rhcase**: Case data validation and cross-referencing

### Integration Benefits
- **Consistent Tooling**: Uses familiar PAI workflow tools
- **Audit Compliance**: Maintains audit trail using existing framework
- **Knowledge Persistence**: Stores insights in established knowledge base
- **Quality Assurance**: Leverages proven PAI quality processes

## Quality Assurance Framework

### Factual Accuracy
- **Complete Dataset**: Processes ALL available cases, no sampling
- **Mathematical Precision**: Script-based calculations for SLA metrics
- **Data Validation**: Multiple checks for completeness and accuracy
- **Cross-Verification**: Results can be independently verified

### AI Analysis Quality
- **Factual Foundation**: AI analysis builds on verified factual data
- **Pattern Recognition**: Uses AI for complex pattern identification
- **Insight Generation**: AI provides strategic insights on factual patterns
- **Validation Required**: All AI insights must be validated against source data

### Report Quality
- **Executive Ready**: Professional format suitable for customer presentation
- **Data-Driven**: All conclusions supported by specific metrics
- **Actionable**: Clear, specific recommendations with implementation guidance
- **Verifiable**: All claims can be traced back to source case data

## Integration with TSR-Specific Tools

### New TSR Tools Orchestrated
- **tsr-discover-analyzer**: Factual analysis engine
- **tsr-case-extractor**: Case data extraction (when needed)
- **tsr-sla-analyzer**: Advanced SLA calculation
- **tsr-pattern-analyzer**: Pattern recognition system

### Workflow Coordination
- **Sequential Processing**: Factual analysis first, then AI enhancement
- **Data Flow**: Each step uses outputs from previous steps
- **Quality Gates**: Validation at each step before proceeding
- **Error Handling**: Graceful handling of individual step failures

## Use Cases

### Account Onboarding
```bash
# New TAM account assignment
cd ~/Documents/rh/projects/tam-ocp/[account]/strategic/tsr-initial
tsr-workflow-orchestrator [account]
```

### Quarterly Reviews
```bash
# Regular account performance review
cd ~/Documents/rh/projects/tam-ocp/[account]/strategic/quarterly-review
tsr-workflow-orchestrator [account] --tsr-dir $(pwd)
```

### Issue Investigation
```bash
# Specific problem investigation
cd ~/Documents/rh/projects/tam-ocp/[account]/strategic/issue-investigation
tsr-workflow-orchestrator [account] --focus-period "last-6-months"
```

## Output Deliverables

### For Customer Meetings
- **Executive Briefing**: `DISCOVER_TSR_EXECUTIVE_BRIEFING_[timestamp].md`
- **Factual Metrics**: `analysis/reports/discover_factual_tsr_analysis.md`
- **CSV Data**: `analysis/processed/discover_all_cases_metrics.csv`

### For Internal Use
- **AI Insights**: `analysis/reports/discover_ai_enhanced_analysis.md`
- **Audit Logs**: Stored via pai-audit for compliance
- **Knowledge Base**: Insights stored via pai-search

### For Ongoing Work
- **Methodology**: Reusable workflow for other accounts
- **Templates**: Standardized approach for future TSR work
- **Best Practices**: Documented process for team use

## Performance and Scalability

### Processing Capabilities
- **Large Datasets**: Handles 500+ cases efficiently
- **Time Requirements**: 5-15 minutes for complete workflow
- **Memory Usage**: Optimized for standard development environments
- **Error Resilience**: Continues processing despite individual failures

### Validation Standards
- **Factual Accuracy**: 100% verification requirement for customer-facing metrics
- **Data Completeness**: Reports data quality and coverage statistics
- **Statistical Confidence**: Provides confidence intervals where applicable
- **Reproducible Results**: Consistent output across multiple runs

This orchestrator ensures that TSR analysis is both comprehensive and accurate, leveraging the best of script-based factual analysis and AI-enhanced insights while maintaining integration with existing PAI workflows.