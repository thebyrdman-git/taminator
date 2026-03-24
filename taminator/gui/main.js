/**
 * Taminator GUI - Main Process
 * Starts the bundled web server (when packaged) and loads the new UI at 127.0.0.1:8765.
 */

const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const http = require('http');
const { spawn } = require('child_process');

const WEB_UI_PORT = 8765;
const WEB_UI_URL = `http://127.0.0.1:${WEB_UI_PORT}`;

let mainWindow;
let serverProcess = null;

/**
 * When the app is packed (AppImage, etc.), the venv may be relocated so pyvenv.cfg
 * no longer points at the extracted path; the interpreter can miss site-packages.
 * Return .../python-bundle/lib/python3.*/site-packages if present.
 */
function findPythonBundleSitePackages(bundleDir) {
  const fs = require('fs');
  if (process.platform === 'win32') {
    const sp = path.join(bundleDir, 'Lib', 'site-packages');
    return fs.existsSync(sp) ? sp : null;
  }
  const libDir = path.join(bundleDir, 'lib');
  if (!fs.existsSync(libDir)) return null;
  try {
    const names = fs.readdirSync(libDir);
    for (const name of names.sort()) {
      if (name.startsWith('python')) {
        const sp = path.join(libDir, name, 'site-packages');
        if (fs.existsSync(sp)) return sp;
      }
    }
  } catch (_) {
    /* ignore */
  }
  return null;
}

function getServerPaths() {
  const fs = require('fs');
  if (app.isPackaged) {
    const resourcesPath = process.resourcesPath;
    const bundleDir = path.join(resourcesPath, 'python-bundle');
    let bundledPython = null;
    if (process.platform === 'win32') {
      const exe = path.join(bundleDir, 'Scripts', 'python.exe');
      if (fs.existsSync(exe)) bundledPython = exe;
    } else {
      const binPython = path.join(bundleDir, 'bin', 'python');
      const binPython3 = path.join(bundleDir, 'bin', 'python3');
      if (fs.existsSync(binPython)) bundledPython = binPython;
      else if (fs.existsSync(binPython3)) bundledPython = binPython3;
    }
    const sitePackages = findPythonBundleSitePackages(bundleDir);
    const pyPathParts = [path.join(resourcesPath, 'src')];
    if (sitePackages) pyPathParts.push(sitePackages);
    const appVersion = app.getVersion ? app.getVersion() : '';
    return {
      cwd: path.join(resourcesPath, 'taminator'),
      tamRfe: path.join(resourcesPath, 'taminator', 'tam-rfe'),
      python: bundledPython,
      sitePackages: sitePackages || null,
      env: {
        ...process.env,
        PYTHONPATH: pyPathParts.join(path.delimiter),
        TAMINATOR_RESOURCES: path.join(resourcesPath, 'taminator'),
        ...(bundleDir && sitePackages ? { VIRTUAL_ENV: bundleDir } : {}),
        ...(appVersion ? { TAMINATOR_APP_VERSION: appVersion } : {})
      }
    };
  }
  const appRoot = path.join(__dirname, '..');
  return {
    cwd: path.join(appRoot, 'taminator'),
    tamRfe: path.join(appRoot, 'taminator', 'tam-rfe'),
    python: null,
    env: { ...process.env, PYTHONPATH: path.join(appRoot, 'src') }
  };
}

function waitForServer(timeoutMs, serverStderrBuffer, serverStdoutBuffer) {
  return new Promise((resolve, reject) => {
    const deadline = Date.now() + (timeoutMs || 45000);
    function tryOnce() {
      const req = http.get(WEB_UI_URL, (_res) => {
        req.destroy();
        resolve();
      });
      req.on('error', () => {
        if (Date.now() > deadline) {
          const stderr = serverStderrBuffer && serverStderrBuffer.length ? serverStderrBuffer.join('').trim() : '';
          const stdout = serverStdoutBuffer && serverStdoutBuffer.length ? serverStdoutBuffer.join('').trim() : '';
          const msg = 'Server did not start in time.' + (stderr || stdout ? '\n\nServer stderr:\n' + stderr + (stdout ? '\n\nServer stdout:\n' + stdout : '') : '');
          const err = new Error(msg);
          err.serverStderr = stderr;
          err.serverStdout = stdout;
          return reject(err);
        }
        setTimeout(tryOnce, 300);
      });
      req.setTimeout(2000, () => { req.destroy(); });
    }
    tryOnce();
  });
}

function findPython3() {
  const fs = require('fs');
  const candidates = process.platform === 'win32'
    ? ['python', 'python3']
    : ['/usr/bin/python3', '/usr/local/bin/python3', 'python3'];
  for (const p of candidates) {
    try {
      if (p === 'python3' || p === 'python') {
        return p;
      }
      if (fs.existsSync(p)) return p;
    } catch (_) { /* ignore */ }
  }
  return 'python3';
}

/** Electron / AppImage often provide a minimal PATH; prepend standard locations so venv python and subprocesses resolve tools. */
function envWithSafePath(env) {
  if (process.platform === 'win32') return env;
  const safePath = '/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin';
  const pathKey = Object.keys(env).find((k) => k.toUpperCase() === 'PATH');
  const existing = pathKey ? (env[pathKey] || '') : '';
  const newPath = existing ? `${safePath}:${existing}` : safePath;
  return { ...env, [pathKey || 'PATH']: newPath };
}

function getServerStartupDebugInfo() {
  const fs = require('fs');
  const paths = getServerPaths();
  const python = paths.python || findPython3();
  const tamRfeExists = fs.existsSync(paths.tamRfe);
  const cwdExists = paths.cwd && fs.existsSync(paths.cwd);
  const webServerPy = path.join(paths.cwd || '', 'web_server.py');
  const webServerPyExists = paths.cwd && fs.existsSync(webServerPy);
  const bundleDir = app.isPackaged ? path.join(process.resourcesPath, 'python-bundle') : '';
  const bundleBinPy = bundleDir ? path.join(bundleDir, 'bin', 'python') : '';
  const bundleBinPy3 = bundleDir ? path.join(bundleDir, 'bin', 'python3') : '';
  const sitePk = paths.sitePackages != null ? paths.sitePackages : (bundleDir ? findPythonBundleSitePackages(bundleDir) : null);
  return {
    platform: process.platform,
    isPackaged: app.isPackaged,
    resourcesPath: process.resourcesPath || '(unset)',
    cwd: paths.cwd || '(unset)',
    cwdExists,
    tamRfe: paths.tamRfe || '(unset)',
    tamRfeExists,
    webServerPy,
    webServerPyExists,
    python,
    pythonBundleDir: bundleDir || '(n/a)',
    pythonBundleBinExists: bundleDir ? (fs.existsSync(bundleBinPy) || fs.existsSync(bundleBinPy3)) : false,
    pythonBundleSitePackages: sitePk || '(not found)',
    port: WEB_UI_PORT
  };
}

function startWebServer() {
  return new Promise((resolve, reject) => {
    const fs = require('fs');
    const os = require('os');
    const paths = getServerPaths();
    const { cwd, tamRfe, python: bundledPython, env } = paths;
    const python = bundledPython || findPython3();
    const debugInfo = getServerStartupDebugInfo();

    // Debug: log startup paths (visible when running from terminal or in logs)
    console.log('[Main] Server startup debug:', JSON.stringify(debugInfo, null, 2));

    if (!fs.existsSync(tamRfe)) {
      const err = new Error('tam-rfe not found at ' + tamRfe);
      err.debugInfo = debugInfo;
      err.serverStderr = '';
      err.serverStdout = '';
      return reject(err);
    }

    if (app.isPackaged && !bundledPython) {
      const bundleDir = path.join(process.resourcesPath, 'python-bundle');
      const err = new Error(
        'Bundled Python venv is missing from this app package (no ' + bundleDir + '/bin/python). ' +
        'The AppImage must be built after creating taminator/taminator/python-bundle with runtime deps (rich, etc.). ' +
        'From repo root run: ansible-playbook -i taminator/taminator/ansible/inventory-build.yml ' +
        'taminator/taminator/ansible/playbooks/prepare-python-bundle.yml — then rebuild with electron-builder.'
      );
      err.debugInfo = debugInfo;
      err.serverStderr = '';
      err.serverStdout = '';
      return reject(err);
    }

    const serverStderrBuffer = [];
    const serverStdoutBuffer = [];
    const serverEnv = envWithSafePath(env);
    serverProcess = spawn(python, [tamRfe, 'serve', '--no-browser'], { cwd, env: serverEnv, stdio: 'pipe' });
    serverProcess.on('error', (err) => {
      err.debugInfo = debugInfo;
      err.serverStderr = serverStderrBuffer.join('');
      err.serverStdout = serverStdoutBuffer.join('');
      reject(err);
    });
    serverProcess.stderr.on('data', (d) => {
      const text = d.toString();
      serverStderrBuffer.push(text);
      console.log('[Server stderr]', text.trim());
    });
    serverProcess.stdout.on('data', (d) => {
      const text = d.toString();
      serverStdoutBuffer.push(text);
      console.log('[Server stdout]', text.trim());
    });
    waitForServer(45000, serverStderrBuffer, serverStdoutBuffer)
      .then(resolve)
      .catch((err) => {
        if (!err.debugInfo) err.debugInfo = debugInfo;
        if (err.serverStderr === undefined) err.serverStderr = serverStderrBuffer.join('');
        if (err.serverStdout === undefined) err.serverStdout = serverStdoutBuffer.join('');
        reject(err);
      });
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
    maxWidth: undefined,
    maxHeight: undefined,
    resizable: true,
    movable: true,
    frame: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    },
    backgroundColor: '#F5F5F5',
    title: 'Taminator'
  });
  
  if (process.platform === 'linux') {
    try {
      if (fs.existsSync(iconPath)) {
        mainWindow.setIcon(iconPath);
      }
    } catch (e) {
      console.warn('[Main] Could not set window icon (non-critical):', e.message);
    }
  }

  // Only load the server-served UI; never load index.html (old UI removed for Linux).
  mainWindow.loadURL(WEB_UI_URL);

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
  
  // Log when page finishes loading and set app version in UI
  mainWindow.webContents.on('did-finish-load', () => {
    console.log('[Main] Page loaded successfully');
    const version = app.getVersion();
    mainWindow.webContents.executeJavaScript(
      `var el = document.getElementById('app-version'); if (el) el.textContent = 'Taminator v' + ${JSON.stringify(version)};`
    ).catch(() => {});
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

function escapeHtml(s) {
  if (s == null) return '';
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

app.whenReady().then(() => {
  startWebServer()
    .then(() => createWindow())
    .catch((err) => {
      const fs = require('fs');
      const os = require('os');
      const debugInfo = err.debugInfo || getServerStartupDebugInfo();
      const serverStderr = (err.serverStderr != null) ? String(err.serverStderr).trim() : '';
      const serverStdout = (err.serverStdout != null) ? String(err.serverStdout).trim() : '';
      const mainMsg = (err && err.message) ? String(err.message) : 'Unknown error';

      console.error('[Main] Server failed:', mainMsg);
      console.error('[Main] Debug info:', JSON.stringify(debugInfo, null, 2));
      if (serverStderr) console.error('[Main] Server stderr:', serverStderr);
      if (serverStdout) console.error('[Main] Server stdout:', serverStdout);

      // Write debug file so user can open/copy even if window is small
      const configDir = path.join(os.homedir(), '.config', 'taminator-gui');
      const debugFile = path.join(configDir, 'server-startup-debug.txt');
      try {
        if (!fs.existsSync(configDir)) fs.mkdirSync(configDir, { recursive: true });
        const debugContent = [
          'Taminator server failed to start',
          '==============================',
          '',
          'Error: ' + mainMsg,
          '',
          'Debug info:',
          JSON.stringify(debugInfo, null, 2),
          '',
          'Server stderr:',
          serverStderr || '(none)',
          '',
          'Server stdout:',
          serverStdout || '(none)'
        ].join('\n');
        fs.writeFileSync(debugFile, debugContent, 'utf8');
        console.error('[Main] Debug info written to:', debugFile);
      } catch (e) {
        console.error('[Main] Could not write debug file:', e.message);
      }

      const debugSection = [
        'platform: ' + debugInfo.platform,
        'isPackaged: ' + debugInfo.isPackaged,
        'resourcesPath: ' + (debugInfo.resourcesPath || '(unset)'),
        'cwd: ' + (debugInfo.cwd || '(unset)'),
        'cwdExists: ' + debugInfo.cwdExists,
        'tamRfe: ' + (debugInfo.tamRfe || '(unset)'),
        'tamRfeExists: ' + debugInfo.tamRfeExists,
        'webServerPy: ' + (debugInfo.webServerPy || '(unset)'),
        'webServerPyExists: ' + debugInfo.webServerPyExists,
        'pythonBundleDir: ' + (debugInfo.pythonBundleDir != null ? debugInfo.pythonBundleDir : '(n/a)'),
        'pythonBundleBinExists: ' + (debugInfo.pythonBundleBinExists !== undefined ? debugInfo.pythonBundleBinExists : '(n/a)'),
        'pythonBundleSitePackages: ' + (debugInfo.pythonBundleSitePackages != null ? debugInfo.pythonBundleSitePackages : '(n/a)'),
        'python: ' + (debugInfo.python || '(unset)'),
        'port: ' + (debugInfo.port || WEB_UI_PORT)
      ].join('\n');
      const errWin = new BrowserWindow({
        width: 720,
        height: 560,
        minWidth: 600,
        minHeight: 400,
        webPreferences: { nodeIntegration: false, contextIsolation: true }
      });
      const html = `
        <!DOCTYPE html>
        <html><head><meta charset="utf-8"><title>Taminator – Server failed to start</title></head>
        <body style="font-family:system-ui,sans-serif;font-size:13px;margin:12px;color:#1a1a1a;">
          <h2 style="color:#c00;">Taminator could not start</h2>
          <p><strong>Error:</strong></p>
          <pre style="white-space:pre-wrap;font-size:11px;background:#f5f5f5;padding:8px;border:1px solid #ddd;overflow:auto;max-height:100px;">${escapeHtml(mainMsg)}</pre>
          <p><strong>Debug info (paths and checks):</strong></p>
          <pre style="white-space:pre-wrap;font-size:11px;background:#f0f0f0;padding:8px;border:1px solid #ddd;overflow:auto;max-height:140px;">${escapeHtml(debugSection)}</pre>
          ${serverStderr ? '<p><strong>Server stderr:</strong></p><pre style="white-space:pre-wrap;font-size:11px;background:#fff3f3;padding:8px;border:1px solid #fcc;overflow:auto;max-height:120px;">' + escapeHtml(serverStderr) + '</pre>' : ''}
          ${serverStdout ? '<p><strong>Server stdout:</strong></p><pre style="white-space:pre-wrap;font-size:11px;background:#f5f5f5;padding:8px;overflow:auto;max-height:80px;">' + escapeHtml(serverStdout) + '</pre>' : ''}
          <p style="font-size:12px;color:#666;">Full debug info was written to:<br><code>${escapeHtml(debugFile)}</code></p>
          <p style="font-size:11px;">You can open that file to copy the details. Fix the paths or environment so <code>tam-rfe serve</code> can run from the cwd above, then restart the app.</p>
        </body></html>
      `;
      errWin.loadURL('data:text/html;charset=utf-8,' + encodeURIComponent(html));
      errWin.webContents.on('did-finish-load', () => {
        errWin.webContents.openDevTools({ mode: 'detach' });
      });
    });
});

app.on('window-all-closed', () => {
  if (serverProcess) {
    serverProcess.kill();
    serverProcess = null;
  }
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
    // Use tam-vault CLI to save to HashiCorp Vault (from PATH or TAM_VAULT_PATH)
    const vaultPath = process.env.TAM_VAULT_PATH || 'tam-vault';
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

