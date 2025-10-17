"""
Slack Webhook Integration

Enables posting notifications to Slack channels:
- Case alerts (SLA breaches, escalations)
- Agenda summaries
- Backlog reports
- T3 article recommendations
- Coverage announcements

Authentication: Webhook URLs (no OAuth needed for incoming webhooks)
API: Slack Incoming Webhooks

Configuration:
  Environment variables:
    SLACK_WEBHOOK_URL - Primary webhook URL
    SLACK_WEBHOOK_ALERTS - Alert-specific webhook
    SLACK_WEBHOOK_REPORTS - Report-specific webhook
  
  Or config file: ~/.config/rfe-automation/slack.conf
"""

import os
import json
import requests
from pathlib import Path
from typing import Optional, Dict, List, Any
from datetime import datetime


class SlackConfig:
    """Slack configuration manager"""
    def __init__(self):
        # Default webhook (general notifications)
        self.webhook_url = os.getenv('SLACK_WEBHOOK_URL', '')
        
        # Specialized webhooks (optional)
        self.webhook_alerts = os.getenv('SLACK_WEBHOOK_ALERTS', self.webhook_url)
        self.webhook_reports = os.getenv('SLACK_WEBHOOK_REPORTS', self.webhook_url)
        
        self._load_from_config()
    
    def _load_from_config(self):
        """Load configuration from file"""
        config_locations = [
            Path.home() / ".config" / "rfe-automation" / "slack.conf",
            Path.home() / ".config" / "pai" / "slack.conf",
        ]
        
        for config_file in config_locations:
            if config_file.exists():
                try:
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                        self.webhook_url = config.get('webhook_url', self.webhook_url)
                        self.webhook_alerts = config.get('webhook_alerts', self.webhook_alerts)
                        self.webhook_reports = config.get('webhook_reports', self.webhook_reports)
                    print(f"  ✅ Loaded Slack config from {config_file}")
                    break
                except Exception as e:
                    print(f"  ⚠️  Error loading Slack config from {config_file}: {e}")
    
    def is_configured(self) -> bool:
        """Check if at least the default webhook is configured"""
        return bool(self.webhook_url)


_slack_handler_instance = None


class SlackHandler:
    """Handles interactions with Slack via incoming webhooks."""
    
    def __init__(self):
        self.config = SlackConfig()
    
    def _post_to_webhook(self, webhook_url: str, payload: Dict[str, Any]) -> bool:
        """Post a message to a Slack webhook"""
        if not webhook_url:
            print("❌ Slack webhook URL not configured")
            return False
        
        try:
            response = requests.post(
                webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to post to Slack: {e}")
            return False
    
    def post_simple_message(self, text: str, webhook_type: str = "default") -> bool:
        """Post a simple text message to Slack"""
        if not self.config.is_configured():
            print("❌ Slack not configured")
            print("   Set SLACK_WEBHOOK_URL environment variable or create slack.conf")
            return False
        
        webhook_url = {
            "default": self.config.webhook_url,
            "alerts": self.config.webhook_alerts,
            "reports": self.config.webhook_reports
        }.get(webhook_type, self.config.webhook_url)
        
        payload = {"text": text}
        return self._post_to_webhook(webhook_url, payload)
    
    def post_agenda_notification(self, customer: str, tam_name: str, critical_count: int, trend_count: int) -> bool:
        """Post TAM agenda notification to Slack"""
        if not self.config.is_configured():
            return False
        
        payload = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"📋 TAM Agenda Generated - {customer}",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*TAM:*\n{tam_name}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Date:*\n{datetime.now().strftime('%B %d, %Y')}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Critical Items:*\n{critical_count}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Trends Detected:*\n{trend_count}"
                        }
                    ]
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": "Posted automatically by Taminator"
                        }
                    ]
                }
            ]
        }
        
        return self._post_to_webhook(self.config.webhook_reports, payload)
    
    def post_backlog_alert(self, customer: str, total_cases: int, closeable: int, breached: int, health_score: int) -> bool:
        """Post backlog cleanup alert to Slack"""
        if not self.config.is_configured():
            return False
        
        color = "good" if health_score >= 70 else "warning" if health_score >= 50 else "danger"
        
        payload = {
            "attachments": [
                {
                    "color": color,
                    "blocks": [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": f"🧹 Backlog Report - {customer}",
                                "emoji": True
                            }
                        },
                        {
                            "type": "section",
                            "fields": [
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Total Cases:*\n{total_cases}"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Closeable:*\n{closeable}"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": f"*SLA Breached:*\n{breached}"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Health Score:*\n{health_score}/100"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        return self._post_to_webhook(self.config.webhook_reports, payload)
    
    def post_sla_breach_alert(self, customer: str, case_number: str, case_summary: str, hours_breached: int) -> bool:
        """Post SLA breach alert to Slack"""
        if not self.config.is_configured():
            return False
        
        payload = {
            "attachments": [
                {
                    "color": "danger",
                    "blocks": [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": "🚨 SLA BREACH ALERT",
                                "emoji": True
                            }
                        },
                        {
                            "type": "section",
                            "fields": [
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Customer:*\n{customer}"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Case:*\n{case_number}"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Breached By:*\n{hours_breached} hours"
                                }
                            ]
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"*Summary:*\n{case_summary}"
                            }
                        },
                        {
                            "type": "context",
                            "elements": [
                                {
                                    "type": "mrkdwn",
                                    "text": "⚡ Immediate action required"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        return self._post_to_webhook(self.config.webhook_alerts, payload)
    
    def post_t3_recommendations(self, customer: str, article_count: int, top_article: Optional[Dict] = None) -> bool:
        """Post T3 article recommendations to Slack"""
        if not self.config.is_configured():
            return False
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"📰 T3 Blog Recommendations - {customer}",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Found {article_count} relevant articles for sharing with customer"
                }
            }
        ]
        
        if top_article:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Top Recommendation:*\n{top_article.get('title', 'Untitled')}\n{top_article.get('url', '#')}"
                }
            })
        
        payload = {"blocks": blocks}
        return self._post_to_webhook(self.config.webhook_reports, payload)
    
    def post_coverage_announcement(self, tam_name: str, backup_name: str, start_date: str, end_date: str, customer: Optional[str] = None) -> bool:
        """Post TAM coverage announcement to Slack"""
        if not self.config.is_configured():
            return False
        
        customer_text = f" - {customer}" if customer else ""
        
        payload = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"📢 TAM Coverage Notification{customer_text}",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Primary TAM:*\n{tam_name}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Backup TAM:*\n{backup_name}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Out of Office:*\n{start_date} to {end_date}"
                        }
                    ]
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": "All critical issues will be monitored during this period"
                        }
                    ]
                }
            ]
        }
        
        return self._post_to_webhook(self.config.webhook_reports, payload)


def get_slack_handler() -> SlackHandler:
    """Get singleton Slack handler instance"""
    global _slack_handler_instance
    if _slack_handler_instance is None:
        _slack_handler_instance = SlackHandler()
    return _slack_handler_instance

