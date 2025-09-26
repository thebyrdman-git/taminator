# Personal PAI - Home AI Infrastructure 

Personal AI Infrastructure for home automation, media management, and energy optimization.

## 🏠 What This Is

**Hatter** - Your personal AI assistant for smart home management, based on Red Hat's PAI framework but customized for home use.

### Key Capabilities

🏡 **Home Automation**
- Home Assistant integration with 432+ devices
- Energy monitoring and optimization (Green Button data support)
- Smart scheduling and automation templates
- IoT security monitoring

🎬 **Media Management** 
- Plex Media Server management (miraclemax server)
- Library organization and optimization
- Remote server administration

⚡ **Energy Optimization**
- Real-time cost monitoring and alerts  
- Smart device scheduling (Xbox auto-shutdown, camera scheduling)
- Peak hours optimization (projected $54.50/month savings)
- Green Button utility data integration

🤖 **Private AI Processing**
- LiteLLM integration for data sovereignty
- Context-aware task management
- Anti-dilution focused contexts

## 🚀 Quick Start

```bash
# Switch to home automation context
pai-context-switch home-automation

# Check Home Assistant status
pai-home-assistant status

# Analyze energy usage
pai-energy-optimize analyze

# Set up Plex management
pai-plex-remote setup

# Create focused task context  
pai-context-task plex-management
```

## 🛠️ Available Tools

### Core PAI System
- `pai-context-switch` - Switch between home, plex, finance, etc.
- `pai-context-task` - Create focused task contexts (prevents AI dilution)
- `pai-rules-generate` - Generate Cursor AI rules for contexts

### Home Automation
- `pai-home-assistant` - HA integration (secure token management)
- `pai-energy-optimize` - Energy analysis and optimization
- `pai-energy-scheduler` - Smart automation generation
- `pai-iot-security` - Network security monitoring

### Media & Entertainment  
- `pai-plex-remote` - Plex server management (miraclemax)
- `pai-plex-library-organizer` - Media library organization

### Energy Management
- `pai-greenbutton-import` - Utility data import and analysis
- `pai-energy-dashboard` - Real-time monitoring
- `pai-energy-discovery` - Device power profiling

## 🏗️ System Architecture

```
miraclemax (HP Server - 192.168.1.34)
├── Home Assistant VM (192.168.1.39)  
│   └── 432 smart home devices
│   └── DuckDNS SSL: byrdhome.duckdns.org
└── Plex Media Server (192.168.1.17)
    └── Byrd Library media collection

Local PAI Client (Fedora)
├── ~/.config/pai/secrets/ (GPG encrypted tokens)
├── ~/hatter-pai/ (this repository)
└── Context management & AI tools
```

## 🔐 Security & Privacy

- **All tokens GPG encrypted** in `~/.config/pai/secrets/`
- **No hardcoded credentials** in any scripts
- **Personal data stays local** (customer/case files gitignored)
- **Data sovereignty** via LiteLLM for sensitive processing

## 📊 Energy Optimization Results

**Smart Automations Deployed:**
- Xbox auto-shutdown after 2hrs idle (nights/weekdays)  
- Camera motion detection scheduling (2-6 AM pause)
- Peak hours alerts (5-9 PM weekdays)
- Load balancing recommendations

**Projected Annual Savings: $654** 💰

## 🤖 AI Context Management

Smart context switching prevents AI dilution:

```bash
# System-wide contexts
pai-context-switch plex          # Media server focus
pai-context-switch home-automation # Smart home focus  
pai-context-switch finance       # Budget & investment focus

# Task-specific contexts (anti-dilution)
pai-context-task plex-management      # Focused Plex work
pai-context-task energy-optimization  # Focused energy work
```

Each context provides:
- ✅ Specialized tool access
- ✅ Relevant knowledge base  
- ✅ Context-appropriate AI behavior
- ✅ Reduced cognitive load

---

**Built on Red Hat PAI Framework** | **Home AI Infrastructure** | **Privacy-First Design**