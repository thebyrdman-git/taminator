#!/bin/bash
# Deploy Enterprise-Grade Monitoring Stack
# Fortune 500-level observability for miraclemax

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║    Deploying Enterprise Monitoring Stack - miraclemax    ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo

# Create required directories on host
echo "📁 Creating data directories..."
ssh jbyrd@192.168.1.34 'sudo mkdir -p /home/jbyrd/{grafana-data,alertmanager-data,prometheus-data} && \
  sudo chown -R jbyrd:jbyrd /home/jbyrd/{grafana-data,alertmanager-data,prometheus-data}'

# Sync configuration files to miraclemax
echo "📤 Syncing configuration files to miraclemax..."
rsync -avz --delete \
  "$PROJECT_ROOT/config/" \
  jbyrd@192.168.1.34:/home/jbyrd/pai/repositories/pai-infrastructure-automation/miraclemax/config/

rsync -avz --delete \
  "$PROJECT_ROOT/compose/" \
  jbyrd@192.168.1.34:/home/jbyrd/pai/repositories/pai-infrastructure-automation/miraclemax/compose/

# Ensure traefik-network exists
echo "🌐 Creating traefik-network (if not exists)..."
ssh jbyrd@192.168.1.34 'sudo podman network create traefik-network 2>/dev/null || true'

# Deploy components in order
echo
echo "🚀 Deploying monitoring components..."
echo

# 1. Node Exporter (host metrics)
echo "1️⃣  Deploying node-exporter..."
ssh jbyrd@192.168.1.34 'cd /home/jbyrd/pai/repositories/pai-infrastructure-automation/miraclemax && \
  sudo podman-compose -f compose/node-exporter.yml up -d --force-recreate'
echo "   ✅ node-exporter deployed"
sleep 2

# 2. Blackbox Exporter (endpoint monitoring)
echo "2️⃣  Deploying blackbox-exporter..."
ssh jbyrd@192.168.1.34 'cd /home/jbyrd/pai/repositories/pai-infrastructure-automation/miraclemax && \
  sudo podman-compose -f compose/blackbox-exporter.yml up -d --force-recreate'
echo "   ✅ blackbox-exporter deployed"
sleep 2

# 3. Process Exporter (process monitoring)
echo "3️⃣  Deploying process-exporter..."
ssh jbyrd@192.168.1.34 'cd /home/jbyrd/pai/repositories/pai-infrastructure-automation/miraclemax && \
  sudo podman-compose -f compose/process-exporter.yml up -d --force-recreate'
echo "   ✅ process-exporter deployed"
sleep 2

# 4. Update Prometheus with new config
echo "4️⃣  Updating Prometheus configuration..."
ssh jbyrd@192.168.1.34 'sudo podman exec prometheus kill -HUP 1 2>/dev/null || \
  echo "   ⚠️  Prometheus not running or reload failed"'
echo "   ✅ Prometheus config reloaded"
sleep 2

# 5. Alertmanager
echo "5️⃣  Deploying alertmanager..."
echo "   ⚠️  NOTE: You must set up Gmail App Password first!"
echo "   📖 See: docs/EMAIL-ALERTING-SETUP.md"
ssh jbyrd@192.168.1.34 'cd /home/jbyrd/pai/repositories/pai-infrastructure-automation/miraclemax && \
  sudo podman-compose -f compose/alertmanager.yml up -d --force-recreate'
echo "   ✅ alertmanager deployed"
sleep 2

# 6. Grafana
echo "6️⃣  Deploying grafana..."
ssh jbyrd@192.168.1.34 'cd /home/jbyrd/pai/repositories/pai-infrastructure-automation/miraclemax && \
  sudo podman-compose -f compose/grafana.yml up -d --force-recreate'
echo "   ✅ grafana deployed"
sleep 5

echo
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║           Monitoring Stack Deployment Complete           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo

# Verify deployment
echo "📊 Verifying deployment..."
echo
ssh jbyrd@192.168.1.34 'sudo podman ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | \
  grep -E "node-exporter|blackbox|process|alert|grafana|prometheus"' || true

echo
echo "🌐 Access Points:"
echo "   Grafana:       https://grafana.jbyrd.org   (admin/changeme)"
echo "   Prometheus:    https://metrics.jbyrd.org"
echo "   Alertmanager:  https://alerts.jbyrd.org"
echo "   Node Exporter: http://192.168.1.34:9100/metrics"
echo "   Blackbox:      http://192.168.1.34:9115/"
echo "   Process:       http://192.168.1.34:9256/metrics"
echo
echo "📧 Email Alerts: jimmykbyrd@gmail.com"
echo "   ⚠️  Remember to set up Gmail App Password!"
echo "   📖 Guide: docs/EMAIL-ALERTING-SETUP.md"
echo
echo "🎯 Next Steps:"
echo "   1. Set up Gmail App Password (see EMAIL-ALERTING-SETUP.md)"
echo "   2. Access Grafana and change default password"
echo "   3. Configure custom dashboards"
echo "   4. Set up Red Hat Insights (see REDHAT-INSIGHTS-SETUP.md)"
echo "   5. Test email alerts"
echo

