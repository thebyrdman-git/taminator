#!/bin/bash
# Red Hat PAI Installation Script
# Enterprise-focused PAI system for Red Hat teams

set -euo pipefail

echo "🔴 Installing Red Hat PAI System..."
echo ""
echo "📋 PREREQUISITES - Complete these steps first:"
echo "   1. Red Hat AI Models API keys (VPN required):"
echo "      https://developer.models.corp.redhat.com"
echo "   2. Cursor IDE setup: https://source.redhat.com/projects_and_programs/ai/ai_tools/cursor"
echo "   3. Gemini API key: https://source.redhat.com/departments/it/datacenter_infrastructure/itcloudservices/itpubliccloudpage/cloud/gcp/gcpgeminiapi"
echo "   4. Personal Access Token for Confluence/Jira:"
echo "      https://spaces.redhat.com/spaces/OMEGA/pages/228005232/Personal+Access+Token+Usage"
echo ""
echo "⚠️  Without these prerequisites, the PAI system will not function properly."
echo "   Press Ctrl+C to cancel if you haven't completed these steps."
echo ""
read -p "🚀 Ready to proceed with installation? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Installation cancelled. Please complete prerequisites first."
    exit 1
fi
echo ""

# Detect supported platforms
detect_platform() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [ -f /etc/fedora-release ]; then
        echo "fedora"
    elif [ -f /etc/redhat-release ]; then
        echo "rhel"
    else
        echo "unsupported"
    fi
}

# Install system dependencies
install_dependencies() {
    local platform=$(detect_platform)
    echo "🔍 Detected platform: $platform"

    case "$platform" in
        "macos")
            echo "📦 macOS: Checking dependencies..."
            if ! command -v node &> /dev/null || ! command -v npm &> /dev/null; then
                echo "❌ Node.js/npm not found. Please install Node.js from https://nodejs.org/"
                echo "   Or install via Homebrew: brew install node"
                exit 1
            fi
            if ! command -v python3 &> /dev/null; then
                echo "❌ Python 3 not found. Please install from https://python.org/"
                echo "   Or install via Homebrew: brew install python"
                exit 1
            fi
            echo "✅ macOS dependencies verified"
            ;;
        "fedora"|"rhel")
            echo "📦 Installing dependencies via dnf..."
            if ! command -v node &> /dev/null || ! command -v npm &> /dev/null; then
                sudo dnf install -y nodejs npm
            fi
            if ! rpm -qa | grep -q python3-devel; then
                echo "📦 Installing python3-devel for LiteLLM..."
                sudo dnf install -y python3-devel python3-pip
            fi
            echo "✅ Fedora dependencies installed"
            ;;
        "unsupported")
            echo "⚠️  Unsupported platform detected. Red Hat PAI is optimized for:"
            echo "   • Fedora/RHEL (recommended for Red Hat teams)"
            echo "   • macOS (for development and testing)"
            echo ""
            echo "📝 Continuing installation with manual dependency requirements:"
            if ! command -v node &> /dev/null || ! command -v npm &> /dev/null; then
                echo "⚠️  Node.js/npm not found. Please install manually."
                echo "   Installation may fail without these dependencies."
            fi
            if ! command -v python3 &> /dev/null; then
                echo "⚠️  Python 3 not found. Please install manually."
                echo "   LiteLLM installation may fail without Python."
            fi
            echo "⚠️  Best-effort installation continuing..."
            ;;
    esac
}

# Check and install system dependencies
echo "🔧 Checking system dependencies..."
install_dependencies

# Create directory structure
PAI_ROOT="$HOME/pai-context"
mkdir -p "$PAI_ROOT"/{redhat,personal}
mkdir -p "$PAI_ROOT/redhat"/{contexts,config,bin}
mkdir -p ~/.config/pai/secrets
chmod 700 ~/.config/pai/secrets

echo "📁 Created PAI directory structure"

# Install AI Tools
echo "🚀 Installing AI Tools..."

# Install Fabric AI
if ! command -v fabric &> /dev/null; then
    echo "📦 Installing Fabric AI..."
    if command -v go &> /dev/null; then
        go install github.com/danielmiessler/fabric@latest
    else
        echo "⚠️  Go not found. Installing Fabric via pip..."
        pip3 install --user fabric-ai
    fi
else
    echo "✅ Fabric AI already installed"
fi

# Install Gemini CLI
if ! command -v gemini &> /dev/null; then
    echo "📦 Installing Gemini CLI..."
    npm install -g @google/gemini-cli
else
    echo "✅ Gemini CLI already installed"
fi

# Install LiteLLM
if ! command -v litellm &> /dev/null; then
    echo "📦 Installing LiteLLM..."
    if pip3 install --user litellm; then
        echo "✅ LiteLLM installed successfully"
        # Ensure ~/.local/bin is in PATH
        if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
            echo "📝 Added ~/.local/bin to PATH in ~/.bashrc"
        fi
    else
        echo "⚠️  LiteLLM installation failed. Install manually with: pip3 install --user litellm"
        echo "   This is required for Red Hat model access"
    fi
else
    echo "✅ LiteLLM already installed"
fi

# Copy Red Hat contexts
echo "📋 Installing Red Hat contexts..."
curl -sSL https://gitlab.cee.redhat.com/gvaughn/hatter-pai/-/raw/main/contexts/hatter-personality.md > "$PAI_ROOT/redhat/contexts/hatter-personality.md"

# Copy Red Hat configuration
echo "⚙️  Installing Red Hat configuration..."
curl -sSL https://gitlab.cee.redhat.com/gvaughn/hatter-pai/-/raw/main/config/models.yaml > "$PAI_ROOT/redhat/config/models.yaml"

# Install Red Hat PAI scripts
echo "🔧 Installing Red Hat workflow scripts..."
mkdir -p /tmp/redhat-pai-install
cd /tmp/redhat-pai-install

# Download all scripts
curl -sSL https://gitlab.cee.redhat.com/gvaughn/hatter-pai/-/archive/main/hatter-pai-main.tar.gz | tar xz
cp hatter-pai-main/bin/* "$PAI_ROOT/redhat/bin/"

# Make scripts executable
chmod +x "$PAI_ROOT/redhat/bin/"*

# Create symlinks to ~/.local/bin
mkdir -p ~/.local/bin
for script in "$PAI_ROOT/redhat/bin/pai-"*; do
    ln -sf "$script" ~/.local/bin/
done

# Clean up
rm -rf /tmp/redhat-pai-install

# Configure Gemini CLI
echo "🎭 Configuring Gemini CLI..."
mkdir -p ~/.gemini

cat > ~/.gemini/settings.json << 'SETTINGS_EOF'
{
  "contextFileName": [
    "GEMINI.md"
  ],
  "hideTips": false,
  "hideBanner": false,
  "includeDirectories": [
    "~/pai-context/redhat/contexts"
  ],
  "loadMemoryFromIncludeDirectories": true,
  "model": "gemini-1.5-pro-latest",
  "selectedAuthType": "gemini-api-key",
  "theme": "GitHub",
  "tools": {
    "allowed": ["run_shell_command(pai-)", "run_shell_command(ls)"]
  }
}
SETTINGS_EOF

# Create GEMINI.md for Red Hat context
curl -sSL https://gitlab.cee.redhat.com/gvaughn/hatter-pai/-/raw/main/GEMINI.md > ~/GEMINI.md

echo "✅ Red Hat PAI installation complete!"
echo ""
echo "🚀 Available commands:"
echo "   pai-context-current    # Show PAI status"
echo "   pai-case-processor     # Process support cases"
echo "   pai-supportshell       # SupportShell integration"
echo "   pai-compliance-check   # Check AI policy compliance"
echo ""
echo "🎭 AI Tools installed:"
echo "   fabric                 # Fabric AI with Red Hat model routing"
echo "   gemini                 # Gemini CLI with Hatter personality"
echo "   litellm                # LiteLLM proxy for Red Hat AI models"
echo ""
echo "📖 All pai- scripts available via run_shell_command in Gemini CLI"

# Verify installation
echo ""
echo "🔍 Verifying installation..."
if command -v pai-context-current &> /dev/null; then
    echo "✅ PAI scripts installed: $(pai-context-current)"
else
    echo "⚠️  PAI scripts not found in PATH. Add ~/.local/bin to your PATH:"
    echo "   export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

if command -v fabric &> /dev/null; then
    echo "✅ Fabric AI installed"
else
    echo "⚠️  Fabric AI installation may have failed"
fi

if command -v gemini &> /dev/null; then
    echo "✅ Gemini CLI installed"
else
    echo "⚠️  Gemini CLI installation may have failed"
fi

if command -v litellm &> /dev/null; then
    echo "✅ LiteLLM proxy available"
else
    echo "⚠️  LiteLLM may need manual PATH setup or installation"
fi

# Display setup completion and next steps
echo ""
echo "🔐 IMPORTANT: Configure your API keys and tokens"
echo "   Add these to ~/.config/pai/secrets/redhat-api-keys:"
echo "   • Red Hat AI Models API keys (from developer.models.corp.redhat.com)"
echo "   • Gemini API key (from Red Hat GCP setup)"
echo "   • Personal Access Token (for Confluence/Jira access)"
echo ""
echo "🏁 Next steps:"
echo "   1. Restart your terminal or run: source ~/.bashrc"
echo "   2. Add your API keys and tokens to ~/.config/pai/secrets/"
echo "   3. Complete Cursor IDE setup if not done:"
echo "      https://source.redhat.com/projects_and_programs/ai/ai_tools/cursor"
echo "   4. Test with: pai-context-current"
echo "   5. Start Gemini CLI with: gemini"