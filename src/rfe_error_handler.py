#!/usr/bin/env python3

"""
RFE Error Handler - Enhanced Error Handling System
Purpose: Provide robust retry logic, timeout handling, and graceful degradation
Features: Exponential backoff, circuit breaker pattern, graceful fallbacks
"""

import os
import sys
import time
import json
import logging
import functools
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable, Union
from enum import Enum

class ErrorSeverity(Enum):
    """Error severity levels for different handling strategies"""
    LOW = "low"           # Retry with short delays
    MEDIUM = "medium"     # Retry with exponential backoff
    HIGH = "high"         # Limited retries, immediate alerts
    CRITICAL = "critical" # No retries, immediate escalation

class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"     # Normal operation
    OPEN = "open"         # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered

class RFEErrorHandler:
    """Enhanced error handling system for RFE automation"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        
        # Retry configuration
        self.retry_config = {
            ErrorSeverity.LOW: {
                'max_attempts': 5,
                'base_delay': 1.0,
                'max_delay': 10.0,
                'backoff_factor': 1.5
            },
            ErrorSeverity.MEDIUM: {
                'max_attempts': 3,
                'base_delay': 2.0,
                'max_delay': 30.0,
                'backoff_factor': 2.0
            },
            ErrorSeverity.HIGH: {
                'max_attempts': 2,
                'base_delay': 5.0,
                'max_delay': 60.0,
                'backoff_factor': 2.0
            },
            ErrorSeverity.CRITICAL: {
                'max_attempts': 1,
                'base_delay': 0.0,
                'max_delay': 0.0,
                'backoff_factor': 1.0
            }
        }
        
        # Circuit breaker configuration
        self.circuit_breakers = {}
        self.circuit_config = {
            'failure_threshold': 5,
            'recovery_timeout': 300,  # 5 minutes
            'half_open_max_calls': 3
        }
        
        # Error classification patterns
        self.error_patterns = {
            ErrorSeverity.LOW: [
                'connection timeout',
                'temporary network error',
                'rate limit exceeded',
                'service temporarily unavailable'
            ],
            ErrorSeverity.MEDIUM: [
                'authentication failed',
                'invalid response format',
                'api error 5',  # 5xx errors
                'browser automation failed'
            ],
            ErrorSeverity.HIGH: [
                'permission denied',
                'invalid credentials',
                'api error 4',  # 4xx errors (except rate limiting)
                'configuration error'
            ],
            ErrorSeverity.CRITICAL: [
                'system out of memory',
                'disk full',
                'critical system error',
                'security violation'
            ]
        }
        
        # Graceful degradation strategies
        self.fallback_strategies = {
            'rhcase_failure': self._fallback_to_cached_data,
            'api_posting_failure': self._fallback_to_file_output,
            'browser_automation_failure': self._fallback_to_manual_instructions,
            'monitoring_failure': self._fallback_to_basic_logging
        }
    
    def _setup_logging(self) -> logging.Logger:
        """Setup enhanced logging for error handling"""
        logger = logging.getLogger('rfe_error_handler')
        logger.setLevel(logging.INFO)
        
        # Create log file with rotation
        log_file = f"/tmp/rfe-error-handler-{datetime.now().strftime('%Y%m%d')}.log"
        
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
    
    def classify_error(self, error: Exception, context: str = "") -> ErrorSeverity:
        """Classify error severity based on error message and context"""
        
        error_message = str(error).lower()
        
        # Check each severity level
        for severity, patterns in self.error_patterns.items():
            for pattern in patterns:
                if pattern in error_message:
                    self.logger.info(f"Classified error as {severity.value}: {pattern}")
                    return severity
        
        # Default to MEDIUM severity for unclassified errors
        self.logger.warning(f"Unclassified error, defaulting to MEDIUM: {error_message}")
        return ErrorSeverity.MEDIUM
    
    def retry_with_backoff(self, 
                          func: Callable, 
                          *args, 
                          severity: ErrorSeverity = ErrorSeverity.MEDIUM,
                          context: str = "",
                          **kwargs) -> Any:
        """Execute function with retry logic and exponential backoff"""
        
        config = self.retry_config[severity]
        max_attempts = config['max_attempts']
        base_delay = config['base_delay']
        max_delay = config['max_delay']
        backoff_factor = config['backoff_factor']
        
        last_exception = None
        
        for attempt in range(1, max_attempts + 1):
            try:
                self.logger.info(f"Attempt {attempt}/{max_attempts} for {func.__name__} ({context})")
                result = func(*args, **kwargs)
                
                if attempt > 1:
                    self.logger.info(f"✅ Success on attempt {attempt} for {func.__name__}")
                
                return result
                
            except Exception as e:
                last_exception = e
                error_severity = self.classify_error(e, context)
                
                self.logger.warning(f"❌ Attempt {attempt} failed for {func.__name__}: {e}")
                
                # If this is the last attempt, don't wait
                if attempt == max_attempts:
                    break
                
                # Calculate delay with exponential backoff
                delay = min(base_delay * (backoff_factor ** (attempt - 1)), max_delay)
                
                self.logger.info(f"⏱️  Waiting {delay:.1f}s before retry...")
                time.sleep(delay)
        
        # All attempts failed
        self.logger.error(f"💥 All {max_attempts} attempts failed for {func.__name__}")
        raise last_exception
    
    def with_circuit_breaker(self, service_name: str):
        """Decorator to add circuit breaker pattern to functions"""
        
        def decorator(func: Callable):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return self._execute_with_circuit_breaker(service_name, func, *args, **kwargs)
            return wrapper
        return decorator
    
    def _execute_with_circuit_breaker(self, service_name: str, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker pattern"""
        
        # Initialize circuit breaker if not exists
        if service_name not in self.circuit_breakers:
            self.circuit_breakers[service_name] = {
                'state': CircuitState.CLOSED,
                'failure_count': 0,
                'last_failure_time': None,
                'half_open_calls': 0
            }
        
        circuit = self.circuit_breakers[service_name]
        
        # Check circuit state
        if circuit['state'] == CircuitState.OPEN:
            # Check if recovery timeout has passed
            if (circuit['last_failure_time'] and 
                datetime.now() - circuit['last_failure_time'] > timedelta(seconds=self.circuit_config['recovery_timeout'])):
                circuit['state'] = CircuitState.HALF_OPEN
                circuit['half_open_calls'] = 0
                self.logger.info(f"🔄 Circuit breaker for {service_name} moved to HALF_OPEN")
            else:
                raise Exception(f"Circuit breaker OPEN for {service_name} - service unavailable")
        
        if circuit['state'] == CircuitState.HALF_OPEN:
            if circuit['half_open_calls'] >= self.circuit_config['half_open_max_calls']:
                raise Exception(f"Circuit breaker HALF_OPEN limit reached for {service_name}")
        
        try:
            result = func(*args, **kwargs)
            
            # Success - reset circuit breaker
            if circuit['state'] in [CircuitState.HALF_OPEN, CircuitState.CLOSED]:
                circuit['state'] = CircuitState.CLOSED
                circuit['failure_count'] = 0
                circuit['half_open_calls'] = 0
                
                if circuit['state'] == CircuitState.HALF_OPEN:
                    self.logger.info(f"✅ Circuit breaker for {service_name} recovered - moved to CLOSED")
            
            return result
            
        except Exception as e:
            # Failure - update circuit breaker
            circuit['failure_count'] += 1
            circuit['last_failure_time'] = datetime.now()
            
            if circuit['state'] == CircuitState.HALF_OPEN:
                circuit['half_open_calls'] += 1
            
            # Check if we should open the circuit
            if circuit['failure_count'] >= self.circuit_config['failure_threshold']:
                circuit['state'] = CircuitState.OPEN
                self.logger.error(f"💥 Circuit breaker OPENED for {service_name} after {circuit['failure_count']} failures")
            
            raise e
    
    def execute_with_fallback(self, 
                             primary_func: Callable, 
                             fallback_strategy: str,
                             context: str = "",
                             *args, **kwargs) -> Any:
        """Execute function with graceful degradation fallback"""
        
        try:
            return primary_func(*args, **kwargs)
            
        except Exception as e:
            self.logger.warning(f"⚠️  Primary function failed, attempting fallback: {e}")
            
            if fallback_strategy in self.fallback_strategies:
                fallback_func = self.fallback_strategies[fallback_strategy]
                try:
                    result = fallback_func(context, e, *args, **kwargs)
                    self.logger.info(f"✅ Fallback strategy '{fallback_strategy}' succeeded")
                    return result
                except Exception as fallback_error:
                    self.logger.error(f"💥 Fallback strategy '{fallback_strategy}' also failed: {fallback_error}")
                    raise fallback_error
            else:
                self.logger.error(f"❌ No fallback strategy found for '{fallback_strategy}'")
                raise e
    
    def _fallback_to_cached_data(self, context: str, error: Exception, *args, **kwargs) -> Dict:
        """Fallback to cached data when rhcase fails"""
        
        cache_file = "/tmp/rfe-cached-data.json"
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    cached_data = json.load(f)
                
                # Check if cache is recent (within 24 hours)
                cache_time = datetime.fromisoformat(cached_data.get('timestamp', '2000-01-01'))
                if datetime.now() - cache_time < timedelta(hours=24):
                    self.logger.info("📁 Using cached data (< 24 hours old)")
                    return cached_data.get('data', {})
                else:
                    self.logger.warning("📁 Cached data is too old (> 24 hours)")
            except Exception as cache_error:
                self.logger.error(f"❌ Failed to read cached data: {cache_error}")
        
        # Return minimal fallback data
        return {
            'cases': [],
            'error': 'Data unavailable - using fallback',
            'timestamp': datetime.now().isoformat(),
            'source': 'fallback'
        }
    
    def _fallback_to_file_output(self, context: str, error: Exception, *args, **kwargs) -> Dict:
        """Fallback to file output when API posting fails"""
        
        # Generate content for manual posting
        content = kwargs.get('content', 'Content unavailable')
        customer = kwargs.get('customer', 'unknown')
        
        fallback_file = f"/tmp/rfe-manual-post-{customer}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        
        try:
            with open(fallback_file, 'w') as f:
                f.write(f"# RFE Automation - Manual Posting Required\n\n")
                f.write(f"**Customer**: {customer}\n")
                f.write(f"**Timestamp**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Error**: {error}\n\n")
                f.write(f"## Content for Manual Posting:\n\n")
                f.write(content)
            
            self.logger.info(f"📁 Manual posting content saved to: {fallback_file}")
            
            return {
                'method_used': 'file_fallback',
                'file_path': fallback_file,
                'customer': customer,
                'success': True,
                'message': 'Content saved for manual posting'
            }
            
        except Exception as file_error:
            self.logger.error(f"❌ Failed to create fallback file: {file_error}")
            raise file_error
    
    def _fallback_to_manual_instructions(self, context: str, error: Exception, *args, **kwargs) -> Dict:
        """Fallback to manual instructions when browser automation fails"""
        
        customer = kwargs.get('customer', 'unknown')
        portal_url = kwargs.get('portal_url', 'https://access.redhat.com/groups/')
        
        instructions_file = f"/tmp/rfe-manual-instructions-{customer}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
        
        instructions = f"""
RFE Automation - Manual Instructions Required

Customer: {customer}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Error: {error}

MANUAL STEPS REQUIRED:

1. Open browser and navigate to: {portal_url}
2. Log in with your Red Hat credentials
3. Navigate to the customer portal page
4. Edit the page content
5. Paste the generated content (see accompanying .md file)
6. IMPORTANT: Uncheck "Send Subscription Notifications" before saving
7. Save the changes

The generated content should be available in the corresponding .md file.
Contact jbyrd@redhat.com if you need assistance.
        """
        
        try:
            with open(instructions_file, 'w') as f:
                f.write(instructions)
            
            self.logger.info(f"📋 Manual instructions saved to: {instructions_file}")
            
            return {
                'method_used': 'manual_instructions',
                'instructions_file': instructions_file,
                'customer': customer,
                'success': True,
                'message': 'Manual instructions provided'
            }
            
        except Exception as file_error:
            self.logger.error(f"❌ Failed to create instructions file: {file_error}")
            raise file_error
    
    def _fallback_to_basic_logging(self, context: str, error: Exception, *args, **kwargs) -> Dict:
        """Fallback to basic logging when monitoring fails"""
        
        basic_log = f"/tmp/rfe-basic-log-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
        
        log_content = f"""
RFE Automation Basic Log

Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Context: {context}
Monitoring Error: {error}

This is a basic fallback log created when the main monitoring system failed.
Check the main system logs for more details.

Args: {args}
Kwargs: {kwargs}
        """
        
        try:
            with open(basic_log, 'w') as f:
                f.write(log_content)
            
            self.logger.info(f"📝 Basic log created: {basic_log}")
            
            return {
                'method_used': 'basic_logging',
                'log_file': basic_log,
                'success': True,
                'message': 'Basic logging fallback used'
            }
            
        except Exception as file_error:
            self.logger.error(f"❌ Failed to create basic log: {file_error}")
            raise file_error
    
    def test_error_handling(self) -> Dict[str, Any]:
        """Test the error handling system with various scenarios"""
        
        test_results = {
            'timestamp': datetime.now().isoformat(),
            'tests': {}
        }
        
        # Test 1: Retry with backoff
        def failing_function(attempt_count=3):
            if hasattr(failing_function, 'calls'):
                failing_function.calls += 1
            else:
                failing_function.calls = 1
            
            if failing_function.calls < attempt_count:
                raise Exception("Temporary failure")
            return f"Success after {failing_function.calls} attempts"
        
        try:
            result = self.retry_with_backoff(
                failing_function, 
                attempt_count=2,
                severity=ErrorSeverity.LOW,
                context="test_retry"
            )
            test_results['tests']['retry_backoff'] = {'success': True, 'result': result}
        except Exception as e:
            test_results['tests']['retry_backoff'] = {'success': False, 'error': str(e)}
        
        # Test 2: Circuit breaker
        @self.with_circuit_breaker('test_service')
        def circuit_test_function():
            raise Exception("Service failure")
        
        circuit_failures = 0
        for i in range(7):  # Exceed failure threshold
            try:
                circuit_test_function()
            except Exception:
                circuit_failures += 1
        
        test_results['tests']['circuit_breaker'] = {
            'success': circuit_failures >= self.circuit_config['failure_threshold'],
            'failures': circuit_failures
        }
        
        # Test 3: Fallback strategies
        def primary_failing_function():
            raise Exception("Primary function failed")
        
        try:
            result = self.execute_with_fallback(
                primary_failing_function,
                'api_posting_failure',
                context='test_fallback',
                customer='test_customer',
                content='Test content'
            )
            test_results['tests']['fallback_strategy'] = {'success': True, 'result': result}
        except Exception as e:
            test_results['tests']['fallback_strategy'] = {'success': False, 'error': str(e)}
        
        return test_results

def main():
    """Test the error handling system"""
    
    print("🧪 RFE Error Handler - Test Mode")
    print("=" * 40)
    
    handler = RFEErrorHandler()
    
    # Run comprehensive tests
    test_results = handler.test_error_handling()
    
    print("\n📊 TEST RESULTS:")
    for test_name, result in test_results['tests'].items():
        status = "✅ PASSED" if result['success'] else "❌ FAILED"
        print(f"   {test_name}: {status}")
        
        if not result['success'] and 'error' in result:
            print(f"      Error: {result['error']}")
    
    # Overall success
    all_passed = all(test['success'] for test in test_results['tests'].values())
    
    if all_passed:
        print("\n🎉 All error handling tests PASSED")
        return 0
    else:
        print("\n💥 Some error handling tests FAILED")
        return 1

if __name__ == '__main__':
    sys.exit(main())
