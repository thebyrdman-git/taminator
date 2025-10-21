#!/usr/bin/env python3
"""
Test the Auth-Box comprehensive audit system.
"""

import sys
sys.path.insert(0, 'src')

from taminator.core.auth_audit import run_auth_audit

if __name__ == '__main__':
    print("\n🔐 Running Auth-Box Comprehensive Audit...\n")
    results = run_auth_audit()
    print("\n✅ Audit complete! Results saved to audit log.\n")

