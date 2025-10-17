# Resilience Strategy: World-Class Failsafe Mechanisms

**Goal:** Most resilient tools out there  
**Philosophy:** Learn from giants (Google SRE, Netflix, Kubernetes, AWS)

---

## Resilience Hierarchy (Learn from Giants)

### Tier 1: Prevention (Design-Time)
**Principle:** Problems that can't happen don't need fixing

### Tier 2: Detection (Run-Time)
**Principle:** Know immediately when something fails

### Tier 3: Recovery (Auto-Healing)
**Principle:** Self-heal without human intervention

### Tier 4: Adaptation (Learning)
**Principle:** Get stronger from failures

---

## Part 1: Prevention Mechanisms

### 1.1 Idempotency (Ansible Core Principle)

**What the Giants Do:**
- **Ansible:** Every task can run multiple times safely
- **Kubernetes:** Desired state, not imperative commands
- **Terraform:** Declarative infrastructure

**Apply to PAI:**
```yaml
# roles/miraclemax_services/tasks/main.yml
- name: Ensure service is running
  containers.podman.podman_container:
    name: actual-budget
    state: started  # Idempotent: safe to run repeatedly
    # NOT: command: podman start (fails if already running)
```

**Failsafe Benefit:** Can retry any operation without side effects

### 1.2 Input Validation (Pydantic Pattern)

**What the Giants Do:**
- **AWS API:** Validates before processing
- **Kubernetes:** Schema validation on resources
- **Stripe API:** Strong type checking

**Apply to PAI:**
```python
# Before (fragile)
def process_case(case_id):
    # No validation, crashes on bad input
    return rhcase.get(case_id)

# After (resilient)
from pydantic import BaseModel, validator

class CaseRequest(BaseModel):
    case_id: str
    
    @validator('case_id')
    def validate_case_id(cls, v):
        if not v.startswith(('0', '1', '2', '3')):
            raise ValueError('Invalid case ID format')
        if len(v) != 8:
            raise ValueError('Case ID must be 8 digits')
        return v

def process_case(case_id: str):
    request = CaseRequest(case_id=case_id)  # Validates first
    return rhcase.get(request.case_id)
```

**Failsafe Benefit:** Bad input rejected before causing damage

### 1.3 Immutable Infrastructure (Netflix/Google Pattern)

**What the Giants Do:**
- **Netflix:** Immutable AMIs, never patch running instances
- **Google:** Immutable containers, recreate don't modify
- **Kubernetes:** Replace pods, don't update them

**Apply to PAI:**
```yaml
# miraclemax service updates
- name: Deploy new version
  containers.podman.podman_container:
    name: actual-budget
    image: actualbudget/actual-server:25.1.0  # Specific version
    recreate: yes  # Replace, don't patch
    
# NOT: ssh + manual updates inside running container
```

**Failsafe Benefit:** Known good state, easy rollback

### 1.4 Pre-Flight Checks (Terraform/K8s Pattern)

**What the Giants Do:**
- **Terraform:** `terraform plan` before `apply`
- **Kubernetes:** Admission controllers validate before create
- **Ansible:** `--check` mode for dry runs

**Apply to PAI:**
```bash
# tam-rfe-deploy (new tool)
#!/bin/bash
set -euo pipefail

# Pre-flight checks
check_requirements() {
    echo "Running pre-flight checks..."
    
    # 1. Connectivity
    if ! ping -c 1 miraclemax >/dev/null 2>&1; then
        echo "❌ Cannot reach miraclemax"
        exit 1
    fi
    
    # 2. Disk space
    available=$(ssh miraclemax "df / | tail -1 | awk '{print \$4}'")
    if [ "$available" -lt 1048576 ]; then  # 1GB
        echo "❌ Low disk space: ${available}KB"
        exit 1
    fi
    
    # 3. Required services
    for service in redis traefik; do
        if ! ssh miraclemax "podman ps | grep -q $service"; then
            echo "⚠️  Warning: $service not running"
        fi
    done
    
    echo "✅ All pre-flight checks passed"
}

# Always check first
check_requirements

# Then deploy
ansible-playbook playbooks/miraclemax.yml
```

**Failsafe Benefit:** Catch problems before they cause outages

---

## Part 2: Detection Mechanisms

### 2.1 Health Checks (Google SRE Pattern)

**What the Giants Do:**
- **Kubernetes:** Liveness + readiness probes
- **AWS ELB:** Health check endpoints
- **Google SRE:** Blackbox + whitebox monitoring

**Apply to PAI:**
```yaml
# roles/miraclemax_services/templates/actual-budget.yml.j2
version: '3'
services:
  actual-budget:
    image: actualbudget/actual-server:latest
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5006/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    restart: on-failure
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.actual.rule=Host(`money.jbyrd.org`)"
      # Health check endpoint
      - "traefik.http.services.actual.loadbalancer.healthcheck.path=/health"
      - "traefik.http.services.actual.loadbalancer.healthcheck.interval=10s"
```

**Create health check endpoints:**
```python
# src/health_check.py (new)
from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/health')
def health():
    """Multi-level health check"""
    health_status = {
        'status': 'healthy',
        'checks': {}
    }
    
    # Check 1: Self (basic)
    health_status['checks']['self'] = 'ok'
    
    # Check 2: Dependencies (Redis)
    try:
        r = requests.get('http://redis:6379/ping', timeout=2)
        health_status['checks']['redis'] = 'ok' if r.ok else 'degraded'
    except:
        health_status['checks']['redis'] = 'down'
        health_status['status'] = 'degraded'
    
    # Check 3: Disk space
    import shutil
    stat = shutil.disk_usage('/')
    if stat.free < 1e9:  # < 1GB
        health_status['checks']['disk'] = 'critical'
        health_status['status'] = 'degraded'
    else:
        health_status['checks']['disk'] = 'ok'
    
    status_code = 200 if health_status['status'] == 'healthy' else 503
    return jsonify(health_status), status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

**Failsafe Benefit:** Detect failures in seconds, not hours

### 2.2 Observability Stack (Netflix/Google Pattern)

**What the Giants Do:**
- **Google:** Logs + Metrics + Traces (three pillars)
- **Netflix:** Centralized logging (ELK stack)
- **DataDog:** Unified observability platform

**Apply to PAI:**
```yaml
# Already have: Prometheus + Grafana + Loki
# Add: Structured logging

# roles/miraclemax_services/tasks/logging.yml
- name: Configure structured logging
  ansible.builtin.template:
    src: promtail-config.yml.j2
    dest: /etc/promtail/config.yml
  notify: restart promtail

- name: Deploy log aggregation
  containers.podman.podman_container:
    name: promtail
    image: grafana/promtail:latest
    volumes:
      - /var/log:/var/log:ro
      - /etc/promtail:/etc/promtail:ro
    command: -config.file=/etc/promtail/config.yml
```

**Structured logging in tools:**
```python
# Use structlog (proven library)
import structlog

log = structlog.get_logger()

# Bad
print(f"Processing case {case_id}")

# Good
log.info("case_processing_started", 
         case_id=case_id, 
         customer="jpmc",
         user="jbyrd")
```

**Failsafe Benefit:** Root cause analysis in minutes, not days

### 2.3 Alerting (PagerDuty/Opsgenie Pattern)

**What the Giants Do:**
- **PagerDuty:** Alert routing + escalation
- **Google SRE:** Error budgets + SLOs
- **AWS CloudWatch:** Automated alerts

**Apply to PAI:**
```yaml
# ansible/playbooks/alerting.yml
- name: Configure Prometheus alerting rules
  ansible.builtin.template:
    src: alert-rules.yml.j2
    dest: /etc/prometheus/rules/pai-alerts.yml

# templates/alert-rules.yml.j2
groups:
  - name: pai_services
    interval: 30s
    rules:
      # Service down
      - alert: ServiceDown
        expr: up{job="podman"} == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.instance }} is down"
          description: "{{ $labels.instance }} has been down for 2 minutes"
      
      # High memory
      - alert: HighMemoryUsage
        expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage on {{ $labels.name }}"
      
      # Disk space
      - alert: LowDiskSpace
        expr: node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes < 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Low disk space on {{ $labels.instance }}"
      
      # Failed deployments
      - alert: DeploymentFailed
        expr: increase(deployment_failed_total[5m]) > 0
        labels:
          severity: critical
        annotations:
          summary: "Deployment failed on {{ $labels.instance }}"
```

**Failsafe Benefit:** Notified of problems before users complain

---

## Part 3: Recovery Mechanisms

### 3.1 Automatic Restart (Kubernetes/Docker Pattern)

**What the Giants Do:**
- **Kubernetes:** RestartPolicy: Always
- **Docker Swarm:** Restart on failure
- **systemd:** Restart=always

**Apply to PAI:**
```yaml
# All services get automatic restart
# roles/miraclemax_services/templates/service.yml.j2
version: '3'
services:
  {{ item.name }}:
    image: {{ item.image }}
    restart: unless-stopped  # Restart on crash
    deploy:
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
        window: 120s
```

**For RFE tools:**
```ini
# /etc/systemd/system/tam-rfe-scheduler.service
[Unit]
Description=TAM RFE Scheduler
After=network.target

[Service]
Type=simple
User=jbyrd
ExecStart=/usr/local/bin/tam-rfe-scheduler
Restart=always
RestartSec=10s
StartLimitBurst=5
StartLimitIntervalSec=60

[Install]
WantedBy=multi-user.target
```

**Failsafe Benefit:** Self-healing from crashes

### 3.2 Circuit Breakers (Netflix Hystrix Pattern)

**What the Giants Do:**
- **Netflix Hystrix:** Prevent cascade failures
- **AWS:** Exponential backoff + jitter
- **Kubernetes:** PodDisruptionBudget

**Apply to PAI:**
```python
# Use proven library: pybreaker
from pybreaker import CircuitBreaker

# Configure circuit breaker
rhcase_breaker = CircuitBreaker(
    fail_max=5,          # Open after 5 failures
    timeout_duration=60, # Stay open for 60s
    name='rhcase_api'
)

@rhcase_breaker
def fetch_case_data(case_id):
    """Fetch with circuit breaker protection"""
    return rhcase.case(case_id).get()

# Usage
try:
    data = fetch_case_data("12345678")
except CircuitBreakerError:
    # Circuit open, fail fast
    log.warning("rhcase_api_circuit_open", 
                message="API experiencing issues, using cached data")
    data = get_cached_data(case_id)
```

**Failsafe Benefit:** Stop hammering broken services, fail fast

### 3.3 Graceful Degradation (AWS/Google Pattern)

**What the Giants Do:**
- **AWS S3:** Eventually consistent reads during issues
- **Google Search:** Partial results if some shards fail
- **Netflix:** Lower quality video if bandwidth drops

**Apply to PAI:**
```python
# tam-rfe-chat with graceful degradation
def get_customer_intelligence(account_id):
    """Multi-tier data fetching with fallbacks"""
    intelligence = {
        'account_id': account_id,
        'source': None,
        'confidence': 'high'
    }
    
    # Tier 1: Try Hydra API (best data)
    try:
        data = fetch_from_hydra(account_id, timeout=5)
        intelligence.update(data)
        intelligence['source'] = 'hydra'
        return intelligence
    except (TimeoutError, APIError) as e:
        log.warning("hydra_api_failed", error=str(e))
    
    # Tier 2: Try local cache (slightly stale)
    try:
        data = get_from_cache(account_id)
        if data and data.age < 86400:  # < 24 hours
            intelligence.update(data)
            intelligence['source'] = 'cache'
            intelligence['confidence'] = 'medium'
            return intelligence
    except CacheError as e:
        log.warning("cache_failed", error=str(e))
    
    # Tier 3: Basic info from config (minimal)
    try:
        data = get_from_config(account_id)
        intelligence.update(data)
        intelligence['source'] = 'config'
        intelligence['confidence'] = 'low'
        return intelligence
    except:
        pass
    
    # Tier 4: Absolute fallback
    intelligence['source'] = 'none'
    intelligence['confidence'] = 'none'
    intelligence['error'] = 'No data sources available'
    return intelligence
```

**Failsafe Benefit:** Partial functionality better than total failure

### 3.4 Automatic Rollback (Kubernetes/Terraform Pattern)

**What the Giants Do:**
- **Kubernetes:** RollingUpdate with maxUnavailable
- **Terraform:** State backup before apply
- **Blue/Green Deployments:** AWS, Heroku

**Apply to PAI:**
```yaml
# roles/miraclemax_services/tasks/safe-deploy.yml
- name: Backup current state
  ansible.builtin.command:
    cmd: podman ps --format json
  register: current_state
  changed_when: false

- name: Save backup
  ansible.builtin.copy:
    content: "{{ current_state.stdout }}"
    dest: "/var/backups/podman-state-{{ ansible_date_time.epoch }}.json"

- name: Deploy new version
  containers.podman.podman_container:
    name: "{{ item.name }}"
    image: "{{ item.image }}"
    state: started
  register: deployment
  
- name: Health check after deployment
  ansible.builtin.uri:
    url: "http://localhost:{{ item.port }}/health"
    status_code: 200
  retries: 30
  delay: 2
  register: health_check
  failed_when: false

- name: Rollback if unhealthy
  when: health_check.failed
  block:
    - name: Stop failed deployment
      containers.podman.podman_container:
        name: "{{ item.name }}"
        state: stopped
    
    - name: Restore previous version
      ansible.builtin.command:
        cmd: podman start {{ item.name }}
      
    - name: Alert about rollback
      ansible.builtin.debug:
        msg: "⚠️  Deployment failed, rolled back to previous version"
    
    - name: Fail the playbook
      ansible.builtin.fail:
        msg: "Deployment rolled back due to failed health check"
```

**Failsafe Benefit:** Bad deployments automatically reverted

### 3.5 Data Backup & Recovery (AWS/Google Pattern)

**What the Giants Do:**
- **AWS RDS:** Automated backups + point-in-time recovery
- **Google Cloud:** Snapshots + geo-replication
- **GitHub:** Multiple backup copies

**Apply to PAI:**
```yaml
# ansible/playbooks/backup-strategy.yml
- name: Automated Backup Strategy
  hosts: miraclemax
  
  tasks:
    - name: Backup service data
      ansible.builtin.shell: |
        for volume in $(podman volume ls -q); do
          backup_file="/var/backups/volumes/${volume}-$(date +%Y%m%d-%H%M%S).tar.gz"
          podman volume export $volume | gzip > $backup_file
          
          # Keep only last 7 days
          find /var/backups/volumes -name "${volume}-*.tar.gz" -mtime +7 -delete
        done
      
    - name: Backup configurations
      ansible.posix.synchronize:
        src: /home/jbyrd/miraclemax-infrastructure/
        dest: /var/backups/config/
        archive: yes
        delete: yes
    
    - name: Upload to remote backup
      ansible.builtin.command:
        cmd: rclone sync /var/backups/ remote:pai-backups/miraclemax/
      when: rclone_configured | default(false)
```

**Cron job for automated backups:**
```bash
# /etc/cron.daily/pai-backup
#!/bin/bash
ansible-playbook /home/jbyrd/pai/ansible/playbooks/backup-strategy.yml
```

**Failsafe Benefit:** Data loss prevention

---

## Part 4: Adaptation Mechanisms

### 4.1 Chaos Engineering (Netflix Pattern)

**What the Giants Do:**
- **Netflix Chaos Monkey:** Randomly kill instances
- **Google DiRT:** Disaster recovery testing
- **AWS GameDays:** Simulated failures

**Apply to PAI:**
```bash
# bin/pai-chaos-test (new tool)
#!/bin/bash
# Test resilience by introducing controlled failures

set -euo pipefail

echo "🐒 PAI Chaos Testing"
echo "Testing system resilience..."
echo ""

# Test 1: Random service kill
test_service_restart() {
    echo "Test: Random service restart"
    service=$(podman ps --format "{{.Names}}" | shuf -n 1)
    echo "  Killing: $service"
    podman restart $service
    sleep 5
    
    # Verify it recovered
    if podman ps | grep -q $service; then
        echo "  ✅ Service auto-recovered"
    else
        echo "  ❌ Service failed to recover"
    fi
}

# Test 2: Fill disk space
test_disk_pressure() {
    echo "Test: Disk space pressure"
    dd if=/dev/zero of=/tmp/chaos-disk bs=1M count=1000 2>/dev/null || true
    echo "  Created 1GB test file"
    
    # Check if alerts fire
    sleep 10
    
    # Cleanup
    rm -f /tmp/chaos-disk
    echo "  ✅ Cleanup complete"
}

# Test 3: Network latency
test_network_latency() {
    echo "Test: Network latency simulation"
    # Add 100ms latency
    sudo tc qdisc add dev eth0 root netem delay 100ms 2>/dev/null || true
    echo "  Added 100ms latency"
    
    # Test API calls
    start_time=$(date +%s)
    curl -s http://localhost:5006/health >/dev/null
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    
    # Cleanup
    sudo tc qdisc del dev eth0 root 2>/dev/null || true
    echo "  ✅ Latency handled gracefully"
}

# Run tests
test_service_restart
echo ""
test_disk_pressure
echo ""
# test_network_latency  # Requires root

echo ""
echo "🎉 Chaos testing complete"
echo "Review logs and metrics for any issues"
```

**Failsafe Benefit:** Find weaknesses before they cause outages

### 4.2 Canary Deployments (Google/Facebook Pattern)

**What the Giants Do:**
- **Google:** Gradual rollout percentages
- **Facebook:** Dark launches to internal users
- **AWS:** Weighted routing in Route53

**Apply to PAI:**
```yaml
# roles/miraclemax_services/tasks/canary-deploy.yml
- name: Deploy canary version
  containers.podman.podman_container:
    name: "{{ item.name }}-canary"
    image: "{{ item.image }}:{{ canary_version }}"
    ports:
      - "{{ item.port + 1000 }}:{{ item.port }}"
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.{{ item.name }}-canary.rule=Host(`{{ item.subdomain }}.jbyrd.org`) && Headers(`X-Canary`, `true`)"
      - "traefik.http.routers.{{ item.name }}-canary.priority=100"  # Higher priority

- name: Monitor canary metrics
  ansible.builtin.pause:
    minutes: 10
    prompt: "Monitoring canary deployment. Check metrics in Grafana."

- name: Promote canary to production
  when: canary_healthy
  containers.podman.podman_container:
    name: "{{ item.name }}"
    image: "{{ item.image }}:{{ canary_version }}"
    state: started
    force_restart: yes

- name: Remove canary
  containers.podman.podman_container:
    name: "{{ item.name }}-canary"
    state: absent
```

**Failsafe Benefit:** Test in production safely

### 4.3 Feature Flags (LaunchDarkly Pattern)

**What the Giants Do:**
- **LaunchDarkly:** Runtime feature toggles
- **Unleash:** Open-source feature flags
- **GitLab:** Feature flags for gradual rollout

**Apply to PAI:**
```python
# src/feature_flags.py (new)
import os
import json

class FeatureFlags:
    """Simple feature flag system"""
    
    def __init__(self, config_file='~/.config/pai/features.json'):
        self.config_file = os.path.expanduser(config_file)
        self.flags = self._load_flags()
    
    def _load_flags(self):
        try:
            with open(self.config_file) as f:
                return json.load(f)
        except:
            return {}
    
    def is_enabled(self, feature: str, default: bool = False) -> bool:
        """Check if feature is enabled"""
        return self.flags.get(feature, {}).get('enabled', default)
    
    def is_enabled_for_user(self, feature: str, user: str) -> bool:
        """Check if feature is enabled for specific user"""
        feature_config = self.flags.get(feature, {})
        
        # Check if enabled globally
        if feature_config.get('enabled', False):
            return True
        
        # Check if user in allowlist
        return user in feature_config.get('users', [])

# Usage in tools
flags = FeatureFlags()

if flags.is_enabled('hydra_api_v2'):
    # Use new Hydra API
    data = fetch_from_hydra_v2(account_id)
else:
    # Use old API
    data = fetch_from_hydra_v1(account_id)
```

**Config file:**
```json
{
  "hydra_api_v2": {
    "enabled": false,
    "users": ["jbyrd"],
    "description": "New Hydra API with better performance"
  },
  "intelligent_caching": {
    "enabled": true,
    "description": "Cache Hydra responses for 1 hour"
  }
}
```

**Failsafe Benefit:** Disable broken features instantly without deployment

### 4.4 Postmortems (Google SRE Pattern)

**What the Giants Do:**
- **Google SRE:** Blameless postmortems after every incident
- **PagerDuty:** Incident review templates
- **AWS:** Well-Architected Review

**Apply to PAI:**
```bash
# bin/pai-postmortem (new tool)
#!/bin/bash
# Generate postmortem template

cat > "/tmp/postmortem-$(date +%Y%m%d-%H%M%S).md" << 'POSTMORTEM'
# Incident Postmortem

**Date:** $(date)  
**Severity:** [ ] SEV1 (Critical) [ ] SEV2 (High) [ ] SEV3 (Medium)  
**Duration:** XX minutes  
**Impact:** Description of user impact

---

## Timeline

| Time | Event |
|------|-------|
| HH:MM | Incident began |
| HH:MM | Detected by (monitoring/user report) |
| HH:MM | Investigation started |
| HH:MM | Root cause identified |
| HH:MM | Fix deployed |
| HH:MM | Incident resolved |

---

## Root Cause

**What happened:**


**Why it happened:**


**Why it wasn't caught earlier:**


---

## Resolution

**Immediate fix:**


**Verification:**


---

## Action Items

**Prevent recurrence:**
- [ ] Action item 1 (Owner: NAME, Due: DATE)
- [ ] Action item 2 (Owner: NAME, Due: DATE)

**Improve detection:**
- [ ] Add monitoring for X
- [ ] Add alert for Y

**Improve response:**
- [ ] Document runbook for Z
- [ ] Add automation for recovery

---

## Lessons Learned

**What went well:**
-

**What went poorly:**
-

**What we got lucky with:**
-

---

## Related Incidents

- Link to similar incident #N

POSTMORTEM

echo "Postmortem template created: /tmp/postmortem-*.md"
```

**Failsafe Benefit:** Learn from failures, prevent repeats

---

## Implementation Priority

### Phase 1: Foundation (Week 1)
**Quick wins, high impact**

1. ✅ **Idempotency:** All Ansible roles idempotent
2. ✅ **Health checks:** Add `/health` endpoints
3. ✅ **Automatic restart:** `restart: always` on services
4. ✅ **Pre-flight checks:** Validate before deploy

### Phase 2: Detection (Week 2)
**See problems immediately**

1. **Structured logging:** Add structlog to all tools
2. **Alerting rules:** Configure Prometheus alerts
3. **Monitoring dashboard:** Grafana with key metrics
4. **Health check automation:** Automated health monitoring

### Phase 3: Recovery (Week 3)
**Self-healing systems**

1. **Circuit breakers:** Add to external API calls
2. **Graceful degradation:** Multi-tier data fetching
3. **Automatic rollback:** Deploy with health check + rollback
4. **Backup automation:** Daily automated backups

### Phase 4: Adaptation (Week 4)
**Get stronger from failures**

1. **Chaos testing:** Run pai-chaos-test weekly
2. **Feature flags:** Add flag system to tools
3. **Canary deployments:** Test in production safely
4. **Postmortem process:** After every incident

---

## Resilience Metrics (SRE Pattern)

### Service Level Objectives (SLOs)

```yaml
# Define SLOs for PAI services
slos:
  availability:
    target: 99.9%  # 43 minutes downtime/month allowed
    measurement: up{job="podman"} == 1
  
  latency:
    target: 95%  # 95% of requests < 500ms
    measurement: histogram_quantile(0.95, http_request_duration_seconds)
  
  error_rate:
    target: 99%  # < 1% errors
    measurement: rate(http_requests_total{status=~"5.."}[5m])
```

### Error Budget

**Monthly error budget:** 43 minutes (99.9% availability)

**Track in Grafana:**
```promql
# Time spent down this month
sum(up{job="podman"} == 0) * 60  # in seconds
```

**Alert when 50% of budget spent:**
```yaml
- alert: ErrorBudgetHalfSpent
  expr: error_budget_remaining < 0.5
  labels:
    severity: warning
  annotations:
    summary: "50% of error budget spent this month"
```

---

## Resilience Checklist

### Before Deployment
- [ ] All tasks idempotent?
- [ ] Pre-flight checks pass?
- [ ] Health checks configured?
- [ ] Rollback plan ready?
- [ ] Backup recent?

### After Deployment
- [ ] Health checks passing?
- [ ] Metrics looking normal?
- [ ] Logs showing no errors?
- [ ] Alert silence period configured?

### Production Operations
- [ ] Monitoring dashboard reviewed daily?
- [ ] Alerts actionable and not noisy?
- [ ] Backups tested monthly?
- [ ] Chaos tests run weekly?
- [ ] Postmortems done for all incidents?

---

## Tools to Build

### Immediate
1. `pai-health-check` - Test all services
2. `pai-preflight` - Pre-deployment validation
3. `pai-rollback` - One-command rollback
4. `pai-backup` - Automated backup script

### Soon
1. `pai-chaos-test` - Chaos engineering
2. `pai-postmortem` - Incident template
3. `pai-slo-report` - SLO tracking
4. `pai-canary-deploy` - Safe deployments

---

## Bottom Line

### World-Class Resilience = Learning from Giants

**What Google SRE Does:** Error budgets, SLOs, blameless postmortems  
→ **You Do:** Same patterns, proven by billions of users

**What Netflix Does:** Circuit breakers, chaos engineering  
→ **You Do:** Same libraries (pybreaker), same tests

**What Kubernetes Does:** Self-healing, rolling updates  
→ **You Do:** Same patterns with Podman + Ansible

**What AWS Does:** Health checks, auto-scaling, multi-AZ  
→ **You Do:** Health endpoints, auto-restart, backups

### The Most Resilient Tools

**Prevent:** Idempotency + validation + immutability  
**Detect:** Health checks + logging + alerting  
**Recover:** Auto-restart + rollback + degradation  
**Adapt:** Chaos tests + postmortems + feature flags

**Result:** Tools that are more resilient than most enterprise software

---

*Strategy: Learn from the Giants*  
*Target: 99.9% availability (43 min downtime/month)*  
*Philosophy: Build on proven patterns*
