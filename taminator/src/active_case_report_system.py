#!/usr/bin/env python3

"""
Active Case Report System - RFE Case Discovery and Processing
Purpose: Discover and process RFE/Bug cases using rhcase tool
Features: Case discovery, filtering, enrichment, and data processing
"""

import os
import sys
import json
import subprocess
import re
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict

@dataclass
class CaseInfo:
    """Represents a single RFE/Bug case with all relevant information"""
    case_number: str
    summary: str
    status: str
    sbr_group: str
    created_date: str
    updated_date: str
    rfe_type: str  # 'RFE' or 'Bug'
    priority: str
    jira_refs: List[Dict] = None
    customer_account: str = ""
    raw_data: Dict = None

class ActiveCaseReportSystem:
    """System for discovering and processing active RFE/Bug cases"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        
        # SBR Group filters for case discovery (focused on Ansible)
        self.sbr_group_filters = [
            'Ansible',
            'Ansible Automation Platform',
            'Ansible Tower',
            'Ansible AWX',
            'Red Hat Ansible Automation Platform'
        ]
        
        # Case status filters
        self.active_statuses = [
            'Waiting on Red Hat',
            'Waiting on Customer',
            'In Progress',
            'New',
            'Assigned',
            'Under Investigation'
        ]
        
        self.closed_statuses = [
            'Closed',
            'Resolved',
            'Solved',
            'Done',
            'Complete',
            'Delivered'
        ]
        
        self.logger.info("Active Case Report System initialized")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for case report system"""
        logger = logging.getLogger('active_case_report_system')
        logger.setLevel(logging.INFO)
        
        # Create log file
        log_file = f"/tmp/active-case-report-{datetime.now().strftime('%Y%m%d')}.log"
        
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
    
    def discover_cases(self, 
                      customer_account: str, 
                      months: int = 1,
                      sbr_groups: List[str] = None) -> List[CaseInfo]:
        """
        Discover RFE/Bug cases for a customer using rhcase
        
        Args:
            customer_account: Customer account number
            months: Number of months to look back
            sbr_groups: Specific SBR groups to filter by
            
        Returns:
            List of CaseInfo objects
        """
        try:
            self.logger.info(f"Discovering cases for customer {customer_account}")
            
            # Build rhcase command
            cmd = ['rhcase', 'list', customer_account, '--months', str(months)]
            
            # Add SBR group filter if specified
            if sbr_groups:
                for sbr_group in sbr_groups:
                    cmd.extend(['--filter', f'SBR Group:{sbr_group}'])
            
            # Execute rhcase command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                self.logger.error(f"rhcase command failed: {result.stderr}")
                return []
            
            # Parse rhcase output
            cases = self._parse_rhcase_output(result.stdout, customer_account)
            
            self.logger.info(f"Discovered {len(cases)} cases for customer {customer_account}")
            return cases
            
        except subprocess.TimeoutExpired:
            self.logger.error(f"rhcase command timed out for customer {customer_account}")
            return []
        except Exception as e:
            self.logger.error(f"Error discovering cases for {customer_account}: {e}")
            return []
    
    def _parse_rhcase_output(self, output: str, customer_account: str) -> List[CaseInfo]:
        """Parse rhcase command output into CaseInfo objects"""
        
        cases = []
        lines = output.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and headers
            if not line or line.startswith('Case') or line.startswith('---'):
                continue
            
            # Parse case line (format: CaseNumber\tSummary\tStatus\tSBRGroup\t...)
            case_data = self._parse_case_line(line, customer_account)
            if case_data:
                cases.append(case_data)
        
        return cases
    
    def _parse_case_line(self, line: str, customer_account: str) -> Optional[CaseInfo]:
        """Parse a single case line from rhcase output"""
        
        try:
            # Split by tabs or multiple spaces
            parts = re.split(r'\t+|\s{2,}', line)
            
            if len(parts) < 3:
                return None
            
            case_number = parts[0].strip()
            summary = parts[1].strip()
            status = parts[2].strip()
            
            # Extract SBR group (usually in summary or separate field)
            sbr_group = self._extract_sbr_group(summary, parts)
            
            # Determine RFE/Bug type from summary
            rfe_type = self._determine_case_type(summary)
            
            # Extract priority from summary or status
            priority = self._extract_priority(summary, status)
            
            # Create CaseInfo object
            case_info = CaseInfo(
                case_number=case_number,
                summary=summary,
                status=status,
                sbr_group=sbr_group,
                created_date=datetime.now().strftime('%Y-%m-%d'),  # Placeholder
                updated_date=datetime.now().strftime('%Y-%m-%d'),  # Placeholder
                rfe_type=rfe_type,
                priority=priority,
                customer_account=customer_account,
                raw_data={'original_line': line}
            )
            
            return case_info
            
        except Exception as e:
            self.logger.error(f"Error parsing case line '{line}': {e}")
            return None
    
    def _extract_sbr_group(self, summary: str, parts: List[str]) -> str:
        """Extract SBR group from case summary or parts"""
        
        # Check if any of our known SBR groups are in the summary
        for sbr_group in self.sbr_group_filters:
            if sbr_group.lower() in summary.lower():
                return sbr_group
        
        # Check additional parts for SBR group
        for part in parts[3:]:
            for sbr_group in self.sbr_group_filters:
                if sbr_group.lower() in part.lower():
                    return sbr_group
        
        return 'Unknown'
    
    def _determine_case_type(self, summary: str) -> str:
        """Determine if case is RFE or Bug from summary"""
        
        summary_lower = summary.lower()
        
        if '[rfe]' in summary_lower or 'rfe:' in summary_lower:
            return 'RFE'
        elif '[bug]' in summary_lower or 'bug:' in summary_lower:
            return 'Bug'
        else:
            # Default to RFE if unclear
            return 'RFE'
    
    def _extract_priority(self, summary: str, status: str) -> str:
        """Extract priority from summary or status"""
        
        text = (summary + ' ' + status).lower()
        
        if any(priority in text for priority in ['critical', 'urgent', 'high']):
            return 'High'
        elif any(priority in text for priority in ['medium', 'normal']):
            return 'Medium'
        elif any(priority in text for priority in ['low', 'minor']):
            return 'Low'
        else:
            return 'Medium'
    
    def filter_cases_by_sbr_group(self, cases: List[CaseInfo], sbr_groups: List[str]) -> List[CaseInfo]:
        """Filter cases by SBR group"""
        
        filtered_cases = []
        
        for case in cases:
            if case.sbr_group in sbr_groups:
                filtered_cases.append(case)
        
        return filtered_cases
    
    def filter_cases_by_status(self, cases: List[CaseInfo], statuses: List[str]) -> List[CaseInfo]:
        """Filter cases by status"""
        
        filtered_cases = []
        
        for case in cases:
            if case.status in statuses:
                filtered_cases.append(case)
        
        return filtered_cases
    
    def enrich_case_data(self, cases: List[CaseInfo]) -> List[CaseInfo]:
        """Enrich case data with additional information"""
        
        enriched_cases = []
        
        for case in cases:
            try:
                # Get detailed case information
                detailed_case = self._get_case_details(case.case_number)
                if detailed_case:
                    # Merge detailed information
                    case.jira_refs = detailed_case.get('jira_refs', [])
                    case.created_date = detailed_case.get('created_date', case.created_date)
                    case.updated_date = detailed_case.get('updated_date', case.updated_date)
                
                enriched_cases.append(case)
                
            except Exception as e:
                self.logger.error(f"Error enriching case {case.case_number}: {e}")
                enriched_cases.append(case)  # Add case without enrichment
        
        return enriched_cases
    
    def _get_case_details(self, case_number: str) -> Optional[Dict]:
        """Get detailed information for a specific case"""
        
        try:
            # Use rhcase to get case details
            result = subprocess.run(
                ['rhcase', 'show', case_number],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                return None
            
            # Parse detailed case information
            details = self._parse_case_details(result.stdout)
            return details
            
        except Exception as e:
            self.logger.error(f"Error getting case details for {case_number}: {e}")
            return None
    
    def _parse_case_details(self, output: str) -> Dict:
        """Parse detailed case information from rhcase show output"""
        
        details = {
            'jira_refs': [],
            'created_date': '',
            'updated_date': ''
        }
        
        lines = output.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Extract dates
            if 'Created:' in line:
                details['created_date'] = line.split('Created:')[1].strip()
            elif 'Updated:' in line:
                details['updated_date'] = line.split('Updated:')[1].strip()
            
            # Extract JIRA references
            if 'JIRA:' in line or 'Bug:' in line:
                jira_ref = line.split(':')[1].strip()
                details['jira_refs'].append({'jira_id': jira_ref})
        
        return details
    
    def generate_case_report(self, 
                           customer_account: str,
                           customer_name: str,
                           months: int = 1,
                           sbr_groups: List[str] = None) -> Dict[str, Any]:
        """
        Generate comprehensive case report for a customer
        
        Args:
            customer_account: Customer account number
            customer_name: Customer name for display
            months: Number of months to look back
            sbr_groups: Specific SBR groups to filter by
            
        Returns:
            Dict with case report data
        """
        try:
            self.logger.info(f"Generating case report for {customer_name} ({customer_account})")
            
            # Discover cases
            all_cases = self.discover_cases(customer_account, months, sbr_groups)
            
            # Filter by SBR groups if specified
            if sbr_groups:
                filtered_cases = self.filter_cases_by_sbr_group(all_cases, sbr_groups)
            else:
                filtered_cases = all_cases
            
            # Enrich case data
            enriched_cases = self.enrich_case_data(filtered_cases)
            
            # Categorize cases
            active_cases = self.filter_cases_by_status(enriched_cases, self.active_statuses)
            closed_cases = self.filter_cases_by_status(enriched_cases, self.closed_statuses)
            
            # Filter by type
            active_rfe_cases = [c for c in active_cases if c.rfe_type == 'RFE']
            active_bug_cases = [c for c in active_cases if c.rfe_type == 'Bug']
            
            # Generate report
            report = {
                'customer_account': customer_account,
                'customer_name': customer_name,
                'report_date': datetime.now().isoformat(),
                'months_covered': months,
                'sbr_groups_filtered': sbr_groups,
                'total_cases': len(enriched_cases),
                'active_cases': len(active_cases),
                'closed_cases': len(closed_cases),
                'active_rfe_cases': len(active_rfe_cases),
                'active_bug_cases': len(active_bug_cases),
                'cases': {
                    'all': [asdict(c) for c in enriched_cases],
                    'active': [asdict(c) for c in active_cases],
                    'closed': [asdict(c) for c in closed_cases],
                    'active_rfe': [asdict(c) for c in active_rfe_cases],
                    'active_bug': [asdict(c) for c in active_bug_cases]
                }
            }
            
            self.logger.info(f"Case report generated for {customer_name}: {len(enriched_cases)} total cases")
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating case report for {customer_name}: {e}")
            return {
                'customer_account': customer_account,
                'customer_name': customer_name,
                'error': str(e),
                'cases': {'all': [], 'active': [], 'closed': [], 'active_rfe': [], 'active_bug': []}
            }

def main():
    """Test the active case report system"""
    
    print("🧪 Active Case Report System - Test Mode")
    print("=" * 45)
    
    # Initialize system
    case_system = ActiveCaseReportSystem()
    
    # Test with Wells Fargo
    print("\n📋 Testing Wells Fargo case discovery...")
    wells_fargo_report = case_system.generate_case_report(
        customer_account="838043",
        customer_name="Wells Fargo",
        months=1,
        sbr_groups=["Ansible", "OpenShift"]
    )
    
    print(f"Wells Fargo Report:")
    print(f"  Total Cases: {wells_fargo_report.get('total_cases', 0)}")
    print(f"  Active Cases: {wells_fargo_report.get('active_cases', 0)}")
    print(f"  Active RFE: {wells_fargo_report.get('active_rfe_cases', 0)}")
    print(f"  Active Bug: {wells_fargo_report.get('active_bug_cases', 0)}")
    
    # Test with TD Bank
    print("\n📋 Testing TD Bank case discovery...")
    td_bank_report = case_system.generate_case_report(
        customer_account="1912101",
        customer_name="TD Bank",
        months=1,
        sbr_groups=["Ansible", "OpenShift"]
    )
    
    print(f"TD Bank Report:")
    print(f"  Total Cases: {td_bank_report.get('total_cases', 0)}")
    print(f"  Active Cases: {td_bank_report.get('active_cases', 0)}")
    print(f"  Active RFE: {td_bank_report.get('active_rfe_cases', 0)}")
    print(f"  Active Bug: {td_bank_report.get('active_bug_cases', 0)}")
    
    # Save test reports
    test_dir = "/tmp/rfe-case-reports"
    os.makedirs(test_dir, exist_ok=True)
    
    with open(f"{test_dir}/wells-fargo-report.json", 'w') as f:
        json.dump(wells_fargo_report, f, indent=2)
    
    with open(f"{test_dir}/td-bank-report.json", 'w') as f:
        json.dump(td_bank_report, f, indent=2)
    
    print(f"\n📁 Test reports saved to: {test_dir}")
    print("✅ Active Case Report System test completed successfully!")
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
