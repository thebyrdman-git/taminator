# Repository Permissions Issue - Investigation

## Problem Statement

User `dcarmich` (Dave Carmichael) reports:
- ✅ Can clone `https://gitlab.cee.redhat.com/gvaughn/rhcase.git`
- ❌ Cannot clone `https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation.git`

Error: "HTTP Basic: Access denied"

## Analysis

If Dave can access other GitLab CEE repos but not this one specifically, it's **NOT** a license issue - it's a **repository visibility/permissions issue**.

## Likely Causes

### 1. Repository Visibility
Current setting might be:
- **Private**: Only you and explicitly added members can access
- **Internal**: All Red Hat employees with GitLab account should access
- **Public**: Anyone can access (even without GitLab account)

### 2. Group/Member Permissions
- Repository may not be shared with appropriate groups
- Dave may need explicit member access
- Missing group inheritance

## How to Check/Fix

### Check Repository Settings

1. Go to: https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation/-/edit
2. Look at **Visibility Level**:
   - If **Private**: Only you and added members
   - Should be **Internal**: All Red Hat employees

### Check Current Visibility

1. Go to: https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation
2. Look under project name for visibility badge
3. Or go to: Settings → General → Visibility, project features, permissions

### Fix: Change to Internal

**Recommended for TAM tools:**

1. Go to: https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation/-/edit
2. Click **Settings** → **General**
3. Expand **Visibility, project features, permissions**
4. Change **Project visibility** to: **Internal**
   - "The project can be accessed by any logged in user except external users."
5. Click **Save changes**

### Alternative: Add Dave as Member

If you want to keep it Private:

1. Go to: https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation/-/project_members
2. Click **Invite members**
3. Add: `dcarmich` (Dave Carmichael)
4. Role: **Developer** or **Reporter** (for read-only)
5. Click **Invite**

### Compare with rhcase Repository

Check what `gvaughn/rhcase` uses:
1. Go to: https://gitlab.cee.redhat.com/gvaughn/rhcase
2. Look at visibility badge
3. Likely set to **Internal** (that's why Dave can access it)

## Actual Root Cause (RESOLVED)

**Fork Relationship Issue**

The repository was a **fork** from a private parent repo (`Grimm Greysson / Hatter PAI`).

GitLab enforces: **Fork visibility ≤ Parent visibility**

Even though the fork was set to "Internal", it inherited access restrictions from the Private parent.

## Resolution Applied

**Removed fork relationship:**

1. Settings → General → Advanced
2. Click "Remove fork relationship"
3. Confirmed removal

**Result**: Repository is now standalone and properly respects Internal visibility setting.

## Post-Fix Response to Dave

After fixing visibility:

```markdown
Hi Dave! Found the issue - the repository visibility was too restrictive.

I've updated it to **Internal** visibility, which means all Red Hat employees with GitLab access can now clone it.

**Try again:**
```bash
git clone https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation.git
```

Should work now! Let me know if you still have issues.
```

---

*Investigation Date: 2025-10-15*
*Issue: Repository permissions too restrictive*

