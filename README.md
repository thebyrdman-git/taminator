# TAM RFE Automation Tool - Personal Development Fork

## 🎯 Overview

**This is my personal development fork of the TAM RFE Automation Tool, originally created by grimm. I'm developing this independently to create a standalone, self-contained solution that uses tools from grimm's PAI project but operates as my own independent project.**

**The tool automatically generates and posts professional RFE/Bug tracker reports to customer portal groups, saving TAMs 2-3 hours per customer per week.**

### 🔄 Project Status
- **Original Author**: grimm (PAI framework tools)
- **Personal Fork**: jbyrd - Independent development
- **Development Approach**: Standalone, self-contained solution using PAI tools
- **Current Status**: Active development and enhancement

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

### Prerequisites
- Red Hat VPN connection
- `rhcase` tool installed and configured
- Python 3.7+
- Red Hat SSO credentials
- Customer portal group access

### 🎯 **First Time Setup (Required)**

**Run this ONCE to configure the tool:**
```bash
./bin/tam-rfe-onboard-intelligent
```

**What this does:**
- Asks you about your customers (Wells Fargo, TD Bank, etc.)
- Configures your preferences
- Sets up the tool for your specific needs
- **No Python knowledge required** - just answer the questions!

### 📋 **After Setup, Choose Your Method**

1. **Chat Interface (Easiest)**: `./bin/tam-rfe-chat`
2. **Direct Commands**: `./bin/tam-rfe-monitor-simple [customer] --test`
3. **Auto-Detection**: `./bin/tam-rfe-auto-detect` (if you have existing setup)

## 💬 How to Use

### 🎯 **Simple 3-Step Process**

#### Step 1: Run the Setup Script
```bash
./bin/tam-rfe-onboard-intelligent
```
*This configures your customer accounts and preferences - just answer the questions!*

#### Step 2: Choose Your Method

**Option A: Chat Interface (Easiest)**
```bash
./bin/tam-rfe-chat
```
*Then just ask naturally: "Generate RFE report for Wells Fargo"*

**Option B: Direct Commands**
```bash
# Test with specific customer (no portal posting)
./bin/tam-rfe-monitor-simple wellsfargo --test

# Run daily automation (posts to portal)
./bin/tam-rfe-monitor-simple wellsfargo --daily

# Run all customers at once
./bin/tam-rfe-monitor-simple --all
```

#### Step 3: Get Your Reports
- **Copy/Paste**: Tool shows you the markdown, you paste it where needed
- **Auto-Post**: Tool automatically posts to customer portal

### 🚀 **Quick Start Commands**

```bash
# 1. First time setup (run once)
./bin/tam-rfe-onboard-intelligent

# 2. Generate a report (choose one)
./bin/tam-rfe-chat                    # Interactive chat
./bin/tam-rfe-monitor-simple wellsfargo --test    # Test mode
./bin/tam-rfe-monitor-simple wellsfargo --daily   # Production mode
```

### 📋 **What Each Script Does**

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `tam-rfe-onboard-intelligent` | Initial setup & configuration | First time only |
| `tam-rfe-chat` | Interactive chat interface | Easiest way to use |
| `tam-rfe-monitor-simple` | Direct command execution | Automation/scheduling |
| `tam-rfe-verify` | System health check | Troubleshooting |
| `tam-rfe-template-customizer` | Customize report styles | Optional customization |

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

| Process | Manual | Automated | Savings |
|---------|--------|-----------|---------|
| **Per Customer Per Week** | 2-3 hours | 5 minutes | 95% reduction |
| **Per TAM Per Week** | 8-12 hours | 20 minutes | 95% reduction |
| **Per TAM Per Year** | 400-600 hours | 17 hours | 95% reduction |

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

**🤖 TAM Automation Assistant - Personal Development Edition**  
*Making your life easier, one report at a time*

**💝 Built with passion for helping TAMs succeed, developed independently for maximum flexibility**