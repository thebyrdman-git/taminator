# RFE Automation Tool - Prerequisites & Setup Guide

## 🎯 Overview

This guide provides step-by-step instructions for setting up all prerequisites required to use the RFE Automation Tool, including Cursor IDE configuration, Red Hat tools, and system requirements.

## 📋 Prerequisites Checklist

- [ ] Red Hat laptop with terminal access
- [ ] Red Hat SSO credentials (`rhn-support-[username]`)
- [ ] Cursor IDE installed and configured
- [ ] `rhcase` tool installed and configured
- [ ] Python 3.8+ with required packages
- [ ] Red Hat AI models API access
- [ ] Customer portal group access
- [ ] Git access to Red Hat repositories

---

## 🖥️ System Requirements

### Operating System
- **Red Hat Enterprise Linux** (recommended)
- **Fedora** (supported)
- **macOS** (with Red Hat VPN)
- **Windows** (with WSL2 and Red Hat VPN)

### Hardware Requirements
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 10GB free space
- **Network**: Red Hat VPN access required

---

## 🔧 Cursor IDE Configuration

### Step 1: Install Cursor IDE

#### For Red Hat Enterprise Linux / Fedora
```bash
# Download Cursor IDE
curl -L https://downloader.cursor.sh/linux/appImage/x64 -o cursor.AppImage

# Make executable
chmod +x cursor.AppImage

# Create symlink for easy access
sudo ln -s $(pwd)/cursor.AppImage /usr/local/bin/cursor

# Launch Cursor
cursor
```

#### For macOS
```bash
# Install via Homebrew
brew install --cask cursor

# Or download from: https://cursor.sh/
```

#### For Windows
1. Download from: https://cursor.sh/
2. Run installer as administrator
3. Follow installation wizard

### Step 2: Configure Cursor for Red Hat Development

#### Install Required Extensions
```bash
# Open Cursor and install these extensions:
# 1. Python (Microsoft)
# 2. YAML (Red Hat)
# 3. GitLens (GitKraken)
# 4. Red Hat YAML (Red Hat)
# 5. Ansible (Red Hat)
```

#### Configure Python Interpreter
1. Open Cursor
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
3. Type "Python: Select Interpreter"
4. Choose Python 3.8+ from your system

#### Configure Git Integration
```bash
# Set up Git configuration
git config --global user.name "Your Name"
git config --global user.email "your.email@redhat.com"

# Configure Git for Red Hat repositories
git config --global url."https://gitlab.cee.redhat.com/".insteadOf "git@gitlab.cee.redhat.com:"
```

### Step 3: Red Hat-Specific Cursor Configuration

#### Create `.cursor/settings.json`
```json
{
    "python.defaultInterpreterPath": "/usr/bin/python3",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "yaml.schemas": {
        "https://raw.githubusercontent.com/ansible/ansible-lint/main/src/ansiblelint/schemas/ansible.json": "**/ansible/**/*.yml",
        "https://raw.githubusercontent.com/ansible/ansible-lint/main/src/ansiblelint/schemas/ansible.json": "**/ansible/**/*.yaml"
    },
    "files.associations": {
        "*.yml": "yaml",
        "*.yaml": "yaml"
    },
    "terminal.integrated.shell.linux": "/bin/bash",
    "git.autofetch": true,
    "git.confirmSync": false
}
```

#### Create `.cursor/extensions.json`
```json
{
    "recommendations": [
        "ms-python.python",
        "redhat.vscode-yaml",
        "eamodio.gitlens",
        "redhat.ansible",
        "ms-vscode.vscode-json"
    ]
}
```

---

## 🔐 Red Hat Authentication Setup

### Step 1: Red Hat SSO Configuration

#### Install Red Hat SSO Tools
```bash
# Install Red Hat SSO CLI
sudo dnf install -y redhat-sso-cli

# Or via pip
pip3 install redhat-sso-cli
```

#### Configure SSO Credentials
```bash
# Login to Red Hat SSO
redhat-sso login

# Follow prompts to authenticate with your Red Hat credentials
# Username: your.username@redhat.com
# Password: [your Red Hat password]
```

### Step 2: Red Hat AI Models API Access

#### Get API Keys (VPN Required)
1. Connect to Red Hat VPN
2. Visit: https://developer.models.corp.redhat.com
3. Login with Red Hat SSO
4. Generate API key for Red Hat Granite models
5. Save API key securely

#### Configure API Keys
```bash
# Create secrets directory
mkdir -p ~/.config/pai/secrets

# Store API key (use your actual key)
echo "your-redhat-granite-api-key" > ~/.config/pai/secrets/redhat_granite_api_key

# Set secure permissions
chmod 600 ~/.config/pai/secrets/redhat_granite_api_key
```

### Step 3: Customer Portal Access

#### Verify Portal Access
1. Connect to Red Hat VPN
2. Visit: https://access.redhat.com
3. Login with Red Hat SSO
4. Navigate to your customer portal groups
5. Verify you can edit group content

---

## 🛠️ Red Hat Tools Installation

### Step 1: Install rhcase Tool

#### For Red Hat Enterprise Linux
```bash
# Install via RPM
sudo dnf install -y rhcase

# Or download from Red Hat internal repositories
wget https://internal-repo.redhat.com/rhcase-latest.rpm
sudo dnf install -y rhcase-latest.rpm
```

#### For Fedora
```bash
# Install via dnf
sudo dnf install -y rhcase
```

#### For macOS (with Homebrew)
```bash
# Install via Homebrew
brew install rhcase
```

### Step 2: Configure rhcase

#### Initial Configuration
```bash
# Test rhcase installation
rhcase --version

# Configure rhcase (first run)
rhcase configure

# Follow prompts:
# - Enter your Red Hat SSO username
# - Enter your Red Hat SSO password
# - Select default customer (optional)
```

#### Test rhcase Connectivity
```bash
# Test with a known customer account
rhcase list 838043 --months 1

# Should return case data without errors
```

### Step 3: Install Additional Red Hat Tools

#### Install TAM Scripts
```bash
# Clone TAM scripts repository
git clone https://gitlab.cee.redhat.com/tam-tools/tam-scripts.git ~/tam-scripts

# Install TAM scripts
cd ~/tam-scripts
./install.sh

# Configure TAM scripts
~/.config/tamscripts/tamscripts.config
```

---

## 🐍 Python Environment Setup

### Step 1: Install Python 3.8+

#### For Red Hat Enterprise Linux
```bash
# Install Python 3.8+
sudo dnf install -y python3 python3-pip python3-venv

# Verify installation
python3 --version
pip3 --version
```

#### For Fedora
```bash
# Install Python 3.8+
sudo dnf install -y python3 python3-pip python3-venv
```

#### For macOS
```bash
# Install via Homebrew
brew install python@3.9

# Or use system Python (usually 3.8+)
python3 --version
```

### Step 2: Install Required Python Packages

#### Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv ~/venv/rfe-automation

# Activate virtual environment
source ~/venv/rfe-automation/bin/activate

# Upgrade pip
pip install --upgrade pip
```

#### Install Required Packages
```bash
# Install core packages
pip install requests pyyaml jinja2 python-dateutil

# Install Red Hat specific packages
pip install redhat-sso-cli

# Install development packages
pip install black pylint pytest
```

#### Create requirements.txt
```bash
# Generate requirements file
pip freeze > requirements.txt

# Contents should include:
# requests>=2.25.0
# pyyaml>=5.4.0
# jinja2>=3.0.0
# python-dateutil>=2.8.0
# redhat-sso-cli>=1.0.0
```

---

## 🔧 Git Configuration

### Step 1: Install Git

#### For Red Hat Enterprise Linux / Fedora
```bash
# Install Git
sudo dnf install -y git

# Verify installation
git --version
```

#### For macOS
```bash
# Install via Homebrew
brew install git
```

### Step 2: Configure Git for Red Hat

#### Basic Configuration
```bash
# Set global Git configuration
git config --global user.name "Your Full Name"
git config --global user.email "your.email@redhat.com"

# Set default branch name
git config --global init.defaultBranch main

# Configure line endings
git config --global core.autocrlf input
```

#### Red Hat Repository Configuration
```bash
# Configure Git for Red Hat GitLab
git config --global url."https://gitlab.cee.redhat.com/".insteadOf "git@gitlab.cee.redhat.com:"

# Configure SSH for GitLab
ssh-keygen -t ed25519 -C "your.email@redhat.com"

# Add SSH key to GitLab
cat ~/.ssh/id_ed25519.pub
# Copy output and add to GitLab SSH keys
```

---

## 🌐 Network Configuration

### Step 1: Red Hat VPN Setup

#### Install VPN Client
```bash
# For Red Hat Enterprise Linux / Fedora
sudo dnf install -y openconnect

# For macOS
brew install openconnect
```

#### Configure VPN Connection
```bash
# Connect to Red Hat VPN
sudo openconnect vpn.redhat.com

# Follow prompts:
# - Username: your.username@redhat.com
# - Password: [your Red Hat password]
# - Group: [select appropriate group]
```

### Step 2: Network Testing

#### Test Connectivity
```bash
# Test Red Hat internal sites
curl -I https://access.redhat.com
curl -I https://gitlab.cee.redhat.com
curl -I https://developer.models.corp.redhat.com

# All should return HTTP 200 or 302
```

---

## ✅ Verification Checklist

### System Verification
- [ ] Python 3.8+ installed and working
- [ ] Git installed and configured
- [ ] Red Hat VPN connection working
- [ ] Terminal access to Red Hat systems

### Red Hat Tools Verification
- [ ] `rhcase` installed and configured
- [ ] Red Hat SSO login working
- [ ] Customer portal access verified
- [ ] Red Hat AI models API access confirmed

### Cursor IDE Verification
- [ ] Cursor IDE installed and launched
- [ ] Python interpreter configured
- [ ] Required extensions installed
- [ ] Git integration working
- [ ] Red Hat-specific settings applied

### Network Verification
- [ ] Red Hat VPN connected
- [ ] Access to Red Hat internal sites
- [ ] GitLab access working
- [ ] Customer portal access confirmed

---

## 🚨 Troubleshooting

### Common Issues

#### Cursor IDE Won't Launch
```bash
# Check if Cursor is executable
ls -la cursor.AppImage

# Make executable if needed
chmod +x cursor.AppImage

# Launch with debug output
./cursor.AppImage --verbose
```

#### rhcase Authentication Fails
```bash
# Clear rhcase cache
rm -rf ~/.rhcase/cache

# Reconfigure rhcase
rhcase configure

# Test with verbose output
rhcase list 838043 --months 1 --verbose
```

#### Python Packages Won't Install
```bash
# Upgrade pip
pip install --upgrade pip

# Install with user flag
pip install --user requests pyyaml

# Use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install requests pyyaml
```

#### Red Hat VPN Connection Issues
```bash
# Check VPN status
ip addr show

# Restart VPN connection
sudo pkill openconnect
sudo openconnect vpn.redhat.com

# Check DNS resolution
nslookup access.redhat.com
```

### Getting Help

#### Red Hat Internal Resources
- **IT Support**: https://ithelp.redhat.com
- **TAM Tools Slack**: #tam-tools
- **RFE Automation Slack**: #rfe-automation
- **GitLab Issues**: https://gitlab.cee.redhat.com/tam-tools/rfe-automation/-/issues

#### External Resources
- **Cursor IDE Docs**: https://cursor.sh/docs
- **Python Docs**: https://docs.python.org/3/
- **Git Docs**: https://git-scm.com/doc

---

## 🎯 Next Steps

Once all prerequisites are installed and verified:

1. **Clone RFE Automation Tool**:
   ```bash
   git clone https://gitlab.cee.redhat.com/tam-tools/rfe-automation.git
   cd rfe-automation
   ```

2. **Run Installation**:
   ```bash
   ./bin/tam-rfe-deploy --install
   ```

3. **Configure Your First Customer**:
   ```bash
   ./bin/tam-rfe-onboard
   ```

4. **Test the System**:
   ```bash
   ./bin/tam-rfe-monitor --test-system
   ```

5. **Run Your First Automation**:
   ```bash
   ./bin/tam-rfe-monitor [customer] --test
   ```

---

**Need Help?** Contact the TAM automation team via Slack (#tam-automation-tools) or email (tam-automation-team@redhat.com).

