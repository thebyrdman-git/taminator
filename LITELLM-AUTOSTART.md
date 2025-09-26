# LiteLLM Auto-Start Configuration

LiteLLM is now configured to automatically start at login using systemd user services.

## 🚀 Auto-Start Status

✅ **Service Enabled**: LiteLLM will start automatically when you log in  
✅ **Currently Running**: Service is active and responding  
✅ **API Available**: http://localhost:4000  
✅ **Linger Enabled**: Service will keep running even if you log out  

## 🎛️ Service Management

Use the `pai-litellm-service` command to manage the auto-start service:

### Basic Commands
```bash
# Check service status
pai-litellm-service status

# Start/stop/restart the service
pai-litellm-service start
pai-litellm-service stop  
pai-litellm-service restart

# Enable/disable auto-start at login
pai-litellm-service enable
pai-litellm-service disable

# View service logs
pai-litellm-service logs
pai-litellm-service logs 100  # Show last 100 lines

# Test API connectivity
pai-litellm-service test

# Show help
pai-litellm-service help
```

### Service Status Example
```
[PAI-LiteLLM-Service] LiteLLM Service Status
======================
[PAI-LiteLLM-Service] ✅ Service is enabled (will start at login)
[PAI-LiteLLM-Service] ✅ Service is running
[PAI-LiteLLM-Service] ✅ API is responding
[PAI-LiteLLM-Service] 🌐 Available at: http://localhost:4000
```

## 🔧 Technical Details

### Systemd Service Configuration
- **Service File**: `~/.config/systemd/user/pai-litellm.service`
- **Service Name**: `pai-litellm.service`
- **Run Level**: User service (starts with user session)
- **Auto-Restart**: Yes (restarts automatically if it crashes)
- **Resource Limits**: 2GB RAM limit, 65536 file descriptors

### Key Features
- **Automatic Startup**: Starts when you log in
- **Crash Recovery**: Automatically restarts if it fails
- **Resource Protection**: Memory and file descriptor limits
- **Security Hardening**: Runs with restricted privileges
- **Logging**: Full systemd journal integration

### Advanced systemctl Commands
```bash
# Direct systemd management (if needed)
systemctl --user status pai-litellm.service
systemctl --user restart pai-litellm.service
systemctl --user enable pai-litellm.service
systemctl --user disable pai-litellm.service

# View detailed logs
journalctl --user -u pai-litellm.service -f  # Follow logs in real-time
journalctl --user -u pai-litellm.service --since "1 hour ago"
```

## 📊 Service Monitoring

### Health Check
```bash
# Quick health check
curl http://localhost:4000/health

# Full API test
curl http://localhost:4000/v1/models
```

### Performance Monitoring
```bash
# Check resource usage
systemctl --user status pai-litellm.service

# Monitor in real-time
watch -n 5 'systemctl --user status pai-litellm.service'
```

## 🛠️ Troubleshooting

### Service Won't Start
```bash
# Check detailed status
pai-litellm-service status

# View recent logs
pai-litellm-service logs 50

# Restart the service
pai-litellm-service restart
```

### API Not Responding
```bash
# Test connectivity
pai-litellm-service test

# Check if port is blocked
sudo netstat -tlnp | grep :4000

# Restart service
pai-litellm-service restart
```

### Disable Auto-Start (if needed)
```bash
# Disable auto-start but keep service running
pai-litellm-service disable

# Stop and disable
pai-litellm-service stop
pai-litellm-service disable
```

## 🔄 What Happens at Login

1. **User Session Starts**: You log into your desktop/session
2. **Systemd User Manager**: Starts your user services
3. **PAI LiteLLM Service**: Automatically starts in the background
4. **Network Check**: Waits for network connectivity
5. **LiteLLM Startup**: Loads configuration and starts proxy server
6. **API Available**: Red Hat models accessible at http://localhost:4000
7. **Health Monitoring**: Service monitors itself and auto-restarts if needed

## 📱 Integration with Other PAI Tools

All your existing PAI tools that use LiteLLM will now work automatically:
- `pai-fabric-compliant` - Uses local LiteLLM proxy
- `pai-case-processor` - Can leverage Red Hat models
- `pai-email-processor` - Text analysis with Granite models

The service provides a stable, always-available AI inference endpoint for your entire PAI ecosystem.

---

*Auto-start configured on $(date)*  
*Part of the PAI (Personal AI Infrastructure) System*
