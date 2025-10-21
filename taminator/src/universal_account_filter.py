#!/usr/bin/env python3

"""
Universal Account Filter - Flexible Customer Account Management
Purpose: Provide robust, flexible account filtering for any TAM customer
Features: Dynamic account discovery, flexible filtering, validation, and error handling
"""

import os
import sys
import json
import yaml
import re
import subprocess
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum

class FilterType(Enum):
    """Types of account filters available"""
    ACCOUNT_NUMBER = "account_number"
    CUSTOMER_NAME = "customer_name"
    SBR_GROUP = "sbr_group"
    CASE_STATUS = "case_status"
    DATE_RANGE = "date_range"
    CUSTOM_FILTER = "custom_filter"

@dataclass
class AccountFilter:
    """Represents a single account filter configuration"""
    filter_type: FilterType
    value: Union[str, List[str], Dict[str, Any]]
    operator: str = "equals"  # equals, contains, starts_with, ends_with, in_list, regex
    case_sensitive: bool = False
    description: str = ""
    enabled: bool = True

@dataclass
class CustomerAccount:
    """Represents a customer account configuration"""
    account_number: str
    customer_name: str
    sbr_groups: List[str]
    filters: List[AccountFilter]
    group_id: Optional[str] = None
    portal_url: Optional[str] = None
    template_key: Optional[str] = None
    enabled: bool = True
    last_updated: Optional[str] = None
    confidence: str = "unknown"  # confirmed, extracted, manual, unknown

class UniversalAccountFilter:
    """Universal account filtering system for any TAM customer"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        
        # Configuration directories
        self.config_dir = os.path.expanduser("~/.config/tam-rfe-automation")
        self.accounts_file = os.path.join(self.config_dir, "customer_accounts.yaml")
        self.filters_file = os.path.join(self.config_dir, "account_filters.yaml")
        
        # Ensure config directory exists
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Load existing configurations
        self.customer_accounts = self._load_customer_accounts()
        self.account_filters = self._load_account_filters()
        
        # Default filter templates
        self.default_filters = {
            "ansible_sbr": AccountFilter(
                filter_type=FilterType.SBR_GROUP,
                value=["Ansible", "Ansible Automation Platform"],
                operator="in_list",
                description="Ansible-related SBR groups"
            ),
            "active_cases": AccountFilter(
                filter_type=FilterType.CASE_STATUS,
                value=["Waiting on Red Hat", "Waiting on Customer", "In Progress"],
                operator="in_list",
                description="Active case statuses"
            ),
            "recent_cases": AccountFilter(
                filter_type=FilterType.DATE_RANGE,
                value={"days": 30},
                operator="within_days",
                description="Cases within last 30 days"
            )
        }
        
        self.logger.info("Universal Account Filter initialized")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the account filter system"""
        logger = logging.getLogger('universal_account_filter')
        logger.setLevel(logging.INFO)
        
        # Create log file
        log_file = f"/tmp/universal-account-filter-{datetime.now().strftime('%Y%m%d')}.log"
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _load_customer_accounts(self) -> Dict[str, CustomerAccount]:
        """Load customer accounts from configuration file"""
        accounts = {}
        
        if os.path.exists(self.accounts_file):
            try:
                with open(self.accounts_file, 'r') as f:
                    data = yaml.safe_load(f)
                
                for account_id, account_data in data.get('accounts', {}).items():
                    # Convert filters from dict to AccountFilter objects
                    filters = []
                    for filter_data in account_data.get('filters', []):
                        filter_obj = AccountFilter(
                            filter_type=FilterType(filter_data['filter_type']),
                            value=filter_data['value'],
                            operator=filter_data.get('operator', 'equals'),
                            case_sensitive=filter_data.get('case_sensitive', False),
                            description=filter_data.get('description', ''),
                            enabled=filter_data.get('enabled', True)
                        )
                        filters.append(filter_obj)
                    
                    account = CustomerAccount(
                        account_number=account_data['account_number'],
                        customer_name=account_data['customer_name'],
                        sbr_groups=account_data.get('sbr_groups', []),
                        filters=filters,
                        group_id=account_data.get('group_id'),
                        portal_url=account_data.get('portal_url'),
                        template_key=account_data.get('template_key'),
                        enabled=account_data.get('enabled', True),
                        last_updated=account_data.get('last_updated'),
                        confidence=account_data.get('confidence', 'unknown')
                    )
                    accounts[account_id] = account
                
                self.logger.info(f"Loaded {len(accounts)} customer accounts")
                
            except Exception as e:
                self.logger.error(f"Failed to load customer accounts: {e}")
        
        return accounts
    
    def _load_account_filters(self) -> Dict[str, AccountFilter]:
        """Load account filters from configuration file"""
        filters = {}
        
        if os.path.exists(self.filters_file):
            try:
                with open(self.filters_file, 'r') as f:
                    data = yaml.safe_load(f)
                
                for filter_id, filter_data in data.get('filters', {}).items():
                    filter_obj = AccountFilter(
                        filter_type=FilterType(filter_data['filter_type']),
                        value=filter_data['value'],
                        operator=filter_data.get('operator', 'equals'),
                        case_sensitive=filter_data.get('case_sensitive', False),
                        description=filter_data.get('description', ''),
                        enabled=filter_data.get('enabled', True)
                    )
                    filters[filter_id] = filter_obj
                
                self.logger.info(f"Loaded {len(filters)} account filters")
                
            except Exception as e:
                self.logger.error(f"Failed to load account filters: {e}")
        
        return filters
    
    def _save_customer_accounts(self):
        """Save customer accounts to configuration file"""
        try:
            data = {'accounts': {}}
            
            for account_id, account in self.customer_accounts.items():
                # Convert AccountFilter objects to dict
                filters = []
                for filter_obj in account.filters:
                    filter_dict = {
                        'filter_type': filter_obj.filter_type.value,
                        'value': filter_obj.value,
                        'operator': filter_obj.operator,
                        'case_sensitive': filter_obj.case_sensitive,
                        'description': filter_obj.description,
                        'enabled': filter_obj.enabled
                    }
                    filters.append(filter_dict)
                
                account_dict = {
                    'account_number': account.account_number,
                    'customer_name': account.customer_name,
                    'sbr_groups': account.sbr_groups,
                    'filters': filters,
                    'group_id': account.group_id,
                    'portal_url': account.portal_url,
                    'template_key': account.template_key,
                    'enabled': account.enabled,
                    'last_updated': account.last_updated,
                    'confidence': account.confidence
                }
                data['accounts'][account_id] = account_dict
            
            with open(self.accounts_file, 'w') as f:
                yaml.dump(data, f, default_flow_style=False, indent=2)
            
            self.logger.info(f"Saved {len(self.customer_accounts)} customer accounts")
            
        except Exception as e:
            self.logger.error(f"Failed to save customer accounts: {e}")
            raise
    
    def add_customer_account(self, 
                           account_id: str,
                           account_number: str,
                           customer_name: str,
                           sbr_groups: List[str] = None,
                           filters: List[AccountFilter] = None,
                           group_id: str = None,
                           portal_url: str = None,
                           template_key: str = None) -> bool:
        """Add a new customer account with validation"""
        
        try:
            # Validate account number
            if not self._validate_account_number(account_number):
                raise ValueError(f"Invalid account number: {account_number}")
            
            # Check for duplicates
            for existing_id, existing_account in self.customer_accounts.items():
                if existing_account.account_number == account_number:
                    raise ValueError(f"Account number {account_number} already exists for {existing_id}")
            
            # Create default filters if none provided
            if filters is None:
                filters = [
                    self.default_filters["ansible_sbr"],
                    self.default_filters["active_cases"],
                    self.default_filters["recent_cases"]
                ]
            
            # Create customer account
            account = CustomerAccount(
                account_number=account_number,
                customer_name=customer_name,
                sbr_groups=sbr_groups or [],
                filters=filters,
                group_id=group_id,
                portal_url=portal_url,
                template_key=template_key or account_id.lower().replace(' ', '_'),
                enabled=True,
                last_updated=datetime.now().isoformat(),
                confidence="manual"
            )
            
            # Add to accounts
            self.customer_accounts[account_id] = account
            
            # Save configuration
            self._save_customer_accounts()
            
            self.logger.info(f"Added customer account: {account_id} ({customer_name})")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add customer account {account_id}: {e}")
            return False
    
    def _validate_account_number(self, account_number: str) -> bool:
        """Validate account number format"""
        # Basic validation - should be numeric and reasonable length
        if not account_number.isdigit():
            return False
        
        if len(account_number) < 4 or len(account_number) > 10:
            return False
        
        return True
    
    def discover_account_info(self, account_number: str) -> Dict[str, Any]:
        """Discover account information using rhcase"""
        
        try:
            # Use rhcase to get account information
            result = subprocess.run(
                ['rhcase', 'list', account_number, '--months', '1'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                raise Exception(f"rhcase failed: {result.stderr}")
            
            # Parse rhcase output to extract account information
            account_info = self._parse_rhcase_output(result.stdout)
            
            self.logger.info(f"Discovered account info for {account_number}")
            return account_info
            
        except Exception as e:
            self.logger.error(f"Failed to discover account info for {account_number}: {e}")
            return {
                'account_number': account_number,
                'customer_name': 'Unknown',
                'sbr_groups': [],
                'error': str(e)
            }
    
    def _parse_rhcase_output(self, output: str) -> Dict[str, Any]:
        """Parse rhcase output to extract account information"""
        
        account_info = {
            'account_number': '',
            'customer_name': 'Unknown',
            'sbr_groups': [],
            'case_count': 0,
            'recent_cases': []
        }
        
        try:
            lines = output.split('\n')
            
            for line in lines:
                line = line.strip()
                
                # Look for account number
                if 'Account:' in line:
                    account_match = re.search(r'Account:\s*(\d+)', line)
                    if account_match:
                        account_info['account_number'] = account_match.group(1)
                
                # Look for customer name
                if 'Customer:' in line:
                    customer_match = re.search(r'Customer:\s*(.+)', line)
                    if customer_match:
                        account_info['customer_name'] = customer_match.group(1).strip()
                
                # Look for SBR groups
                if 'SBR Group:' in line:
                    sbr_match = re.search(r'SBR Group:\s*(.+)', line)
                    if sbr_match:
                        sbr_group = sbr_match.group(1).strip()
                        if sbr_group not in account_info['sbr_groups']:
                            account_info['sbr_groups'].append(sbr_group)
                
                # Count cases
                if re.match(r'^\d{8}', line):  # Case number pattern
                    account_info['case_count'] += 1
                    
                    # Extract case info
                    case_parts = line.split('\t')
                    if len(case_parts) >= 3:
                        case_info = {
                            'case_number': case_parts[0],
                            'summary': case_parts[1] if len(case_parts) > 1 else '',
                            'status': case_parts[2] if len(case_parts) > 2 else ''
                        }
                        account_info['recent_cases'].append(case_info)
            
        except Exception as e:
            self.logger.error(f"Failed to parse rhcase output: {e}")
        
        return account_info
    
    def apply_filters(self, account_id: str, cases: List[Dict]) -> List[Dict]:
        """Apply filters to a list of cases for a specific account"""
        
        if account_id not in self.customer_accounts:
            self.logger.error(f"Account {account_id} not found")
            return []
        
        account = self.customer_accounts[account_id]
        filtered_cases = cases.copy()
        
        for filter_obj in account.filters:
            if not filter_obj.enabled:
                continue
            
            filtered_cases = self._apply_single_filter(filter_obj, filtered_cases)
            self.logger.info(f"Applied filter {filter_obj.filter_type.value}: {len(filtered_cases)} cases remaining")
        
        return filtered_cases
    
    def _apply_single_filter(self, filter_obj: AccountFilter, cases: List[Dict]) -> List[Dict]:
        """Apply a single filter to a list of cases"""
        
        filtered_cases = []
        
        for case in cases:
            if self._case_matches_filter(case, filter_obj):
                filtered_cases.append(case)
        
        return filtered_cases
    
    def _case_matches_filter(self, case: Dict, filter_obj: AccountFilter) -> bool:
        """Check if a case matches a specific filter"""
        
        try:
            if filter_obj.filter_type == FilterType.SBR_GROUP:
                return self._match_sbr_group(case, filter_obj)
            elif filter_obj.filter_type == FilterType.CASE_STATUS:
                return self._match_case_status(case, filter_obj)
            elif filter_obj.filter_type == FilterType.DATE_RANGE:
                return self._match_date_range(case, filter_obj)
            elif filter_obj.filter_type == FilterType.CUSTOM_FILTER:
                return self._match_custom_filter(case, filter_obj)
            else:
                self.logger.warning(f"Unknown filter type: {filter_obj.filter_type}")
                return True  # Include by default for unknown filters
                
        except Exception as e:
            self.logger.error(f"Error applying filter {filter_obj.filter_type.value}: {e}")
            return True  # Include by default on error
    
    def _match_sbr_group(self, case: Dict, filter_obj: AccountFilter) -> bool:
        """Match SBR group filter"""
        case_sbr = case.get('sbr_group', '').strip()
        
        if filter_obj.operator == "in_list":
            filter_values = filter_obj.value if isinstance(filter_obj.value, list) else [filter_obj.value]
            for filter_value in filter_values:
                if not filter_obj.case_sensitive:
                    if filter_value.lower() in case_sbr.lower():
                        return True
                else:
                    if filter_value in case_sbr:
                        return True
        
        return False
    
    def _match_case_status(self, case: Dict, filter_obj: AccountFilter) -> bool:
        """Match case status filter"""
        case_status = case.get('status', '').strip()
        
        if filter_obj.operator == "in_list":
            filter_values = filter_obj.value if isinstance(filter_obj.value, list) else [filter_obj.value]
            for filter_value in filter_values:
                if not filter_obj.case_sensitive:
                    if filter_value.lower() == case_status.lower():
                        return True
                else:
                    if filter_value == case_status:
                        return True
        
        return False
    
    def _match_date_range(self, case: Dict, filter_obj: AccountFilter) -> bool:
        """Match date range filter"""
        try:
            case_date_str = case.get('created_date', case.get('updated_date', ''))
            if not case_date_str:
                return True  # Include if no date available
            
            case_date = datetime.fromisoformat(case_date_str.replace('Z', '+00:00'))
            
            if filter_obj.operator == "within_days":
                days = filter_obj.value.get('days', 30)
                cutoff_date = datetime.now() - timedelta(days=days)
                return case_date >= cutoff_date
            
        except Exception as e:
            self.logger.error(f"Error matching date range: {e}")
        
        return True  # Include by default on error
    
    def _match_custom_filter(self, case: Dict, filter_obj: AccountFilter) -> bool:
        """Match custom filter using regex or other custom logic"""
        try:
            if filter_obj.operator == "regex":
                pattern = filter_obj.value
                case_text = json.dumps(case).lower() if not filter_obj.case_sensitive else json.dumps(case)
                return bool(re.search(pattern, case_text))
            
        except Exception as e:
            self.logger.error(f"Error matching custom filter: {e}")
        
        return True  # Include by default on error
    
    def validate_account_setup(self, account_id: str) -> Dict[str, Any]:
        """Validate account setup and configuration"""
        
        validation_result = {
            'account_id': account_id,
            'valid': False,
            'issues': [],
            'warnings': [],
            'recommendations': []
        }
        
        if account_id not in self.customer_accounts:
            validation_result['issues'].append(f"Account {account_id} not found")
            return validation_result
        
        account = self.customer_accounts[account_id]
        
        # Validate account number
        if not self._validate_account_number(account.account_number):
            validation_result['issues'].append(f"Invalid account number: {account.account_number}")
        
        # Validate customer name
        if not account.customer_name or account.customer_name == 'Unknown':
            validation_result['warnings'].append("Customer name not set or unknown")
        
        # Validate SBR groups
        if not account.sbr_groups:
            validation_result['warnings'].append("No SBR groups configured")
        
        # Validate filters
        if not account.filters:
            validation_result['warnings'].append("No filters configured")
        else:
            enabled_filters = [f for f in account.filters if f.enabled]
            if not enabled_filters:
                validation_result['warnings'].append("No enabled filters")
        
        # Validate group ID
        if not account.group_id:
            validation_result['warnings'].append("No portal group ID configured")
        
        # Test rhcase connectivity
        try:
            result = subprocess.run(
                ['rhcase', 'list', account.account_number, '--months', '1'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                validation_result['issues'].append(f"rhcase connectivity failed: {result.stderr}")
            else:
                validation_result['recommendations'].append("rhcase connectivity verified")
                
        except Exception as e:
            validation_result['issues'].append(f"rhcase test failed: {e}")
        
        # Overall validation
        validation_result['valid'] = len(validation_result['issues']) == 0
        
        return validation_result
    
    def get_account_summary(self, account_id: str) -> Dict[str, Any]:
        """Get summary information for an account"""
        
        if account_id not in self.customer_accounts:
            return {'error': f"Account {account_id} not found"}
        
        account = self.customer_accounts[account_id]
        
        # Get recent case count
        try:
            result = subprocess.run(
                ['rhcase', 'list', account.account_number, '--months', '1'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            case_count = 0
            if result.returncode == 0:
                case_count = len([line for line in result.stdout.split('\n') if re.match(r'^\d{8}', line.strip())])
            
        except Exception:
            case_count = -1  # Unknown
        
        summary = {
            'account_id': account_id,
            'account_number': account.account_number,
            'customer_name': account.customer_name,
            'sbr_groups': account.sbr_groups,
            'filter_count': len([f for f in account.filters if f.enabled]),
            'recent_case_count': case_count,
            'group_id': account.group_id,
            'portal_url': account.portal_url,
            'enabled': account.enabled,
            'confidence': account.confidence,
            'last_updated': account.last_updated
        }
        
        return summary
    
    def list_all_accounts(self) -> Dict[str, Dict[str, Any]]:
        """List all configured accounts with summaries"""
        
        accounts = {}
        
        for account_id in self.customer_accounts.keys():
            accounts[account_id] = self.get_account_summary(account_id)
        
        return accounts

def main():
    """Test the universal account filter system"""
    
    print("🧪 Universal Account Filter - Test Mode")
    print("=" * 45)
    
    filter_system = UniversalAccountFilter()
    
    # Test adding a customer account
    print("\n📋 Testing account management...")
    
    test_account_id = "test_customer"
    test_account_number = "123456"
    
    success = filter_system.add_customer_account(
        account_id=test_account_id,
        account_number=test_account_number,
        customer_name="Test Customer",
        sbr_groups=["Ansible", "OpenShift"],
        group_id="1234567"
    )
    
    if success:
        print(f"✅ Successfully added test account: {test_account_id}")
    else:
        print(f"❌ Failed to add test account: {test_account_id}")
    
    # Test validation
    print("\n🔍 Testing account validation...")
    validation = filter_system.validate_account_setup(test_account_id)
    
    print(f"Validation result: {'✅ VALID' if validation['valid'] else '❌ INVALID'}")
    if validation['issues']:
        print(f"Issues: {validation['issues']}")
    if validation['warnings']:
        print(f"Warnings: {validation['warnings']}")
    
    # Test account summary
    print("\n📊 Testing account summary...")
    summary = filter_system.get_account_summary(test_account_id)
    print(f"Account summary: {summary}")
    
    # List all accounts
    print("\n📋 All configured accounts:")
    all_accounts = filter_system.list_all_accounts()
    for account_id, account_info in all_accounts.items():
        print(f"  {account_id}: {account_info.get('customer_name', 'Unknown')}")
    
    print("\n🎉 Universal Account Filter test completed!")

if __name__ == '__main__':
    main()

