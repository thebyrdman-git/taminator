# Ansible Lightspeed AI Integration
## Presentation Deck Outline

**Target Audience:** Customer Technical & Business Stakeholders  
**Duration:** 45-60 minutes (with Q&A)  
**Format:** Architecture workshop or executive briefing

---

## Slide 1: Title Slide

**Title:** Ansible Automation Platform 2.6  
**Subtitle:** AI-Powered Automation with Ansible Lightspeed

**Presented by:**
- [Your Name], Technical Account Manager, Red Hat
- [Solution Architect Name], Solution Architect, Red Hat

**Date:** [Presentation Date]  
**Customer:** [Customer Name]

**Footer:** Red Hat Confidential - Customer Use Only

---

## Slide 2: Agenda

**Today's Discussion:**

1. Business Challenge & Opportunity (5 min)
2. Ansible Lightspeed Overview (10 min)
3. LLM Integration Architecture (15 min)
4. Deployment Options & Decision Framework (10 min)
5. Implementation Roadmap (5 min)
6. Q&A and Next Steps (15 min)

**Our Goal Today:**
Determine the best Ansible Lightspeed deployment approach for [Customer Organization] and agree on next steps.

---

## Slide 3: The Business Challenge

**What We're Hearing from Automation Teams:**

❌ **Slow Development Cycles**
- "Writing playbooks from scratch takes too long"
- "Onboarding new team members takes weeks"

❌ **Inconsistent Quality**
- "Every engineer codes differently"
- "Best practices aren't consistently applied"

❌ **Knowledge Silos**
- "Expertise locked in a few senior engineers"
- "Documentation is always out of date"

❌ **Growing Backlog**
- "We can't keep up with automation requests"
- "Manual processes still everywhere"

**Does this resonate with your team?**

---

## Slide 4: The Opportunity

**What if your automation engineers had an AI assistant that:**

✅ Generates Ansible code from natural language descriptions  
✅ Provides real-time best practices guidance  
✅ Answers questions about Ansible syntax and modules  
✅ Helps troubleshoot playbook issues instantly  
✅ Learns your organization's coding patterns  

**This is Ansible Lightspeed in AAP 2.6**

---

## Slide 5: Ansible Lightspeed - What It Is

**An AI-Powered Intelligent Assistant for Ansible**

**Three Key Capabilities:**

1. **Code Generation**
   - Natural language → Ansible playbooks
   - "Deploy nginx with SSL" → Complete playbook with best practices

2. **Intelligent Q&A**
   - Ask questions about Ansible concepts
   - Get troubleshooting guidance
   - Understand module parameters and options

3. **Real-time Assistance**
   - VS Code integration for code completion
   - Context-aware suggestions while you code
   - Best practices enforcement

**Built into AAP 2.6 - not a separate tool**

---

## Slide 6: Demo / Use Case Examples

**Example 1: Code Generation**

**User:** "Create a playbook that deploys Apache web server with custom configuration, enables HTTPS, configures firewall rules, and sets up log rotation"

**Lightspeed:** [Shows generated playbook with proper structure, variables, handlers, best practices]

---

**Example 2: Troubleshooting**

**User:** "Why does my playbook run tasks every time even though nothing changed?"

**Lightspeed:** [Explains idempotency, identifies non-idempotent tasks, suggests fixes]

---

**Example 3: Learning**

**User:** "How do I use the aws_ec2 inventory plugin for dynamic inventory?"

**Lightspeed:** [Provides configuration example, explains parameters, suggests best practices]

---

## Slide 7: Early Adopter Results

**Measured Business Impact:**

📊 **30-50% Faster Development**
- Playbook creation time cut in half
- Less time debugging syntax errors

📊 **60% Reduction in Onboarding Time**
- New engineers productive in days, not weeks
- AI provides instant mentorship

📊 **Improved Code Quality**
- Consistent best practices application
- Reduced security vulnerabilities

📊 **Increased Adoption**
- Lower barrier to entry for automation
- More teams using Ansible effectively

**Source:** Early adopter customer reports (financial services, government, enterprise)

---

## Slide 8: Architecture Overview

**How It Works:**

```
┌─────────────────────────────────┐
│ Automation Engineer             │
│                                  │
│  • AAP Web UI (chat interface) │
│  • VS Code + Ansible extension │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ Ansible Automation Platform 2.6 │
│ (on Red Hat OpenShift)          │
│                                  │
│  ┌─────────────────────────┐   │
│  │ Ansible Lightspeed      │   │
│  │ Intelligent Assistant   │   │
│  └──────────┬──────────────┘   │
└─────────────┼──────────────────┘
              │ Secure API
              │ (HTTPS/TLS)
              ▼
┌─────────────────────────────────┐
│ LLM Provider                     │
│ (Choose deployment model)        │
│                                  │
│  • IBM watsonx Code Assistant   │
│  • Red Hat Enterprise Linux AI  │
│  • Red Hat OpenShift AI         │
└─────────────────────────────────┘
```

**Key Point:** Requires specific LLM infrastructure from Red Hat or IBM

---

## Slide 9: LLM Integration - Important Constraints

**What's Supported in AAP 2.6:**

✅ IBM watsonx Code Assistant (SaaS or Self-hosted)  
✅ Red Hat Enterprise Linux AI (Self-hosted)  
✅ Red Hat OpenShift AI (Platform)  

**What's NOT Supported:**

❌ OpenAI (GPT-4, ChatGPT, etc.)  
❌ Anthropic Claude  
❌ Google Gemini  
❌ Azure OpenAI Service  
❌ AWS Bedrock  
❌ Any other third-party LLM  

**Future:** Model Context Protocol (MCP) support is in tech preview - will enable broader LLM compatibility in future AAP releases.

**Why this matters:** Architecture and procurement planning must account for specific Red Hat/IBM infrastructure

---

## Slide 10: Deployment Option 1 - IBM watsonx SaaS

**Fully Managed Cloud Service**

**Architecture:**
- IBM Cloud-hosted LLM service
- Ansible-specific Granite models
- Managed by IBM (no infrastructure for you)

**Pros:**
- ⚡ **Fastest deployment:** 4-5 days to production
- 🎯 **Best Ansible accuracy:** Purpose-trained for Ansible
- 🔧 **Zero infrastructure:** IBM manages everything
- 📈 **Auto-scaling:** Handles usage spikes automatically

**Cons:**
- ☁️ **Requires cloud connectivity:** Not for air-gapped
- 🌐 **Data leaves premises:** Processed in IBM Cloud
- 💰 **Usage-based costs:** Variable monthly billing

**Best For:**
- Fast time to value
- Cloud-first strategies
- Standard security postures
- Organizations without AI infrastructure expertise

**Investment:** Subscription + usage fees | **Timeline:** 4-5 days

---

## Slide 11: Deployment Option 2 - RHEL AI (Self-Hosted)

**Self-Hosted Open-Source AI Platform**

**Architecture:**
- Dedicated RHEL 9.x server(s) in your data center
- Open-source Granite models via vLLM inference
- Complete data control

**Pros:**
- 🔒 **Complete data sovereignty:** Nothing leaves your network
- 🚫 **Air-gap compatible:** No internet required
- 💰 **Predictable costs:** No per-token charges
- 🎨 **Customizable:** Fine-tune models with InstructLab

**Cons:**
- 🏗️ **Infrastructure required:** Servers + GPU recommended
- ⚙️ **Operational complexity:** You manage and maintain
- 🕒 **Longer deployment:** 2-3 weeks to production
- 🤹 **Requires expertise:** AI/ML operations knowledge

**Best For:**
- Data sovereignty requirements
- Air-gapped environments
- Regulated industries (finance, healthcare, government)
- Long-term deployments with high usage

**Investment:** RHEL AI subscription + infrastructure | **Timeline:** 2-3 weeks

---

## Slide 12: Deployment Option 3 - OpenShift AI Platform

**Enterprise MLOps Platform**

**Architecture:**
- OpenShift cluster with AI/ML capabilities
- Model serving infrastructure (KServe + vLLM)
- Granite models deployed as services

**Pros:**
- 🏢 **Enterprise platform:** Supports multiple AI initiatives
- 📊 **MLOps built-in:** Model versioning, monitoring, governance
- 🔄 **Multi-tenant:** Share infrastructure across teams
- 🎯 **GPU optimization:** Efficient resource utilization

**Cons:**
- 🏗️ **Significant infrastructure:** Full OpenShift cluster required
- 💰 **Higher initial cost:** Platform + GPU nodes
- 🕒 **Longer deployment:** 2-4 weeks if cluster doesn't exist
- 🤹 **Complex operations:** OpenShift + AI expertise needed

**Best For:**
- Organizations with multiple AI initiatives
- Existing OpenShift investments
- Need for centralized AI governance
- Teams building custom ML models

**Investment:** OpenShift AI subscription + cluster infrastructure | **Timeline:** 2-4 weeks

---

## Slide 13: Deployment Decision Matrix

**Choosing the Right Option:**

| **Factor** | **watsonx SaaS** | **RHEL AI** | **OpenShift AI** |
|-----------|---------------|-----------|---------------|
| **Speed to Production** | 🟢 Days | 🟡 Weeks | 🟡 Weeks |
| **Infrastructure Needed** | 🟢 None | 🟡 Moderate | 🔴 Significant |
| **Ansible Accuracy** | 🟢 Best | 🟡 Good | 🟡 Good |
| **Data Sovereignty** | 🔴 IBM Cloud | 🟢 Complete | 🟢 Complete |
| **Air-gap Support** | 🔴 No | 🟢 Yes | 🟢 Yes |
| **Operational Complexity** | 🟢 Low | 🟡 Moderate | 🔴 High |
| **Cost Predictability** | 🟡 Variable | 🟢 Fixed | 🟡 Fixed |

🟢 = Strong | 🟡 = Moderate | 🔴 = Consideration

---

## Slide 14: [Customer Name] - Recommended Approach

**Based on our understanding of [Customer Organization]:**

**Your Requirements:**
- [Requirement 1: e.g., Air-gapped environment]
- [Requirement 2: e.g., Data sovereignty for compliance]
- [Requirement 3: e.g., Existing OpenShift deployment]
- [Requirement 4: e.g., Timeline: Production in 60 days]

**Our Recommendation:** **[Option Name]**

**Why this fits:**
✅ [Reason 1 aligned to their requirement]  
✅ [Reason 2 aligned to their requirement]  
✅ [Reason 3 aligned to their requirement]  

**Trade-offs to consider:**
⚠️ [Trade-off 1]  
⚠️ [Trade-off 2]  

**Alternative consideration:** [Brief mention of alternate if close call]

---

## Slide 15: Infrastructure Requirements (Self-Hosted)

**If Choosing RHEL AI or OpenShift AI:**

**Compute Requirements (Minimum):**
- 16 vCPU per inference server
- 64 GB RAM per inference server
- 500 GB storage for models and data
- RHEL 9.x or OpenShift 4.14+

**GPU Acceleration (Highly Recommended):**
- NVIDIA A100 (40GB) or H100 (80GB)
- 1-2 GPUs for small deployment (< 50 users)
- 3-4+ GPUs for medium deployment (50-200 users)
- GPU cluster for large deployment (200+ users)

**Network:**
- Low-latency connection to AAP 2.6
- HTTPS/TLS for API communication
- Bandwidth: 10 Gbps recommended

**Cost Estimate:**
- Hardware: $[X]K - $[Y]K (depending on GPU choice)
- Annual subscription: $[Z]K
- Operational costs: $[A]K annually

---

## Slide 16: Implementation Roadmap

**Proposed Timeline:**

**Phase 1: Planning & Approval (Weeks 1-2)**
- Week 1: Architecture finalization and approval
- Week 2: Procurement (subscriptions + hardware if needed)
- Week 2: Pilot team selection and kickoff

**Phase 2: Deployment (Weeks 3-6)**
- Weeks 3-4: Infrastructure deployment (if self-hosted)
- Week 5: Ansible Lightspeed configuration
- Week 6: Integration testing and validation

**Phase 3: Pilot Program (Weeks 7-12)**
- Week 7: Pilot launch with [X] engineers
- Weeks 8-11: Usage, feedback collection, optimization
- Week 12: Results analysis and ROI measurement

**Phase 4: Rollout (Month 4+)**
- Month 4: Expand to broader team (phased approach)
- Month 5+: Track ongoing value and optimization
- Continuous: Knowledge sharing and best practices

**Total time to pilot results:** ~12 weeks

---

## Slide 17: Success Metrics & ROI

**How We'll Measure Success:**

**Primary Metrics:**
- ⏱️ **Time to develop automation:** Hours per playbook (target: -40%)
- 📚 **Onboarding time:** Days to productivity (target: -60%)
- 🐛 **Code quality:** Error rate, best practices compliance (target: +30%)
- 😊 **User satisfaction:** Team adoption and feedback (target: 80%+ positive)

**Business Metrics:**
- 💰 **Automation backlog reduction:** % decrease in pending requests
- 🚀 **Automation coverage:** % of infrastructure under automation
- 💼 **Business value:** Revenue protected, cost avoided, time saved

**Expected ROI:**
- Break-even: [X] months
- Annual benefit: $[Y]K in productivity gains
- 3-year NPV: $[Z]K

**Case Study:** [Include brief example from similar customer if available]

---

## Slide 18: Security & Compliance

**Data Security:**

**For All Options:**
- 🔒 TLS 1.3 encryption in transit
- 🔐 API key authentication
- 📊 Audit logging enabled
- 👥 RBAC integration with AAP

**For Self-Hosted (RHEL AI / OpenShift AI):**
- 🏢 All data stays within your environment
- 🔒 Your encryption policies apply
- 🌐 No external data transmission
- 🛡️ Your security controls govern access

**For IBM watsonx SaaS:**
- 🏢 IBM Cloud security controls (SOC 2, ISO 27001)
- 🔒 Data encrypted at rest in IBM infrastructure
- 📋 GDPR and compliance certifications
- 🤝 IBM Data Processing Agreement

**Compliance Assessment:**
[Table showing how each option meets specific customer compliance requirements]

---

## Slide 19: Risk Assessment & Mitigation

**Potential Risks & Mitigations:**

**Risk: AI generates incorrect or insecure code**
- ✅ Mitigation: Code review processes remain essential
- ✅ Mitigation: CI/CD testing validates all generated code
- ✅ Mitigation: Ansible Lint integration for quality checks

**Risk: Team adoption resistance**
- ✅ Mitigation: Start with champion users (pilot program)
- ✅ Mitigation: Training and enablement plan
- ✅ Mitigation: Highlight productivity gains and frustration reduction

**Risk: Infrastructure investment before ROI**
- ✅ Mitigation: Start with IBM watsonx SaaS (minimal investment)
- ✅ Mitigation: Pilot program validates value before scale
- ✅ Mitigation: Clear ROI metrics and timeline

**Risk: Vendor/technology lock-in**
- ✅ Mitigation: Open technologies (OpenShift, RHEL, open models)
- ✅ Mitigation: MCP support coming (broader LLM compatibility)
- ✅ Mitigation: Red Hat + IBM enterprise support

---

## Slide 20: Investment Summary

**Total Investment Overview:**

**Option 1: IBM watsonx SaaS**
- **Upfront:** $[X]K (subscription, setup)
- **Year 1:** $[Y]K total
- **Year 2-3:** $[Z]K annually
- **TCO (3-year):** $[Total]K

**Option 2: RHEL AI (Self-Hosted)**
- **Upfront:** $[X]K (hardware, subscription, services)
- **Year 1:** $[Y]K total
- **Year 2-3:** $[Z]K annually (subscription + ops)
- **TCO (3-year):** $[Total]K

**Option 3: OpenShift AI**
- **Upfront:** $[X]K (platform, GPU, subscription, services)
- **Year 1:** $[Y]K total
- **Year 2-3:** $[Z]K annually
- **TCO (3-year):** $[Total]K

**Expected ROI:**
- Productivity gains: $[X]K annually
- Break-even: [Y] months
- 3-year NPV: $[Z]K

---

## Slide 21: Comparison to Alternatives

**Why Not Just Use ChatGPT or Claude?**

❌ **Not integrated with AAP:** Separate tool, context switching  
❌ **Not Ansible-optimized:** Generic AI, not trained on Ansible  
❌ **No code completion:** Can't help while you're coding  
❌ **Compliance issues:** Data sent to external AI services  
❌ **No governance:** Can't control or audit usage  

**Ansible Lightspeed Advantages:**

✅ **Native AAP integration:** Built into the platform you already use  
✅ **Ansible-specific training:** Best accuracy for Ansible code generation  
✅ **IDE integration:** Real-time assistance while coding  
✅ **Enterprise control:** Deploy on-premises, audit everything  
✅ **Red Hat support:** Enterprise SLA and support model  

---

## Slide 22: What's Next - Pilot Program Proposal

**Proposed Pilot:**

**Scope:**
- Duration: 6-8 weeks
- Team: [10-20] automation engineers from [specific team/department]
- Environment: [Production / Non-production]
- Use cases: [Specific automation initiatives]

**Success Criteria:**
- 30%+ reduction in playbook development time
- 80%+ user satisfaction
- Zero security/compliance incidents
- Positive ROI demonstrated

**Deliverables:**
- Pilot report with metrics
- User feedback and recommendations
- Rollout plan for broader organization
- Lessons learned and optimizations

**Investment:**
- [Chosen option] deployment
- Red Hat services: [X] days
- Customer resources: [Y] people over [Z] weeks

---

## Slide 23: Immediate Next Steps

**Action Items:**

**Today (Before we leave this meeting):**
- [ ] Agree on recommended deployment option
- [ ] Identify pilot team and executive sponsor
- [ ] Confirm budget and timeline expectations

**This Week:**
- [ ] [Customer]: Assemble pilot team
- [ ] [Red Hat]: Prepare detailed architecture document
- [ ] [Customer]: Begin procurement process
- [ ] [Red Hat]: Schedule kickoff meeting

**Next 2 Weeks:**
- [ ] Finalize architecture and design
- [ ] Complete procurement
- [ ] Infrastructure planning (if self-hosted)
- [ ] Pilot team kickoff and training

**Weeks 3-6:**
- [ ] Deploy infrastructure
- [ ] Configure Ansible Lightspeed
- [ ] Begin pilot program

---

## Slide 24: Questions & Discussion

**Open Discussion:**

**Topics to Cover:**
- Any concerns or questions about deployment options?
- Security or compliance questions?
- Infrastructure sizing and requirements?
- Budget and procurement process?
- Pilot team composition and timeline?

**Our Commitment:**
- Architecture support throughout deployment
- Regular check-ins during pilot program
- Optimization and troubleshooting support
- Executive reporting and metrics

**Your Red Hat Team:**
- Technical Account Manager: [Name, contact]
- Solution Architect: [Name, contact]
- Account Executive: [Name, contact]

---

## Slide 25: Summary & Decision

**Key Takeaways:**

1. ✅ **Ansible Lightspeed delivers measurable value:** 30-50% productivity gains
2. ✅ **Three production-ready deployment options:** SaaS, RHEL AI, OpenShift AI
3. ✅ **Recommendation for [Customer]:** **[Chosen option]** based on your requirements
4. ✅ **Clear path forward:** Pilot program → Broader rollout
5. ✅ **Red Hat support:** Architecture, implementation, ongoing optimization

**Decision Needed Today:**
- Approve recommended deployment option
- Commit to pilot program
- Assign executive sponsor and budget

**Timeline:**
- **Decision today** → Production pilot in [X] weeks

**Next Meeting:**
- Kickoff: [Proposed date, 1-2 weeks]

---

## Slide 26: Thank You

**Contact Information:**

[Your Name]  
Technical Account Manager  
Red Hat  
📧 [email]  
📱 [phone]  

[Solution Architect Name]  
Solution Architect  
Red Hat  
📧 [email]  
📱 [phone]  

**Follow-up Materials:**
- Detailed technical integration guide
- Customer decision brief (15 pages)
- Architecture diagrams
- Custom quote and timeline

**Thank you for your time!**

Questions?

---

## APPENDIX SLIDES (As Needed)

### Appendix A: Detailed Architecture Diagram
[Full technical architecture with all components]

### Appendix B: Hardware Specifications
[Detailed specs for self-hosted options]

### Appendix C: Model Comparison
[Granite model variants and capabilities]

### Appendix D: Security Deep Dive
[Detailed security controls and compliance mapping]

### Appendix E: API and Integration Details
[Technical integration points and APIs]

### Appendix F: Competitive Comparison
[How this compares to other AI coding assistants]

### Appendix G: Case Studies
[2-3 customer success stories with metrics]

### Appendix H: FAQ
[Common questions and answers]

---

## Presenter Notes

### Slide-by-Slide Tips

**Slides 1-4:** Set the context, establish pain points (5 minutes)
- Ask customer about their current challenges
- Get agreement that these are real problems for them

**Slides 5-7:** Show the solution and value (10 minutes)
- Demo if possible (screen share or recording)
- Focus on "wow factor" - this is significantly better than status quo

**Slides 8-9:** Technical reality check (5 minutes)
- Be honest about constraints (no direct OpenAI, etc.)
- Position as strategic vs. tactical limitation

**Slides 10-13:** Deployment options (15 minutes)
- Go deep on pros/cons for each
- Watch body language for which resonates
- Ask clarifying questions about requirements

**Slide 14:** Make recommendation (5 minutes)
- Be confident but open to discussion
- Tie directly to their stated requirements

**Slides 15-19:** Details and planning (10 minutes)
- Cover infrastructure, timeline, security based on chosen option
- Answer questions as they arise

**Slides 20-22:** Business case and next steps (5 minutes)
- Reinforce ROI and value
- Create urgency for decision

**Slides 23-25:** Close and commit (10 minutes)
- Get concrete commitments
- Schedule follow-up meetings
- Assign action items

**Slide 26:** Thank you and wrap (2 minutes)

### Customization Checklist

Before presenting:
- [ ] Replace all [Customer Name] placeholders
- [ ] Update timeline estimates based on customer requirements
- [ ] Insert actual cost estimates (work with Red Hat sales)
- [ ] Add customer-specific requirements to Slide 14
- [ ] Prepare demo or screenshots for Slide 6
- [ ] Customize risk mitigation for customer's concerns
- [ ] Add relevant case study to appendix
- [ ] Update contact information
- [ ] Review with Solution Architect for technical accuracy
- [ ] Practice timing (aim for 45 minutes + 15 min Q&A)

---

*Presentation Deck Outline for Ansible AAP 2.6 Lightspeed Customer Workshops*  
*Red Hat TAM Enablement - October 2025*

