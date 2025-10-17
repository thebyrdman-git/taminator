#!/usr/bin/env python3

"""
RFE Verification System - Comprehensive Testing & Validation
Purpose: Ensure RFE automation tool works reliably every time
Features: End-to-end testing, component validation, regression testing, performance monitoring
"""

import os
import sys
import json
import yaml
import time
import subprocess
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import traceback

class TestStatus(Enum):
    """Test result status"""
    PASS = "PASS"
    FAIL = "FAIL"
    WARN = "WARN"
    SKIP = "SKIP"

class TestSeverity(Enum):
    """Test severity levels"""
    CRITICAL = "critical"    # Must pass for tool to work
    HIGH = "high"           # Should pass for reliable operation
    MEDIUM = "medium"       # Nice to have for optimal performance
    LOW = "low"            # Optional features

@dataclass
class TestCase:
    """Represents a single test case"""
    name: str
    description: str
    severity: TestSeverity
    category: str
    command: Optional[str] = None
    expected_result: Optional[str] = None
    timeout_seconds: int = 30
    retry_count: int = 1
    dependencies: List[str] = None

@dataclass
class TestResult:
    """Represents a test result"""
    test_name: str
    status: TestStatus
    execution_time: float
    output: str
    error: Optional[str] = None
    timestamp: str = None
    retry_attempts: int = 0

class RFEVerificationSystem:
    """Comprehensive verification system for RFE automation tool"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        
        # Test configuration
        self.test_timeout = 300  # 5 minutes max for full test suite
        self.retry_delay = 2     # 2 seconds between retries
        
        # Test results storage
        self.test_results = []
        self.test_summary = {
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'warnings': 0,
            'skipped': 0,
            'execution_time': 0.0
        }
        
        # Define comprehensive test cases
        self.test_cases = self._define_test_cases()
        
        self.logger.info("RFE Verification System initialized")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for verification system"""
        logger = logging.getLogger('rfe_verification')
        logger.setLevel(logging.INFO)
        
        # Create log file
        log_file = f"/tmp/rfe-verification-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _define_test_cases(self) -> List[TestCase]:
        """Define comprehensive test cases for RFE automation tool"""
        
        test_cases = [
            # System Prerequisites Tests
            TestCase(
                name="system_python_version",
                description="Verify Python 3.8+ is available",
                severity=TestSeverity.CRITICAL,
                category="prerequisites",
                command="python3 --version",
                expected_result="Python 3.8"
            ),
            TestCase(
                name="system_git_available",
                description="Verify Git is installed and configured",
                severity=TestSeverity.CRITICAL,
                category="prerequisites",
                command="git --version",
                expected_result="git version"
            ),
            TestCase(
                name="system_rhcase_available",
                description="Verify rhcase tool is installed",
                severity=TestSeverity.CRITICAL,
                category="prerequisites",
                command="rhcase --version",
                expected_result="rhcase"
            ),
            TestCase(
                name="system_cursor_available",
                description="Verify Cursor IDE is installed",
                severity=TestSeverity.HIGH,
                category="prerequisites",
                command="cursor --version",
                expected_result="cursor"
            ),
            
            # Red Hat Connectivity Tests
            TestCase(
                name="redhat_vpn_connectivity",
                description="Verify Red Hat VPN connectivity",
                severity=TestSeverity.CRITICAL,
                category="connectivity",
                command="curl -s --connect-timeout 10 https://access.redhat.com",
                expected_result="200"
            ),
            TestCase(
                name="redhat_gitlab_access",
                description="Verify GitLab access",
                severity=TestSeverity.HIGH,
                category="connectivity",
                command="curl -s --connect-timeout 10 https://gitlab.cee.redhat.com",
                expected_result="200"
            ),
            TestCase(
                name="redhat_ai_models_access",
                description="Verify Red Hat AI models API access",
                severity=TestSeverity.HIGH,
                category="connectivity",
                command="curl -s --connect-timeout 10 https://developer.models.corp.redhat.com",
                expected_result="200"
            ),
            
            # Authentication Tests
            TestCase(
                name="rhcase_authentication",
                description="Verify rhcase authentication works",
                severity=TestSeverity.CRITICAL,
                category="authentication",
                command="rhcase list 838043 --months 1",
                expected_result="cases found"
            ),
            TestCase(
                name="redhat_sso_credentials",
                description="Verify Red Hat SSO credentials are configured",
                severity=TestSeverity.CRITICAL,
                category="authentication",
                command="test -f ~/.config/pai/secrets/redhat_granite_api_key",
                expected_result="0"
            ),
            
            # Python Dependencies Tests
            TestCase(
                name="python_requests_available",
                description="Verify requests library is available",
                severity=TestSeverity.CRITICAL,
                category="dependencies",
                command="python3 -c 'import requests; print(requests.__version__)'",
                expected_result="2."
            ),
            TestCase(
                name="python_yaml_available",
                description="Verify PyYAML library is available",
                severity=TestSeverity.CRITICAL,
                category="dependencies",
                command="python3 -c 'import yaml; print(yaml.__version__)'",
                expected_result="5."
            ),
            TestCase(
                name="python_jinja2_available",
                description="Verify Jinja2 library is available",
                severity=TestSeverity.HIGH,
                category="dependencies",
                command="python3 -c 'import jinja2; print(jinja2.__version__)'",
                expected_result="3."
            ),
            
            # RFE Tool Components Tests
            TestCase(
                name="rfe_monitoring_system",
                description="Verify RFE monitoring system is available",
                severity=TestSeverity.CRITICAL,
                category="components",
                command="python3 -c 'import sys; sys.path.append(\"/home/jbyrd/pai/src\"); from rfe_monitoring_system import RFEMonitoringSystem; print(\"OK\")'",
                expected_result="OK"
            ),
            TestCase(
                name="rfe_error_handler",
                description="Verify RFE error handler is available",
                severity=TestSeverity.HIGH,
                category="components",
                command="python3 -c 'import sys; sys.path.append(\"/home/jbyrd/pai/src\"); from rfe_error_handler import RFEErrorHandler; print(\"OK\")'",
                expected_result="OK"
            ),
            TestCase(
                name="rfe_api_client",
                description="Verify RFE API client is available",
                severity=TestSeverity.CRITICAL,
                category="components",
                command="python3 -c 'from rfe_discussion_api_client import RFEDiscussionAPIClient; print(\"OK\")'",
                expected_result="OK"
            ),
            
            # Configuration Tests
            TestCase(
                name="customer_configuration",
                description="Verify customer configuration files exist",
                severity=TestSeverity.CRITICAL,
                category="configuration",
                command="test -f ~/.config/tam-rfe-automation/customer_accounts.yaml",
                expected_result="0"
            ),
            TestCase(
                name="group_ids_configuration",
                description="Verify group IDs configuration exists",
                severity=TestSeverity.CRITICAL,
                category="configuration",
                command="test -f ~/.config/tam-rfe-automation/customer_group_ids_config.json",
                expected_result="0"
            ),
            
            # End-to-End Tests
            TestCase(
                name="rfe_monitor_help",
                description="Verify RFE monitor command works",
                severity=TestSeverity.CRITICAL,
                category="e2e",
                command="tam-rfe-monitor --help",
                expected_result="Usage:"
            ),
            TestCase(
                name="rfe_deploy_help",
                description="Verify RFE deploy command works",
                severity=TestSeverity.HIGH,
                category="e2e",
                command="tam-rfe-deploy --help",
                expected_result="Usage:"
            ),
            
            # Performance Tests
            TestCase(
                name="rhcase_performance",
                description="Verify rhcase performance is acceptable",
                severity=TestSeverity.MEDIUM,
                category="performance",
                command="time rhcase list 838043 --months 1",
                expected_result="real",
                timeout_seconds=60
            ),
            TestCase(
                name="python_import_performance",
                description="Verify Python import performance",
                severity=TestSeverity.LOW,
                category="performance",
                command="time python3 -c 'import requests, yaml, json'",
                expected_result="real"
            ),
        ]
        
        return test_cases
    
    def run_single_test(self, test_case: TestCase) -> TestResult:
        """Run a single test case with retry logic"""
        
        self.logger.info(f"Running test: {test_case.name}")
        
        start_time = time.time()
        last_error = None
        
        for attempt in range(test_case.retry_count):
            try:
                # Execute the test command
                result = subprocess.run(
                    test_case.command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=test_case.timeout_seconds
                )
                
                execution_time = time.time() - start_time
                
                # Check if test passed
                if result.returncode == 0:
                    # Check expected result if specified
                    if test_case.expected_result:
                        if test_case.expected_result in result.stdout:
                            return TestResult(
                                test_name=test_case.name,
                                status=TestStatus.PASS,
                                execution_time=execution_time,
                                output=result.stdout,
                                timestamp=datetime.now().isoformat(),
                                retry_attempts=attempt
                            )
                        else:
                            last_error = f"Expected '{test_case.expected_result}' not found in output"
                    else:
                        # No expected result specified, just check return code
                        return TestResult(
                            test_name=test_case.name,
                            status=TestResult.PASS,
                            execution_time=execution_time,
                            output=result.stdout,
                            timestamp=datetime.now().isoformat(),
                            retry_attempts=attempt
                        )
                else:
                    last_error = f"Command failed with return code {result.returncode}: {result.stderr}"
                    
            except subprocess.TimeoutExpired:
                last_error = f"Test timed out after {test_case.timeout_seconds} seconds"
            except Exception as e:
                last_error = f"Test execution error: {str(e)}"
            
            # Wait before retry (except on last attempt)
            if attempt < test_case.retry_count - 1:
                time.sleep(self.retry_delay)
        
        # All attempts failed
        execution_time = time.time() - start_time
        return TestResult(
            test_name=test_case.name,
            status=TestStatus.FAIL,
            execution_time=execution_time,
            output="",
            error=last_error,
            timestamp=datetime.now().isoformat(),
            retry_attempts=test_case.retry_count
        )
    
    def run_test_suite(self, categories: List[str] = None, severity: TestSeverity = None) -> Dict[str, Any]:
        """Run comprehensive test suite"""
        
        self.logger.info("Starting RFE Verification Test Suite")
        
        start_time = time.time()
        
        # Filter test cases
        filtered_tests = self.test_cases
        
        if categories:
            filtered_tests = [t for t in filtered_tests if t.category in categories]
        
        if severity:
            filtered_tests = [t for t in filtered_tests if t.severity == severity]
        
        # Run tests
        for test_case in filtered_tests:
            result = self.run_single_test(test_case)
            self.test_results.append(result)
            
            # Log result
            status_icon = "✅" if result.status == TestStatus.PASS else "❌" if result.status == TestStatus.FAIL else "⚠️"
            self.logger.info(f"{status_icon} {test_case.name}: {result.status.value} ({result.execution_time:.2f}s)")
            
            if result.error:
                self.logger.error(f"   Error: {result.error}")
        
        # Calculate summary
        execution_time = time.time() - start_time
        self._calculate_summary(execution_time)
        
        # Generate report
        report = self._generate_report()
        
        return report
    
    def _calculate_summary(self, execution_time: float):
        """Calculate test summary statistics"""
        
        self.test_summary = {
            'total_tests': len(self.test_results),
            'passed': len([r for r in self.test_results if r.status == TestStatus.PASS]),
            'failed': len([r for r in self.test_results if r.status == TestStatus.FAIL]),
            'warnings': len([r for r in self.test_results if r.status == TestStatus.WARN]),
            'skipped': len([r for r in self.test_results if r.status == TestStatus.SKIP]),
            'execution_time': execution_time
        }
    
    def _generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        
        # Group results by category
        categories = {}
        for test_case in self.test_cases:
            if test_case.category not in categories:
                categories[test_case.category] = []
            categories[test_case.category].append(test_case)
        
        # Calculate category statistics
        category_stats = {}
        for category, tests in categories.items():
            category_results = [r for r in self.test_results if r.test_name in [t.name for t in tests]]
            category_stats[category] = {
                'total': len(category_results),
                'passed': len([r for r in category_results if r.status == TestStatus.PASS]),
                'failed': len([r for r in category_results if r.status == TestStatus.FAIL]),
                'success_rate': len([r for r in category_results if r.status == TestStatus.PASS]) / len(category_results) * 100 if category_results else 0
            }
        
        # Determine overall health
        critical_tests = [r for r in self.test_results if any(t.severity == TestSeverity.CRITICAL and t.name == r.test_name for t in self.test_cases)]
        critical_failures = [r for r in critical_tests if r.status == TestStatus.FAIL]
        
        if critical_failures:
            overall_health = "CRITICAL_FAILURE"
        elif self.test_summary['failed'] > 0:
            overall_health = "DEGRADED"
        else:
            overall_health = "HEALTHY"
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'overall_health': overall_health,
            'summary': self.test_summary,
            'category_stats': category_stats,
            'test_results': [asdict(r) for r in self.test_results],
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results"""
        
        recommendations = []
        
        # Check for critical failures
        critical_failures = [r for r in self.test_results if r.status == TestStatus.FAIL and any(t.severity == TestSeverity.CRITICAL and t.name == r.test_name for t in self.test_cases)]
        
        if critical_failures:
            recommendations.append("🚨 CRITICAL: Fix critical test failures before using the tool")
            for failure in critical_failures:
                recommendations.append(f"   - {failure.test_name}: {failure.error}")
        
        # Check for connectivity issues
        connectivity_failures = [r for r in self.test_results if r.status == TestStatus.FAIL and "connectivity" in r.test_name]
        if connectivity_failures:
            recommendations.append("🌐 NETWORK: Check Red Hat VPN connection and network access")
        
        # Check for authentication issues
        auth_failures = [r for r in self.test_results if r.status == TestStatus.FAIL and "authentication" in r.test_name]
        if auth_failures:
            recommendations.append("🔐 AUTH: Verify Red Hat SSO credentials and rhcase configuration")
        
        # Check for dependency issues
        dep_failures = [r for r in self.test_results if r.status == TestStatus.FAIL and "dependencies" in r.test_name]
        if dep_failures:
            recommendations.append("📦 DEPS: Install missing Python dependencies")
        
        # Performance recommendations
        slow_tests = [r for r in self.test_results if r.execution_time > 10.0]
        if slow_tests:
            recommendations.append("⚡ PERFORMANCE: Some tests are running slowly - check system resources")
        
        # Success recommendations
        if not critical_failures and not connectivity_failures and not auth_failures:
            recommendations.append("✅ SUCCESS: All critical tests passed - tool is ready for use")
            recommendations.append("🚀 NEXT: Run 'tam-rfe-monitor --test-system' to test the full system")
        
        return recommendations
    
    def save_report(self, report: Dict[str, Any], filename: str = None) -> str:
        """Save test report to file"""
        
        if not filename:
            filename = f"/tmp/rfe-verification-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"Test report saved to: {filename}")
        return filename
    
    def print_summary(self, report: Dict[str, Any]):
        """Print test summary to console"""
        
        print("\n" + "="*60)
        print("🧪 RFE VERIFICATION SYSTEM - TEST RESULTS")
        print("="*60)
        
        # Overall health
        health_icon = "🟢" if report['overall_health'] == "HEALTHY" else "🟡" if report['overall_health'] == "DEGRADED" else "🔴"
        print(f"\n{health_icon} Overall Health: {report['overall_health']}")
        
        # Summary statistics
        summary = report['summary']
        print(f"\n📊 Test Summary:")
        print(f"   Total Tests: {summary['total_tests']}")
        print(f"   Passed: {summary['passed']} ✅")
        print(f"   Failed: {summary['failed']} ❌")
        print(f"   Warnings: {summary['warnings']} ⚠️")
        print(f"   Skipped: {summary['skipped']} ⏭️")
        print(f"   Execution Time: {summary['execution_time']:.2f}s")
        print(f"   Success Rate: {(summary['passed']/summary['total_tests']*100):.1f}%")
        
        # Category breakdown
        print(f"\n📋 Category Breakdown:")
        for category, stats in report['category_stats'].items():
            success_rate = stats['success_rate']
            status_icon = "✅" if success_rate == 100 else "⚠️" if success_rate >= 80 else "❌"
            print(f"   {status_icon} {category.title()}: {stats['passed']}/{stats['total']} ({success_rate:.1f}%)")
        
        # Recommendations
        if report['recommendations']:
            print(f"\n💡 Recommendations:")
            for rec in report['recommendations']:
                print(f"   {rec}")
        
        print("\n" + "="*60)

def main():
    """Run RFE verification system"""
    
    print("🧪 RFE Verification System")
    print("=" * 40)
    
    # Initialize verification system
    verifier = RFEVerificationSystem()
    
    # Run test suite
    report = verifier.run_test_suite()
    
    # Print summary
    verifier.print_summary(report)
    
    # Save report
    report_file = verifier.save_report(report)
    
    # Return appropriate exit code
    if report['overall_health'] == "CRITICAL_FAILURE":
        print("\n💥 CRITICAL FAILURES DETECTED - Tool is not ready for use")
        return 1
    elif report['overall_health'] == "DEGRADED":
        print("\n⚠️  DEGRADED PERFORMANCE - Tool may have issues")
        return 2
    else:
        print("\n✅ ALL TESTS PASSED - Tool is ready for use")
        return 0

if __name__ == '__main__':
    sys.exit(main())

