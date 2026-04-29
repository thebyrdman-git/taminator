#!/usr/bin/env python3
"""
HTTP server for browser UIs that drive the tam-rfe CLI (check/update, etc.).

**Taminator** (``tam-rfe serve``) is TAM-focused. **RFE and Bug Tracker** uses the same
server module but is a separate product aimed at **anyone who needs the content** (e.g.
account teams through executives); its static files should live under
``rfe-and-bug-tracker/web`` (see RFEBUGTRACKER_WEB_ROOT), not conflated with Taminator’s
own ``web/`` bundle when both exist in a workspace.

**Managed UI:** Set ``RFE_UI_MANAGED=1`` when JIRA/Portal APIs are provisioned server-side.
The browser then hides token settings and shows Red Hat SSO-oriented chrome (no OIDC
implementation here; wire SSO at the edge when ready).
"""

import csv
import io
import json
import os
import re
import subprocess
import sys
import threading
import traceback
from datetime import datetime, timedelta
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:
    import requests
except ImportError:
    requests = None

# Directory containing this script (taminator/taminator)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Dev checkout: package lives under …/taminator/taminator/src — not Resources/taminator/src (packaged).
SCRIPT_DIR_CHILD_SRC = os.path.join(SCRIPT_DIR, "src")


def _resolve_web_dir() -> str:
    """Directory of static files (index.html) for whichever browser tool is being run.

    Prefer **RFE and Bug Tracker** assets when present; otherwise fall back to **Taminator**’s
    bundled ``web/`` next to this module.

    Order:
    1) RFEBUGTRACKER_WEB_ROOT or RFE_BUG_TRACKER_WEB_DIR
    2) <workspace-root>/rfe-and-bug-tracker/web (or …/rfe-and-bug-tracker with index.html)
    3) SCRIPT_DIR/web (Taminator app directory)

    Workspace root = parent of the ``taminator`` repo (…/taminator/taminator -> …/redhat).
    """
    for env_key in ("RFEBUGTRACKER_WEB_ROOT", "RFE_BUG_TRACKER_WEB_DIR"):
        raw = os.environ.get(env_key, "").strip()
        if raw:
            p = os.path.abspath(os.path.expanduser(raw))
            if os.path.isfile(os.path.join(p, "index.html")):
                return p
    workspace_root = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
    rfe_web = os.path.join(workspace_root, "rfe-and-bug-tracker", "web")
    if os.path.isfile(os.path.join(rfe_web, "index.html")):
        return rfe_web
    rfe_root = os.path.join(workspace_root, "rfe-and-bug-tracker")
    if os.path.isfile(os.path.join(rfe_root, "index.html")):
        return rfe_root
    return os.path.join(SCRIPT_DIR, "web")


WEB_DIR = _resolve_web_dir()
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
ROADMAP_HTML_FILE = os.path.join(REPO_ROOT, "ROADMAP.html")
ROADMAP_MD_FILE = os.path.join(REPO_ROOT, "ROADMAP.md")
# RFE and Bug Tracker UI (not the Taminator desktop app repo). Override with GITLAB_ROADMAP_URL.
RFE_BUG_TRACKER_GITLAB_PROJECT = "https://gitlab.cee.redhat.com/jbyrd/rfe-bug-tracker"
GITLAB_ROADMAP_URL = os.environ.get("GITLAB_ROADMAP_URL", RFE_BUG_TRACKER_GITLAB_PROJECT).strip()
TAM_RFE = os.path.join(SCRIPT_DIR, "tam-rfe")
# Stale index.html (older bundles) may still reference jbyrd/taminator; rewrite when serving.
_GITLAB_LEGACY_RFE_UI_PREFIX = b"https://gitlab.cee.redhat.com/jbyrd/taminator"
_GITLAB_LEGACY_AUTOMATION_PREFIX = b"https://gitlab.cee.redhat.com/jbyrd/rfe-and-bug-tracker-automation"


def _env_truthy(name: str) -> bool:
    v = os.environ.get(name, "").strip().lower()
    return v in ("1", "true", "yes", "on")


def _ui_status_payload() -> dict:
    """Hints for the browser UI: managed deploy (APIs on server; hide token settings; SSO-style chrome)."""
    managed = _env_truthy("RFE_UI_MANAGED")
    return {
        "managed_deployment": managed,
        "show_token_settings": not managed,
        "auth_presentation": "red_hat_sso" if managed else "local",
    }


def _taminator_src_path():
    """Path to the directory that contains the 'taminator' package (for sys.path).
    Prefer PYTHONPATH (set by Electron when packaged), then SCRIPT_DIR layouts."""
    # Packaged app: Python sources live at Resources/src (sibling of Resources/taminator where this file sits).
    # Do not use SCRIPT_DIR/src alone — that resolves to Resources/taminator/src and omits integrations/.
    for p in os.environ.get("PYTHONPATH", "").split(os.pathsep):
        p = p.strip()
        if p and os.path.isdir(p) and os.path.isdir(os.path.join(p, "taminator")):
            return p
    candidates = [
        SCRIPT_DIR_CHILD_SRC,
        os.path.normpath(os.path.join(SCRIPT_DIR, "..", "src")),
        os.path.join(SCRIPT_DIR, "app.asar.unpacked", "src"),
    ]
    resources = os.environ.get("TAMINATOR_RESOURCES", "").strip()
    if resources and resources != SCRIPT_DIR:
        candidates.extend([
            os.path.join(resources, "src"),
            os.path.normpath(os.path.join(resources, "..", "src")),
            os.path.join(resources, "app.asar.unpacked", "src"),
        ])
    for p in candidates:
        if os.path.isdir(p) and os.path.isdir(os.path.join(p, "taminator")):
            return p
    return candidates[0]  # fallback so insert/remove stay consistent


def _ensure_taminator_on_path():
    """Ensure the taminator package is on sys.path (e.g. when running from packaged app)."""
    if "taminator" in sys.modules:
        return
    src_path = _taminator_src_path()
    if os.path.isdir(src_path) and os.path.isdir(os.path.join(src_path, "taminator")):
        if src_path not in sys.path:
            sys.path.insert(0, src_path)


# Support Case column when JIRA is tracked but there is no access.redhat.com case
# (e.g. external SNOW, ROSA FedRAMP) — not discoverable via Hydra/Portal the usual way.
NOT_IN_PORTAL_SUPPORT_CASE_LABEL = "Not in Customer Portal"


def _parse_jira_keys_from_paste(pasted: str) -> list:
    """Extract JIRA issue keys from free text: browse URLs, plain PROJ-123, etc. Order preserved, deduped."""
    if not (pasted or "").strip():
        return []
    text = (pasted or "").strip()
    out = []
    _ensure_taminator_on_path()
    from taminator.core.hydra_search import JIRA_ID_PATTERN

    for m in JIRA_ID_PATTERN.finditer(text):
        out.append(m.group(1).upper())
    # JIRA/Atlassian browse and selected path forms (picks up keys for projects not in the static prefix list)
    for m in re.finditer(r"/browse/([A-Za-z][A-Za-z0-9_]*-\d+)", text):
        out.append(m.group(1).upper())
    return list(dict.fromkeys(out))


def _classify_jira_paste_row_kind(issue_type: str, summary: str) -> str:
    """RFE vs Bug for pasted JIRA rows, using JIRA issuetype and summary as fallback."""
    it = (issue_type or "").lower()
    if re.search(r"(^|[^a-z])bug([^a-z]|$)", it) and "debug" not in it and "debt" not in it:
        return "Bug"
    if any(
        x in it
        for x in (
            "feature",
            "improvement",
            "story",
            "enhancement",
            "epic",
            "initiative",
            "new feature",
        )
    ) or it in ("task",) or "task" in it.split():
        return "RFE"
    from taminator.commands.update import _classify_rfe_or_bug

    k = _classify_rfe_or_bug(summary or "")
    if k in ("RFE", "Bug"):
        return k
    return "RFE"


# Same search paths as CustomerReportParser in check.py
REPORT_SEARCH_PATHS = [
    Path.home() / "taminator-test-data",
    Path.home() / "Documents" / "rh" / "customers",
    Path("/tmp/taminator-test-data"),
]

# User-configured accounts and report structure, stored in taminator config
CONFIG_DIR = Path.home() / ".config" / "taminator"
ACCOUNTS_FILE = CONFIG_DIR / "accounts.json"
REPORT_STRUCTURE_FILE = CONFIG_DIR / "report_structure.json"

DEFAULT_REPORT_STRUCTURE = {
    "report_title_suffix": "RFE/Bug Tracker",
    "section_customer_info": "Customer Information",
    "section_rfe": "Enhancement Requests (RFE)",
    "section_bug": "Bug Reports",
    "section_notes": "Notes",
    "default_tam_name": "",
    "default_contact": "",
    "section_order": ["customer_info", "rfe", "bug", "notes"],
    "section_included": {"customer_info": True, "rfe": True, "bug": True, "notes": True},
}


def _slug(s: str) -> str:
    """Return a slug suitable for report filename: lowercase, alphanumeric and underscores."""
    if not s or not s.strip():
        return ""
    return "".join(c if c.isalnum() or c == "_" else "_" for c in s.strip().lower()).strip("_") or "account"


def _normalize_sbr_groups(val) -> list:
    """Return a list of non-empty trimmed strings from sbr_groups (list or comma-separated string)."""
    if val is None:
        return []
    if isinstance(val, list):
        return [str(x).strip() for x in val if str(x).strip()]
    return [x.strip() for x in str(val).split(",") if x.strip()]


def _sbr_groups_set(account_or_groups) -> frozenset:
    """Normalized SBR group set for comparison. Pass an account dict or a list of group names."""
    if hasattr(account_or_groups, "get"):
        groups = account_or_groups.get("sbr_groups") or []
    else:
        groups = account_or_groups if account_or_groups is not None else []
    return frozenset(_normalize_sbr_groups(groups))


def _normalize_account_numbers(val) -> list:
    """Return a list of non-empty trimmed strings from account_numbers (list or comma-separated string)."""
    if val is None:
        return []
    if isinstance(val, list):
        return [str(x).strip() for x in val if str(x).strip()]
    return [x.strip() for x in str(val).split(",") if x.strip()]


def _dedupe_accounts(accounts: list) -> list:
    """Merge two accounts only when they share an account number and the same SBR group."""
    if not accounts:
        return []
    result = [dict(a) for a in accounts]
    while True:
        changed = False
        for i in range(len(result)):
            if changed:
                break
            nums_i = set(result[i].get("account_numbers") or [])
            sbr_i = _sbr_groups_set(result[i])
            for j in range(i + 1, len(result)):
                nums_j = set(result[j].get("account_numbers") or [])
                if nums_i & nums_j and _sbr_groups_set(result[j]) == sbr_i:
                    merged_nums = _normalize_account_numbers(list(nums_i | nums_j)) or list(nums_i | nums_j)
                    result[i]["account_numbers"] = merged_nums
                    result[i]["account_number"] = merged_nums[0] if merged_nums else result[i].get("account_number")
                    name_i = (result[i].get("customer_name") or "").strip()
                    name_j = (result[j].get("customer_name") or "").strip()
                    if name_j and not name_i:
                        result[i]["customer_name"] = name_j
                    if result[j].get("sbr_groups") and not result[i].get("sbr_groups"):
                        result[i]["sbr_groups"] = result[j]["sbr_groups"]
                    result.pop(j)
                    changed = True
                    break
        if not changed:
            break
    return result


def _load_accounts() -> list:
    """Load accounts from ~/.config/taminator/accounts.json. Returns list of dicts with id, account_number, account_numbers, customer_name, sbr_groups. Duplicates (same account number + same SBR group) are merged."""
    if not ACCOUNTS_FILE.exists():
        return []
    try:
        with open(ACCOUNTS_FILE) as f:
            data = json.load(f)
        out = []
        for a in data.get("accounts", []):
            a = dict(a)
            nums = _normalize_account_numbers(a.get("account_numbers") or a.get("account_number"))
            if not nums and a.get("account_number"):
                nums = [str(a.get("account_number")).strip()]
            a["account_numbers"] = nums
            a["account_number"] = nums[0] if nums else ""
            out.append(a)
        deduped = _dedupe_accounts(out)
        if len(deduped) < len(out):
            _save_accounts(deduped)
            return deduped
        return deduped
    except Exception:
        return []


def _account_numbers_from_loaded_account(a: dict) -> list:
    nums = a.get("account_numbers") or []
    if isinstance(nums, list):
        return [str(x).strip() for x in nums if str(x).strip()]
    s = str(nums or a.get("account_number") or "").strip()
    if not s:
        return []
    return [x.strip() for x in s.split(",") if x.strip()]


def _collect_account_numbers_for_portal_search(accounts: list, account_ids: list) -> list:
    """Union of Red Hat account numbers for selected customer ids; empty account_ids means all configured customers."""
    if not accounts:
        return []
    want = {(x or "").strip() for x in (account_ids or []) if (x or "").strip()}
    nums_out = []
    if not want:
        for a in accounts:
            nums_out.extend(_account_numbers_from_loaded_account(a))
    else:
        for a in accounts:
            if (a.get("id") or "").strip() in want:
                nums_out.extend(_account_numbers_from_loaded_account(a))
    seen = set()
    out = []
    for n in nums_out:
        if n and n not in seen:
            seen.add(n)
            out.append(n)
    return out


def _accounts_in_portal_search_scope(accounts: list, account_ids: list) -> list:
    """Account dicts included in a Portal search: all configured if account_ids empty, else matching ids."""
    if not accounts:
        return []
    want = {(x or "").strip() for x in (account_ids or []) if (x or "").strip()}
    if not want:
        return list(accounts)
    return [a for a in accounts if (a.get("id") or "").strip() in want]


def _sbr_products_for_portal_search(accounts: list, account_ids: list) -> list:
    """Union of SBR strings from accounts in scope (order preserved, case-insensitive dedupe)."""
    scoped = _accounts_in_portal_search_scope(accounts, account_ids)
    seen: set = set()
    out: list = []
    for a in scoped:
        for g in _normalize_sbr_groups(a.get("sbr_groups")):
            key = g.lower()
            if key not in seen:
                seen.add(key)
                out.append(g)
    return out


def _every_account_in_scope_has_sbr(accounts: list, account_ids: list) -> bool:
    """True when every account row in scope has at least one SBR group (required for full Portal scoping)."""
    scoped = _accounts_in_portal_search_scope(accounts, account_ids)
    if not scoped:
        return False
    for a in scoped:
        if not _normalize_sbr_groups(a.get("sbr_groups")):
            return False
    return True


def _find_account_by_account_numbers(accounts: list, account_numbers: list, sbr_groups=None) -> tuple:
    """Return (index, account) of the first account with overlapping account numbers and the same SBR group, or (None, None).
    Duplicates are only merged when they share the same SBR group. sbr_groups: list or [] for no SBR."""
    want = set(_normalize_account_numbers(account_numbers) or [])
    if not want:
        return (None, None)
    want_sbr = _sbr_groups_set(sbr_groups if sbr_groups is not None else [])
    for i, a in enumerate(accounts):
        have = set(a.get("account_numbers") or [])
        if (have & want) and _sbr_groups_set(a) == want_sbr:
            return (i, a)
    return (None, None)


def _ensure_account_from_dump(account_numbers: list, customer_name: str) -> dict:
    """Ensure an account exists: add if none match these account numbers and SBR, else update (merge numbers, customer_name).
    Only merges into an account that has the same SBR group; from dump we use no SBR ([]), so we only merge into accounts with no SBR."""
    account_numbers = _normalize_account_numbers(account_numbers) or []
    if not account_numbers:
        return {}
    accounts = _load_accounts()
    idx, existing = _find_account_by_account_numbers(accounts, account_numbers, sbr_groups=[])
    if idx is not None:
        # Merge: add any new account numbers, update customer_name if provided
        merged_nums = list(dict.fromkeys((existing.get("account_numbers") or []) + account_numbers))
        merged_nums = _normalize_account_numbers(merged_nums) or merged_nums
        name = (customer_name or "").strip() or (existing.get("customer_name") or "").strip()
        accounts[idx] = {
            **existing,
            "account_numbers": merged_nums,
            "account_number": merged_nums[0] if merged_nums else existing.get("account_number"),
            "customer_name": name or existing.get("customer_name"),
        }
        _save_accounts(accounts)
        return accounts[idx]
    # Add new account
    aid = _slug(customer_name) or _slug("Account-" + str(account_numbers[0]))
    if not aid:
        aid = "account_" + str(account_numbers[0])
    existing_ids = {(a.get("id") or "").strip().lower() for a in accounts}
    base_id = aid
    idx = 0
    while aid.lower() in existing_ids:
        idx += 1
        aid = f"{base_id}_{idx}"
    name = customer_name.strip() or f"Account {account_numbers[0]}"
    entry = {"id": aid, "account_numbers": account_numbers, "account_number": account_numbers[0], "customer_name": name, "created_at": datetime.utcnow().isoformat() + "Z"}
    accounts.append(entry)
    _save_accounts(accounts)
    return entry


def _save_accounts(accounts: list) -> None:
    """Save accounts to ~/.config/taminator/accounts.json. Each entry must have account_numbers (list); we also write account_number (first) for backward compat."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    out = []
    for a in accounts:
        a = dict(a)
        nums = _normalize_account_numbers(a.get("account_numbers") or a.get("account_number"))
        if not nums and a.get("account_number"):
            nums = [str(a.get("account_number")).strip()]
        a["account_numbers"] = nums
        a["account_number"] = nums[0] if nums else ""
        out.append(a)
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump({"accounts": out}, f, indent=2)
    try:
        os.chmod(ACCOUNTS_FILE, 0o600)
    except OSError:
        pass


def _load_report_structure() -> dict:
    """Load report structure preferences from ~/.config/taminator/report_structure.json. Returns dict with section titles, defaults, section_order, section_included."""
    out = dict(DEFAULT_REPORT_STRUCTURE)
    if not REPORT_STRUCTURE_FILE.exists():
        return out
    try:
        with open(REPORT_STRUCTURE_FILE) as f:
            data = json.load(f)
        for k in list(out):
            if k == "section_order":
                if isinstance(data.get(k), list) and len(data[k]) > 0:
                    out[k] = [str(x) for x in data[k] if str(x) in ("customer_info", "rfe", "bug", "notes")]
                    if not out[k]:
                        out[k] = list(DEFAULT_REPORT_STRUCTURE["section_order"])
                continue
            if k == "section_included":
                if isinstance(data.get(k), dict):
                    out[k] = {sid: bool(data[k].get(sid, True)) for sid in ("customer_info", "rfe", "bug", "notes")}
                continue
            if k in data and data[k] is not None:
                out[k] = str(data[k]).strip() or out[k]
        return out
    except Exception:
        return out


def _save_report_structure(data: dict) -> None:
    """Save report structure to ~/.config/taminator/report_structure.json. Writes allowed keys including section_order and section_included."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    out = {}
    for k in DEFAULT_REPORT_STRUCTURE:
        if k == "section_order":
            if isinstance(data.get(k), list) and len(data[k]) > 0:
                out[k] = [str(x) for x in data[k] if str(x) in ("customer_info", "rfe", "bug", "notes")]
            if k not in out or not out[k]:
                out[k] = list(DEFAULT_REPORT_STRUCTURE["section_order"])
            continue
        if k == "section_included":
            if isinstance(data.get(k), dict):
                out[k] = {sid: bool(data[k].get(sid, True)) for sid in ("customer_info", "rfe", "bug", "notes")}
            else:
                out[k] = dict(DEFAULT_REPORT_STRUCTURE["section_included"])
            continue
        if k in data and data[k] is not None:
            val = data[k]
            out[k] = str(val).strip() if str(val).strip() else DEFAULT_REPORT_STRUCTURE[k]
        else:
            out[k] = DEFAULT_REPORT_STRUCTURE[k]
    with open(REPORT_STRUCTURE_FILE, "w") as f:
        json.dump(out, f, indent=2)
    try:
        os.chmod(REPORT_STRUCTURE_FILE, 0o600)
    except OSError:
        pass


def _build_report_from_structure(
    struct: dict,
    customer_slug: str,
    display_name: str,
    account: str,
    contact: str,
    tam: str,
) -> str:
    """Build report markdown from a structure dict."""
    suffix = (struct.get("report_title_suffix") or DEFAULT_REPORT_STRUCTURE["report_title_suffix"]).strip() or "RFE/Bug Tracker"
    sec_info = (struct.get("section_customer_info") or DEFAULT_REPORT_STRUCTURE["section_customer_info"]).strip() or "Customer Information"
    sec_rfe = (struct.get("section_rfe") or DEFAULT_REPORT_STRUCTURE["section_rfe"]).strip() or "Enhancement Requests (RFE)"
    sec_bug = (struct.get("section_bug") or DEFAULT_REPORT_STRUCTURE["section_bug"]).strip() or "Bug Reports"
    sec_notes = (struct.get("section_notes") or DEFAULT_REPORT_STRUCTURE["section_notes"]).strip() or "Notes"
    default_tam = (struct.get("default_tam_name") or "").strip() or (tam or "TAM")
    default_contact = (struct.get("default_contact") or "").strip() or (contact or "TBD")
    tam_val = (tam or "").strip() or default_tam
    contact_val = (contact or "").strip() or default_contact
    account_val = (account or "").strip() or "TBD"
    timestamp = datetime.now().strftime("%b %d, %Y, %I:%M %p %Z")
    title = f"{display_name or customer_slug} {suffix}"
    order = struct.get("section_order") or DEFAULT_REPORT_STRUCTURE["section_order"]
    included = struct.get("section_included") or DEFAULT_REPORT_STRUCTURE["section_included"]
    if not isinstance(included, dict):
        included = dict(DEFAULT_REPORT_STRUCTURE["section_included"])

    blocks = ["# " + title, "", timestamp + " " + tam_val, "", "Summary: 0 total cases (0 RFE, 0 Bug)"]
    customer_info_lines = [f"- **Account:** {account_val}", f"- **Primary Contact:** {contact_val}", f"- **TAM:** {tam_val}"]
    section_blocks = {
        "customer_info": "## " + sec_info + "\n\n" + "\n".join(customer_info_lines),
        "rfe": f"""## {sec_rfe}

| RED HAT JIRA ID | Support Case | Description | Status/Notes |
|-----------------|--------------|-------------|--------------|
| | | | |

*No RFEs tracked yet. Use Check report / Update report to add RFEs.*""",
        "bug": f"""## {sec_bug}

| RED HAT JIRA ID | Support Case | Description | Status/Notes |
|-----------------|--------------|-------------|--------------|
| | | | |

*No bugs tracked yet. Use Check report / Update report to add bugs.*""",
        "notes": f"""---

**{sec_notes}:**
- This tracker is automatically updated via RFE and Bug Tracker
- Last check: {timestamp}
- For questions, contact {tam_val} ({default_contact})""",
    }
    for sid in order:
        if included.get(sid, True) and sid in section_blocks:
            blocks.append("")
            blocks.append(section_blocks[sid])
    return "\n".join(blocks).strip() + "\n"


def _build_report_template(
    customer_slug: str, display_name: str, account: str, contact: str, tam: str
) -> str:
    """Build report markdown using saved report_structure."""
    return _build_report_from_structure(
        _load_report_structure(), customer_slug, display_name, account, contact, tam
    )


def list_reports():
    """Scan known paths for report files (.md, .html, .txt); return list of { customer, path, name, mtime }."""
    seen = set()
    out = []
    for base in REPORT_SEARCH_PATHS:
        if not base.exists():
            continue
        for ext in ("*.md", "*.html", "*.txt", "*.csv"):
            for f in base.glob(ext):
                key = (f.stem.lower(), str(f))
                if key in seen:
                    continue
                seen.add(key)
                try:
                    mtime = int(f.stat().st_mtime)
                except OSError:
                    mtime = 0
                out.append({"customer": f.stem, "path": str(f.resolve()), "name": f.name, "mtime": mtime})
    out.sort(key=lambda x: (x["customer"].lower(), -x["mtime"]))
    return out


def list_reports_with_accounts():
    """Return merged list: report files on disk + configured accounts that have no file yet. Each item has customer, path, name, mtime, and no_file (true when account is configured but has no report file)."""
    file_by_customer = {}
    for r in list_reports():
        key = (r["customer"] or "").strip().lower()
        if key:
            file_by_customer[key] = r
    out = list(file_by_customer.values())
    for a in _load_accounts():
        aid = (a.get("id") or "").strip()
        if not aid:
            continue
        key = aid.lower()
        if key in file_by_customer:
            continue
        name = (a.get("customer_name") or aid).strip()
        out.append({"customer": aid, "path": None, "name": None, "mtime": None, "no_file": True, "display_name": name})
    out.sort(key=lambda x: ((x.get("customer") or "").lower(), -(x.get("mtime") or 0)))
    return out


def delete_report(path_str: str) -> tuple:
    """Delete a report file. path_str must be under REPORT_SEARCH_PATHS. Returns (True, None) or (False, error_message)."""
    path_str = (path_str or "").strip()
    if not path_str:
        return False, "path is required"
    try:
        report_path = Path(path_str).expanduser().resolve()
    except Exception as e:
        return False, str(e)
    if not report_path.is_file():
        return False, "Not a file or does not exist"
    allowed_bases = [p.expanduser().resolve() for p in REPORT_SEARCH_PATHS]
    if not any(report_path.parent == base or base in report_path.parents for base in allowed_bases):
        return False, "Report must be in an allowed search path"
    try:
        report_path.unlink()
        return True, None
    except OSError as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)


def _find_report_path(customer: str):
    """Find a report file for customer (stem) in REPORT_SEARCH_PATHS. Prefer .md, then .html, then .txt. Return Path or None."""
    stem = (customer or "").strip().lower()
    if not stem:
        return None
    for base in REPORT_SEARCH_PATHS:
        base = Path(base).expanduser().resolve()
        if not base.exists():
            continue
        for ext in (".md", ".html", ".txt", ".csv"):
            p = base / (stem + ext)
            if p.is_file():
                return p
    return None


def get_report_content(customer: str, path: str = None) -> tuple:
    """Return (content, error_message). If path is given and under REPORT_SEARCH_PATHS, read that file; else find by customer stem."""
    if path:
        try:
            p = Path(path).expanduser().resolve()
            allowed = {str(d.resolve()) for d in REPORT_SEARCH_PATHS}
            if any(str(p).startswith(d.rstrip("/") + "/") or str(p) == d.rstrip("/") for d in allowed):
                if p.is_file():
                    return p.read_text(encoding="utf-8", errors="replace"), None
                return None, "File not found"
            # path not under allowed dirs
        except Exception as e:
            return None, str(e)
    report_path = _find_report_path(customer)
    if not report_path or not report_path.exists():
        return None, "Report not found"
    try:
        return report_path.read_text(encoding="utf-8", errors="replace"), None
    except Exception as e:
        return None, str(e)


def _escape_html(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _markdown_inline_to_html(s: str) -> str:
    s = _escape_html(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    return s


def _markdown_to_html_simple(md: str) -> str:
    """Minimal markdown to HTML for roadmap display."""
    if not md:
        return ""
    html = []
    in_code = False
    for line in md.splitlines():
        if line.strip().startswith("```"):
            if in_code:
                html.append("</pre>")
            else:
                html.append("<pre>")
            in_code = not in_code
            continue
        if in_code:
            html.append(_escape_html(line) + "\n")
            continue
        m = re.match(r"^(#{1,3})\s+(.+)$", line)
        if m:
            level = len(m.group(1))
            html.append(f"<h{level}>{_markdown_inline_to_html(m.group(2))}</h{level}>")
            continue
        if not line.strip():
            html.append("<br>")
            continue
        html.append("<p>" + _markdown_inline_to_html(line) + "</p>")
    if in_code:
        html.append("</pre>")
    return "\n".join(html)


def get_roadmap() -> dict:
    """Return { html, markdown, gitlab_roadmap_url } or { error, ... }. Uses ROADMAP.html (HTML only); falls back to ROADMAP.md converted to HTML if present."""
    out = {"html": "", "markdown": "", "gitlab_roadmap_url": GITLAB_ROADMAP_URL}
    try:
        if os.path.isfile(ROADMAP_HTML_FILE):
            with open(ROADMAP_HTML_FILE, encoding="utf-8", errors="replace") as f:
                out["html"] = f.read()
        elif os.path.isfile(ROADMAP_MD_FILE):
            with open(ROADMAP_MD_FILE, encoding="utf-8", errors="replace") as f:
                md = f.read()
            out["markdown"] = md
            out["html"] = _markdown_to_html_simple(md)
        else:
            out["error"] = "Roadmap not found (ROADMAP.html or ROADMAP.md)"
    except Exception as e:
        out["error"] = str(e)
    return out


def check_vpn() -> dict:
    """Check if Red Hat VPN appears to be up (can reach issues.redhat.com). Returns { ok: bool, message: str }."""
    src_path = _taminator_src_path()
    try:
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
        from taminator.core import jira_config
        base_url = jira_config.get_jira_base_url()
        if jira_config.is_jira_cloud(base_url):
            return {"ok": True, "message": "JIRA Cloud configured; VPN check skipped (not required for Cloud)."}
    except Exception:
        pass
    finally:
        if src_path in sys.path:
            sys.path.remove(src_path)
    # Use stdlib urllib only: requests + charset_normalizer on large HTML can recurse
    # deeply on Apple Python 3.9 and abort the worker thread.
    try:
        req = Request(
            "https://issues.redhat.com",
            headers={"User-Agent": "RFE-Bug-Tracker-VPN-check/1.0"},
            method="GET",
        )
        with urlopen(req, timeout=8) as resp:
            resp.read(8192)
        return {"ok": True, "message": "VPN connectivity OK (issues.redhat.com reachable)"}
    except HTTPError:
        return {"ok": True, "message": "VPN connectivity OK (issues.redhat.com reachable)"}
    except URLError as e:
        return {"ok": False, "message": str(e) or "Cannot reach issues.redhat.com. Connect to Red Hat VPN."}
    except TimeoutError:
        return {"ok": False, "message": "Timeout reaching issues.redhat.com. Connect to Red Hat VPN and try again."}
    except OSError as e:
        return {"ok": False, "message": str(e) or "Cannot reach issues.redhat.com. Connect to Red Hat VPN."}


def _get_ui_tokens():
    """Return dict of token key -> value from ~/.config/taminator/ui_tokens.json, or {}.
    When Vault is configured (VAULT_ADDR/VAULT_TOKEN), overlays jira/portal tokens from Vault.
    Supports encoded storage (base64 payload) and legacy plain JSON."""
    tokens_file = Path.home() / ".config" / "taminator" / "ui_tokens.json"
    src_path = _taminator_src_path()
    inserted = src_path not in sys.path
    if inserted:
        sys.path.insert(0, src_path)
    try:
        try:
            from taminator.core.token_store import load_ui_tokens
            tokens = load_ui_tokens(tokens_file)
        except ImportError:
            tokens = {}
            if tokens_file.exists():
                try:
                    with open(tokens_file) as f:
                        tokens = json.load(f)
                except Exception:
                    pass
        # Overlay from Vault when configured
        try:
            from taminator.core.hybrid_auth import hybrid_auth
            if hybrid_auth.is_vault_available():
                for vault_service, key in [("jira", "jira_token"), ("portal", "portal_token")]:
                    t = hybrid_auth.get_token(vault_service, required=False)
                    # Do not overwrite tokens already loaded from ui_tokens.json (Settings save wins).
                    if t and not (tokens.get(key) or "").strip():
                        tokens[key] = t
        except Exception:
            pass
        return tokens
    finally:
        if inserted and src_path in sys.path:
            sys.path.remove(src_path)


def _env_with_ui_tokens():
    """Return os.environ augmented with tokens from ~/.config/taminator/ui_tokens.json if present.
    Hydra: REDHAT_USERNAME/PASSWORD from env or from UI-saved credentials.
    JIRA: JIRA_TOKEN_API_TOKEN for Red Hat; for JIRA Cloud also JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN.
    """
    env = dict(os.environ)
    tokens = _get_ui_tokens()
    if tokens.get("jira_token"):
        env["JIRA_TOKEN_API_TOKEN"] = tokens["jira_token"]
    if tokens.get("jira_base_url") and not env.get("JIRA_BASE_URL"):
        env["JIRA_BASE_URL"] = tokens["jira_base_url"]
    if tokens.get("jira_email") and not env.get("JIRA_EMAIL"):
        env["JIRA_EMAIL"] = tokens["jira_email"]
    if tokens.get("jira_api_token") and not env.get("JIRA_API_TOKEN"):
        env["JIRA_API_TOKEN"] = tokens["jira_api_token"]
    if tokens.get("portal_token"):
        env["PORTAL_TOKEN"] = tokens["portal_token"]
    if not env.get("REDHAT_USERNAME") and tokens.get("redhat_username"):
        env["REDHAT_USERNAME"] = tokens["redhat_username"]
    if not env.get("REDHAT_PASSWORD") and tokens.get("redhat_password"):
        env["REDHAT_PASSWORD"] = tokens["redhat_password"]
    return env


def _markdown_to_html_fallback(text: str) -> str:
    """Convert common markdown to HTML without the markdown package. Used when markdown lib is not installed."""
    import html as html_module
    import re
    if not (text or "").strip():
        return ""
    lines = (text or "").split("\n")
    out = []
    i = 0
    in_fence = False
    fence_char = None
    list_tag = None

    def inline_convert(s: str) -> str:
        s = html_module.escape(s)
        s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        # Linear-time bare URL linkify; lookbehind + re.sub on long strings can recurse deeply on py3.9.
        _url = re.compile(r"https?://[^\s<>\"')\]]{1,4000}")
        parts = []
        pos = 0
        for m in _url.finditer(s):
            parts.append(s[pos : m.start()])
            u = m.group(0)
            parts.append(f'<a href="{u}" target="_blank" rel="noopener">{u}</a>')
            pos = m.end()
        parts.append(s[pos:])
        s = "".join(parts)
        return s

    while i < len(lines):
        line = lines[i]
        if re.match(r"^```", line):
            if in_fence:
                out.append("</code></pre>")
                in_fence = False
            else:
                in_fence = True
                out.append("<pre><code>")
            i += 1
            continue
        if in_fence:
            out.append(html_module.escape(line) + "\n")
            i += 1
            continue
        if re.match(r"^###\s+", line):
            t = re.sub(r"^###\s+", "", line).strip()
            out.append("<h3>" + inline_convert(t) + "</h3>")
            i += 1
            continue
        if re.match(r"^##\s+", line):
            t = re.sub(r"^##\s+", "", line).strip()
            out.append("<h2>" + inline_convert(t) + "</h2>")
            i += 1
            continue
        if re.match(r"^#\s+", line):
            t = re.sub(r"^#\s+", "", line).strip()
            out.append("<h1>" + inline_convert(t) + "</h1>")
            i += 1
            continue
        if re.match(r"^---+$", line) or re.match(r"^\*+$", line) or re.match(r"^_+$", line):
            out.append("<hr/>")
            i += 1
            continue
        if re.match(r"^-\s+", line) or re.match(r"^\*\s+", line) or re.match(r"^\d+\.\s+", line):
            if list_tag != "ul":
                if list_tag:
                    out.append("</" + list_tag + ">")
                out.append("<ul>")
                list_tag = "ul"
            rest = re.sub(r"^[-*]\s+|\d+\.\s+", "", line).strip()
            out.append("<li>" + inline_convert(rest) + "</li>")
            i += 1
            continue
        if list_tag:
            out.append("</" + list_tag + ">")
            list_tag = None
        line_stripped = line.strip()
        if not line_stripped:
            out.append("<p></p>")
            i += 1
            continue
        if "|" in line_stripped and line_stripped.count("|") >= 2:
            table_rows = []
            j = i
            while j < len(lines):
                row_line = lines[j].strip()
                if not row_line or "|" not in row_line or row_line.count("|") < 2:
                    break
                cells = [c.strip() for c in row_line.split("|")]
                if cells and cells[0] == "":
                    cells = cells[1:]
                if cells and cells[-1] == "":
                    cells = cells[:-1]
                if not cells:
                    break
                is_sep = all(re.match(r"^[\s\-:]+$", (c or "")) for c in cells)
                if is_sep:
                    j += 1
                    continue
                table_rows.append(cells)
                j += 1
            if table_rows:
                out.append("<table border=\"1\" cellpadding=\"4\" cellspacing=\"0\" style=\"border-collapse:collapse; width:100%\">")
                for row_idx, row_cells in enumerate(table_rows):
                    tag = "th" if row_idx == 0 else "td"
                    out.append("<tr>")
                    for c in row_cells:
                        out.append("<" + tag + ">" + inline_convert(c or "") + "</" + tag + ">")
                    out.append("</tr>")
                out.append("</table>")
                i = j
                i += 1
                continue
        out.append("<p>" + inline_convert(line_stripped) + "</p>")
        i += 1
    if list_tag:
        out.append("</" + list_tag + ">")
    if in_fence:
        out.append("</code></pre>")
    return "\n".join(out)


def _markdown_to_plain_text(text: str) -> str:
    """Convert markdown to plain text (strip formatting for .txt reports). Tables become tab-separated rows."""
    import re
    if not (text or "").strip():
        return ""
    lines = (text or "").split("\n")

    def strip_inline(s: str) -> str:
        s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
        s = re.sub(r"\*([^*]+)\*", r"\1", s)
        s = re.sub(r"`([^`]+)`", r"\1", s)
        s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
        return s.strip()

    out = []
    i = 0
    in_fence = False
    while i < len(lines):
        line = lines[i]
        if re.match(r"^```", line):
            in_fence = not in_fence
            i += 1
            continue
        if in_fence:
            out.append(line)
            i += 1
            continue
        # Markdown table: rows with | and multiple cells
        if "|" in line and line.strip().count("|") >= 2:
            table_rows = []
            j = i
            while j < len(lines):
                row_line = lines[j].strip()
                if not row_line or "|" not in row_line or row_line.count("|") < 2:
                    break
                cells = [strip_inline(c.strip()) for c in row_line.split("|")]
                if cells and cells[0] == "":
                    cells = cells[1:]
                if cells and cells[-1] == "":
                    cells = cells[:-1]
                if not cells:
                    break
                is_sep = all(re.match(r"^[\s\-:]+$", (c or "")) for c in cells)
                if is_sep:
                    j += 1
                    continue
                table_rows.append(cells)
                j += 1
            if table_rows:
                for row in table_rows:
                    out.append("\t".join(row))
                i = j
                i += 1
                continue
        # Headings: strip leading #
        if re.match(r"^#+\s+", line):
            line = re.sub(r"^#+\s+", "", line).strip()
        # Horizontal rules -> blank line
        if re.match(r"^[-*_]+$", line):
            out.append("")
            i += 1
            continue
        # List items
        line = re.sub(r"^\s*[-*]\s+|\s*\d+\.\s+", "- ", line, count=1)
        line = strip_inline(line)
        out.append(line)
        i += 1
    return "\n".join(out).strip() + "\n"


def _markdown_tables_to_csv(markdown_text: str) -> str:
    """Extract RFE and Bug tables from report markdown and return CSV with Section column (for Google Sheets etc.)."""
    if not (markdown_text or "").strip():
        return "Section,RED HAT JIRA ID,Support Case,Description,Status/Notes\n"
    lines = (markdown_text or "").split("\n")
    section_headers = ("Section", "RED HAT JIRA ID", "Support Case", "Description", "Status/Notes")
    rows_out = []
    current_section = None
    table_header = None
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if re.match(r"^##\s+", stripped):
            lower = stripped.lower()
            if "rfe" in lower or "enhancement" in lower:
                current_section = "RFE"
            elif "bug" in lower:
                current_section = "Bug"
            else:
                current_section = None
            i += 1
            continue
        if "|" not in stripped or stripped.count("|") < 2:
            i += 1
            continue
        cells = [c.strip() for c in stripped.split("|")]
        if cells and cells[0] == "":
            cells = cells[1:]
        if cells and cells[-1] == "":
            cells = cells[:-1]
        if not cells:
            i += 1
            continue
        is_sep = all(re.match(r"^[\s\-:]+$", (c or "")) for c in cells)
        if is_sep:
            i += 1
            continue
        if table_header is None and current_section == "RFE":
            table_header = cells
            i += 1
            continue
        if table_header is not None and cells == table_header:
            i += 1
            continue
        if current_section and table_header is not None:
            row = [current_section] + cells
            rows_out.append(row)
        i += 1
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(section_headers)
    for row in rows_out:
        w.writerow(row)
    return buf.getvalue()


def _load_docs_sections():
    """Load README and GETTING-STARTED into sections for the in-app User Guide. Returns list of { id, title, content } (content is HTML)."""
    import re
    # Resolve script dir with realpath so symlinks (e.g. in .app bundle) don't break lookup
    _script_file = os.path.realpath(os.path.abspath(__file__))
    script_dir = Path(os.path.dirname(_script_file))
    repo_root = script_dir.parent
    cwd = Path(os.getcwd()).resolve()
    # Packaged app: TAMINATOR_RESOURCES set by Electron or by tam-rfe before importing this module
    resources_env = os.environ.get("TAMINATOR_RESOURCES", "").strip()
    search_bases = [script_dir, repo_root, cwd]
    if resources_env:
        search_bases.insert(0, Path(resources_env).resolve())
    for base in search_bases:
        user_guide = base / "USER-GUIDE.md"
        if user_guide.is_file():
            files = [user_guide]
            break
    else:
        files = [repo_root / "README.md", repo_root / "GETTING-STARTED.md"]
        if not any(p.is_file() for p in files):
            files = [script_dir / "README.md", script_dir / "GETTING-STARTED.md"]
    seen = set()
    raw_parts = []
    for f in files:
        try:
            p = f.resolve()
            if p in seen or not p.is_file():
                continue
            seen.add(p)
            raw_parts.append(p.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            continue
    if not raw_parts:
        return [{"id": "overview", "title": "User Guide", "content": "<p>Documentation not found. See <a href=\"https://gitlab.cee.redhat.com/jbyrd/rfe-bug-tracker\" target=\"_blank\" rel=\"noopener\">GitLab Repository</a>.</p>"}]
    full = "\n\n---\n\n".join(raw_parts)
    blocks = re.split(r"\n##\s+", full, maxsplit=0)
    intro = (blocks[0].strip() if blocks else "")
    sections = []
    if intro:
        sections.append({"id": "overview", "title": "Overview", "content": intro})
    for block in blocks[1:]:
        first_line = block.split("\n", 1)[0].strip()
        rest = block.split("\n", 1)[1].strip() if "\n" in block else ""
        sid = re.sub(r"[^a-z0-9]+", "-", first_line.lower()).strip("-")[:48] or "section"
        sections.append({"id": sid, "title": first_line, "content": rest})

    # Do not use the third-party `markdown` package here: on some macOS/Python 3.9
    # stacks it recurses thousands of frames for normal docs and trips the interpreter
    # limit (SIGABRT) or the thread stack (SIGBUS). The local fallback is iterative.
    # Do not run a second HTML pass with heavy regex (linkify): inline_convert already
    # linkifies bare URLs per line.
    for s in sections:
        raw_md = s.get("content") or ""
        s["content"] = _markdown_to_html_fallback(raw_md)
    return sections


def get_token_status():
    """Return { jira, portal, hydra } booleans (configured or not).
    Hydra is configured via Portal token or REDHAT_USERNAME + REDHAT_PASSWORD (or REDHAT_PORTAL_*).
    """
    ui_tokens = _get_ui_tokens()
    env = os.environ

    def _has(ui_key, env_key):
        return bool(ui_tokens.get(ui_key) or env.get(env_key))

    username = env.get("REDHAT_USERNAME") or env.get("REDHAT_PORTAL_USERNAME") or ui_tokens.get("redhat_username")
    password = env.get("REDHAT_PASSWORD") or env.get("REDHAT_PORTAL_PASSWORD") or ui_tokens.get("redhat_password")
    hydra_ok = bool(username and password) or _has("portal_token", "PORTAL_TOKEN")

    result = {
        "jira": _has("jira_token", "JIRA_TOKEN_API_TOKEN"),
        "portal": _has("portal_token", "PORTAL_TOKEN"),
        "hydra": hydra_ok,
        "hydra_credentials_set": bool(ui_tokens.get("redhat_username") and ui_tokens.get("redhat_password")),
    }
    try:
        sys.path.insert(0, _taminator_src_path())
        from taminator.core.auth_box import auth_box
        from taminator.core.auth_types import AuthType
        if auth_box.get_token(AuthType.JIRA_TOKEN, required=False):
            result["jira"] = True
        if auth_box.get_token(AuthType.PORTAL_TOKEN, required=False):
            result["portal"] = True
            result["hydra"] = True
    except Exception:
        pass
    finally:
        if _taminator_src_path() in sys.path:
            sys.path.remove(_taminator_src_path())
    return result


def _get_effective_hydra_token():
    """Return Bearer token for Hydra (test + search).

    Hydra case search (rhcase) uses an SSO access token from password grant
    (client_id hydra-client-cli), not necessarily the Customer Portal *management* API
    token. Try SSO first, then Portal API token from Settings/env, then auth_box.
    """
    token = None
    try:
        sys.path.insert(0, _taminator_src_path())
        from taminator.core.hydra_search import get_bearer_token_from_env, get_bearer_token
        ui_tokens = _get_ui_tokens()
        if ui_tokens.get("redhat_username") and ui_tokens.get("redhat_password"):
            try:
                token = get_bearer_token(ui_tokens["redhat_username"], ui_tokens["redhat_password"])
            except Exception:
                pass
        if not token:
            token = get_bearer_token_from_env()
    except Exception:
        pass
    finally:
        if _taminator_src_path() in sys.path:
            sys.path.remove(_taminator_src_path())
    if token:
        return token
    tokens = _get_ui_tokens()
    pt_ui = (tokens.get("portal_token") or "").strip()
    if pt_ui:
        return pt_ui
    pt_env = (os.environ.get("PORTAL_TOKEN") or "").strip()
    if pt_env:
        return pt_env
    try:
        sys.path.insert(0, _taminator_src_path())
        from taminator.core.auth_box import auth_box
        from taminator.core.auth_types import AuthType
        token = auth_box.get_token(AuthType.PORTAL_TOKEN, required=False)
        return token
    except Exception:
        return None
    finally:
        if _taminator_src_path() in sys.path:
            sys.path.remove(_taminator_src_path())


def _get_hydra_basic_auth():
    """Return (username, password) for Hydra Basic auth from UI tokens or env, or None.

    Same as update.py: prefer Basic when Red Hat username/password are available.
    """
    ui_tokens = _get_ui_tokens()
    username = ui_tokens.get("redhat_username") or os.environ.get("REDHAT_USERNAME") or os.environ.get("REDHAT_PORTAL_USERNAME")
    password = ui_tokens.get("redhat_password") or os.environ.get("REDHAT_PASSWORD") or os.environ.get("REDHAT_PORTAL_PASSWORD")
    if username and password:
        return (username.strip(), password)
    return None


def _get_hydra_basic_auth_credentials():
    """Red Hat username/password for Hydra Basic auth (UI or env), ignoring Portal token presence.

    Used when Bearer was tried first but Hydra returned 401 — some accounts need Basic for Hydra.
    """
    ui_tokens = _get_ui_tokens()
    username = ui_tokens.get("redhat_username") or os.environ.get("REDHAT_USERNAME") or os.environ.get("REDHAT_PORTAL_USERNAME")
    password = ui_tokens.get("redhat_password") or os.environ.get("REDHAT_PASSWORD") or os.environ.get("REDHAT_PORTAL_PASSWORD")
    if username and password:
        return (username.strip(), password)
    return None


def test_hydra_access():
    """Test Hydra API using Basic auth (username/password) or Bearer token. Returns { ok: bool, message: str }."""
    if not requests:
        return {"ok": False, "message": "requests library not available"}
    url = "https://access.redhat.com/hydra/rest/search/cases"
    params = {"q": "*:*", "rows": 0, "start": 0}
    headers_json = {"Content-Type": "application/json"}
    bearer = _get_effective_hydra_token()
    basic_auth = _get_hydra_basic_auth()
    try:
        if basic_auth:
            r = requests.get(url, headers=headers_json, params=params, auth=basic_auth, timeout=15)
            # Wrong password or Hydra rejects Basic: try SSO/Portal Bearer (rhcase-style token).
            if r.status_code == 401 and bearer:
                r = requests.get(
                    url,
                    headers={**headers_json, "Authorization": f"Bearer {bearer}"},
                    params=params,
                    timeout=15,
                )
                if r.status_code == 200:
                    return {
                        "ok": True,
                        "message": "Hydra reachable with SSO/Portal Bearer (HTTP Basic was rejected). Check username/password or rely on Portal token / SSO.",
                    }
        elif bearer:
            r = requests.get(
                url,
                headers={**headers_json, "Authorization": f"Bearer {bearer}"},
                params=params,
                timeout=15,
            )
            if r.status_code == 401:
                creds = _get_hydra_basic_auth_credentials()
                if creds:
                    r = requests.get(url, headers=headers_json, params=params, auth=creds, timeout=15)
                    if r.status_code == 200:
                        return {
                            "ok": True,
                            "message": "Hydra reachable with Red Hat username/password. Bearer token was rejected (401); Hydra often needs SSO or Basic, not only the management API token.",
                        }
        else:
            return {
                "ok": False,
                "message": "Set Red Hat username/password in Settings, or a Customer Portal API token, or REDHAT_USERNAME and REDHAT_PASSWORD in your environment.",
            }
        if r.status_code == 200:
            return {"ok": True, "message": "Hydra API reachable (Basic auth or Bearer token)."}
        if r.status_code == 401:
            return {
                "ok": False,
                "message": "Hydra returned 401 Unauthorized. Add Red Hat username/password (SSO) in Settings, or use an SSO token: Hydra case search follows rhcase (password grant), not only the management API token.",
            }
        return {"ok": False, "message": f"Hydra API returned {r.status_code}. Check credentials or VPN."}
    except requests.exceptions.Timeout:
        return {"ok": False, "message": "Timeout reaching Hydra. Connect to Red Hat VPN and try again."}
    except requests.exceptions.RequestException as e:
        return {"ok": False, "message": str(e) or "Network error reaching Hydra."}


def run_cmd(args, cwd=None, extra_env=None):
    """Run tam-rfe subcommand; return (stdout, stderr, returncode). extra_env: optional dict merged into env (e.g. for TAMINATOR_DEBUG_*)."""
    cwd = cwd or SCRIPT_DIR
    cmd = [sys.executable, TAM_RFE] + args
    env = _env_with_ui_tokens()
    if extra_env:
        env = {**env, **extra_env}
    try:
        r = subprocess.run(
            cmd,
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            timeout=120,
        )
        return (r.stdout or "", r.stderr or "", r.returncode)
    except subprocess.TimeoutExpired:
        return ("", "Command timed out after 120 seconds", -1)
    except Exception as e:
        return ("", str(e), -1)


class TaminatorHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Quiet logs unless needed
        pass

    def _cors_headers(self):
        """Allow browser/API clients when origin differs (localhost vs 127.0.0.1, file://, Electron)."""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors_headers()
        self.end_headers()

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self._cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _get_app_version(self):
        # Prefer version set by Electron (installed app); then VERSION file(s)
        version = (os.environ.get("TAMINATOR_APP_VERSION") or "").strip()
        if version:
            return version
        version = "dev"
        for base in [SCRIPT_DIR, os.environ.get("TAMINATOR_RESOURCES", "")]:
            if not base:
                continue
            version_file = os.path.join(base, "VERSION")
            if os.path.isfile(version_file):
                try:
                    with open(version_file, "r", encoding="utf-8") as f:
                        version = (f.read() or "").strip() or version
                except Exception:
                    pass
                break
        return version

    def send_html(self, path):
        if path == "" or path == "/":
            path = "index.html"
        if ".." in path or path.startswith("/"):
            path = path.lstrip("/")
        filepath = os.path.join(WEB_DIR, path)
        if not os.path.isfile(filepath):
            self.send_error(404)
            return
        self.send_response(200)
        if path.endswith(".js"):
            self.send_header("Content-Type", "application/javascript")
        elif path.endswith(".css"):
            self.send_header("Content-Type", "text/css")
        elif path.endswith(".png"):
            self.send_header("Content-Type", "image/png")
        elif path.endswith(".ico"):
            self.send_header("Content-Type", "image/x-icon")
        elif path.endswith(".svg"):
            self.send_header("Content-Type", "image/svg+xml")
        else:
            self.send_header("Content-Type", "text/html")
            if path.endswith(".html") or path == "index.html":
                self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
                self.send_header("Pragma", "no-cache")
        self.end_headers()
        with open(filepath, "rb") as f:
            body = f.read()
        if path == "index.html":
            try:
                version = self._get_app_version()
                body = body.replace(b"Version \xe2\x80\xa6", ("Version " + version).encode("utf-8"))
            except Exception:
                pass
            if _GITLAB_LEGACY_RFE_UI_PREFIX in body:
                body = body.replace(
                    _GITLAB_LEGACY_RFE_UI_PREFIX,
                    RFE_BUG_TRACKER_GITLAB_PROJECT.encode("utf-8"),
                )
            if _GITLAB_LEGACY_AUTOMATION_PREFIX in body:
                body = body.replace(
                    _GITLAB_LEGACY_AUTOMATION_PREFIX,
                    RFE_BUG_TRACKER_GITLAB_PROJECT.encode("utf-8"),
                )
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.strip("/")
        qs = parse_qs(parsed.query)
        if path.startswith("api/"):
            if path == "api/status":
                self.send_json({
                    "status": "ok",
                    "service": "rfe_bug_tracker",
                    "display_name": "RFE and Bug Tracker",
                    "ui": _ui_status_payload(),
                })
            elif path == "api/version":
                self.send_json({"version": self._get_app_version()})
            elif path == "api/status/indicators":
                try:
                    vpn = check_vpn()
                except Exception:
                    vpn = {"ok": False}
                try:
                    tokens = get_token_status()
                except Exception:
                    tokens = {"jira": False, "portal": False, "hydra": False, "hydra_credentials_set": False}
                # Google check with short timeout so indicators load quickly
                google_result = [False]  # mutable for thread
                def _check_google():
                    try:
                        sys.path.insert(0, _taminator_src_path())
                        from taminator.integrations.google_drive import get_credentials
                        google_result[0] = bool(get_credentials())
                    except Exception:
                        pass
                    finally:
                        if _taminator_src_path() in sys.path:
                            sys.path.remove(_taminator_src_path())
                t = threading.Thread(target=_check_google, daemon=True)
                t.start()
                t.join(timeout=1.5)
                tokens["google"] = google_result[0]
                self.send_json({"vpn": {"ok": vpn.get("ok", False)}, "tokens": tokens})
            elif path == "api/library":
                # Library lists only report files that have been created (no "no file yet" placeholders)
                reports = list_reports()
                accounts_by_id = {
                    (a.get("id") or "").strip().lower(): (a.get("customer_name") or a.get("id") or "").strip()
                    for a in _load_accounts()
                }
                for r in reports:
                    r["display_name"] = accounts_by_id.get((r.get("customer") or "").lower()) or r.get("customer") or ""
                self.send_json({"reports": reports})
            elif path == "api/report":
                customer = (qs.get("customer") or [""])[0].strip()
                if not customer:
                    self.send_json({"error": "customer required"}, 400)
                    return
                content, err = get_report_content(customer)
                if err:
                    self.send_json({"ok": False, "error": err}, 404)
                    return
                self.send_json({"customer": customer, "content": content})
            elif path == "api/google/status":
                try:
                    sys.path.insert(0, _taminator_src_path())
                    from taminator.integrations.google_drive import is_configured, get_credentials
                    configured = is_configured()
                    connected = bool(get_credentials()) if configured else False
                    self.send_json({"configured": configured, "connected": connected})
                except Exception:
                    self.send_json({"configured": False, "connected": False})
                finally:
                    if _taminator_src_path() in sys.path:
                        sys.path.remove(_taminator_src_path())
            elif path == "api/vpn/check":
                self.send_json(check_vpn())
            elif path == "api/test/hydra":
                self.send_json(test_hydra_access())
            elif path == "api/accounts":
                try:
                    accounts = _load_accounts()
                    self.send_json({"accounts": accounts})
                except Exception as e:
                    self.send_json({"ok": False, "error": str(e)}, 500)
            elif path == "api/portal/search":
                q = (qs.get("q") or [""])[0].strip()
                ids_raw = (qs.get("accounts") or [""])[0].strip()
                account_ids = [x.strip() for x in ids_raw.split(",") if x.strip()]
                try:
                    accounts = _load_accounts()
                except Exception as e:
                    self.send_json({"ok": False, "error": str(e), "cases": [], "numFound": 0}, 500)
                    return
                nums = _collect_account_numbers_for_portal_search(accounts, account_ids)
                # No configured account numbers: only allow Portal "discovery" when the user typed keywords
                # (search by case summary / account name / case number across visible cases, time-bounded).
                discovery = False
                if not nums:
                    if not q:
                        self.send_json(
                            {
                                "ok": False,
                                "error": "No account numbers in scope. Add accounts under Accounts & setup, or type keywords to search the Customer Portal for matching cases and account names.",
                                "cases": [],
                                "numFound": 0,
                            },
                            400,
                        )
                        return
                    discovery = True
                srcp = _taminator_src_path()
                try:
                    sys.path.insert(0, srcp)
                    from taminator.core import hydra_search

                    # Same credential resolution as api/test/hydra: Basic if password set; else SSO/Portal Bearer.
                    basic_auth = _get_hydra_basic_auth()
                    bearer_token = _get_effective_hydra_token()
                    token = None if basic_auth else bearer_token
                    if not basic_auth and not token:
                        self.send_json(
                            {
                                "ok": False,
                                "error": "Customer Portal token or Red Hat credentials required to search the Customer Portal.",
                                "cases": [],
                                "numFound": 0,
                            },
                            400,
                        )
                        return
                    modified_after = None
                    products_for_query = None
                    if discovery:
                        # Bound unscoped keyword search (configured accounts not required).
                        modified_after = (datetime.utcnow() - timedelta(days=365)).strftime("%Y-%m-%d")
                    elif _every_account_in_scope_has_sbr(accounts, account_ids):
                        # Account number(s) + SBR on every selected row: no date cap (old RFEs); filter by product.
                        products_for_query = _sbr_products_for_portal_search(accounts, account_ids) or None
                    elif not q:
                        # Account scope without full SBR setup: keep a time bound when listing all cases (no keywords).
                        modified_after = (datetime.utcnow() - timedelta(days=90)).strftime("%Y-%m-%d")
                    solr_q = hydra_search.build_solr_query_portal_search(
                        q,
                        nums if not discovery else [],
                        include_closed=False,
                        modified_after=modified_after,
                        products=products_for_query,
                    )
                    try:
                        rows_req = int((qs.get("rows") or ["50"])[0])
                    except ValueError:
                        rows_req = 50
                    rows_req = max(1, min(rows_req, 150))
                    result = hydra_search.search_cases(
                        token=token,
                        query=solr_q,
                        start=0,
                        rows=rows_req,
                        basic_auth=basic_auth,
                        timeout=45,
                        basic_auth_fallback=_get_hydra_basic_auth_credentials() if not basic_auth else None,
                        bearer_fallback=bearer_token if basic_auth else None,
                    )
                    docs = result.get("response", {}).get("docs", [])
                    num_found = result.get("response", {}).get("numFound", len(docs))
                    cases_out = [hydra_search.doc_to_portal_search_row(d) for d in docs]
                    out = {"ok": True, "cases": cases_out, "numFound": num_found}
                    if discovery:
                        out["discovery"] = True
                    self.send_json(out)
                except Exception as e:
                    self.send_json({"ok": False, "error": str(e), "cases": [], "numFound": 0}, 500)
                finally:
                    if srcp in sys.path:
                        sys.path.remove(srcp)
            elif path == "api/report-structure":
                self.send_json(_load_report_structure())
            elif path == "api/reports/paths":
                # Resolved paths so the build API accepts report_dir when sent back
                paths = [str(p.expanduser().resolve()) for p in REPORT_SEARCH_PATHS]
                self.send_json({"paths": paths})
            elif path == "api/config/status":
                stdout, stderr, code = run_cmd(["config"])
                self.send_json({"ok": code == 0, "stdout": stdout, "stderr": stderr})
            elif path == "api/config/jira-settings":
                try:
                    tokens = _get_ui_tokens()
                    base = (tokens.get("jira_base_url") or "").strip()
                    self.send_json({
                        "jira_base_url": base or "https://issues.redhat.com",
                        "jira_email": (tokens.get("jira_email") or "").strip(),
                        "jira_api_token_set": bool((tokens.get("jira_api_token") or "").strip()),
                        "jira_token_set": bool((tokens.get("jira_token") or "").strip()),
                        "is_jira_cloud": "atlassian.net" in (base or ""),
                    })
                except Exception as e:
                    self.send_json({"ok": False, "error": str(e)}, 500)
            elif path.rstrip("/") == "api/google/set-credentials":
                self.send_json({"ok": False, "error": "Use POST to save credentials (click Save credentials in the UI)."}, 405)
            elif path.rstrip("/") == "api/config/set-hydra-credentials":
                self.send_json({"ok": False, "error": "Use POST to save Hydra credentials (click Save credentials in the UI)."}, 405)
            elif path == "api/docs":
                try:
                    sections = _load_docs_sections()
                    self.send_json({"sections": sections})
                except Exception as e:
                    self.send_json({"ok": False, "error": str(e), "sections": []}, 500)
            elif path == "api/docs/roadmap":
                self.send_json(get_roadmap())
            elif path == "api/vault/status":
                try:
                    sys.path.insert(0, _taminator_src_path())
                    from taminator.core.vault_client import vault_client
                    from taminator.core.hybrid_auth import hybrid_auth
                    vstatus = vault_client.get_status()
                    hstatus = hybrid_auth.get_status()
                    if _taminator_src_path() in sys.path:
                        sys.path.remove(_taminator_src_path())
                    self.send_json({
                        "available": vstatus.get("available", False),
                        "addr": vstatus.get("addr") or os.environ.get("VAULT_ADDR") or "Not configured",
                        "version": vstatus.get("version", "N/A") if vstatus.get("available") else "N/A",
                        "initialized": vstatus.get("initialized", False) if vstatus.get("available") else None,
                        "sealed": vstatus.get("sealed", True) if vstatus.get("available") else None,
                        "strategy": hstatus.get("strategy", "auth-box-only"),
                        "error": vstatus.get("error") if not vstatus.get("available") else None,
                    })
                except Exception as e:
                    if _taminator_src_path() in sys.path:
                        sys.path.remove(_taminator_src_path())
                    self.send_json({"available": False, "addr": os.environ.get("VAULT_ADDR") or "Not configured", "strategy": "auth-box-only", "error": str(e)}, 200)
            elif path == "api/vault/list":
                try:
                    sys.path.insert(0, _taminator_src_path())
                    from taminator.core.vault_client import vault_client
                    tokens = vault_client.list_tokens()
                    if _taminator_src_path() in sys.path:
                        sys.path.remove(_taminator_src_path())
                    self.send_json({"ok": True, "tokens": [k.replace("/", "") for k in (tokens or [])]})
                except Exception as e:
                    if _taminator_src_path() in sys.path:
                        sys.path.remove(_taminator_src_path())
                    self.send_json({"ok": False, "error": str(e), "tokens": []}, 500)
            elif path == "api/vault/get":
                service = (qs.get("service") or [""])[0].strip()
                if not service:
                    self.send_json({"ok": False, "error": "service required"}, 400)
                    return
                try:
                    sys.path.insert(0, _taminator_src_path())
                    from taminator.core.hybrid_auth import hybrid_auth
                    token = hybrid_auth.get_token(service, required=False)
                    if _taminator_src_path() in sys.path:
                        sys.path.remove(_taminator_src_path())
                    self.send_json({"ok": True, "value": token or ""})
                except Exception as e:
                    if _taminator_src_path() in sys.path:
                        sys.path.remove(_taminator_src_path())
                    self.send_json({"ok": False, "error": str(e), "value": ""}, 500)
            else:
                self.send_json({"ok": False, "error": "Not found"}, 404)
            return
        self.send_html(path or "index.html")

    def _do_post_reports_build(self, data: dict):
        """Handle POST api/reports/build: create a new report file from template."""
        customer_slug = (_slug((data.get("customer_slug") or data.get("customer_id") or data.get("id") or "").strip()) or "").strip()
        display_name = (data.get("display_name") or "").strip() or customer_slug.replace("_", " ").title()
        account = (data.get("account") or data.get("account_number") or "").strip()
        account_numbers = _normalize_account_numbers(data.get("account_numbers") or account)
        if account_numbers:
            account = ", ".join(account_numbers)
        contact = (data.get("contact") or data.get("primary_contact") or "").strip()
        tam = (data.get("tam") or data.get("tam_name") or "").strip()
        sbr_groups = _normalize_sbr_groups(data.get("sbr_groups"))
        report_dir = (data.get("report_dir") or "").strip()
        if not customer_slug:
            self.send_json({"ok": False, "error": "customer_slug or id is required"}, 400)
            return
        allowed_resolved = {str(p.resolve()) for p in REPORT_SEARCH_PATHS}
        if report_dir:
            dir_path = Path(report_dir).expanduser().resolve()
            if str(dir_path) not in allowed_resolved:
                self.send_json({"ok": False, "error": "report_dir must be one of the allowed paths"}, 400)
                return
        else:
            dir_path = REPORT_SEARCH_PATHS[0].resolve()
        dir_path.mkdir(parents=True, exist_ok=True)
        fmt = (data.get("format") or "markdown").strip().lower()
        if fmt not in ("markdown", "html", "text", "csv"):
            fmt = "markdown"
        ext = {"markdown": ".md", "html": ".html", "text": ".txt", "csv": ".csv"}[fmt]
        report_path = dir_path / f"{customer_slug}{ext}"
        if report_path.exists() and not data.get("overwrite"):
            self.send_json({"ok": False, "error": f"Report already exists: {report_path}. Set overwrite: true to replace."}, 400)
            return
        try:
            content = _build_report_template(customer_slug, display_name, account, contact, tam)
            if fmt == "html":
                content = _markdown_to_html_fallback(content)
            elif fmt == "text":
                content = _markdown_to_plain_text(content)
            elif fmt == "csv":
                content = _markdown_tables_to_csv(content)
            report_path.write_text(content, encoding="utf-8")

            # Always add this account to configured accounts when creating a report so it appears on Check/Update and Library
            account_added = False
            try:
                accounts = _load_accounts()
                existing_ids = {(a.get("id") or "").strip().lower() for a in accounts}
                if customer_slug and customer_slug.lower() not in existing_ids:
                    nums = account_numbers or []
                    entry = {"id": customer_slug, "account_numbers": nums, "account_number": (nums[0] if nums else ""), "customer_name": display_name, "created_at": datetime.utcnow().isoformat() + "Z"}
                    if sbr_groups:
                        entry["sbr_groups"] = sbr_groups
                    accounts.append(entry)
                    _save_accounts(accounts)
                    account_added = True
            except Exception as save_err:
                # Don't fail the whole request if accounts save fails; report file was already created
                self.send_json({"ok": True, "path": str(report_path), "customer": customer_slug, "message": f"Report created: {report_path}. Account could not be added to config: {save_err}", "account_added": False})
                return

            # Populate the new report from JIRA and Customer Portal (same as "Update report")
            update_stdout, update_stderr, update_code = run_cmd(["update", customer_slug, "-y"])
            populated = update_code == 0
            msg = f"Report created: {report_path}"
            if populated:
                msg += ". Fetched data from JIRA and Customer Portal."
            else:
                msg += ". Template only; run Update in Generate Reports to pull data (check VPN and tokens)."
            if account_added:
                msg += " Account added to Check/Update Reports."
            self.send_json({
                "ok": True,
                "path": str(report_path),
                "customer": customer_slug,
                "message": msg,
                "populated": populated,
                "account_added": account_added,
                "update_stdout": update_stdout,
                "update_stderr": update_stderr,
            })
        except Exception as e:
            self.send_json({"ok": False, "error": str(e)}, 500)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = (parsed.path or "").strip().strip("/").rstrip("/")
        try:
            content_length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            content_length = 0
        body = self.rfile.read(content_length).decode("utf-8", errors="replace") if content_length else "{}"
        try:
            data = json.loads(body) if body.strip() else {}
        except json.JSONDecodeError:
            data = {}
        if path == "api/google/create-doc":
            # Create Google Doc from report content; return URL.
            customer = (data.get("customer") or "").strip()
            title = (data.get("title") or "").strip() or (customer and f"RFE Report - {customer}")
            content = data.get("content")
            if not content and customer:
                content, err = get_report_content(customer)
                if err:
                    self.send_json({"ok": False, "error": err}, 400)
                    return
            if not content:
                self.send_json({"ok": False, "error": "Provide customer (to load report) or content and title."}, 400)
                return
            try:
                sys.path.insert(0, _taminator_src_path())
                from taminator.integrations.google_drive import create_doc_from_text, get_credentials
                if not get_credentials():
                    self.send_json({"ok": False, "error": "Google Drive not connected. In Settings → Google Drive & Docs, add client ID/secret and click Connect Google."}, 400)
                    return
                result = create_doc_from_text(title or "RFE and Bug Tracker Report", content)
                self.send_json({"ok": True, "url": result.get("url", ""), "id": result.get("id", "")})
            except Exception as e:
                self.send_json({"ok": False, "error": str(e)}, 400)
            finally:
                if _taminator_src_path() in sys.path:
                    sys.path.remove(_taminator_src_path())
            return
        if path == "api/google/create-gmail-draft":
            customer = (data.get("customer") or "").strip()
            title = (data.get("title") or "").strip() or (customer and f"RFE Report - {customer}")
            content = data.get("content")
            if not content and customer:
                content, err = get_report_content(customer)
                if err:
                    self.send_json({"ok": False, "error": err}, 400)
                    return
            if not content:
                self.send_json({"ok": False, "error": "Provide customer (to load report) or content and title."}, 400)
                return
            try:
                sys.path.insert(0, _taminator_src_path())
                from taminator.integrations.google_drive import create_gmail_draft, get_credentials
                if not get_credentials():
                    self.send_json({"ok": False, "error": "Google not connected. In Settings → Google Drive & Docs, add client ID/secret and click Connect Google. Reconnect to enable Gmail drafts."}, 400)
                    return
                result = create_gmail_draft(title or "RFE and Bug Tracker Report", content)
                self.send_json({"ok": True, "url": result.get("url", ""), "draft_id": result.get("draft_id", ""), "message_id": result.get("message_id", "")})
            except Exception as e:
                self.send_json({"ok": False, "error": str(e)}, 400)
            finally:
                if _taminator_src_path() in sys.path:
                    sys.path.remove(_taminator_src_path())
            return
        if path.rstrip("/") == "api/google/set-credentials" or path == "api/google/set-credentials":
            client_id = (data.get("client_id") or "").strip()
            client_secret = (data.get("client_secret") or data.get("client_secret_value") or "").strip()
            if not client_id or not client_secret:
                self.send_json({"ok": False, "error": "client_id and client_secret are required"}, 400)
                return
            config_dir = Path.home() / ".config" / "taminator"
            config_dir.mkdir(parents=True, exist_ok=True)
            credentials_file = config_dir / "google_credentials.json"
            payload = {
                "installed": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["http://localhost"],
                }
            }
            try:
                with open(credentials_file, "w") as f:
                    json.dump(payload, f, indent=2)
                os.chmod(credentials_file, 0o600)
                self.send_json({"ok": True, "message": "Credentials saved. Click Connect Google to sign in."})
            except Exception as e:
                self.send_json({"ok": False, "error": str(e)}, 500)
            return
        if path == "api/report-structure":
            try:
                _save_report_structure(data)
                self.send_json({"ok": True, "message": "Report structure saved.", "structure": _load_report_structure()})
            except Exception as e:
                self.send_json({"ok": False, "error": str(e)}, 500)
            return
        if path == "api/report-structure/preview":
            try:
                struct = dict(DEFAULT_REPORT_STRUCTURE)
                for k in struct:
                    if k in data and data[k] is not None:
                        if k == "section_order" and isinstance(data[k], list):
                            struct[k] = [str(x) for x in data[k] if str(x) in ("customer_info", "rfe", "bug", "notes")] or struct[k]
                        elif k == "section_included" and isinstance(data[k], dict):
                            struct[k] = {sid: bool(data[k].get(sid, True)) for sid in ("customer_info", "rfe", "bug", "notes")}
                        elif k not in ("section_order", "section_included"):
                            struct[k] = str(data[k]).strip() or struct[k]
                markdown = _build_report_from_structure(
                    struct, "sample", "Sample Customer", "12345", "contact@example.com", "TAM Name"
                )
                html = _markdown_to_html_fallback(markdown)
                text = _markdown_to_plain_text(markdown)
                csv_content = _markdown_tables_to_csv(markdown)
                self.send_json({"markdown": markdown, "html": html, "text": text, "csv": csv_content})
            except Exception as e:
                self.send_json({"ok": False, "error": str(e)}, 500)
            return
        if path == "api/reports/build":
            self._do_post_reports_build(data)
            return
        if path == "api/cases/from-paste":
            # Paste case numbers (or dump text); discover via Hydra, get JIRA statuses, auto-configure accounts.
            pasted = (data.get("pasted") or "").strip()
            case_numbers = data.get("case_numbers")
            if isinstance(case_numbers, list):
                case_numbers = [str(c).strip() for c in case_numbers if str(c).strip()]
            else:
                case_numbers = []
            if not case_numbers and pasted:
                # Parse case numbers from pasted text (e.g. Salesforce dump): 04xxxxxx or 8+ digit numbers
                case_numbers = list(dict.fromkeys(re.findall(r"\b(04\d{6})\b|\b(\d{8,})\b", pasted)))
                case_numbers = [c[0] or c[1] for c in case_numbers if c[0] or c[1]]
            if not case_numbers:
                self.send_json({"ok": False, "error": "Paste case numbers or a case list (e.g. from Salesforce), or send case_numbers array."}, 400)
                return
            _ensure_taminator_on_path()
            try:
                sys.path.insert(0, _taminator_src_path())
                from taminator.core import hydra_search
                from taminator.commands.check import JIRAClient
                from taminator.core import jira_config
                basic_auth = _get_hydra_basic_auth()
                bearer_token = _get_effective_hydra_token()
                token = None if basic_auth else bearer_token
                if not basic_auth and not token:
                    self.send_json({"ok": False, "error": "Customer Portal token or Red Hat username/password required for case lookup. Configure in Settings."}, 400)
                    return
                cases, detected_accounts = hydra_search.discover_cases_by_case_numbers(
                    token=token,
                    case_numbers=case_numbers,
                    basic_auth=basic_auth,
                    basic_auth_fallback=_get_hydra_basic_auth_credentials() if not basic_auth else None,
                    bearer_fallback=bearer_token if basic_auth else None,
                )
                if not cases:
                    self.send_json({"ok": False, "error": "No cases found for those case numbers. Check VPN and Portal credentials.", "case_numbers": case_numbers[:20]}, 404)
                    return
                # Auto-configure accounts from detected account info
                accounts_ensured = []
                for acc in detected_accounts:
                    nums = acc.get("account_numbers") or []
                    name = (acc.get("customer_name") or "").strip()
                    if nums:
                        ensured = _ensure_account_from_dump(nums, name)
                        if ensured:
                            accounts_ensured.append(ensured)
                # Fetch JIRA status for each case (report uses JIRA status, not internal/case status)
                jira_ids = list(dict.fromkeys([c[3] for c in cases if c[3]]))
                jira_statuses = {}
                if jira_ids:
                    _base, _auth_header, _ = jira_config.get_jira_auth()
                    if _auth_header:
                        api_url = jira_config.get_jira_api_url()
                        client = JIRAClient(api_base_url=api_url, auth_header=_auth_header)
                        for jid in jira_ids:
                            info = client.get_issue_status(jid)
                            jira_statuses[jid] = (info or {}).get("status") or "—"
                    else:
                        for jid in jira_ids:
                            jira_statuses[jid] = "—"
                # Build report rows: case_number, jira_id, summary, jira_status (not case status)
                report_rows = []
                for case_number, summary, _case_status, jira_id, kind in cases:
                    jira_status = jira_statuses.get(jira_id, "—") if jira_id else "—"
                    report_rows.append({"case_number": case_number, "jira_id": jira_id or "TBD", "summary": summary, "jira_status": jira_status, "kind": kind})
                # Markdown table snippet
                def _cell(s):
                    return (str(s).replace("|", " ").replace("\n", " ").strip()[:200]) if s else ""
                lines = ["| RED HAT JIRA ID | Support Case | Description | Status/Notes |", "| --- | --- | --- | --- |"]
                for r in report_rows:
                    case_cell = f"[{r['case_number']}](https://access.redhat.com/support/cases/#/case/{r['case_number']})" if r["case_number"] else ""
                    jira_cell = r["jira_id"]
                    lines.append(f"| {jira_cell} | {case_cell} | {_cell(r['summary'][:80])} | {r['jira_status']} |")
                report_markdown = "\n".join(lines)
                self.send_json({
                    "ok": True,
                    "cases": report_rows,
                    "report_markdown": report_markdown,
                    "accounts_ensured": accounts_ensured,
                    "detected_accounts": detected_accounts,
                    "message": f"Found {len(cases)} case(s). " + (f"Added/updated {len(accounts_ensured)} account(s)." if accounts_ensured else ""),
                })
            except Exception as e:
                self.send_json({"ok": False, "error": str(e)}, 500)
            finally:
                if _taminator_src_path() in sys.path:
                    sys.path.remove(_taminator_src_path())
            return
        if path == "api/jira/from-paste":
            # JIRA keys/URLs only — for accounts with no case↔JIRA linkage in access.redhat.com (e.g. SNOW, ROSA FedRAMP).
            pasted = (data.get("pasted") or "").strip()
            if not pasted:
                self.send_json({"ok": False, "error": "Paste at least one JIRA key or URL."}, 400)
                return
            jira_keys = _parse_jira_keys_from_paste(pasted)
            if not jira_keys:
                self.send_json(
                    {
                        "ok": False,
                        "error": "No JIRA issue keys found. Paste issues.redhat.com browse links or issue keys (e.g. AAPRFE-100).",
                    },
                    400,
                )
                return
            if len(jira_keys) > 200:
                self.send_json({"ok": False, "error": "Too many issues; paste at most 200 keys at a time."}, 400)
                return
            _ensure_taminator_on_path()
            try:
                sys.path.insert(0, _taminator_src_path())
                from taminator.commands.check import JIRAClient
                from taminator.core import jira_config
                from taminator.commands.update import _format_case_cell, _format_jira_cell, _escape_table_cell

                _base, _auth_header, _ = jira_config.get_jira_auth()
                if not _auth_header:
                    self.send_json(
                        {
                            "ok": False,
                            "error": "JIRA is not configured. In Settings, add a Red Hat JIRA token (or JIRA Cloud credentials) to look up pasted issues.",
                        },
                        400,
                    )
                    return
                api_url = jira_config.get_jira_api_url()
                client = JIRAClient(api_base_url=api_url, auth_header=_auth_header)
                rfe_row_lines = []
                bug_row_lines = []
                report_rows = []
                for jid in jira_keys:
                    info = client.get_issue_status(jid) or {}
                    st = (info.get("status") or "").strip() or "—"
                    if st in ("ERROR", "NOT_FOUND"):
                        st = (info.get("error") or st).strip()
                    summary = (info.get("summary") or "—").strip() or "—"
                    itype = (info.get("issue_type") or "").strip()
                    kind = _classify_jira_paste_row_kind(itype, summary)
                    jira_cell = _format_jira_cell(jid)
                    case_cell = _format_case_cell(NOT_IN_PORTAL_SUPPORT_CASE_LABEL)
                    row_line = f"| {jira_cell} | {case_cell} | {_escape_table_cell(summary[:200])} | {_escape_table_cell(str(st)[:200])} |"
                    if kind == "Bug":
                        bug_row_lines.append(row_line)
                    else:
                        rfe_row_lines.append(row_line)
                    report_rows.append(
                        {
                            "jira_id": jid,
                            "summary": summary,
                            "jira_status": st,
                            "issue_type": itype,
                            "kind": kind,
                            "no_portal_case": True,
                        }
                    )
                sep = "|-----------------|--------------|-------------|--------------|"
                head = "| RED HAT JIRA ID | Support Case | Description | Status/Notes |"
                parts = []
                if rfe_row_lines:
                    parts.append(
                        "**Enhancement (RFE) — pasted, not linked in Customer Portal**\n\n"
                        + head
                        + "\n"
                        + sep
                        + "\n"
                        + "\n".join(rfe_row_lines)
                    )
                if bug_row_lines:
                    parts.append(
                        "**Bugs — pasted, not linked in Customer Portal**\n\n"
                        + head
                        + "\n"
                        + sep
                        + "\n"
                        + "\n".join(bug_row_lines)
                    )
                report_markdown = "\n\n".join(parts) if parts else ""
                n = len(jira_keys)
                self.send_json(
                    {
                        "ok": True,
                        "jira_keys": jira_keys,
                        "cases": report_rows,
                        "report_markdown": report_markdown,
                        "message": f"Found {n} JIRA issue(s). Support Case shows “{NOT_IN_PORTAL_SUPPORT_CASE_LABEL}” — copy the table into your report.",
                    }
                )
            except Exception as e:
                self.send_json({"ok": False, "error": str(e)}, 500)
            finally:
                if _taminator_src_path() in sys.path:
                    sys.path.remove(_taminator_src_path())
            return
        if path.rstrip("/") == "api/library/delete" or path == "api/library/delete":
            path_str = (data.get("path") or data.get("path_str") or "").strip()
            if not path_str:
                self.send_json({"ok": False, "error": "path is required"}, 400)
                return
            ok, err = delete_report(path_str)
            if ok:
                self.send_json({"ok": True, "message": "Report deleted"})
            else:
                self.send_json({"ok": False, "error": err or "Delete failed"}, 400)
            return
        if path == "api/google/connect":
            try:
                sys.path.insert(0, _taminator_src_path())
                from taminator.integrations.google_drive import run_oauth_flow
                success, err = run_oauth_flow()
                if success:
                    self.send_json({"ok": True, "message": "Connected. You can now back up to Drive and open reports in Google Docs."})
                else:
                    self.send_json({"ok": False, "error": err or "OAuth flow failed"}, 400)
            except Exception as e:
                self.send_json({"ok": False, "error": str(e)}, 400)
            finally:
                if _taminator_src_path() in sys.path:
                    sys.path.remove(_taminator_src_path())
            return
        if path == "api/google/backup":
            try:
                sys.path.insert(0, _taminator_src_path())
                from taminator.integrations.google_drive import backup_reports_to_drive, get_credentials
                if not get_credentials():
                    self.send_json({"ok": False, "error": "Google Drive not connected. Click Connect Google below first."}, 400)
                    return
                reports = list_reports()
                files = []
                for r in reports:
                    path_str = r.get("path") or ""
                    name = r.get("name") or r.get("customer", "report") + ".md"
                    try:
                        content = Path(path_str).read_text(encoding="utf-8", errors="replace")
                        files.append({"name": name, "content": content})
                    except Exception:
                        continue
                if not files:
                    self.send_json({"ok": False, "error": "No report files found to back up."}, 400)
                    return
                result = backup_reports_to_drive(files)
                self.send_json({"ok": True, "url": result.get("url", ""), "count": result.get("count", 0)})
            except Exception as e:
                self.send_json({"ok": False, "error": str(e)}, 400)
            finally:
                if _taminator_src_path() in sys.path:
                    sys.path.remove(_taminator_src_path())
            return
        if path == "api/config/set-token":
            # Never log or expose token values (enterprise UX standard: security).
            token_type = (data.get("type") or data.get("token_type") or "").strip().lower()
            value = (data.get("value") or data.get("token") or "").strip()
            if not token_type or not value:
                self.send_json({"ok": False, "error": "type and value required"}, 400)
                return
            allowed = ("jira", "portal", "jira_token", "portal_token")
            if token_type not in allowed:
                self.send_json({"ok": False, "error": "type must be jira or portal"}, 400)
                return
            if token_type in ("jira", "jira_token"):
                key = "jira_token"
            else:
                key = "portal_token"
            config_dir = Path.home() / ".config" / "taminator"
            tokens_file = config_dir / "ui_tokens.json"
            src_path = _taminator_src_path()
            try:
                if src_path not in sys.path:
                    sys.path.insert(0, src_path)
                from taminator.core.token_store import load_ui_tokens, save_ui_tokens
                existing = load_ui_tokens(tokens_file)
                existing[key] = value
                save_ui_tokens(existing, tokens_file)
                # When Vault is configured, sync to Vault as well
                try:
                    from taminator.core.hybrid_auth import hybrid_auth
                    if hybrid_auth.is_vault_available():
                        service = "jira" if key == "jira_token" else "portal" if key == "portal_token" else None
                        if service:
                            hybrid_auth.set_token(service, value)
                except Exception:
                    pass
            except Exception as e:
                traceback.print_exc(file=sys.stderr)
                self.send_json({"ok": False, "error": str(e)}, 500)
                return
            finally:
                if src_path in sys.path:
                    sys.path.remove(src_path)
            self.send_json({"ok": True, "message": "Token saved. Restart the server or run a report for it to take effect."})
            return
        if path.rstrip("/") == "api/config/set-hydra-credentials":
            username = (data.get("redhat_username") or "").strip()
            password = (data.get("redhat_password") or "")
            config_dir = Path.home() / ".config" / "taminator"
            tokens_file = config_dir / "ui_tokens.json"
            src_path = _taminator_src_path()
            try:
                if src_path not in sys.path:
                    sys.path.insert(0, src_path)
                from taminator.core.token_store import load_ui_tokens, save_ui_tokens
                existing = load_ui_tokens(tokens_file)
                if username:
                    existing["redhat_username"] = username
                else:
                    existing.pop("redhat_username", None)
                if password:
                    existing["redhat_password"] = password
                else:
                    existing.pop("redhat_password", None)
                save_ui_tokens(existing, tokens_file)
            except Exception as e:
                traceback.print_exc(file=sys.stderr)
                self.send_json({"ok": False, "error": str(e)}, 500)
                return
            finally:
                if src_path in sys.path:
                    sys.path.remove(src_path)
            self.send_json({"ok": True, "message": "Hydra credentials saved (stored encoded). Env vars override these."})
            return
        if path == "api/config/set-jira-settings":
            config_dir = Path.home() / ".config" / "taminator"
            tokens_file = config_dir / "ui_tokens.json"
            src_path = _taminator_src_path()
            try:
                if src_path not in sys.path:
                    sys.path.insert(0, src_path)
                from taminator.core.token_store import load_ui_tokens, save_ui_tokens
                existing = load_ui_tokens(tokens_file)
                for key in ("jira_base_url", "jira_email", "jira_api_token", "jira_token"):
                    if key not in data:
                        continue
                    val = data[key]
                    if val is None or (isinstance(val, str) and not val.strip()):
                        existing.pop(key, None)
                    else:
                        existing[key] = val.strip() if isinstance(val, str) else val
                save_ui_tokens(existing, tokens_file)
                self.send_json({"ok": True, "message": "JIRA settings saved."})
            except Exception as e:
                traceback.print_exc(file=sys.stderr)
                self.send_json({"ok": False, "error": str(e)}, 500)
            finally:
                if src_path in sys.path:
                    sys.path.remove(src_path)
            return
        if path == "api/vault/set":
            service = (data.get("service") or "").strip()
            token = (data.get("token") or "").strip()
            if not service or not token:
                self.send_json({"ok": False, "error": "service and token required"}, 400)
                return
            try:
                sys.path.insert(0, _taminator_src_path())
                from taminator.core.hybrid_auth import hybrid_auth
                ok = hybrid_auth.set_token(service, token)
                if _taminator_src_path() in sys.path:
                    sys.path.remove(_taminator_src_path())
                self.send_json({"ok": ok, "message": "Token stored." if ok else "Failed to store token."})
            except Exception as e:
                if _taminator_src_path() in sys.path:
                    sys.path.remove(_taminator_src_path())
                self.send_json({"ok": False, "error": str(e)}, 500)
            return
        if path == "api/vault/delete":
            service = (data.get("service") or "").strip()
            if not service:
                self.send_json({"ok": False, "error": "service required"}, 400)
                return
            try:
                sys.path.insert(0, _taminator_src_path())
                from taminator.core.vault_client import vault_client
                ok = vault_client.delete_token(service)
                if _taminator_src_path() in sys.path:
                    sys.path.remove(_taminator_src_path())
                self.send_json({"ok": ok, "message": "Token deleted." if ok else "Failed to delete."})
            except Exception as e:
                if _taminator_src_path() in sys.path:
                    sys.path.remove(_taminator_src_path())
                self.send_json({"ok": False, "error": str(e)}, 500)
            return
        if path == "api/vault/migrate":
            try:
                sys.path.insert(0, _taminator_src_path())
                from taminator.core.hybrid_auth import hybrid_auth
                migrated, failed = hybrid_auth.migrate_to_vault()
                if _taminator_src_path() in sys.path:
                    sys.path.remove(_taminator_src_path())
                self.send_json({"ok": True, "migrated": migrated, "failed": failed, "message": f"Migrated {migrated} tokens to Vault."})
            except Exception as e:
                if _taminator_src_path() in sys.path:
                    sys.path.remove(_taminator_src_path())
                self.send_json({"ok": False, "error": str(e)}, 500)
            return
        if path == "api/accounts":
            action = (data.get("action") or "add").strip().lower()
            accounts = _load_accounts()
            aid = (data.get("id") or "").strip()
            account_number = (data.get("account_number") or "").strip()
            account_numbers = _normalize_account_numbers(data.get("account_numbers") or (account_number if account_number else None))
            if not account_numbers and account_number:
                account_numbers = [account_number]
            customer_name = (data.get("customer_name") or "").strip()
            if action == "delete":
                if not aid:
                    self.send_json({"ok": False, "error": "id required to delete"}, 400)
                    return
                new_list = [a for a in accounts if (a.get("id") or "").strip() != aid]
                if len(new_list) == len(accounts):
                    self.send_json({"ok": False, "error": "Account not found"}, 404)
                    return
                _save_accounts(new_list)
                self.send_json({"ok": True, "message": "Account removed", "accounts": new_list})
                return
            if action == "update":
                if not aid:
                    self.send_json({"ok": False, "error": "id required to update"}, 400)
                    return
                idx = next((i for i, a in enumerate(accounts) if (a.get("id") or "").strip() == aid), None)
                if idx is None:
                    self.send_json({"ok": False, "error": "Account not found"}, 404)
                    return
                if account_numbers:
                    accounts[idx]["account_numbers"] = account_numbers
                    accounts[idx]["account_number"] = account_numbers[0]
                if customer_name:
                    accounts[idx]["customer_name"] = customer_name
                if "sbr_groups" in data:
                    accounts[idx]["sbr_groups"] = _normalize_sbr_groups(data["sbr_groups"])
                _save_accounts(accounts)
                self.send_json({"ok": True, "message": "Account updated", "accounts": accounts})
                return
            # add
            if not customer_name or not account_numbers:
                self.send_json({"ok": False, "error": "customer_name and at least one account number required"}, 400)
                return
            # Avoid duplicate accounts: only merge when same account numbers and same SBR group
            idx, existing = _find_account_by_account_numbers(accounts, account_numbers, sbr_groups=data.get("sbr_groups") or [])
            if idx is not None:
                merged_nums = list(dict.fromkeys((existing.get("account_numbers") or []) + list(account_numbers)))
                merged_nums = _normalize_account_numbers(merged_nums) or merged_nums
                accounts[idx]["account_numbers"] = merged_nums
                accounts[idx]["account_number"] = merged_nums[0] if merged_nums else ""
                accounts[idx]["customer_name"] = customer_name
                if "sbr_groups" in data:
                    accounts[idx]["sbr_groups"] = _normalize_sbr_groups(data["sbr_groups"])
                _save_accounts(accounts)
                self.send_json({"ok": True, "message": "Account updated (already had this account number)", "accounts": accounts})
                return
            if not aid:
                aid = _slug(customer_name)
            if not aid:
                self.send_json({"ok": False, "error": "Could not derive id from customer name"}, 400)
                return
            if any((a.get("id") or "").strip() == aid for a in accounts):
                self.send_json({"ok": False, "error": f"Account with id '{aid}' already exists"}, 400)
                return
            entry = {"id": aid, "account_numbers": account_numbers, "account_number": account_numbers[0], "customer_name": customer_name, "created_at": datetime.utcnow().isoformat() + "Z"}
            sbr = _normalize_sbr_groups(data.get("sbr_groups"))
            if sbr:
                entry["sbr_groups"] = sbr
            accounts.append(entry)
            _save_accounts(accounts)
            self.send_json({"ok": True, "message": "Account added", "accounts": accounts})
            return
        if path not in ("api/check", "api/update"):
            self.send_json({"ok": False, "error": "Not found"}, 404)
            return
        customer = (data.get("customer") or "").strip()
        use_test_data = data.get("test_data") is True
        full_refresh = data.get("full_refresh") is True
        if not customer and not use_test_data:
            self.send_json({"ok": False, "error": "customer required (or test_data: true)"}, 400)
            return
        if use_test_data:
            args = ["--test-data"]
        else:
            args = [customer]
        # Debug: set TAMINATOR_DEBUG_* so CLI logs API response details to stderr (shown in result).
        # HYDRA_JIRA=missing-case doc keys + external trackers data; HYDRA_RESPONSE=query + numFound + first doc keys;
        # JIRA=per-issue HTTP status/body; RHCASE=rhcase stdout/stderr when fallback is used.
        extra_env = {}
        if data.get("debug") is True:
            extra_env["TAMINATOR_DEBUG_HYDRA_JIRA"] = "1"
            extra_env["TAMINATOR_DEBUG_HYDRA_RESPONSE"] = "1"
            extra_env["TAMINATOR_DEBUG_JIRA"] = "1"
            extra_env["TAMINATOR_DEBUG_RHCASE"] = "1"
        if path == "api/check":
            stdout, stderr, code = run_cmd(["check"] + args, extra_env=extra_env or None)
        else:
            # CLI expects: update <customer> -y (customer must be argv[2])
            # --verbose: external trackers (JIRA links) when available
            # --full-refresh: re-discover all cases from portal and repopulate report
            update_args = ["-y", "--verbose"]
            if full_refresh:
                update_args.append("--full-refresh")
            stdout, stderr, code = run_cmd(["update"] + args + update_args, extra_env=extra_env or None)
        self.send_json({
            "ok": code == 0,
            "returncode": code,
            "stdout": stdout,
            "stderr": stderr,
        })


def serve(port=8765, open_browser=True):
    _ensure_taminator_on_path()
    if not os.path.isdir(WEB_DIR):
        print(f"Web directory not found: {WEB_DIR}", file=sys.stderr)
        sys.exit(1)
    server = ThreadingHTTPServer(("127.0.0.1", port), TaminatorHandler)
    url = f"http://127.0.0.1:{port}"
    print(f"RFE and Bug Tracker web UI: {url}")
    if open_browser:
        import webbrowser
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.shutdown()


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="RFE and Bug Tracker web UI server")
    p.add_argument("--port", type=int, default=8765, help="Port (default 8765)")
    p.add_argument("--no-browser", action="store_true", help="Do not open browser")
    args = p.parse_args()
    serve(port=args.port, open_browser=not args.no_browser)
