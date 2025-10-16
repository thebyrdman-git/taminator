# Intelligence Engine Testing Guide

## Overview

The "intelligence engine" consists of:
1. **Dynamic Customer Onboarding** (`tam-rfe-onboard-intelligent`)
2. **Configuration Synchronization** (`customers.conf` + `tamscripts.config`)
3. **rhcase Integration** (case searching and data retrieval)
4. **Natural Language Processing** (`tam-rfe-chat` command interpretation)
5. **Case Analysis** (similarity detection, filtering, reporting)

## Testing Strategies

### 1. Integration Testing with Real Accounts

#### Test New Customer Onboarding
```bash
# Test the full onboarding workflow
./bin/tam-rfe-onboard-intelligent

# Verify configurations were created correctly
echo "=== Checking customers.conf ==="
cat config/customers.conf

echo "=== Checking tamscripts.config ==="
grep -A 30 "name: [new-customer-key]" ~/.config/tamscripts/tamscripts.config

# Immediate searchability test
./rhcase/.venv/bin/rhcase list [customer-key] --months 3 --format json | jq '.[] | {caseNumber, subject, sbrGroup}'
```

#### Test Case Search Accuracy
```bash
# Search for known cases
./bin/tam-rfe-chat

# Inside the chat, test these queries:
> show cases for [customer]
> show open cases for [customer]  
> show ansible cases for [customer]
> find similar cases to [known-case-number]
```

### 2. Automated Validation Scripts

#### Create Comprehensive Validation Tool
```bash
#!/bin/bash
# bin/tam-rfe-validate-intelligence

validate_customer_config() {
    local customer_key="$1"
    
    echo "🔍 Validating intelligence engine for: $customer_key"
    echo ""
    
    # Check customers.conf
    echo "1️⃣ Checking customers.conf..."
    if grep -q "^${customer_key}:" config/customers.conf; then
        echo "   ✅ Found in customers.conf"
    else
        echo "   ❌ Missing from customers.conf"
        return 1
    fi
    
    # Check tamscripts.config
    echo "2️⃣ Checking tamscripts.config..."
    if grep -q "^- name: ${customer_key}$" ~/.config/tamscripts/tamscripts.config; then
        echo "   ✅ Found in tamscripts.config"
    else
        echo "   ❌ Missing from tamscripts.config"
        return 1
    fi
    
    # Test rhcase access
    echo "3️⃣ Testing rhcase access..."
    local cases=$(./rhcase/.venv/bin/rhcase list "$customer_key" --months 1 --format json 2>/dev/null)
    if [[ -n "$cases" ]] && [[ "$cases" != "[]" ]]; then
        local case_count=$(echo "$cases" | jq '. | length')
        echo "   ✅ rhcase found $case_count case(s)"
    else
        echo "   ⚠️  rhcase returned no cases (might be expected)"
    fi
    
    # Test tam-rfe-chat integration
    echo "4️⃣ Testing tam-rfe-chat integration..."
    # This would need to be an automated test
    echo "   ℹ️  Manual test required: Run ./bin/tam-rfe-chat and query for this customer"
    
    echo ""
    echo "✅ Validation complete for $customer_key"
}

# Run validation
if [[ $# -eq 0 ]]; then
    echo "Usage: $0 <customer-key>"
    echo "Example: $0 westpac"
    exit 1
fi

validate_customer_config "$1"
```

### 3. End-to-End Workflow Testing

#### Test Complete Customer Lifecycle
```bash
# Test 1: Add new customer
echo "Test 1: Adding test customer..."
./bin/tam-rfe-onboard-intelligent
# (Answer questions with test data)

# Test 2: Verify immediate searchability
echo "Test 2: Searching for new customer's cases..."
./rhcase/.venv/bin/rhcase list testcustomer --months 6

# Test 3: Test natural language queries
echo "Test 3: Testing NLP queries..."
./bin/tam-rfe-chat << EOF
show cases for testcustomer
show ansible cases for testcustomer
exit
EOF

# Test 4: Generate report
echo "Test 4: Generating test report..."
./bin/tam-rfe-monitor-simple testcustomer --test

# Test 5: Verify data accuracy
echo "Test 5: Validating report accuracy..."
./bin/validate-rfe-reports testcustomer
```

### 4. Configuration Verification Tests

#### Automated Config Sync Check
```bash
#!/bin/bash
# bin/tam-rfe-check-config-sync

echo "🔍 Checking configuration synchronization..."

# Get all customers from customers.conf
echo "1️⃣ Extracting customers from customers.conf..."
customers_conf=$(grep -v "^#" config/customers.conf | cut -d: -f1)

# Check each customer exists in tamscripts.config
echo "2️⃣ Verifying each customer is in tamscripts.config..."
missing_count=0
for customer in $customers_conf; do
    if ! grep -q "^- name: ${customer}$" ~/.config/tamscripts/tamscripts.config; then
        echo "   ❌ Missing: $customer"
        ((missing_count++))
    else
        echo "   ✅ Synced: $customer"
    fi
done

if [[ $missing_count -eq 0 ]]; then
    echo ""
    echo "✅ All customers are synchronized!"
else
    echo ""
    echo "⚠️  Found $missing_count customer(s) not synchronized"
    echo "Run: ./bin/tam-rfe-onboard-intelligent to fix"
fi
```

### 5. Case Search Accuracy Testing

#### Test Against Known Cases
```bash
#!/bin/bash
# tests/test-case-search-accuracy.sh

# Define test cases with known results
declare -A test_cases=(
    ["westpac"]="1363155"  # account number
    ["jpmc"]="334224"
    ["wellsfargo"]="838043"
)

echo "🧪 Testing case search accuracy..."

for customer in "${!test_cases[@]}"; do
    account="${test_cases[$customer]}"
    
    echo ""
    echo "Testing: $customer (account: $account)"
    
    # Search via rhcase
    cases=$(./rhcase/.venv/bin/rhcase list "$customer" --months 1 --format json 2>/dev/null)
    
    if [[ -z "$cases" ]] || [[ "$cases" == "[]" ]]; then
        echo "   ⚠️  No cases found (might be expected)"
        continue
    fi
    
    # Validate account numbers match
    found_accounts=$(echo "$cases" | jq -r '.[].accountNumber' | sort -u)
    
    if echo "$found_accounts" | grep -q "^${account}$"; then
        echo "   ✅ Account number matches"
    else
        echo "   ❌ Account mismatch. Expected: $account, Found: $found_accounts"
    fi
    
    # Check for required fields
    missing_fields=$(echo "$cases" | jq -r '.[] | select(.caseNumber == null or .subject == null or .status == null) | .caseNumber // "unknown"')
    
    if [[ -z "$missing_fields" ]]; then
        echo "   ✅ All cases have required fields"
    else
        echo "   ⚠️  Some cases missing fields"
    fi
done
```

### 6. Report Validation Testing

#### Automated Report Quality Checks
```bash
#!/bin/bash
# bin/tam-rfe-validate-report-quality

customer="$1"
if [[ -z "$customer" ]]; then
    echo "Usage: $0 <customer-key>"
    exit 1
fi

echo "🔍 Validating report quality for: $customer"

# Generate test report
echo "1️⃣ Generating test report..."
./bin/tam-rfe-monitor-simple "$customer" --test > /tmp/test-report-${customer}.md

# Check for dummy/placeholder data
echo "2️⃣ Checking for dummy data..."
if grep -qi "example\|dummy\|placeholder\|test\|lorem ipsum" /tmp/test-report-${customer}.md; then
    echo "   ❌ Found placeholder/dummy data in report"
    grep -i "example\|dummy\|placeholder\|test" /tmp/test-report-${customer}.md | head -5
else
    echo "   ✅ No dummy data found"
fi

# Check for real case numbers
echo "3️⃣ Checking for real case numbers..."
case_numbers=$(grep -oE '[0-9]{8}' /tmp/test-report-${customer}.md | head -5)
if [[ -n "$case_numbers" ]]; then
    echo "   ✅ Found real case numbers:"
    echo "$case_numbers" | sed 's/^/      /'
else
    echo "   ⚠️  No case numbers found (might indicate no cases)"
fi

# Validate case numbers are real
echo "4️⃣ Validating case numbers are real..."
for case_num in $case_numbers; do
    if ./rhcase/.venv/bin/rhcase search "$case_num" --format json 2>/dev/null | jq -e '. != null' > /dev/null; then
        echo "   ✅ Case $case_num is valid"
    else
        echo "   ❌ Case $case_num not found in system"
    fi
done

echo ""
echo "✅ Report quality validation complete"
```

### 7. Monitoring and Logging

#### Add Detailed Logging to tam-rfe-chat
```bash
# Add to bin/tam-rfe-chat

LOG_FILE="${PROJECT_ROOT}/logs/tam-rfe-chat-$(date +%Y%m%d).log"

log_query() {
    local query="$1"
    local result_count="$2"
    echo "[$(date -Iseconds)] QUERY: $query | RESULTS: $result_count" >> "$LOG_FILE"
}

log_error() {
    local error="$1"
    echo "[$(date -Iseconds)] ERROR: $error" >> "$LOG_FILE"
}

# Usage in case search:
log_query "show cases for $customer" "$case_count"
```

#### Monitor rhcase Performance
```bash
#!/bin/bash
# bin/tam-rfe-monitor-rhcase-performance

echo "📊 rhcase Performance Monitoring"

for customer in westpac jpmc wellsfargo; do
    echo ""
    echo "Testing: $customer"
    
    start_time=$(date +%s%N)
    ./rhcase/.venv/bin/rhcase list "$customer" --months 1 --format json > /dev/null 2>&1
    end_time=$(date +%s%N)
    
    duration=$((($end_time - $start_time) / 1000000))  # Convert to milliseconds
    
    if [[ $duration -lt 5000 ]]; then
        echo "   ✅ Response time: ${duration}ms (Good)"
    else
        echo "   ⚠️  Response time: ${duration}ms (Slow)"
    fi
done
```

### 8. User Acceptance Testing (UAT)

#### Create UAT Test Plan
```markdown
# User Acceptance Test Plan

## Test Scenario 1: New Customer Onboarding
1. Run `./bin/tam-rfe-onboard-intelligent`
2. Enter new customer: "Test Bank"
3. Account number: 123456
4. SBR Groups: Ansible, OpenShift
5. Verify customer appears in both config files
6. Test searching immediately: `./rhcase/.venv/bin/rhcase list test-bank --months 1`

**Expected Result**: Customer is searchable immediately without manual config editing

## Test Scenario 2: Natural Language Queries
1. Run `./bin/tam-rfe-chat`
2. Test queries:
   - "show cases for westpac"
   - "show open ansible cases for jpmc"
   - "find similar cases to 04244831"
3. Verify real case data appears (no dummy data)

**Expected Result**: Real case numbers, subjects, and details displayed

## Test Scenario 3: Report Accuracy
1. Generate report: `./bin/tam-rfe-monitor-simple wellsfargo --test`
2. Manually verify case numbers in report match Portal
3. Check case subjects match Portal
4. Verify SBR groups are correct

**Expected Result**: 99%+ accuracy compared to Portal data
```

### 9. Regression Testing

#### Automated Regression Test Suite
```bash
#!/bin/bash
# tests/regression-suite.sh

echo "🧪 Running Intelligence Engine Regression Tests"

test_count=0
pass_count=0
fail_count=0

run_test() {
    local test_name="$1"
    local test_command="$2"
    
    ((test_count++))
    echo ""
    echo "Test $test_count: $test_name"
    
    if eval "$test_command"; then
        echo "   ✅ PASS"
        ((pass_count++))
    else
        echo "   ❌ FAIL"
        ((fail_count++))
    fi
}

# Test 1: rhcase is accessible
run_test "rhcase accessibility" \
    "./rhcase/.venv/bin/rhcase --version"

# Test 2: Configs are synchronized
run_test "Config synchronization" \
    "./bin/tam-rfe-check-config-sync"

# Test 3: tam-rfe-chat starts correctly
run_test "tam-rfe-chat startup" \
    "echo 'exit' | ./bin/tam-rfe-chat > /dev/null 2>&1"

# Test 4: Case search works
run_test "Case search functionality" \
    "./rhcase/.venv/bin/rhcase list westpac --months 1 --format json | jq -e '. | length > 0'"

# Test 5: Report generation works
run_test "Report generation" \
    "./bin/tam-rfe-monitor-simple westpac --test > /dev/null 2>&1"

echo ""
echo "═══════════════════════════════════"
echo "Test Results: $pass_count/$test_count passed"
if [[ $fail_count -eq 0 ]]; then
    echo "✅ All tests passed!"
    exit 0
else
    echo "❌ $fail_count test(s) failed"
    exit 1
fi
```

## Continuous Improvement

### Collect User Feedback
```bash
#!/bin/bash
# bin/tam-rfe-feedback-collector

echo "📝 Intelligence Engine Feedback"
echo ""
echo "Please rate your experience (1-5):"
read -p "1. Case search accuracy: " search_rating
read -p "2. Response time: " speed_rating
read -p "3. Natural language understanding: " nlp_rating
read -p "4. Overall satisfaction: " overall_rating

echo ""
read -p "Any issues or suggestions? " feedback

# Log feedback
cat >> logs/user-feedback.log << EOF
[$(date -Iseconds)]
Search: $search_rating/5
Speed: $speed_rating/5
NLP: $nlp_rating/5
Overall: $overall_rating/5
Feedback: $feedback
---
EOF

echo ""
echo "✅ Thank you for your feedback!"
```

### Monitor Error Rates
```bash
#!/bin/bash
# bin/tam-rfe-error-monitor

echo "📊 Error Rate Monitoring (Last 24 hours)"

log_file="logs/tam-rfe-chat-$(date +%Y%m%d).log"

if [[ ! -f "$log_file" ]]; then
    echo "No log file found for today"
    exit 0
fi

total_queries=$(grep -c "QUERY:" "$log_file")
error_queries=$(grep -c "ERROR:" "$log_file")

if [[ $total_queries -gt 0 ]]; then
    error_rate=$((error_queries * 100 / total_queries))
    echo "Total queries: $total_queries"
    echo "Errors: $error_queries"
    echo "Error rate: ${error_rate}%"
    
    if [[ $error_rate -gt 10 ]]; then
        echo "⚠️  High error rate detected!"
    else
        echo "✅ Error rate within acceptable range"
    fi
else
    echo "No queries logged today"
fi
```

## Best Practices

1. **Test with Real Data**: Always test with actual customer accounts
2. **Automate Tests**: Run regression suite before each merge
3. **Monitor Performance**: Track response times and error rates
4. **Validate Reports**: Cross-check generated reports against Portal
5. **Collect Feedback**: Regularly gather user feedback
6. **Document Issues**: Log all discovered issues in GitLab
7. **Iterate**: Continuously improve based on test results

## Success Criteria

✅ **Configuration Sync**: 100% of customers in both config files
✅ **Case Search**: <5 second response time, 99%+ accuracy
✅ **Report Quality**: 99%+ accuracy vs Portal data
✅ **Error Rate**: <10% of queries result in errors
✅ **User Satisfaction**: 4+ out of 5 rating

---

**Next Steps**: Implement these testing strategies progressively and incorporate into CI/CD pipeline.

