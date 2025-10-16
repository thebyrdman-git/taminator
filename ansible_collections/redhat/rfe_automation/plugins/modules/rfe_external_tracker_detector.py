#!/usr/bin/env python3

from ansible.module_utils.basic import AnsibleModule
import json
import subprocess
import sys
from typing import Dict, List, Any, Optional

def get_external_trackers_for_case(case_number: str, rhcase_path: str = "rhcase") -> Dict[str, Any]:
    """Get external tracker information for a specific case using rhcase tool"""
    
    try:
        # Use rhcase analyze to get detailed case information including external trackers
        cmd = [rhcase_path, "analyze", case_number, "--debug"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            return {
                'case_number': case_number,
                'has_external_trackers': False,
                'external_trackers': [],
                'jira_status': None,
                'error': f"rhcase analyze command failed: {result.stderr}"
            }
        
        # Parse the output to extract external tracker information
        output = result.stdout
        
        # Look for externalTrackers in the debug output
        has_external_trackers = False
        external_trackers = []
        jira_status = None
        
        # Extract external trackers from the debug output
        if 'externalTrackers:' in output:
            # Find the externalTrackers section
            start_idx = output.find('externalTrackers:')
            if start_idx != -1:
                # Extract the external trackers data
                # This is a simplified extraction - in practice, you'd want more robust parsing
                if 'resourceKey' in output and 'status' in output:
                    has_external_trackers = True
                    
                    # Extract JIRA status from the output
                    # Look for pattern like 'status': 'Release Pending'
                    import re
                    status_match = re.search(r"'status':\s*'([^']+)'", output)
                    if status_match:
                        jira_status = status_match.group(1)
                    
                    # Extract JIRA ID
                    jira_match = re.search(r"'resourceKey':\s*'([^']+)'", output)
                    jira_id = jira_match.group(1) if jira_match else None
                    
                    # Extract JIRA URL
                    url_match = re.search(r"'resourceURL':\s*'([^']+)'", output)
                    jira_url = url_match.group(1) if url_match else None
                    
                    if jira_id:
                        external_trackers.append({
                            'tracker_type': 'JIRA',
                            'tracker_id': jira_id,
                            'url': jira_url,
                            'status': jira_status
                        })
        
        return {
            'case_number': case_number,
            'has_external_trackers': has_external_trackers,
            'external_trackers': external_trackers,
            'jira_status': jira_status,
            'raw_output': output
        }
        
    except subprocess.TimeoutExpired:
        return {
            'case_number': case_number,
            'has_external_trackers': False,
            'external_trackers': [],
            'error': "Timeout getting external tracker information"
        }
    except json.JSONDecodeError as e:
        return {
            'case_number': case_number,
            'has_external_trackers': False,
            'external_trackers': [],
            'error': f"Failed to parse JSON response: {str(e)}"
        }
    except Exception as e:
        return {
            'case_number': case_number,
            'has_external_trackers': False,
            'external_trackers': [],
            'error': f"Unexpected error: {str(e)}"
        }

def detect_external_trackers_in_cases(cases: List[Dict[str, Any]], rhcase_path: str = "rhcase") -> Dict[str, Any]:
    """Detect external trackers for a list of cases"""
    
    cases_with_external_trackers = []
    cases_without_external_trackers = []
    errors = []
    
    for case in cases:
        case_number = case.get('caseNumber')
        if not case_number:
            errors.append(f"Case missing caseNumber: {case}")
            continue
        
        external_info = get_external_trackers_for_case(case_number, rhcase_path)
        
        if external_info.get('has_external_trackers'):
            # Add external tracker info to the case
            case_with_trackers = case.copy()
            case_with_trackers['external_trackers'] = external_info['external_trackers']
            case_with_trackers['has_external_trackers'] = True
            case_with_trackers['jira_status'] = external_info.get('jira_status')
            cases_with_external_trackers.append(case_with_trackers)
        else:
            case_without_trackers = case.copy()
            case_without_trackers['external_trackers'] = []
            case_without_trackers['has_external_trackers'] = False
            cases_without_external_trackers.append(case_without_trackers)
            
            if 'error' in external_info:
                errors.append(f"Case {case_number}: {external_info['error']}")
    
    return {
        'cases_with_external_trackers': cases_with_external_trackers,
        'cases_without_external_trackers': cases_without_external_trackers,
        'total_cases_processed': len(cases),
        'cases_with_trackers_count': len(cases_with_external_trackers),
        'cases_without_trackers_count': len(cases_without_external_trackers),
        'errors': errors
    }

def main():
    module = AnsibleModule(
        argument_spec=dict(
            cases=dict(type='list', elements='dict', required=True),
            rhcase_path=dict(type='str', default='rhcase'),
            check_mode=dict(type='bool', default=False)
        ),
        supports_check_mode=True
    )
    
    cases = module.params['cases']
    rhcase_path = module.params['rhcase_path']
    
    try:
        # Detect external trackers
        result = detect_external_trackers_in_cases(cases, rhcase_path)
        
        # Prepare the result
        module_result = {
            'changed': False,
            'cases_with_external_trackers': result['cases_with_external_trackers'],
            'cases_without_external_trackers': result['cases_without_external_trackers'],
            'statistics': {
                'total_cases_processed': result['total_cases_processed'],
                'cases_with_trackers_count': result['cases_with_trackers_count'],
                'cases_without_trackers_count': result['cases_without_trackers_count']
            }
        }
        
        if result['errors']:
            module_result['errors'] = result['errors']
            module_result['msg'] = f"Processed {result['total_cases_processed']} cases with {len(result['errors'])} errors"
        else:
            module_result['msg'] = f"Successfully processed {result['total_cases_processed']} cases"
        
        module.exit_json(**module_result)
        
    except Exception as e:
        module.fail_json(msg=f"External tracker detection failed: {str(e)}")

if __name__ == '__main__':
    main()
