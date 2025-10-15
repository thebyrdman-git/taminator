# PAI Systemd Units

Systemd user service and timer files for PAI automation.

## Installation

Copy these files to your systemd user directory:

```bash
cp systemd/*.{service,timer} ~/.config/systemd/user/
systemctl --user daemon-reload
```

## Available Units

### Kerberos Auto-Renewal

**Files:**
- `pai-kerberos-renewal.timer` - Runs every 30 minutes
- `pai-kerberos-renewal.service` - Executes the renewal script

**Enable:**
```bash
systemctl --user enable --now pai-kerberos-renewal.timer
```

**Status:**
```bash
systemctl --user status pai-kerberos-renewal.timer
systemctl --user list-timers pai-kerberos-renewal.timer
```

**Logs:**
```bash
journalctl --user -u pai-kerberos-renewal.service -f
tail -f ~/.local/log/pai-kerberos-renewal.log
```

**Disable:**
```bash
systemctl --user disable --now pai-kerberos-renewal.timer
```

