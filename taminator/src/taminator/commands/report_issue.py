"""
tam-rfe report-issue: Submit bug reports or feature requests to Taminator GitHub.

Creates GitHub issues with system information, logs, and screenshots.

Usage:
    tam-rfe report-issue
    tam-rfe report-issue --bug
    tam-rfe report-issue --feature
"""

import os
import sys
import platform
import subprocess
from datetime import datetime
from typing import Dict, Optional

import requests
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.markdown import Markdown

from ..core.hybrid_auth import hybrid_auth
from ..core.auth_box import auth_required, AuthType

console = Console()

# Taminator GitHub repository
GITHUB_REPO_OWNER = "thebyrdman-git"  # Update with actual repo
GITHUB_REPO_NAME = "taminator"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/issues"


class GitHubIssueReporter:
    """Submit issues to GitHub repository."""
    
    @staticmethod
    def collect_system_info() -> Dict[str, str]:
        """Collect system information for bug reports."""
        info = {
            'os': platform.system(),
            'os_version': platform.release(),
            'python_version': platform.python_version(),
            'taminator_version': '2.0.0-alpha',
        }
        
        # Check if in GUI or CLI
        info['interface'] = 'GUI' if os.environ.get('ELECTRON_RUN_AS_NODE') else 'CLI'
        
        # VPN status
        try:
            from ..core.auth_box import auth_box
            vpn_result = auth_box.check_vpn_connection()
            info['vpn_connected'] = 'Yes' if vpn_result.passed else 'No'
        except:
            info['vpn_connected'] = 'Unknown'
        
        # Kerberos status
        try:
            kerb_result = auth_box.check_kerberos_ticket()
            info['kerberos'] = 'Valid' if kerb_result.passed else 'No ticket'
        except:
            info['kerberos'] = 'Unknown'
        
        return info
    
    @staticmethod
    def create_bug_report_template(title: str, description: str, steps: str, expected: str, actual: str, system_info: Dict) -> str:
        """Create bug report issue body."""
        template = f"""## Bug Description

{description}

## Steps to Reproduce

{steps}

## Expected Behavior

{expected}

## Actual Behavior

{actual}

## System Information

- **OS:** {system_info['os']} {system_info['os_version']}
- **Python:** {system_info['python_version']}
- **Taminator:** {system_info['taminator_version']}
- **Interface:** {system_info['interface']}
- **VPN Connected:** {system_info['vpn_connected']}
- **Kerberos:** {system_info['kerberos']}

## Additional Context

_Add any additional context, logs, or screenshots here._

---

*Reported via Taminator Issue Reporter*
"""
        return template
    
    @staticmethod
    def create_feature_request_template(title: str, description: str, use_case: str, alternatives: str) -> str:
        """Create feature request issue body."""
        template = f"""## Feature Description

{description}

## Use Case

{use_case}

## Proposed Solution

_Describe how you envision this feature working._

## Alternatives Considered

{alternatives}

## Additional Context

_Add any mockups, examples, or additional details._

---

*Reported via Taminator Issue Reporter*
"""
        return template
    
    @staticmethod
    def submit_issue(title: str, body: str, labels: list, token: str) -> Optional[str]:
        """
        Submit issue to GitHub.
        
        Args:
            title: Issue title
            body: Issue body (markdown)
            labels: List of labels
            token: GitHub Personal Access Token
        
        Returns:
            Issue URL if successful, None otherwise
        """
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        }
        
        data = {
            'title': title,
            'body': body,
            'labels': labels
        }
        
        try:
            response = requests.post(
                GITHUB_API_URL,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 201:
                issue_data = response.json()
                return issue_data['html_url']
            else:
                console.print(f"\n❌ GitHub API Error: {response.status_code}", style="red bold")
                console.print(f"Response: {response.text[:200]}", style="red")
                return None
                
        except Exception as e:
            console.print(f"\n❌ Error submitting issue: {e}", style="red bold")
            return None


@auth_required([AuthType.GITHUB_TOKEN])
def report_issue_interactive(issue_type: Optional[str] = None):
    """
    Interactive issue reporter.
    
    Args:
        issue_type: 'bug' or 'feature', or None for prompt
    """
    console.print()
    console.print("╔════════════════════════════════════════════════════════════╗", style="cyan bold")
    console.print("║            TAMINATOR ISSUE REPORTER                        ║", style="cyan bold")
    console.print("╚════════════════════════════════════════════════════════════╝", style="cyan bold")
    console.print()
    
    welcome = """
Report bugs or request features for Taminator!

Your issue will be submitted to the Taminator GitHub repository
where the development team can track and address it.

This helps make Taminator better for all TAMs!
"""
    console.print(Panel(welcome, border_style="cyan", title="🐛 Issue Reporter"))
    console.print()
    
    # Determine issue type
    if not issue_type:
        console.print("What type of issue are you reporting?\n", style="cyan bold")
        console.print("  1. 🐛 Bug Report - Something isn't working")
        console.print("  2. ✨ Feature Request - Suggest a new feature")
        console.print()
        
        choice = Prompt.ask(
            "Select issue type",
            choices=['1', '2'],
            default='1'
        )
        
        issue_type = 'bug' if choice == '1' else 'feature'
    
    console.print()
    
    if issue_type == 'bug':
        console.print("═══ Bug Report ═══\n", style="cyan bold")
        
        title = Prompt.ask("Bug title (short summary)")
        
        console.print()
        description = Prompt.ask("Describe the bug")
        
        console.print()
        steps = Prompt.ask("Steps to reproduce", default="1. \n2. \n3. ")
        
        console.print()
        expected = Prompt.ask("What should happen?")
        
        console.print()
        actual = Prompt.ask("What actually happens?")
        
        # Collect system info
        console.print("\n📊 Collecting system information...", style="cyan")
        system_info = GitHubIssueReporter.collect_system_info()
        
        # Create issue body
        issue_body = GitHubIssueReporter.create_bug_report_template(
            title, description, steps, expected, actual, system_info
        )
        
        labels = ['bug']
        
    else:  # feature request
        console.print("═══ Feature Request ═══\n", style="cyan bold")
        
        title = Prompt.ask("Feature title (short summary)")
        
        console.print()
        description = Prompt.ask("Describe the feature you'd like")
        
        console.print()
        use_case = Prompt.ask("What problem does this solve?")
        
        console.print()
        alternatives = Prompt.ask("Have you considered alternatives?", default="None")
        
        # Create issue body
        issue_body = GitHubIssueReporter.create_feature_request_template(
            title, description, use_case, alternatives
        )
        
        labels = ['enhancement']
    
    console.print()
    console.print("═══ Preview ═══\n", style="cyan bold")
    
    preview = f"**Title:** {title}\n\n**Labels:** {', '.join(labels)}\n\n**Body:**\n{issue_body[:300]}..."
    console.print(Panel(preview, border_style="cyan"))
    console.print()
    
    # Confirm submission
    if not Confirm.ask("Submit this issue to GitHub?", default=True):
        console.print("\n❌ Issue submission cancelled.\n", style="yellow")
        return
    
    console.print()
    console.print("📤 Submitting issue to GitHub...", style="cyan")
    
    # Get GitHub token
    github_token = hybrid_auth.get_token('github')
    
    # Submit issue
    issue_url = GitHubIssueReporter.submit_issue(
        title=title,
        body=issue_body,
        labels=labels,
        token=github_token
    )
    
    if issue_url:
        console.print("\n✅ Issue submitted successfully!", style="green bold")
        console.print(f"\nIssue URL: {issue_url}", style="cyan")
        console.print("\nYou can track your issue at the URL above.", style="green")
        console.print("The development team will be notified.\n")
    else:
        console.print("\n❌ Failed to submit issue. Please try again.\n", style="red bold")


# CLI entry point
def main(bug: bool = False, feature: bool = False):
    """Main entry point for tam-rfe report-issue command."""
    
    if bug:
        report_issue_interactive(issue_type='bug')
    elif feature:
        report_issue_interactive(issue_type='feature')
    else:
        # Interactive selection
        report_issue_interactive()


if __name__ == '__main__':
    import sys
    
    bug = '--bug' in sys.argv
    feature = '--feature' in sys.argv
    
    main(bug=bug, feature=feature)

