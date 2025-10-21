# Taminator Deployment Architecture

**Goal:** Clean separation between application code (safe to commit) and user data (never commit)

---

## 🏗️ Directory Structure

### Inside Git Repository (Safe to Commit)
```
taminator/                          # Git repository root
├── .git/
│   └── hooks/
│       └── pre-commit              # ✅ Auto-blocks sensitive data
├── .gitignore                      # ✅ Excludes user data
├── src/taminator/                  # ✅ Application code
│   ├── core/                       # ✅ Auth-Box, audit
│   └── commands/                   # ✅ CLI commands
├── gui/                            # ✅ Electron GUI
├── docs/                           # ✅ Documentation
├── requirements.txt                # ✅ Python dependencies
├── tam-rfe                         # ✅ CLI entry point
└── README.md                       # ✅ Setup instructions
```

### Outside Git Repository (User Data - Never Commit)
```
~/.taminator-data/                  # ❌ User data directory (NOT in git)
├── customers/                      # ❌ Customer reports
│   ├── tdbank.md
│   ├── wellsfargo.md
│   └── fanniemae.md
├── test-data/                      # ❌ Test customer data
│   └── testcustomer.md
├── backups/                        # ❌ Report backups
│   ├── tdbank_backup_20251021.md
│   └── wellsfargo_backup_20251021.md
└── logs/                           # ❌ Application logs
    └── taminator.log

~/.config/taminator/                # ❌ Configuration (NOT in git)
├── config.yaml                     # ❌ User preferences
└── secrets/                        # ❌ Encrypted tokens (if not using keyring)
    └── tokens.enc

~/.local/share/taminator/           # ❌ Application data (NOT in git)
└── cache/                          # ❌ Cached JIRA responses
```

---

## 🔒 Security Layers

### Layer 1: .gitignore (Passive Protection)
Prevents accidentally staging sensitive files.

**What it blocks:**
- `taminator-test-data/`
- `customers/`
- `.env` files
- Token files
- Backup files

### Layer 2: Pre-Commit Hook (Active Protection)
**Automatically runs** before every commit to scan staged changes.

**What it blocks:**
- API tokens (ghp_*, Bearer tokens)
- Real customer names (TD Bank, Wells Fargo, etc.)
- Real JIRA IDs (AAPRFE-1 through AAPRFE-899)
- Test data directories
- Customer report files

**Result:** Commit is **REJECTED** if sensitive data detected.

### Layer 3: Data Directory Separation
User data lives **completely outside** the git repository.

**Benefits:**
- User data never enters git tracking
- Clean application updates (just git pull)
- Each user has their own data directory
- No risk of accidental commits

---

## 🚀 Clean Deployment Process

### For New Users (First-Time Setup)

1. **Clone Repository** (clean, no user data)
   ```bash
   git clone https://github.com/thebyrdman-git/taminator.git
   cd taminator
   ```

2. **Install Dependencies**
   ```bash
   # Python dependencies
   pip3 install -r requirements.txt --user
   
   # Node.js dependencies (for GUI)
   cd gui && npm install
   ```

3. **Run Setup Script** (creates user directories)
   ```bash
   ./setup.sh
   ```
   
   This creates:
   - `~/.taminator-data/` - User data directory
   - `~/.config/taminator/` - Configuration
   - Pre-commit hook installed
   - Test data template

4. **Configure Tokens**
   ```bash
   ./tam-rfe config --add-token
   ```

5. **Ready to Use!**
   ```bash
   ./tam-rfe check --test-data
   ```

### For Existing Users (Updates)

1. **Pull Latest Code**
   ```bash
   cd taminator
   git pull
   ```

2. **Update Dependencies** (if needed)
   ```bash
   pip3 install -r requirements.txt --user --upgrade
   ```

3. **User Data Untouched**
   - All customer reports: Safe in `~/.taminator-data/`
   - All tokens: Safe in keyring or `~/.config/taminator/`
   - All logs: Safe in `~/.local/share/taminator/`

---

## 📁 Path Resolution

### How Taminator Finds User Data

```python
# In code
from pathlib import Path

# User data directory
DATA_DIR = Path.home() / '.taminator-data'
CUSTOMERS_DIR = DATA_DIR / 'customers'
TEST_DATA_DIR = DATA_DIR / 'test-data'
BACKUPS_DIR = DATA_DIR / 'backups'

# Config directory
CONFIG_DIR = Path.home() / '.config' / 'taminator'

# Find customer report
def find_customer_report(customer_name):
    # Try user's customer directory first
    report = CUSTOMERS_DIR / f'{customer_name}.md'
    if report.exists():
        return report
    
    # Fall back to test data
    report = TEST_DATA_DIR / f'{customer_name}.md'
    if report.exists():
        return report
    
    return None
```

---

## 🧪 Test Data Strategy

### Included in Repository (Safe)
```
docs/examples/
└── sample-report-template.md    # ✅ Generic template
                                 # ✅ Uses placeholder text
                                 # ✅ Test JIRA IDs (999)
```

### Generated at Runtime (Not Committed)
```bash
$ ./tam-rfe check --test-data

# Creates ~/.taminator-data/test-data/testcustomer.md
# Uses generic test data
# Never committed to git
```

---

## 🔄 Migration from Old Structure

If you have data in the old location:

```bash
# Move customer reports
mv ~/taminator-test-data/* ~/.taminator-data/customers/

# Or use the migration script
./migrate-data.sh
```

---

## 👥 Multi-User Environment

Each user has their own isolated data:

```
User: alice
~/.taminator-data/customers/     # Alice's customer reports
~/.config/taminator/             # Alice's config & tokens

User: bob
~/.taminator-data/customers/     # Bob's customer reports  
~/.config/taminator/             # Bob's config & tokens
```

**Shared:**
- Application code (via git)
- Documentation

**Private:**
- Customer data
- API tokens
- Configuration

---

## 🎯 What Gets Committed vs What Doesn't

### ✅ COMMIT (Application Code)
- Source code (`src/`)
- Documentation (`docs/`, `README.md`)
- Dependencies (`requirements.txt`, `package.json`)
- CLI entry point (`tam-rfe`)
- GUI code (`gui/`)
- Tests (with mock data)
- .gitignore
- Pre-commit hook
- Templates (generic)

### ❌ NEVER COMMIT (User Data)
- Customer reports (`~/.taminator-data/customers/`)
- Test data (`~/.taminator-data/test-data/`)
- API tokens (keyring or `~/.config/taminator/secrets/`)
- Configuration (`~/.config/taminator/config.yaml`)
- Logs (`~/.local/share/taminator/logs/`)
- Backups (`~/.taminator-data/backups/`)
- Cache (`~/.local/share/taminator/cache/`)

---

## 🛡️ Security Benefits

1. **Accidental Commit Protection**
   - Pre-commit hook blocks sensitive data
   - .gitignore prevents staging
   - Data directory outside repo

2. **Clean Updates**
   - `git pull` only updates code
   - User data never affected
   - No merge conflicts with data

3. **Easy Sharing**
   - Share git URL with colleagues
   - They get clean application
   - No risk of sharing your tokens/data

4. **Audit Trail**
   - Git history only contains code changes
   - User data changes not in git
   - Compliance-friendly

---

## 📋 Deployment Checklist

Before pushing to GitHub:

```bash
# 1. Run security check
git diff --cached | grep -i "token\|tdbank\|wellsfargo"

# 2. Verify pre-commit hook is installed
ls -la .git/hooks/pre-commit

# 3. Test the hook
git commit --dry-run

# 4. Verify .gitignore is working
git status --ignored

# 5. Check what's staged
git diff --cached --name-only

# 6. Review actual changes
git diff --cached
```

---

## 🚀 First Public Release

When ready to make Taminator public:

1. **Final Security Audit**
   ```bash
   # Check entire repo for sensitive data
   git log --all --full-history --source --find-object=<blob>
   ```

2. **Clean .git History** (if needed)
   ```bash
   # Remove sensitive data from history
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch <file>" \
     --prune-empty --tag-name-filter cat -- --all
   ```

3. **Push to GitHub**
   ```bash
   git remote add origin https://github.com/thebyrdman-git/taminator.git
   git push -u origin main
   ```

4. **Users Clone & Setup**
   ```bash
   git clone https://github.com/thebyrdman-git/taminator.git
   cd taminator
   ./setup.sh
   ./tam-rfe config --add-token
   ```

---

## 💡 Best Practices

1. **Never edit files in the repo with real data**
   - Always work in `~/.taminator-data/`

2. **Use test data for examples**
   - `./tam-rfe check --test-data`
   - Uses testcustomer, not real customers

3. **Trust the pre-commit hook**
   - It will save you from mistakes
   - Don't override it (--no-verify)

4. **Keep data outside repo**
   - Use `~/.taminator-data/` for everything

5. **Regular security audits**
   - Run `git log -p | grep -i token` occasionally

---

*This architecture ensures Taminator can be safely open-sourced while protecting all sensitive TAM and customer data.*

