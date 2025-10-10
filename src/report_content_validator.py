#!/usr/bin/env python3

"""
Report Content Accuracy Validator
Purpose: Ensure RFE reports contain accurate, relevant, and properly formatted content
Features: Content validation, data accuracy checks, consistency verification, quality scoring
"""

import os
import sys
import json
import re
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import difflib

class ContentValidationResult(Enum):
    """Content validation result status"""
    ACCURATE = "accurate"
    INACCURATE = "inaccurate"
    INCOMPLETE = "incomplete"
    INCONSISTENT = "inconsistent"
    SUSPICIOUS = "suspicious"

class ContentSeverity(Enum):
    """Content issue severity levels"""
    CRITICAL = "critical"    # Report contains false information
    HIGH = "high"           # Major content issues affecting accuracy
    MEDIUM = "medium"       # Minor content issues
    LOW = "low"            # Formatting or presentation issues

@dataclass
class ContentIssue:
    """Represents a content accuracy issue"""
    issue_type: str
    severity: ContentSeverity
    description: str
    location: str  # e.g., "Active RFE table, row 3"
    expected_value: Optional[str] = None
    actual_value: Optional[str] = None
    recommendation: Optional[str] = None

@dataclass
class ContentValidationReport:
    """Comprehensive content validation report"""
    report_id: str
    validation_timestamp: str
    overall_accuracy_score: float  # 0.0 to 1.0
    validation_status: ContentValidationResult
    total_issues: int
    critical_issues: int
    high_issues: int
    medium_issues: int
    low_issues: int
    content_issues: List[ContentIssue]
    recommendations: List[str]
    validation_summary: str

class ReportContentValidator:
    """Comprehensive report content accuracy validation system"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        
        # Validation thresholds - Enterprise-grade standards
        self.accuracy_threshold = 0.99  # 99% accuracy required for customer reports
        self.consistency_threshold = 0.995  # 99.5% consistency required
        self.customer_report_threshold = 0.99  # 99% minimum for customer-facing reports
        
        # Known patterns for validation
        self.valid_case_number_pattern = r'^\d{8}$'  # 8-digit case numbers
        self.valid_rfe_pattern = r'^RFE-\d+$'  # RFE-XXXX format
        self.valid_bug_pattern = r'^Bug \d+$'  # Bug XXXX format
        
        # Product mapping for cross-validation
        self.product_keywords = {
            'openshift': ['openshift', 'ocp', 'kubernetes', 'k8s', 'container', 'pod'],
            'rhel': ['rhel', 'red hat enterprise linux', 'linux'],
            'ansible': ['ansible', 'automation', 'playbook', 'tower'],
            'satellite': ['satellite', 'spacewalk', 'foreman'],
            'jboss': ['jboss', 'wildfly', 'eap', 'application server']
        }
        
        self.logger.info("Report Content Validator initialized")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for content validation"""
        logger = logging.getLogger('content_validator')
        logger.setLevel(logging.INFO)
        
        # Create log file
        log_file = f"/tmp/content-validation-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
        
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
    
    def validate_report_content(self, report_data: Dict[str, Any], customer_name: str) -> ContentValidationReport:
        """
        Comprehensive content validation for RFE reports
        
        Args:
            report_data: The generated report data
            customer_name: Customer name for context validation
            
        Returns:
            ContentValidationReport with detailed validation results
        """
        self.logger.info(f"Starting content validation for {customer_name}")
        
        validation_start = datetime.now()
        content_issues = []
        
        # Extract report sections
        active_rfe_table = report_data.get('active_rfe_table', [])
        active_bug_table = report_data.get('active_bug_table', [])
        closed_case_history = report_data.get('closed_case_history', [])
        
        # Validate each section
        content_issues.extend(self._validate_active_rfe_table(active_rfe_table, customer_name))
        content_issues.extend(self._validate_active_bug_table(active_bug_table, customer_name))
        content_issues.extend(self._validate_closed_case_history(closed_case_history, customer_name))
        
        # Cross-section validation
        content_issues.extend(self._validate_cross_section_consistency(
            active_rfe_table, active_bug_table, closed_case_history, customer_name
        ))
        
        # Calculate accuracy score
        accuracy_score = self._calculate_accuracy_score(content_issues, len(active_rfe_table) + len(active_bug_table) + len(closed_case_history))
        
        # Determine overall validation status
        validation_status = self._determine_validation_status(accuracy_score, content_issues)
        
        # Generate recommendations
        recommendations = self._generate_content_recommendations(content_issues, accuracy_score)
        
        # Create validation report
        validation_report = ContentValidationReport(
            report_id=f"content_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            validation_timestamp=validation_start.isoformat(),
            overall_accuracy_score=accuracy_score,
            validation_status=validation_status,
            total_issues=len(content_issues),
            critical_issues=len([i for i in content_issues if i.severity == ContentSeverity.CRITICAL]),
            high_issues=len([i for i in content_issues if i.severity == ContentSeverity.HIGH]),
            medium_issues=len([i for i in content_issues if i.severity == ContentSeverity.MEDIUM]),
            low_issues=len([i for i in content_issues if i.severity == ContentSeverity.LOW]),
            content_issues=content_issues,
            recommendations=recommendations,
            validation_summary=self._generate_validation_summary(validation_status, accuracy_score, content_issues)
        )
        
        self.logger.info(f"Content validation completed: {validation_status.value} (Score: {accuracy_score:.2f})")
        return validation_report
    
    def _validate_active_rfe_table(self, rfe_table: List[Dict], customer_name: str) -> List[ContentIssue]:
        """Validate Active RFE table content"""
        issues = []
        
        for i, rfe in enumerate(rfe_table):
            row_location = f"Active RFE table, row {i+1}"
            
            # Validate RFE ID format
            rfe_id = rfe.get('rfe_id', '')
            if not re.match(self.valid_rfe_pattern, rfe_id):
                issues.append(ContentIssue(
                    issue_type="invalid_rfe_format",
                    severity=ContentSeverity.HIGH,
                    description=f"Invalid RFE ID format: {rfe_id}",
                    location=row_location,
                    expected_value="RFE-XXXX format",
                    actual_value=rfe_id,
                    recommendation="Verify RFE ID format matches Red Hat standards"
                ))
            
            # Validate case number format
            case_number = rfe.get('case_number', '')
            if case_number and not re.match(self.valid_case_number_pattern, case_number):
                issues.append(ContentIssue(
                    issue_type="invalid_case_number",
                    severity=ContentSeverity.HIGH,
                    description=f"Invalid case number format: {case_number}",
                    location=row_location,
                    expected_value="8-digit number",
                    actual_value=case_number,
                    recommendation="Verify case number is 8 digits"
                ))
            
            # Validate product consistency
            product = rfe.get('product', '').lower()
            title = rfe.get('title', '').lower()
            if not self._validate_product_consistency(product, title):
                issues.append(ContentIssue(
                    issue_type="product_inconsistency",
                    severity=ContentSeverity.MEDIUM,
                    description=f"Product '{product}' doesn't match title content",
                    location=row_location,
                    expected_value="Product should match title keywords",
                    actual_value=f"Product: {product}, Title: {title}",
                    recommendation="Verify product classification matches RFE content"
                ))
            
            # Validate date formats
            created_date = rfe.get('created_date', '')
            if created_date and not self._validate_date_format(created_date):
                issues.append(ContentIssue(
                    issue_type="invalid_date_format",
                    severity=ContentSeverity.MEDIUM,
                    description=f"Invalid date format: {created_date}",
                    location=row_location,
                    expected_value="YYYY-MM-DD or MM/DD/YYYY format",
                    actual_value=created_date,
                    recommendation="Standardize date format across all entries"
                ))
        
        return issues
    
    def _validate_active_bug_table(self, bug_table: List[Dict], customer_name: str) -> List[ContentIssue]:
        """Validate Active Bug table content"""
        issues = []
        
        for i, bug in enumerate(bug_table):
            row_location = f"Active Bug table, row {i+1}"
            
            # Validate Bug ID format
            bug_id = bug.get('bug_id', '')
            if not re.match(self.valid_bug_pattern, bug_id):
                issues.append(ContentIssue(
                    issue_type="invalid_bug_format",
                    severity=ContentSeverity.HIGH,
                    description=f"Invalid Bug ID format: {bug_id}",
                    location=row_location,
                    expected_value="Bug XXXX format",
                    actual_value=bug_id,
                    recommendation="Verify Bug ID format matches Red Hat standards"
                ))
            
            # Validate case number format
            case_number = bug.get('case_number', '')
            if case_number and not re.match(self.valid_case_number_pattern, case_number):
                issues.append(ContentIssue(
                    issue_type="invalid_case_number",
                    severity=ContentSeverity.HIGH,
                    description=f"Invalid case number format: {case_number}",
                    location=row_location,
                    expected_value="8-digit number",
                    actual_value=case_number,
                    recommendation="Verify case number is 8 digits"
                ))
            
            # Validate severity levels
            severity = bug.get('severity', '').lower()
            valid_severities = ['1', '2', '3', '4', 'urgent', 'high', 'medium', 'low']
            if severity and severity not in valid_severities:
                issues.append(ContentIssue(
                    issue_type="invalid_severity",
                    severity=ContentSeverity.MEDIUM,
                    description=f"Invalid severity level: {severity}",
                    location=row_location,
                    expected_value="1-4 or Urgent/High/Medium/Low",
                    actual_value=severity,
                    recommendation="Use standard Red Hat severity levels"
                ))
        
        return issues
    
    def _validate_closed_case_history(self, case_history: List[Dict], customer_name: str) -> List[ContentIssue]:
        """Validate Closed Case History content"""
        issues = []
        
        for i, case in enumerate(case_history):
            row_location = f"Closed Case History, row {i+1}"
            
            # Validate case number format
            case_number = case.get('case_number', '')
            if not re.match(self.valid_case_number_pattern, case_number):
                issues.append(ContentIssue(
                    issue_type="invalid_case_number",
                    severity=ContentSeverity.HIGH,
                    description=f"Invalid case number format: {case_number}",
                    location=row_location,
                    expected_value="8-digit number",
                    actual_value=case_number,
                    recommendation="Verify case number is 8 digits"
                ))
            
            # Validate resolution status
            resolution = case.get('resolution', '').lower()
            valid_resolutions = ['resolved', 'closed', 'abandoned', 'duplicate', 'not a bug']
            if resolution and resolution not in valid_resolutions:
                issues.append(ContentIssue(
                    issue_type="invalid_resolution",
                    severity=ContentSeverity.MEDIUM,
                    description=f"Invalid resolution status: {resolution}",
                    location=row_location,
                    expected_value="Resolved/Closed/Abandoned/Duplicate/Not a Bug",
                    actual_value=resolution,
                    recommendation="Use standard Red Hat resolution statuses"
                ))
            
            # Validate closure date is in the past
            closure_date = case.get('closure_date', '')
            if closure_date and not self._validate_date_in_past(closure_date):
                issues.append(ContentIssue(
                    issue_type="future_closure_date",
                    severity=ContentSeverity.HIGH,
                    description=f"Closure date is in the future: {closure_date}",
                    location=row_location,
                    expected_value="Date in the past",
                    actual_value=closure_date,
                    recommendation="Verify closure date is accurate"
                ))
        
        return issues
    
    def _validate_cross_section_consistency(self, rfe_table: List[Dict], bug_table: List[Dict], 
                                          case_history: List[Dict], customer_name: str) -> List[ContentIssue]:
        """Validate consistency across report sections"""
        issues = []
        
        # Check for duplicate case numbers across sections
        all_case_numbers = []
        
        for rfe in rfe_table:
            if rfe.get('case_number'):
                all_case_numbers.append(rfe['case_number'])
        
        for bug in bug_table:
            if bug.get('case_number'):
                all_case_numbers.append(bug['case_number'])
        
        for case in case_history:
            if case.get('case_number'):
                all_case_numbers.append(case['case_number'])
        
        # Find duplicates
        seen_cases = set()
        duplicates = set()
        for case_num in all_case_numbers:
            if case_num in seen_cases:
                duplicates.add(case_num)
            seen_cases.add(case_num)
        
        for duplicate in duplicates:
            issues.append(ContentIssue(
                issue_type="duplicate_case_number",
                severity=ContentSeverity.HIGH,
                description=f"Case number {duplicate} appears in multiple sections",
                location="Cross-section validation",
                expected_value="Each case number should appear only once",
                actual_value=f"Case {duplicate} duplicated",
                recommendation="Remove duplicate entries or verify case classification"
            ))
        
        # Check for logical inconsistencies (e.g., case in both active and closed)
        rfe_case_numbers = {rfe.get('case_number') for rfe in rfe_table if rfe.get('case_number')}
        bug_case_numbers = {bug.get('case_number') for bug in bug_table if bug.get('case_number')}
        closed_case_numbers = {case.get('case_number') for case in case_history if case.get('case_number')}
        
        # Cases shouldn't be both active and closed
        active_in_closed = (rfe_case_numbers | bug_case_numbers) & closed_case_numbers
        for case_num in active_in_closed:
            issues.append(ContentIssue(
                issue_type="case_status_inconsistency",
                severity=ContentSeverity.CRITICAL,
                description=f"Case {case_num} appears in both active and closed sections",
                location="Cross-section validation",
                expected_value="Case should be either active OR closed",
                actual_value=f"Case {case_num} in both sections",
                recommendation="Verify case status and remove from incorrect section"
            ))
        
        return issues
    
    def _validate_product_consistency(self, product: str, title: str) -> bool:
        """Validate that product classification matches title content"""
        if not product or not title:
            return True  # Skip validation if data is missing
        
        product_lower = product.lower()
        title_lower = title.lower()
        
        # Check if any product keywords appear in the title
        for product_name, keywords in self.product_keywords.items():
            if product_name in product_lower:
                return any(keyword in title_lower for keyword in keywords)
        
        return True  # Default to valid if we can't determine
    
    def _validate_date_format(self, date_str: str) -> bool:
        """Validate date format"""
        if not date_str:
            return True
        
        # Common date formats
        date_patterns = [
            r'^\d{4}-\d{2}-\d{2}$',  # YYYY-MM-DD
            r'^\d{2}/\d{2}/\d{4}$',  # MM/DD/YYYY
            r'^\d{4}/\d{2}/\d{2}$',  # YYYY/MM/DD
        ]
        
        return any(re.match(pattern, date_str) for pattern in date_patterns)
    
    def _validate_date_in_past(self, date_str: str) -> bool:
        """Validate that date is in the past"""
        if not date_str:
            return True
        
        try:
            # Try to parse the date
            if '-' in date_str:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            elif '/' in date_str:
                if len(date_str.split('/')[0]) == 4:  # YYYY/MM/DD
                    date_obj = datetime.strptime(date_str, '%Y/%m/%d')
                else:  # MM/DD/YYYY
                    date_obj = datetime.strptime(date_str, '%m/%d/%Y')
            else:
                return True  # Unknown format, skip validation
            
            return date_obj.date() <= datetime.now().date()
        except ValueError:
            return True  # Invalid date format, skip validation
    
    def _calculate_accuracy_score(self, issues: List[ContentIssue], total_items: int) -> float:
        """Calculate overall accuracy score"""
        if total_items == 0:
            return 1.0
        
        # Weight issues by severity
        severity_weights = {
            ContentSeverity.CRITICAL: 0.5,  # Critical issues heavily penalize
            ContentSeverity.HIGH: 0.3,      # High issues moderately penalize
            ContentSeverity.MEDIUM: 0.1,    # Medium issues lightly penalize
            ContentSeverity.LOW: 0.05       # Low issues minimally penalize
        }
        
        total_penalty = 0.0
        for issue in issues:
            total_penalty += severity_weights.get(issue.severity, 0.1)
        
        # Calculate score (0.0 to 1.0)
        accuracy_score = max(0.0, 1.0 - (total_penalty / max(1, total_items)))
        return round(accuracy_score, 3)
    
    def _determine_validation_status(self, accuracy_score: float, issues: List[ContentIssue]) -> ContentValidationResult:
        """Determine overall validation status with enterprise-grade standards"""
        critical_issues = [i for i in issues if i.severity == ContentSeverity.CRITICAL]
        high_issues = [i for i in issues if i.severity == ContentSeverity.HIGH]
        
        # Enterprise-grade validation logic
        if critical_issues:
            return ContentValidationResult.INACCURATE
        elif high_issues and accuracy_score < 0.95:
            return ContentValidationResult.INACCURATE
        elif accuracy_score < 0.95:
            return ContentValidationResult.INACCURATE
        elif accuracy_score < self.customer_report_threshold:
            return ContentValidationResult.INCONSISTENT
        else:
            return ContentValidationResult.ACCURATE
    
    def _generate_content_recommendations(self, issues: List[ContentIssue], accuracy_score: float) -> List[str]:
        """Generate recommendations based on content issues with enterprise standards"""
        recommendations = []
        
        # Enterprise-grade accuracy standards
        if accuracy_score < 0.95:
            recommendations.append("🚨 CRITICAL: Report accuracy is below enterprise standards (95% minimum). DO NOT send to customers until fixed.")
        elif accuracy_score < 0.99:
            recommendations.append("⚠️ WARNING: Report accuracy below customer-facing threshold (99% required). Review and fix issues before publishing.")
        
        # Critical issue handling
        critical_issues = [i for i in issues if i.severity == ContentSeverity.CRITICAL]
        if critical_issues:
            recommendations.append("🚨 CRITICAL ISSUES DETECTED: Report contains false information. DO NOT PUBLISH.")
        
        # High issue handling
        high_issues = [i for i in issues if i.severity == ContentSeverity.HIGH]
        if high_issues:
            recommendations.append("⚠️ HIGH PRIORITY ISSUES: Major accuracy problems detected. Fix before customer distribution.")
        
        # Group recommendations by issue type
        issue_types = {}
        for issue in issues:
            if issue.issue_type not in issue_types:
                issue_types[issue.issue_type] = []
            issue_types[issue.issue_type].append(issue)
        
        for issue_type, type_issues in issue_types.items():
            count = len(type_issues)
            if count > 1:
                recommendations.append(f"📋 {issue_type.replace('_', ' ').title()}: {count} instances found. Batch correction required.")
            else:
                recommendations.append(f"📋 {issue_type.replace('_', ' ').title()}: {type_issues[0].recommendation}")
        
        if not issues:
            recommendations.append("✅ Enterprise-grade accuracy achieved. Report meets customer-facing standards.")
        
        return recommendations
    
    def _generate_validation_summary(self, status: ContentValidationResult, accuracy_score: float, 
                                   issues: List[ContentIssue]) -> str:
        """Generate validation summary with enterprise standards"""
        critical_count = len([i for i in issues if i.severity == ContentSeverity.CRITICAL])
        high_count = len([i for i in issues if i.severity == ContentSeverity.HIGH])
        
        if status == ContentValidationResult.ACCURATE:
            return f"✅ Enterprise-grade accuracy achieved (Score: {accuracy_score:.2%}). Report meets customer-facing standards and is ready for publication."
        elif status == ContentValidationResult.INACCURATE:
            return f"❌ Report fails enterprise standards (Score: {accuracy_score:.2%}). Contains {critical_count} critical and {high_count} high-priority issues. DO NOT PUBLISH until corrected."
        elif status == ContentValidationResult.INCONSISTENT:
            return f"⚠️ Report accuracy below customer-facing threshold (Score: {accuracy_score:.2%}). Requires 99%+ accuracy for customer distribution. Review and correct before publishing."
        else:
            return f"🔍 Report validation completed (Score: {accuracy_score:.2%}). {len(issues)} issues identified. Enterprise standards require 99%+ accuracy for customer reports."
    
    def save_validation_report(self, report: ContentValidationReport, output_dir: str = "/tmp") -> str:
        """Save validation report to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"content_validation_report_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(asdict(report), f, indent=2, default=str)
        
        self.logger.info(f"Validation report saved to: {filepath}")
        return filepath

def main():
    """Example usage of content validator"""
    print("🔍 Report Content Accuracy Validator")
    print("=" * 50)
    
    # Example report data (replace with actual report data)
    sample_report = {
        'active_rfe_table': [
            {
                'rfe_id': 'RFE-12345',
                'case_number': '12345678',
                'product': 'OpenShift',
                'title': 'OpenShift cluster performance improvement',
                'created_date': '2024-01-15'
            }
        ],
        'active_bug_table': [
            {
                'bug_id': 'Bug 98765',
                'case_number': '87654321',
                'severity': '2',
                'title': 'RHEL kernel panic issue'
            }
        ],
        'closed_case_history': [
            {
                'case_number': '11111111',
                'resolution': 'Resolved',
                'closure_date': '2024-01-10'
            }
        ]
    }
    
    # Initialize validator
    validator = ReportContentValidator()
    
    # Validate content
    validation_report = validator.validate_report_content(sample_report, "Test Customer")
    
    # Print results
    print(f"\n📊 Validation Results:")
    print(f"   Status: {validation_report.validation_status.value}")
    print(f"   Accuracy Score: {validation_report.overall_accuracy_score:.1%}")
    print(f"   Total Issues: {validation_report.total_issues}")
    print(f"   Critical Issues: {validation_report.critical_issues}")
    print(f"   High Issues: {validation_report.high_issues}")
    
    if validation_report.recommendations:
        print(f"\n💡 Recommendations:")
        for rec in validation_report.recommendations:
            print(f"   {rec}")
    
    # Save report
    report_file = validator.save_validation_report(validation_report)
    print(f"\n📄 Detailed report saved to: {report_file}")

if __name__ == '__main__':
    main()
