#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Red Hat TAM Operations
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: rfe_external_tracker
short_description: Detects external tracker references in case data
version_added: "1.0.0"
description:
    - Searches for JIRA and other external tracker references in case content
    - Supports multiple search patterns and fields
    - Provides detailed detection results and statistics
author:
    - "Red Hat TAM Operations"
options:
    case_data:
        description:
            - List of case data to analyze
        required: true
        type: list
        elements: dict
    search_patterns:
        description:
            - List of regex patterns to search for
        required: false
        type: list
        elements: str
        default: ["issues\\.redhat\\.com", "jira\\.redhat\\.com"]
    search_fields:
        description:
            - List of case fields to search in
        required: false
        type: list
        elements: str
        default: ["subject", "description", "tags"]
    case_sensitive:
        description:
            - Whether search is case sensitive
        required: false
        type: bool
        default: false
    include_closed_cases:
        description:
            - Whether to include closed cases in analysis
        required: false
        type: bool
        default: false
'''

EXAMPLES = r'''
- name: Detect external tracker references
  redhat.rfe_automation.rfe_external_tracker:
    case_data: "{{ all_cases }}"
    search_patterns:
      - "issues\\.redhat\\.com"
      - "jira\\.redhat\\.com"
    search_fields: ["subject", "description", "tags"]
    case_sensitive: false
    include_closed_cases: false
  register: tracker_results

- name: Display detection results
  debug:
    msg: "Found {{ tracker_results.cases_with_trackers | length }} cases with external trackers"
'''

RETURN = r'''
cases_with_trackers:
    description: List of cases containing external tracker references
    returned: always
    type: list
    elements: dict
detection_stats:
    description: Detection statistics
    returned: always
    type: dict
    contains:
        total_cases_analyzed:
            description: Total number of cases analyzed
            type: int
        cases_with_trackers:
            description: Number of cases with tracker references
            type: int
        detection_rate:
            description: Percentage of cases with tracker references
            type: float
        pattern_matches:
            description: Number of matches per pattern
            type: dict
        field_matches:
            description: Number of matches per field
            type: dict
search_results:
    description: Detailed search results per case
    returned: always
    type: list
    elements: dict
    contains:
        case_number:
            description: Case number
            type: str
        matches:
            description: List of matches found
            type: list
        matched_patterns:
            description: Patterns that matched
            type: list
        matched_fields:
            description: Fields that contained matches
            type: list
'''

import re
from ansible.module_utils.basic import AnsibleModule


def search_case_content(case, patterns, fields, case_sensitive=False):
    """Search for patterns in case content."""
    matches = []
    matched_patterns = set()
    matched_fields = set()
    
    flags = 0 if case_sensitive else re.IGNORECASE
    
    for field in fields:
        if field not in case or case[field] is None:
            continue
            
        field_content = str(case[field])
        
        for pattern in patterns:
            try:
                if re.search(pattern, field_content, flags):
                    matches.append({
                        'pattern': pattern,
                        'field': field,
                        'content': field_content[:200] + '...' if len(field_content) > 200 else field_content
                    })
                    matched_patterns.add(pattern)
                    matched_fields.add(field)
            except re.error as e:
                # Skip invalid regex patterns
                continue
    
    return {
        'matches': matches,
        'matched_patterns': list(matched_patterns),
        'matched_fields': list(matched_fields)
    }


def analyze_cases(case_data, patterns, fields, case_sensitive=False, include_closed=False):
    """Analyze all cases for external tracker references."""
    cases_with_trackers = []
    search_results = []
    pattern_matches = {pattern: 0 for pattern in patterns}
    field_matches = {field: 0 for field in fields}
    
    for case in case_data:
        # Skip closed cases if not including them
        if not include_closed and case.get('isClosed', False):
            continue
            
        search_result = search_case_content(case, patterns, fields, case_sensitive)
        
        if search_result['matches']:
            cases_with_trackers.append(case)
            
            # Update statistics
            for pattern in search_result['matched_patterns']:
                pattern_matches[pattern] += 1
            for field in search_result['matched_fields']:
                field_matches[field] += 1
        
        search_results.append({
            'case_number': case.get('caseNumber', 'unknown'),
            'matches': search_result['matches'],
            'matched_patterns': search_result['matched_patterns'],
            'matched_fields': search_result['matched_fields']
        })
    
    return {
        'cases_with_trackers': cases_with_trackers,
        'search_results': search_results,
        'pattern_matches': pattern_matches,
        'field_matches': field_matches
    }


def calculate_detection_stats(analysis_results, total_cases):
    """Calculate detection statistics."""
    cases_with_trackers = len(analysis_results['cases_with_trackers'])
    detection_rate = (cases_with_trackers / total_cases * 100) if total_cases > 0 else 0
    
    return {
        'total_cases_analyzed': total_cases,
        'cases_with_trackers': cases_with_trackers,
        'detection_rate': detection_rate,
        'pattern_matches': analysis_results['pattern_matches'],
        'field_matches': analysis_results['field_matches']
    }


def main():
    module_args = dict(
        case_data=dict(type='list', elements='dict', required=True),
        search_patterns=dict(type='list', elements='str', default=['issues\\.redhat\\.com', 'jira\\.redhat\\.com']),
        search_fields=dict(type='list', elements='str', default=['subject', 'description', 'tags']),
        case_sensitive=dict(type='bool', default=False),
        include_closed_cases=dict(type='bool', default=False)
    )
    
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    
    case_data = module.params['case_data']
    search_patterns = module.params['search_patterns']
    search_fields = module.params['search_fields']
    case_sensitive = module.params['case_sensitive']
    include_closed_cases = module.params['include_closed_cases']
    
    try:
        # Filter cases if needed
        filtered_cases = case_data if include_closed_cases else [case for case in case_data if not case.get('isClosed', False)]
        
        # Analyze cases
        analysis_results = analyze_cases(filtered_cases, search_patterns, search_fields, case_sensitive, include_closed_cases)
        
        # Calculate statistics
        detection_stats = calculate_detection_stats(analysis_results, len(filtered_cases))
        
        module.exit_json(
            changed=False,
            cases_with_trackers=analysis_results['cases_with_trackers'],
            detection_stats=detection_stats,
            search_results=analysis_results['search_results']
        )
        
    except Exception as e:
        module.fail_json(msg=f"External tracker detection error: {str(e)}")


if __name__ == '__main__':
    main()
