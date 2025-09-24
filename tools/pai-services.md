# pai-services

Manage PAI infrastructure services via systemd.

## Location
`~/.local/bin/pai-services`

## Description
Helper script to manage PAI services (Qdrant, Open WebUI, n8n, Ollama) running under Podman Compose with systemd integration.

## Commands

### Start Services
```bash
pai-services start
```

### Stop Services
```bash
pai-services stop
```

### Restart Services
```bash
pai-services restart
```

### Check Status
```bash
pai-services status
```

### View Logs
```bash
pai-services logs
# Follows logs in real-time
```

### Enable Auto-start
```bash
pai-services enable
# Services start automatically on login
```

### Disable Auto-start
```bash
pai-services disable
```

## Service Endpoints
When running, services are available at:
- **Qdrant**: http://localhost:6333 (vector database)
- **Open WebUI**: http://localhost:8080 (AI chat interface)
- **n8n**: http://localhost:5678 (workflow automation)
- **Ollama**: http://localhost:11434 (local model runner)

## Configuration
- Service definitions: `~/.claude/pai/services/podman-compose.yml`
- Systemd unit: `~/.config/systemd/user/pai-services.service`
- Data volumes: `~/.claude/pai/services/*/data`

## Resource Limits
- Memory: 8GB maximum
- CPU: 200% quota (2 cores)

## Troubleshooting
```bash
# Check individual container status
cd ~/.claude/pai/services
podman-compose ps

# View specific service logs
podman-compose logs qdrant
podman-compose logs openwebui

# Restart individual service
podman-compose restart openwebui
```

## Environment
Requires API keys to be set:
```fish
source ~/.claude/pai/config/export-model-keys.fish
```
