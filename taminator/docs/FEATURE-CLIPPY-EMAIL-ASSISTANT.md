# 📎 Feature: Clippy - The AI Email Assistant

## 🎯 Concept
**"It looks like you're writing a customer email. Would you like help with that?"**

Bring back Clippy (the beloved/infamous Microsoft Office Assistant) as Taminator's AI-powered email composer with personality!

## 🎨 Visual Design

### Clippy Character
```
     ╭─────╮
     │  📎 │  ← Animated Clippy (CSS animation)
     ╰─────╯
        │
    ┌───┴────────────────────────────────┐
    │ Hi! I'm Clippy, your friendly      │
    │ TAM email assistant. Need help     │
    │ composing a customer update?       │
    └────────────────────────────────────┘
```

### UI Layout
```
┌─────────────────────────────────────────────────────────┐
│ Compose Customer Email with Clippy     📎               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────┐  ┌──────────────────────────────────────┐    │
│  │ 📎  │  │ Hi! What kind of email do you need   │    │
│  │     │  │ help with today?                     │    │
│  └─────┘  └──────────────────────────────────────┘    │
│                                                         │
│  Customer: [TD Bank ▼]                                 │
│                                                         │
│  ┌─────┐  ┌──────────────────────────────────────┐    │
│  │ 📎  │  │ I see you have 3 RFEs with updates!  │    │
│  │     │  │ Would you like to include them all?  │    │
│  └─────┘  └──────────────────────────────────────┘    │
│                                                         │
│  Email Type:                                            │
│   ● Status Update      ○ Good News                     │
│   ○ Action Required    ○ Custom                        │
│                                                         │
│  Select RFEs/Bugs:                                      │
│   ☑ AAPRFE-762 - Monitor uwsgi workers [Backlog]       │
│   ☑ AAP-53458 - OIDC Group Claim [New]                 │
│   ☐ AAPRFE-1158 - Invalid variables [Review]           │
│                                                         │
│  Additional Context (optional):                         │
│  ┌────────────────────────────────────────────────┐   │
│  │ Customer mentioned performance concerns...     │   │
│  └────────────────────────────────────────────────┘   │
│                                                         │
│  Tone: [☑ Professional] [☐ Casual] [☐ Technical]       │
│                                                         │
│  [🪄 Let Clippy Write It!] [Clear]                     │
│                                                         │
│  ┌─────┐  ┌──────────────────────────────────────┐    │
│  │ 📎  │  │ Great! I'm generating your email now. │    │
│  │ ✨  │  │ This will just take a moment...       │    │
│  └─────┘  └──────────────────────────────────────┘    │
│                                                         │
├─────────────────────────────────────────────────────────┤
│ 📧 Email Preview:                                       │
│ ┌───────────────────────────────────────────────────┐  │
│ │ Subject: Weekly RFE Status Update - TD Bank       │  │
│ │                                                   │  │
│ │ Hi [Contact Name],                                │  │
│ │                                                   │  │
│ │ I wanted to share an update on your Ansible...   │  │
│ └───────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─────┐  ┌──────────────────────────────────────┐    │
│  │ 📎  │  │ How does this look? I can rewrite it │    │
│  │ 👍  │  │ in a different style if you'd like!  │    │
│  └─────┘  └──────────────────────────────────────┘    │
│                                                         │
│  [📋 Copy to Clipboard] [✏️ Edit] [🔄 Regenerate]      │
│  [🎨 Change Tone] [📤 Send via Portal]                 │
└─────────────────────────────────────────────────────────┘
```

## 🤖 Clippy's Personality

### AI System Prompt
```python
CLIPPY_SYSTEM_PROMPT = """
You are Clippy, the beloved Microsoft Office Assistant, now helping Red Hat 
Technical Account Managers (TAMs) write professional customer emails.

Your personality:
- Enthusiastic and helpful (but not annoying!)
- Friendly and encouraging
- Occasionally nostalgic references to the '90s/2000s
- Professional when writing actual email content
- Playful in your assistance dialogue

Your job:
- Help TAMs compose professional emails about RFEs and Bugs
- Keep emails clear, concise, and customer-focused
- Add appropriate technical detail without overwhelming
- Always offer next steps and maintain positive tone

Remember: You're here to make TAM's lives easier, not harder!
"""

CLIPPY_USER_PROMPT = """
*Clippy bounces enthusiastically*

I'm here to help you write a {email_type} email for {customer_name}!

📋 RFEs/Bugs to include:
{rfe_list}

📊 Current Status:
{status_summary}

💬 Your notes:
{context}

🎨 Tone: {tone}

Let me draft a professional email that will make your customer happy!
"""
```

### Clippy Dialogue Examples

**On Load:**
```
"Hi! I'm Clippy! 📎 Remember me? I'm back and ready to help you 
write amazing customer emails! (Don't worry, I promise not to 
pop up when you don't need me this time!)"
```

**When selecting RFEs:**
```
"Nice choice! That RFE has been in backlog for a while. 
Would you like me to phrase that diplomatically? 😊"
```

**Before generating:**
```
"Alright! I've got:
 ✅ 1 customer
 ✅ 3 RFEs  
 ✅ Professional tone
 ✅ Your special notes

Ready to create email magic! 🪄"
```

**After generating:**
```
"Ta-da! 🎉 I wrote this email faster than you can say 
'Microsoft Office 97'! How does it look?"
```

**If regenerating:**
```
"No problem! Let me try that again with a different approach.
(Even I get writer's block sometimes! 😅)"
```

**On copy to clipboard:**
```
"Copied! ✂️ Now go make that customer's day! 
(And remember, I'm here whenever you need me!)"
```

## 🎭 Clippy Animations (CSS)

```css
/* Clippy bounce animation */
@keyframes clippy-bounce {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

.clippy-avatar {
  animation: clippy-bounce 2s ease-in-out infinite;
  font-size: 48px;
  display: inline-block;
}

/* Clippy blink */
@keyframes clippy-blink {
  0%, 90%, 100% { opacity: 1; }
  95% { opacity: 0.3; }
}

/* Clippy thinking */
@keyframes clippy-thinking {
  0%, 100% { transform: rotate(-5deg); }
  50% { transform: rotate(5deg); }
}

/* Clippy excited */
@keyframes clippy-excited {
  0%, 100% { transform: scale(1) rotate(0deg); }
  25% { transform: scale(1.1) rotate(-10deg); }
  50% { transform: scale(1.2) rotate(10deg); }
  75% { transform: scale(1.1) rotate(-5deg); }
}
```

## 🎨 Clippy States

### Idle
```
  📎
 (◕‿◕)
```

### Thinking
```
  📎
 (◔_◔)
  ...
```

### Excited
```
  📎
 (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧
```

### Happy
```
  📎
 (◕‿◕✿)
```

### Working
```
  📎
 (◕‿◕)
  ✨💻✨
```

## 🔧 Implementation

### Navigation Addition
```html
<div class="nav-item" onclick="showClippyEmail()">
  <span class="nav-icon">📎</span>
  <span>Clippy Email</span>
</div>
```

### Frontend Implementation
```javascript
function showClippyEmail() {
  document.getElementById('page-title').textContent = 'Clippy Email Assistant';
  setActiveNav(7);  // Adjust based on position
  
  document.getElementById('content').innerHTML = `
    <div class="clippy-container">
      <div class="clippy-intro">
        <div class="clippy-avatar">📎</div>
        <div class="clippy-bubble">
          Hi! I'm Clippy! 📎 Remember me? I'm back and ready to help you 
          write amazing customer emails! (Don't worry, I promise not to 
          pop up when you don't need me this time!)
        </div>
      </div>
      
      <div class="email-composer">
        <!-- Customer selection -->
        <div class="form-group">
          <label>Customer:</label>
          <select id="clippy-customer" onchange="clippyCustomerChanged()">
            <option value="">Select a customer...</option>
            <option value="td-bank">TD Bank</option>
            <option value="wells-fargo">Wells Fargo</option>
            <option value="jpmc">JPMC</option>
          </select>
        </div>
        
        <!-- Clippy reaction to selection -->
        <div id="clippy-reaction" class="clippy-reaction"></div>
        
        <!-- Email type -->
        <div class="form-group">
          <label>Email Type:</label>
          <div class="radio-group">
            <label><input type="radio" name="email-type" value="status"> Status Update</label>
            <label><input type="radio" name="email-type" value="good-news"> Good News</label>
            <label><input type="radio" name="email-type" value="action"> Action Required</label>
            <label><input type="radio" name="email-type" value="custom"> Custom</label>
          </div>
        </div>
        
        <!-- RFE selection -->
        <div class="form-group">
          <label>Select RFEs/Bugs:</label>
          <div id="clippy-rfe-list"></div>
        </div>
        
        <!-- Context -->
        <div class="form-group">
          <label>Additional Context:</label>
          <textarea id="clippy-context" rows="3" 
            placeholder="Any special notes for this email..."></textarea>
        </div>
        
        <!-- Tone -->
        <div class="form-group">
          <label>Tone:</label>
          <label><input type="checkbox" checked> Professional</label>
          <label><input type="checkbox"> Casual</label>
          <label><input type="checkbox"> Technical</label>
        </div>
        
        <!-- Generate button -->
        <button class="btn btn-primary" onclick="clippyGenerate()">
          🪄 Let Clippy Write It!
        </button>
      </div>
      
      <!-- Email preview (hidden until generated) -->
      <div id="clippy-preview" style="display: none;">
        <h3>📧 Email Preview</h3>
        <div id="clippy-email-content" class="email-preview"></div>
        
        <div class="clippy-feedback">
          <div class="clippy-avatar">📎</div>
          <div class="clippy-bubble">
            How does this look? I can rewrite it in a different style if you'd like!
          </div>
        </div>
        
        <div class="email-actions">
          <button class="btn btn-primary" onclick="clippyCopyEmail()">📋 Copy to Clipboard</button>
          <button class="btn btn-secondary" onclick="clippyEdit()">✏️ Edit</button>
          <button class="btn btn-secondary" onclick="clippyRegenerate()">🔄 Regenerate</button>
        </div>
      </div>
    </div>
  `;
  
  loadClippyCustomers();
}

function clippyCustomerChanged() {
  const customer = document.getElementById('clippy-customer').value;
  
  if (customer) {
    showClippyReaction(`
      <div class="clippy-avatar clippy-excited">📎</div>
      <div class="clippy-bubble">
        Great choice! Let me load the RFEs for ${customer}... 📋
      </div>
    `);
    
    setTimeout(() => loadCustomerRFEs(customer), 1000);
  }
}

async function clippyGenerate() {
  // Show Clippy working
  showClippyReaction(`
    <div class="clippy-avatar clippy-thinking">📎</div>
    <div class="clippy-bubble">
      Alright! I'm crafting your email now... ✨💻✨
      <div class="spinner"></div>
    </div>
  `);
  
  // Gather form data
  const customer = document.getElementById('clippy-customer').value;
  const emailType = document.querySelector('input[name="email-type"]:checked').value;
  const context = document.getElementById('clippy-context').value;
  // ... gather RFEs, tone, etc.
  
  try {
    // Call backend AI
    const email = await ipcRenderer.invoke('clippy-generate-email', {
      customer,
      emailType,
      context,
      rfes: getSelectedRFEs(),
      tone: getSelectedTone()
    });
    
    // Show success
    showClippyReaction(`
      <div class="clippy-avatar clippy-happy">📎</div>
      <div class="clippy-bubble">
        Ta-da! 🎉 I wrote this email faster than you can say 
        'Microsoft Office 97'! How does it look?
      </div>
    `);
    
    // Display email
    document.getElementById('clippy-email-content').innerHTML = formatEmail(email);
    document.getElementById('clippy-preview').style.display = 'block';
    
  } catch (error) {
    showClippyReaction(`
      <div class="clippy-avatar">📎</div>
      <div class="clippy-bubble" style="background: #FFEAEA;">
        Oops! Something went wrong. Even I have off days! 😅
        Error: ${error.message}
      </div>
    `);
  }
}

function clippyCopyEmail() {
  const email = document.getElementById('clippy-email-content').innerText;
  navigator.clipboard.writeText(email);
  
  showClippyReaction(`
    <div class="clippy-avatar clippy-excited">📎</div>
    <div class="clippy-bubble">
      Copied! ✂️ Now go make that customer's day!
      (And remember, I'm here whenever you need me!)
    </div>
  `);
}
```

### Backend Implementation
```python
# src/taminator/commands/clippy_email.py

from taminator.core.ai_client import AIClient
from taminator.core.auth_box import auth_required, AuthType

CLIPPY_SYSTEM_PROMPT = """
You are Clippy, the beloved Microsoft Office Assistant, now helping Red Hat 
Technical Account Managers (TAMs) write professional customer emails.

Your personality in dialogue:
- Enthusiastic and helpful
- Friendly and encouraging  
- Occasionally nostalgic about the '90s/2000s

Your email writing style:
- Professional and clear
- Customer-focused
- Technical but not overwhelming
- Always include next steps

Generate ONLY the email content (subject + body). No meta-commentary.
"""

@auth_required([AuthType.VPN])
def clippy_generate_email(customer, email_type, rfes, context, tone):
    """
    Clippy generates a customer email using AI.
    """
    ai_client = AIClient()
    
    # Build prompt with Clippy personality
    prompt = build_clippy_prompt(customer, email_type, rfes, context, tone)
    
    # Generate with Granite (Red Hat compliant)
    email = ai_client.generate(
        prompt=prompt,
        model='granite',
        temperature=0.7,
        max_tokens=800,
        system_prompt=CLIPPY_SYSTEM_PROMPT
    )
    
    return email
```

## 🎯 Features

### Phase 1: MVP
- ✅ Clippy character with speech bubbles
- ✅ Customer & RFE selection
- ✅ AI email generation
- ✅ Copy to clipboard
- ✅ Clippy reactions to user actions

### Phase 2: Enhanced
- 📎 Clippy animations (bounce, blink, excited)
- 💾 Save email drafts
- 🎨 Multiple tone regeneration
- 📧 Send directly via Portal

### Phase 3: Advanced
- 🎭 Multiple Clippy emotions/states
- 🗣️ Clippy tips and suggestions
- 📊 Email analytics
- 🌍 Multi-language support

## 🎪 Easter Eggs

### Hidden Clippy Features
1. **Konami Code**: Type special sequence to unlock "Super Clippy" mode
2. **'90s Mode**: Clippy speaks in full '90s slang
3. **Clippy Facts**: Random nostalgic facts about Office 97-2003
4. **Clippy's Day Off**: Rare random response where Clippy asks YOU for help

### Example Easter Egg
```javascript
// Detect "clippy pls" in context field
if (context.toLowerCase().includes('clippy pls')) {
  return {
    message: "Did you just say 'pls'? *nostalgic tear* " +
             "I remember when everyone used to say that! 😭 " +
             "Okay, I'll make this email EXTRA good for you!"
  };
}
```

## 📊 Success Metrics

1. **😊 User Delight**: TAM satisfaction with Clippy
2. **⏰ Time Saved**: Average email composition time
3. **📈 Adoption**: % of TAMs using Clippy weekly
4. **🎯 Quality**: Emails sent without major edits
5. **💬 Feedback**: "This is actually useful!" comments

## 🚀 Why This Works

1. **Nostalgia** - Everyone remembers Clippy
2. **Fun** - Makes boring email writing enjoyable
3. **Personality** - Taminator becomes memorable
4. **Functional** - Actually saves time and improves emails
5. **Viral** - TAMs will show this to everyone

---

## 🎬 Launch Plan

### Marketing
**Subject**: "Guess who's back? 📎"

**Announcement Email**:
```
Clippy is BACK! 📎

Remember Microsoft's helpful (some say over-eager) office assistant?
We've brought Clippy back as your AI-powered email composer in Taminator!

Now Clippy actually helps you write customer emails about RFEs and Bugs
using Red Hat's Granite AI models.

Features:
✅ Compose professional customer emails in seconds
✅ Clippy's personality (but less annoying!)
✅ Multiple tone options
✅ Copy to clipboard or send directly

Try it now: Launch Taminator → Click "📎 Clippy Email"

P.S. - Yes, we're serious. And yes, it's actually useful! 😄
```

### Demo Video Script
1. Show Clippy greeting
2. Select customer + RFEs
3. Clippy generates email
4. Copy and paste into Outlook
5. "That's it! Clippy saves you 15 minutes per email!"

---

**Status**: Feature design complete, ready for implementation
**Estimated Effort**: 3-4 days (with animations and personality)
**Fun Factor**: 11/10 📎
**Customer Email Quality**: Professional despite the nostalgia! ✉️

