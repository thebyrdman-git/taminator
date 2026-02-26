# RFE: Template library for reports and customer content

**Source:** TAM feedback (jbyrd) — template library for reports and customer-facing content.

**One-liner:** Add a template library so TAMs can choose and apply shared report/customer content templates and reduce manual editing.

---

## Problem

- No shared, reusable set of templates for reports and customer content; everyone customizes from scratch or ad hoc.
- A curated library would make output more consistent and closer to "customer-ready," reducing manual tweaking.

## Proposed direction

- **Template library:** Curated, versioned templates (e.g. by customer type, product, report type) that users can pick when building or updating reports.
- Templates drive structure, sections, and optional boilerplate so output is closer to customer-ready.

## Scope

**In scope**

- Template storage and selection in the app.
- At least one "blessed" set of templates (e.g. by product/SBR).
- Optional variables/placeholders (customer name, date, etc.).

**Out of scope (for this RFE)**

- Full CMS or complex conditional logic.
- Ansible-driven template execution (see [RFE-ANSIBLE-ORCHESTRATION.md](RFE-ANSIBLE-ORCHESTRATION.md)).

## Implementation notes

*(To be filled when scoping implementation.)*

- Existing report structure (e.g. `report_structure.json`, section_order, section_included) could be extended or mirrored for template definitions.
- Consider: template format (markdown + frontmatter, or JSON schema), versioning, and UI to pick/apply a template.
