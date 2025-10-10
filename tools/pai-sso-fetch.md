# PAI SSO Fetch

## Purpose
Access SSO-protected Red Hat internal sites (like source.redhat.com) using existing Chrome browser authentication cookies, eliminating the need for manual authentication in scripts.

## Location
`~/.local/bin/pai-sso-fetch`

## Description
`pai-sso-fetch` leverages your active Chrome SSO session to programmatically access internal Red Hat sites that are behind Single Sign-On (SSO) authentication. It automatically detects Chrome profiles with @redhat.com email addresses and extracts the necessary authentication cookies.

## Key Features
- **Automatic Work Profile Detection**: Finds Chrome profiles with @redhat.com emails
- **Cookie Extraction**: Safely extracts session cookies from Chrome
- **Multiple Output Formats**: HTML, text, or markdown output
- **Profile Support**: Works with multiple Chrome profiles
- **Pipeline Friendly**: Supports stdout output for scripting
- **Domain Testing**: Verify access before fetching content

## Usage

### Basic Commands

```bash
# List available Chrome profiles
pai-sso-fetch list-profiles

# Test access to a domain
pai-sso-fetch test source.redhat.com

# Fetch a page
pai-sso-fetch fetch https://source.redhat.com/some/page

# Extract cookies for a specific domain
pai-sso-fetch extract-cookies -d redhat.com

# Initial setup
pai-sso-fetch setup
```

### Command Options

#### Global Options
- `-p, --profile <name>`: Specify Chrome profile to use (auto-detects Red Hat profile by default)
- `-h, --help`: Show help message

#### fetch Command
- `-o, --output <file>`: Save to specific file (default: auto-generated)
- `-f, --format <fmt>`: Output format: html, text, markdown (default: markdown)

#### extract-cookies Command
- `-d, --domain <domain>`: Domain to extract cookies for (default: redhat.com)

### Examples

#### Basic Page Fetch
```bash
# Fetch a page from source.redhat.com
pai-sso-fetch fetch https://source.redhat.com/groups/public/kubernetes

# Save with specific filename
pai-sso-fetch fetch https://source.redhat.com/page -o kubernetes-guide.md
```

#### Different Output Formats
```bash
# Save as HTML
pai-sso-fetch fetch https://source.redhat.com/page -f html

# Save as plain text
pai-sso-fetch fetch https://source.redhat.com/page -f text
```

#### Pipeline Usage
```bash
# Fetch and process with other tools
pai-sso-fetch fetch https://source.redhat.com/api/data -f text | grep "important"

# Extract specific information
pai-sso-fetch fetch https://source.redhat.com/docs/guide -f markdown | \
    grep "^##" > sections.txt
```

#### Using Specific Profile
```bash
# List profiles to find the right one
pai-sso-fetch list-profiles

# Use a specific profile
pai-sso-fetch -p "Profile 2" fetch https://source.redhat.com/page
```

#### Testing Access
```bash
# Test if you can access a domain
pai-sso-fetch test source.redhat.com
pai-sso-fetch test docs.redhat.com
```

## How It Works

1. **Profile Detection**: Automatically finds Chrome profiles with @redhat.com emails
2. **Cookie Extraction**: Copies Chrome's cookie database and extracts relevant cookies
3. **Authentication**: Uses extracted cookies with curl to maintain SSO session
4. **Content Conversion**: Converts HTML to requested format (markdown, text, or HTML)

## Configuration

### Chrome Profile Detection
The tool automatically detects Chrome profiles containing Red Hat email addresses by:
1. Scanning Chrome profile directories
2. Checking Preferences files for @redhat.com emails
3. Using the first Red Hat profile found (or specified profile)

### Cookie Storage
- Cookies are temporarily stored in `~/.claude/context/secrets/browser-cookies/`
- Cookie files are refreshed if older than 30 minutes
- Cookies are stored in Netscape format compatible with curl

## Output Formats

### Markdown (default)
```markdown
---
title: "Page Title"
source: "https://source.redhat.com/page"
fetched: 2025-09-11T14:30:00-04:00
domain: "source.redhat.com"
---

# Page Title

[Content converted to markdown...]
```

### HTML
- Raw HTML as fetched from the server
- Useful for pages with complex formatting

### Text
- Plain text conversion using lynx/w3m if available
- Basic HTML stripping as fallback

## Integration with Other PAI Tools

```bash
# Fetch internal documentation and analyze
pai-sso-fetch fetch https://source.redhat.com/docs/security-guide | \
    pai-fabric analyze-security

# Archive internal pages
for url in $(cat internal-urls.txt); do
    pai-sso-fetch fetch "$url" -o "archive/$(basename $url).md"
done
```

## Dependencies

### Required
- `curl`: For HTTP requests
- `sqlite3`: For reading Chrome cookie database
- Chrome or Chromium browser

### Optional
- `pandoc`: For better HTML to Markdown conversion
- `lynx` or `w3m`: For HTML to text conversion
- `python3`: For advanced cookie extraction (with encryption support)

### Installation
```bash
# Fedora/RHEL
sudo dnf install sqlite curl pandoc lynx

# Python dependencies (optional, for encrypted cookies)
pip install pycryptodome secretstorage
```

## Security Considerations

### Cookie Handling
- Cookies are copied, not moved from Chrome
- Temporary files are created with restricted permissions
- Cookie files should not be shared or committed to version control

### Authentication
- Requires active Chrome session with SSO login
- Cookies expire based on SSO session timeout
- Tool will fail gracefully if authentication expires

### Best Practices
- Use for internal tools and automation only
- Do not share extracted cookies
- Re-login to Chrome if access fails
- Keep Chrome profile locked when not in use

## Troubleshooting

### No Chrome Profile Found
```
Error: Chrome/Chromium cookie database not found
```
**Solution**: Run `pai-sso-fetch setup` and ensure Chrome is installed

### Authentication Failed
```
Error: Authentication failed. Please login to source.redhat.com in Chrome and try again
```
**Solution**: 
1. Open Chrome with your Red Hat profile
2. Navigate to the target site and ensure you're logged in
3. Try the command again

### No Red Hat Profile Detected
```
Error: Chrome cookie database not found for profile: Default
```
**Solution**:
1. Run `pai-sso-fetch list-profiles` to see available profiles
2. Use `-p "Profile Name"` to specify the correct profile
3. Ensure you're logged into Chrome with your @redhat.com account

### Cookie Extraction Issues
- Some cookies may be encrypted (Chrome 80+)
- The tool attempts basic extraction first
- Python helper script provided for encrypted cookie support

## Advanced Usage

### Scripting with pai-sso-fetch
```bash
#!/bin/bash
# Fetch multiple pages from a list

while IFS= read -r url; do
    echo "Fetching: $url"
    if pai-sso-fetch fetch "$url" -o "fetched/$(echo $url | md5sum | cut -d' ' -f1).md"; then
        echo "✓ Success"
    else
        echo "✗ Failed" >> fetch-errors.log
    fi
    sleep 2  # Be nice to the server
done < urls.txt
```

### Creating Page Archives
```bash
# Archive an entire section
pai-sso-fetch fetch https://source.redhat.com/section/index -o index.md
grep -oE 'href="(/section/[^"]+)"' index.md | while read -r path; do
    pai-sso-fetch fetch "https://source.redhat.com$path"
done
```

## Related Tools
- `pai-confluence`: Access Confluence spaces with API tokens
- `pai-fabric`: Process fetched content with AI
- `pai-knowledge-sync`: Sync fetched content to knowledge base
