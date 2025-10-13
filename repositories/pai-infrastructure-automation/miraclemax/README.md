# miraclemax Infrastructure

**Infrastructure as Code for miraclemax home server**

## Server Specifications

- **Hostname**: miraclemax.local
- **IP**: 192.168.1.34
- **OS**: RHEL 9.6 (Plow)
- **Container Runtime**: Podman 5.4.0
- **Resources**:
  - CPU: x86_64
  - RAM: 62GB (18GB used, 43GB available)
  - Storage Root: 80GB (45GB used, 56%)
  - Storage Home: 353GB (222GB used, 63%)
  - Storage Data: 3.6TB (27GB used, 1%)

## Architecture

```
miraclemax (192.168.1.34)
├── Traefik v3.0 (reverse proxy)
│   └── Ports: 80, 8080
├── Home Assistant (stable)
│   └── Port: 8123
├── Actual Budget (latest)
│   └── Port: 5006
├── n8n (latest)
│   └── Port: 5678
└── cAdvisor v0.47.0 (metrics)
    └── Port: 8084
```

## Quick Start

### Deploy All Services

```bash
# Deploy from this repository
./deploy.sh

# Or individual services
podman-compose -f compose/traefik.yml up -d
podman-compose -f compose/homeassistant.yml up -d
```

### Rollback

```bash
# Rollback to previous version
./rollback.sh
```

### Verify Deployment

```bash
# Check all services
./verify.sh

# View logs
./logs.sh <service-name>
```

## Repository Structure

```
miraclemax-infrastructure/
├── compose/                  # Container compose files
│   ├── traefik.yml
│   ├── homeassistant.yml
│   ├── actual-budget.yml
│   ├── n8n.yml
│   ├── cadvisor.yml
│   └── monitoring.yml
├── config/                   # Service configurations
│   ├── traefik/
│   └── prometheus/
├── docs/                     # Documentation
│   ├── deployment.md
│   ├── troubleshooting.md
│   └── runbooks/
├── scripts/                  # Automation scripts
│   ├── deploy.sh
│   ├── rollback.sh
│   ├── verify.sh
│   └── backup.sh
└── README.md
```

## Services

### Traefik (Reverse Proxy)
- **Image**: traefik:v3.0.0 (pinned)
- **Ports**: 80 (HTTP), 8080 (Dashboard)
- **Config**: `config/traefik/traefik.yml`
- **Networks**: traefik-network

### Home Assistant
- **Image**: ghcr.io/home-assistant/home-assistant:2024.10.0 (pinned)
- **Port**: 8123
- **Data**: `/home/jbyrd/homeassistant-config`
- **Networks**: traefik-network

### Actual Budget
- **Image**: actualbudget/actual-server:24.10.1 (pinned)
- **Port**: 5006
- **Data**: `/home/jbyrd/actual-budget-data`
- **Networks**: traefik-network

### n8n (Workflow Automation)
- **Image**: n8nio/n8n:1.60.1 (pinned)
- **Port**: 5678
- **Data**: `/home/jbyrd/n8n-data`
- **Networks**: traefik-network

### cAdvisor (Container Metrics)
- **Image**: gcr.io/cadvisor/cadvisor:v0.47.0 (pinned)
- **Port**: 8084
- **Prometheus**: Exports to monitoring-stack
- **Networks**: monitoring-stack

## Operations

### Deployment Process

1. **Pre-deployment checks**
   - Verify miraclemax connectivity
   - Check disk space
   - Review change log

2. **Deployment**
   - Pull new images
   - Stop existing containers
   - Start new containers
   - Run health checks

3. **Post-deployment**
   - Verify all services healthy
   - Check logs for errors
   - Update documentation

### Rollback Procedure

1. Stop current containers
2. Restore previous version from Git
3. Redeploy using previous commit
4. Verify services operational
5. Document incident

### Monitoring

- **Health Checks**: Built into each compose file
- **Metrics**: cAdvisor exports to Prometheus
- **Logs**: Accessed via `podman logs <container>`
- **Alerts**: (To be configured in Phase 2)

## Security

- All services behind Traefik reverse proxy
- No `:latest` tags (version pinning enforced)
- Secrets stored in `/home/jbyrd/.config/pai/secrets/` (GPG encrypted)
- SELinux enforcing (to be verified)
- Firewall rules (to be documented)

## Maintenance

### Updates

```bash
# Check for updates
./scripts/check-updates.sh

# Update specific service
./scripts/update-service.sh <service-name>

# Update all services (with approval)
./scripts/update-all.sh
```

### Backups

```bash
# Manual backup
./scripts/backup.sh

# Automated: Daily at 2 AM via systemd timer
systemctl status miraclemax-backup.timer
```

### Capacity Management

Current utilization:
- Root disk: 56% (alert @ 75%)
- Home disk: 63% (alert @ 75%)
- Memory: 29% (alert @ 75%)
- Storage: 1% (alert @ 80%)

## Troubleshooting

See [docs/troubleshooting.md](docs/troubleshooting.md) for common issues and solutions.

### Quick Diagnostics

```bash
# Check service status
podman ps -a

# View logs
podman logs <container-name> --tail 50

# Check resources
df -h
free -h
podman stats

# Test connectivity
curl http://localhost:8123  # Home Assistant
curl http://localhost:5006  # Actual Budget
```

## Phase 1 Implementation Status

**Current Phase**: 1.1 Infrastructure as Code

- [x] Create Git repository
- [x] Document current state
- [ ] Convert to podman-compose files (in progress)
- [ ] Pin all image versions
- [ ] Add container resource limits
- [ ] Test deployment from scratch
- [ ] Document rollback procedure

**Next Phase**: 1.2 Monitoring & Observability

## Contributing

This is personal infrastructure. Changes should follow:
1. Create feature branch
2. Test on local environment
3. Update documentation
4. Merge to main
5. Deploy to miraclemax

## References

- [Technical Roadmap](../MIRACLEMAX-TECHNICAL-ROADMAP.md)
- [SRE Principles](../contexts/sysadmin/persona.md)
- [Podman Documentation](https://docs.podman.io/)
- [Traefik Documentation](https://doc.traefik.io/traefik/)

---

*miraclemax Infrastructure v1.0*  
*Managed with Infrastructure as Code principles*  
*Last Updated: 2025-10-12*

