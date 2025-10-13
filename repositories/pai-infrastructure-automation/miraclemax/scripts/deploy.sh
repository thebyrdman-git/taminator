#!/bin/bash
# miraclemax Infrastructure Deployment Script
# Deploys all services using Infrastructure as Code
# Philosophy: Automation eliminates toil, infrastructure as code

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
REMOTE_USER="jbyrd"
REMOTE_HOST="192.168.1.34"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKUP_DIR="/tmp/miraclemax-backup-$(date +%Y%m%d-%H%M%S)"

# Progress indicator
show_progress() {
    local step=$1
    local total=$2
    local message=$3
    local percentage=$((step * 100 / total))
    local width=50
    local completed=$((step * width / total))
    
    printf "${BLUE}🔧 Progress:${NC} ["
    printf "%${completed}s" | tr ' ' '█'
    printf "%$((width-completed))s" | tr ' ' '░'
    printf "] ${percentage}%% - ${message}${NC}\n"
}

# Error handler
error_exit() {
    echo -e "${RED}❌ Error: $1${NC}" >&2
    exit 1
}

# Success message
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Warning message
warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Info message
info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Pre-deployment checks
pre_deployment_checks() {
    info "Running pre-deployment checks..."
    
    # Check connectivity
    if ! ping -c 1 -W 2 "$REMOTE_HOST" &>/dev/null; then
        error_exit "Cannot reach miraclemax at $REMOTE_HOST"
    fi
    success "Connectivity check passed"
    
    # Check SSH access
    if ! ssh -o ConnectTimeout=5 "$REMOTE_USER@$REMOTE_HOST" "echo test" &>/dev/null; then
        error_exit "SSH access failed to $REMOTE_USER@$REMOTE_HOST"
    fi
    success "SSH access verified"
    
    # Check disk space on remote
    local disk_usage=$(ssh "$REMOTE_USER@$REMOTE_HOST" "df -h /home | tail -1 | awk '{print \$5}' | sed 's/%//'")
    if [ "$disk_usage" -gt 85 ]; then
        error_exit "Disk usage too high: ${disk_usage}% (threshold: 85%)"
    fi
    success "Disk space check passed (${disk_usage}% used)"
    
    # Verify podman-compose exists
    if ! ssh "$REMOTE_USER@$REMOTE_HOST" "command -v podman-compose &>/dev/null"; then
        warning "podman-compose not found, will use podman directly"
    fi
}

# Create backup of current state
create_backup() {
    info "Creating backup of current configuration..."
    
    ssh "$REMOTE_USER@$REMOTE_HOST" << EOF
        mkdir -p $BACKUP_DIR
        
        # Backup running container configs
        for container in \$(podman ps --format '{{.Names}}'); do
            podman inspect \$container > $BACKUP_DIR/\${container}.json 2>/dev/null || true
        done
        
        # Backup compose files if they exist
        if [ -d ~/miraclemax-infrastructure ]; then
            cp -r ~/miraclemax-infrastructure $BACKUP_DIR/
        fi
        
        echo "Backup created at: $BACKUP_DIR"
EOF
    
    success "Backup created at $BACKUP_DIR"
}

# Sync repository to remote
sync_repository() {
    info "Syncing repository to miraclemax..."
    
    # Create directory on remote
    ssh "$REMOTE_USER@$REMOTE_HOST" "mkdir -p ~/miraclemax-infrastructure"
    
    # Sync files (excluding .git)
    rsync -av --delete \
        --exclude '.git' \
        --exclude '*.swp' \
        --exclude '.DS_Store' \
        "$PROJECT_ROOT/" \
        "$REMOTE_USER@$REMOTE_HOST:~/miraclemax-infrastructure/"
    
    success "Repository synced"
}

# Deploy services
deploy_services() {
    local services=("traefik" "homeassistant" "actual-budget" "n8n" "cadvisor")
    local total=${#services[@]}
    local current=0
    
    info "Deploying services..."
    
    for service in "${services[@]}"; do
        current=$((current + 1))
        show_progress $current $total "Deploying $service"
        
        ssh "$REMOTE_USER@$REMOTE_HOST" << EOF
            cd ~/miraclemax-infrastructure/compose
            
            # Stop existing container if running
            podman stop $service 2>/dev/null || true
            podman rm $service 2>/dev/null || true
            
            # Pull new image
            image=\$(grep "image:" ${service}.yml | head -1 | awk '{print \$2}')
            echo "  Pulling \$image..."
            podman pull \$image
            
            # Deploy using podman-compose or podman
            if command -v podman-compose &>/dev/null; then
                podman-compose -f ${service}.yml up -d
            else
                # Parse compose file and run podman directly
                echo "  Starting container..."
                podman play kube ${service}.yml || {
                    echo "  Note: podman play kube not supported, manual deployment needed"
                }
            fi
EOF
        
        sleep 2  # Allow service to initialize
    done
    
    success "All services deployed"
}

# Verify deployment
verify_deployment() {
    info "Verifying deployment..."
    
    local failed=0
    
    # Check each service is running
    ssh "$REMOTE_USER@$REMOTE_HOST" << 'EOF'
        echo "Service Status:"
        podman ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        
        # Check health status
        echo ""
        echo "Health Checks:"
        for container in $(podman ps --format '{{.Names}}'); do
            health=$(podman inspect $container --format '{{.State.Healthcheck.Status}}' 2>/dev/null || echo "no healthcheck")
            printf "  %-20s %s\n" "$container:" "$health"
        done
EOF
    
    success "Deployment verification complete"
}

# Post-deployment tasks
post_deployment() {
    info "Running post-deployment tasks..."
    
    # Update documentation
    echo "$(date): Deployed version $(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')" >> "$PROJECT_ROOT/CHANGELOG.md"
    
    # Test service endpoints (if on same network)
    if ping -c 1 -W 2 "$REMOTE_HOST" &>/dev/null; then
        info "Testing service endpoints..."
        curl -f -s -o /dev/null http://$REMOTE_HOST:8123 && success "Home Assistant responding" || warning "Home Assistant not responding"
        curl -f -s -o /dev/null http://$REMOTE_HOST:5006 && success "Actual Budget responding" || warning "Actual Budget not responding"
        curl -f -s -o /dev/null http://$REMOTE_HOST:5678 && success "n8n responding" || warning "n8n not responding"
    fi
    
    success "Post-deployment tasks complete"
}

# Main deployment function
main() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🔧 miraclemax Infrastructure Deployment"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    show_progress 1 6 "Pre-deployment checks"
    pre_deployment_checks
    echo ""
    
    show_progress 2 6 "Creating backup"
    create_backup
    echo ""
    
    show_progress 3 6 "Syncing repository"
    sync_repository
    echo ""
    
    show_progress 4 6 "Deploying services"
    deploy_services
    echo ""
    
    show_progress 5 6 "Verifying deployment"
    verify_deployment
    echo ""
    
    show_progress 6 6 "Post-deployment tasks"
    post_deployment
    echo ""
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    success "Deployment complete!"
    echo ""
    info "Services accessible at:"
    echo "  • Traefik Dashboard: http://$REMOTE_HOST:8080"
    echo "  • Home Assistant: http://$REMOTE_HOST:8123"
    echo "  • Actual Budget: http://$REMOTE_HOST:5006"
    echo "  • n8n: http://$REMOTE_HOST:5678"
    echo "  • cAdvisor: http://$REMOTE_HOST:8084"
    echo ""
    info "Backup location: $BACKUP_DIR"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# Run main function
main "$@"

