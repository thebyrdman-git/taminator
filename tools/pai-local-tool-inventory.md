# pai-local-tool-inventory

List all locally available tools and repositories.

## Location
`~/.local/bin/pai-local-tool-inventory`

## Description
Provides a quick inventory of:
- Executables in ~/.local/bin
- Public git repositories
- Internal Red Hat repositories

## Usage
```bash
pai-local-tool-inventory
```

## Output Sections
1. **Local Executables in ~/.local/bin**
   - All user-installed scripts and tools
   - Includes PAI tools and utilities

2. **Local Repos: gits/active**
   - Active public git repositories
   - Currently being worked on

3. **Local Repos: gits/references**
   - Reference public repositories
   - For lookup/reference only

4. **Internal Repos: gitlabs/active**
   - Active Red Hat internal repositories
   - From gitlab.cee.redhat.com

5. **Internal Repos: gitlabs/references**
   - Reference internal repositories
   - For lookup/reference only

## Example Output
```
[Local Executables in ~/.local/bin]
pai-case-initial-screen
pai-local-tool-inventory
pai-my-plate
pai-services
rhcase
supportshell-tool-scan

[Local Repos: gits/active]
(empty)

[Local Repos: gits/references]
(empty)

[Internal Repos: gitlabs/active]
(empty)

[Internal Repos: gitlabs/references]
(empty)
```

## Use Cases
- Quick tool discovery
- Verify tool installation
- Check repository status
- Audit available resources
