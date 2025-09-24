# Red Hat PAI - Global Integration

## 🌍 This Project is Part of Universal PAI System

This Red Hat PAI project is integrated with your global PAI infrastructure and is **not limited to this directory**.

### ✅ Global Configuration Active

**Primary Config Files (Universal)**:
- `~/AGENTS.md` - Universal agent config for Cursor (works everywhere)
- `~/GEMINI.md` - Universal Hatter config for Gemini CLI (works everywhere)
- `~/pai-context/` - Global PAI context system
- `~/.claude/context/` → symlinked to `~/pai-context/`

**This Project's Role**:
- Contains Red Hat PAI scripts and tools
- Provides Red Hat-specific documentation
- Enhances global PAI with TAM workflows
- **But Hatter and PAI tools work everywhere, not just here**

### 🛠️ Red Hat PAI Tools (Global Access)

All these tools work from **any directory**, not just this project:

```bash
# From ~/Desktop/, ~/Downloads/, ~/Documents/, anywhere:
pai-case-processor          # Process Red Hat support cases
pai-supportshell           # SupportShell integration
pai-compliance-check       # Check Red Hat AI policy compliance
pai-contact-intelligence   # Customer analysis

# All 62+ scripts from ~/.local/bin/pai-scripts-from-rhgrimm/
# Available globally via PATH
```

### 🎯 Smart Context Detection

Hatter automatically switches to Red Hat compliance mode when:
- Working with files containing "customer", "case", "TAM"
- In directories with Red Hat content
- Processing .rh files
- **Regardless of current directory location**

### 🏢 Universal Business Context

```bash
# These work from anywhere:
~/Desktop/meeting-notes/     # Hatter available for note-taking
~/Downloads/attachments/     # Auto-detects Red Hat content
~/Documents/rh/cases/       # Red Hat compliance mode activates
~/coding/personal/          # Personal mode with full creativity
```

### 🔐 Global Compliance

Red Hat AI Policy compliance is enforced universally:
- **Customer data**: AIA-approved models only (anywhere you work)
- **Audit logging**: All operations tracked (global)
- **Secure processing**: Via grimm@rhgrimm when needed (universal)
- **No external APIs**: For customer data (enforced everywhere)

### 📁 Project Structure vs Global Access

```
This Project Directory:
~/coding/gitlabs/active/redhat-pai/
├── bin/                    # Scripts (also in global PATH)
├── contexts/              # Red Hat contexts
├── AGENTS.md              # References global config
├── GEMINI.md              # References global config
└── README.md              # Project documentation

Global PAI System:
~/AGENTS.md                # Universal Cursor config
~/GEMINI.md                # Universal Gemini CLI config
~/pai-context/             # Universal context system
├── redhat/               # Red Hat contexts
├── personal/             # Personal contexts
└── businesses/           # Business contexts
```

### 🎭 Consistent Experience

Whether you're working:
- **In this project directory**: Full Red Hat PAI functionality
- **In ~/Documents/**: Hatter available with context detection
- **In ~/Desktop/**: Same Hatter personality, universal tools
- **In ~/Downloads/**: Auto-detects Red Hat content for compliance

### 🚀 Benefits of Global Integration

1. **Location Independence**: PAI works everywhere you work
2. **Smart Context Switching**: Automatic Red Hat compliance when needed
3. **Universal Tool Access**: All 62+ scripts available globally
4. **Consistent Personality**: Same Hatter across all directories
5. **Centralized Configuration**: Single point of control for updates

---

*This Red Hat PAI project enhances your universal PAI system*
*Hatter and tools available everywhere, not just in coding directories*
*Global compliance and context detection active across all locations*