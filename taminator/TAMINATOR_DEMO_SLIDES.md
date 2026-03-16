# Taminator Demo — Slide content for Google Slides

**Import into Google Slides:** Open Google Slides → create a new presentation. For each slide below: Insert → New slide → click the title/body box and paste the content from one "--- SLIDE ---" block (paste as plain text; you can then apply a theme).

**Import into Google Sheets:** Use the file `TAMINATOR_DEMO_SLIDES.csv` → File → Import → Upload → select the CSV. Columns: Slide #, Title, Content (use | as line breaks within a cell for bullets).

---

## SLIDE 1: Title
**Taminator**
RFE & Bug Report Generator for Red Hat TAMs
Demo — [Your name] — [Date]

---

## SLIDE 2: What is Taminator?
**What is Taminator?**
- Generates and maintains RFE and bug reports for Red Hat TAMs
- Uses JIRA and case data → consistent markdown reports
- Can post to customer portal groups
- Typical use: saves 2–3 hours per customer per week vs manual tracking

---

## SLIDE 3: How to get it
**How to get Taminator**
- **Desktop app (recommended):** Download AppImage (Linux) or DMG (macOS) from GitLab releases — double-click to run
- **From repo:** git clone for CLI or development
- **Official:** gitlab.cee.redhat.com/jbyrd/taminator (Red Hat VPN required)

---

## SLIDE 4: No terminal required
**Desktop app — no terminal required**
- Double-click the app; it opens in its own window
- Full UI: Report Manager, Check/Update, Library, Settings, User Guide
- Linux: AppImage | macOS: DMG (Intel + Apple Silicon) | Windows: installer

---

## SLIDE 5: Core workflow
**Core workflow**
1. **Create** a report (Report Manager — add account, SBR Group, account numbers)
2. **Check** report — compare to JIRA (no file changes)
3. **Update** report — write current JIRA statuses into the file (backup created first)
4. **Post** (optional) — post to customer portal group

---

## SLIDE 6: JIRA: Red Hat + Cloud
**JIRA: Red Hat and JIRA Cloud**
- **Red Hat JIRA** (default): issues.redhat.com — use Personal Access Token
- **JIRA Cloud:** e.g. your-tenant.atlassian.net — use Email + API token (id.atlassian.com)
- Set in Settings → Token configuration → JIRA instance
- Same Check/Update flow for both; report links use the configured instance

---

## SLIDE 7: Security & credentials
**Security & credentials**
- Tokens stored in ~/.config/taminator/ui_tokens.json (encoded, not plaintext)
- **Optional:** HashiCorp Vault — set VAULT_ADDR + VAULT_TOKEN; tokens sync to Vault when saved from Settings
- VPN required for Red Hat JIRA (skipped when using JIRA Cloud)

---

## SLIDE 8: Demo outline
**Demo outline**
1. Open Taminator (desktop app)
2. Report Manager — show report creation / accounts
3. Check/Update Reports — run Check or Update on a customer
4. Library — browse report files
5. Settings — VPN check, tokens (JIRA, Portal)
6. User Guide — in-app docs

---

## SLIDE 9: Links & feedback
**Links & feedback**
- **Releases:** gitlab.cee.redhat.com/jbyrd/taminator/-/releases
- **User guide (README):** Same repo — front page
- **Issues / feedback:** gitlab.cee.redhat.com/jbyrd/taminator/-/issues

---

## SLIDE 10: Q&A
**Questions?**

Taminator — RFE and Bug Report Generator for Red Hat TAMs
