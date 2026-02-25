# RFE/Bug Tracker - Gap Analysis

**Date:** October 21, 2025  
**Purpose:** Identify all missing features and functionality gaps  
**Priority:** Fix gaps before adding new features

---

## Critical Gaps (Blocking TAM Workflow)

### Gap #1: No Status Verification Command ⭐ CRITICAL
**What's Missing:**
- No command to check if customer report is up-to-date
- No way to compare report statuses with current JIRA
- Must manually check each JIRA issue before customer calls

**Impact:**
- TAMs spend 10-15 minutes before every customer call
- Risk of discussing outdated status information
- Unprofessional if TAM has wrong status during call

**Solution:** `tam-rfe check <customer>`

**User Story:**
```
As a TAM,
I need to verify my TD Bank RFE report is current before our call,
So I can confidently discuss RFE statuses without errors.

Acceptance Criteria:
- Command completes in < 10 seconds
- Shows clear table of status comparisons
- Indicates which statuses changed
- Provides next steps if update needed
```

---

### Gap #2: No Token Management System ⭐ CRITICAL
**What's Missing:**
- No centralized token storage
- No validation of tokens before use
- Cryptic errors when tokens are missing or invalid
- No guidance on how to obtain tokens

**Impact:**
- Tools fail with confusing error messages
- TAMs don't know what tokens they need
- No clear instructions on obtaining tokens
- Security risk (tokens in environment variables)

**Solution:** TokenManager module + mandatory onboarding with validation

**User Story:**
```
As a new TAM,
When I first run the RFE tool,
I need to be guided through token setup with validation testing,
So I know the tool is configured correctly before I need it for customer work.

Acceptance Criteria:
- Mandatory onboarding wizard (tam-rfe onboard)
- Token collection (JIRA + Portal)
- Real-time validation with API tests
- Cannot proceed without valid tokens
- Clear error messages if validation fails
- Secure storage (system keyring)
```

**Integration:** Token management is part of onboarding, not a separate step.

---

### Gap #3: No Auto-Update Capability
**What's Missing:**
- Cannot automatically update report with current statuses
- Must manually edit markdown report file
- No backup before making changes
- No diff showing what changed

**Impact:**
- Time-consuming manual editing
- Risk of formatting errors
- No audit trail of changes
- Fear of breaking report format

**Solution:** `tam-rfe update <customer>`

**User Story:**
```
As a TAM,
When my TD Bank report is outdated (3 statuses changed),
I need a command that auto-updates the report safely,
So I don't waste time manually editing markdown.

Acceptance Criteria:
- Creates backup before changes
- Shows diff of what will change
- Updates only status column (preserves formatting)
- Confirms changes before applying
```

---

## Moderate Gaps (Quality of Life)

### Gap #4: No Report Auto-Detection
**What's Missing:**
- Must specify full path to report file
- No smart search for customer reports
- No standardized report location

**Impact:**
- Long command lines
- Hard to remember where reports are stored
- Different TAMs store reports in different locations

**Solution:** Smart file discovery

**Implementation:**
```python
def find_customer_report(customer: str) -> Path:
    """Search common locations for customer report."""
    search_paths = [
        Path.cwd() / f"{customer}-rfe-tracker.md",
        Path.cwd() / f"{customer}.md",
        Path.home() / "Documents" / "customers" / customer,
        Path.home() / "rfe-reports" / customer,
    ]
    # ... search and return
```

---

### Gap #5: No Diff Display
**What's Missing:**
- Cannot preview what will change before updating
- No visual diff of status changes
- Hard to review changes before applying

**Impact:**
- Fear of running update commands
- Must manually compare before/after
- No confidence in automated updates

**Solution:** `tam-rfe check <customer> --diff`

**Output Example:**
```diff
AAPRFE-762:
- | Backlog        |
+ | In Progress    |

AAPRFE-1158:
- | Review         |
+ | Closed         |
```

---

### Gap #6: No Batch Operations
**What's Missing:**
- Cannot check multiple customers at once
- Cannot update all customer reports in batch
- Must run commands one customer at a time

**Impact:**
- Repetitive commands for TAMs with many customers
- Time-consuming for weekly updates
- No way to automate "check all customers"

**Solution:** `tam-rfe check --all-customers`

**Use Case:**
```bash
# Check all configured customers
$ tam-rfe check --all

╭────────────────────────────────────────────────╮
│  Checking All Customer Reports                │
╰────────────────────────────────────────────────╯

TD Bank:        ✅ Up-to-date (9/9 match)
Wells Fargo:    ⚠️  Outdated (15/18 match - 3 changed)
JPMC:           ✅ Up-to-date (26/26 match)
Fannie Mae:     ⚠️  Outdated (8/12 match - 4 changed)

Summary: 2 reports need updates

💡 Update all: tam-rfe update --all
```

---

## Minor Gaps (Nice to Have)

### Gap #7: No Historical Tracking
**What's Missing:**
- No record of when statuses changed
- Cannot see history of RFE progress
- No trend analysis (are RFEs moving forward?)

**Impact:**
- Cannot answer: "When did this RFE move to In Progress?"
- No visibility into RFE velocity
- Hard to identify stalled RFEs

**Solution:** Status change log

**Implementation:**
```yaml
# ~/.config/taminator/status-history.yaml
AAPRFE-762:
  - date: 2025-10-01
    status: Backlog
  - date: 2025-10-15
    status: In Progress
    
AAPRFE-1158:
  - date: 2025-09-20
    status: Review
  - date: 2025-10-20
    status: Closed
    resolution: Won't Do
```

---

### Gap #8: No Customer Portal Integration
**What's Missing:**
- Cannot post updated reports to customer portal automatically
- Manual copy/paste required
- No verification that portal matches local report

**Impact:**
- Extra manual step after updating report
- Risk of forgetting to update portal
- Customer sees outdated information

**Solution:** `tam-rfe post <customer>`

**Implementation:**
- Auto-post updated report to customer portal
- Verify successful posting
- Option to preview before posting

---

### Gap #9: No JIRA Watching/Notifications
**What's Missing:**
- No alerts when customer RFE status changes
- Must manually check for updates
- No proactive notifications

**Impact:**
- Discover status changes during customer calls (embarrassing)
- Reactive instead of proactive
- Miss important updates

**Solution:** `tam-rfe watch <customer>`

**Implementation:**
```bash
# Watch TD Bank RFEs for changes
$ tam-rfe watch tdbank --notify-slack --notify-email

Watching 9 JIRA issues for TD Bank...
Will notify via:
  • Slack: #tam-td-bank channel
  • Email: jbyrd@redhat.com

Checking every 1 hour...
```

---

### Gap #10: No Report Templates
**What's Missing:**
- No standardized report format
- Each TAM creates reports differently
- Hard to share best practices

**Impact:**
- Inconsistent customer experience
- Some reports missing key information
- Hard to onboard new TAMs

**Solution:** Template library

**Implementation:**
```bash
# Create new customer report from template
$ tam-rfe init tdbank --template standard

Created: tdbank-rfe-tracker.md
Template: Standard RFE/Bug Tracker (3-table format)
```

---

## Command Feature Matrix

### Current vs Proposed

| Feature | Current | Proposed | Gap? |
|---------|---------|----------|------|
| Check status | ❌ None | `tam-rfe check` | ✅ GAP #1 |
| Token management | ❌ None | `tam-rfe config` | ✅ GAP #2 |
| Auto-update | ❌ None | `tam-rfe update` | ✅ GAP #3 |
| Auto-detect report | ❌ Must specify path | Smart search | ✅ GAP #4 |
| Show diff | ❌ None | `--diff` flag | ✅ GAP #5 |
| Batch operations | ❌ One at a time | `--all-customers` | ✅ GAP #6 |
| Historical tracking | ❌ None | Status log | ⚠️ GAP #7 |
| Portal posting | ⚠️ Complex script | `tam-rfe post` | ⚠️ GAP #8 |
| Change notifications | ❌ None | `tam-rfe watch` | ℹ️ GAP #9 |
| Report templates | ⚠️ Ad-hoc | `tam-rfe init` | ℹ️ GAP #10 |

**Legend:**
- ✅ Critical Gap (must fix)
- ⚠️ Moderate Gap (should fix)
- ℹ️ Minor Gap (nice to have)

---

## Gap Prioritization

### Phase 1: Critical Gaps (Weeks 1-3)
**Goal:** Make tool usable for core workflow

1. **Gap #1: Status Verification** (Week 1-2)
   - Implement `tam-rfe check` command
   - JIRA fetching via rhcase
   - Comparison logic
   - Beautiful table output
   - Create test customer data (not customer-specific)

2. **Gap #2: Token Management + Onboarding** (Week 3)
   - Build TokenManager module
   - Implement `tam-rfe onboard` wizard
   - Mandatory token validation with API tests
   - Block progress if validation fails
   - Clear error messages with recovery flow
   - Secure keyring storage
   - Test customer data option

3. **Gap #3: Auto-Update** (Week 4)
   - Implement `tam-rfe update`
   - Backup logic
   - Markdown parsing/updating
   - Diff display

### Phase 2: Quality of Life (Weeks 4-5)
**Goal:** Make tool delightful to use

4. **Gap #4: Auto-Detection** (Week 4)
   - Smart file search
   - Multiple search locations
   - User-configurable paths

5. **Gap #5: Diff Display** (Week 4)
   - Visual diff output
   - Side-by-side comparison
   - Syntax highlighting

6. **Gap #6: Batch Operations** (Week 5)
   - `--all-customers` flag
   - Parallel JIRA fetching
   - Summary report

### Phase 3: Advanced Features (Weeks 6-8)
**Goal:** Make tool proactive and intelligent

7. **Gap #7: Historical Tracking** (Week 6)
   - Status change logging
   - Trend analysis
   - Velocity metrics

8. **Gap #8: Portal Integration** (Week 7)
   - Auto-post to customer portal
   - Verification checks
   - Silent updates

9. **Gap #9: Change Notifications** (Week 8)
   - Watch mode
   - Slack/email alerts
   - Configurable frequency

10. **Gap #10: Report Templates** (Week 8)
    - Template library
    - `tam-rfe init` command
    - Best practices documentation

---

## Technical Debt Gaps

### TD #1: Bash Scripts (Not Elegant)
**Current:** 13 bash scripts with basic ANSI colors  
**Proposed:** Python with Rich library  
**Effort:** 2-3 weeks to migrate all scripts

### TD #2: No Testing
**Current:** No automated tests  
**Proposed:** pytest + test coverage  
**Effort:** 1 week to add test suite

### TD #3: Inconsistent Error Handling
**Current:** Each script handles errors differently  
**Proposed:** Centralized error handling with clear messages  
**Effort:** 1 week to standardize

### TD #4: No Documentation
**Current:** Scattered README files  
**Proposed:** Comprehensive docs site  
**Effort:** 1 week to create docs

### TD #5: No CI/CD
**Current:** Manual testing and deployment  
**Proposed:** GitLab CI/CD pipeline  
**Effort:** 2-3 days to set up

---

## Gap Impact Analysis

### Most Impactful Gaps (Fix First)

1. **Gap #1 (Status Verification)** - 90% impact
   - Saves 10-15 min per customer call
   - Prevents embarrassing mistakes
   - Primary use case

2. **Gap #2 (Token Management)** - 80% impact
   - Blocks tool adoption (tools don't work without tokens)
   - Frustrating error messages
   - Security improvement

3. **Gap #3 (Auto-Update)** - 70% impact
   - Saves 5-10 min per update
   - Reduces formatting errors
   - Encourages more frequent updates

### Lower Impact Gaps (Fix Later)

4-6. Quality of life improvements (30-50% impact each)
7-10. Advanced features (10-20% impact each)

---

## Success Criteria

### After Phase 1 (Critical Gaps Fixed):
- ✅ TAM can verify customer report in < 10 seconds
- ✅ TAM can update report with 1 command
- ✅ Mandatory onboarding with token validation
- ✅ Cannot proceed without validated configuration
- ✅ Test data available for exploration
- ✅ No manual JIRA checking required

### After Phase 2 (Quality of Life):
- ✅ No need to specify file paths (auto-detect)
- ✅ Can preview changes before applying
- ✅ Can update all customers in batch

### After Phase 3 (Advanced Features):
- ✅ Proactive notifications when RFEs change
- ✅ Historical tracking of RFE progress
- ✅ One-command portal posting

---

## Next Steps

1. **Immediate:** Start Gap #1 implementation (`tam-rfe check`)
2. **Week 1:** Build core functionality + Rich UI + test data
3. **Week 2:** Test with generic test data (not customer-specific)
4. **Week 3:** Build onboarding wizard with mandatory validation (Gap #2)
5. **Week 4:** Add auto-update (Gap #3)

**Bottom Line:** 10 identified gaps, 3 critical. Start with status verification command - it's the foundation. Onboarding with token validation is mandatory before tool can be used.

