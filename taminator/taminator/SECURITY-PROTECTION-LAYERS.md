# 🔒 Taminator Security Protection Layers

## 📋 TLDR

**For Contributors:** See [CONTRIBUTING.md](CONTRIBUTING.md) - Complete security and contribution guide  
**For TAM Users:** This document is for developers only. If you're using Taminator, see [README.md](README.md)

**Security Layers:**
1. .gitignore → Passive blocking
2. Pre-commit hook → Active scanning  
3. Manual audit → Required before push
4. Code review → Human verification

**Blocks:** Customer names, case numbers, tokens, personal files

---

## Overview

Taminator has **4 layers of protection** to prevent personal and customer data from being committed to the repository.

---

## Layer 1: `.gitignore` (Passive Protection)

**Location:** `taminator/.gitignore`

**What it blocks:**
- ✅ Customer names (td-bank, wells-fargo, fannie-mae, etc.)
- ✅ Case numbers (case_04275428, etc.)
- ✅ JIRA IDs in filenames
- ✅ Personal files (oauth_credentials, youtube_token, etc.)
- ✅ API tokens and secrets
- ✅ Customer data directories
- ✅ User-specific configurations
- ✅ Build artifacts

**How it works:**
- Prevents files matching patterns from being staged
- Automatic, no user action needed
- First line of defense

---

## Layer 2: Pre-Commit Hook (Active Protection)

**Location:** `taminator/.git/hooks/pre-commit`

**What it checks:**
1. ✅ Customer/client names in filenames and content
2. ✅ Case numbers (case-12345678)
3. ✅ JIRA IDs (AAP-12345, AAPRFE-1234)
4. ✅ API tokens and secrets
5. ✅ Personal files
6. ✅ Email addresses
7. ✅ Configuration files

**How it works:**
- Runs automatically before every commit
- Scans all staged files
- Blocks commit if sensitive data detected
- Shows exactly what was found

**Example output:**
```
🔒 Running Taminator pre-commit security checks...
  Checking for customer names...
❌ BLOCKED: Customer name found in: src/example.py
  Line preview:
  customer = "td-bank"

═══════════════════════════════════════
❌ COMMIT BLOCKED - Security Check Failed
═══════════════════════════════════════
```

---

## Layer 3: Manual Pre-Push Audit (Required)

**Location:** `.cursorrules` (Mandatory Rules)

**What it requires:**
1. ✅ Run comprehensive directory audit
2. ✅ Verify root directory structure
3. ✅ Check for personal files
4. ✅ Check for customer data
5. ✅ Get explicit user confirmation

**How it works:**
- Manual audit BEFORE every push
- Shows complete file list
- Requires confirmation
- Documented in `.cursorrules`

**Commands:**
```bash
# Check what files will be pushed
git ls-files | head -50
git ls-files | wc -l

# Verify NO personal files
git ls-files | grep -iE "(fannie|wells|fargo|td-bank|family-finance)" || echo "✅ Clean"

# Show directory structure
git ls-files | cut -d/ -f1 | sort -u
```

---

## Layer 4: Production Project Standards

**Location:** `.cursorrules` (Mandatory Checklist)

**What it enforces:**
- ✅ Production-ready code only
- ✅ Tested and working
- ✅ Documented
- ✅ No debug artifacts
- ✅ Security first
- ✅ Backwards compatible

**Before ANY commit:**
1. ❓ Is this code production-ready?
2. ❓ Is it tested and working?
3. ❓ Is it documented?
4. ❓ Does it maintain backwards compatibility?
5. ❓ Are there any debug artifacts to remove?
6. ❓ Will this break existing TAM workflows?

**If ANY answer is NO, do NOT commit.**

---

## Testing the Protection

### Test 1: Try to commit a customer name
```bash
echo "customer = 'td-bank'" > test.py
git add test.py
git commit -m "test"
# ❌ Should be BLOCKED by pre-commit hook
```

### Test 2: Try to commit a case number
```bash
echo "case_04275428_analysis.md" > case_file.md
git add case_file.md
git commit -m "test"
# ❌ Should be BLOCKED by pre-commit hook
```

### Test 3: Try to commit an API token
```bash
echo "api_key = 'abc123def456ghi789jkl012mno345pqr678stu901vwx'" > config.py
git add config.py
git commit -m "test"
# ❌ Should be BLOCKED by pre-commit hook
```

### Test 4: Verify .gitignore works
```bash
echo "test" > td-bank-report.md
git status
# ✅ Should NOT show the file (blocked by .gitignore)
```

---

## Bypass (Emergency Only)

**DO NOT USE UNLESS ABSOLUTELY NECESSARY**

If you need to bypass the pre-commit hook (NOT RECOMMENDED):
```bash
git commit --no-verify -m "message"
```

**Warning:** This bypasses ALL security checks. Use only in emergencies and with extreme caution.

---

## Maintaining Protection

### When Adding New Customers
Add their name patterns to:
1. `.gitignore` (passive blocking)
2. `.git/hooks/pre-commit` (active blocking)

### When Adding New Secret Patterns
Update the `SECRET_PATTERNS` in `.git/hooks/pre-commit`

### Regular Audits
Run monthly audits:
```bash
# Check for any leaked data
git log --all --full-history --source --name-only | grep -iE "customer|case|jira"

# Verify protection layers are active
ls -la .git/hooks/pre-commit
cat .gitignore | grep -A 5 "CRITICAL"
```

---

## Summary

**4 Layers = Maximum Protection**

1. 🛡️ `.gitignore` - Passive prevention
2. 🚨 Pre-commit hook - Active blocking
3. 📋 Manual audit - Required verification
4. ✅ Production standards - Quality enforcement

**Result:** Customer and personal data cannot be committed to Taminator repository.

---

## Credential storage (current and planned)

**Current:** Tokens (JIRA, Portal, Hydra) in `~/.config/taminator/ui_tokens.json` are stored as a **base64-encoded payload** (not plaintext). The file contains `{"v":1,"payload":"<base64>"}` so credentials are not human-readable on disk. Access is still protected by filesystem permissions (mode 0o600). Legacy plain JSON files are still read for backward compatibility. Google OAuth and other config may still use separate plaintext files; see User Guide.

**Planned (see [ROADMAP.md](../ROADMAP.md)):** Optional support for a proper secret store (e.g. HashiCorp Vault) so teams can use existing vaults.

---

**Last Updated:** October 21, 2025  
**Version:** 1.7.0

