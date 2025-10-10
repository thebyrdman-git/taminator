# TAM RFE Automation Tool - Quick Start Guide

## 🎯 What This Tool Does

**Automatically generates and posts RFE/Bug reports to customer portals, saving you 2-3 hours per customer per week.**

## 🚀 Quick Start (5 Minutes)

### 1. Install & Setup
```bash
# Clone the tool
git clone <repository-url>
cd rfe-bug-tracker

# Run intelligent onboarding
./bin/tam-rfe-onboard-intelligent
```

### 2. Use the Tool
```bash
# Start the chat interface
./bin/tam-rfe-chat

# Then ask naturally:
# "Generate RFE report for Wells Fargo"
# "Create active case report for TD Bank"
```

## 💬 How to Use

### Option 1: Chat Interface (Recommended)
```bash
./bin/tam-rfe-chat
```
**Ask me anything:**
- "Generate RFE report for Wells Fargo"
- "Show me all Ansible cases for TD Bank"
- "Prepare summary for JPMC quarterly meeting"

### 🎯 Comprehensive Multiple Choice System
**When you ask for reports, I'll guide you through 9 simple choices:**
1. **Report Type**: Active Case, RFE/Bug Tracker, or Both
2. **Customer**: Wells Fargo, TD Bank, JPMC, Fannie Mae, or Other
3. **SBR Groups**: Ansible only, Ansible + OpenShift, All SBR groups, or Custom
4. **Time Range**: Last 7 days, 30 days, 90 days, 6 months, or Custom
5. **Case Status**: Active only, All cases, Closed only, High priority, or Custom
6. **Report Format**: Standard, Executive, Technical, Customer-friendly, or Custom
7. **Priority Levels**: High only, High + Medium, All levels, Critical only, or Custom
8. **Case Types**: RFE only, Bug only, Both, Enhancement only, or Critical only
9. **Delivery Method**: Copy/Paste, Auto-Post, Both, Email, or Multiple destinations

**Just pick numbers - no typing required!**

### Option 2: Direct Commands
```bash
# Generate reports
./bin/tam-rfe-monitor-simple wellsfargo --test
./bin/tam-rfe-monitor-simple tdbank --test

# Run all customers
./bin/tam-rfe-monitor-simple --all
```

## 📋 Report Options

When you ask for reports, I'll give you **two options**:

### Option 1: Copy/Paste
- I show you the markdown report
- You copy and paste it wherever you need it
- Full control over timing and content

### Option 2: Auto-Post
- I automatically post to the customer portal
- Immediate posting with email confirmation
- Perfect for automated workflows

## 🎯 What You Need

### Required
- Red Hat VPN connection
- `rhcase` tool installed
- Python 3.7+

### Optional (for auto-posting)
- Red Hat Customer Portal API credentials
- Customer portal group IDs

## 🆘 Need Help?

### Quick Commands
```bash
# Test the system
./bin/tam-rfe-verify --quick

# Get help
./bin/tam-rfe-chat --help
./bin/tam-rfe-onboard-intelligent --help
```

### Common Questions
- **"How do I add a new customer?"** → Run `./bin/tam-rfe-onboard-intelligent`
- **"The tool isn't finding cases"** → Check your `rhcase` configuration
- **"I want to customize the reports"** → Use the chat interface and ask me to modify them

## 📊 Time Savings

| Task | Before | After | Savings |
|------|--------|-------|---------|
| **Per Customer Per Week** | 2-3 hours | 5 minutes | 95% reduction |
| **Per TAM Per Week** | 8-12 hours | 20 minutes | 95% reduction |

## 🎉 Ready to Start?

### For Brand New TAMs (Zero Experience)
1. **Start chatting**: `./bin/tam-rfe-chat`
2. **Tell the AI**: "I'm new to this" or "I need help getting started"
3. **Follow the guided onboarding**: The AI will walk you through everything step by step
4. **Complete setup**: From installation to your first report

**💝 Special Note**: This tool was created with a passion for helping new TAMs succeed. The AI assistant is designed to be patient, encouraging, and supportive - just like having a knowledgeable mentor by your side!

### For Experienced TAMs
1. **Run onboarding**: `./bin/tam-rfe-onboard-intelligent`
2. **Start chatting**: `./bin/tam-rfe-chat`
3. **Ask for reports**: "Generate RFE report for [Customer]"

**That's it! The tool will learn your preferences and get smarter over time.**

---

**🤖 TAM Automation Assistant**  
*Making your life easier, one report at a time*
