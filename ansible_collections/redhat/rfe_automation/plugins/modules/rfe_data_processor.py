#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: rfe_data_processor
short_description: Process and categorize RFE/Bug case data
version_added: "1.0.0"
description:
    - This module processes raw case data and categorizes it into RFEs, bugs, and active cases
    - Supports external tracker detection and intelligent filtering
    - Returns structured data for report generation
author:
    - Red Hat TAM Operations
options:
    cases:
        description:
            - List of case data to process
        required: true
        type: list
        elements: dict
    case_types:
        description:
            - List of case types to consider for RFE/Bug categorization
        required: false
        type: list
        elements: str
        default: ["Feature / Enhancement Request", "Defect / Bug"]
    rfe_keywords:
        description:
            - Keywords that indicate RFE cases in subject
        required: false
        type: list
        elements: str
        default: ["[RFE]"]
    bug_keywords:
        description:
            - Keywords that indicate bug cases in subject
        required: false
        type: list
        elements: str
        default: ["[BUG]"]
    external_tracker_patterns:
        description:
            - Patterns to detect external tracker references
        required: false
        type: list
        elements: str
        default: ["issues.redhat.com", "jira.redhat.com"]
    priority_components:
        description:
            - Priority SBR components for filtering
        required: false
        type: list
        elements: str
        default: []
'''

EXAMPLES = r'''
# Process case data
- name: Process case data
  rfe_data_processor:
    cases: "{{ raw_cases }}"
    case_types: ["Feature / Enhancement Request", "Defect / Bug"]
    rfe_keywords: ["[RFE]"]
    bug_keywords: ["[BUG]"]
    external_tracker_patterns: ["issues.redhat.com", "jira.redhat.com"]
    priority_components: ["Ansible"]
  register: processed_data

# Process with custom keywords
- name: Process with custom keywords
  rfe_data_processor:
    cases: "{{ raw_cases }}"
    rfe_keywords: ["[RFE]", "[ENHANCEMENT]", "[FEATURE]"]
    bug_keywords: ["[BUG]", "[DEFECT]", "[ISSUE]"]
  register: processed_data
'''

RETURN = r'''
active_rfes:
    description: List of active RFE cases
    returned: always
    type: list
    elements: dict
active_bugs:
    description: List of active bug cases
    returned: always
    type: list
    elements: dict
closed_cases:
    description: List of closed cases
    returned: always
    type: list
    elements: dict
all_active_cases:
    description: List of all active cases (excluding RFE/Bug by title)
    returned: always
    type: list
    elements: dict
priority_active_cases:
    description: List of active cases in priority components
    returned: always
    type: list
    elements: dict
cases_with_external_trackers:
    description: List of cases with external tracker references
    returned: always
    type: list
    elements: dict
statistics:
    description: Processing statistics
    returned: always
    type: dict
    contains:
        total_cases:
            description: Total cases processed
            type: int
        active_rfes_count:
            description: Number of active RFEs
            type: int
        active_bugs_count:
            description: Number of active bugs
            type: int
        closed_cases_count:
            description: Number of closed cases
            type: int
        external_tracker_cases_count:
            description: Number of cases with external trackers
            type: int
        all_active_cases_count:
            description: Number of all active cases
            type: int
        priority_active_cases_count:
            description: Number of priority active cases
            type: int
available_case_types:
    description: List of available case types in the data
    returned: always
    type: list
    elements: str
'''

import re
from ansible.module_utils.basic import AnsibleModule


def detect_case_type_by_subject(subject, rfe_keywords, bug_keywords):
    """Detect case type based on subject keywords"""
    if not subject:
        return None
    
    subject_upper = subject.upper()
    
    # Check for RFE keywords
    for keyword in rfe_keywords:
        if keyword.upper() in subject_upper:
            return 'rfe'
    
    # Check for bug keywords
    for keyword in bug_keywords:
        if keyword.upper() in subject_upper:
            return 'bug'
    
    return None


def has_external_tracker_reference(case, patterns):
    """Check if case has external tracker references"""
    if not patterns:
        return False
    
    # Check subject
    subject = case.get('subject', '')
    if subject:
        for pattern in patterns:
            if pattern.lower() in subject.lower():
                return True
    
    # Check description
    description = case.get('description', '')
    if description:
        for pattern in patterns:
            if pattern.lower() in description.lower():
                return True
    
    # Check tags
    tags = case.get('tags', '')
    if tags:
        for pattern in patterns:
            if pattern.lower() in tags.lower():
                return True
    
    return False


def get_available_case_types(cases):
    """Get list of available case types in the data"""
    case_types = set()
    for case in cases:
        case_type = case.get('caseType')
        if case_type:
            case_types.add(case_type)
    return sorted(list(case_types))


def process_cases(cases, case_types, rfe_keywords, bug_keywords, external_tracker_patterns, priority_components):
    """Process and categorize cases"""
    active_rfes = []
    active_bugs = []
    closed_cases = []
    all_active_cases = []
    priority_active_cases = []
    cases_with_external_trackers = []
    
    # Get available case types
    available_case_types = get_available_case_types(cases)
    
    for case in cases:
        is_closed = case.get('isClosed', False)
        subject = case.get('subject', '')
        case_type = case.get('caseType', '')
        sbr_group = case.get('sbrGroup', '')
        
        # Detect external tracker references
        if has_external_tracker_reference(case, external_tracker_patterns):
            cases_with_external_trackers.append(case)
        
        # Categorize cases
        if is_closed:
            closed_cases.append(case)
        else:
            # Detect type by subject keywords
            subject_type = detect_case_type_by_subject(subject, rfe_keywords, bug_keywords)
            
            # Categorize based on case type and subject
            if case_type in case_types or subject_type:
                if case_type == 'Feature / Enhancement Request' or subject_type == 'rfe':
                    active_rfes.append(case)
                elif case_type == 'Defect / Bug' or subject_type == 'bug':
                    active_bugs.append(case)
                else:
                    # Default to RFE for other case types with RFE keywords
                    if subject_type == 'rfe':
                        active_rfes.append(case)
                    elif subject_type == 'bug':
                        active_bugs.append(case)
                    else:
                        # Include in active cases if not explicitly RFE/Bug
                        all_active_cases.append(case)
                        if sbr_group in priority_components:
                            priority_active_cases.append(case)
            else:
                # Include in active cases if not explicitly RFE/Bug
                all_active_cases.append(case)
                if sbr_group in priority_components:
                    priority_active_cases.append(case)
    
    # Remove cases with external trackers from active cases
    external_tracker_case_numbers = {case.get('caseNumber') for case in cases_with_external_trackers}
    all_active_cases = [case for case in all_active_cases if case.get('caseNumber') not in external_tracker_case_numbers]
    priority_active_cases = [case for case in priority_active_cases if case.get('caseNumber') not in external_tracker_case_numbers]
    
    # Calculate statistics
    statistics = {
        'total_cases': len(cases),
        'active_rfes_count': len(active_rfes),
        'active_bugs_count': len(active_bugs),
        'closed_cases_count': len(closed_cases),
        'external_tracker_cases_count': len(cases_with_external_trackers),
        'all_active_cases_count': len(all_active_cases),
        'priority_active_cases_count': len(priority_active_cases)
    }
    
    return {
        'active_rfes': active_rfes,
        'active_bugs': active_bugs,
        'closed_cases': closed_cases,
        'all_active_cases': all_active_cases,
        'priority_active_cases': priority_active_cases,
        'cases_with_external_trackers': cases_with_external_trackers,
        'statistics': statistics,
        'available_case_types': available_case_types
    }


def main():
    """Main module function"""
    module = AnsibleModule(
        argument_spec=dict(
            cases=dict(type='list', elements='dict', required=True),
            case_types=dict(type='list', elements='str', default=['Feature / Enhancement Request', 'Defect / Bug']),
            rfe_keywords=dict(type='list', elements='str', default=['[RFE]']),
            bug_keywords=dict(type='list', elements='str', default=['[BUG]']),
            external_tracker_patterns=dict(type='list', elements='str', default=['issues.redhat.com', 'jira.redhat.com']),
            priority_components=dict(type='list', elements='str', default=[])
        ),
        supports_check_mode=True
    )
    
    # Get parameters
    cases = module.params['cases']
    case_types = module.params['case_types']
    rfe_keywords = module.params['rfe_keywords']
    bug_keywords = module.params['bug_keywords']
    external_tracker_patterns = module.params['external_tracker_patterns']
    priority_components = module.params['priority_components']
    
    # In check mode, return without making changes
    if module.check_mode:
        module.exit_json(
            changed=False,
            active_rfes=[],
            active_bugs=[],
            closed_cases=[],
            all_active_cases=[],
            priority_active_cases=[],
            cases_with_external_trackers=[],
            statistics={},
            available_case_types=[],
            msg="Check mode - no changes made"
        )
    
    try:
        # Process cases
        result = process_cases(
            cases, case_types, rfe_keywords, bug_keywords,
            external_tracker_patterns, priority_components
        )
        
        # Prepare result
        result.update({
            'changed': False,
            'msg': f"Processed {len(cases)} cases into {result['statistics']['active_rfes_count']} RFEs, {result['statistics']['active_bugs_count']} bugs, and {result['statistics']['all_active_cases_count']} active cases"
        })
        
        module.exit_json(**result)
        
    except Exception as e:
        module.fail_json(msg=f"Unexpected error processing cases: {e}")


if __name__ == '__main__':
    main()
