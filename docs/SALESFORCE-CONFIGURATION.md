# 💼 Salesforce Write Operations Configuration

## 🎯 Overview

Taminator can automatically write case updates, comments, and status changes to Salesforce. This enables full automation of case management workflows.

**What You Can Do:**
- 💬 **Add case comments** - Post updates to cases
- 📝 **Update case status** - Change status programmatically
- ✅ **Close cases** - Auto-close with resolution
- 🔄 **Bulk operations** - Update multiple cases at once
- 📋 **Agenda updates** - Post TAM call updates to all discussed cases

**Framework Ready For:**
- Automated backlog cleanup
- Post-call case updates
- Status synchronization
- Customer notifications

---

## ⚡ Quick Start

### Prerequisites

You'll need Salesforce credentials with API access:
- Instance URL (e.g., `https://redhat.my.salesforce.com`)
- Client ID (Connected App)
- Client Secret (Connected App)
- Username
- Password
- Security Token

### Option 1: Environment Variables

```bash
# Add to ~/.bashrc or ~/.zshrc
export SALESFORCE_INSTANCE_URL="https://redhat.my.salesforce.com"
export SALESFORCE_CLIENT_ID="your_client_id_here"
export SALESFORCE_CLIENT_SECRET="your_client_secret_here"
export SALESFORCE_USERNAME="jbyrd@redhat.com"
export SALESFORCE_PASSWORD="your_password"
export SALESFORCE_SECURITY_TOKEN="your_security_token"

# Reload shell
source ~/.bashrc
```

### Option 2: Configuration File (Recommended)

```bash
# Create config directory
mkdir -p ~/.config/rfe-automation

# Create Salesforce config
cat > ~/.config/rfe-automation/salesforce.conf << 'EOF'
{
  "instance_url": "https://redhat.my.salesforce.com",
  "client_id": "your_client_id_here",
  "client_secret": "your_client_secret_here",
  "username": "jbyrd@redhat.com",
  "password": "your_password",
  "security_token": "your_security_token"
}
EOF

# Secure the file (IMPORTANT!)
chmod 600 ~/.config/rfe-automation/salesforce.conf
```

---

## 🔐 Salesforce Setup

### Step 1: Create Connected App

1. **Login to Salesforce**
   - Go to Setup → Apps → App Manager

2. **Create New Connected App**
   - Click "New Connected App"
   - Name: "Taminator API Access"
   - Contact Email: your-email@redhat.com

3. **Enable OAuth Settings**
   - ✅ Enable OAuth Settings
   - Callback URL: `https://localhost:8080/callback` (not used for password flow)
   - Selected OAuth Scopes:
     - Full access (full)
     - Perform requests on your behalf at any time (refresh_token, offline_access)
     - Access and manage your data (api)

4. **Save and Get Credentials**
   - After saving, click "Manage Consumer Details"
   - Copy **Consumer Key** (Client ID)
   - Copy **Consumer Secret** (Client Secret)

### Step 2: Get Security Token

1. **Reset Security Token**
   - Go to Personal Settings → Reset My Security Token
   - Click "Reset Security Token"
   - Token will be emailed to you

2. **Save Token**
   - Copy token from email
   - This is appended to your password for API access

### Step 3: Test Connection

```bash
# Test with Python
python3 << 'EOF'
import sys
sys.path.insert(0, '/home/jbyrd/pai/taminator')
from foundation.salesforce_handler import get_salesforce_handler

handler = get_salesforce_handler()

if handler.config.is_configured():
    print("✅ Salesforce configured")
    
    # Test authentication
    if handler._authenticate():
        print("✅ Salesforce authentication successful")
    else:
        print("❌ Salesforce authentication failed")
else:
    print("❌ Salesforce not configured")
EOF
```

---

## 📚 API Reference

### Python API

```python
from foundation.salesforce_handler import get_salesforce_handler

# Get handler
handler = get_salesforce_handler()

# Add case comment
handler.add_case_comment(
    case_number="04280915",
    comment="Updated case after customer call",
    is_public=True  # Visible to customer
)

# Update case status
handler.update_case_status(
    case_number="04280915",
    status="Waiting on Customer",
    comment="Waiting for customer to provide logs"
)

# Close case
handler.close_case(
    case_number="04280915",
    resolution="Issue resolved by upgrading to AAP 2.5",
    close_code="Solved"
)

# Update custom fields
handler.update_case_fields(
    case_number="04280915",
    fields={
        "Priority": "High",
        "Custom_Field__c": "Custom Value"
    }
)

# Bulk add comments
cases = [
    {"case_number": "04280915", "comment": "Updated after TAM call"},
    {"case_number": "04280916", "comment": "Discussed in meeting"}
]
results = handler.bulk_add_comments(cases, is_public=True)

# Post agenda updates to all cases
updated_count = handler.post_agenda_update(
    customer="jpmc",
    cases=[{"number": "04280915"}, {"number": "04280916"}],
    agenda_summary="Discussed AAP upgrade and RHEL migration"
)
```

---

## 🧪 Testing Salesforce Integration

### Test 1: Check Configuration

```bash
python3 << 'EOF'
import sys
sys.path.insert(0, '/home/jbyrd/pai/taminator')
from foundation.salesforce_handler import SalesforceConfig

config = SalesforceConfig()
print(f"Instance URL: {config.instance_url}")
print(f"Client ID: {config.client_id[:10]}..." if config.client_id else "Client ID: (not set)")
print(f"Username: {config.username}")
print(f"Configured: {config.is_configured()}")
EOF
```

### Test 2: Test Authentication

```bash
python3 << 'EOF'
import sys
sys.path.insert(0, '/home/jbyrd/pai/taminator')
from foundation.salesforce_handler import get_salesforce_handler

handler = get_salesforce_handler()

if handler._authenticate():
    print("✅ Authentication successful!")
    print(f"   Access token: {handler.config.access_token[:20]}...")
else:
    print("❌ Authentication failed")
EOF
```

### Test 3: Add Test Comment

```bash
python3 << 'EOF'
import sys
sys.path.insert(0, '/home/jbyrd/pai/taminator')
from foundation.salesforce_handler import add_case_comment

# Replace with actual case number
success = add_case_comment(
    case_number="04280915",
    comment="Test comment from Taminator",
    is_public=False  # Internal comment only
)

if success:
    print("✅ Test comment added successfully")
else:
    print("❌ Failed to add comment")
EOF
```

---

## 🛠️ Troubleshooting

### Issue: "Salesforce not configured"

**Problem:** Missing credentials

**Solution:**
```bash
# Check if variables are set
echo $SALESFORCE_INSTANCE_URL
echo $SALESFORCE_USERNAME

# If empty, set them:
export SALESFORCE_INSTANCE_URL="https://redhat.my.salesforce.com"
export SALESFORCE_USERNAME="jbyrd@redhat.com"
# ... etc

# Or create config file (recommended)
mkdir -p ~/.config/rfe-automation
# Create salesforce.conf as shown above
```

---

### Issue: "Authentication failed"

**Problem:** Invalid credentials or security token

**Solution:**

1. **Check Password + Security Token**
   - API password = regular password + security token
   - Example: If password is "MyPass123" and token is "ABC456", use "MyPass123ABC456"

2. **Reset Security Token**
   - Salesforce → Personal Settings → Reset My Security Token
   - New token will be emailed

3. **Verify Connected App**
   - Ensure Connected App is approved
   - Check OAuth scopes include "api" and "full"

4. **Test Credentials**
```bash
# Test with curl
curl -X POST https://redhat.my.salesforce.com/services/oauth2/token \
  -d "grant_type=password" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "username=jbyrd@redhat.com" \
  -d "password=YOUR_PASSWORD_WITH_TOKEN"

# Should return JSON with access_token
```

---

### Issue: "Case not found in Salesforce"

**Problem:** Case number doesn't exist or wrong format

**Solution:**
1. Verify case number in Salesforce
2. Check case number format (should match Salesforce CaseNumber field)
3. Ensure you have access to the case

---

### Issue: "Insufficient privileges"

**Problem:** User doesn't have permission for operation

**Solution:**
1. Check Salesforce user permissions
2. Ensure profile/permission set includes:
   - API Enabled
   - Modify All Data (or specific object permissions)
3. Contact Salesforce admin to grant permissions

---

### Issue: "Invalid field name"

**Problem:** Field doesn't exist or wrong API name

**Solution:**
1. Verify field API names in Salesforce
2. Use Setup → Object Manager → Case → Fields
3. Use API name (e.g., `Custom_Field__c`, not "Custom Field")

---

## 🔒 Security Best Practices

### 1. Use Config File (Not Environment Variables)

```bash
# ✅ DO: Store in secure config file
chmod 600 ~/.config/rfe-automation/salesforce.conf

# ❌ DON'T: Store in environment (visible in process list)
export SALESFORCE_PASSWORD="MyPassword123"
```

### 2. Limit Connected App Permissions

- **Only grant necessary OAuth scopes**
- Use "Refresh Token" policy for token expiration
- Enable IP restrictions if possible

### 3. Rotate Credentials Regularly

```bash
# Rotate security token quarterly
# Update config file with new token
```

### 4. Audit API Usage

- Monitor Salesforce Setup Audit Trail
- Review API usage in Setup → System Overview
- Set up alerts for unusual activity

### 5. Never Commit Secrets

```bash
# Ensure salesforce.conf is in .gitignore
echo "*.conf" >> .gitignore

# ❌ NEVER commit salesforce.conf to git
```

---

## 📊 Use Cases

### Use Case 1: Auto-Update Cases After TAM Call

```python
from foundation.salesforce_handler import get_salesforce_handler

handler = get_salesforce_handler()

# Cases discussed in TAM call
cases = ["04280915", "04280916", "04280917"]

# Add update to each
for case_number in cases:
    handler.add_case_comment(
        case_number=case_number,
        comment="""TAM Call Update (2025-10-17)

Discussed in today's TAM call:
- Status: Making progress
- Next steps: Customer to provide updated logs by Friday
- Follow-up: Review again next week

---
Posted automatically by Taminator""",
        is_public=True
    )
```

### Use Case 2: Auto-Close Stale Cases

```python
from foundation.salesforce_handler import get_salesforce_handler

handler = get_salesforce_handler()

# Cases to close
stale_cases = [
    {"number": "04278900", "reason": "No customer response in 30 days"},
    {"number": "04278901", "reason": "Customer confirmed issue resolved"}
]

for case in stale_cases:
    handler.close_case(
        case_number=case["number"],
        resolution=case["reason"],
        close_code="No Response" if "No customer response" in case["reason"] else "Solved"
    )
```

### Use Case 3: Bulk Status Update

```python
from foundation.salesforce_handler import get_salesforce_handler

handler = get_salesforce_handler()

# Set all cases to "Waiting on Customer"
cases = ["04280915", "04280916", "04280917"]

for case_number in cases:
    handler.update_case_status(
        case_number=case_number,
        status="Waiting on Customer",
        comment="Waiting for customer to provide requested information"
    )
```

---

## 🔄 Integration with Taminator Tools

### Future Integration Points

**tam-generate-agenda:**
```bash
# After generating agenda, post updates to Salesforce
tam-generate-agenda --customer jpmc --post-to-salesforce

# Expected behavior:
# ✅ Generated agenda
# 📤 Posting updates to 12 cases in Salesforce...
# ✅ Posted to 12 cases
```

**tam-backlog-cleanup:**
```bash
# After cleanup, update case statuses
tam-backlog-cleanup --customer jpmc --update-salesforce

# Expected behavior:
# ✅ Auto-closed 5 cases (no customer response)
# ✅ Updated status on 3 cases (waiting on customer)
# 📤 Syncing changes to Salesforce...
# ✅ Salesforce updated
```

---

## ✅ Verification Checklist

Before using Salesforce integration:

- [ ] Connected App created in Salesforce
- [ ] Client ID and Client Secret obtained
- [ ] Security Token obtained (reset if needed)
- [ ] Configuration file created (`salesforce.conf`)
- [ ] Config file secured (`chmod 600`)
- [ ] Test authentication successful
- [ ] Test comment added to case
- [ ] User has necessary Salesforce permissions

---

## ⚠️ Important Notes

### API Limits

- **Daily API Limits:** Salesforce limits API calls per 24 hours
- **Monitor Usage:** Setup → System Overview → API Usage
- **Best Practice:** Use bulk operations when updating multiple cases

### Field Names

- Use **API Names** not labels (e.g., `Custom_Field__c`)
- Standard fields use **CamelCase** (e.g., `Status`, `Priority`)
- Custom fields end with `__c`

### Case Status Values

Valid status values depend on your Salesforce configuration:
- Common: `New`, `In Progress`, `Waiting on Customer`, `Waiting on Red Hat`, `Closed`
- Check: Setup → Object Manager → Case → Fields → Status → Values

---

## 📞 Need Help?

### Still Having Issues?

1. **Check Salesforce Logs:** Setup → Debug Logs
2. **Verify Permissions:** Setup → Users → Your User → View Permissions
3. **Test with Workbench:** https://workbench.developerforce.com
4. **Contact Salesforce Admin:** For permission issues
5. **Ask for help:** Slack #tam-automation

### Common Solutions

| Problem | Solution |
|---------|----------|
| Authentication failed | Reset security token, verify password + token |
| Case not found | Check case number format and access |
| Insufficient privileges | Contact Salesforce admin for permissions |
| Invalid field | Use API name, check field exists |
| API limit exceeded | Wait 24 hours or request limit increase |

---

**"I'll be back"** — with Salesforce automation! 💼🤖

*Taminator Salesforce Configuration Guide*  
*Terminate manual case updates*


