# RFE Report Validation Guide

## Overview

This guide explains how to ensure your RFE reports are both **functionally correct** and **content accurate**. The RFE automation tool now includes comprehensive validation systems that check both system functionality and report content quality.

## Why Validation Matters

### System Functionality Validation
- **Connectivity**: Ensures you can connect to Red Hat systems
- **Authentication**: Verifies your credentials work properly
- **Dependencies**: Checks that all required tools are installed
- **Configuration**: Validates customer setup and account numbers

### Content Accuracy Validation
- **Data Format**: Verifies case numbers, RFE IDs, and Bug IDs follow correct formats
- **Logical Consistency**: Ensures cases aren't duplicated across sections
- **Product Classification**: Validates that products match case content
- **Date Accuracy**: Checks that dates are valid and logical
- **Cross-Section Validation**: Ensures no case appears in both active and closed sections

## Quick Start: Running Validation

### Full Validation (Recommended)
```bash
# Validate everything for a customer
./bin/validate-rfe-reports wellsfargo

# Validate with detailed output
./bin/validate-rfe-reports wellsfargo --verbose
```

### System-Only Validation
```bash
# Check system functionality only
./bin/validate-rfe-reports --system-only
```

### Content-Only Validation
```bash
# Check report content accuracy only
./bin/validate-rfe-reports wellsfargo --content-only
```

## Understanding Validation Results

### System Validation Results

#### ✅ Success Indicators
- Python 3 is available
- All required Python modules installed
- rhcase tool is accessible
- RFE verification system passes
- Customer configuration is valid

#### ❌ Failure Indicators
- Missing Python modules
- rhcase tool not found
- Authentication failures
- Network connectivity issues
- Invalid customer configuration

### Content Validation Results

#### Accuracy Score (Enterprise Standards)
- **0.99+ (99%+)**: Enterprise-grade - Report ready for customer distribution
- **0.95-0.98 (95-98%)**: Acceptable for internal use - Review before customer distribution
- **0.90-0.94 (90-94%)**: Poor - Significant issues, fix before any distribution
- **<0.90 (<90%)**: Critical - Major accuracy problems, do not use

#### Issue Severity Levels

**🔴 Critical Issues**
- Cases appearing in both active and closed sections
- Invalid case number formats
- False information in reports

**🟡 High Issues**
- Invalid RFE or Bug ID formats
- Missing required data fields
- Logical inconsistencies

**🟠 Medium Issues**
- Product classification mismatches
- Invalid date formats
- Minor formatting issues

**🟢 Low Issues**
- Presentation problems
- Minor formatting inconsistencies

## Common Validation Issues and Solutions

### System Issues

#### "rhcase tool not found"
**Solution**: Run the dependency installer
```bash
./bin/install-dependencies
```

#### "Missing Python modules"
**Solution**: Install required modules
```bash
pip3 install requests yaml
```

#### "Authentication failed"
**Solution**: Check your Red Hat SSO credentials
```bash
# Test rhcase authentication
./rhcase/rhcase auth test
```

### Content Issues

#### "Invalid case number format"
**Problem**: Case numbers must be exactly 8 digits
**Solution**: Verify case numbers in your data source

#### "Case appears in multiple sections"
**Problem**: Same case number in both active and closed sections
**Solution**: Check case status in Red Hat systems, remove from incorrect section

#### "Product classification mismatch"
**Problem**: Product field doesn't match case title content
**Solution**: Review case content and update product classification

#### "Invalid date format"
**Problem**: Dates not in standard format (YYYY-MM-DD or MM/DD/YYYY)
**Solution**: Standardize date formats in your data source

## Validation Best Practices

### Before Publishing Reports

1. **Always run full validation**
   ```bash
   ./bin/validate-rfe-reports [customer] --verbose
   ```

2. **Check accuracy score (Enterprise Standards)**
   - **Must be ≥99% for customer distribution**
   - **≥95% acceptable for internal use only**
   - Review all critical and high issues

3. **Verify system health**
   - Ensure all system validations pass
   - Check for authentication issues

### Regular Maintenance

1. **Weekly system validation**
   ```bash
   ./bin/validate-rfe-reports --system-only
   ```

2. **Monthly content validation**
   ```bash
   ./bin/validate-rfe-reports [customer] --content-only
   ```

3. **After system updates**
   - Run full validation after any tool updates
   - Verify customer configurations still work

### Quality Assurance Process

1. **Generate report**
2. **Run validation**
3. **Review issues**
4. **Fix problems**
5. **Re-validate**
6. **Publish only if accuracy ≥99% (customer reports) or ≥95% (internal use)**

## Validation Reports and Logs

### Report Locations
- **System validation**: `/tmp/rfe-verification-*.log`
- **Content validation**: `/tmp/content_validation_*.json`
- **Customer validation**: Console output

### Understanding Log Files

#### System Validation Log
```
2024-01-15 10:30:15 - rfe_verification - INFO - Testing rhcase connectivity
2024-01-15 10:30:16 - rfe_verification - INFO - Authentication successful
2024-01-15 10:30:17 - rfe_verification - INFO - Case discovery test passed: 15 cases found
```

#### Content Validation Report
```json
{
  "validation_timestamp": "2024-01-15T10:30:15",
  "overall_accuracy_score": 0.92,
  "validation_status": "accurate",
  "total_issues": 2,
  "critical_issues": 0,
  "high_issues": 1,
  "medium_issues": 1,
  "content_issues": [
    {
      "issue_type": "invalid_date_format",
      "severity": "medium",
      "description": "Invalid date format: 15/01/2024",
      "location": "Active RFE table, row 3",
      "recommendation": "Standardize date format across all entries"
    }
  ]
}
```

## Troubleshooting

### Validation Script Won't Run
```bash
# Check if you're in the right directory
ls -la README.md bin/

# Make sure script is executable
chmod +x bin/validate-rfe-reports
```

### Python Import Errors
```bash
# Check Python path
python3 -c "import sys; print(sys.path)"

# Install missing modules
pip3 install --user requests yaml
```

### rhcase Authentication Issues
```bash
# Test rhcase directly
./rhcase/rhcase auth test

# Check credentials
./rhcase/rhcase config show
```

### Content Validation Fails
1. Check the detailed JSON report in `/tmp/`
2. Review each issue type and location
3. Fix data source issues
4. Re-run validation

## Advanced Validation

### Custom Validation Rules
You can extend the content validator by modifying `src/report_content_validator.py`:

```python
def _validate_custom_rule(self, data):
    """Add your custom validation logic here"""
    issues = []
    # Your validation code
    return issues
```

### Integration with CI/CD
```bash
# For automated testing
./bin/validate-rfe-reports $CUSTOMER --system-only
if [ $? -ne 0 ]; then
    echo "System validation failed"
    exit 1
fi
```

## Getting Help

### For System Issues
- Check `/tmp/rfe-verification-*.log` for detailed error messages
- Verify Red Hat VPN connection
- Test rhcase authentication manually

### For Content Issues
- Review `/tmp/content_validation_*.json` for detailed issue analysis
- Check your data sources for accuracy
- Verify case statuses in Red Hat systems

### For Tool Issues
- Contact jbyrd via GitLab: https://gitlab.cee.redhat.com/jbyrd
- Include validation logs and error messages
- Specify customer and validation type

## Summary

The RFE automation tool now provides comprehensive validation to ensure both system functionality and report content accuracy. Always run validation before publishing reports, and maintain an accuracy score of ≥85% for reliable, professional reports.

**Remember**: Accurate reports protect your reputation and provide real value to customers. Validation is not optional - it's essential for professional TAM operations.
