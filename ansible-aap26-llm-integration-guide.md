# Ansible Automation Platform 2.6 - LLM Integration Guide

**Date:** October 16, 2025  
**Source:** Red Hat official documentation and web research  
**Status:** Current as of AAP 2.6 release

---

## Executive Summary

Ansible Automation Platform 2.6 introduces **Ansible Lightspeed intelligent assistant**, an AI-powered chat interface that requires LLM integration. Unlike general-purpose LLM APIs, AAP 2.6 has **specific hosting and model requirements**.

---

## Supported LLM Integration Options

### Option 1: IBM watsonx Code Assistant (Recommended - Production Ready)

**Overview:**
- Purpose-built for Ansible automation
- Powered by IBM Granite models specifically trained on Ansible playbooks
- Official Red Hat partnership
- Production-ready and fully supported

**Deployment Models:**
1. **SaaS (Cloud-hosted by IBM)**
   - Fastest time to value
   - Managed by IBM
   - No infrastructure requirements
   - Subscription-based pricing

2. **Self-hosted (On-premises)**
   - Full data control
   - Air-gapped deployment supported
   - Requires your own infrastructure
   - Ideal for regulated industries

**Key Features:**
- Ansible-specific code generation
- Trained on extensive Ansible playbook datasets
- Best practices enforcement
- Syntax validation
- Role and task recommendations

**Requirements:**
- AAP 2.6 on OpenShift Container Platform
- IBM watsonx subscription
- Integration via Ansible Lightspeed

---

### Option 2: Red Hat Enterprise Linux AI (RHEL AI)

**Overview:**
- Self-hosted LLM platform
- Open-source Granite models from IBM Research
- InstructLab model alignment tools included
- Bootable RHEL image optimized for AI workloads

**Architecture:**
```
Ansible Lightspeed → vLLM Server → Granite Models (RHEL AI)
     (AAP 2.6)         (Inference)    (Self-hosted)
```

**Supported Inference Engine:**
- **vLLM Server** - Required for model serving
- Must be accessible via secure connection from AAP
- API endpoint configured in Ansible Lightspeed chatbot operator

**Available Models:**
- IBM Granite family (general purpose)
- Granite 3.0, 3.1, 3.2 series (8B parameters)
- Granite Code models (code-specific)
- Can fine-tune with InstructLab

**Requirements:**
- Dedicated RHEL AI server/infrastructure
- GPU recommended for performance (inference workload)
- Network connectivity to AAP 2.6 on OpenShift
- vLLM Server deployment

**Deployment:**
- Bootable RHEL AI image installation
- Model download and configuration
- vLLM Server setup
- Chatbot operator configuration in AAP

---

### Option 3: Red Hat OpenShift AI

**Overview:**
- Enterprise AI platform on OpenShift
- Managed AI/ML workflows
- Model serving infrastructure included
- GPU acceleration support

**Architecture:**
```
Ansible Lightspeed → OpenShift AI Model Serving → Granite Models
     (AAP 2.6)           (KServe/vLLM)              (Deployed)
```

**Features:**
- JupyterLab for model development
- Data science pipelines
- Model registry and versioning
- GPU resource management
- Multi-model serving

**Available Models:**
- IBM Granite models (included)
- Custom fine-tuned models
- Community models (via model registry)
- Support for multiple model formats

**Requirements:**
- OpenShift Container Platform cluster
- OpenShift AI subscription
- GPU nodes (recommended for LLM inference)
- AAP 2.6 deployed on same or accessible OpenShift cluster

**Deployment:**
- OpenShift AI operator installation
- Model deployment via model serving
- Chatbot operator configuration in AAP

---

## Emerging Option: Model Context Protocol (MCP) - Technology Preview

**Status:** Technology Preview in AAP 2.6  
**Availability:** Not for production use

**Overview:**
- Open protocol developed by Anthropic
- Standardizes LLM context and tool access
- Enables broader LLM compatibility
- Allows any MCP-compatible LLM to invoke AAP

**Potential Future Support:**
- OpenAI (GPT models)
- Anthropic (Claude models)
- Google (Gemini models)
- Other MCP-compatible providers

**Architecture:**
```
External LLM → MCP Server → Ansible Lightspeed → AAP 2.6
  (Any MCP)    (Protocol)    (Integration)       (Execution)
```

**Policy Enforcement:**
- Open Policy Agent (OPA) framework integration
- Guardrails for AI agent access
- Security and compliance controls

**When to Consider:**
- Future planning (2025+)
- Proof-of-concept testing
- Not for production workloads yet

---

## Deployment Architecture

### Standard Architecture
```
┌─────────────────────────────────────────────────────────┐
│ Ansible Automation Platform 2.6                         │
│ (OpenShift Container Platform)                          │
│                                                          │
│  ┌─────────────────────────────────────────────┐       │
│  │ Ansible Lightspeed Intelligent Assistant    │       │
│  │ (Chatbot Operator)                          │       │
│  └────────────────┬────────────────────────────┘       │
│                   │                                      │
│                   │ API Connection                       │
│                   │ (Secure HTTPS)                       │
└───────────────────┼──────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│ LLM Provider (Choose One)                               │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ Option 1: IBM watsonx Code Assistant                    │
│   - SaaS: IBM Cloud                                     │
│   - Self-hosted: Your infrastructure                    │
│                                                          │
│ Option 2: Red Hat Enterprise Linux AI                   │
│   - vLLM Server (inference engine)                      │
│   - Granite models (self-hosted)                        │
│   - Dedicated RHEL AI server                            │
│                                                          │
│ Option 3: Red Hat OpenShift AI                          │
│   - Model serving (KServe/vLLM)                         │
│   - Granite models (deployed on OpenShift)              │
│   - Same or separate OpenShift cluster                  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Configuration Requirements

### Ansible Lightspeed Chatbot Operator Configuration

**Required Secret Configuration:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: chatbot-config
  namespace: ansible-automation-platform
type: Opaque
stringData:
  config.yaml: |
    llm:
      provider: "rhel-ai"  # or "openshift-ai" or "watsonx"
      endpoint: "https://vllm-server.example.com/v1"
      api_key: "your-api-key"
      model: "granite-3.2-8b-instruct"
    
    # Optional: MCP Server (Tech Preview)
    mcp:
      enabled: false
      server_url: "https://mcp-server.example.com"
```

**Deployment:**
1. Create configuration secret
2. Deploy chatbot operator via AAP installer
3. Verify LLM connectivity
4. Test Ansible Lightspeed in AAP UI

---

## Model Selection Guide

### IBM Granite Model Family

| Model | Parameters | Context | Best For | Deployment |
|-------|------------|---------|----------|------------|
| Granite (Ansible-tuned) | Unknown* | Unknown* | Ansible code generation | watsonx Code Assistant |
| Granite 3.2 8B Instruct | 8B | 4096 tokens | General purpose chat | RHEL AI / OpenShift AI |
| Granite 3.1 8B Instruct | 8B | 4096 tokens | General purpose tasks | RHEL AI / OpenShift AI |
| Granite 8B Code Instruct | 8B | 4096 tokens | Code generation | RHEL AI / OpenShift AI |

*IBM watsonx Code Assistant uses proprietary Ansible-tuned Granite models - exact specifications not publicly disclosed

### Choosing the Right Model

**For Production Ansible Code Generation:**
- **IBM watsonx Code Assistant** - Purpose-built, most accurate for Ansible

**For General Ansible Q&A:**
- **Granite 3.2 8B Instruct** - Latest general-purpose model
- **Granite 8B Code Instruct** - If answering code-related questions

**For Cost Control:**
- **RHEL AI with Granite 3.2 8B** - Self-hosted, no per-token costs
- Lower resource requirements than larger models

**For Air-gapped Environments:**
- **RHEL AI** - Fully disconnected deployment
- **IBM watsonx (self-hosted)** - Enterprise air-gapped option

---

## Hardware Requirements

### RHEL AI Infrastructure

**Minimum Requirements:**
- 8 vCPU
- 32 GB RAM
- 100 GB storage
- RHEL 9.x compatible hardware

**Recommended for Production:**
- 16+ vCPU
- 64 GB+ RAM
- GPU acceleration (NVIDIA A100/H100 recommended)
- 500 GB+ storage for models and data

**GPU Considerations:**
- Optional but highly recommended for production
- 8B parameter models: 16+ GB VRAM
- Significantly improves inference latency
- NVIDIA GPUs with CUDA support

### OpenShift AI Infrastructure

**OpenShift Cluster Requirements:**
- Minimum 3 worker nodes
- 8 vCPU per node
- 32 GB RAM per node
- GPU nodes recommended for model serving

**GPU Worker Nodes (Recommended):**
- NVIDIA A100, H100, or equivalent
- Node Feature Discovery Operator
- NVIDIA GPU Operator
- At least 1 GPU node for model serving

---

## Integration vs. Self-hosted Decision Matrix

| Factor | IBM watsonx SaaS | IBM watsonx Self-hosted | RHEL AI | OpenShift AI |
|--------|------------------|------------------------|---------|--------------|
| **Setup Time** | Days | Weeks | Weeks | Weeks |
| **Infrastructure** | None required | Significant | Moderate | Significant |
| **Data Sovereignty** | IBM Cloud | Full control | Full control | Full control |
| **Air-gapped Support** | No | Yes | Yes | Yes |
| **Ansible Optimization** | Excellent | Excellent | Good | Good |
| **Ongoing Costs** | Subscription + usage | Subscription | Subscription | Subscription |
| **GPU Requirements** | N/A (IBM manages) | Yes (recommended) | Recommended | Recommended |
| **Model Customization** | Limited | Yes | Yes | Yes |
| **Best For** | Quick deployment | Regulated industries | Cost control | ML/AI teams |

---

## Integration Process

### Step 1: Choose LLM Provider
- Evaluate requirements (air-gap, sovereignty, cost)
- Review compliance requirements
- Assess infrastructure availability
- Determine budget for subscription/infrastructure

### Step 2: Deploy LLM Infrastructure
**For IBM watsonx SaaS:**
- Sign up for IBM watsonx subscription
- Obtain API credentials
- Configure network access to IBM Cloud

**For RHEL AI:**
- Deploy RHEL AI bootable image
- Install and configure vLLM Server
- Download Granite models
- Configure secure HTTPS endpoint

**For OpenShift AI:**
- Install OpenShift AI operator
- Deploy model serving infrastructure
- Deploy Granite models
- Configure model serving endpoints

### Step 3: Deploy AAP 2.6 on OpenShift
- Install AAP 2.6 operator on OpenShift
- Configure AAP components
- Verify AAP functionality

### Step 4: Configure Ansible Lightspeed
- Create chatbot configuration secret
- Specify LLM provider and endpoint
- Configure authentication (API key)
- Deploy chatbot operator

### Step 5: Verify Integration
- Access AAP 2.6 UI
- Open Ansible Lightspeed chat
- Test queries about Ansible tasks
- Validate code generation responses

---

## Limitations and Considerations

### Current Limitations (AAP 2.6)
- **No third-party LLM support** - Cannot use OpenAI, Anthropic, Google directly
- **OpenShift required** - AAP 2.6 Lightspeed only on OpenShift Container Platform
- **Model selection limited** - Restricted to Red Hat/IBM Granite ecosystem
- **MCP in preview** - Model Context Protocol not production-ready

### Security Considerations
- **Data in transit** - Ensure HTTPS/TLS for LLM communication
- **API key management** - Store credentials in OpenShift secrets
- **Network policies** - Restrict LLM endpoint access
- **Audit logging** - Enable logging for compliance

### Performance Considerations
- **Latency** - Self-hosted may have lower latency than SaaS
- **Concurrent users** - Scale LLM infrastructure accordingly
- **Token limits** - Monitor context window limitations
- **GPU requirements** - Inference speed directly tied to GPU availability

---

## Future Roadmap

### Expected in Future AAP Releases
- **MCP GA (General Availability)** - Production support for Model Context Protocol
- **Broader LLM support** - OpenAI, Anthropic, Google integration via MCP
- **Fine-tuning tools** - Easier custom model training with organizational data
- **Multi-model support** - Use different models for different tasks
- **Enhanced policy controls** - OPA-based guardrails for AI interactions

### Preparing for Future Updates
- **Start with IBM watsonx** - Production-ready today
- **Plan RHEL AI infrastructure** - For data sovereignty requirements
- **Test MCP (preview)** - Gain experience with future architecture
- **Monitor Red Hat announcements** - Updates to supported models

---

## Getting Started Checklist

### Pre-deployment
- [ ] Review organizational AI policy requirements
- [ ] Assess data sovereignty and compliance needs
- [ ] Evaluate air-gap requirements
- [ ] Determine budget (subscription + infrastructure)
- [ ] Choose LLM provider option

### Infrastructure
- [ ] OpenShift Container Platform deployed (if needed)
- [ ] LLM infrastructure deployed (RHEL AI / OpenShift AI)
- [ ] GPU resources available (recommended)
- [ ] Network connectivity verified

### AAP 2.6 Deployment
- [ ] AAP 2.6 operator installed on OpenShift
- [ ] AAP components configured
- [ ] Ansible Lightspeed chatbot operator deployed
- [ ] LLM provider configured in chatbot secret

### Validation
- [ ] Ansible Lightspeed accessible in AAP UI
- [ ] Test queries return accurate responses
- [ ] Code generation functional
- [ ] Audit logging enabled
- [ ] User training completed

---

## Support and Resources

### Official Documentation
- [AAP 2.6 Release Notes](https://docs.redhat.com/documentation/red_hat_ansible_automation_platform/2.6/html/release_notes/new-features)
- [Deploying Ansible Lightspeed](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.6/html/installing_on_openshift_container_platform/deploying-chatbot-operator)
- [RHEL AI Documentation](https://access.redhat.com/products/red-hat-enterprise-linux-ai/)
- [OpenShift AI Documentation](https://docs.redhat.com/en/documentation/red_hat_ai/)

### IBM watsonx Resources
- [IBM watsonx Code Assistant](https://www.ibm.com/architectures/hybrid/genai-code-generation-ansible)
- [Ansible Lightspeed Overview](https://developers.redhat.com/products/ansible/lightspeed)

### Community Resources
- Red Hat Developer Hub - Model Catalog Bridge
- Hugging Face RedHatAI Collections
- Red Hat Ansible Collection: `redhat.ai`

### Getting Help
- **Red Hat Support** - Open support case for AAP issues
- **Red Hat Account Team** - Architectural guidance and planning
- **IBM Support** - For watsonx-specific questions
- **Red Hat Training** - RHEL AI technical deep dives

---

## Summary

**The Bottom Line:**

AAP 2.6 LLM integration is **not plug-and-play with any LLM**. You must use:

1. **IBM watsonx Code Assistant** (SaaS or self-hosted) - Production ready
2. **Red Hat Enterprise Linux AI** (self-hosted with vLLM) - Self-managed
3. **Red Hat OpenShift AI** (managed AI platform) - Enterprise MLOps

**Future:** MCP support (tech preview) will enable broader LLM compatibility, but that's not production-ready in AAP 2.6.

**Recommendation:**
- **Start fast:** IBM watsonx SaaS
- **Data sovereignty:** RHEL AI or OpenShift AI self-hosted
- **Future-proof:** Plan for MCP migration when GA

---

*Document compiled from Red Hat official documentation and web research - October 2025*  
*For latest updates, consult Red Hat documentation or your Red Hat account team*

