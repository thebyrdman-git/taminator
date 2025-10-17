# Template Customization Strategy

## Vision: Make Template Creation Accessible to All TAMs

TAMs should be able to customize their email reports without editing YAML files or understanding technical details.

## Three-Tier Approach

### 1. Google Form (Easiest - Recommended for most TAMs)
**Target users:** All TAMs, especially those new to automation

**Features:**
- Simple web form with dropdowns and checkboxes
- Pre-populated with common options
- Real-time preview of what the template will look like
- Submit and template is auto-generated
- Shareable - see what other TAMs are using

**Google Form Fields:**
- Template Name
- Report Type (dropdown): Comprehensive, Minimal, Priority-Focused, Executive
- Summary Metrics (checkboxes): Total Cases, RFEs, Bugs, High Priority, Aging Cases, etc.
- Case List Options:
  - Max cases to show (dropdown): 5, 10, 20, 50, All
  - Sort by (dropdown): Priority, Age, Last Update, Severity
  - Fields to include (checkboxes): Case#, Title, Severity, Age, Owner, etc.
- Analysis Sections (checkboxes): Aging Analysis, Priority Breakdown, Trends, Action Items
- Alert Thresholds:
  - Alert on cases older than (days): 7, 14, 30, 60, 90
  - Alert on high priority increase: Yes/No
- Email Format:
  - Include HTML formatting: Yes/No
  - Color-code by priority: Yes/No
  - Include charts/graphs: Yes/No

**Backend:**
- Google Sheet as database
- Sync script runs every 15 minutes (cron)
- Converts Sheet rows to YAML templates

### 2. Interactive CLI Wizard (Medium - For Power Users)
**Target users:** TAMs comfortable with command line

**Tool:** `tam-rfe-template-wizard`

```bash
tam-rfe-template-wizard

Welcome to Template Customizer!

What type of template do you want to create?
1. Comprehensive (all case details)
2. Minimal (quick status)
3. Priority-focused (high priority only)
4. Executive (trends and metrics)
5. Custom (build from scratch)

> 5

Let's build your custom template!

Template name: My Weekly Review

What summary metrics do you want?
☑ Total Cases
☑ High Priority Cases
☐ RFEs
☐ Bugs
☑ Aging Cases (>30 days)
☐ Resolved this week
☐ New this week

[Continue...]
```

### 3. Direct YAML Editing (Advanced - Maximum Control)
**Target users:** Advanced users, automation developers

**Files:**
- `~/.config/rfe-tool/email-templates.yaml` - User templates
- `$RFE_TOOL/config/email-templates.yaml` - System templates

**Benefits:**
- Complete control
- Can use YAML anchors, variables, complex logic
- Version control friendly
- Works offline

## Implementation Plan

### Phase 1: Google Form Integration ✅ **START HERE**

1. **Create Google Form**
   - Design form with all template options
   - Add logic to show/hide fields based on selections
   - Add description/help text for each option

2. **Create Google Sheet Backend**
   - Auto-populate from form responses
   - Add validation columns
   - Add "Sync Status" column

3. **Build Sync Script: `tam-rfe-template-sync`**
   ```bash
   #!/usr/bin/env python3
   # Syncs Google Sheets templates to local YAML
   
   - Authenticate with Google Sheets API
   - Fetch new/updated templates
   - Convert to YAML format
   - Validate template structure
   - Save to ~/.config/rfe-tool/email-templates.yaml
   - Send confirmation email to TAM
   ```

4. **Add to Cron**
   ```
   */15 * * * * tam-rfe-template-sync
   ```

### Phase 2: Interactive Wizard

1. **Build `tam-rfe-template-wizard`**
   - Use `dialog` or Python `rich` for TUI
   - Step-by-step prompts
   - Live preview
   - Save to YAML

2. **Add template validation**
   - Check for required fields
   - Validate field names
   - Test email generation

### Phase 3: Template Library

1. **Shared Template Repository**
   - Public Google Sheet of community templates
   - Browse and import templates created by other TAMs
   - Rate/comment on templates
   - "Featured Templates" section

2. **Template Discovery**
   ```bash
   tam-rfe-template-browse
   
   Featured Templates:
   1. "Priority Focus" by jsmith - 45 users
   2. "Executive Summary" by ajones - 38 users
   3. "Daily Quick Check" by mwilson - 27 users
   
   Import template #1? (y/n)
   ```

## Google Form Design

### Section 1: Template Basics
- **Name your template:** ___________
- **Description (optional):** ___________
- **Based on existing template:** [Dropdown: Start Fresh, Comprehensive, Minimal, etc.]

### Section 2: Summary Metrics
**Which metrics do you want in the summary?**
- ☐ Total open cases
- ☐ Feature requests (RFEs)
- ☐ Bugs
- ☐ High priority cases
- ☐ Aging cases (>30 days)
- ☐ Resolved this week
- ☐ New this week
- ☐ Average age of cases

### Section 3: Case List
**How many cases to show:** [Dropdown: 5, 10, 20, 50, All]
**Sort cases by:** [Dropdown: Priority, Age, Last Update, Severity]
**Fields to include:**
- ☑ Case number
- ☑ Title
- ☑ Priority
- ☐ Status
- ☐ Age (days)
- ☐ Last update
- ☐ Component
- ☐ Owner
- ☐ Customer contact

### Section 4: Analysis
**Include these analysis sections:**
- ☐ Priority breakdown (chart showing Urgent/High/Medium/Low)
- ☐ Aging analysis (cases grouped by age buckets)
- ☐ Component breakdown (cases by product component)
- ☐ Trend analysis (compare to last week/month)
- ☐ Recommended actions (auto-generated suggestions)

### Section 5: Alerts
**Send alerts when:**
- ☐ Cases older than ___ days (enter number)
- ☐ High priority cases increase by more than ___
- ☐ No updates in ___ days
- ☐ SLA breach risk detected

### Section 6: Formatting
- **Include HTML formatting:** Yes / No
- **Color-code by priority:** Yes / No
- **Include charts:** Yes / No
- **Link to case portal:** Yes / No

### Section 7: Schedule (Optional)
**How often should this report run:**
- ○ Don't schedule (manual only)
- ○ Daily at ___ (time)
- ○ Weekly on ___ (day) at ___ (time)
- ○ Monthly on day ___ at ___ (time)

**Send to (email):** ___________

---

## Benefits of This Approach

### For TAMs:
- ✅ No YAML knowledge required
- ✅ Visual, intuitive interface
- ✅ Can create templates from anywhere (mobile, desktop)
- ✅ See what works for other TAMs
- ✅ Immediate feedback and validation

### For Tool Maintainers:
- ✅ Less support requests ("how do I edit YAML?")
- ✅ Centralized template database
- ✅ Analytics on what features TAMs actually use
- ✅ Easy to add new options (just add form field)

### For the Organization:
- ✅ Best practices sharing
- ✅ Template standardization (optional)
- ✅ Usage metrics and adoption tracking
- ✅ Onboarding made easier

## Success Metrics

- **Adoption:** % of TAMs who create at least one custom template
- **Usage:** # of custom templates in use
- **Satisfaction:** Survey rating of template customization experience
- **Time saved:** Reduction in "how do I..." support tickets

## Next Steps

1. **Create Google Form** (1 hour)
2. **Set up Google Sheet backend** (30 minutes)
3. **Build `tam-rfe-template-sync` script** (2-3 hours)
4. **Test with pilot group of TAMs** (1 week)
5. **Roll out to all TAMs** (after successful pilot)
6. **Build CLI wizard** (Phase 2)
7. **Create template library** (Phase 3)

---

*This strategy makes template customization accessible to all TAMs, regardless of technical skill level, while maintaining flexibility for power users.*

