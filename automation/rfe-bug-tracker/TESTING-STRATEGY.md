# Taminator Testing Strategy

**Approach:** Hybrid testing combining real user testing and automated simulations

---

## 🎯 Testing Philosophy

Taminator uses a **hybrid testing approach** that balances:
- **Real testing** by the user (Jimmy) for UX-critical features
- **Simulated testing** for automation, unit tests, and repeatable checks

---

## 👤 Real Testing (User-Driven)

### What Requires Real Testing

**1. GUI Functionality**
- ✅ Window opens and renders correctly
- ✅ Navigation between views
- ✅ Button clicks and interactions
- ✅ Forms and input fields
- ✅ Real-time updates (auth status)
- ✅ Visual design and branding
- ✅ Cross-platform behavior (Linux, macOS, Windows)

**Test Method:** Launch GUI (`npm start`), manually interact, verify visually

**2. Authentication Workflows**
- ✅ VPN connection detection
- ✅ Kerberos ticket validation
- ✅ Token configuration wizard
- ✅ Pre-flight checks blocking commands
- ✅ Error messages and guidance

**Test Method:** Run commands without auth, configure auth, verify blocking/passing

**3. End-to-End Workflows**
- ✅ Complete customer onboarding flow
- ✅ Check → Update → Post sequence
- ✅ Issue reporting to GitHub
- ✅ Report generation and backup

**Test Method:** Walk through complete user journey, verify each step

**4. UX and Error Messages**
- ✅ Error messages are clear and helpful
- ✅ Progress indicators show during operations
- ✅ Confirmation prompts work as expected
- ✅ Color coding and formatting is readable

**Test Method:** Trigger errors intentionally, verify messages

---

## 🤖 Simulated Testing (Automated)

### What Can Be Simulated

**1. Unit Tests (pytest)**
```python
# test_auth_box.py
def test_vpn_detection():
    result = auth_box.check_vpn_connection()
    assert result.auth_type == AuthType.VPN
    assert isinstance(result.passed, bool)

def test_jira_client():
    client = JIRAClient("test_token")
    # Mock API response
    mock_data = {'status': 'Backlog'}
    assert client.parse_status(mock_data) == 'Backlog'
```

**2. Security Checks**
- ✅ Pre-commit hook blocks sensitive data
- ✅ .gitignore prevents staging
- ✅ Token patterns detected
- ✅ Customer names blocked

**Test Method:** 
```bash
# Simulate bad commit
echo 'TOKEN="ghp_fake123"' > test.py
git add test.py
./.git/hooks/pre-commit  # Should FAIL
```

**3. API Response Handling**
```python
# Mock JIRA API responses
def test_jira_status_fetch():
    with mock.patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'fields': {'status': {'name': 'Backlog'}}
        }
        
        result = jira_client.get_issue_status('AAPRFE-999')
        assert result['status'] == 'Backlog'
```

**4. Data Parsing**
- ✅ Extract JIRA IDs from markdown
- ✅ Parse report templates
- ✅ Compare statuses
- ✅ Generate backups

**Test Method:** Use test data files, verify parsing logic

**5. Error Handling**
```python
def test_missing_token_error():
    with pytest.raises(AuthenticationError):
        auth_box.get_token(AuthType.JIRA_TOKEN, required=True)
```

---

## 📊 Testing Matrix

| Feature | Real Test | Simulated Test | Priority |
|---------|-----------|----------------|----------|
| GUI Launch | ✅ | ❌ | High |
| VPN Detection | ✅ | ✅ | High |
| Token Config | ✅ | ✅ | High |
| JIRA API Calls | ✅ | ✅ | High |
| Report Parsing | ❌ | ✅ | Medium |
| Error Messages | ✅ | ✅ | High |
| Pre-commit Hook | ✅ | ✅ | Critical |
| Report Updates | ✅ | ✅ | High |
| GitHub Issues | ✅ | ❌ | Medium |
| Cross-platform | ✅ | ❌ | Low |

---

## 🔄 Test Workflow

### Phase 1: Development Testing (Continuous)

**While Building Features:**
1. Write unit tests first (TDD when appropriate)
2. Test locally with real data (CLI)
3. Verify with test data (`--test-data`)
4. Check GUI integration

```bash
# Example development test cycle
pytest tests/test_auth_box.py           # Unit tests
./tam-rfe check --test-data             # CLI real test
cd gui && npm start                      # GUI real test
```

### Phase 2: Feature Complete Testing

**Before Marking Feature "Done":**
1. ✅ Unit tests pass
2. ✅ Real user test (Jimmy)
3. ✅ Documentation updated
4. ✅ Error scenarios tested

### Phase 3: Release Testing

**Before Git Push:**
1. ✅ Run full test suite
2. ✅ Security checks pass
3. ✅ End-to-end workflow test
4. ✅ GUI smoke test

```bash
# Release testing checklist
pytest tests/                           # All unit tests
./.git/hooks/pre-commit                 # Security check
./tam-rfe check testcustomer            # Real workflow
cd gui && npm start                      # GUI verification
```

---

## 🧪 Test Data Management

### Simulated Test Data (Safe for Git)

**Location:** `tests/fixtures/`

```
tests/
└── fixtures/
    ├── sample_report.md          # Generic template
    ├── jira_response.json        # Mock API response
    └── test_config.yaml          # Test configuration
```

**Contents:**
- Use AAPRFE-999, AAP-99999 (test IDs)
- Use "testcustomer" (generic name)
- Use fake tokens (ghp_fake123...)

### Real Test Data (Never Commit)

**Location:** `~/.taminator-data/test-data/`

```
~/.taminator-data/
└── test-data/
    ├── testcustomer.md           # Generated at runtime
    └── testcustomer2.md          # User-created
```

**Contents:**
- Created by `./tam-rfe check --test-data`
- Can use real JIRA API
- Uses real VPN/Kerberos
- Never committed to git

---

## 📝 Test Documentation

### For Each Feature

**Required Documentation:**
1. **How to test manually**
   ```
   # Test tam-rfe check
   1. Ensure VPN connected
   2. Configure JIRA token
   3. Run: ./tam-rfe check --test-data
   4. Verify: Comparison table displays
   5. Expected: 5 issues, 4 up-to-date
   ```

2. **Automated tests**
   ```python
   # tests/test_check.py
   def test_check_command():
       # Arrange
       # Act
       # Assert
   ```

3. **Edge cases**
   ```
   - What if VPN disconnects mid-check?
   - What if JIRA API times out?
   - What if report file is corrupted?
   ```

---

## 🚨 Security Testing (Critical)

### Always Test With Real Data First

**Why:** Security checks must work with actual sensitive data patterns

**Process:**
1. Create file with real token (in test branch)
2. Try to commit
3. Verify pre-commit hook blocks it
4. Delete file, reset branch

**Example:**
```bash
# Security test procedure
git checkout -b security-test

# Create bad file
echo 'TOKEN="actual_token_here"' > test.py
git add test.py

# Try to commit (should fail)
git commit -m "test"  # ❌ MUST BE REJECTED

# Clean up
git checkout main
git branch -D security-test
```

### Simulate for CI/CD

**For automated pipelines:**
```bash
# Create test file with patterns
echo 'ghp_1234567890abcdef' > test.tmp
git add test.tmp

# Run hook
./.git/hooks/pre-commit
# Expected exit code: 1 (failure)

# Cleanup
git restore --staged test.tmp
rm test.tmp
```

---

## 🎓 Testing Best Practices

### DO:
- ✅ Test happy path AND error cases
- ✅ Use real auth for integration tests
- ✅ Mock external APIs when appropriate
- ✅ Test security features with real patterns
- ✅ Verify error messages are helpful
- ✅ Test on clean environments (VM)

### DON'T:
- ❌ Skip real testing just because unit tests pass
- ❌ Commit sensitive data for "testing purposes"
- ❌ Test only happy path
- ❌ Assume GUI works because CLI works
- ❌ Skip cross-platform testing

---

## 📈 Testing Metrics

### Coverage Goals

**Unit Test Coverage:** 70%+ for core modules
- auth_box.py: 80%
- commands/*.py: 60%
- GUI: Manual testing only

**Integration Tests:** All critical workflows
- check → update → post pipeline
- Onboarding wizard
- Issue reporting

**Security Tests:** 100% of security features
- Pre-commit hook
- .gitignore patterns
- Token detection

---

## 🔄 Continuous Testing

### During Development

```bash
# Watch mode for unit tests
pytest tests/ --watch

# Quick smoke test
./tam-rfe check --test-data

# GUI quick test
cd gui && npm start
```

### Before Each Commit

```bash
# Pre-commit checklist
pytest tests/                    # Unit tests pass
./.git/hooks/pre-commit          # Security check
git diff --cached | grep -i token  # Manual review
```

### Before Each Push

```bash
# Full validation
pytest tests/ --cov              # Coverage report
./tam-rfe check testcustomer     # Real workflow
python3 test_auth_audit.py       # Auth audit
cd gui && npm start              # GUI test
```

---

## 🎯 Success Criteria

### Feature is "Done" When:

1. ✅ **Unit tests pass** - Automated tests green
2. ✅ **Real user test passes** - Jimmy verifies manually
3. ✅ **Error handling tested** - Edge cases covered
4. ✅ **Security checked** - No sensitive data leaked
5. ✅ **Documentation updated** - Test procedures documented
6. ✅ **Cross-platform verified** - Works on target platforms

---

*Testing is not just about finding bugs - it's about building confidence that Taminator will work reliably for all TAMs.*

