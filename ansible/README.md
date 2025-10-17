# RFE Tool - Ansible Installation

**Cross-platform automated installation using proven Geerling roles**

---

## Quick Start

### 1. Install Ansible Galaxy Dependencies

```bash
cd ansible
ansible-galaxy install -r requirements.yml
```

### 2. Run Installation

```bash
ansible-playbook install-rfe.yml
```

**The installer will:**
- Detect your platform (Linux/macOS)
- Install prerequisites
- Clone the RFE repository
- Setup Python environment
- Install all TAM tools
- Configure for Red Hat workflows
- Optionally setup VPN

---

## Installation Options

### Interactive Installation (Recommended)
```bash
ansible-playbook install-rfe.yml
```

The playbook will prompt for:
- Confirmation to proceed
- VPN setup (yes/no)
- VPN profile path (if applicable)

### Non-Interactive Installation
```bash
ansible-playbook install-rfe.yml \
  -e "install_confirm=yes" \
  -e "setup_vpn_prompt=no"
```

### With VPN Setup
```bash
ansible-playbook install-rfe.yml \
  -e "install_confirm=yes" \
  -e "setup_vpn_prompt=yes" \
  -e "vpn_profile_path=~/Downloads/your-vpn-profile.ovpn"
```

### Custom Installation Directory
```bash
ansible-playbook install-rfe.yml \
  -e "rfe_install_dir=~/custom/path/rfe-tool"
```

---

## Supported Platforms

| Platform | Versions | Package Manager | Status |
|----------|----------|-----------------|--------|
| **RHEL** | 8, 9, 10 | DNF | ✅ Full Support |
| **Fedora** | 40, 41, 42, 43 | DNF | ✅ Full Support |
| **Alma Linux** | 8, 9 | DNF | ✅ Full Support |
| **Rocky Linux** | 8, 9 | DNF | ✅ Full Support |
| **Ubuntu** | 20.04, 22.04, 24.04 | APT | ✅ Full Support |
| **Debian** | 11, 12 | APT | ✅ Full Support |
| **macOS** | 11+ | Homebrew | ✅ Full Support |

---

## What Gets Installed

### System Packages
- Git
- Python 3.8+
- Python pip
- Development tools (gcc, python3-devel)
- Kerberos client (krb5-workstation)

### Python Packages
- platformdirs (OS-agnostic paths)
- keyring (credential storage)
- requests (HTTP client)
- pyyaml (configuration)
- click (CLI framework)
- jinja2 (templating)

### TAM Tools
- `tam-rfe-chat` - Interactive case analysis
- `tam-rfe-onboard-intelligent` - Customer onboarding
- `tam-rfe-validate-intelligence` - Configuration validation
- `tam-rfe-tui` - Text user interface
- `tam-rfe-scheduler` - Report scheduling
- `tam-rfe-hydra-api` - Hydra API integration
- `tam-rfe-discover-customers` - Customer discovery

---

## Configuration

### Default Paths

| Item | Linux | macOS |
|------|-------|-------|
| **Install Dir** | `~/rfe-bug-tracker-automation` | `~/rfe-bug-tracker-automation` |
| **Tools** | `~/.local/bin` | `~/.local/bin` |
| **Config** | `~/.config/rfe-tool` | `~/Library/Application Support/rfe-tool` |
| **Data** | `~/.local/share/rfe-tool` | `~/Library/Application Support/rfe-tool` |

### Override Defaults

Create `ansible/inventory.yml`:

```yaml
all:
  hosts:
    localhost:
      ansible_connection: local
  vars:
    rfe_install_dir: ~/custom/path
    rfe_python_version: "3.11"
    rfe_use_venv: true
    rfe_setup_kerberos: true
```

Then run:
```bash
ansible-playbook -i inventory.yml install-rfe.yml
```

---

## Architecture

### Geerling Roles Used
This installation follows the **"Build on Giants' Shoulders"** philosophy:

- `geerlingguy.git` - Proven Git installation
- `geerlingguy.pip` - Proven Python package management
- `geerlingguy.homebrew` - Proven macOS package management
- `redhat_vpn` - Our extracted VPN Lego block

**Custom code:** ~5% (just the business logic)  
**Proven code:** ~95% (Geerling + stdlib)

### Role Structure
```
ansible/
├── requirements.yml          # Geerling role dependencies
├── install-rfe.yml           # Master playbook
├── inventory.yml             # Optional custom config
└── roles/
    └── rfe_install/          # Our installation role
        ├── tasks/            # Installation steps
        ├── defaults/         # Default variables
        ├── templates/        # Config templates
        └── meta/             # Role metadata + dependencies
```

---

## Troubleshooting

### Ansible Not Found
```bash
# RHEL/Fedora
sudo dnf install ansible-core

# Ubuntu/Debian
sudo apt install ansible

# macOS
brew install ansible
```

### Python Version Too Old
```bash
# Update Python
sudo dnf install python3.11  # RHEL/Fedora
brew install python@3.11     # macOS
```

### Git Clone Fails (VPN Required)
If cloning from GitLab CEE fails:
1. Connect to Red Hat VPN first
2. Or use the offline installer package

### Permission Denied
```bash
# Ensure you have write access to install directory
ls -la ~/

# Or install to different directory
ansible-playbook install-rfe.yml -e "rfe_install_dir=~/my-tools/rfe"
```

---

## Uninstallation

```bash
# Remove tools
rm -rf ~/.local/bin/tam-rfe-*

# Remove installation
rm -rf ~/rfe-bug-tracker-automation

# Remove configuration (optional)
rm -rf ~/.config/rfe-tool
rm -rf ~/.local/share/rfe-tool
```

---

## Testing the Installation

```bash
# Check tools are accessible
which tam-rfe-chat

# Test help output
tam-rfe-chat --help

# Validate installation
tam-rfe-validate-intelligence --help
```

---

## Philosophy: Build on Giants' Shoulders

This installation uses **Geerling's proven Ansible roles** for:
- ✅ Git installation (`geerlingguy.git`)
- ✅ Python package management (`geerlingguy.pip`)
- ✅ macOS support (`geerlingguy.homebrew`)

**Why?** These roles are:
- Battle-tested across thousands of deployments
- Maintained by experts
- Support multiple platforms
- Handle edge cases we'd miss

**Result:** 95% proven code, 5% custom glue = Reliable, maintainable installation

---

## Next Steps After Installation

1. **Configure your first customer:**
   ```bash
   tam-rfe-onboard-intelligent
   ```

2. **Test the configuration:**
   ```bash
   tam-rfe-validate-intelligence <customer-name>
   ```

3. **Explore the TUI:**
   ```bash
   tam-rfe-tui
   ```

4. **Schedule reports:**
   ```bash
   tam-rfe-scheduler
   ```

---

*RFE Tool Ansible Installation Guide*  
*Following PAI Gold Standard Framework*  
*Cross-Platform • Proven Roles • 95% Reusable Code*

