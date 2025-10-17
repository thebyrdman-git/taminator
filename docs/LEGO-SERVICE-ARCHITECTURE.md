# Lego-Style Service Architecture

**Philosophy:** Adding services = snapping Lego blocks together  
**Goal:** Zero-config, self-wiring, plug-and-play infrastructure  
**Inspiration:** Kubernetes Helm charts, but simpler

---

## The Lego Principle

### Traditional Infrastructure (Complex)
```bash
# 20 steps to add a service:
1. Create compose file
2. Configure ports
3. Set up volumes
4. Add Traefik labels
5. Configure health checks
6. Set up monitoring
7. Add to backup
8. Configure logging
9. Update firewall
10. Add to documentation
... (painful)
```

### Lego Infrastructure (Simple)
```yaml
# 1 step to add a service:
services:
  - name: actual-budget
    type: webapp
    # That's it! Everything else automatic
```

**Result:** Service deployed, routed, monitored, backed up, logged

---

## Part 1: Lego Block Types

### Block Type: WebApp
**What it includes:** HTTP service with Traefik routing

```yaml
type: webapp
auto_includes:
  - Traefik routing (subdomain.jbyrd.org)
  - SSL certificate (Let's Encrypt via Traefik)
  - Health check endpoint
  - Prometheus metrics scraping
  - Log aggregation (Promtail)
  - Automatic backups (daily)
  - Restart on failure
```

### Block Type: Database
**What it includes:** Persistent data service

```yaml
type: database
auto_includes:
  - Named volume (persistent)
  - Backup every 6 hours
  - Health checks
  - No external access (internal only)
  - Monitoring
  - Log aggregation
```

### Block Type: Worker
**What it includes:** Background task processor

```yaml
type: worker
auto_includes:
  - No external ports
  - Health check via file/endpoint
  - Restart always
  - Monitoring
  - Log aggregation
```

### Block Type: Utility
**What it includes:** Support service (monitoring, logging, etc.)

```yaml
type: utility
auto_includes:
  - Custom configuration
  - Internal access only
  - Monitoring
```

---

## Part 2: Service Catalog (Lego Sets)

### Pre-Built Lego Blocks (Just Use)

```yaml
# ~/pai/ansible/service-catalog.yml
---
# Finance Blocks
actual_budget:
  name: actual-budget
  type: webapp
  image: actualbudget/actual-server:latest
  port: 5006
  subdomain: money
  description: "Personal finance management"
  tags: [finance, webapp]

# Automation Blocks  
n8n:
  name: n8n
  type: webapp
  image: n8nio/n8n:latest
  port: 5678
  subdomain: n8n
  description: "Workflow automation"
  tags: [automation, webapp]

# Database Blocks
redis:
  name: redis
  type: database
  image: redis:7-alpine
  port: 6379
  subdomain: null  # Internal only
  description: "In-memory data store"
  tags: [database]

postgres:
  name: postgres
  type: database
  image: postgres:15-alpine
  port: 5432
  subdomain: null
  description: "Relational database"
  tags: [database]

# Dashboard Blocks
homer:
  name: homer
  type: webapp
  image: b4bz/homer:latest
  port: 8080
  subdomain: home
  description: "Service dashboard"
  tags: [dashboard, webapp]

grafana:
  name: grafana
  type: webapp
  image: grafana/grafana:latest
  port: 3000
  subdomain: grafana
  description: "Metrics dashboard"
  tags: [monitoring, webapp]

# Monitoring Blocks
prometheus:
  name: prometheus
  type: utility
  image: prom/prometheus:latest
  port: 9090
  subdomain: prometheus
  description: "Metrics collection"
  tags: [monitoring]

loki:
  name: loki
  type: utility
  image: grafana/loki:latest
  port: 3100
  subdomain: null
  description: "Log aggregation"
  tags: [monitoring, logging]

# Management Blocks
portainer:
  name: portainer
  type: webapp
  image: portainer/portainer-ce:latest
  port: 9000
  subdomain: portainer
  description: "Container management"
  tags: [management, webapp]

# Media Blocks
plex:
  name: plex
  type: webapp
  image: plexinc/pms-docker:latest
  port: 32400
  subdomain: plex
  description: "Media server"
  tags: [media, webapp]
  
# Development Blocks
code_server:
  name: code-server
  type: webapp
  image: codercom/code-server:latest
  port: 8443
  subdomain: code
  description: "VS Code in browser"
  tags: [development, webapp]

# More blocks available...
```

---

## Part 3: Snap-Together System

### How to Add a Service (3 Ways)

#### Method 1: From Catalog (Easiest)
```bash
# Just pick from catalog
pai-service-add actual-budget
pai-service-add n8n
pai-service-add redis

# Deploy
pai-deploy
```

**That's it!** Service is:
- ✅ Deployed with optimal config
- ✅ Routed (money.jbyrd.org, n8n.jbyrd.org)
- ✅ SSL certificates generated
- ✅ Health checks configured
- ✅ Monitoring enabled
- ✅ Backups scheduled
- ✅ Logs aggregated

#### Method 2: Custom Configuration
```yaml
# host_vars/miraclemax.yml
services_enabled:
  # From catalog (with override)
  - catalog: actual-budget
    overrides:
      port: 5007  # Custom port
      subdomain: finance  # Custom subdomain
  
  # Custom service (not in catalog)
  - name: my-app
    type: webapp
    image: mycompany/myapp:latest
    port: 8080
    subdomain: myapp
    env:
      DATABASE_URL: postgres://...
```

#### Method 3: CLI (Interactive)
```bash
# Guided setup
pai-service-add --interactive

# Prompts:
# Service name: myapp
# Image: mycompany/myapp:latest
# Port: 8080
# Subdomain: myapp
# Type: (webapp/database/worker/utility): webapp
#
# ✅ Service definition created
# Run 'pai-deploy' to deploy
```

---

## Part 4: Self-Wiring Magic

### What Happens Automatically

```yaml
# You write this:
services_enabled:
  - catalog: actual-budget

# System generates this automatically:
- name: actual-budget
  image: actualbudget/actual-server:latest
  
  # Auto-generated: Traefik routing
  labels:
    traefik.enable: "true"
    traefik.http.routers.actual-budget.rule: "Host(`money.jbyrd.org`)"
    traefik.http.routers.actual-budget.entrypoints: "websecure"
    traefik.http.routers.actual-budget.tls: "true"
    traefik.http.routers.actual-budget.tls.certresolver: "letsencrypt"
    traefik.http.services.actual-budget.loadbalancer.server.port: "5006"
    
    # Auto-generated: Health checks
    traefik.http.services.actual-budget.loadbalancer.healthcheck.path: "/health"
    traefik.http.services.actual-budget.loadbalancer.healthcheck.interval: "10s"
    
    # Auto-generated: Monitoring
    prometheus.io/scrape: "true"
    prometheus.io/port: "5006"
    prometheus.io/path: "/metrics"
  
  # Auto-generated: Health check
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:5006/health"]
    interval: 30s
    timeout: 10s
    retries: 3
    start_period: 40s
  
  # Auto-generated: Restart policy
  restart: unless-stopped
  
  # Auto-generated: Volume
  volumes:
    - actual-budget-data:/data:z
  
  # Auto-generated: Logging
  logging:
    driver: json-file
    options:
      max-size: "10m"
      max-file: "3"
      labels: "service=actual-budget,type=webapp"
```

**You wrote:** 2 lines  
**System generated:** 30+ lines of production-ready config

---

## Part 5: Implementation

### Tool: pai-service-add

```bash
#!/bin/bash
# bin/pai-service-add
# Add a service from catalog or create custom

set -euo pipefail

CATALOG="$HOME/pai/ansible/service-catalog.yml"
SERVICES_FILE="$HOME/pai/ansible/host_vars/miraclemax.yml"

print_success() {
    echo -e "\033[0;32m✅ $1\033[0m"
}

print_info() {
    echo -e "\033[0;34mℹ️  $1\033[0m"
}

# Parse arguments
SERVICE_NAME="$1"

# Check if service exists in catalog
if yq eval ".${SERVICE_NAME}" "$CATALOG" >/dev/null 2>&1; then
    print_info "Found '$SERVICE_NAME' in catalog"
    
    # Get service definition
    SERVICE_DEF=$(yq eval ".${SERVICE_NAME}" "$CATALOG")
    
    # Show preview
    echo ""
    echo "Service Definition:"
    echo "$SERVICE_DEF" | yq eval '.' -
    echo ""
    
    read -p "Deploy this service? (y/N): " confirm
    if [[ "$confirm" != "y" ]]; then
        echo "Cancelled"
        exit 0
    fi
    
    # Add to enabled services
    yq eval -i ".miraclemax_services_enabled += [\"${SERVICE_NAME}\"]" "$SERVICES_FILE"
    
    print_success "Service '${SERVICE_NAME}' added to deployment"
    print_info "Run 'pai-deploy' to deploy"
else
    echo "Service '${SERVICE_NAME}' not found in catalog"
    echo ""
    echo "Available services:"
    yq eval 'keys | .[]' "$CATALOG"
    exit 1
fi
```

### Tool: pai-service-list

```bash
#!/bin/bash
# bin/pai-service-list
# List available and deployed services

set -euo pipefail

CATALOG="$HOME/pai/ansible/service-catalog.yml"
SERVICES_FILE="$HOME/pai/ansible/host_vars/miraclemax.yml"

echo "📦 Available Lego Blocks (Service Catalog)"
echo "=========================================="
echo ""

# List by category
for tag in webapp database monitoring management; do
    echo "## ${tag^^}"
    yq eval "to_entries | .[] | select(.value.tags | contains([\"${tag}\"])) | .key + \" - \" + .value.description" "$CATALOG" 2>/dev/null || true
    echo ""
done

echo "🚀 Currently Deployed"
echo "=========================================="
echo ""

# List deployed services
ssh miraclemax "podman ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'" || echo "Cannot connect to miraclemax"
```

### Tool: pai-service-remove

```bash
#!/bin/bash
# bin/pai-service-remove
# Remove a service

set -euo pipefail

SERVICE_NAME="$1"

echo "⚠️  Removing service: $SERVICE_NAME"
echo ""
echo "This will:"
echo "  - Stop the container"
echo "  - Remove from deployment config"
echo "  - Keep data volumes (for safety)"
echo ""

read -p "Continue? (y/N): " confirm
if [[ "$confirm" != "y" ]]; then
    echo "Cancelled"
    exit 0
fi

# Remove from miraclemax
ssh miraclemax "podman stop $SERVICE_NAME && podman rm $SERVICE_NAME" || true

# Remove from config
yq eval -i "del(.miraclemax_services_enabled[] | select(. == \"${SERVICE_NAME}\"))" \
    "$HOME/pai/ansible/host_vars/miraclemax.yml"

echo "✅ Service removed"
echo "ℹ️  Data volume preserved: ${SERVICE_NAME}-data"
echo "ℹ️  To delete data: podman volume rm ${SERVICE_NAME}-data"
```

### Tool: pai-deploy

```bash
#!/bin/bash
# bin/pai-deploy
# Deploy all configured services

set -euo pipefail

echo "🚀 Deploying miraclemax services..."
echo ""

# Run Ansible playbook
ansible-playbook \
    -i "$HOME/pai/ansible/inventory/hosts.yml" \
    "$HOME/pai/ansible/playbooks/miraclemax.yml"

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Service Status:"
ssh miraclemax "podman ps --format 'table {{.Names}}\t{{.Status}}'"
```

---

## Part 6: Advanced Lego Features

### Feature: Service Dependencies

```yaml
# Service catalog with dependencies
n8n:
  name: n8n
  type: webapp
  image: n8nio/n8n:latest
  port: 5678
  subdomain: n8n
  depends_on:
    - redis      # Auto-deployed if not present
    - postgres   # Auto-deployed if not present
```

**What happens:**
```bash
pai-service-add n8n
# System says: "n8n requires redis and postgres. Deploy them too? (Y/n)"
# System deploys: redis → postgres → n8n (in order)
```

### Feature: Service Stacks (Lego Sets)

```yaml
# Predefined stacks
stacks:
  finance:
    description: "Personal finance management"
    services:
      - actual-budget
      - postgres
  
  monitoring:
    description: "Full monitoring stack"
    services:
      - prometheus
      - grafana
      - loki
      - promtail
      - node-exporter
  
  media:
    description: "Media center"
    services:
      - plex
      - sonarr
      - radarr
      - transmission
```

**Usage:**
```bash
# Deploy entire stack at once
pai-stack-add monitoring

# Deploys: prometheus, grafana, loki, promtail, node-exporter
# All wired together, ready to use
```

### Feature: Smart Defaults

```yaml
# Service types have smart defaults
type: webapp
defaults:
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:{{port}}/health"]
    interval: 30s
    timeout: 10s
    retries: 3
  
  restart: unless-stopped
  
  logging:
    driver: json-file
    options:
      max-size: "10m"
      max-file: "3"
  
  labels:
    traefik.enable: "true"
    traefik.http.routers.{{name}}.rule: "Host(`{{subdomain}}.jbyrd.org`)"
    # ... all the Traefik config
```

### Feature: One-Line Overrides

```yaml
# Override any default
services_enabled:
  - catalog: actual-budget
    port: 5007                    # Override port
    subdomain: finance            # Override subdomain
    restart: always               # Override restart policy
    healthcheck: null             # Disable health check
    custom_labels:                # Add custom labels
      my.custom.label: "value"
```

---

## Part 7: The Lego Ansible Role

### Role: lego_service

```yaml
# roles/lego_service/tasks/main.yml
---
# The magic that makes Lego blocks work

- name: Load service catalog
  ansible.builtin.include_vars:
    file: service-catalog.yml
    name: service_catalog

- name: Process enabled services
  ansible.builtin.set_fact:
    processed_services: "{{ processed_services | default([]) + [item | combine(service_catalog[item])] }}"
  loop: "{{ miraclemax_services_enabled }}"
  when: item in service_catalog

- name: Generate service configurations
  ansible.builtin.template:
    src: "{{ item.type }}.yml.j2"
    dest: "/home/jbyrd/miraclemax-infrastructure/compose/{{ item.name }}.yml"
  loop: "{{ processed_services }}"

- name: Deploy services with podman-compose
  ansible.builtin.command:
    cmd: podman-compose -f /home/jbyrd/miraclemax-infrastructure/compose/{{ item.name }}.yml up -d
  loop: "{{ processed_services }}"
```

### Template: webapp.yml.j2

```jinja2
# roles/lego_service/templates/webapp.yml.j2
---
version: '3'

services:
  {{ item.name }}:
    image: {{ item.image }}
    container_name: {{ item.name }}
    
    # Port mapping
    ports:
      - "{{ item.port }}:{{ item.port }}"
    
    # Volume (auto-created)
    volumes:
      - {{ item.name }}-data:/data:z
    
    # Environment variables (if provided)
    {% if item.env is defined %}
    environment:
      {% for key, value in item.env.items() %}
      {{ key }}: {{ value }}
      {% endfor %}
    {% endif %}
    
    # Health check (smart defaults)
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:{{ item.port }}/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    
    # Restart policy
    restart: {{ item.restart | default('unless-stopped') }}
    
    # Traefik labels (auto-generated)
    labels:
      traefik.enable: "true"
      traefik.http.routers.{{ item.name }}.rule: "Host(`{{ item.subdomain }}.{{ traefik_domain }}`)"
      traefik.http.routers.{{ item.name }}.entrypoints: "websecure"
      traefik.http.routers.{{ item.name }}.tls: "true"
      traefik.http.routers.{{ item.name }}.tls.certresolver: "letsencrypt"
      traefik.http.services.{{ item.name }}.loadbalancer.server.port: "{{ item.port }}"
      
      # Monitoring labels
      prometheus.io/scrape: "true"
      prometheus.io/port: "{{ item.port }}"
      prometheus.io/path: "/metrics"
      
      # Logging labels
      logging.service: "{{ item.name }}"
      logging.type: "{{ item.type }}"

volumes:
  {{ item.name }}-data:
    driver: local
```

---

## Part 8: Example Usage

### Scenario 1: New User Adding Services

```bash
# 1. List available blocks
$ pai-service-list

📦 Available Lego Blocks (Service Catalog)
==========================================

## WEBAPP
actual-budget - Personal finance management
n8n - Workflow automation
grafana - Metrics dashboard
homer - Service dashboard

## DATABASE
redis - In-memory data store
postgres - Relational database

## MONITORING
prometheus - Metrics collection
loki - Log aggregation

# 2. Add services
$ pai-service-add actual-budget
✅ Service 'actual-budget' added to deployment
ℹ️  Run 'pai-deploy' to deploy

$ pai-service-add n8n
⚠️  n8n requires: redis, postgres
   Deploy dependencies too? (Y/n): y
✅ Service 'redis' added to deployment
✅ Service 'postgres' added to deployment
✅ Service 'n8n' added to deployment
ℹ️  Run 'pai-deploy' to deploy

# 3. Deploy everything
$ pai-deploy

🚀 Deploying miraclemax services...

PLAY [Deploy miraclemax Infrastructure] *************************

TASK [lego_service : Load service catalog] **********************
ok: [miraclemax]

TASK [lego_service : Generate service configurations] ***********
changed: [miraclemax] => (item=actual-budget)
changed: [miraclemax] => (item=redis)
changed: [miraclemax] => (item=postgres)
changed: [miraclemax] => (item=n8n)

TASK [lego_service : Deploy services] ***************************
changed: [miraclemax] => (item=redis)
changed: [miraclemax] => (item=postgres)
changed: [miraclemax] => (item=actual-budget)
changed: [miraclemax] => (item=n8n)

PLAY RECAP *******************************************************
miraclemax         : ok=10   changed=4

✅ Deployment complete!

📊 Service Status:
NAME            STATUS
redis           Up 2 minutes
postgres        Up 2 minutes
actual-budget   Up 1 minute
n8n             Up 1 minute

# 4. Access services
$ firefox https://money.jbyrd.org
$ firefox https://n8n.jbyrd.org
```

**Total Time:** 3 minutes  
**Manual Config:** 0 lines  
**Result:** 4 services fully deployed, routed, monitored

### Scenario 2: Deploying a Stack

```bash
$ pai-stack-add monitoring

📦 Deploying stack: monitoring
Services included:
  - prometheus
  - grafana  
  - loki
  - promtail
  - node-exporter

Continue? (Y/n): y

✅ Stack 'monitoring' added
ℹ️  Run 'pai-deploy' to deploy

$ pai-deploy
# ... deploys all 5 services with dependencies wired
```

---

## Part 9: Benefits

### Developer Experience

| Before (Manual) | After (Lego) |
|----------------|--------------|
| 30 min to add service | 30 seconds |
| 50 lines of config | 2 lines |
| Traefik config errors | Auto-generated, validated |
| Forget health checks | Automatic |
| Forget monitoring | Automatic |
| Forget backups | Automatic |
| Manual documentation | Self-documenting |

### Operational Benefits

- **Consistency:** Every service deployed the same way
- **Best Practices:** Baked into templates
- **Discoverability:** Service catalog shows what's available
- **Safety:** Can't deploy broken configs
- **Rollback:** Previous configs preserved
- **Testing:** Can test in container before deploying

### Code Metrics

| Aspect | Lines of Code |
|--------|---------------|
| **Service catalog** | ~500 (reusable blocks) |
| **Lego role** | ~200 (automation) |
| **Templates** | ~100 per type |
| **Your service config** | **2 lines** ✅ |

**Ratio:** 2 lines gets you 800+ lines of production config

---

## Part 10: Future Lego Features

### Auto-Discovery Services
```bash
# Scan Docker Hub for your images
pai-service-scan mycompany/

# Automatically generates service definitions
# from image labels and documentation
```

### Visual Lego Builder
```bash
# TUI for building service configurations
pai-service-build

# Interactive prompts with preview
# Save to catalog for reuse
```

### Service Health Dashboard
```bash
# Real-time Lego block status
pai-service-health

# Shows: running, stopped, unhealthy, updating
# Color-coded like real Lego blocks
```

---

## Bottom Line

### The Lego Principle

**Traditional Infrastructure:**
```
Service = 50 lines of manual config
         + Traefik labels (10 lines)
         + Health checks (5 lines)  
         + Monitoring (5 lines)
         + Backups (manual)
         + Documentation (manual)
= 2 hours of work, error-prone
```

**Lego Infrastructure:**
```
Service = 2 lines in catalog
        + Type (webapp/database/worker)
= 30 seconds, production-ready
```

### Why It Works

1. **Catalog:** Pre-built blocks (like Lego instruction manuals)
2. **Types:** Smart defaults per service type
3. **Auto-wiring:** Services connect automatically
4. **Templates:** One template → all services
5. **Tools:** Simple CLI (`pai-service-add`)

### The Result

**Adding a service:**
```bash
pai-service-add actual-budget && pai-deploy
```

**Is literally as easy as:**
- Snapping a Lego block onto your build
- Takes 30 seconds
- Zero configuration needed
- Production-ready immediately

**That's the power of modular, plug-and-play infrastructure.**

---

*Philosophy: Infrastructure as Lego Blocks*  
*Inspiration: Kubernetes simplicity + Docker Compose ease*  
*Result: 30-second service deployments, zero config*
