# pai-my-plate

Generate daily "My Plate" briefing for TAM responsibilities.

## Location
`~/.local/bin/pai-my-plate`

## Description
Creates a structured daily briefing document that summarizes key TAM responsibilities including breach risks, stale cases, severity changes, RFEs/bugs status, and priority actions.

## Usage
```bash
pai-my-plate
```

## Output
- Creates file at: `~/.claude/pai/create/outputs/briefs/daily/YYYY-MM-DD.md`
- YAML frontmatter with metadata
- Sections for:
  - Breach risk / SBT
  - Stale cases / needs update
  - Severity changes
  - RFEs / Bugs status
  - Priority actions

## Example Output
```markdown
---
title: Daily My Plate (2025-01-07 UTC)
generated: 2025-01-07T12:00:00Z
tags: [daily,myplate]
---

## Breach risk / SBT
(populate from Hydra/SF email later)

## Stale cases / needs update

## Severity changes

## RFEs / Bugs status

## Priority actions
- Review CAP/Watchlist items
- Update stale cases
- Process new severities
```

## Integration Points
- Designed to be populated by email ingestion pipeline
- Can be enhanced with data from rhcase and Salesforce
- Suitable for daily review in Obsidian

## Future Enhancements
- Auto-populate from email/Hydra notifications
- Integrate with rhcase for live data
- Add trend analysis
