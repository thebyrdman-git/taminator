#!/usr/bin/env python3
"""
PAI GitLab Webhook Receiver
Handles GitLab issue notifications for RFE & Bug Tracker
Part of the Personal AI Infrastructure (PAI)
"""

import os
import json
import logging
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from flask import Flask, request, jsonify
from logging.handlers import RotatingFileHandler

# Configuration
LOG_DIR = Path("/app/logs")
LOG_FILE = LOG_DIR / "gitlab-webhook.log"
EVENTS_LOG = LOG_DIR / "gitlab-events.jsonl"
WEBHOOK_PORT = int(os.environ.get("GITLAB_WEBHOOK_PORT", 3002))
WEBHOOK_SECRET = os.environ.get("GITLAB_WEBHOOK_SECRET", "")
EMAIL_TO = os.environ.get("GITLAB_WEBHOOK_EMAIL", "jbyrd@redhat.com")
EMAIL_FROM = os.environ.get("GITLAB_WEBHOOK_FROM", "hatter@miraclemax")
SMTP_SERVER = os.environ.get("SMTP_SERVER", "localhost")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 25))

# Ensure directories exist
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Flask app
app = Flask(__name__)

# Configure logging
handler = RotatingFileHandler(LOG_FILE, maxBytes=10*1024*1024, backupCount=5)
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
))
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)


def verify_gitlab_token(request_headers):
    """Verify GitLab webhook secret token"""
    if not WEBHOOK_SECRET:
        return True  # No secret configured, allow all
    
    token = request_headers.get("X-Gitlab-Token", "")
    return token == WEBHOOK_SECRET


def log_event(event_type, event_data):
    """Log event to JSONL file for audit trail"""
    try:
        with open(EVENTS_LOG, "a") as f:
            event_record = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "type": event_type,
                "data": event_data
            }
            f.write(json.dumps(event_record) + "\n")
    except Exception as e:
        app.logger.error(f"Failed to log event: {e}")


def send_email(subject, body_text, body_html=None):
    """Send email notification via SMTP"""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = EMAIL_FROM
        msg["To"] = EMAIL_TO
        
        # Attach plain text
        msg.attach(MIMEText(body_text, "plain"))
        
        # Attach HTML if provided
        if body_html:
            msg.attach(MIMEText(body_html, "html"))
        
        # Send via SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.send_message(msg)
        
        app.logger.info(f"Email sent successfully to {EMAIL_TO}")
        return True
    except Exception as e:
        app.logger.error(f"Failed to send email: {e}")
        return False


def format_issue_notification(issue_data):
    """Format issue data into email notification"""
    issue = issue_data.get("object_attributes", {})
    user = issue_data.get("user", {})
    project = issue_data.get("project", {})
    
    # Extract key information
    issue_id = issue.get("iid", "Unknown")
    title = issue.get("title", "No title")
    description = issue.get("description", "No description provided")
    author = user.get("name", "Unknown")
    author_username = user.get("username", "unknown")
    url = issue.get("url", "")
    state = issue.get("state", "unknown")
    labels = issue.get("labels", [])
    created_at = issue.get("created_at", "")
    project_name = project.get("name", "Unknown Project")
    
    # Format labels
    label_names = [label.get("title", "") for label in labels] if isinstance(labels, list) else []
    labels_str = ", ".join(label_names) if label_names else "None"
    
    # Plain text body
    text_body = f"""New Issue Filed: {project_name}

Issue #{issue_id}: {title}

Author: {author} (@{author_username})
State: {state}
Labels: {labels_str}
Created: {created_at}

Description:
{description}

View Issue: {url}

---
This notification was sent by PAI GitLab Webhook Receiver
Running on miraclemax infrastructure
"""
    
    # HTML body
    html_body = f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #dc143c; color: white; padding: 15px; border-radius: 5px 5px 0 0; }}
        .content {{ background: #f9f9f9; padding: 20px; border: 1px solid #ddd; border-top: none; border-radius: 0 0 5px 5px; }}
        .issue-title {{ font-size: 18px; font-weight: bold; margin: 10px 0; }}
        .meta {{ color: #666; font-size: 14px; margin: 5px 0; }}
        .description {{ background: white; padding: 15px; border-left: 3px solid #dc143c; margin: 15px 0; white-space: pre-wrap; }}
        .button {{ display: inline-block; background: #dc143c; color: white; padding: 10px 20px; text-decoration: none; border-radius: 3px; margin: 15px 0; }}
        .footer {{ text-align: center; color: #999; font-size: 12px; margin-top: 20px; }}
        .label {{ display: inline-block; background: #eee; padding: 2px 8px; border-radius: 3px; font-size: 12px; margin: 2px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>🔴 New Issue Filed</h2>
            <p style="margin: 0;">{project_name}</p>
        </div>
        <div class="content">
            <div class="issue-title">Issue #{issue_id}: {title}</div>
            <div class="meta">
                <strong>Author:</strong> {author} (@{author_username})<br>
                <strong>State:</strong> {state}<br>
                <strong>Created:</strong> {created_at}<br>
                <strong>Labels:</strong> {' '.join([f'<span class="label">{label}</span>' for label in label_names]) if label_names else 'None'}
            </div>
            <div class="description">
                <strong>Description:</strong><br><br>
                {description}
            </div>
            <a href="{url}" class="button">View Issue on GitLab</a>
        </div>
        <div class="footer">
            This notification was sent by PAI GitLab Webhook Receiver<br>
            Hatter - Red Hat Digital Assistant
        </div>
    </div>
</body>
</html>"""
    
    subject = f"[GitLab] New Issue #{issue_id}: {title}"
    
    return subject, text_body, html_body


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "pai-gitlab-webhook-receiver",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })


@app.route("/webhook/gitlab", methods=["POST"])
def gitlab_webhook():
    """Handle GitLab webhook events"""
    try:
        # Verify token
        if not verify_gitlab_token(request.headers):
            app.logger.warning("Unauthorized webhook request - invalid token")
            return jsonify({"error": "Unauthorized"}), 401
        
        # Get event type
        event_type = request.headers.get("X-Gitlab-Event", "Unknown")
        
        # Parse payload
        payload = request.json
        if not payload:
            return jsonify({"error": "No payload"}), 400
        
        app.logger.info(f"Received GitLab event: {event_type}")
        
        # Log event for audit
        log_event(event_type, {
            "event": event_type,
            "summary": payload.get("object_attributes", {}).get("title", "No title") if "object_attributes" in payload else "Unknown"
        })
        
        # Handle Issue events
        if event_type == "Issue Hook":
            object_attributes = payload.get("object_attributes", {})
            action = object_attributes.get("action", "unknown")
            
            # Only send email for new issues
            if action == "open":
                subject, text_body, html_body = format_issue_notification(payload)
                
                if send_email(subject, text_body, html_body):
                    app.logger.info(f"Issue notification sent: {subject}")
                    return jsonify({
                        "status": "success",
                        "message": "Issue notification sent",
                        "event": event_type
                    }), 200
                else:
                    return jsonify({
                        "status": "error",
                        "message": "Failed to send notification"
                    }), 500
            else:
                app.logger.info(f"Ignoring issue action: {action}")
                return jsonify({
                    "status": "ignored",
                    "message": f"Action '{action}' not configured for notifications"
                }), 200
        
        # Handle other events (log only, no notification)
        else:
            app.logger.info(f"Event '{event_type}' logged but not configured for notifications")
            return jsonify({
                "status": "logged",
                "message": f"Event '{event_type}' received and logged"
            }), 200
            
    except Exception as e:
        app.logger.error(f"Error processing webhook: {e}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/stats", methods=["GET"])
def stats():
    """Return statistics about processed webhooks"""
    try:
        event_counts = {}
        total_events = 0
        
        if EVENTS_LOG.exists():
            with open(EVENTS_LOG, "r") as f:
                for line in f:
                    try:
                        event = json.loads(line)
                        event_type = event.get("type", "Unknown")
                        event_counts[event_type] = event_counts.get(event_type, 0) + 1
                        total_events += 1
                    except json.JSONDecodeError:
                        continue
        
        return jsonify({
            "total_events": total_events,
            "event_counts": event_counts,
            "log_file": str(EVENTS_LOG)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def index():
    """Root endpoint with service information"""
    return jsonify({
        "service": "PAI GitLab Webhook Receiver",
        "version": "1.0.0",
        "endpoints": {
            "/health": "Health check",
            "/webhook/gitlab": "GitLab webhook handler (POST only)",
            "/stats": "Event statistics"
        },
        "configuration": {
            "port": WEBHOOK_PORT,
            "email_to": EMAIL_TO,
            "email_from": EMAIL_FROM,
            "smtp_server": SMTP_SERVER,
            "smtp_port": SMTP_PORT,
            "secret_configured": bool(WEBHOOK_SECRET)
        }
    })


if __name__ == "__main__":
    app.logger.info(f"Starting PAI GitLab Webhook Receiver on port {WEBHOOK_PORT}")
    app.logger.info(f"Email notifications will be sent to: {EMAIL_TO}")
    app.logger.info(f"Webhook secret configured: {bool(WEBHOOK_SECRET)}")
    
    # Run Flask app
    app.run(
        host="0.0.0.0",
        port=WEBHOOK_PORT,
        debug=False
    )

