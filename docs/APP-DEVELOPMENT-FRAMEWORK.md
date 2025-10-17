# Application Development Framework: Gold Standard Template

**Philosophy:** 95% reusable foundation + 5% custom business logic = New app  
**Pattern:** Clone → Configure → Build new flavor  
**Result:** New production-ready apps in hours, not months

---

## The Vision

### Traditional App Development

```
New App Idea:
  ↓
Start from scratch:
  - Set up authentication (2 weeks)
  - Build database layer (1 week)
  - Create API framework (1 week)
  - Add logging (3 days)
  - Set up monitoring (3 days)
  - Add health checks (2 days)
  - Configure CI/CD (1 week)
  - Write tests (1 week)
  - Add documentation (3 days)
  ↓
Finally start on actual business logic (Month 2)
  ↓
Result: 80% boilerplate, 20% unique value
Time: 2-3 months to production
```

### PAI App Development Framework

```
New App Idea:
  ↓
Clone framework:
  - Authentication ✅ (already built)
  - Database layer ✅ (already built)
  - API framework ✅ (already built)
  - Logging ✅ (already built)
  - Monitoring ✅ (already built)
  - Health checks ✅ (already built)
  - CI/CD ✅ (already built)
  - Tests ✅ (already built)
  - Documentation ✅ (already built)
  ↓
Write ONLY business logic (Day 1)
  ↓
Result: 95% proven foundation, 5% unique value
Time: Days to production
```

---

## Part 1: The Foundation (Reusable)

### Foundation Stack Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Your App Logic                    │
│              (5% - Your Unique Value)               │
├─────────────────────────────────────────────────────┤
│              Business Logic Layer                   │
│         (Your routes, handlers, logic)              │
├─────────────────────────────────────────────────────┤
│              Foundation Layer (95%)                 │
│  ┌──────────────────────────────────────────────┐  │
│  │ Authentication │ Database │ Logging │ Cache │  │
│  ├──────────────────────────────────────────────┤  │
│  │ Health Checks │ Metrics │ Config │ Secrets  │  │
│  ├──────────────────────────────────────────────┤  │
│  │ Error Handling │ Validation │ Middleware    │  │
│  ├──────────────────────────────────────────────┤  │
│  │ API Framework │ CLI │ Background Jobs       │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
         Built on Proven Libraries (Geerling Pattern)
```

### Foundation Repository Structure

```
pai-app-foundation/
├── README.md                    # "Clone to build your app"
├── requirements.txt             # Proven dependencies
├── Dockerfile                   # Multi-stage build
├── docker-compose.yml           # Local development
├── .github/workflows/           # CI/CD ready
│
├── foundation/                  # The 95% (DON'T CHANGE)
│   ├── __init__.py
│   ├── auth/                    # Authentication (proven)
│   │   ├── jwt.py
│   │   ├── oauth.py
│   │   └── rbac.py
│   ├── database/                # Database (proven)
│   │   ├── base.py
│   │   ├── session.py
│   │   └── models.py
│   ├── api/                     # API framework (proven)
│   │   ├── app.py
│   │   ├── middleware.py
│   │   └── errors.py
│   ├── monitoring/              # Observability (proven)
│   │   ├── health.py
│   │   ├── metrics.py
│   │   └── logging.py
│   ├── cache/                   # Caching (proven)
│   │   ├── redis.py
│   │   └── memory.py
│   ├── queue/                   # Background jobs (proven)
│   │   ├── celery.py
│   │   └── tasks.py
│   ├── config/                  # Configuration (proven)
│   │   ├── settings.py
│   │   └── secrets.py
│   └── utils/                   # Utilities (proven)
│       ├── validation.py
│       ├── serialization.py
│       └── pagination.py
│
├── app/                         # The 5% (YOUR CHANGES)
│   ├── __init__.py
│   ├── config.yml               # Your app config
│   ├── routes/                  # Your API routes
│   │   └── __init__.py
│   ├── models/                  # Your data models
│   │   └── __init__.py
│   ├── services/                # Your business logic
│   │   └── __init__.py
│   └── cli/                     # Your CLI commands
│       └── __init__.py
│
├── tests/                       # Tests (foundation + yours)
│   ├── foundation/              # Foundation tests (DON'T CHANGE)
│   └── app/                     # Your app tests
│
└── docs/
    ├── FOUNDATION.md            # Foundation docs
    ├── QUICKSTART.md            # Build your first app
    └── DEPLOYMENT.md            # Deploy to production
```

---

## Part 2: The Foundation Code

### `foundation/api/app.py` (Proven Flask/FastAPI Foundation)

```python
"""
Foundation API Framework
DO NOT MODIFY - This is the proven, battle-tested foundation
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import structlog
from prometheus_client import Counter, Histogram
import time

from foundation.monitoring import health, metrics, logging
from foundation.config import settings
from foundation.database import database
from foundation.cache import cache
from foundation.auth import auth_middleware

# Proven libraries (Geerling pattern)
log = structlog.get_logger()

# Metrics (SRE pattern)
REQUEST_COUNT = Counter('http_requests_total', 'Total requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'Request duration', ['method', 'endpoint'])

def create_app(app_config: dict = None) -> FastAPI:
    """
    Create production-ready FastAPI app with all foundation features
    
    This function is the foundation - it includes:
    - Health checks
    - Metrics
    - Logging
    - Error handling
    - Authentication
    - Database
    - Cache
    - CORS
    
    Your app just provides routes and business logic
    """
    app = FastAPI(
        title=app_config.get('name', 'PAI App'),
        version=app_config.get('version', '1.0.0'),
        docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    )
    
    # CORS (configurable)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_config.get('cors_origins', ["*"]),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Request timing middleware (SRE pattern)
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        
        # Log request
        log.info("request_started",
                 method=request.method,
                 path=request.url.path,
                 client=request.client.host)
        
        try:
            response = await call_next(request)
            
            # Record metrics
            duration = time.time() - start_time
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                status=response.status_code
            ).inc()
            REQUEST_DURATION.labels(
                method=request.method,
                endpoint=request.url.path
            ).observe(duration)
            
            # Log response
            log.info("request_completed",
                     method=request.method,
                     path=request.url.path,
                     status=response.status_code,
                     duration=duration)
            
            response.headers["X-Process-Time"] = str(duration)
            return response
            
        except Exception as e:
            # Log error
            log.error("request_failed",
                      method=request.method,
                      path=request.url.path,
                      error=str(e))
            
            # Return error response
            return JSONResponse(
                status_code=500,
                content={"error": "Internal server error", "message": str(e)}
            )
    
    # Authentication middleware (if enabled)
    if app_config.get('auth_enabled', True):
        app.add_middleware(auth_middleware.AuthMiddleware)
    
    # Foundation routes (don't change these)
    app.include_router(health.router, prefix="/health", tags=["health"])
    app.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
    
    # Startup events
    @app.on_event("startup")
    async def startup():
        log.info("app_starting", name=app_config.get('name'))
        
        # Initialize database
        if app_config.get('database_enabled', True):
            await database.connect()
            log.info("database_connected")
        
        # Initialize cache
        if app_config.get('cache_enabled', True):
            await cache.connect()
            log.info("cache_connected")
        
        log.info("app_started")
    
    # Shutdown events
    @app.on_event("shutdown")
    async def shutdown():
        log.info("app_stopping")
        
        if app_config.get('database_enabled', True):
            await database.disconnect()
        
        if app_config.get('cache_enabled', True):
            await cache.disconnect()
        
        log.info("app_stopped")
    
    return app
```

### `foundation/monitoring/health.py` (Kubernetes Pattern)

```python
"""
Foundation Health Checks
DO NOT MODIFY - Kubernetes/SRE best practices
"""
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import asyncio
from typing import Dict, Any

from foundation.database import database
from foundation.cache import cache

router = APIRouter()

@router.get("/live")
async def liveness():
    """
    Liveness probe - Is the app running?
    Kubernetes uses this to restart crashed containers
    """
    return {"status": "alive"}

@router.get("/ready")
async def readiness():
    """
    Readiness probe - Is the app ready to serve traffic?
    Kubernetes uses this to route traffic
    """
    health_checks = {
        "status": "healthy",
        "checks": {}
    }
    
    # Check database
    try:
        await database.execute("SELECT 1")
        health_checks["checks"]["database"] = "healthy"
    except Exception as e:
        health_checks["checks"]["database"] = f"unhealthy: {e}"
        health_checks["status"] = "unhealthy"
    
    # Check cache
    try:
        await cache.ping()
        health_checks["checks"]["cache"] = "healthy"
    except Exception as e:
        health_checks["checks"]["cache"] = f"unhealthy: {e}"
        health_checks["status"] = "unhealthy"
    
    status_code = status.HTTP_200_OK if health_checks["status"] == "healthy" else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return JSONResponse(content=health_checks, status_code=status_code)

@router.get("/startup")
async def startup():
    """
    Startup probe - Has the app finished initializing?
    Kubernetes uses this for slow-starting apps
    """
    # Check if all initialization is complete
    checks = await asyncio.gather(
        database.is_ready(),
        cache.is_ready(),
        return_exceptions=True
    )
    
    if all(checks):
        return {"status": "ready"}
    else:
        return JSONResponse(
            content={"status": "starting", "checks": checks},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
```

---

## Part 3: Your App (The 5%)

### `app/config.yml` (Your Configuration)

```yaml
# Your App Configuration
# This is the ONLY file you need to configure for basic setup

name: "My Awesome App"
version: "1.0.0"
description: "My app built on PAI foundation"

# Foundation Features (enable/disable)
features:
  auth_enabled: true
  database_enabled: true
  cache_enabled: true
  background_jobs_enabled: false
  
# CORS (for web apps)
cors_origins:
  - "https://myapp.com"
  - "http://localhost:3000"

# Database (foundation handles connection)
database:
  auto_migrate: true
  pool_size: 10

# Cache (foundation handles connection)
cache:
  ttl: 3600  # 1 hour default

# Your custom settings
app:
  max_upload_size_mb: 10
  default_page_size: 50
  feature_flags:
    new_feature: false
```

### `app/routes/__init__.py` (Your Business Logic)

```python
"""
Your App Routes
THIS IS WHERE YOU ADD YOUR UNIQUE VALUE
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel

# Foundation provides these (don't reimplement)
from foundation.auth import get_current_user, User
from foundation.database import get_db, AsyncSession
from foundation.cache import cache
from foundation.utils import validate, paginate

# Your business logic
from app.services import business_logic
from app.models import YourModel

router = APIRouter(prefix="/api/v1", tags=["your-app"])

# Your endpoints (focus on business logic only)
@router.get("/items")
async def list_items(
    page: int = 1,
    user: User = Depends(get_current_user),  # Auth from foundation
    db: AsyncSession = Depends(get_db)       # DB from foundation
):
    """
    Your business logic - foundation handles:
    - Authentication (user is already validated)
    - Database connection (db session ready)
    - Logging (request/response logged)
    - Metrics (request counted)
    - Error handling (exceptions caught)
    
    You just write your query!
    """
    # Check cache first (foundation provides this)
    cache_key = f"items:page:{page}:user:{user.id}"
    cached = await cache.get(cache_key)
    if cached:
        return cached
    
    # Your actual business logic (this is your 5%)
    items = await business_logic.get_user_items(db, user.id, page)
    
    # Cache result (foundation provides this)
    await cache.set(cache_key, items, ttl=300)
    
    return items

@router.post("/items")
async def create_item(
    item_data: dict,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create new item - your business logic only
    Foundation handles validation, auth, db, logging, etc.
    """
    # Validate (foundation provides this)
    validated = validate(item_data, YourModel)
    
    # Your business logic
    new_item = await business_logic.create_item(db, user.id, validated)
    
    # Invalidate cache
    await cache.delete(f"items:*:user:{user.id}")
    
    return new_item
```

---

## Part 4: Building New Apps

### Step 1: Clone Foundation

```bash
# Clone the foundation template
git clone https://github.com/jbyrd/pai-app-foundation.git my-new-app
cd my-new-app

# Remove git history (start fresh)
rm -rf .git
git init
```

### Step 2: Configure Your App (ONE File)

```bash
# Edit your app config
vim app/config.yml

# Change:
# - name: "My New App"
# - features: What you need
# - app: Your custom settings
```

### Step 3: Write Your Business Logic

```bash
# Create your data models
vim app/models/user.py

# Create your business logic
vim app/services/user_service.py

# Create your API routes
vim app/routes/users.py

# Register routes in main.py
vim main.py  # Add: app.include_router(users.router)
```

### Step 4: Run Locally

```bash
# Install dependencies (proven stack)
pip install -r requirements.txt

# Run database migrations (foundation handles this)
alembic upgrade head

# Start app (foundation configured)
uvicorn main:app --reload

# Health check
curl http://localhost:8000/health/ready
# {  "status": "healthy", "checks": {"database": "healthy", "cache": "healthy"} }
```

### Step 5: Deploy

```bash
# Build Docker image (foundation Dockerfile)
docker build -t my-new-app:1.0 .

# Deploy to Kubernetes (foundation manifests)
kubectl apply -f k8s/

# Or deploy with Ansible (foundation playbook)
ansible-playbook deploy.yml
```

**Done!** Production-ready app in hours, not months.

---

## Part 5: Real-World Examples

### Example 1: Todo App (2 Hours)

**What you write:**
```python
# app/models/todo.py (10 lines)
class Todo(BaseModel):
    title: str
    completed: bool = False

# app/services/todo_service.py (30 lines)
async def get_todos(db, user_id):
    return await db.query(Todo).filter_by(user_id=user_id).all()

async def create_todo(db, user_id, title):
    todo = Todo(user_id=user_id, title=title)
    db.add(todo)
    await db.commit()
    return todo

# app/routes/todos.py (40 lines)
@router.get("/todos")
async def list_todos(user: User = Depends(get_current_user), db = Depends(get_db)):
    return await todo_service.get_todos(db, user.id)

@router.post("/todos")
async def create_todo(data: dict, user: User = Depends(get_current_user), db = Depends(get_db)):
    return await todo_service.create_todo(db, user.id, data["title"])
```

**What you get:**
- ✅ REST API (foundation)
- ✅ Authentication (foundation)
- ✅ Database (foundation)
- ✅ Caching (foundation)
- ✅ Logging (foundation)
- ✅ Metrics (foundation)
- ✅ Health checks (foundation)
- ✅ Docker deployment (foundation)
- ✅ Kubernetes manifests (foundation)

**Time:** 2 hours (80 lines of business logic)

### Example 2: URL Shortener (3 Hours)

**What you write:**
```python
# app/services/url_service.py (50 lines)
import hashlib

async def shorten_url(db, long_url):
    # Generate short code
    short_code = hashlib.md5(long_url.encode()).hexdigest()[:6]
    
    # Check cache first
    cached = await cache.get(f"url:{short_code}")
    if cached:
        return cached
    
    # Save to database
    url = ShortURL(code=short_code, url=long_url)
    db.add(url)
    await db.commit()
    
    # Cache it
    await cache.set(f"url:{short_code}", long_url, ttl=86400)
    
    return short_code

# app/routes/urls.py (60 lines)
@router.post("/shorten")
async def shorten(data: dict, db = Depends(get_db)):
    code = await url_service.shorten_url(db, data["url"])
    return {"short_url": f"https://myapp.com/{code}"}

@router.get("/{code}")
async def redirect(code: str, db = Depends(get_db)):
    url = await url_service.get_url(db, code)
    return RedirectResponse(url)
```

**Time:** 3 hours (110 lines of business logic)

### Example 3: TAM RFE Chat (Your Current Tool) - Refactored

**Before (custom everything):**
- 500 lines custom code
- Custom auth, custom DB, custom logging
- Custom health checks, custom metrics
- 2 weeks to build

**After (foundation):**
```python
# app/services/rfe_service.py (200 lines - your unique logic)
from rhcase import RHCase  # Proven library (Geerling pattern)
from pybreaker import CircuitBreaker  # Netflix pattern
from foundation.cache import cache  # Foundation
from foundation.database import get_db  # Foundation

breaker = CircuitBreaker(fail_max=5)

@breaker
async def get_customer_cases(account_id):
    # Your business logic (200 lines)
    # Everything else from foundation
    pass

# app/routes/rfe.py (100 lines - your API)
@router.get("/customers/{account_id}/cases")
async def get_cases(account_id: str, user: User = Depends(get_current_user)):
    return await rfe_service.get_customer_cases(account_id)
```

**After:**
- 300 lines business logic
- Auth/DB/logging/health/metrics from foundation
- 2 days to build

---

## Part 6: The Gold Standard Template

### `pai-app-foundation` Repository (Public Template)

**Make this the gold standard:**

```markdown
# PAI App Foundation - Gold Standard Template

## What Is This?

The proven, battle-tested foundation for building production-ready applications.

**Foundation provides (95%):**
- ✅ Authentication (JWT, OAuth, RBAC)
- ✅ Database (PostgreSQL, async, migrations)
- ✅ Caching (Redis, memory)
- ✅ API Framework (FastAPI, validated)
- ✅ Monitoring (Prometheus, health checks)
- ✅ Logging (Structured, Loki)
- ✅ Background Jobs (Celery, async)
- ✅ Error Handling (Graceful, logged)
- ✅ Configuration (12-factor, secrets)
- ✅ Testing (Pytest, fixtures)
- ✅ CI/CD (GitHub Actions, GitLab CI)
- ✅ Docker (Multi-stage, optimized)
- ✅ Kubernetes (Manifests, helm)
- ✅ Documentation (OpenAPI, examples)

**You provide (5%):**
- 🎯 Your business logic
- 🎯 Your data models
- 🎯 Your API routes
- 🎯 Your configuration

## Philosophy

Built on proven patterns:
- **Geerling Pattern:** Use proven libraries, not custom
- **SRE Pattern:** Health checks, metrics, logging
- **12-Factor:** Configuration, stateless, logs
- **Netflix Pattern:** Circuit breakers, graceful degradation
- **Kubernetes Pattern:** Liveness, readiness, startup probes

## Quick Start

### 1. Clone Template
\`\`\`bash
git clone https://github.com/jbyrd/pai-app-foundation.git my-app
cd my-app
\`\`\`

### 2. Configure (ONE File)
\`\`\`bash
vim app/config.yml  # Set app name, features
\`\`\`

### 3. Write Business Logic
\`\`\`bash
vim app/services/my_service.py  # Your logic
vim app/routes/my_routes.py     # Your API
\`\`\`

### 4. Run
\`\`\`bash
docker-compose up  # Everything works
\`\`\`

### 5. Deploy
\`\`\`bash
kubectl apply -f k8s/  # Production ready
\`\`\`

## Time to Production

| Task | Traditional | With Foundation |
|------|-------------|-----------------|
| Setup infrastructure | 2 weeks | 0 minutes ✅ |
| Authentication | 1 week | 0 minutes ✅ |
| Database layer | 1 week | 0 minutes ✅ |
| API framework | 1 week | 0 minutes ✅ |
| Monitoring | 3 days | 0 minutes ✅ |
| Health checks | 2 days | 0 minutes ✅ |
| CI/CD | 1 week | 0 minutes ✅ |
| **Your business logic** | **Varies** | **Focus here** 🎯 |
| **Total** | **2-3 months** | **Days to weeks** |

## Examples

### Todo App (2 hours)
- 80 lines of business logic
- Full production-ready API

### URL Shortener (3 hours)
- 110 lines of business logic
- Deployed to Kubernetes

### Enterprise SaaS (2 weeks)
- 2,000 lines of business logic
- Multi-tenant, auth, billing, all production features

## Architecture

\`\`\`
Your App (5%) ─────────┐
                        │
Foundation (95%) ───────┤
                        │
Proven Libraries ───────┤ (Geerling Pattern)
                        │
Container Platform ─────┘ (K8s/Docker)
\`\`\`

## Support

- Docs: [docs/](docs/)
- Examples: [examples/](examples/)
- Issues: GitHub Issues
- Community: Discord

## License

MIT - Use for any project
\`\`\`

---

## Part 7: Integration with Infrastructure

### Your App → Ansible Framework → Deployed

**Step 1: Build app with foundation**
```bash
git clone pai-app-foundation my-app
cd my-app
# Write business logic (5%)
# Everything else provided (95%)
```

**Step 2: Add to Ansible service catalog**
```yaml
# ~/pai/ansible/group_vars/services.yml
my_app:
  image: mycompany/my-app:latest
  type: webapp
  port: 8000
  subdomain: myapp
  healthcheck_path: /health/ready  # Foundation provides this
  memory_limit: 512m
```

**Step 3: Enable in inventory**
```yaml
# ~/pai/ansible/inventory/my-server.yml
services_enabled:
  - my_app
```

**Step 4: Deploy**
```bash
ansible-playbook site.yml
```

**Result:**
- ✅ App built with foundation (95% proven)
- ✅ Deployed with Ansible (Lego block)
- ✅ Monitored (Prometheus + Grafana)
- ✅ Backed up (automated)
- ✅ SSL (Let's Encrypt)
- ✅ Production-ready

---

## Part 8: The Complete Philosophy

### Infrastructure + Applications = Complete System

```
PAI Complete Philosophy
========================

Infrastructure Layer (Ansible):
  - Geerling's roles (infrastructure)
  - Generic service roles (deployment)
  - Service catalog (available apps)
  - One config file (environment)
  
Application Layer (Foundation):
  - Proven libraries (functionality)
  - SRE patterns (resilience)
  - 12-factor (configuration)
  - Foundation code (95%)
  
Your Value Layer (Business Logic):
  - Data models (5%)
  - Business logic (5%)
  - API routes (5%)
  - Configuration (1 file)
  
Result:
  - Clone infrastructure framework
  - Clone app foundation
  - Write business logic
  - Deploy with one command
  - Production-ready in days
```

### The Numbers

| Layer | % of Code | Who Maintains |
|-------|-----------|---------------|
| Infrastructure | 90% | Geerling + Ansible community |
| Foundation | 5% | You (shared across apps) |
| App Logic | 5% | You (per app) |
| **Your Effort** | **5%** | **Focus here** ✅ |

### Time Comparison

| Task | Traditional | PAI Framework |
|------|-------------|---------------|
| **Infrastructure** | 1 month | 10 minutes |
| **App foundation** | 2 months | 0 (clone) |
| **Business logic** | 2 weeks | 2 weeks |
| **Testing** | 1 week | 1 day |
| **Deployment** | 1 week | 1 command |
| **Monitoring** | 1 week | 0 (built-in) |
| **Total** | **4-5 months** | **2-3 weeks** |

---

## Bottom Line

### Traditional Development

```
Every new app = Start from scratch
Every developer = Reinvents infrastructure
Every project = 80% boilerplate, 20% value
Time to production = Months
```

### PAI Framework

```
Every new app = Clone proven foundation
Every developer = Focus on business logic
Every project = 5% custom, 95% proven
Time to production = Days
```

### The Gold Standard

**Infrastructure:**
```bash
git clone pai-ansible-framework  # Proven infrastructure
vim inventory/my-server.yml      # Configure
ansible-playbook site.yml        # Deploy
```

**Applications:**
```bash
git clone pai-app-foundation     # Proven foundation
vim app/config.yml               # Configure
# Write business logic (app/*.py)
docker build && kubectl apply    # Deploy
```

**Result:**
- ✅ Infrastructure: 99% proven (Geerling + community)
- ✅ Applications: 95% proven (foundation + libraries)
- ✅ Your focus: Business logic (5% custom)
- ✅ Time to production: Days, not months
- ✅ Replicable: Anyone can clone and build

**This is the gold standard.** Others will emulate it.

---

*Philosophy: Foundation Layer + Business Logic = Complete Application*  
*Pattern: 95% Proven + 5% Custom = Production Ready*  
*Result: New apps in days, systematically applied*
