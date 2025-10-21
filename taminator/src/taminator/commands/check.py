"""
tam-rfe check: Verify customer RFE/Bug reports are up-to-date.

Compares report JIRA statuses with current JIRA data and displays
beautiful comparison tables.

Usage:
    tam-rfe check <customer>
    tam-rfe check --test-data
"""

import os
import re
from typing import Dict, List, Tuple, Optional
from pathlib import Path

import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..core.auth_box import auth_box, auth_required, AuthType
from ..core.auth_types import AUTH_REQUIREMENTS

console = Console()


class JIRAClient:
    """Simple JIRA API client for fetching issue statuses."""
    
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://issues.redhat.com/rest/api/2"
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
    
    def get_issue_status(self, issue_key: str) -> Optional[Dict]:
        """
        Fetch issue status from JIRA.
        
        Args:
            issue_key: JIRA issue key (e.g., AAPRFE-762)
        
        Returns:
            Dictionary with issue details or None if not found
        """
        try:
            response = requests.get(
                f'{self.base_url}/issue/{issue_key}',
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                assignee_obj = data['fields'].get('assignee')
                assignee_name = assignee_obj.get('displayName', 'Unassigned') if assignee_obj else 'Unassigned'
                
                return {
                    'key': issue_key,
                    'status': data['fields']['status']['name'],
                    'summary': data['fields']['summary'],
                    'assignee': assignee_name,
                    'updated': data['fields']['updated']
                }
            elif response.status_code == 404:
                return {
                    'key': issue_key,
                    'status': 'NOT_FOUND',
                    'error': 'Issue not found'
                }
            else:
                return {
                    'key': issue_key,
                    'status': 'ERROR',
                    'error': f'HTTP {response.status_code}'
                }
        except Exception as e:
            return {
                'key': issue_key,
                'status': 'ERROR',
                'error': str(e)
            }
    
    def get_multiple_statuses(self, issue_keys: List[str]) -> Dict[str, Dict]:
        """
        Fetch statuses for multiple issues.
        
        Args:
            issue_keys: List of JIRA issue keys
        
        Returns:
            Dictionary mapping issue key to status info
        """
        results = {}
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task(f"Fetching JIRA statuses for {len(issue_keys)} issues...", total=len(issue_keys))
            
            for issue_key in issue_keys:
                results[issue_key] = self.get_issue_status(issue_key)
                progress.advance(task)
        
        return results


class CustomerReportParser:
    """Parse customer RFE/Bug report markdown files."""
    
    @staticmethod
    def find_report(customer_name: str) -> Optional[Path]:
        """
        Find customer report file.
        
        Args:
            customer_name: Customer name
        
        Returns:
            Path to report file or None
        """
        # Search in common locations
        search_paths = [
            Path.home() / 'taminator-test-data',
            Path.home() / 'Documents' / 'rh' / 'customers',
            Path('/tmp/taminator-test-data'),
        ]
        
        for base_path in search_paths:
            if base_path.exists():
                # Try exact match
                report_file = base_path / f'{customer_name}.md'
                if report_file.exists():
                    return report_file
                
                # Try case-insensitive search
                for file in base_path.glob('*.md'):
                    if customer_name.lower() in file.stem.lower():
                        return file
        
        return None
    
    @staticmethod
    def extract_jira_issues(report_path: Path) -> List[Tuple[str, str]]:
        """
        Extract JIRA issue IDs and their statuses from report.
        
        Args:
            report_path: Path to markdown report
        
        Returns:
            List of tuples: (jira_id, reported_status)
        """
        issues = []
        
        with open(report_path, 'r') as f:
            content = f.read()
        
        # Match JIRA IDs in markdown tables
        # Format: | AAPRFE-762 | ... | Status Name | ...
        # Also match: AAPRFE-762	03666005	[RFE] ... Backlog
        
        patterns = [
            # Markdown table format
            r'\|\s*(AAP(?:RFE)?-\d+)\s*\|[^|]*\|[^|]*\|\s*([^\|]+?)\s*\|',
            # Tab-separated format
            r'(AAP(?:RFE)?-\d+)\s+\d+\s+.*?\s+(\w+)\s*$',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                jira_id = match.group(1).strip()
                status = match.group(2).strip()
                issues.append((jira_id, status))
        
        # Remove duplicates while preserving order
        seen = set()
        unique_issues = []
        for issue in issues:
            if issue[0] not in seen:
                seen.add(issue[0])
                unique_issues.append(issue)
        
        return unique_issues


@auth_required([AuthType.VPN, AuthType.JIRA_TOKEN])
def check_customer_report(customer_name: str):
    """
    Check if customer RFE report is up-to-date.
    
    Args:
        customer_name: Customer name
    """
    console.print()
    console.print("╔════════════════════════════════════════════════════════════╗", style="cyan bold")
    console.print(f"║  tam-rfe check: {customer_name.upper():^42} ║", style="cyan bold")
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
        console.print(f"\nTip: Use --test-data flag to test with sample data", style="cyan")
        return
    
    console.print(f"✅ Found report: {report_path}", style="green")
    console.print()
    
    # Extract JIRA issues from report
    console.print("📋 Parsing report...", style="cyan")
    issues = CustomerReportParser.extract_jira_issues(report_path)
    
    if not issues:
        console.print("\n⚠️  No JIRA issues found in report", style="yellow")
        return
    
    console.print(f"✅ Found {len(issues)} JIRA issues in report", style="green")
    console.print()
    
    # Fetch current statuses from JIRA
    jira_token = auth_box.get_token(AuthType.JIRA_TOKEN)
    jira_client = JIRAClient(jira_token)
    
    issue_keys = [issue[0] for issue in issues]
    current_statuses = jira_client.get_multiple_statuses(issue_keys)
    
    console.print()
    
    # Compare and display results
    display_comparison_table(issues, current_statuses)
    
    # Summary
    display_summary(issues, current_statuses)


def display_comparison_table(report_issues: List[Tuple[str, str]], current_statuses: Dict[str, Dict]):
    """Display beautiful comparison table."""
    
    table = Table(
        title="📊 RFE/Bug Status Comparison",
        show_header=True,
        header_style="bold cyan",
        title_style="bold cyan"
    )
    
    table.add_column("JIRA ID", style="cyan", width=15)
    table.add_column("Report Status", style="white", width=18)
    table.add_column("Current Status", style="white", width=18)
    table.add_column("Match", style="white", width=10, justify="center")
    table.add_column("Notes", style="white", width=25)
    
    for jira_id, reported_status in report_issues:
        current_info = current_statuses.get(jira_id, {})
        current_status = current_info.get('status', 'UNKNOWN')
        
        # Normalize statuses for comparison
        reported_normalized = reported_status.strip().lower()
        current_normalized = current_status.strip().lower()
        
        if current_status == 'ERROR':
            match_icon = "⚠️"
            match_style = "yellow"
            notes = current_info.get('error', 'API error')
        elif current_status == 'NOT_FOUND':
            match_icon = "❌"
            match_style = "red"
            notes = "Issue not found"
        elif reported_normalized == current_normalized:
            match_icon = "✅"
            match_style = "green"
            notes = "Up-to-date"
        else:
            match_icon = "🔄"
            match_style = "yellow"
            notes = "Status changed"
        
        table.add_row(
            jira_id,
            reported_status,
            current_status,
            f"[{match_style}]{match_icon}[/{match_style}]",
            notes
        )
    
    console.print(table)
    console.print()


def display_summary(report_issues: List[Tuple[str, str]], current_statuses: Dict[str, Dict]):
    """Display summary of check results."""
    
    total = len(report_issues)
    up_to_date = 0
    changed = 0
    errors = 0
    
    for jira_id, reported_status in report_issues:
        current_info = current_statuses.get(jira_id, {})
        current_status = current_info.get('status', 'UNKNOWN')
        
        if current_status in ['ERROR', 'NOT_FOUND']:
            errors += 1
        elif reported_status.strip().lower() == current_status.strip().lower():
            up_to_date += 1
        else:
            changed += 1
    
    # Build summary text
    summary = f"""
╔═══════════════════════════════════════════════════════════╗
║                      CHECK SUMMARY                        ║
╚═══════════════════════════════════════════════════════════╝

  Total Issues: {total}
  ✅ Up-to-date: {up_to_date}
  🔄 Changed: {changed}
  ⚠️  Errors: {errors}

"""
    
    if changed == 0 and errors == 0:
        summary += "  Overall Status: ✅ ALL UP-TO-DATE\n"
        summary += "\n  Your report matches current JIRA statuses!\n"
        style = "green bold"
    elif changed > 0 and errors == 0:
        summary += "  Overall Status: 🔄 UPDATE NEEDED\n"
        summary += f"\n  {changed} issue(s) have different statuses.\n"
        summary += "  Run 'tam-rfe update <customer>' to update your report.\n"
        style = "yellow bold"
    else:
        summary += "  Overall Status: ⚠️  ISSUES DETECTED\n"
        summary += f"\n  {errors} issue(s) could not be verified.\n"
        style = "yellow bold"
    
    console.print(summary, style=style)


def create_test_data():
    """Create test customer data for demonstration."""
    test_dir = Path.home() / 'taminator-test-data'
    test_dir.mkdir(exist_ok=True)
    
    test_report = test_dir / 'testcustomer.md'
    
    # Create sample report with real JIRA IDs (that we can verify)
    content = """# Test Customer RFE/Bug Tracker

Oct 21, 2025, 10:51 AM EDT Jimmy Byrd

Summary: 5 total cases (3 RFE, 2 Bug)

## Enhancement Requests (RFE)

| RED HAT JIRA ID | Support Case | Enhancement Request | Status |
|-----------------|--------------|---------------------|--------|
| AAPRFE-762 | 03666005 | [RFE] Add a method for monitoring uwsgi workers in Controller | Backlog |
| AAPRFE-430 | 03666015 | [RFE] Make the mesh aware of which execution node can reach which managed nodes | Backlog |
| AAPRFE-1158 | 03745841 | [RFE] Request to not have invalid variable names imported into AAP | Review |

## Bug Reports

| RED HAT JIRA ID | Support Case | Bug Description | Status |
|-----------------|--------------|-----------------|--------|
| AAP-53458 | 04244831 | [BUG] OIDC Group Claim Misinterpretation in AAP 2.5 | New |
| AAP-45405 | 04134770 | [BUG] Unable to enter multi-line default survey answer in AAP 2.5 Controller UI | Closed |
"""
    
    with open(test_report, 'w') as f:
        f.write(content)
    
    console.print(f"✅ Created test data: {test_report}", style="green")
    return test_report


# CLI entry point
def main(customer: str = None, test_data: bool = False):
    """Main entry point for tam-rfe check command."""
    
    if test_data:
        console.print("\n🧪 Creating test data...\n", style="cyan bold")
        create_test_data()
        customer = 'testcustomer'
    
    if not customer:
        console.print("\n❌ Error: Customer name required", style="red bold")
        console.print("\nUsage:", style="cyan")
        console.print("  tam-rfe check <customer>")
        console.print("  tam-rfe check --test-data")
        console.print("\nExamples:", style="cyan")
        console.print("  tam-rfe check tdbank")
        console.print("  tam-rfe check testcustomer")
        console.print("  tam-rfe check --test-data  # Use sample data")
        return
    
    check_customer_report(customer)


if __name__ == '__main__':
    import sys
    
    # Simple argument parsing
    if '--test-data' in sys.argv:
        main(test_data=True)
    elif len(sys.argv) > 1:
        main(customer=sys.argv[1])
    else:
        main()

