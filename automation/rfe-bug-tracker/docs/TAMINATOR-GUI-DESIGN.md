# Taminator GUI - Design Specification

**Date:** October 21, 2025  
**Component:** Taminator GUI Application  
**Branding:** Taminator (primary) with Red Hat design elements (secondary)  
**Platforms:** macOS, Windows, Linux

---

## Branding Strategy

### Primary Brand: TAMINATOR
- **Logo:** User-selected Taminator logo (top priority in UI)
- **Name:** "Taminator" or "Taminator RFE Tool"
- **Identity:** TAM automation tool with personality
- **Positioning:** Professional TAM productivity tool

### Secondary: Red Hat Design Elements
- **Color Scheme:** Red Hat colors (Red #EE0000, Black #000000, White #FFFFFF)
- **Typography:** Red Hat Display, Red Hat Text (official fonts)
- **Design System:** Based on PatternFly (Red Hat's design system)
- **Compliance:** Follows Red Hat brand guidelines where appropriate

### Visual Hierarchy
```
┌─────────────────────────────────────────┐
│ [TAMINATOR LOGO] Taminator             │ ← Primary brand
│ RFE & Bug Tracking Tool for TAMs       │
│                                         │
│ Powered by Red Hat                      │ ← Secondary attribution
└─────────────────────────────────────────┘
```

---

## Technology Stack

### Recommended: Electron + React
**Why:**
- ✅ True cross-platform (Mac, Windows, Linux)
- ✅ Modern, elegant UI capabilities
- ✅ Excellent Red Hat PatternFly React components
- ✅ Large ecosystem and community
- ✅ Easy distribution (single executable per platform)
- ✅ Access to Node.js for CLI tool integration

**Stack:**
```
Frontend:  React + PatternFly React (Red Hat's design system)
Backend:   Electron (Node.js)
CLI Bridge: Spawn tam-rfe commands from Node.js
Packaging: electron-builder (DMG for Mac, EXE for Windows, AppImage for Linux)
State:     React Context or Redux
Styling:   PatternFly CSS + custom Taminator theme
```

---

## Application Architecture

### CLI + GUI Hybrid Approach
```
┌─────────────────────────────────────────────────────┐
│                  Taminator GUI                      │
│  (Electron + React + PatternFly)                    │
│                                                     │
│  ┌──────────────────┐    ┌──────────────────┐    │
│  │  Dashboard       │    │  Auth-Box        │    │
│  │  Component       │    │  Component       │    │
│  └────────┬─────────┘    └────────┬─────────┘    │
│           │                       │              │
│           └───────────┬───────────┘              │
│                       │                          │
│              ┌────────▼────────┐                 │
│              │   CLI Bridge    │                 │
│              │ (spawn tam-rfe) │                 │
│              └────────┬────────┘                 │
└───────────────────────┼──────────────────────────┘
                        │
            ┌───────────▼───────────┐
            │   tam-rfe CLI Tools   │
            │  (Python + Rich)      │
            └───────────────────────┘
```

**Benefits:**
- GUI and CLI share the same backend logic
- No code duplication
- GUI is essentially a beautiful wrapper around CLI
- Both stay in sync automatically

---

## Main Application Window

### Layout Structure
```
┌─────────────────────────────────────────────────────────────┐
│ [🤖 TAMINATOR LOGO]  Taminator RFE Tool        [⚙️] [−][□][×] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ ┌───────────┐  ┌───────────────────────────────────────┐  │
│ │           │  │                                       │  │
│ │ 🏠 Home   │  │          Main Content Area            │  │
│ │           │  │                                       │  │
│ │ ✅ Check  │  │   (Dashboard, Check Results,          │  │
│ │           │  │    Auth Status, Settings, etc.)       │  │
│ │ 🔄 Update │  │                                       │  │
│ │           │  │                                       │  │
│ │ 📤 Post   │  │                                       │  │
│ │           │  │                                       │  │
│ │ ➕ Onboard│  │                                       │  │
│ │           │  │                                       │  │
│ │ 🔐 Auth   │  │                                       │  │
│ │           │  │                                       │  │
│ │ ⚙️ Config │  │                                       │  │
│ │           │  │                                       │  │
│ └───────────┘  └───────────────────────────────────────┘  │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ ✅ All authentication OK  |  Last check: 2 mins ago         │
└─────────────────────────────────────────────────────────────┘
```

---

## Screen Designs

### 1. Dashboard (Home Screen)

```
╔═══════════════════════════════════════════════════════════╗
║  [🤖] Taminator                                            ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  👋 Welcome, Jimmy                                        ║
║                                                           ║
║  ┌─────────────────┐  ┌─────────────────┐              ║
║  │ 📊 Customers    │  │ 🔐 Auth Status  │              ║
║  │                 │  │                 │              ║
║  │ TD Bank      ✅ │  │ JIRA Token   ✅ │              ║
║  │ Wells Fargo  ⚠️  │  │ Portal       ⚠️  │              ║
║  │ JPMC         ✅ │  │ VPN          ✅ │              ║
║  │ Fannie Mae   ✅ │  │ Kerberos     ✅ │              ║
║  │                 │  │                 │              ║
║  │ [+ Add Customer]│  │ [Run Audit]     │              ║
║  └─────────────────┘  └─────────────────┘              ║
║                                                           ║
║  ┌────────────────────────────────────────────────────┐  ║
║  │ 📝 Recent Activity                                 │  ║
║  │                                                    │  ║
║  │ ✅ Checked TD Bank report (2 hours ago)           │  ║
║  │ ✅ Updated Wells Fargo report (1 day ago)         │  ║
║  │ ⚠️  Portal token expires in 2 days                │  ║
║  │                                                    │  ║
║  └────────────────────────────────────────────────────┘  ║
║                                                           ║
║  Quick Actions:                                           ║
║  [Check All Reports] [Run Auth Audit] [View Settings]    ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

### 2. Check Report Screen

```
╔═══════════════════════════════════════════════════════════╗
║  [🤖] Taminator › Check Report                            ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Customer: [TD Bank ▼]         [Check Now]               ║
║                                                           ║
║  Status: ⚠️ Report needs update (3 statuses changed)     ║
║                                                           ║
║  ┌────────────────────────────────────────────────────┐  ║
║  │ JIRA ID     │ Report Status │ Current  │ Match    │  ║
║  ├────────────────────────────────────────────────────┤  ║
║  │ AAPRFE-762  │ Backlog      │ Progress │ ✗ Changed│  ║
║  │ AAPRFE-430  │ Backlog      │ Backlog  │ ✓ Match  │  ║
║  │ AAPRFE-1158 │ Review       │ Closed   │ ✗ Changed│  ║
║  │ AAPRFE-873  │ Backlog      │ Backlog  │ ✓ Match  │  ║
║  │ AAPRFE-1207 │ Backlog      │ Backlog  │ ✓ Match  │  ║
║  │ AAPRFE-1257 │ Backlog      │ Backlog  │ ✓ Match  │  ║
║  │ AAPRFE-650  │ Closed       │ Closed   │ ✓ Match  │  ║
║  │ AAP-53458   │ New          │ Progress │ ✗ Changed│  ║
║  │ AAP-45405   │ Closed       │ Closed   │ ✓ Match  │  ║
║  └────────────────────────────────────────────────────┘  ║
║                                                           ║
║  Summary: 6/9 match (67%)                                 ║
║                                                           ║
║  [View Diff] [Update Report] [Export]                    ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

### 3. Auth-Box Status Screen

```
╔═══════════════════════════════════════════════════════════╗
║  [🤖] Taminator › Authentication                          ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Overall Status: ⚠️ 2 warnings, 1 error                  ║
║                                                           ║
║  [Run Full Audit]                                         ║
║                                                           ║
║  🔑 API Tokens                                            ║
║  ┌────────────────────────────────────────────────────┐  ║
║  │ JIRA Token           ✅ Valid (87 days)             │  ║
║  │ Portal Token         ⚠️  Valid (2 days) - EXPIRING  │  ║
║  │ Hydra Token          ✅ Valid                       │  ║
║  │ SupportShell Token   ❌ NOT CONFIGURED              │  ║
║  │                                                    │  ║
║  │ [Manage Tokens]                                    │  ║
║  └────────────────────────────────────────────────────┘  ║
║                                                           ║
║  🌐 Network & Connectivity                                ║
║  ┌────────────────────────────────────────────────────┐  ║
║  │ Red Hat VPN          ✅ Connected (24ms)            │  ║
║  │ JIRA (issues.r.com)  ✅ Reachable (18ms)            │  ║
║  │ Hydra API            ✅ Reachable (31ms)            │  ║
║  │                                                    │  ║
║  │ [Test Connectivity]                                │  ║
║  └────────────────────────────────────────────────────┘  ║
║                                                           ║
║  🎫 Kerberos                                              ║
║  ┌────────────────────────────────────────────────────┐  ║
║  │ Ticket Status        ✅ Valid (9 hours left)        │  ║
║  │ Principal            jbyrd@IPA.REDHAT.COM          │  ║
║  │                                                    │  ║
║  │ [Renew Ticket]                                     │  ║
║  └────────────────────────────────────────────────────┘  ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

### 4. Onboarding Wizard

```
╔═══════════════════════════════════════════════════════════╗
║  [🤖] Taminator › Onboarding                              ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Step 2 of 5: JIRA API Token                             ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                  ║
║  ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░ 40%              ║
║                                                           ║
║  Why This Is Needed:                                      ║
║  Query Red Hat JIRA for RFE/Bug statuses.                ║
║                                                           ║
║  How To Get This Token:                                   ║
║   1. Go to issues.redhat.com/secure/ViewProfile.jspa     ║
║   2. Click "Personal Access Tokens" tab                   ║
║   3. Click "Create token"                                 ║
║   4. Copy the token                                       ║
║                                                           ║
║  [Open JIRA in Browser]                                   ║
║                                                           ║
║  Enter JIRA API Token:                                    ║
║  ┌────────────────────────────────────────────────────┐  ║
║  │ ••••••••••••••••••••••••••••••••••••••••••••       │  ║
║  └────────────────────────────────────────────────────┘  ║
║                                                           ║
║  ⏳ Validating token...                                   ║
║  ✅ Token valid! Connected as jbyrd@redhat.com            ║
║                                                           ║
║  [< Back]                    [Skip]          [Next >]     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

## Color Scheme & Theme

### Taminator Theme (Red Hat-Inspired)

```css
/* Primary Colors (Taminator + Red Hat) */
--taminator-primary: #EE0000;        /* Red Hat Red */
--taminator-dark: #000000;           /* Black */
--taminator-light: #FFFFFF;          /* White */
--taminator-accent: #0066CC;         /* Blue for links/actions */

/* Status Colors */
--success: #3E8635;                  /* Green */
--warning: #F0AB00;                  /* Yellow/Gold */
--error: #C9190B;                    /* Red */
--info: #2B9AF3;                     /* Blue */

/* UI Colors */
--background: #F5F5F5;               /* Light gray background */
--surface: #FFFFFF;                  /* Card/panel background */
--border: #D2D2D2;                   /* Borders */
--text-primary: #151515;             /* Primary text */
--text-secondary: #6A6E73;           /* Secondary text */

/* Sidebar */
--sidebar-bg: #212427;               /* Dark sidebar */
--sidebar-text: #FFFFFF;
--sidebar-hover: #292E34;
--sidebar-active: #EE0000;           /* Red Hat Red for active item */
```

### Typography

```css
/* Red Hat Official Fonts */
@font-face {
  font-family: 'Red Hat Display';
  src: url('fonts/RedHatDisplay-*.woff2');
}

@font-face {
  font-family: 'Red Hat Text';
  src: url('fonts/RedHatText-*.woff2');
}

/* Usage */
h1, h2, h3 {
  font-family: 'Red Hat Display', sans-serif;
  font-weight: 700;
}

body, p, span {
  font-family: 'Red Hat Text', sans-serif;
  font-weight: 400;
}

code, pre {
  font-family: 'Red Hat Mono', 'Courier New', monospace;
}
```

---

## Feature Parity: CLI vs GUI

### Complete Feature Matrix

| Feature | CLI | GUI | Notes |
|---------|-----|-----|-------|
| **Check Reports** |
| Check single customer | ✅ `tam-rfe check` | ✅ Check screen | Full parity |
| Check all customers | ✅ `--all` | ✅ Checkbox "All" | Full parity |
| View diff | ✅ `--diff` | ✅ "View Diff" button | Visual diff in GUI |
| Export results | ✅ `--format json` | ✅ "Export" button | GUI adds PDF export |
| **Update Reports** |
| Update report | ✅ `tam-rfe update` | ✅ "Update Report" button | GUI shows preview |
| Backup before update | ✅ Auto | ✅ Auto + show location | GUI more visual |
| **Authentication** |
| Add token | ✅ `tam-rfe config --add-token` | ✅ "Add Token" form | GUI has wizard |
| Renew token | ✅ `--renew-token` | ✅ "Renew" button | GUI opens browser |
| Auth audit | ✅ `tam-rfe auth-audit` | ✅ Auth screen | GUI shows live status |
| **Onboarding** |
| Onboard customer | ✅ `tam-rfe onboard` | ✅ Onboarding wizard | GUI more interactive |
| Test customer | ✅ Flag option | ✅ Checkbox option | Full parity |
| **Settings** |
| Configure | ✅ `tam-rfe config` | ✅ Settings screen | GUI has forms |
| View config | ✅ `--show` | ✅ Settings screen | Full parity |
| **Extra GUI Features** |
| Dashboard | ❌ N/A | ✅ Home screen | GUI-only |
| Real-time status | ❌ N/A | ✅ Status bar | GUI-only |
| Notifications | ❌ Email only | ✅ Desktop notifications | GUI advantage |
| Drag & drop | ❌ N/A | ✅ Import reports | GUI-only |

---

## Implementation Plan

### Phase 1: Core GUI (Week 1-2)
- [ ] Set up Electron + React + PatternFly project
- [ ] Implement Taminator branding (logo, colors, fonts)
- [ ] Create main window layout
- [ ] Build dashboard screen
- [ ] Implement CLI bridge (spawn tam-rfe commands)

### Phase 2: Feature Screens (Week 3-4)
- [ ] Check report screen
- [ ] Auth-Box status screen
- [ ] Onboarding wizard
- [ ] Settings screen

### Phase 3: Polish & Distribution (Week 5-6)
- [ ] Notifications system
- [ ] Error handling
- [ ] Loading states
- [ ] Package for macOS (DMG)
- [ ] Package for Windows (EXE installer)
- [ ] Package for Linux (AppImage)

### Phase 4: Testing & Refinement (Week 7)
- [ ] User testing with TAMs
- [ ] Performance optimization
- [ ] Accessibility compliance
- [ ] Documentation

---

## Distribution

### Installation Packages

**macOS:**
```
Taminator-1.0.0.dmg
- Drag-and-drop installation
- Code signed (if Apple Developer account)
- Notarized (for Gatekeeper)
```

**Windows:**
```
Taminator-Setup-1.0.0.exe
- Standard Windows installer
- Adds to Start Menu
- Desktop shortcut option
- Uninstaller included
```

**Linux:**
```
Taminator-1.0.0.AppImage
- Single executable file
- No installation required
- Runs on most distros
```

### Auto-Updates
```javascript
// Electron auto-updater
const { autoUpdater } = require('electron-updater');

autoUpdater.checkForUpdatesAndNotify();
```

---

## Success Criteria

### GUI Must Be:
- ✅ Elegant: Beautiful, modern design
- ✅ State-of-the-art: Latest UI patterns
- ✅ Branded: Taminator logo prominent, Red Hat elements secondary
- ✅ Cross-platform: Works on Mac, Windows, Linux
- ✅ Feature parity: Everything CLI can do
- ✅ Intuitive: TAMs can use without training
- ✅ Professional: Suitable for customer demonstrations

### Performance:
- ✅ Launches in < 2 seconds
- ✅ Responsive UI (no freezing)
- ✅ Small package size (< 200MB)

### User Experience:
- ✅ One-click actions for common tasks
- ✅ Real-time status updates
- ✅ Desktop notifications
- ✅ Beautiful error messages (not cryptic)

---

## Next Steps

1. **Get Taminator logo** from you
2. **Set up Electron + React project**
3. **Implement dashboard screen first** (most visible)
4. **Test with you** for feedback
5. **Iterate on design** based on your input
6. **Build remaining screens**
7. **Package for distribution**

**Bottom Line:** GUI provides elegant, state-of-the-art interface with Taminator branding, complete feature parity with CLI, and cross-platform support for Mac/Windows/Linux users.

