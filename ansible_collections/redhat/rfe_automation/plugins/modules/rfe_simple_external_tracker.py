#!/usr/bin/env python3

from ansible.module_utils.basic import AnsibleModule
import json
from typing import Dict, List, Any, Optional

def detect_external_trackers_in_cases(cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Detect external trackers in cases by checking the externalTrackers field"""
    
    cases_with_external_trackers = []
    cases_without_external_trackers = []
    
    for case in cases:
        case_number = case.get('caseNumber')
        if not case_number:
            continue
        
        # Check if case has externalTrackers field
        external_trackers = case.get('externalTrackers', [])
        has_external_trackers = len(external_trackers) > 0
        
        if has_external_trackers:
            # Extract JIRA status from external trackers
            jira_status = None
            for tracker in external_trackers:
                if tracker.get('system', '').upper() == 'JIRA':
                    jira_status = tracker.get('status', None)
                    break  # Use the first JIRA tracker's status
            
            # Add JIRA status to the case
            case_with_trackers = case.copy()
            case_with_trackers['jira_status'] = jira_status
            case_with_trackers['has_external_trackers'] = True
            cases_with_external_trackers.append(case_with_trackers)
        else:
            case_without_trackers = case.copy()
            case_without_trackers['jira_status'] = None
            case_without_trackers['has_external_trackers'] = False
            cases_without_external_trackers.append(case_without_trackers)
    
    return {
        'cases_with_external_trackers': cases_with_external_trackers,
        'cases_without_external_trackers': cases_without_external_trackers,
        'total_cases_processed': len(cases),
        'cases_with_trackers_count': len(cases_with_external_trackers),
        'cases_without_trackers_count': len(cases_without_external_trackers)
    }

def main():
    module = AnsibleModule(
        argument_spec=dict(
            cases=dict(type='list', elements='dict', required=True)
        ),
        supports_check_mode=True
    )
    
    cases = module.params['cases']
    
    try:
        # Detect external trackers
        result = detect_external_trackers_in_cases(cases)
        
        # Prepare the result
        module_result = {
            'changed': False,
            'cases_with_external_trackers': result['cases_with_external_trackers'],
            'cases_without_external_trackers': result['cases_without_external_trackers'],
            'statistics': {
                'total_cases_processed': result['total_cases_processed'],
                'cases_with_trackers_count': result['cases_with_trackers_count'],
                'cases_without_trackers_count': result['cases_without_trackers_count']
            },
            'msg': f"Processed {result['total_cases_processed']} cases, found {result['cases_with_trackers_count']} with external trackers"
        }
        
        module.exit_json(**module_result)
        
    except Exception as e:
        module.fail_json(msg=f"External tracker detection failed: {str(e)}")

if __name__ == '__main__':
    main()
