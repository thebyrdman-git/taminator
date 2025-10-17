# Google Forms Data Handling & Security

## Data Privacy & Security

### What Data We Collect

**Customer Information:**
- Customer name (public information)
- Account number (not PII, but protected)
- Product usage (not sensitive)
- Report preferences (configuration only)

**TAM Information:**
- Name and email (Red Hat employee info)
- Manager email (internal only)
- Red Hat username (internal only)

### What We DON'T Collect

❌ Customer passwords or credentials
❌ Customer contact information (unless TAM explicitly adds)
❌ Sensitive customer data
❌ Personal Identifiable Information (PII)
❌ Case details or content

### Data Protection

**Google Sheets Security:**
- Domain-restricted forms (only @redhat.com)
- Sheets shared only with service account
- No public access
- Audit trail of all changes

**Local Storage:**
- Configs stored in `~/.config/rfe-tool/`
- Only accessible to user
- No secrets or passwords stored
- Account numbers are public identifiers

**Data Transmission:**
- HTTPS only (Google APIs)
- No data sent to external services
- Email notifications use internal mail system

### Compliance

**Red Hat AI Policy:**
- No customer data processed by external AI
- All case analysis happens locally
- No data sent to OpenAI, Anthropic, etc.
- Compliant with data handling requirements

**Audit Trail:**
- All form submissions timestamped
- Google Sheets track all changes
- Sync script logs all operations
- Email notifications sent for all actions

---

## Clearing Customer Data

### Option 1: Clear Individual Customer (Google Form)

**Form: "TAM RFE Automation - Remove Customer"**

**Questions:**
1. Your Email (verification)
2. Customer to remove (dropdown)
3. Reason for removal (required)
   - Customer engagement ended
   - Moved to different TAM
   - Account closed
   - Other

**Process:**
- Form submission logged
- Sync script removes from configs
- Status updated to "Removed"
- Notification sent to TAM and manager

### Option 2: Bulk Clear from Google Sheets

**Manual Process:**
1. Open Google Sheet
2. Select rows to clear
3. Change Status column to "Remove"
4. Next sync will process removals

### Option 3: CLI Command

```bash
# Remove specific customer
tam-rfe-remove-customer westpac

# Remove all customers (requires confirmation)
tam-rfe-remove-customer --all

# Remove customers from specific TAM
tam-rfe-remove-customer --tam jsmith@redhat.com

# Dry run (show what would be removed)
tam-rfe-remove-customer --all --dry-run
```

### Option 4: Archive Instead of Delete

**Recommended approach:**
- Don't delete, mark as "Archived"
- Keeps audit trail
- Can be reactivated if needed
- Preserves historical data

---

## Data Retention Policy

### Active Customers
- Kept in Google Sheets indefinitely
- Status: "Activated"
- Configs auto-updated

### Removed Customers
- Moved to "Archived" sheet
- Status: "Removed" + date
- Reason for removal recorded
- Local configs removed
- Historical data preserved

### Auto-Cleanup
- Customers with no cases for 90 days → flagged for review
- Customers with Status="Error" for 30 days → auto-archived
- Duplicate entries → merged automatically

---

## Data Validation

### Pre-Submission (Form Validation)
- Email format validation
- Account number format (6 digits)
- Short name format (alphanumeric + dashes)
- Required fields enforced

### Post-Submission (Sync Script Validation)
- Account number exists in Hydra
- No duplicate short names
- Valid product selections
- Email addresses valid
- Manager email is Red Hat employee

### Data Quality Checks
- Account number matches customer name (Hydra lookup)
- TAM email matches Red Hat directory
- Product selections match account subscriptions
- Report frequency is valid cron schedule

---

## Clear All Functionality

### Implementation

```python
# In tam-rfe-onboard-sync

def clear_all_customers(dry_run=False, backup=True):
    """
    Clear all customer configurations
    
    Args:
        dry_run: Show what would be removed without removing
        backup: Create backup before clearing
    """
    
    print("WARNING: This will remove ALL customer configurations!")
    print()
    
    # List what will be cleared
    config_dir = Path.home() / ".config" / "rfe-tool"
    customers_conf = config_dir / "customers.conf"
    tamscripts_config = config_dir / "tamscripts.config"
    
    if customers_conf.exists():
        content = customers_conf.read_text()
        customer_count = content.count("CUSTOMER_")
        print(f"  - customers.conf: ~{customer_count} customers")
    
    if tamscripts_config.exists():
        with open(tamscripts_config) as f:
            config = yaml.safe_load(f)
        customers = len(config.get('customers', []))
        print(f"  - tamscripts.config: {customers} customers")
    
    print()
    
    if dry_run:
        print("[DRY RUN] No changes made")
        return
    
    # Require confirmation
    response = input("Type 'DELETE ALL' to confirm: ")
    if response != "DELETE ALL":
        print("Cancelled")
        return
    
    # Create backup
    if backup:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_dir = config_dir / "backups" / timestamp
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        if customers_conf.exists():
            shutil.copy(customers_conf, backup_dir / "customers.conf")
        if tamscripts_config.exists():
            shutil.copy(tamscripts_config, backup_dir / "tamscripts.config")
        
        print(f"[OK] Backup created: {backup_dir}")
    
    # Clear customers.conf
    if customers_conf.exists():
        customers_conf.write_text("# TAM RFE Automation - Customer Configuration\n# All customers cleared on " + datetime.now().isoformat() + "\n")
        print("[OK] Cleared customers.conf")
    
    # Clear tamscripts.config
    if tamscripts_config.exists():
        with open(tamscripts_config) as f:
            config = yaml.safe_load(f) or {}
        
        config['customers'] = []
        config['cleared_date'] = datetime.now().isoformat()
        
        with open(tamscripts_config, 'w') as f:
            yaml.dump(config, f)
        
        print("[OK] Cleared tamscripts.config")
    
    print()
    print("All customer configurations cleared!")
    print(f"Backup location: {backup_dir}")
```

### Usage

```bash
# Show what would be cleared
tam-rfe-clear-customers --dry-run

# Clear all (creates backup automatically)
tam-rfe-clear-customers --all

# Clear without backup (NOT RECOMMENDED)
tam-rfe-clear-customers --all --no-backup

# Restore from backup
tam-rfe-restore-customers 20251017-103045
```

---

## Product-Specific Form Templates

### Template 1: RHEL-Focused TAM

**Pre-filled values:**
- Priority Products: ✅ RHEL, ✅ Satellite
- Report Template: Comprehensive
- Alert on: ✅ Kernel issues, ✅ System stability

**Best for:** Infrastructure TAMs, government sector

**Form link:** `https://forms.gle/rhel-focused-XXXXXX`

### Template 2: OpenShift-Focused TAM

**Pre-filled values:**
- Priority Products: ✅ OpenShift, ✅ ACM, ✅ ODF
- Report Template: Priority-focused
- Alert on: ✅ High priority cases, ✅ Outage risks

**Best for:** Container platform TAMs, enterprises

**Form link:** `https://forms.gle/openshift-focused-XXXXXX`

### Template 3: Ansible-Focused TAM

**Pre-filled values:**
- Priority Products: ✅ Ansible Automation Platform
- Report Template: Executive
- Alert on: ✅ Automation failures, ✅ Integration issues

**Best for:** Automation TAMs, DevOps customers

**Form link:** `https://forms.gle/ansible-focused-XXXXXX`

### Template 4: Middleware-Focused TAM

**Pre-filled values:**
- Priority Products: ✅ JBoss EAP, ✅ AMQ, ✅ Fuse
- Report Template: Comprehensive
- Alert on: ✅ Performance issues, ✅ Integration problems

**Best for:** Application platform TAMs, financial services

**Form link:** `https://forms.gle/middleware-focused-XXXXXX`

### Template 5: Multi-Product TAM

**Pre-filled values:**
- Priority Products: ✅ RHEL, ✅ OpenShift, ✅ Ansible
- Report Template: Executive
- Alert on: ✅ All high priority

**Best for:** Strategic account TAMs, large enterprises

**Form link:** `https://forms.gle/multi-product-XXXXXX`

---

## Creating Product-Specific Templates

### In Google Forms:

1. **Create master form** (all questions)
2. **Duplicate for each product focus**
3. **Pre-fill values:**
   - Click "⋮" menu → "Get pre-filled link"
   - Select appropriate checkboxes
   - Copy link
4. **Share template links** with TAMs

### Pre-fill URL Format:

```
https://docs.google.com/forms/d/e/FORM_ID/viewform?
  usp=pp_url
  &entry.123456=RHEL
  &entry.234567=OpenShift
  &entry.345678=Comprehensive
```

### Automated Template Generation:

```bash
# Generate product-specific form links
tam-rfe-generate-form-templates

Output:
  RHEL-focused:       https://forms.gle/...
  OpenShift-focused:  https://forms.gle/...
  Ansible-focused:    https://forms.gle/...
  Middleware-focused: https://forms.gle/...
  Multi-product:      https://forms.gle/...
```

---

## Best Practices

### Data Entry
- ✅ Use customer's official name (from Salesforce/Hydra)
- ✅ Verify account number before submission
- ✅ Choose appropriate product focus
- ✅ Set realistic report frequency
- ❌ Don't include sensitive customer data
- ❌ Don't add personal contact info without approval

### Data Maintenance
- Review customer list quarterly
- Remove inactive customers
- Update product selections as needed
- Archive old accounts properly

### Data Sharing
- ✅ Share within Red Hat only
- ✅ Use Google Sheets permissions properly
- ❌ Don't export to external systems
- ❌ Don't share form links publicly

---

## Summary

**Data Protection:**
- Domain-restricted (@redhat.com only)
- No PII or sensitive data collected
- Audit trail of all operations
- Compliant with Red Hat policies

**Clear Functionality:**
- Individual customer removal
- Bulk clear with confirmation
- Automatic backups
- Archive instead of delete (recommended)

**Product Templates:**
- 5 pre-configured templates
- Easy to customize
- Quick onboarding for new TAMs
- Best practices baked in

**Result:** Secure, auditable, easy-to-use system that respects data privacy while enabling TAM productivity.

