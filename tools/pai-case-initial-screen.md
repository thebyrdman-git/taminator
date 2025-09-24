# pai-case-initial-screen

Generate initial screening plan for new support cases.

## Location
`~/.local/bin/pai-case-initial-screen`

## Description
Creates a structured initial screening document for TAMs to use when first engaging with a new support case. Includes checklists, clarifying questions, and action plan templates.

## Usage
```bash
pai-case-initial-screen
```

## Output
- Creates file at: `~/.claude/pai/create/outputs/plans/case-initial-screen-TIMESTAMP.md`
- YAML frontmatter with metadata
- Checklist items for case validation
- Template for action plans

## Example Output
```markdown
---
title: Case Initial Screen (2025-01-07T12:00:00Z)
tags: [case,initial-screen]
---

Checklist:
- Is SBR correct?
- Are subscriptions/tags/severity correct?
- Clarifying questions prepared?
- Attach KCS/Jira links?

Outputs:
- Basic understanding of issue and business impact
- KCS/Jira references
- Action Plan next steps
```

## Integration Points
- Designed to work with case data from rhcase
- Can be enhanced with KCS/Jira lookups
- Integrates with TAM workflow documentation

## Usage Workflow
1. Run when assigned a new case
2. Fill out checklist items
3. Add case-specific details
4. Use as reference during initial customer contact

## Future Enhancements
- Auto-populate from case data
- Integrate with rhcase for automatic KCS/Jira lookups
- Add severity-specific checklists
