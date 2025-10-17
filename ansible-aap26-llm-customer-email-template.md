# Customer Email Template: Ansible Lightspeed AI Integration

---

## Email Template 1: Initial Introduction (Executive Level)

**Subject:** Ansible Automation Platform 2.6: AI-Powered Automation Acceleration

**To:** [Customer CIO/VP Infrastructure/VP Automation]  
**CC:** [Customer IT Director, TAM, Account Executive]

---

[Customer Name],

Red Hat has released **Ansible Automation Platform 2.6** with a significant new capability: **Ansible Lightspeed**, an AI-powered intelligent assistant that accelerates automation development and improves team productivity.

**What this means for [Customer Organization]:**
- 30-50% faster automation development (describe task → get Ansible code)
- Dramatically reduced onboarding time for new automation engineers
- Real-time best practices guidance and troubleshooting assistance
- Improved code quality and consistency across teams

**Key Insight:** Early adopters report cutting playbook development time in half while improving code quality.

Unlike generic AI chatbots, Ansible Lightspeed is purpose-built for Ansible automation and requires specific LLM infrastructure from Red Hat or IBM. There are three production-ready deployment options, each optimized for different business requirements:

1. **IBM watsonx (SaaS)** - Fastest deployment (days), fully managed, Ansible-optimized
2. **Self-hosted (RHEL AI)** - Complete data sovereignty, air-gap capable, predictable costs
3. **OpenShift AI Platform** - Enterprise AI/ML platform for multiple initiatives

**I'd like to discuss:**
- Which deployment model aligns with your security and compliance requirements
- Expected ROI and productivity gains for your automation teams
- Implementation timeline and resource requirements
- Pilot program approach with 10-20 of your automation engineers

**Proposed next step:** 60-minute architecture review call with Red Hat Solution Architect to assess fit and deployment options.

Are you available [propose 2-3 time slots] for a brief discussion?

I've attached a one-page executive summary and can provide detailed technical documentation upon request.

Best regards,

[Your Name]  
[Your Title]  
Red Hat Technical Account Manager  
[Contact Information]

**Attachments:**
- `ansible-aap26-llm-executive-summary.pdf` (1 page)

---

## Email Template 2: Technical Stakeholder (Detailed)

**Subject:** AAP 2.6 AI Integration: Technical Overview & Architecture Options

**To:** [Customer Automation Lead/Architect/DevOps Manager]  
**CC:** [TAM, Solution Architect]

---

[Customer Name],

Following up on [previous conversation/CIO meeting/AAP 2.6 announcement], I wanted to provide technical details about Ansible Lightspeed AI integration options for your environment.

**Technical Overview:**

Ansible Lightspeed delivers:
- Natural language to Ansible code generation
- Context-aware code completion in VS Code
- Best practices guidance and troubleshooting assistance
- Integration with AAP 2.6 on OpenShift

**The Key Technical Decision:** LLM Infrastructure

AAP 2.6 Lightspeed requires specific LLM infrastructure from Red Hat or IBM. You have three production-ready options:

**Option 1: IBM watsonx Code Assistant (SaaS)**
- Deployment: 4-5 days
- Infrastructure: None (IBM Cloud)
- Best for: Fast deployment, cloud-connected environments
- Model: Ansible-specific Granite (best accuracy)

**Option 2: Red Hat Enterprise Linux AI (Self-hosted)**
- Deployment: 2-3 weeks
- Infrastructure: Dedicated RHEL server + GPU (recommended)
- Best for: Data sovereignty, air-gapped environments
- Model: Open-source Granite models via vLLM

**Option 3: Red Hat OpenShift AI (Platform)**
- Deployment: 2-4 weeks
- Infrastructure: OpenShift cluster + GPU nodes
- Best for: Multiple AI initiatives, enterprise MLOps
- Model: Granite models via model serving

**Important Limitation:**
- Cannot use OpenAI, Anthropic, Google, or other third-party LLMs directly
- Must use Red Hat/IBM AI infrastructure
- (Future: Model Context Protocol support will expand options)

**Your Environment Considerations:**

Based on what I know about [Customer Organization]:
- [Data sovereignty requirements] → Suggests self-hosted approach
- [Existing OpenShift deployment] → OpenShift AI may be efficient
- [Air-gap requirements] → RHEL AI or watsonx self-hosted required
- [Cloud-first strategy] → IBM watsonx SaaS fastest path

**Proposed Next Steps:**

1. **Architecture Workshop** (2 hours)
   - Review your security/compliance requirements
   - Size infrastructure for self-hosted options
   - Discuss integration with existing AAP deployment
   - Identify pilot team and success metrics

2. **Proof of Concept** (Optional, 2-4 weeks)
   - Deploy in non-production environment
   - Test with 5-10 engineers
   - Measure productivity gains
   - Validate security and compliance

3. **Pilot Program** (6-8 weeks)
   - Production deployment
   - 10-20 automation engineers
   - Measure ROI and gather feedback
   - Plan broader rollout

**Technical Documentation Available:**
- Complete integration guide (20+ pages)
- Quick reference card (5 pages)
- Customer decision brief (15 pages)
- Architecture diagrams and configuration examples

**Would you like to schedule an architecture workshop?**

I can bring in our Solution Architect to walk through the options in detail and size infrastructure requirements specific to your environment.

Available times: [propose 2-3 time slots]

Let me know what works best for your team.

Best regards,

[Your Name]  
[Your Title]  
Red Hat Technical Account Manager  
[Contact Information]

**Attachments:**
- `ansible-aap26-llm-quick-reference.pdf`
- `ansible-aap26-llm-integration-guide.pdf`

---

## Email Template 3: Follow-up After Initial Discussion

**Subject:** AAP 2.6 AI Integration: Next Steps & Architecture Review

**To:** [Customer Stakeholder]  
**CC:** [Red Hat SA, Account Executive]

---

[Customer Name],

Thank you for the productive discussion about Ansible Lightspeed AI integration on [date]. 

**Summary of Your Requirements:**
- [Data sovereignty: Yes/No]
- [Air-gap requirement: Yes/No]  
- [Existing OpenShift: Yes/No]
- [Timeline expectation: X weeks/months]
- [Pilot team size: X engineers]

**Recommended Approach:**

Based on your requirements, I recommend **[Option Name]** for the following reasons:
- [Reason 1 aligned to their requirements]
- [Reason 2 aligned to their requirements]
- [Reason 3 aligned to their requirements]

**Proposed Timeline:**

**Phase 1: Planning & Approval (Weeks 1-2)**
- Week 1: Architecture workshop with Red Hat Solution Architect
- Week 2: Infrastructure sizing and cost proposal
- Week 2: Executive approval and procurement

**Phase 2: Deployment (Weeks 3-6)**
- [Details specific to chosen option]
- Infrastructure deployment (if self-hosted)
- Ansible Lightspeed configuration
- Integration testing and validation

**Phase 3: Pilot (Weeks 7-12)**
- Pilot with [X] engineers from [team name]
- Training and enablement
- Gather metrics: development time, code quality, user satisfaction
- Optimization based on feedback

**Phase 4: Rollout (Month 4+)**
- Expand to broader organization
- Track ROI and business value
- Plan additional automation initiatives

**Next Steps:**

1. **Schedule Architecture Workshop**
   - Duration: 2 hours
   - Attendees: [Your team] + Red Hat Solution Architect + TAM
   - Proposed dates: [3 options]

2. **Prepare for Workshop**
   - Review attached decision brief
   - Identify pilot team members
   - Document any specific security/compliance requirements

3. **Post-Workshop**
   - Custom architecture proposal
   - Detailed cost breakdown
   - Implementation plan with milestones

**Questions or Concerns?**

Please don't hesitate to reach out. I'm available [your availability] for a quick call if you'd like to discuss any aspect in more detail.

Looking forward to the architecture workshop!

Best regards,

[Your Name]  
[Your Title]  
Red Hat Technical Account Manager  
[Contact Information]

**Attachments:**
- `ansible-aap26-llm-customer-brief.pdf`

---

## Email Template 4: Quick "Did You Know" / Awareness

**Subject:** New in AAP 2.6: AI-Powered Automation Assistant

**To:** [Customer Ansible Users/Champions]  
**CC:** [Customer IT Leadership]

---

[Customer Team],

Quick heads-up about an exciting new capability in Ansible Automation Platform 2.6:

**Ansible Lightspeed** - an AI assistant that lives right inside AAP and your IDE.

**How it works:**
1. Type a description: "Deploy nginx with SSL and firewall rules"
2. Get instant Ansible code with best practices built in
3. Ask questions: "Why isn't this playbook idempotent?"
4. Get real-time guidance while you code

**Early adopter results:**
- 30-50% faster playbook development
- New team members productive in days instead of weeks
- Improved code quality (AI knows all the best practices)

**Demo video:** [link if available]

This requires some infrastructure planning (it's not just "plug in ChatGPT"), so I wanted to start the conversation early.

**Interested in learning more?**

Reply to this email and I'll set up a brief demo and discussion about deployment options.

Quick read: [attach one-page executive summary]

Thanks,

[Your Name]  
Red Hat TAM

---

## Email Template 5: Post-Webinar/Event Follow-up

**Subject:** Following up: AAP 2.6 AI Integration Discussion

**To:** [Customer Attendee]

---

[Customer Name],

Great to connect with you at [event/webinar name] yesterday!

As discussed, Ansible Lightspeed in AAP 2.6 could significantly accelerate your automation initiatives, particularly around [specific use case they mentioned].

**What I heard from you:**
- [Pain point 1: e.g., slow playbook development]
- [Pain point 2: e.g., inconsistent coding practices across teams]
- [Requirement: e.g., must stay on-premises for compliance]

**How Ansible Lightspeed addresses this:**
- [Solution to pain point 1]
- [Solution to pain point 2]
- [How it meets their requirement]

**Recommended Next Step:**

Let's schedule a 30-minute call to:
1. Discuss your specific environment and requirements
2. Identify which deployment option fits best (SaaS vs. self-hosted)
3. Outline a pilot program approach

I have availability:
- [Time slot 1]
- [Time slot 2]
- [Time slot 3]

Or suggest a time that works better for you.

I've attached a quick reference guide that summarizes the options - worth a 5-minute read before our call.

Looking forward to continuing the conversation!

Best regards,

[Your Name]  
[Title]  
[Contact Info]

**Attachment:** `ansible-aap26-llm-quick-reference.pdf`

---

## Email Template 6: Quarterly Business Review (QBR) Mention

**Subject:** Q[X] QBR: Agenda & AAP 2.6 AI Capabilities

**To:** [Customer Executive Sponsor]  
**CC:** [Customer IT Leads, Red Hat Account Team]

---

[Customer Name],

Looking forward to our Q[X] Quarterly Business Review on [date].

**Proposed Agenda:**

1. **AAP Usage & Value Review** (15 min)
   - Current automation coverage and growth
   - Business value delivered this quarter
   - Key metrics and trends

2. **Technical Health Check** (15 min)
   - Platform performance and stability
   - Support case review and resolution
   - Upgrade planning (if applicable)

3. **New Capability: Ansible Lightspeed AI** (20 min)
   - Overview of AI-powered automation assistant
   - Deployment options aligned to your requirements
   - Expected ROI and productivity gains
   - Pilot program proposal

4. **Roadmap & Strategic Planning** (10 min)
   - Upcoming automation initiatives
   - Infrastructure modernization alignment
   - Training and enablement needs

**Pre-read Materials:**

I've attached a one-page overview of Ansible Lightspeed for your review before the meeting. This will help maximize our discussion time.

**Meeting Details:**
- **Date:** [Date]
- **Time:** [Time + Timezone]
- **Duration:** 60 minutes
- **Location:** [In-person / Video conference link]

Please let me know if you'd like to adjust the agenda or add any topics.

See you on [date]!

Best regards,

[Your Name]  
Red Hat Technical Account Manager  
[Contact Information]

**Attachment:** `ansible-aap26-llm-executive-summary.pdf`

---

## Tips for Using These Templates

### Personalization
- Replace ALL bracketed placeholders with customer-specific details
- Reference actual conversations, pain points, and requirements
- Adjust tone based on customer relationship (formal vs. casual)
- Use customer's terminology (if they say "runbooks" instead of "playbooks", match it)

### Timing
- **Initial Introduction:** After AAP 2.6 upgrade discussion or general check-in
- **Technical Detail:** After executive expresses interest
- **Follow-up:** Within 24-48 hours of verbal discussion
- **QBR Mention:** 1-2 weeks before scheduled QBR

### Attachments
- **Executive:** One-page summary only (don't overwhelm)
- **Technical:** Quick reference + full guide (they want depth)
- **Follow-up:** Custom architecture proposal if available

### Response Tracking
- Set follow-up reminder for 3-5 business days if no response
- Have Red Hat Account Executive reach out if TAM emails go unanswered
- Escalate to executive sponsor if strategic opportunity

---

**Using These Templates:**

1. Copy template to email client
2. Replace ALL [bracketed content] with specifics
3. Personalize based on customer relationship
4. Attach appropriate documents
5. Send and track response
6. Follow up as needed

**Success Metrics:**
- 30%+ response rate to initial outreach
- 60%+ conversion to architecture workshop
- 40%+ conversion from workshop to pilot

---

*Email Templates for Ansible AAP 2.6 Lightspeed Customer Engagement*  
*Red Hat TAM Enablement - October 2025*

