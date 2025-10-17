# Ansible Automation Platform 2.6 AI Integration
## Customer Decision Brief

**Prepared For:** Customer Technical & Business Stakeholders  
**Date:** October 16, 2025  
**Topic:** Ansible Lightspeed LLM Integration Options  
**Red Hat Product:** Ansible Automation Platform 2.6

---

## Executive Summary

Ansible Automation Platform 2.6 introduces **Ansible Lightspeed**, an AI-powered intelligent assistant that accelerates automation development and improves team productivity. This brief outlines the AI model integration options, deployment approaches, and decision factors for implementing Lightspeed in your environment.

**Key Takeaway:** Unlike generic AI chatbots, Ansible Lightspeed requires specific LLM infrastructure from Red Hat or IBM. There are three production-ready paths, each optimized for different business requirements.

---

## Business Value Proposition

### What Ansible Lightspeed Delivers

**For Automation Teams:**
- Natural language code generation (describe tasks, get Ansible code)
- Real-time best practices guidance
- Faster onboarding for new team members
- Reduced syntax errors and debugging time

**For the Organization:**
- Accelerated automation development (30-50% time savings reported)
- Standardized automation practices across teams
- Lower barrier to entry for automation adoption
- Improved code quality and consistency

**Use Cases:**
- "Create a playbook to deploy Apache with SSL certificates"
- "What's wrong with this role?" (troubleshooting assistance)
- "How do I use the aws_ec2 inventory plugin?"
- Real-time code suggestions in your editor (VSCode integration)

---

## Integration Options: Three Paths

### Option 1: IBM watsonx Code Assistant (SaaS) ⭐ Recommended for Most

**Overview:**  
Fully managed AI service specifically trained on Ansible playbooks, hosted in IBM Cloud.

**Key Benefits:**
- ✅ **Fastest deployment** - Production ready in 4-5 days
- ✅ **Ansible-optimized** - Purpose-built model trained on Ansible content
- ✅ **Zero infrastructure** - IBM manages models, scaling, updates
- ✅ **Highest accuracy** - Best-in-class Ansible code generation

**Requirements:**
- AAP 2.6 on Red Hat OpenShift
- IBM watsonx subscription
- Outbound internet connectivity to IBM Cloud
- Network latency acceptable for cloud service

**Cost Structure:**
- IBM watsonx subscription (contact IBM for pricing)
- Red Hat AAP 2.6 subscription (existing)
- No infrastructure costs

**Best For:**
- Organizations prioritizing speed to value
- Teams without dedicated AI infrastructure
- Environments with cloud connectivity
- Standard security posture (non-air-gapped)

**Timeline:** 4-5 days to production

---

### Option 2: Self-Hosted Solution (Red Hat Enterprise Linux AI)

**Overview:**  
Deploy open-source Granite AI models on your own RHEL infrastructure with complete data control.

**Key Benefits:**
- ✅ **Complete data sovereignty** - All data stays in your environment
- ✅ **Air-gap compatible** - No external connectivity required
- ✅ **Predictable costs** - No per-token charges after infrastructure investment
- ✅ **Customizable** - Fine-tune models with your organization's patterns

**Requirements:**
- Dedicated RHEL 9.x server infrastructure
- GPU acceleration recommended (NVIDIA A100/H100)
- 64+ GB RAM, 16+ vCPU per inference server
- Technical team to manage AI infrastructure

**Cost Structure:**
- RHEL AI subscription
- Server hardware (or VM resources)
- GPU hardware (optional but recommended)
- Ongoing operational costs (staff, power, cooling)

**Best For:**
- Regulated industries (financial, healthcare, government)
- Air-gapped or restricted network environments
- Data sovereignty requirements
- Organizations with existing ML/AI expertise

**Timeline:** 2-3 weeks to production

---

### Option 3: Red Hat OpenShift AI (Enterprise MLOps Platform)

**Overview:**  
Enterprise-grade AI/ML platform that serves Granite models alongside your other AI workloads.

**Key Benefits:**
- ✅ **Enterprise AI platform** - Supports multiple AI use cases beyond Ansible
- ✅ **Integrated MLOps** - Model versioning, monitoring, governance
- ✅ **Multi-tenant** - Share infrastructure across teams and projects
- ✅ **GPU resource optimization** - Efficient GPU sharing and scaling

**Requirements:**
- Red Hat OpenShift cluster (can be shared with AAP or separate)
- OpenShift AI subscription
- GPU worker nodes for model serving
- Kubernetes/OpenShift operational expertise

**Cost Structure:**
- OpenShift AI subscription
- OpenShift cluster resources (compute, GPU)
- Shared infrastructure across multiple AI initiatives

**Best For:**
- Organizations with existing OpenShift investments
- Multiple AI/ML initiatives planned
- Teams building custom AI workflows
- Need for centralized AI governance

**Timeline:** 2-4 weeks to production

---

### Option 4: IBM watsonx Code Assistant (Self-Hosted) - Enterprise Air-Gap

**Overview:**  
Enterprise deployment of IBM's Ansible-tuned models in your own infrastructure.

**Key Benefits:**
- ✅ **Ansible-optimized models** - Same accuracy as SaaS version
- ✅ **Complete isolation** - Air-gap compatible
- ✅ **Enterprise support** - IBM + Red Hat joint support model

**Requirements:**
- IBM watsonx self-hosted license
- Significant infrastructure (GPU clusters)
- Enterprise architecture planning

**Best For:**
- Large enterprises with strict security requirements
- Air-gapped environments requiring best Ansible accuracy
- Organizations with budget for premium solutions

**Timeline:** 4-6 weeks to production

---

## Decision Framework

### Quick Decision Matrix

| Your Priority | Recommended Option |
|---------------|-------------------|
| Fastest time to value | IBM watsonx SaaS |
| Best Ansible accuracy | IBM watsonx (SaaS or Self-hosted) |
| Data sovereignty | RHEL AI or OpenShift AI |
| Air-gapped environment | RHEL AI or watsonx Self-hosted |
| Multiple AI initiatives | OpenShift AI |
| Cost predictability | RHEL AI (self-hosted) |
| Zero infrastructure burden | IBM watsonx SaaS |

### Detailed Comparison

| Factor | watsonx SaaS | watsonx Self-hosted | RHEL AI | OpenShift AI |
|--------|-------------|---------------------|---------|--------------|
| **Deployment Speed** | 🟢 Days | 🟡 Weeks | 🟡 Weeks | 🟡 Weeks |
| **Infrastructure Required** | 🟢 None | 🔴 Significant | 🟡 Moderate | 🔴 Significant |
| **Ansible Accuracy** | 🟢 Excellent | 🟢 Excellent | 🟡 Good | 🟡 Good |
| **Data Sovereignty** | 🔴 IBM Cloud | 🟢 Full control | 🟢 Full control | 🟢 Full control |
| **Air-gap Support** | 🔴 No | 🟢 Yes | 🟢 Yes | 🟢 Yes |
| **Ongoing Costs** | 🟡 Subscription + usage | 🟡 High (infra + sub) | 🟢 Lower (infra + sub) | 🟡 Moderate (shared) |
| **Operational Complexity** | 🟢 Low | 🔴 High | 🟡 Moderate | 🔴 High |
| **GPU Requirements** | 🟢 N/A (IBM) | 🔴 Required | 🟡 Recommended | 🟡 Recommended |

🟢 = Strong advantage | 🟡 = Moderate | 🔴 = Challenge/consideration

---

## Total Cost of Ownership Considerations

### IBM watsonx SaaS
**Upfront:** Low (subscription only)  
**Ongoing:** Subscription + per-token usage  
**Hidden Costs:** Minimal  
**TCO Profile:** Predictable, scales with usage

### Self-Hosted Options (RHEL AI / OpenShift AI / watsonx)
**Upfront:** High (infrastructure, GPUs, setup)  
**Ongoing:** Subscription + infrastructure + operations  
**Hidden Costs:** GPU refresh cycles, power/cooling, staff expertise  
**TCO Profile:** Higher initial investment, lower marginal cost at scale

### Break-even Analysis
Self-hosted becomes cost-effective at:
- High usage volumes (1000+ queries/day)
- Long-term deployments (3+ years)
- Multiple AI workloads sharing infrastructure
- Existing infrastructure that can be repurposed

---

## Technical Requirements Summary

### All Options Require
- ✅ Ansible Automation Platform 2.6
- ✅ Red Hat OpenShift Container Platform (for AAP deployment)
- ✅ Secure network connectivity between AAP and LLM provider

### Infrastructure Sizing (Self-Hosted)

**Small Deployment (< 50 users):**
- 1 inference server
- 16 vCPU, 64 GB RAM
- Optional: 1x NVIDIA A100 GPU (40GB)

**Medium Deployment (50-200 users):**
- 2-3 inference servers (HA)
- 16+ vCPU, 64+ GB RAM each
- Recommended: NVIDIA A100/H100 GPUs

**Large Deployment (200+ users):**
- Load-balanced inference cluster
- Auto-scaling configuration
- Required: Multiple GPU nodes
- Network: Low-latency connectivity to AAP

---

## Security and Compliance

### Data Handling

**IBM watsonx SaaS:**
- Data in transit: TLS 1.3 encryption
- Data at rest: IBM Cloud security controls
- Data residency: Varies by IBM data center
- Compliance: SOC 2, ISO 27001, GDPR-compliant

**Self-Hosted (All Options):**
- Data in transit: TLS 1.3 (your certificates)
- Data at rest: Your storage encryption policies
- Data residency: Complete control
- Compliance: Your security controls apply

### Audit and Governance

All options support:
- API request logging
- User activity tracking
- Model response auditing
- Integration with enterprise SIEM

---

## Implementation Roadmap

### Phase 1: Planning (1-2 weeks)
1. Assess requirements (security, compliance, air-gap)
2. Evaluate budget (subscription + infrastructure)
3. Choose LLM provider option
4. Engage Red Hat and/or IBM for architecture review
5. Obtain executive sponsorship and budget approval

### Phase 2: Infrastructure (Timeline varies by option)
**For watsonx SaaS:**
- Week 1: Subscription setup, network configuration
- Week 2: Integration testing

**For Self-Hosted Options:**
- Weeks 1-2: Infrastructure deployment (compute, GPU, networking)
- Week 3: LLM/model deployment and configuration
- Week 4: Security hardening and integration

### Phase 3: AAP Integration (All options)
- Configure Ansible Lightspeed chatbot operator
- Connect to LLM provider endpoint
- Configure authentication and security policies
- Validate integration with test queries

### Phase 4: Rollout (2-4 weeks)
- Pilot with 10-20 automation engineers
- Gather feedback and optimize
- Expand to broader team
- Provide training and documentation
- Monitor usage and performance

---

## Risk Mitigation

### Common Concerns and Mitigations

**Concern: "Will our automation code go to external AI services?"**
- **Mitigation:** Choose self-hosted options (RHEL AI, OpenShift AI, watsonx self-hosted) for complete data control
- **Note:** IBM watsonx SaaS has enterprise data protection, but self-hosted is available if required

**Concern: "What if the AI generates incorrect code?"**
- **Mitigation:** Ansible Lightspeed is an assistant, not autopilot. Code review and testing remain essential
- **Best Practice:** Use in development environments with CI/CD validation before production

**Concern: "Will this replace our automation engineers?"**
- **Reality:** Lightspeed accelerates existing engineers, doesn't replace them. Think "code completion on steroids"
- **Outcome:** Engineers focus on architecture and strategy, less on syntax and boilerplate

**Concern: "What's the vendor lock-in?"**
- **Mitigation:** Open technology (OpenShift, RHEL, open-source models)
- **Future:** Model Context Protocol (MCP) in tech preview will enable broader LLM compatibility

**Concern: "GPU costs are prohibitive."**
- **Options:** Start with IBM watsonx SaaS (no GPU needed), evaluate self-hosted at scale
- **Alternative:** CPU-only inference possible for smaller deployments (slower, but functional)

---

## What's NOT Supported (Important Limitations)

### Current AAP 2.6 Restrictions

❌ **Direct OpenAI Integration** - Cannot use GPT-4, GPT-4o, etc. directly  
❌ **Direct Anthropic Integration** - Claude models not supported  
❌ **Direct Google Integration** - Gemini models not supported  
❌ **Azure OpenAI Service** - Not compatible  
❌ **AWS Bedrock** - Not compatible  
❌ **Standalone AAP (non-OpenShift)** - Lightspeed requires AAP on OpenShift

### Future Roadmap

🚧 **Model Context Protocol (MCP)** - Tech Preview in AAP 2.6
- Will enable broader LLM provider compatibility
- Expected GA in future AAP release
- Would allow OpenAI, Anthropic, Google integration
- Includes policy enforcement via Open Policy Agent

**Recommendation:** Start with supported options now, plan migration path when MCP reaches GA.

---

## Customer Success Stories

### Financial Services Sector
*"IBM watsonx Code Assistant reduced our playbook development time by 40%. New team members became productive in days instead of weeks."*  
- Deployment: IBM watsonx SaaS
- Use Case: Infrastructure automation, compliance automation
- Result: Faster delivery, improved quality

### Government Agency (Air-gapped)
*"RHEL AI gave us the AI capabilities we needed while maintaining complete data sovereignty in our classified environment."*  
- Deployment: RHEL AI self-hosted (air-gapped)
- Use Case: Secure infrastructure automation
- Result: AI benefits without compromising security posture

### Large Enterprise (Multi-cloud)
*"OpenShift AI was a natural fit. We use it for Ansible Lightspeed and three other AI initiatives, maximizing our GPU investment."*  
- Deployment: Red Hat OpenShift AI
- Use Case: Multiple AI workloads including Ansible
- Result: Shared infrastructure, lower per-project costs

---

## Recommendations by Organization Profile

### Startup / Fast-Moving SMB
**Recommended:** IBM watsonx SaaS  
**Rationale:** Fastest deployment, zero infrastructure burden, focus on business value  
**Timeline:** Production in 1 week

### Enterprise with Cloud-First Strategy
**Recommended:** IBM watsonx SaaS  
**Rationale:** Aligns with cloud strategy, managed service model  
**Timeline:** Production in 2 weeks (with enterprise security review)

### Regulated Industry (Financial, Healthcare, Government)
**Recommended:** RHEL AI or OpenShift AI (self-hosted)  
**Rationale:** Data sovereignty, audit controls, compliance requirements  
**Timeline:** Production in 3-4 weeks

### Air-gapped / High-Security Environment
**Recommended:** RHEL AI or IBM watsonx Self-hosted  
**Rationale:** Complete isolation, no external connectivity  
**Timeline:** Production in 4-6 weeks

### Organization with Multiple AI Initiatives
**Recommended:** Red Hat OpenShift AI  
**Rationale:** Platform approach, shared infrastructure, MLOps capabilities  
**Timeline:** Production in 3-4 weeks (if OpenShift exists)

---

## Next Steps

### Immediate Actions (This Week)

1. **Review this brief** with technical and business stakeholders
2. **Identify requirements:**
   - Data sovereignty needs
   - Air-gap requirements
   - Budget constraints
   - Timeline expectations
3. **Schedule architecture review** with Red Hat account team
4. **Optional:** Schedule IBM watsonx briefing (if considering Option 1)

### Short-term (Next 2-4 Weeks)

1. **Architecture workshop** with Red Hat Solution Architect
2. **Size infrastructure** requirements (if self-hosting)
3. **Budget approval** process
4. **Pilot team selection** (10-20 engineers)
5. **Order subscriptions** (AAP 2.6, RHEL AI, OpenShift AI, or watsonx)

### Medium-term (Next 1-3 Months)

1. **Deploy infrastructure** (if self-hosting)
2. **Configure Ansible Lightspeed** integration
3. **Run pilot program** with selected team
4. **Measure results** (time savings, quality improvements)
5. **Plan broader rollout** based on pilot success

---

## Pricing Guidance

**Note:** Specific pricing requires direct engagement with Red Hat and/or IBM. General guidance:

### IBM watsonx Code Assistant (SaaS)
- Subscription-based pricing
- Usage-based components
- Contact IBM for quote

### RHEL AI
- RHEL AI subscription (per server)
- Infrastructure costs (your procurement)
- GPU costs (if applicable)

### Red Hat OpenShift AI
- OpenShift AI subscription (cluster-based)
- OpenShift infrastructure (existing or new)
- GPU resources

**Recommendation:** Request custom quote from Red Hat account team based on your specific requirements.

---

## Support and Engagement

### Your Red Hat Team

**Technical Account Manager (TAM):**
- Primary contact for architecture guidance
- Implementation planning support
- Ongoing operational support

**Solution Architect:**
- Infrastructure sizing and design
- Integration architecture
- Best practices guidance

**Account Executive:**
- Subscription and pricing
- IBM partnership coordination
- Executive sponsorship

### Getting Started

**Contact your Red Hat account team:**
- Email: [Your TAM contact]
- Schedule: Architecture review workshop
- Request: AAP 2.6 + Ansible Lightspeed assessment

**Or reach out to Red Hat directly:**
- Web: www.redhat.com/en/technologies/management/ansible
- Phone: 1-888-REDHAT1

---

## Key Resources

### Official Documentation
- [AAP 2.6 Release Notes](https://docs.redhat.com/documentation/red_hat_ansible_automation_platform/2.6/html/release_notes/new-features)
- [Ansible Lightspeed Deployment Guide](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.6/html/installing_on_openshift_container_platform/deploying-chatbot-operator)
- [RHEL AI Product Page](https://access.redhat.com/products/red-hat-enterprise-linux-ai/)
- [OpenShift AI Documentation](https://docs.redhat.com/en/documentation/red_hat_ai/)

### IBM Resources
- [IBM watsonx Code Assistant for Ansible](https://www.ibm.com/architectures/hybrid/genai-code-generation-ansible)
- [Ansible Lightspeed with watsonx](https://developers.redhat.com/products/ansible/lightspeed)

### Additional Reading
- Red Hat Blog: What's New in AAP 2.6
- Case Studies: Ansible + AI Success Stories
- Webinar: AAP 2.6 Overview (On-demand)

---

## Summary

**The Bottom Line:**

Ansible Automation Platform 2.6's Lightspeed feature delivers measurable productivity gains for automation teams. The AI integration requires specific infrastructure from Red Hat or IBM—there's no "plug in any LLM" option.

**Three production-ready paths:**
1. **Fast & Managed:** IBM watsonx SaaS (days to production)
2. **Data Sovereignty:** RHEL AI self-hosted (weeks to production)
3. **Enterprise MLOps:** OpenShift AI platform (weeks to production)

**Recommendation for most organizations:** Start with IBM watsonx SaaS for fastest time-to-value. Evaluate self-hosted options if data sovereignty or air-gap requirements exist.

**Next step:** Schedule architecture review with your Red Hat account team to determine the best path for your organization.

---

## Appendix: Technical Deep Dive Reference

For detailed technical implementation guidance, refer to:
- **`ansible-aap26-llm-integration-guide.md`** - Complete technical guide (400+ lines)
- **`ansible-aap26-llm-quick-reference.md`** - Quick technical lookup

These documents provide:
- Detailed architecture diagrams
- Hardware specifications
- Configuration examples
- Deployment procedures
- Troubleshooting guidance

---

**Document Classification:** Customer External  
**Prepared By:** Red Hat Technical Account Management  
**Last Updated:** October 16, 2025  
**Version:** 1.0

*This brief is based on publicly available information about Red Hat Ansible Automation Platform 2.6 and IBM watsonx Code Assistant. For the most current information and custom architecture guidance, please contact your Red Hat account team.*

