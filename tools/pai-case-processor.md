# pai-case-processor

Automated case lifecycle and comprehensive analysis following workflow.md methodology.

## Location
`~/.local/bin/pai-case-processor`

## Description
Implements the complete TAM case analysis workflow across all specialties and accounts. Automatically ensures all active cases have proper analysis structure following the proven methodology from workflow.md, including timeline, problem statement, hypotheses, and research.

## Core Functionality

### Case Lifecycle Management
- **Resolved Case Movement**: Automatically moves cases from active/ to resolved/ when no longer in rhcase list
- **Analysis Verification**: Ensures all cases have required analysis files
- **Structure Creation**: Uses pai-workspace to create proper directory structure

### Comprehensive Analysis
For each case, generates:
1. **Initial Analysis**: Uses pai-case-initial-screen-v2 with AI
2. **Timeline**: Incident timeline from case data
3. **Problem Statement**: Detailed problem analysis
4. **Root Cause Hypotheses**: Testable theories with validation steps
5. **Research**: KCS and JIRA search results
6. **Knowledge Base**: Adds analysis to searchable KB

## Commands

### Account Processing
```bash
pai-case-processor account <specialty> <account>
# Examples:
pai-case-processor account tam-ocp bny
pai-case-processor account tam-ai cibc
```

### Individual Case Analysis
```bash
pai-case-processor case <specialty> <account> <case_number>
# Example:
pai-case-processor case tam-ocp bny 04056105
```

### Bulk Processing
```bash
pai-case-processor all             # Process all accounts across all specialties
pai-case-processor report          # Generate daily case analysis report
```

## Analysis Workflow Per Case

### Step 1: Structure Verification
- Ensures case directory exists with proper structure
- Creates directories if missing: extracts/, pieces/, kcs/, jira/, etc.

### Step 2: Data Export
- Uses rhcase to export case data to extracts/case.json
- Handles export failures gracefully

### Step 3: AI Analysis
- Runs pai-case-initial-screen-v2 in AI mode
- Moves analysis output to case pieces/ directory

### Step 4: Research Automation
- Extracts keywords from case data using fabric
- Searches KCS articles with rhcase kcs search
- Searches JIRA issues with rhcase jira search
- Saves results to kcs/ and jira/ directories

### Step 5: Analysis Artifacts
- Generates timeline from case data
- Creates detailed problem statement
- Develops root cause hypotheses
- All using fabric patterns for consistency

### Step 6: Knowledge Integration
- Adds case analysis to pai-search knowledge base
- Logs all activities via pai-audit

## Case Lifecycle Management

### Resolved Case Detection
- Compares local case directories with rhcase list output
- Cases not in rhcase list are considered resolved
- Automatically moves to resolved/ with timestamp

### Directory Structure
```
~/Documents/rh/projects/{specialty}/{account}/casework/
├── active/
│   └── {case_number}/
│       ├── extracts/
│       ├── pieces/
│       ├── kcs/
│       └── jira/
└── resolved/
    └── {case_number}-resolved-YYYYMMDD/
```

## Integration Points

### Daily Briefing Integration
- Called by pai-my-plate-v2 for comprehensive case processing
- Provides case analysis data for daily briefings
- Tracks resolved case movements

### TAM Workspace Integration
- Uses pai-workspace for case structure creation
- Integrates with existing directory organization
- Preserves TAM workflow patterns

### Tool Dependencies
- **rhcase**: Case data export and research
- **pai-workspace**: Directory structure management
- **pai-case-initial-screen-v2**: AI analysis generation
- **fabric**: Pattern-based analysis enhancement
- **pai-search**: Knowledge base integration
- **pai-audit**: Comprehensive logging

## Account Mappings
Processes these accounts automatically:
- **tam-ocp**: bny, cibc, citi, discover
- **tam-ai**: (ready for future accounts)
- **tam-sec**: (ready for future accounts)

## Output Locations
- **Case Analysis**: `~/Documents/rh/projects/{specialty}/{account}/casework/active/{case}/pieces/`
- **Knowledge Base**: `~/.claude/context/knowledge/cases/`
- **Reports**: `~/.claude/context/create/outputs/reports/`

## Error Handling
- Graceful handling of rhcase export failures
- Skips already-analyzed cases to avoid duplication
- Logs all failures and successes via pai-audit
- Continues processing even if individual cases fail

## Performance Considerations
- Processes cases in parallel where possible
- Skips analysis for cases already completed
- Uses efficient case detection algorithms
- Minimizes API calls through caching

## Security Features
- All case data processing logged
- Sensitive data handling via fabric redaction
- No external data exposure
- Audit trail for all case movements

## Usage Examples

### Daily Automation
```bash
# Process all accounts (typically called by pai-my-plate-v2)
pai-case-processor all

# Generate detailed report
pai-case-processor report
```

### Specific Account Focus
```bash
# Process just BNY cases
pai-case-processor account tam-ocp bny

# Analyze specific case comprehensively
pai-case-processor case tam-ocp bny 04056105
```

### Integration with Other Tools
```bash
# Complete workflow
pai-case-processor all
pai-my-plate-v2
pai-calendar summary
```
