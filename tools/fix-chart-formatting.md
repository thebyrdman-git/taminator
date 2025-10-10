# fix-chart-formatting

Fix chart formatting and readability issues for professional customer presentations.

## Location
`~/.local/bin/fix_chart_formatting.py`

## Description
Chart formatting repair tool that addresses common visualization issues like overlapping text, inadequate headroom, and data clarity problems. Essential for creating professional, customer-ready presentation materials.

## Key Features
- **Text Overlap Resolution**: Fixes overlapping labels and percentages
- **Headroom Management**: Ensures adequate space for all chart elements
- **Data Clarity**: Removes misleading or incorrect data displays
- **Professional Polish**: Creates executive-ready chart formatting

## Fixes Applied
1. **SLA Chart**: Removes incorrect overall average boxes that obscure data
2. **Complexity Chart**: Adds adequate headroom for text labels
3. **Executive Dashboard**: Improves pie chart readability and text positioning

## Usage
```bash
# Run from TSR directory after initial chart generation
cd ~/Documents/rh/projects/tam-ocp/[account]/strategic/tsr-initial
fix_chart_formatting.py
```

## Integration
- Final step in chart generation pipeline
- Ensures all charts meet professional presentation standards
- Addresses common matplotlib formatting limitations for business presentations