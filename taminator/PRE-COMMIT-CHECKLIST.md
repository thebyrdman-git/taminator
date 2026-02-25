# 🔒 Pre-Commit Security Checklist

**CRITICAL:** Run this checklist before EVERY commit to prevent sensitive data leaks.

---

## ❌ NEVER COMMIT

### 1. API Tokens / Credentials
```bash
# Check for token strings
grep -r "ghp_" . --exclude-dir=node_modules --exclude-dir=.git
grep -r "ODI3" . --exclude-dir=node_modules --exclude-dir=.git
grep -r "Bearer " . --exclude-dir=node_modules --exclude-dir=.git
grep -r "token.*=" . --exclude-dir=node_modules --exclude-dir=.git | grep -v "token_type"
```

**Never commit:**
- ❌ GitHub tokens (ghp_*)
- ❌ JIRA API tokens
- ❌ Portal API tokens
- ❌ Any Bearer tokens
- ❌ Password files
- ❌ .env files with secrets

### 2. Customer Data
```bash
# Check for customer names
grep -ri "tdbank\|td bank" . --exclude-dir=node_modules --exclude-dir=.git
grep -ri "wellsfargo\|wells fargo" . --exclude-dir=node_modules --exclude-dir=.git
grep -ri "fannie mae\|fanniemae" . --exclude-dir=node_modules --exclude-dir=.git

# Check for real JIRA IDs from customers
grep -r "AAPRFE-" . --exclude-dir=node_modules --exclude-dir=.git
grep -r "AAP-[0-9]" . --exclude-dir=node_modules --exclude-dir=.git
```

**Never commit:**
- ❌ Real customer names (TD Bank, Wells Fargo, Fannie Mae, etc.)
- ❌ Customer reports (*.md files with real data)
- ❌ Real JIRA issue IDs from customer engagements
- ❌ Customer account numbers
- ❌ Customer contact information
- ❌ taminator-test-data/ directory

### 3. Personal Information
```bash
# Check for email addresses
grep -r "@redhat.com" . --exclude-dir=node_modules --exclude-dir=.git | grep -v "jbyrd@redhat.com"

# Check for internal URLs
grep -r "redhat.com/\|corp.redhat.com" . --exclude-dir=node_modules --exclude-dir=.git
```

**Never commit:**
- ❌ Personal email addresses (other than generic examples)
- ❌ Red Hat internal URLs
- ❌ VPN configuration details
- ❌ Kerberos principal names (real ones)

---

## ✅ SAFE TO COMMIT

### Code & Documentation
- ✅ Source code (Python, JavaScript, HTML)
- ✅ Documentation (README, guides, specs)
- ✅ Test files (without real data)
- ✅ Configuration templates (without tokens)
- ✅ .gitignore file
- ✅ Requirements files (package names only)

### Sample/Generic Data
- ✅ Example templates with placeholder text
- ✅ "testcustomer" references (generic test name)
- ✅ Fake JIRA IDs (e.g., AAPRFE-999, AAP-99999)
- ✅ jbyrd@redhat.com (generic contact)
- ✅ "Jimmy Byrd" (author name)

---

## 🔍 Pre-Commit Commands

Run these commands before committing:

```bash
# 1. Check git status
git status

# 2. Review what's staged
git diff --cached

# 3. Check for tokens (returns nothing if safe)
git diff --cached | grep -i "token" | grep -v "token_type"

# 4. Check for customer names (returns nothing if safe)
git diff --cached | grep -iE "tdbank|wellsfargo|fannie.?mae"

# 5. Check for real JIRA IDs (should only see test IDs like 999)
git diff --cached | grep -E "AAPRFE-[0-9]|AAP-[0-9]"

# 6. Verify .gitignore is working
git check-ignore -v taminator-test-data/testcustomer.md
# Should output: .gitignore:...:taminator-test-data/
```

---

## 🧹 Cleaning Before Commit

If you accidentally staged sensitive data:

```bash
# Unstage specific file
git restore --staged <file>

# Unstage all files
git restore --staged .

# Remove from working directory (CAREFUL!)
git clean -fd --dry-run  # Preview first
git clean -fd            # Actually remove
```

---

## 📋 Safe Commit Examples

### Example 1: Adding New Feature
```bash
git add src/taminator/commands/new_feature.py
git add docs/NEW-FEATURE.md
git commit -m "feat: Add new customer onboarding wizard"
```

### Example 2: Bug Fix
```bash
git add src/taminator/core/auth_box.py
git commit -m "fix: Handle null assignee in JIRA API response"
```

### Example 3: Documentation
```bash
git add README.md
git add docs/USAGE-GUIDE.md
git commit -m "docs: Update usage examples"
```

---

## ⚠️ What To Do If You Committed Secrets

**If you accidentally committed secrets:**

1. **DO NOT PUSH** to remote repository
2. Amend or reset the commit:
   ```bash
   # If it's the last commit
   git reset HEAD~1
   
   # Remove the file properly
   git rm --cached <sensitive-file>
   
   # Re-commit without the sensitive data
   ```
3. **Revoke the exposed token immediately**
4. Generate a new token

**If you already pushed:**

1. **Revoke ALL exposed tokens IMMEDIATELY**
2. Contact GitHub support to purge from history
3. Force push after cleaning:
   ```bash
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch <file>" \
     --prune-empty --tag-name-filter cat -- --all
   
   git push origin --force --all
   ```

---

## 🎯 Quick Pre-Commit Script

Save as `check-commit.sh`:

```bash
#!/bin/bash

echo "🔒 Running pre-commit security checks..."

# Check for tokens
if git diff --cached | grep -iE "ghp_|Bearer |token.*=.*[a-zA-Z0-9]{20}"; then
    echo "❌ FAIL: Found potential token in staged changes"
    exit 1
fi

# Check for customer names
if git diff --cached | grep -iE "tdbank|wellsfargo|fannie.?mae"; then
    echo "❌ FAIL: Found customer name in staged changes"
    exit 1
fi

# Check for test data directory
if git status --short | grep "taminator-test-data/"; then
    echo "❌ FAIL: Attempting to commit test data directory"
    exit 1
fi

echo "✅ PASS: No sensitive data detected"
echo "Review your changes with: git diff --cached"
```

Make executable: `chmod +x check-commit.sh`

Run before commit: `./check-commit.sh && git commit`

---

## 📝 Commit Message Format

Use conventional commits:

```
feat: Add GitHub issue submission feature
fix: Resolve VPN detection on macOS
docs: Update installation guide
test: Add unit tests for auth_box
refactor: Simplify token management
chore: Update dependencies
```

---

**Remember:** When in doubt, don't commit. Review first, commit second.

