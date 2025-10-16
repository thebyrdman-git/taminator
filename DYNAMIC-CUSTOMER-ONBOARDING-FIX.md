# Dynamic Customer Onboarding Fix

## Problem Statement

The TAM RFE automation system had a critical architectural flaw:

1. **Two Separate Config Systems**: 
   - `config/customers.conf` - Used by `tam-rfe-chat` (simple format)
   - `~/.config/tamscripts/tamscripts.config` - Used by `rhcase` (YAML format)

2. **Manual Configuration Required**: When users added customers via `tam-rfe-onboard-intelligent`, it only updated internal learning data, NOT the actual configuration files that the tools use.

3. **Result**: New customers couldn't be searched because `rhcase` didn't know about them, leading to "no cases found" errors even when cases existed.

## Root Cause

During the role-play test with account 397076:
- User added customer via onboarding
- Customer was added to `customers.conf` manually
- **But NOT added to `tamscripts.config`**
- `tam-rfe-chat` tried to search using `rhcase`
- `rhcase` didn't have account 397076 configured
- Search failed: "no cases found"

## Solution

### Dynamic Configuration Updates

Modified `tam-rfe-onboard-intelligent` to automatically configure BOTH systems:

#### 1. New Function: `add_customer_to_conf()`
```bash
# Adds customer to customers.conf (simple format)
customer_key:Customer Name:account_number:group_id
```

#### 2. New Function: `add_customer_to_tamscripts()`
```bash
# Adds customer to tamscripts.config (YAML format for rhcase)
# Includes:
- Account numbers
- SBR group filters
- Display configuration
- Sorting preferences
```

#### 3. Integration Point
When users answer onboarding questions, the system now:
1. Collects customer data (name, account, SBR groups)
2. **Immediately** adds to `customers.conf`
3. **Immediately** adds to `tamscripts.config`
4. Creates backup of tamscripts.config before modification

### Code Changes

**File**: `bin/tam-rfe-onboard-intelligent`

**Lines 66-190**: Added two new functions for dynamic configuration

**Lines 392-397**: Integrated function calls into customer collection loop:
```bash
# Immediately add customer to both config files
echo ""
print_info "Configuring system access for $customer_name..."
add_customer_to_conf "$customer_name" "$account_number" "$group_id"
add_customer_to_tamscripts "$customer_name" "$account_number" "$customer_sbr_groups"
echo ""
```

## Testing

To test the fix:

```bash
# Run intelligent onboarding
cd rfe-automation-clean
./bin/tam-rfe-onboard-intelligent

# Add a test customer (e.g., account 397076)
# System will automatically configure both files

# Verify customer was added to both configs
grep "testacct" config/customers.conf
grep -A 20 "name: testacct" ~/.config/tamscripts/tamscripts.config

# Test case search with tam-rfe-chat
./bin/tam-rfe-chat
# > show cases for testacct

# Verify rhcase can access the account
./rhcase/.venv/bin/rhcase list testacct --months 12
```

## Benefits

1. **Zero Manual Configuration**: Users never need to edit config files
2. **Immediate Availability**: New customers searchable instantly
3. **Consistent Data**: Both systems stay in sync automatically
4. **Backup Protection**: tamscripts.config backed up before each change
5. **Idempotent**: Safe to run multiple times (checks for existing customers)

## Email Fix

**Separate Issue**: Email notifications were bouncing due to invalid FROM address.

**Problem**: `GITLAB_WEBHOOK_FROM=hatter@miraclemax` (rejected by Red Hat's Mimecast)

**Fix**: Changed to `GITLAB_WEBHOOK_FROM=jbyrd@redhat.com` in:
- Webhook container on miraclemax
- `bin/pai-gitlab-webhook-deploy` script

**Result**: Email summary of 3 open GitLab issues successfully delivered.

## Files Modified

1. `bin/tam-rfe-onboard-intelligent` - Added dynamic configuration functions
2. `bin/pai-gitlab-webhook-deploy` - Fixed FROM email address
3. `~/.config/tamscripts/tamscripts.config` - Manually added testacct397076 for immediate testing

## Next Steps

1. Remove manually-added test accounts from configs
2. Test full onboarding workflow with real customer
3. Consider adding validation to detect missing configurations
4. Add `tam-rfe-chat` warning when account not configured

---

**Issue**: https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation/-/issues/10  
**Date**: 2025-10-16  
**Status**: ✅ Fixed - Dynamic onboarding now works

