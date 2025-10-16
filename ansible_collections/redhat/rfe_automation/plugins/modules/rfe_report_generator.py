#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: rfe_report_generator
short_description: Generate RFE/Bug reports from processed case data
version_added: "1.0.0"
description:
    - This module generates professional RFE/Bug reports in multiple formats
    - Supports Markdown and JSON output formats
    - Includes comprehensive validation and quality metrics
author:
    - Red Hat TAM Operations
options:
    report_type:
        description:
            - Type of report to generate
        required: true
        type: str
        choices: ['rfe_bug_tracker', 'active_cases']
    customer_name:
        description:
            - Customer name for the report
        required: true
        type: str
    account_name:
        description:
            - Account name for the report
        required: true
        type: str
    account_number:
        description:
            - Account number for the report
        required: true
        type: str
    active_rfes:
        description:
            - List of active RFE cases
        required: false
        type: list
        elements: dict
        default: []
    active_bugs:
        description:
            - List of active bug cases
        required: false
        type: list
        elements: dict
        default: []
    closed_cases:
        description:
            - List of closed cases
        required: false
        type: list
        elements: dict
        default: []
    all_active_cases:
        description:
            - List of all active cases
        required: false
        type: list
        elements: dict
        default: []
    priority_active_cases:
        description:
            - List of priority active cases
        required: false
        type: list
        elements: dict
        default: []
    data_quality_score:
        description:
            - Data quality score (0.0 to 1.0)
        required: false
        type: float
        default: 1.0
    output_dir:
        description:
            - Output directory for reports
        required: true
        type: str
    output_formats:
        description:
            - List of output formats to generate
        required: false
        type: list
        elements: str
        choices: ['markdown', 'json']
        default: ['markdown', 'json']
    include_timestamp:
        description:
            - Whether to include timestamp in filename
        required: false
        type: bool
        default: true
'''

EXAMPLES = r'''
# Generate RFE/Bug Tracker report
- name: Generate RFE/Bug Tracker report
  rfe_report_generator:
    report_type: "rfe_bug_tracker"
    customer_name: "JPMC"
    account_name: "jpmc"
    account_number: "334224"
    active_rfes: "{{ processed_data.active_rfes }}"
    active_bugs: "{{ processed_data.active_bugs }}"
    closed_cases: "{{ processed_data.closed_cases }}"
    data_quality_score: "{{ processed_data.data_quality_score }}"
    output_dir: "./output"
    output_formats: ["markdown", "json"]

# Generate Active Cases report
- name: Generate Active Cases report
  rfe_report_generator:
    report_type: "active_cases"
    customer_name: "JPMC"
    account_name: "jpmc"
    account_number: "334224"
    all_active_cases: "{{ processed_data.all_active_cases }}"
    priority_active_cases: "{{ processed_data.priority_active_cases }}"
    output_dir: "./output"
    output_formats: ["markdown"]
'''

RETURN = r'''
report_files:
    description: List of generated report files
    returned: always
    type: list
    elements: dict
    contains:
        format:
            description: Report format
            type: str
        path:
            description: Full path to the report file
            type: str
        size:
            description: File size in bytes
            type: int
report_summary:
    description: Summary of the generated report
    returned: always
    type: dict
    contains:
        report_type:
            description: Type of report generated
            type: str
        customer_name:
            description: Customer name
            type: str
        total_cases:
            description: Total cases in report
            type: int
        data_quality_score:
            description: Data quality score
            type: float
        generated_at:
            description: Report generation timestamp
            type: str
'''

import json
import os
from datetime import datetime
from ansible.module_utils.basic import AnsibleModule


def format_case_subject(subject, max_length=80):
    """Format case subject for display"""
    if not subject:
        return "N/A"
    
    if len(subject) <= max_length:
        return subject
    
    return subject[:max_length] + "..."


def generate_rfe_bug_tracker_markdown(customer_name, account_name, account_number, active_rfes, active_bugs, closed_cases, data_quality_score):
    """Generate RFE/Bug Tracker report in Markdown format"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    markdown = f"""# RFE/Bug Tracker Report - {customer_name}

**Generated:** {timestamp}  
**Customer:** {customer_name} ({account_name})  
**Account Number:** {account_number}  

## 📊 Executive Summary

- **Total Cases Analyzed:** {len(active_rfes) + len(active_bugs) + len(closed_cases)}
- **Active RFEs:** {len(active_rfes)}
- **Active Bugs:** {len(active_bugs)}
- **Closed Cases:** {len(closed_cases)}
- **Data Quality Score:** {data_quality_score * 100:.1f}%

## 🎯 Active RFE Cases ({len(active_rfes)})

"""
    
    if active_rfes:
        markdown += """| Case Number | Subject | Severity | Status |
|-------------|---------|----------|--------|
"""
        for case in active_rfes:
            case_number = case.get('caseNumber', 'N/A')
            subject = format_case_subject(case.get('subject', 'N/A'))
            severity = case.get('severity', 'N/A')
            status = case.get('internalStatus', 'N/A')
            markdown += f"| {case_number} | {subject} | {severity} | {status} |\n"
    else:
        markdown += "No active RFE cases found.\n"
    
    markdown += f"""
## 🐛 Active Bug Cases ({len(active_bugs)})

"""
    
    if active_bugs:
        markdown += """| Case Number | Subject | Severity | Status |
|-------------|---------|----------|--------|
"""
        for case in active_bugs:
            case_number = case.get('caseNumber', 'N/A')
            subject = format_case_subject(case.get('subject', 'N/A'))
            severity = case.get('severity', 'N/A')
            status = case.get('internalStatus', 'N/A')
            markdown += f"| {case_number} | {subject} | {severity} | {status} |\n"
    else:
        markdown += "No active bug cases found.\n"
    
    markdown += f"""
## 📋 Closed Cases ({len(closed_cases)})

"""
    
    if closed_cases:
        markdown += """| Case Number | Subject | Type | Closed Date |
|-------------|---------|------|-------------|
"""
        for case in closed_cases:
            case_number = case.get('caseNumber', 'N/A')
            subject = format_case_subject(case.get('subject', 'N/A'), 60)
            case_type = case.get('caseType', 'N/A')
            closed_date = case.get('lastUpdateDate', 'N/A')
            markdown += f"| {case_number} | {subject} | {case_type} | {closed_date} |\n"
    else:
        markdown += "No closed cases found.\n"
    
    markdown += f"""
## 📈 Data Quality Report

- **Data Quality Score:** {data_quality_score * 100:.1f}%
- **Total Cases Processed:** {len(active_rfes) + len(active_bugs) + len(closed_cases)}
- **Validation Status:** {'✅ Passed' if data_quality_score >= 0.95 else '❌ Failed'}

---

*This report was automatically generated by the Red Hat RFE Automation System.*  
*For questions or issues, please contact your TAM or the TAM Operations team.*
"""
    
    return markdown


def generate_active_cases_markdown(customer_name, account_name, account_number, all_active_cases, priority_active_cases):
    """Generate Active Cases report in Markdown format"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    markdown = f"""# Active Cases Report - {customer_name}

**Generated:** {timestamp}  
**Customer:** {customer_name} ({account_name})  
**Account Number:** {account_number}  

## 📊 Executive Summary

- **Total Active Cases:** {len(all_active_cases)}
- **Priority Component Cases:** {len(priority_active_cases)}
- **Other Active Cases:** {len(all_active_cases) - len(priority_active_cases)}

## 🎯 Priority Component Cases ({len(priority_active_cases)})

"""
    
    if priority_active_cases:
        markdown += """| Case Number | Subject | Severity | Status |
|-------------|---------|----------|--------|
"""
        for case in priority_active_cases:
            case_number = case.get('caseNumber', 'N/A')
            subject = format_case_subject(case.get('subject', 'N/A'))
            severity = case.get('severity', 'N/A')
            status = case.get('internalStatus', 'N/A')
            markdown += f"| {case_number} | {subject} | {severity} | {status} |\n"
    else:
        markdown += "No priority component cases found.\n"
    
    markdown += f"""
## 📋 All Active Cases ({len(all_active_cases)})

"""
    
    if all_active_cases:
        markdown += """| Case Number | Subject | Severity | Status |
|-------------|---------|----------|--------|
"""
        for case in all_active_cases:
            case_number = case.get('caseNumber', 'N/A')
            subject = format_case_subject(case.get('subject', 'N/A'))
            severity = case.get('severity', 'N/A')
            status = case.get('internalStatus', 'N/A')
            markdown += f"| {case_number} | {subject} | {severity} | {status} |\n"
    else:
        markdown += "No active cases found.\n"
    
    markdown += """
---

*This report was automatically generated by the Red Hat RFE Automation System.*  
*For questions or issues, please contact your TAM or the TAM Operations team.*
"""
    
    return markdown


def generate_json_report(report_type, customer_name, account_name, account_number, active_rfes, active_bugs, closed_cases, all_active_cases, priority_active_cases, data_quality_score):
    """Generate report in JSON format"""
    timestamp = datetime.now().isoformat()
    
    json_data = {
        "report_type": report_type,
        "customer": customer_name,
        "account": account_name,
        "account_number": account_number,
        "timestamp": timestamp,
        "summary": {
            "total_cases": len(active_rfes) + len(active_bugs) + len(closed_cases) + len(all_active_cases),
            "active_rfes": len(active_rfes),
            "active_bugs": len(active_bugs),
            "closed_cases": len(closed_cases),
            "all_active_cases": len(all_active_cases),
            "priority_active_cases": len(priority_active_cases),
            "data_quality_score": data_quality_score
        }
    }
    
    if report_type == "rfe_bug_tracker":
        json_data.update({
            "active_rfes": active_rfes,
            "active_bugs": active_bugs,
            "closed_cases": closed_cases
        })
    elif report_type == "active_cases":
        json_data.update({
            "all_active_cases": all_active_cases,
            "priority_active_cases": priority_active_cases
        })
    
    return json.dumps(json_data, indent=2, default=str)


def main():
    """Main module function"""
    module = AnsibleModule(
        argument_spec=dict(
            report_type=dict(type='str', required=True, choices=['rfe_bug_tracker', 'active_cases']),
            customer_name=dict(type='str', required=True),
            account_name=dict(type='str', required=True),
            account_number=dict(type='str', required=True),
            active_rfes=dict(type='list', elements='dict', default=[]),
            active_bugs=dict(type='list', elements='dict', default=[]),
            closed_cases=dict(type='list', elements='dict', default=[]),
            all_active_cases=dict(type='list', elements='dict', default=[]),
            priority_active_cases=dict(type='list', elements='dict', default=[]),
            data_quality_score=dict(type='float', default=1.0),
            output_dir=dict(type='str', required=True),
            output_formats=dict(type='list', elements='str', choices=['markdown', 'json'], default=['markdown', 'json']),
            include_timestamp=dict(type='bool', default=True)
        ),
        supports_check_mode=True
    )
    
    # Get parameters
    report_type = module.params['report_type']
    customer_name = module.params['customer_name']
    account_name = module.params['account_name']
    account_number = module.params['account_number']
    active_rfes = module.params['active_rfes']
    active_bugs = module.params['active_bugs']
    closed_cases = module.params['closed_cases']
    all_active_cases = module.params['all_active_cases']
    priority_active_cases = module.params['priority_active_cases']
    data_quality_score = module.params['data_quality_score']
    output_dir = module.params['output_dir']
    output_formats = module.params['output_formats']
    include_timestamp = module.params['include_timestamp']
    
    # In check mode, return without making changes
    if module.check_mode:
        module.exit_json(
            changed=False,
            report_files=[],
            report_summary={},
            msg="Check mode - no changes made"
        )
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate timestamp for filename
        timestamp_suffix = ""
        if include_timestamp:
            timestamp_suffix = f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Generate base filename
        base_filename = f"{customer_name.lower()}_{report_type}_report{timestamp_suffix}"
        
        report_files = []
        
        # Generate Markdown report
        if 'markdown' in output_formats:
            if report_type == "rfe_bug_tracker":
                markdown_content = generate_rfe_bug_tracker_markdown(
                    customer_name, account_name, account_number,
                    active_rfes, active_bugs, closed_cases, data_quality_score
                )
            elif report_type == "active_cases":
                markdown_content = generate_active_cases_markdown(
                    customer_name, account_name, account_number,
                    all_active_cases, priority_active_cases
                )
            
            markdown_path = os.path.join(output_dir, f"{base_filename}.md")
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            report_files.append({
                'format': 'markdown',
                'path': markdown_path,
                'size': os.path.getsize(markdown_path)
            })
        
        # Generate JSON report
        if 'json' in output_formats:
            json_content = generate_json_report(
                report_type, customer_name, account_name, account_number,
                active_rfes, active_bugs, closed_cases, all_active_cases,
                priority_active_cases, data_quality_score
            )
            
            json_path = os.path.join(output_dir, f"{base_filename}.json")
            with open(json_path, 'w', encoding='utf-8') as f:
                f.write(json_content)
            
            report_files.append({
                'format': 'json',
                'path': json_path,
                'size': os.path.getsize(json_path)
            })
        
        # Prepare result
        total_cases = len(active_rfes) + len(active_bugs) + len(closed_cases) + len(all_active_cases)
        
        result = {
            'changed': True,
            'report_files': report_files,
            'report_summary': {
                'report_type': report_type,
                'customer_name': customer_name,
                'total_cases': total_cases,
                'data_quality_score': data_quality_score,
                'generated_at': datetime.now().isoformat()
            },
            'msg': f"Generated {len(report_files)} report files for {customer_name}"
        }
        
        module.exit_json(**result)
        
    except Exception as e:
        module.fail_json(msg=f"Unexpected error generating report: {e}")


if __name__ == '__main__':
    main()
