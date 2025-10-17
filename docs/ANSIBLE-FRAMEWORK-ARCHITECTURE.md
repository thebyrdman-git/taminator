# Pure Ansible Framework: Clone & Deploy in Minutes

**Goal:** Friend clones repo → Edits one config file → Runs one command → Full stack deployed  
**Philosophy:** 100% Ansible, 0% custom scripts, infinitely replicable  
**Speed:** 5 minutes to understand, 10 minutes to deploy

---

## The Vision

### Your Friend's Experience

```bash
# Day 1, Minute 1: Clone your framework
git clone https://github.com/jbyrd/pai-ansible-framework.git
cd pai-ansible-framework

# Minute 2: Edit ONE file with their settings
vim inventory/my-server.yml
# Change: server IP, domain name, which services to enable

# Minute 3: Deploy everything
ansible-playbook site.yml

# Minutes 4-10: Watch Ansible deploy their entire infrastructure
# - Install Docker/Podman
# - Set up Traefik with SSL
# - Deploy all selected services
# - Configure monitoring
# - Set up backups
# Done!

# Result: https://money.their-domain.com works
#         https://n8n.their-domain.com works
#         https://grafana.their-domain.com works
#         All with SSL, monitoring, backups
```

**That's it. Zero custom scripts. Pure Ansible.**

---

## Part 1: Repository Structure

### The Complete Framework

```
pai-ansible-framework/
├── README.md                    # "Clone, edit, deploy"
├── ansible.cfg                  # Ansible configuration
├── site.yml                     # Master playbook (one command to rule them all)
│
├── inventory/
│   ├── example-server.yml       # Template for users to copy
│   └── my-server.yml            # User's actual config (gitignored)
│
├── group_vars/
│   ├── all.yml                  # Defaults for everyone
│   └── services.yml             # Service catalog (what's available)
│
├── playbooks/
│   ├── 01-bootstrap.yml         # Install Ansible dependencies
│   ├── 02-infrastructure.yml    # Docker, Podman, security
│   ├── 03-traefik.yml           # Reverse proxy + SSL
│   ├── 04-services.yml          # Deploy selected services
│   ├── 05-monitoring.yml        # Prometheus, Grafana, Loki
│   └── 06-backups.yml           # Automated backup system
│
├── roles/
│   ├── service_webapp/          # Generic webapp service
│   ├── service_database/        # Generic database service
│   ├── service_worker/          # Generic worker service
│   └── service_utility/         # Generic utility service
│
├── templates/
│   ├── traefik.yml.j2           # Traefik config
│   ├── prometheus.yml.j2        # Prometheus config
│   └── docker-compose.yml.j2    # Generic compose template
│
└── docs/
    ├── QUICKSTART.md            # 5-minute guide
    ├── SERVICES.md              # Available services
    └── CUSTOMIZATION.md         # How to add services
```

---

## Part 2: User's Single Configuration File

### `inventory/my-server.yml` (The ONLY File Users Edit)

```yaml
---
# Your Server Configuration
# Edit this file, then run: ansible-playbook site.yml

all:
  hosts:
    myserver:
      # ===========================================
      # Basic Settings (REQUIRED)
      # ===========================================
      ansible_host: 192.168.1.100       # Your server IP
      ansible_user: myuser                # SSH user
      ansible_become: true                # Use sudo
      
      # Domain Configuration
      domain: mywebsite.com               # Your domain
      letsencrypt_email: me@mywebsite.com # For SSL certs
      
      # ===========================================
      # Services to Deploy (Pick & Choose)
      # ===========================================
      services_enabled:
        # Finance
        - actual-budget      # Personal finance
        
        # Automation
        - n8n                # Workflow automation
        
        # Monitoring (recommended)
        - grafana            # Dashboards
        - prometheus         # Metrics
        - loki               # Logs
        
        # Management
        - homer              # Service dashboard
        - portainer          # Container management
        
        # Media (optional)
        # - plex             # Media server
        # - jellyfin         # Open source media
        
        # Development (optional)
        # - code-server      # VS Code in browser
        # - gitea            # Git server
      
      # ===========================================
      # Service Configuration (Optional Overrides)
      # ===========================================
      service_config:
        # Override defaults for specific services
        actual_budget:
          subdomain: money        # Access at money.mywebsite.com
          # port: 5006            # Use default
          
        n8n:
          subdomain: automation   # Access at automation.mywebsite.com
          memory_limit: 1g        # Give it more RAM
          
        grafana:
          subdomain: metrics
          # All other settings from defaults
      
      # ===========================================
      # Features (Enable/Disable)
      # ===========================================
      features:
        ssl_enabled: true              # Let's Encrypt SSL
        monitoring_enabled: true       # Prometheus + Grafana
        backups_enabled: true          # Daily backups
        log_aggregation: true          # Centralized logs
        
      # ===========================================
      # Resource Limits (Optional)
      # ===========================================
      default_memory_limit: 512m
      default_cpu_limit: 1.0
      
      # ===========================================
      # Backup Configuration (Optional)
      # ===========================================
      backup_schedule: "0 2 * * *"   # 2 AM daily
      backup_retention_days: 7
      # backup_remote: "s3://my-bucket"  # Optional: remote backup
```

**That's it!** One file, their entire infrastructure defined.

---

## Part 3: The Master Playbook

### `site.yml` (One Command to Deploy Everything)

```yaml
---
# PAI Ansible Framework - Master Playbook
# Usage: ansible-playbook site.yml

- name: PAI Infrastructure Deployment
  hosts: all
  become: true
  
  vars_prompt:
    - name: confirm_deployment
      prompt: "Deploy to {{ inventory_hostname }} ({{ ansible_host }})? (yes/no)"
      private: no
      default: "no"
  
  pre_tasks:
    - name: Verify confirmation
      fail:
        msg: "Deployment cancelled"
      when: confirm_deployment != "yes"
    
    - name: Display deployment info
      debug:
        msg: |
          Deploying PAI Infrastructure
          =============================
          Target: {{ inventory_hostname }}
          IP: {{ ansible_host }}
          Domain: {{ domain }}
          Services: {{ services_enabled | length }} selected
          
          This will:
          - Install Docker/Podman
          - Set up Traefik (reverse proxy + SSL)
          - Deploy {{ services_enabled | length }} services
          - Configure monitoring
          - Set up automated backups
          
          Estimated time: 10-15 minutes
  
  roles:
    # Phase 1: Bootstrap (Geerling's roles)
    - role: geerlingguy.docker
      tags: [bootstrap, docker]
    
    - role: geerlingguy.security
      tags: [bootstrap, security]
    
    - role: geerlingguy.firewall
      tags: [bootstrap, firewall]
    
    # Phase 2: Infrastructure
    - role: traefik
      tags: [infrastructure, traefik]
      when: features.ssl_enabled | default(true)
    
    # Phase 3: Services (our generic roles)
    - role: service_deploy
      tags: [services]
      loop: "{{ services_enabled }}"
      loop_control:
        loop_var: service_name
    
    # Phase 4: Monitoring
    - role: monitoring_stack
      tags: [monitoring]
      when: features.monitoring_enabled | default(true)
    
    # Phase 5: Backups
    - role: backup_system
      tags: [backups]
      when: features.backups_enabled | default(true)
  
  post_tasks:
    - name: Display deployment summary
      debug:
        msg: |
          ✅ Deployment Complete!
          
          Services deployed:
          {% for service in services_enabled %}
          - {{ service }}: https://{{ service_config[service].subdomain | default(service) }}.{{ domain }}
          {% endfor %}
          
          Management URLs:
          - Dashboard: https://home.{{ domain }}
          - Traefik: https://traefik.{{ domain }}
          {% if 'grafana' in services_enabled %}
          - Grafana: https://grafana.{{ domain }}
          {% endif %}
          
          Next steps:
          1. Visit https://home.{{ domain }} for service dashboard
          2. Check https://grafana.{{ domain }} for metrics
          3. Backups run daily at {{ backup_schedule }}
```

---

## Part 4: Service Defaults (Pre-Configured)

### `group_vars/services.yml` (Service Catalog)

```yaml
---
# Service Catalog - Default Configurations
# Users can override in their inventory file

service_defaults:
  # Finance Services
  actual_budget:
    image: actualbudget/actual-server:latest
    type: webapp
    port: 5006
    subdomain: money
    memory_limit: 256m
    cpu_limit: 0.5
    healthcheck_path: /
    description: "Personal finance management"
    
  # Automation Services
  n8n:
    image: n8nio/n8n:latest
    type: webapp
    port: 5678
    subdomain: n8n
    memory_limit: 512m
    cpu_limit: 1.0
    healthcheck_path: /healthz
    environment:
      N8N_PORT: 5678
      WEBHOOK_URL: "https://n8n.{{ domain }}"
      GENERIC_TIMEZONE: "{{ timezone | default('America/New_York') }}"
    depends_on:
      - redis
      - postgres
    description: "Workflow automation platform"
    
  # Monitoring Services
  grafana:
    image: grafana/grafana:latest
    type: webapp
    port: 3000
    subdomain: grafana
    memory_limit: 512m
    cpu_limit: 0.5
    healthcheck_path: /api/health
    environment:
      GF_SERVER_ROOT_URL: "https://grafana.{{ domain }}"
      GF_SECURITY_ADMIN_USER: admin
      GF_AUTH_ANONYMOUS_ENABLED: false
    description: "Metrics and monitoring dashboards"
    
  prometheus:
    image: prom/prometheus:latest
    type: utility
    port: 9090
    subdomain: prometheus
    memory_limit: 1g
    cpu_limit: 1.0
    healthcheck_path: /-/healthy
    description: "Metrics collection and storage"
    
  loki:
    image: grafana/loki:latest
    type: utility
    port: 3100
    subdomain: null  # Internal only
    memory_limit: 512m
    cpu_limit: 0.5
    description: "Log aggregation system"
    
  # Dashboard Services
  homer:
    image: b4bz/homer:latest
    type: webapp
    port: 8080
    subdomain: home
    memory_limit: 128m
    cpu_limit: 0.25
    healthcheck_path: /
    description: "Service dashboard"
    
  portainer:
    image: portainer/portainer-ce:latest
    type: webapp
    port: 9000
    subdomain: portainer
    memory_limit: 256m
    cpu_limit: 0.5
    healthcheck_path: /api/system/status
    description: "Container management UI"
    
  # Database Services
  redis:
    image: redis:7-alpine
    type: database
    port: 6379
    subdomain: null  # Internal only
    memory_limit: 256m
    cpu_limit: 0.5
    command: "redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru"
    description: "In-memory data store"
    
  postgres:
    image: postgres:15-alpine
    type: database
    port: 5432
    subdomain: null  # Internal only
    memory_limit: 512m
    cpu_limit: 1.0
    environment:
      POSTGRES_DB: pai_db
      POSTGRES_USER: pai_user
      POSTGRES_PASSWORD: "{{ vault_postgres_password }}"
    description: "Relational database"
    
  # Media Services
  plex:
    image: plexinc/pms-docker:latest
    type: webapp
    port: 32400
    subdomain: plex
    memory_limit: 2g
    cpu_limit: 2.0
    environment:
      TZ: "{{ timezone | default('America/New_York') }}"
      PLEX_CLAIM: "{{ vault_plex_claim_token }}"
    description: "Media server"
    
  jellyfin:
    image: jellyfin/jellyfin:latest
    type: webapp
    port: 8096
    subdomain: media
    memory_limit: 2g
    cpu_limit: 2.0
    description: "Open source media server"
```

---

## Part 5: Generic Service Role

### `roles/service_deploy/tasks/main.yml`

```yaml
---
# Generic Service Deployment Role
# Works for ANY service in the catalog

- name: Load service defaults
  set_fact:
    service_def: "{{ service_defaults[service_name] }}"
    
- name: Merge with user overrides
  set_fact:
    service: "{{ service_def | combine(service_config[service_name] | default({}), recursive=true) }}"

- name: Create service directory
  file:
    path: "/opt/services/{{ service_name }}"
    state: directory
    owner: "{{ ansible_user }}"
    mode: '0755'

- name: Deploy docker-compose file
  template:
    src: docker-compose.yml.j2
    dest: "/opt/services/{{ service_name }}/docker-compose.yml"
    owner: "{{ ansible_user }}"
    mode: '0644'
  register: compose_file

- name: Create named volume for service
  command: "podman volume create {{ service_name }}-data"
  when: service.type in ['webapp', 'database']
  failed_when: false

- name: Deploy service
  command:
    cmd: "podman-compose -f /opt/services/{{ service_name }}/docker-compose.yml up -d"
  when: compose_file.changed

- name: Wait for service to be healthy
  uri:
    url: "http://localhost:{{ service.port }}{{ service.healthcheck_path | default('/health') }}"
    status_code: 200
  register: result
  until: result.status == 200
  retries: 30
  delay: 2
  when: service.healthcheck_path is defined
  failed_when: false

- name: Verify service is running
  command: "podman ps --filter name={{ service_name }} --format '{{'{{'}} .Status {{'}}'}}'"
  register: service_status
  changed_when: false
  
- name: Display service status
  debug:
    msg: "{{ service_name }}: {{ service_status.stdout }}"
```

### `roles/service_deploy/templates/docker-compose.yml.j2`

```yaml
---
version: '3'

services:
  {{ service_name }}:
    image: {{ service.image }}
    container_name: {{ service_name }}
    
    # Ports
    ports:
      - "{{ service.port }}:{{ service.port }}"
    
    # Environment variables
    {% if service.environment is defined %}
    environment:
      {% for key, value in service.environment.items() %}
      {{ key }}: "{{ value }}"
      {% endfor %}
    {% endif %}
    
    # Volumes
    {% if service.type in ['webapp', 'database'] %}
    volumes:
      - {{ service_name }}-data:/data:z
    {% endif %}
    
    # Resource limits
    deploy:
      resources:
        limits:
          cpus: "{{ service.cpu_limit | default(default_cpu_limit) }}"
          memory: "{{ service.memory_limit | default(default_memory_limit) }}"
    
    # Health check
    {% if service.healthcheck_path is defined %}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:{{ service.port }}{{ service.healthcheck_path }}"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    {% endif %}
    
    # Restart policy
    restart: unless-stopped
    
    # Traefik labels
    {% if service.subdomain %}
    labels:
      traefik.enable: "true"
      traefik.http.routers.{{ service_name }}.rule: "Host(`{{ service.subdomain }}.{{ domain }}`)"
      traefik.http.routers.{{ service_name }}.entrypoints: "websecure"
      {% if features.ssl_enabled | default(true) %}
      traefik.http.routers.{{ service_name }}.tls: "true"
      traefik.http.routers.{{ service_name }}.tls.certresolver: "letsencrypt"
      {% endif %}
      traefik.http.services.{{ service_name }}.loadbalancer.server.port: "{{ service.port }}"
      
      # Monitoring
      {% if features.monitoring_enabled | default(true) %}
      prometheus.io/scrape: "true"
      prometheus.io/port: "{{ service.port }}"
      {% endif %}
    {% endif %}

{% if service.type in ['webapp', 'database'] %}
volumes:
  {{ service_name }}-data:
    driver: local
{% endif %}
```

---

## Part 6: Quick Start for Users

### `README.md` (In Repository Root)

```markdown
# PAI Ansible Framework

**Deploy a complete self-hosted infrastructure in 10 minutes**

## Quick Start

### 1. Clone This Repository
```bash
git clone https://github.com/yourusername/pai-ansible-framework.git
cd pai-ansible-framework
```

### 2. Install Ansible
```bash
# macOS
brew install ansible

# Linux
sudo dnf install ansible  # Fedora/RHEL
sudo apt install ansible  # Ubuntu/Debian
```

### 3. Install Dependencies
```bash
ansible-galaxy install -r requirements.yml
ansible-galaxy collection install -r requirements.yml
```

### 4. Configure Your Server
```bash
# Copy example configuration
cp inventory/example-server.yml inventory/my-server.yml

# Edit with your details
vim inventory/my-server.yml

# Required changes:
# - ansible_host: Your server IP
# - domain: Your domain name
# - letsencrypt_email: Your email
# - services_enabled: Pick services you want
```

### 5. Deploy Everything
```bash
ansible-playbook -i inventory/my-server.yml site.yml
```

### 6. Access Your Services
Visit `https://home.yourdomain.com` for your dashboard!

## What You Get

- ✅ Automatic SSL certificates (Let's Encrypt)
- ✅ Reverse proxy (Traefik)
- ✅ Pick services from catalog (20+ available)
- ✅ Monitoring (Prometheus + Grafana)
- ✅ Centralized logging (Loki)
- ✅ Automated backups
- ✅ Container management (Portainer)
- ✅ Service dashboard (Homer)

## Available Services

### Finance
- **Actual Budget** - Personal finance management

### Automation
- **n8n** - Workflow automation

### Monitoring
- **Grafana** - Dashboards
- **Prometheus** - Metrics
- **Loki** - Logs

### Media
- **Plex** - Media server
- **Jellyfin** - Open source media server

### Development
- **Code Server** - VS Code in browser
- **Gitea** - Self-hosted Git

[See full list in docs/SERVICES.md]

## Customization

Add your own services by editing `group_vars/services.yml`:

```yaml
my_custom_service:
  image: myorg/myapp:latest
  type: webapp
  port: 8080
  subdomain: myapp
```

Then add to `services_enabled` in your inventory file.

## Support

- Documentation: [docs/](docs/)
- Issues: GitHub Issues
- Discussions: GitHub Discussions
```

---

## Part 7: Maintenance Playbooks

### Individual Task Playbooks (For Common Operations)

```yaml
# playbooks/update-services.yml
---
- name: Update all services
  hosts: all
  become: true
  tasks:
    - name: Pull latest images
      command: "podman pull {{ item.image }}"
      loop: "{{ services_enabled | map('extract', service_defaults) | list }}"
      
    - name: Restart services
      command: "podman-compose -f /opt/services/{{ item }}/docker-compose.yml restart"
      loop: "{{ services_enabled }}"

# Usage: ansible-playbook -i inventory/my-server.yml playbooks/update-services.yml
```

```yaml
# playbooks/backup-now.yml
---
- name: Run backup immediately
  hosts: all
  become: true
  roles:
    - backup_system

# Usage: ansible-playbook -i inventory/my-server.yml playbooks/backup-now.yml
```

```yaml
# playbooks/add-service.yml
---
- name: Add new service
  hosts: all
  become: true
  vars_prompt:
    - name: new_service
      prompt: "Service name from catalog"
      private: no
  
  tasks:
    - name: Deploy service
      include_role:
        name: service_deploy
      vars:
        service_name: "{{ new_service }}"

# Usage: ansible-playbook -i inventory/my-server.yml playbooks/add-service.yml
```

---

## Part 8: Benefits for Your Friend

### Clone to Production in 15 Minutes

**Minute 1-5: Setup**
```bash
git clone https://github.com/jbyrd/pai-ansible-framework.git
cd pai-ansible-framework
ansible-galaxy install -r requirements.yml
cp inventory/example-server.yml inventory/production.yml
vim inventory/production.yml  # Edit 4 values
```

**Minute 6-15: Deploy**
```bash
ansible-playbook -i inventory/production.yml site.yml
# ☕ Coffee time - Ansible does everything
```

**Minute 16: Done**
```
✅ 10 services deployed
✅ SSL certificates installed
✅ Monitoring configured
✅ Backups scheduled
✅ Ready for production
```

### What Your Friend Gets

**Infrastructure:**
- Pure Ansible (no custom scripts to understand)
- Geerling's proven roles (Docker, security, firewall)
- Your generic service roles (works for any service)
- One config file (their entire infrastructure)

**Reusability:**
- Works on any Linux server
- Any domain name
- Any combination of services
- Any cloud provider (AWS, Digital Ocean, Linode, etc.)

**Maintainability:**
- `git pull` → Get your updates
- Edit one file → Their customizations preserved
- Run playbook → Infrastructure updated
- Pure Infrastructure as Code

---

## Part 9: Advanced: Multi-Environment

### Friend Deploys Dev + Staging + Prod from Same Repo

```
inventory/
├── dev.yml          # Development server
├── staging.yml      # Staging server
└── prod.yml         # Production server

# Each file: same structure, different values
```

**Deploy to each:**
```bash
# Development
ansible-playbook -i inventory/dev.yml site.yml

# Staging
ansible-playbook -i inventory/staging.yml site.yml

# Production
ansible-playbook -i inventory/prod.yml site.yml
```

**All from same framework!**

---

## Part 10: Extending the Framework

### Your Friend Adds Custom Service

**Step 1: Add to service catalog**
```yaml
# group_vars/services.yml
my_awesome_app:
  image: company/awesome:latest
  type: webapp
  port: 3000
  subdomain: awesome
  memory_limit: 512m
  environment:
    DATABASE_URL: "postgres://{{ databases.postgres.host }}/awesome"
```

**Step 2: Enable in inventory**
```yaml
# inventory/my-server.yml
services_enabled:
  - my_awesome_app
```

**Step 3: Deploy**
```bash
ansible-playbook -i inventory/my-server.yml site.yml --tags services
```

**Done!** Generic roles handle everything.

---

## Bottom Line

### Traditional Approach

```
Friend: "How do I set this up?"
You: "Well, first install Docker..."
You: "Then configure Traefik..."
You: "Then set up each service..."
You: "Then configure SSL..."
You: "Then set up monitoring..."
Friend: *gives up after 6 hours*
```

### PAI Ansible Framework

```
Friend: "How do I set this up?"
You: "git clone my-repo"
You: "Edit one YAML file with your IP and domain"
You: "Run ansible-playbook site.yml"
Friend: *has full stack running in 10 minutes*
Friend: "This is amazing!"
```

### The Framework

```
Pure Ansible
+
Geerling's Roles (infrastructure)
+
Your Generic Roles (services)
+
Service Catalog (pre-configured)
+
One Config File (user's settings)
=
Clone → Edit → Deploy → Done
```

**Time to Deploy:** 10 minutes  
**Files to Edit:** 1  
**Commands to Run:** 2  
**Result:** Production-ready infrastructure

**Your friend can replicate everything you've built in the time it takes to make coffee.** ☕

---

*Philosophy: Pure Ansible + Infinite Replicability*  
*Pattern: Clone → Configure → Deploy*  
*Result: Lightning-fast infrastructure deployment*
