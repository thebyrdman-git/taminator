# pai-onboard-customer

## Purpose
Automated customer onboarding workflow tool that handles PAI system integration steps (5-8) of the comprehensive 10-step customer onboarding process.

## Location
`~/.local/bin/pai-onboard-customer`

## Description
`pai-onboard-customer` automates the data organization and system integration aspects of customer onboarding, while leaving relationship-building and approval steps to manual TAM execution. It creates folder structures, processes contact lists, resolves portal usernames, and generates completion documentation.

## Key Features
- **Automated Folder Creation**: Standard customer directory structure
- **Contact Processing**: Google Contacts labeling and organization
- **SSO Username Resolution**: Portal access preparation
- **Progress Tracking**: Status monitoring and completion reporting
- **Template Integration**: Uses standardized onboarding checklists
- **Audit Logging**: Complete onboarding activity tracking

## Usage

### Complete Customer Onboarding Example

```bash
# Step 5: Initialize new customer
pai-onboard-customer init newcorp 1234567 tam-ocp

# Step 6: Process VAT member emails (after extracting from meeting)
pai-onboard-customer vat-contacts newcorp vat-members.txt

# Step 7: Process customer emails (after extracting from meeting)
pai-onboard-customer customer-contacts newcorp customer-attendees.txt

# Step 8: Resolve portal usernames for CPG access
pai-onboard-customer sso-lookup newcorp

# Check progress and generate report
pai-onboard-customer status newcorp
pai-onboard-customer complete newcorp
```

### Commands

#### init - Initialize Customer Onboarding
```bash
pai-onboard-customer init <customer> <account> <specialty>
```

**Parameters**:
- `customer`: Customer name (lowercase, used for folder naming)
- `account`: Red Hat account number
- `specialty`: TAM specialty (tam-ocp, tam-ai, tam-sec)

**Actions**:
- Creates standard folder structure
- Generates onboarding checklist from template
- Sets up strategic planning directory
- Creates account-info documentation structure

**Example**:
```bash
pai-onboard-customer init discover 999625 tam-ocp
```

#### vat-contacts - Process VAT Member Contacts
```bash
pai-onboard-customer vat-contacts <customer> <emails-file>
```

**Parameters**:
- `customer`: Customer name (must match init)
- `emails-file`: Text file with VAT member emails, one per line

**Actions**:
- Copies emails to customer strategic directory
- Labels contacts in Google Contacts with `{customer}-vat` tag
- Creates VAT.md documentation
- Updates account-info with VAT member list

**Example**:
```bash
echo "gnair@redhat.com" > vat-list.txt
echo "mbauer@redhat.com" >> vat-list.txt
pai-onboard-customer vat-contacts discover vat-list.txt
```

#### customer-contacts - Process Customer Contacts
```bash
pai-onboard-customer customer-contacts <customer> <emails-file>
```

**Parameters**:
- `customer`: Customer name (must match init)
- `emails-file`: Text file with customer emails, one per line

**Actions**:
- Copies emails to customer strategic directory
- Labels contacts in Google Contacts with `{customer}-cust` tag
- Updates contacts.csv with customer contact information
- Prepares for portal access setup

**Example**:
```bash
echo "john.smith@discover.com" > customer-list.txt
echo "jane.doe@discover.com" >> customer-list.txt
pai-onboard-customer customer-contacts discover customer-list.txt
```

#### sso-lookup - Resolve Portal Usernames
```bash
pai-onboard-customer sso-lookup <customer>
```

**Parameters**:
- `customer`: Customer name (must have contact files processed)

**Actions**:
- Aggregates all contact files (VAT + Customer)
- Processes through `pai-email-to-sso` for username resolution
- Generates username mapping file for CPG access
- Reports resolution success rate

**Example**:
```bash
pai-onboard-customer sso-lookup discover
# Processes all discover contacts and creates discover-sso-usernames
```

#### status - Check Onboarding Progress
```bash
pai-onboard-customer status <customer>
```

**Output Example**:
```
📋 Onboarding Status: discover
==================================================
📁 Folder Structure
✓ Customer directory created
✓ account-info/
✓ casework/
✓ communications/
✓ coordination/
✓ strategic/

👥 Contact Processing
✓ VAT contacts: 18 processed
✓ Customer contacts: 9 processed
✓ SSO usernames: 24/27 resolved

📄 Documentation
✓ Onboarding checklist created
✓ VAT documentation created

Customer directory: /home/grimm/Documents/rh/projects/tam-ocp/discover
```

#### complete - Generate Completion Report
```bash
pai-onboard-customer complete <customer>
```

**Actions**:
- Generates comprehensive completion report
- Summarizes all automated steps completed
- Lists remaining manual steps for TAM
- Documents all generated files and their locations

## Integration with 10-Step Workflow

### Manual Steps (TAM Responsibility)
1. **CPG Request** - Submit through Red Hat internal systems
2. **KAB Entry** - Create in CRM system
3. **VAT Meeting Access** - Coordinate with Account Executive
4. **Sync Meeting Setup** - Coordinate with customer stakeholders
9. **CPG Contact Addition** - Use SSO usernames from Step 8
10. **Landing Page Creation** - Design and publish in CPG

### Automated Steps (PAI Responsibility)
5. **Folder Creation** - `pai-onboard-customer init`
6. **VAT Contact Processing** - `pai-onboard-customer vat-contacts`
7. **Customer Contact Processing** - `pai-onboard-customer customer-contacts`
8. **SSO Username Resolution** - `pai-onboard-customer sso-lookup`

## Generated File Structure

### Customer Directory Layout
```
~/Documents/rh/projects/tam-{specialty}/{customer}/
├── onboarding-checklist.md              # Customized checklist
├── onboarding-completion-report.md      # Final report
├── account-info/
│   ├── VAT.md                           # VAT member documentation
│   └── contacts.csv                     # Customer contact database
├── casework/
│   ├── active/                          # Future case organization
│   └── closed/                          # Closed case archive
├── communications/                       # Email and message archive
├── coordination/                         # Meeting notes and planning
└── strategic/
    ├── {customer}-vat-contacts          # VAT email list
    ├── {customer}-customer-contacts     # Customer email list
    ├── {customer}-all-contacts          # Aggregated contact list
    └── {customer}-sso-usernames         # Username mapping for CPG
```

### Google Contacts Integration
**Contact Labels Created**:
- `{customer}-vat` - Red Hat VAT team members
- `{customer}-cust` - Customer stakeholders

**Benefits**:
- Easy email filtering and communication targeting
- Quick access to customer-specific contacts
- Integration with existing Google Workspace workflow

## Error Handling and Recovery

### Common Issues

#### Customer Directory Already Exists
**Symptom**: Warning during `init` command
**Solution**: Continue with processing, existing structure preserved
**Prevention**: Check with `status` command before `init`

#### Contact Labeling Failures
**Symptom**: Warnings during contact processing
**Cause**: Google Contacts API rate limits or authentication
**Solution**: Re-run specific contact processing step
**Recovery**: `pai-contacts-label` can be run independently

#### SSO Lookup Timeouts
**Symptom**: Partial username resolution
**Cause**: Hydra API latency or rate limiting
**Solution**: Re-run `sso-lookup` command (resumes from last position)
**Monitoring**: Check resolution rate in status output

#### Missing Email Files
**Symptom**: "Emails file not found" error
**Cause**: Incorrect file path or file not created
**Solution**: Extract emails from meeting invites manually
**Prevention**: Verify file existence before running commands

### Recovery Procedures

#### Partial Onboarding Completion
```bash
# Check what's completed
pai-onboard-customer status customer-name

# Re-run specific steps as needed
pai-onboard-customer vat-contacts customer-name corrected-vat-list.txt
pai-onboard-customer sso-lookup customer-name
```

#### Complete Restart
```bash
# Remove customer directory (careful!)
rm -rf ~/Documents/rh/projects/tam-specialty/customer-name

# Start fresh
pai-onboard-customer init customer-name account-number tam-specialty
```

## Integration with PAI Project Tracking

### Onboarding as PAI Project
Add customer onboarding to PAI project tracking:

```yaml
# Add to ~/.claude/context/create/outputs/projects/projects.yaml
newcorp-onboarding:
  category: "customer"
  account: "1234567"
  priority: "high"
  status: "active"
  tasks:
    - id: "newcorp-onboard-001"
      task: "CPG request submitted"
      status: "pending"
    - id: "newcorp-onboard-005"
      task: "PAI folder structure"
      status: "completed"
    - id: "newcorp-onboard-006"
      task: "VAT contact processing"
      status: "completed"
    # ... etc
```

### Mobile Tracking
Onboarding tasks will appear in Google Tasks as:
- `PAI-Customer-NewcorpOnboarding`
- Individual tasks for each onboarding step
- Status updates sync from mobile back to PAI

## Performance and Scalability

### Typical Execution Times
- **init**: 1-2 seconds (folder creation)
- **vat-contacts**: 30-60 seconds (depends on contact count and Google API)
- **customer-contacts**: 30-60 seconds (depends on contact count and Google API)
- **sso-lookup**: 1-2 minutes per 10 contacts (Hydra API latency)

### Resource Requirements
- **Disk Space**: ~1MB per customer for documentation
- **Network**: Google Contacts API and Hydra API access required
- **Authentication**: Google Workspace OAuth and Red Hat Hydra credentials

### Concurrent Operations
- **Rate Limiting**: Built-in delays for API compliance
- **Lock Files**: Prevent conflicts with other PAI operations
- **Error Resilience**: Graceful handling of API failures

## Best Practices

### Preparation
1. **Gather Information**: Collect customer name, account number, specialty before starting
2. **Meeting Coordination**: Ensure VAT and sync meetings are scheduled before contact extraction
3. **Email Lists**: Prepare clean email lists (one email per line, no headers)

### Execution
1. **Run in Sequence**: Complete steps 5-8 in order for proper dependencies
2. **Monitor Progress**: Use `status` command between steps
3. **Verify Results**: Check Google Contacts and file generation after each step

### Quality Control
1. **Review SSO Results**: Check username resolution rates before CPG addition
2. **Validate Contacts**: Ensure contact labeling worked correctly in Google Contacts
3. **Document Issues**: Note any problems in onboarding checklist for follow-up

## Integration Points

### PAI System Integration
- **Folder Structure**: Aligns with existing customer account organization
- **Contact System**: Integrates with Google Contacts labeling used elsewhere
- **Username Resolution**: Uses existing `pai-email-to-sso` infrastructure
- **Project Tracking**: Compatible with PAI project management system

### Red Hat Systems Integration
- **CPG Workflow**: Prepares usernames for CPG access management
- **VAT Process**: Supports existing Virtual Account Team coordination
- **Customer Sync**: Enables regular customer-facing meeting cadence
- **Documentation**: Creates audit trail for account management

---

**Tool Type**: Customer onboarding automation
**Integration**: PAI ecosystem and Google Workspace
**Automation Level**: Steps 5-8 fully automated
**Manual Coordination**: Steps 1-4, 9-10 require TAM execution
**Success Metrics**: 3-week onboarding completion target