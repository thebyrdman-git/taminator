#!/usr/bin/env python3

"""
Template Engine for TAM RFE Report Scheduler
Renders report templates with dynamic data
"""

import re
from datetime import datetime, timedelta
from typing import Dict, Any


class ReportTemplate:
    """Template rendering engine"""
    
    def __init__(self, template_path: str = None, template_string: str = None):
        if template_path:
            with open(template_path, 'r') as f:
                self.template = f.read()
        elif template_string:
            self.template = template_string
        else:
            raise ValueError("Must provide template_path or template_string")
    
    def render(self, context: Dict[str, Any]) -> str:
        """Render template with context data"""
        result = self.template
        
        # Simple variable substitution: {{variable}}
        for key, value in context.items():
            pattern = r'\{\{' + key + r'\}\}'
            result = re.sub(pattern, str(value), result)
        
        # Handle conditionals: {{#if variable}}content{{/if}}
        result = self._process_conditionals(result, context)
        
        # Handle loops: {{#each items}}content{{/each}}
        result = self._process_loops(result, context)
        
        return result
    
    def _process_conditionals(self, text: str, context: Dict[str, Any]) -> str:
        """Process {{#if variable}}...{{/if}} blocks"""
        pattern = r'\{\{#if\s+(\w+)\}\}(.*?)\{\{/if\}\}'
        
        def replace_conditional(match):
            var_name = match.group(1)
            content = match.group(2)
            value = context.get(var_name, False)
            
            # Check if value is truthy
            if value and value != '0' and value != 'false':
                return content
            return ''
        
        return re.sub(pattern, replace_conditional, text, flags=re.DOTALL)
    
    def _process_loops(self, text: str, context: Dict[str, Any]) -> str:
        """Process {{#each items}}...{{/each}} blocks"""
        pattern = r'\{\{#each\s+(\w+)\}\}(.*?)\{\{/each\}\}'
        
        def replace_loop(match):
            var_name = match.group(1)
            content = match.group(2)
            items = context.get(var_name, [])
            
            if not isinstance(items, list):
                return ''
            
            result = []
            for item in items:
                # Make item properties available in template
                item_context = {**context, **item}
                item_result = content
                for key, value in item_context.items():
                    pattern = r'\{\{' + key + r'\}\}'
                    item_result = re.sub(pattern, str(value), item_result)
                result.append(item_result)
            
            return ''.join(result)
        
        return re.sub(pattern, replace_loop, text, flags=re.DOTALL)


def create_weekly_digest_context(cases_data: str) -> Dict[str, Any]:
    """Create context for weekly digest template"""
    return {
        'week_start': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
        'week_end': datetime.now().strftime('%Y-%m-%d'),
        'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'cases_data': cases_data,
        'total_cases': len(cases_data.split('\n')) if cases_data else 0
    }


def create_executive_brief_context(data: str) -> Dict[str, Any]:
    """Create context for executive brief template"""
    return {
        'report_date': datetime.now().strftime('%B %d, %Y'),
        'content': data,
        'summary': data[:500] + '...' if len(data) > 500 else data
    }


# Built-in templates
WEEKLY_DIGEST_HTML = """
<html>
<head>
<style>
body {
    font-family: 'Segoe UI', Arial, sans-serif;
    margin: 20px;
    background-color: #f5f5f5;
}
.container {
    max-width: 800px;
    margin: 0 auto;
    background-color: white;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 25px;
    border-radius: 8px;
    margin-bottom: 25px;
}
.header h1 {
    margin: 0;
    font-size: 28px;
}
.meta {
    color: rgba(255,255,255,0.9);
    font-size: 14px;
    margin-top: 10px;
}
.stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin-bottom: 25px;
}
.stat-card {
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 6px;
    border-left: 4px solid #667eea;
}
.stat-card h3 {
    margin: 0 0 10px 0;
    color: #667eea;
    font-size: 14px;
    text-transform: uppercase;
}
.stat-card .number {
    font-size: 32px;
    font-weight: bold;
    color: #2d3748;
}
.content {
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 6px;
    font-family: 'Courier New', monospace;
    white-space: pre-wrap;
    font-size: 13px;
    line-height: 1.6;
}
.footer {
    margin-top: 25px;
    padding-top: 20px;
    border-top: 1px solid #e2e8f0;
    color: #718096;
    font-size: 12px;
    text-align: center;
}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>📊 Weekly TAM Digest</h1>
        <div class="meta">
            Week: {{week_start}} to {{week_end}}<br>
            Generated: {{generated_date}}
        </div>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <h3>Total Cases</h3>
            <div class="number">{{total_cases}}</div>
        </div>
    </div>
    
    <h2 style="color: #2d3748; margin-bottom: 15px;">📝 Case Summary</h2>
    <div class="content">{{cases_data}}</div>
    
    <div class="footer">
        Automated by TAM RFE Report Scheduler<br>
        Red Hat Technical Account Management
    </div>
</div>
</body>
</html>
"""

EXECUTIVE_BRIEF_HTML = """
<html>
<head>
<style>
body {
    font-family: 'Segoe UI', Arial, sans-serif;
    margin: 20px;
    background-color: #f5f5f5;
}
.container {
    max-width: 900px;
    margin: 0 auto;
    background-color: white;
    padding: 40px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.header {
    text-align: center;
    border-bottom: 3px solid #cc0000;
    padding-bottom: 20px;
    margin-bottom: 30px;
}
.header h1 {
    color: #cc0000;
    font-size: 32px;
    margin: 0 0 10px 0;
}
.header .date {
    color: #666;
    font-size: 16px;
}
.executive-summary {
    background-color: #fff3cd;
    border-left: 4px solid #ffc107;
    padding: 20px;
    margin-bottom: 25px;
}
.executive-summary h2 {
    margin-top: 0;
    color: #856404;
}
.content {
    line-height: 1.8;
    color: #2d3748;
}
.content pre {
    background-color: #f8f9fa;
    padding: 15px;
    border-radius: 4px;
    overflow-x: auto;
}
.footer {
    margin-top: 40px;
    padding-top: 20px;
    border-top: 2px solid #e2e8f0;
    text-align: center;
    color: #718096;
    font-size: 12px;
}
.redhat-logo {
    color: #cc0000;
    font-weight: bold;
}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>🎯 Executive Brief</h1>
        <div class="date">{{report_date}}</div>
    </div>
    
    <div class="executive-summary">
        <h2>Executive Summary</h2>
        <p>{{summary}}</p>
    </div>
    
    <div class="content">
        <pre>{{content}}</pre>
    </div>
    
    <div class="footer">
        <div class="redhat-logo">RED HAT</div>
        Technical Account Management<br>
        Automated Report • Confidential
    </div>
</div>
</body>
</html>
"""

SLACK_MESSAGE_TEMPLATE = """
{
    "blocks": [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "{{title}}",
                "emoji": true
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Status:*\\n{{status}}"
                },
                {
                    "type": "mrkdwn",
                    "text": "*Duration:*\\n{{duration}}s"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "```{{output}}```"
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "Generated: {{timestamp}} | TAM RFE Scheduler"
                }
            ]
        }
    ]
}
"""

