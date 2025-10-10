# LiteLLM Integration - Critical Component for Red Hat PAI

## 🎯 LiteLLM's Essential Role

LiteLLM is the **critical bridge** that enables Fabric AI to work with Red Hat-hosted models for compliance.

### 🏗️ Architecture Flow
```
Fabric AI → LiteLLM Proxy → Red Hat Granite Models
    ↑           ↑                    ↑
User Tools   Translation      AIA-Approved Models
             Bridge           (Compliance Required)
```

## 🔗 Integration Points

### With Fabric AI
- **pai-fabric-compliant**: Routes through LiteLLM for Red Hat compliance
- **pai-fabric-hybrid**: Manages local vs remote model routing
- **Model Translation**: LiteLLM handles model name translation
- **API Standardization**: Provides OpenAI-compatible API for Fabric

### With Red Hat Infrastructure
- **grimm@rhgrimm**: LiteLLM proxy hosted on remote system
- **Granite Models**: Direct access to AIA-approved models
- **Compliance Bridge**: Ensures customer data uses approved models only
- **Audit Trail**: LiteLLM logs all model requests for compliance

## 🛠️ PAI Tools with LiteLLM Integration

### Fabric-Based Tools
```bash
# These tools depend on LiteLLM for Red Hat compliance:
pai-fabric-compliant       # Direct LiteLLM proxy usage
pai-fabric-hybrid          # Smart routing via LiteLLM
pai-email-processor        # Uses Fabric patterns via LiteLLM
pai-case-processor         # Customer data via LiteLLM only
```

### Model Routing Strategy
```yaml
# LiteLLM Configuration (on grimm@rhgrimm)
model_list:
  - model_name: granite-34b-instruct
    litellm_params:
      model: granite-34b-instruct
      base_url: http://rh-internal-models:8080

  - model_name: granite-7b-instruct
    litellm_params:
      model: granite-7b-instruct
      base_url: http://rh-internal-models:8080
```

## 🔐 Compliance Integration

### Customer Data Processing
- **Fabric Patterns**: Must route through LiteLLM for customer data
- **Model Selection**: LiteLLM ensures only approved Granite models used
- **Audit Logging**: All requests logged through LiteLLM proxy
- **Access Control**: Customer data never hits external APIs

### Development vs Production
```bash
# Development (Personal Data)
fabric --pattern extract_wisdom input.md
# → Can use any model directly

# Production (Customer Data)
pai-fabric-compliant --pattern extract_wisdom customer_case.md
# → MUST route through LiteLLM → Red Hat Granite models
```

## 🌐 Global Availability

### Local Processing (via Red Hat VPN)
- **LiteLLM Proxy**: Running locally on your system (localhost:4000)
- **VPN Access**: Red Hat VPN tunnel for model access
- **Local Installation**: Part of redhat-pai setup process
- **Model Caching**: LiteLLM handles local optimization

### Local Integration
```bash
# PAI tools automatically detect compliance needs:
pai-fabric-compliant       # Forces LiteLLM routing
fabric                     # Direct access (non-customer data)
```

## 🔧 Technical Stack

### Core Components
1. **Fabric AI**: Pattern-based AI processing framework
2. **LiteLLM**: Model proxy and translation layer
3. **Red Hat Granite**: AIA-approved language models
4. **PAI Scripts**: Orchestration and compliance enforcement

### Integration Chain
```
User Request
    ↓
PAI Script Detection (customer data?)
    ↓ (if yes)
LiteLLM Proxy (grimm@rhgrimm)
    ↓
Red Hat Granite Model
    ↓
Compliant Response
```

## 📊 Usage Examples

### Compliant Customer Analysis
```bash
# Customer case analysis - MUST use LiteLLM
pai-case-processor customer_issue.txt
# → Detects customer data
# → Routes through LiteLLM proxy
# → Uses Red Hat Granite models only
# → Returns analysis with audit trail
```

### Personal Content Processing
```bash
# Personal document - Can use any model
fabric --pattern summarize personal_notes.md
# → Direct Fabric access
# → Uses configured personal models
# → No LiteLLM routing needed
```

## 🚨 Critical Dependencies

### For Red Hat Compliance
- **LiteLLM Proxy**: Must be running on grimm@rhgrimm
- **SSH Access**: Required for remote model access
- **Granite Models**: Must be available via LiteLLM
- **PAI Scripts**: Handle automatic routing decisions

### Failure Modes
```bash
# If LiteLLM proxy unavailable:
pai-fabric-compliant → Error: Cannot process customer data
fabric → Works normally (personal data only)

# If SSH connection fails:
pai-case-processor → Falls back to local processing (non-compliant)
```

---

*LiteLLM: The Essential Bridge for Red Hat PAI Compliance*
*Enabling Fabric AI integration with AIA-approved models*
*Critical component for customer data processing*