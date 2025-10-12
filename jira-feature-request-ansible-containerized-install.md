# JIRA Feature Request: Publish ansible.containerized_install Collection

## Summary
Publish ansible.containerized_install collection to Automation Hub for direct consumption in automated AAP deployment workflows

## Problem Statement
Currently, the `ansible.containerized_install` collection is only available within the Red Hat AAP setup-bundle, preventing direct consumption in automated deployment pipelines. While all other collections in the setup-bundle are published externally, this critical collection remains inaccessible for automation use cases.

## Business Impact
- **Automation Limitations**: Prevents integration with existing infrastructure-as-code workflows
- **Operational Inefficiency**: Requires manual collection extraction and custom hub management
- **Scalability Constraints**: Limits adoption of automated AAP deployment patterns
- **Customer Enablement**: Blocks customers from leveraging modern DevOps practices for AAP deployments

## Technical Requirements

**Current State:**
- Collection exists within setup-bundle alongside published collections
- Manual extraction and custom hub upload required for automation use
- Validated internally but requires workaround implementation

**Desired State:**
- Direct collection availability via Automation Hub or similar Red Hat distribution channel
- Standard `ansible-galaxy collection install` compatibility
- Version management and dependency resolution support

## Use Case Details

**Automated Deployment Workflow:**
1. Infrastructure provisioning via ansible-local
2. Collection installation via `ansible-galaxy collection install`
3. Inventory compilation and validation
4. Playbook execution from within collections
5. Infrastructure configuration and AAP deployment

**Current Workaround:**
- Manual collection extraction from setup-bundle
- Custom hub deployment (POC → Satellite migration planned)
- Functional but not sustainable for production use

## Technical Validation
- Internal testing confirms collection functionality
- Integration with existing automation framework validated
- Version constraint management tested and working

## Acceptance Criteria
- [ ] Collection available via standard Red Hat distribution channels
- [ ] Compatible with `ansible-galaxy collection install` workflow
- [ ] Version management and dependency resolution functional
- [ ] Documentation available for collection usage
- [ ] Integration with existing automation frameworks supported

## Additional Considerations
- Collection may require additional packaging considerations for external distribution
- Dependencies and version constraints need validation
- Documentation updates may be required for standalone usage

## Priority Justification
This enhancement enables customers to adopt modern DevOps practices for AAP deployment, aligns with Red Hat's automation-first strategy, and removes barriers to automated infrastructure management.
