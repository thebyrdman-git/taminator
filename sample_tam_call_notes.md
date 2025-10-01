## Wells Fargo TAM Call Notes - October 1, 2025

### Call Details
- **Duration**: 45 minutes
- **Attendees**: Jimmy Byrd (Red Hat TAM), Sarah Johnson (Wells Fargo IT), Mike Chen (DevOps Lead)

### Agenda Items
1. Review current support cases
2. Discuss podman upgrade issues
3. Job failure troubleshooting update
4. Q4 automation planning

### Discussion Points

#### Active Cases Review
- Case 04247094: podman 4.6.1-8 upgrade to 4.9.4-20 - Waiting on customer testing
- Case 04213804: Job ran for 10 hours and failed without error message - Investigating logs
- Case 04165187: High risk security vulnerabilities in ee-supported-rhel8 - Patch testing in progress

#### Recent Issues & Resolutions
- **Podman Upgrade**: Customer experiencing container startup issues after upgrade
  - Root cause identified as configuration mismatch
  - Provided updated configuration template
- **Job Timeout Issue**: Long-running playbooks timing out unexpectedly
  - Adjusted timeout settings in AAP configuration
  - Customer to test with next scheduled job run

#### Upcoming Projects
- **Q4 Automation Expansion**: Planning to automate 15 additional workflows
  - Timeline: November 2025 start
  - Need capacity planning discussion with Red Hat
- **Security Hardening Initiative**: Implementing enhanced security policies
  - JIRA AAPRFE-875 for API rate limiting integration
  - Target completion: December 2025

### Action Items
- [ ] Follow up on case 04247094 podman testing - Owner: Sarah Johnson - Due: October 8, 2025
- [ ] Provide job timeout monitoring script - Owner: Jimmy Byrd - Due: October 3, 2025
- [ ] Schedule Q4 capacity planning call - Owner: Mike Chen - Due: October 10, 2025
- [ ] Review security patch testing results - Owner: Sarah Johnson - Due: October 5, 2025

### Questions & Answers
- Q: Can we get priority support for the podman upgrade issue?
- A: Case 04247094 is already marked as High severity. Will escalate if testing reveals additional complications.

- Q: What's the timeline for API rate limiting feature (AAPRFE-875)?
- A: Currently in backlog, will check with product team for updated timeline.

### Next Steps
1. Monitor progress on active troubleshooting cases
2. Schedule Q4 planning session with broader team
3. Continue security vulnerability remediation
4. Follow up on automation expansion requirements

### Next Call
- **Scheduled**: October 8, 2025 at 2:00 PM EST
- **Focus**: Podman upgrade resolution, Q4 planning deep dive

---

*Template for Wells Fargo TAM call notes*
*Customize sections as needed for your specific call format*
