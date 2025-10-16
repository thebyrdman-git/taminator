# TAM RFE Automation Tool

**Automatically generates and posts professional RFE/Bug tracker reports to Customer Portal Groups, saving TAMs 2-3 hours per customer per week.**

Developed by jbyrd, using tools from [grimm's PAI project](https://gitlab.cee.redhat.com/gvaughn/hatter-pai).

## 🚀 Quick Start

```bash
# 1. Clone and enter directory
git clone https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation.git
cd rfe-and-bug-tracker-automation

# 2. Run automated installer (no sudo needed)
./install-improved.sh

# 3. Configure your customers (one-time setup)
./bin/tam-rfe-onboard-intelligent

# 4. Start using the tool
./bin/tam-rfe-chat
```

**Requirements**: Red Hat VPN, `git`, `python3` 3.8+ (usually pre-installed)

## ✨ What's New: Dynamic Customer Onboarding

**Zero-configuration customer management** - The tool now automatically configures both `customers.conf` and `tamscripts.config` when you add customers through the onboarding wizard.

### How It Works
1. Run `./bin/tam-rfe-onboard-intelligent`
2. Answer questions about your customers (name, account number, SBR groups)
3. **Done!** Customer is instantly searchable with `rhcase` - no manual config file editing required

### Benefits
- ✅ **Instant availability** - New customers searchable immediately
- ✅ **Zero manual config** - No more editing YAML files
- ✅ **Automatic sync** - Both config systems stay synchronized
- ✅ **Safe operations** - Automatic backups before changes

**See**: `DYNAMIC-CUSTOMER-ONBOARDING-FIX.md` for technical details

## 💬 Common Commands

Once installed, use natural language commands:

```
show cases for Westpac
show open cases for Wells Fargo  
generate report for TD Bank
find similar cases to 04244831
prepare meeting for JPMC
help
```

**Full command reference**: [COMMANDS.md](COMMANDS.md)

## 🎯 What This Tool Does

- **Discovers** all RFE and Bug cases using `rhcase`
- **Filters** by SBR Group (Ansible, OpenShift, etc.) and status
- **Generates** professional reports:
  - Active case reports (open cases)
  - RFE/Bug tracker reports (3-table format with history)
- **Posts** directly to customer portal groups
- **Notifies** TAMs via email with status updates

## 🚫 What This Tool Does NOT Do

- ❌ Create or modify cases
- ❌ Send notifications to customers
- ❌ Access data outside Red Hat systems
- ❌ Replace TAM judgment

## 📊 Time Savings

| Process | Manual | Automated | Savings |
|---------|--------|-----------|---------|
| **Per Customer/Week** | 2-3 hours | 5 minutes | **95%** |
| **Per TAM/Year** | 400-600 hours | 17 hours | **95%** |

## 🔍 Report Types

### RFE/Bug Tracker Report
- Cases with `[RFE]` or `[BUG]` in title
- Recent closed cases for historical context
- Excludes configuration/support issues

### Active Cases Report
- All active cases EXCEPT RFEs/Bugs
- Configuration issues, account service requests
- Excludes cases with external tracker references (JIRA URLs)

**Together**: Complete picture of all customer cases without duplication

## 🔍 Report Validation

Ensure report accuracy before distribution:

```bash
# Validate everything
./bin/validate-rfe-reports wellsfargo

# System check only
./bin/validate-rfe-reports --system-only
```

**Quality Standards**:
- ✅ **99%+**: Ready for customer distribution
- ⚠️ **95-98%**: Review before sharing
- ❌ **<95%**: Fix issues first

**See**: `docs/REPORT-VALIDATION-GUIDE.md`

## 🛡️ Security & Compliance

- ✅ Customer data: Red Hat Granite models only
- ✅ External APIs: Blocked for customer data
- ✅ Audit logging: All operations tracked
- ✅ Red Hat AI Policy: Fully compliant

## 🆘 Troubleshooting

```bash
# Verify system health
./bin/tam-rfe-verify --quick
```

**Common Issues**:
- **No cases found**: Check VPN connection (`curl -I https://source.redhat.com`)
- **Python packages missing**: Run `./bin/install-dependencies`
- **New customer not working**: Re-run `./bin/tam-rfe-onboard-intelligent`

**Support**:
- **GitLab Issues**: https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation/-/issues
- **Developer**: jbyrd@redhat.com
- **Slack**: #tam-automation-tools

## 📚 Documentation

- **[Command Reference](COMMANDS.md)**: Complete command list
- **[Getting Started](GETTING-STARTED.md)**: 5-minute setup guide
- **[Purpose Statement](PURPOSE.md)**: Detailed functionality
- **[Prerequisites](docs/PREREQUISITES-GUIDE.md)**: Setup requirements
- **[Dynamic Onboarding](DYNAMIC-CUSTOMER-ONBOARDING-FIX.md)**: Technical details

## 🤝 Contributing

Help improve report consistency and quality:

1. Use the tool with your customers for a week
2. Note any issues with report quality or formatting
3. Submit feedback via GitLab issues
4. Share success stories with the team

**Every contribution helps ensure consistent, professional customer communication.**

## 🏢 Example Configuration

| Customer | Account # | Status |
|----------|-----------|--------|
| Wells Fargo | 838043 | ✅ Production |
| TD Bank | 1912101 | ✅ Production |
| JPMC | 334224 | ✅ Production |
| Fannie Mae | 1460290 | ✅ Production |

*Configure with your customers during setup*

## 🎯 Bottom Line

**Transforms a 2-3 hour manual weekly task into a 5-minute automated process**, freeing TAMs to focus on strategic customer work while ensuring consistent, professional customer communication.

---

**🤖 TAM Automation Assistant**  
*Built by jbyrd for the Red Hat TAM community*  
*Making your life easier, one report at a time*
