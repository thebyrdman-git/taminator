# GitLab Webhook Receiver - miraclemax Deployment

## Overview

Deploy the GitLab webhook receiver as a Docker container on miraclemax infrastructure to receive email notifications for RFE & Bug Tracker issues.

## Architecture

```
GitLab CEE (gitlab.cee.redhat.com)
    ↓ HTTPS
Cloudflare Tunnel → Traefik → GitLab Webhook Container
    ↓ SMTP
Email (jbyrd@redhat.com)
```

## Deployment Steps

### 1. Build Docker Image on miraclemax

```bash
# SSH to miraclemax
ssh jbyrd@miraclemax

# Navigate to compose directory
cd ~/pai-infrastructure-automation/miraclemax

# Build the image
docker build -t gitlab-webhook-receiver:latest docker/gitlab-webhook/

# Verify image
docker images | grep gitlab-webhook
```

### 2. Deploy Container

```bash
# Deploy using docker-compose
docker-compose -f compose/gitlab-webhook.yml up -d

# Check container status
docker ps | grep gitlab-webhook

# View logs
docker logs -f gitlab-webhook
```

### 3. Verify Service

```bash
# Test health endpoint
curl http://localhost:3002/health

# Test from workstation via Traefik
curl http://gitlab-webhook.jbyrd.org/health

# Check Traefik dashboard
# https://traefik.jbyrd.org
```

### 4. Configure GitLab Webhook

1. Navigate to: https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation/-/settings/webhooks
2. Click **Add new webhook**
3. Configure:
   - **URL:** `https://gitlab-webhook.jbyrd.org/webhook/gitlab`
   - **Secret Token:** (optional, set via GITLAB_WEBHOOK_SECRET)
   - **Trigger:** ✅ Issues events
   - **SSL verification:** ✅ Enable (Cloudflare handles SSL)
4. Click **Add webhook**
5. Test: Click **Test** → **Issues events**

### 5. Verify Email Delivery

```bash
# Check container logs
docker logs gitlab-webhook

# Check event log
docker exec gitlab-webhook cat /app/logs/gitlab-events.jsonl

# View statistics
curl http://gitlab-webhook.jbyrd.org/stats
```

## Configuration

### Environment Variables

Edit `/home/jbyrd/pai-infrastructure-automation/miraclemax/compose/gitlab-webhook.yml`:

```yaml
environment:
  - GITLAB_WEBHOOK_EMAIL=jbyrd@redhat.com  # Change recipient
  - GITLAB_WEBHOOK_SECRET=your-secret-here  # Optional security token
  - SMTP_SERVER=localhost                    # SMTP relay
  - SMTP_PORT=25                            # SMTP port
```

### Webhook Secret (Recommended)

Generate and set a secret token:

```bash
# Generate secret
SECRET=$(openssl rand -hex 32)
echo $SECRET

# Add to compose file
echo "      - GITLAB_WEBHOOK_SECRET=$SECRET" >> compose/gitlab-webhook.yml

# Redeploy
docker-compose -f compose/gitlab-webhook.yml up -d

# Add to GitLab webhook configuration
```

## Automated Deployment

### Using pai-miraclemax-deploy

```bash
# From workstation
cd ~/pai

# Deploy to miraclemax
pai-miraclemax-deploy

# Or use the repository script
cd repositories/pai-infrastructure-automation/miraclemax
./scripts/deploy.sh
```

This will:
- Sync configuration to miraclemax
- Build Docker image
- Deploy container
- Update Traefik routing
- Verify deployment

## Monitoring

### Container Health

```bash
# Check container status
docker ps -f name=gitlab-webhook

# View resource usage
docker stats gitlab-webhook

# Check health endpoint
curl http://localhost:3002/health
```

### Logs

```bash
# Container logs
docker logs -f gitlab-webhook

# Event log (JSONL format)
docker exec gitlab-webhook cat /app/logs/gitlab-events.jsonl | jq .

# Application log
docker exec gitlab-webhook cat /app/logs/gitlab-webhook.log
```

### Traefik Dashboard

Access Traefik dashboard: http://traefik.jbyrd.org

Look for:
- `gitlab-webhook@docker` router
- Health status: green
- Request metrics

### Prometheus Metrics (Future)

The container is on the `monitoring-network` for future Prometheus integration:
- Request count
- Response times
- Email success rate

## SMTP Configuration

### Local Postfix (Default)

Container uses `localhost:25` which maps to miraclemax's Postfix relay.

Verify Postfix is running on miraclemax:
```bash
systemctl status postfix
```

### External SMTP Relay

To use Red Hat's internal mail relay:

```yaml
environment:
  - SMTP_SERVER=smtp.corp.redhat.com
  - SMTP_PORT=25
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs gitlab-webhook

# Check if port is available
netstat -tuln | grep 3002

# Rebuild image
docker-compose -f compose/gitlab-webhook.yml build --no-cache
docker-compose -f compose/gitlab-webhook.yml up -d
```

### Not Receiving Emails

```bash
# Check container logs for SMTP errors
docker logs gitlab-webhook | grep -i smtp

# Test SMTP from container
docker exec gitlab-webhook python3 -c "
import smtplib
from email.mime.text import MIMEText
msg = MIMEText('Test')
msg['Subject'] = 'Test from gitlab-webhook'
msg['From'] = 'hatter@miraclemax'
msg['To'] = 'jbyrd@redhat.com'
with smtplib.SMTP('localhost', 25) as s:
    s.send_message(msg)
print('Sent')
"

# Check Postfix on miraclemax
ssh miraclemax 'tail -f /var/log/maillog'
```

### GitLab Can't Reach Webhook

```bash
# Test from miraclemax
curl http://localhost:3002/health

# Test via Traefik
curl http://gitlab-webhook.jbyrd.org/health

# Check Traefik routing
docker logs traefik | grep gitlab-webhook

# Verify Cloudflare Tunnel is running
systemctl --user status cloudflare-tunnel
```

### View Event Statistics

```bash
# Get webhook stats
curl http://gitlab-webhook.jbyrd.org/stats | jq .

# Count events by type
docker exec gitlab-webhook sh -c "cat /app/logs/gitlab-events.jsonl | jq -r .type | sort | uniq -c"

# Recent events
docker exec gitlab-webhook sh -c "tail -n 10 /app/logs/gitlab-events.jsonl | jq ."
```

## Backup & Recovery

### Backup Event Logs

The event logs are backed up automatically via miraclemax backup system:

```bash
# Manual backup
docker cp gitlab-webhook:/app/logs /home/jbyrd/backups/gitlab-webhook-logs-$(date +%Y%m%d)
```

### Restore from Backup

```bash
# Restore logs
docker cp /path/to/backup/logs gitlab-webhook:/app/

# Restart container
docker restart gitlab-webhook
```

## Updates & Maintenance

### Update Container Image

```bash
# SSH to miraclemax
ssh miraclemax

cd ~/pai-infrastructure-automation/miraclemax

# Pull latest code
git pull

# Rebuild image
docker-compose -f compose/gitlab-webhook.yml build --no-cache

# Redeploy
docker-compose -f compose/gitlab-webhook.yml up -d

# Verify
curl http://localhost:3002/health
```

### View Recent Activity

```bash
# Last 50 log lines
docker logs --tail 50 gitlab-webhook

# Follow logs in real-time
docker logs -f gitlab-webhook

# Search for specific issue
docker logs gitlab-webhook | grep "Issue #123"
```

## Security Considerations

### Network Access

- Container is on `traefik-network` for external access
- Accessible via Cloudflare Tunnel (SSL termination)
- Rate limiting applied via Traefik middleware
- No direct internet exposure

### Webhook Secret

Always configure a webhook secret in production:

```bash
# Generate strong secret
openssl rand -hex 32

# Add to compose file and GitLab webhook config
```

### SMTP Security

- Uses internal Postfix relay
- No authentication required (trusted local network)
- Emails sent to @redhat.com only

## Integration with miraclemax Infrastructure

### Service Discovery

The webhook receiver integrates with:
- **Traefik:** Automatic routing and load balancing
- **Monitoring Network:** Ready for Prometheus metrics
- **Backup System:** Automatic log backups
- **Cloudflare Tunnel:** Secure external access

### Labels

Container labels enable:
- Automatic backup scheduling
- Health monitoring
- Service discovery
- Traefik routing

### Resource Limits

Conservative resource allocation:
- **CPU:** 0.5 cores max (0.1 reserved)
- **Memory:** 256MB max (64MB reserved)
- Suitable for low-volume webhook traffic

## URLs

After deployment, access at:
- **Webhook URL:** https://gitlab-webhook.jbyrd.org/webhook/gitlab
- **Health Check:** https://gitlab-webhook.jbyrd.org/health
- **Statistics:** https://gitlab-webhook.jbyrd.org/stats
- **Service Info:** https://gitlab-webhook.jbyrd.org/

## Support

### Logs Location
- Container: `/app/logs/`
- Events: `/app/logs/gitlab-events.jsonl`
- Application: `/app/logs/gitlab-webhook.log`

### Commands Reference
```bash
# Start
docker-compose -f compose/gitlab-webhook.yml up -d

# Stop
docker-compose -f compose/gitlab-webhook.yml down

# Restart
docker restart gitlab-webhook

# Logs
docker logs -f gitlab-webhook

# Stats
curl http://localhost:3002/stats

# Health
curl http://localhost:3002/health
```

---

*Part of the PAI (Personal AI Infrastructure) System*  
*Deployed on miraclemax - Production Infrastructure*  
*Hatter - Red Hat Digital Assistant*

