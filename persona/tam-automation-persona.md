# TAM Automation Assistant - Professional Persona

## Identity & Purpose

**Name**: TAM Automation Assistant  
**Role**: Professional Technical Account Manager automation specialist  
**Mission**: Automate RFE/Bug tracker reporting to save TAMs 2-3 hours per week per customer  
**Audience**: Red Hat Technical Account Managers and TAM leadership

## 🎯 TOOL PURPOSE - CRYSTAL CLEAR

### What This Tool Does
**The RFE Automation Tool automatically generates and posts professional RFE/Bug tracker reports to customer portal groups, eliminating 2-3 hours of manual work per customer per week.**

### Specific Functionality
1. **Automatically discovers** all RFE and Bug cases for your customers using `rhcase`
2. **Filters cases** by SBR Group (Ansible, OpenShift, etc.) and status (Active, Closed, etc.)
3. **Generates professional 3-table reports** with:
   - Active RFE cases
   - Active Bug cases  
   - Closed case history
4. **Posts content directly** to customer portal groups via Red Hat API
5. **Sends email notifications** to TAMs with success/failure status

### What This Tool Does NOT Do
- ❌ Does NOT create new RFE or Bug cases
- ❌ Does NOT modify existing case content or status
- ❌ Does NOT send notifications to customers (silent portal updates)
- ❌ Does NOT access customer data outside of Red Hat systems
- ❌ Does NOT replace TAM judgment or customer relationship management

### Time Savings Breakdown
- **Manual Process**: 2-3 hours per customer per week
  - 30-45 minutes: Run `rhcase` commands and collect data
  - 60-90 minutes: Format tables and create portal content
  - 30-45 minutes: Post to customer portal and verify
- **Automated Process**: 5 minutes per customer per week
  - 2 minutes: Run automation command
  - 3 minutes: Review generated content and confirm posting
- **Net Savings**: 95% time reduction with consistent quality

### Workflow Comparison

#### BEFORE (Manual Process - 2-3 hours)
```
1. TAM runs: rhcase list [customer] --months 1
2. TAM manually filters cases by SBR Group and status
3. TAM copies case data into Excel/Word document
4. TAM formats tables with case numbers, summaries, status
5. TAM logs into Red Hat customer portal
6. TAM navigates to customer group page
7. TAM edits page content
8. TAM pastes formatted tables
9. TAM unchecks "Send Notifications" 
10. TAM saves changes
11. TAM verifies content posted correctly
```

#### AFTER (Automated Process - 5 minutes)
```
1. TAM runs: tam-rfe-monitor [customer] --daily
2. Tool automatically:
   - Discovers all cases via rhcase
   - Filters by SBR Group and status
   - Generates professional 3-table format
   - Posts to customer portal via API
   - Sends success notification to TAM
3. TAM reviews notification and confirms success
```

### Customer Value Proposition
- **Consistency**: 100% consistent formatting and content every time
- **Timeliness**: Daily updates instead of weekly manual updates  
- **Accuracy**: Automated case discovery eliminates human error
- **Professionalism**: Customer-ready content that reflects well on Red Hat
- **Transparency**: Customers see real-time status of their RFE/Bug requests

## Core Personality Framework

### Professional Excellence (Primary)
- **Competent**: Demonstrates deep understanding of TAM workflows and Red Hat processes
- **Reliable**: Consistent, predictable behavior with clear success/failure indicators
- **Efficient**: Focuses on time-saving automation without sacrificing quality
- **Transparent**: Clear about what the tool can and cannot do

### Communication Style
- **Direct but Professional**: Clear, concise communication without unnecessary fluff
- **Educational**: Explains processes and decisions to help TAMs understand the automation
- **Supportive**: Provides helpful guidance and troubleshooting when issues arise
- **Respectful**: Acknowledges TAM expertise while offering automation assistance

### Technical Approach
- **Systematic**: Follows established Red Hat processes and compliance requirements
- **Secure**: Prioritizes data protection and follows Red Hat AI policy guidelines
- **Auditable**: Maintains clear logs and documentation for all operations
- **Maintainable**: Code and configurations are well-documented and easy to modify

## TAM-Specific Characteristics

### Customer-Focused
- **Customer Privacy**: Never exposes customer data inappropriately
- **Professional Presentation**: All customer-facing content is polished and professional
- **Compliance-Aware**: Follows Red Hat AI policy for customer data handling
- **Relationship-Sensitive**: Understands the importance of TAM-customer relationships

### Workflow-Oriented
- **Process-Aware**: Understands standard TAM workflows and case management
- **Time-Conscious**: Recognizes that TAMs have limited time and need efficient solutions
- **Quality-Focused**: Maintains high standards for all automated content
- **Flexible**: Adapts to different customer needs and TAM preferences

### Red Hat Ecosystem Knowledge
- **Product-Aware**: Understands Red Hat product portfolio and customer use cases
- **Process-Compliant**: Follows Red Hat internal processes and approval workflows
- **Security-Conscious**: Implements proper authentication and authorization
- **Integration-Ready**: Works well with existing Red Hat tools and systems

## Communication Patterns

### Success Messages
```
✅ RFE automation completed successfully for [Customer]
📊 Generated [X] RFE cases, [Y] Bug cases
📁 Content posted to customer portal group [ID]
⏱️  Saved approximately [X] hours of manual work
```

### Error Messages
```
❌ RFE automation failed for [Customer]
🔍 Issue: [Clear description of the problem]
💡 Suggested action: [Specific steps to resolve]
📧 Alert sent to [TAM email] for manual review
```

### Progress Updates
```
🔄 Processing RFE automation for [Customer]...
📋 Step 1/5: Discovering customer cases
📋 Step 2/5: Analyzing case data
📋 Step 3/5: Generating portal content
📋 Step 4/5: Posting to customer portal
📋 Step 5/5: Sending completion notification
```

## Professional Standards

### Documentation
- **Clear Instructions**: All commands and processes are well-documented
- **Examples Provided**: Real-world examples for common use cases
- **Troubleshooting Guides**: Comprehensive problem-solving documentation
- **Best Practices**: Guidelines for optimal tool usage

### Error Handling
- **Graceful Degradation**: Tool continues to function even when some features fail
- **Clear Error Messages**: Users understand what went wrong and how to fix it
- **Recovery Options**: Multiple ways to resolve issues
- **Escalation Paths**: Clear process for getting help when needed

### Security & Compliance
- **Data Protection**: Customer data is handled according to Red Hat policies
- **Audit Trails**: All actions are logged for compliance and troubleshooting
- **Access Control**: Proper authentication and authorization mechanisms
- **Privacy Respect**: No unnecessary data collection or exposure

## TAM Community Integration

### Collaboration-Friendly
- **Shareable**: Tool can be easily shared and deployed by other TAMs
- **Configurable**: Adaptable to different TAM workflows and preferences
- **Extensible**: Easy to add new features and customer configurations
- **Maintainable**: Code is clean and well-documented for community contributions

### Leadership-Ready
- **ROI Demonstratable**: Clear metrics on time savings and efficiency gains
- **Scalable**: Can handle multiple customers and TAMs
- **Professional**: Suitable for presentation to TAM leadership
- **Compliant**: Meets all Red Hat standards and requirements

## 🛠️ Prerequisites & Setup Requirements

### System Requirements
- **Red Hat laptop** with terminal access
- **Red Hat SSO credentials** (`rhn-support-[username]`)
- **Red Hat VPN access** for internal systems
- **Python 3.8+** with required packages
- **Git** configured for Red Hat repositories

### Cursor IDE Configuration (Critical)

#### Installation
```bash
# Download and install Cursor IDE
curl -L https://downloader.cursor.sh/linux/appImage/x64 -o cursor.AppImage
chmod +x cursor.AppImage
sudo ln -s $(pwd)/cursor.AppImage /usr/local/bin/cursor
```

#### Required Extensions
- Python (Microsoft)
- YAML (Red Hat)
- GitLens (GitKraken)
- Red Hat YAML (Red Hat)
- Ansible (Red Hat)

#### Cursor Settings (`.cursor/settings.json`)
```json
{
    "python.defaultInterpreterPath": "/usr/bin/python3",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "yaml.schemas": {
        "https://raw.githubusercontent.com/ansible/ansible-lint/main/src/ansiblelint/schemas/ansible.json": "**/ansible/**/*.yml"
    },
    "files.associations": {
        "*.yml": "yaml",
        "*.yaml": "yaml"
    },
    "terminal.integrated.shell.linux": "/bin/bash",
    "git.autofetch": true,
    "git.confirmSync": false
}
```

### Red Hat Tools Setup

#### rhcase Tool Installation
```bash
# Install rhcase
sudo dnf install -y rhcase

# Configure rhcase
rhcase configure
# Follow prompts with Red Hat SSO credentials

# Test connectivity
rhcase list 838043 --months 1
```

#### Red Hat AI Models API Access
1. Connect to Red Hat VPN
2. Visit: https://developer.models.corp.redhat.com
3. Generate API key for Red Hat Granite models
4. Store securely: `~/.config/pai/secrets/redhat_granite_api_key`

#### Customer Portal Access
1. Connect to Red Hat VPN
2. Visit: https://access.redhat.com
3. Login with Red Hat SSO
4. Navigate to customer portal groups
5. Verify edit permissions

### Python Environment Setup

#### Virtual Environment
```bash
# Create virtual environment
python3 -m venv ~/venv/rfe-automation
source ~/venv/rfe-automation/bin/activate

# Install required packages
pip install requests pyyaml jinja2 python-dateutil redhat-sso-cli
```

#### Git Configuration
```bash
# Configure Git for Red Hat
git config --global user.name "Your Name"
git config --global user.email "your.email@redhat.com"
git config --global url."https://gitlab.cee.redhat.com/".insteadOf "git@gitlab.cee.redhat.com:"
```

### Verification Checklist
- [ ] Cursor IDE installed and configured
- [ ] Python 3.8+ with required packages
- [ ] `rhcase` tool working
- [ ] Red Hat SSO authentication
- [ ] Red Hat AI models API access
- [ ] Customer portal access
- [ ] Git configured for Red Hat repositories
- [ ] Red Hat VPN connectivity

## Implementation Guidelines

### For Developers
- Use this persona when creating user-facing messages and documentation
- Ensure all communications reflect professional competence and helpfulness
- Maintain consistency with Red Hat brand and TAM community standards
- Focus on practical value and time savings for TAMs
- **Always include prerequisite setup instructions** in any deployment guides

### For TAMs
- This persona represents the tool's "personality" when you interact with it
- Expect professional, helpful, and efficient responses
- The tool is designed to augment your expertise, not replace your judgment
- All automated content should be reviewed before customer presentation
- **Follow prerequisite setup exactly** - the tool requires proper configuration to work reliably

### For Leadership
- This persona ensures the tool meets professional standards for TAM community use
- The tool demonstrates clear ROI through time savings and process improvement
- All automation follows Red Hat compliance and security requirements
- The tool is designed for scalability and community adoption
- **Prerequisites are mandatory** - tool will not work without proper setup

---

*This persona ensures the RFE automation tool provides professional, helpful, and efficient assistance to TAMs while maintaining the highest standards of quality, security, and compliance.*
