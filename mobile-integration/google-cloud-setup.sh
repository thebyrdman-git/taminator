#!/bin/bash

# Google Cloud Setup Script for PAI Mobile Integration
# Part of the Personal AI Infrastructure (PAI)
# Created for Hatter - Red Hat Digital Assistant

set -e

# Load progress tracking system
SCRIPT_DIR="$(dirname "$0")"
PAI_ROOT="$(dirname "$SCRIPT_DIR")"

# Try multiple paths to find the progress tracker
PROGRESS_TRACKER_PATHS=(
    "$PAI_ROOT/bin/pai-progress-tracker"
    "/home/jbyrd/hatter-pai/bin/pai-progress-tracker"
    "$(pwd)/../bin/pai-progress-tracker"
)

PROGRESS_LOADED=false
for path in "${PROGRESS_TRACKER_PATHS[@]}"; do
    if [[ -f "$path" ]]; then
        source "$path" 2>/dev/null && {
            PROGRESS_LOADED=true
            echo "📊 Progress tracking system loaded from: $path"
            break
        }
    fi
done

if [[ "$PROGRESS_LOADED" != "true" ]]; then
    echo "⚠️  Progress tracking system not found - using basic progress"
    show_progress() { echo "Progress: $1/$2 - $3"; }
    show_task_status() { echo "$2: $1"; }
    run_with_progress() { shift 2; for cmd in "$@"; do eval "$cmd"; done; }
fi

PROJECT_ID="pai-mobile-assistant-$(date +%s)"
REGION="us-central1"
SERVICE_ACCOUNT_NAME="pai-webhook-service"

# Setup progress tracking
TOTAL_SETUP_STEPS=7
CURRENT_STEP=0

# Progress step tracker
next_step() {
    ((CURRENT_STEP++))
    show_progress $CURRENT_STEP $TOTAL_SETUP_STEPS "Google Cloud Setup"
}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if gcloud is installed
check_gcloud() {
    show_task_status "Google Cloud CLI Check" "starting"
    next_step
    
    log "Checking Google Cloud CLI installation..."
    
    if ! command -v gcloud &> /dev/null; then
        error "Google Cloud CLI not found!"
        echo ""
        echo "📥 INSTALL GOOGLE CLOUD CLI:"
        echo "   For Fedora/CentOS/RHEL:"
        echo "   curl https://sdk.cloud.google.com | bash"
        echo "   exec -l \$SHELL"
        echo ""
        echo "   For Debian/Ubuntu:"
        echo "   curl https://sdk.cloud.google.com | bash"
        echo "   exec -l \$SHELL"
        echo ""
        echo "   Or visit: https://cloud.google.com/sdk/docs/install"
        show_task_status "Google Cloud CLI Check" "error"
        exit 1
    fi
    
    local gcloud_version=$(gcloud version --format='text' | grep 'Google Cloud SDK' | cut -d' ' -f4 || echo "installed")
    success "Google Cloud CLI found: version $gcloud_version"
    show_task_status "Google Cloud CLI Check" "complete"
}

# Authenticate with Google Cloud
authenticate_gcloud() {
    show_task_status "Google Cloud Authentication" "starting"
    next_step
    
    log "Authenticating with Google Cloud..."
    
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "@"; then
        warning "Not authenticated with Google Cloud"
        echo ""
        echo "🔐 Please authenticate with Google Cloud:"
        echo "   This will open a browser window for login"
        echo ""
        read -p "Press Enter to continue with authentication..."
        
        show_task_status "Google Cloud Authentication" "progress"
        gcloud auth login --brief
        gcloud auth application-default login --brief
        
        success "Authentication completed"
    else
        success "Already authenticated with Google Cloud"
        gcloud auth list --filter=status:ACTIVE --format="table(account,status)"
    fi
    
    show_task_status "Google Cloud Authentication" "complete"
}

# Create Google Cloud project
create_project() {
    show_task_status "Project Creation" "starting"
    next_step
    
    log "Creating Google Cloud project: $PROJECT_ID"
    
    if gcloud projects describe "$PROJECT_ID" >/dev/null 2>&1; then
        warning "Project $PROJECT_ID already exists"
    else
        show_task_status "Project Creation" "progress"
        gcloud projects create "$PROJECT_ID" --name="PAI Mobile Assistant"
        success "Project created: $PROJECT_ID"
    fi
    
    # Set the project as active
    show_progress 2 3 "Project Setup"
    gcloud config set project "$PROJECT_ID"
    success "Active project set to: $PROJECT_ID"
    
    echo ""
    echo "📝 PROJECT DETAILS:"
    echo "   Project ID: $PROJECT_ID"
    echo "   Project Name: PAI Mobile Assistant"
    echo "   Region: $REGION"
    
    show_task_status "Project Creation" "complete"
}

# Enable required APIs
enable_apis() {
    show_task_status "API Enablement" "starting"
    next_step
    
    log "Enabling required Google Cloud APIs..."
    
    local apis=(
        "dialogflow.googleapis.com"
        "cloudfunctions.googleapis.com"
        "cloudbuild.googleapis.com"
        "logging.googleapis.com"
        "monitoring.googleapis.com"
    )
    
    local total_apis=${#apis[@]}
    local api_count=0
    
    for api in "${apis[@]}"; do
        ((api_count++))
        show_progress $api_count $total_apis "Enabling APIs"
        log "Enabling $api..."
        gcloud services enable "$api"
        success "$api enabled"
    done
    
    echo ""
    success "All required APIs enabled"
    show_task_status "API Enablement" "complete"
}

# Create service account
create_service_account() {
    show_task_status "Service Account Setup" "starting"
    next_step
    
    log "Creating service account: $SERVICE_ACCOUNT_NAME"
    
    local service_account_email="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
    
    show_progress 1 4 "Service Account Creation"
    if gcloud iam service-accounts describe "$service_account_email" >/dev/null 2>&1; then
        warning "Service account already exists: $service_account_email"
    else
        show_task_status "Service Account Setup" "progress"
        gcloud iam service-accounts create "$SERVICE_ACCOUNT_NAME" \
            --display-name="PAI Webhook Service Account" \
            --description="Service account for PAI mobile webhook integration"
        
        success "Service account created: $service_account_email"
    fi
    
    # Grant necessary roles
    show_progress 2 4 "IAM Role Assignment"
    log "Granting IAM roles to service account..."
    
    local roles=(
        "roles/dialogflow.admin"
        "roles/cloudfunctions.invoker"
        "roles/logging.logWriter"
        "roles/monitoring.metricWriter"
    )
    
    local role_count=0
    for role in "${roles[@]}"; do
        ((role_count++))
        show_progress $role_count ${#roles[@]} "Granting Roles"
        gcloud projects add-iam-policy-binding "$PROJECT_ID" \
            --member="serviceAccount:$service_account_email" \
            --role="$role"
        success "Granted role: $role"
    done
    
    # Create and download service account key
    show_progress 3 4 "Service Account Key"
    local key_file="$SCRIPT_DIR/service-account-key.json"
    
    if [[ -f "$key_file" ]]; then
        warning "Service account key already exists: $key_file"
    else
        gcloud iam service-accounts keys create "$key_file" \
            --iam-account="$service_account_email"
        
        success "Service account key created: $key_file"
        warning "Keep this key file secure and do not commit it to git!"
    fi
    
    show_progress 4 4 "Service Account Complete"
    echo ""
    echo "🔑 SERVICE ACCOUNT DETAILS:"
    echo "   Email: $service_account_email"
    echo "   Key File: $key_file"
    echo "   Roles: Dialogflow Admin, Cloud Functions Invoker, Logging Writer"
    
    show_task_status "Service Account Setup" "complete"
}

# Create Dialogflow agent
create_dialogflow_agent() {
    log "Setting up Dialogflow agent..."
    
    echo ""
    echo "📱 DIALOGFLOW AGENT SETUP:"
    echo "   1. Go to: https://dialogflow.cloud.google.com/"
    echo "   2. Select project: $PROJECT_ID"
    echo "   3. Create new agent: 'PAI Mobile Assistant'"
    echo "   4. Set default language: English (en)"
    echo "   5. Set time zone: America/New_York (or your timezone)"
    echo ""
    echo "   Agent will be created at:"
    echo "   https://dialogflow.cloud.google.com/cx/projects/$PROJECT_ID"
    echo ""
    
    warning "Manual step: Create Dialogflow agent via web console"
    echo "   We'll provide the import files after agent creation"
}

# Set up webhook URL (using ngrok for testing)
setup_webhook_url() {
    log "Setting up webhook URL for testing..."
    
    # Check if ngrok is installed
    if ! command -v ngrok &> /dev/null; then
        warning "ngrok not found - installing for webhook testing"
        echo ""
        echo "📥 INSTALLING NGROK:"
        
        # Download and install ngrok
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
            echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
            sudo apt update && sudo apt install ngrok
        else
            echo "   Please install ngrok manually from: https://ngrok.com/download"
            echo "   Or use: npm install -g ngrok"
            return 1
        fi
    fi
    
    success "ngrok is available for webhook tunneling"
    
    echo ""
    echo "🌐 WEBHOOK URL SETUP:"
    echo "   1. Start your PAI webhook server: pai-mobile-webhook start"
    echo "   2. In a new terminal, run: ngrok http 3001"
    echo "   3. Copy the HTTPS URL (e.g., https://abc123.ngrok.io)"
    echo "   4. Use this URL + /webhook in Dialogflow settings"
    echo ""
    echo "   Example webhook URL: https://abc123.ngrok.io/webhook"
}

# Generate environment configuration
generate_config() {
    log "Generating configuration files..."
    
    # Create .env file for webhook server
    local env_file="$SCRIPT_DIR/webhook-server/.env"
    cat > "$env_file" << EOF
# PAI Mobile Webhook Server - Google Cloud Configuration
# Generated on $(date)

# Google Cloud Configuration
GOOGLE_PROJECT_ID=$PROJECT_ID
GOOGLE_APPLICATION_CREDENTIALS=$SCRIPT_DIR/service-account-key.json

# Server Configuration
PORT=3001
NODE_ENV=production
LOG_LEVEL=info

# PAI Configuration
PAI_TOOLS_PATH=/home/jbyrd/hatter-pai/bin
MAX_EXECUTION_TIME=30000
EOF

    success "Environment configuration created: $env_file"
    
    # Update Dialogflow config with project ID
    local dialogflow_config="$SCRIPT_DIR/dialogflow-config/agent-settings.json"
    sed -i "s/pai-mobile-assistant/$PROJECT_ID/g" "$dialogflow_config"
    
    success "Dialogflow configuration updated with project ID"
    
    echo ""
    echo "📁 CONFIGURATION FILES:"
    echo "   Environment: $env_file"
    echo "   Service Key: $SCRIPT_DIR/service-account-key.json"
    echo "   Dialogflow: $SCRIPT_DIR/dialogflow-config/"
}

# Main setup function
main() {
    echo "🌐 PAI MOBILE GOOGLE CLOUD SETUP"
    echo "================================"
    echo ""
    
    show_task_status "Google Cloud Setup" "starting" "15-20 minutes"
    show_progress 0 $TOTAL_SETUP_STEPS "Google Cloud Setup"
    
    check_gcloud
    authenticate_gcloud
    create_project
    enable_apis
    create_service_account
    generate_config
    create_dialogflow_agent
    setup_webhook_url
    
    echo ""
    echo "🎉 GOOGLE CLOUD SETUP COMPLETE!"
    echo "==============================="
    echo ""
    success "Project created and configured: $PROJECT_ID"
    success "Service account and credentials ready"
    success "APIs enabled for Dialogflow and Cloud Functions"
    success "Configuration files generated"
    echo ""
    echo "📋 NEXT STEPS:"
    echo "   1. Create Dialogflow agent via web console"
    echo "   2. Start webhook server: pai-mobile-webhook start"
    echo "   3. Start ngrok tunnel: ngrok http 3001"
    echo "   4. Import intents to Dialogflow"
    echo "   5. Test with 'Hey Google'"
    echo ""
    echo "🔗 USEFUL LINKS:"
    echo "   Google Cloud Console: https://console.cloud.google.com/home/dashboard?project=$PROJECT_ID"
    echo "   Dialogflow Console: https://dialogflow.cloud.google.com/cx/projects/$PROJECT_ID"
    echo "   PAI Setup Guide: $SCRIPT_DIR/SETUP-GUIDE.md"
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
