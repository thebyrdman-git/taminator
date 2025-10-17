# Release Notes

Detailed release information for the TAM RFE Bug Tracker Automation Tool.

---

## Version 1.4.1 - Bug Fix Release (October 17, 2025)

**Release Type:** Patch  
**Focus:** Critical bug fixes for cross-platform compatibility

### What's Fixed

#### Issue #12: macOS sed Compatibility
**Problem:** Customer onboarding failed on macOS with cryptic sed error  
**Impact:** Tool unusable on macOS systems  
**Solution:** Cross-platform sed implementation with explicit backup handling

#### Issue #13: Verification System Crash
**Problem:** `tam-rfe-verify --full` crashed with AttributeError  
**Impact:** Full verification unavailable, reduced confidence in system health  
**Solution:** Renamed enum to eliminate Python naming collision

#### Issue #14: False Negative Checks
**Problem:** Python 3.11+ incorrectly flagged as "too old", rhcase warnings incorrect  
**Impact:** Confusion for users, false sense of system failure  
**Solution:** Improved version detection and downgraded rhcase to warning

### Who Should Upgrade

- ✅ **macOS users** - Critical fix for you
- ✅ **Python 3.11+ users** - Eliminates false warnings
- ⚠️ **All users** - Recommended for improved reliability

### Upgrade Instructions

```bash
cd ~/rfe-bug-tracker-automation
git pull origin main
```

No configuration changes required.

---

## Version 1.4.0 - Report Scheduler & TUI (October 16, 2025)

**Release Type:** Minor  
**Focus:** Automation and user experience improvements

### What's New

#### 🖥️ Text User Interface (TUI)
New dialog-based menu system for routine TAM workflows:
- Quick access to common operations
- No command memorization needed
- Keyboard-driven navigation

**Usage:**
```bash
tam-rfe-tui
```

#### 📅 TAM RFE Report Scheduler
Automated report generation and delivery system:

**Phase 1 - Cron Scheduling:**
- YAML-based schedule configuration
- Multiple customer support
- Flexible timing (daily, weekly, monthly)

**Phase 2 - Daemon Mode:**
- Systemd service integration
- Automatic execution
- Email delivery to stakeholders

**Phase 3 - Advanced Features:**
- Schedule validation
- Timezone support
- Conflict detection
- Health monitoring

**Setup:**
```bash
tam-rfe-tool-report-scheduler
# or
active-case-report-scheduler
```

#### 🔐 Red Hat VPN Intelligence
Automatic detection and configuration:
- Kerberos ticket validation
- CA certificate installation
- NetworkManager VPN profiles
- Multi-distribution support

#### 📦 Dynamic COPR Repository Detection
Automatic repository configuration for:
- EPEL 8, 9, 10
- Fedora 40, 41, 42, 43, rawhide
- Detects "Active Releases" dynamically

### Breaking Changes

None. All new features are opt-in.

### Migration Guide

#### Enable Report Scheduler
```bash
# Configure schedules
tam-rfe-tool-report-scheduler

# Enable systemd service
sudo systemctl enable tam-rfe-scheduler
sudo systemctl start tam-rfe-scheduler
```

#### Try the TUI
```bash
tam-rfe-tui
```

No configuration changes required for existing workflows.

---

## Version 1.3.0 - Hydra API & Customer Discovery (October 16, 2025)

**Release Type:** Minor  
**Focus:** Enterprise scalability via intelligent customer discovery

### What's New

#### 🌐 Hydra API Integration - Phase 1
Geographic customer discovery via Red Hat network:
```bash
tam-rfe-discover-customers-hydra
```

Features:
- Automatic TAM assignment detection
- Geographic organization mapping
- Case data correlation

#### 🏢 Hydra API Integration - Phase 2
Organizational customer discovery:
```bash
tam-rfe-hydra-api "North American Public Sector"
```

Features:
- Organization-based discovery
- Intelligent heuristics
- Backend via rhcase for data security

#### 🔍 Intelligence Validation Framework
Comprehensive validation tooling:
```bash
tam-rfe-validate-intelligence [customer]
```

Features:
- Configuration validation
- Case data verification
- Sync status checking
- Actionable error messages

#### 🧪 Testing & Validation
Automated intelligence engine testing:
- Westpac validation case study
- Configuration accuracy verification
- Multi-customer testing

### Why This Matters

**Before 1.3.0:** Manual customer discovery (slow, error-prone)  
**After 1.3.0:** Dynamic discovery across global accounts (fast, reliable)

**Example:**
- Old way: Search Hydra, copy data, manually configure (15 minutes)
- New way: `tam-rfe-hydra-api "NAPS"` (30 seconds)

### Phase 3 Status

**Blocked:** Direct Hydra OAuth2 + Kerberos API access requires Red Hat infrastructure changes.  
**Current:** Phases 1 & 2 provide full functionality via rhcase backend.

### Breaking Changes

None. Discovery tools are additive to existing workflows.

---

## Version 1.2.0 - Dynamic Customer Onboarding (October 16, 2025)

**Release Type:** Minor  
**Focus:** Eliminate manual configuration editing

### What's New

#### 🎯 Automatic Config Synchronization
The tool now maintains two configuration systems:
1. `customers.conf` - Simple format for tam-rfe-chat
2. `tamscripts.config` - YAML format for rhcase

**Problem Solved:** Previously required manual editing of both files (error-prone).  
**Solution:** Automatic synchronization with intelligent validation.

#### ✨ Benefits
- Zero manual config file editing
- Automatic conflict resolution
- Data validation at onboarding time
- Single source of truth

### Breaking Changes

None. Existing manual configurations remain compatible.

### Migration Guide

**If you have manually configured customers:**

Your existing configurations work as-is. To adopt dynamic onboarding:

```bash
# Re-onboard a customer to enable sync
tam-rfe-onboard-intelligent
```

The tool will detect existing entries and update both config files automatically.

---

## Version 1.1.0 - Automated Installer (October 15, 2025)

**Release Type:** Minor  
**Focus:** Zero-dependency installation experience

### What's New

#### 🚀 Fully Automated Installation
One-command setup:
```bash
./install.sh
```

Features:
- Automatic Python 3.8+ detection
- Virtual environment creation
- Dependency installation
- Git submodule initialization (rhcase)
- Path configuration

**Before 1.1.0:** 8-step manual process  
**After 1.1.0:** Single command

#### 🔧 rhcase Git Submodule Handling
Automatic detection and initialization of rhcase as a git submodule.

### Breaking Changes

None. Manual installation still supported.

### Migration Guide

**For existing installations:**
```bash
cd ~/rfe-bug-tracker-automation
./install.sh
```

The installer detects existing installations and updates them safely.

---

## Version 1.0.0 - Production Release (October 10, 2025)

**Release Type:** Major  
**Focus:** Production-ready enterprise TAM automation

### What's New

This is the first production-ready release of the TAM RFE Bug Tracker Automation Tool.

#### 🎯 Core Tools

**tam-rfe-chat**
Natural language interface to case data:
```bash
tam-rfe-chat "Show me JPMC Sev 1 cases"
```

**tam-rfe-onboard-intelligent**
Smart customer onboarding with learning system:
```bash
tam-rfe-onboard-intelligent
```

**tam-rfe-verify**
System health verification:
```bash
tam-rfe-verify --quick
tam-rfe-verify --full
```

**Report Generation**
Multiple customer report support:
```bash
./generate-tam-reports.sh jpmc westpac bofa
```

#### 🏢 Enterprise Features

- **Enterprise-grade validation** for report accuracy
- **Standalone solution** with integrated rhcase
- **Contribution framework** for multi-TAM teams
- **Red Hat integration** (GitLab, VPN, SSO)

#### 📚 Documentation

- Sales-friendly README for non-technical users
- Comprehensive troubleshooting guide
- Step-by-step setup instructions
- Red Hat-specific resource links

#### 🔐 Red Hat Integration

- Cursor IDE enterprise license setup
- GitLab CEE access instructions
- VPN configuration guide
- ServiceNow integration

### Who This Is For

- **TAMs (Technical Account Managers)** - Primary users
- **Sales Teams** - Demo and customer engagement
- **Support Engineers** - Case management workflows

### System Requirements

- **Python:** 3.8 or higher
- **OS:** RHEL 8+, Fedora 38+, macOS 12+
- **Network:** Red Hat VPN access
- **Tools:** Git, rhcase, Cursor IDE (recommended)

### Getting Started

```bash
# Clone repository
git clone https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation.git
cd rfe-and-bug-tracker-automation

# Install
./install.sh

# Verify
tam-rfe-verify --quick

# Onboard first customer
tam-rfe-onboard-intelligent

# Start using
tam-rfe-chat "Show me all Sev 1 cases"
```

### Support

- **Tool Issues:** Contact jbyrd via GitLab
- **rhcase Issues:** Contact grimm via GitLab
- **General Questions:** See [TROUBLESHOOTING.md](docs/tam-deployment/04-TROUBLESHOOTING-GUIDE.md)

---

## Pre-1.0 Development (September 2025)

### Version 0.2.0 (September 24, 2025)
- Enhanced installation with dependency management
- AI tools integration (Fabric, LiteLLM)
- Initial documentation framework

### Version 0.1.0 (September 23, 2025)
- Initial Hatter PAI system
- Repository structure
- Basic tooling framework

---

## Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.x.x): Breaking changes, major feature additions
- **MINOR** (x.1.x): New features, backward-compatible
- **PATCH** (x.x.1): Bug fixes, documentation updates

---

## Release Schedule

- **Patch releases:** As needed for critical bugs
- **Minor releases:** Monthly (new features)
- **Major releases:** Quarterly (breaking changes, major milestones)

---

## Communication Channels

- **GitLab Issues:** Bug reports and feature requests
- **Email Notifications:** Automatic issue alerts (if configured)
- **Internal Red Hat:** Slack #tam-automation (coming soon)

---

*For a complete list of changes, see [CHANGELOG.md](CHANGELOG.md)*

