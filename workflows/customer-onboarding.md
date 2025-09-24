# Customer Onboarding Workflow for TAM Accounts

## Overview
Comprehensive 10-step workflow for onboarding new TAM customer accounts, integrating manual TAM responsibilities with automated PAI system support.

## Workflow Steps

### Phase 1: Initial Setup (Manual TAM Steps)

#### Step 1: Request New CPG for Customer
**Responsibility**: TAM (Manual)
**Action**: Submit Customer Portal Group (CPG) request through Red Hat internal systems
**Dependencies**: Customer account number, contact information
**Timeline**: 2-3 business days processing
**Documentation**: Track CPG request number for follow-up

#### Step 2: Create KAB Entry for Customer
**Responsibility**: TAM (Manual)
**Action**: Create Knowledge, Advocacy, and Barriers (KAB) entry in Red Hat CRM
**Dependencies**: Customer business context, technical environment
**Timeline**: Within 24 hours of account assignment
**Documentation**: KAB entry ID for reference

#### Step 3: Get Invite to VAT Meetings
**Responsibility**: TAM (Manual)
**Action**: Request addition to Virtual Account Team (VAT) recurring meetings
**Dependencies**: Account Executive coordination, meeting organizer contact
**Timeline**: Within 1 week of account assignment
**Documentation**: Meeting calendar invites, VAT member list

#### Step 4: Get Invite Sent to Sync Meetings
**Responsibility**: TAM (Manual)
**Action**: Request customer-facing sync meeting invitations
**Dependencies**: Customer willingness, stakeholder identification
**Timeline**: Within 2 weeks of account assignment
**Documentation**: Meeting calendar invites, customer attendee list

### Phase 2: PAI System Integration (Automated)

#### Step 5: Creation of Customer Folder Structure
**Responsibility**: PAI Automation
**Command**: `pai-workspace create <account> <customer-name>`
**Location**: `~/Documents/rh/projects/tam-{specialty}/{customer-name}/`
**Structure**:
```
~/Documents/rh/projects/tam-ocp/{customer-name}/
├── account-info/
│   ├── VAT.md
│   ├── contacts.csv
│   └── account-overview.md
├── casework/
│   ├── active/
│   └── closed/
├── communications/
├── coordination/
└── strategic/
```

#### Step 6: Documentation of VAT Members and Contact Tagging
**Responsibility**: PAI Automation
**Process**:
1. Extract VAT member emails from meeting invites
2. Create contact file: `{customer-name}-vat-contacts`
3. Run contact labeling: `cat {file} | pai-contacts-label --label "{customer}-vat"`
4. Document in `account-info/VAT.md`

**Commands**:
```bash
# Extract and label VAT contacts
pai-calendar prep "VAT {customer} meeting"  # Extract attendees
echo "email1@redhat.com" > {customer}-vat-contacts
echo "email2@redhat.com" >> {customer}-vat-contacts
cat {customer}-vat-contacts | pai-contacts-label --label "{customer}-vat"
```

#### Step 7: Documentation of Customer Contacts and Tagging
**Responsibility**: PAI Automation
**Process**:
1. Extract customer emails from sync meeting invites
2. Create contact file: `{customer-name}-customer-contacts`
3. Run contact labeling: `cat {file} | pai-contacts-label --label "{customer}-cust"`
4. Document in `account-info/contacts.csv`

**Commands**:
```bash
# Extract and label customer contacts
pai-calendar prep "Bi-Weekly {customer}/Red Hat sync"  # Extract attendees
echo "contact1@customer.com" > {customer}-customer-contacts
echo "contact2@customer.com" >> {customer}-customer-contacts
cat {customer}-customer-contacts | pai-contacts-label --label "{customer}-cust"
```

#### Step 8: Portal Username Lookup
**Responsibility**: PAI Automation
**Process**:
1. Aggregate all contacts: `cat {customer}-vat-contacts {customer}-customer-contacts > {customer}-all-contacts`
2. Run SSO lookup: Process through `pai-email-to-sso`
3. Generate username mapping: `{customer-name}-sso-usernames`

**Commands**:
```bash
# Create aggregate contact list
cat {customer}-vat-contacts {customer}-customer-contacts > {customer}-all-contacts

# Process for SSO usernames
#!/bin/bash
input_file="{customer}-all-contacts"
output_file="{customer}-sso-usernames"
> "$output_file"

while IFS= read -r email; do
    if [[ -n "$email" ]]; then
        result=$(pai-email-to-sso "$email" 2>&1 | grep -v "LOOKUP_FAILED" | head -1)
        echo "$email -> $result" >> "$output_file"
        sleep 1
    fi
done < "$input_file"
```

### Phase 3: Finalization (Manual TAM Steps)

#### Step 9: Addition of VAT and Customer Contacts to CPG
**Responsibility**: TAM (Manual)
**Action**: Add all identified contacts to the Customer Portal Group
**Dependencies**: CPG approval from Step 1, SSO usernames from Step 8
**Timeline**: After CPG is available and usernames are resolved
**Documentation**: CPG member list, access confirmation

#### Step 10: Addition of Landing Page to CPG
**Responsibility**: TAM (Manual)
**Action**: Create and publish customer-specific landing page in CPG
**Dependencies**: CPG access, customer requirements understanding
**Timeline**: Within 1 week of CPG availability
**Documentation**: Landing page URL, customer feedback

## Implementation Example: Onboarding "NewCorp"

### Manual Steps (TAM)
```bash
# Step 1: CPG Request
# Submit request for NewCorp CPG through internal portal
# Request ID: CPG-2025-NEWCORP-001

# Step 2: KAB Entry
# Create KAB entry in CRM system
# KAB ID: KAB-NEWCORP-2025-001

# Steps 3-4: Meeting Invites
# Request VAT meeting access from AE
# Request customer sync meeting setup
```

### PAI Automation
```bash
# Step 5: Create folder structure
pai-workspace create 1234567 newcorp

# Step 6: VAT contact processing
echo "gnair@redhat.com" > newcorp-vat-contacts
echo "mbauer@redhat.com" >> newcorp-vat-contacts
echo "njoshi@redhat.com" >> newcorp-vat-contacts
cat newcorp-vat-contacts | pai-contacts-label --label "newcorp-vat"

# Step 7: Customer contact processing
echo "john.smith@newcorp.com" > newcorp-customer-contacts
echo "jane.doe@newcorp.com" >> newcorp-customer-contacts
cat newcorp-customer-contacts | pai-contacts-label --label "newcorp-cust"

# Step 8: SSO username lookup
cat newcorp-vat-contacts newcorp-customer-contacts > newcorp-all-contacts
# Process through pai-email-to-sso script (as documented above)
```

### Final Manual Steps (TAM)
```bash
# Steps 9-10: CPG finalization
# Add contacts from newcorp-sso-usernames to CPG
# Create and publish landing page
```

## PAI Tool Integration

### Project Tracking Integration
```bash
# Add onboarding project to PAI tracking
pai-projects  # (manually add to projects.yaml):

newcorp-onboarding:
  category: "customer"
  account: "1234567"
  priority: "high"
  status: "active"
  tasks:
    - id: "newcorp-001"
      task: "CPG request submitted"
      status: "pending"
    - id: "newcorp-002"
      task: "KAB entry created"
      status: "pending"
    - id: "newcorp-003"
      task: "VAT meeting access"
      status: "pending"
    # ... continue for all 10 steps
```

### Automated Checklist Generation
Create automated onboarding project template:

```bash
# Generate onboarding project template
cat > ~/.claude/context/templates/customer-onboarding-template.yaml << 'EOF'
{customer-name}-onboarding:
  category: "customer"
  account: "{account-number}"
  priority: "high"
  status: "active"
  tasks:
    - id: "{customer}-onboard-001"
      task: "CPG request"
      subtask: "submit through internal portal"
      status: "pending"
    - id: "{customer}-onboard-002"
      task: "KAB entry"
      subtask: "create in CRM system"
      status: "pending"
    # ... all 10 steps
EOF
```

## Onboarding Timeline

### Week 1: Foundation
- **Days 1-2**: Steps 1-2 (CPG request, KAB entry)
- **Days 3-5**: Steps 3-4 (VAT and sync meeting access)
- **Day 5**: Step 5 (PAI folder creation)

### Week 2: Contact Integration
- **Days 1-2**: Steps 6-7 (VAT and customer contact documentation)
- **Day 3**: Step 8 (SSO username lookup)
- **Days 4-5**: Step 9 (CPG contact addition)

### Week 3: Completion
- **Days 1-3**: Step 10 (Landing page creation)
- **Days 4-5**: Validation and documentation completion

## Quality Assurance

### Validation Checklist
- [ ] CPG request approved and active
- [ ] KAB entry created and populated
- [ ] VAT meeting calendar access confirmed
- [ ] Customer sync meeting scheduled and accepted
- [ ] PAI folder structure created with all subdirectories
- [ ] VAT contacts documented and labeled in Google Contacts
- [ ] Customer contacts documented and labeled in Google Contacts
- [ ] SSO usernames resolved for all contacts
- [ ] All contacts added to CPG with appropriate permissions
- [ ] Landing page published and customer-accessible

### Success Metrics
- **Time to First Customer Meeting**: Target <2 weeks
- **Contact Resolution Rate**: >90% of emails resolve to SSO usernames
- **CPG Completion**: All contacts accessible within 3 weeks
- **Documentation Quality**: All files created and populated

## Tools Required

### Red Hat Internal Tools
- CPG management portal (manual access)
- CRM system for KAB entries (manual access)
- Internal meeting coordination systems

### PAI Tools Used
- `pai-workspace` - Folder structure creation
- `pai-calendar` - Meeting attendee extraction
- `pai-contacts-label` - Google Contacts organization
- `pai-email-to-sso` - Portal username resolution
- `pai-projects` - Onboarding task tracking

### Google Workspace Tools
- Google Calendar (meeting management)
- Google Contacts (contact organization)
- Google Drive (documentation storage)

## Common Challenges and Solutions

### Challenge: Customer Email Domains Not in Hydra
**Symptom**: `pai-email-to-sso` returns "NOT FOUND" for customer emails
**Solution**: Document external contacts separately, focus on Red Hat VAT usernames
**Workaround**: Use email addresses directly for CPG if SSO lookup fails

### Challenge: Complex Customer Organization Structures
**Symptom**: Multiple customer domains, subsidiary companies
**Solution**: Create multiple contact files per domain, use descriptive labeling
**Example**: `{customer}-finance-contacts`, `{customer}-engineering-contacts`

### Challenge: Large VAT Teams
**Symptom**: 15+ Red Hat team members across multiple specialties
**Solution**: Use PAI contact organization with role-based labeling
**Example**: `{customer}-vat-primary`, `{customer}-vat-secondary`, `{customer}-vat-specialists`

### Challenge: Meeting Scheduling Conflicts
**Symptom**: Customer availability doesn't align with VAT schedules
**Solution**: Document preferred timing, create multiple sync cadences
**Tracking**: Use PAI projects to track scheduling negotiations

## Integration with Existing TAM Workflows

### Case Management Integration
- **Onboarding Tasks**: Track alongside case work using PAI projects
- **Customer Context**: Folder structure supports future case organization
- **Contact Resolution**: SSO usernames enable case escalation paths

### Communication Integration
- **Email Organization**: Google Contacts labeling improves email filtering
- **Meeting Coordination**: Calendar integration streamlines scheduling
- **Documentation**: Structured folder approach supports knowledge management

### Reporting Integration
- **Account Health**: Onboarding completion supports overall account metrics
- **Relationship Mapping**: Contact organization enables relationship tracking
- **Success Metrics**: Timeline tracking supports TAM performance measurement

## Automation Opportunities

### Current PAI Automation (Steps 5-8)
- **Folder Creation**: Automated directory structure generation
- **Contact Processing**: Automated email extraction and labeling
- **Username Resolution**: Automated SSO lookup for portal access
- **Documentation**: Automated file generation and organization

### Future Automation Potential
- **CPG Integration**: API integration for automated CPG requests
- **Calendar Automation**: Automatic meeting scheduling based on availability
- **CRM Integration**: Automated KAB entry population from customer data
- **Landing Page Generation**: Template-based customer portal creation

### Hybrid Approach Benefits
- **Manual Steps**: Maintain personal touch and relationship building
- **Automated Steps**: Ensure consistency and reduce administrative overhead
- **Quality Control**: Human oversight on customer-facing activities
- **Efficiency**: PAI handles repetitive data organization tasks

---

**Workflow Type**: Customer Onboarding
**Duration**: 3 weeks typical
**Manual Steps**: 6 (relationship and approval focused)
**Automated Steps**: 4 (data organization and processing)
**Success Rate**: Target >95% completion within timeline
**Integration**: Full PAI ecosystem support