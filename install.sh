#!/bin/bash
# ANSAI Installation Script
# Installs ANSAI AI-powered automation framework

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Installation settings
ANSAI_DIR="${ANSAI_DIR:-$HOME/.ansai}"
ANSAI_CONFIG="$HOME/.config/ansai"
ANSAI_REPO="https://github.com/thebyrdman-git/ansai.git"

# Function to print colored output
print_header() {
    echo -e "\n${BLUE}${BOLD}═══════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}${BOLD}  $1${NC}"
    echo -e "${BLUE}${BOLD}═══════════════════════════════════════════════════${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ ERROR: $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  WARNING: $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

print_step() {
    echo -e "${BOLD}→ $1${NC}"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if we can read from TTY (for interactive prompts)
can_prompt() {
    # Test if /dev/tty exists and we can open it
    ( exec < /dev/tty ) 2>/dev/null
}

# Prompt user or use default in non-interactive mode
prompt_yn() {
    local prompt="$1"
    local default="${2:-y}"
    
    if can_prompt; then
        read -p "$prompt " -n 1 -r < /dev/tty
        echo "" > /dev/tty
        [[ $REPLY =~ ^[Yy]$ ]]
    else
        # Non-interactive: show prompt and use default
        echo "$prompt [auto: $default]"
        [[ $default =~ ^[Yy]$ ]]
    fi
}

# Prompt for choice or use default in non-interactive mode
prompt_choice() {
    local prompt="$1"
    local default="$2"
    
    if can_prompt; then
        read -p "$prompt " -n 1 -r < /dev/tty
        echo "" > /dev/tty
        echo "$REPLY"
    else
        # Non-interactive: use default (prompt goes to stderr, value to stdout)
        echo "$prompt [auto: $default]" >&2
        echo "$default"
    fi
}

# Function to run pip (handles RHEL where pip3 isn't a standalone command)
run_pip() {
    if command_exists pip3; then
        pip3 "$@"
    elif command_exists pip; then
        pip "$@"
    else
        python3 -m pip "$@"
    fi
}

# Function to detect shell
detect_shell() {
    if [ -n "$BASH_VERSION" ]; then
        echo "bash"
    elif [ -n "$ZSH_VERSION" ]; then
        echo "zsh"
    else
        basename "$SHELL"
    fi
}

# Function to get shell config file
get_shell_config() {
    local shell_type
    shell_type=$(detect_shell)
    case "$shell_type" in
        bash)
            if [ -f "$HOME/.bashrc" ]; then
                echo "$HOME/.bashrc"
            else
                echo "$HOME/.bash_profile"
            fi
            ;;
        zsh)
            echo "$HOME/.zshrc"
            ;;
        fish)
            echo "$HOME/.config/fish/config.fish"
            ;;
        *)
            echo "$HOME/.profile"
            ;;
    esac
}

# Start installation
clear
print_header "ANSAI Installation"

echo -e "${BOLD}AI-Powered Automation Infrastructure${NC}"
echo -e "ANSAI = Ansible + AI\n"
echo -e "This installer will:"
echo -e "  1. Install ANSAI to ${CYAN}$ANSAI_DIR${NC}"
echo -e "  2. Set up PATH in your shell profile"
echo -e "  3. Install AI dependencies (optional)"
echo -e "  4. Create configuration directories"
echo -e ""

if ! prompt_yn "Continue with installation? (y/n)" "y"; then
    print_warning "Installation cancelled."
    exit 0
fi

# Check prerequisites
print_header "Step 1: Checking Prerequisites"

MISSING_DEPS=()

print_step "Checking for required dependencies..."

# Check Git
if command_exists git; then
    print_success "Git installed ($(git --version | cut -d' ' -f3))"
else
    print_error "Git not found"
    MISSING_DEPS+=("git")
fi

# Check Python
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python installed ($PYTHON_VERSION)"
else
    print_error "Python 3 not found"
    MISSING_DEPS+=("python3")
fi

# Check Ansible (optional but recommended)
if command_exists ansible; then
    ANSIBLE_VERSION=$(ansible --version | head -n1 | cut -d' ' -f2 | sed 's/\[.*\]//')
    print_success "Ansible installed ($ANSIBLE_VERSION)"
else
    print_warning "Ansible not found (recommended for automation)"
    echo -e "   ${CYAN}Install with: python3 -m pip install ansible${NC}"
fi

# Check curl or wget
if command_exists curl; then
    print_success "curl installed"
elif command_exists wget; then
    print_success "wget installed"
else
    print_error "Neither curl nor wget found"
    MISSING_DEPS+=("curl or wget")
fi

# Exit if missing critical dependencies
if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    print_error "Missing required dependencies: ${MISSING_DEPS[*]}"
    echo -e "\n${YELLOW}Please install missing dependencies:${NC}"

    # Detect OS and provide install commands
    if [ -f /etc/os-release ]; then
        # shellcheck source=/dev/null
        . /etc/os-release
        case "$ID" in
            ubuntu|debian)
                echo -e "${CYAN}sudo apt update && sudo apt install -y ${MISSING_DEPS[*]}${NC}"
                ;;
            fedora|rhel|centos)
                echo -e "${CYAN}sudo dnf install -y ${MISSING_DEPS[*]}${NC}"
                ;;
            arch|manjaro)
                echo -e "${CYAN}sudo pacman -S ${MISSING_DEPS[*]}${NC}"
                ;;
            *)
                echo -e "${CYAN}Please install: ${MISSING_DEPS[*]}${NC}"
                ;;
        esac
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo -e "${CYAN}brew install ${MISSING_DEPS[*]}${NC}"
    fi

    exit 1
fi

print_success "All prerequisites met!"

# Clone ANSAI repository
print_header "Step 2: Installing ANSAI"

# Check if we're running from within ANSAI_DIR (prevents self-deletion)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNNING_FROM_ANSAI=false
if [[ "$SCRIPT_DIR" == "$ANSAI_DIR"* ]]; then
    RUNNING_FROM_ANSAI=true
    print_warning "Detected: Running installer from within ANSAI directory"
fi

if [ -d "$ANSAI_DIR" ]; then
    print_warning "ANSAI directory already exists: $ANSAI_DIR"
    if prompt_yn "Remove and reinstall? (y/n)" "y"; then
        # If running from within ANSAI, copy script to /tmp first
        if [ "$RUNNING_FROM_ANSAI" = true ]; then
            print_step "Copying installer to /tmp to prevent self-deletion..."
            cp "$0" /tmp/ansai-install-temp.sh
            chmod +x /tmp/ansai-install-temp.sh
            print_info "Re-running installer from safe location..."
            exec /tmp/ansai-install-temp.sh
            exit 0
        fi

        print_step "Removing existing installation..."
        rm -rf "$ANSAI_DIR"
        print_success "Existing installation removed"
    else
        print_info "Keeping existing installation. Pulling latest changes..."
        cd "$ANSAI_DIR"
        git pull origin main
        print_success "ANSAI updated!"
        exit 0
    fi
fi

if [ ! -d "$ANSAI_DIR" ]; then
    print_step "Cloning ANSAI repository..."
    git clone "$ANSAI_REPO" "$ANSAI_DIR"
    print_success "ANSAI cloned to $ANSAI_DIR"
fi

# Create config directories
print_header "Step 3: Setting Up Configuration"

print_step "Creating configuration directories..."
mkdir -p "$ANSAI_CONFIG"
mkdir -p "$ANSAI_CONFIG/hooks"
mkdir -p "$ANSAI_CONFIG/fabric_patterns"

print_success "Configuration directories created"

# Set up PATH
print_header "Step 4: Configuring Shell Environment"

SHELL_CONFIG=$(get_shell_config)
print_step "Detected shell config: $SHELL_CONFIG"

# Check if PATH already configured
if grep -q "ANSAI" "$SHELL_CONFIG" 2>/dev/null; then
    print_warning "ANSAI PATH already configured in $SHELL_CONFIG"
else
    print_step "Adding ANSAI to PATH..."
    cat >> "$SHELL_CONFIG" << 'EOF'

# ANSAI - AI-Powered Automation Infrastructure
export ANSAI_DIR="$HOME/.ansai"
export ANSAI_CONFIG_DIR="$HOME/.config/ansai"
export PATH="$ANSAI_DIR/bin:$PATH"
EOF
    print_success "ANSAI PATH added to $SHELL_CONFIG"
fi

# Export for current session
export ANSAI_DIR="$HOME/.ansai"
export ANSAI_CONFIG_DIR="$HOME/.config/ansai"
export PATH="$ANSAI_DIR/bin:$PATH"

# AI dependencies installation
print_header "Step 5: AI Dependencies (Optional)"

echo -e "${BOLD}ANSAI requires AI capabilities to be useful.${NC}"
echo -e "Choose your AI backend:\n"
echo -e "  ${CYAN}1) LiteLLM${NC} - Multi-model proxy (OpenAI, Claude, Groq, local models)"
echo -e "     Cost optimization, intelligent routing, automatic fallback"
echo -e ""
echo -e "  ${CYAN}2) Fabric${NC} - AI text processing framework (Go binary)"
echo -e "     Pattern-based analysis, log processing, text transformation"
echo -e "     ${YELLOW}Note: Requires Go or Homebrew to install${NC}"
echo -e ""
echo -e "  ${CYAN}3) Both${NC} - Full AI capabilities (recommended)"
echo -e ""
echo -e "  ${CYAN}4) Skip${NC} - I'll install manually later"
echo -e ""

AI_CHOICE=$(prompt_choice "Choose option (1-4):" "4")

case $AI_CHOICE in
    1)
        print_step "Installing LiteLLM..."
        run_pip install --user 'litellm[proxy]'
        print_success "LiteLLM installed"
        ;;
    2)
        print_step "Installing Fabric..."
        if command_exists brew; then
            brew install fabric-ai
            print_success "Fabric installed via Homebrew"
        elif command_exists go; then
            GO111MODULE=on go install github.com/danielmiessler/fabric/cmd/fabric@latest
            print_success "Fabric installed via Go"
        else
            print_warning "Fabric requires Homebrew (macOS) or Go to install"
            print_info "macOS: brew install fabric-ai"
            print_info "Linux: Install Go, then: go install github.com/danielmiessler/fabric/cmd/fabric@latest"
            print_info "Or download binary: https://github.com/danielmiessler/fabric/releases"
        fi
        ;;
    3)
        print_step "Installing LiteLLM..."
        run_pip install --user 'litellm[proxy]'
        print_success "LiteLLM installed"
        
        print_step "Installing Fabric..."
        if command_exists brew; then
            brew install fabric-ai
            print_success "Fabric installed via Homebrew"
        elif command_exists go; then
            GO111MODULE=on go install github.com/danielmiessler/fabric/cmd/fabric@latest
            print_success "Fabric installed via Go"
        else
            print_warning "Fabric requires Homebrew (macOS) or Go to install"
            print_info "macOS: brew install fabric-ai"
            print_info "Linux: go install github.com/danielmiessler/fabric/cmd/fabric@latest"
        fi
        ;;
    4)
        print_info "Skipping AI dependencies. Install later with:"
        echo -e "   ${CYAN}LiteLLM: python3 -m pip install 'litellm[proxy]'${NC}"
        echo -e "   ${CYAN}Fabric:  brew install fabric-ai (macOS)${NC}"
        echo -e "   ${CYAN}         go install github.com/danielmiessler/fabric/cmd/fabric@latest (Linux)${NC}"
        ;;
    *)
        print_warning "Invalid choice. Skipping AI dependencies."
        ;;
esac

# Ansible installation
print_header "Step 6: Ansible (Optional but Recommended)"

if ! command_exists ansible; then
    echo -e "${YELLOW}Ansible not found.${NC}"
    echo -e "Ansible is ${BOLD}highly recommended${NC} for ANSAI automation."
    echo -e ""
    if prompt_yn "Install Ansible now? (y/n)" "n"; then
        print_step "Installing Ansible..."
        run_pip install --user ansible
        print_success "Ansible installed"
    else
        print_info "Skipping Ansible. Install later with:"
        echo -e "   ${CYAN}python3 -m pip install ansible${NC}"
    fi
fi

# Create example config files
print_header "Step 7: Creating Example Configurations"

# Create example LiteLLM config
if [ ! -f "$ANSAI_CONFIG/litellm_config.yaml.example" ]; then
    print_step "Creating example LiteLLM config..."
    cat > "$ANSAI_CONFIG/litellm_config.yaml.example" << 'EOF'
# Example LiteLLM Configuration for ANSAI
# Copy to litellm_config.yaml and configure your API keys

model_list:
  # OpenAI models
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY
      max_tokens: 4096

  # Anthropic models
  - model_name: claude-3-opus
    litellm_params:
      model: anthropic/claude-3-opus-20240229
      api_key: os.environ/ANTHROPIC_API_KEY
      max_tokens: 4096

  # Groq models (fast and cheap)
  - model_name: groq-llama3
    litellm_params:
      model: groq/llama3-8b-8192
      api_key: os.environ/GROQ_API_KEY
      max_tokens: 4096

  # Local Ollama models (free!)
  - model_name: local-llama3
    litellm_params:
      model: ollama/llama3
      api_base: http://localhost:11434
      api_key: "sk-ollama"  # Dummy key for local
      max_tokens: 4096

litellm_settings:
  set_verbose: true
  drop_params: true
EOF
    print_success "Example LiteLLM config created"
fi

# Create example Ansible inventory
if [ ! -f "$ANSAI_DIR/orchestrators/ansible/inventory/hosts.yml.example" ]; then
    print_step "Example Ansible inventory already exists in repository"
fi

# Installation complete!
print_header "Installation Complete! 🎉"

print_success "ANSAI installed successfully!"
echo -e ""
echo -e "${BOLD}Next Steps:${NC}"
echo -e ""
echo -e "${CYAN}1. Reload your shell:${NC}"
echo -e "   ${BOLD}source $SHELL_CONFIG${NC}"
echo -e ""
echo -e "${CYAN}2. Set up your AI backend:${NC}"
echo -e "   • For LiteLLM: Configure API keys and start proxy"
echo -e "     ${BOLD}export OPENAI_API_KEY='your-key'${NC}"
echo -e "     ${BOLD}ansai-litellm-proxy${NC}"
echo -e ""
echo -e "   • For Fabric: Set up patterns"
echo -e "     ${BOLD}fabric --setup${NC}"
echo -e ""
echo -e "${CYAN}3. Deploy your first AI-powered automation:${NC}"
echo -e "   ${BOLD}cd ~/.ansai/orchestrators/ansible${NC}"
echo -e "   ${BOLD}ansible-playbook playbooks/deploy-ai-powered-monitoring.yml${NC}"
echo -e ""
echo -e "${CYAN}4. Check out the documentation:${NC}"
echo -e "   ${BOLD}https://ansai.dev${NC}"
echo -e ""
echo -e "${CYAN}5. (Optional) Cursor IDE integration:${NC}"
echo -e "   ${BOLD}https://ansai.dev/integrations/CURSOR_IDE/${NC}"
echo -e ""

print_info "Quick test: Run ${BOLD}ansai-progress-tracker${NC} to test installation"

echo -e "\n${GREEN}${BOLD}Welcome to ANSAI! 🚀${NC}"
echo -e "${CYAN}AI-powered automation starts now.${NC}\n"

# Offer to reload shell
echo -e "${YELLOW}Note: You need to reload your shell for PATH changes to take effect.${NC}"
if can_prompt; then
    read -p "Open a new terminal or run: source $SHELL_CONFIG (press any key)" -n 1 -r < /dev/tty
    echo "" > /dev/tty
else
    echo -e "Run: ${BOLD}source $SHELL_CONFIG${NC}"
fi

# Clean up temp installer if it exists
if [ -f /tmp/ansai-install-temp.sh ]; then
    rm -f /tmp/ansai-install-temp.sh
fi

exit 0
