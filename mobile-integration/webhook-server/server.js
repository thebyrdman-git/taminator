#!/usr/bin/env node

/**
 * PAI Mobile Google Assistant Integration Webhook Server
 * Handles Google Assistant voice commands and routes them to PAI tools
 * 
 * Architecture:
 * Google Assistant → Dialogflow → This Webhook → PAI Tools → Response
 */

const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const { exec } = require('child_process');
const { promisify } = require('util');
const { v4: uuidv4 } = require('uuid');

// Configuration
const config = {
  port: process.env.PORT || 3001,
  paiToolsPath: '/home/jbyrd/hatter-pai/bin',
  logLevel: process.env.LOG_LEVEL || 'info',
  maxExecutionTime: 30000, // 30 seconds
  environment: process.env.NODE_ENV || 'development'
};

// Initialize Express app
const app = express();
const execAsync = promisify(exec);

// Middleware
app.use(helmet());
app.use(cors());
app.use(bodyParser.json());
app.use(morgan('combined'));

// Request logging middleware
app.use((req, res, next) => {
  req.requestId = uuidv4();
  console.log(`[${new Date().toISOString()}] [${req.requestId}] ${req.method} ${req.path}`);
  next();
});

/**
 * PAI Command Router - Routes Dialogflow intents to PAI tools
 */
class PAICommandRouter {
  constructor() {
    this.commandMap = {
      // Plex Management Commands
      'plex.status': () => this.executePAITool('pai-plex-remote', ['status']),
      'plex.libraries': () => this.executePAITool('pai-plex-remote', ['libraries']),
      'plex.health': () => this.executePAITool('pai-plex-remote', ['health-check']),
      'plex.activity': () => this.executePAITool('pai-plex-remote', ['recent-activity']),
      
      // Context Management
      'context.switch': (params) => this.executePAITool('pai-context-switch', [params.context || 'default']),
      'context.current': () => this.executePAITool('pai-context-current', []),
      
      // System Status
      'system.status': () => this.executePAITool('pai-status-show', []),
      'system.health': () => this.executePAITool('pai-audit', []),
      
      // Meal Planning
      'meal.plan': () => this.executePAITool('pai-meal-planner', ['generate']),
      'meal.shopping': () => this.executePAITool('pai-shopping-list', ['show']),
      
      // Case Management (Red Hat specific)
      'case.status': () => this.executePAITool('pai-case-processor', ['status']),
      'case.sync': () => this.executePAITool('pai-hourly-case-sync', []),
      
      // Email Management
      'email.sync': () => this.executePAITool('pai-email-sync', []),
      'email.process': () => this.executePAITool('pai-email-processor', []),
    };
  }

  /**
   * Execute PAI tool with arguments
   */
  async executePAITool(toolName, args = []) {
    const toolPath = `${config.paiToolsPath}/${toolName}`;
    const command = `${toolPath} ${args.join(' ')}`;
    
    console.log(`[PAI] Executing: ${command}`);
    
    try {
      const { stdout, stderr } = await execAsync(command, {
        timeout: config.maxExecutionTime,
        cwd: config.paiToolsPath
      });
      
      return {
        success: true,
        output: stdout.trim(),
        error: stderr ? stderr.trim() : null,
        command: toolName,
        args: args
      };
    } catch (error) {
      console.error(`[PAI] Error executing ${toolName}:`, error.message);
      return {
        success: false,
        output: null,
        error: error.message,
        command: toolName,
        args: args
      };
    }
  }

  /**
   * Route intent to appropriate PAI command
   */
  async routeCommand(intent, parameters = {}) {
    if (this.commandMap[intent]) {
      return await this.commandMap[intent](parameters);
    } else {
      return {
        success: false,
        output: null,
        error: `Unknown intent: ${intent}`,
        command: 'unknown',
        args: []
      };
    }
  }
}

/**
 * Response Formatter - Formats PAI output for Google Assistant
 */
class ResponseFormatter {
  
  /**
   * Format successful PAI response for Google Assistant
   */
  formatSuccess(paiResult, intent) {
    const output = paiResult.output || '';
    
    // Context-specific formatting
    switch (intent) {
      case 'plex.status':
        return this.formatPlexStatus(output);
      case 'plex.libraries':
        return this.formatPlexLibraries(output);
      case 'context.current':
        return `Your current PAI context is: ${output}`;
      case 'meal.plan':
        return this.formatMealPlan(output);
      default:
        return this.formatGenericSuccess(output, intent);
    }
  }

  /**
   * Format error response for Google Assistant
   */
  formatError(error, intent) {
    const friendlyErrors = {
      'plex.status': 'Sorry, I couldn\'t check the Plex server status right now.',
      'context.switch': 'I had trouble switching contexts. Please try again.',
      'meal.plan': 'I couldn\'t generate a meal plan at the moment.',
      'default': 'I encountered an issue processing that request.'
    };

    return friendlyErrors[intent] || friendlyErrors['default'];
  }

  /**
   * Format Plex status for voice response
   */
  formatPlexStatus(output) {
    if (output.includes('Server is running')) {
      return 'Plex server is running smoothly. All systems are operational.';
    } else if (output.includes('Server appears to be down')) {
      return 'The Plex server appears to be offline. You may want to check the connection.';
    } else {
      return 'I checked the Plex server, but the status is unclear. Here\'s what I found: ' + output.substring(0, 100);
    }
  }

  /**
   * Format Plex libraries for voice response
   */
  formatPlexLibraries(output) {
    const lines = output.split('\n').filter(line => line.trim());
    if (lines.length > 0) {
      return `You have ${lines.length} Plex libraries configured, including your main media collections.`;
    } else {
      return 'I couldn\'t retrieve the Plex library information right now.';
    }
  }

  /**
   * Format meal planning response
   */
  formatMealPlan(output) {
    if (output.includes('meal plan generated') || output.includes('planning')) {
      return 'I\'ve generated a meal plan for you. Check your PAI system for the details.';
    } else {
      return 'Meal planning is ready. Your options have been prepared in the PAI system.';
    }
  }

  /**
   * Format generic successful response
   */
  formatGenericSuccess(output, intent) {
    if (!output || output.trim() === '') {
      return 'Done! The command completed successfully.';
    }
    
    // Truncate long responses for voice
    const maxLength = 200;
    if (output.length > maxLength) {
      return output.substring(0, maxLength) + '... Task completed successfully.';
    }
    
    return output;
  }

  /**
   * Create Google Assistant response object
   */
  createGoogleResponse(speechText, displayText = null) {
    return {
      fulfillmentText: displayText || speechText,
      fulfillmentMessages: [
        {
          text: {
            text: [displayText || speechText]
          }
        }
      ],
      source: 'pai-webhook'
    };
  }
}

// Initialize components
const commandRouter = new PAICommandRouter();
const responseFormatter = new ResponseFormatter();

/**
 * Main webhook endpoint for Google Assistant/Dialogflow
 */
app.post('/webhook', async (req, res) => {
  const requestId = req.requestId;
  
  try {
    console.log(`[${requestId}] Webhook request received`);
    console.log(`[${requestId}] Body:`, JSON.stringify(req.body, null, 2));
    
    // Extract intent and parameters from Dialogflow request
    const intent = req.body.queryResult?.intent?.displayName;
    const parameters = req.body.queryResult?.parameters || {};
    const queryText = req.body.queryResult?.queryText;
    
    console.log(`[${requestId}] Intent: ${intent}, Query: ${queryText}`);
    
    if (!intent) {
      throw new Error('No intent found in request');
    }

    // Route command to PAI
    const paiResult = await commandRouter.routeCommand(intent, parameters);
    console.log(`[${requestId}] PAI Result:`, paiResult);

    // Format response for Google Assistant
    let responseText;
    if (paiResult.success) {
      responseText = responseFormatter.formatSuccess(paiResult, intent);
    } else {
      responseText = responseFormatter.formatError(paiResult.error, intent);
    }

    const googleResponse = responseFormatter.createGoogleResponse(responseText);
    
    console.log(`[${requestId}] Sending response: ${responseText}`);
    res.json(googleResponse);

  } catch (error) {
    console.error(`[${requestId}] Webhook error:`, error.message);
    
    const errorResponse = responseFormatter.createGoogleResponse(
      'Sorry, I encountered an issue processing that request. Please try again later.'
    );
    
    res.status(500).json(errorResponse);
  }
});

/**
 * Health check endpoint
 */
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    uptime: process.uptime()
  });
});

/**
 * Test endpoint for development
 */
app.post('/test', async (req, res) => {
  try {
    const { intent, parameters = {} } = req.body;
    
    if (!intent) {
      return res.status(400).json({ error: 'Intent required' });
    }

    const result = await commandRouter.routeCommand(intent, parameters);
    res.json({
      intent,
      parameters,
      paiResult: result,
      formattedResponse: result.success 
        ? responseFormatter.formatSuccess(result, intent)
        : responseFormatter.formatError(result.error, intent)
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

/**
 * List available intents
 */
app.get('/intents', (req, res) => {
  const intents = Object.keys(commandRouter.commandMap);
  res.json({
    intents,
    total: intents.length,
    categories: {
      plex: intents.filter(i => i.startsWith('plex.')),
      context: intents.filter(i => i.startsWith('context.')),
      system: intents.filter(i => i.startsWith('system.')),
      meal: intents.filter(i => i.startsWith('meal.')),
      case: intents.filter(i => i.startsWith('case.')),
      email: intents.filter(i => i.startsWith('email.'))
    }
  });
});

// Error handling middleware
app.use((error, req, res, next) => {
  console.error(`[${req.requestId}] Unhandled error:`, error);
  res.status(500).json({
    error: 'Internal server error',
    requestId: req.requestId
  });
});

// Start server
const server = app.listen(config.port, () => {
  console.log(`\n🚀 PAI Mobile Webhook Server Started`);
  console.log(`   Port: ${config.port}`);
  console.log(`   Environment: ${config.environment}`);
  console.log(`   PAI Tools Path: ${config.paiToolsPath}`);
  console.log(`   Health Check: http://localhost:${config.port}/health`);
  console.log(`   Test Endpoint: http://localhost:${config.port}/test`);
  console.log(`   Available Intents: http://localhost:${config.port}/intents\n`);
});

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\n🔴 Received SIGINT, shutting down gracefully...');
  server.close(() => {
    console.log('✅ Server closed successfully');
    process.exit(0);
  });
});

process.on('SIGTERM', () => {
  console.log('\n🔴 Received SIGTERM, shutting down gracefully...');
  server.close(() => {
    console.log('✅ Server closed successfully');  
    process.exit(0);
  });
});

module.exports = app;
