# GitLab Webhook Email Notifications - miraclemax Quick Start

Get email notifications for RFE tracker issues in 3 commands.

## Quick Deploy

```bash
# 1. Deploy to miraclemax
pai-gitlab-webhook-deploy

# 2. Check status
pai-gitlab-webhook-deploy status

# 3. Configure GitLab webhook
```

## GitLab Configuration

1. Go to: https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation/-/settings/webhooks
2. Click **Add new webhook**
3. Configure:
   - **URL:** `https://gitlab-webhook.jbyrd.org/webhook/gitlab`
   - **Trigger:** ✅ Issues events
   - **SSL verification:** ✅ Enable
4. Click **Add webhook**
5. Test: Click **Test** → **Issues events**

## Verify

```bash
# Check service status
pai-gitlab-webhook-deploy status

# View logs
pai-gitlab-webhook-deploy logs

# Test health endpoint
curl https://gitlab-webhook.jbyrd.org/health
```

Create a test issue in GitLab - you should receive an email at `jbyrd@redhat.com`.

## Management Commands

```bash
pai-gitlab-webhook-deploy          # Deploy/update
pai-gitlab-webhook-deploy status   # Check status
pai-gitlab-webhook-deploy logs     # Follow logs
pai-gitlab-webhook-deploy restart  # Restart service
pai-gitlab-webhook-deploy stop     # Stop service
```

## Troubleshooting

**Not receiving emails?**
```bash
# Check logs
pai-gitlab-webhook-deploy logs

# Verify SMTP on miraclemax
ssh miraclemax 'systemctl status postfix'
```

**GitLab can't reach webhook?**
```bash
# Test locally on miraclemax
ssh miraclemax 'curl http://localhost:3002/health'

# Test via Traefik
curl https://gitlab-webhook.jbyrd.org/health

# Check Cloudflare Tunnel
ssh miraclemax 'systemctl --user status cloudflare-tunnel'
```

**Full documentation:** `/home/jbyrd/pai/docs/GITLAB-WEBHOOK-MIRACLEMAX-DEPLOYMENT.md`

## Architecture

- **Runs on:** miraclemax (192.168.1.34)
- **Docker Container:** `gitlab-webhook-receiver:latest`
- **Exposed via:** Traefik + Cloudflare Tunnel
- **Email via:** Postfix SMTP relay on miraclemax
- **Logs:** Persistent volume in Docker

## URLs

- **Webhook:** https://gitlab-webhook.jbyrd.org/webhook/gitlab
- **Health:** https://gitlab-webhook.jbyrd.org/health
- **Stats:** https://gitlab-webhook.jbyrd.org/stats

---

*Part of the PAI (Personal AI Infrastructure) System*  
*Running on miraclemax - Production Infrastructure*

