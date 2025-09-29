# Ansible Automation Platform External Logging Debug Configuration
## File-Based Logging for Splunk Agent Integration

**Red Hat Solution Reference:** [https://access.redhat.com/solutions/6985722](https://access.redhat.com/solutions/6985722)

---

## Overview

This guide addresses the common enterprise scenario where Ansible Automation Platform (AAP) cannot send logs directly to Splunk due to network security policies. Instead, AAP writes debug logs to local files that are then monitored by a Splunk Universal Forwarder or similar log collection agent.

## Prerequisites

- Ansible Automation Platform 2.x
- Splunk Universal Forwarder installed on AAP nodes
- Administrative access to AAP configuration
- Root/sudo access for file permissions

---

## Part 1: AAP File-Based Logging Configuration

### 1.1 Configure AAP Settings for File Logging

Add the following configuration to AAP (via Settings UI or `/etc/tower/settings.py`):

```python
# Disable direct network logging
LOGGING_AGGREGATOR_ENABLED = False

# Configure file-based debug logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(name)s %(process)d %(thread)d %(message)s'
        },
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s'
        }
    },
    'handlers': {
        'external_debug_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/tower/external_debug.log',
            'maxBytes': 50000000,  # 50MB
            'backupCount': 5,
            'formatter': 'json'
        },
        'job_events_file': {
            'level': 'DEBUG', 
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/tower/job_events.log',
            'maxBytes': 100000000,  # 100MB
            'backupCount': 10,
            'formatter': 'json'
        },
        'activity_stream_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/tower/activity_stream.log',
            'maxBytes': 50000000,  # 50MB
            'backupCount': 5,
            'formatter': 'json'
        }
    },
    'loggers': {
        'awx': {
            'handlers': ['external_debug_file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'awx.main.models.jobs': {
            'handlers': ['job_events_file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'activity_stream': {
            'handlers': ['activity_stream_file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'awx.main.tasks': {
            'handlers': ['external_debug_file'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}
```

### 1.2 Apply Configuration Changes

```bash
# Restart AAP services to apply logging changes
sudo systemctl restart automation-controller
sudo systemctl restart automation-hub  # if applicable

# Verify services are running
sudo systemctl status automation-controller
```

---

## Part 2: Splunk Universal Forwarder Configuration

### 2.1 Create Splunk App Structure

```bash
# Create application directory for AAP monitoring
sudo mkdir -p /opt/splunkforwarder/etc/apps/ansible_tower/local
sudo chown -R splunk:splunk /opt/splunkforwarder/etc/apps/ansible_tower
```

### 2.2 Configure Inputs

Create `/opt/splunkforwarder/etc/apps/ansible_tower/local/inputs.conf`:

```ini
[monitor:///var/log/tower/external_debug.log]
disabled = false
index = ansible_tower
sourcetype = ansible:tower:debug
source = ansible_tower_debug
host_segment = 3
# Extract hostname from file path

[monitor:///var/log/tower/job_events.log] 
disabled = false
index = ansible_tower
sourcetype = ansible:tower:jobs
source = ansible_tower_jobs
host_segment = 3

[monitor:///var/log/tower/activity_stream.log]
disabled = false
index = ansible_tower
sourcetype = ansible:tower:activity
source = ansible_tower_activity
host_segment = 3

[monitor:///var/log/tower/tower.log]
disabled = false
index = ansible_tower  
sourcetype = ansible:tower:main
source = ansible_tower_main
host_segment = 3

# Monitor job stdout/stderr files
[monitor:///var/lib/awx/job_status/**/stdout]
disabled = false
index = ansible_tower
sourcetype = ansible:job:stdout
source = ansible_job_output
recursive = true
followTail = 0

[monitor:///var/log/tower/management_playbooks.log]
disabled = false
index = ansible_tower
sourcetype = ansible:tower:management
source = ansible_tower_mgmt
host_segment = 3
```

### 2.3 Configure Props (Optional - for better parsing)

Create `/opt/splunkforwarder/etc/apps/ansible_tower/local/props.conf`:

```ini
[ansible:tower:debug]
SHOULD_LINEMERGE = false
LINE_BREAKER = ([\r\n]+)
TIME_PREFIX = {"asctime": "
TIME_FORMAT = %Y-%m-%d %H:%M:%S,%3N
TRUNCATE = 10000
KV_MODE = json

[ansible:tower:jobs]
SHOULD_LINEMERGE = false
LINE_BREAKER = ([\r\n]+) 
TIME_PREFIX = {"asctime": "
TIME_FORMAT = %Y-%m-%d %H:%M:%S,%3N
TRUNCATE = 10000
KV_MODE = json

[ansible:tower:activity]
SHOULD_LINEMERGE = false
LINE_BREAKER = ([\r\n]+)
TIME_PREFIX = {"asctime": "
TIME_FORMAT = %Y-%m-%d %H:%M:%S,%3N
KV_MODE = json
```

---

## Part 3: System Configuration

### 3.1 File Permissions and Access

```bash
# Ensure log directory exists with proper permissions
sudo mkdir -p /var/log/tower
sudo chown tower:tower /var/log/tower
sudo chmod 755 /var/log/tower

# Add splunk user to tower group for file access
sudo usermod -a -G tower splunk

# Test file access (should succeed without errors)
sudo -u splunk test -r /var/log/tower/tower.log
echo $?  # Should return 0
```

### 3.2 SELinux Configuration (if enabled)

```bash
# Check if SELinux is enforcing
getenforce

# If SELinux is enabled, set proper contexts
sudo setsebool -P httpd_can_network_connect 1
sudo semanage fcontext -a -t admin_home_t "/var/log/tower/external_debug.log"
sudo semanage fcontext -a -t admin_home_t "/var/log/tower/job_events.log"
sudo semanage fcontext -a -t admin_home_t "/var/log/tower/activity_stream.log"
sudo restorecon -Rv /var/log/tower/

# Verify contexts
ls -lZ /var/log/tower/
```

### 3.3 Log Rotation Setup

Create `/etc/logrotate.d/tower-external`:

```bash
/var/log/tower/external_debug.log /var/log/tower/job_events.log /var/log/tower/activity_stream.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    create 0644 tower tower
    sharedscripts
    postrotate
        systemctl reload automation-controller
        /opt/splunkforwarder/bin/splunk restart
    endscript
}
```

---

## Part 4: Restart and Verify

### 4.1 Restart Services

```bash
# Restart Splunk forwarder to pick up new configuration
sudo /opt/splunkforwarder/bin/splunk restart

# Restart AAP to initialize new log files
sudo systemctl restart automation-controller

# Wait for services to fully start
sleep 30
```

### 4.2 Verification Commands

```bash
# Check that AAP is writing to debug files
tail -f /var/log/tower/external_debug.log

# Verify Splunk forwarder is monitoring files
/opt/splunkforwarder/bin/splunk list monitor

# Check forwarder connectivity to indexers
/opt/splunkforwarder/bin/splunk show deploy-poll

# Test search in Splunk (from indexer/search head)
# Replace with your Splunk search interface
# | search index=ansible_tower sourcetype=ansible:tower:debug | head 10
```

---

## Part 5: Troubleshooting

### 5.1 Common Issues and Solutions

**Issue: No logs appearing in debug files**
```bash
# Check AAP service logs for errors
journalctl -u automation-controller -f

# Verify disk space
df -h /var/log

# Check file permissions
ls -la /var/log/tower/
```

**Issue: Splunk forwarder cannot read files**
```bash
# Verify splunk user can access files
sudo -u splunk cat /var/log/tower/external_debug.log

# Check group membership
groups splunk

# Review SELinux denials
sudo ausearch -m AVC -ts recent
```

**Issue: Data not reaching Splunk indexers**
```bash
# Check forwarder connectivity
/opt/splunkforwarder/bin/splunk list forward-server

# Review forwarder logs
tail -f /opt/splunkforwarder/var/log/splunk/splunkd.log

# Test network connectivity
telnet <indexer-ip> 9997
```

### 5.2 Debug Commands

```bash
# Generate test log entries
curl -X POST -k -H "Authorization: Bearer <token>" \
  https://aap-server/api/v2/jobs/<job-id>/start/

# Monitor real-time log generation
watch -n 1 "wc -l /var/log/tower/external_debug.log"

# Check JSON formatting
tail -1 /var/log/tower/external_debug.log | jq '.'
```

---

## Part 6: Splunk Search Examples

### 6.1 Basic Searches

```splunk
# View all AAP logs from last hour
index=ansible_tower earliest=-1h

# Job execution logs only
index=ansible_tower sourcetype=ansible:tower:jobs

# Debug level messages
index=ansible_tower levelname=DEBUG

# Failed jobs
index=ansible_tower sourcetype=ansible:tower:jobs status=failed
```

### 6.2 Advanced Analytics

```splunk
# Job completion times by template
index=ansible_tower sourcetype=ansible:tower:jobs 
| stats avg(elapsed) as avg_duration by job_template_name
| sort -avg_duration

# Error patterns
index=ansible_tower levelname=ERROR 
| rex field=message "(?<error_type>\w+Error)"
| stats count by error_type
| sort -count
```

---

## Configuration Summary

1. **AAP**: File-based logging with JSON format
2. **Splunk**: Universal Forwarder monitoring log files
3. **System**: Proper permissions and log rotation
4. **Security**: SELinux contexts and group access

This configuration provides reliable external logging for AAP without requiring direct network connections to Splunk, meeting most enterprise security requirements while enabling comprehensive log analysis.

---

**Document Version:** 1.0  
**Last Updated:** $(date)  
**Prepared for:** Customer Support Case  
**Red Hat Solution:** https://access.redhat.com/solutions/6985722
