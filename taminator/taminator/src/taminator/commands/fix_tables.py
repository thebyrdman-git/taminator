#!/usr/bin/env python3
"""
tam-rfe fix-tables: One-time fix for report markdown tables.

Scans all report files in the library paths and inserts the required
separator row (|---|---|) after each RFE and Bug table header if missing,
so tables render correctly in markdown viewers.
"""

import re
from pathlib import Path
from typing import Tuple

from rich.console import Console

# Same search paths as CustomerReportParser and web server
REPORT_SEARCH_PATHS = [
    Path.home() / "taminator-test-data",
    Path.home() / "Documents" / "rh" / "customers",
    Path("/tmp/taminator-test-data"),
]

TABLE_SEPARATOR = "|-----------------|--------------|-------------|--------------|"


def _needs_separator_after(line: str) -> bool:
    """True if this line is a table header that must be followed by a separator."""
    if not line.strip().startswith("|") or "|" not in line[1:]:
        return False
    # Separator row (|---|---|) should not be considered a header
    if re.match(r"^\|\s*[\-\s:]+\|", line.strip()):
        return False
    return "RED HAT JIRA ID" in line and "Description" in line


def _is_separator_line(line: str) -> bool:
    """True if line is a markdown table separator (|---|---|)."""
    s = line.strip()
    if not s.startswith("|") or not s.endswith("|"):
        return False
    # Content between pipes should be only dashes, spaces, colons
    return bool(re.match(r"^\|[\s\-:|]+\|$", s))


def fix_tables_in_content(content: str) -> Tuple[str, int]:
    """
    Insert missing separator row after RFE/Bug table headers. Returns (new_content, number_of_insertions).
    """
    insertions = 0
    lines = content.splitlines()
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        result.append(line)
        if _needs_separator_after(line) and i + 1 < len(lines):
            next_line = lines[i + 1]
            if not _is_separator_line(next_line):
                result.append(TABLE_SEPARATOR)
                insertions += 1
        i += 1
    return "\n".join(result) + ("\n" if content.endswith("\n") else ""), insertions


def fix_all_reports(dry_run: bool = False) -> None:
    """Scan library paths for .md reports and fix table markup in each."""
    console = Console()
    seen = set()  # (parent_name, filename) to dedupe
    total_files = 0
    total_insertions = 0

    for base in REPORT_SEARCH_PATHS:
        base = base.expanduser().resolve()
        if not base.exists():
            continue
        for path in base.glob("*.md"):
            path = path.resolve()
            key = str(path)
            if key in seen:
                continue
            seen.add(key)
            total_files += 1
            try:
                content = path.read_text(encoding="utf-8", errors="replace")
            except Exception as e:
                console.print(f"  [red]Skip {path.name}: {e}[/red]")
                continue
            new_content, insertions = fix_tables_in_content(content)
            if insertions > 0:
                total_insertions += insertions
                if dry_run:
                    console.print(f"  [dim]Would fix {path.name} ({insertions} separator(s) added)[/dim]")
                else:
                    path.write_text(new_content, encoding="utf-8")
                    console.print(f"  [green]Fixed {path.name} ({insertions} separator(s) added)[/green]")
    if total_files == 0:
        console.print("[yellow]No report files found in library paths.[/yellow]")
        return
    if dry_run:
        console.print(f"\n[dim]Would fix {total_insertions} table(s) in {total_files} file(s). Run without --dry-run to apply.[/dim]")
    else:
        console.print(f"\n[green]Done. Fixed {total_insertions} table(s) in {total_files} file(s).[/green]")


def main(dry_run: bool = False) -> None:
    console = Console()
    console.print("🔧 Fix markdown tables in report library", style="cyan bold")
    console.print("   Adding missing separator row after table headers so tables render correctly.\n")
    fix_all_reports(dry_run=dry_run)
