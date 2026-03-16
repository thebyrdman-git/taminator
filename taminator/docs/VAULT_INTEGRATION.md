# HashiCorp Vault integration

Taminator can use **HashiCorp Vault** as a secret store for JIRA, Portal, Hydra, and related tokens. When Vault is configured, tokens are read from (and optionally written to) Vault with fallback to the local encoded file and keyring.

## What’s already there

- **`tam-vault`** – CLI: `status`, `migrate`, `list`, `get <service>`, `set <service>`, `delete <service>`, `test`
- **`vault_client.py`** – HTTP client for Vault (KV); uses `VAULT_ADDR`, `VAULT_TOKEN`, optional `VAULT_NAMESPACE`
- **`hybrid_auth.py`** – “Vault first, then Auth Box (file/keyring/env)”; `get_token(service)`, `set_token(service, token)`
- **GUI** – Vault tab in Settings runs `tam-vault` commands via shell

## Implemented integration

1. **Read path** – When `VAULT_ADDR` and `VAULT_TOKEN` are set, `auth_box.get_token()` and `_get_ui_tokens()` try Vault first (via hybrid_auth), then keyring/env/encoded file.
2. **Write path** – Saving a token from Settings (web API or desktop IPC) writes to the local file and, when Vault is configured, syncs to Vault (web_server calls hybrid_auth.set_token(); Electron runs `tam-vault set jira|portal` with token on stdin when `VAULT_ADDR` is set).
3. **No new dependencies** – `vault_client` uses `requests` (already used).

## Configuration

Set before starting the app or `tam-rfe`:

```bash
export VAULT_ADDR="https://vault.example.com"   # required for Vault use
export VAULT_TOKEN="s.xxxx"
# optional:
export VAULT_NAMESPACE="pai/taminator"
export VAULT_CACERT="/path/to/ca-bundle.pem"    # for TLS verification (recommended in production)
export VAULT_SKIP_VERIFY=1                      # only for dev with self-signed certs
```

Vault KV path used: `{VAULT_NAMESPACE}/{service}` (e.g. `pai/taminator/jira`). Each secret is `{ "token": "...", "stored_at": "...", "stored_by": "username" }`.

## Code touch points (implemented)

| Location | Behavior |
|----------|----------|
| `auth_box.get_token()` | Tries hybrid_auth (Vault) first (lazy import), then keyring → env → config file |
| `web_server._get_ui_tokens()` | When Vault available, overlays jira_token and portal_token from hybrid_auth |
| `web_server` save-token API | After token_store.save_ui_tokens(), calls hybrid_auth.set_token() when Vault available |
| Electron `main.js` save-token | After writing file, if `VAULT_ADDR` is set, runs `tam-vault set jira|portal` with token on stdin |

## Security notes

- `VAULT_TOKEN` is a secret; use env or a helper that injects it (e.g. from a signed-in Vault CLI session).
- **TLS:** By default the client verifies SSL. For self-signed or dev Vault, set `VAULT_SKIP_VERIFY=1`. For production, set `VAULT_CACERT` to your CA bundle.
- Tokens are still written to the local encoded file when you save from Settings so the app works offline or when Vault is down.

## Desktop app and Vault

The desktop app (Electron) syncs tokens to Vault only when `VAULT_ADDR` is set in the process environment. On macOS (and some Linux setups), apps started from the Dock or file manager often do not inherit shell environment variables. To use Vault with the desktop app, either:

- Launch the app from a terminal after exporting `VAULT_ADDR` and `VAULT_TOKEN`, or  
- Use a wrapper script or launcher that sets those variables before starting the app.

The in-app Vault tab and the web UI (when run via `tam-rfe serve` from a terminal) will see the same env and can sync to Vault as usual.

## Optional: migrate existing tokens

Run once to copy tokens from the local file into Vault:

```bash
tam-vault migrate
```

This reads from Auth Box (keyring + file) and writes each token to Vault.
