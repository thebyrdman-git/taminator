#!/usr/bin/env python3

"""
Slack Notifier for TAM RFE Report Scheduler
Sends notifications to Slack channels via webhooks
"""

import json
import urllib.request
import urllib.error
from datetime import datetime
from typing import Dict, Any, Optional


class SlackNotifier:
    """Send notifications to Slack"""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    def send_message(self, 
                    title: str,
                    output: str,
                    status: str = "success",
                    duration: float = 0,
                    schedule_name: str = None) -> bool:
        """
        Send a message to Slack
        
        Args:
            title: Message title
            output: Command output or error message
            status: "success" or "failed"
            duration: Execution duration in seconds
            schedule_name: Name of the schedule
        
        Returns:
            bool: True if sent successfully
        """
        emoji = "✅" if status == "success" else "❌"
        color = "good" if status == "success" else "danger"
        
        # Truncate output if too long (Slack has limits)
        max_output_length = 2000
        if len(output) > max_output_length:
            output = output[:max_output_length] + "\n... (truncated)"
        
        # Build Slack message payload
        payload = {
            "attachments": [
                {
                    "color": color,
                    "title": f"{emoji} {title}",
                    "text": f"```{output}```",
                    "fields": [
                        {
                            "title": "Status",
                            "value": status.capitalize(),
                            "short": True
                        },
                        {
                            "title": "Duration",
                            "value": f"{duration:.1f}s",
                            "short": True
                        }
                    ],
                    "footer": "TAM RFE Scheduler",
                    "footer_icon": "https://www.redhat.com/favicon.ico",
                    "ts": int(datetime.now().timestamp())
                }
            ]
        }
        
        if schedule_name:
            payload["attachments"][0]["author_name"] = schedule_name
        
        try:
            request = urllib.request.Request(
                self.webhook_url,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(request, timeout=10) as response:
                return response.status == 200
                
        except urllib.error.HTTPError as e:
            print(f"HTTP Error sending to Slack: {e.code} {e.reason}")
            return False
        except urllib.error.URLError as e:
            print(f"URL Error sending to Slack: {e.reason}")
            return False
        except Exception as e:
            print(f"Error sending to Slack: {e}")
            return False
    
    def send_simple_message(self, text: str) -> bool:
        """Send a simple text message to Slack"""
        payload = {"text": text}
        
        try:
            request = urllib.request.Request(
                self.webhook_url,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(request, timeout=10) as response:
                return response.status == 200
                
        except Exception as e:
            print(f"Error sending simple message to Slack: {e}")
            return False
    
    def send_blocks_message(self, blocks: list) -> bool:
        """Send a Slack message with blocks (advanced formatting)"""
        payload = {"blocks": blocks}
        
        try:
            request = urllib.request.Request(
                self.webhook_url,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(request, timeout=10) as response:
                return response.status == 200
                
        except Exception as e:
            print(f"Error sending blocks message to Slack: {e}")
            return False


def create_success_blocks(schedule_name: str, output: str, duration: float) -> list:
    """Create Slack blocks for success notification"""
    return [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"✅ {schedule_name}",
                "emoji": True
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Status:*\nSuccess"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Duration:*\n{duration:.1f}s"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"```{output[:2000]}```"
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | TAM RFE Scheduler"
                }
            ]
        }
    ]


def create_failure_blocks(schedule_name: str, error: str, duration: float) -> list:
    """Create Slack blocks for failure notification"""
    return [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"❌ {schedule_name}",
                "emoji": True
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Status:*\n⚠️ Failed"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Duration:*\n{duration:.1f}s"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"```{error[:2000]}```"
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | TAM RFE Scheduler"
                }
            ]
        }
    ]


# Example usage
if __name__ == '__main__':
    # Test with a dummy webhook (will fail, just for testing structure)
    webhook_url = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    notifier = SlackNotifier(webhook_url)
    
    # Test success message
    notifier.send_message(
        title="Westpac Weekly Report",
        output="15 cases found\n3 Sev 1, 7 Sev 2, 5 Sev 3",
        status="success",
        duration=2.3,
        schedule_name="westpac-weekly"
    )

