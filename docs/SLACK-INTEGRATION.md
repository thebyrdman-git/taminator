# Slack Integration for Taminator

## Overview

Taminator integrates with Slack via **incoming webhooks** to provide real-time notifications for TAM operations:

- **Agenda Summaries:** Daily TAM call agenda highlights
- **Backlog Alerts:** Health scores and cleanup recommendations
- **SLA Breach Alerts:** Immediate notifications for breached cases
- **T3 Recommendations:** New article suggestions for customers
- **Coverage Announcements:** Out-of-office and backup TAM notifications

## Setup

### 1. Create Slack Incoming Webhooks

Go to your Slack workspace and create incoming webhooks:

1. Visit: https://api.slack.com/messaging/webhooks
2. Click "Create New App" → "From scratch"
3. Name: "Taminator"
4. Choose your workspace
5. Click "Incoming Webhooks" → Toggle "Activate Incoming Webhooks" to **On**
6. Click "Add New Webhook to Workspace"
7. Select channel (e.g., `#tam-notifications`)
8. Copy the webhook URL (looks like: `https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX`)

**Optional:** Create separate webhooks for alerts vs reports:
- `#tam-alerts` - Critical notifications (SLA breaches, escalations)
- `#tam-reports` - Daily reports (agendas, backlog, T3)

### 2. Configure Taminator

**Option A: Environment Variables**

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

# Optional: Separate webhooks for different notification types
export SLACK_WEBHOOK_ALERTS="https://hooks.slack.com/services/YOUR/ALERTS/WEBHOOK"
export SLACK_WEBHOOK_REPORTS="https://hooks.slack.com/services/YOUR/REPORTS/WEBHOOK"
```

**Option B: Configuration File**

Create `~/.config/rfe-automation/slack.conf`:

```json
{
  "webhook_url": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
  "webhook_alerts": "https://hooks.slack.com/services/YOUR/ALERTS/WEBHOOK",
  "webhook_reports": "https://hooks.slack.com/services/YOUR/REPORTS/WEBHOOK"
}
```

## Usage

### 1. TAM Agenda Notifications

```bash
tam-generate-agenda --customer jpmc --slack
```

**Slack Message:**
```
📋 TAM Agenda Generated - JPMC

TAM: Jim Byrd
Date: October 17, 2025
Critical Items: 3
Trends Detected: 2

Posted automatically by Taminator
```

### 2. Backlog Cleanup Alerts

```bash
tam-backlog-cleanup --customer jpmc --slack
```

**Slack Message (Good Health):**
```
🧹 Backlog Report - JPMC

Total Cases: 15
Closeable: 5
SLA Breached: 0
Health Score: 85/100
```

**Slack Message (Poor Health - RED):**
```
🧹 Backlog Report - JPMC  ⚠️

Total Cases: 32
Closeable: 12
SLA Breached: 3
Health Score: 42/100
```

### 3. SLA Breach Alerts (Automated)

When Taminator detects an SLA breach:

```
🚨 SLA BREACH ALERT

Customer: JPMC
Case: 04280915
Breached By: 6 hours

Summary: AAP authentication failures in production

⚡ Immediate action required
```

### 4. T3 Article Recommendations

```bash
tam-t3-reader --customer jpmc --recommend --slack
```

**Slack Message:**
```
📰 T3 Blog Recommendations - JPMC

Found 5 relevant articles for sharing with customer

Top Recommendation:
Optimizing Ansible Automation Platform 2.6 Performance
https://access.redhat.com/articles/t3-aap-26-performance
```

### 5. Coverage Announcements

```bash
tam-coverage \
  --tam "Jim Byrd" \
  --tam-email "jbyrd@redhat.com" \
  --backup "Sarah Johnson" \
  --backup-email "sjohnson@redhat.com" \
  --start "2025-10-20" \
  --end "2025-10-25" \
  --customer jpmc \
  --slack
```

**Slack Message:**
```
📢 TAM Coverage Notification - JPMC

Primary TAM: Jim Byrd
Backup TAM: Sarah Johnson
Out of Office: 2025-10-20 to 2025-10-25

All critical issues will be monitored during this period
```

## Integration with Scheduler

Enable automatic Slack notifications via the scheduler:

**Add to schedule configuration:**

```yaml
schedules:
  - name: "Daily JPMC Agenda (with Slack)"
    customer: "jpmc"
    report_type: "agenda"
    frequency: "daily"
    time: "08:00"
    email_to: "jbyrd@redhat.com"
    slack_notify: true  # ← Enable Slack
    
  - name: "Weekly Backlog Cleanup (with Slack alerts)"
    customer: "jpmc"
    report_type: "backlog"
    frequency: "weekly"
    day_of_week: "friday"
    time: "16:00"
    email_to: "jbyrd@redhat.com"
    slack_notify: true  # ← Enable Slack
```

## Channel Recommendations

### Single Workspace
- `#tam-operations` - All Taminator notifications

### Multi-Channel Setup
- `#tam-alerts` - SLA breaches, escalations (high priority)
- `#tam-reports` - Daily agendas, backlog summaries (informational)
- `#tam-articles` - T3 recommendations, knowledge sharing

### Customer-Specific Channels
- `#jpmc-tam` - JPMC-specific notifications
- `#westpac-tam` - Westpac-specific notifications

(Requires separate webhook per customer)

## Formatting

Slack messages use **Block Kit** for rich formatting:
- **Headers** for message titles
- **Fields** for structured data
- **Color coding** for status (green/yellow/red)
- **Context elements** for metadata

## Security Best Practices

1. **Webhook URLs are secrets** - Do NOT commit to Git
2. **Use separate webhooks** for production vs testing
3. **Rotate webhooks** if accidentally exposed
4. **Limit permissions** - Webhooks can only post, not read
5. **Verify origin** - Slack webhook URLs always start with `https://hooks.slack.com/services/`

## Testing

Test your Slack integration:

```bash
# Test with a simple message
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Test from Taminator"}' \
  YOUR_WEBHOOK_URL

# Test with Taminator
tam-generate-agenda --customer test --slack --print
```

## Troubleshooting

### "Slack not configured"
- Check `SLACK_WEBHOOK_URL` is set
- Verify `~/.config/rfe-automation/slack.conf` exists and is valid JSON

### "Failed to post to Slack: 404"
- Webhook URL is invalid or has been revoked
- Regenerate webhook in Slack app settings

### "Failed to post to Slack: Invalid payload"
- Check Taminator logs for payload details
- Verify JSON structure in Slack Block Kit Builder

### "Messages not appearing"
- Check the correct channel was selected when creating webhook
- Verify webhook is still active in Slack app settings
- Check Slack workspace permissions

## Advanced: Programmatic Usage

```python
from foundation.slack_handler import get_slack_handler

handler = get_slack_handler()

# Simple message
handler.post_simple_message("Hello from Taminator!", webhook_type="reports")

# SLA breach alert
handler.post_sla_breach_alert(
    customer="JPMC",
    case_number="04280915",
    case_summary="Production authentication failures",
    hours_breached=6
)

# Custom message with blocks
import requests
webhook_url = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
requests.post(webhook_url, json={
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Custom *formatted* message"
            }
        }
    ]
})
```

## References

- Slack Incoming Webhooks: https://api.slack.com/messaging/webhooks
- Block Kit Builder: https://app.slack.com/block-kit-builder
- Message Formatting: https://api.slack.com/reference/surfaces/formatting

---

*Taminator - "I'll be back" with Slack notifications* 🤖📢

