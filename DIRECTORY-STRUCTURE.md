# RFE Bug Tracker Automation - Directory Structure

## Clean, Organized Repository Structure

**Last Updated:** October 16, 2025  
**Project:** `/home/jbyrd/pai/rfe-bug-tracker-automation`

---

## 📁 Main Directory (Key Docs)

All essential documentation remains in the root for easy access:

### Hydra API Documentation
- `HYDRA-PHASES-OVERVIEW.md` - Quick reference for all 3 phases
- `HYDRA-PHASES-SUMMARY.md` - Complete phase details
- `HYDRA-API-PHASE1.md` - Geographic customer discovery
- `HYDRA-API-PHASE2.md` - Organizational customer discovery  
- `HYDRA-API-INVESTIGATION.md` - Phase 3 blocker analysis
- `CUSTOMER-DISCOVERY.md` - Original discovery tool docs

### Core Guides
- `README.md` - Main project documentation
- `README-SIMPLE.md` - Simplified quick start
- `README-TAM-COMMUNITY.md` - TAM community guide
- `README-GLOBAL-INTEGRATION.md` - Global PAI integration
- `README-UPDATES.md` - Update history
- `GETTING-STARTED.md` - Quick start guide
- `INSTALLATION-GUIDE.md` - Installation instructions
- `PURPOSE.md` - Project purpose and goals

### Configuration & Architecture
- `AGENTS.md` - Hatter assistant configuration
- `GEMINI.md` - Gemini AI configuration
- `ARCHITECTURE-DIAGRAM.md` - System architecture
- `ANSIBLE-DEPLOYMENT.md` - Ansible deployment guide
- `COMMANDS.md` - Quick command reference
- `DYNAMIC-CUSTOMER-ONBOARDING-FIX.md` - Onboarding improvements
- `FABRIC-MODEL-SELECTION.md` - AI model selection
- `LITELLM-INTEGRATION.md` - LiteLLM setup

---

## 📂 Organized Subdirectories

### `bin/` - Executable Scripts (70+ tools)

TAM RFE Tools:
- `tam-rfe-chat` - Natural language case interface
- `tam-rfe-onboard-intelligent` - Smart customer onboarding
- `tam-rfe-discover-customers` - Customer discovery (original)
- `tam-rfe-discover-customers-hydra` - Geographic discovery (Phase 1)
- `tam-rfe-hydra-api` - Organizational discovery (Phase 2)
- `tam-rfe-validate-intelligence` - Configuration validation
- `tam-rfe-monitor-intelligent` - Intelligent monitoring
- And 60+ more PAI tools...

### `scripts/` - Organized Shell Scripts

```
scripts/
├── installation/
│   ├── install.sh
│   ├── install-improved.sh
│   └── install-offline.sh
├── setup/
│   ├── setup-enhanced-tam-portfolio.sh
│   └── setup-tam-portfolio.sh
├── generation/
│   ├── generate_reports.sh
│   ├── generate_reports_dynamic.sh
│   ├── generate_reports_smart.sh
│   └── build-standalone.sh
├── deployment/
│   └── deploy-with-ansible.sh
├── testing/
│   ├── test-tam-portfolio.sh
│   ├── test_dynamic_inventory.py
│   └── test_external_trackers.py
└── GIT-COMMANDS*.sh (3 files)
```

### `ansible/` - Ansible Automation

```
ansible/
├── playbooks/
│   ├── generation/
│   │   ├── generate_and_copy_reports.yml
│   │   ├── generate_bulletproof_reports.yml
│   │   ├── generate_enhanced_tam_reports.yml
│   │   └── 21 more playbooks...
│   ├── generate_rfe_reports.yml
│   ├── rfe-automation-master.yml
│   └── test_rfe_bug_tracker.yml
├── roles/
├── group_vars/
└── inventory/
```

### `config/` - Configuration Files

- `customers.conf` - Customer list (dynamically updated)
- `customer_group_ids.yaml` - Group ID mapping
- `rfe-automation-cron.txt` - Cron schedules
- `rfe-deployment-config.yaml` - Deployment config
- `weekly_troubleshooting_schedule.yaml` - Schedule config

### `src/` - Python Source Code

Core modules:
- `redhat_portal_api_client.py` - Portal API client
- `rfe_monitoring_system.py` - Monitoring system
- `rfe_verification_system.py` - Verification logic
- `ultimate_rfe_portal_system.py` - Portal integration
- And 10+ more modules...

### `templates/` - Jinja2 Templates

Report templates:
- `bulletproof_rfe_bug_report.j2`
- `enhanced_tam_portfolio_summary.j2`
- `external_tracker_summary.j2`
- And 10+ more templates...

### `docs/` - Supporting Documentation

```
docs/
├── ADVANCED-INTELLIGENCE-ROADMAP.md
├── AMAZING-ONBOARDING-TOOLS.md
├── ANSIBLE-BEST-PRACTICES-GUIDE.md
├── API-CONFIGURATION-GUIDE.md
├── BRAND-NEW-TAM-GUIDE.md
├── INTELLIGENCE-ENGINE-TESTING.md
├── PREREQUISITES-GUIDE.md
├── tam-deployment/ (deployment guides)
└── And 15+ more guides...
```

### `archive/` - Historical Files

```
archive/
├── merge-requests/
│   ├── MERGE-REQUEST-AUTOMATED-INSTALLER.md
│   ├── MERGE-REQUEST-README-UPDATE.md
│   ├── MERGE-REQUEST-SUBMODULE-FIX.md
│   └── MERGE-REQUEST-SUMMARY.md
├── issue-responses/
│   ├── ISSUE-RESPONSE-DAVE.md
│   ├── DAVE-ISSUE-DEEP-DIVE.md
│   └── 5 more issue docs...
├── TESTING-PLAN.md
├── TESTING-SUMMARY.md
├── INSTALLATION-TESTING-PLAN.md
└── And 10+ archived docs...
```

### `tests/` - Test Infrastructure

```
tests/
├── molecule/ (Molecule testing)
├── .vagrant/ (Vagrant VMs)
├── TESTING-GUIDE.md
├── VM-TESTING-GUIDE.md
├── VAGRANT-SETUP.md
├── test-installation.sh
└── Various test scripts...
```

### `tools/` - Tool Documentation

Documentation for 60+ PAI tools:
- `pai-case-processor.md`
- `pai-email-processor.md`
- `pai-hydra.md`
- `rhcase.md`
- And 50+ more tool docs...

### `workflows/` - Workflow Documentation

- `customer-onboarding.md`
- `tsr-production-workflow.md`
- `complete-tsr-replicable-process.md`
- And more workflow guides...

### Other Key Directories

- `contexts/` - Persona/context configurations
- `examples/` - Usage examples
- `inventory/` - Ansible inventory files
- `persona/` - TAM automation personas
- `vars/` - Ansible variables
- `rhcase/` - rhcase submodule (case management)

---

## 📊 Structure Summary

| Directory | Purpose | File Count |
|-----------|---------|------------|
| **Main Dir** | Key docs, installers | 36 files |
| **bin/** | Executable tools | 70+ scripts |
| **scripts/** | Organized shell scripts | 14 scripts |
| **ansible/** | Automation playbooks | 30+ playbooks |
| **config/** | Configuration files | 7 configs |
| **src/** | Python source | 15+ modules |
| **templates/** | Jinja2 templates | 15+ templates |
| **docs/** | Supporting guides | 20+ docs |
| **archive/** | Historical files | 21 archived |
| **tests/** | Test infrastructure | 15+ test files |
| **tools/** | Tool documentation | 60+ docs |

---

## 🎯 Key Improvements

### Before Reorganization
❌ 60+ files cluttering root directory  
❌ Scripts scattered everywhere  
❌ Playbooks mixed with docs  
❌ No logical grouping  
❌ Hard to find files  

### After Reorganization
✅ 36 essential files in root (all key docs)  
✅ Scripts organized by purpose  
✅ Playbooks grouped in ansible/playbooks/  
✅ Clear logical structure  
✅ Easy navigation  
✅ Historical files preserved in archive/  

---

## 🔍 Quick Navigation

**Need to find:**
- Hydra API docs? → Main directory (`HYDRA-*.md`)
- Installation scripts? → `scripts/installation/`
- Generate playbooks? → `ansible/playbooks/generation/`
- TAM tools? → `bin/tam-rfe-*`
- Test scripts? → `scripts/testing/`
- Old merge requests? → `archive/merge-requests/`
- Tool documentation? → `tools/`

---

## 📝 Notes

- All Hydra API documentation kept in main directory for visibility
- Core guides (README, GETTING-STARTED, etc.) easily accessible in root
- Scripts organized by function (installation, setup, generation, etc.)
- Archive preserves all historical files without cluttering main dir
- Generated output/ and logs/ added to .gitignore

**Result:** Clean, logical structure that's easy to navigate while preserving all important documentation in the main directory.
