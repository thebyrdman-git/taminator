# Ansible Implementation Guide - RFE Automation Tool

## Overview

The RFE Automation Tool now uses **Ansible playbooks with structured variables** to generate consistent, reliable reports. This enterprise-grade approach ensures reproducible results across all customers and environments.

## Key Benefits

### 🎯 **Consistent Results**
- **Structured Variables**: Customer data stored in YAML inventory files
- **Template-Based**: Jinja2 templates ensure consistent formatting
- **Validation Integration**: Built-in content validation with 99%+ accuracy requirements

### 🔧 **Enterprise-Grade Automation**
- **Idempotent Operations**: Safe to run multiple times
- **Error Handling**: Comprehensive error checking and logging
- **Audit Trail**: Complete execution logging and reporting

### 📊 **Scalable Architecture**
- **Multi-Customer Support**: Process multiple customers in single execution
- **Flexible Configuration**: Easy to add new customers and components
- **Modular Design**: Separate roles for different report types

## Architecture

```
ansible/
├── inventory/
│   └── customers.yml          # Customer account numbers, group IDs, config
├── playbooks/
│   └── generate_rfe_reports.yml  # Main execution playbook
├── roles/
│   └── rfe-reports/
│       ├── tasks/
│       │   ├── main.yml           # Main task orchestration
│       │   ├── generate_rfe_report.yml
│       │   ├── generate_active_cases_report.yml
│       │   ├── validate_report.yml
│       │   └── post_to_portal.yml
│       ├── templates/
│       │   ├── jpmc_rfe_bug_report.j2
│       │   ├── active_cases_report.j2
│       │   ├── report_summary.j2
│       │   └── execution_summary.j2
│       └── vars/
│           └── main.yml           # Default variables
└── ansible.cfg                # Ansible configuration
```

## Customer Configuration

### Inventory Structure (`ansible/inventory/customers.yml`)

```yaml
all:
  children:
    customers:
      children:
        jpmc:
          vars:
            customer_name: "JPMorgan Chase"
            account_number: "838043"
            account_name: "JPMorgan Chase & Co"
            portal_group_id: "jpmc-rfe-group"
            priority_components:
              - "OpenShift"
              - "RHEL"
              - "Ansible"
              - "Satellite"
            report_frequency: "weekly"
            validation_threshold: 0.99
          hosts:
            jpmc-rfe-system:
              ansible_host: localhost
              ansible_connection: local
```

### Key Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `customer_name` | Display name for reports | "JPMorgan Chase" |
| `account_number` | Red Hat account number | "838043" |
| `account_name` | Account name for rhcase | "JPMorgan Chase & Co" |
| `portal_group_id` | Customer portal group ID | "jpmc-rfe-group" |
| `priority_components` | List of priority components | ["OpenShift", "RHEL"] |
| `report_frequency` | How often to generate reports | "weekly" |
| `validation_threshold` | Minimum accuracy score | 0.99 |

## Usage

### Basic Commands

```bash
# Generate reports for all customers
./bin/ansible-rfe-generate

# Generate report for specific customer
./bin/ansible-rfe-generate jpmc

# List available customers
./bin/ansible-rfe-generate --list

# Dry run (show what would be done)
./bin/ansible-rfe-generate --dry-run

# Check mode (no changes)
./bin/ansible-rfe-generate --check
```

### Advanced Options

```bash
# Generate only RFE/Bug tracker reports
./bin/ansible-rfe-generate --rfe-only

# Generate only Active Cases reports
./bin/ansible-rfe-generate --active-only

# Skip content validation
./bin/ansible-rfe-generate --no-validation

# Verbose output
./bin/ansible-rfe-generate --verbose
```

## Report Generation Process

### 1. **System Validation**
- Check rhcase tool availability
- Verify customer account configuration
- Validate template files

### 2. **Data Collection**
- Execute `rhcase` with customer-specific filters
- Parse JSON output for case data
- Filter cases by type and status

### 3. **Report Generation**
- Apply Jinja2 templates with customer data
- Generate markdown and JSON versions
- Create structured output files

### 4. **Content Validation**
- Run enterprise-grade validation (99%+ accuracy)
- Check data format, consistency, and completeness
- Generate validation reports

### 5. **Portal Posting** (Optional)
- Post reports to Red Hat Customer Portal
- Handle API authentication and errors
- Log posting results

## Output Structure

```
output/
├── jpmc_rfe_bug_report_1703123456.md      # Markdown report
├── jpmc_rfe_bug_report_1703123456.json    # JSON data
├── jpmc_active_cases_1703123456.md        # Active cases report
├── jpmc_validation_1703123456.json        # Validation results
├── jpmc_1703123456_summary.md             # Customer summary
└── execution_summary_1703123456.md        # Overall execution summary

logs/
├── rfe_reports.log                        # RFE report generation logs
├── active_cases.log                       # Active cases logs
├── validation.log                         # Validation results
├── portal_posts.log                       # Portal posting logs
└── ansible.log                           # Ansible execution logs
```

## Adding New Customers

### 1. **Update Inventory**
Add customer configuration to `ansible/inventory/customers.yml`:

```yaml
newcustomer:
  vars:
    customer_name: "New Customer"
    account_number: "123456"
    account_name: "New Customer Inc"
    portal_group_id: "newcustomer-rfe-group"
    priority_components:
      - "OpenShift"
      - "RHEL"
    report_frequency: "weekly"
    validation_threshold: 0.99
  hosts:
    newcustomer-rfe-system:
      ansible_host: localhost
      ansible_connection: local
```

### 2. **Test Configuration**
```bash
# Validate inventory
ansible-inventory -i ansible/inventory/customers.yml --list

# Test customer-specific execution
./bin/ansible-rfe-generate newcustomer --dry-run
```

### 3. **Generate Reports**
```bash
# Generate reports for new customer
./bin/ansible-rfe-generate newcustomer
```

## Validation System

### Accuracy Thresholds
- **99%+ (0.99)**: Enterprise-grade - Ready for customer distribution
- **95-98% (0.95-0.98)**: Acceptable for internal use
- **<95% (<0.95)**: Critical issues - Fix before distribution

### Validation Checks
- **Data Format**: Case numbers, JIRA IDs, dates
- **Logical Consistency**: Active vs closed case counts
- **Product Classification**: Component mapping accuracy
- **Duplicate Detection**: Prevent duplicate case entries
- **Cross-Section Validation**: Consistency across report sections

## Troubleshooting

### Common Issues

#### **rhcase Tool Not Found**
```bash
# Install dependencies
./bin/install-dependencies

# Verify installation
ls -la rhcase/.venv/bin/rhcase
```

#### **Customer Account Not Found**
```bash
# Check account configuration
ansible-inventory -i ansible/inventory/customers.yml --host jpmc

# Verify account name in rhcase config
rhcase --list-accounts
```

#### **Validation Failures**
```bash
# Check validation report
cat output/customer_validation_TIMESTAMP.json

# Review validation logs
tail -f logs/validation.log
```

#### **Template Errors**
```bash
# Validate Jinja2 syntax
python3 -c "from jinja2 import Template; Template(open('templates/report.j2').read())"

# Check template variables
ansible-playbook --syntax-check ansible/playbooks/generate_rfe_reports.yml
```

### Debug Mode
```bash
# Enable verbose output
./bin/ansible-rfe-generate --verbose

# Check Ansible logs
tail -f logs/ansible.log
```

## Best Practices

### 1. **Configuration Management**
- Keep customer data in inventory files
- Use version control for all configurations
- Document customer-specific requirements

### 2. **Template Development**
- Use consistent variable naming
- Include error handling in templates
- Test templates with sample data

### 3. **Validation**
- Always enable content validation for customer reports
- Review validation results before distribution
- Maintain 99%+ accuracy standards

### 4. **Monitoring**
- Set up automated execution schedules
- Monitor log files for errors
- Track validation scores over time

## Integration with Existing Tools

### **rhcase Integration**
- Uses structured account names from inventory
- Applies customer-specific component filters
- Parses JSON output for consistent data processing

### **Validation System**
- Integrates with existing `ReportContentValidator`
- Maintains enterprise-grade accuracy standards
- Provides detailed validation reports

### **Portal Posting**
- Compatible with existing portal API client
- Uses customer-specific group IDs
- Handles authentication and error cases

## Future Enhancements

### **Scheduled Execution**
- Cron job integration for automated reports
- CI/CD pipeline integration
- Email notifications for completion

### **Advanced Analytics**
- Historical trend analysis
- Component performance metrics
- Customer satisfaction tracking

### **Multi-Environment Support**
- Development, staging, production environments
- Environment-specific configurations
- Automated testing and validation

---

*This Ansible-based implementation provides enterprise-grade reliability and consistency for RFE report generation, ensuring accurate and professional reports for all customers.*
