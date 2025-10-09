# JP Morgan Chase - RFE/Bug Tracker Report (Organized by JIRA Components)
**Generated**: January 10, 2025  
**Time Period**: All Active Cases  
**SBR Groups**: Ansible  
**Account Number**: 334224

## Executive Summary
- **Total Active Cases**: 26 (19 RFE, 2 Bug, 5 Other)
- **JIRA Status**: Various (New, In Progress, Under Review, etc.)
- **Cases In Progress**: 0

---

# 🔧 **REQUEST FOR ENHANCEMENTS (RFEs)**

## 🔧 **API & Integration** (5 cases)
*Component: API, REST API, Integration*

| Case Number | Summary | JIRA Status | Created |
|-------------|---------|-------------|---------|
| 03684788 | [RFE] Create Inventory and populate inventory in one API call | New | 2023-12-07 |
| 03684782 | [RFE] Enable API components to be created by names rather than INT value of ID | New | 2023-12-07 |
| 03858389 | [RFE] Downloading the output of a job in the AAP controller API /api/v2/jobs/<jobid>/stdout needs a download as zip | New | 2024-06-25 |
| 03618756 | [RFE] Add method for atomic creation of AAP content & execution | New | 2023-09-20 |
| 04264385 | [RFE] Add API Authorization through External (i.e. AzureAD) OAuth Token | New | 2025-09-25 |

**Business Impact**: Enhanced API efficiency, reduced network overhead, simplified integration workflows, OAuth integration

---

## 🔐 **Security & Authentication** (4 cases)
*Component: Security, Authentication, LDAP, Encryption*

| Case Number | Summary | JIRA Status | Created |
|-------------|---------|-------------|---------|
| 03208295 | [RFE] Kerberizing Authentication to the database (postgres) | New | 2023-10-09 |
| 04197938 | [RFE] PostgreSQL Password Encryption and HashiCorp Vault Integration | New | 2025-07-11 |
| 04160410 | [RFE] Native Integration of HashiCorp Vault for Secure System Account Management and Encryption Key Storage during Installation | New | 2025-10-09 |
| 04156105 | [RFE] Extra Vars Need to be Encrypted | New | 2025-10-09 |

**Business Impact**: Meeting bank security standards, audit compliance, credential encryption, database security

---

## 🏗️ **Infrastructure & Deployment** (4 cases)
*Component: Infrastructure, Deployment, Execution Environment, Kubernetes*

| Case Number | Summary | JIRA Status | Created |
|-------------|---------|-------------|---------|
| 04107348 | [RFE] Extend AAP functionality with execution nodes on native Kubernetes | New | 2025-10-09 |
| 03810727 | [RFE] Ability to add execution nodes after the initial install | New | 2024-05-06 |
| 04010595 | [RFE] Enable AAP Execution Environments to manage credentials where restrictive local regulations apply | New | 2024-12-11 |
| 03563047 | [RFE] Make the mesh aware of which execution node can reach which managed nodes | New | 2025-10-09 |

**Business Impact**: Dynamic infrastructure scaling, Kubernetes integration, compliance with local regulations, network topology awareness

---

## 🔍 **Monitoring & Observability** (2 cases)
*Component: Monitoring, Metrics, Observability*

| Case Number | Summary | JIRA Status | Created |
|-------------|---------|-------------|---------|
| 03616800 | [RFE] Add a method for monitoring uwsgi workers in Controller | New | 2025-10-09 |
| 03957320 | [RFE] Request for AAP to accurately report hung receptor service state | New | 2025-10-09 |

**Business Impact**: Enhanced monitoring capabilities, service health visibility, operational insights

---

## 🔔 **Notifications & Webhooks** (2 cases)
*Component: Notifications, Webhooks, Templates*

| Case Number | Summary | JIRA Status | Created |
|-------------|---------|-------------|---------|
| 03677529 | [RFE] Notification Template & Credentials | New | 2025-10-09 |
| 03862331 | [RFE] Webhook notification retry option | New | 2025-10-09 |

**Business Impact**: Improved notification reliability, template management, webhook resilience

---

## 🔑 **Credentials & Authentication** (2 cases)
*Component: Credentials, Custom Types, Authentication*

| Case Number | Summary | JIRA Status | Created |
|-------------|---------|-------------|---------|
| 03675254 | [RFE] Custom Credential Type doesn't not allow the key of ask_at_runtime for prompt at launch custom credentials | New | 2025-10-09 |
| 03846714 | [RFE] Want automation hub to ingest the AUTH_LDAP_BIND_PASSWORD value whenever it's updated | New | 2024-06-12 |

**Business Impact**: Enhanced credential management, LDAP integration, runtime credential prompts

---

## 📦 **Backport & Maintenance** (1 case)
*Component: Backport, Maintenance, Version Management*

| Case Number | Summary | JIRA Status | Created |
|-------------|---------|-------------|---------|
| 03533803 | [RFE] Backport Request: Add instance_group to bulk api feature to 4.4 branch | New | 2025-10-09 |

**Business Impact**: Feature availability in supported versions, maintenance continuity

---

# 🐛 **BUGS**

## 🔧 **API & Integration** (1 case)
*Component: API, REST API, Integration*

| Case Number | Summary | JIRA Status | Created |
|-------------|---------|-------------|---------|
| 04173350 | [BUG] Task stdout escapes quotes twice in Controller API api/v2/jobs/{id}/stdout/?format=txt | New | 2025-10-09 |

**Business Impact**: API output formatting issues affecting data integrity

---

## 🐛 **Build & Development Tools** (1 case)
*Component: Build Tools, Development, ansible-builder*

| Case Number | Summary | JIRA Status | Created |
|-------------|---------|-------------|---------|
| 03662419 | [BUG] ansible-builder doesn't seem to honor the dns=x.x.x.x flag | New | 2023-11-10 |

**Business Impact**: DNS configuration issues in containerized environments

---

## 📊 **Component Distribution Analysis**

### **RFE Distribution**
| Component Category | RFEs | Percentage | Key Themes |
|-------------------|------|------------|------------|
| **API & Integration** | 5 | 26% | Atomic operations, OAuth, data export, API efficiency |
| **Security & Authentication** | 4 | 21% | Compliance, encryption, Vault integration, database security |
| **Infrastructure & Deployment** | 4 | 21% | Kubernetes, scaling, regulatory compliance, network topology |
| **Monitoring & Observability** | 2 | 11% | Service monitoring, health visibility |
| **Notifications & Webhooks** | 2 | 11% | Reliability, template management |
| **Credentials & Authentication** | 2 | 11% | Credential management, LDAP integration |
| **Backport & Maintenance** | 1 | 5% | Version management |

### **Bug Distribution**
| Component Category | Bugs | Percentage | Key Themes |
|-------------------|------|------------|------------|
| **API & Integration** | 1 | 50% | API output formatting |
| **Build & Development Tools** | 1 | 50% | Container configuration |

## 🎯 **Strategic Priorities by Component**

### **High Priority Components**
1. **API & Integration** - Core platform functionality for JPMC's automation ecosystem
2. **Security & Authentication** - Critical for financial services compliance
3. **Infrastructure & Deployment** - Kubernetes integration and regulatory compliance

### **Medium Priority Components**  
4. **Monitoring & Observability** - Operational excellence and service visibility
5. **Notifications & Webhooks** - Communication reliability
6. **Credentials & Authentication** - Enhanced credential management

### **Support Components**
7. **Backport & Maintenance** - Version continuity
8. **Build & Development Tools** - Development workflow optimization

---
**🤖 Automated Update via Red Hat Customer Portal API**  
*Last updated: January 10, 2025*  
*Generated by: RFE Discussion API Client*  
*Organized by: JIRA Component Categories*
