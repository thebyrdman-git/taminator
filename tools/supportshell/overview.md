# SupportShell Tools Overview

SupportShell is Red Hat's secure environment for analyzing customer data and troubleshooting issues.

## Access
```bash
ssh -o ServerAliveInterval=500 -o ServerAliveCountMax=5 \
    -o ControlMaster=auto -o ControlPath="~/.ssh/sushe/%C" \
    -o ControlPersist=8h \
    gvaughn@supportshell-1.sush-001.prod.us-west-2.aws.redhat.com
```

## Available Tools

### Log Analysis
- **yank-ng**: Extract and analyze logs from various sources
- **must-gather-explorer**: Analyze OpenShift must-gather archives
- **insights-client**: Run Red Hat Insights analysis

### System Analysis
- **sosreport**: Collect system diagnostics
- **retrace-server**: Analyze crash dumps and core files
- **prometheus-query**: Query Prometheus metrics

### OpenShift Tools
- **oc**: OpenShift CLI for cluster operations
- **kubectl**: Kubernetes CLI
- **helm**: Kubernetes package manager

### Container Tools
- **podman**: Container runtime
- **skopeo**: Container image operations
- **cri-o**: Container runtime interface

## Key Features
- Isolated environment for customer data
- Pre-installed diagnostic tools
- Direct access to case attachments
- Integration with Red Hat systems

## Common Workflows

### Analyze Case Attachments
```bash
# List case attachments
case-files 03719989

# Extract must-gather
must-gather-explorer analyze /case/03719989/must-gather.tar.gz
```

### Run Diagnostics
```bash
# Analyze logs
yank-ng --case 03719989 --pattern "error|fatal"

# Check insights
insights-client --analyze /case/03719989/sosreport.tar.xz
```

## Security Notes
- Customer data stays in SupportShell
- No direct download of sensitive data
- Audit logging of all activities
- Time-limited access per session
