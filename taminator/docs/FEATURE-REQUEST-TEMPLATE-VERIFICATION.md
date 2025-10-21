# Feature Request: Template Status Verification

**Date:** October 21, 2025  
**Requestor:** Jimmy Byrd (TAM)  
**Use Case:** Pre-call verification of customer RFE/Bug tracker templates  
**Priority:** High (saves time before customer calls)

---

## Problem Statement

### Current Workflow
TAMs maintain RFE/Bug tracker templates for customers (e.g., TD Bank, Wells Fargo, JPMC) that show:
- Active RFE cases with JIRA statuses
- Active Bug cases with JIRA statuses  
- Closed cases with final status

**Before customer calls**, TAMs need to verify if the template is up-to-date with current JIRA statuses.

### Current Manual Process (10-15 minutes per customer)
1. Open customer template in editor
2. Extract all JIRA IDs manually (AAPRFE-XXX, AAP-XXXXX)
3. Visit issues.redhat.com or run rhcase for each JIRA
4. Compare template status vs current JIRA status
5. Update template if statuses changed
6. Save and prepare for call

**Pain Points:**
- Time-consuming before every customer call
- Error-prone (easy to miss a status change)
- Repetitive task
- No quick "is this up-to-date?" check

---

## Proposed Feature: `tam-rfe-verify-template`

### Command Usage
```bash
# Basic usage: verify single template
tam-rfe-verify-template --file tdbank-rfe-tracker.md

# Verify and update in place
tam-rfe-verify-template --file tdbank-rfe-tracker.md --update

# Verify all customer templates
tam-rfe-verify-template --customer tdbank --all-templates

# Output formats
tam-rfe-verify-template --file tdbank.md --format table
tam-rfe-verify-template --file tdbank.md --format json
```

### Expected Output (Table Format)
```
TD Bank RFE/Bug Template Verification
=====================================
Template: tdbank-rfe-tracker.md
Checked: 2025-10-21 09:30:00

JIRA ID      | Template Status | Current Status | Match | Action
-------------|-----------------|----------------|-------|--------
AAPRFE-762   | Backlog        | Backlog        | ✓     | None
AAPRFE-430   | Backlog        | Backlog        | ✓     | None
AAPRFE-1158  | Review         | Review         | ✓     | None
AAPRFE-873   | Backlog        | Backlog        | ✓     | None
AAPRFE-1207  | Backlog        | Backlog        | ✓     | None
AAPRFE-1257  | Backlog        | Backlog        | ✓     | None
AAPRFE-650   | Closed         | Closed         | ✓     | None
AAP-53458    | New            | New            | ✓     | None
AAP-45405    | Closed         | Closed         | ✓     | None

Summary: 9/9 statuses match (100%)
Status: ✅ Template is UP-TO-DATE
Action: No updates needed - ready for customer call
```

### Expected Output (Outdated Template)
```
JIRA ID      | Template Status | Current Status | Match | Action
-------------|-----------------|----------------|-------|--------
AAPRFE-762   | Backlog        | In Progress    | ✗     | UPDATE
AAPRFE-1158  | Review         | Closed         | ✗     | UPDATE
AAP-53458    | New            | In Progress    | ✗     | UPDATE

Summary: 6/9 statuses match (67%)
Status: ⚠️  Template is OUTDATED
Action: Run with --update flag to refresh statuses
```

---

## Implementation Details

### Step 1: Parse Template and Extract JIRA IDs
```python
def extract_jira_ids(template_file):
    """Extract all JIRA IDs from markdown template."""
    with open(template_file, 'r') as f:
        content = f.read()
    
    # Regex to find JIRA IDs in markdown links
    # Matches: [AAPRFE-762](https://issues.redhat.com/...)
    # Matches: [AAP-53458](https://issues.redhat.com/...)
    jira_pattern = r'\[(AAP(?:RFE)?-\d+)\]'
    jira_ids = re.findall(jira_pattern, content)
    
    return list(set(jira_ids))  # Deduplicate
```

### Step 2: Query Current JIRA Statuses
```python
def get_current_statuses(jira_ids):
    """Query JIRA API for current statuses."""
    statuses = {}
    for jira_id in jira_ids:
        result = subprocess.run(
            ['rhcase', 'jira', 'fetch', jira_id],
            capture_output=True,
            text=True,
            env={'JIRA_API_TOKEN': os.getenv('JIRA_API_TOKEN')}
        )
        
        # Parse status from rhcase output
        status_match = re.search(r'\| \*\*Status\*\* \| (.+?) \|', result.stdout)
        if status_match:
            statuses[jira_id] = status_match.group(1).strip()
    
    return statuses
```

### Step 3: Compare Template vs Current
```python
def compare_statuses(template_file, current_statuses):
    """Compare template statuses with current JIRA statuses."""
    with open(template_file, 'r') as f:
        lines = f.readlines()
    
    mismatches = []
    for jira_id, current_status in current_statuses.items():
        # Find line in template containing this JIRA ID
        for i, line in enumerate(lines):
            if jira_id in line:
                # Extract status from markdown table
                # Format: | [JIRA](link) | [Case](link) | Description | Status |
                parts = line.split('|')
                if len(parts) >= 5:
                    template_status = parts[4].strip()
                    
                    if template_status != current_status:
                        mismatches.append({
                            'jira_id': jira_id,
                            'line_number': i,
                            'template_status': template_status,
                            'current_status': current_status
                        })
    
    return mismatches
```

### Step 4: Update Template (Optional)
```python
def update_template(template_file, mismatches):
    """Update template with current JIRA statuses."""
    with open(template_file, 'r') as f:
        lines = f.readlines()
    
    for mismatch in mismatches:
        line = lines[mismatch['line_number']]
        # Replace old status with new status in markdown table
        updated_line = line.replace(
            f"| {mismatch['template_status']} |",
            f"| {mismatch['current_status']} |"
        )
        lines[mismatch['line_number']] = updated_line
    
    # Backup original
    backup_file = f"{template_file}.backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    shutil.copy(template_file, backup_file)
    
    # Write updated template
    with open(template_file, 'w') as f:
        f.writelines(lines)
    
    return backup_file
```

---

## Use Cases

### Use Case 1: Quick Pre-Call Check
```bash
# 5 minutes before TD Bank call
tam-rfe-verify-template --file ~/Documents/customers/tdbank/rfe-tracker.md

# Output: ✅ Template is UP-TO-DATE - ready for call
```

### Use Case 2: Auto-Update Before Call
```bash
# Morning of customer call day
tam-rfe-verify-template --customer tdbank --update --notify-slack

# Automatically:
# 1. Checks template
# 2. Updates statuses if changed
# 3. Notifies in Slack: "TD Bank template updated: 2 statuses changed"
```

### Use Case 3: Weekly Verification (Cron Job)
```bash
# Run every Monday at 8am for all customers
0 8 * * 1 tam-rfe-verify-template --all-customers --update --email-report
```

### Use Case 4: CI/CD Integration
```yaml
# GitLab CI job: verify templates on commit
verify-templates:
  script:
    - tam-rfe-verify-template --all-templates --fail-if-outdated
  only:
    - schedules
```

---

## Configuration File

### `~/.config/taminator/template-verification.yaml`
```yaml
# Template verification configuration
templates:
  tdbank:
    file: ~/Documents/customers/tdbank/rfe-tracker.md
    account_number: "540251"
    notification:
      slack: true
      email: jbyrd@redhat.com
      
  wellsfargo:
    file: ~/Documents/customers/wellsfargo/rfe-tracker.md
    account_number: "123456"
    notification:
      slack: true
      email: jbyrd@redhat.com

  jpmc:
    file: ~/Documents/customers/jpmc/rfe-tracker.md
    account_number: "334224"
    notification:
      slack: true
      email: jbyrd@redhat.com

# Global settings
verification:
  auto_backup: true
  backup_retention_days: 30
  fail_on_api_error: false
  
jira:
  api_token_source: env  # or 'keyring'
  rate_limit_delay: 1    # seconds between JIRA queries
```

---

## Benefits

### Time Savings
- **Current:** 10-15 minutes manual verification per customer
- **With Tool:** 30 seconds automated verification per customer
- **Savings:** 90%+ time reduction

### Accuracy Improvement
- **Current:** Manual comparison (error-prone)
- **With Tool:** Automated comparison (100% accurate)

### Confidence Boost
- Enter customer calls knowing data is current
- No surprises during status discussions
- Professional presentation

### Scalability
- Works for 1 customer or 50 customers
- Cron job handles weekly verification
- No additional TAM time required

---

## Real-World Example: TD Bank Call Preparation

### Current Process (15 minutes)
```
08:45 - Open TD Bank template
08:47 - Copy JIRA ID: AAPRFE-762
08:48 - Open browser, go to issues.redhat.com
08:49 - Search for AAPRFE-762
08:50 - Check status: Backlog (unchanged)
08:51 - Repeat for AAPRFE-430...
08:52 - Repeat for AAPRFE-1158...
...
09:00 - Finally ready for call
```

### With Tool (30 seconds)
```
08:59:00 - Run: tam-rfe-verify-template --file tdbank.md
08:59:10 - Output: ✅ Template is UP-TO-DATE (9/9 match)
08:59:30 - Join call (confident and prepared)
```

---

## Implementation Priority

### Phase 1: Core Functionality (Week 1)
- ✅ Parse template and extract JIRA IDs
- ✅ Query JIRA via rhcase
- ✅ Compare statuses
- ✅ Display verification report

### Phase 2: Update Capability (Week 2)
- ⏳ Auto-update template with new statuses
- ⏳ Create backup before updates
- ⏳ Diff display (show what changed)

### Phase 3: Automation (Week 3)
- ⏳ Configuration file support
- ⏳ Multi-customer batch verification
- ⏳ Slack/email notifications

### Phase 4: Advanced Features (Week 4)
- ⏳ Cron job integration
- ⏳ GitLab CI integration
- ⏳ Historical tracking (status change over time)

---

## Success Metrics

- **Adoption:** 80%+ of TAMs using tool within 3 months
- **Time Savings:** 10+ hours per TAM per month
- **Accuracy:** 100% status accuracy before customer calls
- **Satisfaction:** TAM feedback survey > 4.5/5 stars

---

**Next Steps:**
1. Create GitLab issue in taminator project
2. Prototype core parsing and verification logic
3. Test with TD Bank, Wells Fargo, JPMC templates
4. Release v1.6.0 with `tam-rfe-verify-template` command

---

**Related Issues:**
- Feature request for automated template generation
- Integration with Customer Portal API for live updates
- JIRA webhook notifications for status changes

