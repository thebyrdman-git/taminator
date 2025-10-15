# TAM RFE Automation Tool

## 🎯 Overview

**This is the TAM RFE Automation Tool, developed by jbyrd as a standalone, self-contained solution that uses tools from [grimm's PAI project](https://gitlab.cee.redhat.com/gvaughn/hatter-pai). This IS the RFE automation tool itself.**

**The tool automatically generates and posts professional RFE/Bug tracker reports and Active Case reports to Customer Portal Groups, saving TAMs 2-3 hours per customer per week.**

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

**Complete installation in under 5 minutes:**

```bash
# 1. Clone the repository
git clone https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation.git
cd rfe-and-bug-tracker-automation

# 2. Run the automated installer (no sudo needed!)
./install-improved.sh

# 3. Start using the tool
./bin/tam-rfe-chat
```

**For detailed setup:** → [**GETTING-STARTED.md**](GETTING-STARTED.md)

### What You Need (Minimal!)
- Red Hat laptop with internet connection
- Red Hat VPN access (see connection instructions below)
- `git` (usually pre-installed on RHEL/Fedora)
- `python3` 3.8+ (usually pre-installed on RHEL/Fedora)
- Your Red Hat login credentials for GitLab

**That's it!** No sudo, no build tools, no system packages required.

**Optional (Recommended)**:
- Cursor IDE with enterprise license (for best experience)

### 🔐 **Connect to Red Hat VPN (Required)**

**Before using the tool, you must be connected to Red Hat VPN:**

**Follow the official Red Hat VPN setup instructions:**
- **CSB (Corporate Standard Build) laptops**: https://redhat.service-now.com/help?id=kb_article_view&sysparm_article=KB0005449&sys_kb_id=1125a41b136f6640daa77b304244b0e9
- **Non-CSB Linux builds**: https://redhat.service-now.com/help?id=kb_article_view&sysparm_article=KB0005424&sys_kb_id=a7cb24531b1e5cd0aa0f960abc4bcb25

#### **Test VPN Connection:**
```bash
# Test if you can access Red Hat internal sites
curl -I https://source.redhat.com
```
*Should return HTTP 200 or 302 (not connection refused)*

### 📥 **Step 1: Get the Tool**

**Clone from GitLab:**
```bash
git clone https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation.git
cd rfe-and-bug-tracker-automation
```

**Or download ZIP:**
1. Go to: https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation
2. Click the green "Clone" button → "Download ZIP"
3. Extract to a folder (like `~/rfe-automation`)
4. `cd` into that folder

### 🔧 **Installation (One Command - Fully Automated)**

**Zero-dependency-hell installation. Just run:**
```bash
./install-improved.sh
```

**That's it!** The installer:
- ✅ **Fully automated** - No user interaction required
- ✅ **No sudo needed** - Works on locked-down laptops
- ✅ **User-space only** - No system packages touched
- ✅ **Smart fallback** - Tries UV (fast), falls back to pip+venv
- ✅ **Auto-clones rhcase** - Gets latest from GitLab
- ✅ **Clear errors** - Helpful messages if something goes wrong

**Requirements** (usually already installed):
- `git` - For cloning repositories
- `python3` (3.8+) - Runtime environment
- Red Hat VPN - For accessing internal GitLab

**Installation time**: 2-5 minutes

**For more details**: See [INSTALLATION-REQUIREMENTS.md](INSTALLATION-REQUIREMENTS.md)

**⚠️ IMPORTANT: GitLab CEE License Required**
- **First-time access**: You have a 10-minute timer for viewing the site before your non-licensed access is denied
- **License request**: Must be completed during your first login session
- **Getting access guide**: https://source.redhat.com/groups/public/gitlabcee/user_documentation/getting_started_guide#getting-access

**GitLab.cee License Request Form Information:**
When filling out the license request form, you'll need to provide:
- **# licenses requested**: 1
- **Username / Full name**: Your Red Hat username and full name
- **Projects to collaborate on**: rfe-and-bug-tracker-automation
- **Why access is required**: Collaborating with group and need ability to update GitLab repos
- **How long you need access**: Permanent access

### 💻 **Optional: Install Cursor IDE (Recommended)**

**For the best experience, install Cursor IDE with Red Hat enterprise license:**

**⚠️ IMPORTANT: You must be connected to Red Hat VPN first!**

#### **Step-by-Step Cursor License and Installation Process:**

1. **Connect to Red Hat VPN** (see VPN connection instructions above)
2. **Submit license request**: https://devservices.dpp.openshift.com/support/cursor_license_request/
3. **Check your email** - You'll receive an email with a login link
4. **Click the email link** - You'll be taken to a login page
5. **Enter your Red Hat email address** (your @redhat.com email)
6. **Complete SSO login** - You'll be redirected to Red Hat SSO for authentication
7. **Accept the invitation** - You'll see a prompt to accept the Cursor license invitation
8. **Download Cursor IDE**:
   - Click your **profile icon** (top right corner)
   - Select **"Download desktop client"** for your OS (RHEL/Fedora/Mac)
9. **Install Cursor IDE**:
   - **For AppImage files** (Linux): Right-click the downloaded file → Properties → Permissions → Check "Execute" or run: `chmod +x cursor-*.AppImage`
   - **For other formats**: Follow standard installation procedures for your OS
10. **Open the RFE automation tool folder** in Cursor for enhanced AI assistance
11. **Customize your experience** (optional):
    - Install relevant Cursor extensions from the Extensions marketplace
    - Popular extensions: Python, Git, Markdown, YAML, JSON formatters
    - Feel free to install any extensions that enhance your developer workflow

#### **Additional Resources:**
- **Setup guide**: https://source.redhat.com/projects_and_programs/ai/ai_tools/cursor#getting-started

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

**Step 3: Install dependencies**
```bash
./bin/install-dependencies
```
*This installs everything you need automatically*

**Step 4: Run the setup wizard**
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

### 📋 **After Setup, You Have 3 Easy Options**

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

**Option 3: Validate Before Using (Recommended)**
```bash
./bin/validate-rfe-reports wellsfargo
```
*This checks both system functionality and report content accuracy*

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

**You get 3 options:**
1. **Copy the report** - Tool shows you the text, you copy and paste it anywhere
2. **Auto-post** - Tool automatically puts it on the customer portal (you get an email confirmation)
3. **Validate first** - Check report accuracy before publishing (recommended)

## 🔍 **How Filtering Works (Sets Your Expectations)**

The tool generates **two different types of reports** with different filtering logic:

### **📊 RFE/Bug Tracker Report**
**What it includes:**
- ✅ All cases with `[RFE]` in the title (Feature Requests)
- ✅ All cases with `[BUG]` in the title (Bug Reports)
- ✅ Recent closed cases for historical context

**What it excludes:**
- ❌ Cases without `[RFE]` or `[BUG]` in the title
- ❌ Configuration issues, account service requests, etc.

### **📋 Active Cases Report**
**What it includes:**
- ✅ All active cases EXCEPT those with `[RFE]` or `[BUG]` in the title
- ✅ Configuration issues, account service requests, support cases
- ✅ Any other active cases that aren't explicitly RFE or Bug

**What it excludes:**
- ❌ Cases with `[RFE]` in the title
- ❌ Cases with `[BUG]` in the title
- ❌ Cases with external tracker references (`issues.redhat.com` or `jira.redhat.com` URLs in subject, description, or tags)

### **🔍 External Tracker Detection**
The tool automatically detects cases that are tracked in external systems (like JIRA) by searching for patterns in:
- **Subject/Title**: `issues.redhat.com` or `jira.redhat.com` URLs
- **Description**: Same patterns as above  
- **Tags**: Same patterns as above

**Example**: Case 03208295 contains `https://issues.redhat.com/browse/AAP-3456` in the description field.

Cases with external tracker references are excluded from the Active Cases Report to avoid duplication with formal tracking systems.

### **🎯 Why This Matters**
- **RFE/Bug Report**: Focuses on feature requests and bug reports for product development
- **Active Cases Report**: Shows operational issues, configuration problems, and support requests
- **External Tracker Detection**: Prevents duplicate tracking of cases already managed in JIRA or other systems
- **Together**: They give you a complete picture of all customer cases without duplication

## 📋 Report Options

When you ask for reports, I'll give you **three options**:

1. **Copy/Paste** - I show you the markdown, you paste it wherever you need it
2. **Auto-Post** - I automatically post to the customer portal
3. **Validate First** - Check report accuracy before publishing (recommended)

## 🔍 Report Validation (NEW!)

**Ensure your reports are accurate and professional:**

### Quick Validation
```bash
# Validate everything for a customer
./bin/validate-rfe-reports wellsfargo

# Check system functionality only
./bin/validate-rfe-reports --system-only

# Check report content accuracy only
./bin/validate-rfe-reports wellsfargo --content-only
```

### What Validation Checks
- **System Health**: Connectivity, authentication, dependencies
- **Content Accuracy**: Case numbers, RFE IDs, data consistency
- **Quality Score**: 99%+ accuracy required for customer reports
- **Issue Detection**: Identifies problems before customers see them

### Validation Results (Enterprise Standards)
- **✅ 99%+ Accuracy**: Report ready for customer distribution
- **⚠️ 95-98% Accuracy**: Acceptable for internal use, review before customer distribution
- **❌ <95% Accuracy**: Fix issues before any distribution

**📚 For detailed validation guide**: See `docs/REPORT-VALIDATION-GUIDE.md`

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
  - Make sure you're connected to Red Hat VPN (see VPN connection instructions above)
  - Test VPN connection: `curl -I https://source.redhat.com` (should return HTTP 200/302)
  - Run the dependency installer again: `./bin/install-dependencies`
  - Test rhcase works: type `./rhcase/rhcase --version` in terminal
  - Try: `./rhcase/rhcase list [customer-name] --months 1` to see if it finds cases
  - If rhcase doesn't work, contact grimm (rhcase creator) via GitLab: https://gitlab.cee.redhat.com/gvaughn/rhcase/-/issues
- **"Python packages missing"** → Install with: `pip3 install requests` or see: https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/installing_and_using_dynamic_programming_languages/installing-and-using-python
- **"Git not configured"** → Set up with: `git config --global user.name "Your Name"` or see: https://source.redhat.com/groups/public/gitlabcee/user_documentation/getting_started_guide
- **"I can't find customer account numbers"** → Check your customer portal or ask your manager
- **"I want to change how reports look"** → Use the chat and ask: "Can you customize the report format?"
- **"I'm stuck!"** → Use the chat and type: "Help me" or "I need assistance"
- **"Can't access Cursor license request page"** → Make sure you're connected to Red Hat VPN first, then try: https://devservices.dpp.openshift.com/support/cursor_license_request/ (if still having issues on CSB laptops, contact Red Hat IT support or check the official Cursor setup documentation)
- **"RFE tool issues"** → Contact jbyrd (RFE tool developer) via GitLab: https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation/-/issues

### Getting Support
- **Slack**: #tam-automation-tools
- **Email**: tam-automation-team@redhat.com
- **Developer**: jbyrd@redhat.com

## 🎉 Ready to Start?

### For All Users

**Step 1: Open Terminal**
- RHEL/Fedora: Press `Ctrl + Alt + T` or click Activities → Terminal
- Mac: Press `Cmd + Space`, type "Terminal", press Enter

**Step 2: Install Dependencies (One Time Only)**
```bash
./bin/install-dependencies
```
*This installs everything you need automatically*

**Step 3: Run Setup (One Time Only)**
```bash
./bin/tam-rfe-onboard-intelligent
```
*Answer the questions about your customers*

**Step 4: Start Using It**
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

## 🤝 Contributing to Improve Report Consistency

### 🎯 **Why Your Contribution Matters**
This tool generates reports that represent Red Hat to customers. Your input helps ensure:
- **Consistent formatting** across all TAM reports
- **Professional presentation** that reflects well on Red Hat
- **Accurate case information** and proper categorization
- **Customer-appropriate content** for different audiences

### 📋 **How TAMs Can Contribute**

#### **Report Quality & Consistency**
- **Test reports with your customers** and share feedback
- **Report formatting issues** via GitLab issues
- **Suggest improvements** to report templates and content
- **Share successful customer feedback** about report quality

#### **Customer-Specific Templates**
- **Contribute customer templates** that work well for specific industries
- **Share best practices** for different customer types (enterprise, government, etc.)
- **Provide examples** of well-received reports

#### **Case Categorization & Filtering**
- **Report incorrect case categorization** (wrong SBR groups, status, etc.)
- **Suggest better filtering options** for different report types
- **Share insights** about which cases customers find most valuable

#### **User Experience**
- **Report usability issues** or confusing parts of the tool
- **Suggest workflow improvements** based on your daily usage
- **Share time-saving tips** with other TAMs

### 🔧 **How to Contribute**

#### **Quick Feedback (5 minutes)**
```bash
# After generating a report, provide feedback
./bin/tam-rfe-feedback
```
*This opens a quick feedback form to report issues or suggestions*

#### **Detailed Contributions**
1. **Create GitLab Issue**: https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation/-/issues
2. **Use issue templates** for:
   - Report formatting problems
   - Case categorization issues
   - Customer feedback
   - Feature requests

#### **Share Success Stories**
- **Email**: jbyrd@redhat.com with subject "RFE Tool Success Story"
- **Include**: Customer name (anonymized), what worked well, time saved

### 🎯 **Priority Contribution Areas**

#### **High Priority (Report Quality)**
- **Case status accuracy** - Are cases showing correct status?
- **SBR group categorization** - Are cases in the right groups?
- **Report formatting** - Does the output look professional?
- **Customer feedback** - What do customers say about the reports?

#### **Medium Priority (Usability)**
- **Setup process** - Is the onboarding clear and easy?
- **Error messages** - Are they helpful and actionable?
- **Documentation** - What's missing or confusing?

#### **Low Priority (Enhancements)**
- **New report types** - What additional reports would be valuable?
- **Integration ideas** - How could this work better with other tools?
- **Automation opportunities** - What manual steps could be automated?

### 📊 **Contribution Impact**

**Your contributions directly improve:**
- **Report consistency** across all TAMs
- **Customer satisfaction** with Red Hat communication
- **TAM productivity** and time savings
- **Professional presentation** of Red Hat services

### 🚀 **Getting Started with Contributions**

1. **Use the tool** for a week with your customers
2. **Note any issues** with report quality or formatting
3. **Collect customer feedback** about the reports
4. **Share your findings** via GitLab issues or email
5. **Help other TAMs** by sharing successful approaches

**Every contribution, no matter how small, helps make this tool better for all TAMs and ensures consistent, professional customer communication.**

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