"""
tam-rfe update: Auto-update customer RFE/Bug reports with current JIRA statuses.

Fetches current JIRA statuses and updates the report file in-place,
preserving formatting and adding update timestamp.

Usage:
    tam-rfe update <customer>
    tam-rfe update --test-data
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

from ..core.hybrid_auth import hybrid_auth
from ..core.auth_box import auth_required, AuthType
from ..core.hydra_search import discover_cases as hydra_discover_cases, get_bearer_token_from_env, get_basic_auth_from_env, JIRA_ID_REGEX_GROUP
from .check import CustomerReportParser, JIRAClient, _resolve_customer_arg
from ..core import jira_config

console = Console()


class ReportUpdater:
    """Update customer reports with current JIRA statuses."""
    
    @staticmethod
    def update_report_file(report_path: Path, current_statuses: Dict[str, Dict]) -> Tuple[int, str]:
        """
        Update report file with current JIRA statuses.
        
        Args:
            report_path: Path to report file
            current_statuses: Dictionary of current JIRA statuses
        
        Returns:
            Tuple of (updates_made, new_content)
        """
        with open(report_path, 'r') as f:
            content = f.read()
        
        original_content = content
        updates_made = 0
        
        # Find and replace statuses in markdown tables
        # Format: | AAPRFE-762 | ... | Status Name |
        for jira_id, status_info in current_statuses.items():
            new_status = status_info.get('status', 'ERROR')
            clones = status_info.get('clones') or []
            if clones:
                new_status = new_status + " | Clones: " + ", ".join(clones)
            
            # Skip errors
            if status_info.get('status') in ['ERROR', 'NOT_FOUND']:
                continue
            
            # Pattern: Match JIRA ID row; replace last column (Status/Notes). First column may be plain ID or [ID](url). Use [^|\n]* so we never match across newlines.
            jira_col = rf'(?:\[\s*{re.escape(jira_id)}\s*\]\s*\([^\)]+\)|{re.escape(jira_id)})'
            pattern_4 = rf'(\|\s*{jira_col}\s*\|[^|\n]*\|[^|\n]*\|\s*)([^\|\n]+?)(\s*\|)'
            pattern_5 = rf'(\|\s*{jira_col}\s*\|[^|\n]*\|[^|\n]*\|[^|\n]*\|\s*)([^\|\n]+?)(\s*\|)'
            
            def replacer(match):
                nonlocal updates_made
                old_status = match.group(2).strip()
                if old_status.lower() != new_status.lower():
                    updates_made += 1
                    return f"{match.group(1)}{new_status}{match.group(3)}"
                return match.group(0)
            
            content = re.sub(pattern_4, replacer, content)
            content = re.sub(pattern_5, replacer, content)
        
        # Refresh summary line to match actual RFE/Bug row counts
        content = _refresh_summary_line_from_content(content)
        
        # Add update timestamp at the top (replace any existing Last Updated lines so we don't stack them)
        if updates_made > 0:
            timestamp = datetime.now().strftime('%b %d, %Y, %I:%M %p %Z')
            update_line = f"**Last Updated:** {timestamp} (via Taminator)\n\n"
            # Remove any existing "**Last Updated:** ... (via Taminator)" lines
            content = re.sub(r'\n?\*\*Last Updated:\*\*[^\n]+\(via Taminator\)\n+', '\n', content)
            # Find the first line that looks like report header (timestamp + optional TAM name) and add Last Updated after it
            author_pattern = r'(^[A-Za-z]{3} \d{1,2}, \d{4},[^\n]+\n)'
            match = re.search(author_pattern, content, re.MULTILINE)
            if match:
                author_line = match.group(1)
                content = content.replace(author_line, author_line + update_line, 1)
            else:
                content = update_line + content
        
        return updates_made, content
    
    @staticmethod
    def create_backup(report_path: Path) -> Path:
        """
        Create backup of report before updating.
        
        Args:
            report_path: Path to report file
        
        Returns:
            Path to backup file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = report_path.parent / f"{report_path.stem}_backup_{timestamp}{report_path.suffix}"
        
        # Copy original to backup
        with open(report_path, 'r') as f:
            content = f.read()
        
        with open(backup_path, 'w') as f:
            f.write(content)
        
        return backup_path


def _normalize_sbr_groups(val) -> List[str]:
    """Return list of non-empty trimmed strings from sbr_groups (list or comma-separated string)."""
    if val is None:
        return []
    if isinstance(val, list):
        return [str(x).strip() for x in val if str(x).strip()]
    return [x.strip() for x in str(val).split(",") if x.strip()]


def _get_account_for_customer(customer_name: str, report_content: str) -> Optional[str]:
    """Resolve account number from report body (Account: 838043) or from ~/.config/taminator/accounts.json."""
    account, _ = _get_account_and_sbr_groups(customer_name, report_content)
    return account


def _get_account_and_sbr_groups(customer_name: str, report_content: str) -> Tuple[Optional[str], List[str]]:
    """Resolve account number and SBR groups. Returns (account_number, sbr_groups_list)."""
    # From report: **Account:** 838043 or 838043, 1912101
    m = re.search(r'\*\*Account:\*\*\s*([^\n]+)', report_content)
    if m:
        raw = m.group(1).strip()
        first = raw.split(",")[0].strip()
        if re.match(r'^\d+$', first):
            account = first
            _, sbr = _get_account_and_sbr_groups_from_config(customer_name)
            return (account, sbr)
    # From config
    acc, sbr = _get_account_and_sbr_groups_from_config(customer_name)
    if acc is not None:
        return (acc, sbr)
    return (None, [])


def _get_account_and_sbr_groups_from_config(customer_name: str) -> Tuple[Optional[str], List[str]]:
    """Load accounts.json and return (account_number, sbr_groups) for the matching customer."""
    config_dir = Path.home() / ".config" / "taminator"
    accounts_file = config_dir / "accounts.json"
    if not accounts_file.exists():
        return (None, [])
    try:
        with open(accounts_file) as f:
            data = json.load(f)
        for a in data.get("accounts", []):
            aid = (a.get("id") or "").strip().lower()
            cname = (a.get("customer_name") or "").strip().lower()
            if aid == customer_name.lower() or cname == customer_name.lower():
                acc = a.get("account_number") or (a.get("account_numbers") or [None])[0]
                sbr = _normalize_sbr_groups(a.get("sbr_groups"))
                if acc:
                    return (str(acc).strip(), sbr)
                return (None, sbr)
    except Exception:
        pass
    return (None, [])


def _parse_rhcase_list_output(stdout: str) -> List[Tuple[str, str, str, str]]:
    """
    Parse rhcase list output into (case_number, summary, status, jira_id).
    Assumes tab- or space-separated columns; first column digits = case number.
    JIRA ID extracted from summary or a column (see Centralized Jira Project Mapping / JIRA_PROJECT_PREFIXES).
    """
    rows = []
    jira_pat = re.compile(r"(" + JIRA_ID_REGEX_GROUP + ")")
    for line in stdout.splitlines():
        line = line.strip()
        if not line or line.startswith("Case") or line.startswith("---"):
            continue
        parts = re.split(r'\t+|\s{2,}', line, maxsplit=2)
        if len(parts) < 3:
            continue
        case_number = parts[0].strip()
        if not re.match(r'^\d{6,}', case_number):
            continue
        summary = parts[1].strip() if len(parts) > 1 else ""
        rest = parts[2].strip() if len(parts) > 2 else ""
        # Status often third; remainder may be in rest
        sub = re.split(r'\t+|\s{2,}', rest, maxsplit=1)
        status = sub[0].strip() if sub else ""
        jira_match = jira_pat.search(summary) or jira_pat.search(rest)
        jira_id = jira_match.group(1) if jira_match else ""
        rows.append((case_number, summary, status, jira_id))
    return rows


def _classify_rfe_or_bug(summary: str) -> str:
    """Return 'RFE', 'Bug', or 'other' based on summary. Cases with neither (e.g. 04369905) are excluded from RFE/Bug tables."""
    s = (summary or "").lower()
    if "[bug]" in s or " bug:" in s or " bug " in s:
        return "Bug"
    if "[rfe]" in s or " rfe:" in s or " rfe " in s:
        return "RFE"
    return "other"


def _escape_table_cell(s: str) -> str:
    """Escape a cell so it doesn't break markdown table (no | or newlines)."""
    if not s:
        return ""
    return str(s).replace("|", " ").replace("\n", " ").strip()[:200]


# URLs for hyperlinks in reports (JIRA browse URL is from jira_config)
SUPPORT_CASE_URL = "https://access.redhat.com/support/cases/#/case/{case_number}"

# Known support case -> JIRA ID when discovery returns TBD. Add mappings as needed.
CASE_JIRA_OVERRIDES = {
    "04142623": "AAPRFE-875",  # RFE link for case 04142623
}


def _format_jira_cell(jira_id: str) -> str:
    """Format JIRA ID as plain text or markdown link. Links for any known project key (see JIRA_PROJECT_PREFIXES)."""
    if not jira_id or not str(jira_id).strip():
        return "TBD"
    raw = str(jira_id).strip()
    if re.match(r"^(" + JIRA_ID_REGEX_GROUP + r")$", raw, re.IGNORECASE):
        url = jira_config.get_jira_browse_url(raw)
        return f"[{_escape_table_cell(raw)}]({url})"
    return _escape_table_cell(raw)


def _format_case_cell(case_number: str) -> str:
    """Format support case number as markdown link to access.redhat.com."""
    if not case_number or not str(case_number).strip():
        return ""
    raw = str(case_number).strip()
    if re.match(r"^\d{6,}$", raw):
        url = SUPPORT_CASE_URL.format(case_number=raw)
        return f"[{raw}]({url})"
    return _escape_table_cell(raw)


def _inject_rhcase_rows_into_report(content: str, cases: List[Tuple[str, ...]]) -> str:
    """
    Inject case rows into report markdown. cases = (case_number, summary, status, jira_id) or
    (case_number, summary, status, jira_id, kind). External trackers are source of truth: include any
    case that has a JIRA link (from external trackers or elsewhere); prefer kind from external trackers.
    """
    rfe_rows = []
    bug_rows = []
    for case in cases:
        case_number = case[0]
        summary = case[1]
        status = case[2]
        jira_id = (case[3] or "").strip() if len(case) > 3 else ""
        kind = case[4] if len(case) >= 5 else "unknown"
        has_jira = bool(jira_id or CASE_JIRA_OVERRIDES.get((case_number or "").strip()))
        resolved_jira = jira_id or CASE_JIRA_OVERRIDES.get((case_number or "").strip()) or "TBD"
        if not has_jira and kind not in ("RFE", "Bug"):
            continue
        if kind not in ("RFE", "Bug"):
            kind = _classify_rfe_or_bug(summary)
        if kind not in ("RFE", "Bug") and has_jira:
            kind = "RFE"
        if kind not in ("RFE", "Bug"):
            continue
        jira_cell = _format_jira_cell(resolved_jira)
        case_cell = _format_case_cell(case_number)
        row = f"| {jira_cell} | {case_cell} | {_escape_table_cell(summary)} | {_escape_table_cell(status)} |"
        if kind == "Bug":
            bug_rows.append(row)
        else:
            rfe_rows.append(row)

    # Markdown tables require a separator row (|---|---|) after the header to render. 4 columns: JIRA ID | Support Case | Description | Status/Notes
    table_separator = "|-----------------|--------------|-------------|--------------|"
    table_header_line = "| RED HAT JIRA ID | Support Case | Description | Status/Notes |\n"

    # Match both old (5-col: Enhancement Request / Bug Description, Owner) and new (4-col: Description) headers so injection works for existing reports too. First match = RFE, second = Bug.
    table_header = re.compile(
        r'\|\s*RED HAT JIRA ID\s*\|\s*Support Case\s*\|\s*(?:Enhancement Request|Bug Description|Description)\s*\|[^\n]*\n'
        r'([\s\S]*?)(?=\n##|\n---|\n\*\*|\Z)',
        re.IGNORECASE
    )
    placeholder_rfe = "| | | | |\n\n*No RFEs tracked yet. Use Check report / Update report to add RFEs.*"
    placeholder_bug = "| | | | |\n\n*No bugs tracked yet. Use Check report / Update report to add bugs.*"
    tables_done = [0]  # mutable so repl can update

    def table_repl(m):
        if tables_done[0] == 0:
            new_body = "\n".join(rfe_rows) if rfe_rows else placeholder_rfe
            tables_done[0] = 1
        else:
            new_body = "\n".join(bug_rows) if bug_rows else placeholder_bug
        # Always write 4-column header + separator + rows (normalizes old 5-col reports)
        return table_header_line + table_separator + "\n" + new_body + "\n"
    content = table_header.sub(table_repl, content)

    # Always derive summary from final table row counts so the total is correct even if replacement was partial or format changed
    content = _refresh_summary_line_from_content(content)

    return content


def _refresh_summary_line_from_content(content: str) -> str:
    """Count RFE and Bug table data rows in report content and replace the Summary line with accurate counts."""
    # Table data row: starts with |, has multiple |, not a separator line (|---|---|)
    def count_data_rows_until_next_section(rest: str) -> int:
        count = 0
        for line in rest.splitlines():
            line = line.strip()
            if not line or line.startswith("##") or line.startswith("---"):
                break  # end of this table
            if not line.startswith("|") or "|" not in line[1:]:
                break
            if re.match(r"^\|[\s\-:]+\|", line):  # separator row (|---|---|)
                continue
            if re.match(r"^\|\s*(\|\s*)+\|$", line):  # placeholder row (| | | | |)
                continue
            count += 1
        return count

    rfe_count = 0
    bug_count = 0
    lines = content.splitlines()
    i = 0
    table_index = 0  # 0 = RFE, 1 = Bug (both use "Description" header)
    while i < len(lines):
        line = lines[i]
        # Tables: header is RED HAT JIRA ID | Support Case | Description | Status/Notes. First = RFE, second = Bug.
        if "RED HAT JIRA ID" in line and "Description" in line and "|" in line:
            rest = "\n".join(lines[i + 1 :])
            n = count_data_rows_until_next_section(rest)
            if table_index == 0:
                rfe_count = n
                table_index = 1
            else:
                bug_count = n
                break
        i += 1
    total = rfe_count + bug_count
    summary_line = f"Summary: {total} total cases ({rfe_count} RFE, {bug_count} Bug)"
    return re.sub(
        r"Summary:\s*\d+\s+total cases\s*\(\d+\s+RFE,\s*\d+\s+Bug\)",
        summary_line,
        content,
        count=1,
    )


def _try_populate_from_rhcase(customer_name: str, report_path: Path, console, months_back: int = 1) -> bool:
    """
    Try to discover cases via Hydra SOLR API (or rhcase CLI fallback) and populate the report.
    Returns True if report was populated, False otherwise.
    months_back: How many months of modified cases to include (use 12 for full refresh).
    """
    content = report_path.read_text(encoding="utf-8", errors="replace")
    account, sbr_groups = _get_account_and_sbr_groups(customer_name, content)
    if not account:
        console.print("   [dim]No account number found in report or in Report Manager; skipping case discovery.[/dim]")
        return False

    # Hydra: prefer Basic auth (username/password), else Bearer token (Portal or SSO)
    basic_auth = get_basic_auth_from_env()
    hydra_token = None if basic_auth else (get_bearer_token_from_env() or hybrid_auth.get_token("portal", required=False))
    if basic_auth or hydra_token:
        parts = [f"account {account}"]
        if sbr_groups:
            parts.append(f"SBR/product: {', '.join(sbr_groups)}")
        console.print(f"   [dim]Discovering cases via Hydra for {'; '.join(parts)} (last {months_back} month(s))...[/dim]")
        try:
            cases = hydra_discover_cases(
                token=hydra_token,
                account_numbers=[account],
                months_back=months_back,
                include_closed=False,
                products=sbr_groups or None,
                max_rows=500,
                basic_auth=basic_auth,
            )
            if cases:
                console.print(f"   [green]Found {len(cases)} case(s); populating report.[/green]")
                new_content = _inject_rhcase_rows_into_report(content, cases)
                report_path.write_text(new_content, encoding="utf-8")
                return True
        except Exception as e:
            err_str = str(e).strip()
            if "401" in err_str or "Unauthorized" in err_str:
                console.print("   [yellow]Hydra returned Unauthorized. Use a Customer Portal token (Settings) or set REDHAT_USERNAME and REDHAT_PASSWORD in your environment.[/yellow]")
            else:
                console.print(f"   [dim]Hydra search failed: {e}; trying rhcase CLI fallback.[/dim]")

    # Fallback: rhcase CLI (if installed)
    console.print(f"   [dim]Discovering cases via rhcase for account {account} (last {months_back} month(s))...[/dim]")
    try:
        result = subprocess.run(
            ["rhcase", "list", account, "--months", str(months_back)],
            capture_output=True,
            text=True,
            timeout=90,
        )
    except FileNotFoundError:
        console.print("   [dim]rhcase not found (install and configure for Red Hat case discovery).[/dim]")
        return False
    except subprocess.TimeoutExpired:
        console.print("   [dim]rhcase list timed out.[/dim]")
        return False
    if result.returncode != 0:
        console.print(f"   [dim]rhcase list failed: {result.stderr or result.stdout or 'unknown'}[/dim]")
        return False
    # Debug: log what rhcase returned (set TAMINATOR_DEBUG_RHCASE=1)
    if os.environ.get("TAMINATOR_DEBUG_RHCASE"):
        max_len = 2000
        out = (result.stdout or "")[:max_len]
        err = (result.stderr or "")[:max_len]
        if len(result.stdout or "") > max_len:
            out += "... (truncated)"
        if len(result.stderr or "") > max_len:
            err += "... (truncated)"
        print(f"[rhcase] returncode={result.returncode}; stdout={out!r}", file=sys.stderr)
        if result.stderr:
            print(f"[rhcase] stderr={err!r}", file=sys.stderr)
    cases = _parse_rhcase_list_output(result.stdout)
    if not cases:
        console.print("   [dim]No cases parsed from rhcase output.[/dim]")
        return False
    console.print(f"   [green]Found {len(cases)} case(s); populating report.[/green]")
    new_content = _inject_rhcase_rows_into_report(content, cases)
    report_path.write_text(new_content, encoding="utf-8")
    return True


@auth_required([AuthType.VPN, AuthType.JIRA_TOKEN])
def update_customer_report(customer_name: str, auto_confirm: bool = False, full_refresh: bool = False):
    """
    Update customer RFE report with current JIRA statuses.
    
    Args:
        customer_name: Customer name (report slug) or account number (e.g. 838043). If account number, Report Manager must have that account with an id/customer_name so the report file can be found.
        auto_confirm: Skip confirmation prompts (for automation)
        full_refresh: If True, re-discover all cases from portal (Hydra/rhcase) and repopulate the report before updating JIRA statuses.
    """
    customer_name = (customer_name or "").strip()
    resolved = _resolve_customer_arg(customer_name)
    if resolved != customer_name:
        console.print(f"[dim]Resolved account {customer_name} → customer: {resolved}[/dim]")
    customer_name = resolved

    console.print()
    console.print("╔════════════════════════════════════════════════════════════╗", style="cyan bold")
    console.print(f"║  tam-rfe update: {customer_name.upper():^40} ║", style="cyan bold")
    console.print("╚════════════════════════════════════════════════════════════╝", style="cyan bold")
    console.print()

    # Find report file
    console.print(f"🔍 Searching for {customer_name} report...", style="cyan")
    report_path = CustomerReportParser.find_report(customer_name)

    if not report_path:
        console.print(f"\n❌ Report not found for customer: {customer_name}", style="red bold")
        console.print(f"\nSearched in:", style="yellow")
        console.print(f"  • ~/taminator-test-data/{customer_name}.md")
        console.print(f"  • ~/Documents/rh/customers/{customer_name}.md")
        console.print(f"\nTip: Use the customer name (report filename), e.g. tam-rfe update wellsfargo. If you used an account number, add that account in Report Manager with a customer id and create a report for it.", style="dim")
        return
    
    console.print(f"✅ Found report: {report_path}", style="green")
    console.print()
    
    # Full refresh: re-discover cases from portal and repopulate report (then continue to JIRA status update)
    if full_refresh:
        console.print("🔄 Full refresh: re-discovering cases from portal...", style="cyan bold")
        populated = _try_populate_from_rhcase(customer_name, report_path, console, months_back=12)
        if populated:
            console.print("✅ Report repopulated from portal.", style="green")
        else:
            console.print("⚠️  Full refresh could not discover cases (check account, Portal token, and VPN). Continuing with existing report content.", style="yellow")
        console.print()
    
    # Extract JIRA issues from report
    console.print("📋 Parsing report...", style="cyan")
    issues = CustomerReportParser.extract_jira_issues(report_path)
    
    # If report is empty (and we didn't just full-refresh), try to populate from portal with same window as full refresh (12 months) so initial report gets full results
    if not issues:
        populated = _try_populate_from_rhcase(customer_name, report_path, console, months_back=12)
        if populated:
            issues = CustomerReportParser.extract_jira_issues(report_path)
        if not issues:
            console.print("\n⚠️  No case data could be pulled into the report.", style="yellow")
            console.print("   Case discovery was tried (Hydra with Portal token or username/password, then rhcase CLI). Configure a Portal token in Settings or set REDHAT_USERNAME and REDHAT_PASSWORD. Otherwise install rhcase CLI and run Update again.", style="dim")
            return
    
    console.print(f"✅ Found {len(issues)} JIRA issues in report", style="green")
    console.print()
    
    # Fetch current statuses from JIRA (Red Hat Bearer or JIRA Cloud Basic)
    base_url, auth_header, _ = jira_config.get_jira_auth()
    if not auth_header:
        console.print(
            "\n❌ JIRA auth not configured. Set JIRA token (Red Hat) or, for JIRA Cloud, JIRA_EMAIL + JIRA_API_TOKEN (or configure in Settings).",
            style="red bold",
        )
        return
    api_url = jira_config.get_jira_api_url()
    jira_client = JIRAClient(api_base_url=api_url, auth_header=auth_header)
    
    issue_keys = [issue[0] for issue in issues]
    current_statuses = jira_client.get_multiple_statuses(issue_keys)
    
    console.print()
    
    # Check what will change
    changes = []
    for jira_id, reported_status in issues:
        current_info = current_statuses.get(jira_id, {})
        current_status = current_info.get('status', 'UNKNOWN')
        
        if current_status not in ['ERROR', 'NOT_FOUND']:
            if reported_status.strip().lower() != current_status.strip().lower():
                changes.append({
                    'jira_id': jira_id,
                    'old': reported_status,
                    'new': current_status
                })
    
    if not changes:
        console.print("✅ Report is already up-to-date! No changes needed.\n", style="green bold")
        return
    
    # Display proposed changes
    console.print(f"📝 Found {len(changes)} status change(s) to apply:\n", style="cyan bold")
    
    for change in changes:
        console.print(f"  • {change['jira_id']}: ", style="white", end="")
        console.print(f"[yellow]{change['old']}[/yellow] → [green]{change['new']}[/green]")
    
    console.print()
    
    # Confirm update
    if not auto_confirm:
        if not Confirm.ask("Apply these updates to the report?", default=True):
            console.print("\n❌ Update cancelled.\n", style="yellow")
            return
    
    console.print()
    
    # Create backup
    console.print("💾 Creating backup...", style="cyan")
    backup_path = ReportUpdater.create_backup(report_path)
    console.print(f"✅ Backup created: {backup_path}", style="green")
    console.print()
    
    # Update report
    console.print("📝 Updating report...", style="cyan")
    updates_made, new_content = ReportUpdater.update_report_file(report_path, current_statuses)
    
    # Write updated content
    with open(report_path, 'w') as f:
        f.write(new_content)
    
    console.print(f"✅ Report updated successfully!", style="green bold")
    console.print()
    
    # Summary
    summary = f"""
╔═══════════════════════════════════════════════════════════╗
║                    UPDATE SUMMARY                         ║
╚═══════════════════════════════════════════════════════════╝

  File: {report_path.name}
  Updates Applied: {updates_made}
  Backup Location: {backup_path.name}
  
  Status: ✅ SUCCESS

  Your report now reflects current JIRA statuses!
"""
    
    console.print(summary, style="green bold")
    
    # Offer to view diff
    if not auto_confirm:
        if Confirm.ask("View updated report?", default=False):
            console.print("\n" + "="*70 + "\n")
            console.print(new_content)
            console.print("\n" + "="*70 + "\n")


# CLI entry point
def main(customer: str = None, test_data: bool = False, auto_confirm: bool = False, full_refresh: bool = False):
    """Main entry point for tam-rfe update command."""
    
    if test_data:
        # Use test customer
        customer = 'testcustomer'
        console.print("\n🧪 Using test data...\n", style="cyan bold")
    
    if not customer:
        console.print("\n❌ Error: Customer name required", style="red bold")
        console.print("\nUsage:", style="cyan")
        console.print("  tam-rfe update <customer>")
        console.print("  tam-rfe update --test-data")
        console.print("\nExamples:", style="cyan")
        console.print("  tam-rfe update acmecorp")
        console.print("  tam-rfe update testcustomer")
        console.print("  tam-rfe update --test-data")
        return
    
    update_customer_report(customer, auto_confirm=auto_confirm, full_refresh=full_refresh)


if __name__ == '__main__':
    import sys
    
    # Simple argument parsing
    test_data = '--test-data' in sys.argv
    auto_confirm = '--yes' in sys.argv or '-y' in sys.argv
    full_refresh = '--full-refresh' in sys.argv
    
    if test_data:
        main(test_data=True, auto_confirm=auto_confirm, full_refresh=full_refresh)
    elif len(sys.argv) > 1 and not sys.argv[1].startswith('--'):
        main(customer=sys.argv[1], auto_confirm=auto_confirm, full_refresh=full_refresh)
    else:
        main()

