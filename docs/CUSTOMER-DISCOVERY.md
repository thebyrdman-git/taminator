# Dynamic Customer Discovery

## Overview

Instead of maintaining a static local database, the TAM RFE automation tool can **dynamically search Red Hat's network** for customer account information in real-time.

## The Problem with Static Databases

❌ **Static databases become stale:**
- Customer names change
- Account numbers reassign
- TAM assignments shift
- Requires manual updates
- Data gets out of sync

## The Solution: Dynamic Discovery

✅ **Query Red Hat's live systems:**
- Always up-to-date
- No maintenance required
- Authoritative source
- Real-time accuracy

## Available Red Hat Data Sources

### 1. Red Hat Case System (via rhcase)
**What it provides:**
- Customer account numbers
- Account names
- CSM/TAM assignments
- Vertical (Financial Services, etc.)
- Case history (proves account activity)
- SBR group distribution

**Access:** Already configured via `rhcase` authentication

### 2. Hydra API
**What it provides:**
- Account details
- TAM assignments
- Entitlements
- Customer Portal Group IDs

**Access:** Via `tamscripts.config` credentials

### 3. Customer Portal API
**What it provides:**
- Subscription details
- Contact information
- Entitlement status

## Customer Discovery Tool

### Installation

The tool is already included:
```bash
bin/tam-rfe-discover-customers
```

### Usage

#### 1. List All Accessible Accounts
```bash
./bin/tam-rfe-discover-customers list
```

**Output:**
```
📋 Listing All Accessible Customer Accounts

✅ Found 7 unique customer account(s):

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏢 Customer: Westpac Banking Corporation
   Account #: 1363155
   Vertical: Financial Services
   CSM: Daniel Forte

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏢 Customer: JP Morgan Chase
   Account #: 334224
   Vertical: Financial Services
   CSM: Unknown
...
```

#### 2. Search for Specific Customer
```bash
./bin/tam-rfe-discover-customers search "Wells Fargo"
```

**Output:**
```
🔍 Searching Red Hat Network for: Wells Fargo

✅ Found matching customer(s):

  🏢 Customer: WELLS FARGO
     Account: 838043
     Vertical: Financial Services
```

#### 3. Get Account Details
```bash
./bin/tam-rfe-discover-customers account 1363155
```

**Output:**
```
📊 Account Details for: 1363155

✅ Account Found!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏢 Customer Name: Westpac Banking Corporation
   Account Number: 1363155
   Vertical: Financial Services
   CSM: Daniel Forte
   Cases (last 3 months): 23
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ℹ️  Case Distribution by SBR Group:
   • Ansible: 7 case(s)
   • Shift: 4 case(s)
   • Virtualization: 2 case(s)
...

ℹ️  Recent Cases:
   • Case 04210398: Ongoing performance issues...
   • Case 04275756: Issue with too many connections...
```

#### 4. Discover Your Assigned Accounts
```bash
./bin/tam-rfe-discover-customers discover
```

## Integration with Onboarding

### Current Workflow
1. **Discover** customer with discovery tool
2. **Copy** account details (name, number, SBR groups)
3. **Add** via onboarding tool

### Future Enhancement: Auto-Populate
```bash
# Future feature
./bin/tam-rfe-onboard-intelligent --auto-discover

# Would automatically:
1. Query Red Hat network for your assigned accounts
2. Extract account details
3. Populate configuration automatically
4. Confirm with TAM before finalizing
```

## How It Works

### Data Source: Red Hat Case System
The tool queries the case system (via `rhcase`) which provides:

1. **Recent Cases** (last 6 months)
2. **Account Metadata** from each case:
   - Account number
   - Customer name
   - Vertical classification
   - CSM assignment
   - SBR groups

3. **Real-Time Accuracy**
   - No caching (always fresh)
   - No stale data
   - Authoritative source

### Authentication
Uses existing `rhcase` authentication:
- Configured in `~/.config/tamscripts/tamscripts.config`
- Leverages Red Hat SSO
- No additional setup needed

## Advantages Over Static Database

| Feature | Static Database | Dynamic Discovery |
|---------|----------------|-------------------|
| **Data Freshness** | Stale | Real-time |
| **Maintenance** | Manual updates required | None |
| **Accuracy** | Degrades over time | Always accurate |
| **Coverage** | Limited to configured accounts | All accessible accounts |
| **Discovery** | Manual research | Automatic |
| **TAM Changes** | Requires update | Auto-reflects |
| **Customer Name Changes** | Breaks queries | Always current |

## Requirements

- ✅ Red Hat VPN connection
- ✅ `rhcase` installed and configured
- ✅ Valid Red Hat SSO credentials
- ✅ TAM/CSM account assignments in Red Hat systems

## Use Cases

### 1. New TAM Onboarding
```bash
# Discover all your assigned customers
./bin/tam-rfe-discover-customers list

# Add each one to automation
./bin/tam-rfe-onboard-intelligent
```

### 2. Customer Research
```bash
# Look up unfamiliar customer
./bin/tam-rfe-discover-customers search "Acme Corp"

# Get detailed account info
./bin/tam-rfe-discover-customers account 123456
```

### 3. Audit Existing Configuration
```bash
# See what accounts you have access to
./bin/tam-rfe-discover-customers list

# Compare with configured accounts
./bin/tam-rfe-validate-intelligence
```

### 4. Find SBR Group Distribution
```bash
# See which SBR groups a customer uses most
./bin/tam-rfe-discover-customers account 1363155

# Use this to configure SBR filters in onboarding
```

## Troubleshooting

### "Could not retrieve customer data"
**Cause:** Not connected to Red Hat VPN

**Solution:**
```bash
# Test VPN connection
curl -I https://source.redhat.com

# Should return HTTP 200 or 302
# If connection refused, connect to VPN first
```

### "rhcase not found"
**Cause:** rhcase not installed

**Solution:**
```bash
# Install rhcase
cd rfe-automation-clean
./install-improved.sh
```

### "No customers found matching search"
**Possible causes:**
- Typo in customer name
- Customer has no recent cases
- Not assigned to you in Red Hat systems

**Solution:**
```bash
# Try broader search
./bin/tam-rfe-discover-customers list

# Search by account number instead
./bin/tam-rfe-discover-customers account 123456
```

## Future Enhancements

### 1. Hydra API Direct Integration
Query Hydra API directly for:
- Complete account roster
- TAM assignments
- Customer Portal Group IDs
- Entitlement details

### 2. Auto-Onboarding
```bash
./bin/tam-rfe-onboard-intelligent --auto-discover
```
- Discovers all assigned accounts
- Auto-populates configuration
- Confirms with TAM before saving

### 3. Change Detection
```bash
./bin/tam-rfe-watch-assignments
```
- Monitor for TAM assignment changes
- Alert when new customers added
- Detect when customers removed

### 4. Multi-Source Validation
- Cross-check case system, Hydra, SFDC
- Detect discrepancies
- Flag accounts needing attention

## Best Practices

1. **Run Discovery Monthly**
   - Check for new assignments
   - Verify existing accounts still active

2. **Use for Account Research**
   - Before customer meetings
   - When taking over accounts
   - For case handoffs

3. **Validate After Discovery**
   ```bash
   ./bin/tam-rfe-discover-customers account 123456
   ./bin/tam-rfe-validate-intelligence customer-key
   ```

4. **Keep Configuration Minimal**
   - Only configure active customers
   - Remove inactive accounts
   - Use discovery tool for ad-hoc queries

---

**Key Insight:** No local database needed! Red Hat's network IS the database.

