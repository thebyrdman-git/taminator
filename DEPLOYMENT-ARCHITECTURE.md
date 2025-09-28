# PAI Deployment Architecture

## Primary Deployment Target: miraclemax (HP Server)

All PAI automation systems are designed to run on **miraclemax** - the HP server infrastructure.

### Deployment Options on miraclemax

#### Option 1: Container Deployment (Recommended)
- **Platform**: Docker/Podman containers on miraclemax
- **Benefits**: Isolated, reproducible, easy to manage
- **Storage**: Mounted volumes to NFS shares
- **Network**: Direct access to home network services

#### Option 2: Virtual Machine Deployment
- **Platform**: VM on miraclemax hypervisor
- **Benefits**: Full OS isolation, dedicated resources
- **Storage**: VM disk + NFS mounts
- **Network**: Bridged to home network

### Current Architecture

```
miraclemax (HP Server)
├── Container/VM: YouTube-Plex Automation
│   ├── Storage: /mnt/nfs_share/charles/youtube/
│   ├── Database: ~/.config/pai/youtube/
│   ├── Logs: ~/.config/pai/logs/
│   └── Cron: Automated scheduling
├── Container/VM: [Future Contexts]
│   └── Each context gets isolated environment
└── Shared Resources
    ├── NFS Storage Access
    ├── Plex Server Integration (192.168.1.17)
    └── Network Services
```

### Deployment Standards

#### **PRIORITY #1: VISUALLY STUNNING**
- All containers/VMs include beautiful progress bars
- Unified visual experience across deployments
- Consistent emoji and color schemes

#### Storage Configuration
- **YouTube Content**: `/mnt/nfs_share/charles/youtube/`
- **Configuration**: `~/.config/pai/`
- **Logs**: `~/.config/pai/logs/`
- **Databases**: `~/.config/pai/[context]/`

#### Network Configuration
- **Plex Server**: 192.168.1.17:32400
- **miraclemax**: Primary compute platform
- **Home Network**: Full integration access

#### Security Standards
- **Secrets**: GPG-encrypted in `~/.config/pai/secrets/`
- **No Hardcoding**: All sensitive data from secure storage
- **Repository Safety**: No secrets in Git repositories
- **Red Hat Compliance**: All operations audit-logged

### Container/VM Resource Allocation

#### YouTube-Plex Automation
- **CPU**: 2 cores minimum
- **RAM**: 4GB minimum  
- **Storage**: 50GB + NFS mounts
- **Network**: Bridged access to home network

#### Future Context Deployments
- **Scalable**: Each context in separate container/VM
- **Resource Isolation**: Dedicated resources per context
- **Shared Services**: Common PAI infrastructure

### Automation Scheduling

All automation runs on miraclemax with:
- **Cron Jobs**: System-level scheduling
- **Container Orchestration**: Docker Compose or Kubernetes
- **Health Monitoring**: Automated restart on failure
- **Log Aggregation**: Centralized logging system

### Visual Excellence Standards

Every deployment includes:
- ✨ **Beautiful Progress Bars**: Unicode animations with rainbow colors
- 🎨 **Elegant Headers**: Box-drawing characters with themed emojis  
- 🌈 **Color Harmony**: Consistent visual design language
- 💎 **Status Indicators**: Crystal-clear operational feedback
- 🚀 **Premium Feel**: Polished, professional interfaces

### Backup & Recovery

- **Configuration Backup**: Git repository + encrypted secrets
- **Data Backup**: NFS storage with snapshots
- **Container Images**: Tagged, versioned container builds
- **Disaster Recovery**: Rapid deployment from backups

---

*PAI Deployment Architecture - miraclemax HP Server Platform*  
*Priority #1: Visually Stunning Automation Infrastructure*

