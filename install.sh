#!/bin/bash
# Red Hat PAI Installation Script
# Enterprise-focused PAI system for Red Hat teams

set -euo pipefail

echo "🔴 Installing Red Hat PAI System..."

# Create directory structure
PAI_ROOT="$HOME/pai-context"
mkdir -p "$PAI_ROOT"/{redhat,personal}
mkdir -p "$PAI_ROOT/redhat"/{contexts,config,bin}
mkdir -p ~/.config/pai/secrets
chmod 700 ~/.config/pai/secrets

echo "📁 Created PAI directory structure"

# Install Gemini CLI if not present
if ! command -v gemini &> /dev/null; then
    echo "📦 Installing Gemini CLI..."
    npm install -g @google/gemini-cli
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
echo "🎭 Start Gemini CLI with: gemini"
echo "📖 All pai- scripts available via run_shell_command"

# Display secrets setup reminder
echo ""
echo "🔐 IMPORTANT: Configure your secrets in ~/.config/pai/secrets/"
echo "   Example: ~/.config/pai/secrets/redhat-api-keys"