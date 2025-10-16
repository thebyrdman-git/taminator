# Enhanced TAM Portfolio System

## 🎯 **Real-World TAM Complexity Handled**

Based on the **NA FSI TAM Accounts Overview** data, this system handles:

### **📊 Scale & Scope**
- **Multi-TAM Accounts** - Up to 5 TAMs per account (Citigroup: 5 TAMs)
- **Product Specialization** - Platform (23), OpenShift (16), Ansible (13), Middleware (5)
- **Coverage Models** - Dedicated vs Shared coverage
- **Account Weights** - 1-4 priority scale
- **Backup Relationships** - Primary/backup TAM assignments
- **Multi-Account Customers** - Same customer, multiple account numbers

### **🏢 Account Examples from FSI Data**
- **Bank of America**: 4 TAMs (Platform, Ansible, OpenShift, Middleware)
- **Citigroup**: 5 TAMs (Platform, Ansible, OpenShift x2, Middleware)
- **JPMC**: 3 TAMs (Platform, Ansible, OpenShift)
- **Multiple account numbers** per customer

## 🚀 **Enhanced TAM Portfolio Features**

### **1. Multi-TAM Coordination**
```yaml
coordination:
  shared_accounts:
    - customer_name: "Bank of America"
      other_tams:
        - name: "Stephen Hobbs"
          products: ["Platform"]
          role: "Primary"
      coordination_notes: "Weekly sync calls"
```

### **2. Product Specialization**
```yaml
accounts:
  - customer_name: "JP Morgan Chase"
    products: ["Ansible"]
    tam_role: "Primary"
    account_weight: 3
    coverage_model: "Shared"
```

### **3. Backup Coverage**
```yaml
backup_coverage:
  primary_backup: "Peter Sagat"
  coverage_schedule:
    - dates: "2024-12-20 to 2024-12-31"
      backup_tam: "Peter Sagat"
      accounts: ["334224", "54545"]
```

### **4. Account Prioritization**
```yaml
prioritization:
  high_priority: ["6231835"]  # Citigroup - Weight 4
  medium_priority: ["334224"]  # JPMC - Weight 3
  low_priority: ["54545"]     # BofA - Weight 1
```

## 🛠️ **System Components**

### **Enhanced Inventory Plugin**
- **File**: `ansible_collections/redhat/rfe_automation/plugins/inventory/enhanced_tam_portfolio.py`
- **Features**: Multi-TAM coordination, backup coverage, account weights
- **Validation**: Real-time case data validation
- **Suggestions**: Smart portfolio maintenance suggestions

### **Enhanced Setup Tool**
- **File**: `setup-enhanced-tam-portfolio.sh`
- **Features**: Interactive setup with real-world complexity
- **Analysis**: Case data analysis for suggestions
- **Configuration**: Generates comprehensive portfolio config

### **Enhanced Playbook**
- **File**: `generate_enhanced_tam_reports.yml`
- **Features**: Multi-account processing, coordination awareness
- **Reporting**: Account weight prioritization
- **Output**: Customer-specific directories with account numbers

## 📋 **Usage Examples**

### **Setup Enhanced Portfolio**
```bash
# Interactive setup with real-world complexity
make setup-enhanced

# Creates: ~/.config/rfe-automation/enhanced-tam-portfolio.yml
```

### **Generate Reports**
```bash
# Generate all reports for enhanced portfolio
make generate-enhanced

# Generate only RFE reports
make generate-enhanced-rfe

# Generate only active cases
make generate-enhanced-active
```

### **Portfolio Management**
```bash
# Discover portfolio structure
make discover-enhanced-portfolio

# Review suggestions and coordination opportunities
ansible-inventory -i inventory/enhanced-tam-portfolio.yml --list | jq '.suggestions'
```

## 🎯 **Key Advantages**

### **Real-World Accuracy**
- ✅ **Handles multi-TAM accounts** (up to 5 TAMs per account)
- ✅ **Product specialization** (Platform, OpenShift, Ansible, Middleware)
- ✅ **Coverage models** (Dedicated vs Shared)
- ✅ **Account weights** (1-4 priority scale)
- ✅ **Backup relationships** (Primary/backup TAMs)

### **TAM Flexibility**
- ✅ **Works for any TAM** regardless of product mix
- ✅ **Handles any vertical** (FSI, Healthcare, Government, etc.)
- ✅ **Scales from 5 to 50+ accounts**
- ✅ **Supports complex coverage models**

### **Enterprise Features**
- ✅ **Multi-TAM coordination** awareness
- ✅ **Backup coverage** management
- ✅ **Account prioritization** by weight
- ✅ **Smart suggestions** for portfolio maintenance
- ✅ **Real-time validation** against case data

## 🚀 **Next Steps**

1. **Setup your enhanced portfolio**: `make setup-enhanced`
2. **Configure multi-TAM coordination** in the config file
3. **Set up backup coverage** schedules
4. **Generate reports**: `make generate-enhanced`
5. **Review suggestions** and update portfolio as needed

This system now handles the **real-world complexity** of TAM account management based on actual FSI data!
