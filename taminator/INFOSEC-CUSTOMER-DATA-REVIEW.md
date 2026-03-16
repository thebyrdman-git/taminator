# Infosec alert: customer data exposure

**If infosec reported customer data on "taminator.dev":** that hostname does not appear in this repository. It may be a deployed instance (e.g. GitHub Pages, internal server, or docs site) that is serving content from this repo or from config that contains customer data. **Immediate actions:** identify what taminator.dev is, take it down or restrict access, and remove/redact the exposed data from the deployed content.

## Customer-related data found in this repository

The following types of data appear in **committed** files and would be present in any clone or deployed copy of the repo:

| Type | Examples in repo | Where |
|------|------------------|--------|
| Customer names | Wells Fargo, TD Bank, JPMC, Fannie Mae | READMEs, docs, examples, design docs, config |
| Red Hat account numbers | 838043, 1912101, 334224, 1460290 | Source code, config, examples, templates, scripts |
| Portal group IDs | 4357341, 7028358, 6956770, 7095107 | Source code, config, examples, docs |
| Case/discussion URLs | access.redhat.com/groups/4357341/... | Source code, config, examples |

### High-impact locations (code and config)

- `taminator/taminator/README.md` — Supported Customers table (names + group IDs + account numbers)
- `taminator/config/weekly_troubleshooting_schedule.yaml` — group_id and customer references
- `taminator/taminator/src/` — rfe_discussion_api_client, tam_call_notes_poster, weekly_discussion_poster, enhanced_group_id_discovery, automated_group_id_extractor, account_based_group_discovery, redhat_cppg_api_client, active_case_report_system
- `taminator/taminator/src/rfe_verification_system.py` — hardcoded account in rhcase command
- `taminator/bin/` — tam-rfe-chat, tam-rfe-auto-detect, tam-rfe-api-test, tam-rfe-template-customizer
- `taminator/examples/WELLS-FARGO-EXAMPLE.md`, `TD-BANK-EXAMPLE.md` — full account/group details
- `taminator/templates/rfe_bug_report_standardized.md` — account number
- Root-level case/account docs: `CASE_04369905_WELLS_FARGO_*.md`, `CASE_04380749_*.md`, etc.

### Documentation / design (example text)

- Many docs use "Wells Fargo", "TD Bank", "JPMC" as example customers in narrative or UI mockups. These are still customer names and may need to be replaced with generic placeholders (e.g. "Customer A", "Example Bank") for any public or shared deployment.

## Recommended remediation

1. **taminator.dev**  
   - Determine what serves that hostname (GitHub Pages, internal host, etc.).  
   - Take the site down or restrict access until content is redacted.  
   - Remove or redact customer names, account numbers, group IDs, and case URLs from deployed content.

2. **Repository sanitization**  
   - Replace real customer names with placeholders (e.g. "Example Customer", "Customer A").  
   - Replace real account numbers and group IDs with placeholders (e.g. `ACCT_EXAMPLE`, `GROUP_ID_EXAMPLE`) or load them from config that is **not** committed (e.g. `~/.config/taminator/` or env).  
   - Keep examples and docs useful by using consistent placeholders and a short note that real IDs go in local config only.

3. **Prevention**  
   - `.gitignore` already blocks many customer-name and case-number patterns.  
   - Add or tighten pre-commit / CI checks to block commits containing known account numbers or group IDs.  
   - Document in CONTRIBUTING or SECURITY that customer names and identifiers must not be committed.

## Next steps

- [ ] Identify and secure taminator.dev (take down or restrict; redact deployed data).  
- [ ] Run sanitization pass on the repo (replace real identifiers with placeholders).  
- [ ] Review and strengthen pre-commit/CI for customer data.  
- [ ] Report back to infosec with actions taken and remaining controls.
