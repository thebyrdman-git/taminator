#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Red Hat TAM Operations
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: rfe_data_validator
short_description: Validates RFE automation data quality and structure
version_added: "1.0.0"
description:
    - Validates case data structure, quality, and consistency
    - Calculates data quality scores
    - Detects anomalies and suspicious patterns
    - Provides comprehensive validation reporting
author:
    - "Red Hat TAM Operations"
options:
    case_data:
        description:
            - List of case data to validate
        required: true
        type: list
        elements: dict
    validation_threshold:
        description:
            - Minimum data quality threshold (0.0-1.0)
        required: false
        type: float
        default: 0.95
    strict_validation:
        description:
            - Enable strict validation mode
        required: false
        type: bool
        default: false
    check_anomalies:
        description:
            - Enable anomaly detection
        required: false
        type: bool
        default: true
'''

EXAMPLES = r'''
- name: Validate RFE case data
  redhat.rfe_automation.rfe_data_validator:
    case_data: "{{ rfe_cases }}"
    validation_threshold: 0.99
    strict_validation: true
    check_anomalies: true
  register: validation_result

- name: Display validation results
  debug:
    msg: "Data quality score: {{ validation_result.quality_score }}"
'''

RETURN = r'''
quality_score:
    description: Overall data quality score (0.0-1.0)
    returned: always
    type: float
    sample: 0.98
validation_results:
    description: Detailed validation results
    returned: always
    type: dict
    contains:
        structure_valid:
            description: Whether data structure is valid
            type: bool
        required_fields_present:
            description: Percentage of cases with required fields
            type: float
        data_consistency:
            description: Data consistency score
            type: float
        anomalies_detected:
            description: List of detected anomalies
            type: list
        recommendations:
            description: Validation recommendations
            type: list
summary:
    description: Validation summary
    returned: always
    type: dict
    contains:
        total_cases:
            description: Total number of cases validated
            type: int
        valid_cases:
            description: Number of valid cases
            type: int
        invalid_cases:
            description: Number of invalid cases
            type: int
        validation_passed:
            description: Whether validation passed threshold
            type: bool
'''

import json
from ansible.module_utils.basic import AnsibleModule


def validate_case_structure(case_data):
    """Validate case data structure and required fields."""
    required_fields = ['caseNumber', 'caseType', 'sbrGroup', 'isClosed']
    structure_valid = True
    missing_fields = []
    
    for case in case_data:
        for field in required_fields:
            if field not in case or case[field] is None:
                structure_valid = False
                missing_fields.append(f"{case.get('caseNumber', 'unknown')}: {field}")
    
    return {
        'structure_valid': structure_valid,
        'missing_fields': missing_fields,
        'required_fields_present': 1.0 - (len(missing_fields) / (len(case_data) * len(required_fields))) if case_data else 1.0
    }


def calculate_data_quality(case_data):
    """Calculate overall data quality score."""
    if not case_data:
        return 0.0
    
    quality_factors = []
    
    # Field completeness
    required_fields = ['caseNumber', 'caseType', 'sbrGroup', 'isClosed']
    complete_cases = 0
    for case in case_data:
        if all(field in case and case[field] is not None for field in required_fields):
            complete_cases += 1
    quality_factors.append(complete_cases / len(case_data))
    
    # Data consistency
    case_types = [case.get('caseType') for case in case_data if case.get('caseType')]
    unique_types = len(set(case_types))
    total_types = len(case_types)
    consistency_score = unique_types / total_types if total_types > 0 else 1.0
    quality_factors.append(consistency_score)
    
    # SBR Group consistency
    sbr_groups = [case.get('sbrGroup') for case in case_data if case.get('sbrGroup')]
    unique_sbr = len(set(sbr_groups))
    total_sbr = len(sbr_groups)
    sbr_consistency = unique_sbr / total_sbr if total_sbr > 0 else 1.0
    quality_factors.append(sbr_consistency)
    
    return sum(quality_factors) / len(quality_factors)


def detect_anomalies(case_data):
    """Detect anomalies in case data."""
    anomalies = []
    
    if not case_data:
        anomalies.append("No case data provided")
        return anomalies
    
    # Check for unusual case counts
    if len(case_data) == 0:
        anomalies.append("Zero cases detected")
    elif len(case_data) > 1000:
        anomalies.append(f"Unusually high case count: {len(case_data)}")
    
    # Check for missing case types
    case_types = [case.get('caseType') for case in case_data if case.get('caseType')]
    if not case_types:
        anomalies.append("No case types found in data")
    
    # Check for closed case ratio
    closed_cases = [case for case in case_data if case.get('isClosed')]
    closed_ratio = len(closed_cases) / len(case_data) if case_data else 0
    if closed_ratio > 0.9:
        anomalies.append(f"Unusually high closed case ratio: {closed_ratio:.2%}")
    elif closed_ratio < 0.1:
        anomalies.append(f"Unusually low closed case ratio: {closed_ratio:.2%}")
    
    return anomalies


def generate_recommendations(validation_results, quality_score, anomalies):
    """Generate validation recommendations."""
    recommendations = []
    
    if quality_score < 0.95:
        recommendations.append("Data quality score is below recommended threshold (95%)")
    
    if validation_results['required_fields_present'] < 1.0:
        recommendations.append("Some cases are missing required fields - review data collection")
    
    if anomalies:
        recommendations.append("Anomalies detected - review data for accuracy")
    
    if not recommendations:
        recommendations.append("Data quality is good - no immediate action required")
    
    return recommendations


def main():
    module_args = dict(
        case_data=dict(type='list', elements='dict', required=True),
        validation_threshold=dict(type='float', default=0.95),
        strict_validation=dict(type='bool', default=False),
        check_anomalies=dict(type='bool', default=True)
    )
    
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    
    case_data = module.params['case_data']
    validation_threshold = module.params['validation_threshold']
    strict_validation = module.params['strict_validation']
    check_anomalies = module.params['check_anomalies']
    
    try:
        # Validate case structure
        structure_results = validate_case_structure(case_data)
        
        # Calculate data quality
        quality_score = calculate_data_quality(case_data)
        
        # Detect anomalies
        anomalies = detect_anomalies(case_data) if check_anomalies else []
        
        # Generate recommendations
        recommendations = generate_recommendations(structure_results, quality_score, anomalies)
        
        # Prepare results
        validation_results = {
            'structure_valid': structure_results['structure_valid'],
            'required_fields_present': structure_results['required_fields_present'],
            'data_consistency': quality_score,
            'anomalies_detected': anomalies,
            'recommendations': recommendations
        }
        
        summary = {
            'total_cases': len(case_data),
            'valid_cases': len([case for case in case_data if all(field in case and case[field] is not None for field in ['caseNumber', 'caseType', 'sbrGroup', 'isClosed'])]),
            'invalid_cases': len(case_data) - len([case for case in case_data if all(field in case and case[field] is not None for field in ['caseNumber', 'caseType', 'sbrGroup', 'isClosed'])]),
            'validation_passed': quality_score >= validation_threshold
        }
        
        # Check if validation should fail
        validation_failed = False
        if strict_validation and not structure_results['structure_valid']:
            validation_failed = True
        if quality_score < validation_threshold:
            validation_failed = True
        
        if validation_failed:
            module.fail_json(
                msg=f"Data validation failed. Quality score: {quality_score:.3f}, Threshold: {validation_threshold}",
                quality_score=quality_score,
                validation_results=validation_results,
                summary=summary
            )
        else:
            module.exit_json(
                changed=False,
                quality_score=quality_score,
                validation_results=validation_results,
                summary=summary
            )
            
    except Exception as e:
        module.fail_json(msg=f"Validation error: {str(e)}")


if __name__ == '__main__':
    main()
