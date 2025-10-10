# create-sbr-technical-patterns

Create technical patterns chart organized by SBR Group assignments with proactive vs reactive breakdown.

## Location
`~/.local/bin/create_sbr_technical_patterns.py`

## Description
Advanced technical patterns visualization that categorizes cases by actual SBR (Support Business Resource) group assignments rather than generic technical categories. Shows meaningful case distribution and workload patterns across support teams.

## Key Features
- **SBR Group Organization**: Uses actual support team assignments from case data
- **Proactive vs Reactive**: Stacked visualization showing case types within each SBR
- **Meaningful Categories**: Eliminates generic "Other" category with specific team assignments
- **Workload Visualization**: Shows support team case distribution and types

## Data Source
- **Enhanced Dataset**: `discover_final_enhanced_data.csv` (includes SBR group data)
- **SBR Field**: Uses first SBR group when multiple groups assigned
- **Proactive Detection**: Identifies proactive cases from problem statement text

## SBR Group Categories (Discover Example)
- **Shift**: 50 cases (general support team)
- **Shift Install Upgrade**: 35 cases (30 proactive - shows planned upgrade support)
- **Shift Networking**: 13 cases (6 proactive - network maintenance)
- **Cloud Management**: 10 cases (cloud platform support)
- **Shift Monitoring**: 6 cases (monitoring/alerting support)
- **Shift Security**: 6 cases (security-related support)
- **Shift Storage**: 6 cases (storage/persistent volume support)

## Usage
```bash
# Run from TSR directory with enhanced data
cd ~/Documents/rh/projects/tam-ocp/[account]/strategic/tsr-initial
create_sbr_technical_patterns.py

# Prerequisites:
# - discover_final_enhanced_data.csv (from fix_sbr_extraction.py)
```

## Chart Output
- **File**: `analysis/charts/kickoff_03_technical_patterns.png`
- **Format**: Horizontal stacked bars (reactive=blue, proactive=orange)
- **Organization**: Cases grouped by actual support team assignments
- **Labels**: Total case counts and breakdown by type

## Customer Discussion Value
### Workload Understanding
- **Team Specialization**: Shows how cases are distributed across specialized teams
- **Proactive Engagement**: Highlights proactive support patterns (especially upgrades)
- **Resource Allocation**: Demonstrates Red Hat's specialized support structure

### TAM Value Demonstration
- **Team Coordination**: TAM can coordinate across multiple SBR groups
- **Proactive Planning**: High proactive case volume shows strategic support value
- **Specialization Access**: TAM provides access to specialized teams as needed

## Integration with TSR Workflow
### Standard Process
```bash
# 1. Extract case data via rhcase
process_cases.fish case_numbers.txt

# 2. Extract SBR and escalation data
fix_sbr_extraction.py

# 3. Create SBR-based technical patterns
create_sbr_technical_patterns.py
```

### Workflow Benefits
- **Accurate Categorization**: Based on actual team assignments vs keyword guessing
- **Meaningful Insights**: Shows real support workload distribution
- **Customer Credibility**: Demonstrates understanding of Red Hat's support structure

This tool transforms generic technical categories into meaningful support team workload visualization that provides valuable insights for customer discussions about Red Hat's specialized support capabilities.