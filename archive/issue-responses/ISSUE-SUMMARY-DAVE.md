# Issue Summary: Dave Carmichael Access Problem

## Timeline

1. **Issue Reported**: Dave could clone `rhcase` but not `rfe-and-bug-tracker-automation`
2. **Initial Theory**: GitLab CEE license required → Incorrect
3. **Second Theory**: Repository visibility set to Private → Incorrect (was already Internal)
4. **Root Cause Found**: Repository was a fork from private parent
5. **Fix Applied**: Removed fork relationship
6. **Status**: ✅ RESOLVED

## Root Cause

**Fork Visibility Inheritance**

The repository was forked from `Grimm Greysson / Hatter PAI` (private repo).

GitLab enforces: **Fork visibility cannot exceed parent visibility**

- Parent: **Private**
- Fork setting: **Internal** (displayed in settings)
- Fork effective: **Private** (enforced by GitLab)

This is why:
- `rhcase`: Standalone Internal repo → Dave could access ✅
- `rfe-and-bug-tracker-automation`: Fork of Private repo → Dave denied ❌

## Resolution

**Action Taken**: Removed fork relationship

**Steps**:
1. Settings → General → Advanced
2. "Remove fork relationship" section
3. Clicked button and confirmed

**Result**:
- Repository is now standalone
- Internal visibility properly applies
- All Red Hat employees with GitLab access can clone

## Documentation Updates

### README.md
- Kept simple "Internal visibility" note
- No complex GitLab CEE license instructions needed
- ZIP download still available as backup

### Response to Dave
- Explained fork relationship issue
- Confirmed fix applied
- Asked to try cloning again

## Lessons Learned

1. **Forked repos inherit parent visibility restrictions** even if settings show otherwise
2. **Check fork status** when troubleshooting access issues
3. **Standalone repos** work better for independent tools

## For Future TAMs

If you see similar "Access denied" errors on Internal repos:

1. Check if repo is a fork: Settings → General → "Remove fork relationship" section exists?
2. If yes: Remove fork relationship to make it standalone
3. If no: Check actual visibility settings

---

*Issue: Dave Carmichael (dcarmich)*
*Resolved: 2025-10-15*
*Root Cause: Fork visibility inheritance*
*Fix: Removed fork relationship*

