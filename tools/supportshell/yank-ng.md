# yank-ng

Advanced log extraction and analysis tool in SupportShell.

## Description
yank-ng is an enhanced version of the yank tool for extracting and analyzing log entries from various sources including compressed archives, systemd journals, and container logs.

## Basic Usage
```bash
# Extract logs from a case
yank-ng --case <case_number>

# Search for specific patterns
yank-ng --case <case_number> --pattern "error|fatal|panic"

# Time-based filtering
yank-ng --case <case_number> --since "2025-01-01" --until "2025-01-07"
```

## Advanced Options

### Pattern Matching
```bash
# Multiple patterns
yank-ng --pattern "OutOfMemory" --pattern "OOMKilled"

# Regex patterns
yank-ng --regex "pod-[0-9a-f]{8}"

# Exclude patterns
yank-ng --exclude "DEBUG" --exclude "INFO"
```

### Source Selection
```bash
# Specific log files
yank-ng --file "/var/log/messages" --file "/var/log/secure"

# Container logs
yank-ng --container "api-server" --namespace "openshift-apiserver"

# Systemd journals
yank-ng --unit "kubelet.service"
```

### Output Formats
```bash
# JSON output
yank-ng --format json > analysis.json

# CSV for spreadsheets
yank-ng --format csv > logs.csv

# Summary statistics
yank-ng --stats
```

## Common Use Cases

### OpenShift Analysis
```bash
# API server errors
yank-ng --namespace "openshift-apiserver" --pattern "error" --last 24h

# Node issues
yank-ng --node "worker-1" --pattern "NotReady|pressure"

# Pod failures
yank-ng --pattern "CrashLoopBackOff|ImagePullBackOff"
```

### RHEL System Analysis
```bash
# Kernel panics
yank-ng --pattern "kernel panic" --context 50

# Storage issues
yank-ng --pattern "I/O error|filesystem full"

# Security events
yank-ng --file "/var/log/secure" --pattern "Failed password"
```

## Performance Tips
- Use specific time ranges to reduce data volume
- Combine with case number for faster access
- Use --stats first to understand log volume
- Chain with other tools using pipes

## Integration Examples
```bash
# Find errors and get context
yank-ng --pattern "error" --context 10 | less

# Extract and count unique errors
yank-ng --pattern "error" | sort | uniq -c | sort -nr

# Generate timeline
yank-ng --format json | jq '.timestamp' | sort
```
