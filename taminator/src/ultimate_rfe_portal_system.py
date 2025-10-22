#!/usr/bin/env python3

"""
Ultimate RFE Portal System - Complete RFE Automation Workflow
Purpose: End-to-end RFE automation from case discovery to portal posting
Features: Case discovery, template rendering, API posting, monitoring, error handling
"""

import os
import sys
import json
import yaml
import argparse
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

# Import our custom modules
from active_case_report_system import ActiveCaseReportSystem
from customer_template_renderer import CustomerTemplateRenderer
from redhat_cppg_api_client import RedHatCPPGAPIClient
from rfe_discussion_api_client import RFEDiscussionAPIClient

class UltimateRFEPortalSystem:
    """Complete RFE automation system"""
    
    def __init__(self, environment: str = "production"):
        """
        Initialize the ultimate RFE portal system
        
        Args:
            environment: 'qa', 'stage', or 'production'
        """
        self.environment = environment
        self.logger = self._setup_logging()
        
        # Initialize components
        self.case_system = ActiveCaseReportSystem()
        self.template_renderer = CustomerTemplateRenderer()
        self.api_client = RedHatCPPGAPIClient(environment)
        self.rfe_client = RFEDiscussionAPIClient(environment)
        
        # Load customer configuration
        self.customer_config = self._load_customer_config()
        
        self.logger.info(f"Ultimate RFE Portal System initialized for {environment}")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the ultimate system"""
        logger = logging.getLogger('ultimate_rfe_portal_system')
        logger.setLevel(logging.INFO)
        
        # Create log file
        log_file = f"/tmp/ultimate-rfe-portal-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _load_customer_config(self) -> Dict[str, Any]:
        """Load customer configuration from files"""
        
        config = {}
        
        try:
            # Load from JSON config
            json_config_file = os.path.join(os.path.dirname(__file__), '..', 'config', 'customer_group_ids_config.json')
            if os.path.exists(json_config_file):
                with open(json_config_file, 'r') as f:
                    json_config = json.load(f)
                    config.update(json_config.get('customer_group_ids', {}))
            
            # Load from YAML config
            yaml_config_file = os.path.join(os.path.dirname(__file__), '..', 'config', 'customer_group_ids.yaml')
            if os.path.exists(yaml_config_file):
                with open(yaml_config_file, 'r') as f:
                    yaml_config = yaml.safe_load(f)
                    config.update(yaml_config.get('customers', {}))
            
            self.logger.info(f"Loaded configuration for {len(config)} customers")
            
        except Exception as e:
            self.logger.error(f"Error loading customer configuration: {e}")
        
        return config
    
    def process_customer(self, 
                        customer_key: str, 
                        test_mode: bool = False) -> Dict[str, Any]:
        """
        Process RFE automation for a single customer
        
        Args:
            customer_key: Customer key (e.g., 'wellsfargo', 'tdbank')
            test_mode: If True, don't post to portal
            
        Returns:
            Dict with processing results
        """
        try:
            self.logger.info(f"Processing RFE automation for {customer_key}")
            
            # Get customer configuration
            customer_config = self.customer_config.get(customer_key)
            if not customer_config:
                raise ValueError(f"Customer {customer_key} not found in configuration")
            
            customer_name = customer_config.get('name', customer_key.title())
            account_number = customer_config.get('account_number')
            group_id = customer_config.get('group_id')
            
            if not account_number:
                raise ValueError(f"No account number configured for {customer_key}")
            
            # Step 1: Discover cases
            self.logger.info(f"Step 1: Discovering cases for {customer_name}")
            case_report = self.case_system.generate_case_report(
                customer_account=account_number,
                customer_name=customer_name,
                months=1,
                sbr_groups=["Ansible", "Ansible Automation Platform"]
            )
            
            if case_report.get('error'):
                raise Exception(f"Case discovery failed: {case_report['error']}")
            
            # Step 2: Generate portal content
            self.logger.info(f"Step 2: Generating portal content for {customer_name}")
            portal_content = self.template_renderer.render_portal_content(
                cases=case_report['cases']['all'],
                customer_name=customer_name,
                template_key=customer_key
            )
            
            # Step 3: Post to portal (if not in test mode)
            posting_result = None
            if not test_mode and group_id:
                self.logger.info(f"Step 3: Posting to portal for {customer_name}")
                posting_result = self.rfe_client.post_rfe_discussion(
                    customer_key=customer_key,
                    cases=case_report['cases']['all']
                )
            elif test_mode:
                self.logger.info(f"Step 3: Test mode - skipping portal posting for {customer_name}")
                posting_result = {'test_mode': True, 'content_generated': True}
            else:
                self.logger.warning(f"Step 3: No group ID configured for {customer_name} - skipping portal posting")
                posting_result = {'error': 'No group ID configured'}
            
            # Step 4: Generate results
            results = {
                'customer_key': customer_key,
                'customer_name': customer_name,
                'account_number': account_number,
                'group_id': group_id,
                'processing_timestamp': datetime.now().isoformat(),
                'test_mode': test_mode,
                'case_report': case_report,
                'portal_content': portal_content,
                'posting_result': posting_result,
                'success': posting_result is not None and not posting_result.get('error')
            }
            
            # Step 5: Save results
            self._save_processing_results(results)
            
            self.logger.info(f"RFE automation completed for {customer_name}")
            return results
            
        except Exception as e:
            self.logger.error(f"Error processing customer {customer_key}: {e}")
            return {
                'customer_key': customer_key,
                'error': str(e),
                'success': False,
                'processing_timestamp': datetime.now().isoformat()
            }
    
    def _save_processing_results(self, results: Dict[str, Any]):
        """Save processing results to file"""
        
        try:
            # Create results directory
            results_dir = "/tmp/rfe-automation-results"
            os.makedirs(results_dir, exist_ok=True)
            
            # Save results
            timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            customer_key = results['customer_key']
            
            results_file = f"{results_dir}/rfe-{customer_key}-{timestamp}.json"
            with open(results_file, 'w') as f:
                json.dump(results, f, indent=2)
            
            # Save portal content
            if results.get('portal_content'):
                content_file = f"{results_dir}/rfe-{customer_key}-{timestamp}.md"
                with open(content_file, 'w') as f:
                    f.write(results['portal_content'])
            
            self.logger.info(f"Processing results saved to: {results_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving processing results: {e}")
    
    def process_all_customers(self, test_mode: bool = False) -> Dict[str, Any]:
        """
        Process RFE automation for all configured customers
        
        Args:
            test_mode: If True, don't post to portal
            
        Returns:
            Dict with results for all customers
        """
        self.logger.info("Processing RFE automation for all customers")
        
        all_results = {}
        
        for customer_key in self.customer_config.keys():
            result = self.process_customer(customer_key, test_mode)
            all_results[customer_key] = result
        
        # Generate summary
        successful = [r for r in all_results.values() if r.get('success')]
        failed = [r for r in all_results.values() if not r.get('success')]
        
        summary = {
            'total_customers': len(all_results),
            'successful': len(successful),
            'failed': len(failed),
            'success_rate': len(successful) / len(all_results) * 100 if all_results else 0,
            'processing_timestamp': datetime.now().isoformat(),
            'test_mode': test_mode,
            'results': all_results
        }
        
        self.logger.info(f"All customers processed: {len(successful)}/{len(all_results)} successful")
        return summary
    
    def validate_customer_config(self, customer_key: str) -> Dict[str, Any]:
        """
        Validate customer configuration
        
        Args:
            customer_key: Customer key to validate
            
        Returns:
            Dict with validation results
        """
        validation_result = {
            'customer_key': customer_key,
            'valid': False,
            'issues': [],
            'warnings': []
        }
        
        try:
            customer_config = self.customer_config.get(customer_key)
            if not customer_config:
                validation_result['issues'].append(f"Customer {customer_key} not found in configuration")
                return validation_result
            
            # Check required fields
            required_fields = ['name', 'account_number', 'group_id']
            for field in required_fields:
                if not customer_config.get(field):
                    validation_result['issues'].append(f"Missing required field: {field}")
            
            # Check account number format
            account_number = customer_config.get('account_number')
            if account_number and not account_number.isdigit():
                validation_result['issues'].append(f"Invalid account number format: {account_number}")
            
            # Check group ID format
            group_id = customer_config.get('group_id')
            if group_id and not group_id.isdigit():
                validation_result['issues'].append(f"Invalid group ID format: {group_id}")
            
            # Test rhcase connectivity
            if account_number:
                try:
                    case_report = self.case_system.generate_case_report(
                        customer_account=account_number,
                        customer_name=customer_config.get('name', customer_key),
                        months=1
                    )
                    if case_report.get('error'):
                        validation_result['warnings'].append(f"Case discovery test failed: {case_report['error']}")
                    else:
                        validation_result['warnings'].append(f"Case discovery test passed: {case_report.get('total_cases', 0)} cases found")
                except Exception as e:
                    validation_result['warnings'].append(f"Case discovery test error: {e}")
            
            # Overall validation
            validation_result['valid'] = len(validation_result['issues']) == 0
            
        except Exception as e:
            validation_result['issues'].append(f"Validation error: {e}")
        
        return validation_result

def main():
    """Main function for command-line usage"""
    
    parser = argparse.ArgumentParser(description='Ultimate RFE Portal System')
    parser.add_argument('customer', nargs='?', help='Customer key to process (e.g., wellsfargo, tdbank)')
    parser.add_argument('--test', action='store_true', help='Test mode (no portal posting)')
    parser.add_argument('--all', action='store_true', help='Process all customers')
    parser.add_argument('--validate', action='store_true', help='Validate customer configuration')
    parser.add_argument('--environment', default='production', choices=['qa', 'stage', 'production'], help='Environment to use')
    
    args = parser.parse_args()
    
    # Initialize system
    system = UltimateRFEPortalSystem(environment=args.environment)
    
    print(f"🚀 Ultimate RFE Portal System - {args.environment.upper()}")
    print("=" * 50)
    
    if args.validate:
        # Validate configuration
        if args.customer:
            validation = system.validate_customer_config(args.customer)
            print(f"\n📋 Validation Results for {args.customer}:")
            print(f"   Valid: {'✅ YES' if validation['valid'] else '❌ NO'}")
            if validation['issues']:
                print(f"   Issues: {validation['issues']}")
            if validation['warnings']:
                print(f"   Warnings: {validation['warnings']}")
        else:
            print("❌ Customer key required for validation")
            return 1
    
    elif args.all:
        # Process all customers
        print(f"\n🔄 Processing all customers (test_mode={args.test})...")
        results = system.process_all_customers(test_mode=args.test)
        
        print(f"\n📊 Results Summary:")
        print(f"   Total Customers: {results['total_customers']}")
        print(f"   Successful: {results['successful']}")
        print(f"   Failed: {results['failed']}")
        print(f"   Success Rate: {results['success_rate']:.1f}%")
        
        if results['failed'] > 0:
            print(f"\n❌ Failed Customers:")
            for customer_key, result in results['results'].items():
                if not result.get('success'):
                    print(f"   - {customer_key}: {result.get('error', 'Unknown error')}")
        
        return 0 if results['successful'] == results['total_customers'] else 1
    
    elif args.customer:
        # Process single customer
        print(f"\n🔄 Processing {args.customer} (test_mode={args.test})...")
        result = system.process_customer(args.customer, test_mode=args.test)
        
        if result.get('success'):
            print(f"✅ {args.customer} processing completed successfully")
            print(f"   Cases Found: {result['case_report'].get('total_cases', 0)}")
            print(f"   Active Cases: {result['case_report'].get('active_cases', 0)}")
            print(f"   Portal Posted: {'Yes' if not args.test else 'No (test mode)'}")
        else:
            print(f"❌ {args.customer} processing failed: {result.get('error', 'Unknown error')}")
            return 1
    
    else:
        parser.print_help()
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
