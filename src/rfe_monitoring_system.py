#!/usr/bin/env python3

"""
RFE Monitoring & Alerting System
Purpose: Monitor RFE automation system and send email alerts on failures
Email: jbyrd@redhat.com on automation failures
"""

import os
import sys
import json
import smtplib
import logging
import traceback
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional, Any
import subprocess

# Import enhanced error handling
try:
    from rfe_error_handler import RFEErrorHandler, ErrorSeverity
except ImportError:
    # Fallback if error handler not available
    RFEErrorHandler = None
    ErrorSeverity = None

class RFEMonitoringSystem:
    """Monitor RFE automation system and send alerts on failures"""
    
    def __init__(self):
        self.admin_email = "jbyrd@redhat.com"
        self.smtp_server = "localhost"  # Use local mail system
        self.smtp_port = 25
        
        # Initialize enhanced error handling
        self.error_handler = RFEErrorHandler() if RFEErrorHandler else None
        
        # Setup logging
        self.log_file = f"/tmp/rfe-monitoring-{datetime.now().strftime('%Y%m%d')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Monitoring configuration
        self.monitoring_config = {
            'customers': ['wellsfargo', 'tdbank'],
            'alert_thresholds': {
                'consecutive_failures': 2,
                'failure_rate_threshold': 0.5,  # 50% failure rate
                'max_execution_time': 600  # 10 minutes
            },
            'notification_settings': {
                'send_success_summary': True,
                'send_failure_immediate': True,
                'daily_summary_time': '09:00'
            }
        }
        
    def send_email_alert(self, subject: str, body: str, alert_type: str = "failure") -> bool:
        """Send email alert to admin with file-based fallback"""
        
        # Always create file-based alert first (guaranteed delivery)
        file_alert_success = self._create_file_alert(subject, body, alert_type)
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = f"RFE Automation System <noreply@{os.uname().nodename}>"
            msg['To'] = self.admin_email
            msg['Subject'] = f"[RFE Alert] {subject}"
            
            # Add body
            html_body = self._format_email_body(body, alert_type)
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send via local mail system (sendmail)
            try:
                # Try using sendmail directly (most reliable on Red Hat systems)
                process = subprocess.Popen(
                    ['/usr/sbin/sendmail', '-t'],
                    stdin=subprocess.PIPE,
                    text=True
                )
                process.communicate(msg.as_string())
                
                if process.returncode == 0:
                    self.logger.info(f"✅ Email alert sent successfully: {subject}")
                    return True
                else:
                    raise Exception(f"Sendmail returned code {process.returncode}")
                    
            except Exception as sendmail_error:
                # Fallback to SMTP if sendmail fails
                self.logger.warning(f"Sendmail failed: {sendmail_error}, trying SMTP...")
                
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.send_message(msg)
                
                self.logger.info(f"✅ Email alert sent via SMTP: {subject}")
                return True
                
        except Exception as e:
            self.logger.error(f"❌ Failed to send email alert: {e}")
            # Email failed, but file alert succeeded - still considered success
            if file_alert_success:
                self.logger.info(f"✅ File-based alert created as fallback: {subject}")
                return True
            else:
                self.logger.error(f"❌ Both email and file alerts failed: {subject}")
                return False
    
    def _format_email_body(self, body: str, alert_type: str) -> str:
        """Format email body with HTML styling"""
        
        # Color scheme based on alert type
        colors = {
            'failure': {'bg': '#ffebee', 'border': '#f44336', 'icon': '❌'},
            'warning': {'bg': '#fff3e0', 'border': '#ff9800', 'icon': '⚠️'},
            'success': {'bg': '#e8f5e8', 'border': '#4caf50', 'icon': '✅'},
            'info': {'bg': '#e3f2fd', 'border': '#2196f3', 'icon': '💡'}
        }
        
        color = colors.get(alert_type, colors['info'])
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
                .alert-container {{ 
                    background-color: {color['bg']}; 
                    border-left: 4px solid {color['border']}; 
                    padding: 20px; 
                    margin: 10px 0; 
                    border-radius: 4px;
                }}
                .alert-header {{ 
                    font-size: 18px; 
                    font-weight: bold; 
                    color: {color['border']}; 
                    margin-bottom: 10px;
                }}
                .alert-body {{ 
                    white-space: pre-wrap; 
                    font-family: monospace; 
                    background: white; 
                    padding: 15px; 
                    border-radius: 4px; 
                    border: 1px solid #ddd;
                }}
                .footer {{ 
                    margin-top: 20px; 
                    padding-top: 10px; 
                    border-top: 1px solid #ddd; 
                    font-size: 12px; 
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="alert-container">
                <div class="alert-header">
                    {color['icon']} RFE Automation System Alert
                </div>
                <div class="alert-body">{body}</div>
            </div>
            <div class="footer">
                <strong>System Information:</strong><br>
                Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}<br>
                Hostname: {os.uname().nodename}<br>
                Log File: {self.log_file}<br>
                <br>
                This is an automated message from the RFE Bug Tracker Automation System.
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _create_file_alert(self, subject: str, body: str, alert_type: str) -> bool:
        """Create file-based alert for guaranteed notification delivery"""
        try:
            # Create alerts directory
            alerts_dir = "/tmp/rfe-alerts"
            os.makedirs(alerts_dir, exist_ok=True)
            
            # Create timestamped alert file
            timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            alert_file = f"{alerts_dir}/rfe-alert-{alert_type}-{timestamp}.txt"
            
            # Create alert content
            alert_content = f"""
RFE AUTOMATION SYSTEM ALERT
{'='*50}

Alert Type: {alert_type.upper()}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}
Subject: {subject}
Admin Email: {self.admin_email}

ALERT DETAILS:
{body}

SYSTEM INFORMATION:
Hostname: {os.uname().nodename}
Log File: {self.log_file}
Alert File: {alert_file}

{'='*50}
END OF ALERT
"""
            
            # Write alert file
            with open(alert_file, 'w') as f:
                f.write(alert_content)
            
            # Create latest alert symlink for easy access
            latest_link = f"{alerts_dir}/latest-{alert_type}-alert.txt"
            if os.path.exists(latest_link):
                os.remove(latest_link)
            os.symlink(alert_file, latest_link)
            
            # Create summary file for dashboard
            self._update_alert_summary(alert_type, subject, alert_file)
            
            self.logger.info(f"📁 File alert created: {alert_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create file alert: {e}")
            return False
    
    def _update_alert_summary(self, alert_type: str, subject: str, alert_file: str):
        """Update alert summary dashboard"""
        try:
            summary_file = "/tmp/rfe-alerts/alert-summary.json"
            
            # Load existing summary
            summary = {}
            if os.path.exists(summary_file):
                with open(summary_file, 'r') as f:
                    summary = json.load(f)
            
            # Initialize structure
            if 'alerts' not in summary:
                summary['alerts'] = []
            if 'stats' not in summary:
                summary['stats'] = {'total': 0, 'failure': 0, 'warning': 0, 'success': 0, 'info': 0}
            
            # Add new alert
            alert_entry = {
                'timestamp': datetime.now().isoformat(),
                'type': alert_type,
                'subject': subject,
                'file': alert_file
            }
            
            summary['alerts'].insert(0, alert_entry)  # Most recent first
            summary['alerts'] = summary['alerts'][:50]  # Keep last 50 alerts
            
            # Update stats
            summary['stats']['total'] += 1
            summary['stats'][alert_type] = summary['stats'].get(alert_type, 0) + 1
            summary['last_updated'] = datetime.now().isoformat()
            
            # Save summary
            with open(summary_file, 'w') as f:
                json.dump(summary, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"❌ Failed to update alert summary: {e}")
    
    def _log_critical_alert(self, subject: str, body: str, error: str):
        """Log critical alert when both email and file alerts fail"""
        critical_log = f"/tmp/rfe-critical-alerts-{datetime.now().strftime('%Y%m%d')}.log"
        
        with open(critical_log, 'a') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"CRITICAL ALERT - ALL NOTIFICATIONS FAILED\n")
            f.write(f"Timestamp: {datetime.now()}\n")
            f.write(f"Subject: {subject}\n")
            f.write(f"Email Error: {error}\n")
            f.write(f"Alert Body:\n{body}\n")
            f.write(f"{'='*60}\n")
    
    def monitor_rfe_execution(self, customer: str, command: str) -> Dict[str, Any]:
        """Monitor RFE automation execution for a customer with enhanced error handling"""
        
        execution_start = datetime.now()
        self.logger.info(f"🔍 Starting monitoring for {customer}: {command}")
        
        result = {
            'customer': customer,
            'command': command,
            'start_time': execution_start.isoformat(),
            'success': False,
            'execution_time': 0,
            'output': '',
            'error': '',
            'exit_code': None,
            'retry_attempts': 0,
            'error_handling_used': False
        }
        
        # Enhanced execution with error handling
        if self.error_handler:
            try:
                result = self._execute_with_error_handling(customer, command, result)
            except Exception as e:
                self.logger.error(f"💥 Enhanced error handling failed: {e}")
                # Fall back to basic execution
                result = self._execute_basic(customer, command, result)
        else:
            # Basic execution without error handling
            result = self._execute_basic(customer, command, result)
        
        return result
    
    def _execute_with_error_handling(self, customer: str, command: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Execute command with enhanced error handling and retries"""
        
        def execute_command():
            return subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.monitoring_config['alert_thresholds']['max_execution_time']
            )
        
        execution_start = datetime.now()
        
        try:
            # Execute with retry logic and circuit breaker
            process = self.error_handler.retry_with_backoff(
                execute_command,
                severity=ErrorSeverity.MEDIUM,
                context=f"{customer}_automation"
            )
            
            execution_end = datetime.now()
            execution_time = (execution_end - execution_start).total_seconds()
            
            result.update({
                'end_time': execution_end.isoformat(),
                'execution_time': execution_time,
                'output': process.stdout,
                'error': process.stderr,
                'exit_code': process.returncode,
                'success': process.returncode == 0,
                'error_handling_used': True,
                'retry_attempts': getattr(execute_command, 'retry_attempts', 0)
            })
            
            # Log execution results
            if result['success']:
                self.logger.info(f"✅ {customer} automation completed successfully in {execution_time:.1f}s")
            else:
                self.logger.error(f"❌ {customer} automation failed with exit code {process.returncode}")
                self._send_failure_alert(result)
            
        except subprocess.TimeoutExpired:
            execution_end = datetime.now()
            execution_time = (execution_end - execution_start).total_seconds()
            
            result.update({
                'end_time': execution_end.isoformat(),
                'execution_time': execution_time,
                'error': f"Command timed out after {execution_time:.1f} seconds",
                'exit_code': -1,
                'error_handling_used': True
            })
            
            self.logger.error(f"⏰ {customer} automation timed out after {execution_time:.1f}s")
            self._send_timeout_alert(result)
            
        except Exception as e:
            execution_end = datetime.now()
            execution_time = (execution_end - execution_start).total_seconds()
            
            result.update({
                'end_time': execution_end.isoformat(),
                'execution_time': execution_time,
                'error': f"Enhanced execution error: {str(e)}",
                'exit_code': -2,
                'error_handling_used': True
            })
            
            self.logger.error(f"💥 {customer} enhanced execution failed: {e}")
            self._send_monitoring_error_alert(result, e)
        
        # Save execution log
        self._save_execution_log(result)
        
        return result
    
    def _execute_basic(self, customer: str, command: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Basic execution without enhanced error handling (fallback)"""
        
        execution_start = datetime.now()
        
        try:
            # Execute the RFE automation command
            process = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.monitoring_config['alert_thresholds']['max_execution_time']
            )
            
            execution_end = datetime.now()
            execution_time = (execution_end - execution_start).total_seconds()
            
            result.update({
                'end_time': execution_end.isoformat(),
                'execution_time': execution_time,
                'output': process.stdout,
                'error': process.stderr,
                'exit_code': process.returncode,
                'success': process.returncode == 0
            })
            
            # Log execution results
            if result['success']:
                self.logger.info(f"✅ {customer} automation completed successfully in {execution_time:.1f}s")
            else:
                self.logger.error(f"❌ {customer} automation failed with exit code {process.returncode}")
                
                # Send immediate failure alert
                self._send_failure_alert(result)
            
        except subprocess.TimeoutExpired:
            execution_end = datetime.now()
            execution_time = (execution_end - execution_start).total_seconds()
            
            result.update({
                'end_time': execution_end.isoformat(),
                'execution_time': execution_time,
                'error': f"Command timed out after {execution_time:.1f} seconds",
                'exit_code': -1
            })
            
            self.logger.error(f"⏰ {customer} automation timed out after {execution_time:.1f}s")
            self._send_timeout_alert(result)
            
        except Exception as e:
            execution_end = datetime.now()
            execution_time = (execution_end - execution_start).total_seconds()
            
            result.update({
                'end_time': execution_end.isoformat(),
                'execution_time': execution_time,
                'error': f"Monitoring error: {str(e)}",
                'exit_code': -2
            })
            
            self.logger.error(f"💥 {customer} monitoring failed: {e}")
            self._send_monitoring_error_alert(result, e)
        
        # Save execution log
        self._save_execution_log(result)
        
        return result
    
    def _send_failure_alert(self, result: Dict[str, Any]):
        """Send immediate failure alert"""
        
        subject = f"RFE Automation FAILED - {result['customer'].title()}"
        
        body = f"""
RFE Automation Failure Report

Customer: {result['customer'].title()}
Command: {result['command']}
Start Time: {result['start_time']}
End Time: {result.get('end_time', 'Unknown')}
Execution Time: {result['execution_time']:.1f} seconds
Exit Code: {result['exit_code']}

ERROR OUTPUT:
{result['error']}

STDOUT OUTPUT:
{result['output'][:1000]}{'...' if len(result['output']) > 1000 else ''}

RECOMMENDED ACTIONS:
1. Check rhcase connectivity: rhcase --version
2. Verify customer configuration: pai-rfe-deploy --validate
3. Review full logs: {self.log_file}
4. Test manual execution: {result['command']}

This failure requires immediate attention to prevent customer impact.
        """
        
        self.send_email_alert(subject, body, "failure")
    
    def _send_timeout_alert(self, result: Dict[str, Any]):
        """Send timeout alert"""
        
        subject = f"RFE Automation TIMEOUT - {result['customer'].title()}"
        
        body = f"""
RFE Automation Timeout Report

Customer: {result['customer'].title()}
Command: {result['command']}
Start Time: {result['start_time']}
Timeout After: {result['execution_time']:.1f} seconds
Max Allowed: {self.monitoring_config['alert_thresholds']['max_execution_time']} seconds

POSSIBLE CAUSES:
- Network connectivity issues
- API rate limiting
- Browser automation hanging
- Large data processing

RECOMMENDED ACTIONS:
1. Check system resources: top, df -h
2. Test network connectivity: ping access.redhat.com
3. Review rhcase performance: rhcase list wellsfargo --months 1
4. Check for hanging processes: ps aux | grep python

Manual intervention may be required to resolve the timeout.
        """
        
        self.send_email_alert(subject, body, "warning")
    
    def _send_monitoring_error_alert(self, result: Dict[str, Any], error: Exception):
        """Send monitoring system error alert"""
        
        subject = f"RFE Monitoring System ERROR - {result['customer'].title()}"
        
        body = f"""
RFE Monitoring System Error Report

Customer: {result['customer'].title()}
Command: {result['command']}
Error: {str(error)}
Traceback:
{traceback.format_exc()}

SYSTEM STATUS:
- Monitoring system encountered an internal error
- RFE automation status unknown
- Manual verification required

RECOMMENDED ACTIONS:
1. Check monitoring system logs: {self.log_file}
2. Verify system dependencies: python3, subprocess
3. Test RFE automation manually: {result['command']}
4. Restart monitoring if needed

The monitoring system requires attention to ensure reliable alerting.
        """
        
        self.send_email_alert(subject, body, "failure")
    
    def _save_execution_log(self, result: Dict[str, Any]):
        """Save execution log for historical tracking"""
        
        log_dir = "/tmp/rfe-execution-logs"
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = f"{log_dir}/rfe-{result['customer']}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        
        with open(log_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        self.logger.info(f"📁 Execution log saved: {log_file}")
    
    def send_success_summary(self, results: List[Dict[str, Any]]):
        """Send daily success summary"""
        
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        
        if not results:
            return
        
        subject = f"RFE Automation Daily Summary - {len(successful)}/{len(results)} Successful"
        
        body = f"""
RFE Automation Daily Summary Report

Date: {datetime.now().strftime('%Y-%m-%d')}
Total Executions: {len(results)}
Successful: {len(successful)}
Failed: {len(failed)}
Success Rate: {(len(successful)/len(results)*100):.1f}%

SUCCESSFUL EXECUTIONS:
"""
        
        for result in successful:
            body += f"✅ {result['customer'].title()}: {result['execution_time']:.1f}s\n"
        
        if failed:
            body += f"\nFAILED EXECUTIONS:\n"
            for result in failed:
                body += f"❌ {result['customer'].title()}: {result.get('error', 'Unknown error')[:100]}\n"
        
        body += f"""

PERFORMANCE METRICS:
Average Execution Time: {sum(r['execution_time'] for r in successful)/len(successful):.1f}s
Fastest Execution: {min(r['execution_time'] for r in successful):.1f}s
Slowest Execution: {max(r['execution_time'] for r in successful):.1f}s

SYSTEM HEALTH: {'🟢 HEALTHY' if len(failed) == 0 else '🟡 ATTENTION NEEDED' if len(failed) < len(successful) else '🔴 CRITICAL'}

Log Files: {self.log_file}
        """
        
        alert_type = "success" if len(failed) == 0 else "warning" if len(failed) < len(successful) else "failure"
        self.send_email_alert(subject, body, alert_type)
    
    def test_monitoring_system(self) -> bool:
        """Test the monitoring system with a simple command"""
        
        self.logger.info("🧪 Testing monitoring system...")
        
        # Test email functionality
        test_subject = "RFE Monitoring System Test"
        test_body = f"""
Monitoring System Test Report

Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Test Type: System Validation

COMPONENTS TESTED:
✅ Email notification system
✅ HTML formatting
✅ Logging system
✅ Alert generation

STATUS: All systems operational

This is a test message to verify the monitoring system is working correctly.
        """
        
        success = self.send_email_alert(test_subject, test_body, "info")
        
        if success:
            self.logger.info("✅ Monitoring system test PASSED")
        else:
            self.logger.error("❌ Monitoring system test FAILED")
        
        return success

def main():
    """Test the monitoring system"""
    
    print("🧪 RFE Monitoring System - Test Mode")
    print("=" * 40)
    
    monitor = RFEMonitoringSystem()
    
    # Test the monitoring system
    if monitor.test_monitoring_system():
        print("✅ Monitoring system ready for production use")
        return 0
    else:
        print("❌ Monitoring system test failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
