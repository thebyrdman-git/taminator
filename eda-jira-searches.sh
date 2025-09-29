#!/bin/bash
# EDA Redis Cluster Jira Search Queries
# Run after configuring rhcase with: rhcase config setup

echo "🔍 Searching for EDA Redis Cluster and HA issues..."

echo "1. Direct Redis cluster references:"
rhcase jira search "project = EDA AND summary ~ 'redis cluster'"

echo "2. High availability requests:"  
rhcase jira search "project = EDA AND summary ~ 'high availability'"

echo "3. HA RFEs across AAP:"
rhcase jira search "project in (EDA, AAP, RFE) AND summary ~ 'Event-Driven Ansible' AND summary ~ 'availability'"

echo "4. Redis dependency issues:"
rhcase jira search "project = EDA AND description ~ 'redis' AND description ~ 'single point'"

echo "5. Clustering and failover:"
rhcase jira search "project = EDA AND (summary ~ 'cluster' OR summary ~ 'failover' OR summary ~ 'fault tolerance')"

echo "6. Customer-requested enhancements:"
rhcase jira search "project = RFE AND summary ~ 'Event-Driven Ansible' AND (summary ~ 'HA' OR summary ~ 'availability' OR summary ~ 'cluster')"

echo "✅ Search completed. Review results for roadmap intelligence."
