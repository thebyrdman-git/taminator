# supportshell-tool-scan

Scan SupportShell for available tools and versions.

## Location
`~/.local/bin/supportshell-tool-scan`

## Description
Connects to SupportShell via SSH and scans for commonly used support tools, reporting their availability and versions.

## Usage
```bash
supportshell-tool-scan
```

## Requirements
- VPN connection to Red Hat network
- SSH access to SupportShell
- Valid Kerberos ticket or SSH key

## Tools Scanned
- **yank-ng**: Enhanced log extraction tool
- **retrace-server**: Crash analysis tool
- **insights-client**: Red Hat Insights client
- **sosreport**: System diagnostic collection
- **oc**: OpenShift CLI

## Output Format
```
[SupportShell Tool Scan on gvaughn@supportshell-1.sush-001.prod.us-west-2.aws.redhat.com]

Present:
  - yank-ng
  - insights-client
  - sosreport
  - oc

Versions:
yank-ng: 1.2.3
insights-client: 3.1.0
sosreport: 4.5.6
oc: 4.13.0
```

## Environment Variables
- `SSH_CMD`: Override SSH command (default: ssh)
- `HOST`: Override SupportShell host
- `USER_NAME`: Override username (default: gvaughn)

## Error Handling
- Timeout after 5 seconds if no connection
- BatchMode prevents password prompts
- Reports which tools are missing

## Integration
- Used to verify SupportShell capabilities
- Helps plan remote analysis workflows
- Confirms tool versions for compatibility
