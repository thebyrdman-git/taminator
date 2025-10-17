# Email CC Feature - Send Report Copies

## Overview

TAMs can now send copies of their automated reports to additional Red Hat email addresses. This is useful for:

- **Managers:** Keep your manager in the loop
- **Team Leads:** Share with practice leads or product specialists
- **Colleagues:** CC colleagues who support the same customer
- **Handoffs:** Include the person taking over an account
- **Visibility:** Give stakeholders access to reports

---

## Security & Validation

### Red Hat Emails Only
- ✅ Only `@redhat.com` addresses accepted
- ❌ External/customer emails blocked
- ✅ Validation in both form and sync script
- ✅ Prevents accidental data leakage

### Data Protection
- Reports contain case summaries (not sensitive)
- All recipients are Red Hat employees
- Compliant with data handling policies
- Audit trail maintained

---

## Using CC in Google Form

### During Onboarding

**Question 14: CC report to (optional)**

**Examples:**
- Single CC: `manager@redhat.com`
- Multiple CCs: `manager@redhat.com, teamlead@redhat.com`
- Team DL: `openshift-tam-team@redhat.com`

**Validation:**
- Must be @redhat.com addresses
- Comma-separated for multiple
- Spaces are trimmed automatically
- Invalid emails filtered out

### What Happens

1. TAM fills out onboarding form
2. Adds manager email to CC field
3. Form submitted
4. Sync script validates emails
5. Configs updated with CC list
6. Reports sent to primary + CC recipients

---

## Using CC in CLI

### Command Syntax

```bash
# Send report with CC
tam-rfe-scheduler-v2 westpac default \
  tam@redhat.com \
  manager@redhat.com,colleague@redhat.com

# Using environment variable
export EMAIL_CC="manager@redhat.com,teamlead@redhat.com"
tam-rfe-scheduler-v2 westpac default tam@redhat.com
```

### Configuration File

In `tamscripts.config`:

```yaml
customers:
  - account_number: "123456"
    account_name: "Westpac Banking"
    customer_shortname: "westpac"
    send_reports_to: "tam@redhat.com"
    cc_reports_to:
      - "manager@redhat.com"
      - "teamlead@redhat.com"
      - "colleague@redhat.com"
```

### In Email Template Config

In `email-templates.yaml`:

```yaml
default:
  name: "Comprehensive Case Report"
  subject: "[RFE Report] {customer} - {total_cases} cases"
  recipients:
    primary: "{tam_email}"
    cc:
      - "{manager_email}"  # From onboarding form
      - "openshift-smes@redhat.com"  # Team DL
  sections:
    - type: summary
      enabled: true
```

---

## Common Use Cases

### Use Case 1: Manager Oversight

**Scenario:** Manager wants visibility into customer reports

**Setup:**
```
Send reports to: tam@redhat.com
CC report to: manager@redhat.com
```

**Result:** TAM and manager both receive reports

### Use Case 2: Backup TAM Coverage

**Scenario:** TAM going on vacation, backup TAM needs visibility

**Setup:**
```
Send reports to: primary-tam@redhat.com
CC report to: backup-tam@redhat.com
```

**Result:** Backup TAM stays informed and can cover during PTO

**Why It's Important:**
- Seamless coverage during vacations/PTO
- Backup TAM already familiar with customer status
- No knowledge gap when primary TAM is unavailable
- Critical alerts don't get missed
- Customer continuity maintained

**Best Practice:**
- Add backup TAM CC at least 1 week before PTO
- Remove CC when returning from PTO
- Use this for extended absences (>3 days)

### Use Case 3: Team Collaboration

**Scenario:** Multiple TAMs support the same customer

**Setup:**
```
Send reports to: primary-tam@redhat.com
CC report to: backup-tam@redhat.com, specialist@redhat.com
```

**Result:** Entire team stays informed

### Use Case 4: Account Handoff

**Scenario:** Transitioning customer to new TAM

**Setup:**
```
Send reports to: current-tam@redhat.com
CC report to: new-tam@redhat.com
```

**Result:** Both TAMs receive reports during transition

### Use Case 5: Product Specialist

**Scenario:** Complex OpenShift cases need specialist review

**Setup:**
```
Send reports to: tam@redhat.com
CC report to: openshift-specialist@redhat.com
```

**Result:** Specialist can proactively assist

### Use Case 6: Practice Lead

**Scenario:** Practice lead tracks all accounts in region

**Setup:**
```
Send reports to: tam@redhat.com
CC report to: practice-lead@redhat.com
```

**Result:** Lead has visibility across portfolio

---

## Email Header Format

### In Email Headers

```
From: tam-rfe-automation@redhat.com
To: primary-tam@redhat.com
Cc: manager@redhat.com, colleague@redhat.com
Subject: [RFE Report] Westpac Banking - 15 cases | 3 high priority
```

### What Recipients See

**Primary Recipient (To:)**
- Receives full report
- Can reply directly
- Primary point of contact

**CC Recipients:**
- Receives same full report
- Can see who else got the report
- Can reply to all
- For awareness/visibility

---

## Managing CC Recipients

### Update CC List

**Option 1: Via Google Form**
1. Go to Customer Onboarding form
2. Submit update with new CC list
3. Status will be updated on next sync

**Option 2: Via Config File**

Edit `~/.config/rfe-tool/tamscripts.config`:

```yaml
customers:
  - customer_shortname: "westpac"
    cc_reports_to:
      - "new-manager@redhat.com"
      - "team-lead@redhat.com"
```

**Option 3: Via CLI** (future feature)

```bash
tam-rfe-update-customer westpac \
  --add-cc new-manager@redhat.com \
  --remove-cc old-manager@redhat.com
```

### Remove All CCs

```yaml
customers:
  - customer_shortname: "westpac"
    cc_reports_to: []  # Empty list = no CCs
```

---

## Validation Rules

### What's Accepted ✅
- `manager@redhat.com`
- `team-lead@redhat.com`
- `openshift-specialists@redhat.com`
- `emea-tam-team@redhat.com`

### What's Rejected ❌
- `customer@example.com` (external)
- `partner@vendor.com` (external)
- `invalid-email` (malformed)
- `test@redhat.org` (not .com)

### Automatic Cleanup
- Whitespace trimmed
- Duplicates removed
- Invalid emails filtered
- Non-Red Hat emails stripped

---

## Privacy Considerations

### What CCs Receive
- ✅ Case summaries and metrics
- ✅ Priority breakdowns
- ✅ Aging analysis
- ✅ Action items
- ✅ Case numbers and titles

### What CCs DON'T Receive
- ❌ Full case details
- ❌ Customer-provided attachments
- ❌ Detailed troubleshooting
- ❌ Customer contact info (unless in report)

### Why It's Safe
- Reports are summaries only
- All recipients are Red Hat employees
- No PII or sensitive customer data
- Compliant with data handling policies

---

## Best Practices

### DO ✅
- CC your manager for oversight
- CC backup TAM for coverage (especially before PTO)
- CC colleagues who support the customer
- CC product specialists for specific expertise
- CC during account transitions
- CC practice/team leads for visibility

### DON'T ❌
- Don't CC external email addresses
- Don't CC people unnecessarily (email overload)
- Don't CC customer contacts (use primary address instead)
- Don't CC distribution lists you're not sure about

### Guidelines
- **Keep it minimal:** Only CC those who need visibility
- **Update regularly:** Remove CCs when no longer needed
- **Be transparent:** Recipients can see who else got the report
- **Use team DLs:** Better than individual emails for teams

---

## Troubleshooting

### CC Not Receiving Emails

**Check:**
1. Email is @redhat.com
2. Email spelled correctly
3. No typos in config
4. SMTP server allows CC
5. Recipient's email not bouncing

**Debug:**
```bash
# Test email delivery
tam-rfe-scheduler-v2 testcust default \
  your@redhat.com \
  colleague@redhat.com

# Check logs
tail -f /var/log/tam-rfe/scheduler.log
```

### Too Many CCs

**Problem:** Email marked as spam due to many recipients

**Solution:**
- Limit to 5-10 CCs maximum
- Use distribution lists for teams
- Consider separate reports for different audiences

### External Email Attempted

**Problem:** Tried to CC customer or partner

**Solution:**
- Use "Send reports to" field for external addresses (if approved)
- CC field is Red Hat internal only
- Create separate manual report for external stakeholders

---

## Examples

### Example 1: Simple Manager CC

```yaml
send_reports_to: "jsmith@redhat.com"
cc_reports_to:
  - "manager@redhat.com"
```

### Example 2: Team Coverage

```yaml
send_reports_to: "primary-tam@redhat.com"
cc_reports_to:
  - "backup-tam@redhat.com"
  - "apac-manager@redhat.com"
  - "openshift-sme@redhat.com"
```

### Example 3: Practice Lead Visibility

```yaml
send_reports_to: "tam@redhat.com"
cc_reports_to:
  - "emea-practice-lead@redhat.com"
  - "financial-services-lead@redhat.com"
```

### Example 4: Backup Coverage During PTO

```yaml
send_reports_to: "primary-tam@redhat.com"
cc_reports_to:
  - "backup-tam@redhat.com"
# Add 1 week before PTO, remove when returning
```

### Example 5: Transition Period

```yaml
send_reports_to: "outgoing-tam@redhat.com"
cc_reports_to:
  - "incoming-tam@redhat.com"
  - "manager@redhat.com"
# After transition, swap primary and remove CC
```

---

## Summary

**Feature:** Send report copies to additional Red Hat email addresses

**Security:** @redhat.com only, automatic validation

**Use Cases:** Manager oversight, backup TAM coverage, team collaboration, handoffs, specialists

**Setup:** Add in Google Form field or config file

**Limit:** Recommend 5-10 CCs maximum

**Privacy:** Safe - reports are summaries, all recipients are Red Hat

**Result:** Better visibility and collaboration across TAM teams! 🚀

