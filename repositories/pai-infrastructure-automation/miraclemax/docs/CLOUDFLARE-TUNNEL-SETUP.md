# Cloudflare Tunnel Setup Guide
## Zero Trust Access for Miraclemax Infrastructure

### 🎯 **Why Cloudflare Tunnel?**

- ✅ **No Port Forwarding** - No exposed ports 80/443
- ✅ **No DDNS Needed** - IP changes don't matter
- ✅ **Works Behind Any Firewall/NAT** - Including CGNAT
- ✅ **Built-in DDoS Protection** - Cloudflare's global network
- ✅ **Zero Trust Security** - Outbound-only connections
- ✅ **Automatic Failover** - Multiple Cloudflare datacenters

### 📋 **Setup Steps**

#### **Step 1: Create Tunnel in Cloudflare Dashboard**

1. Visit: https://dash.cloudflare.com
2. Navigate: **Zero Trust** → **Networks** → **Tunnels**
3. Click: **"Create a tunnel"**
4. Select: **"Cloudflared"** as connector type
5. Name: `miraclemax`
6. Click: **"Save tunnel"**

#### **Step 2: Get Tunnel Token**

After saving, you'll see installation instructions. Look for:
```bash
cloudflared service install <TOKEN>
```

Copy the TOKEN (starts with `eyJh...`) - it will be very long (~400+ characters).

**Important**: The token contains your tunnel credentials - keep it secure!

#### **Step 3: Configure Tunnel Routes**

In the Cloudflare dashboard, add these public hostnames:

| Public Hostname | Service | URL |
|----------------|---------|-----|
| ha.jbyrd.org | HTTP | http://localhost:80 |
| budget.jbyrd.org | HTTP | http://localhost:80 |
| n8n.jbyrd.org | HTTP | http://localhost:80 |
| cadvisor.jbyrd.org | HTTP | http://localhost:80 |
| traefik.jbyrd.org | HTTP | http://localhost:80 |
| auth.jbyrd.org | HTTP | http://localhost:80 |
| metrics.jbyrd.org | HTTP | http://localhost:80 |

**Or** use a single wildcard: `*.jbyrd.org` → `http://localhost:80`

#### **Step 4: Provide Token**

Once you have the token, the system will:
- Install tunnel service
- Configure all routes
- Enable auto-start on boot
- Test all services

### 🔧 **Technical Details**

**How it works:**
1. cloudflared connects OUT to Cloudflare (no inbound needed)
2. Cloudflare routes traffic through tunnel to Traefik
3. Traefik terminates SSL and routes to services
4. Services protected by Authelia MFA

**Architecture:**
```
Internet User
     ↓
Cloudflare Edge (SSL termination option)
     ↓
Cloudflare Tunnel (encrypted)
     ↓
cloudflared on miraclemax
     ↓
Traefik (localhost:80 → SSL → services)
     ↓
Authelia MFA
     ↓
Services
```

### 🔒 **Security**

- Tunnel connection is encrypted (TLS)
- No inbound firewall rules needed
- Can add Cloudflare Access policies for additional protection
- Rate limiting built-in
- DDoS protection automatic

### 📊 **After Setup**

**Remove port forwarding rules** (optional but recommended):
- No longer need 80/443 forwarded to 192.168.1.34
- More secure without exposed ports

**Keep local access:**
- SSH port 22 can stay for management
- Or use Cloudflare Access for SSH over tunnel

### 🎯 **Status**

- ✅ cloudflared installed (v2025.9.1)
- ⏳ Awaiting tunnel token from dashboard
- ⏳ Service configuration pending
- ⏳ Route setup pending

---

**Ready to proceed once you provide the tunnel token!**

