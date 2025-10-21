# Brand New TAM Guide - Complete Step-by-Step Process

## 🎯 You're a Brand New TAM - Here's Everything You Need to Know

**Welcome! This guide assumes you have ZERO experience with:**
- Cursor IDE
- AI development
- This RFE automation tool
- Red Hat development tools
- Command line interfaces

**Don't worry - we'll walk through everything step by step!**

---

## 📋 STEP 1: Understanding What This Tool Does

### What is an RFE/Bug Report?
- **RFE** = Request for Enhancement (new features you want)
- **Bug** = Problems that need fixing
- **TAMs** create reports showing customers what Red Hat is working on for them

### What This Tool Does for You
**BEFORE (Manual Process - 2-3 hours per customer per week):**
1. Log into Red Hat systems
2. Search for cases manually
3. Copy/paste case information
4. Format into tables
5. Post to customer portal
6. Send email notifications

**AFTER (Automated Process - 5 minutes per customer per week):**
1. Run one command
2. Tool does everything automatically
3. Get professional reports posted to customer portal
4. Receive email confirmation

### Time Savings
- **Per customer per week**: 2-3 hours → 5 minutes (95% reduction)
- **Per TAM per week**: 8-12 hours → 20 minutes (95% reduction)
- **Per TAM per year**: 400-600 hours → 17 hours (95% reduction)

---

## 🖥️ STEP 2: System Requirements

### What You Need on Your Computer
- **Operating System**: Windows, Mac, or Linux
- **Internet Connection**: For Red Hat VPN and tools
- **Red Hat VPN Access**: Required for accessing Red Hat systems
- **Basic Computer Skills**: Opening programs, typing commands

### What You DON'T Need
- ❌ Programming experience
- ❌ AI development knowledge
- ❌ Advanced technical skills
- ❌ Previous experience with automation tools

---

## 🔧 STEP 3: Installing Cursor IDE (Your AI-Powered Editor)

### What is Cursor IDE?
- **Cursor** = A smart code editor that helps you work with AI
- **Think of it like**: Microsoft Word, but for code and AI assistance
- **Why we use it**: It makes working with AI tools much easier

### Installation Steps

#### For Windows:
1. **Go to**: https://cursor.sh/
2. **Click**: "Download for Windows"
3. **Run the installer**: Double-click the downloaded file
4. **Follow the prompts**: Click "Next" through the installation
5. **Launch Cursor**: Look for the Cursor icon on your desktop

#### For Mac:
1. **Go to**: https://cursor.sh/
2. **Click**: "Download for Mac"
3. **Open the downloaded file**: It will be in your Downloads folder
4. **Drag Cursor to Applications**: Follow the on-screen instructions
5. **Launch Cursor**: Find it in your Applications folder

#### For Linux:
1. **Go to**: https://cursor.sh/
2. **Click**: "Download for Linux"
3. **Follow the installation instructions** for your Linux distribution

### First Time Setup in Cursor
1. **Open Cursor**
2. **Sign in or create account** (free account is fine)
3. **Accept the terms** and complete setup
4. **You're ready!** Cursor will look like a text editor with AI features

---

## 🐍 STEP 4: Installing Python (The Language This Tool Uses)

### What is Python?
- **Python** = A programming language (don't worry, you won't need to learn it)
- **Think of it like**: The engine that runs this tool
- **Why we need it**: The RFE automation tool is built with Python

### Installation Steps

#### For Windows:
1. **Go to**: https://www.python.org/downloads/
2. **Click**: "Download Python 3.11" (or latest version)
3. **Run the installer**: Double-click the downloaded file
4. **IMPORTANT**: Check "Add Python to PATH" during installation
5. **Click**: "Install Now"
6. **Wait for installation** to complete

#### For Mac:
1. **Open Terminal** (press Cmd + Space, type "Terminal")
2. **Install Homebrew** (if you don't have it):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. **Install Python**:
   ```bash
   brew install python
   ```

#### For Linux:
1. **Open Terminal**
2. **Install Python**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

### Verify Python Installation
1. **Open Terminal** (Windows: Command Prompt, Mac/Linux: Terminal)
2. **Type**: `python --version`
3. **You should see**: Python 3.x.x (some version number)
4. **If you see an error**: Python didn't install correctly, try again

---

## 🔴 STEP 5: Setting Up Red Hat Tools

### What You Need from Red Hat
- **Red Hat VPN Access**: To connect to Red Hat systems
- **rhcase Tool**: Red Hat's case management tool
- **Customer Portal Access**: To post reports to customer groups
- **AI Models API Access**: For the AI features (your manager can help with this)

### Installing rhcase Tool
1. **Connect to Red Hat VPN** (ask your manager how to do this)
2. **Open Terminal/Command Prompt**
3. **Install rhcase**:
   ```bash
   pip install rhcase
   ```
4. **Test installation**:
   ```bash
   rhcase --help
   ```
5. **You should see**: Help information for rhcase commands

### Getting Customer Portal Access
1. **Ask your manager** for customer portal group IDs
2. **Get API credentials** for posting reports
3. **Test access** by logging into https://access.redhat.com/

---

## 📁 STEP 6: Getting the RFE Automation Tool

### Download the Tool
1. **Open Cursor IDE**
2. **Open Terminal in Cursor** (View → Terminal)
3. **Navigate to where you want the tool**:
   ```bash
   cd ~/Documents  # or wherever you want to store it
   ```
4. **Clone the tool** (ask your manager for the repository URL):
   ```bash
   git clone <repository-url>
   cd rfe-bug-tracker
   ```

### What You Just Downloaded
- **rfe-bug-tracker folder**: Contains all the tool files
- **bin folder**: Contains the commands you'll run
- **docs folder**: Contains documentation and guides
- **persona folder**: Contains the AI personality settings

---

## 🚀 STEP 7: First Time Setup (Onboarding)

### Run the Intelligent Onboarding
1. **In Terminal, make sure you're in the tool directory**:
   ```bash
   cd rfe-bug-tracker
   ```
2. **Run the onboarding script**:
   ```bash
   ./bin/tam-rfe-onboard-intelligent
   ```

### What the Onboarding Will Ask You
The tool will ask you questions to learn your preferences:

1. **Your Name**: So it can personalize responses
2. **Your Customers**: Which customers you work with
3. **Account Numbers**: For each customer
4. **Group IDs**: For customer portal posting
5. **SBR Groups**: Which Red Hat products you focus on
6. **Report Preferences**: How you like reports formatted
7. **Notification Preferences**: How you want to be notified

### Example Onboarding Session
```
🤖 TAM Automation Assistant: Welcome! Let's set up your preferences.

What's your name? John Smith
Which customers do you work with? Wells Fargo, TD Bank
What's Wells Fargo's account number? 838043
What's Wells Fargo's group ID? 4357341
Which SBR groups do you focus on? Ansible, OpenShift
How do you like reports formatted? Standard format
How do you want notifications? Email

✅ Setup complete! You're ready to use the tool.
```

---

## 💬 STEP 8: Using the Tool (Your First Report)

### Start the Chat Interface
1. **In Terminal, make sure you're in the tool directory**:
   ```bash
   cd rfe-bug-tracker
   ```
2. **Start the chat interface**:
   ```bash
   ./bin/tam-rfe-chat
   ```

### Your First Report Request
The tool will guide you through a simple conversation:

```
🤖 TAM Automation Assistant: Hi John! How can I help you today?

You: Generate RFE report for Wells Fargo

🤖 TAM Automation Assistant: I'd be happy to generate reports! Let me show you the options.

📋 Report Generation - Multiple Choice:

1. Which type of report do you want?
   [1] Active Case Report only
   [2] RFE/Bug Tracker Report only
   [3] Both reports (Active Case + RFE/Bug Tracker)

Your choice: 2

2. Which customer do you want the report for?
   [1] Wells Fargo (Account: 838043, Group: 4357341)
   [2] TD Bank (Account: 1912101, Group: 7028358)
   [3] Other customer (specify)

Your choice: 1

3. Which SBR groups should I focus on?
   [1] Ansible only (recommended for your setup)
   [2] Ansible + OpenShift
   [3] All SBR groups
   [4] Custom selection (specify)

Your choice: 1

📋 Let me confirm all details:
   • Report Type: RFE/Bug Tracker Report only
   • Customer: Wells Fargo
   • Account Number: 838043
   • Group ID: 4357341
   • SBR Groups: Ansible, Ansible Automation Platform

Is this correct before I generate the report? y

✅ Confirmed! Generating RFE/Bug Tracker Report for Wells Fargo...

📊 Generating report...
✅ Report Generated Successfully!

📋 Here are your delivery options:

📋 Option 1: Copy/Paste Markdown Template
   • I'll display the complete markdown report in this chat
   • You can copy the entire report and paste it directly into:
     - Customer portal group discussions
     - Email communications
     - Documentation systems
   • Full control over posting timing and content review

📋 Option 2: Automatic Portal Posting
   • I'll automatically post the report to the customer portal group
   • Uses your configured group ID and Red Hat API credentials
   • Immediate posting with professional formatting
   • Email notification sent to you with posting confirmation

Which option would you prefer? (1 for Copy/Paste, 2 for Auto-Post, or 'both' to see both options)

Your choice: 2

✅ Posting report to Wells Fargo customer portal...
✅ Report posted successfully! Check your email for confirmation.
```

---

## 📊 STEP 9: Understanding the Report Output

### What You Get
The tool generates professional reports with:

1. **Executive Summary**: High-level overview of cases
2. **Active RFE Cases**: New feature requests in progress
3. **Active Bug Cases**: Issues being worked on
4. **Closed Case History**: Recently completed work
5. **Trends and Insights**: Analysis of case patterns

### Sample Report Structure
```markdown
# Wells Fargo - RFE/Bug Tracker Report
**Generated**: December 15, 2024
**Time Period**: Last 30 days
**SBR Groups**: Ansible, Ansible Automation Platform

## Executive Summary
- **Total Active Cases**: 12
- **High Priority Cases**: 3
- **Cases Closed This Month**: 8
- **Average Resolution Time**: 15 days

## Active RFE Cases
| Case # | Summary | Status | Priority | SBR Group |
|--------|---------|--------|----------|-----------|
| 123456 | Ansible Tower integration | In Progress | High | Ansible |
| 123457 | Automation workflow | Open | Medium | Ansible |

## Active Bug Cases
| Case # | Summary | Status | Priority | SBR Group |
|--------|---------|--------|----------|-----------|
| 123458 | Performance issue | Waiting on Red Hat | High | Ansible |
| 123459 | UI bug | In Progress | Medium | Ansible |

## Closed Case History
| Case # | Summary | Resolution | Closed Date |
|--------|---------|------------|-------------|
| 123460 | Feature request | Delivered | Dec 10, 2024 |
| 123461 | Bug fix | Resolved | Dec 8, 2024 |
```

---

## 🔧 STEP 10: Common Tasks and Commands

### Daily Workflow
```bash
# Start your day
cd rfe-bug-tracker
./bin/tam-rfe-chat

# Ask for reports
"Generate RFE report for Wells Fargo"
"Show me all Ansible cases for TD Bank"
"Prepare summary for JPMC quarterly meeting"
```

### Weekly Tasks
```bash
# Generate weekly reports for all customers
./bin/tam-rfe-monitor-simple --all

# Check system status
./bin/tam-rfe-verify --quick
```

### Troubleshooting
```bash
# Test the system
./bin/tam-rfe-verify --full

# Get help
./bin/tam-rfe-chat --help
```

---

## 🆘 STEP 11: Getting Help When You Need It

### Common Issues and Solutions

#### "The tool won't start"
- **Check**: Are you in the right directory? (`cd rfe-bug-tracker`)
- **Check**: Is Python installed? (`python --version`)
- **Check**: Are you connected to Red Hat VPN?

#### "I can't find cases"
- **Check**: Is rhcase working? (`rhcase --help`)
- **Check**: Are you connected to Red Hat VPN?
- **Check**: Are the account numbers correct?

#### "The report looks wrong"
- **Check**: Are the SBR groups correct?
- **Check**: Is the time range appropriate?
- **Ask**: Use the chat interface to ask for adjustments

#### "I can't post to the customer portal"
- **Check**: Do you have API credentials?
- **Check**: Is the group ID correct?
- **Alternative**: Use the copy/paste option instead

### Who to Ask for Help
1. **Your TAM Manager**: For Red Hat access and credentials
2. **The Tool's Chat Interface**: Ask the AI assistant for help
3. **Documentation**: Check the docs folder for detailed guides
4. **Other TAMs**: Who are already using the tool

### Getting More Advanced
Once you're comfortable with the basics:
- **Customize templates**: Use `./bin/tam-rfe-template-customizer`
- **Set up automation**: Use `./bin/tam-rfe-schedule`
- **Monitor performance**: Use `./bin/tam-rfe-monitor-intelligent`

---

## 🎉 STEP 12: You're Ready!

### What You've Accomplished
- ✅ Installed Cursor IDE
- ✅ Installed Python
- ✅ Set up Red Hat tools
- ✅ Downloaded the RFE automation tool
- ✅ Completed onboarding
- ✅ Generated your first report
- ✅ Learned the basic workflow

### Your New Workflow
**Instead of spending 2-3 hours per customer per week:**
1. Open Terminal
2. Run `./bin/tam-rfe-chat`
3. Ask for reports using natural language
4. Pick options from multiple choice menus
5. Get professional reports in 5 minutes

### Next Steps
1. **Practice**: Generate reports for all your customers
2. **Customize**: Adjust templates to match your style
3. **Automate**: Set up scheduled reports
4. **Share**: Tell other TAMs about the tool
5. **Improve**: Provide feedback to make the tool better

---

## 📞 Quick Reference

### Essential Commands
```bash
# Start the tool
./bin/tam-rfe-chat

# Test the system
./bin/tam-rfe-verify --quick

# Get help
./bin/tam-rfe-chat --help

# Generate reports for all customers
./bin/tam-rfe-monitor-simple --all
```

### Common Chat Requests
- "Generate RFE report for [Customer]"
- "Show me all Ansible cases for [Customer]"
- "Prepare summary for [Customer] quarterly meeting"
- "Create active case report for [Customer]"
- "Help me customize my report template"

### Emergency Contacts
- **Your TAM Manager**: For Red Hat access issues
- **Tool Documentation**: Check the docs folder
- **AI Assistant**: Ask the chat interface for help

---

**🎉 Congratulations! You're now ready to use the TAM RFE Automation Tool like a pro!**

**Remember**: The tool is designed to be simple and user-friendly. If you get stuck, just ask the AI assistant for help - it's there to guide you through everything.

---

*🤖 TAM Automation Assistant - Making your life easier, one report at a time*
