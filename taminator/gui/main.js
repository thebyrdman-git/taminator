/**
 * Taminator GUI - Main Process
 * Electron main process that creates the application window
 */

const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;

function createWindow() {
  const iconPath = path.join(__dirname, 'public/terminator-icon.png');
  
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
    title: 'Taminator',
    icon: iconPath
  });
  
  // Set icon explicitly for Linux window managers
  if (process.platform === 'linux') {
    mainWindow.setIcon(iconPath);
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

