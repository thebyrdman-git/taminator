# Red Hat PAI Installation Guide

## 🎯 **What Gets Installed**

The Red Hat PAI system installs locally on your machine and includes:

1. **Fabric AI**: Universal AI processing framework
2. **LiteLLM Proxy**: Local proxy for Red Hat Granite models (localhost:4000)
3. **PAI Scripts**: 62+ Red Hat workflow automation tools
4. **Context System**: Global PAI context for all AI tools
5. **Agent Configurations**: AGENTS.md and GEMINI.md for cross-platform AI

## 📦 **Installation Process**

### Quick Install
```bash
curl -sSL https://gitlab.cee.redhat.com/gvaughn/hatter-pai/-/raw/main/install.sh | bash
```

### Manual Install
```bash
# 1. Clone repository
git clone git@gitlab.cee.redhat.com:gvaughn/hatter-pai.git
cd hatter-pai

# 2. Run installation script
./install.sh

# 3. Verify installation
pai-context-current
fabric --list-models | grep granite
```

## 🔧 **What the Installation Script Does**

### 1. System Dependencies
```bash
# Installs required tools
npm install -g @danielmiessler/fabric
pip install litellm
```

### 2. Local LiteLLM Setup
```bash
# Creates local LiteLLM configuration
mkdir -p ~/.config/pai/
cp config/litellm-config.yaml ~/.config/pai/

# Starts LiteLLM proxy service
litellm --config ~/.config/pai/litellm-config.yaml --port 4000 --host 0.0.0.0
```

### 3. PAI Scripts Installation
```bash
# Copies all pai-* scripts to global PATH
cp bin/* ~/.local/bin/
chmod +x ~/.local/bin/pai-*
```

### 4. Global Context Setup
```bash
# Creates universal PAI context
cp contexts/* ~/pai-context/redhat/
ln -sf ~/pai-context ~/.claude/context

# Creates global agent configs
cp AGENTS.md ~/AGENTS.md
cp GEMINI.md ~/GEMINI.md
```

### 5. Service Integration
```bash
# Sets up LiteLLM as system service (macOS)
cp scripts/com.redhat.pai.litellm.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.redhat.pai.litellm.plist
```

## ⚙️ **Local LiteLLM Configuration**

**File**: `~/.config/pai/litellm-config.yaml`
```yaml
model_list:
  - model_name: granite-34b-instruct
    litellm_params:
      model: granite-34b-instruct
      base_url: http://rh-internal-models:8080  # via Red Hat VPN
      api_key: ${RH_GRANITE_API_KEY}

  - model_name: granite-7b-instruct
    litellm_params:
      model: granite-7b-instruct
      base_url: http://rh-internal-models:8080
      api_key: ${RH_GRANITE_API_KEY}

general_settings:
  master_key: ${LITELLM_MASTER_KEY}
  database_url: "sqlite:///~/.config/pai/litellm.db"
```

## 🔐 **Secrets Configuration**

**File**: `~/.config/pai/secrets/env`
```bash
# Red Hat model access (via VPN)
export RH_GRANITE_API_KEY="your-red-hat-api-key"
export LITELLM_MASTER_KEY="your-litellm-master-key"

# Personal model access (optional)
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
export GOOGLE_AI_API_KEY="your-google-key"
```

## 🧪 **Verification Steps**

### 1. Check LiteLLM Service
```bash
# Verify LiteLLM is running
curl http://localhost:4000/health

# List available models
curl http://localhost:4000/models
```

### 2. Test Fabric Integration
```bash
# Test Red Hat model access
fabric --model granite-34b-instruct --pattern extract_wisdom test_document.md

# Test personal model access
fabric --model gpt-4o --pattern summarize personal_notes.md
```

### 3. Test PAI Scripts
```bash
# Check PAI system status
pai-context-current
pai-status-show

# Test compliance detection
echo "customer case analysis needed" | pai-fabric-compliant --pattern summarize
```

## 🛠️ **Service Management**

### Start/Stop LiteLLM
```bash
# macOS (LaunchAgent)
launchctl start com.redhat.pai.litellm
launchctl stop com.redhat.pai.litellm

# Manual start
litellm --config ~/.config/pai/litellm-config.yaml --port 4000 &

# Check status
ps aux | grep litellm
```

### Update Installation
```bash
# Pull latest changes
cd ~/coding/gitlabs/active/redhat-pai
git pull

# Re-run installation
./install.sh --update
```

## 🚨 **Troubleshooting**

### LiteLLM Not Starting
```bash
# Check configuration
cat ~/.config/pai/litellm-config.yaml

# Check logs
tail -f ~/.config/pai/litellm.log

# Test VPN connection
ping rh-internal-models
```

### Models Not Available
```bash
# Verify Red Hat VPN is connected
curl http://rh-internal-models:8080/health

# Check API key
echo $RH_GRANITE_API_KEY

# Test direct model access
curl -H "Authorization: Bearer $RH_GRANITE_API_KEY" http://rh-internal-models:8080/models
```

### PAI Scripts Not Working
```bash
# Check PATH
echo $PATH | grep -o ~/.local/bin

# Verify scripts are executable
ls -la ~/.local/bin/pai-*

# Test basic PAI function
pai-context-current
```

## 📋 **Requirements Checklist**

- [ ] Red Hat VPN access configured
- [ ] Node.js installed (for Fabric)
- [ ] Python 3.8+ installed (for LiteLLM)
- [ ] Git access to gitlab.cee.redhat.com
- [ ] ~/.local/bin in PATH
- [ ] Red Hat API credentials available

---

*Complete installation guide for Red Hat PAI system*
*Local installation with LiteLLM proxy for Red Hat model access*