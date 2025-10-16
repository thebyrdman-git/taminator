#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
plugin: tam_portfolio
short_description: TAM Portfolio Configuration inventory plugin
version_added: "1.0.0"
description:
    - This plugin uses TAM-defined account portfolios for RFE automation
    - TAMs explicitly define their accounts in a configuration file
    - System validates portfolios against real case data
    - Provides smart suggestions for portfolio maintenance
author:
    - Red Hat TAM Operations
options:
    tam_config_file:
        description:
            - Path to TAM portfolio configuration file
        required: false
        type: str
        default: "~/.config/rfe-automation/tam-portfolio.yml"
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
    auto_suggestions:
        description:
            - Whether to provide smart suggestions
        required: false
        type: bool
        default: true
    min_cases_for_suggestion:
        description:
            - Minimum cases to suggest a new account
        required: false
        type: int
        default: 3
'''

EXAMPLES = r'''
# Basic usage with default config file
plugin: redhat.rfe_automation.tam_portfolio

# Custom config file location
plugin: redhat.rfe_automation.tam_portfolio
tam_config_file: "/path/to/my-portfolio.yml"

# Disable suggestions
plugin: redhat.rfe_automation.tam_portfolio
auto_suggestions: false

# Validate against all cases (not just active)
plugin: redhat.rfe_automation.tam_portfolio
validation_mode: all_cases
'''

import json
import subprocess
import os
import yaml
from collections import defaultdict
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable
from ansible.errors import AnsibleError, AnsibleParserError


class InventoryModule(BaseInventoryPlugin, Constructable):
    """TAM Portfolio Configuration inventory plugin"""

    NAME = 'redhat.rfe_automation.tam_portfolio'

    def __init__(self):
        super(InventoryModule, self).__init__()

    def verify_file(self, path):
        """Verify if the file is a valid inventory source"""
        valid = False
        if super(InventoryModule, self).verify_file(path):
            if path.endswith(('tam-portfolio.yml', 'tam-portfolio.yaml')):
                valid = True
        return valid

    def parse(self, inventory, loader, path, cache=True):
        """Parse the inventory source"""
        super(InventoryModule, self).parse(inventory, loader, path, cache)

        # Get configuration
        config = self._read_config_data(path)
        self._set_config_options(config)

        try:
            # Load TAM portfolio
            portfolio_data = self._load_tam_portfolio()
            
            # Validate portfolio against case data
            if self.validation_mode != 'none':
                validated_data = self._validate_portfolio(portfolio_data)
            else:
                validated_data = portfolio_data
                
            # Generate suggestions if enabled
            if self.auto_suggestions:
                suggestions = self._generate_suggestions(validated_data)
                validated_data['suggestions'] = suggestions
            
            # Populate inventory
            self._populate_inventory(validated_data)

        except Exception as e:
            raise AnsibleParserError(f"Failed to process TAM portfolio: {e}")

    def _set_config_options(self, config):
        """Set configuration options"""
        self.tam_config_file = os.path.expanduser(self.get_option('tam_config_file'))
        self.rhcase_path = self.get_option('rhcase_path')
        self.validation_mode = self.get_option('validation_mode')
        self.auto_suggestions = self.get_option('auto_suggestions')
        self.min_cases_for_suggestion = self.get_option('min_cases_for_suggestion')

    def _load_tam_portfolio(self):
        """Load TAM portfolio configuration"""
        if not os.path.exists(self.tam_config_file):
            raise AnsibleError(f"TAM portfolio config file not found: {self.tam_config_file}")
        
        try:
            with open(self.tam_config_file, 'r') as f:
                portfolio = yaml.safe_load(f)
        except Exception as e:
            raise AnsibleError(f"Failed to load TAM portfolio config: {e}")
        
        # Validate required fields
        if 'tam_name' not in portfolio:
            raise AnsibleError("TAM portfolio config missing 'tam_name'")
        if 'accounts' not in portfolio:
            raise AnsibleError("TAM portfolio config missing 'accounts'")
        
        self.display.v(f"Loaded TAM portfolio for: {portfolio['tam_name']}")
        self.display.v(f"Portfolio contains {len(portfolio['accounts'])} accounts")
        
        return portfolio

    def _validate_portfolio(self, portfolio):
        """Validate portfolio against real case data"""
        self.display.v("Validating portfolio against case data...")
        
        # Get case data for validation
        case_data = self._get_case_data()
        
        validated_accounts = []
        validation_results = {
            'validated_accounts': 0,
            'accounts_with_cases': 0,
            'accounts_without_cases': 0,
            'total_cases_found': 0
        }
        
        for account in portfolio['accounts']:
            account_number = account['account_number']
            account_cases = [case for case in case_data if case.get('accountNumber') == account_number]
            
            validation_result = {
                'account': account,
                'cases_found': len(account_cases),
                'active_cases': len([case for case in account_cases if not case.get('isClosed', False)]),
                'validated': len(account_cases) > 0
            }
            
            validated_accounts.append(validation_result)
            
            if len(account_cases) > 0:
                validation_results['accounts_with_cases'] += 1
                validation_results['total_cases_found'] += len(account_cases)
            else:
                validation_results['accounts_without_cases'] += 1
            
            validation_results['validated_accounts'] += 1
        
        self.display.v(f"Validation complete: {validation_results['accounts_with_cases']}/{validation_results['validated_accounts']} accounts have cases")
        
        return {
            'tam_name': portfolio['tam_name'],
            'tam_email': portfolio.get('tam_email', ''),
            'accounts': validated_accounts,
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

    def _generate_suggestions(self, validated_data):
        """Generate smart suggestions for portfolio maintenance"""
        if not self.auto_suggestions:
            return {}
        
        self.display.v("Generating portfolio suggestions...")
        
        # Find accounts with case activity not in portfolio
        portfolio_accounts = {acc['account']['account_number'] for acc in validated_data['accounts']}
        case_data = validated_data['case_data']
        
        # Group cases by account
        account_cases = defaultdict(list)
        for case in case_data:
            account_number = case.get('accountNumber')
            if account_number and account_number not in portfolio_accounts:
                account_cases[account_number].append(case)
        
        # Generate suggestions
        suggestions = {
            'add_accounts': [],
            'remove_accounts': [],
            'product_suggestions': []
        }
        
        # Suggest accounts with sufficient case activity
        for account_number, cases in account_cases.items():
            active_cases = [case for case in cases if not case.get('isClosed', False)]
            if len(active_cases) >= self.min_cases_for_suggestion:
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
                    'reason': f"You have {len(active_cases)} active cases for this account"
                }
                suggestions['add_accounts'].append(suggestion)
        
        # Sort suggestions by confidence and case count
        suggestions['add_accounts'].sort(key=lambda x: (x['confidence'] == 'high', x['active_cases']), reverse=True)
        
        self.display.v(f"Generated {len(suggestions['add_accounts'])} account suggestions")
        
        return suggestions

    def _populate_inventory(self, validated_data):
        """Populate the Ansible inventory with TAM portfolio"""
        accounts = validated_data['accounts']
        suggestions = validated_data.get('suggestions', {})
        
        # Add TAM metadata
        self.inventory.set_variable('all', 'tam_name', validated_data['tam_name'])
        self.inventory.set_variable('all', 'tam_email', validated_data['tam_email'])
        self.inventory.set_variable('all', 'validation_results', validated_data['validation_results'])
        self.inventory.set_variable('all', 'suggestions', suggestions)
        
        # Create TAM portfolio group
        self.inventory.add_group('tam_portfolio')
        
        # Add each account
        for account_data in accounts:
            account = account_data['account']
            account_name = account['account_name']
            
            # Create account group
            group_name = f"account_{account_name}"
            self.inventory.add_group(group_name)
            
            # Add account as host
            host_name = f"host_{account_name}"
            self.inventory.add_host(host_name, group=group_name)
            
            # Set account variables
            account_vars = {
                'customer_name': account['customer_name'],
                'account_name': account_name,
                'account_number': account['account_number'],
                'products': account.get('products', []),
                'vertical': account.get('vertical', 'Unknown'),
                'priority': account.get('priority', 'medium'),
                'description': account.get('description', ''),
                'cases_found': account_data['cases_found'],
                'active_cases': account_data['active_cases'],
                'validated': account_data['validated'],
                'priority_components': account.get('products', []),
                'validation_threshold': 0.99,
                'data_quality_threshold': 0.95,
                'report_types': ['rfe_bug_tracker', 'active_cases'],
                'notifications_enabled': False,
                'portal_posting_enabled': False
            }
            
            for var_name, var_value in account_vars.items():
                self.inventory.set_variable(host_name, var_name, var_value)
            
            # Add to TAM portfolio group
            self.inventory.add_child('tam_portfolio', group_name)
            
            # Add to product groups
            for product in account.get('products', []):
                product_group = f"product_{product.lower()}"
                if not self.inventory.groups.get(product_group):
                    self.inventory.add_group(product_group)
                self.inventory.add_child(product_group, group_name)
            
            # Add to vertical group
            vertical = account.get('vertical', 'Unknown').lower().replace(' ', '_')
            vertical_group = f"vertical_{vertical}"
            if not self.inventory.groups.get(vertical_group):
                self.inventory.add_group(vertical_group)
            self.inventory.add_child(vertical_group, group_name)
        
        self.display.v(f"Populated inventory with {len(accounts)} TAM portfolio accounts")
