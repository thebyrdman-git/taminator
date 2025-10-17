# Google Form Integration Strategy

## Vision: Web-Based Self-Service for TAMs

Make RFE automation accessible without requiring SSH, command-line knowledge, or technical setup.

---

## Use Case 1: Customer Onboarding ⭐ **PRIORITY**

### Current Pain Points
- Requires SSH access to run `tam-rfe-onboard-intelligent`
- Command-line interface intimidating for new TAMs
- Can't onboard from mobile or during customer meetings
- No approval workflow
- Hard to audit who onboarded what customer
- No visibility into which TAMs own which accounts

### Google Form Solution

**Form Title:** "Red Hat TAM - Customer Onboarding for RFE Automation"

**Form Sections:**

#### Section 1: TAM Information
- **Your Name:** ___________
- **Your Email:** ___________ (auto-filled from Google login)
- **Manager Email:** ___________ (for approval notifications)
- **Red Hat Username:** ___________

#### Section 2: Customer Details
- **Customer Name:** ___________
  - *Example: JPMorgan Chase, Westpac Banking, Citi*
- **Account Number:** ___________
  - *Validation: Must be numeric, 6 digits*
  - *Where to find: Hydra or Customer Portal*
- **Customer Short Name:** ___________
  - *Example: jpmc, westpac, citi (lowercase, no spaces)*
  - *Used in filenames and commands*

#### Section 3: Priority Products/Components
**Which Red Hat products does this customer primarily use?**
- ☐ Red Hat Enterprise Linux (RHEL)
- ☐ OpenShift Container Platform
- ☐ Ansible Automation Platform
- ☐ Red Hat OpenStack Platform
- ☐ Red Hat Satellite
- ☐ JBoss Enterprise Application Platform
- ☐ Red Hat Virtualization
- ☐ OpenShift Data Foundation
- ☐ Advanced Cluster Management
- ☐ Other: ___________

**Specific components to monitor (optional):**
___________
*Example: kernel, networking, storage, etc.*

#### Section 4: Automation Preferences
- **Report Frequency:** [Dropdown: Daily, Weekly, Bi-weekly, Monthly, Manual only]
- **Report Day (if weekly):** [Dropdown: Monday, Tuesday, ...]
- **Report Time:** [Dropdown: 07:00, 08:00, 09:00, ...]
- **Send reports to:** ___________
  - *Default: Your email, or specify customer DL*
- **Report Template:** [Dropdown: Comprehensive, Minimal, Priority-Focused, Executive]

#### Section 5: Alert Preferences
**Send alerts when:**
- ☐ New high-priority cases are opened
- ☐ Cases age beyond 30 days
- ☐ No updates in 7 days
- ☐ SLA breach risk detected
- ☐ Case volume spikes above normal

**Alert delivery method:**
- ☐ Email
- ☐ Slack (if configured)
- ☐ Teams (if configured)

#### Section 6: Additional Context (Optional)
- **Customer vertical:** [Dropdown: Financial Services, Healthcare, Government, Telecom, Retail, Manufacturing, Other]
- **Strategic account?** Yes / No
- **Special handling notes:** ___________
- **Escalation contacts:** ___________

#### Section 7: Confirmation
- ☑ I have verified the account number is correct
- ☑ I have customer approval to automate case monitoring
- ☑ I will keep this information updated

**Submit Button:** "Onboard Customer"

---

### Backend Workflow

```
Google Form → Google Sheets → Sync Script → Validation → Config Generation
                                   ↓                           ↓
                            Manager Approval              customers.conf
                                   ↓                      tamscripts.config
                            Activation Email              Schedule setup
```

#### Implementation: `tam-rfe-onboard-sync`

```python
#!/usr/bin/env python3
"""
Sync customer onboarding from Google Sheets
Runs every 5 minutes via cron
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import yaml
from pathlib import Path
import subprocess
from datetime import datetime

# Google Sheets setup
SHEET_ID = "your-sheet-id-here"
SHEET_NAME = "Customer Onboarding"

# Configuration paths
CONFIG_DIR = Path.home() / ".config" / "tamscripts"
CUSTOMERS_CONF = CONFIG_DIR / "customers.conf"
TAMSCRIPTS_CONFIG = CONFIG_DIR / "tamscripts.config"

def authenticate_google_sheets():
    """Authenticate with Google Sheets API"""
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        str(CONFIG_DIR / "google-credentials.json"),
        scope
    )
    client = gspread.authorize(creds)
    return client

def fetch_pending_onboardings(sheet):
    """Get rows where Status = 'Pending' or 'Approved'"""
    all_records = sheet.get_all_records()
    return [r for r in all_records if r.get('Status') in ['Pending', 'Approved']]

def validate_onboarding(record):
    """Validate onboarding data"""
    errors = []
    
    # Required fields
    required = ['Customer Name', 'Account Number', 'Short Name', 'TAM Name', 'TAM Email']
    for field in required:
        if not record.get(field):
            errors.append(f"Missing required field: {field}")
    
    # Account number validation
    account = str(record.get('Account Number', ''))
    if not account.isdigit() or len(account) != 6:
        errors.append("Account number must be 6 digits")
    
    # Short name validation
    short_name = record.get('Short Name', '').lower()
    if not short_name.replace('-', '').replace('_', '').isalnum():
        errors.append("Short name must be alphanumeric (- and _ allowed)")
    
    return errors

def generate_config(record):
    """Generate customers.conf and tamscripts.config entries"""
    short_name = record['Short Name'].lower()
    account = record['Account Number']
    products = record.get('Priority Products', '').split(',')
    
    # Add to customers.conf
    customers_entry = f"\n# {record['Customer Name']}\n"
    customers_entry += f"CUSTOMER_{short_name.upper()}_ACCOUNT=\"{account}\"\n"
    customers_entry += f"CUSTOMER_{short_name.upper()}_NAME=\"{record['Customer Name']}\"\n"
    
    # Add to tamscripts.config
    tamscripts_entry = {
        'account_number': account,
        'account_name': record['Customer Name'],
        'customer_shortname': short_name,
        'tam_name': record['TAM Name'],
        'tam_email': record['TAM Email'],
        'products': [p.strip() for p in products if p.strip()],
        'report_frequency': record.get('Report Frequency', 'Weekly'),
        'onboarded_date': datetime.now().isoformat(),
        'onboarded_via': 'google_form'
    }
    
    return customers_entry, tamscripts_entry

def update_sheet_status(sheet, row_number, status, message=""):
    """Update status column in Google Sheet"""
    sheet.update_cell(row_number, get_column_index('Status'), status)
    if message:
        sheet.update_cell(row_number, get_column_index('Notes'), message)

def send_notification(record, status):
    """Send email notification to TAM"""
    if status == "Activated":
        subject = f"✅ Customer Onboarded: {record['Customer Name']}"
        body = f"""
Your customer has been successfully onboarded!

Customer: {record['Customer Name']}
Account: {record['Account Number']}
Short Name: {record['Short Name']}

You can now run:
  tam-rfe-chat {record['Short Name']}
  tam-rfe-validate-intelligence {record['Short Name']}

Reports will be sent {record.get('Report Frequency', 'Weekly')} to: {record.get('Send reports to', record['TAM Email'])}

Next steps:
1. Verify the configuration: tam-rfe-validate-intelligence {record['Short Name']}
2. Customize your report template: tam-rfe-template-customizer
3. Run your first report: tam-rfe-chat {record['Short Name']}
"""
    else:
        subject = f"❌ Onboarding Failed: {record['Customer Name']}"
        body = f"Onboarding failed. Please check the Notes column in the sheet."
    
    # Send via tam-rfe email system
    subprocess.run([
        "mail",
        "-s", subject,
        record['TAM Email']
    ], input=body.encode())

def main():
    print("[OK] Starting customer onboarding sync...")
    
    # Authenticate
    client = authenticate_google_sheets()
    sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
    
    # Fetch pending onboardings
    pending = fetch_pending_onboardings(sheet)
    print(f"[OK] Found {len(pending)} pending onboardings")
    
    for i, record in enumerate(pending):
        row_number = i + 2  # Account for header row
        
        # Validate
        errors = validate_onboarding(record)
        if errors:
            update_sheet_status(sheet, row_number, "Error", "; ".join(errors))
            send_notification(record, "Error")
            continue
        
        # Generate config
        try:
            customers_entry, tamscripts_entry = generate_config(record)
            
            # Append to customers.conf
            with open(CUSTOMERS_CONF, 'a') as f:
                f.write(customers_entry)
            
            # Update tamscripts.config
            with open(TAMSCRIPTS_CONFIG, 'r') as f:
                config = yaml.safe_load(f) or {}
            
            if 'customers' not in config:
                config['customers'] = []
            config['customers'].append(tamscripts_entry)
            
            with open(TAMSCRIPTS_CONFIG, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
            
            # Update status
            update_sheet_status(sheet, row_number, "Activated", f"Activated on {datetime.now()}")
            send_notification(record, "Activated")
            
            print(f"[OK] Onboarded: {record['Customer Name']}")
            
        except Exception as e:
            update_sheet_status(sheet, row_number, "Error", str(e))
            print(f"[FAIL] Error onboarding {record['Customer Name']}: {e}")
    
    print("[OK] Sync complete!")

if __name__ == '__main__':
    main()
```

---

## Use Case 2: Email Template Customization

### Google Form: "TAM RFE Automation - Custom Email Template"

*(See TEMPLATE-CUSTOMIZATION-STRATEGY.md for full details)*

**Quick Summary:**
- TAMs fill out form with template preferences
- Form auto-generates YAML template
- Template syncs to user's config
- Available immediately for use

---

## Use Case 3: Schedule Management

### Google Form: "TAM RFE Automation - Schedule Reports"

**Form Sections:**
- Customer selection (dropdown from onboarded customers)
- Frequency (Daily, Weekly, Monthly)
- Day/Time selection
- Template selection
- Delivery options (Email, Slack, Both)

**Backend:**
- Updates cron jobs
- Manages systemd timers
- Sends confirmation

---

## Infrastructure Requirements

### 1. Google API Setup
```bash
# Install dependencies
pip install gspread oauth2client

# Create service account
# Download credentials JSON
# Store in ~/.config/rfe-tool/google-credentials.json
```

### 2. Google Sheets Structure

**Sheet 1: Customer Onboarding**
```
| Timestamp | TAM Name | TAM Email | Customer Name | Account # | Short Name | Products | Report Freq | Status | Notes |
|-----------|----------|-----------|---------------|-----------|------------|----------|-------------|--------|-------|
```

**Sheet 2: Email Templates**
```
| Timestamp | TAM Email | Template Name | Report Type | Metrics | Max Cases | Sort By | Analysis | Status | Generated Config |
|-----------|-----------|---------------|-------------|---------|-----------|---------|----------|--------|------------------|
```

**Sheet 3: Schedules**
```
| Timestamp | TAM Email | Customer | Frequency | Day | Time | Template | Status | Cron Entry |
|-----------|-----------|----------|-----------|-----|------|----------|--------|------------|
```

### 3. Sync Scripts (Cron Jobs)

```bash
# /etc/cron.d/tam-rfe-google-sync

# Customer onboarding - every 5 minutes
*/5 * * * * tam-user tam-rfe-onboard-sync >> /var/log/tam-rfe/onboard-sync.log 2>&1

# Template sync - every 15 minutes
*/15 * * * * tam-user tam-rfe-template-sync >> /var/log/tam-rfe/template-sync.log 2>&1

# Schedule sync - every 15 minutes
*/15 * * * * tam-user tam-rfe-schedule-sync >> /var/log/tam-rfe/schedule-sync.log 2>&1
```

---

## Benefits

### For TAMs
- ✅ Onboard customers from anywhere (mobile, meeting room, home)
- ✅ No command-line knowledge required
- ✅ Self-service - no waiting for admin
- ✅ Visual, intuitive interface
- ✅ Can save partial progress
- ✅ See status of onboarding requests
- ✅ Template management without YAML editing

### For Managers
- ✅ Approval workflow for customer onboarding
- ✅ Visibility into which TAMs manage which customers
- ✅ Audit trail of all onboardings
- ✅ Metrics on adoption and usage
- ✅ Quality control (validation before activation)

### For Automation Team
- ✅ Centralized data source
- ✅ Easy to add new fields/features
- ✅ Reduced support burden
- ✅ Better data quality (validation rules)
- ✅ Integration with other Google Workspace tools

---

## Implementation Priority

### Phase 1: Customer Onboarding (Highest Impact) ⭐
- **Effort:** 4-6 hours
- **Impact:** Massive - removes biggest friction point
- **Dependencies:** Google Sheets API access

### Phase 2: Email Template Customization
- **Effort:** 2-3 hours
- **Impact:** High - makes templates accessible
- **Dependencies:** Phase 1 infrastructure

### Phase 3: Schedule Management
- **Effort:** 2-3 hours
- **Impact:** Medium - nice to have
- **Dependencies:** Phase 1 + 2

### Phase 4: Template Library & Sharing
- **Effort:** 3-4 hours
- **Impact:** Medium - community building
- **Dependencies:** Phase 2

---

## Security Considerations

1. **Authentication**
   - Use Google Workspace domain restriction
   - Only @redhat.com emails can access forms
   - Service account with minimal permissions

2. **Data Protection**
   - Sheets not publicly accessible
   - No sensitive data in forms (no passwords, keys)
   - Account numbers are not PII but should be protected

3. **Audit Trail**
   - All form submissions timestamped
   - Track who onboarded which customer
   - Log all sync operations

4. **Validation**
   - Server-side validation in sync script
   - Don't trust form data blindly
   - Verify account numbers via Hydra API

---

## Success Metrics

- **Adoption Rate:** % of TAMs using Google Form vs CLI
- **Onboarding Time:** Time from form submission to activation
- **Error Rate:** % of onboardings that fail validation
- **User Satisfaction:** Survey after onboarding
- **Support Tickets:** Reduction in "how do I onboard?" tickets

---

## Rollout Plan

### Week 1: Build
- Create Google Forms
- Set up Google Sheets
- Build sync scripts
- Test with dummy data

### Week 2: Pilot
- Select 3-5 TAMs for pilot
- Onboard 2-3 test customers each
- Collect feedback
- Fix bugs

### Week 3: Internal Launch
- Announce to all TAMs
- Provide training/documentation
- Monitor adoption
- Offer office hours for questions

### Week 4: Iteration
- Analyze usage metrics
- Add requested features
- Optimize based on feedback

---

*This strategy transforms RFE automation from a command-line tool into a self-service web platform, dramatically lowering the barrier to entry for TAMs.*

