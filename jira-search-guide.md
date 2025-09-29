# Redis Cluster EDA Jira Search Guide

## 🔧 Setting Up rhcase Jira Access

### Step 1: Create Personal Access Token
1. Go to: https://issues.redhat.com/secure/ViewProfile.jspa?selectedTab=com.atlassian.pats.pats-plugin:jira-user-personal-access-tokens
2. Click "Create token"
3. Name it: "rhcase-cli-access"
4. Copy the generated token

### Step 2: Configure rhcase
```bash
rhcase config setup
# Follow prompts to enter your Jira token
```

## 🎯 Key Search Terms for Redis Cluster EDA

### Primary Jira Projects to Search
- **EDA**: Event-Driven Ansible project
- **AAP**: Ansible Automation Platform  
- **RFE**: Request for Enhancement
- **RHEL**: Enterprise Linux (Redis infrastructure)

### Specific Search Queries to Try

#### Redis Cluster + EDA
```bash
rhcase jira search "project = EDA AND summary ~ 'redis cluster'"
rhcase jira search "project = EDA AND summary ~ 'high availability'"
rhcase jira search "project = AAP AND summary ~ 'event driven ansible HA'"
```

#### High Availability RFEs
```bash  
rhcase jira search "project = RFE AND summary ~ 'Event-Driven Ansible' AND summary ~ 'availability'"
rhcase jira search "project = EDA AND labels = 'high-availability'"
rhcase jira search "project = EDA AND summary ~ 'Redis' AND summary ~ 'cluster'"
```

#### Infrastructure Dependencies
```bash
rhcase jira search "project = EDA AND description ~ 'single point of failure'"
rhcase jira search "project = AAP AND summary ~ 'Redis' AND component = 'Event-Driven Ansible'"
```

## 🌐 Manual Web Search Alternative

### Direct Jira Web Interface
Visit: https://issues.redhat.com/issues/

**Search JQL Queries**:
```jql
project = EDA AND summary ~ "redis cluster" 
project = EDA AND summary ~ "high availability"
project = AAP AND summary ~ "event driven ansible" AND summary ~ "HA"
project = RFE AND summary ~ "Event-Driven Ansible" AND summary ~ "availability"
labels = "high-availability" AND project in (EDA, AAP)
```

### Advanced Search Tips
1. **Use JQL (Jira Query Language)** for precise results
2. **Search both EDA and AAP projects** (cross-project dependencies)  
3. **Look for RFEs** (Request for Enhancement) - these show customer requests
4. **Check labels**: high-availability, clustering, redis, fault-tolerance
5. **Search descriptions** too, not just titles

## 🔍 What to Look For

### Existing Issues
- **Open RFEs**: Customer requests for HA capabilities
- **Backlog Items**: Planned but not scheduled work  
- **Architecture Discussions**: Technical design conversations
- **Dependencies**: Redis clustering infrastructure requirements

### Key Information to Extract
- **Timeline**: Any committed delivery dates
- **Scope**: What HA features are planned
- **Dependencies**: What needs to be built first  
- **Alternatives**: Interim solutions or workarounds
- **Customer Impact**: Which customers are asking

### Business Intelligence
- **Voting/Watchers**: How many people care about these issues
- **Comments**: Product management and engineering discussions
- **Linked Issues**: Related infrastructure work
- **Labels/Components**: Priority and ownership indicators

## 📊 Search Results Analysis Framework

### Priority Indicators
- **High votes/watchers**: Strong customer demand
- **Recent activity**: Active development discussion
- **PM comments**: Product management engagement  
- **Target versions**: Roadmap commitment

### Competitive Intelligence  
- **Customer mentions**: Specific companies asking for this
- **Competitive references**: Mentions of competitor capabilities
- **Escalations**: Issues marked as customer-critical

## 🎯 Product Management Questions Based on Search Results

### If Issues Exist:
- "I see [issue numbers] in the backlog for EDA HA. What's the current timeline?"
- "Issue [number] has [X] votes - is this driving prioritization?"
- "The RFE mentions [customer/scenario] - are we seeing similar requests?"

### If No Issues Found:
- "Should I create an RFE for EDA high availability?"
- "Are HA requirements being tracked in a different project?"
- "Is this functionality planned but not yet documented in Jira?"

## 🛠️ Alternative Research Methods

### Internal Red Hat Resources
- **Confluence**: Search AAP roadmap documents
- **Slack**: #event-driven-ansible, #ansible-automation-platform channels  
- **Product Management**: Direct outreach with customer use cases
- **Engineering**: Technical feasibility discussions

### Customer Feedback Channels
- **Support Cases**: Search for Redis/EDA availability issues
- **Field Feedback**: TAM reports about customer requirements
- **RFE Database**: Official enhancement request tracking

---

## 📋 Action Plan

1. **Set up rhcase Jira access** for comprehensive searching
2. **Run the suggested search queries** above
3. **Document findings** for product management discussions  
4. **Create RFE if needed** based on customer requirements
5. **Use results to strengthen** your HA roadmap conversations

---

**Goal**: Use Jira intelligence to understand what's already planned, what's been requested, and where gaps exist in the EDA HA roadmap.
