# pai-workspace

PAI integration tool for existing TAM directory structure.

## Location
`~/.local/bin/pai-workspace`

## Description
Bridges PAI tools with your existing TAM workspace at `/home/grimm/Documents/rh/projects/`. Provides commands to manage cases, run analyses, and sync outputs between PAI and your established multi-specialty directory structure.

## TAM Specialties Supported
- **tam-ocp**: OpenShift Container Platform TAM
- **tam-ai**: Red Hat AI Portfolio TAM  
- **tam-sec**: Security TAM (all products)

## Directory Structure
Your TAM workspace follows this pattern:
```
/home/grimm/Documents/rh/projects/
├── tam-ocp/                   # OpenShift Container Platform
├── tam-ai/                    # Red Hat AI Portfolio
├── tam-sec/                   # Security (all products)
└── _system/                   # Templates and automation

Each specialty contains:
<specialty>/
├── <account>/                 # e.g., bny, cibc, citi, discover
│   ├── account-info/
│   │   ├── architecture/
│   │   ├── contacts/
│   │   └── environments/
│   ├── casework/
│   │   ├── active/
│   │   │   └── <case_number>/
│   │   │       ├── extracts/      # Case JSON exports
│   │   │       ├── pieces/        # Analysis outputs
│   │   │       ├── kcs/          # KCS articles
│   │   │       ├── jira/         # JIRA issues
│   │   │       ├── attachments/  # Customer files
│   │   │       ├── reports/      # Generated reports
│   │   │       ├── PRPs/         # Problem Resolution Plans
│   │   │       ├── scripts/      # Case-specific scripts
│   │   │       └── validation_results/
│   │   └── resolved/
│   ├── communications/
│   └── strategic/
```

## Commands

### List Accounts
```bash
pai-workspace list
# Shows all accounts by specialty with active case counts
```

Example output:
```
Active TAM Accounts by Specialty:
=================================

[tam-ocp]
  bny:        6 active cases
  cibc:      26 active cases
  citi:       6 active cases
  discover:  20 active cases

[tam-ai]
  (ready for accounts)

[tam-sec]
  (ready for accounts)
```

### Case Operations
```bash
# Show case information (searches all specialties)
pai-workspace case 04056105 info

# Change to case directory
pai-workspace case 04056105 open

# Run AI analysis and save to case
pai-workspace case 04056105 analyze
```

### Create New Case
```bash
# Create case (auto-detect account specialty)
pai-workspace create <account> <case_number>
pai-workspace create bny 04123456

# Create case in specific specialty
pai-workspace create <specialty> <account> <case_number>
pai-workspace create tam-ai cibc 04789012
```

### Create Account Links
```bash
# Create link (auto-detect specialty)
pai-workspace link <account>
pai-workspace link cibc

# Create link for specific specialty
pai-workspace link <specialty> <account>
pai-workspace link tam-sec discover
```

### Sync PAI Outputs
```bash
pai-workspace sync <case_number>
# Copies PAI outputs to case pieces directory
```

## Integration with PAI Tools

### Enhanced Case Initial Screen
The `pai-case-initial-screen-v2` tool auto-detects case directories across all specialties:
```bash
# Just provide case number - searches all specialties automatically
pai-case-initial-screen-v2 -a -c 04056105

# Or use pai-workspace for full integration
pai-workspace case 04056105 analyze
```

### Workflow Examples

#### New Case Workflow
```bash
# 1. Create case structure
pai-workspace create bny 04123456

# 2. Add case data to extracts directory
rhcase analyze 04123456 > ~/Documents/rh/projects/tam-ocp/bny/casework/active/04123456/extracts/case.json

# 3. Run initial analysis
pai-workspace case 04123456 analyze

# 4. Fetch related resources
cd ~/Documents/rh/projects/tam-ocp/bny/casework/active/04123456
rhcase kcs search "relevant terms" | fabric -p extract_wisdom > kcs/search_results.md
rhcase jira search "issue keywords" > jira/related_issues.md
```

#### Cross-Specialty Case Review
```bash
# List all active cases across specialties
pai-workspace list

# Find a case without knowing which specialty it's in
pai-workspace case 04056105 info
# Output shows: Specialty: tam-ocp, Account: bny

# Generate daily brief across all specialties
pai-my-plate > ~/Documents/rh/projects/reports/daily-$(date +%Y%m%d).md
```

#### Specialty-Specific Workflows

**OpenShift TAM (tam-ocp)**:
```bash
# Create OCP-specific case
pai-workspace create tam-ocp cibc 04567890

# Analyze with OCP context
pai-workspace case 04567890 analyze
```

**AI TAM (tam-ai)**:
```bash
# Create AI portfolio case
pai-workspace create tam-ai newclient 04111222

# Focus on AI-specific analysis
fabric -p analyze_ai_issue < case_description.txt
```

**Security TAM (tam-sec)**:
```bash
# Create security-focused case
pai-workspace create tam-sec enterprise 04333444

# Security-specific analysis
fabric -p analyze_security_incident < security_report.txt
```

## Configuration
Edit `~/.claude/pai/config/workspace.yaml` to:
- Add new accounts to specialties
- Customize directory structures
- Define output mappings
- Set specialty-specific product lists

## Symbolic Links
PAI workspace links are created at:
- `~/.claude/pai/workspace/tam-ocp` → Main OCP TAM directory
- `~/.claude/pai/workspace/tam-ai` → AI TAM directory  
- `~/.claude/pai/workspace/tam-sec` → Security TAM directory
- `~/.claude/pai/workspace/<specialty>-<account>` → Individual account directories

## Best Practices
1. **Case Creation**: Always use `pai-workspace create` to ensure consistent structure
2. **Specialty Awareness**: Specify specialty when creating accounts in new areas
3. **Data Organization**: Keep raw data in `extracts/`, analysis in `pieces/`
4. **Resource Collection**: Save KCS/JIRA content to respective directories
5. **Cross-Specialty Search**: Use case commands without specialty - they search everywhere
6. **Report Generation**: Use `reports/` for formal documentation
7. **Version Control**: Consider git repos per specialty or per account

## Integration Points
- Works with `rhcase` for data collection across all specialties
- Integrates with `fabric` for AI-powered analysis
- Compatible with `pai-case-initial-screen-v2` for automated screening
- Syncs with PAI output directories
- Maintains your existing multi-specialty workflow
- Supports specialty-specific product configurations

## Error Handling
- Searches across all specialties when case location is unknown
- Provides clear specialty identification in output
- Handles missing directories gracefully
- Validates account existence before operations