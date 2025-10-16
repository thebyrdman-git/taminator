# Simple RFE/Bug Report Guide

## 🎯 Purpose
Generate two simple reports:
1. **RFE/Bug Status** - Track feature requests and bug reports
2. **Open Troubleshooting Cases** - Track cases needing troubleshooting

## 📋 Report Types

### 1. RFE/Bug Status Report
**What it shows:**
- Active RFE cases (feature requests)
- Active bug cases (defects)
- Recently closed cases

**What it's for:**
- Product development tracking
- Bug resolution status
- Historical context

### 2. Open Troubleshooting Cases Report  
**What it shows:**
- All open cases except RFE/Bug cases
- Configuration issues
- Support requests
- Operational problems

**What it's for:**
- Daily troubleshooting work
- Support case management
- Customer issue tracking

## 🚀 Usage

### Generate Simple Reports
```bash
# Generate both reports for a customer
ansible-playbook generate_simple_reports.yml -e "customer=jpmc"

# Generate only RFE/Bug report
ansible-playbook generate_simple_reports.yml -e "customer=jpmc" --tags rfe_bug

# Generate only troubleshooting cases
ansible-playbook generate_simple_reports.yml -e "customer=jpmc" --tags active_cases
```

### Simple Output
```
📁 output/
├── jpmc_rfe_bug_report.md
└── jpmc_active_cases_report.md
```

## 📊 What You Get

### RFE/Bug Report Example
```markdown
# RFE/Bug Status Report - JPMC

**Generated:** 2024-12-19
**Account:** 334224

## 📋 Active RFE Cases
| Case # | Subject | Status | Priority |
|--------|---------|--------|----------|
| 03208295 | [RFE] Add new feature | Open | High |

## 🐛 Active Bug Cases  
| Case # | Subject | Status | Priority |
|--------|---------|--------|----------|
| 04131060 | [BUG] Fix login issue | Open | Critical |

## ✅ Recently Closed Cases
| Case # | Subject | Closed Date |
|--------|---------|-------------|
| 04276978 | [RFE] Improve performance | 2024-12-15 |
```

### Active Cases Report Example
```markdown
# Open Troubleshooting Cases - JPMC

**Generated:** 2024-12-19
**Account:** 334224

## 🔧 Open Cases for Troubleshooting
| Case # | Subject | Status | Priority | SBR Group |
|--------|---------|--------|----------|-----------|
| 04345678 | Configuration issue | Open | Medium | Ansible |
| 04345679 | Support request | Open | Low | Ansible |

**Total Open Cases:** 2

## 🎯 Priority Component Cases
| Case # | Subject | Status | Priority |
|--------|---------|--------|----------|
| 04345678 | Configuration issue | Open | Medium |

**Priority Cases:** 1
```

## 🎯 That's It!
Simple, focused reports that do exactly what you need:
- **RFE/Bug tracking** for product development
- **Troubleshooting cases** for daily support work

No complexity, no extra features - just the essential information.
