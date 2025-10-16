# Red Hat RFE Automation Collection Playbooks

This directory contains orchestration playbooks that use the hybrid approach with 4 specialized roles to provide complete RFE automation workflows.

## 📋 **Available Playbooks**

### **Main Orchestration Playbooks**

#### **`generate_all_reports.yml`**
Complete end-to-end workflow that generates all reports and handles notifications/portal posting.

**Usage:**
```bash
ansible-playbook generate_all_reports.yml \
  -e "customer_name=JPMC" \
  -e "account_name=JPMC" \
  -e "account_number=334224" \
  -e "priority_components=['Ansible']" \
  -e "notifications_enabled=true" \
  -e "portal_posting_enabled=true"
```

**Features:**
- Generates both RFE/Bug Tracker and Active Cases reports
- Handles customer portal posting
- Sends multi-channel notifications
- Comprehensive validation and quality assurance
- Complete audit trail and logging

#### **`generate_rfe_bug_report.yml`**
Focused workflow for RFE and Bug case tracking only.

**Usage:**
```bash
ansible-playbook generate_rfe_bug_report.yml \
  -e "customer_name=JPMC" \
  -e "account_name=JPMC" \
  -e "account_number=334224" \
  -e "priority_components=['Ansible']"
```

**Features:**
- RFE/Bug Tracker report generation only
- Intelligent case type detection
- Portal posting (if enabled)
- Notifications (if enabled)

#### **`generate_active_cases_report.yml`**
Focused workflow for active support cases (excluding RFE/Bug cases).

**Usage:**
```bash
ansible-playbook generate_active_cases_report.yml \
  -e "customer_name=JPMC" \
  -e "account_name=JPMC" \
  -e "account_number=334224" \
  -e "priority_components=['Ansible']"
```

**Features:**
- Active Cases report generation only
- External tracker detection (JIRA integration)
- Title-based filtering (`[RFE]`, `[BUG]`)
- Portal posting (if enabled)
- Notifications (if enabled)

### **Customer-Specific Playbooks**

#### **`customer_specific/jpmc_reports.yml`**
Pre-configured workflow for JPMC with their specific requirements.

**Usage:**
```bash
ansible-playbook customer_specific/jpmc_reports.yml
```

**JPMC-Specific Features:**
- Pre-configured customer settings
- Enterprise-grade validation (99% threshold)
- Multi-channel notifications (Email + Slack)
- Aggressive retry settings (5 attempts)
- JPMC-specific portal sections
- Comprehensive audit trail

#### **`customer_specific/template_customer.yml`**
Template for creating customer-specific playbooks.

**Usage:**
1. Copy this template to a new file (e.g., `customer_specific/acme_reports.yml`)
2. Customize the customer-specific settings
3. Run the customized playbook

**Customization Required:**
- `customer_name`: Replace "CUSTOMER_NAME"
- `account_name`: Replace "ACCOUNT_NAME"  
- `account_number`: Replace "ACCOUNT_NUMBER"
- `priority_components`: Replace with actual components
- `email_recipients`: Update with customer contacts
- `slack_channel`: Update with customer Slack channel
- `portal_sections`: Update with customer portal sections

## 🎯 **Playbook Architecture**

### **Hybrid Approach**
Each playbook orchestrates the 4 specialized roles:

1. **`rfe_bug_tracker`** - RFE/Bug report generation
2. **`active_cases`** - Active cases management
3. **`customer_portal`** - Portal integration
4. **`notification_system`** - Multi-channel notifications

### **Role Dependencies**
- Roles can be run independently or together
- Data flows between roles via Ansible variables
- Each role validates its own data and results
- Comprehensive error handling and retry logic

## 🔧 **Configuration Options**

### **Required Variables**
```yaml
customer_name: "Customer Name"
account_name: "Account Name"
account_number: "Account Number"
priority_components: ["Component1", "Component2"]
```

### **Optional Variables**
```yaml
# Paths
rhcase_path: "rhcase"
output_dir: "./output"
logs_dir: "./logs"

# Report Types
report_types: ["rfe_bug_tracker", "active_cases"]

# Validation
validation_threshold: 0.99
data_quality_threshold: 0.95

# Notifications
notifications_enabled: true
notification_methods: ["email", "slack"]

# Portal
portal_posting_enabled: true
portal_auto_post: true
```

## 📊 **Output Structure**

### **Directory Structure**
```
output/
├── customer_name/
│   ├── reports/
│   │   ├── customer_rfe_bug_tracker_report_TIMESTAMP.md
│   │   ├── customer_rfe_bug_tracker_report_TIMESTAMP.json
│   │   ├── customer_active_cases_report_TIMESTAMP.md
│   │   └── customer_active_cases_report_TIMESTAMP.json
│   ├── notifications/
│   │   ├── notification_results_TIMESTAMP.json
│   │   └── notification_metadata_TIMESTAMP.json
│   ├── portal/
│   │   ├── portal_posting_results_TIMESTAMP.json
│   │   └── portal_metadata_TIMESTAMP.json
│   └── customer_workflow_results_TIMESTAMP.json
└── logs/
    └── customer_name/
        ├── reports/
        ├── notifications/
        ├── portal/
        └── customer_workflow_history.log
```

### **Report Files**
- **Markdown Reports**: Human-readable format for review
- **JSON Reports**: Machine-readable format for integration
- **Validation Reports**: Data quality and validation results
- **Workflow Results**: Complete workflow summary and metadata

## 🚀 **Quick Start Examples**

### **Basic RFE/Bug Report**
```bash
ansible-playbook generate_rfe_bug_report.yml \
  -e "customer_name=ACME" \
  -e "account_name=ACME" \
  -e "account_number=123456" \
  -e "priority_components=['Ansible']"
```

### **Complete Workflow with Notifications**
```bash
ansible-playbook generate_all_reports.yml \
  -e "customer_name=ACME" \
  -e "account_name=ACME" \
  -e "account_number=123456" \
  -e "priority_components=['Ansible']" \
  -e "notifications_enabled=true" \
  -e "notification_methods=['email', 'slack']" \
  -e "portal_posting_enabled=true"
```

### **JPMC Enterprise Workflow**
```bash
ansible-playbook customer_specific/jpmc_reports.yml
```

## 🔍 **Validation & Quality Assurance**

### **Built-in Validation**
- Data structure validation
- Data quality scoring (95% threshold)
- Anomaly detection
- Result sanity checking
- External tracker detection validation

### **Quality Metrics**
- Data completeness scoring
- Case type consistency validation
- SBR group distribution validation
- Result consistency checking

## 📧 **Notification Channels**

### **Email**
- HTML-formatted reports
- Professional styling
- Customer-specific branding
- Configurable recipients

### **Slack**
- Rich attachments
- Case summaries
- Interactive elements
- Channel-specific formatting

### **Teams**
- Message cards
- Actionable buttons
- Professional layout
- Customer branding

### **Webhook**
- JSON payloads
- Custom integrations
- Configurable headers
- Event-driven notifications

## 🌐 **Portal Integration**

### **Features**
- Automatic content preparation
- Authentication handling
- Duplicate detection
- Retry logic
- Comprehensive logging

### **Sections**
- RFE/Bug Tracker reports
- Active Cases reports
- Customer-specific sections
- Configurable titles and metadata

## 🔧 **Troubleshooting**

### **Common Issues**
1. **Authentication failures**: Check credential files
2. **Data quality issues**: Review validation reports
3. **Notification failures**: Check recipient validation
4. **Portal posting issues**: Verify portal configuration

### **Debug Mode**
```bash
ansible-playbook generate_all_reports.yml -v
```

### **Log Files**
- Check `logs/customer_name/` for detailed logs
- Review validation reports for data quality issues
- Check notification logs for delivery status

## 📚 **Best Practices**

1. **Always validate data quality** before portal posting
2. **Use customer-specific playbooks** for consistency
3. **Monitor notification delivery** and retry failures
4. **Review validation reports** for data anomalies
5. **Keep audit trails** for compliance requirements

## 🔗 **Related Documentation**

- [Collection README](../README.md)
- [Role Documentation](../roles/)
- [Plugin Documentation](../plugins/)
- [Templates Documentation](../roles/*/templates/)
