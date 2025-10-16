#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
plugin: enhanced_tam_portfolio
short_description: Enhanced TAM Portfolio Configuration inventory plugin
version_added: "1.0.0"
description:
    - This plugin handles real-world TAM complexity including multi-TAM accounts,
      product specialization, coverage models, backup relationships, and account weights
    - Supports coordination between TAMs on shared accounts
    - Handles backup coverage and account prioritization
author:
    - Red Hat TAM Operations
options:
    tam_config_file:
        description:
            - Path to enhanced TAM portfolio configuration file
        required: false
        type: str
        default: "~/.config/rfe-automation/enhanced-tam-portfolio.yml"
    rhcase_path:
        description:
            - Path to rhcase executable
        required: false
        type: str
        default: "rhcase"
    validation_mode:
        description:
            - How to validate the portfolio
        required: false
        type: str
        choices: ['active_cases', 'all_cases', 'none']
        default: 'active_cases'
    include_coordination:
        description:
            - Whether to include multi-TAM coordination data
        required: false
        type: bool
        default: true
    include_backup_coverage:
        description:
            - Whether to include backup coverage information
        required: false
        type: bool
        default: true
'''

EXAMPLES = r'''
# Basic usage with enhanced portfolio
plugin: redhat.rfe_automation.enhanced_tam_portfolio

# Custom config file
plugin: redhat.rfe_automation.enhanced_tam_portfolio
tam_config_file: "/path/to/my-enhanced-portfolio.yml"

# Disable coordination data
plugin: redhat.rfe_automation.enhanced_tam_portfolio
include_coordination: false
'''

import json
import subprocess
import os
import yaml
from collections import defaultdict
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable
from ansible.errors import AnsibleError, AnsibleParserError


class InventoryModule(BaseInventoryPlugin, Constructable):
    """Enhanced TAM Portfolio Configuration inventory plugin"""

    NAME = 'redhat.rfe_automation.enhanced_tam_portfolio'

    def __init__(self):
        super(InventoryModule, self).__init__()

    def verify_file(self, path):
        """Verify if the file is a valid inventory source"""
        valid = False
        if super(InventoryModule, self).verify_file(path):
            if path.endswith(('enhanced-tam-portfolio.yml', 'enhanced-tam-portfolio.yaml')):
                valid = True
        return valid

    def parse(self, inventory, loader, path, cache=True):
        """Parse the inventory source"""
        super(InventoryModule, self).parse(inventory, loader, path, cache)

        # Get configuration
        config = self._read_config_data(path)
        self._set_config_options(config)

        try:
            # Load enhanced TAM portfolio
            portfolio_data = self._load_enhanced_tam_portfolio()
            
            # Validate portfolio against case data
            if self.validation_mode != 'none':
                validated_data = self._validate_enhanced_portfolio(portfolio_data)
            else:
                validated_data = portfolio_data
                
            # Generate suggestions
            suggestions = self._generate_enhanced_suggestions(validated_data)
            validated_data['suggestions'] = suggestions
            
            # Populate inventory
            self._populate_enhanced_inventory(validated_data)

        except Exception as e:
            raise AnsibleParserError(f"Failed to process enhanced TAM portfolio: {e}")

    def _set_config_options(self, config):
        """Set configuration options"""
        self.tam_config_file = os.path.expanduser(self.get_option('tam_config_file'))
        self.rhcase_path = self.get_option('rhcase_path')
        self.validation_mode = self.get_option('validation_mode')
        self.include_coordination = self.get_option('include_coordination')
        self.include_backup_coverage = self.get_option('include_backup_coverage')

    def _load_enhanced_tam_portfolio(self):
        """Load enhanced TAM portfolio configuration"""
        if not os.path.exists(self.tam_config_file):
            raise AnsibleError(f"Enhanced TAM portfolio config file not found: {self.tam_config_file}")
        
        try:
            with open(self.tam_config_file, 'r') as f:
                portfolio = yaml.safe_load(f)
        except Exception as e:
            raise AnsibleError(f"Failed to load enhanced TAM portfolio config: {e}")
        
        # Validate required fields
        required_fields = ['tam_name', 'accounts']
        for field in required_fields:
            if field not in portfolio:
                raise AnsibleError(f"Enhanced TAM portfolio config missing '{field}'")
        
        self.display.v(f"Loaded enhanced TAM portfolio for: {portfolio['tam_name']}")
        self.display.v(f"Portfolio contains {len(portfolio['accounts'])} accounts")
        
        return portfolio

    def _validate_enhanced_portfolio(self, portfolio):
        """Validate enhanced portfolio against real case data"""
        self.display.v("Validating enhanced portfolio against case data...")
        
        # Get case data for validation
        case_data = self._get_case_data()
        
        validated_accounts = []
        validation_results = {
            'validated_accounts': 0,
            'accounts_with_cases': 0,
            'accounts_without_cases': 0,
            'total_cases_found': 0,
            'multi_account_customers': 0,
            'shared_accounts': 0
        }
        
        # Track customers with multiple accounts
        customer_accounts = defaultdict(list)
        
        for account in portfolio['accounts']:
            customer_name = account['customer_name']
            account_numbers = account['account_numbers']
            
            customer_accounts[customer_name].extend(account_numbers)
            
            account_validation = {
                'account': account,
                'cases_found': 0,
                'active_cases': 0,
                'validated': False,
                'account_numbers_validated': []
            }
            
            # Validate each account number
            for account_number in account_numbers:
                account_cases = [case for case in case_data if case.get('accountNumber') == account_number]
                account_validation['cases_found'] += len(account_cases)
                account_validation['active_cases'] += len([case for case in account_cases if not case.get('isClosed', False)])
                
                if len(account_cases) > 0:
                    account_validation['account_numbers_validated'].append(account_number)
            
            account_validation['validated'] = len(account_validation['account_numbers_validated']) > 0
            validated_accounts.append(account_validation)
            
            if account_validation['validated']:
                validation_results['accounts_with_cases'] += 1
                validation_results['total_cases_found'] += account_validation['cases_found']
            else:
                validation_results['accounts_without_cases'] += 1
            
            validation_results['validated_accounts'] += 1
        
        # Count multi-account customers and shared accounts
        validation_results['multi_account_customers'] = len([k for k, v in customer_accounts.items() if len(v) > 1])
        validation_results['shared_accounts'] = len([acc for acc in portfolio['accounts'] if acc.get('coverage_model') == 'Shared'])
        
        self.display.v(f"Enhanced validation complete: {validation_results['accounts_with_cases']}/{validation_results['validated_accounts']} accounts have cases")
        self.display.v(f"Multi-account customers: {validation_results['multi_account_customers']}")
        self.display.v(f"Shared accounts: {validation_results['shared_accounts']}")
        
        return {
            'tam_name': portfolio['tam_name'],
            'tam_email': portfolio.get('tam_email', ''),
            'tam_type': portfolio.get('tam_type', ''),
            'region': portfolio.get('region', ''),
            'vertical': portfolio.get('vertical', ''),
            'backup_tam': portfolio.get('backup_tam', ''),
            'accounts': validated_accounts,
            'coordination': portfolio.get('coordination', {}),
            'backup_coverage': portfolio.get('backup_coverage', {}),
            'prioritization': portfolio.get('prioritization', {}),
            'reporting': portfolio.get('reporting', {}),
            'validation_results': validation_results,
            'case_data': case_data
        }

    def _get_case_data(self):
        """Get case data from rhcase for validation"""
        try:
            cmd = [self.rhcase_path, "list", "--all", "--format", "json"]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
                check=False
            )
            
            if result.returncode != 0:
                self.display.warning(f"rhcase command failed: {result.stderr}")
                return []
            
            cases = json.loads(result.stdout)
            if not isinstance(cases, list):
                return []
            
            # Filter based on validation mode
            if self.validation_mode == 'active_cases':
                cases = [case for case in cases if not case.get('isClosed', False)]
            
            return cases
            
        except Exception as e:
            self.display.warning(f"Failed to get case data: {e}")
            return []

    def _generate_enhanced_suggestions(self, validated_data):
        """Generate enhanced suggestions for portfolio maintenance"""
        self.display.v("Generating enhanced portfolio suggestions...")
        
        # Find accounts with case activity not in portfolio
        portfolio_account_numbers = set()
        for account_data in validated_data['accounts']:
            portfolio_account_numbers.update(account_data['account']['account_numbers'])
        
        case_data = validated_data['case_data']
        
        # Group cases by account
        account_cases = defaultdict(list)
        for case in case_data:
            account_number = case.get('accountNumber')
            if account_number and account_number not in portfolio_account_numbers:
                account_cases[account_number].append(case)
        
        # Generate suggestions
        suggestions = {
            'add_accounts': [],
            'coordination_opportunities': [],
            'backup_coverage_gaps': [],
            'prioritization_suggestions': []
        }
        
        # Suggest accounts with sufficient case activity
        for account_number, cases in account_cases.items():
            active_cases = [case for case in cases if not case.get('isClosed', False)]
            if len(active_cases) >= 3:  # Minimum threshold
                # Get account info from first case
                first_case = cases[0]
                account_info = first_case.get('account', {})
                
                suggestion = {
                    'account_number': account_number,
                    'customer_name': account_info.get('name', 'Unknown'),
                    'account_name': first_case.get('accountName', 'unknown'),
                    'active_cases': len(active_cases),
                    'total_cases': len(cases),
                    'sbr_groups': list(set(case.get('sbrGroup') for case in cases if case.get('sbrGroup'))),
                    'vertical': account_info.get('vertical', 'Unknown'),
                    'confidence': 'high' if len(active_cases) >= 5 else 'medium',
                    'reason': f"You have {len(active_cases)} active cases for this account",
                    'suggested_coverage_model': 'Shared' if len(active_cases) < 10 else 'Dedicated',
                    'suggested_account_weight': 4 if len(active_cases) >= 10 else 2
                }
                suggestions['add_accounts'].append(suggestion)
        
        # Sort suggestions by confidence and case count
        suggestions['add_accounts'].sort(key=lambda x: (x['confidence'] == 'high', x['active_cases']), reverse=True)
        
        self.display.v(f"Generated {len(suggestions['add_accounts'])} enhanced account suggestions")
        
        return suggestions

    def _populate_enhanced_inventory(self, validated_data):
        """Populate the Ansible inventory with enhanced TAM portfolio"""
        accounts = validated_data['accounts']
        coordination = validated_data.get('coordination', {})
        backup_coverage = validated_data.get('backup_coverage', {})
        prioritization = validated_data.get('prioritization', {})
        reporting = validated_data.get('reporting', {})
        suggestions = validated_data.get('suggestions', {})
        
        # Add TAM metadata
        self.inventory.set_variable('all', 'tam_name', validated_data['tam_name'])
        self.inventory.set_variable('all', 'tam_email', validated_data['tam_email'])
        self.inventory.set_variable('all', 'tam_type', validated_data['tam_type'])
        self.inventory.set_variable('all', 'region', validated_data['region'])
        self.inventory.set_variable('all', 'vertical', validated_data['vertical'])
        self.inventory.set_variable('all', 'backup_tam', validated_data['backup_tam'])
        self.inventory.set_variable('all', 'validation_results', validated_data['validation_results'])
        self.inventory.set_variable('all', 'coordination', coordination)
        self.inventory.set_variable('all', 'backup_coverage', backup_coverage)
        self.inventory.set_variable('all', 'prioritization', prioritization)
        self.inventory.set_variable('all', 'reporting', reporting)
        self.inventory.set_variable('all', 'suggestions', suggestions)
        
        # Create enhanced TAM portfolio group
        self.inventory.add_group('enhanced_tam_portfolio')
        
        # Add each account
        for account_data in accounts:
            account = account_data['account']
            customer_name = account['customer_name']
            
            # Create customer group
            group_name = f"customer_{customer_name.lower().replace(' ', '_')}"
            self.inventory.add_group(group_name)
            
            # Add each account number as a host
            for account_number in account['account_numbers']:
                host_name = f"host_{account_number}"
                self.inventory.add_host(host_name, group=group_name)
                
                # Set enhanced account variables
                account_vars = {
                    'customer_name': customer_name,
                    'account_name': account.get('account_name', 'unknown'),
                    'account_number': account_number,
                    'account_numbers': account['account_numbers'],
                    'tam_role': account.get('tam_role', 'Primary'),
                    'products': account.get('products', []),
                    'account_weight': account.get('account_weight', 1),
                    'coverage_model': account.get('coverage_model', 'Shared'),
                    'backup_tam': account.get('backup_tam', ''),
                    'account_exec': account.get('account_exec', ''),
                    'asa': account.get('asa', ''),
                    'cse': account.get('cse', ''),
                    'start_date': account.get('start_date', ''),
                    'end_date': account.get('end_date', ''),
                    'renewal_status': account.get('renewal_status', 'Active'),
                    'syb_booked_amt': account.get('syb_booked_amt', ''),
                    'notes': account.get('notes', ''),
                    'cases_found': account_data['cases_found'],
                    'active_cases': account_data['active_cases'],
                    'validated': account_data['validated'],
                    'account_numbers_validated': account_data['account_numbers_validated'],
                    'priority_components': account.get('products', []),
                    'validation_threshold': 0.99,
                    'data_quality_threshold': 0.95,
                    'report_types': reporting.get('report_types', ['rfe_bug_tracker', 'active_cases']),
                    'notifications_enabled': reporting.get('notification_preferences', {}).get('email', False),
                    'portal_posting_enabled': False
                }
                
                for var_name, var_value in account_vars.items():
                    self.inventory.set_variable(host_name, var_name, var_value)
                
                # Add to enhanced TAM portfolio group
                self.inventory.add_child('enhanced_tam_portfolio', group_name)
                
                # Add to product groups
                for product in account.get('products', []):
                    product_group = f"product_{product.lower()}"
                    if not self.inventory.groups.get(product_group):
                        self.inventory.add_group(product_group)
                    self.inventory.add_child(product_group, group_name)
                
                # Add to coverage model groups
                coverage_model = account.get('coverage_model', 'Shared')
                coverage_group = f"coverage_{coverage_model.lower()}"
                if not self.inventory.groups.get(coverage_group):
                    self.inventory.add_group(coverage_group)
                self.inventory.add_child(coverage_group, group_name)
                
                # Add to account weight groups
                account_weight = account.get('account_weight', 1)
                weight_group = f"weight_{account_weight}"
                if not self.inventory.groups.get(weight_group):
                    self.inventory.add_group(weight_group)
                self.inventory.add_child(weight_group, group_name)
        
        # Create coordination groups
        if self.include_coordination and coordination:
            self.inventory.add_group('shared_accounts')
            for shared_account in coordination.get('shared_accounts', []):
                customer_name = shared_account['customer_name']
                group_name = f"customer_{customer_name.lower().replace(' ', '_')}"
                self.inventory.add_child('shared_accounts', group_name)
        
        self.display.v(f"Populated enhanced inventory with {len(accounts)} TAM portfolio accounts")
