# RFE Automation Tool - Purpose Statement

## 🎯 What This Tool Does

**The RFE Automation Tool automatically generates and posts professional RFE/Bug tracker reports to customer portal groups, saving TAMs 2-3 hours per customer per week.**

## 📋 Specific Functionality

### Input
- Customer account number
- SBR Group filters (Ansible, OpenShift, etc.)
- Case status filters (Active, Closed, etc.)

### Process
1. **Discovers cases** using `rhcase list [customer] --months 1`
2. **Filters cases** by SBR Group and status
3. **Generates 3-table report**:
   - Active RFE cases
   - Active Bug cases
   - Closed case history
4. **Posts to customer portal** via Red Hat API
5. **Sends notification** to TAM with results

### Output
- Professional portal content posted to customer group
- Email notification to TAM with success/failure status
- Log files for audit and troubleshooting

## ⏱️ Time Savings

| Process | Manual | Automated | Savings |
|---------|--------|-----------|---------|
| **Per Customer Per Week** | 2-3 hours | 5 minutes | 95% reduction |
| **Per TAM Per Week** | 8-12 hours | 20 minutes | 95% reduction |
| **Per TAM Per Year** | 400-600 hours | 17 hours | 95% reduction |

## 🚫 What This Tool Does NOT Do

- ❌ Create new RFE or Bug cases
- ❌ Modify existing case content or status
- ❌ Send notifications to customers
- ❌ Access customer data outside Red Hat systems
- ❌ Replace TAM judgment or customer relationships

## 🎯 Customer Value

- **Consistency**: 100% consistent formatting every time
- **Timeliness**: Daily updates instead of weekly manual updates
- **Accuracy**: Automated discovery eliminates human error
- **Professionalism**: Customer-ready content that reflects well on Red Hat
- **Transparency**: Real-time status of RFE/Bug requests

## 🔧 Technical Details

- **Data Source**: Red Hat `rhcase` tool
- **Output Format**: 3-table markdown with case numbers, summaries, status
- **Posting Method**: Red Hat Customer Portal API
- **Notifications**: Silent (no customer notifications)
- **Compliance**: Red Hat AI policy compliant
- **Audit**: Complete logging and audit trails

---

**Bottom Line**: This tool transforms a 2-3 hour manual weekly task into a 5-minute automated process, freeing TAMs to focus on strategic customer work while ensuring consistent, professional customer communication.

