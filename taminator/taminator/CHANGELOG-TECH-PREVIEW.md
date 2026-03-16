# Taminator 2.0.0 — Tech Preview

**Release:** Tech Preview for testing  
**Version:** 2.0.0-tech-preview  
**Status:** For TAM testing and feedback; run from repo (see README)

---

## Summary

This tech preview adds debugging, GitLab issue reporting with debug attachments, external trackers as the source of truth for case/JIRA linking, and full JIRA project mapping so reports work across Ansible, OpenShift, Platform/RHEL, and other Red Hat products.

---

## Debug and troubleshooting

- **Debug options in UI** — Checkbox “Debug: include Hydra/JIRA diagnostics in result” on Check/Update. When enabled, the result includes:
  - Hydra API response summary (SOLR query, numFound, first doc keys)
  - For cases with no JIRA: top-level doc keys and external trackers / attached resources data returned
  - Per-issue JIRA API HTTP status and error/body when not 200
  - When Update uses rhcase fallback: raw stdout/stderr from rhcase
- **Download debug report** — Button to save the current result (including debug output) as `taminator-debug-YYYYMMDD-HHMMSS.txt`.
- **Report issue in GitLab** — Button copies the result to clipboard and opens the GitLab new-issue page so you can paste and attach the debug report.
- **CLI** — `tam-rfe report-issue --gitlab [--debug-report FILE]` opens GitLab new issue and optionally prints debug report content to paste. `tam-rfe check` / `tam-rfe update` with env `TAMINATOR_DEBUG_HYDRA_JIRA=1` (or via UI debug checkbox) enable the same diagnostics.

---

## External trackers as source of truth

- **JIRA from external trackers first** — When discovering cases (Hydra), the linked JIRA ID is taken from the external trackers / attached resources section first, then from the case summary, then from the rest of the doc. This avoids missing links that exist only in external trackers.
- **RFE vs Bug from external trackers** — When the API exposes type/issue_type in external tracker data, that is used to classify RFE vs Bug. Cases with a JIRA link are always included in the report even if the subject line does not contain “[RFE]” or “[bug]”.
- **Explicit external-tracker search** — Code explicitly searches known external-tracker field names (e.g. `case_external_trackers`, `linked_resources`, `case_linked_resource`) and, in debug mode, logs what data was returned for those fields.

---

## JIRA project mapping (authoritative list)

- **Centralized Jira Project Mapping (The Source, TAM Manual)** — We use this as the single source of truth. To determine where an RFE should be submitted, use the comprehensive JIRA and RFE mapping for products there (Centralized JIRA Project Mapping in The Source). It is a community-managed page across all products; if you find an issue, outdated information, or a missing product in the JIRA mapping, flag it and see if you can get it corrected.
- **In Taminator** — All supported JIRA issue keys are driven by that mapping. The list `JIRA_PROJECT_PREFIXES` in `src/taminator/core/hydra_search.py` is used for discovery (Hydra and rhcase), report table parsing (Check/Update), and link formatting. Update that list to stay in sync with The Source.
- **User-defined (niche) mappings** — You can add project keys not in the main documentation by creating `~/.config/taminator/jira_prefixes.txt` with one key per line (e.g. `MYPROJECT`). These are merged with the built-in list so discovery, parsing, and links work for your niche products.
- **Included products** — Ansible (AAP, AAPRFE, ANSTRAT, ACA, ANA), OpenShift (OCPBUGS, OCM, OCMUI, OCPNODE, CRW, GITOPS, SRVKP, OSSM, CNV, KATA, etc.), Platform/RHEL (RHEL, RHELC, RHELAI, RHELAIRFE), and 70+ other project keys.

---

## Other improvements

- **GitLab issue reporting** — Report bugs/features and attach debug output: UI “Report issue in GitLab” or CLI `tam-rfe report-issue --gitlab --debug-report <file>`.
- **Markdown tables** — Table separator row and summary line handling improved; `tam-rfe fix-tables` and injection keep 4-column format (RED HAT JIRA ID | Support Case | Description | Status/Notes) with links.
- **Case overrides** — `CASE_JIRA_OVERRIDES` in `update.py` for known case → JIRA mappings when discovery returns TBD.

---

## How to run the tech preview

**Desktop app (recommended for UI):** Download the AppImage (Linux) or DMG (macOS) from [GitLab releases](https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases). Double-click to launch; Taminator opens in its own app window. No terminal commands required. Windows is not offered.

**From the repository (CLI or development):**

```bash
git clone https://gitlab.cee.redhat.com/jbyrd/taminator.git
cd taminator/taminator
./tam-rfe serve          # Web UI (default http://127.0.0.1:8765)
./tam-rfe check <customer>
./tam-rfe update <customer>
./tam-rfe report-issue --gitlab --debug-report ./debug.txt
```

Requires Red Hat VPN and tokens (JIRA, Portal) configured in the web UI Settings or environment.

---

## Feedback

- **GitLab issues:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues  
- When reporting problems, use “Download debug report” or “Report issue in GitLab” and attach the debug output so we can see what the APIs returned.
