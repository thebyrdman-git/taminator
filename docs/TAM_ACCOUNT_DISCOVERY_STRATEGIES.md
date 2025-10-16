# TAM Account Discovery Strategies

## The Challenge
Discovering which accounts an individual TAM covers is complex because:
- Case ownership changes over time
- Multiple TAMs may cover the same account
- Temporary assignments during coverage periods
- Historical data may not reflect current assignments

## Proposed Solutions

### 1. **TAM Self-Configuration (Recommended)**
Let TAMs explicitly define their account portfolio in a configuration file.

**Pros:**
- ✅ Most accurate and reliable
- ✅ TAM has full control over their portfolio
- ✅ Easy to maintain and update
- ✅ Works for any TAM regardless of product mix

**Implementation:**
```yaml
# ~/.config/rfe-automation/tam-portfolio.yml
tam_name: "Jimmy Byrd"
tam_email: "jbyrd@redhat.com"
accounts:
  - account_number: "334224"
    account_name: "jpmc"
    customer_name: "JP Morgan Chase"
    products: ["Ansible"]
    priority: "high"
  - account_number: "838043"
    account_name: "wellsfargo"
    customer_name: "WELLS FARGO"
    products: ["Ansible"]
    priority: "high"
```

### 2. **Active Case Analysis**
Analyze currently active cases to infer TAM assignments.

**Pros:**
- ✅ Reflects current reality
- ✅ Automatic discovery
- ✅ No manual configuration needed

**Cons:**
- ❌ May miss accounts with no active cases
- ❌ Could include temporary assignments
- ❌ Less reliable for new TAMs

### 3. **Hybrid Approach (Best of Both)**
Combine self-configuration with active case analysis for validation.

**Implementation:**
1. TAM defines their portfolio in config file
2. System validates against active cases
3. System suggests additions/removals based on case activity
4. TAM can accept/reject suggestions

### 4. **Salesforce Integration**
Query Salesforce directly for TAM account assignments.

**Pros:**
- ✅ Most authoritative source
- ✅ Real-time data
- ✅ Handles complex assignment rules

**Cons:**
- ❌ Requires Salesforce API access
- ❌ More complex implementation
- ❌ May not be available to all TAMs

## Recommended Implementation

### Phase 1: TAM Self-Configuration
Start with explicit TAM portfolio configuration:

```yaml
# inventory/tam-portfolio.yml
plugin: redhat.rfe_automation.tam_portfolio
tam_config_file: "~/.config/rfe-automation/tam-portfolio.yml"
validation_mode: "active_cases"  # Validate against active cases
auto_suggestions: true           # Suggest new accounts based on case activity
```

### Phase 2: Smart Suggestions
Add intelligent suggestions based on case activity:

```yaml
# The system would suggest:
suggestions:
  - account_number: "123456"
    reason: "You have 5 active cases for this account"
    confidence: "high"
  - account_number: "789012"
    reason: "You created 3 cases in the last 30 days"
    confidence: "medium"
```

### Phase 3: Salesforce Integration (Future)
For enterprise deployments, integrate with Salesforce for authoritative data.

## Implementation Priority

1. **Immediate**: TAM self-configuration with case validation
2. **Short-term**: Smart suggestions based on case activity
3. **Long-term**: Salesforce integration for enterprise deployments

This approach gives TAMs control while providing intelligent assistance and validation.
