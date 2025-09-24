# Fabric Patterns Documentation

## Overview
Comprehensive documentation of all fabric patterns available for PAI TAM workflows, automatically generated and updated.

**Last Updated**: $(date -u +"%Y-%m-%d %H:%M:%S UTC")

## Custom TAM Patterns
Located in `~/.config/fabric/custom_patterns/`

### analyze_case
**Purpose**: You are a Senior Technical Account Manager (TAM) at Red Hat with expertise in systematic case analysis. Your job is to analyze support cases using proven troubleshooting methodology and generate structured analysis outputs.  
**Status**: ✅ Working
**Usage**: 
```bash
fabric -p analyze_case -m gpt-4o
```

### analyze_case_support
**Purpose**: 
**Status**: ❌ Error or timeout
**Usage**: 
```bash
fabric -p analyze_case_support -m gpt-4o
```

### redact_tam_data
**Purpose**: You are a data redaction specialist for Technical Account Manager (TAM) workflows at Red Hat. Your job is to sanitize sensitive customer information while preserving the technical content needed for analysis.  
**Status**: ✅ Working
**Usage**: 
```bash
fabric -p redact_tam_data -m gpt-4o
```

### tam_case_screen
**Purpose**: You are a Senior Technical Account Manager (TAM) at Red Hat with expertise in systematic case analysis. Your job is to perform initial case screening following proven TAM methodology to generate structured analysis outputs for technical support cases.  
**Status**: ✅ Working
**Usage**: 
```bash
fabric -p tam_case_screen -m gpt-4o
```

### tam_daily_brief
**Purpose**: You are a Technical Account Manager (TAM) at Red Hat specializing in generating daily activity briefings. Your job is to analyze TAM case data, account status, and priority items to create a structured daily "My Plate" briefing.  
**Status**: ✅ Working
**Usage**: 
```bash
fabric -p tam_daily_brief -m gpt-4o
```

## Standard Fabric Patterns (TAM-Relevant)

### analyze_incident
**Purpose**: Security and operational incident analysis
**Status**: ✅ Working
**Usage**: 
```bash
cat incident_report.txt | fabric -p analyze_incident -m gpt-4o
```

### analyze_logs
**Purpose**: Log file analysis and pattern extraction
**Status**: ✅ Working
**Usage**:
```bash
yank-ng --case 12345 --pattern "error" | fabric -p analyze_logs -m gpt-4o
```

### summarize
**Purpose**: Create concise summaries of long content
**Status**: ✅ Working
**Usage**:
```bash
cat long_document.md | fabric -p summarize -m gpt-4o
```

### extract_wisdom
**Purpose**: Extract key insights from technical documentation
**Status**: ✅ Working
**Usage**:
```bash
rhcase kcs fetch 123456 | fabric -p extract_wisdom -m gpt-4o
```

### analyze_claims
**Purpose**: Verify and analyze technical claims
**Status**: ✅ Working
**Usage**:
```bash
cat technical_proposal.txt | fabric -p analyze_claims -m gpt-4o
```

### clean_text
**Purpose**: Clean and format text content
**Status**: ✅ Working
**Usage**:
```bash
cat messy_text.txt | fabric -p clean_text -m gpt-4o
```

## Model Compatibility

### Working Models (Tested with Patterns)
- **gpt-4o**: ✅ Best compatibility, recommended for all patterns
- **gemini-pro**: ✅ Good compatibility, large context window
- **perplexity-sonar-large**: ✅ Best for research patterns

### Models Under Investigation
- **remote-local-granite-3-2-8b-instruct**: ❌ Currently giving math responses instead of following patterns
- **remote-local-mistral-7b-instruct**: ❌ Currently giving math responses instead of following patterns
- **gpt-5-reasoning**: ⚠️ Use for complex reasoning, may not follow all patterns

## Integration with PAI Tools

### pai-fabric Wrapper
Provides simplified access to fabric patterns:
```bash
pai-fabric redact    # Uses redact_tam_data pattern
pai-fabric analyze   # Uses analyze_case pattern  
pai-fabric research  # Uses extract_wisdom pattern
pai-fabric brief     # Uses summarize pattern
```

### TAM Workflow Integration
```bash
# Case analysis with workspace integration
pai-workspace case 04056105 analyze
# Internally uses: fabric -p tam_case_screen -m gpt-4o

# Daily briefing generation
pai-my-plate | fabric -p tam_daily_brief -m gpt-4o

# Research integration
rhcase kcs search "terms" | fabric -p extract_wisdom -m perplexity-sonar-large
```

## Pattern Development Workflow

### For rhcase Integration
When developing new patterns for rhcase workflows:

1. **Identify the workflow need**:
   ```bash
   # Example: Need pattern for KCS analysis
   rhcase kcs fetch 123456 > sample_kcs.md
   ```

2. **Create pattern directory**:
   ```bash
   mkdir -p ~/.config/fabric/custom_patterns/analyze_kcs
   ```

3. **Write system.md**:
   ```markdown
   # IDENTITY and PURPOSE
   You are a TAM expert at analyzing Red Hat KCS articles...
   
   # STEPS
   - Extract key technical information
   - Identify applicability to current case
   - Suggest implementation steps
   
   # OUTPUT INSTRUCTIONS
   [Specific format for KCS analysis]
   ```

4. **Test the pattern**:
   ```bash
   cat sample_kcs.md | fabric -p analyze_kcs -m gpt-4o
   ```

5. **Update documentation**:
   ```bash
   pai-update-pattern-docs
   ```

### Pattern Naming Convention
- **TAM-specific**: `tam_*` (tam_case_screen, tam_daily_brief)
- **RH-specific**: `rh_*` (rh_kcs_analyze, rh_jira_summary)
- **Workflow-specific**: `*_tam_data` (redact_tam_data, normalize_tam_data)

## Testing and Validation

### Pattern Testing Commands
```bash
# Test all custom patterns
for pattern in ~/.config/fabric/custom_patterns/*/; do
    pattern_name=$(basename "$pattern")
    echo "Testing $pattern_name..."
    echo "test input" | fabric -p "$pattern_name" -m gpt-4o >/dev/null 2>&1 && echo "✅" || echo "❌"
done

# Update documentation after changes
pai-update-pattern-docs
```

### Validation Checklist
- [ ] Pattern responds appropriately to test input
- [ ] Output format matches expectations
- [ ] No math or irrelevant responses
- [ ] Compatible with gpt-4o model
- [ ] Documented in this file

## Future Pattern Ideas
Based on TAM workflows that could benefit from patterns:

- `rh_kcs_analyze` - Analyze KCS articles for case relevance
- `rh_jira_summary` - Summarize JIRA issues and RFEs
- `tam_collaboration_request` - Generate SBR collaboration requests
- `tam_cap_critsit_comms` - CAP/CritSit communication templates
- `tam_proactive_packager` - Proactive case packaging
- `tam_multi_vendor` - Multi-vendor coordination
- `tam_rfe_tracker` - RFE/bug tracking and status
- `supportshell_analysis` - SupportShell output analysis

## Update Instructions
To update this documentation:
```bash
pai-update-pattern-docs
```

This will automatically scan all patterns, test their functionality, and regenerate this documentation.
