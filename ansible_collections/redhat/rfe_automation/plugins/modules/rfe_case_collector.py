#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: rfe_case_collector
short_description: Collect RFE/Bug cases from rhcase tool
version_added: "1.0.0"
description:
    - This module collects case data from the rhcase tool for RFE automation
    - Supports filtering by account number, SBR groups, and case types
    - Returns structured case data for further processing
author:
    - Red Hat TAM Operations
options:
    account_number:
        description:
            - Account number to filter cases
        required: true
        type: str
    sbr_groups:
        description:
            - List of SBR groups to filter by
        required: true
        type: list
        elements: str
    case_types:
        description:
            - List of case types to include (optional)
        required: false
        type: list
        elements: str
        default: []
    rhcase_path:
        description:
            - Path to rhcase executable
        required: false
        type: str
        default: "rhcase"
    include_closed:
        description:
            - Whether to include closed cases
        required: false
        type: bool
        default: false
    validate_data:
        description:
            - Whether to validate the collected data
        required: false
        type: bool
        default: true
'''

EXAMPLES = r'''
# Collect RFE cases for JPMC
- name: Collect RFE cases
  rfe_case_collector:
    account_number: "334224"
    sbr_groups: ["Ansible"]
    case_types: ["Feature / Enhancement Request", "Defect / Bug"]
    validate_data: true
  register: rfe_cases

# Collect all cases for a customer
- name: Collect all cases
  rfe_case_collector:
    account_number: "334224"
    sbr_groups: ["Ansible", "OpenShift"]
    include_closed: true
  register: all_cases
'''

RETURN = r'''
cases:
    description: List of collected cases
    returned: always
    type: list
    elements: dict
    contains:
        caseNumber:
            description: Case number
            type: str
            returned: always
        subject:
            description: Case subject
            type: str
            returned: always
        caseType:
            description: Case type
            type: str
            returned: always
        sbrGroup:
            description: SBR group
            type: str
            returned: always
        isClosed:
            description: Whether case is closed
            type: bool
            returned: always
        accountNumber:
            description: Account number
            type: str
            returned: always
        severity:
            description: Case severity
            type: str
            returned: when available
        internalStatus:
            description: Internal status
            type: str
            returned: when available
        caseOwner:
            description: Case owner information
            type: dict
            returned: when available
        description:
            description: Case description
            type: str
            returned: when available
        tags:
            description: Case tags
            type: str
            returned: when available
total_cases:
    description: Total number of cases collected
    returned: always
    type: int
filtered_cases:
    description: Number of cases after filtering
    returned: always
    type: int
data_quality_score:
    description: Data quality score (0.0 to 1.0)
    returned: when validate_data is true
    type: float
validation_results:
    description: Detailed validation results
    returned: when validate_data is true
    type: dict
    contains:
        missing_fields:
            description: Cases with missing required fields
            type: list
        invalid_data:
            description: Cases with invalid data
            type: list
        quality_issues:
            description: Data quality issues found
            type: list
'''

import json
import subprocess
import tempfile
import os
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text


def run_rhcase_command(module, rhcase_path, sbr_groups):
    """Run rhcase command to collect case data"""
    try:
        # Build the rhcase command
        cmd = [
            rhcase_path,
            "list",
            "--all",
            "--format", "json",
            "--includefilter", f"sbrGroup,{','.join(sbr_groups)}"
        ]
        
        # Execute the command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            check=False
        )
        
        if result.returncode != 0:
            module.fail_json(
                msg=f"rhcase command failed with return code {result.returncode}",
                stdout=result.stdout,
                stderr=result.stderr,
                cmd=cmd
            )
        
        # Parse JSON output
        try:
            cases = json.loads(result.stdout)
            if not isinstance(cases, list):
                module.fail_json(msg="rhcase output is not a list", output=result.stdout)
            return cases
        except json.JSONDecodeError as e:
            module.fail_json(msg=f"Failed to parse rhcase JSON output: {e}", output=result.stdout)
            
    except subprocess.TimeoutExpired:
        module.fail_json(msg="rhcase command timed out after 5 minutes")
    except FileNotFoundError:
        module.fail_json(msg=f"rhcase executable not found at {rhcase_path}")
    except Exception as e:
        module.fail_json(msg=f"Unexpected error running rhcase: {e}")


def filter_cases_by_account(cases, account_number):
    """Filter cases by account number"""
    filtered_cases = []
    for case in cases:
        if case.get('accountNumber') == account_number:
            filtered_cases.append(case)
    return filtered_cases


def filter_cases_by_type(cases, case_types):
    """Filter cases by case type"""
    if not case_types:
        return cases
    
    filtered_cases = []
    for case in cases:
        case_type = case.get('caseType', '')
        if case_type in case_types:
            filtered_cases.append(case)
    return filtered_cases


def filter_closed_cases(cases, include_closed):
    """Filter out closed cases if not requested"""
    if include_closed:
        return cases
    
    filtered_cases = []
    for case in cases:
        if not case.get('isClosed', False):
            filtered_cases.append(case)
    return filtered_cases


def validate_case_data(cases):
    """Validate case data quality"""
    validation_results = {
        'missing_fields': [],
        'invalid_data': [],
        'quality_issues': []
    }
    
    required_fields = ['caseNumber', 'subject', 'caseType', 'sbrGroup', 'accountNumber']
    
    for i, case in enumerate(cases):
        # Check for missing required fields
        missing_fields = []
        for field in required_fields:
            if field not in case or case[field] is None:
                missing_fields.append(field)
        
        if missing_fields:
            validation_results['missing_fields'].append({
                'case_index': i,
                'case_number': case.get('caseNumber', 'unknown'),
                'missing_fields': missing_fields
            })
        
        # Check for invalid data
        if case.get('caseNumber') and not isinstance(case['caseNumber'], str):
            validation_results['invalid_data'].append({
                'case_index': i,
                'case_number': case.get('caseNumber', 'unknown'),
                'issue': 'caseNumber is not a string'
            })
        
        # Check for quality issues
        if case.get('subject') and len(case['subject']) < 10:
            validation_results['quality_issues'].append({
                'case_index': i,
                'case_number': case.get('caseNumber', 'unknown'),
                'issue': 'Subject too short (less than 10 characters)'
            })
    
    # Calculate data quality score
    total_cases = len(cases)
    if total_cases == 0:
        data_quality_score = 1.0
    else:
        issues_count = (
            len(validation_results['missing_fields']) +
            len(validation_results['invalid_data']) +
            len(validation_results['quality_issues'])
        )
        data_quality_score = max(0.0, 1.0 - (issues_count / total_cases))
    
    return data_quality_score, validation_results


def main():
    """Main module function"""
    module = AnsibleModule(
        argument_spec=dict(
            account_number=dict(type='str', required=True),
            sbr_groups=dict(type='list', elements='str', required=True),
            case_types=dict(type='list', elements='str', default=[]),
            rhcase_path=dict(type='str', default='rhcase'),
            include_closed=dict(type='bool', default=False),
            validate_data=dict(type='bool', default=True)
        ),
        supports_check_mode=True
    )
    
    # Get parameters
    account_number = module.params['account_number']
    sbr_groups = module.params['sbr_groups']
    case_types = module.params['case_types']
    rhcase_path = module.params['rhcase_path']
    include_closed = module.params['include_closed']
    validate_data = module.params['validate_data']
    
    # In check mode, return without making changes
    if module.check_mode:
        module.exit_json(
            changed=False,
            cases=[],
            total_cases=0,
            filtered_cases=0,
            msg="Check mode - no changes made"
        )
    
    try:
        # Collect cases from rhcase
        all_cases = run_rhcase_command(module, rhcase_path, sbr_groups)
        total_cases = len(all_cases)
        
        # Filter by account number
        account_cases = filter_cases_by_account(all_cases, account_number)
        
        # Filter by case types if specified
        if case_types:
            account_cases = filter_cases_by_type(account_cases, case_types)
        
        # Filter closed cases if not requested
        account_cases = filter_closed_cases(account_cases, include_closed)
        
        filtered_cases = len(account_cases)
        
        # Validate data if requested
        data_quality_score = None
        validation_results = None
        
        if validate_data:
            data_quality_score, validation_results = validate_case_data(account_cases)
        
        # Prepare result
        result = {
            'changed': False,
            'cases': account_cases,
            'total_cases': total_cases,
            'filtered_cases': filtered_cases,
            'msg': f"Collected {filtered_cases} cases for account {account_number}"
        }
        
        if data_quality_score is not None:
            result['data_quality_score'] = data_quality_score
        
        if validation_results is not None:
            result['validation_results'] = validation_results
        
        module.exit_json(**result)
        
    except Exception as e:
        module.fail_json(msg=f"Unexpected error: {e}")


if __name__ == '__main__':
    main()
