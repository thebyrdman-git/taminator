# 🏗️ RFE Automation - System Architecture

**Technical overview for TAMs and system administrators**

---

## 🎯 Architecture Overview

The RFE Automation System is designed as a modular, resilient, and scalable solution that automates the entire RFE/Bug tracking workflow for TAMs.

```
┌─────────────────────────────────────────────────────────────┐
│                    RFE AUTOMATION SYSTEM                    │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Data      │  │  Content    │  │     Portal          │  │
│  │ Discovery   │→ │ Generation  │→ │   Publishing        │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│         │                 │                     │           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Monitoring  │  │    Error    │  │    Scheduling       │  │
│  │ & Alerting  │  │  Handling   │  │  & Automation       │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Core Components

### 1. Data Discovery Layer
**Purpose**: Automatically discover RFE and Bug cases for customers

**Components**:
- **`rhcase` Integration**: Primary data source for case discovery
- **JIRA API Client**: Optional enrichment for detailed ticket information
- **External Trackers Parser**: Extracts JIRA references from case data
- **SBR Group Filtering**: Ensures accurate Ansible case identification

**Key Files**:
- `src/rhcase_rfe_templated.py` - Main case discovery logic
- `src/jira_api_v2_integration.py` - JIRA API integration
- `src/external_trackers_parser.py` - External tracker parsing

### 2. Content Generation Layer
**Purpose**: Transform raw case data into formatted portal content

**Components**:
- **Template Renderer**: Customer-specific content formatting
- **Table Generator**: Creates structured markdown tables
- **Priority Manager**: Assigns and manages case priorities
- **Content Merger**: Intelligently merges new content with existing portal pages

**Key Files**:
- `src/customer_template_renderer.py` - Template-based content generation
- `config/customer_templates.yaml` - Customer-specific templates
- `src/intelligent_rfe_merger.py` - Content merging logic

### 3. Portal Publishing Layer
**Purpose**: Deliver content to customer portal pages

**Components**:
- **API Client**: Direct API posting to Red Hat Customer Portal
- **Browser Automation**: Fallback for direct page editing
- **Notification Handler**: Manages customer notification settings
- **Content Validator**: Ensures content integrity before posting

**Key Files**:
- `src/redhat_cppg_api_client.py` - Customer Portal Groups API
- `src/api_portal_updater.py` - Hybrid API/browser posting
- `src/safe_portal_updater.py` - Browser automation with safety features

### 4. Monitoring & Alerting Layer
**Purpose**: Ensure system reliability and notify of issues

**Components**:
- **Execution Monitor**: Tracks automation success/failure
- **Alert Manager**: File-based and email alerting system
- **Performance Tracker**: Monitors execution times and success rates
- **Health Checker**: Validates system components

**Key Files**:
- `src/rfe_monitoring_system.py` - Core monitoring logic
- `bin/pai-alerts` - Alert management interface
- `src/rfe_error_handler.py` - Enhanced error handling

### 5. Error Handling Layer
**Purpose**: Provide resilient operation with graceful degradation

**Components**:
- **Retry Logic**: Exponential backoff for transient failures
- **Circuit Breaker**: Prevents cascade failures
- **Fallback Strategies**: Graceful degradation options
- **Recovery Mechanisms**: Automatic error recovery

**Key Files**:
- `src/rfe_error_handler.py` - Comprehensive error handling
- Integrated into all major components

### 6. Scheduling & Automation Layer
**Purpose**: Enable hands-off daily operation

**Components**:
- **Cron Manager**: Automated job scheduling
- **Task Orchestrator**: Coordinates multi-customer automation
- **Maintenance Scheduler**: System cleanup and optimization
- **Health Validator**: Pre-execution system checks

**Key Files**:
- `bin/pai-rfe-schedule` - Scheduling management
- `config/rfe-automation-cron.txt` - Cron job definitions
- `bin/pai-maintenance` - System maintenance

---

## 🔄 Data Flow

### Daily Automation Workflow

```
1. SCHEDULED TRIGGER (9:00 AM EST)
   ↓
2. SYSTEM HEALTH CHECK
   ├─ Validate components
   ├─ Check connectivity
   └─ Verify configurations
   ↓
3. CUSTOMER PROCESSING (for each customer)
   ├─ Discover cases via rhcase
   ├─ Filter RFE/Bug cases
   ├─ Enrich with JIRA data
   └─ Generate portal content
   ↓
4. PORTAL PUBLISHING
   ├─ Attempt API posting
   ├─ Fallback to browser automation
   └─ Verify successful posting
   ↓
5. MONITORING & ALERTING
   ├─ Log execution results
   ├─ Send success/failure alerts
   └─ Update performance metrics
```

### Error Handling Flow

```
ERROR DETECTED
   ↓
CLASSIFY ERROR SEVERITY
   ├─ Low: Network timeouts, rate limits
   ├─ Medium: Authentication issues, API errors
   ├─ High: Permission denied, config errors
   └─ Critical: System failures, security issues
   ↓
APPLY RETRY STRATEGY
   ├─ Exponential backoff
   ├─ Circuit breaker check
   └─ Maximum attempts limit
   ↓
EXECUTE FALLBACK STRATEGY
   ├─ Use cached data
   ├─ Generate manual instructions
   └─ Create file-based output
   ↓
ALERT & RECOVER
   ├─ Send appropriate alerts
   ├─ Log detailed error info
   └─ Attempt automatic recovery
```

---

## 🗄️ Data Storage

### Configuration Storage
- **Location**: `config/` directory
- **Format**: YAML and JSON files
- **Purpose**: Customer configurations, templates, deployment settings

### Temporary Data
- **Location**: `/tmp/` directory
- **Retention**: 7-30 days (configurable)
- **Purpose**: Execution logs, generated content, cached data

### Alert Storage
- **Location**: `/tmp/rfe-alerts/`
- **Format**: Text files and JSON summaries
- **Purpose**: Alert history, dashboard data, troubleshooting info

### No Persistent Database
- **Design Choice**: Stateless operation
- **Benefits**: Simplified deployment, reduced maintenance
- **Data Sources**: Always fetch fresh data from authoritative sources

---

## 🔐 Security Architecture

### Authentication
- **Red Hat SSO**: Primary authentication mechanism
- **Personal Access Tokens**: For JIRA API access (optional)
- **Session Management**: Secure token handling and refresh

### Data Protection
- **No Sensitive Storage**: No customer data stored persistently
- **Secure Transmission**: HTTPS for all API communications
- **Access Control**: Leverages existing Red Hat permissions

### Audit Trail
- **Comprehensive Logging**: All actions logged with timestamps
- **Alert History**: Permanent record of system events
- **Execution Tracking**: Detailed performance and success metrics

---

## 📈 Scalability Design

### Horizontal Scaling
- **Multi-Customer**: Designed for 100+ customers per TAM
- **Multi-TAM**: System can be deployed across entire organization
- **Resource Efficient**: Minimal system resource requirements

### Performance Optimization
- **Parallel Processing**: Multiple customers processed concurrently
- **Intelligent Caching**: Reduces redundant API calls
- **Circuit Breakers**: Prevents resource exhaustion

### Deployment Flexibility
- **Single-User**: Individual TAM deployment
- **Team Deployment**: Shared system for TAM teams
- **Enterprise Scale**: Organization-wide deployment

---

## 🔧 Integration Points

### Red Hat Systems
- **Customer Portal**: Primary integration for content publishing
- **JIRA**: Optional integration for enhanced ticket data
- **rhcase Tool**: Core dependency for case discovery
- **Red Hat SSO**: Authentication and authorization

### External Systems
- **Customer Portals**: Content delivery destination
- **Email Systems**: Alert delivery mechanism
- **Monitoring Tools**: Integration-ready logging and metrics

---

## 🛠️ Maintenance Architecture

### Automated Maintenance
- **Daily**: Temp file cleanup, health checks
- **Weekly**: Alert cleanup, performance reports
- **Monthly**: Log rotation, system optimization

### Manual Maintenance
- **Configuration Updates**: Customer additions/changes
- **Template Customization**: Portal content formatting
- **System Upgrades**: Component updates and improvements

### Monitoring Points
- **System Health**: Component availability and performance
- **Data Quality**: Case discovery accuracy and completeness
- **User Experience**: Portal update success and timing

---

## 🔍 Troubleshooting Architecture

### Diagnostic Tools
- **Health Checkers**: Validate system components
- **Connectivity Tests**: Verify external system access
- **Configuration Validators**: Check setup correctness

### Debug Information
- **Detailed Logging**: Comprehensive execution traces
- **Error Classification**: Structured error reporting
- **Performance Metrics**: Timing and success rate data

### Recovery Mechanisms
- **Automatic Recovery**: Self-healing for common issues
- **Fallback Modes**: Graceful degradation options
- **Manual Override**: Administrative control when needed

---

## 📊 Metrics & Analytics

### Performance Metrics
- **Execution Time**: Per-customer and overall timing
- **Success Rate**: Automation reliability percentage
- **Error Frequency**: Failure pattern analysis

### Business Metrics
- **Time Savings**: Hours saved per TAM per day
- **Customer Coverage**: Percentage of customers automated
- **Adoption Rate**: TAM deployment and usage statistics

### System Metrics
- **Resource Usage**: CPU, memory, disk utilization
- **Network Performance**: API response times and reliability
- **Component Health**: Individual system component status

---

## 🚀 Future Architecture Considerations

### Planned Enhancements
- **Real-time Updates**: Webhook-based immediate updates
- **Advanced Analytics**: Predictive insights and trends
- **Mobile Interface**: Mobile-friendly management interface

### Scalability Improvements
- **Microservices**: Component separation for better scaling
- **Container Deployment**: Docker/Kubernetes support
- **Cloud Integration**: Cloud-native deployment options

### Integration Expansions
- **Additional Data Sources**: Broader case discovery
- **Enhanced Portals**: More customer portal integrations
- **Workflow Integration**: Integration with TAM workflow tools

---

**🏗️ This architecture provides a robust, scalable, and maintainable foundation for automating RFE management across the entire TAM organization.**

---

*RFE Automation System - System Architecture*  
*Version 1.0 - Created for Global TAM Deployment*
