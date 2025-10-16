# GitLab Webhook Email Notifications - Quick Start

Get email notifications for RFE tracker issues in 3 steps.

## 1. Install & Start

```bash
# Install Flask
pip3 install --user flask

# Start webhook receiver
pai-gitlab-webhook start
```

## 2. Configure GitLab

1. Go to: https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation/-/settings/webhooks
2. Click **Add new webhook**
3. Set URL: `http://$(hostname -f):3002/webhook/gitlab`
4. Check: **Issues events**
5. Uncheck: **Enable SSL verification** (unless you have SSL)
6. Click **Add webhook**
7. Click **Test** → **Issues events**

## 3. Test

```bash
# Check status
pai-gitlab-webhook status

# View logs
pai-gitlab-webhook logs
```

Create a test issue in GitLab - you should receive an email.

## Production Setup (Optional)

Run as systemd service:

```bash
# Install service
mkdir -p ~/.config/systemd/user/
cp ~/pai/systemd/pai-gitlab-webhook.service ~/.config/systemd/user/

# Enable and start
systemctl --user enable --now pai-gitlab-webhook.service
loginctl enable-linger $USER

# Check status
systemctl --user status pai-gitlab-webhook.service
```

## Troubleshooting

**Not receiving emails?**
- Check logs: `pai-gitlab-webhook logs`
- Test SMTP: `echo "test" | mail -s "Test" $USER@redhat.com`
- Verify status: `pai-gitlab-webhook status`

**GitLab can't reach webhook?**
- Test locally: `curl http://localhost:3002/health`
- Check firewall: `sudo firewall-cmd --add-port=3002/tcp --permanent && sudo firewall-cmd --reload`

**Full documentation:** `/home/jbyrd/pai/docs/GITLAB-WEBHOOK-SETUP.md`

