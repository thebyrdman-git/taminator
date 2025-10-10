# create-sla-with-escalations

Create SLA performance chart with escalation rates overlay showing case complexity and customer experience indicators.

## Location
`~/.local/bin/create_sla_with_escalations.py`

## Description
Enhanced SLA performance visualization that overlays escalation rates by severity level. Provides insights into case complexity, customer experience issues, and support effectiveness beyond basic SLA metrics.

## Key Features
- **Dual Metrics**: SLA performance + escalation rates by severity
- **Escalation Types**: Tracks both internal (requestManagementEscalation) and external (customerEscalation) escalations
- **Overall Rate**: Summary escalation percentage across all cases
- **Visual Overlay**: Escalation line chart over SLA bar chart for clear comparison

## Escalation Detection
### Internal Escalations (requestManagementEscalation)
- Red Hat internal escalation to management
- Indicates complex technical issues requiring specialist attention
- Shows internal support process effectiveness

### External Escalations (customerEscalation) 
- Customer-initiated escalations
- Indicates customer dissatisfaction or urgency
- Shows customer experience and satisfaction levels

### Combined Analysis
- **Any Escalation**: Either internal OR external escalation
- **Overall Rate**: Total escalation percentage for account health assessment
- **Severity Patterns**: Which severity levels require more escalation

## Usage
```bash
# Run from TSR directory with enhanced data
cd ~/Documents/rh/projects/tam-ocp/[account]/strategic/tsr-initial
create_sla_with_escalations.py

# Prerequisites:
# - discover_final_enhanced_data.csv (with escalation flags)
```

## Chart Output
- **File**: `analysis/charts/kickoff_02_sla_performance.png`
- **Primary Bars**: SLA attainment by severity (left y-axis)
- **Overlay Line**: Escalation rates by severity (right y-axis, red)
- **Summary Box**: Overall escalation rate for account

## Customer Discussion Applications
### Positive Escalation Story (Like Discover)
- **0% Escalation Rate**: Shows effective support without formal escalations
- **Strong SLA Performance**: 95.7% average with no escalations needed
- **Customer Satisfaction**: No external escalations indicates good customer experience
- **Process Effectiveness**: No internal escalations shows support team competence

### Escalation Pattern Analysis
- **High Escalation Rates**: Would indicate process issues or customer dissatisfaction
- **Severity-Specific Patterns**: Identifies which priority levels need attention
- **Trend Analysis**: Changes in escalation rates over time
- **TAM Opportunity**: Areas where TAM engagement prevents escalations

## Integration Benefits
- **Support Quality**: Escalation rates as proxy for support effectiveness
- **Customer Experience**: External escalations indicate satisfaction issues
- **Process Health**: Internal escalations show support process strain
- **TAM Value**: Demonstrates escalation prevention through proactive engagement

For Discover's case, the **0% escalation rate** combined with **95.7% SLA attainment** provides a strong positive story about support quality and customer satisfaction, supporting the overall positive performance narrative for TAM engagement enhancement.