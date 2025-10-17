# PAI Framework - Industry-Standard Terminology

**Purpose:** Ensure all documentation uses professional, industry-recognized terminology

---

## Terminology Mapping

### Architecture & Design Patterns

| ❌ Avoid | ✅ Use Instead | Rationale |
|---------|---------------|-----------|
| Lego blocks | Composable services | Industry standard for microservices |
| Lego Architecture | Composable Service Architecture | Professional terminology |
| Lego-style | Component-based / Declarative | Technical accuracy |
| Snap together | Compose / Orchestrate | Standard DevOps terminology |
| Plug-and-play | Declarative deployment | Infrastructure as Code terminology |
| Self-wiring | Service mesh / Dynamic routing | Kubernetes/Istio terminology |
| Auto-wiring | Service discovery | Industry-standard microservices term |
| Auto-wiring magic | Automatic service discovery | Remove "magic", use technical term |
| Zero-config | Declarative configuration | More accurate - config exists, just centralized |

### Performance & Quality

| ❌ Avoid | ✅ Use Instead | Rationale |
|---------|---------------|-----------|
| Lightning-fast | Sub-minute / Rapid | Quantifiable metrics |
| Fast as lightning | < 60 seconds | Specific measurements |
| Blazing fast | High-performance | Industry standard |
| Seamless | Integrated / Unified | Less marketing-speak |
| Amazing | Efficient / Effective | Professional |
| Awesome | High-quality / Proven | Professional |
| Wonderful | Reliable / Robust | Professional |
| Magical | Automated / Dynamic | Technical accuracy |

### Deployment & Operations

| ❌ Avoid | ✅ Use Instead | Rationale |
|---------|---------------|-----------|
| One-click | Single-command | More accurate |
| Drop-in | Modular / Composable | Industry standard |
| Batteries included | Full-featured | Less colloquial |

---

## Approved Industry Terms

### Architecture Patterns
- **Microservices Architecture** - Distributed system of loosely coupled services
- **Service Mesh** - Infrastructure layer for service-to-service communication
- **Composable Services** - Modular services that can be combined
- **Service Catalog** - Registry of available services
- **Infrastructure as Code (IaC)** - Managing infrastructure via declarative code
- **GitOps** - Git as single source of truth for declarative infrastructure
- **Declarative Configuration** - Describing desired state, not procedures

### Deployment Patterns
- **Service Discovery** - Automatic detection and registration of services
- **Dynamic Routing** - Runtime traffic routing based on configuration
- **Zero-downtime Deployment** - Deployment without service interruption
- **Immutable Infrastructure** - Servers are never modified after deployment
- **Blue-Green Deployment** - Two identical production environments
- **Canary Deployment** - Gradual rollout to subset of users

### Reliability Patterns (SRE)
- **Health Checks** - Automated service health monitoring
- **Circuit Breaker** - Failure isolation pattern
- **Graceful Degradation** - Reduced functionality under load
- **Retry with Exponential Backoff** - Automatic retry with increasing delays
- **Observability** - Understanding system state from external outputs
- **Monitoring** - Collecting and analyzing metrics
- **Alerting** - Automated notification of issues

### Configuration Management
- **Single Source of Truth** - One authoritative data source
- **Configuration as Code** - Version-controlled configuration
- **Environment Parity** - Dev/staging/prod consistency
- **Feature Flags** - Runtime behavior toggles
- **Secrets Management** - Secure credential storage

---

## Documentation Standards

### Technical Writing Guidelines

1. **Be Specific, Not Vague**
   - ❌ "Really fast deployment"
   - ✅ "Deployment completes in < 60 seconds"

2. **Use Metrics, Not Adjectives**
   - ❌ "Amazing performance"
   - ✅ "99.9% availability (43 min downtime/month)"

3. **Technical Terms, Not Marketing**
   - ❌ "Magical auto-wiring"
   - ✅ "Automatic service discovery via Traefik labels"

4. **Industry Patterns, Not Metaphors**
   - ❌ "Like snapping Lego blocks together"
   - ✅ "Declarative service composition"

5. **Quantify Benefits**
   - ❌ "Much faster than before"
   - ✅ "10x reduction in deployment time (4 hours → 20 minutes)"

---

## Examples of Proper Usage

### Before (Casual)
```markdown
# Lego-Style Infrastructure

Just snap these blocks together like Lego! It's amazing - services auto-wire 
themselves and everything just works. Lightning-fast deployments with zero config!
```

### After (Professional)
```markdown
# Composable Service Architecture

Services are deployed via declarative configuration. The service mesh automatically 
handles routing, TLS termination, and health monitoring. Deployments complete in 
< 60 seconds with centralized configuration management.
```

### Before (Marketing)
```markdown
Our awesome plug-and-play system makes everything seamless and magical!
```

### After (Technical)
```markdown
Our declarative deployment system provides automatic service discovery, 
dynamic routing configuration, and integrated monitoring with minimal 
operator intervention.
```

---

## References

These terms come from:

- **Microservices:** Martin Fowler, Sam Newman
- **Service Mesh:** Istio, Linkerd, Consul
- **SRE:** Google Site Reliability Engineering book
- **IaC:** HashiCorp, Terraform, Ansible
- **GitOps:** Weaveworks, Flux, ArgoCD
- **Kubernetes:** Cloud Native Computing Foundation
- **DevOps:** The Phoenix Project, The DevOps Handbook

---

*Last Updated: 2025-10-17*  
*Maintained by: PAI Framework*  
*Purpose: Professional, industry-standard documentation*

