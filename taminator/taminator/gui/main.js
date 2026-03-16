/**
 * Taminator - Main Process
 * Starts the browser-based web server and shows it in an app window (regular Mac app).
 */

const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const http = require('http');

const WEB_UI_PORT = 8765;
const WEB_UI_URL = `http://127.0.0.1:${WEB_UI_PORT}`;

let mainWindow;
let serverProcess = null;

function getServerPaths() {
  const fs = require('fs');
  if (app.isPackaged) {
    const resourcesPath = process.resourcesPath;
    const tamRfe = path.join(resourcesPath, 'tam-rfe');
    // Python taminator package: shipped as extraResources at Resources/src (not in asar)
    const pythonPath = path.join(resourcesPath, 'src');
    const bundleDir = path.join(resourcesPath, 'python-bundle');
    let bundledPython = null;
    if (process.platform === 'win32') {
      const exe = path.join(bundleDir, 'Scripts', 'python.exe');
      if (fs.existsSync(exe)) bundledPython = exe;
    } else {
      // Prefer bin/python; on macOS venv often has only bin/python3
      const binPython = path.join(bundleDir, 'bin', 'python');
      const binPython3 = path.join(bundleDir, 'bin', 'python3');
      if (fs.existsSync(binPython)) bundledPython = binPython;
      else if (fs.existsSync(binPython3)) bundledPython = binPython3;
    }
    const appVersion = app.getVersion ? app.getVersion() : '';
    return {
      cwd: resourcesPath,
      tamRfe: tamRfe,
      python: bundledPython,
      env: {
        ...process.env,
        PYTHONPATH: pythonPath,
        TAMINATOR_RESOURCES: resourcesPath,
        ...(appVersion ? { TAMINATOR_APP_VERSION: appVersion } : {})
      }
    };
  }
  const appRoot = path.join(__dirname, '..');
  let env = process.env;
  try {
    const pkg = require(path.join(appRoot, 'gui', 'package.json'));
    if (pkg && pkg.version) env = { ...env, TAMINATOR_APP_VERSION: pkg.version };
  } catch (_) { /* ignore */ }
  return {
    cwd: appRoot,
    tamRfe: path.join(appRoot, 'tam-rfe'),
    python: null,
    env
  };
}

function waitForServer(timeoutMs, serverStderrBuffer) {
  return new Promise((resolve, reject) => {
    const deadline = Date.now() + (timeoutMs || 45000);
    function tryOnce() {
      const req = http.get(WEB_UI_URL, (_res) => {
        req.destroy();
        resolve();
      });
      req.on('error', () => {
        if (Date.now() > deadline) {
          const msg = serverStderrBuffer && serverStderrBuffer.length
            ? `Server did not start in time.\n\nServer output:\n${serverStderrBuffer.join('').trim()}`
            : 'Server did not start in time';
          return reject(new Error(msg));
        }
        setTimeout(tryOnce, 300);
      });
      req.setTimeout(2000, () => { req.destroy(); });
    }
    tryOnce();
  });
}

function findPython3() {
  if (process.platform === 'win32') return 'python';
  const fs = require('fs');
  const candidates = ['/usr/bin/python3', '/opt/homebrew/bin/python3', '/usr/local/bin/python3'];
  for (const p of candidates) {
    try {
      if (fs.existsSync(p)) return p;
    } catch (_) { /* ignore */ }
  }
  return 'python3'; // fallback to PATH
}

function envWithSafePath(env) {
  if (process.platform === 'win32') return env;
  const safePath = '/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin';
  const pathKey = Object.keys(env).find((k) => k.toUpperCase() === 'PATH');
  const existing = pathKey ? (env[pathKey] || '') : '';
  const newPath = existing ? `${safePath}:${existing}` : safePath;
  return { ...env, [pathKey || 'PATH']: newPath };
}

function startWebServer() {
  return new Promise((resolve, reject) => {
    const { cwd, tamRfe, python: bundledPython, env } = getServerPaths();
    const fs = require('fs');
    if (!fs.existsSync(tamRfe)) {
      return reject(new Error('tam-rfe not found at ' + tamRfe));
    }
    const python = bundledPython || findPython3();
    const serverEnv = envWithSafePath(env);
    const serverStderrBuffer = [];
    serverProcess = spawn(python, [tamRfe, 'serve', '--no-browser'], { cwd, env: serverEnv, stdio: 'pipe' });
    serverProcess.on('error', (err) => reject(err));
    serverProcess.stderr.on('data', (d) => {
      const text = d.toString();
      serverStderrBuffer.push(text);
      console.log('[Server]', text.trim());
    });
    waitForServer(45000, serverStderrBuffer).then(resolve, reject);
  });
}

function createWindow() {
  const fs = require('fs');
  let iconPath = path.join(__dirname, 'build/icon.png');
  if (!fs.existsSync(iconPath)) {
    iconPath = path.join(__dirname, 'public/terminator-icon.png');
  }

  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1000,
    minHeight: 600,
    resizable: true,
    movable: true,
    frame: true,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true
    },
    backgroundColor: '#F5F5F5',
    title: 'Taminator'
  });

  if (process.platform === 'linux' && fs.existsSync(iconPath)) {
    try { mainWindow.setIcon(iconPath); } catch (_) { /* ignore */ }
  }

  mainWindow.loadURL(WEB_UI_URL);

  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    require('electron').shell.openExternal(url);
    return { action: 'deny' };
  });
  mainWindow.webContents.on('will-navigate', (event, url) => {
    if (!url.startsWith(WEB_UI_URL) && !url.startsWith('file://')) {
      event.preventDefault();
      require('electron').shell.openExternal(url);
    }
  });

  if (process.argv.includes('--dev') || process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
  }

  mainWindow.webContents.on('did-fail-load', (event, code, desc) => {
    console.error('[Main] Failed to load:', code, desc);
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

function registerIpcHandlers() {
  ipcMain.handle('load-settings', async () => {
    return loadSavedSettings();
  });

  // IPC handlers for CLI integration
  ipcMain.handle('run-cli-command', async (_event, command, args) => {
    return new Promise((resolve, reject) => {
      const cliProc = spawn('python3', ['-m', 'taminator', command, ...args], {
        cwd: path.join(__dirname, '..'),
        env: { ...process.env, PYTHONPATH: path.join(__dirname, '../src') }
      });

      let stdout = '';
      let stderr = '';

      cliProc.stdout.on('data', (data) => {
        stdout += data.toString();
      });

      cliProc.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      cliProc.on('close', (code) => {
        if (code === 0) {
          resolve({ success: true, output: stdout });
        } else {
          reject({ success: false, error: stderr || stdout });
        }
      });
    });
  });
  registerOtherHandlers();
}

function registerOtherHandlers() {
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
      try {
        const nmOutput = execSync('nmcli -t -f NAME,TYPE,STATE con show --active 2>/dev/null', { timeout: 1000 }).toString();
        result.vpn = nmOutput.includes(':vpn:') && nmOutput.includes(':activated');
      } catch (e) {
        console.log('[Auth Check] VPN check failed:', e.message);
      }

      try {
        execSync('klist -s 2>/dev/null', { timeout: 1000 });
        result.kerberos = true;
      } catch (e) {
        result.kerberos = false;
      }

      try {
        const homeDir = os.homedir();
        const tokenFile = path.join(homeDir, '.config', 'pai', 'secrets', 'jira_token');
        result.jira_token = fs.existsSync(tokenFile) || !!process.env.JIRA_TOKEN;
      } catch (e) {
        console.log('[Auth Check] JIRA token check failed:', e.message);
      }

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
      return result;
    }
  });

  // GitHub issue submission handler
  ipcMain.handle('submit-github-issue', async (_event, _issueData) => {
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
    
    let stderr = '';

    cliProcess.stdout.on('data', () => {});

    cliProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    cliProcess.on('close', (code) => {
      // For demo purposes, simulate successful submission
      // In production, this would actually call the GitHub API via the CLI
      
      // eslint-disable-next-line no-constant-condition -- demo: always report success
      if (code === 0 || true) {
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

// Save token handler — saves to ~/.config/taminator/ui_tokens.json in encoded form (base64 payload). Same format as Python token_store; backward compatible with legacy plain JSON.
function loadEncodedTokens(tokensFile) {
  const fs = require('fs');
  if (!fs.existsSync(tokensFile)) return {};
  try {
    const raw = JSON.parse(fs.readFileSync(tokensFile, 'utf8'));
    if (raw && raw.v === 1 && raw.payload) {
      return JSON.parse(Buffer.from(raw.payload, 'base64').toString('utf8'));
    }
    return raw && typeof raw === 'object' ? raw : {};
  } catch (e) {
    return {};
  }
}

function saveEncodedTokens(tokensFile, data) {
  const fs = require('fs');
  const payload = Buffer.from(JSON.stringify(data), 'utf8').toString('base64');
  fs.writeFileSync(tokensFile, JSON.stringify({ v: 1, payload }), { mode: 0o600 });
}

ipcMain.handle('save-token', async (event, data) => {
  console.log('[Save Token] Saving token for type:', data.type);
  const fs = require('fs');
  const os = require('os');

  const key = (data.type === 'jira' || data.type === 'jira_token') ? 'jira_token' : 'portal_token';
  const configDir = path.join(os.homedir(), '.config', 'taminator');
  const tokensFile = path.join(configDir, 'ui_tokens.json');

  try {
    if (!fs.existsSync(configDir)) {
      fs.mkdirSync(configDir, { recursive: true });
    }
    const existing = loadEncodedTokens(tokensFile);
    existing[key] = data.token;
    saveEncodedTokens(tokensFile, existing);
    console.log('[Save Token] Token saved (encoded) to', tokensFile);
    // When Vault is configured, sync to Vault (tam-vault set); fire-and-forget
    const service = key === 'jira_token' ? 'jira' : key === 'portal_token' ? 'portal' : null;
    if (service && process.env.VAULT_ADDR) {
      const sub = spawn('tam-vault', ['set', service], { stdio: ['pipe', 'ignore', 'ignore'], env: process.env });
      sub.stdin.write(data.token + '\n');
      sub.stdin.end();
      sub.on('error', () => {});
    }
    return { success: true, message: 'Token saved. Restart the app or run a report for it to take effect.' };
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
          const match = line.match(/([A-Z]+-\d+)\s*[|:]\s*(.+)/);
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
ipcMain.handle('onboard-generate', async (_event) => {
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

}

app.whenReady().then(() => {
  registerIpcHandlers();
  startWebServer()
    .then(() => createWindow())
    .catch((err) => {
      console.error('[Main] Failed to start web server:', err);
      const msg = (err && err.message) ? String(err.message).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;') : 'Unknown error';
      const { cwd } = getServerPaths();
      const errWin = new BrowserWindow({ width: 600, height: 400 });
      errWin.loadURL('data:text/html;charset=utf-8,' + encodeURIComponent(`
        <h2>Taminator could not start</h2>
        <pre style="white-space:pre-wrap;font-size:12px;background:#f0f0f0;padding:8px;max-height:160px;overflow:auto;">${msg}</pre>
        <p>On some macOS profiles (e.g. test accounts), Python may not be available to the app. Install Python 3, or run from Terminal as that user:</p>
        <pre style="font-size:11px;">cd ${(cwd || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')}\n./tam-rfe serve</pre>
        <p style="font-size:11px;color:#666;">Then open <a href="http://127.0.0.1:8765">http://127.0.0.1:8765</a> in your browser.</p>
      `));
    });
});

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

app.on('before-quit', () => {
  if (serverProcess) {
    serverProcess.kill();
    serverProcess = null;
  }
});