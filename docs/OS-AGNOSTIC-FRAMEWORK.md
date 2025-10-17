# OS-Agnostic Development Framework

**Philosophy:** Write once, run everywhere - Linux, macOS, Windows  
**Pattern:** Abstraction layer + proven cross-platform libraries  
**Result:** Consistent experience on any operating system

---

## The Vision

### Traditional Approach (Anti-Pattern)

```
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux-specific code
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS-specific code
elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]]; then
    # Windows-specific code
fi

# Result: Spaghetti code, inconsistent behavior, endless edge cases
```

### Gold Standard Approach

```
Use cross-platform libraries:
  ↓
Abstraction layer hides OS differences:
  ↓
Business logic never sees OS:
  ↓
Test on all platforms:
  ↓
Same experience everywhere
```

---

## Part 1: Foundation Architecture

### Cross-Platform Stack

```
┌─────────────────────────────────────────────────────┐
│            Your Business Logic                      │
│         (OS-agnostic, always)                       │
├─────────────────────────────────────────────────────┤
│            PAI Foundation Layer                     │
│  ┌──────────────────────────────────────────────┐  │
│  │ File Operations │ Process Mgmt │ Networking │  │
│  ├──────────────────────────────────────────────┤  │
│  │ User Config │ Secrets │ Logging │ CLI       │  │
│  └──────────────────────────────────────────────┘  │
│         (OS detection happens here)                 │
├─────────────────────────────────────────────────────┤
│        Cross-Platform Libraries (95%)               │
│  ┌──────────────────────────────────────────────┐  │
│  │ Python stdlib │ Click │ Pathlib │ Rich      │  │
│  ├──────────────────────────────────────────────┤  │
│  │ Requests │ PyYAML │ Pydantic │ Keyring     │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
              Linux │ macOS │ Windows
              Works everywhere
```

---

## Part 2: Proven Cross-Platform Libraries

### Core Stack (Use These, Not Custom Code)

#### File Operations
```python
# ❌ BAD: OS-specific paths
home = "/home/user"              # Linux only
home = "/Users/user"             # macOS only
home = "C:\\Users\\user"         # Windows only

# ✅ GOOD: Cross-platform
from pathlib import Path
home = Path.home()               # Works everywhere
config = home / ".config" / "pai"
```

#### Process Management
```python
# ❌ BAD: Shell-specific
subprocess.run("ps aux | grep myapp", shell=True)

# ✅ GOOD: Cross-platform
import psutil
for proc in psutil.process_iter(['name']):
    if proc.info['name'] == 'myapp':
        print(proc)
```

#### User Directories
```python
# ❌ BAD: Hardcoded paths
config_dir = "~/.config"         # Unix only

# ✅ GOOD: Platform-aware
import platformdirs
config_dir = platformdirs.user_config_dir("pai", "jbyrd")
# Linux:   ~/.config/pai
# macOS:   ~/Library/Application Support/pai
# Windows: C:\Users\<user>\AppData\Local\jbyrd\pai
```

#### CLI Interface
```python
# ❌ BAD: Platform-specific formatting
print("\033[32mSuccess\033[0m")  # ANSI codes (breaks on Windows)

# ✅ GOOD: Cross-platform
from rich.console import Console
console = Console()
console.print("[green]Success[/green]")  # Works everywhere
```

#### Secrets Management
```python
# ❌ BAD: OS-specific
# Linux: Gnome Keyring
# macOS: Keychain Access
# Windows: Credential Manager

# ✅ GOOD: Cross-platform
import keyring
keyring.set_password("pai", "gitlab_token", token)
token = keyring.get_password("pai", "gitlab_token")
# Handles all platforms automatically
```

#### Configuration Files
```python
# ❌ BAD: Hardcoded
config_file = "/etc/myapp.conf"  # Unix only

# ✅ GOOD: Platform-aware
import platformdirs
from pathlib import Path
config_file = Path(platformdirs.user_config_dir("pai")) / "config.yml"
```

---

## Part 3: PAI Foundation Abstraction Layer

### `foundation/platform.py` (Hide All OS Differences)

```python
"""
Cross-Platform Abstraction Layer
Business logic NEVER imports os, sys, platform directly
Always use this module instead
"""
import platform
import sys
from pathlib import Path
from typing import Optional
import platformdirs
import keyring

class Platform:
    """
    Single interface for all platform-specific operations
    """
    
    @staticmethod
    def system() -> str:
        """
        Get OS name in normalized form
        Returns: 'linux', 'macos', or 'windows'
        """
        system = platform.system().lower()
        if system == 'darwin':
            return 'macos'
        return system
    
    @staticmethod
    def is_linux() -> bool:
        return Platform.system() == 'linux'
    
    @staticmethod
    def is_macos() -> bool:
        return Platform.system() == 'macos'
    
    @staticmethod
    def is_windows() -> bool:
        return Platform.system() == 'windows'
    
    @staticmethod
    def home_dir() -> Path:
        """User's home directory (cross-platform)"""
        return Path.home()
    
    @staticmethod
    def config_dir(app_name: str = "pai") -> Path:
        """Application config directory (OS-appropriate)"""
        return Path(platformdirs.user_config_dir(app_name, "jbyrd"))
    
    @staticmethod
    def data_dir(app_name: str = "pai") -> Path:
        """Application data directory (OS-appropriate)"""
        return Path(platformdirs.user_data_dir(app_name, "jbyrd"))
    
    @staticmethod
    def cache_dir(app_name: str = "pai") -> Path:
        """Application cache directory (OS-appropriate)"""
        return Path(platformdirs.user_cache_dir(app_name, "jbyrd"))
    
    @staticmethod
    def log_dir(app_name: str = "pai") -> Path:
        """Application log directory (OS-appropriate)"""
        return Path(platformdirs.user_log_dir(app_name, "jbyrd"))
    
    @staticmethod
    def temp_dir() -> Path:
        """Temporary directory (cross-platform)"""
        import tempfile
        return Path(tempfile.gettempdir())
    
    @staticmethod
    def ensure_dirs(app_name: str = "pai") -> None:
        """Create all required directories"""
        for dir_func in [Platform.config_dir, Platform.data_dir, 
                         Platform.cache_dir, Platform.log_dir]:
            dir_path = dir_func(app_name)
            dir_path.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def get_secret(service: str, key: str) -> Optional[str]:
        """Get secret from OS keychain (cross-platform)"""
        try:
            return keyring.get_password(service, key)
        except Exception:
            return None
    
    @staticmethod
    def set_secret(service: str, key: str, value: str) -> bool:
        """Store secret in OS keychain (cross-platform)"""
        try:
            keyring.set_password(service, key, value)
            return True
        except Exception:
            return False
    
    @staticmethod
    def delete_secret(service: str, key: str) -> bool:
        """Delete secret from OS keychain (cross-platform)"""
        try:
            keyring.delete_password(service, key)
            return True
        except Exception:
            return False
    
    @staticmethod
    def shell_available() -> list[str]:
        """
        Get available shells (cross-platform)
        Returns list of shell names
        """
        if Platform.is_windows():
            return ['powershell', 'cmd']
        else:
            return ['bash', 'zsh', 'fish']
    
    @staticmethod
    def default_shell() -> str:
        """Get default shell for this platform"""
        if Platform.is_windows():
            return 'powershell'
        else:
            shell = os.environ.get('SHELL', '/bin/bash')
            return os.path.basename(shell)
    
    @staticmethod
    def executable_extension() -> str:
        """Get executable file extension for this platform"""
        return '.exe' if Platform.is_windows() else ''
    
    @staticmethod
    def path_separator() -> str:
        """Get PATH separator for this platform"""
        return ';' if Platform.is_windows() else ':'
    
    @staticmethod
    def line_ending() -> str:
        """Get line ending for this platform"""
        return '\r\n' if Platform.is_windows() else '\n'
    
    @staticmethod
    def open_file(path: Path) -> bool:
        """Open file with default application (cross-platform)"""
        import subprocess
        try:
            if Platform.is_macos():
                subprocess.run(['open', str(path)])
            elif Platform.is_linux():
                subprocess.run(['xdg-open', str(path)])
            elif Platform.is_windows():
                os.startfile(str(path))
            return True
        except Exception:
            return False
    
    @staticmethod
    def open_url(url: str) -> bool:
        """Open URL in default browser (cross-platform)"""
        import webbrowser
        return webbrowser.open(url)


# Global instance
platform = Platform()
```

---

## Part 4: Usage in Business Logic

### Example: TAM RFE Tool (OS-Agnostic)

```python
# app/services/rfe_service.py
"""
TAM RFE Service - Business Logic
This code NEVER mentions Linux, macOS, or Windows
"""
from foundation.platform import platform
from foundation.config import settings
from pathlib import Path

class RFEService:
    """
    RFE business logic - OS-agnostic
    """
    
    def __init__(self):
        # Get OS-appropriate paths (no OS checks needed)
        self.config_dir = platform.config_dir("rfe-tool")
        self.data_dir = platform.data_dir("rfe-tool")
        self.cache_dir = platform.cache_dir("rfe-tool")
        
        # Ensure directories exist (works everywhere)
        platform.ensure_dirs("rfe-tool")
        
        # Load config (cross-platform paths)
        self.config_file = self.config_dir / "config.yml"
        
    def get_gitlab_token(self) -> str:
        """Get GitLab token from secure storage"""
        # Works on Linux (Secret Service), macOS (Keychain), Windows (Credential Manager)
        token = platform.get_secret("rfe-tool", "gitlab_token")
        if not token:
            raise ValueError("GitLab token not configured")
        return token
    
    def save_gitlab_token(self, token: str) -> None:
        """Save GitLab token to secure storage"""
        # Automatically uses correct keychain for this OS
        platform.set_secret("rfe-tool", "gitlab_token", token)
    
    def get_customer_data_path(self, customer: str) -> Path:
        """Get path to customer data (OS-appropriate)"""
        # Returns correct path for any OS
        return self.data_dir / "customers" / f"{customer}.json"
    
    def open_customer_report(self, customer: str) -> None:
        """Open customer report with default application"""
        report_path = self.data_dir / "reports" / f"{customer}.html"
        platform.open_file(report_path)  # Works on all OS
    
    def open_gitlab_issue(self, issue_url: str) -> None:
        """Open GitLab issue in browser"""
        platform.open_url(issue_url)  # Works on all OS
```

### Example: CLI Tool (OS-Agnostic)

```python
# bin/tam-rfe-chat
"""
TAM RFE Chat CLI
Works identically on Linux, macOS, Windows
"""
import click
from rich.console import Console
from rich.table import Table
from foundation.platform import platform

console = Console()  # Cross-platform colors/formatting

@click.group()
def cli():
    """TAM RFE Chat - Works on any OS"""
    # Ensure directories exist
    platform.ensure_dirs("rfe-tool")

@cli.command()
def configure():
    """Configure RFE tool (OS-agnostic)"""
    console.print("[blue]RFE Tool Configuration[/blue]")
    console.print(f"System: {platform.system()}")
    console.print(f"Config: {platform.config_dir('rfe-tool')}")
    
    # Get token securely (works on all OS)
    token = console.input("GitLab token: ")
    platform.set_secret("rfe-tool", "gitlab_token", token)
    
    console.print("[green]✅ Configuration saved[/green]")

@cli.command()
@click.argument('customer')
def chat(customer: str):
    """Chat with customer's case data"""
    from app.services import rfe_service
    
    service = rfe_service.RFEService()
    
    # All paths work on any OS
    customer_data = service.get_customer_data_path(customer)
    
    if not customer_data.exists():
        console.print(f"[red]❌ Customer {customer} not found[/red]")
        return
    
    # Business logic (OS-agnostic)
    # ...

if __name__ == '__main__':
    cli()
```

---

## Part 5: Ansible Integration (Cross-Platform)

### `ansible/roles/rfe_install/tasks/main.yml`

```yaml
---
# RFE Tool Installation (Cross-Platform)
# Works on Linux, macOS, Windows (WSL)

- name: Detect operating system
  set_fact:
    os_family: "{{ ansible_os_family }}"
    os_name: "{{ ansible_distribution }}"

- name: Display detected OS
  debug:
    msg: "Installing on {{ os_name }} ({{ os_family }})"

# Python installation (cross-platform via Geerling)
- name: Install Python
  include_role:
    name: geerlingguy.pip
  vars:
    pip_install_packages:
      - platformdirs
      - keyring
      - rich
      - click

# Cross-platform package installation
- name: Install system packages (Linux)
  package:
    name: "{{ item }}"
    state: present
  loop: "{{ rfe_packages_linux }}"
  when: os_family == "RedHat" or os_family == "Debian"

- name: Install system packages (macOS)
  homebrew:
    name: "{{ item }}"
    state: present
  loop: "{{ rfe_packages_macos }}"
  when: os_family == "Darwin"

# Clone repository (works everywhere)
- name: Clone RFE repository
  git:
    repo: "{{ rfe_repo_url }}"
    dest: "{{ rfe_install_dir }}"
    version: "{{ rfe_branch }}"

# Python dependencies (cross-platform)
- name: Install Python dependencies
  pip:
    requirements: "{{ rfe_install_dir }}/requirements.txt"
    virtualenv: "{{ rfe_install_dir }}/.venv"
    virtualenv_command: "{{ ansible_python_interpreter }} -m venv"

# Symlink tools to PATH (cross-platform)
- name: Link tools to PATH (Unix)
  file:
    src: "{{ rfe_install_dir }}/bin/{{ item }}"
    dest: "/usr/local/bin/{{ item }}"
    state: link
  loop: "{{ rfe_tools }}"
  when: os_family != "Windows"

- name: Add to PATH (Windows)
  win_path:
    elements: "{{ rfe_install_dir }}/bin"
    state: present
  when: os_family == "Windows"
```

---

## Part 6: Testing Strategy

### Test Matrix (All Platforms)

```yaml
# .github/workflows/test.yml
name: Cross-Platform Tests

on: [push, pull_request]

jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python: ['3.9', '3.10', '3.11', '3.12']
    
    runs-on: ${{ matrix.os }}
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python }}
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: pytest tests/ -v --cov=app
      
      - name: Test platform abstraction
        run: python -m tests.test_platform
```

### Platform-Specific Tests

```python
# tests/test_platform.py
"""
Test that platform abstraction works on all OS
"""
import pytest
from foundation.platform import platform
from pathlib import Path

def test_system_detection():
    """Platform detection works"""
    system = platform.system()
    assert system in ['linux', 'macos', 'windows']

def test_directories_created():
    """Directories are created correctly"""
    platform.ensure_dirs("test-app")
    
    config_dir = platform.config_dir("test-app")
    data_dir = platform.data_dir("test-app")
    cache_dir = platform.cache_dir("test-app")
    
    assert config_dir.exists()
    assert data_dir.exists()
    assert cache_dir.exists()

def test_secrets_management():
    """Secrets work on all platforms"""
    # Set secret
    success = platform.set_secret("test-app", "test-key", "test-value")
    assert success
    
    # Get secret
    value = platform.get_secret("test-app", "test-key")
    assert value == "test-value"
    
    # Delete secret
    success = platform.delete_secret("test-app", "test-key")
    assert success

def test_paths_are_portable():
    """Paths work on all platforms"""
    config_file = platform.config_dir("test-app") / "config.yml"
    
    # Path should be absolute
    assert config_file.is_absolute()
    
    # Path should use OS-appropriate separators
    path_str = str(config_file)
    if platform.is_windows():
        assert '\\' in path_str or '/' in path_str  # Windows accepts both
    else:
        assert '/' in path_str

@pytest.mark.skipif(platform.is_windows(), reason="Unix-specific test")
def test_unix_shell():
    """Unix shells detected correctly"""
    shells = platform.shell_available()
    assert 'bash' in shells

@pytest.mark.skipif(not platform.is_windows(), reason="Windows-specific test")
def test_windows_shell():
    """Windows shells detected correctly"""
    shells = platform.shell_available()
    assert 'powershell' in shells
```

---

## Part 7: Requirements

### `requirements.txt` (Cross-Platform Stack)

```txt
# Core cross-platform libraries
platformdirs>=3.0.0        # OS-appropriate directories
keyring>=24.0.0            # Secure credential storage
rich>=13.0.0               # Terminal formatting
click>=8.0.0               # CLI framework
requests>=2.31.0           # HTTP client
pyyaml>=6.0                # Configuration
pydantic>=2.0.0            # Validation

# Utilities
psutil>=5.9.0              # Process management
python-dateutil>=2.8.0     # Date/time handling

# Testing (all platforms)
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-xdist>=3.3.0        # Parallel testing

# Platform-specific (handled automatically)
pywin32>=306; platform_system=="Windows"        # Windows APIs
pyobjc-framework-Cocoa>=9.0; platform_system=="Darwin"  # macOS APIs
```

---

## Part 8: Documentation

### `docs/CROSS-PLATFORM.md`

```markdown
# Cross-Platform Development

## Philosophy

**Your code should never know what OS it's running on.**

## Rules

### ✅ DO

- Use `pathlib.Path` for all file operations
- Use `platformdirs` for config/data directories
- Use `keyring` for secrets
- Use `rich` for terminal output
- Use `click` for CLI interfaces
- Use `requests` for HTTP
- Use `psutil` for process management

### ❌ DON'T

- Check `sys.platform` or `os.name` in business logic
- Use shell commands (`subprocess.run(..., shell=True)`)
- Hardcode paths (`/home/user`, `C:\\Users`)
- Use ANSI codes directly
- Assume Unix-specific tools exist

## Testing

All code must pass tests on:
- Linux (Ubuntu latest)
- macOS (latest)
- Windows (latest)
- Python 3.9, 3.10, 3.11, 3.12

## Examples

See:
- `foundation/platform.py` - Abstraction layer
- `tests/test_platform.py` - Platform tests
- `app/services/` - Business logic examples
```

---

## Part 9: Developer Checklist

### Before Committing Code

```bash
# Run cross-platform checklist
pai-dev-checklist --cross-platform

# Checklist verifies:
✅ No hardcoded paths
✅ No os.system() or shell=True
✅ No platform-specific imports in business logic
✅ Uses foundation.platform abstraction
✅ Uses proven cross-platform libraries
✅ Tests pass on all platforms (CI)
```

### `bin/pai-dev-checklist` (Add Cross-Platform Check)

```bash
# Add to pai-dev-checklist

print_header "Cross-Platform Check"

# Check for anti-patterns
echo "Checking for platform-specific code..."

# Bad: Hardcoded paths
if grep -r "/home/" app/ --include="*.py" 2>/dev/null; then
    print_error "Hardcoded /home/ paths found"
fi

if grep -r "C:\\\\" app/ --include="*.py" 2>/dev/null; then
    print_error "Hardcoded Windows paths found"
fi

# Bad: Platform checks in business logic
if grep -r "sys.platform" app/ --include="*.py" 2>/dev/null; then
    print_warning "Direct sys.platform usage (use foundation.platform)"
fi

# Bad: Shell commands
if grep -r "shell=True" app/ --include="*.py" 2>/dev/null; then
    print_error "Shell commands found (use cross-platform alternatives)"
fi

# Good: Using abstraction
if grep -r "from foundation.platform import platform" app/ --include="*.py" 2>/dev/null; then
    print_success "Using platform abstraction"
fi

print_header "Cross-Platform Checklist"
echo ""
echo "  [ ] Code uses pathlib.Path?"
echo "  [ ] Code uses platformdirs?"
echo "  [ ] Code uses keyring for secrets?"
echo "  [ ] Code uses rich for output?"
echo "  [ ] No hardcoded paths?"
echo "  [ ] No shell commands?"
echo "  [ ] No OS checks in business logic?"
echo "  [ ] Tests pass on Linux/macOS/Windows?"
```

---

## Bottom Line

### Traditional Approach

```
Write for Linux:
  if linux: do_thing_a()
  
Port to macOS:
  elif macos: do_thing_b()
  
Port to Windows:
  elif windows: do_thing_c()
  
Result: 3x the code, 3x the bugs, 3x the maintenance
```

### Gold Standard Approach

```
Write once:
  platform.do_thing()  # Works everywhere
  
Test everywhere:
  CI runs on Linux/macOS/Windows
  
Result: 1x the code, 1x the bugs, 1x the maintenance
```

### The Promise

**Any tool built with PAI Foundation:**
```
✅ Works on Linux
✅ Works on macOS
✅ Works on Windows
✅ Same CLI experience
✅ Same file locations (OS-appropriate)
✅ Same configuration method
✅ Same secret storage
✅ One codebase
✅ Tested on all platforms
```

**User Experience:**
```bash
# Linux
$ tam-rfe-chat jpmc
[Works]

# macOS
$ tam-rfe-chat jpmc
[Works identically]

# Windows
> tam-rfe-chat jpmc
[Works identically]
```

**Your code never knows the difference.**

---

*Philosophy: OS-Agnostic by Default*  
*Pattern: Abstraction Layer + Proven Libraries*  
*Result: Consistent experience on any operating system*
