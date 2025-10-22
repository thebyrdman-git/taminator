# 💀 Taminator - The Skynet TAMs Actually Want

> *"Come with me if you want to save time."* - Taminator T-800

**Professional TAM automation and workflow tools for Red Hat.** Because sometimes automation doesn't have to be scary.

---

## 📋 TLDR

**What:** Complete automation suite for Red Hat TAM workflows and customer engagement  
**Why:** Saves 2-3 hours per customer per week  
**How:** GUI or CLI - automated tracking, reporting, and customer portal management

**Quick Start:**

## 📥 Download Taminator v1.9.1

### GitLab CEE (Red Hat Internal)
**⚠️ Requires:** Red Hat VPN + GitLab CEE login

**Release Page:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/v1.9.1

- 🐧 **Linux:** `Taminator-1.9.1.AppImage` (~120 MB)
- 🍎 **macOS Intel:** Coming soon via GitHub CI/CD
- 🍎 **macOS Apple Silicon:** Coming soon via GitHub CI/CD
- 🪟 **Windows:** Coming soon via GitHub CI/CD

### GitHub (Public - No VPN Required)
**Release Page:** https://github.com/thebyrdman-git/taminator-ci/releases/tag/v1.9.1

- 🐧 **Linux:** `Taminator-1.9.1.AppImage` (~120 MB) ✅ Available now
- 🍎 **macOS Intel/Apple Silicon:** 🔄 Building via CI/CD
- 🪟 **Windows:** 🔄 Building via CI/CD

### 🐧 Linux Installation
```bash
# Download from release page above
# "I'll be back... with your report."

# Quick install (from GitHub - no VPN required):
curl -L https://github.com/thebyrdman-git/taminator-ci/releases/download/v1.9.1/Taminator-1.9.1.AppImage -o Taminator.AppImage
chmod +x Taminator.AppImage
./Taminator.AppImage

# Or manual install:
chmod +x ~/Downloads/Taminator-1.9.1.AppImage
~/Downloads/Taminator-1.9.1.AppImage

# Optional: Move to ~/Applications for system-wide access
mkdir -p ~/Applications
mv ~/Downloads/Taminator-1.9.1.AppImage ~/Applications/
```

### 🍎 macOS Installation
```bash
# 🔄 macOS builds coming soon via GitHub CI/CD
# "Come with me if you want to save time."

# Check GitHub releases for updates:
# https://github.com/thebyrdman-git/taminator-ci/releases

# When available:
# open ~/Downloads/Taminator-1.9.1*.dmg
# Drag Taminator to Applications folder
# Launch from Launchpad or Applications
```

### 🪟 Windows Installation
```powershell
# 🔄 Windows builds coming soon via GitHub CI/CD
# "I need your clothes, your boots, and your RFE reports."

# Check GitHub releases for updates:
# https://github.com/thebyrdman-git/taminator-ci/releases

# When available:
# Double-click Taminator_Setup_1.9.1.exe
# Follow installation wizard
# Launch from Start Menu or Desktop
```

### 💻 Command Line (All Platforms) - "Hasta la vista, manual tracking!"
```bash
./tam-rfe check --customer <name>
./tam-rfe update --customer <name>
./tam-rfe post --customer <name>
```

**[→ Full Getting Started Guide](GETTING-STARTED.md)** | **[📥 All Downloads](https://gitlab.cee.redhat.com/jbyrd/taminator/-/tree/main)**

---

## 🤖 About Taminator

**Taminator is a professional RFE/Bug tracking tool for Red Hat TAMs with both GUI and CLI interfaces.**

*"Listen, and understand. This tool is out there. It can't be bargained with. It can't be reasoned with. It doesn't feel pity, or remorse, or fear about tracking your RFEs. And it absolutely will not stop, ever, until your reports are generated."*

**The tool automatically tracks RFE and Bug statuses across JIRA and generates professional reports for customer portal groups, saving TAMs 2-3 hours per customer per week.**

### 📊 Version History

| Version | Release Date | Key Features | Status |
|---------|--------------|--------------|--------|
| **v1.9.1** | Oct 2025 | PatternFly 6, KB/T3 API, Clippy, Auth Box, Python bundled | 🟢 Current |
| v1.7.0 | Oct 2025 | Complete GUI redesign, Auth-Box, GitHub integration | ⚪ Previous |
| v1.6.0 | Sep 2025 | Desktop integration, AppImage packaging | ✅ Stable |
| v1.5.0 | Aug 2025 | Enhanced reporting, multi-customer support | ✅ Stable |
| v1.4.0 | Jul 2025 | CLI improvements, email notifications | ✅ Stable |
| v1.3.0 | Jun 2025 | Portal posting automation | ✅ Stable |
| v1.2.0 | May 2025 | JIRA integration, real-time status checks | ✅ Stable |
| v1.1.0 | Apr 2025 | Template system, markdown reports | ✅ Stable |
| v1.0.0 | Mar 2025 | Initial release, basic RFE tracking | ✅ Stable |

###  Project Status
- **Version**: 1.9.1 (Production Release) - *"Advanced prototype. You could say we're... ahead of schedule."*
- **Status**: Production-ready with complete GUI
- **Platforms**: 🐧 Linux (AppImage) | 🍎 macOS (DMG) | 🪟 Windows (NSIS Installer)
- **Architecture**: Intel/AMD (x64) + Apple Silicon (arm64)
- **Threat Level**: Zero. We're the friendly Skynet.

### What This Tool Does
- **Automatically discovers** all RFE and Bug cases for your customers using `rhcase`
- **Filters cases** by SBR Group (Ansible, OpenShift, etc.) and status (Active, Closed, etc.)
- **Generates professional 3-table reports** with Active RFE, Active Bug, and Closed case history
- **Posts content directly** to customer portal groups via Red Hat API
- **Sends email notifications** to TAMs with success/failure status

### What This Tool Does NOT Do
- ❌ Does NOT create new RFE or Bug cases
- ❌ Does NOT modify existing case content or status  
- ❌ Does NOT send notifications to customers (silent portal updates)
- ❌ Does NOT access customer data outside of Red Hat systems
- ❌ Does NOT replace TAM judgment or customer relationship management

## 🚀 Quick Start

**Want to get started immediately?** → [**GETTING-STARTED.md**](GETTING-STARTED.md)

*"Your mission, should you choose to accept it: Install Taminator and never manually track an RFE again."*

### Prerequisites
- Red Hat VPN connection *(Skynet uplink)*
- `rhcase` tool installed and configured *(Target acquisition system)*
- Python 3.7+ *(Neural net processor)*
- Red Hat SSO credentials *(Authorization codes)*
- Customer portal group access *(Mission parameters)*

### Installation Options

#### GUI Application (Recommended for most TAMs)
- **🐧 Linux**: Download `.AppImage` - Single file, no installation required
- **🍎 macOS**: Download `.dmg` - Drag to Applications, ready to go
- **🪟 Windows**: Download `.exe` - Standard installer with Start Menu integration

#### CLI Tools (For automation and advanced users)
1. **Auto-Detection**: `./bin/tam-rfe-auto-detect` - Detects your existing setup automatically
2. **Interactive Setup**: `./bin/tam-rfe-onboard-intelligent` - Learn your preferences through questions
3. **Template Customization**: `./bin/tam-rfe-template-customizer` - Create personalized report styles
4. **Chat Interface**: `./bin/tam-rfe-chat` - Just ask me what you need

## 💬 How to Use

### Start the Chat Interface
```bash
./bin/tam-rfe-chat
```

### Ask Me Anything
- "Generate RFE report for Wells Fargo"
- "Show me all Ansible cases for TD Bank"
- "Prepare summary for JPMC quarterly meeting"

### Direct Commands
```bash
# Test with specific customer
./bin/tam-rfe-monitor-simple wellsfargo --test

# Run daily automation
./bin/tam-rfe-monitor-simple wellsfargo --daily

# Run all customers
./bin/tam-rfe-monitor-simple --all
```

## 📋 Report Options

When you ask for reports, I'll give you **two options**:

1. **Copy/Paste** - I show you the markdown, you paste it wherever you need it
2. **Auto-Post** - I automatically post to the customer portal

## 🏢 Supported Customers

| Customer | Group ID | Status | Account Number |
|----------|----------|--------|----------------|
| Wells Fargo | 4357341 | ✅ Production Ready | 838043 |
| TD Bank | 7028358 | ✅ Sandbox Ready | 1912101 |
| JPMC | 6956770 | ✅ Production Ready | 334224 |
| Fannie Mae | 7095107 | ✅ Production Ready | 1460290 |

## 📊 Time Savings

*"In three hours, I could track 4 customers manually. Or in 5 minutes, Taminator could track them all. It's a no-brainer."* - John Connor, probably

| Process | Manual | Automated | Savings |
|---------|--------|-----------|---------|
| **Per Customer Per Week** | 2-3 hours | 5 minutes | 95% reduction |
| **Per TAM Per Week** | 8-12 hours | 20 minutes | 95% reduction |
| **Per TAM Per Year** | 400-600 hours | 17 hours | 95% reduction |

*Translation: Taminator gives you back 383 hours per year. That's 9.5 work weeks. You're welcome.*

## 🛡️ Security & Compliance

### Red Hat AI Policy Compliance
- ✅ Customer data: Red Hat Granite models only
- ✅ Internal data: AIA-approved model list
- ✅ External APIs: Blocked for customer data
- ✅ Audit logging: All operations tracked

### Data Protection
- Customer data processed via Red Hat Granite models only
- No external API calls for customer data
- All operations logged for audit compliance
- Secure credential management via Red Hat SSO

## 🆘 Need Help?

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

## 🎉 Ready to Start?

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

## 📚 Documentation

- **[Getting Started Guide](GETTING-STARTED.md)**: Quick 5-minute setup
- **[Purpose Statement](PURPOSE.md)**: Detailed functionality overview
- **[TAM Community Guide](README-TAM-COMMUNITY.md)**: Comprehensive community documentation
- **[Ansible Deployment](ANSIBLE-DEPLOYMENT.md)**: Automated deployment options
- **[Prerequisites Guide](docs/PREREQUISITES-GUIDE.md)**: Complete setup requirements

## 🤝 Contributing

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

## 📞 Support & Contact

### Personal Development Contact
- **Developer**: jbyrd (jbyrd@redhat.com)
- **GitLab Repository**: https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation
- **Original Author**: grimm (PAI framework tools)
- **Documentation**: See `docs/` directory for detailed guides

### Community Support
- **Slack**: #tam-automation-tools
- **Email**: tam-automation-team@redhat.com

---

## 🎯 Bottom Line for TAMs

**This tool transforms a 2-3 hour manual weekly task into a 5-minute automated process, freeing TAMs to focus on strategic customer work while ensuring consistent, professional customer communication.**

### The Tool is Designed to:
- **Save time** - 95% reduction in manual work
- **Improve quality** - 100% consistent, professional content
- **Increase reliability** - Automated processes eliminate human error
- **Enhance customer experience** - Daily updates instead of weekly manual updates
- **Maintain compliance** - Full Red Hat AI policy compliance
- **Scale easily** - Works for any TAM customer with proper configuration

## 🚀 Development Philosophy

This personal project is developed with the following principles:

- **Independence**: My own standalone solution that uses PAI tools but operates independently
- **Simplicity**: Easy to deploy and use without complex dependencies
- **Reliability**: Focused on core functionality with robust error handling
- **TAM-Focused**: Built specifically for TAM workflows and needs
- **Continuous Improvement**: Regular updates and enhancements based on real-world usage

## 🙏 Acknowledgments

- **Original Creator**: grimm - PAI framework tools and initial RFE automation concept
- **Development**: jbyrd - Personal project with independent development and enhancements
- **Community**: Red Hat TAM community for feedback and requirements

---

## 🎬 Taminator Quotes to Live By

> *"I'll be back... with your weekly RFE report."* - T-800

> *"Come with me if you want to save time."* - T-800

> *"Hasta la vista, manual tracking!"* - T-800

> *"No fate but what we automate."* - Sarah Connor

> *"The future is not set. There is no fate but what we make. Also, your reports are ready."* - Sarah Connor

> *"Listen, and understand. Taminator is out there. It can't be bargained with. It doesn't feel pity or remorse, and it absolutely will not stop, ever, until your RFE tracking is automated."* - Kyle Reese

---

**🤖 Taminator - RFE Automation Done Right**  
*Making TAMs more efficient, one automated report at a time*

**The Skynet TAMs Actually Want™**

**💝 Built with passion for helping TAMs succeed**  
*v1.9.1 - Production Release - October 2025*

---

<div align="center">

**[📥 Download](https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases)** | **[📖 Docs](GETTING-STARTED.md)** | **[🐛 Report Issue](https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues)** | **[💬 Support](mailto:jbyrd@redhat.com)**

*Remember: In the future, all TAMs use Taminator. Join the resistance... against manual work.*

</div>