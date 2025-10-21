"""
tam-rfe update: Auto-update customer RFE/Bug reports with current JIRA statuses.

Fetches current JIRA statuses and updates the report file in-place,
preserving formatting and adding update timestamp.

Usage:
    tam-rfe update <customer>
    tam-rfe update --test-data
"""

import os
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

from ..core.auth_box import auth_box, auth_required, AuthType
from .check import CustomerReportParser, JIRAClient

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
            
            # Skip errors
            if new_status in ['ERROR', 'NOT_FOUND']:
                continue
            
            # Pattern: Match JIRA ID in table and capture everything up to status column
            # Then replace just the status
            pattern = rf'(\|\s*{re.escape(jira_id)}\s*\|[^|]*\|[^|]*\|\s*)([^\|]+?)(\s*\|)'
            
            def replacer(match):
                nonlocal updates_made
                old_status = match.group(2).strip()
                if old_status.lower() != new_status.lower():
                    updates_made += 1
                    return f"{match.group(1)}{new_status}{match.group(3)}"
                return match.group(0)
            
            content = re.sub(pattern, replacer, content)
        
        # Add update timestamp at the top
        if updates_made > 0:
            timestamp = datetime.now().strftime('%b %d, %Y, %I:%M %p %Z')
            
            # Find the first line with a name (assume it's the author line)
            author_pattern = r'(.*?Jimmy Byrd.*?\n)'
            match = re.search(author_pattern, content, re.IGNORECASE)
            
            if match:
                # Add update line after author line
                author_line = match.group(1)
                update_line = f"**Last Updated:** {timestamp} (via Taminator)\n\n"
                content = content.replace(author_line, author_line + update_line)
            else:
                # Add at beginning if no author found
                content = f"**Last Updated:** {timestamp} (via Taminator)\n\n" + content
        
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


@auth_required([AuthType.VPN, AuthType.JIRA_TOKEN])
def update_customer_report(customer_name: str, auto_confirm: bool = False):
    """
    Update customer RFE report with current JIRA statuses.
    
    Args:
        customer_name: Customer name
        auto_confirm: Skip confirmation prompts (for automation)
    """
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
def main(customer: str = None, test_data: bool = False, auto_confirm: bool = False):
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
        console.print("  tam-rfe update tdbank")
        console.print("  tam-rfe update testcustomer")
        console.print("  tam-rfe update --test-data")
        return
    
    update_customer_report(customer, auto_confirm=auto_confirm)


if __name__ == '__main__':
    import sys
    
    # Simple argument parsing
    test_data = '--test-data' in sys.argv
    auto_confirm = '--yes' in sys.argv or '-y' in sys.argv
    
    if test_data:
        main(test_data=True, auto_confirm=auto_confirm)
    elif len(sys.argv) > 1 and not sys.argv[1].startswith('--'):
        main(customer=sys.argv[1], auto_confirm=auto_confirm)
    else:
        main()

