"""
tam-rfe onboard: Interactive customer onboarding wizard.

Guides TAM through onboarding a new customer:
1. Customer information collection
2. Initial RFE/Bug discovery
3. Report template creation
4. Configuration setup

Usage:
    tam-rfe onboard <customer>
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, List

from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel

from ..core.hybrid_auth import hybrid_auth
from ..core.auth_box import auth_required, AuthType

console = Console()


class CustomerOnboarder:
    """Customer onboarding wizard."""
    
    @staticmethod
    def create_customer_report_template(customer_name: str, customer_info: Dict) -> str:
        """
        Create initial report template for customer.
        
        Args:
            customer_name: Customer name
            customer_info: Dictionary with customer details
        
        Returns:
            Report markdown content
        """
        timestamp = datetime.now().strftime('%b %d, %Y, %I:%M %p %Z')
        
        tam_name = (customer_info.get('tam') or '').strip() or 'TAM'
        template = f"""# {customer_info.get('display_name', customer_name)} RFE/Bug Tracker

{timestamp} {tam_name}

Summary: 0 total cases (0 RFE, 0 Bug)

## Customer Information

- **Account:** {customer_info.get('account', 'TBD')}
- **Primary Contact:** {customer_info.get('contact', 'TBD')}
- **TAM:** {tam_name}

## Enhancement Requests (RFE)

| RED HAT JIRA ID | Support Case | Description | Status/Notes |
|-----------------|--------------|-------------|--------------|
| | | | |

*No RFEs tracked yet. Use `tam-rfe update {customer_name}` to add RFEs.*

## Bug Reports

| RED HAT JIRA ID | Support Case | Description | Status/Notes |
|-----------------|--------------|-------------|--------------|
| | | | |

*No bugs tracked yet. Use `tam-rfe update {customer_name}` to add bugs.*

---

**Notes:**
- This tracker is automatically updated via Taminator
- Last check: {timestamp}
- For questions, see https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues
"""
        return template


@auth_required([AuthType.VPN])
def onboard_customer(customer_name: str):
    """
    Interactive customer onboarding wizard.
    
    Args:
        customer_name: Customer name (slug format, e.g., 'acmecorp')
    """
    console.print()
    console.print("╔════════════════════════════════════════════════════════════╗", style="cyan bold")
    console.print("║          CUSTOMER ONBOARDING WIZARD                        ║", style="cyan bold")
    console.print("╚════════════════════════════════════════════════════════════╝", style="cyan bold")
    console.print()
    
    welcome = f"""
Welcome to the Taminator Customer Onboarding Wizard!

This wizard will help you set up RFE/Bug tracking for:
  {customer_name}

We'll collect some information and create an initial tracking report.
"""
    console.print(Panel(welcome, border_style="cyan", title="🎯 Getting Started"))
    console.print()
    
    if not Confirm.ask("Ready to begin?", default=True):
        console.print("\n❌ Onboarding cancelled.\n", style="yellow")
        return
    
    console.print()
    console.print("═══ Step 1: Customer Information ═══\n", style="cyan bold")
    
    # Collect customer information
    customer_info = {}
    
    customer_info['display_name'] = Prompt.ask(
        "Customer display name",
        default=customer_name.replace('_', ' ').title()
    )
    
    customer_info['account'] = Prompt.ask(
        "Red Hat account number",
        default="TBD"
    )
    
    customer_info['contact'] = Prompt.ask(
        "Primary contact name",
        default="TBD"
    )
    
    customer_info['tam'] = Prompt.ask(
        "TAM name",
        default="TAM"
    )
    
    console.print()
    console.print("═══ Step 2: Report Location ═══\n", style="cyan bold")
    
    # Determine report location
    default_dir = Path.home() / 'taminator-test-data'
    
    console.print(f"Default location: {default_dir}/", style="dim")
    
    use_default = Confirm.ask("Use default location?", default=True)
    
    if use_default:
        report_dir = default_dir
    else:
        custom_path = Prompt.ask("Enter directory path")
        report_dir = Path(custom_path).expanduser()
    
    # Ensure directory exists
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = report_dir / f"{customer_name}.md"
    
    # Check if report already exists
    if report_path.exists():
        console.print(f"\n⚠️  Report already exists: {report_path}", style="yellow")
        if not Confirm.ask("Overwrite existing report?", default=False):
            console.print("\n❌ Onboarding cancelled.\n", style="yellow")
            return
    
    console.print()
    console.print("═══ Step 3: Create Report ═══\n", style="cyan bold")
    
    # Create report template
    console.print("📝 Generating report template...", style="cyan")
    report_content = CustomerOnboarder.create_customer_report_template(
        customer_name,
        customer_info
    )
    
    # Write report
    with open(report_path, 'w') as f:
        f.write(report_content)
    
    console.print(f"✅ Report created: {report_path}", style="green")
    console.print()
    
    # Summary
    summary = f"""
╔═══════════════════════════════════════════════════════════╗
║                  ONBOARDING COMPLETE                      ║
╚═══════════════════════════════════════════════════════════╝

  Customer: {customer_info['display_name']}
  Report: {report_path.name}
  Location: {report_dir}/
  
  Status: ✅ SUCCESS

Next Steps:
  1. Review the report: {report_path}
  2. Add JIRA IDs to the tables manually
  3. Run: tam-rfe check {customer_name}
  4. Run: tam-rfe update {customer_name}

Need help?
  • Documentation / issues: https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues
"""
    
    console.print(summary, style="green bold")
    
    # Offer to open report
    if Confirm.ask("View the new report now?", default=True):
        console.print("\n" + "="*70 + "\n")
        console.print(report_content)
        console.print("\n" + "="*70 + "\n")


# CLI entry point
def main(customer: str = None):
    """Main entry point for tam-rfe onboard command."""
    
    if not customer:
        console.print("\n❌ Error: Customer name required", style="red bold")
        console.print("\nUsage:", style="cyan")
        console.print("  tam-rfe onboard <customer>")
        console.print("\nExamples:", style="cyan")
        console.print("  tam-rfe onboard acmecorp")
        console.print("  tam-rfe onboard exampleinc")
        console.print("\nCustomer name should be:")
        console.print("  • Lowercase")
        console.print("  • No spaces (use underscores)")
        console.print("  • Example: 'acme_corp' or 'acmecorp'")
        return
    
    onboard_customer(customer)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        main(customer=sys.argv[1])
    else:
        main()

