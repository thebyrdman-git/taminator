# Hydra API Integration - Phase 1 Complete

## ✅ What We Built

Phase 1 delivers **geographic and portfolio-based customer discovery** using Red Hat's case system data (via rhcase's Hydra backend).

### New Tool: `tam-rfe-discover-customers-hydra`

**Capabilities:**
- ✅ Discover customers by geographic region (NAMER, EMEA, APAC, LATAM, India)
- ✅ View your complete customer portfolio with activity metrics
- ✅ List all available regions with case counts
- ✅ Real-time data from Red Hat systems (no stale database)

### Commands Available

```bash
# View your configured customer portfolio
./bin/tam-rfe-discover-customers-hydra my-portfolio

# Discover customers by region
./bin/tam-rfe-discover-customers-hydra geo APAC
./bin/tam-rfe-discover-customers-hydra geo NAMER
./bin/tam-rfe-discover-customers-hydra geo EMEA

# List all available regions
./bin/tam-rfe-discover-customers-hydra regions

# Organization discovery (limited - see below)
./bin/tam-rfe-discover-customers-hydra org NAPS
```

## 🎯 What Works

### Geographic Discovery ✅
**Tested and working:**

```bash
$ ./bin/tam-rfe-discover-customers-hydra geo APAC

🌍 Discovering Customers in Region: APAC

✅ Found 1 unique customer(s) in APAC

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏢 Customer: Westpac Banking Corporation
   Account #: 1363155
   Vertical: Financial Services
   CSM: Daniel Forte
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Portfolio View ✅
Shows all configured customers with activity metrics:
- Customer name and account number
- Vertical classification
- CSM assignment
- Case count (last 3 months)

### Regional Distribution ✅
```bash
$ ./bin/tam-rfe-discover-customers-hydra regions

🌍 Geographic Regions Available

  • NA: 103 cases (North America)
  • India: 79 cases
  • EMEA: 17 cases
  • APAC: 13 cases
  • LATAM: 10 cases
```

## ⚠️ Current Limitations

### Organization Filtering (NAPS, etc.)
**Status:** Not available in Phase 1

**Why:** 
- Red Hat case data doesn't include org classification (NAPS, Commercial, etc.)
- Org structure exists only in Hydra's organizational API
- Requires direct Hydra API authentication (OAuth2 + Kerberos)

**Workaround:**
- Use geographic filtering as proxy
- North America customers are often NAPS
- Manual identification for now

### Data Source
**Current:** Case-based discovery (6 month window)
- Only shows customers with recent case activity
- Misses dormant accounts with no cases

**Future:** Direct Hydra API will show all assigned customers

## 🔧 Technical Implementation

### Architecture

```
tam-rfe-discover-customers-hydra
    ↓
rhcase (authenticated)
    ↓
Red Hat Hydra REST API
(https://access.redhat.com/hydra/rest)
    ↓
Case metadata with geographic/CSM info
```

### Data Available Per Customer
- ✅ Account number
- ✅ Customer name
- ✅ Vertical (Financial Services, etc.)
- ✅ Geographic region (caseOwnerSuperRegion)
- ✅ CSM assignment
- ✅ Recent case activity
- ❌ Organization (NAPS, Commercial) - not in case data
- ❌ TAM assignment - inferred from configuration

### Authentication
- Uses existing `rhcase` authentication
- Leverages OAuth2 tokens managed by rhcase
- No additional setup required
- Requires Red Hat VPN connection

## 📊 Use Cases Enabled

### 1. Geographic Customer Discovery
**Scenario:** New TAM in APAC region

```bash
# Discover all APAC customers
./bin/tam-rfe-discover-customers-hydra geo APAC

# Configure them for automation
./bin/tam-rfe-onboard-intelligent
```

### 2. Portfolio Overview
**Scenario:** Review your customer assignments

```bash
# See all configured customers with activity
./bin/tam-rfe-discover-customers-hydra my-portfolio

# Output shows case volume, CSM, vertical
```

### 3. Regional Analysis
**Scenario:** Understand regional distribution

```bash
# See which regions have most activity
./bin/tam-rfe-discover-customers-hydra regions

# NA: 103 cases
# India: 79 cases
# EMEA: 17 cases
```

### 4. Cross-Regional Discovery
**Scenario:** Taking over accounts in multiple regions

```bash
# Check each region
./bin/tam-rfe-discover-customers-hydra geo NAMER
./bin/tam-rfe-discover-customers-hydra geo EMEA
./bin/tam-rfe-discover-customers-hydra geo APAC
```

## 🚀 Phase 2 Roadmap

### Direct Hydra API Access
**Goal:** Full organizational discovery

**Requirements:**
1. OAuth2 + Kerberos authentication to Hydra API
2. Access to organizational endpoints
3. TAM assignment data

**Will Enable:**
- ✅ True NAPS customer discovery
- ✅ Commercial org filtering
- ✅ All assigned customers (not just active)
- ✅ Org hierarchy browsing
- ✅ TAM → Customer mapping

**Endpoints Needed:**
```
GET /api/v1/organizations/NAPS/customers
GET /api/v1/tam/{username}/assignments
GET /api/v1/customers/{account}/details
```

### Hybrid Approach (Recommended)
**Strategy:** Use both data sources

```
Phase 1 (Case-based)     +    Phase 2 (Direct API)
├─ Recent activity              ├─ Complete assignments
├─ Geographic data              ├─ Org structure
├─ Works now                    ├─ Dormant accounts
└─ Limited scope                └─ Authoritative source
```

**Cross-Validation:**
- Compare case activity vs assignments
- Flag: "Assigned but no cases"
- Alert: "Cases from unassigned customer"

## 📁 Files Added

```
bin/
├─ tam-rfe-discover-customers-hydra    # Main tool (Phase 1)
└─ tam-rfe-hydra-connector             # Direct API (Phase 2 foundation)

docs/
├─ HYDRA-API-PHASE1.md                 # This document
└─ CUSTOMER-DISCOVERY.md               # Original case-based discovery
```

## 🎯 Strategic Value

### Phase 1 Achievement
✅ **Geographic Discovery** - Find customers by region
✅ **Portfolio View** - Understand your assignments
✅ **No Additional Auth** - Uses existing rhcase
✅ **Works Today** - Requires VPN only

### What Phase 1 Enables
- Regional TAM transfers
- Cross-geo customer research
- Portfolio analysis
- Activity-based discovery

### What Phase 2 Will Add
- True NAPS org discovery
- Complete TAM assignments
- All customers (active + dormant)
- Authoritative org structure

## 💡 Best Practices

### When to Use Phase 1 Tool
- ✅ Discovering customers by geography
- ✅ Reviewing your active portfolio
- ✅ Finding customers with recent cases
- ✅ Regional analysis

### When You Need Phase 2
- ❌ Finding all NAPS customers
- ❌ Discovering dormant accounts
- ❌ Browsing org hierarchies
- ❌ Getting complete assignments

### Workaround Until Phase 2
**For NAPS discovery:**
1. Use geographic filter (NA region)
2. Check customer names for government indicators
3. Manually verify org assignment
4. Configure via onboarding tool

## 🧪 Testing

All Phase 1 features tested and working:

```bash
# ✅ Regional discovery
./bin/tam-rfe-discover-customers-hydra geo APAC
# Result: Found Westpac Banking Corporation (APAC)

# ✅ Portfolio view  
./bin/tam-rfe-discover-customers-hydra my-portfolio
# Result: 6 customers with activity metrics

# ✅ Regional distribution
./bin/tam-rfe-discover-customers-hydra regions
# Result: NA (103), India (79), EMEA (17), APAC (13), LATAM (10)
```

---

**Phase 1 Status:** ✅ **COMPLETE AND FUNCTIONAL**

**Next Step:** Phase 2 - Direct Hydra API authentication for full org discovery

**Strategic Achievement:** TAMs can now discover customers by geography using live Red Hat data, enabling cross-regional workflows that weren't possible before.

