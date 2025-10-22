/**
 * Taminator GUI - Main Process
 * Electron main process that creates the application window
 */

const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');
const crypto = require('crypto');
const os = require('os');

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
    // console.log('[Main] Page loaded successfully');
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
  // console.log('[Auth Check] Starting Node.js auth check...');
  
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
      // console.log('[Auth Check] VPN check failed:', e.message);
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
      // console.log('[Auth Check] JIRA token check failed:', e.message);
    }
    
    // Check Portal token
    try {
      const homeDir = os.homedir();
      const tokenFile = path.join(homeDir, '.config', 'pai', 'secrets', 'portal_token');
      result.portal_token = fs.existsSync(tokenFile) || !!process.env.PORTAL_TOKEN;
    } catch (e) {
      // console.log('[Auth Check] Portal token check failed:', e.message);
    }
    
    // console.log('[Auth Check] Result:', result);
    return result;
    
  } catch (error) {
    console.error('[Auth Check] Error:', error.message);
    return result;  // Return defaults on error
  }
});

// KB article search handler
ipcMain.handle('search-kb', async (event, searchParams) => {
  return new Promise((resolve, reject) => {
    const { spawn } = require('child_process');
    
    // Load portal token
    const tokens = loadAllTokens();
    const portalToken = tokens.portal?.value || '';
    
    // Determine correct path based on whether we're in development or production (AppImage)
    let basePath, kabManagerPath, pythonEnv;
    if (app.isPackaged) {
      // In production, Python scripts are in extraResources (directly in resources/)
      basePath = process.resourcesPath;
      kabManagerPath = path.join(basePath, 'src/taminator/tools/kab_manager.py');
      
      // Add bundled Python packages to PYTHONPATH and portal token
      const pythonPackagesPath = path.join(basePath, 'python_packages');
      pythonEnv = {
        ...process.env,
        PYTHONPATH: pythonPackagesPath + (process.env.PYTHONPATH ? ':' + process.env.PYTHONPATH : ''),
        RH_PORTAL_TOKEN: portalToken
      };
    } else {
      // In development
      basePath = path.join(__dirname, '..');
      kabManagerPath = path.join(basePath, 'src/taminator/tools/kab_manager.py');
      pythonEnv = {
        ...process.env,
        RH_PORTAL_TOKEN: portalToken
      };
    }
    
    // Build command args: --search query [product] [type] [limit]
    const args = [kabManagerPath, '--search', searchParams.query || ''];
    
    // Add optional parameters (must be in order: product, type, limit)
    if (searchParams.product) {
      args.push(searchParams.product);
    } else if (searchParams.type || searchParams.limit) {
      args.push('');  // Empty string for no product filter
    }
    
    if (searchParams.type) {
      args.push(searchParams.type);
    } else if (searchParams.limit) {
      args.push('');  // Empty string for no type filter
    }
    
    if (searchParams.limit) {
      args.push(searchParams.limit.toString());
    }
    
    // Spawn Python process
    const pythonProcess = spawn('python3', args, {
      cwd: basePath,
      env: pythonEnv
    });
    
    let stdoutData = '';
    let stderrData = '';
    
    pythonProcess.stdout.on('data', (data) => {
      stdoutData += data.toString();
    });
    
    pythonProcess.stderr.on('data', (data) => {
      stderrData += data.toString();
    });
    
    pythonProcess.on('close', (code) => {
      if (code === 0) {
        try {
          // Parse JSON output from Python
          const result = JSON.parse(stdoutData);
          resolve(result);
        } catch (error) {
          reject(new Error(`Failed to parse KB search results: ${error.message}`));
        }
      } else {
        reject(new Error(`KB search failed: ${stderrData || 'Unknown error'}`));
      }
    });
    
    pythonProcess.on('error', (error) => {
      reject(new Error(`Failed to execute KB search: ${error.message}`));
    });
  });
});

// T3 blog fetch handler
ipcMain.handle('fetch-t3-blogs', async () => {
  return new Promise((resolve, reject) => {
    const { spawn } = require('child_process');
    
    // Load portal token
    const tokens = loadAllTokens();
    const portalToken = tokens.portal?.value || '';
    
    // Determine correct path based on whether we're in development or production (AppImage)
    let basePath, t3ManagerPath, pythonEnv;
    if (app.isPackaged) {
      // In production, Python scripts are in extraResources (directly in resources/)
      basePath = process.resourcesPath;
      t3ManagerPath = path.join(basePath, 'src/taminator/tools/t3_manager.py');
      
      // Add bundled Python packages to PYTHONPATH and portal token
      const pythonPackagesPath = path.join(basePath, 'python_packages');
      pythonEnv = {
        ...process.env,
        PYTHONPATH: pythonPackagesPath + (process.env.PYTHONPATH ? ':' + process.env.PYTHONPATH : ''),
        RH_PORTAL_TOKEN: portalToken
      };
    } else {
      // In development
      basePath = path.join(__dirname, '..');
      t3ManagerPath = path.join(basePath, 'src/taminator/tools/t3_manager.py');
      pythonEnv = {
        ...process.env,
        RH_PORTAL_TOKEN: portalToken
      };
    }
    
    // Call with --json flag
    const args = [t3ManagerPath, '--json'];
    
    // Spawn Python process
    const pythonProcess = spawn('python3', args, {
      cwd: basePath,
      env: pythonEnv
    });
    
    let stdoutData = '';
    let stderrData = '';
    
    pythonProcess.stdout.on('data', (data) => {
      stdoutData += data.toString();
    });
    
    pythonProcess.stderr.on('data', (data) => {
      stderrData += data.toString();
    });
    
    pythonProcess.on('close', (code) => {
      if (code === 0) {
        try {
          // Parse JSON output from Python
          const blogs = JSON.parse(stdoutData);
          resolve({ success: true, blogs: blogs });
        } catch (error) {
          reject(new Error(`Failed to parse T3 blog results: ${error.message}`));
        }
      } else {
        reject(new Error(`T3 fetch failed: ${stderrData || 'Unknown error'}`));
      }
    });
    
    pythonProcess.on('error', (error) => {
      reject(new Error(`Failed to execute T3 fetch: ${error.message}`));
    });
  });
});

// Clear all data handler (for Reset All)
ipcMain.handle('clear-all-data', async () => {
  try {
    const { session } = require('electron');
    
    // Clear all caches and storage
    await session.defaultSession.clearStorageData({
      storages: ['localstorage', 'sessionstorage', 'indexdb', 'websql', 'serviceworkers', 'cachestorage']
    });
    
    // Clear cache
    await session.defaultSession.clearCache();
    
    // console.log('[Reset] All Electron storage cleared');
    return { success: true };
  } catch (error) {
    console.error('[Reset] Error clearing storage:', error);
    return { success: false, error: error.message };
  }
});

// GitLab issue submission handler
ipcMain.handle('submit-github-issue', async (event, issueData) => {
  return new Promise((resolve) => {
    // TODO: Implement direct GitLab API integration
    // For now, provide manual link to GitLab CEE
    
    // Format issue for GitLab (encode for URL)
    const title = encodeURIComponent(issueData.title || 'Untitled Issue');
    const description = encodeURIComponent(issueData.body || '');
    const labels = issueData.labels ? issueData.labels.join(',') : 'bug';
    
    // Generate GitLab CEE issue creation URL
    const gitlabUrl = `https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues/new?issue[title]=${title}&issue[description]=${description}`;
    
    // Simulate processing time
    setTimeout(() => {
      resolve({
        success: true,
        url: gitlabUrl,
        message: 'Issue template created. Click the link to submit to GitLab.',
        requiresManualSubmit: true
      });
    }, 500);
  });
});

// ========================================
// Token Management System
// ========================================

/**
 * Get the token storage directory
 */
function getTokenDir() {
  const configDir = path.join(os.homedir(), '.config', 'taminator');
  if (!fs.existsSync(configDir)) {
    fs.mkdirSync(configDir, { recursive: true, mode: 0o700 });
  }
  return configDir;
}

/**
 * Get the token file path
 */
function getTokenFilePath() {
  return path.join(getTokenDir(), 'tokens.enc');
}

/**
 * Simple encryption key (derived from machine ID)
 * NOTE: This is basic security. For production, consider using Electron's safeStorage API
 */
function getEncryptionKey() {
  // Use a combination of hostname and username as a simple key
  const identifier = `${os.hostname()}-${os.userInfo().username}-taminator-v1`;
  return crypto.createHash('sha256').update(identifier).digest();
}

/**
 * Encrypt token data
 */
function encryptData(data) {
  const key = getEncryptionKey();
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);
  
  let encrypted = cipher.update(JSON.stringify(data), 'utf8', 'hex');
  encrypted += cipher.final('hex');
  
  // Prepend IV to encrypted data
  return iv.toString('hex') + ':' + encrypted;
}

/**
 * Decrypt token data
 */
function decryptData(encryptedData) {
  try {
    const key = getEncryptionKey();
    const parts = encryptedData.split(':');
    const iv = Buffer.from(parts[0], 'hex');
    const encrypted = parts[1];
    
    const decipher = crypto.createDecipheriv('aes-256-cbc', key, iv);
    let decrypted = decipher.update(encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    
    return JSON.parse(decrypted);
  } catch (error) {
    console.error('Decryption error:', error);
    return null;
  }
}

/**
 * Load all tokens from encrypted storage
 */
function loadAllTokens() {
  const tokenFile = getTokenFilePath();
  
  if (!fs.existsSync(tokenFile)) {
    return {};
  }
  
  try {
    const encryptedData = fs.readFileSync(tokenFile, 'utf8');
    return decryptData(encryptedData) || {};
  } catch (error) {
    console.error('Error loading tokens:', error);
    return {};
  }
}

/**
 * Save all tokens to encrypted storage
 */
function saveAllTokens(tokens) {
  const tokenFile = getTokenFilePath();
  const encryptedData = encryptData(tokens);
  
  try {
    fs.writeFileSync(tokenFile, encryptedData, { mode: 0o600 });
    return true;
  } catch (error) {
    console.error('Error saving tokens:', error);
    return false;
  }
}

// IPC Handler: Save a token
ipcMain.handle('save-token', async (event, { type, token }) => {
  try {
    const tokens = loadAllTokens();
    
    tokens[type] = {
      value: token,
      savedAt: new Date().toISOString()
    };
    
    const success = saveAllTokens(tokens);
    
    if (success) {
      return { success: true, message: `${type} token saved successfully` };
    } else {
      throw new Error('Failed to save token to storage');
    }
  } catch (error) {
    console.error(`Error saving ${type} token:`, error);
    return { success: false, error: error.message };
  }
});

// IPC Handler: Load a token
ipcMain.handle('load-token', async (event, type) => {
  try {
    const tokens = loadAllTokens();
    
    if (tokens[type]) {
      return { 
        success: true, 
        token: tokens[type].value,
        savedAt: tokens[type].savedAt
      };
    } else {
      return { success: false, message: 'Token not found' };
    }
  } catch (error) {
    console.error(`Error loading ${type} token:`, error);
    return { success: false, error: error.message };
  }
});

// IPC Handler: Get token status (without revealing the actual token)
ipcMain.handle('get-token-status', async () => {
  try {
    const tokens = loadAllTokens();
    
    const status = {
      jira: tokens.jira ? { exists: true, savedAt: tokens.jira.savedAt } : { exists: false },
      portal: tokens.portal ? { exists: true, savedAt: tokens.portal.savedAt } : { exists: false },
      github: tokens.github ? { exists: true, savedAt: tokens.github.savedAt } : { exists: false }
    };
    
    return { success: true, status };
  } catch (error) {
    console.error('Error getting token status:', error);
    return { success: false, error: error.message };
  }
});

// IPC Handler: Test portal token by attempting a KB search
ipcMain.handle('test-portal-token', async () => {
  return new Promise((resolve, reject) => {
    try {
      const tokenResult = loadAllTokens();
      const portalToken = tokenResult.portal?.value;
      
      if (!portalToken) {
        resolve({ success: false, message: 'No portal token saved' });
        return;
      }
      
      // Determine correct path for kab_manager.py
      let basePath, kabManagerPath, pythonEnv;
      if (app.isPackaged) {
        basePath = process.resourcesPath;
        kabManagerPath = path.join(basePath, 'src/taminator/tools/kab_manager.py');
        const pythonPackagesPath = path.join(basePath, 'python_packages');
        pythonEnv = {
          ...process.env,
          PYTHONPATH: pythonPackagesPath + (process.env.PYTHONPATH ? ':' + process.env.PYTHONPATH : ''),
          RH_PORTAL_TOKEN: portalToken
        };
      } else {
        basePath = path.join(__dirname, '..');
        kabManagerPath = path.join(basePath, 'src/taminator/tools/kab_manager.py');
        pythonEnv = {
          ...process.env,
          RH_PORTAL_TOKEN: portalToken
        };
      }
      
      // Test with a simple search
      const args = [kabManagerPath, '--search', 'ansible', '', '', '1'];
      
      const pythonProcess = spawn('python3', args, {
        cwd: basePath,
        env: pythonEnv
      });
      
      let stdoutData = '';
      let stderrData = '';
      
      pythonProcess.stdout.on('data', (data) => {
        stdoutData += data.toString();
      });
      
      pythonProcess.stderr.on('data', (data) => {
        stderrData += data.toString();
      });
      
      pythonProcess.on('close', (code) => {
        if (code === 0 && stdoutData.trim()) {
          try {
            const result = JSON.parse(stdoutData);
            if (result.numFound !== undefined) {
              resolve({ 
                success: true, 
                message: `✓ Token valid - KB search returned ${result.numFound} results`,
                tested: true
              });
            } else {
              resolve({ success: false, message: 'Token may be invalid - unexpected response format' });
            }
          } catch (parseError) {
            resolve({ success: false, message: 'Token may be invalid - failed to parse KB response' });
          }
        } else {
          resolve({ 
            success: false, 
            message: `Token test failed: ${stderrData || 'Unknown error'}`,
            stderr: stderrData
          });
        }
      });
      
      // Timeout after 10 seconds
      setTimeout(() => {
        pythonProcess.kill();
        resolve({ success: false, message: 'Token test timed out (10s)' });
      }, 10000);
      
    } catch (error) {
      resolve({ success: false, message: `Test error: ${error.message}` });
    }
  });
});

// IPC Handler: Customer onboarding discovery
ipcMain.handle('onboard-discover', async (event, customerData) => {
  try {
    // For now, just save customer data to localStorage via return value
    // In production, this would query JIRA/Portal for RFEs/Bugs
    
    // Simulate discovery process
    return {
      success: true,
      customer: customerData,
      rfes: [],  // TODO: Implement actual RFE discovery
      bugs: [],  // TODO: Implement actual Bug discovery
      message: 'Customer onboarded successfully. RFE/Bug discovery is a future feature.'
    };
  } catch (error) {
    console.error('Error during customer onboarding:', error);
    return { success: false, error: error.message };
  }
});

// IPC Handler: Save user settings
ipcMain.handle('save-settings', async (event, settings) => {
  try {
    const configDir = getTokenDir(); // Reuse token directory for settings
    const settingsFile = path.join(configDir, 'settings.json');
    
    // Save settings as JSON
    fs.writeFileSync(settingsFile, JSON.stringify(settings, null, 2), { mode: 0o600 });
    
    return { success: true, message: 'Settings saved successfully' };
  } catch (error) {
    console.error('Error saving settings:', error);
    return { success: false, error: error.message };
  }
});

// IPC Handler: Load user settings
ipcMain.handle('load-settings', async () => {
  try {
    const configDir = getTokenDir();
    const settingsFile = path.join(configDir, 'settings.json');
    
    if (!fs.existsSync(settingsFile)) {
      // Return default settings
      return {
        success: true,
        settings: {
          email: '',
          autoUpdate: true,
          notifications: false,
          reportFormat: 'markdown',
          includeTimestamps: true,
          includeChangelog: true,
          reportsDir: '',
          jiraTimeout: '30',
          debugMode: false
        }
      };
    }
    
    const settingsData = fs.readFileSync(settingsFile, 'utf8');
    const settings = JSON.parse(settingsData);
    
    return { success: true, settings };
  } catch (error) {
    console.error('Error loading settings:', error);
    return { success: false, error: error.message };
  }
});

