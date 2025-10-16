# MiracleMax GitOps Deployment Guide
## Infrastructure as Code - Git as Single Source of Truth

**Version:** 1.0 | **Date:** October 2025 | **Status:** Production Ready

---

## 🎯 Overview

MiracleMax now implements **GitOps methodology**: all infrastructure configuration is version-controlled in Git, and deployments happen automatically from the repository. This provides version control, rollback capability, and infrastructure reproducibility.

---

## 📦 What is GitOps?

GitOps is a way of managing infrastructure where:
1. **Git is the single source of truth** for infrastructure configuration
2. **All changes go through Git** (commits, pull requests, reviews)
3. **Deployments are automated** from Git repository
4. **Infrastructure matches Git state** at all times
5. **Rollbacks are git revert** commands

---

## 🏗️ Repository Structure

```
pai-infrastructure-automation/
├── miraclemax/
│   ├── compose/              # Docker/Podman compose files
│   │   ├── traefik.yml
│   │   ├── grafana.yml
│   │   ├── homeassistant.yml
│   │   ├── n8n.yml
│   │   └── ... (14+ services)
│   ├── config/               # Service configurations
│   │   ├── traefik/
│   │   ├── prometheus/
│   │   ├── alertmanager/
│   │   └── ...
│   ├── docs/                 # Documentation
│   └── scripts/              # Helper scripts
├── miraclemax-deploy.yml     # Ansible playbook
├── inventory/
│   └── miraclemax.yml        # Target host inventory
└── README.md
```

---

## 🚀 Deployment Commands

### Standard Deployment

```bash
# Deploy latest from Git
pai-miraclemax-deploy

# Dry-run (check what would change)
pai-miraclemax-deploy --check

# Show differences
pai-miraclemax-deploy --diff

# Deploy and restart services
pai-miraclemax-deploy --restart
```

### Validation

```bash
# Validate before deploying
pai-miraclemax-validate

# Strict mode (warnings = errors)
pai-miraclemax-validate --strict

# CI/CD mode (JSON output)
pai-miraclemax-validate --json --ci
```

---

## 📋 Deployment Workflow

### 1. Make Changes Locally

```bash
cd ~/pai/repositories/pai-infrastructure-automation/miraclemax

# Edit compose file
vim compose/grafana.yml

# Or edit config
vim config/prometheus/rules/miraclemax.yml
```

### 2. Validate Changes

```bash
# Validate configuration
pai-miraclemax-validate

# Check what would be deployed
pai-miraclemax-deploy --check --diff
```

### 3. Commit to Git

```bash
git add compose/grafana.yml
git commit -m "feat: update Grafana to version 10.3.0"
```

### 4. Deploy

```bash
# Deploy to MiracleMax
pai-miraclemax-deploy

# Or deploy and restart
pai-miraclemax-deploy --restart
```

### 5. Verify

```bash
# Check services
ssh jbyrd@192.168.1.34 'podman ps'

# Check specific service
ssh jbyrd@192.168.1.34 'podman logs grafana'

# Test endpoint
curl http://192.168.1.34:3001
```

---

## 🔄 Common Operations

### Update a Service Version

```bash
# 1. Edit compose file
vim ~/pai/repositories/pai-infrastructure-automation/miraclemax/compose/grafana.yml
# Change: image: grafana/grafana:10.2.3 → 10.3.0

# 2. Validate
pai-miraclemax-validate

# 3. Commit
git add compose/grafana.yml
git commit -m "feat(grafana): upgrade to 10.3.0"

# 4. Deploy
pai-miraclemax-deploy

# 5. Restart service
ssh jbyrd@192.168.1.34 'cd ~/miraclemax-infrastructure/compose && podman-compose -f grafana.yml restart'
```

### Add New Service

```bash
# 1. Create compose file
cat > ~/pai/repositories/pai-infrastructure-automation/miraclemax/compose/new-service.yml <<EOF
version: '3.8'
services:
  new-service:
    image: example/service:latest
    ...
EOF

# 2. Validate
pai-miraclemax-validate

# 3. Commit
git add compose/new-service.yml
git commit -m "feat: add new-service"

# 4. Deploy
pai-miraclemax-deploy

# 5. Start service
ssh jbyrd@192.168.1.34 'cd ~/miraclemax-infrastructure/compose && podman-compose -f new-service.yml up -d'
```

### Update Prometheus Rules

```bash
# 1. Edit rules
vim ~/pai/repositories/pai-infrastructure-automation/miraclemax/config/prometheus/rules/miraclemax.yml

# 2. Validate (if promtool installed)
promtool check rules miraclemax/config/prometheus/rules/miraclemax.yml

# 3. Commit
git add config/prometheus/rules/miraclemax.yml
git commit -m "feat(prometheus): add new backup alert rules"

# 4. Deploy
pai-miraclemax-deploy

# 5. Reload Prometheus
ssh jbyrd@192.168.1.34 'podman exec prometheus kill -HUP 1'
```

### Rollback a Change

```bash
# 1. Find commit to roll back to
git log --oneline -10

# 2. Revert the change
git revert <commit-hash>

# 3. Deploy
pai-miraclemax-deploy
```

---

## 🎯 GitOps Principles

### Single Source of Truth

- **All configuration** is in Git
- **No manual edits** on MiracleMax directly
- **Changes flow** through Git → Deployment

### Declarative Configuration

- Compose files **declare desired state**
- Ansible ensures **state matches declaration**
- No imperative "run this command" scripts

### Automated Deployment

- `pai-miraclemax-deploy` syncs Git → MiracleMax
- Can be triggered by CI/CD on git push
- Idempotent: safe to run multiple times

### Version Control Everything

- Infrastructure changes are **commits**
- Can review via **git diff**
- Can rollback via **git revert**
- **Audit trail** of all changes

---

## 🔒 Security Considerations

### Secrets Management

**❌ DO NOT** commit secrets to Git:
- Passwords
- API keys
- Private keys
- OAuth tokens

**✅ DO** use:
- Environment variables
- Secrets files (not in Git, added to .gitignore)
- External secrets management (Vault, etc.)

**Example:**
```yaml
# ❌ BAD - hardcoded password
environment:
  - DB_PASSWORD=supersecret123

# ✅ GOOD - reference to external secret
environment:
  - DB_PASSWORD_FILE=/run/secrets/db_password
```

### .gitignore

```gitignore
# Secrets
config/*/secrets/
*.key
*.pem
*.p12

# Logs
*.log
logs/

# Backup files
*.bak
*~
```

---

## 📊 Ansible Playbook Details

### What It Does

1. **Backs up** existing infrastructure (timestamped)
2. **Syncs** files from Git to MiracleMax
3. **Validates** compose files
4. **Initializes Git** on MiracleMax (if needed)
5. **Sets ownership** correctly
6. **Verifies** services running

### Idempotency

Safe to run multiple times:
- Only changes what's different
- Doesn't restart services automatically
- Creates backup before changes

### Variables

Defined in `inventory/miraclemax.yml`:
```yaml
ansible_host: 192.168.1.34
ansible_user: jbyrd
miraclemax_infrastructure_path: /home/jbyrd/miraclemax-infrastructure
```

---

## 🎯 CI/CD Integration

### GitHub Actions Example

```yaml
name: Deploy MiracleMax
on:
  push:
    branches: [main]
    paths:
      - 'miraclemax/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Validate
        run: pai-miraclemax-validate --strict --ci
      
      - name: Deploy
        run: pai-miraclemax-deploy
        if: github.ref == 'refs/heads/main'
```

### GitLab CI Example

```yaml
validate:
  stage: test
  script:
    - pai-miraclemax-validate --strict --ci
  only:
    - merge_requests

deploy:
  stage: deploy
  script:
    - pai-miraclemax-deploy
  only:
    - main
  when: manual
```

---

## 🎯 Troubleshooting

### Deployment Failed

```bash
# Check Ansible logs
cat ~/.local/share/pai/logs/miraclemax-deploy.log

# Run with verbose mode
pai-miraclemax-deploy --verbose

# Check what changed
pai-miraclemax-deploy --diff --check
```

### Service Won't Start

```bash
# Check container logs
ssh jbyrd@192.168.1.34 'podman logs <service>'

# Validate compose file
podman-compose -f ~/pai/repositories/pai-infrastructure-automation/miraclemax/compose/<service>.yml config

# Check for port conflicts
ss -tulpn | grep <port>
```

### Config Drift

```bash
# Check Git status on MiracleMax
ssh jbyrd@192.168.1.34 'cd ~/miraclemax-infrastructure && git status'

# Re-deploy from Git (overwrites drift)
pai-miraclemax-deploy

# Or pull changes if they should be kept
ssh jbyrd@192.168.1.34 'cd ~/miraclemax-infrastructure && git pull'
```

---

## 📊 Before vs After GitOps

| Aspect | Before | After |
|--------|--------|-------|
| **Changes** | SSH + manual edits | Git commit + deploy |
| **History** | No audit trail | Full Git history |
| **Rollback** | Recreate from memory | `git revert` + deploy |
| **Validation** | Manual testing | Automated validation |
| **Reproducibility** | Impossible | Clone + deploy |
| **Collaboration** | Screen sharing | Pull requests |
| **Documentation** | Scattered notes | Self-documenting code |

---

## 🎯 Best Practices

### 1. Commit Often, Deploy Carefully

- **Commit** every logical change
- **Validate** before deploying
- **Deploy** during low-traffic times
- **Monitor** after deployment

### 2. Write Good Commit Messages

```bash
# ✅ GOOD
git commit -m "feat(grafana): upgrade to 10.3.0 for security fix CVE-2024-1234"

# ❌ BAD
git commit -m "update stuff"
```

### 3. Use Branches for Big Changes

```bash
# Create feature branch
git checkout -b feature/new-monitoring-stack

# Make changes, test
pai-miraclemax-deploy --check

# Merge when ready
git checkout main
git merge feature/new-monitoring-stack
```

### 4. Always Validate First

```bash
# Every time before deploying
pai-miraclemax-validate && pai-miraclemax-deploy
```

### 5. Keep Backups

- Ansible automatically backs up before deployment
- Manual backups: `ssh jbyrd@192.168.1.34 'tar czf ~/backup-$(date +%Y%m%d).tar.gz ~/miraclemax-infrastructure'`
- Regular offsite backups via `pai-miraclemax-backup`

---

## 🎯 Next Steps

### Immediate
1. ✅ GitOps system deployed
2. Practice: Make a small change and deploy
3. Set up branch protection in Git

### This Month
4. Add pre-commit hooks for validation
5. Set up CI/CD pipeline
6. Document service-specific procedures

### Long Term
7. Implement automated testing
8. Add staging environment
9. Explore Kubernetes/GitOps operators

---

## 📚 Additional Resources

- [GitOps Principles](https://www.gitops.tech/)
- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)
- [Infrastructure as Code](https://www.oreilly.com/library/view/infrastructure-as-code/9781491924357/)

---

*MiracleMax GitOps - Infrastructure as Code for the Modern Era*  
*Confidential - Internal Technical Documentation*

