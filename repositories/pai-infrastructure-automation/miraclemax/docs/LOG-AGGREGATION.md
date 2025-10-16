# MiracleMax Log Aggregation System

Enterprise-grade centralized logging with Loki + Promtail

## 📊 Overview

**Stack**: Grafana Loki 2.9.3 + Promtail 2.9.3  
**Purpose**: Centralized log collection, storage, and querying for all containers  
**Retention**: 30 days (aligned with backup strategy)  
**Storage**: Local filesystem with automatic cleanup

## 🏗️ Architecture

```
┌─────────────────┐
│   Containers    │
│  (18+ services) │
└────────┬────────┘
         │ logs
         ▼
    ┌─────────┐
    │Promtail │ ──discovers via──▶ Podman Socket
    └────┬────┘                    /run/user/1000/podman/podman.sock
         │ pushes
         ▼
    ┌────────┐
    │  Loki  │ ◀──queries── Grafana
    └────────┘
      30-day
     retention
```

## 🚀 Components

### Loki (Log Aggregation)
- **Port**: 3100
- **URL**: https://loki.jbyrd.org (Authelia protected)
- **Storage**: `/var/lib/containers/storage/volumes/loki-data`
- **Retention**: 30 days, auto-compaction enabled
- **Features**:
  - Time-series log storage
  - Label-based indexing
  - LogQL query language
  - Prometheus-like querying

### Promtail (Log Collection)
- **Port**: 9080 (metrics)
- **Discovery**: Automatic via Podman socket
- **Targets**: All running containers
- **Features**:
  - Auto-discovery of containers
  - Log streaming to Loki
  - Metadata extraction (container name, image, labels)
  - JSON log parsing

## 📈 Monitoring Integration

### Prometheus Metrics
- **Loki**: `http://loki:3100/metrics`
- **Promtail**: `http://promtail:9080/metrics`

### Alert Rules
- `LokiDown`: Service unavailable
- `PromtailDown`: Log collection stopped
- `HighLogIngestionRate`: Unusual log volume
- `NoLogsReceived`: Collection failure
- `SlowLogQueries`: Performance degradation

## 🔍 Usage

### Access Logs in Grafana

1. Navigate to **https://grafana.jbyrd.org**
2. Go to **Explore** (compass icon)
3. Select **Loki** datasource
4. Run queries using LogQL

### Example LogQL Queries

```logql
# All logs from Actual Budget
{container_name="actual-budget"}

# Errors across all containers
{job="containers"} |= "error"

# Traefik access logs
{container_name="compose_traefik_1"}

# n8n workflow logs
{container_name="n8n"}

# Last 10 minutes of Home Assistant logs
{container_name="homeassistant"} [10m]

# Count error rate
sum(rate({job="containers"} |= "error" [5m])) by (container_name)
```

### Filtering and Parsing

```logql
# JSON logs
{container_name="actual-budget"} | json

# Regex extraction
{container_name="traefik"} | regexp "(?P<status>\\d{3})"

# Line filters
{container_name="homeassistant"} |= "WARNING" != "homekit"
```

## 📂 Log Labels

Each log entry automatically includes:
- `cluster`: "miraclemax"
- `environment`: "production"
- `container_name`: Container name
- `container_id`: Short container ID (12 chars)
- `image`: Container image name
- `image_version`: Image tag
- `service`: From `com.miraclemax.service` label
- `network`: Docker/Podman network

## 🔧 Management

### Deploy/Update
```bash
pai-miraclemax-logs-deploy
```

### Check Status
```bash
ssh miraclemax 'podman ps | grep -E "(loki|promtail)"'
curl -s https://loki.jbyrd.org/ready
```

### View Live Logs
```bash
# Promtail logs
ssh miraclemax 'podman logs -f promtail'

# Loki logs
ssh miraclemax 'podman logs -f loki'
```

### Query from CLI
```bash
# List all containers being logged
curl -s http://loki:3100/loki/api/v1/label/container_name/values | jq -r '.data[]'

# Query logs
curl -s 'http://loki:3100/loki/api/v1/query_range?query={container_name="actual-budget"}&limit=10'
```

## 📦 Backup

Loki data is NOT included in regular backups due to:
- Large volume (logs regenerate)
- 30-day retention (temporary data)
- Metrics are backed up separately

If log backup is needed:
```bash
ssh miraclemax 'podman volume export loki-data > loki-backup.tar'
```

## 🛠️ Troubleshooting

### Loki Not Receiving Logs
1. Check Promtail is running: `podman ps | grep promtail`
2. Check Promtail targets: `curl localhost:9080/targets`
3. Check Promtail logs: `podman logs promtail | tail -50`

### Cannot Query Logs in Grafana
1. Verify Loki datasource: Grafana → Configuration → Data Sources → Loki
2. Test connection: Click "Save & Test"
3. Check Loki is reachable: `curl http://loki:3100/ready`

### High Disk Usage
```bash
# Check Loki storage size
ssh miraclemax 'du -sh /var/lib/containers/storage/volumes/loki-data'

# Trigger compaction (reduces storage)
curl -X POST http://loki:3100/loki/api/v1/delete
```

### Missing Container Logs
1. Verify container is labeled: `podman inspect <container> | grep miraclemax`
2. Check Promtail discovered it: `curl localhost:9080/targets`
3. Container logs may be empty (no output)

## 🔐 Security

- **Authentication**: Loki UI protected by Authelia 2FA
- **Network**: Isolated on `monitoring-network`
- **Encryption**: Logs stored unencrypted (considered temporary)
- **Access Control**: Only accessible via Grafana or internal network

## 📚 Additional Resources

- [Loki Documentation](https://grafana.com/docs/loki/latest/)
- [LogQL Query Language](https://grafana.com/docs/loki/latest/logql/)
- [Promtail Configuration](https://grafana.com/docs/loki/latest/clients/promtail/)
- [Prometheus Alerts for Loki](../config/prometheus/rules/miraclemax.yml)

---

**Deployed**: 2025-10-16  
**Version**: Loki 2.9.3, Promtail 2.9.3  
**Managed by**: PAI GitOps (pai-miraclemax-deploy)

