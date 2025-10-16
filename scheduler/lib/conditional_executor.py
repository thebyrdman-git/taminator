#!/usr/bin/env python3

"""
Conditional Execution Engine for TAM RFE Report Scheduler
Evaluates conditions before executing scheduled commands
"""

import re
import subprocess
from typing import Dict, Any, Optional


class ConditionalExecutor:
    """Evaluates conditions and executes commands conditionally"""
    
    @staticmethod
    def evaluate_condition(condition: str, context: Dict[str, Any] = None) -> bool:
        """
        Evaluate a condition string
        
        Supported conditions:
        - "sev1_count > 0" - Check Sev 1 case count
        - "case_count > 5" - Check total case count  
        - "always" - Always execute
        - "weekday" - Only on weekdays
        - "weekend" - Only on weekends
        """
        if not condition or condition == "always":
            return True
        
        context = context or {}
        
        # Weekday/weekend conditions
        from datetime import datetime
        today = datetime.now().weekday()  # 0=Monday, 6=Sunday
        
        if condition == "weekday":
            return today < 5  # Monday-Friday
        elif condition == "weekend":
            return today >= 5  # Saturday-Sunday
        
        # Numeric comparisons
        match = re.match(r'(\w+)\s*([<>=!]+)\s*(\d+)', condition)
        if match:
            var_name, operator, threshold = match.groups()
            threshold = int(threshold)
            value = context.get(var_name, 0)
            
            if isinstance(value, str):
                try:
                    value = int(value)
                except ValueError:
                    return False
            
            if operator == '>':
                return value > threshold
            elif operator == '>=':
                return value >= threshold
            elif operator == '<':
                return value < threshold
            elif operator == '<=':
                return value <= threshold
            elif operator == '==' or operator == '=':
                return value == threshold
            elif operator == '!=':
                return value != threshold
        
        # Boolean conditions
        if condition in context:
            return bool(context[condition])
        
        return False
    
    @staticmethod
    def extract_context_from_output(output: str) -> Dict[str, Any]:
        """
        Extract context variables from command output
        
        Looks for patterns like:
        - "Sev 1: 3 cases"
        - "Total cases: 15"
        - "sev1_count=3"
        """
        context = {}
        
        # Pattern: "key: number"
        for match in re.finditer(r'(\w+):\s*(\d+)', output):
            key, value = match.groups()
            context[key.lower().replace(' ', '_')] = int(value)
        
        # Pattern: "key=number"
        for match in re.finditer(r'(\w+)=(\d+)', output):
            key, value = match.groups()
            context[key.lower()] = int(value)
        
        # Specific patterns for case counts
        sev1_match = re.search(r'[Ss]ev\s*1[:\s]+(\d+)', output)
        if sev1_match:
            context['sev1_count'] = int(sev1_match.group(1))
        
        total_match = re.search(r'[Tt]otal[:\s]+(\d+)', output)
        if total_match:
            context['case_count'] = int(total_match.group(1))
        
        return context
    
    @staticmethod
    def should_execute(schedule: Dict[str, Any], dry_run: bool = False) -> tuple[bool, Optional[str]]:
        """
        Check if a schedule should execute based on its condition
        
        Returns:
            (should_execute: bool, reason: str)
        """
        condition = schedule.get('condition')
        
        if not condition or condition == 'always':
            return True, "No condition specified"
        
        # For conditions that need context, we need to run a pre-check command
        pre_check = schedule.get('pre_check_command')
        context = {}
        
        if pre_check:
            try:
                result = subprocess.run(
                    pre_check,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                context = ConditionalExecutor.extract_context_from_output(result.stdout)
            except Exception as e:
                return False, f"Pre-check failed: {e}"
        
        # Evaluate condition
        should_run = ConditionalExecutor.evaluate_condition(condition, context)
        
        if should_run:
            return True, f"Condition '{condition}' evaluated to True"
        else:
            return False, f"Condition '{condition}' evaluated to False (context: {context})"


# Example usage and testing
if __name__ == '__main__':
    executor = ConditionalExecutor()
    
    # Test conditions
    print("Testing conditions:")
    print(f"weekday: {executor.evaluate_condition('weekday')}")
    print(f"always: {executor.evaluate_condition('always')}")
    
    context = {'sev1_count': 3, 'case_count': 15}
    print(f"sev1_count > 0: {executor.evaluate_condition('sev1_count > 0', context)}")
    print(f"case_count > 20: {executor.evaluate_condition('case_count > 20', context)}")
    
    # Test context extraction
    output = """
    Case Summary:
    Sev 1: 3 cases
    Sev 2: 7 cases
    Total: 15 cases
    """
    extracted = executor.extract_context_from_output(output)
    print(f"Extracted context: {extracted}")

