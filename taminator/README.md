# Taminator — RFE and Bug Report Generator

A tool for generating and maintaining RFE and bug reports for TAMs. Uses JIRA and case data; supports CLI and optional desktop app.

---

## Summary

**What:** A tool for generating and maintaining RFE and bug reports for TAMs  
**Why:** Saves 2–3 hours per customer per week  
**How:** Desktop app (recommended for UI) or CLI — report generation, JIRA/case data, optional portal posting

---

## Where to get Taminator

**Official (Red Hat coworkers only):** https://gitlab.cee.redhat.com/jbyrd/taminator

Requires Red Hat VPN and GitLab CEE access.

- **Desktop app (recommended):** Download AppImage (Linux) or DMG (macOS) from the [GitLab releases](https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases) page. Double-click to open Taminator in its own app window. No terminal required.
- **From repo:** `git clone https://gitlab.cee.redhat.com/jbyrd/taminator.git ~/taminator` (for CLI or development).

---

## Prerequisites

- **Red Hat VPN** — Required for JIRA and internal APIs.
- **JIRA API token** — From issues.redhat.com → Personal Access Tokens. Configure in the app under Settings.
- **Customer Portal token** (optional, for posting) — From access.redhat.com/management/api → Generate Token.
- **Python 3.7+** — Only if running from repo (CLI/development). Not required for the desktop app.

---

## Installation

### Desktop app (no terminal required)

Double-click the Taminator app; it opens in its own window. No terminal commands needed.

- **Linux:** Download the AppImage from [GitLab releases](https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases), then double-click. Choose x86_64 or ARM64 to match your system (`uname -m` → x86_64 or aarch64).
- **macOS:** Download the DMG from GitLab releases, drag Taminator to Applications, then double-click. First time: right-click → Open to bypass Gatekeeper if prompted.

### From repo (optional)

For CLI or to run the UI from source: `cd taminator/taminator && ./tam-rfe serve`. Desktop app is easier for UI users.

### Windows

Desktop builds are for Linux and macOS only. On Windows, run from the repo (e.g. WSL or Python): `./tam-rfe serve`.

---

## CLI commands

| Command | Description |
|---------|-------------|
| `tam-rfe check <customer>` | Compare report to JIRA; no file changes. |
| `tam-rfe update <customer>` | Fetch JIRA statuses and write to the report file. |
| `tam-rfe post <customer>` | Post report to Red Hat Customer Portal. |
| `tam-rfe onboard <customer>` | Onboard a new customer (interactive). |
| `tam-rfe config` | Manage tokens and configuration. |
| `tam-rfe docs` | Show full user guide in the terminal. |
| `tam-rfe serve` | Start browser-based UI (default http://127.0.0.1:8765). |

Options: `--test-data`, `--help`, `--version` / `-V`.

---

## Run from repo (optional)

To run from source: `git clone https://gitlab.cee.redhat.com/jbyrd/taminator.git ~/taminator`, then `cd ~/taminator/taminator && ./tam-rfe serve` (browser UI at http://127.0.0.1:8765). For most users, the [desktop app from GitLab releases](https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases) is simpler. See [GETTING-STARTED.md](GETTING-STARTED.md) and the [full user guide](../USER-GUIDE.md).

---

## About Taminator

Taminator generates and maintains RFE and bug reports for TAMs. It uses JIRA and case data for consistent markdown reports and can post to customer portal groups. Typical use saves 2–3 hours per customer per week compared to manual tracking.

### Version history

| Version | Key Features | Status |
|---------|--------------|--------|
| **2.0.0** | Desktop app (Linux + macOS), browser UI, CLI parity, GitLab-only | Current |
| v1.9.5 | Vault integration, CLI router fix | Stable |
| v1.9.2 | Cross-platform release, ARM64 AppImage | Stable |
| v1.7.0 | Complete GUI redesign, Auth-Box integration | Stable |
| (earlier) | See repo history | Stable |

### Project status

- **Version:** 2.0.0
- **Platforms:** Linux (AppImage x86_64 + ARM64) | macOS (DMG when available)
- **Full user guide:** [USER-GUIDE.md](../USER-GUIDE.md) (in repo root); also in the app under User Guide panel.

### What this tool does
- **Automatically discovers** all RFE and Bug cases for your customers using `rhcase`
- **Filters cases** by SBR Group (Ansible, OpenShift, etc.) and status (Active, Closed, etc.)
- **Generates professional 3-table reports** with Active RFE, Active Bug, and Closed case history
- **Posts content directly** to customer portal groups via Red Hat API
- **Sends email notifications** to TAMs with success/failure status

### What This Tool Does NOT Do
- Does NOT create new RFE or Bug cases
- Does NOT modify existing case content or status
- Does NOT send notifications to customers (silent portal updates)
- Does NOT access customer data outside of Red Hat systems
- Does NOT replace TAM judgment or customer relationship management

### JIRA and RFE mapping (where to submit)

To determine where an RFE should be submitted, use the **Centralized JIRA Project Mapping** in The Source (TAM Manual). It is the comprehensive JIRA and RFE mapping for Red Hat products and is community-managed across all products. Taminator uses this mapping as its source for supported JIRA project keys. If you find an issue, outdated information, or a missing product in the JIRA mapping, flag it and see if you can get it corrected.

**Add your own (niche) mappings:** To support JIRA project keys not yet in the main list, add them to `~/.config/taminator/jira_prefixes.txt` — one project key per line (e.g. `MYPROJECT`). Lines starting with `#` and blank lines are ignored. These are merged with the built-in list for discovery, report parsing, and link formatting.

## Quick Start

**Get started:** [GETTING-STARTED.md](GETTING-STARTED.md) | [Full user guide](../USER-GUIDE.md)

## Supported Customers

| Customer | Group ID | Status | Account Number |
|----------|----------|--------|----------------|
| Wells Fargo | 4357341 | Production Ready | 838043 |
| TD Bank | 7028358 | Sandbox Ready | 1912101 |
| JPMC | 6956770 | Production Ready | 334224 |
| Fannie Mae | 7095107 | Production Ready | 1460290 |

## Time Savings


| Process | Manual | Automated | Savings |
|---------|--------|-----------|---------|
| **Per Customer Per Week** | 2-3 hours | 5 minutes | 95% reduction |
| **Per TAM Per Week** | 8-12 hours | 20 minutes | 95% reduction |
| **Per TAM Per Year** | 400-600 hours | 17 hours | 95% reduction |

## Security and compliance

### Red Hat AI Policy Compliance
- Customer data: Red Hat Granite models only
- Internal data: AIA-approved model list
- External APIs: Blocked for customer data
- Audit logging: All operations tracked

### Data Protection
- Customer data processed via Red Hat Granite models only
- No external API calls for customer data
- All operations logged for audit compliance
- Secure credential management via Red Hat SSO

## Need Help?

### Quick Commands
```bash
# Test the system
./bin/tam-rfe-verify --quick

# Comprehensive verification
./bin/tam-rfe-verify --full

# Get help
./bin/tam-rfe-chat --help
```

### Common Questions
- **"How do I add a new customer?"** → Run `./bin/tam-rfe-onboard-intelligent`
- **"The tool isn't finding cases"** → Check your `rhcase` configuration
- **"I want to customize the reports"** → Use the chat interface and ask me to modify them

## Ready to Start?

### For Brand New TAMs (Zero Experience)
1. **Start chatting**: `./bin/tam-rfe-chat`
2. **Tell the AI**: "I'm new to this" or "I need help getting started"
3. **Follow the guided onboarding**: The AI will walk you through everything step by step
4. **Complete setup**: From installation to your first report

### For Experienced TAMs
1. **Run onboarding**: `./bin/tam-rfe-onboard-intelligent`
2. **Start chatting**: `./bin/tam-rfe-chat`
3. **Ask for reports**: "Generate RFE report for [Customer]"

**That's it! The tool will learn your preferences and get smarter over time.**

## Documentation

- **[Full user guide](../USER-GUIDE.md)**: Canonical guide (in app and on GitLab)
- **[Getting Started](GETTING-STARTED.md)**: Quick setup
- **[Purpose](PURPOSE.md)**: What the tool does and does not do
- **Releases:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases
- **Issues:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues

## Contributing

### For TAMs
- Report issues via GitLab issues
- Suggest improvements via merge requests
- Share customer-specific templates
- Provide feedback on usability

### For Developers
- Follow Red Hat coding standards
- Maintain comprehensive documentation
- Include unit tests for all features
- Ensure Red Hat compliance

## Support & Contact

### Personal Development Contact
- **Developer**: jbyrd (jbyrd@redhat.com)
- **GitLab Repository**: https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation
- **Original Author**: grimm (PAI framework tools)
- **Documentation**: See `docs/` directory for detailed guides

### Community Support
- **Slack**: #tam-automation-tools
- **Email**: tam-automation-team@redhat.com

---

## Bottom Line for TAMs

**This tool transforms a 2-3 hour manual weekly task into a 5-minute automated process, freeing TAMs to focus on strategic customer work while ensuring consistent, professional customer communication.**

### The Tool is Designed to:
- **Save time** - 95% reduction in manual work
- **Improve quality** - 100% consistent, professional content
- **Increase reliability** - Automated processes eliminate human error
- **Enhance customer experience** - Daily updates instead of weekly manual updates
- **Maintain compliance** - Full Red Hat AI policy compliance
- **Scale easily** - Works for any TAM customer with proper configuration

## Development Philosophy

This personal project is developed with the following principles:

- **Independence**: My own standalone solution that uses PAI tools but operates independently
- **Simplicity**: Easy to deploy and use without complex dependencies
- **Reliability**: Focused on core functionality with robust error handling
- **TAM-Focused**: Built specifically for TAM workflows and needs
- **Continuous Improvement**: Regular updates and enhancements based on real-world usage

## Acknowledgments

- **Original Creator**: grimm - PAI framework tools and initial RFE automation concept
- **Development**: jbyrd - Personal project with independent development and enhancements
- **Community**: Red Hat TAM community for feedback and requirements

---

[Releases](https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases) | [Getting Started](GETTING-STARTED.md) | [Issues](https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues) | [Contact](mailto:jbyrd@redhat.com)