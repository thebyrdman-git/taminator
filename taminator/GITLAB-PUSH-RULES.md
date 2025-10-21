# 🚨 GitLab Push Rules - MANDATORY

## ⚠️ CRITICAL: Only Taminator Files

**NEVER push files outside the `automation/rfe-bug-tracker/` directory to the Taminator GitLab repository.**

This repository is ONLY for Taminator - the RFE/Bug tracking tool. Personal PAI projects, customer data, and other files must NOT be pushed.

---

## ✅ Allowed Files

### Taminator Core
- `automation/rfe-bug-tracker/**/*`
- `.cursorrules` (only Taminator-related changes)
- `ansible/vm-*.yml` (Taminator test environment only)
- `ansible/vm-inventory.ini` (Taminator test environment only)

### Explicitly EXCLUDED
- ❌ `family-finance-app/`
- ❌ `contexts/`
- ❌ `repositories/`
- ❌ `miraclemax-infrastructure`
- ❌ `red-hat-vpn-configurator`
- ❌ Customer-specific files (Fannie Mae, Wells Fargo, TD Bank, etc.)
- ❌ Personal projects
- ❌ Any files outside `automation/rfe-bug-tracker/`

---

## 📋 Pre-Push Checklist

Before pushing to GitLab, **ALWAYS** run these commands:

```bash
cd ~/pai/automation/rfe-bug-tracker

# 1. Check what will be pushed
git log origin/$(git branch --show-current)..HEAD --name-only

# 2. Verify ONLY Taminator files
git diff --name-only origin/$(git branch --show-current)

# 3. Look for accidental includes
git status --short

# 4. If ANY non-Taminator files are staged, STOP and reset:
git reset HEAD~1  # Reset last commit but keep changes
git reset         # Unstage everything

# 5. Stage ONLY Taminator files
git add .cursorrules automation/rfe-bug-tracker/ ansible/vm-*.yml ansible/vm-inventory.ini

# 6. Commit again with clean scope
git commit -m "Your commit message"

# 7. Push when verified clean
git push origin <branch-name>
git push origin <tag-name>
```

---

## 🔒 Safe Push Commands

### For Feature Branches
```bash
cd ~/pai
git log origin/rfe-redesign-v2..HEAD --oneline  # Review commits
git diff --stat origin/rfe-redesign-v2          # Review changes
git push origin rfe-redesign-v2                  # Push branch
```

### For Releases
```bash
cd ~/pai
git push origin rfe-redesign-v2  # Push branch first
git push origin v1.7.0           # Then push tag
```

---

## 🚨 Emergency: Accidental Push

If you accidentally pushed non-Taminator files:

### Option 1: Force Push (if no one has pulled)
```bash
cd ~/pai
git reset --hard <commit-before-accident>
git push --force origin <branch-name>
```

### Option 2: Revert Commit (safer)
```bash
cd ~/pai
git revert <bad-commit-sha>
git push origin <branch-name>
```

---

## 📝 Commit Message Template

```
[Category] Brief description

✅ Changes:
- Feature/fix description
- Files modified

🔒 Verification:
- Only Taminator files included
- No customer data
- No personal projects
```

---

## 🎯 Automated Check (Future)

Consider adding a pre-push hook:

```bash
# .git/hooks/pre-push
#!/bin/bash

# Get list of files to be pushed
files=$(git diff --name-only origin/$(git branch --show-current))

# Check for forbidden patterns
if echo "$files" | grep -qE "(family-finance|contexts/|repositories/|fannie-mae|wellsfargo|td-bank)"; then
    echo "❌ ERROR: Non-Taminator files detected!"
    echo "Files found:"
    echo "$files" | grep -E "(family-finance|contexts/|repositories/|fannie-mae|wellsfargo|td-bank)"
    echo ""
    echo "See GITLAB-PUSH-RULES.md for instructions"
    exit 1
fi

echo "✅ Push verified: Only Taminator files"
exit 0
```

---

**Remember:** When in doubt, review the diff before pushing!

