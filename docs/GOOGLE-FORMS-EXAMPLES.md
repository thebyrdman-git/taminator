# Example Google Forms for TAM RFE Automation

## Quick Start

Copy these Google Form templates to get started immediately!

---

## Form 1: Customer Onboarding

### Google Form Setup

**Create New Form:** https://forms.google.com/

**Form Title:** TAM RFE Automation - Customer Onboarding

**Description:**
```
Onboard a new customer to TAM RFE automation. This form will automatically configure case monitoring, reporting, and alerts for your customer.

Questions? Contact the TAM Automation team.
```

### Form Questions

#### Section 1: TAM Information

**Question 1: Your Name** (Short answer, Required)
- Help text: Your full name

**Question 2: Your Email** (Short answer, Required)
- Validation: Email address format
- Help text: Your @redhat.com email

**Question 3: Manager Email** (Short answer)
- Validation: Email address format
- Help text: Your manager's email (for approval notifications)

**Question 4: Red Hat Username** (Short answer, Required)
- Help text: Your Red Hat Kerberos username

---

#### Section 2: Customer Details

**Question 5: Customer Name** (Short answer, Required)
- Help text: Full customer name (e.g., "JPMorgan Chase", "Westpac Banking Corporation")

**Question 6: Account Number** (Short answer, Required)
- Validation: Number, exactly 6 digits
- Help text: 6-digit account number from Hydra or Customer Portal

**Question 7: Customer Short Name** (Short answer, Required)
- Validation: Regex pattern: ^[a-z0-9_-]+$
- Help text: Lowercase name for commands (e.g., "jpmc", "westpac", "citi")
- Example: jpmc

---

#### Section 3: Priority Products

**Question 8: Which Red Hat products does this customer use?** (Checkboxes, Required - select at least 1)
- ☐ Red Hat Enterprise Linux (RHEL)
- ☐ OpenShift Container Platform
- ☐ Ansible Automation Platform
- ☐ Red Hat OpenStack Platform
- ☐ Red Hat Satellite
- ☐ JBoss Enterprise Application Platform
- ☐ Red Hat Virtualization
- ☐ OpenShift Data Foundation
- ☐ Advanced Cluster Management
- ☐ Red Hat AMQ
- ☐ Red Hat Fuse
- ☐ Other

**Question 9: Specific components to monitor** (Paragraph, Optional)
- Help text: Specific components or technologies (e.g., "kernel, networking, storage")

---

#### Section 4: Automation Preferences

**Question 10: Report Frequency** (Dropdown, Required)
- Daily
- Weekly (default)
- Bi-weekly
- Monthly
- Manual only (no scheduled reports)

**Question 11: Report Day** (Dropdown, shown if Weekly/Bi-weekly/Monthly)
- Monday (default)
- Tuesday
- Wednesday
- Thursday
- Friday
- Saturday
- Sunday

**Question 12: Report Time** (Dropdown, Required)
- 07:00 EST
- 08:00 EST (default)
- 09:00 EST
- 10:00 EST
- 11:00 EST
- 12:00 EST
- 13:00 EST
- 14:00 EST
- 15:00 EST
- 16:00 EST
- 17:00 EST

**Question 13: Send reports to** (Short answer, Required)
- Validation: Email format
- Default: (pre-fill with TAM email from Q2)
- Help text: Email address for reports (your email or customer DL)

**Question 14: Report Template** (Dropdown, Required)
- Comprehensive (all details) - default
- Minimal (quick status)
- Priority-focused (high priority only)
- Executive (metrics and trends)

---

#### Section 5: Alert Preferences

**Question 15: Send alerts when** (Checkboxes)
- ☐ New high-priority cases are opened
- ☐ Cases age beyond 30 days
- ☐ No updates in 7 days
- ☐ SLA breach risk detected
- ☐ Case volume spikes above normal

**Question 16: Alert delivery method** (Checkboxes)
- ☑ Email (default)
- ☐ Slack (if configured)
- ☐ Teams (if configured)

---

#### Section 6: Additional Context

**Question 17: Customer vertical** (Dropdown, Optional)
- Financial Services
- Healthcare
- Government/Public Sector
- Telecommunications
- Retail
- Manufacturing
- Technology
- Energy/Utilities
- Other

**Question 18: Strategic account?** (Multiple choice, Required)
- Yes
- No (default)

**Question 19: Special handling notes** (Paragraph, Optional)
- Help text: Any special requirements or considerations

**Question 20: Escalation contacts** (Paragraph, Optional)
- Help text: Names/emails for escalations

---

#### Section 7: Confirmation

**Question 21: Confirmations** (Checkboxes, Required - all must be checked)
- ☑ I have verified the account number is correct
- ☑ I have customer approval to automate case monitoring
- ☑ I will keep this information updated

---

### Response Settings

**Collect email addresses:** Yes
**Limit to 1 response:** No
**Allow response editing:** Yes (for 24 hours)
**Send copy of responses to respondent:** Yes

### Link to Google Sheet

**Responses → Create Spreadsheet**
- Sheet name: "Customer Onboarding"
- Add columns:
  - Status (empty by default)
  - Notes (empty by default)
  - Processed Date (empty by default)

---

## Form 2: Email Template Customization

### Google Form Setup

**Form Title:** TAM RFE Automation - Custom Email Template

**Description:**
```
Create a custom email report template. Choose exactly which metrics, case details, and analysis you want in your reports.

No YAML editing required - just check the boxes!
```

### Form Questions

#### Section 1: Template Basics

**Question 1: Your Email** (Short answer, Required)
- Validation: Email format
- Help text: Your @redhat.com email

**Question 2: Template Name** (Short answer, Required)
- Help text: Name for your custom template (e.g., "My Weekly Review")

**Question 3: Template Description** (Short answer, Optional)
- Help text: Brief description of what this template is for

**Question 4: Based on existing template** (Dropdown)
- Start Fresh
- Comprehensive (all details)
- Minimal (quick status)
- Priority-focused (high priority only)
- Executive (trends and metrics)

---

#### Section 2: Summary Metrics

**Question 5: Which metrics do you want in the summary?** (Checkboxes)
- ☑ Total open cases (default)
- ☑ Feature requests (RFEs)
- ☑ Bugs
- ☑ High priority cases (default)
- ☑ Aging cases (>30 days) (default)
- ☐ Resolved this week
- ☐ New this week
- ☐ Average age of cases
- ☐ Cases by component
- ☐ Resolution rate

---

#### Section 3: Case List Options

**Question 6: How many cases to show** (Dropdown, Required)
- 5 cases
- 10 cases (default)
- 20 cases
- 50 cases
- All cases

**Question 7: Sort cases by** (Dropdown, Required)
- Priority (High to Low) - default
- Age (Oldest first)
- Last Update (Recent first)
- Severity

**Question 8: Fields to include in case list** (Checkboxes, Required)
- ☑ Case number (default)
- ☑ Title (default)
- ☑ Priority (default)
- ☐ Status
- ☑ Age (days) (default)
- ☐ Last update date
- ☐ Component
- ☐ Owner/Engineer
- ☐ Customer contact

---

#### Section 4: Analysis Sections

**Question 9: Include these analysis sections** (Checkboxes)
- ☑ Priority breakdown (chart showing Urgent/High/Medium/Low)
- ☑ Aging analysis (cases grouped by age buckets)
- ☐ Component breakdown (cases by product component)
- ☐ Trend analysis (compare to last week/month)
- ☑ Recommended actions (auto-generated suggestions) (default)
- ☐ Top issues (most impactful cases)

---

#### Section 5: Alerts

**Question 10: Send alerts when** (Paragraph, Optional)
- Help text: Enter aging threshold in days (e.g., "30" for cases older than 30 days)

**Question 11: Alert on high priority increase** (Multiple choice)
- Yes
- No (default)

**Question 12: Alert on no updates** (Dropdown)
- Don't alert
- 3 days
- 7 days (default)
- 14 days
- 30 days

---

#### Section 6: Formatting

**Question 13: Include HTML formatting** (Multiple choice, Required)
- Yes (default) - Rich formatting with colors and tables
- No - Plain text only

**Question 14: Color-code by priority** (Multiple choice, Required)
- Yes (default) - Urgent=Red, High=Orange
- No - No color coding

**Question 15: Include charts/graphs** (Multiple choice)
- Yes - Visual charts
- No (default) - Tables only

**Question 16: Link to case portal** (Multiple choice, Required)
- Yes (default) - Case numbers are clickable links
- No - Plain text case numbers

---

### Response Settings
Same as Form 1

---

## Form 3: Schedule Management

### Google Form Setup

**Form Title:** TAM RFE Automation - Schedule Reports

**Description:**
```
Schedule automated reports for your customers. Choose when and how often you want reports delivered.
```

### Form Questions

#### Section 1: Your Information

**Question 1: Your Email** (Short answer, Required)
- Validation: Email format

---

#### Section 2: Schedule Details

**Question 2: Customer** (Dropdown, Required)
- (Dynamically populated from onboarded customers)
- Help text: Select customer to schedule reports for

**Question 3: How often** (Dropdown, Required)
- Don't schedule (manual only)
- Daily
- Weekly
- Bi-weekly
- Monthly

**Question 4: Day of week** (Dropdown, shown if Weekly/Bi-weekly)
- Monday
- Tuesday
- Wednesday
- Thursday
- Friday

**Question 5: Time** (Dropdown, Required)
- 07:00 EST
- 08:00 EST
- 09:00 EST
- ... (same as Form 1)

**Question 6: Template to use** (Dropdown, Required)
- Default (Comprehensive)
- Minimal
- Priority-focused
- Executive
- (Plus any custom templates the user has created)

**Question 7: Send to** (Short answer, Required)
- Validation: Email format
- Default: (pre-fill with user email)

---

## Setting Up the Forms

### Step 1: Create Google Form
1. Go to https://forms.google.com/
2. Click "Blank" to create new form
3. Copy questions from above
4. Set validation rules as specified

### Step 2: Link to Google Sheets
1. Click "Responses" tab in form
2. Click "Create Spreadsheet"
3. Choose "Create a new spreadsheet"
4. Name it appropriately

### Step 3: Add Status Columns
In the Google Sheet, add these columns:
- **Status** (empty initially)
- **Notes** (empty initially)
- **Processed Date** (empty initially)

### Step 4: Share with Service Account
1. In Google Sheet, click "Share"
2. Add your service account email
3. Give "Editor" permissions

### Step 5: Get Sheet ID
1. Look at URL: `https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit`
2. Copy the SHEET_ID_HERE part
3. Add to `~/.config/rfe-tool/google-sheets-config.yaml`

---

## Testing the Forms

### Test Form 1: Customer Onboarding

**Fill out form with test data:**
- TAM Name: Test TAM
- TAM Email: your-email@redhat.com
- Customer Name: Test Customer Inc
- Account Number: 123456
- Short Name: testcust
- Products: RHEL, OpenShift
- Report Frequency: Weekly
- Report Day: Monday
- Report Time: 08:00 EST
- Send reports to: your-email@redhat.com
- Report Template: Comprehensive

**Run sync script:**
```bash
tam-rfe-onboard-sync
```

**Verify:**
1. Check `~/.config/rfe-tool/customers.conf` for new entry
2. Check `~/.config/rfe-tool/tamscripts.config` for customer data
3. Check Google Sheet "Status" column = "Activated"
4. Check your email for confirmation

---

## Shareable Form Links

Once you create the forms, you'll get shareable links like:

```
Customer Onboarding:
https://forms.gle/XXXXXXXXXX

Email Template Customization:
https://forms.gle/YYYYYYYYYY

Schedule Management:
https://forms.gle/ZZZZZZZZZZ
```

Share these links with TAMs for self-service onboarding!

---

## Next Steps

1. **Create the forms** using templates above
2. **Set up Google Sheets** backend
3. **Configure service account** credentials
4. **Test with dummy data**
5. **Pilot with 3-5 TAMs**
6. **Roll out to all TAMs**

Questions? Check the full integration guide:
`docs/GOOGLE-FORM-INTEGRATION.md`

