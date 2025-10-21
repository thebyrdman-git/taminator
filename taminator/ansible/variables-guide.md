# TAM RFE Automation Tool - Ansible Variables Guide

## 🎯 Overview

This guide will walk you through all the variables needed for the Ansible deployment, even if you've never used Ansible before. Don't worry - we'll make it simple!

## 📋 Required Variables

### **1. User Information**
```yaml
user_info:
  name: "Your Full Name"           # Your name (e.g., "John Smith")
  email: "your.email@redhat.com"   # Your Red Hat email address
  role: "TAM"                      # Your role (usually "TAM")
  team: "Your Team Name"           # Your team (e.g., "North America TAM Team")
```

### **2. Customer Information**
```yaml
customers:
  - name: "Customer Name"          # Customer company name
    account_number: "123456"       # Red Hat account number
    group_id: "789012"             # Customer portal group ID
    sbr_groups:                    # SBR groups for this customer
      - "Ansible"
      - "Ansible Automation Platform"
    primary_contact: "contact@customer.com"  # Primary customer contact
```

### **3. System Configuration**
```yaml
system_config:
  install_directory: "/home/yourusername/tam-rfe-automation"  # Where to install
  python_version: "3.7"           # Python version to use
  create_desktop_shortcut: true   # Create desktop shortcut (true/false)
  create_symlinks: true           # Create command shortcuts (true/false)
```

### **4. Red Hat Configuration**
```yaml
redhat_config:
  vpn_required: true              # Red Hat VPN required (true/false)
  rhcase_required: true           # rhcase tool required (true/false)
  portal_access: true             # Customer portal access (true/false)
  api_credentials_required: true  # API credentials needed (true/false)
```

### **5. Notification Settings**
```yaml
notifications:
  email: true                     # Email notifications (true/false)
  slack: false                    # Slack notifications (true/false)
  portal: true                    # Portal notifications (true/false)
  email_address: "your.email@redhat.com"  # Your email for notifications
```

## 🚀 Interactive Variable Setup

### **Step 1: Basic Information**
The system will ask you:
- What's your full name?
- What's your Red Hat email address?
- What's your role? (usually "TAM")
- What team are you on?

### **Step 2: Customer Setup**
For each customer, you'll be asked:
- What's the customer's company name?
- What's their Red Hat account number?
- What's their customer portal group ID?
- Which SBR groups do they use?
- Who's the primary contact?

### **Step 3: System Preferences**
You'll be asked:
- Where should we install the tool? (default is recommended)
- Do you want a desktop shortcut? (yes/no)
- Do you want command shortcuts? (yes/no)

### **Step 4: Red Hat Access**
You'll be asked:
- Do you have Red Hat VPN access? (yes/no)
- Do you have the rhcase tool? (yes/no)
- Do you have customer portal access? (yes/no)
- Do you need API credentials? (yes/no)

### **Step 5: Notifications**
You'll be asked:
- Do you want email notifications? (yes/no)
- Do you want Slack notifications? (yes/no)
- Do you want portal notifications? (yes/no)
- What's your email address for notifications?

## 🛠️ How to Set Variables

### **Method 1: Interactive Setup (Recommended)**
Run the setup script and answer the questions:
```bash
./setup-variables.sh
```

### **Method 2: Edit Configuration File**
Edit the variables file directly:
```bash
nano ansible/group_vars/all.yml
```

### **Method 3: Command Line**
Set variables when running the playbook:
```bash
ansible-playbook -i inventory.yml playbook.yml -e "user_name=John Smith" -e "user_email=john.smith@redhat.com"
```

## 📝 Example Configuration

Here's a complete example of what your variables file might look like:

```yaml
# User Information
user_info:
  name: "John Smith"
  email: "john.smith@redhat.com"
  role: "TAM"
  team: "North America TAM Team"

# Customer Information
customers:
  - name: "Acme Corporation"
    account_number: "123456"
    group_id: "789012"
    sbr_groups:
      - "Ansible"
      - "Ansible Automation Platform"
    primary_contact: "it-team@acme.com"
  
  - name: "Global Tech Solutions"
    account_number: "654321"
    group_id: "210987"
    sbr_groups:
      - "OpenShift"
      - "OpenShift Container Platform"
    primary_contact: "devops@globaltech.com"

# System Configuration
system_config:
  install_directory: "/home/john.smith/tam-rfe-automation"
  python_version: "3.7"
  create_desktop_shortcut: true
  create_symlinks: true

# Red Hat Configuration
redhat_config:
  vpn_required: true
  rhcase_required: true
  portal_access: true
  api_credentials_required: true

# Notification Settings
notifications:
  email: true
  slack: false
  portal: true
  email_address: "john.smith@redhat.com"
```

## 🔍 Variable Validation

The system will automatically check:
- ✅ Required fields are filled in
- ✅ Email addresses are valid format
- ✅ Account numbers are numeric
- ✅ Group IDs are valid format
- ✅ SBR groups are from the approved list
- ✅ File paths are valid
- ✅ Boolean values are true/false

## 🆘 Getting Help

If you need help with any variable:
1. Run the interactive setup: `./setup-variables.sh`
2. Check the examples in this guide
3. Ask your TAM manager for assistance
4. Contact the tool support team

## 🎯 Next Steps

After setting up your variables:
1. Review your configuration
2. Run the Ansible playbook
3. Test the installation
4. Start using the tool!

---

**💝 Remember: This tool was built with passion for helping new TAMs succeed. Don't hesitate to ask for help!**
