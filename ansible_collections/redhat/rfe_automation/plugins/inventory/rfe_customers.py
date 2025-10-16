#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
plugin: rfe_customers
short_description: Dynamic inventory plugin for RFE automation customers
version_added: "1.0.0"
description:
    - This plugin dynamically discovers customers from rhcase data
    - Automatically creates inventory groups based on customer accounts
    - Provides customer-specific variables and configurations
    - Supports filtering by SBR groups and case types
author:
    - Red Hat TAM Operations
options:
    rhcase_path:
        description:
            - Path to rhcase executable
        required: false
        type: str
        default: "rhcase"
    sbr_groups:
        description:
            - List of SBR groups to filter by
        required: false
        type: list
        elements: str
        default: ["Ansible"]
    include_closed:
        description:
            - Whether to include closed cases in discovery
        required: false
        type: bool
        default: false
    min_cases:
        description:
            - Minimum number of cases required for a customer to be included
        required: false
        type: int
        default: 1
    cache:
        description:
            - Whether to cache the inventory data
        required: false
        type: bool
        default: true
    cache_plugin:
        description:
            - Cache plugin to use
        required: false
        type: str
        default: "memory"
    cache_timeout:
        description:
            - Cache timeout in seconds
        required: false
        type: int
        default: 300
'''

EXAMPLES = r'''
# Basic usage - discover all customers with Ansible cases
plugin: redhat.rfe_automation.rfe_customers

# Discover customers with multiple SBR groups
plugin: redhat.rfe_automation.rfe_customers
sbr_groups:
  - Ansible
  - OpenShift
  - RHEL

# Include only customers with at least 5 cases
plugin: redhat.rfe_automation.rfe_customers
min_cases: 5

# Disable caching for real-time data
plugin: redhat.rfe_automation.rfe_customers
cache: false
'''

import json
import subprocess
import os
from collections import defaultdict
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable
from ansible.errors import AnsibleError, AnsibleParserError


class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):
    """Dynamic inventory plugin for RFE automation customers"""

    NAME = 'redhat.rfe_automation.rfe_customers'

    def __init__(self):
        super(InventoryModule, self).__init__()
        self.cache_key = None
        self._cache = {}

    def verify_file(self, path):
        """Verify if the file is a valid inventory source"""
        valid = False
        if super(InventoryModule, self).verify_file(path):
            if path.endswith(('rfe_customers.yml', 'rfe_customers.yaml')):
                valid = True
        return valid

    def parse(self, inventory, loader, path, cache=True):
        """Parse the inventory source"""
        super(InventoryModule, self).parse(inventory, loader, path, cache)

        # Get configuration
        config = self._read_config_data(path)
        self._set_config_options(config)

        # Discover customers (simplified without caching for now)
        try:
            customers_data = self._discover_customers()
            self._populate_inventory(customers_data)
        except Exception as e:
            raise AnsibleParserError("Failed to discover customers: %s" % str(e))

    def _set_config_options(self, config):
        """Set configuration options"""
        self.rhcase_path = self.get_option('rhcase_path')
        self.sbr_groups = self.get_option('sbr_groups')
        self.include_closed = self.get_option('include_closed')
        self.min_cases = self.get_option('min_cases')

    def _discover_customers(self):
        """Discover customers from rhcase data"""
        self.display.v("Discovering customers from rhcase data...")

        try:
            # Run rhcase command to get all cases
            if self.sbr_groups:
                # Filter by specific SBR groups
                cmd = [
                    self.rhcase_path,
                    "list",
                    "--all",
                    "--format", "json",
                    "--includefilter", f"sbrGroup,{','.join(self.sbr_groups)}"
                ]
            else:
                # Get ALL cases regardless of SBR group (TAM perspective)
                cmd = [
                    self.rhcase_path,
                    "list",
                    "--all",
                    "--format", "json"
                ]

            self.display.v(f"Running command: {' '.join(cmd)}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
                check=False
            )

            if result.returncode != 0:
                self.display.v(f"rhcase stderr: {result.stderr}")
                raise AnsibleError(f"rhcase command failed with return code {result.returncode}: {result.stderr}")

            # Parse JSON output
            try:
                cases = json.loads(result.stdout)
                if not isinstance(cases, list):
                    raise AnsibleError("rhcase output is not a list")
                self.display.v(f"Parsed {len(cases)} cases from rhcase")
            except json.JSONDecodeError as e:
                self.display.v(f"Raw rhcase output: {result.stdout[:500]}...")
                raise AnsibleError(f"Failed to parse rhcase JSON output: {e}")

        except subprocess.TimeoutExpired:
            raise AnsibleError("rhcase command timed out")
        except FileNotFoundError:
            raise AnsibleError(f"rhcase executable not found at {self.rhcase_path}")
        except Exception as e:
            raise AnsibleError(f"Unexpected error running rhcase: {e}")

        # Group cases by customer and track TAM's product portfolio
        customers = defaultdict(lambda: {
            'cases': [],
            'account_info': {},
            'sbr_groups': set(),
            'case_types': set(),
            'total_cases': 0,
            'active_cases': 0,
            'closed_cases': 0
        })
        
        # Track TAM's product portfolio
        tam_sbr_groups = set()
        tam_verticals = set()

        for case in cases:
            account_number = case.get('accountNumber')
            account_name = case.get('accountName')
            is_closed = case.get('isClosed', False)

            if not account_number:
                continue

            # Skip closed cases if not requested
            if not self.include_closed and is_closed:
                continue

            customer = customers[account_number]
            customer['cases'].append(case)
            customer['total_cases'] += 1

            if is_closed:
                customer['closed_cases'] += 1
            else:
                customer['active_cases'] += 1

            # Collect account information
            if not customer['account_info']:
                customer['account_info'] = {
                    'account_number': account_number,
                    'account_name': account_name,
                    'customer_name': case.get('account', {}).get('name', account_name),
                    'vertical': case.get('account', {}).get('vertical', 'Unknown'),
                    'has_golden_ticket': case.get('account', {}).get('hasGoldenTicket', False),
                    'secure_support': case.get('account', {}).get('secureSupport', False)
                }

            # Collect SBR groups and case types
            sbr_group = case.get('sbrGroup')
            if sbr_group:
                customer['sbr_groups'].add(sbr_group)
                tam_sbr_groups.add(sbr_group)  # Track TAM's portfolio

            case_type = case.get('caseType')
            if case_type:
                customer['case_types'].add(case_type)
                
            # Track TAM's verticals
            vertical = case.get('account', {}).get('vertical')
            if vertical:
                tam_verticals.add(vertical)

        # Filter customers by minimum cases
        filtered_customers = {}
        for account_number, customer in customers.items():
            if customer['total_cases'] >= self.min_cases:
                # Convert sets to lists for JSON serialization
                customer['sbr_groups'] = list(customer['sbr_groups'])
                customer['case_types'] = list(customer['case_types'])
                filtered_customers[account_number] = customer

        self.display.v(f"Discovered {len(filtered_customers)} customers with {self.min_cases}+ cases")
        self.display.v(f"TAM's Product Portfolio: {sorted(tam_sbr_groups)}")
        self.display.v(f"TAM's Verticals: {sorted(tam_verticals)}")

        return {
            'customers': filtered_customers,
            'discovery_metadata': {
                'total_cases_processed': len(cases),
                'sbr_groups_filtered': self.sbr_groups if self.sbr_groups else 'ALL (Auto-discovered)',
                'tam_sbr_groups': sorted(list(tam_sbr_groups)),
                'tam_verticals': sorted(list(tam_verticals)),
                'include_closed': self.include_closed,
                'min_cases_threshold': self.min_cases,
                'customers_found': len(filtered_customers)
            }
        }

    def _populate_inventory(self, customers_data):
        """Populate the Ansible inventory with discovered customers"""
        customers = customers_data['customers']
        metadata = customers_data['discovery_metadata']

        # Add metadata as inventory variables
        self.inventory.set_variable('all', 'rfe_discovery_metadata', metadata)

        # Create customer groups
        for account_number, customer in customers.items():
            account_info = customer['account_info']
            customer_name = account_info['customer_name']
            account_name = account_info['account_name']

            # Create customer group
            group_name = f"customer_{account_name.lower()}"
            self.inventory.add_group(group_name)

            # Add customer as a host with unique name
            host_name = f"host_{account_name.lower()}"
            self.inventory.add_host(host_name, group=group_name)

            # Set customer variables
            customer_vars = {
                'customer_name': customer_name,
                'account_name': account_name,
                'account_number': account_number,
                'vertical': account_info['vertical'],
                'has_golden_ticket': account_info['has_golden_ticket'],
                'secure_support': account_info['secure_support'],
                'sbr_groups': customer['sbr_groups'],
                'case_types': customer['case_types'],
                'total_cases': customer['total_cases'],
                'active_cases': customer['active_cases'],
                'closed_cases': customer['closed_cases'],
                'priority_components': customer['sbr_groups'],  # Default to all SBR groups
                'validation_threshold': 0.99,
                'data_quality_threshold': 0.95,
                'report_types': ['rfe_bug_tracker', 'active_cases'],
                'notifications_enabled': False,
                'portal_posting_enabled': False
            }

            for var_name, var_value in customer_vars.items():
                self.inventory.set_variable(host_name, var_name, var_value)

            # Add to vertical group
            vertical = account_info['vertical'].lower().replace(' ', '_')
            vertical_group = f"vertical_{vertical}"
            if not self.inventory.groups.get(vertical_group):
                self.inventory.add_group(vertical_group)
            self.inventory.add_child(vertical_group, group_name)

            # Add to SBR groups
            for sbr_group in customer['sbr_groups']:
                sbr_group_name = f"sbr_{sbr_group.lower()}"
                if not self.inventory.groups.get(sbr_group_name):
                    self.inventory.add_group(sbr_group_name)
                self.inventory.add_child(sbr_group_name, group_name)

        # Create summary groups
        self.inventory.add_group('all_customers')
        for account_number in customers.keys():
            account_name = customers[account_number]['account_info']['account_name']
            group_name = f"customer_{account_name.lower()}"
            self.inventory.add_child('all_customers', group_name)

        self.display.v(f"Populated inventory with {len(customers)} customers")
