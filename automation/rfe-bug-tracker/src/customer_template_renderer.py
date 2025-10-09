#!/usr/bin/env python3

"""
Customer Template Renderer - Professional RFE Report Generation
Purpose: Generate professional 3-table RFE reports for customer portal posting
Features: Customer-specific templates, case filtering, professional formatting
"""

import os
import json
import yaml
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from jinja2 import Template, Environment, FileSystemLoader
import logging

@dataclass
class CaseData:
    """Represents a single RFE/Bug case"""
    case_number: str
    summary: str
    status: str
    sbr_group: str
    created_date: str
    updated_date: str
    rfe_type: str  # 'RFE' or 'Bug'
    priority: str = "Medium"
    jira_refs: List[Dict] = None

class CustomerTemplateRenderer:
    """Professional template renderer for customer RFE reports"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        
        # Template configuration
        self.template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        os.makedirs(self.template_dir, exist_ok=True)
        
        # Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader(self.template_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Customer-specific templates
        self.customer_templates = {
            'wellsfargo': {
                'title_format': 'Weekly Troubleshooting Case Report - {customer} - {date}',
                'include_executive_summary': True,
                'max_cases_display': 20,
                'style': 'executive'
            },
            'tdbank': {
                'title_format': 'TD Bank Weekly Case Summary - {date}',
                'include_executive_summary': False,
                'max_cases_display': 15,
                'style': 'concise'
            },
            'jpmc': {
                'title_format': 'Weekly Troubleshooting Status - {customer} - {date}',
                'include_executive_summary': True,
                'max_cases_display': 25,
                'style': 'detailed'
            },
            'fanniemae': {
                'title_format': 'Fannie Mae Weekly Case Report - {date}',
                'include_executive_summary': True,
                'max_cases_display': 18,
                'style': 'standard'
            }
        }
        
        # Create default templates
        self._create_default_templates()
        
        self.logger.info("Customer Template Renderer initialized")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for template renderer"""
        logger = logging.getLogger('customer_template_renderer')
        logger.setLevel(logging.INFO)
        
        # Create log file
        log_file = f"/tmp/customer-template-renderer-{datetime.now().strftime('%Y%m%d')}.log"
        
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
    
    def _create_default_templates(self):
        """Create default Jinja2 templates for RFE reports"""
        
        # Main RFE report template
        main_template = """# {{ title }}

{% if include_executive_summary %}
## Executive Summary
- **Total Active Cases**: {{ active_cases|length }} ({{ active_rfe_cases|length }} RFE, {{ active_bug_cases|length }} Bug)
- **Cases Waiting on Red Hat**: {{ cases_waiting_on_redhat|length }}
- **Cases Waiting on Customer**: {{ cases_waiting_on_customer|length }}
- **Cases In Progress**: {{ cases_in_progress|length }}
- **Recent Closures**: {{ closed_cases|length }} cases resolved this week

{% endif %}
## Active RFE Cases

{% if active_rfe_cases %}
| Case Number | Summary | Status | SBR Group | Created | Priority |
|-------------|---------|--------|-----------|---------|----------|
{% for case in active_rfe_cases[:max_cases_display] %}
| {{ case.case_number }} | {{ case.summary }} | {{ case.status }} | {{ case.sbr_group }} | {{ case.created_date }} | {{ case.priority }} |
{% endfor %}
{% else %}
*No active RFE cases found.*
{% endif %}

## Active Bug Cases

{% if active_bug_cases %}
| Case Number | Summary | Status | SBR Group | Created | Priority |
|-------------|---------|--------|-----------|---------|----------|
{% for case in active_bug_cases[:max_cases_display] %}
| {{ case.case_number }} | {{ case.summary }} | {{ case.status }} | {{ case.sbr_group }} | {{ case.created_date }} | {{ case.priority }} |
{% endfor %}
{% else %}
*No active bug cases found.*
{% endif %}

## Closed Cases (Recent)

{% if closed_cases %}
| Case Number | Summary | Status | SBR Group | Closed | Resolution |
|-------------|---------|--------|-----------|--------|------------|
{% for case in closed_cases[:max_cases_display] %}
| {{ case.case_number }} | {{ case.summary }} | {{ case.status }} | {{ case.sbr_group }} | {{ case.updated_date }} | {{ case.resolution or 'Completed' }} |
{% endfor %}
{% else %}
*No recent closed cases found.*
{% endif %}

---
**🤖 Automated Update via Red Hat Customer Portal API**
*Last updated: {{ timestamp }}*
*Generated by: RFE Discussion API Client*
"""
        
        # Save main template
        template_file = os.path.join(self.template_dir, 'rfe_report.md')
        with open(template_file, 'w') as f:
            f.write(main_template)
        
        self.logger.info("Default templates created")
    
    def parse_case_data(self, raw_cases: List[Dict]) -> List[CaseData]:
        """Parse raw case data into structured CaseData objects"""
        
        parsed_cases = []
        
        for raw_case in raw_cases:
            try:
                # Extract case information
                case_data = CaseData(
                    case_number=raw_case.get('caseNumber', ''),
                    summary=raw_case.get('summary', ''),
                    status=raw_case.get('status', ''),
                    sbr_group=raw_case.get('sbr_group', 'Unknown'),
                    created_date=raw_case.get('created_date', ''),
                    updated_date=raw_case.get('updated_date', ''),
                    rfe_type=raw_case.get('rfe_type', 'Unknown'),
                    priority=raw_case.get('priority', 'Medium'),
                    jira_refs=raw_case.get('jira_refs', [])
                )
                
                parsed_cases.append(case_data)
                
            except Exception as e:
                self.logger.error(f"Error parsing case data: {e}")
                continue
        
        return parsed_cases
    
    def filter_cases_by_status(self, cases: List[CaseData]) -> Dict[str, List[CaseData]]:
        """Filter cases by status into active and closed categories"""
        
        active_cases = []
        closed_cases = []
        
        for case in cases:
            status_lower = case.status.lower()
            
            # Check if case is closed
            if any(closed_status in status_lower for closed_status in 
                   ['closed', 'resolved', 'solved', 'done', 'complete', 'delivered']):
                closed_cases.append(case)
            else:
                active_cases.append(case)
        
        return {
            'active': active_cases,
            'closed': closed_cases
        }
    
    def filter_cases_by_type(self, cases: List[CaseData]) -> Dict[str, List[CaseData]]:
        """Filter cases by RFE/Bug type"""
        
        rfe_cases = []
        bug_cases = []
        
        for case in cases:
            if case.rfe_type.lower() == 'rfe':
                rfe_cases.append(case)
            elif case.rfe_type.lower() == 'bug':
                bug_cases.append(case)
            else:
                # Default to RFE if type is unclear
                rfe_cases.append(case)
        
        return {
            'rfe': rfe_cases,
            'bug': bug_cases
        }
    
    def categorize_cases_by_status(self, cases: List[CaseData]) -> Dict[str, List[CaseData]]:
        """Categorize cases by specific status types"""
        
        categories = {
            'waiting_on_redhat': [],
            'waiting_on_customer': [],
            'in_progress': [],
            'other': []
        }
        
        for case in cases:
            status_lower = case.status.lower()
            
            if any(status in status_lower for status in ['waiting on red hat', 'waiting on redhat']):
                categories['waiting_on_redhat'].append(case)
            elif any(status in status_lower for status in ['waiting on customer', 'waiting on client']):
                categories['waiting_on_customer'].append(case)
            elif any(status in status_lower for status in ['in progress', 'in-progress', 'progress']):
                categories['in_progress'].append(case)
            else:
                categories['other'].append(case)
        
        return categories
    
    def render_portal_content(self, 
                            cases: List[Dict], 
                            customer_name: str, 
                            template_key: str = None) -> str:
        """
        Render professional portal content for customer
        
        Args:
            cases: List of case dictionaries
            customer_name: Customer name for display
            template_key: Customer-specific template key
            
        Returns:
            Rendered markdown content for portal posting
        """
        try:
            self.logger.info(f"Rendering portal content for {customer_name}")
            
            # Get customer template configuration
            if not template_key:
                template_key = customer_name.lower().replace(' ', '_')
            
            template_config = self.customer_templates.get(
                template_key, 
                self.customer_templates['wellsfargo']  # Default to Wells Fargo template
            )
            
            # Parse case data
            parsed_cases = self.parse_case_data(cases)
            
            # Filter cases by status
            status_filtered = self.filter_cases_by_status(parsed_cases)
            active_cases = status_filtered['active']
            closed_cases = status_filtered['closed']
            
            # Filter active cases by type
            type_filtered = self.filter_cases_by_type(active_cases)
            active_rfe_cases = type_filtered['rfe']
            active_bug_cases = type_filtered['bug']
            
            # Categorize cases by status
            status_categories = self.categorize_cases_by_status(active_cases)
            
            # Prepare template context
            context = {
                'title': template_config['title_format'].format(
                    customer=customer_name,
                    date=datetime.now().strftime('%B %d, %Y')
                ),
                'customer_name': customer_name,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S EST'),
                'include_executive_summary': template_config['include_executive_summary'],
                'max_cases_display': template_config['max_cases_display'],
                'active_cases': active_cases,
                'active_rfe_cases': active_rfe_cases,
                'active_bug_cases': active_bug_cases,
                'closed_cases': closed_cases,
                'cases_waiting_on_redhat': status_categories['waiting_on_redhat'],
                'cases_waiting_on_customer': status_categories['waiting_on_customer'],
                'cases_in_progress': status_categories['in_progress']
            }
            
            # Load and render template
            template = self.jinja_env.get_template('rfe_report.md')
            rendered_content = template.render(**context)
            
            self.logger.info(f"Portal content rendered successfully for {customer_name}")
            return rendered_content
            
        except Exception as e:
            self.logger.error(f"Error rendering portal content for {customer_name}: {e}")
            return f"# Error generating report for {customer_name}\n\nAn error occurred while generating the RFE report. Please contact your TAM for assistance."
    
    def render_test_content(self, customer_name: str) -> str:
        """Generate test content for verification"""
        
        # Create sample test cases
        test_cases = [
            {
                'caseNumber': '04244831',
                'summary': '[RFE] Test Ansible Automation Platform integration',
                'status': 'Waiting on Red Hat',
                'sbr_group': 'Ansible',
                'created_date': '2024-12-01',
                'updated_date': '2024-12-19',
                'rfe_type': 'RFE',
                'priority': 'High'
            },
            {
                'caseNumber': '04244832',
                'summary': '[BUG] Test Ansible Tower job execution timeout',
                'status': 'In Progress',
                'sbr_group': 'Ansible',
                'created_date': '2024-12-02',
                'updated_date': '2024-12-19',
                'rfe_type': 'Bug',
                'priority': 'Medium'
            },
            {
                'caseNumber': '04244825',
                'summary': '[RFE] Test Red Hat Satellite integration',
                'status': 'Closed',
                'sbr_group': 'Satellite',
                'created_date': '2024-12-01',
                'updated_date': '2024-12-15',
                'rfe_type': 'RFE',
                'priority': 'Low'
            }
        ]
        
        return self.render_portal_content(test_cases, customer_name)

def main():
    """Test the customer template renderer"""
    
    print("🧪 Customer Template Renderer - Test Mode")
    print("=" * 45)
    
    # Initialize renderer
    renderer = CustomerTemplateRenderer()
    
    # Test with Wells Fargo
    print("\n📋 Testing Wells Fargo template...")
    wells_fargo_content = renderer.render_test_content("Wells Fargo")
    print(f"Generated {len(wells_fargo_content)} characters of content")
    
    # Test with TD Bank
    print("\n📋 Testing TD Bank template...")
    td_bank_content = renderer.render_test_content("TD Bank")
    print(f"Generated {len(td_bank_content)} characters of content")
    
    # Save test outputs
    test_dir = "/tmp/rfe-template-tests"
    os.makedirs(test_dir, exist_ok=True)
    
    with open(f"{test_dir}/wells-fargo-test.md", 'w') as f:
        f.write(wells_fargo_content)
    
    with open(f"{test_dir}/td-bank-test.md", 'w') as f:
        f.write(td_bank_content)
    
    print(f"\n📁 Test outputs saved to: {test_dir}")
    print("✅ Customer Template Renderer test completed successfully!")
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
