# 📱 PAI Mobile Google Assistant Integration - Setup Guide

## 🎯 Overview
This guide walks you through setting up "Hey Google" integration with your PAI (Personal AI Infrastructure) system, enabling voice commands like:

- "Hey Google, ask PAI to check Plex status"
- "Hey Google, tell PAI to switch to work context" 
- "Hey Google, have PAI plan my meals"

## 🏗️ Architecture
```
Mobile Device → "Hey Google" → Google Assistant → Dialogflow → Webhook Server → PAI Tools
```

## ✅ Prerequisites
- Node.js 16+ installed
- PAI system properly configured
- Google Cloud account (for Dialogflow)
- Domain with HTTPS (for production webhook)

## 🚀 Phase 1: Local Setup & Testing

### Step 1: Install & Start Webhook Server
```bash
# Install dependencies
pai-mobile-webhook install

# Start the webhook server  
pai-mobile-webhook start

# Test functionality
pai-mobile-webhook test
```

The webhook server will be running at: `http://localhost:3001`

### Step 2: Test Available Commands
```bash
# Check server health
curl http://localhost:3001/health

# List available intents
curl http://localhost:3001/intents

# Test a PAI command
curl -X POST http://localhost:3001/test \
  -H "Content-Type: application/json" \
  -d '{"intent": "plex.status"}'
```

## 🌐 Phase 2: Google Cloud Setup

### Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project: `pai-mobile-assistant`
3. Enable APIs:
   - Dialogflow API
   - Google Assistant API
   - Cloud Functions API (if using serverless)

### Step 2: Set up Dialogflow
1. Go to [Dialogflow Console](https://dialogflow.cloud.google.com/)
2. Create new agent: "PAI Mobile Assistant"
3. Import intents from: `mobile-integration/dialogflow-config/intents-config.json`
4. Configure webhook URL: `https://your-domain.com/webhook`

### Step 3: Configure Webhook URL
For development (using ngrok):
```bash
# Install ngrok if not already installed
npm install -g ngrok

# Expose local server
ngrok http 3001

# Use the HTTPS URL in Dialogflow webhook settings
```

For production:
- Deploy webhook server to your preferred hosting platform
- Use HTTPS URL in Dialogflow webhook settings

## 🎯 Phase 3: Available PAI Intents

### Plex Management
- **plex.status**: "Check Plex server status"
- **plex.libraries**: "Show my Plex libraries"
- **plex.health**: "Run Plex health check"
- **plex.activity**: "Show current Plex activity"

### Context Management  
- **context.switch**: "Switch to work context"
- **context.current**: "What's my current context?"

### System Operations
- **system.status**: "Show PAI system status"
- **system.health**: "Run system health check"

### Meal Planning
- **meal.plan**: "Plan my meals for the week"
- **meal.shopping**: "Show my shopping list"

### Work Integration (Red Hat)
- **case.status**: "Check my case status"
- **case.sync**: "Sync my support cases"

### Email Management
- **email.sync**: "Sync my emails"
- **email.process**: "Process recent emails"

## 🎙️ Example Voice Commands

### Basic Usage
```
"Hey Google, ask PAI to check server status"
"Hey Google, tell PAI to show Plex libraries"
"Hey Google, have PAI switch to work context"
```

### Advanced Usage
```
"Hey Google, ask PAI to run a health check"
"Hey Google, tell PAI to plan meals for this week"
"Hey Google, have PAI sync my support cases"
```

## 🔧 Troubleshooting

### Common Issues

#### Webhook Server Won't Start
```bash
# Check if port is in use
netstat -tulpn | grep :3001

# Kill existing processes if needed
pkill -f "node.*server.js"

# Restart server
pai-mobile-webhook restart
```

#### PAI Commands Not Working
```bash
# Test PAI tools directly
pai-plex-remote status
pai-context-current
pai-status-show

# Check webhook logs
pai-mobile-webhook logs
```

#### Google Assistant Not Responding
1. Check Dialogflow webhook URL is accessible
2. Verify webhook is returning valid JSON
3. Test webhook endpoint manually:
```bash
curl -X POST https://your-domain.com/webhook \
  -H "Content-Type: application/json" \
  -d '{"queryResult":{"intent":{"displayName":"plex.status"},"parameters":{}}}'
```

## 📊 Monitoring & Logs

### Server Logs
```bash
# View recent logs
pai-mobile-webhook logs

# Follow logs in real-time
tail -f ~/.config/pai/mobile-webhook.log
```

### Health Monitoring
```bash
# Check server status
pai-mobile-webhook status

# Test all endpoints
pai-mobile-webhook test
```

## 🔐 Production Considerations

### Security
- Use HTTPS for webhook endpoints
- Implement request validation
- Add authentication/authorization
- Set up proper firewall rules

### Scalability
- Consider using Google Cloud Functions
- Implement request queuing for long-running PAI commands
- Add rate limiting

### Reliability
- Set up health checks and monitoring
- Implement graceful error handling
- Add backup webhook endpoints

## 🎨 Customization

### Adding New PAI Commands
1. Add command to `server.js` commandMap
2. Create corresponding Dialogflow intent
3. Test with webhook test endpoint

### Custom Response Formatting
Modify the `ResponseFormatter` class in `server.js` to customize how PAI output is converted to Google Assistant responses.

### Context-Specific Commands
Use the `context.switch` intent to enable context-aware command routing based on your current PAI context.

---

## 🎉 Next Steps

Once basic functionality is working:
1. Deploy to production environment
2. Set up monitoring and alerting
3. Add advanced features like command chaining
4. Integrate with additional PAI contexts
5. Create custom Actions for Google Assistant directory

For support, check the PAI system logs and webhook server logs, or refer to the main PAI documentation.

---
*PAI Mobile Google Assistant Integration*  
*Part of the Personal AI Infrastructure (PAI) System*  
*Created by Hatter - Red Hat Digital Assistant*
