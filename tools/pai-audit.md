# pai-audit

Security, audit logging, and secrets management system for PAI.

## Location
`~/.local/bin/pai-audit`

## Description
Comprehensive security layer providing audit logging, encrypted secrets management, data sensitivity detection, and secure fabric call wrapper with automatic redaction capabilities.

## Core Features
- **Audit Logging**: Comprehensive logging of all PAI operations
- **Secrets Management**: GPG-encrypted secret storage
- **Sensitivity Detection**: Automatic detection of sensitive data
- **Secure Fabric Calls**: Wrapper with auto-redaction for high-sensitivity data
- **Data Retention**: Configurable cleanup policies
- **Security Status**: Real-time security monitoring

## Commands

### Audit Logging
```bash
pai-audit log <type> <details>              # Manual audit entry
pai-audit show-log [filter] [lines]         # View audit logs

# Examples:
pai-audit log "CASE_ACCESS" "Accessed case 04056105"
pai-audit show-log "FABRIC_CALL" 20
pai-audit show-log                          # Show last 50 entries
```

### Secrets Management
```bash
pai-audit secret set <name> <value>        # Store encrypted secret
pai-audit secret get <name>                # Retrieve secret
pai-audit secret list                      # List available secrets  
pai-audit secret delete <name>             # Delete secret

# Examples:
pai-audit secret set "api_key" "sk-abc123..."
pai-audit secret get "api_key"
pai-audit secret list
```

### Secure Fabric Calls
```bash
pai-audit fabric <pattern> <model> <data>  # Fabric call with auto-redaction

# Example:
pai-audit fabric "summarize" "gpt-4o" "Account 1216348 case data..."
# Automatically detects high sensitivity and applies redaction
```

### Security Management
```bash
pai-audit status                           # Show security status and metrics
pai-audit cleanup [days]                   # Clean old data (default: 30 days)

# Examples:
pai-audit status
pai-audit cleanup 7                       # Clean data older than 7 days
```

## Automatic Sensitivity Detection

### Sensitivity Scoring
The system automatically scores data sensitivity based on:
- **Case IDs** (8-digit numbers): +20 points
- **Email addresses**: +30 points  
- **IP addresses**: +25 points
- **API keys/tokens**: +40 points
- **Credential keywords**: +35 points

### Automatic Redaction
- **Sensitivity > 50**: Automatic redaction before fabric calls
- **Redaction logging**: All redaction events tracked
- **Model routing**: High-sensitivity data uses secure models

## Audit Log Format
```
[TIMESTAMP] EVENT_TYPE | USER | SESSION_ID | DETAILS
[2025-01-07T12:00:00Z] FABRIC_CALL_START | gvaughn | 1234567890 | pattern=summarize model=gpt-4o sensitivity=75
[2025-01-07T12:00:01Z] DATA_REDACTED | gvaughn | 1234567890 | sensitivity=75 redaction=applied
[2025-01-07T12:00:03Z] FABRIC_CALL_END | gvaughn | 1234567890 | pattern=summarize model=gpt-4o success=true
```

## Security Features

### Encrypted Secrets Storage
- **Location**: `~/.claude/context/secrets/` (700 permissions)
- **Encryption**: GPG symmetric encryption with AES256
- **Access Logging**: All secret access logged

### Data Protection
- **Automatic redaction** for high-sensitivity data
- **Audit trail** for all operations
- **Retention policies** with configurable cleanup
- **Secure fabric integration** with sensitivity awareness

### Directory Security
- **Secrets directory**: 700 permissions (user-only access)
- **Audit logs**: Protected from unauthorized access
- **Temporary data**: Automatic cleanup

## Integration with PAI Tools

### Automatic Integration
All PAI tools automatically use pai-audit for:
- **Operation logging**: Every tool operation logged
- **Security compliance**: Sensitive data handling
- **Audit trails**: Complete activity tracking

### Tool-Specific Logging
- **pai-my-plate-v2**: Daily briefing generation
- **pai-case-processor**: Case analysis and lifecycle events
- **pai-supportshell**: Remote analysis operations
- **pai-email-sync**: Email processing activities
- **pai-calendar**: Meeting preparation activities

## Security Status Monitoring

### Status Dashboard
```bash
pai-audit status
```

Shows:
- **Audit log**: Entry count and health
- **Secrets**: Count of stored secrets
- **Directory permissions**: Security verification
- **High sensitivity events**: Recent redaction activity
- **Model usage**: Recent fabric call patterns

### Example Status Output
```
PAI Security Status:
===================
✅ Audit log: 1,247 entries
🔐 Secrets: 3 stored
✅ Secrets directory: Properly secured (700)
⚠️  High sensitivity events (last 24h): 5

Recent Model Usage:
      8 FABRIC_CALL pattern=tam_daily_plate model=gpt-4o
      3 FABRIC_CALL pattern=redact_tam_data model=gpt-4o
      2 FABRIC_CALL pattern=analyze_case model=remote-local-granite-3-2-8b-instruct
```

## Maintenance and Cleanup

### Automatic Cleanup
- **Old outputs**: Removes files older than retention period
- **Log rotation**: Archives large audit logs (>10MB)
- **Temporary data**: Cleans processing artifacts

### Manual Maintenance
```bash
# Clean data older than 7 days
pai-audit cleanup 7

# View recent activity
pai-audit show-log | tail -20

# Check security status
pai-audit status
```

## Best Practices
1. **Regular monitoring**: Check pai-audit status daily
2. **Secret rotation**: Periodically update stored secrets
3. **Log review**: Monitor audit logs for anomalies
4. **Cleanup scheduling**: Regular cleanup to manage disk space
5. **Sensitivity awareness**: Review high-sensitivity events

## Troubleshooting
- **Permission errors**: Check secrets directory is 700
- **GPG issues**: Ensure GPG is configured for symmetric encryption
- **Log access**: Verify audit log file permissions
- **Integration issues**: Check tool audit logging integration
