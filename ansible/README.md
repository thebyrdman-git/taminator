# PAI Ansible Infrastructure

**Philosophy:** Build on Giants' Shoulders

**Principle:** Use Jeff Geerling's proven roles (80%) + our business logic (20%)

---

## Quick Start

### 1. Install Dependencies

```bash
# Install Geerling's roles + collections
ansible-galaxy install -r requirements.yml
ansible-galaxy collection install -r requirements.yml
```

### 2. Deploy miraclemax

```bash
# Test connection first
ansible miraclemax -i inventory/hosts.yml -m ping

# Dry run
ansible-playbook playbooks/miraclemax.yml --check

# Deploy
ansible-playbook playbooks/miraclemax.yml
```

### 3. Install RFE Tool

```bash
# Local installation
ansible-playbook playbooks/rfe-install.yml
```

---

## Structure

```
ansible/
├── requirements.yml          # Geerling's proven roles
├── inventory/
│   └── hosts.yml            # miraclemax + localhost
├── group_vars/
│   └── all.yml              # Global configuration
├── host_vars/
│   └── miraclemax.yml       # miraclemax-specific config
├── playbooks/
│   ├── miraclemax.yml       # Infrastructure deployment
│   └── rfe-install.yml      # RFE tool installation
└── roles/
    ├── miraclemax_services/ # Service deployment (our logic)
    └── rfe_install/         # RFE setup (our logic)
```

---

## Philosophy

### What Geerling's Roles Handle (80%)
- ✅ Docker/Podman installation
- ✅ System hardening
- ✅ Firewall configuration
- ✅ Python/pip setup
- ✅ Git installation
- ✅ Cross-platform compatibility (macOS/Linux)

### What We Handle (20%)
- 🎯 Service definitions (miraclemax)
- 🎯 RFE tool configuration
- 🎯 Customer onboarding logic
- 🎯 Business-specific workflows

**Result:** Faster development, fewer bugs, proven foundation

---

## Roles

### Proven Roles (Geerling)

| Role | Purpose | Version |
|------|---------|---------|
| `geerlingguy.docker` | Container runtime | 7.4.1 |
| `geerlingguy.security` | System hardening | 3.2.0 |
| `geerlingguy.firewall` | Firewall config | 3.2.1 |
| `geerlingguy.pip` | Python packages | 3.0.0 |
| `geerlingguy.git` | Git installation | 3.2.0 |
| `geerlingguy.homebrew` | macOS packages | 4.2.1 |

### Custom Roles (Our Business Logic)

| Role | Purpose | Lines of Code |
|------|---------|---------------|
| `miraclemax_services` | Deploy Podman services | ~150 |
| `rfe_install` | Install RFE tools | ~100 |

**Total Custom Code:** ~250 lines  
**Total Proven Code:** ~50,000 lines (in dependencies)  
**Ratio:** 0.5% custom, 99.5% proven ✅

---

## Configuration

### Global Variables (`group_vars/all.yml`)

```yaml
pai_user: jbyrd
pai_email: jimmykbyrd@gmail.com
rfe_repo_url: https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation.git
python_version: "3.11"
```

### Host Variables (`host_vars/miraclemax.yml`)

```yaml
miraclemax_services:
  - name: actual-budget
    port: 5006
    subdomain: money
  - name: n8n
    port: 5678
    subdomain: n8n
  # ... more services
```

---

## Usage Examples

### Deploy Specific Service

```bash
# Deploy only Actual Budget
ansible-playbook playbooks/miraclemax.yml --tags=actual-budget
```

### Update Configuration

```bash
# Edit config
vim host_vars/miraclemax.yml

# Apply changes
ansible-playbook playbooks/miraclemax.yml
```

### Install RFE Tool on Remote Host

```bash
# Edit inventory to add remote host
vim inventory/hosts.yml

# Install
ansible-playbook -i inventory/hosts.yml playbooks/rfe-install.yml -l remote-host
```

---

## Maintenance

### Update Geerling's Roles

```bash
# Update to latest versions
ansible-galaxy install -r requirements.yml --force

# Test before deploying
ansible-playbook playbooks/miraclemax.yml --check
```

**Frequency:** Monthly (Geerling maintains, we just update)

### Update Our Roles

```bash
# Edit role
vim roles/miraclemax_services/tasks/main.yml

# Test
ansible-playbook playbooks/miraclemax.yml --check

# Deploy
ansible-playbook playbooks/miraclemax.yml
```

**Frequency:** As needed for new features

---

## Testing

### Verify Installation

```bash
# Test miraclemax
ansible miraclemax -i inventory/hosts.yml -m command -a "podman ps"

# Test RFE tool
ansible localhost -i inventory/hosts.yml -m command -a "tam-rfe-verify --quick"
```

### Dry Run

```bash
# Always test first
ansible-playbook playbooks/miraclemax.yml --check --diff
```

---

## Troubleshooting

### Geerling's Role Failed

**Problem:** Role error from Geerling's role

**Solution:**
1. Check if role is up to date
2. Review role README: https://github.com/geerlingguy/ansible-role-*
3. Pin to known-good version in `requirements.yml`

### Custom Role Failed

**Problem:** Our role error

**Solution:**
1. Check role logs: `ansible-playbook -vvv`
2. Test manually: `ssh miraclemax 'command'`
3. Fix role in `roles/*/tasks/main.yml`

---

## Adding New Services

### Step 1: Add to Configuration

```yaml
# host_vars/miraclemax.yml
miraclemax_services:
  - name: my-new-service
    image: docker.io/myimage:latest
    port: 8080
    subdomain: myservice
    volume: myservice-data:/data:z
```

### Step 2: Create Compose Template (if needed)

```yaml
# roles/miraclemax_services/templates/my-new-service.yml.j2
version: '3'
services:
  my-new-service:
    image: {{ item.image }}
    ports:
      - "{{ item.port }}:{{ item.port }}"
    volumes:
      - {{ item.volume }}
```

### Step 3: Deploy

```bash
ansible-playbook playbooks/miraclemax.yml
```

**That's it!** Geerling handles all the infrastructure.

---

## Best Practices

### 1. Use Proven Roles First
Before writing custom tasks, check if Geerling has a role for it.

### 2. Keep Custom Roles Focused
- Each role should do ONE thing
- Business logic only, no infrastructure

### 3. Configuration Over Code
- Use variables in `group_vars`/`host_vars`
- Avoid hardcoding in roles

### 4. Test Before Deploying
- Always run `--check` first
- Test in container/VM before production

### 5. Pin Versions
- Pin Geerling's roles to specific versions
- Update deliberately, not automatically

---

## Resources

- **Philosophy:** `~/pai/docs/TOOL-DEVELOPMENT-PHILOSOPHY.md`
- **Geerling's Roles:** https://github.com/geerlingguy
- **Ansible Docs:** https://docs.ansible.com/
- **Pre-Dev Checklist:** `pai-dev-checklist "feature"`

---

## Migration from Manual Deployment

### Before (Manual)
```bash
# 50 lines of bash
# OS detection
# Package installation
# Service configuration
# Error-prone, platform-specific
```

### After (Ansible)
```yaml
# 5 lines of YAML
roles:
  - geerlingguy.docker  # Handles everything
  - miraclemax_services # Our logic only
```

**Result:** 90% less code, 100% more reliable

---

*Last Updated: October 17, 2025*  
*Philosophy: Build on Giants' Shoulders*  
*Inspired by: Jeff Geerling's proven roles*
