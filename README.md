# Red Hat PAI - Personal AI Infrastructure

Enterprise-focused Personal AI Infrastructure for Red Hat teams, providing unified context management across AI tools while maintaining Red Hat AI policy compliance.

## Features

- **Red Hat AI Policy Compliant**: Automatic routing for customer data
- **Multi-Tool Integration**: Gemini CLI, Cursor IDE, Fabric AI
- **Secure by Design**: External secrets management, no hardcoded credentials
- **TAM Workflow Tools**: Specialized scripts for Technical Account Managers
- **Enterprise Ready**: Clean separation of business contexts

## Quick Install

```bash
curl -sSL https://gitlab.cee.redhat.com/gvaughn/hatter-pai/-/raw/master/install.sh | bash
```

## What You Get

### AI Tools Integration
- **Gemini CLI**: `gemini` with Hatter personality and Red Hat context
- **Cursor IDE**: Project-specific rules and context
- **Fabric AI**: Red Hat compliant patterns and processing

### Red Hat Workflow Scripts
- **Case Management**: pai-case-processor, pai-supportshell, pai-case-sync-improved
- **Customer Tools**: pai-hydra, pai-onboard-customer, pai-meeting-prep
- **Compliance**: pai-compliance-check, pai-audit, pai-fabric-compliant
- **Documentation**: pai-confluence, pai-gdocs-sync, pai-projects

### Security & Compliance
- **Secrets Management**: External secrets in `~/.config/pai/secrets/`
- **Audit Logging**: Complete audit trail for all operations
- **Data Classification**: Automatic Red Hat model routing
- **Zero Hardcoded Credentials**: All authentication externalized

## Directory Structure

```
~/pai-context/
├── redhat/                 # Red Hat business context
│   ├── contexts/           # Hatter personality, Red Hat context
│   ├── config/             # Red Hat model configurations
│   └── bin/                # Red Hat workflow scripts
└── personal/               # Personal/other business contexts

~/.config/pai/
└── secrets/                # Secure credential storage (NOT in repo)
```

## Usage Examples

```bash
# Check current PAI status
pai-context-current

# Process a support case
pai-case-processor

# Generate compliance brief
pai-brief-generate

# Use Gemini with Red Hat context
gemini
> Run pai-supportshell for case 04243222
```

## Installation for Red Hat Teams

The installation script:
1. Creates Red Hat PAI context structure
2. Installs Red Hat specific workflow scripts
3. Configures Gemini CLI with Hatter personality
4. Sets up secure secrets management
5. Configures Cursor IDE integration

## Requirements

- Node.js (for Gemini CLI)
- Git access to gitlab.cee.redhat.com
- Red Hat VPN for internal model access

## Enterprise Deployment

This repository contains only Red Hat-specific content:
- No personal business information
- No health or consulting data
- No email sync or personal secrets
- Only Red Hat TAM and technical workflows

Perfect for enterprise sharing and team deployment while maintaining privacy separation.