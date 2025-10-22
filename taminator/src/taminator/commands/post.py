"""
tam-rfe post: Post RFE/Bug tracker to Red Hat Customer Portal.

Posts the formatted report to customer portal group page.

Usage:
    tam-rfe post <customer>
    tam-rfe post --dry-run <customer>
"""

from pathlib import Path
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

from ..core.auth_box import auth_box, auth_required, AuthType
from .check import CustomerReportParser

console = Console()


@auth_required([AuthType.VPN, AuthType.PORTAL_TOKEN])
def post_customer_report(customer_name: str, dry_run: bool = False):
    """
    Post customer RFE report to portal.
    
    Args:
        customer_name: Customer name
        dry_run: Preview without posting
    """
    console.print()
    console.print("╔════════════════════════════════════════════════════════════╗", style="cyan bold")
    console.print(f"║  tam-rfe post: {customer_name.upper():^42} ║", style="cyan bold")
    console.print("╚════════════════════════════════════════════════════════════╝", style="cyan bold")
    console.print()
    
    if dry_run:
        console.print("🧪 DRY RUN MODE - No changes will be made\n", style="yellow bold")
    
    # Find report file
    console.print(f"🔍 Searching for {customer_name} report...", style="cyan")
    report_path = CustomerReportParser.find_report(customer_name)
    
    if not report_path:
        console.print(f"\n❌ Report not found for customer: {customer_name}", style="red bold")
        return
    
    console.print(f"✅ Found report: {report_path}", style="green")
    console.print()
    
    # Read report
    with open(report_path, 'r') as f:
        report_content = f.read()
    
    # Preview
    console.print("═══ Report Preview ═══\n", style="cyan bold")
    console.print(Panel(report_content[:500] + "...", border_style="cyan", title="First 500 characters"))
    console.print()
    
    if dry_run:
        console.print("✅ Dry run complete - no changes made\n", style="green")
        console.print("Remove --dry-run flag to post for real\n")
        return
    
    # Confirm posting
    console.print("⚠️  This will post the report to the customer portal", style="yellow bold")
    
    if not Confirm.ask("Proceed with posting?", default=False):
        console.print("\n❌ Posting cancelled.\n", style="yellow")
        return
    
    console.print()
    console.print("📤 Posting to customer portal...", style="cyan")
    
    # TODO: Implement actual portal API posting
    # For now, show what would happen
    console.print("\n🚧 Portal API integration coming soon!", style="yellow bold")
    console.print("\nWhat would happen:", style="cyan")
    console.print(f"  • Connect to Red Hat Customer Portal API")
    console.print(f"  • Locate customer group page for: {customer_name}")
    console.print(f"  • Post report as new article or update existing")
    console.print(f"  • Add timestamp and attribution")
    console.print()
    
    summary = f"""
╔═══════════════════════════════════════════════════════════╗
║                    POST SUMMARY                           ║
╚═══════════════════════════════════════════════════════════╝

  Customer: {customer_name}
  Report: {report_path.name}
  Status: 🚧 API integration pending
  
  The report is ready to post once Portal API is integrated.
"""
    
    console.print(summary, style="yellow bold")


# CLI entry point
def main(customer: str = None, dry_run: bool = False, json_output: bool = False):
    """Main entry point for tam-rfe post command."""
    
    if not customer:
        if json_output:
            import json
            print(json.dumps({
                "success": False,
                "error": "Customer name required",
                "portal_url": "",
                "discussion_id": ""
            }))
        else:
            console.print("\n❌ Error: Customer name required", style="red bold")
            console.print("\nUsage:", style="cyan")
            console.print("  tam-rfe post <customer>")
            console.print("  tam-rfe post --dry-run <customer>")
            console.print("  tam-rfe post --customer <name> --json")
            console.print("\nExamples:", style="cyan")
            console.print("  tam-rfe post acme")
            console.print("  tam-rfe post --dry-run customer123")
            console.print("  tam-rfe post --customer acme --json")
        return
    
    if json_output:
        # JSON mode: Return stub response for now (Portal API not integrated yet)
        import json
        print(json.dumps({
            "success": True,
            "portal_url": f"https://access.redhat.com/discussions/placeholder",
            "discussion_id": "placeholder",
            "preview_mode": dry_run,
            "message": "Portal API integration pending - this is a placeholder response"
        }))
    else:
        post_customer_report(customer, dry_run=dry_run)


if __name__ == '__main__':
    import sys
    
    # Simple argument parsing
    customer_val = None
    json_mode = '--json' in sys.argv
    dry_run_mode = '--dry-run' in sys.argv
    
    # Extract customer name
    if '--customer' in sys.argv:
        idx = sys.argv.index('--customer')
        if idx + 1 < len(sys.argv):
            customer_val = sys.argv[idx + 1]
    else:
        # Get customer name (first non-flag argument)
        for arg in sys.argv[1:]:
            if not arg.startswith('--'):
                customer_val = arg
                break
    
    main(customer=customer_val, dry_run=dry_run_mode, json_output=json_mode)

