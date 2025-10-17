# Product-Specific Google Form Templates

## Quick Links (Create Your Own)

### How to Create Pre-Filled Forms

1. **Open the master form**
2. Click "⋮" (three dots) menu → "Get pre-filled link"
3. Fill in the default values you want
4. Click "Get link"
5. Share that link with TAMs

---

## Template 1: RHEL-Focused TAM 🐧

**Best for:** Infrastructure TAMs, government sector, traditional IT

**Pre-filled Selections:**

**Priority Products:**
- ☑ Red Hat Enterprise Linux (RHEL)
- ☑ Red Hat Satellite
- ☑ Red Hat Insights

**Report Template:** Comprehensive

**Report Frequency:** Weekly

**Report Day:** Monday

**Alert Preferences:**
- ☑ Cases age beyond 30 days
- ☑ No updates in 7 days
- ☑ SLA breach risk detected

**Customer Vertical:** Government/Public Sector

**Use Cases:**
- Traditional server infrastructure
- Patch management and compliance
- System stability and security

---

## Template 2: OpenShift-Focused TAM ☸️

**Best for:** Container platform TAMs, cloud-native customers, DevOps

**Pre-filled Selections:**

**Priority Products:**
- ☑ OpenShift Container Platform
- ☑ Advanced Cluster Management
- ☑ OpenShift Data Foundation
- ☑ Red Hat Enterprise Linux (RHEL)

**Report Template:** Priority-focused

**Report Frequency:** Daily

**Report Time:** 08:00 EST

**Alert Preferences:**
- ☑ New high-priority cases are opened
- ☑ Cases age beyond 30 days
- ☑ SLA breach risk detected
- ☑ Case volume spikes above normal

**Alert Delivery:**
- ☑ Email
- ☑ Slack

**Customer Vertical:** Technology

**Use Cases:**
- Container orchestration
- Cloud-native applications
- Microservices architecture
- CI/CD pipelines

---

## Template 3: Ansible-Focused TAM 🤖

**Best for:** Automation TAMs, DevOps teams, infrastructure as code

**Pre-filled Selections:**

**Priority Products:**
- ☑ Ansible Automation Platform
- ☑ Red Hat Enterprise Linux (RHEL)

**Report Template:** Executive

**Report Frequency:** Weekly

**Report Day:** Friday

**Alert Preferences:**
- ☑ New high-priority cases are opened
- ☑ Cases age beyond 30 days

**Customer Vertical:** Financial Services

**Use Cases:**
- IT automation
- Configuration management
- Workflow orchestration
- Integration with existing tools

---

## Template 4: Middleware-Focused TAM ☕

**Best for:** Application platform TAMs, Java developers, integration specialists

**Pre-filled Selections:**

**Priority Products:**
- ☑ JBoss Enterprise Application Platform
- ☑ Red Hat AMQ
- ☑ Red Hat Fuse
- ☑ Red Hat Enterprise Linux (RHEL)

**Report Template:** Comprehensive

**Report Frequency:** Weekly

**Report Day:** Wednesday

**Alert Preferences:**
- ☑ New high-priority cases are opened
- ☑ Cases age beyond 30 days
- ☑ No updates in 7 days

**Customer Vertical:** Financial Services

**Use Cases:**
- Enterprise Java applications
- Message queuing and streaming
- Integration and API management
- Legacy application modernization

---

## Template 5: Multi-Product TAM 🎯

**Best for:** Strategic account TAMs, large enterprises, complex environments

**Pre-filled Selections:**

**Priority Products:**
- ☑ Red Hat Enterprise Linux (RHEL)
- ☑ OpenShift Container Platform
- ☑ Ansible Automation Platform
- ☑ Red Hat Satellite

**Report Template:** Executive

**Report Frequency:** Weekly

**Report Day:** Monday

**Report Time:** 08:00 EST

**Alert Preferences:**
- ☑ New high-priority cases are opened
- ☑ Cases age beyond 30 days
- ☑ SLA breach risk detected

**Customer Vertical:** Financial Services

**Strategic Account:** Yes

**Use Cases:**
- Full-stack Red Hat deployments
- Hybrid cloud environments
- Enterprise-wide automation
- Multi-product support

---

## Template 6: Virtualization-Focused TAM 💻

**Best for:** Virtualization TAMs, OpenStack, traditional virtualization

**Pre-filled Selections:**

**Priority Products:**
- ☑ Red Hat Virtualization
- ☑ Red Hat OpenStack Platform
- ☑ Red Hat Enterprise Linux (RHEL)

**Report Template:** Comprehensive

**Report Frequency:** Weekly

**Report Day:** Tuesday

**Alert Preferences:**
- ☑ New high-priority cases are opened
- ☑ Cases age beyond 30 days
- ☑ SLA breach risk detected

**Customer Vertical:** Telecommunications

**Use Cases:**
- Virtual machine management
- Private cloud infrastructure
- NFV (Network Functions Virtualization)
- Datacenter consolidation

---

## Template 7: Storage-Focused TAM 💾

**Best for:** Storage specialists, data management, Ceph

**Pre-filled Selections:**

**Priority Products:**
- ☑ OpenShift Data Foundation
- ☑ Red Hat Ceph Storage
- ☑ Red Hat Enterprise Linux (RHEL)

**Report Template:** Comprehensive

**Report Frequency:** Weekly

**Report Day:** Thursday

**Alert Preferences:**
- ☑ New high-priority cases are opened
- ☑ Cases age beyond 30 days
- ☑ No updates in 7 days

**Customer Vertical:** Healthcare

**Use Cases:**
- Software-defined storage
- Object storage
- Block and file storage
- Data lake architecture

---

## Template 8: Security & Compliance TAM 🔒

**Best for:** Security-focused TAMs, regulated industries, compliance

**Pre-filled Selections:**

**Priority Products:**
- ☑ Red Hat Enterprise Linux (RHEL)
- ☑ Red Hat Insights
- ☑ Red Hat Satellite
- ☑ Red Hat Ansible Automation Platform

**Report Template:** Priority-focused

**Report Frequency:** Daily

**Report Time:** 07:00 EST

**Alert Preferences:**
- ☑ New high-priority cases are opened
- ☑ Cases age beyond 30 days
- ☑ No updates in 7 days
- ☑ SLA breach risk detected
- ☑ Case volume spikes above normal

**Alert Delivery:**
- ☑ Email

**Customer Vertical:** Financial Services / Government

**Strategic Account:** Yes

**Use Cases:**
- Security patching and compliance
- Vulnerability management
- Audit reporting
- Policy enforcement

---

## Creating Custom Templates

### Method 1: Via Google Forms UI

1. Open your master onboarding form
2. Click "⋮" → "Get pre-filled link"
3. Select appropriate checkboxes and fill values
4. Click "Get link" at bottom
5. Copy and share the pre-filled link

### Method 2: Via URL Parameters

Base URL:
```
https://docs.google.com/forms/d/e/YOUR_FORM_ID/viewform?usp=pp_url
```

Add parameters:
```
&entry.FIELD_ID=VALUE
```

Example for RHEL-focused:
```
https://docs.google.com/forms/d/e/FORM_ID/viewform?usp=pp_url
&entry.123456=Red+Hat+Enterprise+Linux+(RHEL)
&entry.123456=Red+Hat+Satellite
&entry.234567=Comprehensive
&entry.345678=Weekly
&entry.456789=Monday
```

### Method 3: Automated (Script)

```bash
#!/usr/bin/env python3
# Generate all product-specific form links

templates = {
    'rhel-focused': {
        'products': ['RHEL', 'Satellite', 'Insights'],
        'template': 'Comprehensive',
        'frequency': 'Weekly',
        'vertical': 'Government'
    },
    'openshift-focused': {
        'products': ['OpenShift', 'ACM', 'ODF'],
        'template': 'Priority-focused',
        'frequency': 'Daily',
        'vertical': 'Technology'
    },
    # ... more templates
}

for name, config in templates.items():
    url = generate_prefilled_url(FORM_ID, config)
    print(f"{name}: {url}")
```

---

## Sharing Templates with TAMs

### Internal Wiki/Confluence Page

```markdown
# TAM RFE Automation - Quick Onboarding

Choose your customer type:

- **RHEL Infrastructure?** → [Use this form](https://forms.gle/rhel-XXXXX)
- **OpenShift Platform?** → [Use this form](https://forms.gle/openshift-XXXXX)
- **Ansible Automation?** → [Use this form](https://forms.gle/ansible-XXXXX)
- **Middleware/JBoss?** → [Use this form](https://forms.gle/middleware-XXXXX)
- **Strategic Multi-Product?** → [Use this form](https://forms.gle/multi-XXXXX)

Not sure? Use the [standard form](https://forms.gle/standard-XXXXX)
```

### Email Template

```
Subject: Quick Customer Onboarding - Choose Your Template

Hi TAM Team,

To quickly onboard your customers to RFE automation, use the pre-filled form that matches your customer's primary Red Hat usage:

🐧 RHEL/Infrastructure: https://forms.gle/rhel-XXXXX
☸️ OpenShift/Containers: https://forms.gle/openshift-XXXXX
🤖 Ansible/Automation: https://forms.gle/ansible-XXXXX
☕ Middleware/JBoss: https://forms.gle/middleware-XXXXX
🎯 Multi-Product: https://forms.gle/multi-XXXXX

Each template has smart defaults for that product area - just verify customer details and submit!

Questions? Reply to this email or check the docs:
https://github.com/thebyrdman-git/rfe-bug-tracker-automation/docs/
```

### Slack Message

```
:rocket: Quick customer onboarding now available!

Choose your customer type and use the pre-filled form:

:penguin: RHEL-focused → https://forms.gle/rhel-XXXXX
:kubernetes: OpenShift-focused → https://forms.gle/openshift-XXXXX
:robot: Ansible-focused → https://forms.gle/ansible-XXXXX
:coffee: Middleware-focused → https://forms.gle/middleware-XXXXX
:dart: Multi-product → https://forms.gle/multi-XXXXX

Each template has smart defaults - just add customer details and submit!

Need help? #tam-automation-help
```

---

## Template Maintenance

### Quarterly Review
- Review template usage statistics
- Update based on TAM feedback
- Add new templates for emerging patterns
- Deprecate unused templates

### Analytics to Track
- Which templates are most used?
- Which products are most common?
- What report frequencies are popular?
- Which verticals use which templates?

### Continuous Improvement
- Survey TAMs about template usefulness
- A/B test different defaults
- Add new product combinations
- Optimize for common use cases

---

## Summary

**8 Templates Covering:**
- RHEL/Infrastructure
- OpenShift/Containers
- Ansible/Automation
- Middleware/Integration
- Multi-Product
- Virtualization
- Storage
- Security/Compliance

**Benefits:**
- ✅ Faster onboarding (pre-filled values)
- ✅ Better defaults (product-specific best practices)
- ✅ Fewer errors (appropriate selections)
- ✅ Easier for new TAMs (guided experience)

**Result:** TAMs can onboard customers in under 2 minutes with product-appropriate defaults!

