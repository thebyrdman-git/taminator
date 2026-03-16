"""
Google Drive and Docs integration for Taminator.

Creates Google Docs from report content and backs up report files to Drive.
Requires OAuth2 credentials (client ID/secret) and a one-time authorization.

Environment variables (optional):
  TAMINATOR_GOOGLE_CLIENT_ID
  TAMINATOR_GOOGLE_CLIENT_SECRET
  TAMINATOR_GOOGLE_TOKEN_PATH  (default: ~/.config/taminator/google_token.json)
"""

import base64
import json
import os
import re
from email.mime.text import MIMEText
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

# Optional imports so the rest of the app works without Google deps installed
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaInMemoryUpload
    _HAS_GOOGLE = True
except ImportError:
    _HAS_GOOGLE = False

try:
    import markdown as _markdown_lib
    _HAS_MARKDOWN = True
except ImportError:
    _HAS_MARKDOWN = False

SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/gmail.compose",
]
_DEFAULT_TOKEN_PATH = Path.home() / ".config" / "taminator" / "google_token.json"


def _client_config() -> Optional[dict]:
    """Build OAuth client config from env or config file."""
    client_id = os.environ.get("TAMINATOR_GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("TAMINATOR_GOOGLE_CLIENT_SECRET")
    if client_id and client_secret:
        return {
            "installed": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost"],
            }
        }
    config_path = Path.home() / ".config" / "taminator" / "google_credentials.json"
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return None


def _token_path() -> Path:
    return Path(os.environ.get("TAMINATOR_GOOGLE_TOKEN_PATH", str(_DEFAULT_TOKEN_PATH)))


def is_configured() -> bool:
    """Return True if Google integration is available and client config exists."""
    if not _HAS_GOOGLE:
        return False
    return _client_config() is not None


def get_credentials() -> Optional["Credentials"]:
    """Load stored credentials; return None if not configured or token missing."""
    if not _HAS_GOOGLE:
        return None
    config = _client_config()
    if not config:
        return None
    token_path = _token_path()
    creds = None
    if token_path.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        except Exception:
            pass
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            token_path.parent.mkdir(parents=True, exist_ok=True)
            with open(token_path, "w") as f:
                f.write(creds.to_json())
        except Exception:
            creds = None
    return creds


def run_oauth_flow() -> Tuple[bool, str]:
    """
    Run interactive OAuth2 flow (open browser). On success, save token and return (True, "").
    On failure return (False, error_message).
    """
    if not _HAS_GOOGLE:
        return False, "Google API libraries not installed (pip install google-api-python-client google-auth-oauthlib)."
    config = _client_config()
    if not config:
        return False, "Google client not configured. Set TAMINATOR_GOOGLE_CLIENT_ID and TAMINATOR_GOOGLE_CLIENT_SECRET, or add ~/.config/taminator/google_credentials.json."
    token_path = _token_path()
    token_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        flow = InstalledAppFlow.from_client_config(config, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_path, "w") as f:
            f.write(creds.to_json())
        return True, ""
    except Exception as e:
        return False, str(e)


def _markdown_to_html(text: str) -> str:
    """Convert markdown to HTML for Google Drive import. Removes markdown syntax but keeps
    formatting: headings (h1/h2/h3), sections, tables, bold, lists. Drive imports text/html
    as a formatted Doc with nice headings and sections."""
    if not _HAS_MARKDOWN or not text.strip():
        return ""
    return _markdown_lib.markdown(
        text,
        extensions=["tables", "nl2br"],
        output_format="html",
    )


def _markdown_to_html_fallback(text: str) -> str:
    """Simple markdown-to-HTML so Gmail drafts are never sent as raw markdown.
    Handles headers, bold, lists, and line breaks. Used when the markdown lib
    is unavailable or returns empty."""
    if not (text or "").strip():
        return ""
    html: List[str] = []
    in_list = False
    for line in text.split("\n"):
        stripped = line.strip()
        # Headers (atx-style)
        if stripped.startswith("### "):
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"<h3>{_escape_html(stripped[4:])}</h3>")
        elif stripped.startswith("## "):
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"<h2>{_escape_html(stripped[3:])}</h2>")
        elif stripped.startswith("# "):
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"<h1>{_escape_html(stripped[2:])}</h1>")
        elif stripped.startswith("- ") or stripped.startswith("* "):
            if not in_list:
                html.append("<ul>")
                in_list = True
            html.append(f"<li>{_inline_md_to_html(stripped[2:])}</li>")
        elif re.match(r"^\d+\.\s", stripped):
            if in_list:
                html.append("</ul>")
                in_list = False
            rest = re.sub(r"^\d+\.\s*", "", stripped)
            html.append(f"<p>{_inline_md_to_html(rest)}</p>")
        elif stripped == "":
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append("<br>")
        else:
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"<p>{_inline_md_to_html(stripped)}</p>")
    if in_list:
        html.append("</ul>")
    return "\n".join(html)


def _escape_html(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _inline_md_to_html(s: str) -> str:
    """Convert inline markdown (bold, italic) to HTML."""
    s = _escape_html(s)
    # **bold** and __bold__
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"__(.+?)__", r"<strong>\1</strong>", s)
    # *italic* and _italic_
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    s = re.sub(r"_(.+?)_", r"<em>\1</em>", s)
    return s


# Inline styles matching Google Docs when pasted into Gmail (font, sizes, margins).
_DOCS_STYLE_BODY = (
    "font-family: Arial, Helvetica, sans-serif; font-size: 11pt; line-height: 1.5; color: #222222;"
)
_DOCS_STYLE_H1 = (
    "font-family: Arial, Helvetica, sans-serif; font-size: 18pt; font-weight: bold; margin: 0.5em 0 0.25em 0; color: #222222;"
)
_DOCS_STYLE_H2 = (
    "font-family: Arial, Helvetica, sans-serif; font-size: 14pt; font-weight: bold; margin: 0.5em 0 0.25em 0; color: #222222;"
)
_DOCS_STYLE_H3 = (
    "font-family: Arial, Helvetica, sans-serif; font-size: 12pt; font-weight: bold; margin: 0.5em 0 0.25em 0; color: #222222;"
)
_DOCS_STYLE_P = (
    "font-family: Arial, Helvetica, sans-serif; font-size: 11pt; margin: 0 0 0.5em 0; line-height: 1.5; color: #222222;"
)
_DOCS_STYLE_UL = "margin: 0.5em 0; padding-left: 1.5em;"
_DOCS_STYLE_OL = "margin: 0.5em 0; padding-left: 1.5em;"
_DOCS_STYLE_LI = (
    "font-family: Arial, Helvetica, sans-serif; font-size: 11pt; margin: 0.25em 0; line-height: 1.5; color: #222222;"
)
_DOCS_STYLE_TABLE = "border-collapse: collapse; margin: 0.5em 0; font-size: 11pt; font-family: Arial, Helvetica, sans-serif;"
_DOCS_STYLE_TD = "border: 1px solid #ccc; padding: 4px 8px; vertical-align: top;"


def _html_to_gmail_docs_style(html: str) -> str:
    """Apply Google Docs–style inline formatting so the draft matches copy-paste from Docs into Gmail."""
    if not html or not html.strip():
        return html
    # Add inline styles to block elements (only if the tag doesn't already have style=).
    def add_style(tag: str, style: str) -> str:
        return f'<{tag} style="{style}"'

    out = html
    # Match <tag> or <tag ...> but not <tag ... style=...>
    no_style = r"(?![^>]*style=)(?=\s|>)"
    out = re.sub(rf"<h1{no_style}", add_style("h1", _DOCS_STYLE_H1), out)
    out = re.sub(rf"<h2{no_style}", add_style("h2", _DOCS_STYLE_H2), out)
    out = re.sub(rf"<h3{no_style}", add_style("h3", _DOCS_STYLE_H3), out)
    out = re.sub(rf"<p{no_style}", add_style("p", _DOCS_STYLE_P), out)
    out = re.sub(rf"<ul{no_style}", add_style("ul", _DOCS_STYLE_UL), out)
    out = re.sub(rf"<ol{no_style}", add_style("ol", _DOCS_STYLE_OL), out)
    out = re.sub(rf"<li{no_style}", add_style("li", _DOCS_STYLE_LI), out)
    out = re.sub(rf"<table{no_style}", add_style("table", _DOCS_STYLE_TABLE), out)
    out = re.sub(rf"<td{no_style}", add_style("td", _DOCS_STYLE_TD), out)
    out = re.sub(rf"<th{no_style}", add_style("th", _DOCS_STYLE_TD), out)
    # Wrap in a div with body style so overall font/size/color apply (Gmail uses this like Docs).
    return f'<div style="{_DOCS_STYLE_BODY}">{out}</div>'


def create_doc_from_text(title: str, text: str) -> dict:
    """
    Create a new Google Doc with the given title and text content.
    Markdown is converted to HTML so the Doc has nice headings and sections without
    raw markdown symbols (#, **, |, etc.). Keeps formatting: headings, tables, bold, lists.
    Returns dict with "url" (webViewLink) and "id" (file id).
    Raises RuntimeError if not configured or API call fails.
    """
    if not _HAS_GOOGLE:
        raise RuntimeError("Google API libraries not installed.")
    creds = get_credentials()
    if not creds:
        raise RuntimeError("Google Drive not connected. Run OAuth flow first (e.g. Connect Google in the UI).")
    service = build("drive", "v3", credentials=creds)
    body = {"name": title, "mimeType": "application/vnd.google-apps.document"}
    # Never send raw markdown to Docs: convert to HTML so headings/tables/bold render (no #, **, | in the doc)
    html = _markdown_to_html(text) if _HAS_MARKDOWN else ""
    if not html:
        html = _markdown_to_html_fallback(text)
    if html:
        media = MediaInMemoryUpload(html.encode("utf-8"), mimetype="text/html", resumable=False)
    else:
        # Last resort: strip markdown to plain text so at least ** and # don't appear
        plain = (text or "").replace("**", "").replace("*", "").replace("#", "").strip()
        media = MediaInMemoryUpload((plain or text or "").encode("utf-8"), mimetype="text/plain", resumable=False)
    file = service.files().create(body=body, media_body=media, fields="id,webViewLink").execute()
    return {"id": file.get("id"), "url": file.get("webViewLink", "")}


def backup_reports_to_drive(files: List[dict]) -> dict:
    """
    Create a folder in Google Drive and upload report (markdown) files into it.
    Each item in files should be {"name": str, "content": str}.
    Returns dict with "folder_id", "url" (folder webViewLink), "count" (files uploaded).
    Raises RuntimeError if not configured or API call fails.
    """
    if not _HAS_GOOGLE:
        raise RuntimeError("Google API libraries not installed.")
    creds = get_credentials()
    if not creds:
        raise RuntimeError("Google Drive not connected. Run OAuth flow first (e.g. tam-rfe google-connect).")
    service = build("drive", "v3", credentials=creds)
    folder_name = f"Taminator Backup {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    folder_body = {"name": folder_name, "mimeType": "application/vnd.google-apps.folder"}
    folder = service.files().create(body=folder_body, fields="id,webViewLink").execute()
    folder_id = folder.get("id")
    url = folder.get("webViewLink", "")
    count = 0
    for item in files:
        name = (item.get("name") or "report.md").strip()
        if not name.endswith(".md"):
            name = name + ".md"
        content = item.get("content") or ""
        body = {"name": name, "parents": [folder_id]}
        media = MediaInMemoryUpload(content.encode("utf-8"), mimetype="text/markdown", resumable=False)
        service.files().create(body=body, media_body=media).execute()
        count += 1
    return {"folder_id": folder_id, "url": url, "count": count}


def create_gmail_draft(subject: str, body_markdown: str) -> dict:
    """
    Create a Gmail draft with the given subject and body. Body is converted from
    markdown to HTML for good formatting in Gmail.
    Returns dict with "url" (link to open the draft in Gmail), "draft_id", "message_id".
    Raises RuntimeError if not configured or API call fails.
    """
    if not _HAS_GOOGLE:
        raise RuntimeError("Google API libraries not installed.")
    creds = get_credentials()
    if not creds:
        raise RuntimeError("Google Drive not connected. Run OAuth flow first (e.g. Connect Google in the UI).")
    # Always send HTML so Gmail shows formatted email, not raw markdown.
    html_body = _markdown_to_html(body_markdown) if body_markdown.strip() else ""
    if not html_body and body_markdown.strip():
        html_body = _markdown_to_html_fallback(body_markdown)
    if not html_body:
        html_body = "<p>No content.</p>"
    # Apply Google Docs–style inline formatting (same look as copy-paste from Docs into Gmail).
    html_body = _html_to_gmail_docs_style(html_body)
    message = MIMEText(html_body, "html")
    message["Subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("ascii").rstrip("=")
    service = build("gmail", "v1", credentials=creds)
    draft_body = {"message": {"raw": raw}}
    draft = service.users().drafts().create(userId="me", body=draft_body).execute()
    message_id = draft.get("message", {}).get("id", "")
    url = f"https://mail.google.com/mail/u/0/#drafts/{message_id}" if message_id else ""
    return {
        "url": url,
        "draft_id": draft.get("id", ""),
        "message_id": message_id,
    }
