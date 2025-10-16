#!/usr/bin/env python3

from ansible.module_utils.basic import AnsibleModule
import json
import re
from typing import Dict, List, Any, Optional

def validate_template_data(data: Dict[str, Any], template_type: str) -> Dict[str, Any]:
    """Validate template data based on template type"""
    
    validation_result = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'data_quality_score': 0.0
    }
    
    # Required fields for all templates
    required_fields = ['customer_name', 'account_number', 'ansible_date_time']
    
    for field in required_fields:
        if field not in data:
            validation_result['errors'].append(f"Missing required field: {field}")
            validation_result['valid'] = False
    
    if template_type == 'rfe_bug':
        # Validate RFE/Bug template data
        rfe_fields = ['active_rfes', 'active_bugs', 'closed_cases']
        for field in rfe_fields:
            if field not in data:
                validation_result['warnings'].append(f"Missing optional field: {field}")
            elif not isinstance(data[field], list):
                validation_result['errors'].append(f"Field {field} must be a list")
                validation_result['valid'] = False
    
    elif template_type == 'active_cases':
        # Validate Active Cases template data
        active_fields = ['all_active_cases', 'priority_active_cases']
        for field in active_fields:
            if field not in data:
                validation_result['warnings'].append(f"Missing optional field: {field}")
            elif not isinstance(data[field], list):
                validation_result['errors'].append(f"Field {field} must be a list")
                validation_result['valid'] = False
    
    # Calculate data quality score
    total_fields = len(required_fields) + (2 if template_type == 'rfe_bug' else 2)
    present_fields = sum(1 for field in required_fields if field in data)
    if template_type == 'rfe_bug':
        present_fields += sum(1 for field in ['active_rfes', 'active_bugs', 'closed_cases'] if field in data)
    else:
        present_fields += sum(1 for field in ['all_active_cases', 'priority_active_cases'] if field in data)
    
    validation_result['data_quality_score'] = present_fields / total_fields
    
    return validation_result

def validate_case_data(cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Validate individual case data"""
    
    validation_result = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'case_count': len(cases)
    }
    
    required_case_fields = ['caseNumber', 'subject', 'internalStatus']
    
    for i, case in enumerate(cases):
        for field in required_case_fields:
            if field not in case:
                validation_result['errors'].append(f"Case {i}: Missing required field {field}")
                validation_result['valid'] = False
            elif not case[field]:
                validation_result['warnings'].append(f"Case {i}: Empty field {field}")
    
    return validation_result

def main():
    module = AnsibleModule(
        argument_spec=dict(
            template_data=dict(type='dict', required=True),
            template_type=dict(type='str', required=True, choices=['rfe_bug', 'active_cases']),
            validate_cases=dict(type='bool', default=True)
        ),
        supports_check_mode=True
    )
    
    template_data = module.params['template_data']
    template_type = module.params['template_type']
    validate_cases = module.params['validate_cases']
    
    try:
        # Validate template data structure
        template_validation = validate_template_data(template_data, template_type)
        
        # Validate case data if requested
        case_validation = {'valid': True, 'errors': [], 'warnings': [], 'case_count': 0}
        if validate_cases:
            case_fields = ['active_rfes', 'active_bugs', 'closed_cases'] if template_type == 'rfe_bug' else ['all_active_cases', 'priority_active_cases']
            for field in case_fields:
                if field in template_data and isinstance(template_data[field], list):
                    field_validation = validate_case_data(template_data[field])
                    case_validation['errors'].extend(field_validation['errors'])
                    case_validation['warnings'].extend(field_validation['warnings'])
                    case_validation['case_count'] += field_validation['case_count']
                    if not field_validation['valid']:
                        case_validation['valid'] = False
        
        # Combine validation results
        result = {
            'valid': template_validation['valid'] and case_validation['valid'],
            'template_validation': template_validation,
            'case_validation': case_validation,
            'data_quality_score': template_validation['data_quality_score'],
            'total_cases': case_validation['case_count']
        }
        
        if result['valid']:
            module.exit_json(changed=False, **result)
        else:
            module.fail_json(msg="Template validation failed", **result)
            
    except Exception as e:
        module.fail_json(msg=f"Template validation error: {str(e)}")

if __name__ == '__main__':
    main()
