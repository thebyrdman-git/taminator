# Development Retrospection Framework

**Philosophy:** Learn from every project, improve the framework, compound knowledge  
**Pattern:** Systematic reflection → Capture lessons → Update framework → Repeat  
**Result:** Continuously improving development process

---

## The Problem

Traditional development:
```
Build project → Ship it → Move on
  ↓
Lessons lost
Mistakes repeated
Knowledge siloed
No improvement
```

## The Solution: Systematic Retrospection

```
Build project → Retrospect → Capture lessons → Update framework → Next project better
  ↓
Lessons captured
Patterns identified
Framework improved
Compound learning
```

---

## Part 1: Retrospection Triggers

### Automatic Triggers (Tools Remind You)

**After Project Completion:**
```bash
# Git hook triggers retrospection
git tag v1.0.0
→ Triggers: pai-retrospect --project

# Reminds you to reflect
```

**Weekly Review:**
```bash
# Cron job: Every Friday 4pm
0 16 * * 5 pai-retrospect --weekly

# Shows what you built this week
# Prompts for lessons learned
```

**Monthly Deep Dive:**
```bash
# First Monday of month
0 9 1-7 * 1 pai-retrospect --monthly

# Patterns across projects
# Framework improvements needed
```

**Quarterly Strategic:**
```bash
# Every quarter
pai-retrospect --quarterly

# What's working?
# What needs to change?
# Industry trends to adopt?
```

---

## Part 2: Retrospection Template

### Project Retrospection (`pai-retrospect --project`)

```markdown
# Project Retrospection: [PROJECT_NAME]

**Date:** [DATE]
**Duration:** [START] to [END]
**Team:** [NAMES]

---

## 1. What Did We Build?

**Summary:** (1-2 sentences)

**Components:**
- Component 1: [Description]
- Component 2: [Description]
- Component 3: [Description]

**Lines of Code:**
- Total: [NUMBER]
- Custom (5%): [NUMBER]
- Reused (95%): [NUMBER]

**Time:**
- Planned: [DURATION]
- Actual: [DURATION]
- Variance: [%]

---

## 2. What Went Well? ✅

### Technical Wins
- [ ] Item 1
- [ ] Item 2
- [ ] Item 3

**Why it worked:**


### Process Wins
- [ ] Item 1
- [ ] Item 2

**Why it worked:**


### Tools That Helped
- Tool 1: [How it helped]
- Tool 2: [How it helped]

---

## 3. What Went Wrong? ❌

### Technical Issues
- [ ] Issue 1
- [ ] Issue 2

**Root cause:**


### Process Issues
- [ ] Issue 1
- [ ] Issue 2

**Root cause:**


### Time Wasters
- Wasted time on: [WHAT]
- Could have saved: [TIME] by [DOING WHAT]

---

## 4. Geerling Test Results

**Did we check for existing solutions?**
- [ ] Searched Ansible Galaxy
- [ ] Searched PyPI
- [ ] Searched GitHub (1000+ stars)
- [ ] Checked Geerling repos
- [ ] Checked Unix tools

**What we found and used:**


**What we should have found but didn't:**


**Custom code we wrote that existed:**


---

## 5. Framework Effectiveness

### What Worked (Keep)
- Pattern 1: [Why it worked]
- Pattern 2: [Why it worked]

### What Didn't Work (Change)
- Pattern 1: [Why it failed]
- Pattern 2: [Why it failed]

### What's Missing (Add)
- Missing 1: [What we needed]
- Missing 2: [What we needed]

---

## 6. Lessons Learned

### Technical Lessons
1. **Lesson 1:**
   - What we learned:
   - How to apply next time:
   - Framework update needed:

2. **Lesson 2:**
   - What we learned:
   - How to apply next time:
   - Framework update needed:

### Process Lessons
1. **Lesson 1:**
   - What we learned:
   - How to apply next time:
   - Framework update needed:

---

## 7. Metrics

### Development Speed
- Traditional estimate: [MONTHS]
- Actual time: [WEEKS/DAYS]
- Speedup: [X]x faster

### Code Reuse
- Total code: [LINES]
- Custom code: [LINES] ([%])
- Reused code: [LINES] ([%])

### Quality
- Bugs found in dev: [NUMBER]
- Bugs found in prod: [NUMBER]
- Uptime: [%]
- SLO met: [YES/NO]

---

## 8. Action Items

### Framework Updates
- [ ] Update pattern: [WHAT]
- [ ] Add to checklist: [WHAT]
- [ ] Create new tool: [WHAT]
- [ ] Document pattern: [WHAT]

### Process Improvements
- [ ] Change process: [WHAT]
- [ ] Add automation: [WHAT]
- [ ] Remove waste: [WHAT]

### Learning Goals
- [ ] Study: [TOPIC]
- [ ] Explore: [TOOL/PATTERN]
- [ ] Read: [BOOK/ARTICLE]

---

## 9. Share Knowledge

**Blog post topic:**


**Internal presentation:**


**Contribution back:**
- [ ] Open source contribution
- [ ] Framework documentation
- [ ] Team sharing session

---

## 10. Next Project Prep

**What we'll do differently:**


**What we'll keep:**


**New patterns to try:**


---

**Retrospection completed:** [DATE]
**Reviewed by:** [NAMES]
**Next review:** [DATE]
```

---

## Part 3: The Retrospection Tool

### `bin/pai-retrospect`

```bash
#!/bin/bash
#
# pai-retrospect: Development Retrospection Tool
# Systematic learning from every project
#

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================================${NC}"
}

print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }

# Configuration
RETRO_DIR="$HOME/pai/retrospectives"
TEMPLATE_DIR="$HOME/pai/docs/templates"
CURRENT_DATE=$(date +%Y-%m-%d)

# Ensure directories exist
mkdir -p "$RETRO_DIR"
mkdir -p "$TEMPLATE_DIR"

# Parse arguments
MODE="project"
PROJECT_NAME=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --project)
            MODE="project"
            shift
            ;;
        --weekly)
            MODE="weekly"
            shift
            ;;
        --monthly)
            MODE="monthly"
            shift
            ;;
        --quarterly)
            MODE="quarterly"
            shift
            ;;
        *)
            PROJECT_NAME="$1"
            shift
            ;;
    esac
done

print_header "Development Retrospection"
echo ""

case $MODE in
    project)
        # Project retrospection
        if [ -z "$PROJECT_NAME" ]; then
            # Auto-detect from Git
            if git rev-parse --git-dir > /dev/null 2>&1; then
                PROJECT_NAME=$(basename "$(git rev-parse --show-toplevel)")
                print_info "Detected project: $PROJECT_NAME"
            else
                echo "Usage: pai-retrospect [--project] <project-name>"
                exit 1
            fi
        fi
        
        RETRO_FILE="$RETRO_DIR/$CURRENT_DATE-$PROJECT_NAME.md"
        
        print_info "Creating project retrospection for: $PROJECT_NAME"
        echo ""
        
        # Gather automatic metrics
        if git rev-parse --git-dir > /dev/null 2>&1; then
            COMMITS=$(git rev-list --count HEAD)
            CONTRIBUTORS=$(git log --format='%an' | sort -u | wc -l)
            FIRST_COMMIT=$(git log --reverse --format='%ai' | head -1 | cut -d' ' -f1)
            LAST_COMMIT=$(git log --format='%ai' | head -1 | cut -d' ' -f1)
            
            # Calculate lines of code
            TOTAL_LINES=$(find . -name "*.py" -o -name "*.sh" -o -name "*.yml" | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}')
        else
            COMMITS="N/A"
            CONTRIBUTORS="N/A"
            FIRST_COMMIT="N/A"
            LAST_COMMIT="N/A"
            TOTAL_LINES="N/A"
        fi
        
        # Create retrospection file
        cat > "$RETRO_FILE" << RETRO_TEMPLATE
# Project Retrospection: $PROJECT_NAME

**Date:** $CURRENT_DATE
**Duration:** $FIRST_COMMIT to $LAST_COMMIT
**Contributors:** $CONTRIBUTORS
**Commits:** $COMMITS

---

## 1. What Did We Build?

**Summary:** 

**Components:**
- Component 1: 
- Component 2: 
- Component 3: 

**Metrics:**
- Lines of code: $TOTAL_LINES
- Commits: $COMMITS
- Duration: (calculate from dates above)

---

## 2. What Went Well? ✅

### Technical Wins


### Process Wins


### Tools That Helped


---

## 3. What Went Wrong? ❌

### Technical Issues


### Process Issues


### Time Wasters


---

## 4. Geerling Test Results

**Did we check for existing solutions?**
- [ ] Searched Ansible Galaxy
- [ ] Searched PyPI  
- [ ] Searched GitHub (1000+ stars)
- [ ] Checked Geerling repos
- [ ] Checked Unix tools

**What we found and used:**


**What we should have found but didn't:**


---

## 5. Framework Effectiveness

### What Worked (Keep)


### What Didn't Work (Change)


### What's Missing (Add)


---

## 6. Lessons Learned

### Technical Lessons
1. **Lesson:**
   - What we learned:
   - Apply next time:
   - Framework update:

### Process Lessons
1. **Lesson:**
   - What we learned:
   - Apply next time:
   - Framework update:

---

## 7. Metrics

### Development Speed
- Traditional estimate: [MONTHS]
- Actual time: [WEEKS/DAYS]
- Speedup: [X]x faster

### Code Reuse
- Total code: $TOTAL_LINES lines
- Custom code: [LINES] ([%])
- Reused code: [LINES] ([%])

---

## 8. Action Items

### Framework Updates
- [ ] Update pattern:
- [ ] Add to checklist:
- [ ] Create new tool:

### Process Improvements
- [ ] Change process:
- [ ] Add automation:

### Learning Goals
- [ ] Study:
- [ ] Explore:

---

## 9. Share Knowledge

**Blog post topic:**


**Internal presentation:**


---

## 10. Next Project Prep

**What we'll do differently:**


**What we'll keep:**


**New patterns to try:**


RETRO_TEMPLATE
        
        # Open in editor
        ${EDITOR:-vim} "$RETRO_FILE"
        
        print_success "Retrospection saved: $RETRO_FILE"
        echo ""
        print_info "Next steps:"
        echo "  1. Fill out retrospection"
        echo "  2. Review with team"
        echo "  3. Update framework based on lessons"
        echo "  4. Run: pai-retrospect-analyze"
        ;;
        
    weekly)
        print_info "Weekly retrospection"
        echo ""
        print_info "This week you worked on:"
        
        # Show Git activity
        if git rev-parse --git-dir > /dev/null 2>&1; then
            git log --since="1 week ago" --oneline --author="$(git config user.name)"
        fi
        
        echo ""
        print_info "Quick reflection:"
        read -p "Biggest win this week: " win
        read -p "Biggest challenge: " challenge
        read -p "One thing to improve: " improve
        
        WEEKLY_FILE="$RETRO_DIR/weekly-$CURRENT_DATE.md"
        cat > "$WEEKLY_FILE" << WEEKLY
# Weekly Retrospection: $CURRENT_DATE

**Win:** $win
**Challenge:** $challenge
**Improve:** $improve

---

WEEKLY
        
        print_success "Weekly retrospection saved"
        ;;
        
    monthly)
        print_header "Monthly Retrospection"
        echo ""
        print_info "Analyzing last month's retrospections..."
        
        # Show all retrospections from last month
        find "$RETRO_DIR" -name "*.md" -mtime -30 -type f
        
        echo ""
        print_info "Patterns across projects:"
        echo "  1. What patterns repeated?"
        echo "  2. What's working consistently?"
        echo "  3. What needs framework-level fix?"
        ;;
        
    quarterly)
        print_header "Quarterly Strategic Retrospection"
        echo ""
        print_info "Big picture review:"
        echo "  1. Review all quarterly retrospections"
        echo "  2. Identify major trends"
        echo "  3. Plan framework evolution"
        echo "  4. Set learning goals"
        ;;
esac

echo ""
print_success "Retrospection complete!"
```

---

## Part 4: Retrospection Analysis

### `bin/pai-retrospect-analyze`

```bash
#!/bin/bash
#
# pai-retrospect-analyze: Analyze retrospections for patterns
#

set -euo pipefail

RETRO_DIR="$HOME/pai/retrospectives"

echo "Analyzing retrospections..."
echo ""

# Find common patterns
echo "=== Common Technical Issues ==="
grep -h "### Technical Issues" "$RETRO_DIR"/*.md -A 10 | grep -v "^--$" | sort | uniq -c | sort -rn | head -10
echo ""

echo "=== Tools That Helped Most ==="
grep -h "### Tools That Helped" "$RETRO_DIR"/*.md -A 10 | grep -v "^--$" | sort | uniq -c | sort -rn | head -10
echo ""

echo "=== Framework Improvements Needed ==="
grep -h "Framework update:" "$RETRO_DIR"/*.md | sort | uniq -c | sort -rn
echo ""

echo "=== Geerling Test Failures ==="
grep -h "should have found but didn't" "$RETRO_DIR"/*.md -A 3
echo ""

echo "Analysis complete!"
echo ""
echo "Next: Update framework based on patterns"
```

---

## Part 5: Integration with Workflow

### Git Hooks

**`.git/hooks/post-merge`**
```bash
#!/bin/bash
# Remind about retrospection after major merge

if git log -1 --pretty=%B | grep -q "Merge.*main"; then
    echo ""
    echo "🔍 Major merge detected!"
    echo "Don't forget to run: pai-retrospect --project"
    echo ""
fi
```

**`.git/hooks/post-tag`**
```bash
#!/bin/bash
# Trigger retrospection on version tag

TAG=$(git describe --tags)

if [[ $TAG =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo ""
    echo "🎉 Version $TAG released!"
    echo "Time to reflect: pai-retrospect --project"
    echo ""
    
    # Optionally auto-trigger
    read -p "Run retrospection now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pai-retrospect --project
    fi
fi
```

### Cron Jobs

**Weekly reminder:**
```cron
# Every Friday at 4pm
0 16 * * 5 notify-send "Weekly Retrospection" "Time to reflect on this week: pai-retrospect --weekly"
```

**Monthly deep dive:**
```cron
# First Monday of month at 9am
0 9 1-7 * 1 notify-send "Monthly Retrospection" "Time for monthly review: pai-retrospect --monthly"
```

---

## Part 6: The Learning Loop

```
┌─────────────────────────────────────────────────────┐
│                   Build Project                     │
└────────────────────┬────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────┐
│              Trigger Retrospection                  │
│  • Project completion (Git tag)                    │
│  • Weekly (Friday 4pm)                             │
│  • Monthly (First Monday)                          │
│  • Quarterly (Strategic review)                    │
└────────────────────┬────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────┐
│              Capture Lessons                        │
│  • What went well?                                 │
│  • What went wrong?                                │
│  • Geerling test results                           │
│  • Framework effectiveness                         │
│  • Action items                                    │
└────────────────────┬────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────┐
│              Analyze Patterns                       │
│  • pai-retrospect-analyze                          │
│  • Common issues across projects                   │
│  • Tools that consistently help                    │
│  • Framework gaps                                  │
└────────────────────┬────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────┐
│              Update Framework                       │
│  • Add missing patterns                            │
│  • Update checklists                               │
│  • Create new tools                                │
│  • Document lessons                                │
│  • Share knowledge                                 │
└────────────────────┬────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────┐
│              Next Project (Better)                  │
│  • Apply lessons learned                           │
│  • Use improved framework                          │
│  • Avoid previous mistakes                         │
│  • Build on previous successes                     │
└────────────────────┬────────────────────────────────┘
                     │
                     ↓ (Repeat - Continuous Improvement)
```

---

## Part 7: Retrospection Metrics

### Track Improvement Over Time

```bash
# pai-retrospect-metrics
#!/bin/bash

echo "Retrospection Metrics"
echo "===================="
echo ""

# Project count
TOTAL_RETROS=$(find "$HOME/pai/retrospectives" -name "*.md" -type f | wc -l)
echo "Total retrospections: $TOTAL_RETROS"
echo ""

# Development speed trend
echo "Development Speed Trend:"
grep -h "Speedup:" "$HOME/pai/retrospectives"/*.md | awk '{print $2}' | sort -n
echo ""

# Code reuse trend
echo "Code Reuse Trend:"
grep -h "Reused code:" "$HOME/pai/retrospectives"/*.md
echo ""

# Framework updates
echo "Framework Updates Made:"
grep -h "Framework update:" "$HOME/pai/retrospectives"/*.md | wc -l
echo ""

# Learning goals
echo "Learning Goals Set:"
grep -h "Study:" "$HOME/pai/retrospectives"/*.md | wc -l
```

---

## Part 8: Knowledge Base Integration

### Auto-Update Documentation

```bash
# pai-retrospect-to-docs
#!/bin/bash
#
# Extract lessons from retrospections
# Add to framework documentation
#

RETRO_DIR="$HOME/pai/retrospectives"
PATTERNS_FILE="$HOME/pai/docs/LEARNED-PATTERNS.md"

# Extract all "Framework update needed" items
grep -h "Framework update:" "$RETRO_DIR"/*.md > /tmp/updates.txt

# Categorize
echo "# Patterns Learned from Retrospections" > "$PATTERNS_FILE"
echo "" >> "$PATTERNS_FILE"
echo "Auto-generated from project retrospections" >> "$PATTERNS_FILE"
echo "" >> "$PATTERNS_FILE"

# Add to documentation
cat /tmp/updates.txt >> "$PATTERNS_FILE"

echo "Updated: $PATTERNS_FILE"
```

---

## Part 9: Team Retrospections

### Collaborative Retrospection

```bash
# pai-retrospect-team
#!/bin/bash

PROJECT="$1"
RETRO_FILE="$HOME/pai/retrospectives/team-$(date +%Y-%m-%d)-$PROJECT.md"

echo "Team Retrospection: $PROJECT"
echo ""

# Collect input from all team members
echo "Enter team members (one per line, empty to finish):"
MEMBERS=()
while true; do
    read -p "Member: " member
    [ -z "$member" ] && break
    MEMBERS+=("$member")
done

# Create collaborative retrospection
cat > "$RETRO_FILE" << TEAM_RETRO
# Team Retrospection: $PROJECT

**Date:** $(date +%Y-%m-%d)
**Team:** ${MEMBERS[@]}

---

## Team Feedback

$(for member in "${MEMBERS[@]}"; do
    echo "### $member"
    echo ""
    echo "**What went well:**"
    echo ""
    echo "**What could improve:**"
    echo ""
    echo "**Suggestion for next project:**"
    echo ""
done)

TEAM_RETRO

# Open for collaborative editing
echo ""
echo "Opening collaborative retrospection..."
${EDITOR:-vim} "$RETRO_FILE"
```

---

## Part 10: Retrospection Checklist

### Before Starting Retrospection

- [ ] Project is complete (or milestone reached)
- [ ] Have metrics ready (lines of code, time, etc.)
- [ ] Git history available
- [ ] Team members available (if team retro)
- [ ] Quiet time scheduled (no interruptions)

### During Retrospection

- [ ] Be honest (what really happened?)
- [ ] Focus on lessons (not blame)
- [ ] Identify patterns (not one-offs)
- [ ] Make action items specific
- [ ] Assign owners to action items
- [ ] Set dates for follow-up

### After Retrospection

- [ ] Review with team
- [ ] Create issues for action items
- [ ] Update framework documentation
- [ ] Share knowledge (blog, presentation)
- [ ] Schedule next retrospection
- [ ] Follow up on action items

---

## Bottom Line

### Without Retrospection
```
Project 1 → Ship → Mistakes forgotten
Project 2 → Ship → Repeat same mistakes
Project 3 → Ship → Still repeating
No improvement
```

### With Systematic Retrospection
```
Project 1 → Retrospect → Lessons captured → Framework updated
Project 2 → Retrospect → More lessons → Framework improved
Project 3 → Retrospect → Patterns identified → Framework optimized
Continuous improvement
```

### The Compound Effect

After 1 retrospection: Small improvements  
After 10 retrospections: Noticeable patterns  
After 50 retrospections: Optimized framework  
After 100 retrospections: World-class process

**Retrospection turns experience into expertise.**

---

*Philosophy: Learn from Every Project*  
*Pattern: Reflect → Capture → Improve → Repeat*  
*Result: Continuously improving development process*
