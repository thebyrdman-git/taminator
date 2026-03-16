"""
JIRA configuration: base URL, auth (Red Hat Bearer vs JIRA Cloud Basic), and browse URL.

Supports:
- Red Hat JIRA (issues.redhat.com): Bearer token (JIRA_TOKEN_API_TOKEN / jira_token).
- JIRA Cloud (*.atlassian.net): Email + API token, HTTP Basic auth (JIRA_EMAIL + JIRA_API_TOKEN / jira_email + jira_api_token).

See docs/JIRA_CLOUD_INTEGRATION.md.
"""

import base64
import os
from pathlib import Path
from typing import Optional, Tuple

DEFAULT_BASE_URL = "https://issues.redhat.com"
DEFAULT_API_PATH = "/rest/api/2"


def _load_tokens() -> dict:
    """Load UI tokens (includes jira_base_url, jira_email, jira_api_token when set)."""
    try:
        from .token_store import load_ui_tokens
        path = Path.home() / ".config" / "taminator" / "ui_tokens.json"
        return load_ui_tokens(path)
    except Exception:
        return {}


def get_jira_base_url() -> str:
    """JIRA base URL (no trailing slash, no /rest/api/2). Default: issues.redhat.com."""
    url = os.environ.get("JIRA_BASE_URL") or _load_tokens().get("jira_base_url") or ""
    url = (url or DEFAULT_BASE_URL).strip().rstrip("/")
    # If user stored URL with /rest/api/2, strip it
    for suffix in ["/rest/api/2", "/rest/api/3"]:
        if url.endswith(suffix):
            url = url[: -len(suffix)].rstrip("/")
            break
    return url or DEFAULT_BASE_URL


def is_jira_cloud(base_url: Optional[str] = None) -> bool:
    """True if base_url is a JIRA Cloud host (*.atlassian.net)."""
    url = (base_url or get_jira_base_url()).lower()
    return "atlassian.net" in url


def get_jira_auth() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Returns (base_url, auth_header_value, content_type).
    auth_header_value is either "Bearer <token>" or "Basic <base64(email:api_token)>".
    content_type is "application/json".
    """
    base_url = get_jira_base_url()
    tokens = _load_tokens()

    # JIRA Cloud: email + API token (Basic auth)
    if is_jira_cloud(base_url):
        email = os.environ.get("JIRA_EMAIL") or (tokens.get("jira_email") or "").strip()
        api_token = os.environ.get("JIRA_API_TOKEN") or (tokens.get("jira_api_token") or "").strip()
        if email and api_token:
            credentials = f"{email}:{api_token}"
            encoded = base64.b64encode(credentials.encode("utf-8")).decode("ascii")
            return base_url, f"Basic {encoded}", "application/json"
        # Fallback: single token as Bearer (some Cloud setups)
        token = os.environ.get("JIRA_TOKEN_API_TOKEN") or tokens.get("jira_token") or ""
        if token:
            return base_url, f"Bearer {(token or '').strip()}", "application/json"
        return base_url, None, "application/json"

    # Red Hat JIRA: Bearer token
    token = os.environ.get("JIRA_TOKEN_API_TOKEN") or tokens.get("jira_token") or ""
    token = (token or "").strip()
    if token:
        return base_url, f"Bearer {token}", "application/json"
    return base_url, None, "application/json"


def get_jira_api_url() -> str:
    """Full JIRA REST API base (base_url + /rest/api/2)."""
    base = get_jira_base_url()
    path = os.environ.get("JIRA_API_PATH", DEFAULT_API_PATH).strip().rstrip("/")
    if not path.startswith("/"):
        path = "/" + path
    return f"{base.rstrip('/')}{path}"


def get_jira_browse_url(issue_id: str) -> str:
    """URL to open issue in browser (e.g. https://issues.redhat.com/browse/AAPRFE-123)."""
    base = get_jira_base_url()
    return f"{base.rstrip('/')}/browse/{issue_id}"
