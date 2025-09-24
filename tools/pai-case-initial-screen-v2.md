# pai-case-initial-screen-v2

Enhanced case initial screening with AI analysis and workflow integration.

## Location
`~/.local/bin/pai-case-initial-screen-v2`

## Description
Advanced version of the case initial screening tool that follows the proven TAM workflow methodology from workflow.md. Supports both template generation and AI-assisted analysis using Granite 3.2 model with automatic case directory detection across all TAM specialties.

## Features
- **Template Mode**: Generates comprehensive analysis templates
- **AI Mode**: Uses Granite 3.2 for automated case analysis
- **Multi-Specialty Support**: Searches across tam-ocp, tam-ai, and tam-sec
- **Workspace Integration**: Auto-detects case directories
- **Workflow Compliance**: Follows established TAM methodology

## Usage

### Template Mode (Default)
```bash
pai-case-initial-screen-v2
# Creates comprehensive template for manual completion
```

### AI-Assisted Mode
```bash
# Basic AI analysis with case number (auto-detects location)
pai-case-initial-screen-v2 -a -c 04056105

# AI analysis with specific case directory
pai-case-initial-screen-v2 -a -c 04056105 -d /path/to/case/extracts

# Verbose mode to see progress
pai-case-initial-screen-v2 -a -c 04056105 -v
```

## Command Options
- `-a, --ai-mode`: Enable AI-assisted analysis using Granite
- `-c, --case`: Case number to analyze
- `-d, --case-dir`: Directory containing case extracts (optional if case number provided)
- `-v, --verbose`: Verbose output showing progress
- `-h, --help`: Show help message

## Output Structure

### Template Mode Output
Creates a comprehensive template with:
```markdown
---
title: Case Initial Screen - CASE_NUMBER (TIMESTAMP)
tags: [case,initial-screen,CASE_NUMBER]
generated_by: pai-case-initial-screen-v2
ai_assisted: false
---

# Case CASE_NUMBER Initial Screen

## Basic Information
- Case Number: [TO BE FILLED]
- Account: [TO BE FILLED]
- Product: [TO BE FILLED]
- Specialty: [tam-ocp/tam-ai/tam-sec]

## Pre-engagement Checklist
- [ ] Is SBR status correct?
- [ ] Are subscriptions/entitlements valid?
- [ ] Are tags/labels properly set?
- [ ] Is severity appropriate for business impact?

## Problem Analysis
### Incident Timeline
### Detailed Problem Statement
### Root Cause Hypotheses

## Research Steps
### KCS Research
### JIRA/Bug Research

## Initial Action Plan
### Immediate Actions
### Short-term Actions
### Data Collection Requirements
```

### AI Mode Output
When using AI mode with case data, generates:
- **Automated incident timeline** from case history
- **Enhanced problem statement** with business impact analysis
- **Root cause hypotheses** with validation steps and confidence levels
- **Evidence-based analysis** from case comments and interactions
- **Structured research recommendations**

## Integration with TAM Workflow

### Follows Proven Methodology
Based on the workflow documented in workflow.md:
1. **Problem Documentation** - Comprehensive issue analysis
2. **Evidence Gathering** - Multi-source data collection
3. **Hypothesis Development** - Systematic root cause analysis
4. **Validation Planning** - Testable validation criteria
5. **Action Planning** - Structured next steps

### Multi-Specialty Awareness
Automatically detects and works with:
- **tam-ocp**: OpenShift Container Platform cases
- **tam-ai**: Red Hat AI Portfolio cases
- **tam-sec**: Security-focused cases

### Case Directory Auto-Detection
```bash
# Searches across all specialties automatically
pai-case-initial-screen-v2 -a -c 04056105
# Auto-detects: /home/grimm/Documents/rh/projects/tam-ocp/bny/casework/active/04056105/extracts
```

## AI Analysis Capabilities

### Granite 3.2 Integration
- **Incident Timeline Generation**: Extracts chronological events from case data
- **Problem Statement Enhancement**: Improves initial descriptions with case insights
- **Hypothesis Generation**: Creates 3-5 testable root cause theories
- **Validation Planning**: Suggests specific tests and evidence requirements

### Analysis Components
1. **Timeline Analysis**: Chronological sequence of events and interactions
2. **Problem Decomposition**: Technical issue breakdown with business impact
3. **Hypothesis Framework**: Structured theories with supporting evidence
4. **Validation Strategy**: Specific tests to prove/disprove each hypothesis

## Workflow Integration Examples

### Basic Workflow
```bash
# 1. Generate initial analysis
pai-case-initial-screen-v2 -a -c 04056105

# 2. Review and refine the output
# 3. Use generated research commands
rhcase kcs search "relevant terms"
rhcase jira search "related issues"

# 4. Update case analysis based on findings
```

### Integration with pai-workspace
```bash
# Use workspace integration for full workflow
pai-workspace case 04056105 analyze
# Automatically runs pai-case-initial-screen-v2 and saves to case directory
```

## Configuration
Uses Granite 3.2 endpoint and API key from environment:
- `GRANITE_32_API_KEY`: API key for Granite model
- `GRANITE_ENDPOINT`: Model endpoint (defaults to internal Red Hat endpoint)

## Output Locations
- **PAI Directory**: `~/.claude/pai/create/outputs/plans/`
- **Case Integration**: When used with pai-workspace, also saves to case `pieces/` directory
- **Naming**: `case-CASENUMBER-initial-screen-TIMESTAMP.md`

## Best Practices
1. **Use AI Mode**: For active cases with available data
2. **Template Mode**: For new cases without data yet
3. **Verbose Mode**: When debugging or learning the process
4. **Integration**: Use with pai-workspace for full workflow benefits
5. **Iteration**: Update analysis as new evidence emerges

## Comparison with Basic Version

| Feature | pai-case-initial-screen | pai-case-initial-screen-v2 |
|---------|------------------------|---------------------------|
| Template Generation | ✅ Basic checklist | ✅ Comprehensive template |
| AI Analysis | ❌ No | ✅ Granite 3.2 powered |
| Case Auto-Detection | ❌ No | ✅ Multi-specialty search |
| Workflow Compliance | ❌ Basic | ✅ Full workflow.md methodology |
| Output Format | ❌ Simple | ✅ Structured with YAML frontmatter |
| Integration | ❌ Standalone | ✅ pai-workspace compatible |

## Error Handling
- Graceful fallback when API keys not available
- Clear error messages for missing case directories
- Validation of case number format
- Network timeout handling for AI requests
