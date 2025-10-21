# Taminator Redesign - Implementation & Deployment Plan

**Date:** October 21, 2025  
**Scope:** Limited deployment to 2 environments  
**Status:** Ready to implement

---

## Deployment Targets

### Target 1: Laptop (Primary Development)
- **Host:** jbyrd@localhost (Fedora 42)
- **Path:** `/home/jbyrd/pai/automation/rfe-bug-tracker/`
- **Purpose:** Primary development and testing environment
- **User:** Jimmy Byrd (developer/TAM)

### Target 2: AlmaLinux 9 VM (Testing)
- **Host:** testuser@192.168.122.220 (rfe-test-alma9-local)
- **Path:** `/home/testuser/taminator/`
- **Purpose:** Clean testing environment, deployment validation
- **VPN:** Red Hat VPN configured
- **Snapshot:** vpn-configured-20251021-090843

**Deployment Strategy:**
- Develop on laptop
- Deploy to VM for testing
- Validate both environments before wider rollout

---

## Implementation Order

### Phase 1: Core Infrastructure (Week 1-2)
**Priority: Critical**

#### 1.1: Auth-Box Module
- **Location:** `src/taminator/core/auth_box.py`
- **Components:**
  - TokenManager (API tokens)
  - VPN detector
  - Kerberos checker
  - SSH key validator
  - Pre-flight checks
  - Auth audit submodule

**Implementation:**
```bash
# On laptop
cd ~/pai/automation/rfe-bug-tracker/
mkdir -p src/taminator/core/
touch src/taminator/core/auth_box.py
touch src/taminator/core/auth_audit.py
touch src/taminator/core/auth_types.py
```

**Test:**
```bash
# Test on laptop first
pytest tests/test_auth_box.py

# Deploy to VM
ansible-playbook playbooks/deploy-to-vm.yml --tags auth-box

# Test on VM
ssh testuser@192.168.122.220 'cd ~/taminator && pytest tests/test_auth_box.py'
```

#### 1.2: CLI Command Consolidation
- **Current:** 13 bash scripts
- **New:** 5 Python commands with subcommands

**New Command Structure:**
```
tam-rfe check <customer>      # Replaces: tam-rfe-monitor, tam-rfe-verify
tam-rfe update <customer>     # New functionality
tam-rfe post <customer>       # Replaces: tam-rfe-monitor (posting)
tam-rfe onboard <customer>    # Replaces: tam-rfe-onboard, tam-rfe-onboard-intelligent
tam-rfe config                # Replaces: tam-rfe-verify, tam-rfe-api-test, tam-rfe-chat
```

**Implementation:**
```bash
# Create new command structure
mkdir -p src/taminator/commands/
touch src/taminator/commands/check.py
touch src/taminator/commands/update.py
touch src/taminator/commands/post.py
touch src/taminator/commands/onboard.py
touch src/taminator/commands/config.py
```

### Phase 2: Core Commands (Week 2-3)

#### 2.1: tam-rfe check (Priority 1)
**What it does:** Compare report statuses with current JIRA

**Implementation:**
```python
# src/taminator/commands/check.py
from rich.console import Console
from rich.table import Table
from taminator.core.auth_box import auth_required, AuthType

console = Console()

@auth_required([AuthType.VPN, AuthType.JIRA_TOKEN])
def check_customer(customer: str, options: dict):
    """Check if customer RFE report is up-to-date."""
    # Find report file
    report_path = find_customer_report(customer)
    
    # Extract JIRA IDs from report
    jira_ids = extract_jira_ids(report_path)
    
    # Fetch current statuses from JIRA
    current_statuses = fetch_jira_statuses(jira_ids)
    
    # Compare with report
    results = compare_statuses(report_path, current_statuses)
    
    # Display beautiful table
    display_results_table(results)
```

**Test Data:**
```python
# Create test customer for development
TEST_CUSTOMER = {
    'name': 'testcustomer',
    'jira_ids': ['AAPRFE-999', 'AAPRFE-998', 'AAP-99999'],
    'report_path': '~/taminator-test-data/testcustomer.md'
}
```

**Deploy:**
```bash
# Laptop testing
tam-rfe check testcustomer --test-data

# Deploy to VM
ansible-playbook playbooks/deploy-to-vm.yml --tags check-command

# VM testing
ssh testuser@192.168.122.220 'tam-rfe check testcustomer --test-data'
```

#### 2.2: tam-rfe onboard (Priority 2)
**What it does:** Onboarding wizard with mandatory token validation

**Implementation:** 5-step wizard with Rich TUI

**Deploy:** Same pattern as check command

#### 2.3: tam-rfe update (Priority 3)
**What it does:** Auto-update reports with current statuses

**Deploy:** Same pattern

### Phase 3: Testing & Validation (Week 3-4)

#### 3.1: Laptop Testing Checklist
- [ ] Auth-Box detects VPN status correctly
- [ ] Auth-Box validates JIRA token
- [ ] tam-rfe check works with test data
- [ ] tam-rfe onboard wizard completes successfully
- [ ] All commands show beautiful Rich output
- [ ] Error messages are clear and actionable

#### 3.2: VM Testing Checklist
- [ ] Fresh install works (no laptop dependencies)
- [ ] VPN detection works on AlmaLinux 9
- [ ] All commands work same as laptop
- [ ] Test data creates correctly
- [ ] No hardcoded laptop paths

### Phase 4: GUI (Optional - Week 5-8)
**Status:** Deferred until CLI redesign is stable

---

## Deployment Automation

### Ansible Playbook: Deploy to Both Environments

**File:** `ansible/deploy-redesign.yml`

```yaml
---
- name: Deploy Taminator Redesign
  hosts: all
  vars:
    taminator_version: "2.0.0-alpha"
    test_data_enabled: true
  
  tasks:
    - name: Create directory structure
      file:
        path: "{{ item }}"
        state: directory
        mode: '0755'
      loop:
        - "~/taminator/src/taminator/core"
        - "~/taminator/src/taminator/commands"
        - "~/taminator/tests"
        - "~/taminator-test-data"
    
    - name: Copy source files
      synchronize:
        src: "{{ playbook_dir }}/../src/"
        dest: "~/taminator/src/"
        recursive: yes
        delete: yes
    
    - name: Install Python dependencies
      pip:
        requirements: "~/taminator/requirements.txt"
        state: present
        executable: pip3
        extra_args: --user
    
    - name: Install taminator in development mode
      command: pip3 install -e ~/taminator
      args:
        creates: ~/.local/bin/tam-rfe
    
    - name: Create test customer data
      copy:
        dest: "~/taminator-test-data/testcustomer.md"
        content: |
          # Test Customer RFE/Bug Tracker
          
          | JIRA ID | Status |
          |---------|--------|
          | AAPRFE-999 | Backlog |
          | AAPRFE-998 | Review |
          | AAP-99999 | New |
      when: test_data_enabled
    
    - name: Verify installation
      command: tam-rfe --version
      register: version_check
      changed_when: false
    
    - name: Display installation result
      debug:
        msg: "Taminator {{ taminator_version }} installed successfully"
```

**Inventory:** `ansible/inventory.ini`

```ini
[taminator_dev]
localhost ansible_connection=local

[taminator_test]
192.168.122.220 ansible_user=testuser ansible_python_interpreter=/usr/bin/python3
```

**Deploy Commands:**

```bash
# Deploy to laptop only
ansible-playbook ansible/deploy-redesign.yml --limit localhost

# Deploy to VM only
ansible-playbook ansible/deploy-redesign.yml --limit 192.168.122.220

# Deploy to both
ansible-playbook ansible/deploy-redesign.yml

# Deploy specific component
ansible-playbook ansible/deploy-redesign.yml --tags auth-box
ansible-playbook ansible/deploy-redesign.yml --tags check-command
```

---

## Development Workflow

### Daily Development Cycle

```bash
# Morning: Start on laptop
cd ~/pai/automation/rfe-bug-tracker/

# Make changes
vim src/taminator/commands/check.py

# Test locally
pytest tests/
tam-rfe check testcustomer

# Commit changes
git add .
git commit -m "feat: implement tam-rfe check command"

# Deploy to VM for integration testing
ansible-playbook ansible/deploy-redesign.yml --limit 192.168.122.220

# SSH to VM and test
ssh testuser@192.168.122.220
tam-rfe check testcustomer
exit

# If all good, push to Git
git push origin rfe-redesign-v2
```

---

## Testing Strategy

### Test Pyramid

```
            ┌─────────────┐
            │  GUI Tests  │  (Future)
            │   (E2E)     │
            └─────────────┘
         ┌─────────────────┐
         │ Integration     │  (VM testing)
         │ Tests           │
         └─────────────────┘
      ┌─────────────────────┐
      │   Unit Tests        │  (Laptop)
      │   (pytest)          │
      └─────────────────────┘
```

**Laptop:** Fast unit tests  
**VM:** Integration tests with real environment  
**Future:** GUI E2E tests

### Test Data Management

**Location:** `~/taminator-test-data/`

**Test Customers:**
```yaml
testcustomer:
  name: "Test Customer"
  account: "999999"
  jira_ids:
    - AAPRFE-999
    - AAPRFE-998
    - AAP-99999
  report: testcustomer.md

testcustomer2:
  name: "Test Customer 2"
  account: "999998"
  jira_ids:
    - AAPRFE-997
  report: testcustomer2.md
```

---

## Rollback Plan

### If Implementation Fails

**Laptop:**
```bash
# Old commands still available
cd ~/pai/automation/rfe-bug-tracker/
git checkout main  # Roll back to old version
```

**VM:**
```bash
# Revert to snapshot
sudo virsh snapshot-revert rfe-test-alma9-local vpn-configured-20251021-090843
```

---

## Success Criteria

### Phase 1 Complete:
- ✅ Auth-Box works on both laptop and VM
- ✅ VPN detection works
- ✅ Token management works
- ✅ Pre-flight checks work

### Phase 2 Complete:
- ✅ tam-rfe check works with test data
- ✅ tam-rfe onboard completes successfully
- ✅ Beautiful Rich output on both environments
- ✅ All tests pass on laptop and VM

### Phase 3 Complete:
- ✅ All features work identically on laptop and VM
- ✅ No environment-specific bugs
- ✅ Test data creates correctly
- ✅ Documentation complete

### Ready for Wider Rollout:
- ✅ Stable for 1 week on laptop and VM
- ✅ Zero critical bugs
- ✅ Performance acceptable
- ✅ User feedback positive (your testing)

---

## Timeline

### Week 1: Auth-Box + Infrastructure
- Day 1-2: Auth-Box implementation (laptop)
- Day 3-4: Test on VM
- Day 5: Fix issues, stabilize

### Week 2: Core Commands
- Day 1-2: tam-rfe check (laptop)
- Day 3: Test on VM
- Day 4-5: tam-rfe onboard (laptop + VM)

### Week 3: Remaining Commands + Testing
- Day 1-2: tam-rfe update, tam-rfe config
- Day 3-5: Integration testing, bug fixes

### Week 4: Stabilization
- Day 1-3: Bug fixes based on testing
- Day 4-5: Documentation, final validation

---

## Next Immediate Steps

1. **Create development branch**
   ```bash
   cd ~/pai/automation/rfe-bug-tracker/
   git checkout -b rfe-redesign-v2
   ```

2. **Set up directory structure**
   ```bash
   mkdir -p src/taminator/{core,commands,tests}
   ```

3. **Create requirements.txt**
   ```bash
   cat > requirements.txt << EOF
   rich>=13.0.0
   requests>=2.31.0
   jinja2>=3.1.0
   pyyaml>=6.0
   keyring>=24.0.0
   pytest>=7.4.0
   EOF
   ```

4. **Start with Auth-Box**
   - Implement TokenManager
   - Implement VPN detector
   - Write tests
   - Deploy to VM

**Ready to start implementation?**

---

**Bottom Line:** Implement redesign on laptop first, continuously deploy to VM for testing, keep both environments in sync. Only these 2 targets for now.

