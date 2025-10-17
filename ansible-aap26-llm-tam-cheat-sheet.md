# Ansible Lightspeed - TAM Cheat Sheet
## Quick Reference for Customer Conversations

**Last Updated:** October 16, 2025

---

## 30-Second Elevator Pitch

*"AAP 2.6 includes Ansible Lightspeed - an AI assistant that lives right in the platform. Think of it like GitHub Copilot but specifically trained for Ansible. Early adopters are seeing 30-50% faster playbook development. It requires specific infrastructure from Red Hat or IBM - we have three production-ready options. Would you like to see how this could accelerate your automation initiatives?"*

---

## Key Facts (Memorize These)

### What It Is
✅ AI-powered assistant built into AAP 2.6  
✅ Natural language → Ansible code generation  
✅ Real-time Q&A about Ansible concepts  
✅ IDE integration (VS Code) for code completion  
✅ Production-ready, fully supported by Red Hat  

### What It's NOT
❌ Standalone chatbot (integrated with AAP)  
❌ Works with any LLM (Red Hat/IBM only)  
❌ Replaces automation engineers (accelerates them)  
❌ Available on standalone AAP (requires OpenShift)  

### Key Stats
- **30-50%** faster playbook development
- **60%** reduction in onboarding time
- **4-5 days** to production (watsonx SaaS)
- **3 deployment options** (SaaS, RHEL AI, OpenShift AI)

---

## The Three Options (Quick Version)

### 1. IBM watsonx SaaS ⭐
**When:** Customer wants fast deployment, has cloud connectivity  
**Pitch:** "Production in less than a week, zero infrastructure, best Ansible accuracy"  
**Cost:** Subscription + usage  
**Timeline:** 4-5 days

### 2. RHEL AI (Self-hosted)
**When:** Customer needs data sovereignty, air-gap, or compliance  
**Pitch:** "Complete control, air-gap capable, predictable costs, all data stays on-premises"  
**Cost:** Subscription + infrastructure  
**Timeline:** 2-3 weeks

### 3. OpenShift AI
**When:** Customer has OpenShift, multiple AI initiatives planned  
**Pitch:** "Enterprise AI platform, supports Lightspeed plus other AI workloads, shared infrastructure"  
**Cost:** Subscription + cluster infrastructure  
**Timeline:** 2-4 weeks

---

## Common Customer Questions & Answers

### "Can we use ChatGPT or Claude with this?"
**Answer:** "Not directly in AAP 2.6. Ansible Lightspeed uses Ansible-specific models from Red Hat/IBM for best accuracy. There's a Model Context Protocol in tech preview that will enable broader LLM support in future releases, but today it requires Red Hat or IBM infrastructure."

### "Why not just use ChatGPT separately?"
**Answer:** "Three reasons: First, Lightspeed is trained specifically on Ansible - better accuracy. Second, it's integrated right into AAP and your IDE - no context switching. Third, for many organizations, sending automation code to external AI services violates security policies. Lightspeed gives you enterprise control."

### "Will this replace our automation engineers?"
**Answer:** "Absolutely not. Think of it like spell-check for writers - it makes them faster and more accurate, but you still need skilled engineers. What it does is eliminate boilerplate work, provide instant answers to syntax questions, and help junior engineers learn faster. Your senior engineers will focus more on architecture and less on syntax."

### "How much does it cost?"
**Answer:** "It depends on your deployment model. IBM watsonx SaaS is subscription plus usage-based pricing. Self-hosted options (RHEL AI or OpenShift AI) are subscription plus your infrastructure costs. Let me connect you with our team for a custom quote based on your requirements."

### "Do we need GPUs?"
**Answer:** "For self-hosted deployments, GPUs are highly recommended for production performance but not strictly required. You can start with CPU-only for testing, then add GPUs as you scale. For IBM watsonx SaaS, GPUs are IBM's problem - you don't need to worry about it."

### "What if it generates bad code?"
**Answer:** "Great question - this is an assistant, not autopilot. Code review, testing, and CI/CD validation remain essential. The AI provides a strong starting point and catches common mistakes, but human oversight is still critical. Think of it as pair programming with an AI that knows all the Ansible best practices."

### "Is our code being sent to train other models?"
**Answer:** "No. For IBM watsonx, IBM has strict data protection - your code is not used for training. For self-hosted (RHEL AI/OpenShift AI), everything stays in your environment. All options provide audit logging for compliance."

### "Do we have to upgrade to AAP 2.6?"
**Answer:** "Yes, Ansible Lightspeed is only available in AAP 2.6 and later. The good news is AAP 2.6 has other significant improvements too - new analytics dashboard, self-service portal, and platform enhancements. Let's talk about your upgrade timeline."

### "Can we try it before committing?"
**Answer:** "Absolutely. I recommend a pilot program - we deploy for 10-20 of your automation engineers, run for 6-8 weeks, measure productivity gains, and then you decide on broader rollout. Low risk, measurable ROI."

### "What about air-gapped environments?"
**Answer:** "RHEL AI and IBM watsonx self-hosted both support fully air-gapped deployments. All models and infrastructure run on your premises with no external connectivity required."

### "How long does deployment take?"
**Answer:** "IBM watsonx SaaS: 4-5 days. Self-hosted options: 2-4 weeks depending on infrastructure readiness. Then 6-8 week pilot program to validate value before broader rollout."

---

## Objection Handling

### Objection: "We're not ready to adopt AI yet"
**Response:** "I understand the hesitation. Here's what I'd suggest: Let's do a small pilot with 10 engineers for 6 weeks. You'll have concrete data on productivity gains before making any big decisions. The investment is minimal for the pilot. What if we could prove 30% faster development in your own environment?"

### Objection: "This sounds expensive"
**Response:** "Let's look at the ROI. If you have 20 automation engineers spending 50% of their time writing playbooks, and we can cut that time by 40%, that's [do the math] hours saved annually. At an average engineer cost of $[X]/hour, that's $[Y]K in productivity gains. Self-hosted options have higher upfront costs but lower ongoing costs. SaaS options spread the cost over time. Which financial model works better for your organization?"

### Objection: "We don't have budget this year"
**Response:** "Understood. Can we plan for next fiscal year? I can help you build the business case now with projected ROI, timeline, and resource requirements. We could also explore starting with IBM watsonx SaaS which has lower upfront investment, then migrate to self-hosted in Year 2 if needed."

### Objection: "We need to evaluate other options"
**Response:** "Smart approach. What other options are you considering? [Listen, then position] Most generic AI assistants aren't trained on Ansible specifically, which means lower accuracy and no integration with AAP. Happy to help you evaluate alternatives - I want you to make the best decision for your organization."

### Objection: "Our security team will never approve this"
**Response:** "Let me connect you with customers in [similar industry] who had the same concern. They chose [RHEL AI/OpenShift AI self-hosted] where all data stays on-premises, no external connectivity, and they control all security policies. Would you like me to set up a call with your security team and our security architects to walk through the architecture?"

### Objection: "We need to see it working first"
**Response:** "Absolutely. Two options: First, I can show you a demo right now [screen share or video]. Second, we could do a small proof-of-concept in your environment with a couple of your engineers - typically 2-3 days. Which would be more helpful?"

---

## Customer Qualification Questions

**Ask these to determine fit and next steps:**

### Technical Qualification
- [ ] Current AAP version? (Need 2.6 or willing to upgrade)
- [ ] Deployed on OpenShift? (Required for Lightspeed)
- [ ] Air-gapped environment? (Determines deployment options)
- [ ] Data sovereignty requirements? (Impacts SaaS vs. self-hosted)
- [ ] Existing GPU infrastructure? (Helps with self-hosted sizing)

### Business Qualification
- [ ] Size of automation team? (Determines infrastructure sizing)
- [ ] Current automation backlog? (Pain point identification)
- [ ] Budget availability? (Timing and options)
- [ ] Decision makers identified? (Sales strategy)
- [ ] Timeline expectations? (Realistic planning)

### Engagement Qualification
- [ ] Executive sponsor available? (Required for success)
- [ ] Pilot team identified? (Can we start small?)
- [ ] Success metrics defined? (How will they measure value?)
- [ ] Competitive evaluation? (Who else are they considering?)

---

## Red Flags (When to Pause)

🚩 **"We want to use OpenAI GPT-4 for this"**
- **Issue:** Not supported in AAP 2.6 (MCP in tech preview only)
- **Action:** Explain limitations, discuss future roadmap

🚩 **"We're not on OpenShift and don't plan to be"**
- **Issue:** Lightspeed requires AAP on OpenShift
- **Action:** Discuss OpenShift value or defer until OpenShift adoption

🚩 **"We have 5 automation engineers total"**
- **Issue:** May not have scale for ROI (especially self-hosted)
- **Action:** IBM watsonx SaaS only, or defer until team grows

🚩 **"We don't have any budget this year or next"**
- **Issue:** Not a real opportunity right now
- **Action:** Plant seeds, provide materials, revisit next fiscal cycle

🚩 **"We're still on AAP 1.2"**
- **Issue:** Multi-version upgrade before Lightspeed benefit
- **Action:** Focus on AAP upgrade value, Lightspeed as future benefit

---

## Sales Play Opportunities

### High-Probability Opportunities
✅ AAP 2.5 → 2.6 upgrades (natural addition)  
✅ Large automation teams (20+ engineers)  
✅ Organizations with automation backlog  
✅ Customers with AI strategy initiatives  
✅ New AAP deployments on OpenShift  

### Expansion Opportunities
✅ Customer already using AAP → add Lightspeed  
✅ RHEL AI purchase → add AAP/Lightspeed use case  
✅ OpenShift AI purchase → add Lightspeed workload  
✅ IBM watsonx customers → add Ansible use case  

### Competitive Defense
✅ GitHub Copilot users → "but not Ansible-specific"  
✅ ChatGPT users → "not integrated, security concerns"  
✅ Generic LLM tools → "Lightspeed is purpose-built"  

---

## Proof Points & References

### Industries with Success
- Financial Services (data sovereignty)
- Government (air-gapped deployments)
- Healthcare (compliance requirements)
- Large Enterprise (multi-cloud automation)

### Use Cases
- Infrastructure automation (provisioning, config mgmt)
- Security automation (compliance, remediation)
- Application deployment
- Network automation
- Cloud automation (AWS, Azure, GCP)

### Metrics to Quote
- "30-50% faster playbook development"
- "60% reduction in onboarding time"
- "Improved code quality and consistency"
- "Higher automation adoption rates"

---

## Next Steps Framework

### First Conversation
1. Qualify interest and fit
2. Send executive summary (one-pager)
3. Schedule architecture discussion

### Second Conversation
1. Architecture workshop (60-90 min)
2. Review requirements
3. Recommend deployment option
4. Discuss pilot program

### Third Conversation (Decision Meeting)
1. Present custom proposal
2. Address concerns
3. Get commitment
4. Set kickoff date

### Post-Decision
1. Kickoff meeting
2. Deploy infrastructure
3. Configure integration
4. Launch pilot
5. Measure and expand

---

## Resources to Share

### First Touch (Light)
- `ansible-aap26-llm-executive-summary.md` (1 page)
- AAP 2.6 What's New webinar link

### Second Touch (Detailed)
- `ansible-aap26-llm-customer-brief.md` (15 pages)
- `ansible-aap26-llm-quick-reference.md` (5 pages)
- Case study (if available)

### Technical Deep Dive
- `ansible-aap26-llm-integration-guide.md` (20+ pages)
- Red Hat official documentation links
- Architecture diagrams

---

## Internal Resources

### Who to Engage
- **Solution Architect:** Architecture workshops, technical design
- **Account Executive:** Pricing, contracts, executive relationships
- **Specialist SA (AI):** Deep technical questions, competitive situations
- **Product Management:** Roadmap questions, feature requests

### When to Escalate
- Complex architecture (multi-site, large scale)
- Competitive situation (need specialist)
- Executive-level discussions (bring AE)
- Pricing negotiations (AE + sales management)

---

## Quick Win Strategies

### Strategy 1: AAP Upgrade Add-on
- **When:** Customer planning AAP 2.6 upgrade
- **Pitch:** "While you're upgrading, let's add Lightspeed for a few engineers. Minimal additional investment, significant value."
- **Success Rate:** High

### Strategy 2: New Hire Onboarding Tool
- **When:** Customer hiring automation engineers
- **Pitch:** "Cut onboarding time from weeks to days with AI mentorship."
- **Success Rate:** Medium-High

### Strategy 3: Automation Backlog Attack
- **When:** Customer has large automation backlog
- **Pitch:** "Cut playbook development time in half, clear your backlog faster."
- **Success Rate:** Medium-High

### Strategy 4: Code Quality Initiative
- **When:** Customer has inconsistent automation code
- **Pitch:** "AI enforces best practices automatically, improves code quality."
- **Success Rate:** Medium

---

## Meeting Preparation Checklist

### Before Customer Call
- [ ] Review customer's AAP version and OpenShift status
- [ ] Check recent support cases (any automation pain points?)
- [ ] Review customer industry and compliance requirements
- [ ] Prepare 2-3 relevant use cases for their environment
- [ ] Have demo or screenshots ready
- [ ] Know who else to bring (SA, AE, specialist)

### Materials to Have Ready
- [ ] Executive summary (1-page)
- [ ] Customer brief (detailed)
- [ ] Architecture diagrams
- [ ] Pricing guidance (ballpark)
- [ ] Timeline estimates
- [ ] Reference customer list (similar industry)

### Post-Call Follow-up
- [ ] Send promised materials within 24 hours
- [ ] Log opportunity in CRM
- [ ] Schedule next meeting before ending call
- [ ] Send recap email with action items
- [ ] Coordinate with AE and SA team

---

## Calendar Templates

### Architecture Workshop (2 hours)
**Agenda:**
- 15 min: Introductions and objectives
- 30 min: Ansible Lightspeed overview and demo
- 45 min: Deployment options discussion
- 15 min: Requirements deep dive
- 15 min: Q&A and next steps

**Attendees:**
- Customer: IT leadership, automation leads, security/compliance
- Red Hat: TAM, SA, AE

---

### Executive Briefing (60 min)
**Agenda:**
- 10 min: Business value and ROI
- 20 min: Deployment options
- 15 min: Investment and timeline
- 15 min: Decision and next steps

**Attendees:**
- Customer: CIO/VP level, IT leadership
- Red Hat: TAM, AE, possibly RVP

---

### Pilot Kickoff (90 min)
**Agenda:**
- 15 min: Pilot goals and success criteria
- 30 min: Technical overview and access
- 30 min: Hands-on training
- 15 min: Q&A and support plan

**Attendees:**
- Customer: Pilot team (10-20 engineers), automation leads
- Red Hat: TAM, SA

---

## Success Checklist

### You Know You're Succeeding When:
✅ Customer asks "when can we start?" not "should we do this?"  
✅ Executive sponsor identified and engaged  
✅ Pilot team volunteer list exceeds target  
✅ Budget discussion shifts to "how much?" not "if we can afford it"  
✅ Customer proposing timeline acceleration  
✅ Security/compliance team proactively engaged  
✅ Customer sharing with other teams/departments  

---

## Remember

**Key Messages:**
1. **Ansible-specific:** Not generic AI - purpose-built for Ansible
2. **Integrated:** Built into AAP, not a separate tool
3. **Enterprise-ready:** Production-supported by Red Hat
4. **Proven ROI:** 30-50% faster development (measurable)
5. **Flexible deployment:** SaaS or self-hosted options

**Your Role:**
- Trusted advisor (not product pusher)
- Focus on customer success (not just making the sale)
- Pilot program approach (reduce risk, prove value)
- Solve real problems (address actual pain points)

**Bottom Line:**
This is a **genuine value add** for automation teams. When positioned correctly with the right customers, it's an easy win-win.

---

*TAM Cheat Sheet for Ansible Lightspeed Customer Conversations*  
*Red Hat TAM Enablement - October 2025*  
*Keep this handy for quick reference during customer calls*

