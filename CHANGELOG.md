# Changelog

All notable changes to the TAM RFE Bug Tracker Automation Tool will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.5.0] - 2025-10-17

### Added
- **Comprehensive Testing Suite** - 100% test pass rate across all components
- **Testing Report Generator** - Automated test documentation and validation
- **Slack Integration Handler** - Foundation for Slack notifications
- **Cross-Platform Validation** - Verified Linux, macOS architecture support
- **Test Report Documentation** - `TESTING-REPORT-2025-10-17.md` with full coverage analysis

### Fixed
- **Path Migration Complete** - All references updated from old `/home/jbyrd/pai/rfe-automation-clean` to `/home/jbyrd/taminator`
- **Ansible Playbooks** - Fixed 16+ generation playbooks with correct paths
- **Template Tests** - Updated template test paths for new repository location
- **Ansible vars_prompt** - Removed unsupported `when` clause in installation playbook
- **Geerling Role Version** - Corrected homebrew role from 5.0.0 to 4.0.0 (available version)
- **Python Cache Cleanup** - Removed all stale `__pycache__` and `.pyc` files

### Changed
- Email notifications now default to Gmail SMTP (jimmykbyrd@gmail.com)
- Ansible Galaxy dependencies now install correctly without VPN configurator
- Repository fully validated and production-ready

### Testing
- ✅ Platform Abstraction Tests: 7/7 passed
- ✅ Directory Structure Tests: 5/5 passed
- ✅ Core TAM Tools Tests: 4/4 passed
- ✅ Template Rendering Tests: 4/4 passed
- ✅ Foundation Module Tests: 3/3 passed
- ✅ Ansible Deployment Tests: 6/6 passed
- ✅ Installation Script Tests: 4/4 passed
- **Overall: 33/33 tests passed (100%)**

### PAI Framework Compliance
- Grade: **A (95%)**
- Custom code: ~5%
- Proven code: ~95% (Geerling roles + stdlib)
- Production readiness: **VERIFIED ✅**

## [1.4.1] - 2025-10-17

### Fixed
- **Issue #12:** Cross-platform sed compatibility for macOS/BSD in `tam-rfe-onboard-intelligent`
- **Issue #13:** Python AttributeError crash in verification system due to enum/dataclass naming collision
- **Issue #14:** False negatives in `tam-rfe-verify` for Python 3.11+ and rhcase checks
- Created `tamscripts.config` directory and file before backup operations

### Changed
- Python version check now accepts 3.8+ instead of only 3.8-3.10
- rhcase check downgraded to warning (not critical error) for better usability

## [1.4.0] - 2025-10-16

### Added
- **TUI (Text User Interface)** for routine TAM workflows with dialog-based menus
- **TAM RFE Report Scheduler** with three phases:
  - Phase 1: Cron-based scheduling with YAML configuration
  - Phase 2: Systemd daemon with automatic execution and email delivery
  - Phase 3: Advanced features (schedule validation, timezone support, conflict detection)
- **Red Hat VPN Intelligence** with automatic Kerberos and CA certificate detection
- **Dynamic COPR repository detection** for multi-distribution support (EPEL 8/9/10, Fedora)
- VPN testing infrastructure for Alma 9 VM environments

### Fixed
- Issues #8 and #9 in intelligent onboarding system

### Changed
- Offline installer now uses ZIP format instead of tar.gz
- Defined Sys Admin persona as default for all RFE tools

## [1.3.0] - 2025-10-16

### Added
- **Hydra API Integration Phase 1:** Geographic customer discovery via Red Hat network
- **Hydra API Integration Phase 2:** Organizational customer discovery with intelligent heuristics
- **Dynamic customer discovery** via Red Hat case data correlation
- **Intelligence engine validation framework** with `tam-rfe-validate-intelligence`
- Comprehensive testing system for intelligence engine accuracy

### Changed
- Directory structure reorganized for better clarity
- Documentation moved to main directory for easier access
- README streamlined (69% reduction in length)

### Documented
- Hydra API Phase 3 blockers identified (requires OAuth2 + Kerberos direct API access)
- Complete Hydra phases overview and investigation results

## [1.2.0] - 2025-10-16

### Added
- **Dynamic Customer Onboarding** with automatic config synchronization
  - Eliminates manual editing of `customers.conf` and `tamscripts.config`
  - Synchronizes customer data across both configuration systems
  - Intelligent data validation and conflict resolution

### Changed
- README updated to highlight dynamic onboarding as key differentiator

## [1.1.0] - 2025-10-15

### Added
- **Fully automated zero-dependency-hell installation**
  - Automatic Python 3.8+ detection
  - Virtual environment creation
  - Dependency installation
  - Git submodule initialization
- **rhcase git submodule handling** in installer

### Fixed
- NLP pattern matching in command parser
- Command documentation accuracy

### Changed
- README updated to reflect automated installer capabilities

## [1.0.0] - 2025-10-10

### Added
- **Comprehensive RFE Automation Tool** with Ansible collection
- **Enterprise-grade report content validation system**
- **Standalone solution** with integrated rhcase tool
- **Active case reporting** functionality
- **Contribution framework** for report consistency
- Multiple TAM workflow tools:
  - `tam-rfe-chat`: Natural language case queries
  - `tam-rfe-onboard-intelligent`: Smart customer onboarding
  - `tam-rfe-verify`: System verification
  - Report generation for multiple customers

### Changed
- Complete rewrite for non-technical users (sales-friendly)
- README clarified for TAM audience with step-by-step instructions
- Cursor IDE setup with Red Hat enterprise license integration
- VPN and authentication documentation

### Documented
- Red Hat-specific resources (GitLab, Python packages, ServiceNow)
- Comprehensive troubleshooting guide
- Contact information (jbyrd for tool, grimm for rhcase)
- GitLab CEE license requirements and request process

## [0.2.0] - 2025-09-24

### Added
- Comprehensive dependency management in installation script
- AI tools integration (Fabric AI + LiteLLM)
- API keys configuration guide
- Tools and workflow documentation
- Mermaid diagrams for system architecture

### Changed
- Installation script enhanced with comprehensive checks
- Updated to include API keys needed
- Minor README improvements

## [0.1.0] - 2025-09-23

### Added
- Initial Hatter PAI system for Red Hat teams
- Fabric AI documentation
- LiteLLM configuration
- Repository setup with main branch

---

## Version History Quick Reference

| Version | Date | Key Features |
|---------|------|--------------|
| 1.4.1 | 2025-10-17 | Critical bug fixes (macOS, verification system) |
| 1.4.0 | 2025-10-16 | TUI, Report Scheduler, VPN Intelligence |
| 1.3.0 | 2025-10-16 | Hydra API integration, Customer discovery |
| 1.2.0 | 2025-10-16 | Dynamic customer onboarding |
| 1.1.0 | 2025-10-15 | Automated zero-dependency installer |
| 1.0.0 | 2025-10-10 | Production-ready RFE automation tool |
| 0.2.0 | 2025-09-24 | AI tools integration, dependency management |
| 0.1.0 | 2025-09-23 | Initial release (Hatter PAI) |

---

## Upgrade Notes

### From 1.4.0 to 1.4.1
- No breaking changes
- Bug fixes improve cross-platform compatibility
- Recommended for all macOS users

### From 1.3.x to 1.4.0
- New TUI available via `tam-rfe-tui`
- New scheduler service: `tam-rfe-tool-report-scheduler`
- VPN intelligence now automatic on supported distributions

### From 1.2.x to 1.3.0
- New Hydra API tools for customer discovery
- No configuration changes required

### From 1.1.x to 1.2.0
- Dynamic onboarding now handles config synchronization automatically
- Existing manual configurations remain compatible

### From 1.0.x to 1.1.0
- Installer now fully automated
- Re-run `./install.sh` to update tooling

---

## Contributors

- **Jimmy Byrd (jbyrd)** - Primary Developer
- **Alexey Masolov (amasolov)** - Testing, TUI concept, macOS compatibility
- **Grimm** - rhcase integration and support

---

*For detailed release notes and migration guides, see [RELEASE-NOTES.md](RELEASE-NOTES.md)*

