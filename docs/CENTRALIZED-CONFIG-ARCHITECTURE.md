# Centralized Configuration Architecture

**Philosophy:** Single source of truth for all service configuration  
**Pattern:** 12-factor app + GitOps + Lego simplicity  
**Result:** Services are stateless, config is centralized, deployments are reproducible

---

## The Problem

### Traditional Approach (Fragmented)
```
Service 1: Has its own config file
Service 2: Has its own config file  
Service 3: Environment variables scattered
Service 4: Hardcoded values
Service 5: Mix of all above

Result: 
- Where is X configured?
- How do I change Y?
- Which service uses Z?
- Can't replicate environment
```

### Centralized Approach (Single Source)
```
All Services → Read from → One Config File

miraclemax-config.yml:
  - Database URLs
  - API keys
  - Feature flags
  - Resource limits
  - All service settings

Result:
- All config in one place
- Easy to audit
- Easy to replicate
- GitOps-ready
```

---

## Part 1: The Central Configuration File

### Location
```
~/pai/ansible/host_vars/miraclemax-config.yml
```

### Structure
```yaml
---
# miraclemax Central Configuration
# Single source of truth for all services

# ===========================================
# Global Settings
# ===========================================
global:
  domain: jbyrd.org
  environment: production  # dev/staging/production
  timezone: America/New_York
  backup_retention_days: 7
  
# ===========================================
# Database Configuration
# ===========================================
databases:
  postgres:
    host: postgres
    port: 5432
    database: pai_db
    username: pai_user
    # Password from secrets
    max_connections: 100
    
  redis:
    host: redis
    port: 6379
    # No auth in internal network
    max_memory: 256mb
    eviction_policy: allkeys-lru

# ===========================================
# Service-Specific Configuration
# ===========================================
services:
  
  # Actual Budget
  actual_budget:
    port: 5006
    subdomain: money
    data_dir: /data
    upload_file_sync_size_limit_mb: 20
    upload_sync_encrypted_file_sync_size_limit_mb: 50
    upload_file_size_limit_mb: 20
    
  # n8n Workflow Automation
  n8n:
    port: 5678
    subdomain: n8n
    webhook_url: "https://n8n.{{ global.domain }}"
    timezone: "{{ global.timezone }}"
    basic_auth_active: false  # Use owner account
    executions_mode: queue
    queue_health_check_active: true
    # Database connection
    db_type: postgresdb
    db_postgresdb_host: "{{ databases.postgres.host }}"
    db_postgresdb_port: "{{ databases.postgres.port }}"
    db_postgresdb_database: "{{ databases.postgres.database }}"
    db_postgresdb_user: "{{ databases.postgres.username }}"
    # Redis for queue
    queue_bull_redis_host: "{{ databases.redis.host }}"
    queue_bull_redis_port: "{{ databases.redis.port }}"
    
  # Grafana
  grafana:
    port: 3000
    subdomain: grafana
    admin_user: admin
    # Admin password from secrets
    allow_sign_up: false
    # Database connection
    database_type: postgres
    database_host: "{{ databases.postgres.host }}:{{ databases.postgres.port }}"
    database_name: grafana
    database_user: "{{ databases.postgres.username }}"
    
  # Prometheus
  prometheus:
    port: 9090
    subdomain: prometheus
    retention_time: 15d
    scrape_interval: 15s
    evaluation_interval: 15s
    external_labels:
      environment: "{{ global.environment }}"
      cluster: miraclemax
    
  # Loki
  loki:
    port: 3100
    subdomain: null  # Internal only
    retention_period: 168h  # 7 days
    
  # Homer Dashboard
  homer:
    port: 8080
    subdomain: home
    title: "PAI Dashboard"
    subtitle: "Personal AI Infrastructure"
    # Logo and theme from mounted config
    
  # Portainer
  portainer:
    port: 9000
    subdomain: portainer
    logo: "https://portainer.io/images/logo.png"
    
  # Plex
  plex:
    port: 32400
    subdomain: plex
    # Claim token from secrets
    timezone: "{{ global.timezone }}"
    allowed_networks: "192.168.1.0/24"

# ===========================================
# Resource Limits (per service)
# ===========================================
resource_limits:
  actual_budget:
    memory: 256m
    cpu: 0.5
    
  n8n:
    memory: 512m
    cpu: 1.0
    
  grafana:
    memory: 512m
    cpu: 0.5
    
  prometheus:
    memory: 1g
    cpu: 1.0
    
  redis:
    memory: 256m
    cpu: 0.5
    
  postgres:
    memory: 512m
    cpu: 1.0

# ===========================================
# Traefik Configuration
# ===========================================
traefik:
  dashboard_subdomain: traefik
  letsencrypt_email: "jimmykbyrd@gmail.com"
  letsencrypt_storage: /letsencrypt/acme.json
  log_level: INFO
  access_log: true
  
# ===========================================
# Monitoring Configuration
# ===========================================
monitoring:
  # Prometheus targets (auto-discovered)
  scrape_configs:
    - job_name: podman
      static_configs:
        - targets: ['localhost:9090']
    
  # Alert rules
  alerting:
    slack_webhook_url: null  # Set if using Slack
    email_to: "jimmykbyrd@gmail.com"
    email_from: "alerts@{{ global.domain }}"
    
  # SLO targets
  slos:
    availability: 99.9  # 43 minutes/month downtime allowed
    latency_p95: 500    # 95% requests < 500ms
    error_rate: 1       # < 1% errors

# ===========================================
# Backup Configuration
# ===========================================
backups:
  enabled: true
  schedule: "0 2 * * *"  # 2 AM daily
  retention_days: "{{ global.backup_retention_days }}"
  destination: /var/backups/miraclemax
  remote_destination: null  # Set for rclone remote
  
  # What to backup
  volumes:
    - actual-budget-data
    - n8n-data
    - grafana-data
    - prometheus-data
  
  configs:
    - /home/jbyrd/miraclemax-infrastructure/config
    - /home/jbyrd/miraclemax-infrastructure/compose

# ===========================================
# Feature Flags
# ===========================================
features:
  enable_monitoring: true
  enable_backups: true
  enable_ssl: true
  enable_health_checks: true
  enable_log_aggregation: true
  
  # Experimental features
  enable_canary_deployments: false
  enable_auto_scaling: false
  enable_geo_replication: false
```

---

## Part 2: Variable Injection System

### Template for Service Compose Files

```jinja2
# roles/lego_service/templates/webapp.yml.j2
---
version: '3'

services:
  {{ item.name }}:
    image: {{ item.image }}
    container_name: {{ item.name }}
    
    # Port mapping (from central config)
    ports:
      - "{{ services[item.name].port }}:{{ services[item.name].port }}"
    
    # Environment variables (ALL from central config)
    environment:
      # Inject all service-specific variables
      {% for key, value in services[item.name].items() %}
      {% if key not in ['port', 'subdomain', 'data_dir'] %}
      {{ key | upper }}: "{{ value }}"
      {% endfor %}
      
      # Inject global variables
      TZ: "{{ global.timezone }}"
      ENVIRONMENT: "{{ global.environment }}"
      
      # Inject database connections (if service uses them)
      {% if services[item.name].db_type is defined %}
      DB_HOST: "{{ databases.postgres.host }}"
      DB_PORT: "{{ databases.postgres.port }}"
      DB_NAME: "{{ databases.postgres.database }}"
      DB_USER: "{{ databases.postgres.username }}"
      DB_PASSWORD: "{{ vault_postgres_password }}"
      {% endif %}
    
    # Volume (from central config)
    volumes:
      {% if services[item.name].data_dir is defined %}
      - {{ item.name }}-data:{{ services[item.name].data_dir }}:z
      {% endif %}
    
    # Resource limits (from central config)
    deploy:
      resources:
        limits:
          cpus: "{{ resource_limits[item.name].cpu }}"
          memory: "{{ resource_limits[item.name].memory }}"
    
    # Health check (from central config)
    {% if features.enable_health_checks %}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:{{ services[item.name].port }}/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    {% endif %}
    
    # Restart policy
    restart: unless-stopped
    
    # Labels (from central config)
    labels:
      # Traefik routing
      {% if services[item.name].subdomain %}
      traefik.enable: "true"
      traefik.http.routers.{{ item.name }}.rule: "Host(`{{ services[item.name].subdomain }}.{{ global.domain }}`)"
      traefik.http.routers.{{ item.name }}.entrypoints: "websecure"
      {% if features.enable_ssl %}
      traefik.http.routers.{{ item.name }}.tls: "true"
      traefik.http.routers.{{ item.name }}.tls.certresolver: "letsencrypt"
      {% endif %}
      traefik.http.services.{{ item.name }}.loadbalancer.server.port: "{{ services[item.name].port }}"
      {% endif %}
      
      # Monitoring
      {% if features.enable_monitoring %}
      prometheus.io/scrape: "true"
      prometheus.io/port: "{{ services[item.name].port }}"
      prometheus.io/path: "/metrics"
      {% endif %}
      
      # Logging
      {% if features.enable_log_aggregation %}
      logging.service: "{{ item.name }}"
      logging.environment: "{{ global.environment }}"
      {% endif %}

volumes:
  {{ item.name }}-data:
    driver: local
```

---

## Part 3: Service Catalog Integration

### Updated Service Catalog (References Central Config)

```yaml
# ansible/service-catalog.yml
---
# Services reference central config, no duplication

actual_budget:
  name: actual-budget
  type: webapp
  image: actualbudget/actual-server:latest
  # All other config comes from miraclemax-config.yml
  config_ref: services.actual_budget
  
n8n:
  name: n8n
  type: webapp
  image: n8nio/n8n:latest
  config_ref: services.n8n
  depends_on:
    - postgres
    - redis

grafana:
  name: grafana
  type: webapp
  image: grafana/grafana:latest
  config_ref: services.grafana
  depends_on:
    - postgres

prometheus:
  name: prometheus
  type: utility
  image: prom/prometheus:latest
  config_ref: services.prometheus

# More services...
```

---

## Part 4: Configuration Management Tools

### Tool: pai-config-show

```bash
#!/bin/bash
# bin/pai-config-show
# Show configuration for a service or all services

set -euo pipefail

CONFIG_FILE="$HOME/pai/ansible/host_vars/miraclemax-config.yml"

if [ $# -eq 0 ]; then
    # Show all config
    echo "🔧 miraclemax Central Configuration"
    echo "===================================="
    cat "$CONFIG_FILE"
else
    # Show specific service config
    SERVICE="$1"
    echo "🔧 Configuration for: $SERVICE"
    echo "===================================="
    yq eval ".services.$SERVICE" "$CONFIG_FILE"
fi
```

### Tool: pai-config-edit

```bash
#!/bin/bash
# bin/pai-config-edit
# Edit central configuration

set -euo pipefail

CONFIG_FILE="$HOME/pai/ansible/host_vars/miraclemax-config.yml"

echo "📝 Editing central configuration..."
echo "⚠️  Changes affect ALL services on miraclemax"
echo ""

# Backup before editing
cp "$CONFIG_FILE" "$CONFIG_FILE.backup.$(date +%s)"

# Open in editor
"${EDITOR:-vim}" "$CONFIG_FILE"

echo ""
echo "✅ Configuration updated"
echo "ℹ️  Backup saved: $CONFIG_FILE.backup.*"
echo ""
echo "To apply changes:"
echo "  pai-deploy"
```

### Tool: pai-config-validate

```bash
#!/bin/bash
# bin/pai-config-validate
# Validate central configuration

set -euo pipefail

CONFIG_FILE="$HOME/pai/ansible/host_vars/miraclemax-config.yml"

echo "🔍 Validating configuration..."
echo ""

# Check YAML syntax
if yq eval '.' "$CONFIG_FILE" >/dev/null 2>&1; then
    echo "✅ YAML syntax valid"
else
    echo "❌ YAML syntax error"
    exit 1
fi

# Check required fields
required_fields=(
    "global.domain"
    "global.environment"
    "databases.postgres.host"
    "databases.redis.host"
)

all_valid=true
for field in "${required_fields[@]}"; do
    if yq eval ".$field" "$CONFIG_FILE" | grep -q "null"; then
        echo "❌ Missing required field: $field"
        all_valid=false
    else
        echo "✅ Required field present: $field"
    fi
done

# Check service references
echo ""
echo "🔍 Checking service references..."

for service in $(yq eval '.services | keys | .[]' "$CONFIG_FILE"); do
    if yq eval ".services.$service.port" "$CONFIG_FILE" | grep -q "null"; then
        echo "⚠️  Service $service missing port"
    else
        echo "✅ Service $service configured"
    fi
done

if [ "$all_valid" = true ]; then
    echo ""
    echo "✅ Configuration valid"
    exit 0
else
    echo ""
    echo "❌ Configuration has errors"
    exit 1
fi
```

### Tool: pai-config-diff

```bash
#!/bin/bash
# bin/pai-config-diff
# Show configuration differences

set -euo pipefail

CONFIG_FILE="$HOME/pai/ansible/host_vars/miraclemax-config.yml"

echo "📊 Configuration Changes"
echo "======================="
echo ""

# Show git diff if in git repo
if git rev-parse --git-dir > /dev/null 2>&1; then
    git diff "$CONFIG_FILE" || echo "No changes"
else
    # Compare with latest backup
    latest_backup=$(ls -t "$CONFIG_FILE.backup."* 2>/dev/null | head -1)
    if [ -n "$latest_backup" ]; then
        diff -u "$latest_backup" "$CONFIG_FILE" || echo "No changes"
    else
        echo "No backup found for comparison"
    fi
fi
```

### Tool: pai-config-export

```bash
#!/bin/bash
# bin/pai-config-export
# Export configuration for different environments

set -euo pipefail

CONFIG_FILE="$HOME/pai/ansible/host_vars/miraclemax-config.yml"
ENVIRONMENT="${1:-production}"

echo "📦 Exporting configuration for: $ENVIRONMENT"
echo ""

# Create export with environment-specific values
OUTPUT_FILE="/tmp/miraclemax-config-${ENVIRONMENT}-$(date +%Y%m%d-%H%M%S).yml"

# Copy and modify for environment
yq eval ".global.environment = \"$ENVIRONMENT\"" "$CONFIG_FILE" > "$OUTPUT_FILE"

echo "✅ Configuration exported: $OUTPUT_FILE"
echo ""
echo "To deploy to different environment:"
echo "  1. Copy to target host"
echo "  2. Place in ~/pai/ansible/host_vars/"
echo "  3. Run pai-deploy"
```

---

## Part 5: Environment Management

### Multiple Environments from Same Config

```yaml
# ansible/host_vars/miraclemax-dev-config.yml
# Development environment (extends base config)
---
global:
  domain: dev.jbyrd.org
  environment: development
  
# Override specific services for dev
services:
  actual_budget:
    subdomain: money-dev
    
  n8n:
    subdomain: n8n-dev
    executions_mode: regular  # No queue in dev
    
# Lower resource limits for dev
resource_limits:
  actual_budget:
    memory: 128m
    cpu: 0.25
    
# Disable expensive features in dev
features:
  enable_monitoring: false
  enable_backups: false
  enable_log_aggregation: false
```

### Deployment by Environment

```bash
# Deploy to production
ansible-playbook playbooks/miraclemax.yml -e @host_vars/miraclemax-config.yml

# Deploy to dev
ansible-playbook playbooks/miraclemax.yml -e @host_vars/miraclemax-dev-config.yml
```

---

## Part 6: Secrets Management

### Sensitive Values (Separate from Config)

```yaml
# ansible/host_vars/miraclemax-secrets.yml (encrypted with ansible-vault)
---
vault_postgres_password: "supersecret123"
vault_grafana_admin_password: "admin123"
vault_plex_claim_token: "claim-xxx"
vault_n8n_encryption_key: "encryption-key-xxx"

# Slack/PagerDuty webhooks
vault_slack_webhook_url: "https://hooks.slack.com/xxx"
vault_pagerduty_api_key: "xxx"
```

### Encrypt Secrets

```bash
# Create encrypted secrets file
ansible-vault create ansible/host_vars/miraclemax-secrets.yml

# Edit encrypted secrets
ansible-vault edit ansible/host_vars/miraclemax-secrets.yml

# Deploy with secrets
ansible-playbook playbooks/miraclemax.yml --ask-vault-pass
```

### Reference Secrets in Templates

```jinja2
# In service template
environment:
  DB_PASSWORD: "{{ vault_postgres_password }}"
  ADMIN_PASSWORD: "{{ vault_grafana_admin_password }}"
```

---

## Part 7: Benefits

### Single Source of Truth

**Before (Fragmented):**
```
Where is database URL configured?
- Check n8n compose file
- Check grafana compose file
- Check 5 other files
- Values might be different!
```

**After (Centralized):**
```
All in one place: miraclemax-config.yml
databases:
  postgres:
    host: postgres
    port: 5432

All services reference the same value.
```

### Easy Environment Replication

**Clone entire environment:**
```bash
# Export production config
pai-config-export production

# Modify for staging
# Change: global.domain, global.environment

# Deploy to staging host
ansible-playbook -i staging playbooks/miraclemax.yml
```

### GitOps Ready

```bash
# All configuration in git
git add ansible/host_vars/miraclemax-config.yml
git commit -m "Updated n8n memory limit"
git push

# CI/CD automatically deploys
ansible-playbook playbooks/miraclemax.yml
```

### Configuration Auditing

```bash
# Who changed what when?
git log -p ansible/host_vars/miraclemax-config.yml

# What's different between environments?
diff host_vars/miraclemax-config.yml host_vars/miraclemax-dev-config.yml
```

---

## Part 8: Integration with Lego System

### Lego Block + Central Config = Perfect

**Service catalog (what to deploy):**
```yaml
actual_budget:
  name: actual-budget
  type: webapp
  image: actualbudget/actual-server:latest
```

**Central config (how to deploy):**
```yaml
services:
  actual_budget:
    port: 5006
    subdomain: money
    memory: 256m
    # All configuration
```

**Result:**
```bash
pai-service-add actual-budget
# ↓
# Reads catalog (what)
# Reads config (how)
# Generates fully-configured compose file
# Deploys with all settings
```

---

## Part 9: Configuration Schema

### Enforce Structure with Schema Validation

```yaml
# ansible/config-schema.yml
---
type: object
required: [global, databases, services]
properties:
  global:
    type: object
    required: [domain, environment, timezone]
    properties:
      domain:
        type: string
        pattern: "^[a-z0-9.-]+$"
      environment:
        type: string
        enum: [development, staging, production]
      timezone:
        type: string
  
  databases:
    type: object
    required: [postgres, redis]
  
  services:
    type: object
    patternProperties:
      ".*":
        type: object
        required: [port, subdomain]
```

### Validate Against Schema

```bash
#!/bin/bash
# Validate config against schema
yq eval -o=json miraclemax-config.yml | \
  ajv validate -s config-schema.yml -d -
```

---

## Part 10: Real-World Example

### Adding New Service with Central Config

**Step 1: Add to catalog**
```yaml
# ansible/service-catalog.yml
jellyfin:
  name: jellyfin
  type: webapp
  image: jellyfin/jellyfin:latest
```

**Step 2: Add config (one place)**
```yaml
# ansible/host_vars/miraclemax-config.yml
services:
  jellyfin:
    port: 8096
    subdomain: media
    transcoding_threads: 2
    cache_path: /cache

resource_limits:
  jellyfin:
    memory: 2g
    cpu: 2.0
```

**Step 3: Deploy**
```bash
pai-service-add jellyfin
pai-deploy
```

**What gets generated automatically:**
- Docker Compose file with all variables injected
- Traefik routing (media.jbyrd.org)
- SSL certificate
- Health checks
- Resource limits
- Monitoring labels
- Logging configuration
- Backup schedule

**Manual configuration needed:** 0 lines ✅

---

## Bottom Line

### Traditional Microservices (Fragmented Config)

```
Service 1 config: compose file 1
Service 2 config: compose file 2
Service 3 config: .env file
Service 4 config: hardcoded
Service 5 config: mix of all

Result:
- Hard to find values
- Inconsistencies
- Can't replicate
- Not GitOps-ready
```

### PAI Microservices (Centralized Config)

```
All Services → miraclemax-config.yml

One file contains:
- All ports
- All URLs
- All limits
- All features
- All settings

Result:
- Single source of truth
- Easy to audit
- Easy to replicate
- GitOps-ready
- Ansible-native
```

### The Formula

```
Service Catalog (what to deploy)
+
Central Config (how to deploy)
+
Lego Templates (auto-wiring)
=
Zero-config deployments with complete control
```

**Configuration:** 1 file  
**Deployment:** 1 command (`pai-deploy`)  
**Result:** All services configured consistently

---

*Philosophy: Configuration as Code + Single Source of Truth*  
*Pattern: 12-Factor App + GitOps + Lego Simplicity*  
*Result: Services are stateless, config is centralized*
