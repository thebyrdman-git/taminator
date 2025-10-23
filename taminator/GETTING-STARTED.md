# 🚀 Getting Started with Taminator v1.9.3

**Welcome to Taminator!** The RFE/Bug tracking tool that Red Hat TAMs actually want.

---

## 📦 Installation

### 1. Download

Get the latest AppImage from:
- **GitLab Releases:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases
- **Direct Download:** `Taminator-1.9.3.AppImage`

### 2. Make Executable

```bash
chmod +x Taminator-1.9.3.AppImage
```

### 3. Run

```bash
./Taminator-1.9.3.AppImage
```

Or double-click from your file manager!

### 4. (Optional) Add to Applications Menu

```bash
# Copy to Applications folder
cp Taminator-1.9.3.AppImage ~/Applications/

# Create desktop entry
cat > ~/.local/share/applications/taminator.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Taminator
Comment=RFE/Bug tracking tool for Red Hat TAMs
Exec=/home/$USER/Applications/Taminator-1.9.3.AppImage %U
Icon=taminator
Terminal=false
Categories=Development;Utility;
Keywords=rfe;bug;jira;redhat;tam;
EOF

# Update desktop database
update-desktop-database ~/.local/share/applications/
```

---

## 🔑 Authentication Setup

Taminator v1.9.3 supports **two authentication methods**:

### Option 1: Auth Box (Local Storage) ✅ Recommended for Single Users

**What it is:** Encrypted local token storage on your machine.

**Setup:** No configuration needed! Just add tokens via the GUI.

**Pros:**
- ✅ Works offline
- ✅ No external dependencies
- ✅ Quick setup

**Cons:**
- ❌ Tokens only on one machine
- ❌ No team sharing

### Option 2: HashiCorp Vault 🔒 Recommended for Teams

**What it is:** Centralized secrets management with audit logging.

**Setup:**

1. **Set environment variables** (before launching Taminator):
   ```bash
   export VAULT_ADDR="http://your-vault-server:8201"
   export VAULT_TOKEN="your-vault-token-here"
   ```

2. **Make permanent** (add to `~/.bashrc` or `~/.zshrc`):
   ```bash
   echo 'export VAULT_ADDR="http://your-vault-server:8201"' >> ~/.bashrc
   echo 'export VAULT_TOKEN="your-vault-token-here"' >> ~/.bashrc
   source ~/.bashrc
   ```

3. **Launch Taminator** - It will automatically detect Vault!

**Pros:**
- ✅ Centralized tokens (access from any machine)
- ✅ Team collaboration
- ✅ Audit logging
- ✅ Auto-fallback to Auth Box if offline

**Cons:**
- ❌ Requires Vault server
- ❌ Initial setup needed

---

## 🎯 First-Time Setup

### 1. Launch Taminator

```bash
./Taminator-1.9.3.AppImage
```

### 2. Navigate to Vault Tab (or Use Auth Box Fallback)

**If using Vault:**
- Set VAULT_ADDR and VAULT_TOKEN (see above)
- Navigate to **🔒 Vault** tab
- Connection status should show "✓ Online"

**If using Auth Box:**
- No setup needed
- Vault tab will show "⚠️ Using Auth Box fallback"
- You're ready to go!

### 3. Add Your JIRA Token

**Via Vault Tab:**
1. Click **"Add Token"**
2. Service name: `jira`
3. Token value: `your-jira-token-here`
4. Click **"Save"**

**Via Auth Box (if not using Vault):**
- Auth Box still works automatically in the background
- No manual setup needed for first use

### 4. Add Other Tokens (Optional)

Depending on your workflow, you may want:
- `portal` - Red Hat Customer Portal API token
- `hydra` - Customer intelligence data
- `supportshell` - Case data access
- `github` - For issue reporting

---

## 📝 Generate Your First Report

### Quick Start

1. **Navigate to Home** (🏠 icon)
2. **Enter customer name** in the search box
3. **Click "Check Status"** or "Generate Report"
4. **View results** in the main panel

### Detailed Workflow

#### Step 1: Check JIRA Issues
```bash
# Via CLI (if you prefer terminal)
tam-rfe check <customer-name>
```

Or use the GUI:
- Home → Enter customer name → "Check Status"

#### Step 2: Generate RFE Report
- Click **"Generate Report"**
- Select report type (RFE, Bug, or Both)
- Choose format (Markdown, HTML, PDF)
- Click **"Generate"**

#### Step 3: Review & Post
- Review the generated report
- Edit if needed
- Click **"Post to Portal"** (or save locally)

---

## 🛠️ Common Tasks

### View Current JIRA Status
1. Navigate to **Home** tab
2. Enter customer name
3. Click **"Check Status"**
4. View issue list with current statuses

### Update Report
1. Navigate to **Reports** tab
2. Select existing report
3. Click **"Update"**
4. Review changes
5. Post updated version

### Onboard New Customer
1. Navigate to **Onboard** tab
2. Click **"Add Customer"**
3. Enter customer details:
   - Name
   - Account number
   - SBR groups
4. Click **"Save"**

### Migrate from Auth Box to Vault
1. Set VAULT_ADDR and VAULT_TOKEN
2. Restart Taminator
3. Navigate to **Vault** tab
4. Click **"Migrate from Auth Box"**
5. All tokens copied automatically!

---

## 🔧 Settings

### Access Settings
- Click **Settings** (⚙️) in the navigation

### General Settings
- **Default TAM Email** - Your Red Hat email
- **Auto-update** - Check for report updates on startup
- **Notifications** - Desktop notifications for events

### Report Settings
- **Default Format** - Markdown, HTML, or PDF
- **Include Timestamps** - Add timestamps to reports
- **Generate Changelog** - Track changes on updates

### Advanced Settings
- **Reports Directory** - Where to save reports
- **JIRA Timeout** - Query timeout (default: 30s)
- **Debug Mode** - Enable detailed logging

### Reset All
- Click **"🔄 Reset to Defaults"**
- Clears all settings (including Vault cache)
- **Note:** Vault environment variables must be cleared manually

---

## 🆘 Troubleshooting

### Issue: Blank page on launch
**Fix:** You may have v1.9.2 (known bug). Download v1.9.3.

### Issue: "Vault not configured"
**Fix:** Set VAULT_ADDR and VAULT_TOKEN environment variables before launching.

### Issue: "JIRA token not found"
**Fix:** 
1. Navigate to Vault tab (or Auth Box fallback)
2. Add JIRA token
3. Retry operation

### Issue: "Connection timeout"
**Fix:**
1. Check VPN connection (Red Hat internal APIs require VPN)
2. Increase timeout in Settings → Advanced → JIRA Timeout
3. Check network connectivity

### Issue: Can't see Vault tab
**Fix:** You may have an older version. Download v1.9.3.

### Issue: Vault shows "Offline" but server is running
**Fix:**
1. Verify VAULT_ADDR is correct: `echo $VAULT_ADDR`
2. Verify VAULT_TOKEN is set: `echo $VAULT_TOKEN`
3. Test connection: `curl $VAULT_ADDR/v1/sys/health`
4. Restart Taminator

---

## 📚 Additional Resources

### Documentation
- **CHANGELOG:** See `CHANGELOG-v1.9.3.md` for what's new
- **Vault Integration:** See `VAULT-INTEGRATION-COMPLETE.md` for details
- **GitLab Issues:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues

### Getting Help
- **File a bug:** Use `tam-rfe report-issue` or the GUI
- **Slack:** #tam-automation (internal)
- **GitLab Issues:** Submit directly to the repository

### Tips & Tricks
- **Keyboard shortcuts:** Coming in v2.0!
- **Batch operations:** Select multiple issues for bulk updates
- **Offline mode:** Works perfectly with Auth Box (no Vault needed)
- **Team collaboration:** Use Vault for shared token management

---

## 🎉 What's Next?

### Explore Features
- 📊 **Reports Tab** - View and manage all your reports
- 📋 **Check Tab** - Quick status checks for customers
- ➕ **Onboard Tab** - Add new customers
- 🔒 **Vault Tab** - Manage tokens centrally (v1.9.3+)
- ⚙️ **Settings Tab** - Customize your experience

### Learn Advanced Features
- **Automated updates** - Reports stay current automatically
- **Change tracking** - See what changed in each update
- **Bulk operations** - Process multiple issues at once
- **Team sharing** - Vault enables team token management

### Contribute
- Found a bug? Report it!
- Have a feature request? File an issue!
- Want to contribute? Check the GitLab repository!

---

## 📞 Support

**Need help?** We're here for you!

- **Internal TAMs:** #tam-automation Slack channel
- **Issues:** https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues
- **Email:** jbyrd@redhat.com

---

**Welcome to the team!** 🚀

You're now ready to automate your RFE and bug tracking workflow. Happy reporting!

---

**Version:** Taminator v1.9.3  
**Last Updated:** October 23, 2025  
**Author:** Jimmy Byrd (jbyrd@redhat.com)
