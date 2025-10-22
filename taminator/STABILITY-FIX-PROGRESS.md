# Taminator v1.9.1 - Stability Fix Progress

## 🎯 Goal: Make Core RFE/Bug Features Fully Functional

**Started**: October 22, 2025  
**Status**: Phase 1 Complete - IPC Handlers Implemented

---

## ✅ Phase 1: IPC Handler Implementation (COMPLETE)

### What Was Done

Added 4 missing IPC handlers to `gui/main.js`:

1. **`check-report`** (lines 714-789)
   - Compares local RFE/Bug report with live JIRA data
   - Calls: `src/taminator/commands/check.py --customer <name> --json`
   - Returns: `{ success, issues[], summary }`
   
2. **`update-report`** (lines 794-873)
   - Fetches latest JIRA data and updates local report
   - Calls: `src/taminator/commands/update.py --customer <name> --json`
   - Supports: `--preserve-notes`, `--generate-changelog`
   - Returns: `{ success, updated_count, changes[], report_path }`

3. **`post-report`** (lines 878-958)
   - Publishes report to Customer Portal Group
   - Calls: `src/taminator/commands/post.py --customer <name> --json`
   - Supports: `--dry-run`, `--validate`, `--notify`
   - Returns: `{ success, portal_url, discussion_id }`

4. **`onboard-generate`** (lines 963-1047)
   - Generates initial RFE/Bug report for new customer
   - Calls: `src/taminator/commands/onboard.py --json`
   - Returns: `{ success, report_path, rfes_found, bugs_found }`

### Handler Features

✅ **Development Mode Support**: Resolves Python scripts from `../src` directory  
✅ **Production Mode Support**: Resolves from `process.resourcesPath` (AppImage)  
✅ **Bundled Python Packages**: Uses bundled packages in production  
✅ **Error Handling**: Comprehensive error catching and logging  
✅ **JSON Output**: Expects and parses JSON from Python commands  
✅ **Graceful Failures**: Returns `success: false` with error messages

---

## 🔄 Phase 2: Python Command JSON Output (NEXT)

### What Needs To Be Done

The Python commands currently output Rich console tables (beautiful CLI output), but the GUI needs JSON. We need to add `--json` flag support to each command.

#### 1. Update `check.py`

**Current**: Outputs Rich tables to terminal  
**Needed**: Add `--json` flag that outputs:

```json
{
  "issues": [
    {
      "jira_id": "AAPRFE-1234",
      "title": "Feature X",
      "local_status": "In Progress",
      "live_status": "Resolved",
      "match": false
    }
  ],
  "summary": {
    "total": 10,
    "matching": 8,
    "outdated": 2
  }
}
```

#### 2. Update `update.py`

**Current**: Outputs Rich progress and tables  
**Needed**: Add `--json` flag that outputs:

```json
{
  "updated_count": 5,
  "changes": [
    {
      "jira_id": "AAPRFE-1234",
      "old_status": "In Progress",
      "new_status": "Resolved"
    }
  ],
  "report_path": "/path/to/report.md"
}
```

#### 3. Update `post.py`

**Current**: Outputs Rich success/failure messages  
**Needed**: Add `--json` flag that outputs:

```json
{
  "portal_url": "https://access.redhat.com/discussions/1234567",
  "discussion_id": "1234567",
  "posted_at": "2025-10-22T10:30:00Z"
}
```

#### 4. Update `onboard.py`

**Current**: Interactive CLI prompts  
**Needed**: Add `--json` flag that outputs:

```json
{
  "customer": {
    "name": "Acme Corp",
    "slug": "acme-corp",
    "account": "123456"
  },
  "report_path": "/path/to/report.md",
  "rfes_found": 12,
  "bugs_found": 5
}
```

### Implementation Strategy

For each Python command:

1. Add `--json` argument to `main()` function
2. Check `if json_output:` before any Rich output
3. Build result dictionary instead of printing to console
4. Use `json.dumps(result)` at the end
5. Send to stdout (JSON only, no other text)
6. Send errors/warnings to stderr

**Example Pattern**:

```python
def main(customer: str = None, json_output: bool = False):
    """Main entry point for tam-rfe check command."""
    
    if json_output:
        # Build JSON result
        result = {
            "issues": [],
            "summary": {}
        }
        # ... logic ...
        print(json.dumps(result))
        return
    
    # Existing Rich console output
    console.print(...)
```

---

## 🧪 Phase 3: Testing & Validation (AFTER PHASE 2)

### Test Cases

1. **Check Report**
   - Test with customer that has RFE/Bug report
   - Verify JIRA connection works
   - Verify results display in GUI table

2. **Update Report**
   - Test with outdated report
   - Verify updates are written to file
   - Verify changelog generation

3. **Post Report**
   - Test with `--dry-run` (preview mode)
   - Test actual posting to Customer Portal
   - Verify URL is returned and opened

4. **Onboard Generate**
   - Test with new customer data
   - Verify report is created
   - Verify RFE/Bug discovery works

### Prerequisites for Testing

✅ Red Hat VPN connection  
✅ JIRA API token (stored in Auth Box)  
✅ Customer Portal token (stored in Auth Box)  
✅ Customer with existing RFE/Bug report  
✅ Customer Portal group ID

---

## 📦 Phase 4: Build & Deploy (AFTER PHASE 3)

1. **Update Version**: Increment to v1.9.2
2. **Rebuild AppImage**: `cd gui && npm run build`
3. **Test AppImage**: Verify all 4 features work
4. **Upload to GitLab CEE & GitHub**
5. **Update README with feature status**

---

## 🎯 Success Criteria

- [x] IPC handlers implemented in `main.js`
- [ ] Python commands support `--json` output
- [ ] Check Reports page works with real data
- [ ] Update Reports page works with real data
- [ ] Post to Portal works with real data
- [ ] Onboarding Wizard generates reports
- [ ] No errors when clicking on any core feature
- [ ] Graceful error messages for missing auth
- [ ] Build v1.9.2 AppImage
- [ ] Deploy to GitLab & GitHub

---

## 📝 Notes

- **Commit**: `2939847f` - IPC handlers added to `main.js`
- **Branch**: `taminator-v1.9.1`
- **Lines Added**: 342 lines to `main.js`
- **Next Session**: Implement `--json` flag in Python commands

---

**Current State**: Core RFE/Bug features will now **call** the Python backend, but Python commands need to be updated to return JSON instead of Rich console output.

**Impact**: Pages won't crash anymore, but will show "parse error" until Python commands are updated.

**Priority**: HIGH - These are the core features TAMs need for daily work.

