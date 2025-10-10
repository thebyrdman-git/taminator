# fabric

AI-powered tool to augment human capabilities using a crowdsourced set of patterns.

## Location
`~/.local/bin/fabric`

## Description
Fabric is an open-source framework designed to augment human capabilities using AI. It provides a modular framework for solving specific problems using a crowdsourced set of AI prompts (patterns) that can be used across various AI models and vendors.

## Key Concepts

### Patterns
Pre-built prompts for specific use cases, stored as system prompts that guide the AI's behavior. Examples include:
- `analyze_claims` - Analyze claims made in content
- `analyze_incident` - Analyze security incidents
- `analyze_logs` - Analyze log files
- `analyze_paper` - Analyze academic papers
- `extract_wisdom` - Extract key insights from content
- `summarize` - Create summaries of content

### Contexts
Persistent conversation contexts that can be reused across sessions.

### Sessions
Individual conversation sessions that can be saved and resumed.

## Initial Setup
```bash
# Run interactive setup for all configurable parts
fabric -S
# or
fabric --setup
```

## Core Usage

### Basic Pattern Application
```bash
# Apply a pattern to input
echo "Your content here" | fabric -p analyze_claims

# Apply pattern with streaming output
cat document.txt | fabric -p summarize -s

# Apply pattern and copy to clipboard
fabric -p extract_wisdom -c < article.md
```

### Pattern Management
```bash
# List all available patterns
fabric -l
# or
fabric --listpatterns

# List newest patterns
fabric -n 10

# Update patterns from repository
fabric -U
# or
fabric --updatepatterns
```

### Model Configuration
```bash
# List available models
fabric -L
# or
fabric --listmodels

# Use specific model
fabric -p summarize -m gpt-4

# Change default model
fabric -d
# or
fabric --changeDefaultModel

# Use specific vendor
fabric -V "LM Studio" -m openai/gpt-oss-20b
```

### Advanced Features

#### YouTube Integration
```bash
# Analyze YouTube video transcript
fabric -y "https://youtube.com/watch?v=VIDEO_ID" -p summarize

# Get transcript with timestamps
fabric -y "URL" --transcript-with-timestamps

# Analyze video comments
fabric -y "URL" --comments

# Get video metadata
fabric -y "URL" --metadata
```

#### Web Scraping
```bash
# Scrape website to markdown
fabric -u "https://example.com" -p analyze_claims

# Search and analyze
fabric -q "search query" -p summarize
```

#### Context and Session Management
```bash
# List contexts
fabric -x

# List sessions
fabric -X

# Use specific context
fabric -C mycontext -p analyze_incident

# Use specific session
fabric --session=mysession

# Wipe context
fabric -w contextname

# Wipe session
fabric -W sessionname
```

#### Pattern Variables
```bash
# Use variables in patterns
fabric -p agility_story -v "#role:developer" -v "#points:5"

# Apply variables to user input
echo "Analyze this as #role" | fabric -p analyze_claims --input-has-vars -v "#role:security expert"
```

## TAM-Specific Use Cases

### Case Analysis
```bash
# Analyze case description
rhcase case get 12345678 | fabric -p analyze_incident

# Extract action items from case
rhcase kcs fetch 123456 | fabric -p extract_wisdom

# Summarize long case history
cat case_history.txt | fabric -p summarize -o case_summary.md
```

### Log Analysis
```bash
# Analyze error logs
cat /var/log/messages | fabric -p analyze_logs

# Extract patterns from logs
yank-ng --case 12345 | fabric -p analyze_incident
```

### Documentation Processing
```bash
# Convert complex docs to readable format
curl -s https://docs.example.com | fabric --readability | fabric -p summarize

# Analyze technical documentation
fabric -u "https://access.redhat.com/solutions/123456" -p extract_wisdom
```

### Communication Drafting
```bash
# Draft response based on analysis
echo "Customer reported issue with..." | fabric -p write_email_response

# Create executive summary
cat detailed_report.md | fabric -p create_executive_summary
```

## Output Options
```bash
# Save to file
fabric -p summarize -o output.md

# Save entire session
fabric -p analyze_incident --output-session -o session.md

# Stream output
fabric -p summarize -s

# Copy to clipboard
fabric -p extract_wisdom -c
```

## Model Parameters
```bash
# Set temperature (creativity)
fabric -p write_email -t 0.3

# Set top-p (nucleus sampling)
fabric -p summarize -T 0.95

# Set presence penalty
fabric -p analyze_claims -P 0.5

# Set frequency penalty
fabric -p summarize -F 0.3

# Set seed for reproducibility
fabric -e 12345
```

## Integration Examples

### With rhcase
```bash
# Analyze case patterns
rhcase list bny | fabric -p analyze_patterns

# Extract insights from KCS
rhcase kcs fetch 123456 | fabric -p extract_wisdom -o insights.md
```

### With SupportShell
```bash
# Analyze must-gather output
must-gather-explorer analyze /case/12345/must-gather.tar.gz | fabric -p analyze_logs

# Summarize diagnostic findings
sosreport-analyzer /tmp/sosreport.tar.xz | fabric -p summarize
```

### Daily Workflow
```bash
# Generate daily briefing
pai-my-plate | fabric -p create_executive_summary

# Analyze overnight cases
rhcase list cibc --since yesterday | fabric -p analyze_incidents
```

## Server Mode
```bash
# Serve REST API
fabric --serve --address=:8080 --api-key=your-key

# Serve with Ollama endpoints
fabric --serveOllama
```

## Extension System
```bash
# List extensions
fabric --listextensions

# Add extension
fabric --addextension=/path/to/extension.yaml

# Remove extension
fabric --rmextension=extension-name
```

## Best Practices

1. **Pattern Selection**: Choose patterns that match your specific use case
2. **Model Choice**: Use appropriate models for task complexity
3. **Context Preservation**: Use sessions for multi-turn analysis
4. **Output Format**: Save important analyses to files for reference
5. **Variable Usage**: Leverage variables for customizable patterns

## Common Patterns for TAMs

- `analyze_incident` - Security and operational incident analysis
- `analyze_logs` - Log file pattern extraction
- `analyze_claims` - Verify technical claims in documentation
- `extract_wisdom` - Pull key insights from technical docs
- `summarize` - Create concise summaries of long content
- `write_email_response` - Draft professional responses
- `analyze_paper` - Review technical papers and RFPs
- `create_executive_summary` - Generate executive-level summaries

## Notes
- Requires API keys for cloud models (configured during setup)
- Supports multiple AI vendors (OpenAI, Anthropic, Google, Ollama, etc.)
- Patterns are community-contributed and regularly updated
- Can work with local models via Ollama or LM Studio
