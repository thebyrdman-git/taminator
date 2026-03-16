# TAM RFE Automation Tool - Ansible Deployment Guide

## 🎯 Overview

This guide will help you deploy the TAM RFE Automation Tool using Ansible, even if you've never used Ansible before. The deployment is designed to be simple and guided, with interactive setup for all required variables.

## 🚀 Quick Start

### **For Complete Beginners (Recommended)**
```bash
# 1. Run the interactive setup
./setup-variables.sh

# 2. Deploy with Ansible
./deploy-with-ansible.sh
```

### **For Users with Ansible Experience**
```bash
# 1. Configure variables
ansible-playbook -i ansible/inventory.yml ansible/playbook.yml
```

## 📋 What You Need

### **System Requirements**
- **Operating System**: Linux, macOS, or Windows
- **Python**: 3.7 or higher
- **Disk Space**: 2GB minimum
- **Memory**: 4GB minimum
- **Network**: Red Hat VPN access

### **Optional Requirements**
- **Ansible**: Will be installed automatically if not present
- **Cursor IDE**: Recommended for better experience
- **Red Hat Tools**: rhcase, customer portal access

## 🛠️ Step-by-Step Deployment

### **Step 1: Download the Tool**
```bash
# Clone or download the tool
git clone <repository-url>
cd tam-rfe-automation
```

### **Step 2: Run Interactive Setup**
```bash
# Make the script executable
chmod +x setup-variables.sh

# Run the interactive setup
./setup-variables.sh
```

The interactive setup will ask you:
- **Your Information**: Name, email, role, team
- **Customer Information**: Names, account numbers, group IDs, SBR groups
- **System Preferences**: Installation directory, shortcuts, Python version
- **Red Hat Access**: VPN, rhcase, portal access, API credentials
- **Notifications**: Email, Slack, portal notifications

### **Step 3: Deploy with Ansible**
```bash
# Make the script executable
chmod +x deploy-with-ansible.sh

# Run the deployment
./deploy-with-ansible.sh
```

The deployment will:
- ✅ Check system requirements
- ✅ Install dependencies
- ✅ Download and install the tool
- ✅ Configure Red Hat integration
- ✅ Set up user preferences
- ✅ Create shortcuts and symlinks
- ✅ Verify the installation

### **Step 4: Start Using the Tool**
```bash
# Start the chat interface
~/tam-rfe-automation/bin/tam-rfe-chat

# Or use the desktop shortcut (if created)
```

## 📝 Required Variables

### **1. User Information**
```yaml
user_info:
  name: "Your Full Name"
  email: "your.email@redhat.com"
  role: "TAM"
  team: "Your Team Name"
```

### **2. Customer Information**
```yaml
customers:
  - name: "Customer Name"
    account_number: "123456"
    group_id: "789012"
    sbr_groups:
      - "Ansible"
      - "Ansible Automation Platform"
    primary_contact: "contact@customer.com"
```

### **3. System Configuration**
```yaml
system_config:
  install_directory: "/home/yourusername/tam-rfe-automation"
  python_version: "3.7"
  create_desktop_shortcut: true
  create_symlinks: true
```

### **4. Red Hat Configuration**
```yaml
redhat_config:
  vpn_required: true
  rhcase_required: true
  portal_access: true
  api_credentials_required: true
```

### **5. Notification Settings**
```yaml
notifications:
  email: true
  slack: false
  portal: true
  email_address: "your.email@redhat.com"
```

## 🔧 Advanced Configuration

### **Custom Inventory**
Create a custom inventory file for multiple systems:
```yaml
# custom-inventory.yml
all:
  children:
    tam_workstations:
      hosts:
        workstation-01:
          ansible_host: 192.168.1.100
          ansible_user: tamuser1
        workstation-02:
          ansible_host: 192.168.1.101
          ansible_user: tamuser2
```

### **Custom Variables**
Override default variables:
```bash
ansible-playbook -i inventory.yml playbook.yml \
  -e "user_name=John Smith" \
  -e "user_email=john.smith@redhat.com" \
  -e "install_directory=/opt/tam-rfe-automation"
```

### **Dry Run**
Test the deployment without making changes:
```bash
./deploy-with-ansible.sh --check
```

## 🆘 Troubleshooting

### **Common Issues**

#### **Ansible Not Found**
```bash
# Install Ansible
pip3 install ansible

# Or on macOS
brew install ansible
```

#### **Python Version Issues**
```bash
# Check Python version
python3 --version

# Install Python 3.7+
# On Ubuntu/Debian
sudo apt install python3.7

# On macOS
brew install python@3.9
```

#### **Permission Denied**
```bash
# Make scripts executable
chmod +x setup-variables.sh
chmod +x deploy-with-ansible.sh

# Run with sudo if needed
sudo ./deploy-with-ansible.sh
```

#### **Red Hat VPN Issues**
```bash
# Check VPN connection
ping -c 1 access.redhat.com

# Connect to Red Hat VPN
# (Follow your organization's VPN setup instructions)
```

### **Getting Help**

1. **Check the logs**: `~/.config/tam-rfe-automation/ansible-deployment.log`
2. **Run in verbose mode**: `./deploy-with-ansible.sh --verbose`
3. **Contact your TAM manager**
4. **Check the documentation**: `docs/` directory

## 📚 Additional Resources

### **Documentation**
- **User Guide**: `docs/BRAND-NEW-TAM-GUIDE.md`
- **Getting Started**: `GETTING-STARTED.md`
- **Prerequisites**: `docs/PREREQUISITES-GUIDE.md`
- **Variables Guide**: `ansible/variables-guide.md`

### **Examples**
- **Wells Fargo Example**: `examples/WELLS-FARGO-EXAMPLE.md`
- **TD Bank Example**: `examples/TD-BANK-EXAMPLE.md`

### **Support**
- **Tool Chat Interface**: Run the tool and ask for help
- **TAM Manager**: Contact your TAM manager
- **Red Hat Support**: For Red Hat-specific issues

## 🎯 Success Criteria

After successful deployment, you should have:
- ✅ Tool installed in your chosen directory
- ✅ Desktop shortcut (if enabled)
- ✅ Command shortcuts (if enabled)
- ✅ User configuration file
- ✅ Customer information configured
- ✅ Red Hat integration working
- ✅ Notifications configured

## 💝 Built with Passion

This deployment system was created with a passion for helping new TAMs succeed. Every step is designed to be:
- **Simple**: Easy to follow, even for beginners
- **Guided**: Interactive setup with clear instructions
- **Comprehensive**: Covers all necessary configuration
- **Supportive**: Helpful error messages and troubleshooting

---

**🤖 TAM Automation Assistant - Making deployment easy, one step at a time**
