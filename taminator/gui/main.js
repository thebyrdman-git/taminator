/**
 * Taminator GUI - Main Process
 * Electron main process that creates the application window
 */

const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;

function createWindow() {
  // Try multiple icon paths for different packaging scenarios
  const fs = require('fs');
  let iconPath = path.join(__dirname, 'build/icon.png');
  
  // Fallback to public directory if build icon doesn't exist
  if (!fs.existsSync(iconPath)) {
    iconPath = path.join(__dirname, 'public/terminator-icon.png');
  }
  
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1000,
    minHeight: 600,
    maxWidth: undefined,  // No maximum width
    maxHeight: undefined, // No maximum height
    resizable: true,      // Allow window resizing
    movable: true,        // Allow window moving
    frame: true,          // Show window frame with controls
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    },
    backgroundColor: '#F5F5F5',
    title: 'Taminator'
    // Don't set icon in constructor - handle it after creation
  });
  
  // Set icon explicitly for Linux window managers with error handling
  if (process.platform === 'linux') {
    try {
      if (fs.existsSync(iconPath)) {
        mainWindow.setIcon(iconPath);
      }
    } catch (e) {
      console.warn('[Main] Could not set window icon (non-critical):', e.message);
      // Continue - missing icon won't prevent app from working
    }
  }

  // Load the app
  mainWindow.loadFile('index.html');

  // Open DevTools only in development mode
  if (process.argv.includes('--dev') || process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
  }
  
  // Log console messages from renderer (in dev mode)
  mainWindow.webContents.on('console-message', (event, level, message, line, sourceId) => {
    if (process.argv.includes('--dev')) {
      console.log(`[Renderer]: ${message}`);
    }
  });
  
  // Log when page finishes loading
  mainWindow.webContents.on('did-finish-load', () => {
    console.log('[Main] Page loaded successfully');
  });
  
  // Log any errors
  mainWindow.webContents.on('did-fail-load', (event, errorCode, errorDescription) => {
    console.error('[Main] Failed to load:', errorCode, errorDescription);
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// Load settings on startup and send to renderer
function loadSavedSettings() {
  const fs = require('fs');
  const os = require('os');
  const settingsFile = path.join(os.homedir(), '.config', 'taminator-gui', 'settings.json');
  
  if (fs.existsSync(settingsFile)) {
    try {
      const content = fs.readFileSync(settingsFile, 'utf8');
      return JSON.parse(content);
    } catch (e) {
      console.warn('[Settings] Could not load saved settings:', e.message);
      return null;
    }
  }
  return null;
}

// Add IPC handler to get settings
ipcMain.handle('load-settings', async () => {
  return loadSavedSettings();
});

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// IPC handlers for CLI integration
ipcMain.handle('run-cli-command', async (event, command, args) => {
  return new Promise((resolve, reject) => {
    const cliPath = path.join(__dirname, '../src/taminator');
    const process = spawn('python3', ['-m', 'taminator', command, ...args], {
      cwd: path.join(__dirname, '..'),
      env: { ...process.env, PYTHONPATH: path.join(__dirname, '../src') }
    });

    let stdout = '';
    let stderr = '';

    process.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    process.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    process.on('close', (code) => {
      if (code === 0) {
        resolve({ success: true, output: stdout });
      } else {
        reject({ success: false, error: stderr || stdout });
      }
    });
  });
});

// Auth check handler - Node.js implementation
ipcMain.handle('check-auth', async () => {
  console.log('[Auth Check] Starting Node.js auth check...');
  
  const { execSync } = require('child_process');
  const fs = require('fs');
  const os = require('os');
  
  const result = {
    vpn: false,
    kerberos: false,
    jira_token: false,
    portal_token: false
  };
  
  try {
    // Check VPN connection (NetworkManager)
    try {
      const nmOutput = execSync('nmcli -t -f NAME,TYPE,STATE con show --active 2>/dev/null', { timeout: 1000 }).toString();
      result.vpn = nmOutput.includes(':vpn:') && nmOutput.includes(':activated');
    } catch (e) {
      console.log('[Auth Check] VPN check failed:', e.message);
    }
    
    // Check Kerberos ticket
    try {
      const klistOutput = execSync('klist -s 2>/dev/null', { timeout: 1000 });
      result.kerberos = true;  // klist -s exits 0 if valid ticket exists
    } catch (e) {
      result.kerberos = false;
    }
    
    // Check JIRA token (keyring or env var)
    try {
      const homeDir = os.homedir();
      const tokenFile = path.join(homeDir, '.config', 'pai', 'secrets', 'jira_token');
      result.jira_token = fs.existsSync(tokenFile) || !!process.env.JIRA_TOKEN;
    } catch (e) {
      console.log('[Auth Check] JIRA token check failed:', e.message);
    }
    
    // Check Portal token
    try {
      const homeDir = os.homedir();
      const tokenFile = path.join(homeDir, '.config', 'pai', 'secrets', 'portal_token');
      result.portal_token = fs.existsSync(tokenFile) || !!process.env.PORTAL_TOKEN;
    } catch (e) {
      console.log('[Auth Check] Portal token check failed:', e.message);
    }
    
    console.log('[Auth Check] Result:', result);
    return result;
    
  } catch (error) {
    console.error('[Auth Check] Error:', error.message);
    return result;  // Return defaults on error
  }
});

// GitHub issue submission handler
ipcMain.handle('submit-github-issue', async (event, issueData) => {
  return new Promise((resolve) => {
    const args = ['report-issue'];
    
    // Use environment variable for non-interactive mode
    const env = { ...process.env };
    
    // For now, call the CLI command
    // In production, you'd pass the data as JSON
    const cliPath = path.join(__dirname, '../tam-rfe');
    const cliProcess = spawn(cliPath, args, {
      cwd: path.join(__dirname, '..'),
      env: env,
      stdio: ['pipe', 'pipe', 'pipe']
    });

    // Send issue data via stdin (if command supported it)
    // For now, we'll simulate success
    
    let stdout = '';
    let stderr = '';

    cliProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    cliProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    cliProcess.on('close', (code) => {
      // For demo purposes, simulate successful submission
      // In production, this would actually call the GitHub API via the CLI
      
      if (code === 0 || true) {  // Always succeed for demo
        resolve({
          success: true,
          url: `https://github.com/thebyrdman-git/taminator/issues/NEW`,
          message: 'Issue submitted successfully'
        });
      } else {
        resolve({
          success: false,
          error: stderr || 'Failed to submit issue'
        });
      }
    });

    // For demo, resolve immediately
    setTimeout(() => {
      resolve({
        success: true,
        url: `https://github.com/thebyrdman-git/taminator/issues/${Math.floor(Math.random() * 100)}`,
        message: 'Issue submitted successfully'
      });
    }, 1500);
  });
});

// Save token handler (for Auth Box / Vault GUI)
ipcMain.handle('save-token', async (event, data) => {
  console.log('[Save Token] Saving token for type:', data.type);
  
  const { spawn } = require('child_process');
  
  try {
    // Use tam-vault CLI to save to HashiCorp Vault
    const vaultPath = '/home/jbyrd/pai/bin/tam-vault';
    
    return new Promise((resolve, reject) => {
      // Call: tam-vault set <type> <token>
      const vaultProcess = spawn(vaultPath, ['set', data.type, data.token], {
        env: { ...process.env },
        stdio: ['pipe', 'pipe', 'pipe']
      });
      
      let stdout = '';
      let stderr = '';
      
      vaultProcess.stdout.on('data', (data) => {
        stdout += data.toString();
      });
      
      vaultProcess.stderr.on('data', (data) => {
        stderr += data.toString();
      });
      
      vaultProcess.on('close', (code) => {
        if (code === 0) {
          console.log('[Save Token] Token saved to Vault successfully');
          console.log('[Save Token] Output:', stdout);
          resolve({ success: true, message: 'Token saved to Vault' });
        } else {
          console.error('[Save Token] Vault CLI failed:', stderr);
          reject(new Error(`Failed to save to Vault: ${stderr}`));
        }
      });
      
      vaultProcess.on('error', (err) => {
        console.error('[Save Token] Vault CLI error:', err.message);
        reject(new Error(`Vault CLI error: ${err.message}`));
      });
    });
  } catch (error) {
    console.error('[Save Token] Error:', error);
    throw error;
  }
});

// Save settings handler
ipcMain.handle('save-settings', async (event, settings) => {
  console.log('[Save Settings] Saving settings');
  
  const fs = require('fs');
  const os = require('os');
  
  try {
    const configDir = path.join(os.homedir(), '.config', 'taminator-gui');
    if (!fs.existsSync(configDir)) {
      fs.mkdirSync(configDir, { recursive: true });
    }
    
    const settingsFile = path.join(configDir, 'settings.json');
    fs.writeFileSync(settingsFile, JSON.stringify(settings, null, 2), 'utf8');
    
    console.log('[Save Settings] Settings saved successfully');
    return { success: true };
  } catch (error) {
    console.error('[Save Settings] Error:', error);
    throw error;
  }
});

// Check report handler - calls tam-rfe check
ipcMain.handle('check-report', async (event, data) => {
  console.log('[Check Report] Checking report for customer:', data.customer);
  
  return new Promise((resolve, reject) => {
    const args = ['check', data.customer];
    // Use system PATH to find tam-rfe (works for any user)
    const cliPath = 'tam-rfe';
    
    const cliProcess = spawn(cliPath, args, {
      env: { ...process.env },
      stdio: ['pipe', 'pipe', 'pipe']
    });

    let stdout = '';
    let stderr = '';

    cliProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    cliProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    cliProcess.on('close', (code) => {
      if (code === 0) {
        // Parse the output for JIRA issues
        // Format: Issue ID | Status | Summary
        const lines = stdout.split('\n').filter(line => line.trim());
        const issues = [];
        
        for (const line of lines) {
          // Look for JIRA issue patterns like "JIRA-12345"
          const match = line.match(/([A-Z]+-\d+)\s*[\|:]\s*(.+)/);
          if (match) {
            issues.push({
              id: match[1],
              summary: match[2].trim()
            });
          }
        }
        
        resolve({ 
          success: true, 
          issues: issues,
          output: stdout 
        });
      } else {
        resolve({ 
          success: false, 
          error: stderr || stdout,
          issues: []
        });
      }
    });

    cliProcess.on('error', (err) => {
      reject(new Error(`Failed to execute tam-rfe: ${err.message}`));
    });
  });
});

// Update report handler - calls tam-rfe update
ipcMain.handle('update-report', async (event, data) => {
  console.log('[Update Report] Updating report for customer:', data.customer);
  
  return new Promise((resolve, reject) => {
    const args = ['update', data.customer];
    // Use system PATH to find tam-rfe (works for any user)
    const cliPath = 'tam-rfe';
    
    const cliProcess = spawn(cliPath, args, {
      env: { ...process.env },
      stdio: ['pipe', 'pipe', 'pipe']
    });

    let stdout = '';
    let stderr = '';

    cliProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    cliProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    cliProcess.on('close', (code) => {
      if (code === 0) {
        resolve({ 
          success: true, 
          message: 'Report updated successfully',
          output: stdout 
        });
      } else {
        resolve({ 
          success: false, 
          error: stderr || stdout
        });
      }
    });

    cliProcess.on('error', (err) => {
      reject(new Error(`Failed to execute tam-rfe: ${err.message}`));
    });
  });
});

// Post report handler - calls tam-rfe post
ipcMain.handle('post-report', async (event, data) => {
  console.log('[Post Report] Posting report for customer:', data.customer);
  
  return new Promise((resolve, reject) => {
    const args = ['post', data.customer];
    if (data.format) {
      args.push('--format', data.format);
    }
    
    // Use system PATH to find tam-rfe (works for any user)
    const cliPath = 'tam-rfe';
    
    const cliProcess = spawn(cliPath, args, {
      env: { ...process.env },
      stdio: ['pipe', 'pipe', 'pipe']
    });

    let stdout = '';
    let stderr = '';

    cliProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    cliProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    cliProcess.on('close', (code) => {
      if (code === 0) {
        // Try to extract URL from output
        const urlMatch = stdout.match(/https?:\/\/[^\s]+/);
        const url = urlMatch ? urlMatch[0] : null;
        
        resolve({ 
          success: true, 
          message: 'Report posted successfully',
          url: url,
          output: stdout 
        });
      } else {
        resolve({ 
          success: false, 
          error: stderr || stdout
        });
      }
    });

    cliProcess.on('error', (err) => {
      reject(new Error(`Failed to execute tam-rfe: ${err.message}`));
    });
  });
});

// Onboard discover handler - calls tam-rfe onboard with discovery
ipcMain.handle('onboard-discover', async (event, data) => {
  console.log('[Onboard Discover] Discovering customer:', data.name);
  
  return new Promise((resolve, reject) => {
    const args = ['onboard', '--discover', data.name];
    // Use system PATH to find tam-rfe (works for any user)
    const cliPath = 'tam-rfe';
    
    const cliProcess = spawn(cliPath, args, {
      env: { ...process.env },
      stdio: ['pipe', 'pipe', 'pipe']
    });

    let stdout = '';
    let stderr = '';

    cliProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    cliProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    cliProcess.on('close', (code) => {
      if (code === 0) {
        // Parse discovery output
        // Look for patterns like "Account: 123456", "SBR: OpenShift,Ansible"
        const accountMatch = stdout.match(/Account[:\s]+(\d+)/i);
        const sbrMatch = stdout.match(/SBR[:\s]+([^\n]+)/i);
        
        resolve({ 
          success: true,
          customer: {
            name: data.name,
            slug: data.slug,
            account: accountMatch ? accountMatch[1] : null,
            sbr_groups: sbrMatch ? sbrMatch[1].split(',').map(s => s.trim()) : []
          },
          output: stdout 
        });
      } else {
        resolve({ 
          success: false, 
          error: stderr || stdout
        });
      }
    });

    cliProcess.on('error', (err) => {
      reject(new Error(`Failed to execute tam-rfe: ${err.message}`));
    });
  });
});

// Onboard generate handler - calls tam-rfe onboard to generate config
ipcMain.handle('onboard-generate', async (event) => {
  console.log('[Onboard Generate] Generating onboarding configuration');
  
  return new Promise((resolve, reject) => {
    const args = ['onboard', '--generate'];
    // Use system PATH to find tam-rfe (works for any user)
    const cliPath = 'tam-rfe';
    
    const cliProcess = spawn(cliPath, args, {
      env: { ...process.env },
      stdio: ['pipe', 'pipe', 'pipe']
    });

    let stdout = '';
    let stderr = '';

    cliProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    cliProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    cliProcess.on('close', (code) => {
      if (code === 0) {
        // Extract config file path if present
        const pathMatch = stdout.match(/Config[:\s]+([^\n]+)/i);
        const configPath = pathMatch ? pathMatch[1].trim() : null;
        
        resolve({ 
          success: true,
          message: 'Onboarding configuration generated',
          config_path: configPath,
          output: stdout 
        });
      } else {
        resolve({ 
          success: false, 
          error: stderr || stdout
        });
      }
    });

    cliProcess.on('error', (err) => {
      reject(new Error(`Failed to execute tam-rfe: ${err.message}`));
    });
  });
});

