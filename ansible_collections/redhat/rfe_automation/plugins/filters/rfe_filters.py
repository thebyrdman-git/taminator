#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Red Hat TAM Operations
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

class FilterModule(object):
    """RFE automation custom Jinja2 filters."""

    def filters(self):
        return {
            'rfe_case_type_filter': self.rfe_case_type_filter,
            'rfe_priority_filter': self.rfe_priority_filter,
            'rfe_format_case_number': self.rfe_format_case_number,
            'rfe_calculate_sla_status': self.rfe_calculate_sla_status,
            'rfe_format_duration': self.rfe_format_duration,
            'rfe_get_severity_level': self.rfe_get_severity_level,
            'rfe_is_escalated': self.rfe_is_escalated,
            'rfe_get_case_age': self.rfe_get_case_age,
            'rfe_format_case_summary': self.rfe_format_case_summary,
            'rfe_group_by_sbr': self.rfe_group_by_sbr,
            'rfe_sort_by_priority': self.rfe_sort_by_priority,
        }

    def rfe_case_type_filter(self, cases, case_types):
        """Filter cases by case type."""
        if not isinstance(cases, list) or not isinstance(case_types, list):
            return []
        
        return [case for case in cases if case.get('caseType') in case_types]

    def rfe_priority_filter(self, cases, priority_components):
        """Filter cases by priority components (SBR groups)."""
        if not isinstance(cases, list) or not isinstance(priority_components, list):
            return []
        
        return [case for case in cases if case.get('sbrGroup') in priority_components]

    def rfe_format_case_number(self, case_number):
        """Format case number for display."""
        if not case_number:
            return 'Unknown'
        
        # Remove any HTML tags if present
        import re
        clean_number = re.sub(r'<[^>]+>', '', str(case_number))
        return clean_number.strip()

    def rfe_calculate_sla_status(self, case):
        """Calculate SLA status based on case data."""
        if not isinstance(case, dict):
            return 'Unknown'
        
        is_closed = case.get('isClosed', False)
        is_breached = case.get('numberOfBreaches', 0) > 0
        sbt_state = case.get('sbtState', '')
        
        if is_closed:
            return 'Closed'
        elif is_breached:
            return 'Breached'
        elif sbt_state == 'Not Breached':
            return 'On Track'
        else:
            return 'Unknown'

    def rfe_format_duration(self, hours):
        """Format duration in hours to human readable format."""
        if not isinstance(hours, (int, float)) or hours < 0:
            return 'Unknown'
        
        if hours < 1:
            return f"{int(hours * 60)} minutes"
        elif hours < 24:
            return f"{hours:.1f} hours"
        elif hours < 168:  # 7 days
            days = hours / 24
            return f"{days:.1f} days"
        else:
            weeks = hours / 168
            return f"{weeks:.1f} weeks"

    def rfe_get_severity_level(self, severity):
        """Extract severity level from severity string."""
        if not severity:
            return 'Unknown'
        
        import re
        match = re.search(r'(\d+)', str(severity))
        if match:
            level = int(match.group(1))
            if level == 1:
                return 'Urgent'
            elif level == 2:
                return 'High'
            elif level == 3:
                return 'Medium'
            elif level == 4:
                return 'Low'
        
        return 'Unknown'

    def rfe_is_escalated(self, case):
        """Check if case is escalated."""
        if not isinstance(case, dict):
            return False
        
        return (
            case.get('isEscalated', False) or
            case.get('customerEscalation', False) or
            case.get('requestManagementEscalation', False) or
            case.get('totalEscalation', 0) > 0
        )

    def rfe_get_case_age(self, case):
        """Calculate case age in hours."""
        if not isinstance(case, dict):
            return 0
        
        # Use hoursSinceCaseLastUpdated if available
        if 'hoursSinceCaseLastUpdated' in case:
            return case['hoursSinceCaseLastUpdated']
        
        # Fallback to other time fields
        if 'hoursInCurrentStatus' in case:
            return case['hoursInCurrentStatus']
        
        return 0

    def rfe_format_case_summary(self, case, max_length=100):
        """Format case summary for display."""
        if not isinstance(case, dict):
            return 'No summary available'
        
        subject = case.get('subject', '')
        summary = case.get('summary', '')
        
        # Use subject if available, otherwise summary
        text = subject if subject else summary
        
        if not text:
            return 'No summary available'
        
        # Truncate if too long
        if len(text) > max_length:
            return text[:max_length - 3] + '...'
        
        return text

    def rfe_group_by_sbr(self, cases):
        """Group cases by SBR group."""
        if not isinstance(cases, list):
            return {}
        
        grouped = {}
        for case in cases:
            sbr_group = case.get('sbrGroup', 'Unknown')
            if sbr_group not in grouped:
                grouped[sbr_group] = []
            grouped[sbr_group].append(case)
        
        return grouped

    def rfe_sort_by_priority(self, cases):
        """Sort cases by priority (severity, then age)."""
        if not isinstance(cases, list):
            return []
        
        def get_priority_score(case):
            # Extract severity level
            severity = case.get('severity', '')
            import re
            match = re.search(r'(\d+)', str(severity))
            severity_level = int(match.group(1)) if match else 4
            
            # Get case age
            age = self.rfe_get_case_age(case)
            
            # Calculate priority score (lower is higher priority)
            # Severity 1 = 1000, Severity 2 = 2000, etc.
            # Age in hours adds to the score
            return (severity_level * 1000) + age
        
        return sorted(cases, key=get_priority_score)
