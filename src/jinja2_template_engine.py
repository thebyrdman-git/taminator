#!/usr/bin/env python3

"""
Jinja2 Template Engine for RFE Automation
Purpose: Professional, reliable report generation using Jinja2 templates
Features: Template management, data processing, validation, error handling
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from jinja2 import Environment, FileSystemLoader, Template, select_autoescape
from jinja2.exceptions import TemplateError, UndefinedError

class Jinja2TemplateEngine:
    """Professional Jinja2 template engine for RFE report generation"""
    
    def __init__(self, template_dir: str = "templates"):
        self.logger = self._setup_logging()
        self.template_dir = template_dir
        
        # Initialize Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add custom filters
        self._add_custom_filters()
        
        self.logger.info(f"Jinja2 Template Engine initialized with template directory: {template_dir}")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for template engine"""
        logger = logging.getLogger('jinja2_template_engine')
        logger.setLevel(logging.INFO)
        
        # Create log file
        log_file = f"/tmp/jinja2-template-engine-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _add_custom_filters(self):
        """Add custom Jinja2 filters for professional report generation"""
        
        @self.env.filter('format_date')
        def format_date(date_str: str, format_str: str = '%Y-%m-%d') -> str:
            """Format date string to specified format"""
            try:
                if not date_str:
                    return ''
                
                # Handle ISO format with Z
                if date_str.endswith('Z'):
                    date_str = date_str[:-1] + '+00:00'
                
                date_obj = datetime.fromisoformat(date_str)
                return date_obj.strftime(format_str)
            except Exception:
                return date_str
        
        @self.env.filter('truncate_summary')
        def truncate_summary(summary: str, length: int = 100) -> str:
            """Truncate summary to specified length"""
            if not summary:
                return ''
            
            if len(summary) <= length:
                return summary
            
            return summary[:length-3] + '...'
        
        @self.env.filter('format_case_number')
        def format_case_number(case_number: str) -> str:
            """Format case number with proper linking"""
            if not case_number:
                return ''
            
            # Remove any existing formatting
            case_number = case_number.strip()
            
            # Create Red Hat case link
            return f"[{case_number}](https://access.redhat.com/support/cases/#/case/{case_number})"
        
        @self.env.filter('format_jira_id')
        def format_jira_id(jira_id: str) -> str:
            """Format JIRA ID with proper linking"""
            if not jira_id:
                return ''
            
            jira_id = jira_id.strip()
            
            # Create JIRA link
            return f"[{jira_id}](https://issues.redhat.com/browse/{jira_id})"
        
        @self.env.filter('calculate_percentage')
        def calculate_percentage(count: int, total: int) -> float:
            """Calculate percentage with proper handling"""
            if total == 0:
                return 0.0
            return round((count / total) * 100, 1)
        
        @self.env.filter('format_business_impact')
        def format_business_impact(case_type: str, product: str) -> str:
            """Generate business impact statement based on case type and product"""
            if not case_type or not product:
                return 'Enhanced operational efficiency'
            
            case_type_lower = case_type.lower()
            product_lower = product.lower()
            
            if 'rfe' in case_type_lower or 'enhancement' in case_type_lower:
                if 'ansible' in product_lower:
                    return 'Improved automation capabilities and operational efficiency'
                elif 'openshift' in product_lower:
                    return 'Enhanced container platform functionality and scalability'
                elif 'rhel' in product_lower:
                    return 'Strengthened enterprise Linux platform capabilities'
                else:
                    return 'Enhanced product functionality and user experience'
            
            elif 'bug' in case_type_lower or 'defect' in case_type_lower:
                if 'ansible' in product_lower:
                    return 'Improved automation reliability and stability'
                elif 'openshift' in product_lower:
                    return 'Enhanced container platform stability and performance'
                elif 'rhel' in product_lower:
                    return 'Strengthened enterprise Linux platform reliability'
                else:
                    return 'Improved product stability and reliability'
            
            return 'Enhanced operational efficiency'
    
    def process_case_data(self, raw_cases: List[Dict]) -> Dict[str, Any]:
        """Process raw case data into structured format for templates"""
        
        processed_data = {
            'total_cases': len(raw_cases),
            'active_cases': [],
            'closed_cases': [],
            'rfe_cases': [],
            'bug_cases': [],
            'by_sbr_group': {},
            'by_status': {},
            'by_priority': {},
            'summary_stats': {}
        }
        
        for case in raw_cases:
            # Determine case type
            case_type = case.get('caseType', '').lower()
            is_rfe = 'rfe' in case_type or 'enhancement' in case_type
            is_bug = 'bug' in case_type or 'defect' in case_type
            
            # Determine if closed
            status = case.get('status', '').lower()
            is_closed = status in ['closed', 'resolved', 'solved', 'done', 'complete', 'delivered'] or case.get('isClosed', False)
            
            # Process case data
            processed_case = {
                'case_number': case.get('caseNumber', ''),
                'summary': case.get('summary', ''),
                'status': case.get('status', ''),
                'sbr_group': case.get('sbrGroup', ''),
                'created_date': case.get('createdDate', ''),
                'updated_date': case.get('lastModifiedDate', ''),
                'priority': case.get('severity', ''),
                'product': case.get('product', ''),
                'version': case.get('version', ''),
                'case_type': case.get('caseType', ''),
                'is_rfe': is_rfe,
                'is_bug': is_bug,
                'is_closed': is_closed,
                'business_impact': self._generate_business_impact(case),
                'raw_data': case
            }
            
            # Categorize cases
            if is_closed:
                processed_data['closed_cases'].append(processed_case)
            else:
                processed_data['active_cases'].append(processed_case)
            
            if is_rfe:
                processed_data['rfe_cases'].append(processed_case)
            elif is_bug:
                processed_data['bug_cases'].append(processed_case)
            
            # Group by SBR group
            sbr_group = processed_case['sbr_group']
            if sbr_group not in processed_data['by_sbr_group']:
                processed_data['by_sbr_group'][sbr_group] = []
            processed_data['by_sbr_group'][sbr_group].append(processed_case)
            
            # Group by status
            if status not in processed_data['by_status']:
                processed_data['by_status'][status] = []
            processed_data['by_status'][status].append(processed_case)
            
            # Group by priority
            priority = processed_case['priority']
            if priority not in processed_data['by_priority']:
                processed_data['by_priority'][priority] = []
            processed_data['by_priority'][priority].append(processed_case)
        
        # Calculate summary statistics
        processed_data['summary_stats'] = {
            'total_active': len(processed_data['active_cases']),
            'total_closed': len(processed_data['closed_cases']),
            'total_rfe': len(processed_data['rfe_cases']),
            'total_bug': len(processed_data['bug_cases']),
            'active_rfe': len([c for c in processed_data['active_cases'] if c['is_rfe']]),
            'active_bug': len([c for c in processed_data['active_cases'] if c['is_bug']]),
            'closed_rfe': len([c for c in processed_data['closed_cases'] if c['is_rfe']]),
            'closed_bug': len([c for c in processed_data['closed_cases'] if c['is_bug']])
        }
        
        return processed_data
    
    def _generate_business_impact(self, case: Dict) -> str:
        """Generate business impact statement for a case"""
        case_type = case.get('caseType', '').lower()
        product = case.get('product', '').lower()
        summary = case.get('summary', '').lower()
        
        # RFE cases
        if 'rfe' in case_type or 'enhancement' in case_type:
            if 'ansible' in product:
                if 'api' in summary:
                    return 'Enhanced API capabilities and integration efficiency'
                elif 'security' in summary or 'vault' in summary:
                    return 'Improved security posture and compliance adherence'
                elif 'monitoring' in summary:
                    return 'Enhanced operational visibility and monitoring capabilities'
                else:
                    return 'Improved automation capabilities and operational efficiency'
            
            elif 'openshift' in product:
                return 'Enhanced container platform functionality and scalability'
            
            elif 'rhel' in product:
                return 'Strengthened enterprise Linux platform capabilities'
            
            else:
                return 'Enhanced product functionality and user experience'
        
        # Bug cases
        elif 'bug' in case_type or 'defect' in case_type:
            if 'ansible' in product:
                return 'Improved automation reliability and stability'
            elif 'openshift' in product:
                return 'Enhanced container platform stability and performance'
            elif 'rhel' in product:
                return 'Strengthened enterprise Linux platform reliability'
            else:
                return 'Improved product stability and reliability'
        
        return 'Enhanced operational efficiency'
    
    def render_template(self, template_name: str, data: Dict[str, Any]) -> str:
        """Render a template with the provided data"""
        
        try:
            self.logger.info(f"Rendering template: {template_name}")
            
            # Load template
            template = self.env.get_template(template_name)
            
            # Add common context data
            context = {
                **data,
                'current_date': datetime.now().strftime('%Y-%m-%d'),
                'current_time': datetime.now().strftime('%H:%M:%S'),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S EST'),
                'next_update_time': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
            }
            
            # Render template
            rendered_content = template.render(**context)
            
            self.logger.info(f"Template rendered successfully: {template_name}")
            return rendered_content
            
        except TemplateError as e:
            self.logger.error(f"Template error in {template_name}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error rendering template {template_name}: {e}")
            raise
    
    def validate_template(self, template_name: str) -> Dict[str, Any]:
        """Validate a template for syntax and required variables"""
        
        validation_result = {
            'template_name': template_name,
            'valid': False,
            'errors': [],
            'warnings': [],
            'required_variables': [],
            'optional_variables': []
        }
        
        try:
            # Load template
            template = self.env.get_template(template_name)
            
            # Check template syntax
            validation_result['valid'] = True
            
            # Extract variable information (basic analysis)
            template_source = template.source
            if '{{ current_date }}' in template_source:
                validation_result['required_variables'].append('current_date')
            if '{{ total_active_cases }}' in template_source:
                validation_result['required_variables'].append('total_active_cases')
            if '{{ active_rfe_count }}' in template_source:
                validation_result['required_variables'].append('active_rfe_count')
            
            self.logger.info(f"Template validation completed: {template_name}")
            
        except TemplateError as e:
            validation_result['errors'].append(f"Template syntax error: {e}")
        except Exception as e:
            validation_result['errors'].append(f"Validation error: {e}")
        
        return validation_result
    
    def list_available_templates(self) -> List[str]:
        """List all available templates in the template directory"""
        
        templates = []
        
        try:
            if os.path.exists(self.template_dir):
                for file in os.listdir(self.template_dir):
                    if file.endswith(('.j2', '.jinja2', '.md', '.html')):
                        templates.append(file)
            
            self.logger.info(f"Found {len(templates)} templates in {self.template_dir}")
            
        except Exception as e:
            self.logger.error(f"Error listing templates: {e}")
        
        return sorted(templates)
    
    def create_template(self, template_name: str, content: str) -> bool:
        """Create a new template file"""
        
        try:
            template_path = os.path.join(self.template_dir, template_name)
            
            # Ensure template directory exists
            os.makedirs(self.template_dir, exist_ok=True)
            
            # Write template content
            with open(template_path, 'w') as f:
                f.write(content)
            
            self.logger.info(f"Template created: {template_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating template {template_name}: {e}")
            return False

def main():
    """Test the Jinja2 template engine"""
    
    print("🔧 Jinja2 Template Engine Test")
    print("=" * 40)
    
    # Initialize template engine
    engine = Jinja2TemplateEngine()
    
    # List available templates
    templates = engine.list_available_templates()
    print(f"\n📋 Available Templates: {len(templates)}")
    for template in templates:
        print(f"   - {template}")
    
    # Test template validation
    if templates:
        test_template = templates[0]
        validation = engine.validate_template(test_template)
        print(f"\n🔍 Template Validation: {test_template}")
        print(f"   Valid: {'✅' if validation['valid'] else '❌'}")
        if validation['errors']:
            print(f"   Errors: {validation['errors']}")
        if validation['required_variables']:
            print(f"   Required Variables: {validation['required_variables']}")
    
    print(f"\n✅ Jinja2 Template Engine test completed")

if __name__ == '__main__':
    main()
