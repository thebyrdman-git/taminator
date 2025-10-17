#!/usr/bin/env python3

import os
import sys
import json
import tempfile
from jinja2 import Environment, FileSystemLoader, Template
from typing import Dict, List, Any

class TemplateTester:
    def __init__(self, template_dir: str = "/home/jbyrd/pai/rfe-automation-clean/templates"):
        self.template_dir = template_dir
        self.env = Environment(loader=FileSystemLoader(template_dir))
        
    def test_template(self, template_name: str, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Test a template with given data"""
        
        result = {
            'template': template_name,
            'success': False,
            'output': '',
            'errors': [],
            'warnings': []
        }
        
        try:
            # Load template
            template = self.env.get_template(template_name)
            
            # Render template
            output = template.render(**test_data)
            
            result['success'] = True
            result['output'] = output
            
            # Basic validation
            if not output.strip():
                result['warnings'].append("Template output is empty")
            
            if 'N/A' in output:
                result['warnings'].append("Template contains 'N/A' values - check data completeness")
                
        except Exception as e:
            result['errors'].append(f"Template rendering failed: {str(e)}")
            
        return result
    
    def test_rfe_bug_template(self) -> Dict[str, Any]:
        """Test RFE/Bug template with sample data"""
        
        test_data = {
            'customer_name': 'Test Customer',
            'account_number': '123456',
            'ansible_date_time': {'date': '2024-12-19'},
            'active_rfes': [
                {
                    'caseNumber': '03208295',
                    'subject': '[RFE] Add new feature',
                    'internalStatus': 'Open',
                    'priority': 'High'
                }
            ],
            'active_bugs': [
                {
                    'caseNumber': '04131060',
                    'subject': '[BUG] Fix login issue',
                    'internalStatus': 'Open',
                    'priority': 'Critical'
                }
            ],
            'closed_cases': [
                {
                    'caseNumber': '04276978',
                    'subject': '[RFE] Improve performance',
                    'closedDate': '2024-12-15'
                }
            ]
        }
        
        return self.test_template('bulletproof_rfe_bug_report.j2', test_data)
    
    def test_active_cases_template(self) -> Dict[str, Any]:
        """Test Active Cases template with sample data"""
        
        test_data = {
            'customer_name': 'Test Customer',
            'account_number': '123456',
            'ansible_date_time': {'date': '2024-12-19'},
            'all_active_cases': [
                {
                    'caseNumber': '04345678',
                    'subject': 'Configuration issue',
                    'internalStatus': 'Open',
                    'priority': 'Medium',
                    'sbrGroup': 'Ansible'
                }
            ],
            'priority_active_cases': [
                {
                    'caseNumber': '04345678',
                    'subject': 'Configuration issue',
                    'internalStatus': 'Open',
                    'priority': 'Medium'
                }
            ]
        }
        
        return self.test_template('bulletproof_active_cases_report.j2', test_data)
    
    def test_empty_data(self) -> Dict[str, Any]:
        """Test templates with empty data"""
        
        empty_data = {
            'customer_name': 'Test Customer',
            'account_number': '123456',
            'ansible_date_time': {'date': '2024-12-19'},
            'active_rfes': [],
            'active_bugs': [],
            'closed_cases': [],
            'all_active_cases': [],
            'priority_active_cases': []
        }
        
        results = {}
        results['rfe_bug_empty'] = self.test_template('bulletproof_rfe_bug_report.j2', empty_data)
        results['active_cases_empty'] = self.test_template('bulletproof_active_cases_report.j2', empty_data)
        
        return results
    
    def test_missing_data(self) -> Dict[str, Any]:
        """Test templates with missing data"""
        
        missing_data = {
            'customer_name': 'Test Customer',
            'account_number': '123456',
            'ansible_date_time': {'date': '2024-12-19'}
            # Missing all case data
        }
        
        results = {}
        results['rfe_bug_missing'] = self.test_template('bulletproof_rfe_bug_report.j2', missing_data)
        results['active_cases_missing'] = self.test_template('bulletproof_active_cases_report.j2', missing_data)
        
        return results
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all template tests"""
        
        results = {
            'rfe_bug_test': self.test_rfe_bug_template(),
            'active_cases_test': self.test_active_cases_template(),
            'empty_data_tests': self.test_empty_data(),
            'missing_data_tests': self.test_missing_data()
        }
        
        # Calculate overall success
        all_tests = []
        for test_group in results.values():
            if isinstance(test_group, dict):
                for test in test_group.values():
                    if isinstance(test, dict) and 'success' in test:
                        all_tests.append(test['success'])
        
        results['overall_success'] = all(all_tests) if all_tests else False
        results['total_tests'] = len(all_tests)
        results['passed_tests'] = sum(all_tests)
        
        return results

def main():
    tester = TemplateTester()
    results = tester.run_all_tests()
    
    print("🧪 Template Testing Results")
    print("=" * 50)
    
    for test_name, test_result in results.items():
        if isinstance(test_result, dict) and 'success' in test_result:
            status = "✅ PASS" if test_result['success'] else "❌ FAIL"
            print(f"{test_name}: {status}")
            
            if test_result.get('errors'):
                for error in test_result['errors']:
                    print(f"  ERROR: {error}")
                    
            if test_result.get('warnings'):
                for warning in test_result['warnings']:
                    print(f"  WARNING: {warning}")
    
    print("\n📊 Summary:")
    print(f"Total Tests: {results.get('total_tests', 0)}")
    print(f"Passed: {results.get('passed_tests', 0)}")
    print(f"Failed: {results.get('total_tests', 0) - results.get('passed_tests', 0)}")
    print(f"Overall: {'✅ PASS' if results.get('overall_success') else '❌ FAIL'}")
    
    # Exit with error code if any tests failed
    if not results.get('overall_success', False):
        sys.exit(1)

if __name__ == '__main__':
    main()
