# Feature: AI-Powered Customer Email Composer

## 🎯 Purpose
Help TAMs compose professional customer emails about RFE/Bug updates using AI assistance.

## 👤 User Story
**As a TAM**, I want AI to help me compose customer-facing emails so that I can:
- Save time writing professional updates
- Maintain consistent tone and quality
- Focus on customer relationships, not email formatting
- Ensure all relevant technical details are included

## 🎨 UI Design

### Location
New navigation item: **"Compose Email"** (✉️ icon)

### Layout
```
┌─────────────────────────────────────────────────────┐
│ Compose Customer Email                              │
├─────────────────────────────────────────────────────┤
│                                                     │
│ Customer: [TD Bank ▼]                              │
│                                                     │
│ Email Type:                                         │
│  ○ Status Update (weekly/monthly summary)          │
│  ○ Specific RFE/Bug Update                         │
│  ○ Action Required (customer needs to provide info)│
│  ○ Good News (RFE completed, bug fixed)            │
│  ○ Custom                                           │
│                                                     │
│ Select RFEs/Bugs to Include:                        │
│  ☑ AAPRFE-762 - Monitor uwsgi workers              │
│  ☑ AAP-53458 - OIDC Group Claim issue              │
│  ☐ AAPRFE-1158 - Invalid variable names            │
│                                                     │
│ Additional Context (optional):                      │
│ ┌───────────────────────────────────────────────┐ │
│ │ Customer mentioned performance concerns       │ │
│ │ during last call...                           │ │
│ └───────────────────────────────────────────────┘ │
│                                                     │
│ Tone: [Professional ▼] [Formal/Casual/Technical]   │
│                                                     │
│ [Generate Email Draft] [Clear]                      │
│                                                     │
├─────────────────────────────────────────────────────┤
│ Generated Email Preview:                            │
│ ┌───────────────────────────────────────────────┐ │
│ │ Subject: Weekly RFE Status Update - TD Bank   │ │
│ │                                               │ │
│ │ Hi [Contact Name],                            │ │
│ │                                               │ │
│ │ I wanted to share an update on the RFEs...   │ │
│ │ ...                                           │ │
│ └───────────────────────────────────────────────┘ │
│                                                     │
│ [Copy to Clipboard] [Edit] [Regenerate] [Send via Portal]│
└─────────────────────────────────────────────────────┘
```

## 🤖 AI Integration

### Model Selection (Priority Order)
1. **Red Hat Granite** (via pai-litellm-proxy) - For customer data
2. **Local LLM** (Ollama) - If available
3. **Fallback Template** - No AI, use smart templates

### Prompt Engineering
```python
SYSTEM_PROMPT = """
You are a helpful assistant for Red Hat Technical Account Managers (TAMs).
Your role is to help compose professional, customer-facing emails about 
RFE (Request for Enhancement) and Bug updates.

Guidelines:
- Professional but warm tone
- Focus on customer value and impact
- Technical accuracy without jargon overload
- Action items clearly stated
- Always offer next steps or follow-up options
"""

USER_PROMPT = """
Compose a {email_type} email for {customer_name}.

RFEs/Bugs to include:
{rfe_bug_list}

Current Status Summary:
{status_summary}

Additional Context:
{context}

Tone: {tone}

Generate a professional email with:
- Clear subject line
- Appropriate greeting
- Brief introduction
- RFE/Bug status updates with impact
- Next steps or action items
- Closing with offer to discuss
"""
```

## 🔧 Implementation

### Backend (Python)
```python
# automation/rfe-bug-tracker/src/taminator/commands/email_compose.py

from taminator.core.ai_client import AIClient
from taminator.core.auth_box import auth_required, AuthType

@auth_required([AuthType.VPN])
def compose_email(customer, rfes, email_type, context, tone):
    """
    Generate AI-powered customer email draft.
    """
    ai_client = AIClient()  # Connects to pai-litellm-proxy
    
    # Build prompt
    prompt = build_email_prompt(customer, rfes, email_type, context, tone)
    
    # Generate email
    draft = ai_client.generate(
        prompt=prompt,
        model='granite',  # Red Hat compliant for customer data
        temperature=0.7,
        max_tokens=800
    )
    
    return draft
```

### Frontend (Electron/React)
```javascript
// gui/index.html - Add new view

async function showEmailCompose() {
  // Fetch customer list and their RFEs
  const customers = await ipcRenderer.invoke('get-customers');
  
  // Render email composer UI
  document.getElementById('content').innerHTML = renderEmailComposer(customers);
}

async function generateEmailDraft() {
  const customer = document.getElementById('customer-select').value;
  const emailType = document.querySelector('input[name="email-type"]:checked').value;
  const selectedRfes = getSelectedRfes();
  const context = document.getElementById('context-text').value;
  const tone = document.getElementById('tone-select').value;
  
  // Show loading state
  document.getElementById('email-preview').innerHTML = '<div class="spinner"></div>';
  
  // Call backend
  const draft = await ipcRenderer.invoke('compose-email', {
    customer,
    emailType,
    rfes: selectedRfes,
    context,
    tone
  });
  
  // Display draft
  document.getElementById('email-preview').innerHTML = formatEmailPreview(draft);
}
```

## 📋 Features

### Must Have (MVP)
- ✅ Customer selection dropdown
- ✅ Email type selection (Status Update, Specific RFE, etc.)
- ✅ RFE/Bug multi-select checkboxes
- ✅ AI-generated email draft
- ✅ Copy to clipboard button
- ✅ Professional tone by default

### Nice to Have
- 📝 Edit generated email inline
- 🔄 Regenerate with different tone
- 💾 Save drafts
- 📧 Send directly via Portal API
- 📊 Include charts/graphs in email
- 🌍 Multi-language support
- 🎨 Email templates library
- 📅 Schedule send

## 🔐 Security & Compliance

### Red Hat AI Policy
- ✅ Customer data → Red Hat Granite models ONLY
- ✅ No external APIs for customer information
- ✅ Audit logging for all AI generations
- ✅ No customer data stored in AI service logs

### Data Flow
```
Customer Data → Taminator → pai-litellm-proxy → Granite Model
                    ↓
              Audit Log (local)
```

## 🧪 Testing Strategy

### Manual Testing (TAM with GUI)
1. Select customer and RFEs
2. Choose email type
3. Add context
4. Generate draft
5. Verify tone, accuracy, completeness
6. Copy and paste into Outlook/Gmail

### Simulated Testing (Automated)
1. Unit tests for prompt generation
2. Mock AI responses
3. Template fallback testing
4. Edge cases (no RFEs, very long context)

## 📊 Success Metrics

1. **Time Saved**: Average email composition time reduction
2. **Adoption**: % of TAMs using the feature weekly
3. **Quality**: Customer satisfaction with email communication
4. **Accuracy**: % of emails sent without manual edits

## 🚀 Rollout Plan

### Phase 1: MVP (2-3 days)
- Basic email composer UI
- AI integration with Granite
- Copy to clipboard
- Template fallback (no AI required)

### Phase 2: Enhanced (1 week)
- Inline editing
- Multiple tone options
- Save drafts
- Email templates library

### Phase 3: Advanced (2 weeks)
- Portal integration (send directly)
- Schedule send
- Multi-language support
- Analytics dashboard

## 💡 Example Use Cases

### Use Case 1: Weekly Status Update
**Input:**
- Customer: TD Bank
- Type: Status Update
- RFEs: 3 selected (1 in progress, 2 backlog)
- Context: "Customer concerned about timeline"

**Generated Email:**
```
Subject: Weekly RFE Status Update - TD Bank

Hi [Contact],

I wanted to share a quick update on your Red Hat Ansible Automation 
Platform enhancement requests.

**In Progress:**
• AAPRFE-762: Monitor uwsgi workers - Engineering is actively working 
  on this. Expected completion in Q4 2025.

**In Backlog:**
• AAPRFE-430: Mesh node awareness - Prioritized for Q1 2026
• AAPRFE-1158: Invalid variable handling - Under review

I understand timeline is a concern. Would you like to schedule a call 
this week to discuss priorities and potential workarounds?

Best regards,
[Your Name]
Red Hat Technical Account Manager
```

### Use Case 2: Good News Email
**Input:**
- Customer: Wells Fargo
- Type: Good News
- RFE: AAPRFE-650 (Closed)
- Context: "Customer requested this 6 months ago"

**Generated Email:**
```
Subject: Great News: Your RFE is Now Available!

Hi [Contact],

I have some exciting news! The enhancement you requested 6 months ago
is now available in Ansible Automation Platform 2.6.

**AAPRFE-650: Folder Hierarchy in Templates**
This feature is now live in AAP 2.6, allowing you to organize your
job templates in a hierarchical folder structure - exactly as you
envisioned.

Would you like help planning an upgrade or testing this feature in 
your environment?

Looking forward to hearing your feedback!

Best regards,
[Your Name]
```

## 🎓 Training for TAMs

### Quick Start Guide
1. Navigate to "Compose Email"
2. Select customer and RFEs
3. Choose email type
4. Add any special context
5. Click "Generate Email Draft"
6. Review, edit if needed, copy to clipboard
7. Paste into your email client

### Best Practices
- Always review AI-generated content before sending
- Add personal touch (customer-specific references)
- Verify technical accuracy
- Use "Additional Context" for customer-specific details
- Save time, don't sacrifice quality

---

**Feature Request Source:** TAM colleague feedback during live demo
**Priority:** High - Direct customer communication impact
**Estimated Effort:** 2-3 days for MVP
**Red Hat AI Policy:** Compliant (uses Granite for customer data)

