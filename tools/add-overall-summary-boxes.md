# add-overall-summary-boxes

Add overall performance summary boxes to SLA vs IRT comparison charts for quick executive reference.

## Location
`~/.local/bin/add_overall_summary_boxes.py`

## Description
Chart enhancement tool that adds overall performance summary boxes below SLA and IRT charts for immediate executive reference. Provides quick visual summary of key metrics without requiring detailed chart analysis.

## Key Features
- **Overall SLA Summary**: Average SLA attainment across all cases
- **Overall IRT Summary**: IRT performance using official Salesforce methodology
- **Visual Enhancement**: Color-coded boxes for quick executive consumption
- **Professional Formatting**: Clean presentation suitable for customer meetings

## Usage
```bash
# Run from TSR directory with combined data
cd ~/Documents/rh/projects/tam-ocp/[account]/strategic/tsr-initial
add_overall_summary_boxes.py

# Prerequisites:
# - discover_combined_data.csv (from join_case_and_irt_data.py)
```

## Output Enhancement
- **Green Box (SLA)**: Overall SLA attainment percentage and case count
- **Coral Box (IRT)**: Overall IRT performance percentage and case count
- **Quick Reference**: Executive can see summary without detailed chart analysis

## Integration
- Final step in chart generation pipeline
- Enhances readability for executive presentations
- Provides immediate context for detailed severity-level data