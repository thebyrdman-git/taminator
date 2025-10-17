"""
rhcase Integration Handler

Provides clean Python interface to rhcase tool for fetching customer case data.
Handles authentication, JSON parsing, and error handling.
"""

import os
import json
import subprocess
import shutil
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta


class RHCaseConfig:
    """rhcase configuration manager"""
    
    def __init__(self):
        self.rhcase_path = self._find_rhcase()
    
    def _find_rhcase(self) -> Optional[Path]:
        """Find rhcase binary"""
        # Try local rhcase first (submodule)
        project_root = Path(__file__).parent.parent
        local_rhcase = project_root / "rhcase" / ".venv" / "bin" / "rhcase"
        
        if local_rhcase.exists():
            return local_rhcase
        
        # Try rhcase in project root
        alt_rhcase = project_root / "rhcase" / "rhcase"
        if alt_rhcase.exists():
            return alt_rhcase
        
        # Try system rhcase
        system_rhcase = shutil.which("rhcase")
        if system_rhcase:
            return Path(system_rhcase)
        
        return None
    
    def is_configured(self) -> bool:
        """Check if rhcase is available"""
        if not self.rhcase_path:
            return False
        
        try:
            result = subprocess.run(
                [str(self.rhcase_path), "--version"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False


class RHCaseHandler:
    """Handler for rhcase tool integration"""
    
    def __init__(self):
        self.config = RHCaseConfig()
    
    def _run_rhcase(self, args: List[str], timeout: int = 30) -> Optional[Dict[str, Any]]:
        """
        Run rhcase command and return JSON output
        
        Args:
            args: Command arguments
            timeout: Command timeout in seconds
        
        Returns:
            Parsed JSON output or None on error
        """
        if not self.config.rhcase_path:
            return None
        
        try:
            # Always request JSON format
            if "--format" not in args and "-f" not in args:
                args.extend(["--format", "json"])
            
            result = subprocess.run(
                [str(self.config.rhcase_path)] + args,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False
            )
            
            if result.returncode != 0:
                return None
            
            if not result.stdout.strip():
                return {"cases": []}
            
            # Parse JSON output
            try:
                data = json.loads(result.stdout)
                return data
            except json.JSONDecodeError:
                # Fallback: try to extract cases from text output
                return self._parse_text_output(result.stdout)
                
        except subprocess.TimeoutExpired:
            print(f"  ⚠️  rhcase command timed out")
            return None
        except Exception as e:
            print(f"  ⚠️  rhcase error: {e}")
            return None
    
    def _parse_text_output(self, output: str) -> Dict[str, Any]:
        """Parse text output as fallback"""
        # Basic text parsing for non-JSON output
        cases = []
        for line in output.split('\n'):
            if line.strip() and 'Case' in line:
                # Try to extract basic info
                # This is a fallback - JSON is preferred
                cases.append({"raw_text": line.strip()})
        return {"cases": cases}
    
    def list_cases(
        self,
        customer: Optional[str] = None,
        status: Optional[str] = None,
        months: int = 6,
        severity: Optional[str] = None
    ) -> List[Dict]:
        """
        List cases for customer
        
        Args:
            customer: Customer name/account (None for all)
            status: Case status ("open", "closed", etc.)
            months: Months of history to fetch
            severity: Filter by severity (1, 2, 3, 4)
        
        Returns:
            List of case dictionaries
        """
        args = ["list"]
        
        if customer:
            args.append(str(customer))
        else:
            args.append("--all")
        
        args.extend(["--months", str(months)])
        
        if status:
            args.extend(["--status", status])
        
        if severity:
            args.extend(["--severity", str(severity)])
        
        result = self._run_rhcase(args)
        if not result:
            return []
        
        # Handle different response formats
        if isinstance(result, list):
            return result
        elif isinstance(result, dict):
            return result.get("cases", result.get("data", []))
        
        return []
    
    def get_case_details(self, case_number: str) -> Optional[Dict]:
        """
        Get detailed information for a specific case
        
        Args:
            case_number: Case number (with or without leading zeros)
        
        Returns:
            Case dictionary or None
        """
        args = ["get", str(case_number)]
        result = self._run_rhcase(args)
        
        if not result:
            return None
        
        # Handle different response formats
        if isinstance(result, dict) and "case" in result:
            return result["case"]
        elif isinstance(result, dict):
            return result
        
        return None
    
    def get_open_cases(self, customer: str) -> List[Dict]:
        """Get open cases for customer"""
        return self.list_cases(customer=customer, status="open", months=6)
    
    def get_closed_cases(self, customer: str, days: int = 30) -> List[Dict]:
        """Get recently closed cases"""
        months = max(1, days // 30)
        all_cases = self.list_cases(customer=customer, months=months)
        
        # Filter for closed cases within the time window
        cutoff_date = datetime.now() - timedelta(days=days)
        closed = []
        
        for case in all_cases:
            status = case.get("status", "").lower()
            if status in ["closed", "resolved", "archived"]:
                # Check close date if available
                close_date_str = case.get("close_date") or case.get("closed_date")
                if close_date_str:
                    try:
                        close_date = datetime.fromisoformat(close_date_str.replace('Z', '+00:00'))
                        if close_date >= cutoff_date:
                            closed.append(case)
                    except Exception:
                        # If we can't parse date, include it anyway
                        closed.append(case)
                else:
                    # No close date, include it
                    closed.append(case)
        
        return closed
    
    def get_customer_accounts(self) -> List[Dict]:
        """
        Get list of customer accounts TAM has access to
        
        Returns:
            List of customer dictionaries with account info
        """
        # Get all cases from last 6 months and extract unique customers
        all_cases = self.list_cases(months=6)
        
        customers = {}
        for case in all_cases:
            account_number = case.get("account_number") or case.get("account")
            account_name = case.get("account_name") or case.get("customer")
            
            if account_number and account_number not in customers:
                customers[account_number] = {
                    "account_number": account_number,
                    "account_name": account_name or "Unknown",
                    "case_count": 0
                }
            
            if account_number:
                customers[account_number]["case_count"] += 1
        
        return list(customers.values())
    
    def get_case_count(self, customer: str, status: Optional[str] = None) -> int:
        """Get count of cases for customer"""
        cases = self.list_cases(customer=customer, status=status, months=6)
        return len(cases)
    
    def search_cases(self, query: str, customer: Optional[str] = None) -> List[Dict]:
        """
        Search cases by keyword
        
        Args:
            query: Search query
            customer: Limit to specific customer (optional)
        
        Returns:
            List of matching cases
        """
        args = ["search", query]
        
        if customer:
            args.extend(["--customer", customer])
        
        result = self._run_rhcase(args)
        if not result:
            return []
        
        if isinstance(result, list):
            return result
        elif isinstance(result, dict):
            return result.get("cases", result.get("results", []))
        
        return []


# Convenience functions
_handler = None

def get_rhcase_handler() -> RHCaseHandler:
    """Get rhcase handler instance"""
    global _handler
    if _handler is None:
        _handler = RHCaseHandler()
    return _handler


def list_cases(customer: Optional[str] = None, status: Optional[str] = None, months: int = 6) -> List[Dict]:
    """List cases (convenience function)"""
    handler = get_rhcase_handler()
    return handler.list_cases(customer, status, months)


def get_open_cases(customer: str) -> List[Dict]:
    """Get open cases for customer (convenience function)"""
    handler = get_rhcase_handler()
    return handler.get_open_cases(customer)


def get_case_details(case_number: str) -> Optional[Dict]:
    """Get case details (convenience function)"""
    handler = get_rhcase_handler()
    return handler.get_case_details(case_number)

