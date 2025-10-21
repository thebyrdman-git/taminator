# Contributing to Taminator

## 📋 TLDR

**Rule:** Production-quality code only. No tokens, no customer data.  
**Test:** All features before commit.  
**Security:** Pre-commit hook blocks violations automatically.

```bash
# Quick check before committing
git status --short                  # What's staged?
grep -r "td-bank\|wells\|fannie" . # Any customer names?
grep -r "case_[0-9]" .             # Any case numbers?
```

**If found: Remove before committing.**

---

## 🏭 Production Project Standards

**Taminator is a PRODUCTION project for Red Hat TAMs.**

Treat every commit like it's shipping to customers.

### Before ANY Commit

Ask yourself:
1. ❓ Is this code production-ready?
2. ❓ Is it tested and working?
3. ❓ Is it documented?
4. ❓ Does it maintain backwards compatibility?
5. ❓ Are there any debug artifacts to remove?
6. ❓ Will this break existing TAM workflows?

**If ANY answer is NO, do NOT commit.**

### Production Quality Requirements

- ✅ **Professional Code**: Clean, documented, maintainable
- ✅ **Testing Required**: All features tested before commit
- ✅ **Documentation**: Update README/GETTING-STARTED for changes
- ✅ **No Debug Code**: Remove console.log, test data, debugging artifacts
- ✅ **Semantic Versioning**: Increment version properly (major.minor.patch)
- ✅ **Changelog**: Document changes in commit messages
- ✅ **Security First**: Never commit secrets, tokens, or customer data
- ✅ **Backwards Compatible**: Don't break existing TAM workflows
- ✅ **Professional Commits**: Clear messages, logical grouping

---

## 🔒 Security Rules (CRITICAL)

### 4-Layer Protection System

Taminator uses 4 layers to prevent data leaks:

1. **`.gitignore`** - Passive blocking (159 patterns)
2. **Pre-commit hook** - Active scanning (7 checks)
3. **Manual audit** - Required before push
4. **Code review** - Human verification

### What NEVER Gets Committed

#### 1. Customer/Client Names
❌ **BLOCKED:**
- td-bank, wells-fargo, fannie-mae, jpmc, chase, citibank
- Any bank or financial institution names
- Any identifiable customer references

✅ **ALLOWED:**
- Generic examples in `examples/` directory only
- Use "example-customer" or "customer-a" as placeholders

#### 2. Case Numbers
❌ **BLOCKED:**
- `case_04275428`
- Any format: `case-12345678`, `case_12345678`

✅ **ALLOWED:**
- Reference pattern in documentation: "case_########"

#### 3. JIRA IDs
❌ **BLOCKED:**
- Real JIRA IDs in code: `AAP-12345`, `AAPRFE-1234`

✅ **ALLOWED:**
- In `examples/` directory with "EXAMPLE" disclaimer
- Documentation patterns: "AAP-#####"

#### 4. API Tokens and Secrets
❌ **BLOCKED:**
- GitHub tokens (ghp_*)
- Any Bearer tokens
- API keys in code
- Passwords
- SSH private keys
- `.env` files with real values

✅ **ALLOWED:**
- `.env.example` with placeholder values
- Documentation showing token format (not real tokens)

#### 5. Personal Information
❌ **BLOCKED:**
- Personal file names (jimmy, charles, byrd)
- Personal email addresses (use jbyrd@redhat.com as example only)
- OAuth credentials
- YouTube tokens
- Personal configuration files

#### 6. Configuration Files with Real Data
❌ **BLOCKED:**
- `config/customer_group_ids.yaml` with real IDs
- Any config with production values

✅ **ALLOWED:**
- `config/customer_group_ids.yaml.example` with placeholders
- Template files with dummy data

---

## 🔍 Pre-Commit Security Hook

### Automatic Protection

The pre-commit hook runs automatically and checks:

1. Customer/client names in filenames and content
2. Case numbers (`case-12345678`)
3. JIRA IDs (`AAP-12345`, `AAPRFE-1234`)
4. API tokens and secrets
5. Personal files
6. Email addresses (except approved)
7. Configuration files

### Hook Location

- **Installed:** `.git/hooks/pre-commit` (executable)
- **Source:** `taminator/.git/hooks/pre-commit` (template)
- **Auto-install:** Run `./setup.sh` to install

### If Commit is Blocked

```bash
# 1. Check what triggered the block
cat .git/hooks/pre-commit

# 2. Find the violation
git diff --cached | grep -iE "td-bank|wells|fannie|case_"

# 3. Remove sensitive data
# Edit files to remove violations

# 4. Retry commit
git add <fixed-files>
git commit -m "..."
```

### Emergency Bypass (NOT RECOMMENDED)

```bash
git commit --no-verify -m "..."
# WARNING: This bypasses ALL security checks
# Only use in emergencies and with extreme caution
```

---

## 📋 GitLab Push Rules

### MANDATORY Pre-Push Audit

Before EVERY push, run this audit:

```bash
# 1. Check what files will be pushed
git ls-files | head -50
git ls-files | wc -l

# 2. Verify root directory structure
git ls-files | cut -d/ -f1 | sort -u
# Expected: ansible, README.md, taminator ONLY

# 3. Check for personal files
git ls-files | grep -iE "(fannie|wells|fargo|td-bank|oauth|youtube)" || echo "✅ Clean"

# 4. Check for customer data
git ls-files | grep -iE "case_[0-9]" || echo "✅ Clean"
```

### Allowed Files ONLY

✅ **Push these:**
- `taminator/` - All Taminator files
- `ansible/vm-*.yml` - Test environment files
- `ansible/vm-inventory.ini` - Test inventory
- `README.md` - Root documentation

❌ **NEVER push:**
- Personal PAI projects
- Customer-specific files
- `.cursorrules` (workspace config)
- `AGENTS.md`, `GEMINI.md` (personal config)
- Family finance, miraclemax, vpn-configurator, etc.
- Any files outside `taminator/` and `ansible/vm-*`

### If Audit Fails

```bash
# STOP immediately
# Reset and fix

git reset HEAD~1        # Undo last commit (keep changes)
git reset              # Unstage everything
# Fix violations
# Re-commit correctly
```

---

## 🧪 Testing Requirements

### Hybrid Testing Approach

Use both real and simulated testing:

**Real Testing (Required for):**
- GUI functionality and UX
- Authentication flows (VPN, Kerberos, tokens)
- End-to-end workflows
- Visual verification

**Simulated Testing (Acceptable for):**
- Unit tests for core functions
- Security checks
- Error handling
- API responses (can mock)

### Before Committing

```bash
# Test the feature
# GUI: Launch and verify
./Taminator-*.AppImage

# CLI: Run command
./tam-rfe check --customer example-customer

# Verify no errors in output
```

---

## 📝 Code Quality Standards

### Python Code

```python
# Good: Clean, documented, typed
def fetch_jira_status(issue_id: str) -> dict:
    """
    Fetch JIRA issue status from Red Hat JIRA.
    
    Args:
        issue_id: JIRA issue ID (e.g., "AAP-12345")
    
    Returns:
        dict: Issue status and metadata
    """
    # Implementation
    pass

# Bad: No types, no docs, unclear
def get_status(id):
    return fetch(id)
```

### JavaScript/GUI Code

```javascript
// Good: Clear, no debug code
function checkAuthStatus() {
  const vpnConnected = checkVPN();
  const kerberosValid = checkKerberos();
  return { vpnConnected, kerberosValid };
}

// Bad: Debug code left in
function checkAuthStatus() {
  console.log('Checking auth...');
  const vpn = checkVPN();
  console.log('VPN:', vpn);
  return { vpn };
}
```

### Remove Before Committing

- ❌ `console.log()` statements
- ❌ `print()` debug statements
- ❌ TODO comments without JIRA tickets
- ❌ Commented-out code blocks
- ❌ Test data in production code
- ❌ Hardcoded paths or URLs

---

## 🔄 Contribution Workflow

### 1. Setup Development Environment

```bash
# Clone repository
git clone git@gitlab.cee.redhat.com:jbyrd/taminator.git
cd taminator

# Install pre-commit hook
./setup.sh

# Verify hook is installed
ls -la .git/hooks/pre-commit
```

### 2. Create Feature Branch

```bash
git checkout -b feature/my-feature-name
# or
git checkout -b bugfix/issue-description
```

### 3. Develop

- Write clean, documented code
- Test thoroughly (real + simulated)
- Update documentation if needed

### 4. Commit

```bash
# Stage changes
git add <files>

# Pre-commit hook runs automatically
git commit -m "feat: Add feature description

- Detailed change 1
- Detailed change 2

Closes #123"
```

### 5. Pre-Push Audit

```bash
# Run mandatory audit
git ls-files | head -50
git ls-files | cut -d/ -f1 | sort -u
git ls-files | grep -iE "(fannie|wells|customer)" || echo "✅ Clean"
```

### 6. Push

```bash
git push origin feature/my-feature-name
```

### 7. Create Merge Request

- Provide clear description
- Reference any related issues
- Wait for code review

---

## 📦 Building and Releasing

### Build AppImage (Linux)

```bash
cd gui
npm install
npm run build
```

Output: `gui/dist/Taminator-*.AppImage`

### Version Bumping

```bash
# Update version in gui/package.json
# Follow semantic versioning: MAJOR.MINOR.PATCH

# Major: Breaking changes
# Minor: New features (backwards compatible)
# Patch: Bug fixes
```

### Release Checklist

- [ ] All tests passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped in package.json
- [ ] AppImage built and tested
- [ ] No debug code or test data
- [ ] Security audit passed

---

## ❓ FAQ

### Q: How do I test with customer data?

**A:** Use local test data ONLY. Never commit:
- Create `taminator-test-data/` directory (blocked by .gitignore)
- Use dummy customer names: "example-customer", "test-bank"
- Use fake case numbers: "case_99999999"

### Q: I need to test with real tokens

**A:** Store in environment variables or keyring:
```bash
# Never in code
export JIRA_TOKEN="your-token"

# Or use keyring (recommended)
# Tokens stored in system keyring, never in files
```

### Q: Pre-commit hook blocked my commit

**A:** The hook found sensitive data. Check:
```bash
git diff --cached | grep -iE "customer|token|case_"
```
Remove violations and retry.

### Q: Can I disable the pre-commit hook?

**A:** Only in emergencies:
```bash
git commit --no-verify
# But this bypasses ALL security - use with caution
```

### Q: How do I report a security issue?

**A:** Email jbyrd@redhat.com directly. Do NOT create public issues for security vulnerabilities.

---

## 📞 Getting Help

- **Issues:** Create GitLab issue
- **Security:** Email jbyrd@redhat.com
- **Questions:** Ask in #tam-automation Slack channel

---

## 📄 License

Internal Red Hat tool - see repository for license details.

---

**Thank you for contributing to Taminator!**

Remember: Production quality, security first, TAMs depend on this tool.

