# Industry Patterns That Align with PAI Philosophy

**Philosophy:** Learn from the giants, integrate proven patterns  
**Pattern:** Steal the best ideas from industry leaders  
**Result:** World-class tools without reinventing the wheel

---

## The Philosophy Match

### What We've Built

1. ✅ **Geerling Pattern** - Build on proven code
2. ✅ **Lego Architecture** - Modular, plug-and-play
3. ✅ **SRE Patterns** - Resilience, observability
4. ✅ **OS-Agnostic** - Write once, run everywhere
5. ✅ **95/5 Rule** - Minimize custom code

### What Else Fits?

Industry patterns that align **perfectly** with our philosophy:

---

## Part 1: GitOps (Weaveworks/Flux/ArgoCD)

### What It Is

```
Git repository = Single source of truth for infrastructure
  ↓
Changes committed to Git
  ↓
Automation applies changes
  ↓
System converges to desired state
```

### Why It Fits

- **Declarative** - State, not steps
- **Version controlled** - Git tracks everything
- **Auditable** - Who changed what, when
- **Rollback** - Git revert = infrastructure rollback
- **Self-healing** - System auto-corrects drift

### How PAI Uses It

```
pai/
├── ansible/
│   ├── inventory/
│   │   └── miraclemax.yml        # Desired state
│   └── group_vars/
│       └── services.yml           # Service catalog
│
└── rfe-bug-tracker-automation/
    └── config/
        └── customers.conf         # Customer state

# Change anything:
git commit -m "Add new service"
git push

# CI/CD applies automatically:
ansible-playbook site.yml
```

### Benefits

- ✅ History of all changes
- ✅ Easy rollback (git revert)
- ✅ Multiple environments (branches)
- ✅ Pull request reviews for infrastructure
- ✅ Disaster recovery (re-apply Git repo)

---

## Part 2: Immutable Infrastructure (Netflix/HashiCorp)

### What It Is

```
Traditional: Patch running servers
  ↓
Something breaks
  ↓
"Works on my machine"
  ↓
Configuration drift

Immutable: Never patch, always replace
  ↓
Build new image
  ↓
Deploy new instance
  ↓
Delete old instance
```

### Why It Fits

- **No drift** - Every deploy is clean
- **Predictable** - Same image every time
- **Fast rollback** - Keep old image, deploy it
- **Testable** - Test exact production image

### How PAI Uses It

**Containers (Already Doing This):**
```bash
# Never "fix" a running container
# Always rebuild and redeploy

# Build new image
docker build -t myapp:v2 .

# Deploy new container
podman-compose up -d

# Old container replaced, not patched
```

**VM/Bare Metal (Ansible Makes This Easy):**
```bash
# Provision fresh VM
ansible-playbook bootstrap.yml

# Deploy everything from scratch
ansible-playbook site.yml

# Identical to existing system
# No accumulated cruft
```

### Benefits

- ✅ No "works on my machine"
- ✅ Fast disaster recovery
- ✅ Test exact production config
- ✅ No accumulated technical debt
- ✅ Clean slate every deploy

---

## Part 3: Feature Flags (LaunchDarkly Pattern)

### What It Is

```
Code deployed ≠ Feature released
  ↓
Deploy code with feature OFF
  ↓
Turn on for 5% of users
  ↓
No issues? Turn on for 50%
  ↓
Still good? Turn on for 100%
  ↓
Issue found? Turn off instantly (no redeploy)
```

### Why It Fits

- **Decouple deploy from release**
- **Safe rollout**
- **Instant rollback**
- **A/B testing**
- **User targeting**

### How PAI Uses It

**In Foundation Apps:**
```python
# foundation/features.py
class FeatureFlags:
    def __init__(self):
        self.config = self.load_config()
    
    def is_enabled(self, feature: str, user_id: str = None) -> bool:
        """Check if feature is enabled"""
        feature_config = self.config.get(feature, {})
        
        # Global toggle
        if not feature_config.get('enabled', False):
            return False
        
        # Percentage rollout
        rollout = feature_config.get('rollout_percent', 100)
        if self._hash_user(user_id) > rollout:
            return False
        
        return True

# Usage in business logic
features = FeatureFlags()

if features.is_enabled('new_hydra_api', user.id):
    # Use new Hydra API
    result = hydra_api_v2.query(...)
else:
    # Use old method
    result = rhcase.query(...)
```

**In Configuration:**
```yaml
# config/features.yml
features:
  new_hydra_api:
    enabled: true
    rollout_percent: 10        # Start with 10% of users
    description: "Phase 2 Hydra API"
  
  dynamic_customer_discovery:
    enabled: true
    rollout_percent: 100       # Fully rolled out
  
  experimental_ai_insights:
    enabled: false             # Not ready yet
    rollout_percent: 0
```

### Benefits

- ✅ Deploy anytime (feature OFF)
- ✅ Gradual rollout
- ✅ Instant rollback (no redeploy)
- ✅ Test in production safely
- ✅ A/B test features

---

## Part 4: Observability Triad (Honeycomb/DataDog Pattern)

### What It Is

```
Monitoring: "Is it up?"
  ↓
Observability: "Why is it broken?"

Three Pillars:
1. Metrics  - Numbers (CPU, latency, errors)
2. Logs     - Events (what happened)
3. Traces   - Journey (request flow)
```

### Why It Fits

- **Debug production issues**
- **Understand user experience**
- **Find bottlenecks**
- **Correlation** (link metrics/logs/traces)

### How PAI Uses It

**Already Have (Metrics + Logs):**
```yaml
# miraclemax services
services:
  prometheus:  # Metrics
  loki:        # Logs
  grafana:     # Visualization
```

**Add Traces (OpenTelemetry):**
```python
# foundation/monitoring/tracing.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Setup (foundation handles this)
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

# Usage (in business logic)
@tracer.start_as_current_span("get_customer_cases")
def get_customer_cases(account_id: str):
    span = trace.get_current_span()
    span.set_attribute("customer.account_id", account_id)
    
    with tracer.start_as_current_span("fetch_from_hydra"):
        cases = hydra_api.get_cases(account_id)
    
    with tracer.start_as_current_span("process_cases"):
        processed = process(cases)
    
    return processed

# Now in Grafana:
# See exactly where time is spent
# See which API calls are slow
# See full request journey
```

### Benefits

- ✅ See request flow across services
- ✅ Identify slow database queries
- ✅ Debug production issues
- ✅ Understand system behavior
- ✅ Link metrics + logs + traces

---

## Part 5: Progressive Delivery (Spinnaker Pattern)

### What It Is

```
Traditional: Big bang deploy
  ↓
New version to 100% of users
  ↓
Bug? Everyone affected

Progressive: Gradual rollout
  ↓
Deploy to Canary (5%)
  ↓
Monitor metrics
  ↓
Automatic rollback if errors spike
  ↓
Gradual increase to 100%
```

### Why It Fits

- **Reduce blast radius**
- **Automated rollback**
- **Data-driven decisions**
- **Safe deployments**

### How PAI Uses It

**Canary Deployments:**
```yaml
# ansible/roles/canary_deploy/tasks/main.yml
---
- name: Deploy canary version
  command: >
    podman run -d 
    --label canary=true
    --label weight=10
    {{ service.image }}:{{ new_version }}
  
- name: Monitor canary metrics
  uri:
    url: http://prometheus:9090/api/v1/query
    method: POST
    body_format: json
    body:
      query: "rate(http_errors_total{version='{{ new_version }}'}[5m])"
  register: canary_errors
  until: canary_errors.json.data.result[0].value[1] < 0.01
  retries: 10
  delay: 30

- name: Rollout to 50%
  command: >
    traefik update --weight=50 {{ service.name }}

- name: Rollout to 100%
  command: >
    traefik update --weight=100 {{ service.name }}
  when: canary_errors.json.data.result[0].value[1] < 0.01
```

### Benefits

- ✅ Limited blast radius
- ✅ Automatic rollback
- ✅ Confidence in deploys
- ✅ Catch issues early

---

## Part 6: Policy as Code (OPA Pattern)

### What It Is

```
Security/compliance rules in code
  ↓
Automated enforcement
  ↓
No manual review needed
  ↓
Consistent across all deployments
```

### Why It Fits

- **Compliance automation**
- **Red Hat AI policy enforcement**
- **Consistent rules**
- **Auditable**

### How PAI Uses It

**Red Hat Compliance:**
```python
# foundation/compliance/policy.py
class CompliancePolicy:
    """
    Red Hat AI Policy enforcement
    """
    
    def check_data_classification(self, data_type: str, model: str):
        """
        Enforce Red Hat AI policy:
        - Customer data → Granite only
        - Internal data → AIA-approved only
        """
        policies = {
            'customer_data': {
                'allowed_models': ['granite-*'],
                'blocked_models': ['gpt-*', 'claude-*'],
                'reason': 'Customer data requires Red Hat Granite'
            },
            'internal_data': {
                'allowed_models': ['granite-*', 'gpt-4', 'claude-3'],
                'blocked_models': [],
                'reason': 'Internal data: AIA-approved models only'
            }
        }
        
        policy = policies.get(data_type)
        
        # Check if model is allowed
        if not self._model_matches(model, policy['allowed_models']):
            raise ComplianceViolation(
                f"Model {model} not allowed for {data_type}. {policy['reason']}"
            )
    
    def check_audit_logging(self, service: str):
        """Ensure all customer operations are logged"""
        if not self.audit_enabled(service):
            raise ComplianceViolation(
                f"Service {service} must have audit logging enabled"
            )

# Usage (automatic in foundation)
@enforce_compliance
def process_customer_case(case_id: str, model: str = "granite-13b"):
    # Compliance check runs automatically
    # Raises exception if policy violated
    ...
```

**Ansible Integration:**
```yaml
# ansible/roles/compliance_check/tasks/main.yml
---
- name: Validate deployment against policy
  command: pai-compliance-check {{ service.name }}
  register: compliance
  failed_when: compliance.rc != 0

- name: Block non-compliant deployments
  fail:
    msg: "Deployment violates policy: {{ compliance.stderr }}"
  when: compliance.rc != 0
```

### Benefits

- ✅ Automated compliance
- ✅ No manual review needed
- ✅ Consistent enforcement
- ✅ Audit trail
- ✅ Prevent violations

---

## Part 7: Self-Service Infrastructure (Backstage Pattern)

### What It Is

```
Developers want:
  - New service
  - New environment
  - Database
  - Monitoring
  
Traditional: File ticket, wait for ops
  ↓
Slow, frustrating

Self-Service: Developer portal
  ↓
Click button, get service
  ↓
Fast, empowering
```

### Why It Fits

- **Faster delivery**
- **Consistent setup**
- **Best practices built-in**
- **Ops team scales**

### How PAI Uses It

**PAI Service Portal:**
```python
# bin/pai-service-create
#!/usr/bin/env python3
"""
Self-service infrastructure
Create new service with best practices
"""
import click
from rich.console import Console

console = Console()

@click.command()
@click.option('--name', prompt='Service name')
@click.option('--type', type=click.Choice(['webapp', 'api', 'worker', 'database']))
@click.option('--image', prompt='Docker image')
def create_service(name: str, type: str, image: str):
    """Create new service (self-service)"""
    
    console.print(f"[blue]Creating {type} service: {name}[/blue]")
    
    # Generate from template (best practices built-in)
    template = load_template(type)
    
    # Customize
    config = template.customize(
        name=name,
        image=image,
        # These are automatic:
        health_checks=True,
        metrics=True,
        logging=True,
        ssl=True,
        monitoring=True,
        backups=True,
    )
    
    # Add to service catalog
    add_to_catalog(config)
    
    # Deploy
    console.print("[yellow]Deploying service...[/yellow]")
    deploy(config)
    
    console.print(f"[green]✅ Service created: https://{name}.jbyrd.org[/green]")
    console.print(f"[green]   Metrics: https://grafana.jbyrd.org/d/{name}[/green]")
    console.print(f"[green]   Logs: https://grafana.jbyrd.org/explore?{name}[/green]")

# Usage:
# $ pai-service-create
# Service name: my-new-app
# Service type: webapp
# Docker image: myapp:latest
# ✅ Service created with monitoring, backups, SSL
```

### Benefits

- ✅ Fast service creation
- ✅ Best practices automatic
- ✅ Consistent setup
- ✅ Ops team doesn't bottleneck
- ✅ Developers empowered

---

## Part 8: Contract Testing (Pact Pattern)

### What It Is

```
Traditional: Integration tests break
  ↓
API changed
  ↓
Consumers didn't know
  ↓
Production breaks

Contract Testing: Define API contract
  ↓
Provider must honor contract
  ↓
Consumer tests against contract
  ↓
Breaking change? Tests fail immediately
```

### Why It Fits

- **API stability**
- **Safe refactoring**
- **Consumer-driven**
- **Early detection**

### How PAI Uses It

**For RFE Tool API:**
```python
# tests/contracts/test_rfe_api.py
"""
API contract tests
Ensure RFE API doesn't break consumers
"""
import pytest
from pact import Consumer, Provider

pact = Consumer('rfe-client').has_pact_with(Provider('rfe-api'))

def test_get_customer_cases_contract():
    """
    Contract: GET /customers/{id}/cases
    Returns: List of cases with required fields
    """
    expected = {
        'status': 200,
        'body': {
            'cases': [
                {
                    'case_id': '04280915',
                    'summary': 'AAP installation issue',
                    'severity': 'high',
                    'created': '2024-01-15T10:30:00Z'
                }
            ]
        }
    }
    
    (pact
     .given('customer has cases')
     .upon_receiving('request for cases')
     .with_request('GET', '/customers/397076/cases')
     .will_respond_with(200, body=expected['body']))
    
    with pact:
        response = rfe_api.get_customer_cases('397076')
        assert response['cases'][0]['case_id'] == '04280915'
```

### Benefits

- ✅ API stability
- ✅ Safe refactoring
- ✅ Consumer confidence
- ✅ Breaking changes caught early
- ✅ Documentation via contracts

---

## Part 9: Dependency Management (Renovate/Dependabot Pattern)

### What It Is

```
Traditional: Dependencies rot
  ↓
Security vulnerabilities
  ↓
Manual updates
  ↓
Never happens

Automated: Bot opens PRs
  ↓
Tests run automatically
  ↓
Merge if green
  ↓
Always up-to-date
```

### Why It Fits

- **Security patches**
- **Proven library updates**
- **Automated**
- **Tested before merge**

### How PAI Uses It

**GitLab CI + Renovate:**
```yaml
# .gitlab-ci.yml
stages:
  - security
  - test
  - deploy

dependency_update:
  stage: security
  script:
    - pip install pip-audit safety
    - pip-audit --desc                 # Check for vulnerabilities
    - safety check -r requirements.txt # Security scan
  only:
    - schedules  # Run daily

auto_update_deps:
  stage: security
  script:
    - pip install pur  # Pure Python updater
    - pur -r requirements.txt --dry-run
    - |
      if [ $? -eq 0 ]; then
        pur -r requirements.txt
        git commit -am "chore: update dependencies"
        git push
      fi
  only:
    - schedules
```

**Renovate Configuration:**
```json
{
  "extends": ["config:base"],
  "packageRules": [
    {
      "matchUpdateTypes": ["minor", "patch"],
      "automerge": true,
      "automergeType": "pr",
      "platformAutomerge": true
    },
    {
      "matchPackagePatterns": ["^pytest"],
      "groupName": "pytest"
    }
  ],
  "schedule": ["before 3am on Monday"],
  "labels": ["dependencies"],
  "assignees": ["jbyrd"]
}
```

### Benefits

- ✅ Always up-to-date
- ✅ Security patches automatic
- ✅ Proven library updates
- ✅ No manual work
- ✅ Tested before merge

---

## Part 10: Chaos Engineering (Netflix Pattern)

### What It Is

```
Traditional: Hope it works
  ↓
Production breaks
  ↓
Panic

Chaos: Break it on purpose
  ↓
Find weaknesses
  ↓
Fix before customers hit them
  ↓
Confidence in resilience
```

### Why It Fits

- **Test resilience**
- **Find weaknesses**
- **Confidence**
- **Prevent outages**

### How PAI Uses It

**Chaos Testing for RFE Tool:**
```python
# tests/chaos/test_resilience.py
"""
Chaos engineering tests
Ensure RFE tool handles failures gracefully
"""
import pytest
from foundation.chaos import chaos_monkey

@chaos_monkey.kill_dependency('hydra-api', probability=0.5)
def test_hydra_api_failure():
    """
    Chaos: Hydra API fails 50% of requests
    Expected: Circuit breaker opens, graceful degradation
    """
    # Should fall back to rhcase
    cases = rfe_service.get_customer_cases('397076')
    assert cases is not None
    assert len(cases) > 0

@chaos_monkey.slow_dependency('gitlab-api', latency_ms=5000)
def test_slow_gitlab():
    """
    Chaos: GitLab API responds slowly (5s)
    Expected: Timeout, retry, eventual success
    """
    issues = gitlab_service.get_issues()
    assert issues is not None

@chaos_monkey.network_partition('redis', duration_sec=10)
def test_cache_failure():
    """
    Chaos: Redis unavailable
    Expected: Cache miss, fetch from source
    """
    data = rfe_service.get_cached_data('key')
    assert data is not None  # Should fetch from source

# Run chaos tests in staging
# Verify system handles failures
```

### Benefits

- ✅ Find weaknesses
- ✅ Test circuit breakers
- ✅ Verify graceful degradation
- ✅ Confidence in production
- ✅ Prevent outages

---

## Part 11: Documentation as Code (Swagger/OpenAPI Pattern)

### What It Is

```
Traditional: Docs separate from code
  ↓
Code changes
  ↓
Docs out of date
  ↓
Frustration

Docs as Code: Generated from code
  ↓
Code changes = Docs update
  ↓
Always in sync
```

### Why It Fits

- **Always accurate**
- **No manual updates**
- **Interactive docs**
- **Contract testing source**

### How PAI Uses It

**FastAPI (Already Does This):**
```python
# app/routes/customers.py
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Customer(BaseModel):
    """Customer data model"""
    account_id: str
    name: str
    region: str

@router.get("/customers/{account_id}", response_model=Customer)
async def get_customer(account_id: str):
    """
    Get customer details
    
    Returns:
        Customer: Full customer information
    
    Raises:
        404: Customer not found
    """
    return customer_service.get(account_id)

# Docs auto-generated:
# - /docs (Swagger UI)
# - /redoc (ReDoc)
# - /openapi.json (OpenAPI spec)
```

### Benefits

- ✅ Always accurate
- ✅ Interactive testing
- ✅ Contract source
- ✅ No manual docs
- ✅ Generated from code

---

## Part 12: The Complete Integration

### How Everything Fits Together

```
┌─────────────────────────────────────────────────────────┐
│                    Your Business Logic                  │
│                      (5% custom)                        │
├─────────────────────────────────────────────────────────┤
│              Pattern Integration Layer                  │
│  ┌───────────────────────────────────────────────────┐  │
│  │ GitOps │ Feature Flags │ Observability │ Chaos  │  │
│  ├───────────────────────────────────────────────────┤  │
│  │ Policy │ Self-Service │ Contracts │ Dependency  │  │
│  └───────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│              PAI Foundation (95%)                       │
│  ┌───────────────────────────────────────────────────┐  │
│  │ Geerling │ Lego │ SRE │ OS-Agnostic │ Resilience │  │
│  └───────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│              Proven Libraries                           │
└─────────────────────────────────────────────────────────┘
```

### Implementation Priority

**Phase 1 (Already Have):**
- ✅ Geerling pattern (proven libraries)
- ✅ Lego architecture (modular services)
- ✅ SRE basics (health checks, metrics)
- ✅ OS-agnostic (cross-platform)

**Phase 2 (Easy Wins):**
1. **GitOps** - Already using Git, just enforce it
2. **Immutable Infrastructure** - Already doing with containers
3. **Documentation as Code** - FastAPI does this
4. **Dependency Management** - Add Renovate bot

**Phase 3 (High Impact):**
1. **Feature Flags** - Safe rollouts, instant rollback
2. **Observability Triad** - Add distributed tracing
3. **Policy as Code** - Automate Red Hat compliance
4. **Self-Service** - PAI service portal

**Phase 4 (Advanced):**
1. **Progressive Delivery** - Canary deployments
2. **Contract Testing** - API stability
3. **Chaos Engineering** - Resilience testing

---

## Bottom Line

### Traditional Approach

```
Every pattern implemented from scratch
Every project reinvents resilience
Every team learns by failing in production
Result: Years to world-class, if ever
```

### PAI Approach

```
Steal proven patterns from giants:
  Netflix → Chaos engineering, feature flags
  Google → SRE, observability
  Weaveworks → GitOps
  Spotify → Self-service infrastructure
  HashiCorp → Immutable infrastructure
  
Result: World-class in months
```

### The Stack

**Infrastructure:** Ansible (Geerling) + GitOps  
**Applications:** FastAPI + Foundation (95% proven)  
**Deployment:** Immutable + Progressive delivery  
**Operations:** SRE + Observability + Chaos  
**Governance:** Policy as Code + Contracts  
**Developer Experience:** Self-service + Docs as Code  

**Result:**
- ✅ Deploy anytime (feature flags)
- ✅ Rollback instantly (immutable + GitOps)
- ✅ Compliant automatically (policy as code)
- ✅ Resilient by design (SRE + chaos)
- ✅ Fast delivery (self-service)
- ✅ Always documented (docs as code)
- ✅ Proven patterns (giants' shoulders)

**This is the gold standard.** World-class without reinventing.

---

*Philosophy: Learn from Giants, Integrate Proven Patterns*  
*Pattern: Steal the Best, Adapt to Your Context*  
*Result: World-class tools in months, not years*
