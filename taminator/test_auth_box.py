#!/usr/bin/env python3
"""
Quick test script for Auth-Box functionality.
Run without VPN to test VPN detection.
"""

import sys
sys.path.insert(0, 'src')

from taminator.core.auth_box import auth_box, auth_required, AuthType
from taminator.core.auth_types import AUTH_REQUIREMENTS
from rich.console import Console

console = Console()

def test_vpn_detection():
    """Test VPN connection detection."""
    console.print("\n=== Testing VPN Detection ===\n", style="bold blue")
    
    result = auth_box.check_vpn_connection()
    
    console.print(f"Auth Type: {result.auth_type.value}")
    console.print(f"Status: {result.status.value}")
    console.print(f"Passed: {result.passed}")
    if result.details:
        console.print(f"Details: {result.details}")
    if result.error:
        console.print(f"Error: {result.error}", style="red")


def test_kerberos_check():
    """Test Kerberos ticket check."""
    console.print("\n=== Testing Kerberos Check ===\n", style="bold blue")
    
    result = auth_box.check_kerberos_ticket()
    
    console.print(f"Auth Type: {result.auth_type.value}")
    console.print(f"Status: {result.status.value}")
    console.print(f"Passed: {result.passed}")
    if result.details:
        console.print(f"Details: {result.details}")
    if result.error:
        console.print(f"Error: {result.error}", style="red")


def test_token_management():
    """Test token storage and retrieval."""
    console.print("\n=== Testing Token Management ===\n", style="bold blue")
    
    # Try to get JIRA token (should fail gracefully)
    token = auth_box.get_token(AuthType.JIRA_TOKEN, required=False)
    
    if token:
        console.print(f"✅ JIRA token found: {token[:10]}...", style="green")
    else:
        console.print("ℹ️  JIRA token not configured (expected)", style="yellow")


@auth_required([AuthType.VPN, AuthType.JIRA_TOKEN])
def test_decorated_command():
    """Test command with auth_required decorator."""
    console.print("\n✅ This message only appears if auth passed!", style="green bold")
    console.print("Command executed successfully.")


def main():
    """Run all tests."""
    console.print("\n╭─────────────────────────────────────────╮", style="cyan")
    console.print("│  Auth-Box Test Suite                   │", style="cyan")
    console.print("╰─────────────────────────────────────────╯", style="cyan")
    
    # Test 1: VPN Detection
    test_vpn_detection()
    
    # Test 2: Kerberos Check
    test_kerberos_check()
    
    # Test 3: Token Management
    test_token_management()
    
    # Test 4: Pre-Flight Check (will fail without auth)
    console.print("\n=== Testing Pre-Flight Check ===\n", style="bold blue")
    console.print("This will demonstrate error handling when auth is missing...\n")
    
    try:
        test_decorated_command()
    except Exception as e:
        console.print(f"\n✅ Auth-Box correctly blocked command: {type(e).__name__}", style="green")
    
    console.print("\n" + "="*60)
    console.print("Auth-Box Test Complete!", style="bold green")
    console.print("="*60 + "\n")


if __name__ == "__main__":
    main()

