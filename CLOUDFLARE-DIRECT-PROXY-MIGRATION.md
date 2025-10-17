# Cloudflare Direct Proxy Migration

**Date**: October 16, 2025  
**Status**: ✅ COMPLETE  
**Impact**: Migrated from Cloudflare Tunnel to Direct Cloudflare Proxy

---

## Problem

`money.jbyrd.org` experiencing intermittent 502/503/504 errors due to Cloudflare Tunnel (free tier) idle timeouts and reconnects.

## Root Cause

1. **Cloudflare Tunnel instability** - Free tier has idle timeout issues
2. **Rootless Podman IPv6-only binding** - Traefik binding to `[::]:80` instead of `0.0.0.0:80`, preventing external IPv4 connections

## Solution

### 1. DNS Migration
Migrated Cloudflare DNS from tunnel to direct proxy:
- Changed A records from tunnel IPs to public IP: `75.183.205.24`
- All `*.jbyrd.org` subdomains now proxied through Cloudflare edge
- Cloudflare SSL termination at edge, origin SSL between Cloudflare→MiracleMax

### 2. Rootful Podman Migration
Switched Traefik from rootless to rootful Podman:
- **Problem**: Rootless Podman binds IPv6-only (`[::]:80`), blocking IPv4 connections
- **Solution**: Rootful Podman binds properly (`0.0.0.0:80`)
- **Command**: `sudo podman run ...` instead of `podman run ...`

### 3. Disabled Cloudflare Tunnel
```bash
sudo systemctl stop cloudflared
sudo systemctl disable cloudflared
```

---

## Configuration Changes

### DNS Records (Cloudflare)
All A records updated to:
- **Type**: A
- **Value**: 75.183.205.24
- **Proxy**: Enabled ✓
- **TTL**: Auto

### Traefik (`traefik.yml`)
- **Bind addresses**: Changed from `:80` → `0.0.0.0:80` (explicit IPv4)
- **Port mappings**: Changed from `8000:80` → `80:80` (direct binding)
- **Execution**: `sudo podman` instead of `podman`

### Router (Already Configured)
- Port forwarding: 80 → 192.168.1.34:80
- Port forwarding: 443 → 192.168.1.34:443

---

## Verification

```bash
# DNS resolution
$ dig +short money.jbyrd.org
172.67.220.119  # Cloudflare proxy IP
104.21.53.242   # Cloudflare proxy IP

# Service test
$ curl -I https://money.jbyrd.org
HTTP/2 200 
date: Thu, 16 Oct 2025 03:58:29 GMT
✅ SUCCESS
```

---

## Current Status

### ✅ Working
- `money.jbyrd.org` - Actual Budget (HTTP 200)
- Traefik IPv4 binding (0.0.0.0:80, 0.0.0.0:443)
- Cloudflare proxy routing
- Let's Encrypt SSL certificates

### ⚠️ Needs Configuration
- `ha.jbyrd.org` - Home Assistant (404 - backend not connected)
- `grafana.jbyrd.org` - Grafana (404 - backend not connected)
- Other services need traefik-network connection

---

## Next Steps

1. **Reconnect services** - Connect HA, Grafana, and other services to `traefik-network`
2. **Systemd service** - Create `traefik.service` for rootful Podman autostart
3. **Monitoring** - Update Prometheus to monitor rootful containers
4. **Documentation** - Update deployment docs for rootful Podman architecture

---

## Technical Details

### IPv4 vs IPv6 Binding Issue
```bash
# Rootless Podman (BAD)
$ netstat -tulpn | grep :80
tcp6  :::80  :::*  LISTEN  rootlessport

# Rootful Podman (GOOD)
$ netstat -tulpn | grep :80
tcp  0.0.0.0:80  0.0.0.0:*  LISTEN  conmon
```

### Rootful Podman Command
```bash
sudo podman run -d \
  --name traefik-root \
  --restart unless-stopped \
  --network traefik-network \
  -p 80:80 \
  -p 443:443 \
  -p 8080:8080 \
  -v /home/jbyrd/miraclemax-infrastructure/config/traefik/traefik.yml:/etc/traefik/traefik.yml:ro \
  -v /home/jbyrd/miraclemax-infrastructure/config/traefik/dynamic.yml:/etc/traefik/dynamic.yml:ro \
  -v /home/jbyrd/traefik-data/acme:/acme \
  -v /home/jbyrd/traefik-data/logs:/var/log/traefik \
  -v /run/podman/podman.sock:/var/run/docker.sock:ro \
  -e TZ=America/New_York \
  --security-opt no-new-privileges:true \
  traefik:v3.0
```

---

**Result**: Stable, reliable direct Cloudflare proxy with proper IPv4 support.

