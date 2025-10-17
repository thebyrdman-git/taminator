# AAP 2.6 LLM Integration - Quick Reference

**Last Updated:** October 16, 2025

---

## TL;DR - What LLMs Work with AAP 2.6?

### ✅ Supported (Production Ready)

| Option | Deployment | Setup Time | Best For |
|--------|-----------|------------|----------|
| **IBM watsonx Code Assistant** (SaaS) | IBM Cloud | Days | Fast deployment, Ansible-optimized |
| **IBM watsonx Code Assistant** (Self-hosted) | Your infrastructure | Weeks | Air-gapped, regulated industries |
| **RHEL AI + vLLM + Granite** | Self-hosted RHEL | Weeks | Cost control, data sovereignty |
| **OpenShift AI + Granite** | OpenShift cluster | Weeks | MLOps teams, enterprise AI platform |

### 🚧 Coming Soon (Tech Preview)

| Option | Status | Timeline |
|--------|--------|----------|
| **Model Context Protocol (MCP)** | Tech Preview in AAP 2.6 | Future GA release |
| OpenAI, Anthropic, Google via MCP | Not available yet | When MCP goes GA |

### ❌ NOT Supported

- Direct OpenAI API integration
- Direct Anthropic Claude API integration  
- Direct Google Gemini API integration
- Azure OpenAI Service
- AWS Bedrock
- Any other third-party LLM service

---

## Architecture at a Glance

```
┌──────────────────────────────────────┐
│ Ansible Automation Platform 2.6      │
│ (must be on OpenShift)               │
│                                       │
│  ┌─────────────────────────────┐    │
│  │ Ansible Lightspeed          │    │
│  │ Intelligent Assistant       │    │
│  └──────────┬──────────────────┘    │
└─────────────┼───────────────────────┘
              │ HTTPS API
              ▼
┌──────────────────────────────────────┐
│ LLM Provider (Pick ONE)              │
├──────────────────────────────────────┤
│ • IBM watsonx (Ansible-tuned)        │
│ • RHEL AI (vLLM + Granite models)    │
│ • OpenShift AI (Model serving)       │
└──────────────────────────────────────┘
```

---

## Decision Tree

```
Do you need Ansible-specific code generation?
│
├─ YES → IBM watsonx Code Assistant
│         ├─ Need air-gap? → Self-hosted
│         └─ Fast deployment? → SaaS
│
└─ NO (just Ansible Q&A) → Self-hosted options
          ├─ Have OpenShift cluster? → OpenShift AI
          └─ Standalone server? → RHEL AI
```

---

## Requirements Checklist

### All Options Require
- ✅ Ansible Automation Platform 2.6
- ✅ Red Hat OpenShift Container Platform (for AAP)
- ✅ Network connectivity between AAP and LLM provider

### IBM watsonx (SaaS)
- ✅ IBM watsonx subscription
- ✅ Internet connectivity to IBM Cloud
- ✅ API credentials

### IBM watsonx (Self-hosted)
- ✅ IBM watsonx license (self-hosted)
- ✅ Dedicated infrastructure
- ✅ GPU recommended (NVIDIA A100/H100)

### RHEL AI
- ✅ RHEL 9.x server (dedicated)
- ✅ 16+ vCPU, 64+ GB RAM
- ✅ GPU recommended (16+ GB VRAM)
- ✅ vLLM Server installation
- ✅ Granite models downloaded
- ✅ HTTPS endpoint configured

### OpenShift AI
- ✅ OpenShift cluster (can be same as AAP or separate)
- ✅ OpenShift AI subscription
- ✅ GPU worker nodes recommended
- ✅ Model serving infrastructure

---

## Quick Model Reference

### Granite Models Available

| Model | Size | Context | Use Case |
|-------|------|---------|----------|
| Granite (Ansible-tuned)* | Unknown | Unknown | Ansible code gen (watsonx only) |
| Granite 3.2 8B Instruct | 8B | 4K | General purpose (latest) |
| Granite 3.1 8B Instruct | 8B | 4K | General purpose |
| Granite 8B Code Instruct | 8B | 4K | Code-focused |

*Proprietary IBM watsonx model - specs not public

---

## Configuration Example

### Chatbot Operator Secret (RHEL AI)

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
      provider: "rhel-ai"
      endpoint: "https://rhel-ai-server.example.com:8000/v1"
      api_key: "your-vllm-api-key"
      model: "granite-3.2-8b-instruct"
```

### Chatbot Operator Secret (OpenShift AI)

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
      provider: "openshift-ai"
      endpoint: "https://model-serving.apps.ocp.example.com/v1"
      api_key: "your-model-serving-token"
      model: "granite-3.2-8b-instruct"
```

---

## Deployment Time Estimates

| Option | Setup | Configuration | Testing | Total |
|--------|-------|---------------|---------|-------|
| **IBM watsonx SaaS** | 1 day | 2 days | 1 day | ~4 days |
| **IBM watsonx Self-hosted** | 1-2 weeks | 3-5 days | 2-3 days | ~3 weeks |
| **RHEL AI** | 1 week | 3-5 days | 2-3 days | ~2 weeks |
| **OpenShift AI** | 1-2 weeks | 3-5 days | 2-3 days | ~3 weeks |

---

## Common Questions

### Q: Can I use OpenAI GPT-4 with AAP 2.6?
**A:** Not directly. MCP support (tech preview) may enable this in future releases.

### Q: What's the cheapest option?
**A:** RHEL AI self-hosted - no per-token costs after infrastructure investment.

### Q: What's the fastest deployment?
**A:** IBM watsonx SaaS - managed service, ~4 days to production.

### Q: Do I need GPUs?
**A:** Recommended for production performance, but not strictly required for small-scale deployments.

### Q: Can I use this in an air-gapped environment?
**A:** Yes - IBM watsonx (self-hosted), RHEL AI, or OpenShift AI all support air-gapped.

### Q: What happened to using any LLM?
**A:** AAP 2.6 currently requires Red Hat/IBM AI platforms. MCP (tech preview) will expand options in future.

### Q: Is this just for code generation?
**A:** No - Ansible Lightspeed provides:
  - Code generation
  - Natural language Q&A about Ansible
  - Troubleshooting guidance
  - Best practices recommendations

---

## Next Steps

1. **Evaluate requirements** - Air-gap? Data sovereignty? Budget?
2. **Choose LLM provider** - See decision tree above
3. **Review documentation** - See `ansible-aap26-llm-integration-guide.md`
4. **Engage Red Hat** - Contact account team for architecture review
5. **Plan infrastructure** - GPU resources, network, storage
6. **Deploy and test** - Start with non-production environment

---

## Key Resources

- **Full Guide:** `ansible-aap26-llm-integration-guide.md` (this directory)
- **Red Hat Docs:** [docs.redhat.com/red_hat_ansible_automation_platform/2.6](https://docs.redhat.com/documentation/red_hat_ansible_automation_platform/2.6/html/installing_on_openshift_container_platform/deploying-chatbot-operator)
- **IBM watsonx:** [www.ibm.com/architectures/hybrid/genai-code-generation-ansible](https://www.ibm.com/architectures/hybrid/genai-code-generation-ansible)
- **RHEL AI:** [access.redhat.com/products/red-hat-enterprise-linux-ai](https://access.redhat.com/products/red-hat-enterprise-linux-ai/)

---

**Remember:** No direct third-party LLM support in AAP 2.6 - you must use Red Hat/IBM AI platforms.

*Quick Reference - October 2025*

