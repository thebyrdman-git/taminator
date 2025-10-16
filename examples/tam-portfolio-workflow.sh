#!/bin/bash
# Example TAM Portfolio Workflow

echo "🎯 TAM Portfolio Management Workflow"
echo "===================================="

# Step 1: TAM defines their portfolio
echo "📋 Step 1: TAM Portfolio Configuration"
echo "TAM creates: ~/.config/rfe-automation/tam-portfolio.yml"
echo ""
echo "Example config:"
cat << 'EOF'
tam_name: "Jimmy Byrd"
accounts:
  - account_number: "334224"
    customer_name: "JP Morgan Chase"
    products: ["Ansible"]
  - account_number: "838043"
    customer_name: "WELLS FARGO" 
    products: ["Ansible"]
EOF

echo ""
echo "🔄 Step 2: System Validation"
echo "System queries rhcase for each account and validates:"
echo "✅ Account exists and has cases"
echo "✅ TAM has recent case activity"
echo "✅ Product assignments are correct"

echo ""
echo "📊 Step 3: Generate Reports"
echo "TAM runs: make generate-tam-reports"
echo "System automatically:"
echo "  - Reads TAM's portfolio"
echo "  - Generates reports for ALL accounts"
echo "  - Creates customer-specific directories"
echo "  - Provides portfolio suggestions"

echo ""
echo "💡 Step 4: Smart Suggestions"
echo "System analyzes case patterns and suggests:"
echo "  - New accounts with case activity"
echo "  - Accounts to remove (no recent activity)"
echo "  - Product additions (new SBR groups)"

echo ""
echo "🎯 Benefits:"
echo "✅ TAM controls their portfolio"
echo "✅ Works for any product combination"
echo "✅ Validated against real data"
echo "✅ Easy to maintain and update"
