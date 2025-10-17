# 🔗 rhcase Integration

## 🎯 Overview

Taminator integrates with Red Hat's `rhcase` tool to fetch real customer case data. This provides live case information for agendas, backlog cleanup, and intelligence features.

**What's Integrated:**
- ✅ **Open cases** - Active customer cases
- ✅ **Closed cases** - Recently resolved cases (last 30 days)
- ✅ **Case details** - Full case information
- ✅ **Customer discovery** - Auto-discover customers from cases
- ✅ **Case search** - Search by keywords

**Tools Using rhcase:**
- `tam-generate-agenda` - Fetches real cases for agendas
- `tam-backlog-cleanup` - Analyzes real open cases
- `tam-t3-reader` - Contextual T3 recommendations based on products
- `tam-discover-customers` - Discovers customers from case history

---

## ⚡ Quick Start

### Prerequisites

**Option 1: rhcase Submodule (Included)**
```bash
# Already included if you cloned with --recurse-submodules
cd /home/jbyrd/pai/taminator
git submodule update --init --recursive
```

**Option 2: System rhcase**
```bash
# Install rhcase system-wide
pip install rhcase

# Or use Red Hat internal installation
# (Follow your organization's installation guide)
```

### Authentication

```bash
# Authenticate with rhcase
rhcase auth

# Or use Kerberos (Red Hat internal)
kinit jbyrd@REDHAT.COM

# Test connection
rhcase list --all --months 1
```

### Usage

```bash
# Generate agenda with real case data
tam-generate-agenda --customer jpmc --print

# Cleanup backlog with real cases
tam-backlog-cleanup --customer jpmc --auto-clean

# Tools will automatically use rhcase if available
```

---

## 🔧 How It Works

### Architecture

```
Taminator Tools
     ↓
foundation/rhcase_handler.py (Python wrapper)
     ↓
rhcase CLI (binary)
     ↓
Red Hat Case Management API
```

### Data Flow

1. **Tool requests case data** (e.g., `tam-generate-agenda --customer jpmc`)
2. **rhcase_handler fetches data** (`rhcase list jpmc --status open --format json`)
3. **JSON parsing** (converts rhcase output to Python dicts)
4. **Data enrichment** (calculates age, priority, trends)
5. **Tool uses data** (generates agenda with real cases)

### Fallback Behavior

If rhcase is not available or fails:
- ✅ Tools **still work** with sample data
- ⚠️ Warning message displayed
- ℹ️ Graceful degradation (no crashes)

---

## 📚 API Reference

### Python API

```python
from foundation.rhcase_handler import get_rhcase_handler

# Get handler
handler = get_rhcase_handler()

# Fetch open cases
cases = handler.get_open_cases("jpmc")

# Fetch closed cases (last 30 days)
closed = handler.get_closed_cases("jpmc", days=30)

# Get specific case
case = handler.get_case_details("04280915")

# Search cases
results = handler.search_cases("ansible", customer="jpmc")

# List all cases
all_cases = handler.list_cases(customer="jpmc", months=6)

# Get customer accounts
customers = handler.get_customer_accounts()
```

### Case Data Structure

```python
{
    "number": "04280915",              # Case number
    "id": "04280915",                  # Alias for number
    "case_number": "04280915",         # Alias for number
    "summary": "AAP auth issue",       # Case summary/subject
    "subject": "AAP auth issue",       # Alias for summary
    "title": "AAP auth issue",         # Alias for summary
    "severity": "2",                   # 1-4 (1=critical, 4=low)
    "sev": "2",                        # Alias for severity
    "status": "open",                  # open, closed, waiting, etc.
    "created_date": "2025-10-15T...",  # ISO 8601 date
    "opened_date": "2025-10-15T...",   # Alias for created_date
    "created_at": "2025-10-15T...",    # Alias for created_date
    "last_updated": "2025-10-17T...",  # Last update timestamp
    "updated_at": "2025-10-17T...",    # Alias for last_updated
    "close_date": "2025-10-17T...",    # Close timestamp (if closed)
    "closed_date": "2025-10-17T...",   # Alias for close_date
    "owner": "jbyrd@redhat.com",       # Case owner
    "assigned_to": "jbyrd@redhat.com", # Alias for owner
    "product": "Ansible Automation Platform",
    "component": "Controller",
    "account_number": "123456",
    "account": "123456",               # Alias for account_number
    "account_name": "JPMC",
    "customer": "JPMC",                # Alias for account_name
    "sla_hours_remaining": 48,
    "sla_breached": false,
    "escalated": false,
    "last_customer_update": "2025-10-16T...",
    "waiting_on": "customer",          # customer, red_hat, partner
    "resolution": "Fixed in AAP 2.5"   # Resolution summary (if closed)
}
```

**Note:** Field names may vary. The handler normalizes common variations (e.g., `number`, `id`, `case_number` all map to the same value).

---

## 🧪 Testing rhcase Integration

### Test 1: Check rhcase Availability

```bash
# Check if rhcase is available
tam-verify --test rhcase

# Expected output:
# ✅ rhcase available and functional
# ✅ rhcase connectivity test PASSED
```

### Test 2: Test Case Fetching

```bash
# Test with Python
python3 << 'EOF'
import sys
sys.path.insert(0, '/home/jbyrd/pai/taminator')
from foundation.rhcase_handler import get_rhcase_handler

handler = get_rhcase_handler()

# Check configuration
if not handler.config.is_configured():
    print("❌ rhcase not configured")
    exit(1)

# Fetch cases
cases = handler.list_cases(customer="jpmc", status="open", months=1)
print(f"✅ Found {len(cases)} open cases for jpmc")

# Show first case
if cases:
    case = cases[0]
    print(f"\nSample case:")
    print(f"  Number: {case.get('number')}")
    print(f"  Summary: {case.get('summary')}")
    print(f"  Severity: {case.get('severity')}")
EOF
```

### Test 3: Test Tool Integration

```bash
# Generate agenda (should use real data)
tam-generate-agenda --customer jpmc --print

# Look for:
# ✅ Found X open case(s)  (real data)
# ℹ️  No open cases found (using sample data)  (fallback)
```

---

## 🛠️ Troubleshooting

### Issue: "rhcase not found"

**Problem:** rhcase tool not available

**Solution:**
```bash
# Check if rhcase submodule exists
ls -la /home/jbyrd/pai/taminator/rhcase

# If missing, initialize submodules
git submodule update --init --recursive

# Or install system-wide
pip install rhcase

# Verify
rhcase --version
```

---

### Issue: "rhcase authentication failed"

**Problem:** Not authenticated with Red Hat API

**Solution:**
```bash
# Authenticate with rhcase
rhcase auth

# Follow prompts to enter credentials

# Or use Kerberos (Red Hat internal)
kinit jbyrd@REDHAT.COM
klist  # Verify ticket

# Test
rhcase list --all --months 1
```

---

### Issue: "rhcase command timed out"

**Problem:** Network or VPN issue

**Solution:**
```bash
# Check VPN connection (Red Hat internal)
ping gitlab.cee.redhat.com

# Connect to VPN if needed
sudo nmcli connection up red-hat-vpn

# Check internet connectivity
curl -I https://api.access.redhat.com

# Increase timeout (in code)
# Edit foundation/rhcase_handler.py:
# def _run_rhcase(self, args, timeout=30):  # Increase from 30
```

---

### Issue: "No cases found" but cases exist

**Problem:** Customer name/account number mismatch

**Solution:**
```bash
# Try different customer identifiers
tam-generate-agenda --customer "JPMC"       # Name
tam-generate-agenda --customer "jpmc"       # Lowercase
tam-generate-agenda --customer "123456"     # Account number

# List all customers you have access to
rhcase list --all --months 6 | grep -i jpmc

# Or use discovery tool
tam-discover-customers --geo us
```

---

### Issue: "JSON parsing error"

**Problem:** rhcase output format changed or not JSON

**Solution:**
```bash
# Check rhcase output format
rhcase list jpmc --months 1 --format json

# Should output valid JSON
# If not, fallback to text parsing will be used

# Update rhcase to latest version
pip install --upgrade rhcase

# Or check rhcase configuration
rhcase config show
```

---

## 🔒 Security Considerations

### Authentication

- **Red Hat VPN:** May be required for internal rhcase access
- **Kerberos:** Preferred authentication method (no password storage)
- **OAuth:** rhcase handles token management
- **Credentials:** Never hardcoded, managed by rhcase tool

### Data Access

- **TAM Access Only:** Only cases you're assigned to
- **No Data Export:** Case data stays local
- **Audit Trail:** rhcase logs all API access
- **Compliance:** Follows Red Hat data handling policies

### Best Practices

```bash
# ✅ DO: Use Kerberos authentication
kinit jbyrd@REDHAT.COM

# ✅ DO: Keep rhcase updated
pip install --upgrade rhcase

# ✅ DO: Use VPN for internal access
# Connect to Red Hat VPN

# ❌ DON'T: Share rhcase credentials
# Each TAM uses their own authentication

# ❌ DON'T: Export sensitive case data
# Keep case data in Taminator tools only

# ❌ DON'T: Bypass rhcase authentication
# Always use proper auth mechanisms
```

---

## 📊 Configuration Options

### Environment Variables

```bash
# Override rhcase path
export RHCASE_PATH="/path/to/rhcase"

# Set rhcase API endpoint (if needed)
export RHCASE_API_URL="https://api.access.redhat.com"

# Enable debug output
export RHCASE_DEBUG="true"
```

### Configuration Priority

Taminator searches for rhcase in this order:

1. **Local submodule:** `taminator/rhcase/.venv/bin/rhcase`
2. **Project root:** `taminator/rhcase/rhcase`
3. **System PATH:** `rhcase` (system-wide installation)
4. **Environment variable:** `$RHCASE_PATH`

---

## 📈 Performance

### Caching

- ❌ **No caching** (always fetches fresh data)
- ✅ **Future:** Will add optional caching for performance
- ℹ️ **Why:** Ensures agendas have latest case status

### Timeouts

- **Default:** 30 seconds per rhcase command
- **Adjustable:** Can be increased for slow connections
- **Graceful:** Timeout triggers fallback to sample data

### Rate Limiting

- **rhcase handles:** API rate limiting managed by rhcase
- **No concerns:** Normal TAM usage well within limits
- **Bulk operations:** Use carefully (e.g., --all --months 12)

---

## 🔄 Migration from Sample Data

### Before (Sample Data):
```python
cases = [
    {"number": "04280915", "summary": "Sample case", ...}
]
```

### After (Real Data):
```python
from foundation.rhcase_handler import get_rhcase_handler
handler = get_rhcase_handler()
cases = handler.get_open_cases("jpmc")
```

### Gradual Rollout:
- ✅ **Graceful fallback** to sample data if rhcase unavailable
- ✅ **No breaking changes** for existing users
- ✅ **Transparent upgrade** path

---

## 📞 Need Help?

### Still Having Issues?

1. **Check rhcase status:** `tam-verify --test rhcase`
2. **Check authentication:** `rhcase list --all --months 1`
3. **Check VPN:** `ping gitlab.cee.redhat.com`
4. **Check logs:** Look for warnings in tool output
5. **Ask for help:** Slack #tam-automation

### Common Solutions

| Problem | Solution |
|---------|----------|
| rhcase not found | Initialize submodules or install system-wide |
| Authentication failed | Run `rhcase auth` or `kinit` |
| Timeout | Check VPN, increase timeout in code |
| No cases found | Verify customer name/account number |
| JSON error | Update rhcase to latest version |

---

## ✅ Verification Checklist

Before using rhcase integration:

- [ ] rhcase installed (submodule OR system-wide)
- [ ] Authentication configured (`rhcase auth` OR Kerberos)
- [ ] Test command works (`rhcase list --all --months 1`)
- [ ] VPN connected (if required)
- [ ] Tool verification passed (`tam-verify --test rhcase`)
- [ ] First agenda generated with real data

---

**"I'll be back"** — with real customer case data! 🔗🤖

*Taminator rhcase Integration Guide*  
*Terminate sample data, embrace real cases*


