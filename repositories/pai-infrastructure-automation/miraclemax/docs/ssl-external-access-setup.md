# SSL & External Access Setup Guide

**Goal**: Secure HTTPS access to all services via jbyrd.org domain  
**Method**: Traefik + Let's Encrypt + Cloudflare DNS Challenge  
**Security**: Defense in Depth, Zero Trust principles

---

## Architecture Overview

```
Internet (HTTPS)
    ↓
jbyrd.org (Cloudflare DNS)
    ↓
Traefik (miraclemax:80/443)
    ├→ ha.jbyrd.org → Home Assistant :8123
    ├→ money.jbyrd.org → Actual Budget :5006
    ├→ n8n.jbyrd.org → n8n :5678 (internal only)
    ├→ metrics.jbyrd.org → Prometheus :9090 (auth required)
    └→ traefik.jbyrd.org → Traefik Dashboard :8080 (auth required)
```

---

## Prerequisites

### 1. Cloudflare Account Setup
- [x] Domain jbyrd.org managed by Cloudflare
- [ ] API token or Global API key

### 2. DNS Records (Configure in Cloudflare)

```
Type  Name      Content           Proxy  TTL
A     @         YOUR_PUBLIC_IP    Yes    Auto
A     *         YOUR_PUBLIC_IP    Yes    Auto
CNAME ha        @                 Yes    Auto
CNAME budget    @                 Yes    Auto
CNAME n8n       @                 Yes    Auto
CNAME metrics   @                 Yes    Auto
CNAME traefik   @                 Yes    Auto
```

**Note**: If using Cloudflare Tunnel, configure tunnel instead of A records.

### 3. Firewall Rules
On miraclemax:
```bash
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

On router (port forwarding):
- External 80 → 192.168.1.34:80
- External 443 → 192.168.1.34:443

---

## Setup Procedure

### Step 1: Get Cloudflare API Credentials

**Option A: Scoped API Token (Recommended)**
1. Go to https://dash.cloudflare.com/profile/api-tokens
2. Click "Create Token"
3. Use template: "Edit zone DNS"
4. Zone Resources: Include → Specific zone → jbyrd.org
5. Copy the token

**Option B: Global API Key**
1. Go to https://dash.cloudflare.com/profile/api-tokens
2. View "Global API Key"
3. Copy the key

### Step 2: Configure Secrets

Create environment file with Cloudflare credentials:

```bash
# On miraclemax
ssh jbyrd@192.168.1.34

# Create secrets directory
mkdir -p ~/.config/pai/secrets
chmod 700 ~/.config/pai/secrets

# Create Cloudflare secrets file
cat > ~/.config/pai/secrets/cloudflare.env << 'EOF'
# Cloudflare DNS API Credentials
# Used by Traefik for Let's Encrypt DNS challenge

# Option A: Scoped API Token (recommended)
CF_DNS_API_TOKEN=your-cloudflare-api-token-here

# Option B: Global API Key (less secure)
# CF_API_EMAIL=your-email@example.com
# CF_API_KEY=your-global-api-key-here
EOF

# Secure the file
chmod 600 ~/.config/pai/secrets/cloudflare.env

# Edit and add your credentials
nano ~/.config/pai/secrets/cloudflare.env
```

### Step 3: Create Required Directories

```bash
# On miraclemax
mkdir -p ~/traefik-data/{acme,logs}
chmod 700 ~/traefik-data/acme
```

### Step 4: Generate Dashboard Password

```bash
# Install htpasswd (if not present)
sudo dnf install httpd-tools

# Generate password for Traefik dashboard
htpasswd -nB admin

# Output will be: admin:$2y$05$...
# Copy this and update config/traefik/dynamic.yml
# Replace the line under dashboard-auth middleware
```

### Step 5: Update Traefik Compose File

```bash
cd ~/miraclemax-infrastructure/compose

# Add secrets to traefik.yml
# The deploy script will handle this, or manually:
sed -i '/environment:/a\      - CF_DNS_API_TOKEN=${CF_DNS_API_TOKEN}' traefik.yml
```

### Step 6: Deploy Traefik

```bash
cd ~/miraclemax-infrastructure

# Load Cloudflare credentials
export $(cat ~/.config/pai/secrets/cloudflare.env | xargs)

# Stop existing Traefik
podman stop traefik 2>/dev/null || true
podman rm traefik 2>/dev/null || true

# Deploy new configuration
podman-compose -f compose/traefik.yml up -d

# Check logs
podman logs -f traefik
```

**Expected output**:
```
time="..." level=info msg="Configuration loaded from file: /etc/traefik/traefik.yml"
time="..." level=info msg="Traefik version 3.0.0"
time="..." level=info msg="Starting provider aggregator"
time="..." level=info msg="Starting provider *docker.Provider"
time="..." level=info msg="Starting provider *file.Provider"
```

### Step 7: Verify SSL Certificate Generation

```bash
# Check certificate acquisition
podman logs traefik 2>&1 | grep -i "certificate"

# Should see:
# "Obtaining certificate for domain *.jbyrd.org"
# "Certificate obtained successfully"

# Verify acme.json created
ls -lh ~/traefik-data/acme/acme.json
```

### Step 8: Update Service Compose Files

Services need Traefik labels. Already configured in:
- `compose/homeassistant.yml`
- `compose/actual-budget.yml`
- `compose/n8n.yml`

Deploy services:
```bash
podman-compose -f compose/homeassistant.yml up -d
podman-compose -f compose/actual-budget.yml up -d
podman-compose -f compose/n8n.yml up -d
```

### Step 9: Test External Access

```bash
# Test from external network (use phone data or different network)
curl -I https://ha.jbyrd.org
curl -I https://money.jbyrd.org
curl -I https://traefik.jbyrd.org

# Should return HTTP 200 or 401 (if auth required)
# Should have valid SSL certificate
```

---

## Service URLs

After setup, services available at:

- **Home Assistant**: https://ha.jbyrd.org
- **Actual Budget**: https://money.jbyrd.org
- **n8n**: https://n8n.jbyrd.org (internal network only)
- **Prometheus**: https://metrics.jbyrd.org (auth required)
- **Traefik Dashboard**: https://traefik.jbyrd.org (auth required)
- **cAdvisor**: https://cadvisor.jbyrd.org (auth required)

---

## Security Features

### Applied Principles

✅ **Defense in Depth (5 Layers)**:
1. Network: Cloudflare DDoS protection
2. Edge: Traefik rate limiting
3. Transport: TLS 1.2+ encryption
4. Application: Basic auth for sensitive services
5. Access: IP whitelist for internal services

✅ **Security Headers**:
- X-Frame-Options: SAMEORIGIN
- X-Content-Type-Options: nosniff
- X-XSS-Protection: 1; mode=block
- Strict-Transport-Security: max-age=31536000
- Content-Security-Policy: (to be configured per service)

✅ **Certificate Management**:
- Automatic renewal (Let's Encrypt)
- 90-day validity, renewed at 60 days
- Wildcard certificate (*.jbyrd.org)
- Stored in encrypted volume

---

## Troubleshooting

### Issue: Certificate Not Generating

**Check**:
```bash
# View Traefik logs
podman logs traefik 2>&1 | grep -i "error\|certificate"

# Common causes:
# 1. Cloudflare API credentials invalid
# 2. DNS not propagated (wait 5-10 minutes)
# 3. Rate limit hit (5 certificates/week for same domain)
```

**Solution**:
```bash
# Verify Cloudflare credentials
export $(cat ~/.config/pai/secrets/cloudflare.env | xargs)
echo $CF_DNS_API_TOKEN  # Should show token

# Test DNS resolution
dig @1.1.1.1 _acme-challenge.jbyrd.org TXT

# Remove existing acme.json and retry
rm ~/traefik-data/acme/acme.json
podman restart traefik
```

### Issue: 502 Bad Gateway

**Cause**: Backend service not reachable

**Check**:
```bash
# Verify service is running
podman ps | grep homeassistant

# Test direct access
curl http://192.168.1.34:8123

# Check Traefik routing
podman exec traefik cat /etc/traefik/dynamic.yml
```

### Issue: Can't Access Externally

**Check**:
1. Firewall rules (miraclemax)
2. Port forwarding (router)
3. Cloudflare proxy status
4. DNS propagation

```bash
# Test from external network
curl -v https://ha.jbyrd.org

# Check DNS resolution
dig ha.jbyrd.org +short
```

---

## Maintenance

### Certificate Renewal

Automatic via Let's Encrypt (60-day renewal window).

**Manual renewal**:
```bash
# Force renewal (if needed)
podman exec traefik traefik cert renew

# Verify expiration
podman exec traefik cat /acme/acme.json | jq '.Certificates[0].domain.main'
```

### Update Traefik Configuration

```bash
# Edit configuration
nano config/traefik/dynamic.yml

# Traefik watches for changes - no restart needed
# Verify reload
podman logs traefik --tail 20
```

### Add New Service

1. Add router in `config/traefik/dynamic.yml`:
```yaml
http:
  routers:
    myservice:
      rule: "Host(`myservice.jbyrd.org`)"
      service: myservice
      tls:
        certResolver: letsencrypt
  
  services:
    myservice:
      loadBalancer:
        servers:
          - url: "http://192.168.1.34:PORT"
```

2. Add DNS record in Cloudflare

3. Deploy service with Traefik labels

---

## Monitoring

### Health Checks

```bash
# Check all service health
curl http://192.168.1.34:8080/api/http/routers

# Check certificate status
curl http://192.168.1.34:8080/api/http/routers | jq '.[] | {name: .name, tls: .tls}'
```

### Metrics

Prometheus metrics available at:
- http://192.168.1.34:8080/metrics

**Key metrics**:
- `traefik_entrypoint_requests_total` - Request count
- `traefik_entrypoint_request_duration_seconds` - Latency
- `traefik_backend_requests_total` - Backend health
- `traefik_tls_certs_not_after` - Certificate expiration

---

## Rollback Procedure

If issues occur:

```bash
# Stop new Traefik
podman stop traefik
podman rm traefik

# Restore backup configuration
cp -r /tmp/miraclemax-backup-*/traefik-config ~/

# Restart with old configuration
# (manual restart process here)
```

---

## References

- [Traefik Documentation](https://doc.traefik.io/traefik/)
- [Let's Encrypt DNS Challenge](https://letsencrypt.org/docs/challenge-types/)
- [Cloudflare API Tokens](https://developers.cloudflare.com/api/tokens/)
- [Defense in Depth](../contexts/sysadmin/persona.md#defense-in-depth-security)

---

*SSL & External Access Setup Guide v1.0*  
*Sys Admin - Professional Infrastructure*  
*Based on Zero Trust and Defense in Depth principles*

