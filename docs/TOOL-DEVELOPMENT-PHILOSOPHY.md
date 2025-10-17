# Tool Development Philosophy: Build on Giants' Shoulders

**Core Principle:** Focus on business value, not infrastructure plumbing.

---

## The 80/20 Rule

### What We DON'T Build (80% of Code)
❌ Package managers  
❌ Authentication systems  
❌ HTTP servers  
❌ Database engines  
❌ Configuration parsers  
❌ Logging frameworks  
❌ Testing harnesses  
❌ Platform abstraction  

**Instead:** Use proven libraries/tools

### What We DO Build (20% of Code)
✅ Business logic (TAM workflows, customer intelligence)  
✅ Integration glue (connecting proven components)  
✅ User interfaces (CLI, TUI, Web)  
✅ Domain-specific logic (Red Hat case processing)  

**Result:** 5x faster development, 10x fewer bugs

---

## The Foundation Layer

### System Infrastructure → Ansible (Jeff Geerling's Roles)

**Bad:**
```bash
# Custom install script
if [[ "$OS" == "Darwin" ]]; then
  brew install python3
elif [[ "$OS" == "Linux" ]]; then
  if command -v dnf; then
    dnf install python3
  elif command -v apt; then
    apt install python3
  fi
fi
```

**Good:**
```yaml
# Use proven role
- role: geerlingguy.python
```

**Proven Roles for Everything:**
- `geerlingguy.docker` → Container runtime
- `geerlingguy.pip` → Python packages
- `geerlingguy.git` → Git installation
- `geerlingguy.homebrew` → macOS packages
- `geerlingguy.security` → System hardening

### Python Tools → Standard Library First

**Bad:**
```python
# Custom HTTP client
import socket
def fetch_url(url):
    # 200 lines of socket code
```

**Good:**
```python
# Use proven library
import requests
response = requests.get(url)
```

**Proven Python Stack:**
- `requests` → HTTP client (not urllib)
- `rich` → Terminal output (not custom formatting)
- `click` → CLI interface (not argparse)
- `pydantic` → Data validation (not manual checks)
- `pytest` → Testing (not unittest)
- `structlog` → Logging (not logging.basicConfig)

### Shell Scripts → Standard Tools

**Bad:**
```bash
# Custom JSON parser
parse_json() {
  # 50 lines of sed/awk
}
```

**Good:**
```bash
# Use proven tool
jq '.field' file.json
```

**Proven Shell Stack:**
- `jq` → JSON processing
- `yq` → YAML processing
- `fzf` → Interactive selection
- `dialog` → TUI elements
- `ripgrep` → Fast searching

---

## Decision Framework: Build vs. Use

### When to Use Existing Tool ✅

**Criteria:**
1. **Mature:** 3+ years old, active development
2. **Popular:** 1000+ stars OR used by major projects
3. **Maintained:** Commits in last 3 months
4. **Compatible:** Works with your stack (Python 3.8+, RHEL 9+)
5. **Licensed:** MIT/Apache/GPL compatible

**Examples:**
- ✅ Use `requests` for HTTP (12 years, 50k+ stars)
- ✅ Use `rhcase` for case API (Red Hat official)
- ✅ Use `dialog` for TUIs (30+ years, battle-tested)

### When to Build Custom ❌

**Only if ALL true:**
1. No existing tool does what you need
2. Business-specific logic (not general-purpose)
3. Less than 200 lines of code
4. No maintenance burden

**Examples:**
- ✅ Build `tam-rfe-chat` (TAM-specific, glues rhcase + AI)
- ❌ Build custom HTTP client (requests exists)
- ❌ Build custom JSON parser (jq exists)

---

## The "Proven Projects" Checklist

### Before Writing Any Code

**Step 1: Research** (30 minutes)
```bash
# GitHub search
site:github.com "your feature" stars:>1000

# Ansible Galaxy search
ansible-galaxy search "your feature"

# PyPI search
pip search "your feature"
```

**Step 2: Evaluate Top 3 Results**
- ✅ Last commit < 3 months ago?
- ✅ Issues addressed promptly?
- ✅ Good documentation?
- ✅ Used by known projects?

**Step 3: Test Before Committing**
```bash
# Quick proof-of-concept
python3 -m venv /tmp/test-lib
source /tmp/test-lib/bin/activate
pip install candidate-library
# Test 5 minutes
```

**Step 4: Decide**
- **If proven tool works:** Use it, move on
- **If no tool exists:** Build minimal version, revisit later

---

## Architecture Patterns

### Pattern 1: Thin Wrapper (Preferred)

**Concept:** Your tool = thin business logic + proven tools

```python
#!/usr/bin/env python3
"""tam-rfe-search: Search RFE cases (thin wrapper)"""

import click  # Proven: CLI interface
from rhcase import RHCase  # Proven: Red Hat API
from rich import print  # Proven: Pretty output

@click.command()
@click.argument('query')
def search(query: str):
    """Search RFE cases - ALL LOGIC IN 10 LINES"""
    client = RHCase()  # Authentication handled
    cases = client.search(query)  # API handled
    
    for case in cases:
        print(f"[bold]{case.id}[/bold]: {case.summary}")

if __name__ == '__main__':
    search()
```

**Lines of Code:** 15  
**Functionality:** Full case search with auth, API, formatting  
**Maintenance:** Minimal (dependencies maintained by others)

### Pattern 2: Configuration Over Code

**Concept:** Declarative config + proven engine

**Bad (Code):**
```python
# 500 lines of scheduling logic
def schedule_report(report, cron_expr, email):
    # Custom cron parser
    # Custom email sender
    # Custom job runner
```

**Good (Config):**
```yaml
# schedules.yml - let systemd handle it
reports:
  - name: daily-cases
    schedule: "0 9 * * *"  # Standard cron
    command: tam-rfe-chat "summary"
    notify: jbyrd@redhat.com
```

```bash
# One-time setup: Use systemd timers
systemd-run --user --timer-property="OnCalendar=daily" \
  tam-rfe-chat "summary"
```

**Result:** No custom scheduler code, proven systemd handles it

### Pattern 3: Composition Over Inheritance

**Concept:** Combine proven tools via pipes/APIs

**Bad (Monolithic):**
```python
# tam-rfe-monolith.py (2000 lines)
class RFETool:
    def __init__(self):
        self.http_client = CustomHTTPClient()  # 300 lines
        self.json_parser = CustomJSONParser()  # 200 lines
        self.formatter = CustomFormatter()     # 150 lines
        # ... 1350 more lines
```

**Good (Composed):**
```bash
# Combine proven tools
tam-rfe-fetch-cases |    # Gets case data (50 lines)
  jq '.cases[]' |         # Proven JSON processor
  tam-rfe-format          # Formats output (30 lines)
```

**Result:** 80 lines vs. 2000 lines

---

## Real-World Examples

### Example 1: tam-rfe-chat (Current - Good Design)

**What It Does:**
- Natural language TAM assistance
- Case searching
- Customer information

**What It Uses:**
```python
import rhcase        # ✅ Red Hat official
import openai        # ✅ OpenAI official
import click         # ✅ Proven CLI
from rich import print  # ✅ Proven formatting
```

**Lines of Custom Code:** ~200  
**Lines of Proven Code:** ~50,000 (in dependencies)  

**Ratio:** 1% custom, 99% proven ✅

### Example 2: RFE Installer (Before Ansible - Bad)

**What It Was:**
- 400 lines of bash
- Custom OS detection
- Custom package installation
- Platform-specific paths

**Problems:**
- ❌ macOS compatibility issues (Issue #12, #15)
- ❌ Python version detection bugs (Issue #14)
- ❌ Hard to test
- ❌ High maintenance

### Example 2: RFE Installer (After Ansible - Good)

**What It Will Be:**
```yaml
# playbooks/rfe-install.yml
roles:
  - geerlingguy.python  # ✅ Handles all platforms
  - geerlingguy.git     # ✅ Handles all platforms
  - rfe_install         # ✅ Our logic only (50 lines)
```

**Lines of Custom Code:** ~50  
**Lines of Proven Code:** ~5,000 (in Geerling's roles)  

**Ratio:** 1% custom, 99% proven ✅

### Example 3: gitlab-webhook-receiver (Mixed)

**What It Does:**
- Receives GitLab webhooks
- Sends email notifications

**Current Implementation:**
```python
from flask import Flask  # ✅ Proven web framework
import smtplib          # ✅ Standard library
# 100 lines of custom logic
```

**Could Be Better:**
```yaml
# n8n workflow (0 lines of code)
trigger: gitlab_webhook
action: send_email
```

**Lesson:** For simple integrations, use n8n instead of custom code

---

## The "Geerling Test"

### Before Writing Infrastructure Code, Ask:

**Questions:**
1. Has Jeff Geerling already solved this? → ansible-galaxy search
2. Has someone written a Python lib? → pip search
3. Is there a standard Unix tool? → man pages
4. Can n8n/Ansible handle it? → Check workflows/roles

**If ANY answer is "yes"** → Use existing solution

**Only write custom code if ALL answers are "no"**

---

## Maintenance Burden Calculator

### Before Adding a Dependency

**Questions:**
1. **Last commit?** 
   - < 1 month ago = Low risk
   - 1-6 months = Medium risk
   - > 6 months = High risk

2. **Issue response time?**
   - < 1 week = Low burden
   - 1-4 weeks = Medium burden
   - > 1 month = High burden

3. **Breaking changes?**
   - Semantic versioning = Low burden
   - No versioning = High burden

4. **Bus factor?**
   - 10+ contributors = Low risk
   - 3-10 contributors = Medium risk
   - 1-2 contributors = High risk

**Decision:**
- **All Low:** Add dependency immediately
- **Mix Low/Medium:** Add with version pinning
- **Any High:** Reconsider or plan to fork

---

## Progressive Enhancement Strategy

### Start Simple, Add Features Later

**Phase 1: Minimum Viable Tool (Week 1)**
```bash
#!/bin/bash
# tam-rfe-simple: Just the core feature
rhcase search "$1" | jq '.cases[]'
```

**Phase 2: Add UI (Week 2)**
```python
# Use proven CLI library
import click
@click.command()
def search(query):
    # Same logic, better UX
```

**Phase 3: Add Intelligence (Month 1)**
```python
# Use proven AI library
import openai
# Enhance with AI features
```

**Principle:** Each phase adds proven tools, not custom code

---

## Code Review Checklist

### For Every New Tool

**Before Committing:**
- [ ] Uses proven libraries for infrastructure?
- [ ] Custom code < 200 lines?
- [ ] Focused on business logic only?
- [ ] No reimplemented HTTP/JSON/auth?
- [ ] Dependencies are maintained (< 3 months)?
- [ ] Ansible-installable (or will be)?
- [ ] Works on RHEL 9 + macOS?

**If any ❌** → Refactor before merging

---

## Learning from World-Class Projects

### Ansible
**Lesson:** Modules are thin wrappers around system tools
```yaml
# Ansible doesn't reimplement package managers
- ansible.builtin.package:  # Calls dnf/apt/zypper
    name: git
```

**Apply to PAI:**
```python
# Don't reimplement rhcase API
from rhcase import RHCase  # Use official client
```

### Homebrew
**Lesson:** Formulae are declarations, not implementations
```ruby
# Homebrew formula = metadata only
class Git < Formula
  url "https://..."  # Proven build process handles rest
end
```

**Apply to PAI:**
```yaml
# Tool config = declarations
customers:
  jpmc:
    account: 123456
    # Proven tam-rfe-chat handles rest
```

### Terraform
**Lesson:** Providers handle complexity, users write config
```hcl
# Users write simple config
resource "aws_instance" "server" {
  ami = "ami-123"  # Provider handles AWS API
}
```

**Apply to PAI:**
```yaml
# Simple playbooks
- role: geerlingguy.docker  # Role handles complexity
```

---

## Anti-Patterns to Avoid

### ❌ Not Invented Here (NIH) Syndrome

**Symptom:** "I'll write my own HTTP client, it's only 50 lines"

**Reality:** 
- Those 50 lines grow to 500
- Edge cases take months
- Security issues take years

**Fix:** Use `requests`

### ❌ Resume-Driven Development

**Symptom:** "Let's use [trendy new framework] because it's cool"

**Reality:**
- Learning curve delays project
- Immature ecosystem causes bugs
- Few Stack Overflow answers

**Fix:** Use proven tools (even if "boring")

### ❌ Perfect is the Enemy of Good

**Symptom:** "Before we start, let's design the perfect architecture"

**Reality:**
- Analysis paralysis
- No working code for weeks
- Requirements change anyway

**Fix:** 
1. Build minimum viable version
2. Use proven components
3. Iterate based on real usage

### ❌ Premature Optimization

**Symptom:** "This curl request is too slow, I'll write raw socket code"

**Reality:**
- Months spent optimizing
- Bugs from low-level code
- Negligible real-world improvement

**Fix:** Measure first, optimize only if needed

---

## The PAI Tool Development Workflow

### Step 1: Requirement (Day 1)
```
User: "I need a tool to schedule case reports"
```

### Step 2: Research (30 minutes)
```bash
# Check if solved
ansible-galaxy search scheduler
pip search schedule
github search "systemd timers ansible"
```

### Step 3: Design (1 hour)
```yaml
# Compose proven tools
Solution:
  - systemd timers (proven scheduler)
  - tam-rfe-chat (existing tool)
  - ansible role (proven deployment)
Custom code needed: ~50 lines (glue only)
```

### Step 4: Prototype (2 hours)
```bash
# Test with proven tools
systemd-run --user --timer-property="OnCalendar=daily" \
  tam-rfe-chat "summary"
# If works → productionize
```

### Step 5: Productionize (1 day)
```yaml
# Create Ansible role
- name: Schedule reports
  systemd_timer:  # Proven module
    name: tam-reports
    schedule: daily
    command: tam-rfe-chat "summary"
```

### Step 6: Deploy (30 minutes)
```bash
ansible-playbook playbooks/schedule-reports.yml
```

**Total Time:** 2 days (with proven tools)  
**Without Proven Tools:** 2 weeks (custom scheduler)

---

## Success Metrics

### How to Measure "Building on Giants"

**Code Metrics:**
- **Custom Code Ratio:** < 10% (90%+ from proven libs)
- **Dependency Health:** All deps updated < 3 months ago
- **Bus Factor:** Each dependency has 3+ active maintainers

**Velocity Metrics:**
- **Time to MVP:** < 1 week (using proven components)
- **Bug Rate:** < 1 bug per 100 LOC (proven code = fewer bugs)
- **Onboarding Time:** < 1 hour (familiar tools)

**Maintenance Metrics:**
- **Update Frequency:** Monthly dependency updates only
- **Security Issues:** < 1 per year (upstream handles it)
- **Breaking Changes:** < 1 per year (semver + pinning)

---

## Bottom Line

### The Philosophy in One Sentence

**"If someone world-class has already built it, use their work and focus on your unique value."**

### The PAI Way

**Traditional Approach:**
1. Invent custom solution
2. Debug for months
3. Maintain forever
4. Repeat for each new tool

**PAI Approach:**
1. Find proven solution (30 min research)
2. Integrate with thin wrapper (2 hours)
3. Let upstream maintain it
4. Focus on business logic

### What This Means for Your Tools

**Every PAI Tool Should:**
- ✅ Use Ansible for deployment (Geerling's roles)
- ✅ Use proven Python libs (requests, click, rich)
- ✅ Use standard shell tools (jq, fzf, dialog)
- ✅ Compose via pipes/APIs, not monoliths
- ✅ Config over code where possible
- ✅ Custom code only for business logic

**Result:**
- **80% less code to maintain**
- **10x faster development**
- **90% fewer bugs**
- **100% focus on TAM value**

---

## Quick Reference

### Before Writing Any Code, Check:

1. **Ansible Galaxy** → `ansible-galaxy search <feature>`
2. **PyPI** → `pip search <feature>`  
3. **GitHub** → `site:github.com <feature> stars:>1000`
4. **Jeff Geerling** → https://github.com/geerlingguy
5. **Standard Tools** → `man <command>`

### If Found Proven Solution → Use It

### If No Proven Solution → Build Minimal Version

### Always → Focus on Business Value, Not Plumbing

---

*Last Updated: October 17, 2025*  
*Philosophy: Build on Giants' Shoulders*  
*Inspired by: Jeff Geerling, Ansible, Homebrew, Unix Philosophy*
