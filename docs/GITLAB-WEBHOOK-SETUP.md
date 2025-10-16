# GitLab Webhook Email Notifications Setup

## Overview

Get email notifications when users file issues against your GitLab project:
**https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation**

This system uses a local webhook receiver that listens for GitLab events and sends formatted email notifications.

## Architecture

```
GitLab Issue Created
    ↓
GitLab Webhook (HTTP POST)
    ↓
PAI Webhook Receiver (Flask/Python)
    ↓
Email Notification (SMTP)
    ↓
Your Inbox
```

## Installation

### 1. Install Python Dependencies

```bash
pip3 install --user flask
```

### 2. Configure Environment (Optional)

Create a configuration file at `~/.config/pai/gitlab-webhook.env`:

```bash
# Port for webhook receiver (default: 3002)
export GITLAB_WEBHOOK_PORT=3002

# Email address to receive notifications
export GITLAB_WEBHOOK_EMAIL=jbyrd@redhat.com

# From address for emails
export GITLAB_WEBHOOK_FROM=hatter@localhost

# SMTP configuration
export SMTP_SERVER=localhost
export SMTP_PORT=25

# Optional: Webhook secret for security
export GITLAB_WEBHOOK_SECRET=your-secret-token-here
```

Load configuration:
```bash
source ~/.config/pai/gitlab-webhook.env
```

### 3. Start Webhook Receiver

**Option A: Manual Start (Testing)**
```bash
pai-gitlab-webhook start
```

**Option B: Systemd Service (Production)**

Install systemd service:
```bash
# Copy service file
mkdir -p ~/.config/systemd/user/
cp ~/pai/systemd/pai-gitlab-webhook.service ~/.config/systemd/user/

# Edit service file to customize environment variables (optional)
nano ~/.config/systemd/user/pai-gitlab-webhook.service

# Enable and start service
systemctl --user daemon-reload
systemctl --user enable pai-gitlab-webhook.service
systemctl --user start pai-gitlab-webhook.service

# Check status
systemctl --user status pai-gitlab-webhook.service
```

Make sure systemd user services start on boot:
```bash
loginctl enable-linger $USER
```

## GitLab Configuration

### 1. Access Webhook Settings

1. Navigate to your GitLab project: https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation
2. Go to **Settings** → **Webhooks**

### 2. Add Webhook

Configure the webhook with these settings:

| Field | Value |
|-------|-------|
| **URL** | `http://<your-hostname>:3002/webhook/gitlab` |
| **Secret Token** | (Optional) Match `GITLAB_WEBHOOK_SECRET` if configured |
| **Trigger** | ✅ Issues events |
| **SSL verification** | ❌ Disable (unless you have SSL configured) |

Find your hostname:
```bash
hostname -f
```

Example URL: `http://workstation.example.com:3002/webhook/gitlab`

### 3. Test Webhook

Click **Test** → **Issues events** in GitLab webhook settings.

You should see:
- HTTP 200 response in GitLab
- Email notification in your inbox
- Log entry in `~/.config/pai/logs/gitlab-webhook.log`

## Usage

### Check Status
```bash
pai-gitlab-webhook status
```

### View Logs
```bash
pai-gitlab-webhook logs

# Show last 100 lines
pai-gitlab-webhook logs 100
```

### Test Health
```bash
pai-gitlab-webhook test
```

### Restart Service
```bash
pai-gitlab-webhook restart
```

### Stop Service
```bash
pai-gitlab-webhook stop
```

## Email Format

When a new issue is created, you'll receive an email with:

- **Subject:** `[GitLab] New Issue #123: Issue Title`
- **Content:**
  - Issue number and title
  - Author name and username
  - State and labels
  - Full description
  - Direct link to issue

The email is formatted in both plain text and HTML for compatibility.

## Firewall Configuration

If your webhook receiver is on a different machine than GitLab, ensure port 3002 is accessible:

```bash
# Fedora/RHEL firewalld
sudo firewall-cmd --add-port=3002/tcp --permanent
sudo firewall-cmd --reload

# Or use specific zone
sudo firewall-cmd --zone=public --add-port=3002/tcp --permanent
sudo firewall-cmd --reload
```

## Security Considerations

### 1. Webhook Secret Token

**Recommended:** Set a secret token to verify webhook authenticity:

```bash
export GITLAB_WEBHOOK_SECRET="$(openssl rand -hex 32)"
echo "GITLAB_WEBHOOK_SECRET=$GITLAB_WEBHOOK_SECRET" >> ~/.config/pai/gitlab-webhook.env
```

Add this token to GitLab webhook configuration.

### 2. Network Access

- **Internal Network Only:** Webhook receiver should only be accessible from GitLab server
- **No Public Internet:** Don't expose port 3002 to the internet
- **VPN/Firewall:** Restrict access to Red Hat internal network

### 3. SMTP Configuration

If your local SMTP doesn't work, configure a relay:

```bash
# Red Hat internal mail relay
export SMTP_SERVER=smtp.corp.redhat.com
export SMTP_PORT=25
```

## Troubleshooting

### Issue: Webhook receiver won't start

**Check Python dependencies:**
```bash
python3 -c "import flask" || pip3 install --user flask
```

**Check port availability:**
```bash
netstat -tuln | grep 3002
# or
ss -tuln | grep 3002
```

### Issue: Not receiving emails

**Check logs:**
```bash
pai-gitlab-webhook logs
```

**Test SMTP:**
```bash
echo "Test email" | mail -s "Test" your-email@redhat.com
```

**Verify email configuration:**
```bash
pai-gitlab-webhook status
```

### Issue: GitLab can't reach webhook

**Test connectivity from GitLab server:**
```bash
curl http://your-hostname:3002/health
```

**Check firewall:**
```bash
sudo firewall-cmd --list-ports
```

**Check service status:**
```bash
pai-gitlab-webhook status
```

### Issue: Systemd service fails

**Check service status:**
```bash
systemctl --user status pai-gitlab-webhook.service
```

**View service logs:**
```bash
journalctl --user -u pai-gitlab-webhook.service -n 50
```

**Restart service:**
```bash
systemctl --user restart pai-gitlab-webhook.service
```

## Advanced Configuration

### Multiple Email Recipients

Modify `/home/jbyrd/pai/src/gitlab_webhook_receiver.py`:

```python
EMAIL_TO = "jbyrd@redhat.com,teammate@redhat.com"
```

Or use email aliases/distribution lists in your mail system.

### Custom Email Formatting

Edit the `format_issue_notification()` function in `gitlab_webhook_receiver.py`.

### Webhook Event Filtering

Modify the webhook handler to process additional events:
- Comments
- Issue updates
- Merge requests
- Pipeline events

### Statistics and Monitoring

View webhook statistics:
```bash
curl http://localhost:3002/stats
```

Event log (JSONL format):
```bash
cat ~/.config/pai/logs/gitlab-events.jsonl | jq .
```

## Integration with PAI System

This webhook receiver integrates with your PAI infrastructure:

- **Logging:** Uses PAI logging directory (`~/.config/pai/logs/`)
- **Configuration:** Follows PAI configuration patterns
- **Management:** Uses `pai-*` command naming convention
- **Systemd:** Integrates with PAI systemd services

## References

- **GitLab Webhooks Documentation:** https://docs.gitlab.com/ee/user/project/integrations/webhooks.html
- **PAI System:** `~/pai/README.md`
- **RFE Automation:** https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation

## Support

For issues or questions:
- **GitLab Issues:** https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation/issues
- **Logs:** `~/.config/pai/logs/gitlab-webhook.log`
- **Status:** `pai-gitlab-webhook status`

---

*Part of the PAI (Personal AI Infrastructure) System*  
*Hatter - Red Hat Digital Assistant*

