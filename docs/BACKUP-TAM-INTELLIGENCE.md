# Backup TAM Intelligence Features

**Purpose:** Enable backup TAMs to provide seamless coverage during primary TAM absences by leveraging automated intelligence and cross-case analysis.

---

## The Backup TAM Challenge

From the **TAM Manual**, backup TAMs are expected to:

✅ **Monitor customer cases** and ensure timely responses  
✅ **Handle escalations** and critical situations  
✅ **Maintain customer relationships** and trust  
✅ **Continue proactive engagement** per the TAM Engagement Menu  
✅ **Provide substantive updates** aligned to SLAs  

**The Problem:** Backup TAMs lack the deep customer context, historical knowledge, and pattern recognition that primary TAMs develop over months/years of engagement.

---

## How RFE Tool Intelligence Solves This

### 1. **Cross-Case Analysis** - See What Others Miss

**Primary TAM Problem:**
- Manually reviews each case individually
- Misses patterns across multiple tickets
- Can't see systemic issues until they escalate

**Backup TAM Problem:**
- **10x worse** - no historical context
- Doesn't know if this is the 3rd networking issue this month
- Can't identify if multiple cases share a root cause

**RFE Tool Solution:**
```bash
tam-rfe-active-case-report --customer alma
```

**Automated Cross-Case Analysis Detects:**
- **Pattern Recognition**: "3 Ansible authentication failures in 2 weeks → likely credential rotation issue"
- **Root Cause Linking**: "Cases #123, #456, #789 all reference same RHEL 9.3 kernel → systemic bug"
- **Trend Analysis**: "Storage cases increased 200% this month → capacity planning needed"
- **Related Case Detection**: "This OCP networking issue is related to 2 other tickets from different contacts"

**Backup TAM Benefit:**
- Instantly understand **what's really happening** without reading 50+ case updates
- Spot **systemic issues** the customer hasn't connected themselves
- Provide **strategic insights** that build immediate credibility

---

### 2. **Smart Active Case Report** - Know What Needs Attention

**From TAM Manual:**
> "TAMs should always perform an Initial Screen on every case that comes in... evaluate severity, business impact, review attachments, and determine if the case is progressing."

**Backup TAM Problem:**
- 15+ open cases across 3 customers
- Which ones need immediate attention?
- Which ones are stuck waiting on customer vs Red Hat?
- Which ones are approaching SLA breach?

**RFE Tool Solution:**
```bash
tam-rfe-active-case-report --email backup-tam@redhat.com
```

**Smart Report Includes:**

#### **Priority Scoring**
```
CRITICAL ATTENTION NEEDED:
  Case #04280915 [Priority: 95/100]
    - Severity 2, breaches SLA in 4 hours
    - No update in 3 days
    - Customer last response: "Production impact"
    - Related to 2 other networking cases
    
HIGH PRIORITY:
  Case #04281203 [Priority: 78/100]
    - Severity 3, part of trend (5 similar cases)
    - Possible systemic issue with AAP 2.6 upgrade
    - Customer is strategic account (Tier 1)
```

#### **Health Indicators**
```
Account Health Score: 72/100 (⚠️ CAUTION)
  - SLA compliance: 85% (down from 95% last month)
  - Case velocity: Slower than average
  - Escalation risk: 2 cases flagged
```

#### **Trend Analysis**
```
📈 EMERGING ISSUES:
  - Satellite synchronization: 4 cases in 14 days (↑ 300%)
  - RHEL 9.3 kernel panics: 3 cases (NEW trend)
  
📉 IMPROVING AREAS:
  - OpenShift networking: 0 cases this week (was 3/week)
```

**Backup TAM Benefit:**
- **No guesswork** - tool tells you exactly where to focus
- **Proactive alerts** - catch issues before customer escalates
- **Context at a glance** - understand account health in 2 minutes

---

### 3. **Customer Intelligence Summary** - Get Up to Speed Fast

**From TAM Manual:**
> "Without meaningful engagement with our customers, we are severely limited in how we can support them. Without up to date information on their goals, projects, team and needs you can not form an action plan."

**Backup TAM Problem:**
- Primary TAM has 6+ months of customer knowledge
- Backup TAM has: *checks notes* ... a Salesforce account number
- Customer calls tomorrow - what do you say?

**RFE Tool Solution:**
```bash
tam-rfe-customer-intelligence --account 397076
```

**Intelligence Report Provides:**

#### **Environment Overview**
```
Products in Use:
  - RHEL 8.8, 9.2 (250 systems)
  - Ansible Automation Platform 2.4 (production)
  - OpenShift 4.14 (dev/test)
  
Infrastructure:
  - VMware vSphere 7.0
  - NetApp storage
  - Cisco networking
```

#### **Historical Patterns**
```
Common Issues (Last 6 Months):
  1. Ansible playbook performance (8 cases) → use async tasks
  2. RHEL kernel updates (5 cases) → requires reboot planning
  3. Satellite sync timeouts (4 cases) → known CDN issue
  
Known Workarounds:
  - Satellite: Use squid proxy for CDN
  - AAP: Increase job timeout to 3600s
```

#### **Customer Preferences**
```
Communication:
  - Prefers Slack for urgent issues (@john.smith)
  - Weekly TAM call: Tuesdays 10 AM ET
  - Escalation contact: Jane Doe (Director) - jane@alma.com
  
Constraints:
  - Change window: Sundays 2-6 AM only
  - No reboots during month-end (last 3 days)
  - Requires 2-week notice for major upgrades
```

**Backup TAM Benefit:**
- **Instant credibility** - "I see you've had Satellite sync issues before..."
- **Avoid mistakes** - Don't suggest reboots during month-end
- **Smart recommendations** - Reference solutions that worked before

---

### 4. **Proactive Issue Detection** - Be the Hero

**From TAM Manual:**
> "TAMs are a technical resource and often the fastest and most direct path involves you dedicating time to solve the customer issue. Even if you run into a ticket you cannot solve, add value and never 'kick it over the fence' and forget about it."

**Backup TAM Problem:**
- Primary TAM would have caught this emerging issue
- Backup TAM sees individual cases, misses the pattern
- Customer escalates: "Why didn't Red Hat warn us?"

**RFE Tool Solution:**

**Automated Alerts:**
```
🚨 PROACTIVE ALERT - alma (Account 397076)

EMERGING PATTERN DETECTED:
  Issue: Ansible job failures increasing
  Trend: 1 case/week → 3 cases/week (↑ 200%)
  Root cause: Likely AAP 2.4 → 2.5 upgrade side effect
  
RECOMMENDED ACTION:
  1. Review AAP 2.5 release notes (breaking changes)
  2. Open proactive case for upgrade planning
  3. Schedule customer call to discuss
  
SIMILAR PATTERNS:
  - 3 other TAM customers experienced same issue
  - Known solution: Update execution environment images
  
CUSTOMER IMPACT:
  - Production automation affected
  - Could delay month-end reporting (their constraint)
```

**Backup TAM Benefit:**
- **Be proactive** even without deep customer knowledge
- **Demonstrate value** - "I noticed a trend in your cases..."
- **Prevent escalations** - catch issues before they blow up

---

## Real-World Backup TAM Scenario

**Situation:**
- Primary TAM (Sarah) on PTO for 2 weeks
- Backup TAM (Mike) covering 3 of Sarah's accounts
- Customer (Alma) has 12 open cases

**Without RFE Intelligence:**
```
Mike's approach:
1. Manually read 12 case descriptions (2 hours)
2. Guess which ones are important (???)
3. Wait for customer to escalate (reactive)
4. Struggle to provide strategic insights (no context)
5. Customer thinks: "This backup TAM doesn't know our account"
```

**With RFE Intelligence:**
```
Mike's approach:
1. Run: tam-rfe-active-case-report --customer alma (2 minutes)
2. Tool highlights: 3 critical cases, 1 emerging trend
3. Run: tam-rfe-customer-intelligence --account 397076 (1 minute)
4. Review intelligence summary (5 minutes)

Mike now knows:
  ✅ Which 3 cases need immediate attention
  ✅ Alma has had Satellite sync issues before (known fix)
  ✅ There's an emerging Ansible pattern (3 cases related)
  ✅ Month-end is in 5 days (no changes allowed)
  
Mike sends email:
---
Subject: Account Update - Emerging Ansible Pattern Detected

Hi John,

I'm covering for Sarah this week. I've reviewed your active cases and wanted 
to flag an emerging pattern I noticed:

Three recent Ansible job failures (cases #123, #456, #789) appear related to 
the AAP 2.5 upgrade. This is consistent with what we're seeing across other 
customers who upgraded recently.

I've identified the root cause and have a recommended fix. Since month-end is 
in 5 days, let's schedule a quick call to discuss the fix so we can implement 
it during your next change window (Sunday 2-6 AM).

Also, I see Case #04280915 (networking) is approaching SLA - I've already 
engaged the SBR team and we'll have an update by EOD.

Best regards,
Mike
---

Customer thinks: "Wow, this backup TAM really understands our account!"
```

---

## Email Report Customization for Backup TAMs

**From TAM Manual:**
> "Backup TAMs should add themselves as account members and configure notifications appropriately."

**RFE Tool Enhancement:**

### **Configure Backup TAM Reports**

```bash
tam-rfe-report-scheduler
```

**Backup TAM Workflow:**
1. **Before Primary TAM PTO**: Add backup TAM to email CC
2. **Daily digest**: Backup TAM receives same intelligence as primary
3. **Smart alerts**: Only notified if action needed
4. **After PTO**: Remove backup TAM from CC

**Example Schedule:**
```yaml
# Primary TAM: sarah@redhat.com
# Backup TAM: mike@redhat.com (receives CC during PTO)

schedule:
  frequency: daily
  time: "08:00"
  timezone: "America/New_York"
  
recipients:
  primary: sarah@redhat.com
  cc: mike@redhat.com  # Automatically added during PTO

intelligence_level: backup_tam  # More context, less noise

include:
  - priority_cases      # Cases needing immediate attention
  - emerging_trends     # Patterns to watch
  - customer_context    # Quick reference guide
  - known_workarounds   # Solutions that worked before
  - escalation_risks    # Cases that may escalate
```

---

## Benefits Summary

| **Feature** | **Primary TAM** | **Backup TAM** | **Backup TAM Benefit** |
|-------------|-----------------|----------------|------------------------|
| **Cross-Case Analysis** | Saves 2 hours/week | Saves 5 hours/week | **2.5x time savings** |
| **Priority Scoring** | Nice to have | **Critical** | Know what matters most |
| **Customer Intelligence** | Builds over time | **Instant context** | Immediate credibility |
| **Proactive Alerts** | Enhances service | **Enables service** | Be proactive without deep knowledge |
| **Trend Detection** | Catches patterns | **Prevents blind spots** | See what you'd otherwise miss |

---

## TAM Manager Perspective

**From TAM Manual:**
> "It is your onboarding buddy's responsibility to set you on the path for success and they are fully committed to helping you achieve that goal."

**For TAM Managers:**

### **Enable Seamless Coverage**

**Without RFE Intelligence:**
- Backup TAM struggles with context
- Customer experience degrades during PTO
- Escalations more likely
- Manager fields customer concerns

**With RFE Intelligence:**
- Backup TAM hits ground running
- Customer experience remains consistent
- Proactive engagement continues
- Manager can focus on strategic issues

**Best Practice:**
```bash
# Set up backup coverage intelligence before PTO
tam-rfe-report-scheduler --configure-backup \
  --primary-tam sarah@redhat.com \
  --backup-tam mike@redhat.com \
  --start-date 2025-10-20 \
  --end-date 2025-11-03 \
  --include-intelligence-summary
```

---

## Conclusion

**The TAM Manual emphasizes:**
> "Combining proactive engagement with reactive support and targeted action against critical customer needs, the TAM has the flexibility to provide each customer with a unique experience that helps them deliver on their business goals."

**RFE Tool Intelligence enables backup TAMs to deliver this experience even without months of customer relationship building.**

### **Key Takeaway**

**Backup TAM coverage is no longer a liability - it's an opportunity to demonstrate the depth of Red Hat's commitment to customer success.**

---

**Next Steps:**
1. Try: `tam-rfe-active-case-report --help`
2. Review: `docs/ACTIVE-CASE-REPORT-CUSTOMIZATION.md`
3. Configure: `tam-rfe-report-scheduler` (add backup TAM to CC)

**Questions?** See `docs/PRODUCT-SPECIFIC-FORM-TEMPLATES.md` for backup TAM use cases.

