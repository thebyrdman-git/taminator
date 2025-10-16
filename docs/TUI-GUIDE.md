# TUI Guide - RFE Tools

**Interface:** Menu-driven Text User Interface  
**Purpose:** Simplify routine TAM workflows

---

## Quick Start

```bash
# Launch TUI
tam-rfe-tui

# Or use the shortcut
tam-rfe
```

**Tip:** Install `dialog` for better UI:
```bash
sudo dnf install dialog
```

---

## Main Menu

```
╔════════════════════════════════════════════════════════════╗
║                  RFE Tools Control Panel                   ║
╠════════════════════════════════════════════════════════════╣
║  [1] Customer Management                                   ║
║  [2] Case Intelligence                                     ║
║  [3] Report Scheduler                                      ║
║  [4] Customer Discovery                                    ║
║  [5] System Status                                         ║
║  [6] Advanced (CLI Mode)                                   ║
╚════════════════════════════════════════════════════════════╝
```

---

## Features

### 1. Customer Management

**Intelligent Onboarding:**
- Enter account number or name
- System discovers details automatically
- Selects products based on case history
- Configures both customers.conf and tamscripts.config

**Manual Onboarding:**
- Step-by-step prompts
- Full control over configuration

**View & Validate:**
- List all configured customers
- Check configuration sync
- Remove customers

---

### 2. Case Intelligence

**View Cases:**
- All cases (table view)
- By customer (filtered)
- Sev 1 only (priority)

**Natural Language Query:**
- Type queries in plain English
- "Show Westpac OpenShift cases from last month"
- "Find all Sev 1 cases"

**Similarity Search:**
- Find cases similar to a given case number
- Based on SBR group analysis

---

### 3. Report Scheduler

**Schedule Wizard:**
- Step 1: Name your schedule
- Step 2: Select report type
  - Customer case summary
  - Sev 1 alert
  - Portfolio overview
  - Custom command
- Step 3: Choose customer
- Step 4: Set frequency
  - Daily (9am)
  - Weekly (Monday 8am)
  - Hourly
  - Custom cron
- Step 5: Delivery method
  - Email (plain, HTML digest, executive brief)
  - Slack webhook

**Management:**
- List all schedules
- Run manually
- Remove schedules
- View execution logs

**Daemon Control:**
- Start/stop/restart
- Check status
- Monitor activity

---

### 4. Customer Discovery

**By Region:**
- APAC
- EMEA
- NAMER
- LATAM

**By Organization:**
- NAPS (North American Public Sector)
- Commercial

**Search:**
- Find customers by name
- View portfolio summary

---

### 5. System Status

**Configuration Check:**
- rhcase authentication
- customers.conf (configured customers)
- tamscripts.config (sync status)
- Scheduler daemon (running/stopped)

**Performance:**
- Average query times
- Cache statistics
- Recent activity

**Validation:**
- Run full system validation
- Clear caches
- View logs

---

### 6. Advanced (CLI Mode)

Drop to command-line interface for:
- Complex natural language queries
- Scripting and automation
- Advanced features
- Pipeline integration

**Type `exit` to return to TUI.**

---

## Common Workflows

### Onboard a New Customer

1. Launch TUI: `tam-rfe`
2. Select **[1] Customer Management**
3. Select **[1] Onboard New Customer (Intelligent)**
4. Enter account number or name
5. Confirm discovered details
6. Select products to track
7. Done! Configuration synced automatically

---

### View Customer Cases

1. Launch TUI: `tam-rfe`
2. Select **[2] Case Intelligence**
3. Select **[2] View Cases by Customer**
4. Choose customer
5. Cases displayed in table format

---

### Schedule a Weekly Report

1. Launch TUI: `tam-rfe`
2. Select **[3] Report Scheduler**
3. Select **[1] Add New Schedule (Wizard)**
4. Enter name (e.g., "Westpac Weekly")
5. Select **[1] Customer case summary**
6. Choose customer (e.g., Westpac)
7. Select **[2] Weekly (Monday 8am)**
8. Enter email and select template
9. Confirm creation
10. Select **[7] Daemon Control** → **[1] Start Daemon**

---

### Discover Customers by Region

1. Launch TUI: `tam-rfe`
2. Select **[4] Customer Discovery**
3. Select **[1] Discover by Region**
4. Choose region (e.g., APAC)
5. View customer list with activity metrics

---

## Tips & Tricks

### Navigation
- **Numbers:** Select menu options
- **B:** Back to previous menu
- **Q:** Quit (from main menu)
- **Arrow keys:** Navigate (if using dialog)

### Fallback Mode
If `dialog` is not installed:
- Basic text menus still work
- All functionality available
- Type numbers to select options

### CLI Integration
Mix TUI and CLI freely:
```bash
# Use TUI for onboarding
tam-rfe  # Select Customer Management

# Use CLI for queries
tam-rfe-chat "Show all Sev 1 cases"

# Use CLI for automation
tam-rfe-schedule list
```

### Keyboard Shortcuts
When in dialog mode:
- **Tab:** Move between buttons
- **Space:** Toggle checkboxes
- **Enter:** Confirm selection
- **Esc:** Cancel/Back

---

## Troubleshooting

### "dialog not found"
Install dialog for better UI:
```bash
sudo dnf install dialog
```
TUI still works without it (basic text mode).

### Tools not found
Ensure RFE tools are installed:
```bash
cd rfe-and-bug-tracker-automation
./install.sh
```

### Scheduler not working
1. Check daemon status: **System Status** → **Show Full Status**
2. Start daemon: **Report Scheduler** → **Daemon Control** → **Start**
3. View logs: **Report Scheduler** → **View Logs**

### Kerberos ticket expired
```bash
kinit jbyrd@REDHAT.COM
```
Then return to TUI.

---

## Comparison: TUI vs CLI

| Task | TUI | CLI |
|------|-----|-----|
| **Onboard customer** | Guided wizard (3 steps) | Manual prompts (10+ inputs) |
| **View cases** | Menu → Customer → Table | Remember command syntax |
| **Schedule report** | Wizard (5 steps) | Long command with flags |
| **Complex query** | Natural language box | Natural language (faster) |
| **Automation** | Not applicable | Full scripting support |
| **Learning curve** | Low (menus guide you) | Medium (learn commands) |

**Use TUI for:** Routine tasks, learning, visual workflows  
**Use CLI for:** Advanced queries, scripting, speed (experienced users)

---

## Examples

### Example Session

```
$ tam-rfe

[Main Menu appears]
Select: 1 (Customer Management)

[Customer Management Menu]
Current Customers:
  westpac    Westpac Banking Corp  1363155
  alma       Alma                  397076

Select: 1 (Onboard New Customer - Intelligent)

Enter account number: 1234567
🔍 Searching...

✅ Found: Acme Corporation
   Account: 1234567
   Geo: NAMER
   Products detected:
   [✓] OpenShift (15 cases)
   [✓] Ansible (8 cases)

Configuration Complete!
✅ Added to customers.conf
✅ Added to tamscripts.config
✅ rhcase access verified

[Press Enter]

[Back to Customer Management]
Select: B (Back)

[Main Menu]
Select: 2 (Case Intelligence)

[Case Intelligence Menu]
Select: 2 (View Cases by Customer)

Select customer:
  1. westpac
  2. alma
  3. acme  ← NEW

Select: 3

[Cases displayed in table]
Case #    Sev  Product    Status   Summary
03729481  2    OpenShift  Waiting  Pod crash...
03728941  3    Ansible    Working  Playbook...

[Press Enter]

[Back to menus...]
Select: Q (Quit)

$
```

---

## Summary

**TUI = Guided workflows for routine tasks**  
**CLI = Full power for advanced users**  
**Both = Best of both worlds**

Launch: `tam-rfe` or `tam-rfe-tui`

---

*TUI Guide - Sys Admin Style*  
*Menu-driven. Efficient. Still has CLI.*
