# RFE: Ansible orchestration for template library and report operations

**Source:** TAM feedback (jbyrd) — orchestrate back-end with Ansible Core; template library could be driven by Ansible playbooks.

**One-liner:** Enable Ansible to orchestrate template application and report/backend operations via CLI or API.

---

## Problem

- Back-end and template operations are manual or script-only; some TAMs want to drive them from Ansible for consistency, audit, and automation.

## Proposed direction

- Expose key operations (e.g. "apply template X," "refresh report for account Y," "publish to portal") as something Ansible can call: CLI, local API, or small REST API.
- Optionally: template library updates (add/update templates) driven or validated by Ansible playbooks.

## Scope

**In scope**

- Documented CLI or API that Ansible can invoke (e.g. `tam-rfe` subcommands or a small HTTP API).
- At least one concrete use case (e.g. "run report update for these accounts" or "apply template and generate report").
- Optional: Ansible playbook examples or a small example repo.

**Out of scope (for this RFE)**

- Building a full Ansible collection.
- Changing how the UI runs the same operations.

## Implementation notes

*(To be filled when scoping implementation.)*

- Build on existing CLI (`tam-rfe` check, update, etc.); ensure all operations needed for automation are available and script-friendly.
- Template library (see [RFE-TEMPLATE-LIBRARY.md](RFE-TEMPLATE-LIBRARY.md)) would be a natural dependency for "apply template" from Ansible.
