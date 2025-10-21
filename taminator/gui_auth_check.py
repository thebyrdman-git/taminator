#!/usr/bin/env python3
"""
Lightweight auth check for Taminator GUI.
Returns JSON status without any interactive prompts or hanging.
"""

import sys
import json
sys.path.insert(0, 'src')

def check_auth_status():
    """Quick, non-interactive auth status check."""
    try:
        from taminator.core.auth_box import AuthBox
        
        auth_box = AuthBox()
        
        # Check VPN (quick check, no prompts)
        vpn_result = auth_box.check_vpn_connection()
        
        # Check Kerberos (quick check, no prompts)
        kerberos_result = auth_box.check_kerberos_ticket()
        
        # Check tokens (no prompts, just check if they exist)
        from taminator.core.auth_types import AuthType
        jira_token = auth_box.get_token(AuthType.JIRA_TOKEN, required=False) is not None
        portal_token = auth_box.get_token(AuthType.PORTAL_TOKEN, required=False) is not None
        
        result = {
            'vpn': vpn_result['passed'] if isinstance(vpn_result, dict) else vpn_result.passed,
            'kerberos': kerberos_result['passed'] if isinstance(kerberos_result, dict) else kerberos_result.passed,
            'jira_token': jira_token,
            'portal_token': portal_token
        }
        
        print(json.dumps(result))
        return 0
        
    except Exception as e:
        # On any error, return all false
        print(json.dumps({
            'vpn': False,
            'kerberos': False,
            'jira_token': False,
            'portal_token': False,
            'error': str(e)
        }))
        return 1

if __name__ == "__main__":
    sys.exit(check_auth_status())

