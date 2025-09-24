# Fabric AI + LiteLLM: Red Hat Model Selection Guide

## 🎯 **The Core Concept**

**Fabric AI is model-agnostic** - it knows about hundreds of models from different providers. The only difference for Red Hat compliance is **telling Fabric which model name to use**.

## 🏗️ **Architecture Overview**

```
PAI Script → Fabric AI → Model Selection → LiteLLM Proxy → Red Hat Granite
     ↑            ↑           ↑              ↑                ↑
Smart Wrapper  Universal   Model Name    Bridge to RH    AIA-Approved
Detection      Framework   Selection     Infrastructure     Models
```

## 🔄 **Model Selection Examples**

### Customer Data (Compliance Required)
```bash
# PAI scripts automatically choose Red Hat models
pai-fabric-compliant --pattern extract_wisdom customer_case.md

# Internally executes:
fabric --model granite-34b-instruct --pattern extract_wisdom customer_case.md
#                ↑
#         Red Hat compliant model via LiteLLM
```

### Personal Data (Any Model)
```bash
# Direct Fabric usage - your choice of model
fabric --model gpt-4o --pattern daily_brief personal_emails.md
fabric --model gemini-pro --pattern summarize research_notes.md
fabric --model claude-3-5-sonnet --pattern analyze_trends data.csv

# All work directly, no special routing needed
```

### Hybrid Processing (Smart Detection)
```bash
# pai-fabric-hybrid detects content and chooses model
pai-fabric-hybrid --pattern process_mixed_content document.md

# If customer data detected:
# fabric --model granite-34b-instruct --pattern process_mixed_content

# If personal data:
# fabric --model gpt-4o --pattern process_mixed_content
```

## 🛠️ **Available Models in Your Fabric Installation**

### Via Direct APIs
```bash
# OpenAI models
fabric --model gpt-4o
fabric --model gpt-5
fabric --model o1-preview

# Google models
fabric --model gemini-pro
fabric --model gemini-flash

# Anthropic models
fabric --model claude-3-5-sonnet
fabric --model claude-3-haiku
```

### Via LiteLLM Proxy (Red Hat Infrastructure)
```bash
# Red Hat Granite models (via LiteLLM on grimm@rhgrimm)
fabric --model granite-34b-instruct
fabric --model granite-7b-instruct
fabric --model granite-3b-instruct

# These route: Fabric → LiteLLM Proxy → Red Hat Infrastructure
```

## 🎭 **PAI Script Intelligence**

### pai-fabric-compliant
**Purpose**: Guarantees Red Hat compliance
```bash
pai-fabric-compliant --pattern extract_recommendations customer_ticket.md

# Always uses: --model granite-34b-instruct
# Never uses external APIs for customer data
# Includes audit logging
```

### pai-fabric-hybrid
**Purpose**: Smart model selection based on content
```bash
pai-fabric-hybrid --pattern summarize mixed_document.md

# Content analysis:
# - Contains "customer", "case", "confidential" → granite-34b-instruct
# - Personal notes, research → gpt-4o
# - Unknown content → defaults to granite-34b-instruct (safer)
```

### pai-case-processor
**Purpose**: Support case analysis (always compliant)
```bash
pai-case-processor support_case_04243222.json

# Automatically uses granite-34b-instruct
# Includes Red Hat context and audit trail
# Never sends customer data to external APIs
```

## 🔐 **Compliance Rules**

### Automatic Model Selection
1. **Customer data detected** → `granite-34b-instruct` (via LiteLLM)
2. **Internal analysis** → `granite-7b-instruct` (efficiency)
3. **Personal content** → User's preferred model
4. **Unknown/mixed** → `granite-34b-instruct` (safe default)

### Content Detection Keywords
PAI scripts detect Red Hat content by:
- **File paths**: `/rh/`, `customer`, `cases`
- **Content keywords**: "customer", "case", "supportshell", "TAM"
- **File extensions**: `.rh`, `.case`
- **Explicit flags**: `--redhat`, `--customer-data`

## 🚀 **Usage Patterns**

### Daily TAM Workflow
```bash
# Process morning cases - automatically compliant
pai-case-processor $(ls ~/Documents/rh/cases/new/)

# Analyze customer emails - Red Hat models only
pai-email-processor --folder customer_communications

# Personal research - any model you prefer
fabric --model gpt-4o --pattern extract_insights industry_research.md
```

### Development Work
```bash
# Red Hat project documentation - compliant processing
pai-fabric-compliant --pattern improve_writing project_proposal.md

# Personal coding notes - direct model access
fabric --model claude-3-5-sonnet --pattern code_review personal_script.py
```

## 🔧 **Configuration**

### LiteLLM Proxy Setup
The LiteLLM proxy on `grimm@rhgrimm` exposes Red Hat models:

```yaml
# /home/grimm/litellm-config.yaml
model_list:
  - model_name: granite-34b-instruct
    litellm_params:
      model: granite-34b-instruct
      base_url: http://rh-internal-models:8080
      api_key: ${RH_MODEL_API_KEY}
```

### Fabric Configuration
Fabric knows about LiteLLM models running locally at localhost:4000:

```bash
# LiteLLM proxy starts automatically with redhat-pai installation
# Fabric sees granite models as regular options at localhost:4000
fabric --list-models | grep granite
granite-34b-instruct
granite-7b-instruct
granite-3b-instruct
```

## ✅ **Benefits of This Approach**

1. **Single Fabric Installation**: One tool knows all models
2. **Transparent Integration**: LiteLLM models work like any other model
3. **Smart Compliance**: PAI scripts handle model selection automatically
4. **Flexibility**: Direct access to any model for personal work
5. **Audit Trail**: All Red Hat model usage logged through LiteLLM
6. **No Special Setup**: Fabric + LiteLLM + smart PAI scripts = complete solution

---

*Simple model selection, powerful compliance*
*One Fabric installation, universal model access*
*Smart PAI scripts for automatic Red Hat compliance*