# Red Hat Customer Portal API Configuration Guide

## 🎯 Overview

This guide explains how to configure and test the Red Hat Customer Portal API integration for seamless posting of RFE/Bug tracker reports to customer group discussions.

## 🔧 API Configuration

### **1. Environment Variables**

Set these environment variables for API authentication:

```bash
# Red Hat Customer Portal API Credentials
export REDHAT_PORTAL_USERNAME="your-redhat-username"
export REDHAT_PORTAL_PASSWORD="your-redhat-password"

# Optional: API Environment (qa, stage, production)
export REDHAT_PORTAL_ENVIRONMENT="production"
```

### **2. API Endpoints**

The system supports multiple Red Hat environments:

| Environment | Base URL | Purpose |
|-------------|----------|---------|
| **QA** | `https://access.qa.redhat.com` | Testing and development |
| **Stage** | `https://access.stage.redhat.com` | Pre-production testing |
| **Production** | `https://access.redhat.com` | Live customer portal |

### **3. API Endpoints Used**

- **Authentication**: `/api/v1/auth/login`
- **Group Discussions**: `/api/v1/groups/{group_id}/discussions`
- **User Profile**: `/api/v1/user/profile`

## 🧪 Testing API Integration

### **1. Test API Client**

```bash
cd /home/jbyrd/pai/automation/rfe-bug-tracker/src
python3 redhat_portal_api_client.py
```

**Expected Output:**
```
🧪 Testing Red Hat Portal API Client
==================================================
1. Testing authentication...
✅ Authentication successful
2. Testing connection...
✅ Connection test successful
🎯 Red Hat Portal API Client ready for production use!
```

### **2. Test RFE Discussion Posting**

```bash
cd /home/jbyrd/pai/automation/rfe-bug-tracker/src
python3 -c "
from rfe_discussion_api_client import RFEDiscussionAPIClient
client = RFEDiscussionAPIClient()
test_cases = [{'caseNumber': 'TEST001', 'summary': 'Test RFE', 'rfe_type': 'RFE', 'status': 'Open'}]
result = client.post_rfe_discussion('wellsfargo', test_cases)
print('Result:', result)
"
```

### **3. Test Complete Workflow**

```bash
cd /home/jbyrd/pai/automation/rfe-bug-tracker/bin
./tam-rfe-monitor-simple wellsfargo --test
```

## 🔐 Authentication Methods

### **Method 1: Environment Variables (Recommended)**

```bash
# Set credentials
export REDHAT_PORTAL_USERNAME="your-username"
export REDHAT_PORTAL_PASSWORD="your-password"

# Test authentication
python3 -c "
from redhat_portal_api_client import RedHatPortalAPIClient
client = RedHatPortalAPIClient()
print('Auth result:', client.authenticate())
"
```

### **Method 2: Interactive Authentication**

```python
from redhat_portal_api_client import RedHatPortalAPIClient

client = RedHatPortalAPIClient()
username = input("Red Hat Username: ")
password = input("Red Hat Password: ")

# Set credentials temporarily
import os
os.environ['REDHAT_PORTAL_USERNAME'] = username
os.environ['REDHAT_PORTAL_PASSWORD'] = password

# Authenticate
success = client.authenticate()
print(f"Authentication: {'✅ Success' if success else '❌ Failed'}")
```

## 🚀 Production Deployment

### **1. Secure Credential Storage**

For production deployment, use secure credential storage:

```bash
# Using GPG encryption (recommended)
echo "your-redhat-password" | gpg --symmetric --cipher-algo AES256 --output ~/.config/pai/secrets/redhat-portal-password.gpg

# Using system keyring
python3 -c "
import keyring
keyring.set_password('redhat-portal', 'username', 'your-username')
keyring.set_password('redhat-portal', 'password', 'your-password')
"
```

### **2. Production Configuration**

```bash
# Production environment variables
export REDHAT_PORTAL_ENVIRONMENT="production"
export REDHAT_PORTAL_USERNAME="$(keyring get redhat-portal username)"
export REDHAT_PORTAL_PASSWORD="$(keyring get redhat-portal password)"

# Or from GPG encrypted file
export REDHAT_PORTAL_PASSWORD="$(gpg --decrypt ~/.config/pai/secrets/redhat-portal-password.gpg)"
```

## 🔍 Troubleshooting

### **Common Issues**

#### **1. Authentication Failed**

**Error**: `Authentication failed: 401 - Unauthorized`

**Solutions**:
- Verify username and password are correct
- Check if account has API access permissions
- Ensure environment variables are set correctly

```bash
# Debug authentication
python3 -c "
import os
print('Username:', os.getenv('REDHAT_PORTAL_USERNAME'))
print('Password set:', bool(os.getenv('REDHAT_PORTAL_PASSWORD')))
"
```

#### **2. Connection Failed**

**Error**: `Connection test failed: 404`

**Solutions**:
- Check if you're connected to Red Hat VPN
- Verify API endpoints are correct
- Try different environment (qa, stage, production)

```bash
# Test connectivity
curl -I https://access.redhat.com/api/v1/user/profile
```

#### **3. Group Access Denied**

**Error**: `Failed to create discussion: 403 - Forbidden`

**Solutions**:
- Verify you have access to the customer group
- Check group ID is correct
- Ensure you have posting permissions

```bash
# Test group access
python3 -c "
from redhat_portal_api_client import RedHatPortalAPIClient
client = RedHatPortalAPIClient()
client.authenticate()
discussions = client.get_group_discussions('4357341')  # Wells Fargo group
print('Group access:', '✅ OK' if discussions is not None else '❌ Denied')
"
```

### **Debug Mode**

Enable debug logging for detailed troubleshooting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from redhat_portal_api_client import RedHatPortalAPIClient
client = RedHatPortalAPIClient()
client.authenticate()
```

## 📊 API Usage Monitoring

### **1. Rate Limiting**

The Red Hat Customer Portal API has rate limits:
- **Authentication**: 10 requests per minute
- **Discussion Creation**: 5 requests per minute
- **Discussion Retrieval**: 20 requests per minute

### **2. Error Handling**

The API client includes comprehensive error handling:

```python
result = client.create_group_discussion(group_id, title, body)

if result and result.get('success'):
    print(f"✅ Posted successfully: {result.get('discussion_id')}")
else:
    error = result.get('error', 'Unknown error')
    print(f"❌ Failed: {error}")
```

### **3. Retry Logic**

The API client includes automatic retry logic:
- **Max Retries**: 3 attempts
- **Retry Delay**: 1 second (exponential backoff)
- **Timeout**: 30 seconds per request

## 🎯 Success Criteria

### **API Integration is Working When:**

1. ✅ **Authentication succeeds** without errors
2. ✅ **Connection test passes** to Red Hat Customer Portal
3. ✅ **Group discussions can be retrieved** from customer groups
4. ✅ **New discussions can be created** in customer groups
5. ✅ **RFE reports are posted successfully** to customer portals
6. ✅ **Error handling works gracefully** for failures

### **Test Commands**

```bash
# Complete API test suite
cd /home/jbyrd/pai/automation/rfe-bug-tracker/bin
./tam-rfe-verify --test api
./tam-rfe-verify --test connectivity
./tam-rfe-verify --test authentication

# End-to-end test
./tam-rfe-monitor-simple wellsfargo --test
```

## 🔗 Integration with RFE Automation

### **Automatic API Integration**

The RFE automation system automatically:

1. **Authenticates** with Red Hat Customer Portal API
2. **Generates** professional 3-table RFE reports
3. **Posts** reports to customer group discussions
4. **Monitors** posting success/failure
5. **Sends** email notifications on completion

### **Configuration Files**

- **Customer Groups**: `config/customer_group_ids.json`
- **API Settings**: Environment variables
- **Templates**: `src/templates/rfe_report.md`

## 🚀 Ready for Production

Once configured, the API integration provides:

- ✅ **Seamless posting** of RFE/Bug reports to customer portals
- ✅ **Professional formatting** with 3-table structure
- ✅ **Automatic scheduling** and monitoring
- ✅ **Error handling** and recovery
- ✅ **Email notifications** for TAMs
- ✅ **Audit logging** for compliance

**The tool is now ready to seamlessly post active case reports and RFE/Bug automation reports into customer group discussion pages!**
