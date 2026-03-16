"""
Hydra SOLR case search for Taminator.

Uses the same API as rhcase (case search): Hydra REST search/cases.
Authentication: Customer Portal Bearer token or Red Hat SSO username/password (basic auth).
Repurposed from https://gitlab.cee.redhat.com/gvaughn/rhcase for report population.
"""

import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import requests
except ImportError:
    requests = None

SSO_TOKEN_URL = "https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token"
HYDRA_SEARCH_URL = "https://access.redhat.com/hydra/rest/search/cases"

# Authoritative list: Red Hat Centralized Jira Project Mapping in The Source (TAM Manual).
# To determine where an RFE should be submitted, use the comprehensive JIRA and RFE mapping
# for products there. It is a community-managed page across all products; if you find an issue,
# outdated information, or a missing product in the JIRA mapping, flag it and see if you can
# get it corrected. Format: PROJECTKEY-NNNN. Used for discovery, report parsing, and link formatting.
# Users can add niche/custom project keys via ~/.config/taminator/jira_prefixes.txt (one key per line).
_BUILTIN_JIRA_PREFIXES = (
    "AAP", "AAPRFE", "ACA", "ACM", "ANA", "ANSTRAT", "ARO", "BUILD",
    "CEQ", "CM", "CNV", "CMP", "COO", "CRW", "CSB", "DBZ", "DFBUGS",
    "DISCOVERY", "ECOPROJECT", "ENTMQBR", "ENTMQCL", "ENTMQIC", "ENTESB", "ENTMQST",
    "GITOPS", "HMS", "IPT", "JBCS", "JBEAP", "JDG", "JWS", "KATA", "KEYCLOAK",
    "LOG", "MGMT", "MGDAPI", "MTV", "OADP", "OBSDA", "OCM", "OCMUI", "OCPBUGS",
    "OCPNODE", "OPENJDK", "OSPRH", "OSSM", "PODMAND", "POWERMON", "PROJQUAY",
    "QUARKUS", "RHBAC", "RHBK", "RHDM", "RHDHBUGS", "RHEL", "RHELAI", "RHELAIRFE",
    "RHELC", "RHIDP", "RHIN", "RHINENG", "RHOAIRFE", "RHOAIENG", "RHPAM", "RHSSO",
    "ROX", "RHTAP", "SAT", "SECENGSP", "SECURESIGN", "SB", "SKUPPER", "SRVKP",
    "SWATCH", "TC", "THREESCALE", "TRACING", "WINC", "WRKLDS", "XCMSTRAT",
)


def _load_user_jira_prefixes() -> Tuple[str, ...]:
    """Load user-defined JIRA project keys from ~/.config/taminator/jira_prefixes.txt.
    One key per line; lines starting with # or empty are ignored. Keys are stripped and uppercased.
    Enables niche mappings not yet in the main documentation."""
    path = Path.home() / ".config" / "taminator" / "jira_prefixes.txt"
    if not path.exists():
        return ()
    out = []
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            s = line.split("#", 1)[0].strip().upper()
            if s and s.isalnum():
                out.append(s)
    except OSError:
        pass
    return tuple(out)


_USER_JIRA_PREFIXES = _load_user_jira_prefixes()
JIRA_PROJECT_PREFIXES = _BUILTIN_JIRA_PREFIXES + _USER_JIRA_PREFIXES
JIRA_ID_REGEX_GROUP = "|".join(re.escape(p) + r"-\d+" for p in JIRA_PROJECT_PREFIXES)
JIRA_ID_PATTERN = re.compile(r"(" + JIRA_ID_REGEX_GROUP + ")")

# Keys that typically hold external trackers / attached resources / linked JIRA in case docs.
# We search these explicitly first so JIRA from "External trackers" is never missed.
EXTERNAL_TRACKER_KEYS = (
    "case_external_trackers",
    "external_trackers",
    "case_linked_resource",
    "linked_resources",
    "external_references",
    "case_external_ref",
    "case_trackers",
    "tracker_links",
    "external_id",
    "case_jiraKey",
    "case_jira_key",
    "jira_key",
    "issue_key",
    "jira_issue_key",
)


def get_bearer_token(username: str, password: str, timeout: int = 30) -> str:
    """Get Bearer token from Red Hat SSO using username/password (same as rhcase).

    Args:
        username: Red Hat SSO / Portal username
        password: Red Hat SSO / Portal password
        timeout: Request timeout in seconds

    Returns:
        Bearer token string for Hydra/Portal APIs.

    Raises:
        RuntimeError: If requests not available or SSO returns an error.
    """
    if not requests:
        raise RuntimeError("requests library required (pip install requests)")
    data = {
        "grant_type": "password",
        "client_id": "hydra-client-cli",
        "username": username,
        "password": password,
    }
    resp = requests.post(SSO_TOKEN_URL, data=data, timeout=timeout)
    resp.raise_for_status()
    token = resp.json().get("access_token")
    if not token:
        raise RuntimeError("No access_token in SSO response")
    return token


def get_bearer_token_from_env() -> Optional[str]:
    """Get Bearer token using REDHAT_USERNAME/REDHAT_PASSWORD or REDHAT_PORTAL_USERNAME/REDHAT_PORTAL_PASSWORD from environment."""
    username = os.environ.get("REDHAT_USERNAME") or os.environ.get("REDHAT_PORTAL_USERNAME")
    password = os.environ.get("REDHAT_PASSWORD") or os.environ.get("REDHAT_PORTAL_PASSWORD")
    if not username or not password:
        return None
    try:
        return get_bearer_token(username.strip(), password)
    except Exception:
        return None


def get_basic_auth_from_env() -> Optional[Tuple[str, str]]:
    """Return (username, password) for Hydra Basic auth from REDHAT_* or REDHAT_PORTAL_* env vars, or None."""
    username = os.environ.get("REDHAT_USERNAME") or os.environ.get("REDHAT_PORTAL_USERNAME")
    password = os.environ.get("REDHAT_PASSWORD") or os.environ.get("REDHAT_PORTAL_PASSWORD")
    if username and password:
        return (username.strip(), password)
    return None


def build_solr_query(
    account_numbers: List[str],
    include_closed: bool = False,
    modified_after: Optional[str] = None,
    created_after: Optional[str] = None,
    products: Optional[List[str]] = None,
    statuses: Optional[List[str]] = None,
) -> str:
    """Build SOLR query string for Hydra case search.

    Args:
        account_numbers: List of account numbers (required).
        include_closed: If False, add NOT case_status:Closed.
        modified_after: YYYY-MM-DD — cases modified on or after this date.
        created_after: YYYY-MM-DD — cases created on or after this date.
        products: Filter by product (substring match, OR'd).
        statuses: Filter by exact status (OR'd).

    Returns:
        SOLR query string.
    """
    clauses = []

    if account_numbers:
        accts = " OR ".join(f"case_accountNumber:{a}" for a in account_numbers)
        clauses.append(f"({accts})")

    if statuses:
        stats = " OR ".join(f'case_status:"{s}"' for s in statuses)
        clauses.append(f"({stats})")
    elif not include_closed:
        clauses.append("NOT case_status:Closed")

    if products:
        prods = " OR ".join(f"case_product:*{p}*" for p in products)
        clauses.append(f"({prods})")

    if modified_after:
        clauses.append(f"case_lastModifiedDate:[{modified_after}T00:00:00Z TO *]")
    if created_after:
        clauses.append(f"case_createdDate:[{created_after}T00:00:00Z TO *]")

    return " AND ".join(clauses) if clauses else "*:*"


def build_solr_query_by_case_numbers(case_numbers: List[str]) -> str:
    """Build SOLR query string for Hydra case search by case number(s).
    Use when the user pastes a list of case numbers (e.g. from Salesforce dump).
    """
    if not case_numbers:
        return "*:*"
    # Normalize: strip, ensure string; Hydra typically has case_number as string
    normalized = []
    for c in case_numbers:
        s = (c or "").strip()
        if s and re.match(r"^\d{6,}", s):
            normalized.append(s)
    if not normalized:
        return "*:*"
    clauses = " OR ".join(f"case_number:{c}" for c in normalized)
    return f"({clauses})"


def _extract_account_from_doc(doc: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Extract account number and optional customer name from a case doc.
    Returns None if no account; else dict with account_numbers (list) and customer_name (str, may be empty).
    """
    # Common Hydra/Portal fields for account
    acc_num = doc.get("case_accountNumber") or doc.get("case_account_number") or doc.get("account_number")
    acc_name = doc.get("case_accountName") or doc.get("case_account_name") or doc.get("account_name") or doc.get("customer_name")
    if acc_num is None and acc_name is None:
        return None
    numbers = []
    if acc_num is not None:
        if isinstance(acc_num, list):
            numbers = [str(x).strip() for x in acc_num if str(x).strip()]
        else:
            s = str(acc_num).strip()
            if s:
                numbers = [s]
    name = (acc_name or "").strip() if isinstance(acc_name, str) else ""
    if not numbers and not name:
        return None
    return {"account_numbers": numbers if numbers else [], "customer_name": name}


def search_cases(
    token: Optional[str] = None,
    query: str = "",
    start: int = 0,
    rows: int = 500,
    timeout: int = 60,
    basic_auth: Optional[Tuple[str, str]] = None,
) -> Dict[str, Any]:
    """Execute Hydra SOLR case search.

    Args:
        token: Bearer token (Portal or Hydra token). Ignored if basic_auth is set.
        query: SOLR query from build_solr_query().
        start: Pagination start.
        rows: Max rows to return.
        timeout: Request timeout in seconds.
        basic_auth: Optional (username, password) for HTTP Basic auth. When set, used instead of token.

    Returns:
        SOLR response dict with response.docs[].

    Raises:
        RuntimeError: If requests not available or request fails.
    """
    if not requests:
        raise RuntimeError("requests library required for Hydra search (pip install requests)")
    headers = {"Content-Type": "application/json"}
    params = {"q": query, "start": start, "rows": rows}
    if basic_auth:
        resp = requests.get(HYDRA_SEARCH_URL, headers=headers, params=params, auth=basic_auth, timeout=timeout)
    else:
        if not token:
            raise RuntimeError("Hydra search requires token or basic_auth")
        headers["Authorization"] = f"Bearer {token}"
        resp = requests.get(HYDRA_SEARCH_URL, headers=headers, params=params, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def _find_jira_in_value(val: Any, summary: str) -> Optional[str]:
    """Search a value (string, list, or dict) for first JIRA issue key (see JIRA_PROJECT_PREFIXES). Recurses into dicts/lists."""
    if isinstance(val, str):
        if val == summary:
            return None
        jira_match = JIRA_ID_PATTERN.search(val)
        return jira_match.group(1) if jira_match else None
    if isinstance(val, list):
        for item in val:
            found = _find_jira_in_value(item, summary)
            if found:
                return found
        return None
    if isinstance(val, dict):
        for k, v in val.items():
            if k in ("key", "id", "jira_key", "issue_key", "case_jiraKey", "case_jira_key"):
                if isinstance(v, str):
                    jira_match = JIRA_ID_PATTERN.search(v)
                    if jira_match:
                        return jira_match.group(1)
            found = _find_jira_in_value(v, summary)
            if found:
                return found
        return None
    return None


def _get_external_tracker_values(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Return a dict of key -> value for every EXTERNAL_TRACKER_KEYS key present in doc."""
    out: Dict[str, Any] = {}
    for key in EXTERNAL_TRACKER_KEYS:
        if key in doc and doc[key] is not None:
            out[key] = doc[key]
    return out


def _extract_jira_id_from_doc(doc: Dict[str, Any], summary: str) -> str:
    """Extract first JIRA issue key (see JIRA_PROJECT_PREFIXES) from doc. External trackers are source of truth (checked first), then summary, then full recursive scan."""
    import sys
    tracker_vals = _get_external_tracker_values(doc)
    # 1. External trackers first (source of truth for linked JIRA)
    for key, val in tracker_vals.items():
        found = _find_jira_in_value(val, summary)
        if found:
            return found
    # 2. From summary
    jira_match = JIRA_ID_PATTERN.search(summary)
    if jira_match:
        return jira_match.group(1)
    # 3. Recursive scan of entire doc (catches nested or unknown field names)
    for key, val in doc.items():
        if key == "case_summary":
            continue
        found = _find_jira_in_value(val, summary)
        if found:
            return found
    # Debug: when JIRA is missing, log doc keys and what data was returned for external trackers (set TAMINATOR_DEBUG_HYDRA_JIRA=1)
    if os.environ.get("TAMINATOR_DEBUG_HYDRA_JIRA"):
        case_num = doc.get("case_number", "?")
        all_keys = list(doc.keys())
        print(f"[hydra] case {case_num}: no JIRA in doc; top-level keys={all_keys}", file=sys.stderr)
        if tracker_vals:
            for k, v in tracker_vals.items():
                raw = repr(v)
                if len(raw) > 500:
                    raw = raw[:497] + "..."
                print(f"[hydra] case {case_num}: external trackers / attached resources — {k}={raw}", file=sys.stderr)
        else:
            present = [k for k in EXTERNAL_TRACKER_KEYS if k in doc]
            print(f"[hydra] case {case_num}: no external tracker data in doc (looked for {list(EXTERNAL_TRACKER_KEYS)}; present in doc: {present})", file=sys.stderr)
    return ""


def _extract_kind_from_tracker_values(tracker_vals: Dict[str, Any]) -> str:
    """Infer RFE vs Bug from external tracker data (type, issue_type, etc.). Returns 'RFE', 'Bug', or 'unknown'."""
    kind_keys = ("type", "issue_type", "issuetype", "tracker_type", "kind")
    rfe_vals = ("rfe", "enhancement", "enhancement request", "feature")
    bug_vals = ("bug", "bug report", "defect")

    def check_val(v: Any) -> Optional[str]:
        if isinstance(v, str):
            vn = v.strip().lower()
            if vn in rfe_vals:
                return "RFE"
            if vn in bug_vals:
                return "Bug"
            return None
        if isinstance(v, list):
            for item in v:
                r = check_val(item)
                if r:
                    return r
        if isinstance(v, dict):
            for k, val in v.items():
                if isinstance(k, str) and k.lower() in kind_keys:
                    r = check_val(val)
                    if r:
                        return r
                r = check_val(val)
                if r:
                    return r
        return None

    for _k, val in tracker_vals.items():
        r = check_val(val)
        if r:
            return r
    return "unknown"


def format_doc_for_report(doc: Dict[str, Any]) -> Tuple[str, str, str, str, str]:
    """Convert a SOLR case doc to (case_number, summary, status, jira_id, kind) for report rows.

    JIRA ID: external trackers (source of truth) first, then summary, then rest of doc.
    kind: from external tracker type/issue_type when present, else 'unknown'.
    """
    case_number = doc.get("case_number", "") or ""
    summary = doc.get("case_summary", "") or ""
    raw_status = doc.get("case_status", "") or ""
    status = raw_status[:50] if raw_status else ""
    jira_id = _extract_jira_id_from_doc(doc, summary)
    tracker_vals = _get_external_tracker_values(doc)
    kind = _extract_kind_from_tracker_values(tracker_vals)
    return (case_number, summary, status, jira_id, kind)


def discover_cases(
    token: Optional[str] = None,
    account_numbers: Optional[List[str]] = None,
    months_back: int = 1,
    include_closed: bool = False,
    products: Optional[List[str]] = None,
    max_rows: int = 500,
    basic_auth: Optional[Tuple[str, str]] = None,
) -> List[Tuple[str, str, str, str]]:
    """Discover cases for account(s) via Hydra and return list of (case_number, summary, status, jira_id).

    Paginates through the API until all matching cases are fetched (or max_rows is reached),
    so we get the full set (e.g. 22 RFEs) instead of only the first page.

    Args:
        token: Bearer token. Ignored if basic_auth is set.
        account_numbers: At least one account number.
        months_back: Only cases modified in the last N months.
        include_closed: Include closed cases.
        products: Optional product filter (e.g. SBR/product name substring).
        max_rows: Maximum cases to return total (across all pages).
        basic_auth: Optional (username, password) for HTTP Basic auth. When set, used instead of token.

    Returns:
        List of (case_number, summary, status, jira_id, kind) for report table rows. kind is 'RFE', 'Bug', or 'unknown' from external trackers.
    """
    if not account_numbers:
        return []
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=months_back * 31)
    modified_after = start_date.strftime("%Y-%m-%d")
    query = build_solr_query(
        account_numbers=account_numbers,
        include_closed=include_closed,
        modified_after=modified_after,
        products=products,
    )
    page_size = 100
    all_docs = []
    start = 0
    first_page = True
    while start < max_rows:
        result = search_cases(token=token, query=query, start=start, rows=page_size, basic_auth=basic_auth)
        docs = result.get("response", {}).get("docs", [])
        all_docs.extend(docs)
        # Debug: log what the Hydra API returned (set TAMINATOR_DEBUG_HYDRA_RESPONSE=1)
        if first_page and os.environ.get("TAMINATOR_DEBUG_HYDRA_RESPONSE"):
            import sys
            resp = result.get("response", {})
            num_found = resp.get("numFound", "?")
            print(f"[hydra] API response: response keys={list(result.keys())}; response.numFound={num_found}; this page docs={len(docs)}", file=sys.stderr)
            print(f"[hydra] SOLR query: q={query[:200]}{'...' if len(query) > 200 else ''}", file=sys.stderr)
            if docs:
                print(f"[hydra] first doc keys: {list(docs[0].keys())}", file=sys.stderr)
            first_page = False
        if len(docs) < page_size:
            break
        start += page_size
    return [format_doc_for_report(d) for d in all_docs[:max_rows]]


def discover_cases_by_case_numbers(
    token: Optional[str] = None,
    case_numbers: Optional[List[str]] = None,
    basic_auth: Optional[Tuple[str, str]] = None,
    max_rows: int = 500,
) -> Tuple[List[Tuple[str, str, str, str, str]], List[Dict[str, Any]]]:
    """Discover cases by a list of case numbers (e.g. from pasted Salesforce dump).
    Does not filter by date; returns case data and JIRA IDs. Also extracts account
    number(s) and optional customer name from each doc so the caller can auto-configure accounts.

    Returns:
        (cases, detected_accounts)
        cases: list of (case_number, summary, status, jira_id, kind). status is case_status from API (not JIRA status).
        detected_accounts: list of {"account_numbers": [...], "customer_name": str}, deduplicated by account_numbers.
    """
    if not case_numbers:
        return [], []
    query = build_solr_query_by_case_numbers(case_numbers)
    page_size = 100
    all_docs = []
    start = 0
    while start < max_rows:
        result = search_cases(token=token, query=query, start=start, rows=page_size, basic_auth=basic_auth)
        docs = result.get("response", {}).get("docs", [])
        all_docs.extend(docs)
        if len(docs) < page_size:
            break
        start += page_size
    cases = [format_doc_for_report(d) for d in all_docs[:max_rows]]
    # Collect unique account info from docs (for auto-configuring accounts)
    seen_keys: set = set()
    detected_accounts: List[Dict[str, Any]] = []
    for d in all_docs:
        acc = _extract_account_from_doc(d)
        if not acc:
            continue
        nums = tuple(sorted(acc.get("account_numbers") or []))
        if not nums:
            continue
        key = nums
        if key in seen_keys:
            continue
        seen_keys.add(key)
        # Prefer customer_name from doc; if missing, use placeholder
        name = (acc.get("customer_name") or "").strip()
        if not name:
            name = f"Account {nums[0]}" if nums else "Account"
        detected_accounts.append({"account_numbers": list(nums), "customer_name": name})
    return cases, detected_accounts


def discover_case_groups_for_account(
    token: Optional[str] = None,
    account_numbers: Optional[List[str]] = None,
    months_back: int = 1,
    max_rows: int = 500,
    basic_auth: Optional[Tuple[str, str]] = None,
) -> Dict[str, List[str]]:
    """Discover SBR and product groups that have cases for the given account(s).

    Calls the Hydra case search API filtered by account (and optionally date),
    then collects unique case_sbr and case_product values from the returned docs.
    Use this to know which "case groups" (SBR/product) exist under an account so you
    can filter discovery (e.g. only Ansible cases) or show the user which groups to pick.

    Returns:
        {"sbr": ["Ansible", ...], "product": ["Ansible Automation Platform", ...]}
        SBR and product are sorted and deduplicated; empty list if none or API error.
    """
    if not account_numbers:
        return {"sbr": [], "product": []}
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=months_back * 31)
    modified_after = start_date.strftime("%Y-%m-%d")
    query = build_solr_query(
        account_numbers=account_numbers,
        include_closed=False,
        modified_after=modified_after,
    )
    try:
        result = search_cases(token=token, query=query, start=0, rows=max_rows, basic_auth=basic_auth)
    except Exception:
        return {"sbr": [], "product": []}
    docs = result.get("response", {}).get("docs", [])
    sbr_set: set = set()
    product_set: set = set()

    def _add(val: Any) -> None:
        if isinstance(val, str) and val.strip():
            sbr_set.add(val.strip())
        elif isinstance(val, list):
            for v in val:
                if isinstance(v, str) and v.strip():
                    sbr_set.add(v.strip())

    def _add_product(val: Any) -> None:
        if isinstance(val, str) and val.strip():
            product_set.add(val.strip())
        elif isinstance(val, list):
            for v in val:
                if isinstance(v, str) and v.strip():
                    product_set.add(v.strip())

    for d in docs:
        _add(d.get("case_sbr"))
        _add_product(d.get("case_product"))

    return {
        "sbr": sorted(sbr_set),
        "product": sorted(product_set),
    }
