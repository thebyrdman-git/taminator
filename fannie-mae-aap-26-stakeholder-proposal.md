# Fannie Mae Automation Platform Modernization
## Stakeholder Decision Brief: AAP 2.6 Upgrade

**Current State**: Red Hat Ansible Automation Platform 2.4  
**Proposed Upgrade**: Version 2.6 (Latest Enterprise Release - **Direct upgrade supported**)  
**Decision Timeline**: [Insert Required Date]  
**Business Impact**: Critical infrastructure modernization ensuring regulatory compliance and operational resilience

> **🚨 URGENT**: Red Hat has announced AAP 2.6 is the **final version** supporting RPM installations. AAP 2.7 will eliminate RPM support entirely.

---

## Executive Summary

Fannie Mae's automation infrastructure requires immediate modernization to maintain vendor support, ensure regulatory compliance, and enable future automation capabilities. **This upgrade from version 2.4 to 2.6 is essential for continued operations.**

**Key Decision**: Choose architecture approach that balances investment with operational requirements.

---

## Why This Upgrade Matters

### 🚨 **Critical Business Drivers**

1. **Last RPM Migration Window**: AAP 2.6 is the **final version** supporting current RPM architecture - AAP 2.7 eliminates RPM entirely
2. **Compliance Risk Mitigation**: Version 2.4 approaches end-of-support, creating regulatory vulnerabilities  
3. **Direct Upgrade Advantage**: Red Hat supports direct 2.4 → 2.6 upgrade, skipping intermediate versions
4. **Future Migration Requirement**: Delay means forced containerized migration in next upgrade cycle
5. **Extended Support**: Version 2.6 provides enterprise support through 2027+

---

## Current Infrastructure

**Existing 2.4 Environment**:
- 7 virtual machines running automation platform
- Components: Database, Controller (2), Hub (1), Execution Nodes (2), Event-Driven Automation (1)
- **Status**: Functional but approaching end-of-life support
- **Database Requirement**: PostgreSQL must be version 15+ for AAP 2.6 compatibility

---

## Upgrade Path Options

Based on [Red Hat's official AAP 2.6 guidance](https://www.redhat.com/en/blog/installation-and-upgrade-guide-ansible-automation-platform-26), Fannie Mae has **two strategic approaches**:

### Option A: RPM-Based Upgrade (Last Opportunity)
**Approach**: Direct upgrade from AAP 2.4 to 2.6 using existing RPM architecture

**Business Case**:
- ✅ **Zero additional infrastructure cost**
- ✅ **Fastest implementation** (2-3 weeks)
- ✅ **Direct upgrade path supported** by Red Hat
- ⚠️ **Final RPM version** - AAP 2.7 will require containerized migration
- ⚠️ **Single point of failure** for some components
- ⚠️ **Limited future flexibility**

**Best For**: Immediate budget constraints requiring minimal change

---

### Option B: Future-Ready Enterprise Architecture ⭐ **RECOMMENDED**
**Approach**: Migrate to containerized AAP 2.6 with enterprise topology

**Business Case**:
- ✅ **Future-Proof**: Containerized platform aligns with Red Hat's roadmap
- ✅ **High Availability**: Zero single points of failure
- ✅ **Enhanced Performance**: 50% faster processing capability
- ✅ **Scalability**: Built for 3-5 year growth without re-architecture
- ✅ **Industry Standard**: Matches Fortune 500 financial services deployments
- ✅ **Rolling Updates**: Zero-downtime maintenance capability

**Investment**: Migration to containerized platform + 4 additional VMs + load balancer

**Best For**: Organizations prioritizing strategic value and operational resilience

---

## Decision Criteria Comparison

| **Factor** | **Option A (RPM Final)** | **Option B (Containerized)** |
|------------|------------------------|---------------------------|
| **Upfront Cost** | $0 additional infrastructure | Migration + 4 VMs + load balancer |
| **Timeline** | 2-3 weeks | 4-5 weeks (includes migration) |
| **Future Path** | **Forced migration required for AAP 2.7** | Future-ready platform |
| **Risk Profile** | Moderate (single points of failure) | Low (full redundancy) |
| **Maintenance Windows** | Longer downtime required | Rolling updates (zero downtime) |
| **Technology Stack** | **Legacy RPM (deprecated)** | Modern containerized (supported) |
| **Total 5-Year Cost** | Lower initial + forced migration later | Higher initial, lower ongoing |

---

## Implementation Approach

### **Phase 1: Preparation** (Week 1)
- Complete backup of existing automation platform
- Infrastructure readiness validation
- Team coordination and change management

### **Phase 2: Upgrade Execution** (Week 2-3)
- Update to latest 2.4 baseline (safety checkpoint)
- Execute 2.6 upgrade automation
- Component validation and testing

### **Phase 3: Validation & Handoff** (Week 3-4)
- Business process validation
- Performance verification
- Operational team training

**Risk Mitigation**: Full restore capability maintained throughout process with Red Hat Technical Account Management support.

### **Critical Pre-Upgrade Requirements**
Based on [Red Hat's AAP 2.6 requirements](https://www.redhat.com/en/blog/installation-and-upgrade-guide-ansible-automation-platform-26):

- **PostgreSQL Database**: Must be version 15, 16, or 17 (automatic upgrade if managed by installer)
- **RHEL Operating System**: AAP 2.6 requires RHEL 9 minimum (RHEL 10 supported for containerized)
- **Direct Upgrade**: AAP 2.4 → 2.6 upgrade path is officially supported

---

## Resource Requirements

**Red Hat Support** (Included):
- ✅ Technical Account Management guidance
- ✅ Ansible engineering support
- ✅ 24/7 support during implementation

**Fannie Mae Teams**:
- Infrastructure team (backup/restore, upgrade execution)
- Database team (Option B only - external DB configuration)
- Network team (Option B only - load balancer setup)

**Optional Professional Services**: Red Hat can provide hands-on implementation assistance (separate engagement)

---

## Financial Investment Summary

| **Component** | **Option A** | **Option B** |
|---------------|--------------|--------------|
| **Software Licensing** | $0 (covered by existing Enterprise Agreement) | $0 (covered by existing Enterprise Agreement) |
| **Infrastructure** | $0 | 4 VMs: ~$[X]/month x 48 months = $[Y] total |
| **Implementation** | TAM support (included) | TAM support + optional Professional Services |
| **Total 4-Year TCO** | $0 | $[Y] + implementation services |

---

## Risk Assessment

| **Risk Scenario** | **Option A Impact** | **Option B Mitigation** |
|-------------------|-------------------|------------------------|
| **Component Failure** | Extended downtime | Automatic failover |
| **Peak Processing** | Performance degradation | Load distribution |
| **Security Incident** | Single point vulnerability | Isolated component recovery |
| **Compliance Audit** | Basic evidence | Enhanced audit trail |
| **No Upgrade (Status Quo)** | **HIGH RISK**: Loss of vendor support, compliance violations, security vulnerabilities |

---

## Strategic Recommendation

**Red Hat Technical Account Management strongly recommends Option B (Containerized)** based on [official Red Hat guidance](https://www.redhat.com/en/blog/installation-and-upgrade-guide-ansible-automation-platform-26):

### **Critical Strategic Factors**:

1. **Mandatory Migration Window**: AAP 2.6 is the **final RPM release** - delaying means forced migration under pressure
2. **Red Hat's Roadmap Alignment**: Containerized installations are Red Hat's supported future
3. **One-Time Investment**: Avoid the guaranteed disruption and cost of forced migration in 18-24 months
4. **Risk Mitigation**: Eliminates single points of failure in business-critical automation
5. **Competitive Positioning**: Matches industry standards across financial services

### **Total Cost Analysis**:
- **Option A**: Lower cost now + **guaranteed migration cost later** + operational disruption during forced transition
- **Option B**: Higher initial investment + **no future migration required** + enhanced operational capabilities

**The RPM deprecation makes Option A a temporary solution with guaranteed future disruption. Option B represents strategic infrastructure investment.**

---

## Next Steps

**Upon Architecture Approval**:
1. Finalize Option A or Option B selection
2. Schedule maintenance window coordination
3. Provision additional infrastructure (Option B only)
4. Execute Phase 1 preparation activities
5. Coordinate implementation timeline

---

## Success Metrics

- ✅ Zero unplanned automation downtime post-upgrade
- ✅ 100% existing workflow compatibility maintained
- ✅ Full regulatory compliance validation within 30 days
- ✅ Enhanced performance benchmarks achieved (Option B)

---

**Document Purpose**: Architecture decision and timeline approval  
**Contact**: Red Hat Account Team for questions or Professional Services consultation  
**Decision Required**: [Insert Date]

---

## References

This proposal is based on official Red Hat guidance and documentation:

- [Red Hat Blog: Installation and upgrade guide for Ansible Automation Platform 2.6](https://www.redhat.com/en/blog/installation-and-upgrade-guide-ansible-automation-platform-26) (October 2025)
- [Red Hat Documentation: Ansible Automation Platform 2.6](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.6)
- Red Hat Technical Account Management recommendations

---

*Executive Brief - Fannie Mae Automation Platform Modernization*  
*Prepared by Red Hat Technical Account Management*  
*Updated with AAP 2.6 Official Guidance - October 2025*
