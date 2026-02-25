# 🔐 Taminator - Authentication-First Workflow

**Critical Insight:** Nothing works without authentication tokens!

**Current Problem:** App shows all features immediately, but they all fail without auth configured.

---

## 🎯 What Requires Authentication?

### ✅ **JIRA Token** (REQUIRED for most features)
**Used by:**
- ✅ **Verify (Check) Tab** - Fetches current JIRA status
- ✅ **Update Tab** - Fetches latest JIRA data to update reports
- ✅ **Onboard (Discovery)** - Searches for existing RFEs/Bugs

**Without it:**
- ❌ Can't check report status
- ❌ Can't update reports
- ❌ Can't discover customer issues

---

### ✅ **Portal Token** (REQUIRED for posting)
**Used by:**
- ✅ **Post Tab** - Posts reports to Red Hat Customer Portal

**Without it:**
- ❌ Can't publish reports to customer portal

---

### ⚠️ **Optional Tokens**
**Hydra API Token:**
- Used for advanced customer discovery
- Not required for basic operations

**SupportShell Token:**
- Used for case integration
- Not required for RFE/Bug tracking

---

## 🚫 What DOESN'T Work Without Auth?

| Feature | Requires | Will Fail Without |
|---------|----------|-------------------|
| **Verify Report** | JIRA token | ✅ Yes |
| **Update Report** | JIRA token | ✅ Yes |
| **Post Report** | Portal token | ✅ Yes |
| **Onboard (Discover)** | JIRA token | ✅ Yes |
| **Dashboard** | N/A | ⚠️ Shows demo data anyway |
| **Settings** | N/A | ❌ No (local only) |
| **Navigation** | N/A | ❌ No (UI only) |

**Bottom Line:** 4 out of 5 main features require authentication!

---

## ✅ Proper Workflow (What Should Happen)

### **Step 1: First Launch - Detect No Auth**
```
User launches Taminator
  ↓
App checks for tokens
  ↓
No tokens found
  ↓
Show Setup Wizard
```

### **Step 2: Setup Authentication**
```
Setup Wizard:
1. "Welcome to Taminator!"
2. "Let's configure authentication"
3. Option A: Use HashiCorp Vault (recommended)
4. Option B: Configure tokens directly
5. Test connection
6. ✅ Auth validated
```

### **Step 3: Configure Customer Data**
```
After auth is validated:
1. "Great! Authentication works"
2. "Now let's add your first customer"
3. Onboard customer flow
4. Ready to use!
```

### **Step 4: Normal Operation**
```
Subsequent launches:
1. Check auth on startup
2. If valid → show dashboard
3. If expired → prompt to re-auth
4. If missing → back to setup wizard
```

---

## 🚨 Current Problem (v1.9.5)

### What Happens Now:
```
User launches Taminator
  ↓
Shows full dashboard immediately
  ↓
User tries to check report
  ↓
❌ Error: "JIRA authentication failed"
  ↓
User confused: "What auth? Where?"
```

### Why This Is Bad:
1. ❌ **No guidance** - User doesn't know auth is required
2. ❌ **Late failure** - Error only shows after trying to use feature
3. ❌ **Poor UX** - User has to figure out where to configure auth
4. ❌ **No validation** - Can configure wrong/invalid tokens

---

## ✅ Better Approach (v1.10.0 Proposal)

### First-Run Setup Wizard

#### Screen 1: Welcome
```
╔══════════════════════════════════════════════╗
║                                              ║
║          🎯 Welcome to Taminator!           ║
║                                              ║
║   TAM Workflow Automation for RFEs & Bugs   ║
║                                              ║
║  Before we start, let's set up              ║
║  authentication so you can:                 ║
║                                              ║
║  ✅ Check JIRA status                       ║
║  ✅ Update RFE/Bug trackers                 ║
║  ✅ Post reports to customer portal         ║
║                                              ║
║         [Let's Get Started →]               ║
║                                              ║
╚══════════════════════════════════════════════╝
```

#### Screen 2: Auth Method
```
╔══════════════════════════════════════════════╗
║                                              ║
║      Choose Authentication Method           ║
║                                              ║
║  ┌─────────────────────────────────────┐   ║
║  │ 🔒 HashiCorp Vault (Recommended)    │   ║
║  │                                      │   ║
║  │ ✅ Centralized token management     │   ║
║  │ ✅ Team sharing                     │   ║
║  │ ✅ Secure storage                   │   ║
║  │                                      │   ║
║  │      [Use Vault →]                  │   ║
║  └─────────────────────────────────────┘   ║
║                                              ║
║  ┌─────────────────────────────────────┐   ║
║  │ 📝 Manual Configuration              │   ║
║  │                                      │   ║
║  │ For testing or personal use          │   ║
║  │                                      │   ║
║  │      [Configure Manually →]         │   ║
║  └─────────────────────────────────────┘   ║
║                                              ║
╚══════════════════════════════════════════════╝
```

#### Screen 3: Configure Tokens
```
╔══════════════════════════════════════════════╗
║                                              ║
║         Configure JIRA Token                ║
║                                              ║
║  JIRA API Token: [___________________]      ║
║                                              ║
║  ℹ️  Get your token from:                   ║
║     https://issues.redhat.com               ║
║     → Profile → Personal Access Tokens      ║
║                                              ║
║  [Test Connection] [Next →]                 ║
║                                              ║
║  Status: ⏳ Not tested yet                  ║
║                                              ║
╚══════════════════════════════════════════════╝
```

#### Screen 4: Validation
```
╔══════════════════════════════════════════════╗
║                                              ║
║        Testing Authentication...            ║
║                                              ║
║  ✅ JIRA: Connected                         ║
║  ✅ Portal: Connected                       ║
║                                              ║
║  Great! You're all set up.                  ║
║                                              ║
║  [Start Using Taminator →]                  ║
║                                              ║
╚══════════════════════════════════════════════╝
```

---

## 🎯 Auth Check on Every Launch

### Startup Sequence (v1.10.0 Proposal)
```javascript
// On app launch
async function onAppReady() {
  const authStatus = await checkAuthentication();
  
  if (authStatus.hasValidTokens) {
    // All good - show dashboard
    showDashboard();
  } else if (authStatus.hasExpiredTokens) {
    // Tokens exist but expired
    showAuthRefreshPrompt();
  } else {
    // No tokens at all
    showFirstRunWizard();
  }
}
```

---

## 📋 Auth Requirements by Feature

### Minimum Required (Can't use app without):
```
✅ JIRA Token
   - REQUIRED for: Check, Update, Onboard
   - Can't do anything without this!
```

### Recommended (For full functionality):
```
✅ JIRA Token (required)
✅ Portal Token (for posting reports)
```

### Optional (Advanced features):
```
⚠️ Hydra Token (enhanced discovery)
⚠️ SupportShell Token (case integration)
```

---

## 🔧 Implementation Plan (v1.10.0)

### Phase 1: Detection
1. Add `checkAuthOnStartup()` function
2. Detect if tokens exist
3. Validate tokens are not expired
4. Decide which screen to show

### Phase 2: First-Run Wizard
1. Create wizard component
2. Step-by-step auth setup
3. Connection testing
4. Success confirmation

### Phase 3: Auth Validation
1. Test tokens before showing dashboard
2. Show clear errors if tokens invalid
3. Offer to reconfigure

### Phase 4: Graceful Degradation
1. If no Portal token → disable Post tab
2. If no JIRA token → show auth prompt on all tabs
3. Clear messaging about what's missing

---

## 📝 Error Messages (Before vs After)

### Current (v1.9.5) - BAD
```
User clicks "Check Report"
❌ Error: Authentication failed

(User confused: What auth? Where?)
```

### Proposed (v1.10.0) - GOOD
```
User clicks "Check Report"

╔══════════════════════════════════════════════╗
║  ⚠️  Authentication Required                 ║
║                                              ║
║  To check reports, you need a JIRA token.   ║
║                                              ║
║  [Configure Authentication →]               ║
║  [Learn More]                               ║
╚══════════════════════════════════════════════╝
```

---

## 🎯 User Journey (Correct Flow)

### First-Time User
```
1. Launch Taminator
   ↓
2. See welcome wizard
   ↓
3. Configure JIRA token
   ↓
4. Configure Portal token (optional)
   ↓
5. Test connection
   ↓
6. ✅ Success! Dashboard shown
   ↓
7. Now can onboard customers
   ↓
8. Now can check/update reports
```

### Returning User (Valid Auth)
```
1. Launch Taminator
   ↓
2. Check auth on startup
   ↓
3. ✅ Valid → Dashboard shown
   ↓
4. Ready to work
```

### Returning User (Expired Auth)
```
1. Launch Taminator
   ↓
2. Check auth on startup
   ↓
3. ⚠️ Expired → Prompt to refresh
   ↓
4. Re-enter tokens or reconnect Vault
   ↓
5. ✅ Validated → Dashboard shown
```

---

## 📊 Comparison

| Aspect | Current (v1.9.5) | Proposed (v1.10.0) |
|--------|------------------|-------------------|
| **First launch** | Shows all features | Shows setup wizard |
| **Auth detection** | ❌ None | ✅ Automatic |
| **Auth validation** | ⚠️ On first use | ✅ On startup |
| **Error guidance** | ❌ Generic error | ✅ Clear steps |
| **User knows what's needed** | ❌ No | ✅ Yes |
| **Can use without auth** | ⚠️ No (fails) | ❌ No (blocked) |

---

## 🚀 Quick Win for v1.9.6

### Minimal Auth Detection (30 min implementation)
```javascript
// Add to showDashboard()
document.getElementById('content').innerHTML = `
  ${!hasJiraToken() ? `
    <div style="padding: 16px; background: #FFF4E5; border-left: 4px solid #F0AB00; border-radius: 4px; margin-bottom: 24px;">
      <h3 style="color: #151515; margin: 0 0 8px 0;">⚠️ Authentication Required</h3>
      <p style="margin: 0 0 12px 0;">
        Most features require a JIRA token. Configure authentication to get started.
      </p>
      <button class="btn btn-primary" onclick="showVault()">
        🔒 Configure Authentication →
      </button>
    </div>
  ` : ''}
  
  <!-- rest of dashboard -->
`;
```

**Result:** At least warns users on dashboard!

---

## 🎯 Recommendations

### For v1.9.6 (Emergency Fix - 1 hour)
1. ✅ Add auth warning to dashboard
2. ✅ Add auth check before operations
3. ✅ Show clear error: "Configure JIRA token first"
4. ✅ Link to Vault tab from errors

### For v1.10.0 (Proper Solution - 1 day)
1. ✅ Full first-run setup wizard
2. ✅ Auth validation on startup
3. ✅ Graceful degradation
4. ✅ Clear error messages with guidance

---

## 📚 Documentation Needed

### For Users:
1. **Getting Started Guide**
   - Step 1: Get your JIRA token
   - Step 2: Configure in Taminator
   - Step 3: Add your first customer

2. **Token Setup Guide**
   - Where to get JIRA token
   - Where to get Portal token
   - How to configure Vault

3. **Troubleshooting**
   - "Authentication failed" → Check token
   - "Connection refused" → Check VPN
   - "Token expired" → Refresh token

---

## 🎯 Bottom Line

**You're absolutely right:** Nothing works without auth tokens!

**Current state (v1.9.5):** App lets users try features, then fails with confusing errors

**What we need (v1.10.0):** 
- Auth-first workflow
- First-run setup wizard
- Validation before showing features
- Clear guidance when auth missing

**Quick win (v1.9.6):**
- Add auth warning to dashboard
- Check auth before operations
- Link to Vault tab from errors

---

**Priority:** 🔴 **HIGH** - This is a fundamental UX issue

**Effort:** 
- Quick fix (warning): 1 hour
- Full solution (wizard): 1 day

**User Impact:** 
- Current: Confusing, frustrating
- After fix: Clear, guided, professional

---

## 🔄 Factory Reset / Return to OOBE

### What Users Need
**"Start Over" / "Factory Reset" button** that returns to Out-of-Box Experience (OOBE)

### Use Cases
1. **Testing** - Developers testing first-run experience
2. **Misconfiguration** - User messed up auth and wants to start fresh
3. **Multiple Users** - Switching between users/environments
4. **Training** - Demonstrating setup process
5. **Troubleshooting** - "Have you tried starting over?"

---

## 🎯 Factory Reset Behavior

### What Gets Cleared
```
✅ GUI Settings
   - ~/.config/taminator-gui/settings.json
   - Auto-update preferences
   - UI preferences
   
✅ Session Data
   - localStorage cleared
   - sessionStorage cleared
   - Vault connection cache
   
✅ Auth Tokens (Optional - User Choice)
   - Option 1: Keep tokens (just reset UI)
   - Option 2: Clear tokens from Vault
   - Default: Keep tokens (safer)
```

### What Gets KEPT (User Data)
```
❌ DO NOT CLEAR:
   - Customer configurations (~/.config/taminator/customers/)
   - Generated reports (~/Documents/rh/)
   - RFE/Bug trackers
   - Vault tokens (unless user specifically chooses)
```

---

## 🔧 Implementation

### Settings Tab - Factory Reset Section

```
╔══════════════════════════════════════════════╗
║              ⚙️ Settings                     ║
╚══════════════════════════════════════════════╝

... existing settings ...

╔══════════════════════════════════════════════╗
║         🔄 Advanced Options                  ║
╚══════════════════════════════════════════════╝

┌────────────────────────────────────────────┐
│ Factory Reset                              │
│                                            │
│ Return to first-run setup wizard          │
│                                            │
│ ⚠️ This will:                              │
│ • Clear all GUI settings                   │
│ • Clear session data                       │
│ • Return to welcome screen                 │
│                                            │
│ ✅ Will NOT affect:                        │
│ • Customer data                            │
│ • Generated reports                        │
│ • Vault tokens (unless you choose)        │
│                                            │
│ [🔄 Factory Reset...]                     │
└────────────────────────────────────────────┘
```

---

## ⚠️ Confirmation Dialog

### First Confirmation
```
╔══════════════════════════════════════════════╗
║     🔄 Factory Reset Confirmation           ║
╚══════════════════════════════════════════════╝

Are you sure you want to reset Taminator to
first-run setup?

This will clear:
✅ GUI settings and preferences
✅ Session data and cache
✅ Return to welcome wizard

This will NOT clear:
❌ Customer data
❌ Generated reports
❌ Vault tokens

What about authentication tokens?

○ Keep my tokens (recommended)
   I'll skip the auth setup wizard
   
○ Clear tokens too (start completely fresh)
   I'll reconfigure authentication

[Cancel]  [Continue →]
```

### Second Confirmation (if clearing tokens)
```
╔══════════════════════════════════════════════╗
║     ⚠️ Clear Tokens? (Final Warning)        ║
╚══════════════════════════════════════════════╝

You chose to clear authentication tokens.

This means you'll need to:
1. Reconfigure JIRA token
2. Reconfigure Portal token
3. Go through auth setup again

Are you SURE you want to clear tokens?

[No, Keep Tokens]  [Yes, Clear Everything]
```

---

## 🔧 Implementation Code

### Factory Reset Function
```javascript
async function factoryReset(options = {}) {
  const { clearTokens = false } = options;
  
  // 1. Clear GUI settings
  localStorage.clear();
  sessionStorage.clear();
  
  // 2. Clear settings file
  const fs = require('fs');
  const settingsFile = path.join(
    os.homedir(), 
    '.config/taminator-gui/settings.json'
  );
  if (fs.existsSync(settingsFile)) {
    fs.unlinkSync(settingsFile);
  }
  
  // 3. Clear tokens if requested
  if (clearTokens) {
    await clearAllTokens();
  }
  
  // 4. Set flag to show OOBE on restart
  localStorage.setItem('showOOBE', 'true');
  
  // 5. Reload app
  window.location.reload();
}

async function clearAllTokens() {
  try {
    // Clear from Vault if connected
    if (process.env.VAULT_ADDR && process.env.VAULT_TOKEN) {
      await ipcRenderer.invoke('clear-vault-tokens');
    }
    
    // Clear local token cache (if any)
    const tokensFile = path.join(
      os.homedir(), 
      '.config/taminator-gui/tokens.json'
    );
    if (fs.existsSync(tokensFile)) {
      fs.unlinkSync(tokensFile);
    }
  } catch (error) {
    console.error('Error clearing tokens:', error);
  }
}
```

### Check for OOBE Flag on Startup
```javascript
// In loadSavedSettingsOnStartup()
async function loadSavedSettingsOnStartup() {
  // Check if factory reset was requested
  const showOOBE = localStorage.getItem('showOOBE');
  
  if (showOOBE === 'true') {
    // Clear the flag
    localStorage.removeItem('showOOBE');
    
    // Show OOBE wizard
    showFirstRunWizard();
    return; // Don't proceed with normal startup
  }
  
  // Normal startup...
  const settings = await window.api.invoke('load-settings');
  // ... rest of existing code
}
```

---

## 🎯 Factory Reset Button Location

### Option 1: Settings Tab (Recommended)
```
Settings Tab
  → General Settings
  → Report Settings
  → Advanced Settings
  → ⚠️ Danger Zone
     → Factory Reset
```

**Pros:**
- Logical location (advanced settings)
- Not accidentally clicked
- Follows common UX patterns

---

### Option 2: Help Menu
```
Help Menu (if we add one)
  → Documentation
  → Report Issue
  → About
  → Factory Reset
```

**Pros:**
- Separated from normal settings
- Help/troubleshooting context

---

## 📋 Reset Levels (Future Enhancement)

### Level 1: Soft Reset (UI Only)
```
Clears: GUI settings, cache
Keeps: Tokens, customer data
Time: 1 second
```

### Level 2: Auth Reset (Recommended Default)
```
Clears: GUI settings, cache, returns to OOBE
Keeps: Tokens (skip auth wizard), customer data
Time: 2 seconds
```

### Level 3: Full Reset (Nuclear Option)
```
Clears: Everything except customer data/reports
Result: Complete fresh start
Time: 3 seconds
```

### Level 4: Complete Wipe (Support Only)
```
Clears: EVERYTHING including customer data
⚠️ Requires typing "DELETE EVERYTHING"
Time: 5 seconds
```

---

## 🧪 Testing Factory Reset

### Test Cases
1. ✅ Factory reset clears settings
2. ✅ Factory reset shows OOBE on next launch
3. ✅ Factory reset with "keep tokens" skips auth wizard
4. ✅ Factory reset with "clear tokens" shows auth wizard
5. ✅ Customer data remains after reset
6. ✅ Reports remain after reset
7. ✅ Cancel button works (no reset)
8. ✅ Can use app normally after reset

---

## 🎨 UI Design

### Settings Tab Addition
```html
<div class="card" style="margin-top: 24px; border-left: 4px solid #C9190B;">
  <div class="card-title" style="color: #C9190B;">
    ⚠️ Danger Zone
  </div>
  <div class="card-content">
    <div style="margin-bottom: 16px;">
      <h4 style="margin: 0 0 8px 0;">Factory Reset</h4>
      <p style="color: #6A6E73; margin: 0 0 12px 0;">
        Return to first-run setup wizard. Your customer data 
        and reports will NOT be affected.
      </p>
      <button class="btn" 
              style="background: #C9190B; color: white;"
              onclick="showFactoryResetDialog()">
        🔄 Factory Reset...
      </button>
    </div>
  </div>
</div>
```

---

## 📝 User Documentation

### When to Use Factory Reset

**Use Factory Reset When:**
- ✅ Testing first-run experience
- ✅ Auth is completely broken
- ✅ Settings are corrupted
- ✅ Switching users/environments
- ✅ Want to start fresh with setup

**DON'T Use Factory Reset When:**
- ❌ Just want to change one setting (use Settings tab)
- ❌ Just want to update tokens (use Vault tab)
- ❌ Want to remove a customer (use customer management)

---

## 🚀 Implementation Priority

### v1.9.6 (Quick Win - 2 hours)
```
✅ Add "Reset All" button in Settings
✅ Clear localStorage/sessionStorage
✅ Reload app
✅ Basic confirmation dialog
```

### v1.10.0 (Proper OOBE - 1 day)
```
✅ First-run wizard
✅ Factory reset to OOBE
✅ "Keep tokens" vs "Clear tokens" option
✅ Multiple confirmation dialogs
✅ Skip auth wizard if tokens kept
```

---

## 🎯 Comparison

| Aspect | Current "Reset All" | Enhanced Factory Reset |
|--------|---------------------|------------------------|
| **Clears settings** | ✅ Yes | ✅ Yes |
| **Returns to OOBE** | ❌ No | ✅ Yes |
| **Token options** | ❌ Always keeps | ✅ User choice |
| **Confirmation** | ⚠️ Basic | ✅ Multiple |
| **Keeps customer data** | ✅ Yes | ✅ Yes |
| **Testing friendly** | ⚠️ OK | ✅ Great |

---

## 📊 Reset Statistics (For Future Analytics)

Track how often users reset:
```javascript
// Optional: Track reset usage
{
  timestamp: "2025-10-23T13:00:00Z",
  resetType: "factory_reset",
  tokensCleared: false,
  reason: "testing", // user-provided
  timeSinceLastReset: "5 days"
}
```

**Use cases:**
- Users resetting frequently → UX problem
- Users clearing tokens → Auth confusion
- Users resetting after errors → Bug tracking

---

## 💡 Quick Recovery Codes (Future)

### Recovery Code System
```
User clicks Factory Reset
  ↓
System generates recovery code: 
  "TAMIN-2025-A3F9"
  ↓
Code saved to: ~/Documents/taminator-recovery-2025-10-23.txt
  ↓
Contains:
  - Settings snapshot
  - Token references (not actual tokens!)
  - Customer list
  - Restore instructions
```

**Benefit:** Can restore settings without reconfiguring everything

---

*"Factory reset: The ultimate 'try turning it off and on again'"* 🔄


