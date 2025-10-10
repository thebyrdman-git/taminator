# Ansible Task Structure Guide - RFE Automation Tool

## Overview

The RFE Automation Tool uses a **refined task-based structure** that balances granularity with maintainability. This approach follows Ansible best practices while providing the flexibility needed for enterprise-grade report generation.

## Architecture Decision: Task Files vs Playbooks

### ✅ **Recommended: Task Files (Current Approach)**

**Why task files are optimal:**

1. **Logical Workflow**: Each task file represents a distinct phase of the report generation process
2. **Conditional Execution**: Tasks can be skipped or included based on conditions
3. **Reusability**: Task files can be reused across different scenarios
4. **Maintainability**: Easy to modify specific functionality without affecting others
5. **Testing**: Individual components can be tested in isolation
6. **Ansible Best Practice**: This is the recommended pattern for complex workflows

### ❌ **Not Recommended: Separate Playbooks**

**Why separate playbooks would be problematic:**

- **Complex Orchestration**: Multiple playbooks need complex coordination
- **Variable Passing**: Difficult to share variables between playbooks
- **Error Handling**: Harder to handle failures across playbooks
- **Execution Complexity**: Users would need to run multiple commands
- **State Management**: Difficult to maintain state across playbook executions

## Current Task Structure

```
ansible/roles/rfe-reports/tasks/
├── main.yml                    # Main orchestration (includes all task files)
├── 01_prerequisites.yml        # System validation and setup
├── 02_data_collection.yml      # rhcase data collection and parsing
├── 03_report_generation.yml    # Template-based report generation
├── 04_validation.yml           # Content validation and quality checks
├── 05_portal_posting.yml       # Optional portal API posting
└── 06_summary.yml              # Summary generation and cleanup
```

## Task File Details

### 1. **01_prerequisites.yml** - System Validation
**Purpose**: Ensure system is ready for report generation

**Key Tasks**:
- Create output directories
- Validate rhcase tool availability
- Check customer configuration
- Display customer information

**Tags**: `prerequisites`, `setup`, `validation`

**Example Usage**:
```bash
# Run only prerequisites
ansible-playbook -i inventory/customers.yml playbooks/generate_rfe_reports.yml --tags prerequisites
```

### 2. **02_data_collection.yml** - Data Collection
**Purpose**: Collect and parse data from rhcase

**Key Tasks**:
- Execute rhcase commands with customer-specific filters
- Parse JSON output from rhcase
- Filter cases by type (RFE, Bug, Closed)
- Collect active cases for Active Cases reports

**Tags**: `data_collection`, `rfe_cases`, `active_cases`, `filtering`

**Example Usage**:
```bash
# Run only data collection
ansible-playbook -i inventory/customers.yml playbooks/generate_rfe_reports.yml --tags data_collection
```

### 3. **03_report_generation.yml** - Report Generation
**Purpose**: Generate reports using Jinja2 templates

**Key Tasks**:
- Generate RFE/Bug tracker reports (markdown)
- Generate JSON data files
- Generate Active Cases reports
- Log generation results

**Tags**: `report_generation`, `rfe_bug_tracker`, `active_cases`

**Example Usage**:
```bash
# Run only report generation
ansible-playbook -i inventory/customers.yml playbooks/generate_rfe_reports.yml --tags report_generation
```

### 4. **04_validation.yml** - Content Validation
**Purpose**: Validate report content for accuracy and quality

**Key Tasks**:
- Run content validation using ReportContentValidator
- Parse validation results
- Check accuracy thresholds (99%+ for customer reports)
- Fail execution if validation fails

**Tags**: `validation`, `content_validation`, `threshold_check`

**Example Usage**:
```bash
# Run only validation
ansible-playbook -i inventory/customers.yml playbooks/generate_rfe_reports.yml --tags validation
```

### 5. **05_portal_posting.yml** - Portal Posting
**Purpose**: Post reports to Red Hat Customer Portal (optional)

**Key Tasks**:
- Check API credentials
- Post reports to customer portal groups
- Log posting results
- Handle API errors gracefully

**Tags**: `portal_posting`, `api`, `credentials_check`

**Example Usage**:
```bash
# Run only portal posting
ansible-playbook -i inventory/customers.yml playbooks/generate_rfe_reports.yml --tags portal_posting
```

### 6. **06_summary.yml** - Summary and Cleanup
**Purpose**: Generate summaries and clean up temporary files

**Key Tasks**:
- Generate customer-specific summaries
- Generate execution summaries
- Display completion messages
- Clean up temporary files

**Tags**: `summary`, `cleanup`, `completion`

**Example Usage**:
```bash
# Run only summary tasks
ansible-playbook -i inventory/customers.yml playbooks/generate_rfe_reports.yml --tags summary
```

## Tag-Based Execution

### **Selective Execution**
You can run specific phases of the workflow using tags:

```bash
# Run only prerequisites and data collection
./bin/ansible-rfe-generate --tags prerequisites,data_collection

# Run only report generation and validation
./bin/ansible-rfe-generate --tags report_generation,validation

# Skip portal posting
./bin/ansible-rfe-generate --skip-tags portal_posting
```

### **Common Tag Combinations**
```bash
# Quick validation check
--tags prerequisites,data_collection,validation

# Generate reports without posting
--tags prerequisites,data_collection,report_generation,validation,summary

# Full workflow
--tags all
```

## Benefits of This Structure

### 🎯 **Maintainability**
- **Single Responsibility**: Each task file has a clear, focused purpose
- **Easy Debugging**: Can run individual phases to isolate issues
- **Clear Dependencies**: Task execution order is explicit and logical

### 🔧 **Flexibility**
- **Conditional Execution**: Tasks can be skipped based on conditions
- **Tag-Based Control**: Run specific phases as needed
- **Customer-Specific**: Different customers can have different workflows

### 📊 **Scalability**
- **Add New Phases**: Easy to add new task files for new functionality
- **Modify Existing**: Change individual phases without affecting others
- **Reuse Components**: Task files can be reused in different contexts

### 🛡️ **Reliability**
- **Error Isolation**: Failures in one phase don't affect others
- **Validation Gates**: Built-in validation prevents bad data from propagating
- **Rollback Capability**: Can re-run specific phases after fixes

## Best Practices

### 1. **Task File Naming**
- Use numbered prefixes for execution order: `01_prerequisites.yml`
- Use descriptive names: `data_collection.yml` not `data.yml`
- Keep names consistent with functionality

### 2. **Tag Usage**
- Use consistent tag naming across task files
- Group related tags: `[validation, content_validation, threshold_check]`
- Use hierarchical tags: `prerequisites` and `prerequisites,setup`

### 3. **Error Handling**
- Use `fail` tasks for critical errors
- Use `ignore_errors: yes` for non-critical tasks
- Provide clear error messages with context

### 4. **Logging**
- Log key events in each task file
- Use consistent log formats
- Include timestamps and customer context

## Migration from Old Structure

The new structure maintains backward compatibility while providing better organization:

### **Old Structure**:
```
tasks/
├── main.yml
├── generate_rfe_report.yml
├── generate_active_cases_report.yml
├── validate_report.yml
└── post_to_portal.yml
```

### **New Structure**:
```
tasks/
├── main.yml                    # Orchestrates numbered task files
├── 01_prerequisites.yml        # System validation
├── 02_data_collection.yml      # Data collection (combines old files)
├── 03_report_generation.yml    # Report generation (combines old files)
├── 04_validation.yml           # Content validation
├── 05_portal_posting.yml       # Portal posting
└── 06_summary.yml              # Summary and cleanup
```

## Future Enhancements

### **Potential Additions**:
- `07_notifications.yml` - Email/Slack notifications
- `08_analytics.yml` - Report analytics and metrics
- `09_archival.yml` - Report archival and cleanup
- `10_monitoring.yml` - System health monitoring

### **Advanced Features**:
- **Parallel Execution**: Run data collection for multiple customers in parallel
- **Caching**: Cache rhcase results to reduce API calls
- **Incremental Updates**: Only process changed data
- **Multi-Environment**: Support for dev/staging/prod environments

## Conclusion

The **task-based structure with numbered files** provides the optimal balance of:

- **Granularity**: Each phase is clearly defined and testable
- **Maintainability**: Easy to modify and extend individual components
- **Usability**: Simple execution with tag-based control
- **Reliability**: Robust error handling and validation

This approach is **not too granular** - it provides the right level of organization for enterprise-grade automation while maintaining simplicity and usability.

---

*This structure follows Ansible best practices and provides a solid foundation for scalable, maintainable RFE report automation.*
