# GitLab Repository Rename Guide

## 🎯 Renaming Repository: `rfe-and-bug-tracker-automation` → `taminator`

This guide walks through renaming the GitLab repository to match the new Taminator branding.

---

## ✅ What Happens When You Rename

GitLab automatically:
- ✅ Creates redirect from old URL to new URL
- ✅ Updates all merge requests, issues, wiki links
- ✅ Preserves all history and commits
- ✅ Updates repository URLs for clones

**Old URL:** `https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation`  
**New URL:** `https://gitlab.cee.redhat.com/jbyrd/taminator`

**The old URL will still work!** GitLab redirects automatically.

---

## 📋 Steps to Rename on GitLab

### 1. Navigate to Repository Settings

1. Go to: https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation
2. Click **Settings** → **General** in the left sidebar
3. Expand the **Advanced** section

### 2. Change Repository Name

In the **Advanced** section:

1. Find **"Change path"** 
2. Current path: `rfe-and-bug-tracker-automation`
3. New path: `taminator`
4. Click **"Change path"**

### 3. Confirm the Change

GitLab will show a warning:
- ⚠️ "This will change the repository URL"
- ✅ "Redirects will be created from the old path"

Click **"Confirm"** to proceed.

---

## 🔄 Update Local Git Remotes (Optional)

After renaming, your local repository still points to the old URL (which redirects).

**Option 1: Keep using old URL** (it redirects automatically)
```bash
# No changes needed! The old URL still works via redirect
```

**Option 2: Update to new URL** (cleaner)
```bash
cd ~/pai/taminator

# Update GitLab remote
git remote set-url origin https://gitlab.cee.redhat.com/jbyrd/taminator.git

# Update GitHub remote (if you want to rename there too)
git remote set-url github https://github.com/thebyrdman-git/taminator.git

# Verify
git remote -v
```

---

## 📝 Update Repository Description

While in **Settings** → **General**:

1. **Project description:** 
   ```
   Taminator - Terminate Tedious TAM Work. Intelligent automation for Red Hat TAMs. Better than Skynet. Works FOR you.
   ```

2. **Project avatar:** (optional)
   - Upload a Terminator-themed icon/logo

3. **Topics/Tags:**
   - Add: `tam`, `automation`, `ai`, `taminator`, `skynet`

---

## ✅ Verification

After renaming, verify everything works:

### 1. Old URL Redirects
```bash
# This should redirect to new URL automatically
git clone https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation.git test-old-url
cd test-old-url
git remote -v
# Should show: https://gitlab.cee.redhat.com/jbyrd/taminator.git
```

### 2. New URL Works
```bash
# This should work directly
git clone https://gitlab.cee.redhat.com/jbyrd/taminator.git test-new-url
```

### 3. Issues/MRs Still Accessible
- Old issue links: `https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation/-/issues/1`
- Should redirect to: `https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues/1`

---

## 🐙 GitHub Repository (Optional)

If you also want to rename on GitHub:

### Using GitHub Web Interface
1. Go to: https://github.com/thebyrdman-git/rfe-bug-tracker-automation
2. Click **Settings**
3. In **Repository name**, change to: `taminator`
4. Click **Rename**

GitHub also creates automatic redirects.

### Update Local Remote
```bash
git remote set-url github https://github.com/thebyrdman-git/taminator.git
```

---

## 📚 Documentation Updates

After renaming, all documentation is already updated to use new URLs:

- ✅ README.md
- ✅ LAUNCH-ANNOUNCEMENT.md
- ✅ All references to repository URLs

Old URLs are noted to redirect automatically.

---

## ⚠️ What NOT to Worry About

**GitLab handles these automatically:**
- ✅ Redirects from old URL → new URL
- ✅ Issue/MR links continue working
- ✅ Wiki links updated
- ✅ All git operations (clone, push, pull) work with old URL
- ✅ Webhooks automatically updated
- ✅ CI/CD pipelines continue working

**You DO need to update:**
- 📝 External documentation pointing to the repo
- 📝 Bookmarks (though redirects work)
- 📝 README badges (if any)

---

## 🎬 Summary

1. **Rename on GitLab:** Settings → General → Advanced → Change path
2. **Rename on GitHub (optional):** Settings → Repository name
3. **Update local remotes (optional):** `git remote set-url`
4. **Verification:** Test old and new URLs

**That's it!** GitLab handles the rest automatically.

---

## 📞 Questions?

If you encounter any issues:
- Check GitLab documentation: https://docs.gitlab.com/ee/user/project/settings/
- Contact GitLab support: https://gitlab.cee.redhat.com/help

---

*Guide for Taminator Repository Rename*  
*"I'll be back" — with a better URL! 🤖*

