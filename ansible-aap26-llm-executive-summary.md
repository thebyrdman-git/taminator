# Ansible Automation Platform 2.6 AI Integration
## Executive Summary - One-Page Brief

**Date:** October 16, 2025  
**For:** Executive Leadership & Decision Makers

---

## What's New: Ansible Lightspeed AI Assistant

Ansible Automation Platform 2.6 introduces **Ansible Lightspeed**, an AI-powered assistant that accelerates automation development through natural language code generation and intelligent guidance.

**Business Impact:**
- 30-50% reduction in automation development time
- Faster onboarding for new team members (weeks → days)
- Improved code quality and consistency
- Lower barrier to automation adoption across teams

---

## The Decision: Three Deployment Options

### Option 1: IBM watsonx SaaS (Managed Cloud) 
**Timeline:** 4-5 days | **Best For:** Speed & simplicity

**Pros:** Fastest deployment, zero infrastructure, Ansible-optimized, IBM-managed  
**Cons:** Requires cloud connectivity, data processed in IBM Cloud  
**Cost Model:** Subscription + usage-based pricing

---

### Option 2: Self-Hosted (RHEL AI or OpenShift AI)
**Timeline:** 2-4 weeks | **Best For:** Data sovereignty & compliance

**Pros:** Complete data control, air-gap capable, predictable costs  
**Cons:** Infrastructure investment required, operational complexity  
**Cost Model:** Subscription + infrastructure (hardware/GPU)

---

### Option 3: IBM watsonx Self-Hosted (Enterprise)
**Timeline:** 4-6 weeks | **Best For:** Air-gap + best accuracy

**Pros:** Ansible-optimized + complete isolation  
**Cons:** Highest infrastructure requirements and costs  
**Cost Model:** Enterprise subscription + significant infrastructure

---

## Key Constraints

⚠️ **Important:** AAP 2.6 Lightspeed does NOT support:
- OpenAI (GPT-4, ChatGPT)
- Anthropic (Claude)
- Google (Gemini)
- Other third-party LLM services

✅ **Must use:** Red Hat or IBM AI infrastructure

🚧 **Future:** Model Context Protocol (tech preview) will enable broader LLM support in future releases

---

## Decision Framework

| Your Priority | Choose This |
|--------------|-------------|
| **Fastest time to value** | IBM watsonx SaaS |
| **Data sovereignty required** | RHEL AI or OpenShift AI |
| **Air-gapped environment** | RHEL AI or watsonx Self-hosted |
| **Best Ansible accuracy** | IBM watsonx (SaaS or Self-hosted) |
| **Lowest ongoing cost** | RHEL AI (self-hosted) |
| **Multiple AI initiatives** | OpenShift AI platform |

---

## Investment Overview

### IBM watsonx SaaS
- **Upfront:** Low (subscription only)
- **Ongoing:** Moderate (subscription + usage)
- **Infrastructure:** None required
- **TCO Sweet Spot:** Low-to-medium usage, fast deployment needs

### Self-Hosted (RHEL AI / OpenShift AI)
- **Upfront:** High (infrastructure + GPU + setup)
- **Ongoing:** Moderate (subscription + operations)
- **Infrastructure:** Significant (servers, GPU, networking)
- **TCO Sweet Spot:** High usage, long-term (3+ years), compliance requirements

---

## Requirements (All Options)

**Mandatory:**
- Ansible Automation Platform 2.6 subscription
- Red Hat OpenShift Container Platform (for AAP)
- Network connectivity between AAP and LLM provider

**Self-Hosted Additional:**
- Dedicated server infrastructure (64+ GB RAM, 16+ vCPU)
- GPU acceleration recommended (NVIDIA A100/H100)
- AI/ML operational expertise

---

## Risk Considerations

✅ **Low Risk:**
- Proven technology (Red Hat + IBM partnership)
- Production-ready in AAP 2.6
- Enterprise support from Red Hat and IBM
- Pilot program approach recommended

⚠️ **Moderate Risk:**
- Self-hosted requires infrastructure investment before ROI
- Team adoption requires change management
- AI-generated code still requires review and testing

❌ **Not a Risk:**
- Job replacement: AI accelerates engineers, doesn't replace them
- Vendor lock-in: Open technologies, MCP future-proofs approach

---

## Success Metrics

**Measure These:**
- Time to develop new automation (hours/playbook)
- New team member productivity ramp time
- Automation code quality (error rates, best practices compliance)
- Team adoption rate and satisfaction
- Automation backlog reduction

**Expected Outcomes:**
- 30-50% faster automation development
- 60% reduction in onboarding time
- Improved code consistency and quality
- Increased automation adoption across organization

---

## Recommended Next Steps

### Week 1: Assessment
- [ ] Review this brief with IT leadership
- [ ] Identify security/compliance requirements (air-gap, data sovereignty)
- [ ] Determine budget parameters
- [ ] Assign executive sponsor

### Week 2-3: Planning
- [ ] Architecture review with Red Hat Solution Architect
- [ ] Evaluate deployment options against requirements
- [ ] Size infrastructure (if self-hosting)
- [ ] Obtain pricing quotes (Red Hat + IBM if applicable)

### Week 4-6: Decision & Procurement
- [ ] Present recommendation to leadership
- [ ] Obtain budget approval
- [ ] Order subscriptions (AAP 2.6 + LLM provider)
- [ ] Assign pilot team (10-20 engineers)

### Month 2-3: Implementation
- [ ] Deploy infrastructure (if self-hosting)
- [ ] Configure Ansible Lightspeed
- [ ] Run pilot program
- [ ] Measure results and optimize

### Month 4+: Rollout
- [ ] Expand to broader organization
- [ ] Track ROI metrics
- [ ] Optimize based on usage patterns
- [ ] Plan additional automation initiatives

---

## The Ask

**From Leadership:**
1. Executive sponsorship for AI-enabled automation initiative
2. Budget approval for subscription and infrastructure (if self-hosted)
3. Support for pilot program and team training

**From IT:**
1. Infrastructure planning and deployment (if self-hosted)
2. Security and compliance review
3. Integration with existing AAP deployment

**From Teams:**
1. Pilot participation (10-20 automation engineers)
2. Feedback and adoption metrics
3. Knowledge sharing and best practices

---

## Contact & Next Steps

**To proceed, contact your Red Hat account team:**

**Primary Contact:** [Your Technical Account Manager]  
**Email:** [TAM email]  
**Phone:** [TAM phone]

**Request:**
- Architecture review workshop
- AAP 2.6 + Ansible Lightspeed assessment
- Custom pricing quote
- Reference customer introductions

**Or email:** [Account Executive contact]

---

## Supporting Documentation

Detailed technical and business documentation available:

1. **`ansible-aap26-llm-customer-brief.md`** - Complete customer decision brief (15 pages)
2. **`ansible-aap26-llm-integration-guide.md`** - Technical implementation guide (20+ pages)
3. **`ansible-aap26-llm-quick-reference.md`** - Quick technical reference (5 pages)

**Red Hat Resources:**
- Official AAP 2.6 documentation: docs.redhat.com
- What's New webinar (on-demand)
- Customer success stories

---

## Bottom Line

**Ansible Lightspeed delivers measurable productivity gains for automation teams.**

✅ **Three production-ready deployment options** (SaaS, RHEL AI, OpenShift AI)  
✅ **Proven ROI:** 30-50% faster automation development  
✅ **Enterprise-grade:** Full Red Hat + IBM support  

⚠️ **Requires:** Red Hat/IBM AI infrastructure (no third-party LLM support yet)  
⚠️ **Investment:** Subscription required, infrastructure optional (SaaS vs. self-hosted)  

🎯 **Recommendation:** Start with IBM watsonx SaaS for fastest value, evaluate self-hosted if data sovereignty required.

**Next step:** Schedule architecture review with Red Hat account team this week.

---

**Prepared by:** Red Hat Technical Account Management  
**Classification:** Customer External  
**Version:** 1.0 - October 2025

