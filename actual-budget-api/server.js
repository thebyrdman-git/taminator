const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
require('dotenv').config();

// Import Actual Budget API
const actualApi = require('@actual-app/api');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());

// Configuration
const ACTUAL_CONFIG = {
  dataDir: '/tmp/actual-data', // Temporary directory for API operations
  serverURL: process.env.ACTUAL_SERVER_URL || 'https://money.jbyrd.org',
  password: process.env.ACTUAL_PASSWORD || '',
  budgetId: process.env.ACTUAL_BUDGET_ID || '',
  syncId: process.env.ACTUAL_SYNC_ID || 'fd118f31-1be9-4149-b094-2e75cd8ab59e'
};

// Initialize Actual Budget connection
async function initializeActual() {
  try {
    await actualApi.init({
      dataDir: ACTUAL_CONFIG.dataDir,
      serverURL: ACTUAL_CONFIG.serverURL,
    });
    
    console.log('✅ Actual Budget API initialized');
    
    // Download budget if sync ID is provided
    if (ACTUAL_CONFIG.syncId) {
      await actualApi.downloadBudget(ACTUAL_CONFIG.syncId);
      console.log('✅ Budget downloaded successfully');
    }
    
    return true;
  } catch (error) {
    console.error('❌ Failed to initialize Actual Budget:', error.message);
    return false;
  }
}

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'actual-budget-api',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

// Export budget data endpoint
app.post('/export', async (req, res) => {
  try {
    console.log('📤 Export request received');
    
    // Ensure Actual Budget is initialized
    const initialized = await initializeActual();
    if (!initialized) {
      return res.status(500).json({
        error: 'Failed to initialize Actual Budget connection'
      });
    }
    
    // Get all accounts
    const accounts = await actualApi.getAccounts();
    
    // Get all transactions (last 12 months by default)
    const since = req.body.since || new Date(Date.now() - 365 * 24 * 60 * 60 * 1000);
    const transactions = await actualApi.getTransactions(null, since);
    
    // Get categories
    const categories = await actualApi.getCategories();
    
    // Create export data
    const exportData = {
      timestamp: new Date().toISOString(),
      accounts: accounts,
      transactions: transactions,
      categories: categories,
      summary: {
        accountCount: accounts.length,
        transactionCount: transactions.length,
        categoryCount: categories.length
      }
    };
    
    console.log(`✅ Export completed: ${transactions.length} transactions, ${accounts.length} accounts`);
    
    res.json({
      success: true,
      data: exportData,
      message: `Successfully exported ${transactions.length} transactions`
    });
    
  } catch (error) {
    console.error('❌ Export failed:', error.message);
    res.status(500).json({
      success: false,
      error: error.message,
      message: 'Failed to export budget data'
    });
  }
});

// Get accounts endpoint
app.get('/accounts', async (req, res) => {
  try {
    console.log('📋 Accounts request received');
    
    // Ensure Actual Budget is initialized
    const initialized = await initializeActual();
    if (!initialized) {
      return res.status(500).json({
        error: 'Failed to initialize Actual Budget connection'
      });
    }
    
    const accounts = await actualApi.getAccounts();
    
    res.json({
      success: true,
      accounts: accounts,
      count: accounts.length
    });
    
  } catch (error) {
    console.error('❌ Get accounts failed:', error.message);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Get budget info endpoint
app.get('/budget-info', async (req, res) => {
  try {
    console.log('ℹ️  Budget info request received');
    
    const initialized = await initializeActual();
    if (!initialized) {
      return res.status(500).json({
        error: 'Failed to initialize Actual Budget connection'
      });
    }
    
    const accounts = await actualApi.getAccounts();
    const categories = await actualApi.getCategories();
    
    res.json({
      success: true,
      info: {
        budgetId: ACTUAL_CONFIG.budgetId,
        syncId: ACTUAL_CONFIG.syncId,
        serverURL: ACTUAL_CONFIG.serverURL,
        accountCount: accounts.length,
        categoryCount: categories.length,
        timestamp: new Date().toISOString()
      }
    });
    
  } catch (error) {
    console.error('❌ Get budget info failed:', error.message);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Error handling middleware
app.use((error, req, res, next) => {
  console.error('❌ Unhandled error:', error);
  res.status(500).json({
    success: false,
    error: 'Internal server error',
    message: error.message
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    success: false,
    error: 'Endpoint not found',
    message: `${req.method} ${req.path} is not a valid endpoint`
  });
});

// Start server
app.listen(PORT, () => {
  console.log('🚀 Actual Budget API Server Started');
  console.log(`📡 Server running on port ${PORT}`);
  console.log(`🔗 Health check: http://localhost:${PORT}/health`);
  console.log(`📤 Export endpoint: http://localhost:${PORT}/export`);
  console.log(`📋 Accounts endpoint: http://localhost:${PORT}/accounts`);
  console.log('');
});

// Graceful shutdown
process.on('SIGINT', async () => {
  console.log('\n🛑 Shutting down server...');
  try {
    await actualApi.shutdown();
    console.log('✅ Actual Budget API closed');
  } catch (error) {
    console.error('❌ Error during shutdown:', error.message);
  }
  process.exit(0);
});

process.on('SIGTERM', async () => {
  console.log('\n🛑 Received SIGTERM, shutting down...');
  try {
    await actualApi.shutdown();
    console.log('✅ Actual Budget API closed');
  } catch (error) {
    console.error('❌ Error during shutdown:', error.message);
  }
  process.exit(0);
});
