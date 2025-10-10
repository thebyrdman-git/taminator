# Red Hat RFE Automation Collection

A comprehensive Ansible collection for automating Red Hat RFE (Request for Enhancement) and case management workflows.

## Overview

This collection provides specialized roles and playbooks for:
- **RFE/Bug Tracker Reports**: Comprehensive tracking of Feature Requests and Bug Reports
- **Active Cases Reports**: Management of active support cases with intelligent filtering
- **External Tracker Detection**: Automatic detection of JIRA and other external tracking systems
- **Data Validation**: Comprehensive quality assurance and validation mechanisms

## Collection Structure

```
redhat.rfe_automation/
├── roles/
│   ├── rfe_bug_tracker/          # RFE/Bug Tracker Report generation
│   ├── active_cases/             # Active Cases Report generation
│   └── rfe_reports/              # Legacy combined role (deprecated)
├── playbooks/
│   ├── generate_rfe_bug_report.yml
│   ├── generate_active_cases_report.yml
│   └── generate_all_reports.yml
└── docs/
    ├── getting_started.md
    ├── role_documentation.md
    └── examples/
```

## Installation

```bash
# Install from Galaxy (when published)
ansible-galaxy collection install redhat.rfe_automation

# Or install from local source
ansible-galaxy collection install -p ./collections .
```

## Quick Start

### Generate RFE/Bug Tracker Report

```yaml
---
- name: Generate RFE/Bug Tracker Report
  hosts: localhost
  gather_facts: yes
  collections:
    - redhat.rfe_automation
  vars:
    customer_name: "JPMC"
    account_name: "JPMC"
    account_number: "334224"
    priority_components: ["Ansible"]
    rhcase_path: "rhcase"
    output_dir: "./output"
    logs_dir: "./logs"
  roles:
    - role: rfe_bug_tracker
```

### Generate Active Cases Report

```yaml
---
- name: Generate Active Cases Report
  hosts: localhost
  gather_facts: yes
  collections:
    - redhat.rfe_automation
  vars:
    customer_name: "JPMC"
    account_name: "JPMC"
    account_number: "334224"
    priority_components: ["Ansible"]
    rhcase_path: "rhcase"
    output_dir: "./output"
    logs_dir: "./logs"
  roles:
    - role: active_cases
```

## Key Features

### 🎯 **RFE/Bug Tracker Role**
- Intelligent case type detection
- Dynamic filtering based on case types
- Comprehensive validation and quality assurance
- JSON and Markdown report generation

### 📋 **Active Cases Role**
- Advanced filtering logic (title-based + external tracker detection)
- JIRA integration detection (`issues.redhat.com`, `jira.redhat.com`)
- Priority component filtering
- Self-validating mechanisms

### 🔍 **External Tracker Detection**
- Automatic detection of JIRA references in case content
- Multi-field search (subject, description, tags)
- Prevents duplicate tracking across systems

### ✅ **Data Validation**
- Comprehensive data quality scoring
- Anomaly detection and reporting
- Configurable validation thresholds
- Self-healing capabilities

## Requirements

- **Ansible**: >= 2.9
- **Python**: >= 3.6
- **rhcase**: Red Hat case management tool
- **Red Hat VPN**: Required for rhcase access

## Configuration

### Required Variables

```yaml
customer_name: "Customer Name"
account_name: "Account Name" 
account_number: "Account Number"
priority_components: ["Ansible", "OpenShift", "RHEL"]
rhcase_path: "rhcase"
output_dir: "./output"
logs_dir: "./logs"
```

### Optional Variables

```yaml
validation_threshold: 0.99
data_quality_threshold: 0.95
report_types: ["rfe_bug_tracker", "active_cases"]
enable_debug: false
```

## Examples

See the `docs/examples/` directory for comprehensive usage examples.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

GPL-3.0-or-later

## Support

For issues and questions:
- GitHub Issues: https://github.com/redhat/rfe-automation/issues
- Red Hat Internal: Contact TAM Operations team
