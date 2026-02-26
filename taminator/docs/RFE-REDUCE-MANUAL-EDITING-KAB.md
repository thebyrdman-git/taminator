# RFE: Reduce manual editing (KAB / starting-point workflow)

**Source:** TAM feedback (rbennett, jbyrd) — KAB as starting point but heavy manual editing before sending to customers; RFE tracking and tooling would cut that down.

**One-liner:** Support KAB (or similar) as a starting point and reduce manual editing before sending to customers via better defaults and integration.

---

## Problem

- TAMs use KAB (or similar) as a starting point but still do a lot of manual editing before sending to customers.
- RFE/case tracking and tooling could reduce that manual tweaking; automation could make the output closer to "send-ready."

## Proposed direction

- Integrate or interoperate with KAB (or similar) so tool output is a better "first draft" for customer-facing content.
- Improve defaults and optional pre-fill so less manual editing is needed before send.

## Scope

**In scope**

- Define integration points (export format, API, or file-based handoff) between Taminator and KAB (or similar).
- Improve default report/output so it is closer to "send-ready."
- Document the workflow (e.g. KAB → Taminator or Taminator → customer send).

**Out of scope (for this RFE)**

- Changing KAB itself.
- Full WYSIWYG editor inside Taminator.

## Implementation notes

*(To be filled when scoping implementation.)*

- Consider: export format (markdown/HTML) that KAB or downstream tools can consume; or import from KAB.
- See also: [KAB_FEATURE_REQUEST_TAMINATOR.md](KAB_FEATURE_REQUEST_TAMINATOR.md) for context on KAB.
