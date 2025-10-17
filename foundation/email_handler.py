"""
Email Delivery System for RFE Tools

Unified email handler for all TAM tools:
- SMTP integration
- HTML/plain text support
- Template system
- Attachment support
- Configuration management
"""

import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import Optional, List, Dict
import os


class EmailConfig:
    """Email configuration manager"""
    
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_user = os.getenv('SMTP_USER', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.from_name = os.getenv('SMTP_FROM_NAME', 'Red Hat TAM')
        self.use_tls = os.getenv('SMTP_USE_TLS', 'true').lower() == 'true'
        
        # Load from config file if available
        self._load_from_config()
    
    def _load_from_config(self):
        """Load configuration from file"""
        config_locations = [
            Path.home() / ".config" / "rfe-automation" / "email.conf",
            Path.home() / ".config" / "pai" / "email.conf",
        ]
        
        for config_file in config_locations:
            if config_file.exists():
                try:
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                        self.smtp_server = config.get('smtp_server', self.smtp_server)
                        self.smtp_port = config.get('smtp_port', self.smtp_port)
                        self.smtp_user = config.get('smtp_user', self.smtp_user)
                        self.smtp_password = config.get('smtp_password', self.smtp_password)
                        self.from_name = config.get('from_name', self.from_name)
                        self.use_tls = config.get('use_tls', self.use_tls)
                        break
                except Exception:
                    continue
    
    def is_configured(self) -> bool:
        """Check if email is properly configured"""
        return bool(self.smtp_server and self.smtp_user and self.smtp_password)


class EmailHandler:
    """Unified email handler for RFE tools"""
    
    def __init__(self):
        self.config = EmailConfig()
    
    def send(
        self,
        to_email: str,
        subject: str,
        body: str,
        from_email: Optional[str] = None,
        cc: Optional[List[str]] = None,
        attachments: Optional[List[Path]] = None,
        html: bool = False
    ) -> bool:
        """
        Send email via SMTP
        
        Args:
            to_email: Recipient email address
            subject: Email subject line
            body: Email body (plain text or HTML)
            from_email: Sender email (defaults to config)
            cc: List of CC recipients
            attachments: List of file paths to attach
            html: Whether body is HTML (default: False)
        
        Returns:
            True if sent successfully, False otherwise
        """
        
        if not self.config.is_configured():
            print("❌ Email not configured")
            print("   Set SMTP_* environment variables or create ~/.config/rfe-automation/email.conf")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = f"{self.config.from_name} <{from_email or self.config.smtp_user}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            if cc:
                msg['Cc'] = ', '.join(cc)
            
            # Add body
            if html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            # Add attachments
            if attachments:
                for file_path in attachments:
                    if file_path.exists():
                        with open(file_path, 'rb') as f:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(f.read())
                        
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename={file_path.name}'
                        )
                        msg.attach(part)
            
            # Send email
            recipients = [to_email]
            if cc:
                recipients.extend(cc)
            
            with smtplib.SMTP(self.config.smtp_server, self.config.smtp_port) as server:
                if self.config.use_tls:
                    server.starttls()
                
                server.login(self.config.smtp_user, self.config.smtp_password)
                server.sendmail(
                    from_email or self.config.smtp_user,
                    recipients,
                    msg.as_string()
                )
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return False
    
    def send_agenda(
        self,
        customer: str,
        to_email: str,
        agenda_file: Path,
        from_email: Optional[str] = None
    ) -> bool:
        """Send TAM call agenda"""
        
        if not agenda_file.exists():
            print(f"❌ Agenda file not found: {agenda_file}")
            return False
        
        with open(agenda_file, 'r') as f:
            body = f.read()
        
        # Convert markdown to HTML for better email formatting
        html_body = self._markdown_to_simple_html(body)
        
        subject = f"TAM Call Agenda - {customer.upper()}"
        
        return self.send(
            to_email=to_email,
            subject=subject,
            body=html_body,
            from_email=from_email,
            html=True
        )
    
    def send_backlog_report(
        self,
        customer: str,
        to_email: str,
        report_file: Path,
        from_email: Optional[str] = None
    ) -> bool:
        """Send backlog cleanup report"""
        
        if not report_file.exists():
            print(f"❌ Report file not found: {report_file}")
            return False
        
        with open(report_file, 'r') as f:
            body = f.read()
        
        html_body = self._markdown_to_simple_html(body)
        
        subject = f"Backlog Cleanup Report - {customer.upper()}"
        
        return self.send(
            to_email=to_email,
            subject=subject,
            body=html_body,
            from_email=from_email,
            html=True
        )
    
    def send_t3_recommendations(
        self,
        customer: str,
        to_email: str,
        report_file: Path,
        from_email: Optional[str] = None
    ) -> bool:
        """Send T3 article recommendations"""
        
        if not report_file.exists():
            print(f"❌ Report file not found: {report_file}")
            return False
        
        with open(report_file, 'r') as f:
            body = f.read()
        
        html_body = self._markdown_to_simple_html(body)
        
        subject = f"T3 Article Recommendations - {customer.upper()}"
        
        return self.send(
            to_email=to_email,
            subject=subject,
            body=html_body,
            from_email=from_email,
            html=True
        )
    
    def send_coverage_announcement(
        self,
        customer: str,
        to_email: str,
        announcement_file: Path,
        briefing_file: Optional[Path] = None,
        from_email: Optional[str] = None
    ) -> bool:
        """Send coverage announcement (optionally with backup briefing)"""
        
        if not announcement_file.exists():
            print(f"❌ Announcement file not found: {announcement_file}")
            return False
        
        with open(announcement_file, 'r') as f:
            body = f.read()
        
        html_body = self._markdown_to_simple_html(body)
        
        subject = "Red Hat TAM Out of Office Notification"
        if customer:
            subject += f" - {customer.upper()}"
        
        attachments = []
        if briefing_file and briefing_file.exists():
            attachments.append(briefing_file)
        
        return self.send(
            to_email=to_email,
            subject=subject,
            body=html_body,
            from_email=from_email,
            attachments=attachments if attachments else None,
            html=True
        )
    
    def _markdown_to_simple_html(self, markdown: str) -> str:
        """
        Convert markdown to simple HTML for email
        (Basic implementation - can be enhanced with markdown library)
        """
        
        html = "<html><head><style>"
        html += """
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 { color: #cc0000; border-bottom: 2px solid #cc0000; padding-bottom: 10px; }
        h2 { color: #cc0000; margin-top: 30px; }
        h3 { color: #555; margin-top: 20px; }
        .critical { background-color: #ffeeee; padding: 10px; margin: 10px 0; border-left: 4px solid #cc0000; }
        .warning { background-color: #fff3cd; padding: 10px; margin: 10px 0; border-left: 4px solid #ffc107; }
        .success { background-color: #d4edda; padding: 10px; margin: 10px 0; border-left: 4px solid #28a745; }
        code { background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
        pre { background-color: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }
        ul, ol { margin-left: 20px; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #cc0000; color: white; }
        hr { border: 0; height: 1px; background: #ddd; margin: 30px 0; }
        """
        html += "</style></head><body>"
        
        # Simple markdown conversions
        lines = markdown.split('\n')
        in_code_block = False
        
        for line in lines:
            # Code blocks
            if line.startswith('```'):
                if in_code_block:
                    html += "</pre>"
                    in_code_block = False
                else:
                    html += "<pre>"
                    in_code_block = True
                continue
            
            if in_code_block:
                html += line + '\n'
                continue
            
            # Headers
            if line.startswith('# '):
                html += f"<h1>{line[2:]}</h1>"
            elif line.startswith('## '):
                html += f"<h2>{line[3:]}</h2>"
            elif line.startswith('### '):
                html += f"<h3>{line[4:]}</h3>"
            # Horizontal rule
            elif line.strip() == '---':
                html += "<hr>"
            # Bold
            elif '**' in line:
                line = line.replace('**', '<strong>', 1).replace('**', '</strong>', 1)
                html += f"<p>{line}</p>"
            # List items
            elif line.startswith('- ') or line.startswith('* '):
                html += f"<li>{line[2:]}</li>"
            # Numbered lists
            elif len(line) > 2 and line[0].isdigit() and line[1] == '.':
                html += f"<li>{line[3:]}</li>"
            # Empty line
            elif line.strip() == '':
                html += "<br>"
            # Regular paragraph
            else:
                html += f"<p>{line}</p>"
        
        html += "</body></html>"
        
        return html


# Convenience function for direct imports
_handler = None

def send_email(
    to_email: str,
    subject: str,
    body: str,
    from_email: Optional[str] = None,
    cc: Optional[List[str]] = None,
    attachments: Optional[List[Path]] = None,
    html: bool = False
) -> bool:
    """Send email (convenience function)"""
    global _handler
    if _handler is None:
        _handler = EmailHandler()
    
    return _handler.send(
        to_email=to_email,
        subject=subject,
        body=body,
        from_email=from_email,
        cc=cc,
        attachments=attachments,
        html=html
    )


def get_email_handler() -> EmailHandler:
    """Get email handler instance"""
    global _handler
    if _handler is None:
        _handler = EmailHandler()
    return _handler

