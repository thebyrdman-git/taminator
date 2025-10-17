# 🔍 CPG API Endpoint Verification Guide

## 🎯 Purpose

This document provides instructions for verifying and updating the Customer Portal Private Groups (CPG) API endpoints in Taminator.

**Current Status:** ⚠️ Endpoints are PLACEHOLDERS and need verification

---

## ⚠️ CRITICAL: API Endpoints Need Verification

The CPG integration (`foundation/cpg_handler.py`) currently uses **placeholder endpoints** that need to be verified against actual Red Hat Customer Portal API documentation.

### Current Placeholder Endpoints

```python
# Base URL (likely correct)
api_base_url = "https://api.access.redhat.com/rs"

# Endpoint examples (NEED VERIFICATION):
# - GET /customers/{customer}/groups
# - POST /groups/{group_id}/posts
# - GET /query (for case lookups)
```

---

## 📚 Required Documentation

To verify and fix the CPG API endpoints, you need access to:

1. **Red Hat Customer Portal API Documentation**
   - Internal Red Hat documentation
   - API endpoint specifications
   - Authentication requirements
   - Request/response formats

2. **Private Groups API Specification**
   - How to list customer private groups
   - How to post content to groups
   - Required authentication scopes
   - Rate limiting rules

3. **Test Environment Access**
   - Test Customer Portal instance
   - Test customer with private groups
   - API credentials for testing

---

## 🔧 How to Verify Endpoints

### Step 1: Access API Documentation

**Internal Resources:**
- Red Hat Customer Portal API docs (internal wiki/confluence)
- Contact: Customer Portal API team
- Slack: #customer-portal or #api-support

**Questions to Answer:**
- What is the correct endpoint for listing customer private groups?
- What is the correct endpoint for posting content to a group?
- What authentication method is required? (Kerberos, OAuth2, API key?)
- What are the required HTTP headers?
- What is the request/response format?

### Step 2: Test with curl

Once you have the correct endpoints, test them manually:

```bash
# Test authentication
kinit your-username@REDHAT.COM

# Test listing groups (example)
curl -H "Authorization: Negotiate" \
     -H "Accept: application/json" \
     https://api.access.redhat.com/rs/customers/CUSTOMER_ID/groups

# Test posting content (example)
curl -X POST \
     -H "Authorization: Negotiate" \
     -H "Content-Type: application/json" \
     -H "Accept: application/json" \
     -d '{"title":"Test","content":"Test post","content_type":"markdown"}' \
     https://api.access.redhat.com/rs/groups/GROUP_ID/posts
```

### Step 3: Update cpg_handler.py

Once endpoints are verified, update the following methods in `foundation/cpg_handler.py`:

#### Method: `get_customer_groups()`

**Current (line ~100):**
```python
url = f"{self.config.api_base_url}/customers/{customer_name}/groups"
```

**Update to actual endpoint:**
```python
# Replace with verified endpoint from API docs
url = f"{self.config.api_base_url}/ACTUAL_ENDPOINT_PATH"
```

#### Method: `post_content()`

**Current (line ~150):**
```python
url = f"{self.config.api_base_url}/groups/{group_id}/posts"
```

**Update to actual endpoint:**
```python
# Replace with verified endpoint from API docs
url = f"{self.config.api_base_url}/ACTUAL_ENDPOINT_PATH"
```

#### Method: `_get_case_id()`

**Current (line ~250):**
```python
url = f"{self.config.api_base_url}/query"
```

**Update to actual endpoint:**
```python
# Replace with verified endpoint from API docs
url = f"{self.config.api_base_url}/ACTUAL_ENDPOINT_PATH"
```

### Step 4: Update Request Format

Verify and update the request data format:

```python
# Current post_data format (may need adjustment)
post_data = {
    'title': title,
    'content': content,
    'content_type': content_type,
    'timestamp': datetime.now().isoformat(),
    'author': self.config.username or 'TAM',
    'source': 'Taminator'
}
```

Update based on actual API requirements.

### Step 5: Test with Taminator

After updating endpoints, test with actual tools:

```bash
# Test T3 article posting
tam-t3-reader --customer test-customer --recommend --post-cpg

# Test coverage announcement
tam-coverage --customer test-customer --post-cpg
```

---

## 🔗 Likely Correct Endpoints (To Verify)

Based on Red Hat Customer Portal API patterns, the endpoints are likely:

### Base URL
```
https://api.access.redhat.com/rs
```
**Status:** ✅ Likely correct

### Authentication
- **Kerberos:** `Authorization: Negotiate` header
- **OAuth2:** `Authorization: Bearer {token}` header

**Status:** ✅ Likely correct (Kerberos is standard for internal Red Hat APIs)

### Endpoint Patterns (NEED VERIFICATION)

**List Customer Groups:**
```
GET /rs/customers/{accountNumber}/groups
GET /rs/privategroups?account={accountNumber}
GET /rs/groups?customer={accountNumber}
```

**Post to Group:**
```
POST /rs/groups/{groupId}/posts
POST /rs/privategroups/{groupId}/content
POST /rs/groups/{groupId}/discussions
```

**Get Case by Number:**
```
GET /rs/cases/{caseNumber}
GET /rs/query?caseNumber={caseNumber}
```

---

## 📋 Verification Checklist

Before marking CPG integration as production-ready:

- [ ] Obtained Red Hat Customer Portal API documentation
- [ ] Verified base URL is correct
- [ ] Verified authentication method (Kerberos/OAuth2)
- [ ] Verified endpoint for listing customer groups
- [ ] Verified endpoint for posting content
- [ ] Verified request/response format
- [ ] Verified required HTTP headers
- [ ] Verified rate limiting rules
- [ ] Tested with curl commands
- [ ] Updated cpg_handler.py with correct endpoints
- [ ] Tested with Taminator tools
- [ ] Verified posts appear in Customer Portal
- [ ] Documented any special requirements
- [ ] Updated CPG-CONFIGURATION.md with findings

---

## 🎯 Alternative: Customer Portal UI Research

If API documentation is unavailable, you can reverse-engineer endpoints by:

1. **Using Browser DevTools:**
   - Open Customer Portal in browser
   - Open DevTools (F12) → Network tab
   - Navigate to private groups
   - Post content manually
   - Observe HTTP requests in Network tab
   - Note endpoints, headers, request format

2. **Check for OpenAPI/Swagger:**
   - Try: `https://api.access.redhat.com/docs`
   - Try: `https://api.access.redhat.com/swagger.json`
   - Try: `https://api.access.redhat.com/api-docs`

3. **Contact API Team:**
   - Red Hat IT/Platform team
   - Customer Portal development team
   - Ask for API documentation or Swagger/OpenAPI spec

---

## 🚨 Temporary Workaround

Until CPG API is verified, the integration will:
- ✅ Accept `--post-cpg` flag
- ⚠️ Show warning: "CPG posting failed"
- ℹ️ Suggest configuration
- 📄 Save content to file as fallback

This ensures tools work even without CPG configured.

---

## 📞 Who to Contact

**For API Documentation:**
- Red Hat Customer Portal team
- Red Hat IT Platform Engineering
- Slack: #customer-portal
- Email: customer-portal-dev@redhat.com (if exists)

**For Testing Access:**
- Red Hat TAM manager
- Customer Portal admin team
- Request test customer with private groups

---

## ✅ Success Criteria

CPG integration is verified when:
1. Can authenticate to Customer Portal API
2. Can list customer private groups
3. Can post content to a group
4. Content appears in Customer Portal UI
5. All operations logged and auditable
6. Error handling works correctly

---

## 📝 Notes for Developer

**Current Implementation:**
- Framework is complete and well-structured
- Authentication handling is flexible (Kerberos/OAuth2)
- Error handling and fallbacks work correctly
- **Only need to update endpoint URLs**

**Estimated Time to Fix:**
- With API docs: 1-2 hours
- Without API docs (research): 4-8 hours
- Total including testing: 1 day

**Priority:**
- Medium (framework works, just needs correct endpoints)
- Not blocking other features
- Can be done in parallel with testing

---

**"I'll be back"** — with verified CPG endpoints! 🔗✅

*CPG API Verification Guide*  
*Last updated: 2025-10-17*


