# TAM RFE Automation Tool

## 🎯 Overview

**This is the TAM RFE Automation Tool, developed by jbyrd as a standalone, self-contained solution that uses tools from [grimm's PAI project](https://gitlab.cee.redhat.com/gvaughn/hatter-pai). This IS the RFE automation tool itself.**

**The tool automatically generates and posts professional RFE/Bug tracker reports and active case reports to customer portal groups, saving TAMs 2-3 hours per customer per week.**

### 🔄 Project Status
- **Developer**: jbyrd - Independent development
- **Uses Tools From**: grimm's PAI framework
- **Development Approach**: Standalone, self-contained solution
- **Current Status**: Active development and enhancement

### What This Tool Does
- **Automatically discovers** all RFE and Bug cases for your customers using `rhcase`
- **Filters cases** by SBR Group (Ansible, OpenShift, etc.) and status (Active, Closed, etc.)
- **Generates professional reports** including:
  - Active case reports (current open cases)
  - RFE/Bug tracker reports (3-table format with Active RFE, Active Bug, and Closed JIRA ticket history)
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

### What You Need
- Red Hat laptop with internet connection
- Red Hat VPN access
- Your Red Hat login credentials
- Access to customer portal
- [`rhcase` tool](https://gitlab.cee.redhat.com/gvaughn/rhcase) installed (see installation instructions below)

### 📥 **Step 0: Get the Tool (One Time Only)**

**Download the RFE Automation Tool:**
1. Go to: https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation
2. Click the green "Clone" button
3. Click "Download ZIP"
4. Extract the ZIP file to a folder on your computer (like `~/rfe-automation` or `/home/username/rfe-automation`)
5. Remember where you put it - you'll need to go there to run the commands

### 🔧 **Install rhcase Tool (One Time Only)**

**If you don't have rhcase installed:**
1. Go to: https://gitlab.cee.redhat.com/gvaughn/rhcase
2. Follow the installation instructions on that page
3. Test it works by opening terminal and typing: `rhcase --version`
4. If you see a version number, you're good to go!

### 🎯 **First Time Setup (5 Minutes - One Time Only)**

**Step 1: Open your terminal**
- On RHEL/Fedora: Press `Ctrl + Alt + T` or click Activities → Terminal
- On Mac: Press `Cmd + Space`, type "Terminal", press Enter
- You should see a black window with text (this is your terminal)

**Step 2: Go to the tool folder**
```bash
cd ~/rfe-automation
```
*Replace `~/rfe-automation` with wherever you put the tool folder*

**Step 3: Run the setup wizard**
```bash
./bin/tam-rfe-onboard-intelligent
```
*Just copy and paste this line, then press Enter*

**What happens next:**
- The tool asks you simple questions like "What customers do you work with?"
- You type answers like "Wells Fargo" or "TD Bank"
- It may ask for customer account numbers - you can find these in your customer portal or ask your manager
- It may ask for group IDs - these are also in the customer portal
- The tool remembers your answers for next time
- **No technical knowledge needed** - just answer the questions!

### 📋 **After Setup, You Have 2 Easy Options**

**Option 1: Talk to the Tool (Easiest)**
```bash
./bin/tam-rfe-chat
```
*Then just type: "Generate a report for Wells Fargo"*

**Option 2: Use Simple Commands**
```bash
./bin/tam-rfe-monitor-simple wellsfargo --test
```
*This creates a test report you can review before posting*

## 💬 How to Use (Super Simple!)

### 🎯 **The Easiest Way (Recommended for Everyone)**

**1. Open Terminal** (see instructions above)

**2. Start the Chat**
```bash
./bin/tam-rfe-chat
```

**3. Just Type What You Want**
- "Generate a report for Wells Fargo"
- "Show me TD Bank cases"
- "Create active case report for JPMC"
- "Help me with Wells Fargo"

**That's it!** The tool does everything else.

### 🚀 **Alternative: Simple Commands**

If you prefer commands, here are the only ones you need:

```bash
# Create a test report (safe to try)
./bin/tam-rfe-monitor-simple wellsfargo --test

# Create and post a real report
./bin/tam-rfe-monitor-simple wellsfargo --daily
```

### 📋 **What You Get**

**The tool creates professional reports with:**
- List of all open cases for your customer
- Case numbers, descriptions, and status
- Recent case closures
- Everything formatted nicely for customer meetings

**You get 2 options:**
1. **Copy the report** - Tool shows you the text, you copy and paste it anywhere
2. **Auto-post** - Tool automatically puts it on the customer portal (you get an email confirmation)

## 📋 Report Options

When you ask for reports, I'll give you **two options**:

1. **Copy/Paste** - I show you the markdown, you paste it wherever you need it
2. **Auto-Post** - I automatically post to the customer portal

## 🏢 Example Customers

The tool works with any Red Hat customer. Here are examples of how it's configured:

| Customer Example | Group ID Example | Status | Account Number Example |
|------------------|------------------|--------|------------------------|
| Wells Fargo | 4357341 | ✅ Production Ready | 838043 |
| TD Bank | 7028358 | ✅ Sandbox Ready | 1912101 |
| JPMC | 6956770 | ✅ Production Ready | 334224 |
| Fannie Mae | 7095107 | ✅ Production Ready | 1460290 |

*Note: These are examples for demonstration purposes. You'll configure the tool with your own customers during setup.*

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

### If Something Goes Wrong
```bash
# Check if everything is working
./bin/tam-rfe-verify --quick
```

### Common Questions
- **"How do I add a new customer?"** → Run the setup wizard again: `./bin/tam-rfe-onboard-intelligent`
- **"The tool isn't finding cases"** → Check these things:
  - Make sure you're connected to Red Hat VPN
  - Test rhcase works: type `rhcase --version` in terminal
  - Try: `rhcase list [customer-name] --months 1` to see if it finds cases
  - If rhcase doesn't work, ask your IT team for help
- **"I can't find customer account numbers"** → Check your customer portal or ask your manager
- **"I want to change how reports look"** → Use the chat and ask: "Can you customize the report format?"
- **"I'm stuck!"** → Use the chat and type: "Help me" or "I need assistance"

### Getting Support
- **Slack**: #tam-automation-tools
- **Email**: tam-automation-team@redhat.com
- **Developer**: jbyrd@redhat.com

## 🎉 Ready to Start?

### For All Users

**Step 1: Open Terminal**
- RHEL/Fedora: Press `Ctrl + Alt + T` or click Activities → Terminal
- Mac: Press `Cmd + Space`, type "Terminal", press Enter

**Step 2: Run Setup (One Time Only)**
```bash
./bin/tam-rfe-onboard-intelligent
```
*Answer the questions about your customers*

**Step 3: Start Using It**
```bash
./bin/tam-rfe-chat
```
*Then just type: "Generate a report for [Customer Name]"*

### For First-Time Users
- **The chat interface is like texting** - just type what you want
- **The tool asks you questions** - just answer them
- **If you get stuck, type "help"** - the tool will guide you
- **Contact support** if you need assistance with setup

**That's it! The tool does all the hard work for you.**

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

### Development Contact
- **Developer**: jbyrd (jbyrd@redhat.com)
- **GitLab Repository**: https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation
- **Uses Tools From**: grimm's PAI framework
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

This tool is developed with the following principles:

- **Independence**: Standalone solution that uses PAI tools but operates independently
- **Simplicity**: Easy to deploy and use without complex dependencies
- **Reliability**: Focused on core functionality with robust error handling
- **TAM-Focused**: Built specifically for TAM workflows and needs
- **Continuous Improvement**: Regular updates and enhancements based on real-world usage

## 🙏 Acknowledgments

- **PAI Framework**: grimm - PAI framework tools used by this tool
- **Development**: jbyrd - Independent development and enhancements
- **Community**: Red Hat TAM community for feedback and requirements

---

**🤖 TAM Automation Assistant**  
*Making your life easier, one report at a time*

**💝 Built with passion for helping TAMs succeed**