#!/usr/bin/env python3
"""
Taminator CLI - Command Line Interface Router

Routes CLI commands to appropriate command modules.

Usage:
    tam-rfe check <customer>
    tam-rfe update <customer>
    tam-rfe post <customer>
    tam-rfe onboard <customer>
    tam-rfe config [options]
"""

import sys
import argparse
from pathlib import Path


def main():
    """Main CLI entry point."""
    
    parser = argparse.ArgumentParser(
        prog='tam-rfe',
        description='Taminator RFE Tool - TAM workflow automation for tracking RFEs and Bugs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  tam-rfe check acmecorp            Check Acme Corp report status
  tam-rfe update exampleinc         Update Example Inc report
  tam-rfe post bigcustomer          Post Big Customer report to portal
  tam-rfe onboard newcustomer       Onboard new customer
  tam-rfe config --add-token        Add authentication token

For more help on a command:
  tam-rfe <command> --help
        """
    )
    
    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands',
        required=True
    )
    
    # ========================================
    # CHECK command
    # ========================================
    check_parser = subparsers.add_parser(
        'check',
        help='Check customer RFE/Bug report status',
        description='Compare report JIRA statuses with current JIRA data'
    )
    check_parser.add_argument(
        'customer',
        nargs='?',
        help='Customer name (e.g., acmecorp, exampleinc)'
    )
    check_parser.add_argument(
        '--test-data',
        action='store_true',
        help='Use sample test data instead of real customer'
    )
    
    # ========================================
    # UPDATE command
    # ========================================
    update_parser = subparsers.add_parser(
        'update',
        help='Update customer RFE/Bug report with current JIRA statuses',
        description='Auto-update report file with current JIRA data'
    )
    update_parser.add_argument(
        'customer',
        nargs='?',
        help='Customer name'
    )
    update_parser.add_argument(
        '--test-data',
        action='store_true',
        help='Use sample test data'
    )
    update_parser.add_argument(
        '--auto-confirm',
        action='store_true',
        help='Skip confirmation prompts'
    )
    
    # ========================================
    # POST command
    # ========================================
    post_parser = subparsers.add_parser(
        'post',
        help='Post RFE/Bug report to Red Hat Customer Portal',
        description='Upload report to customer portal group page'
    )
    post_parser.add_argument(
        'customer',
        nargs='?',
        help='Customer name'
    )
    post_parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview without actually posting'
    )
    
    # ========================================
    # ONBOARD command
    # ========================================
    onboard_parser = subparsers.add_parser(
        'onboard',
        help='Onboard new customer',
        description='Interactive wizard to set up new customer'
    )
    onboard_parser.add_argument(
        'customer',
        nargs='?',
        help='Customer name'
    )
    onboard_parser.add_argument(
        '--discover',
        metavar='NAME',
        help='Auto-discover customer information'
    )
    onboard_parser.add_argument(
        '--generate',
        action='store_true',
        help='Generate customer configuration'
    )
    
    # ========================================
    # CONFIG command
    # ========================================
    config_parser = subparsers.add_parser(
        'config',
        help='Manage Taminator configuration',
        description='Configure authentication tokens and settings'
    )
    config_parser.add_argument(
        '--add-token',
        action='store_true',
        help='Add authentication token interactively'
    )
    config_parser.add_argument(
        '--test-tokens',
        action='store_true',
        help='Test all configured tokens'
    )
    config_parser.add_argument(
        '--show-tokens',
        action='store_true',
        help='Show configured token types'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Route to appropriate command
    try:
        if args.command == 'check':
            from taminator.commands.check import main as check_main
            check_main(
                customer=args.customer,
                test_data=args.test_data
            )
        
        elif args.command == 'update':
            from taminator.commands.update import main as update_main
            update_main(
                customer=args.customer,
                test_data=args.test_data,
                auto_confirm=args.auto_confirm
            )
        
        elif args.command == 'post':
            from taminator.commands.post import main as post_main
            post_main(
                customer=args.customer,
                dry_run=args.dry_run
            )
        
        elif args.command == 'onboard':
            from taminator.commands.onboard import main as onboard_main
            
            # Handle special flags
            if args.discover:
                # Discovery mode - pass discover name as customer
                onboard_main(customer=args.discover)
            elif args.generate:
                # Generate mode - need to implement this feature
                from rich.console import Console
                console = Console()
                console.print("\n⚠️  --generate flag not yet implemented", style="yellow bold")
                console.print("Use: tam-rfe onboard <customer>  (interactive wizard)\n")
                sys.exit(1)
            else:
                # Normal onboarding
                onboard_main(customer=args.customer)
        
        elif args.command == 'config':
            from taminator.commands.config import main as config_main
            config_main(
                add_token=args.add_token,
                test_tokens=args.test_tokens,
                show_tokens=args.show_tokens
            )
        
        else:
            parser.print_help()
            sys.exit(1)
    
    except KeyboardInterrupt:
        from rich.console import Console
        console = Console()
        console.print("\n\n⚠️  Operation cancelled by user", style="yellow")
        sys.exit(130)
    
    except Exception as e:
        from rich.console import Console
        console = Console()
        console.print(f"\n❌ Error: {str(e)}", style="red bold")
        
        # Show traceback in debug mode
        if '--debug' in sys.argv:
            import traceback
            console.print("\n[red]Traceback:[/red]")
            console.print(traceback.format_exc())
        
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main())

