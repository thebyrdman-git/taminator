# Makefile for RFE Automation Tool
# Provides easy commands for development, testing, and deployment

.PHONY: help install test lint clean build deploy

# Default target
help:
	@echo "🚀 RFE Automation Tool - Available Commands:"
	@echo ""
	@echo "📦 Installation & Setup:"
	@echo "  make install          Install dependencies"
	@echo "  make setup            Setup development environment"
	@echo ""
	@echo "🧪 Testing:"
	@echo "  make test             Run all tests"
	@echo "  make test-molecule    Run Molecule tests"
	@echo "  make test-integration Run integration tests"
	@echo "  make test-smart       Test smart modules"
	@echo ""
	@echo "🔍 Code Quality:"
	@echo "  make lint             Run all linting"
	@echo "  make lint-ansible     Run ansible-lint"
	@echo "  make lint-yaml        Run yamllint"
	@echo "  make lint-python      Run Python linting"
	@echo ""
	@echo "🚀 Usage:"
	@echo "  make generate-jpmc    Generate reports for JPMC"
	@echo "  make generate-all     Generate all report types"
	@echo "  make generate-rfe     Generate RFE reports only"
	@echo "  make generate-active  Generate active cases only"
	@echo "  make discover         Discover all customers dynamically"
	@echo "  make generate-dynamic Generate reports for all discovered customers"
	@echo "  make setup-portfolio  Setup TAM portfolio configuration"
	@echo "  make generate-tam     Generate reports for TAM portfolio"
	@echo "  make review-portfolio Review and update TAM portfolio"
	@echo "  make setup-enhanced   Setup enhanced TAM portfolio (real-world complexity)"
	@echo "  make generate-enhanced Generate reports for enhanced TAM portfolio"
	@echo ""
	@echo "🔧 Development:"
	@echo "  make clean            Clean temporary files"
	@echo "  make build            Build Ansible collection"
	@echo "  make validate         Validate all configurations"
	@echo ""
	@echo "📋 Examples:"
	@echo "  make generate-jpmc    # Generate all reports for JPMC"
	@echo "  make test && make lint # Run tests and linting"

# Installation and setup
install:
	@echo "📦 Installing dependencies..."
	python3 -m pip install --upgrade pip
	pip install ansible ansible-lint yamllint molecule[docker] docker
	@echo "✅ Dependencies installed"

setup: install
	@echo "🔧 Setting up development environment..."
	mkdir -p output logs
	chmod +x generate_reports*.sh
	@echo "✅ Development environment ready"

# Testing commands
test: test-molecule test-integration test-smart
	@echo "✅ All tests completed"

test-molecule:
	@echo "🧪 Running Molecule tests..."
	cd tests/molecule/default && molecule test
	@echo "✅ Molecule tests completed"

test-integration:
	@echo "🔗 Running integration tests..."
	ansible-playbook generate_reports_smart.yml \
		-e "customer=jpmc" \
		-e "report_types=['rfe_bug_tracker']" \
		--check --diff
	@echo "✅ Integration tests completed"

test-smart:
	@echo "🧠 Testing smart modules..."
	./generate_reports_smart.sh jpmc rfe
	@echo "✅ Smart module tests completed"

# Linting commands
lint: lint-ansible lint-yaml lint-python
	@echo "✅ All linting completed"

lint-ansible:
	@echo "🔍 Running ansible-lint..."
	ansible-lint .
	@echo "✅ Ansible linting completed"

lint-yaml:
	@echo "🔍 Running yamllint..."
	yamllint .
	@echo "✅ YAML linting completed"

lint-python:
	@echo "🔍 Running Python linting..."
	python3 -m py_compile ansible_collections/redhat/rfe_automation/plugins/modules/*.py
	@echo "✅ Python linting completed"

# Usage commands
generate-jpmc:
	@echo "📊 Generating reports for JPMC..."
	./generate_reports_smart.sh jpmc all
	@echo "✅ JPMC reports generated"

generate-all:
	@echo "📊 Generating all report types..."
	./generate_reports_smart.sh jpmc all
	@echo "✅ All reports generated"

generate-rfe:
	@echo "📊 Generating RFE reports..."
	./generate_reports_smart.sh jpmc rfe
	@echo "✅ RFE reports generated"

generate-active:
	@echo "📊 Generating active cases reports..."
	./generate_reports_smart.sh jpmc active
	@echo "✅ Active cases reports generated"

# Dynamic inventory commands
discover:
	@echo "🔍 Discovering customers dynamically..."
	ansible-inventory -i inventory/rfe_customers.yml --list
	@echo "✅ Customer discovery completed"

generate-dynamic:
	@echo "📊 Generating reports for all discovered customers..."
	./generate_reports_dynamic.sh all
	@echo "✅ Dynamic reports generated"

generate-dynamic-rfe:
	@echo "📊 Generating RFE reports for all discovered customers..."
	./generate_reports_dynamic.sh rfe
	@echo "✅ Dynamic RFE reports generated"

generate-dynamic-active:
	@echo "📊 Generating active cases reports for all discovered customers..."
	./generate_reports_dynamic.sh active
	@echo "✅ Dynamic active cases reports generated"

# TAM Portfolio commands
setup-portfolio:
	@echo "🎯 Setting up TAM portfolio configuration..."
	./setup-tam-portfolio.sh
	@echo "✅ TAM portfolio setup completed"

generate-tam:
	@echo "📊 Generating reports for TAM portfolio..."
	ansible-playbook generate_tam_reports.yml -i inventory/tam-portfolio.yml
	@echo "✅ TAM portfolio reports generated"

generate-tam-rfe:
	@echo "📊 Generating RFE reports for TAM portfolio..."
	ansible-playbook generate_tam_reports.yml -i inventory/tam-portfolio.yml -e "report_types=['rfe_bug_tracker']"
	@echo "✅ TAM portfolio RFE reports generated"

generate-tam-active:
	@echo "📊 Generating active cases reports for TAM portfolio..."
	ansible-playbook generate_tam_reports.yml -i inventory/tam-portfolio.yml -e "report_types=['active_cases']"
	@echo "✅ TAM portfolio active cases reports generated"

review-portfolio:
	@echo "🔍 Reviewing TAM portfolio..."
	ansible-inventory -i inventory/tam-portfolio.yml --list | jq '.suggestions.add_accounts[]?' 2>/dev/null || echo "No suggestions available"
	@echo "✅ Portfolio review completed"

discover-portfolio:
	@echo "🔍 Discovering TAM portfolio..."
	ansible-inventory -i inventory/tam-portfolio.yml --list
	@echo "✅ Portfolio discovery completed"

# Enhanced TAM Portfolio commands
setup-enhanced:
	@echo "🎯 Setting up enhanced TAM portfolio configuration..."
	./setup-enhanced-tam-portfolio.sh
	@echo "✅ Enhanced TAM portfolio setup completed"

generate-enhanced:
	@echo "📊 Generating reports for enhanced TAM portfolio..."
	ansible-playbook generate_enhanced_tam_reports.yml -i inventory/enhanced-tam-portfolio.yml
	@echo "✅ Enhanced TAM portfolio reports generated"

generate-enhanced-rfe:
	@echo "📊 Generating RFE reports for enhanced TAM portfolio..."
	ansible-playbook generate_enhanced_tam_reports.yml -i inventory/enhanced-tam-portfolio.yml -e "report_types=['rfe_bug_tracker']"
	@echo "✅ Enhanced TAM portfolio RFE reports generated"

generate-enhanced-active:
	@echo "📊 Generating active cases reports for enhanced TAM portfolio..."
	ansible-playbook generate_enhanced_tam_reports.yml -i inventory/enhanced-tam-portfolio.yml -e "report_types=['active_cases']"
	@echo "✅ Enhanced TAM portfolio active cases reports generated"

discover-enhanced-portfolio:
	@echo "🔍 Discovering enhanced TAM portfolio..."
	ansible-inventory -i inventory/enhanced-tam-portfolio.yml --list
	@echo "✅ Enhanced portfolio discovery completed"

# Development commands
clean:
	@echo "🧹 Cleaning temporary files..."
	rm -rf output/* logs/* .cache/ .molecule/ __pycache__/ *.pyc
	rm -rf tests/molecule/default/.cache/ tests/molecule/default/.molecule/
	find . -name "*.tmp" -delete
	find . -name ".DS_Store" -delete
	@echo "✅ Cleanup completed"

build:
	@echo "🔨 Building Ansible collection..."
	ansible-galaxy collection build ansible_collections/redhat/rfe_automation/
	@echo "✅ Collection built"

validate:
	@echo "✅ Validating configurations..."
	@echo "🔍 Validating Ansible syntax..."
	ansible-playbook --syntax-check generate_reports_smart.yml
	ansible-playbook --syntax-check generate_reports_with_vars.yml
	@echo "🔍 Validating YAML files..."
	yamllint vars/accounts.yml
	@echo "🔍 Validating Python modules..."
	python3 -m py_compile ansible_collections/redhat/rfe_automation/plugins/modules/*.py
	@echo "✅ All validations passed"

# CI/CD commands
ci: lint test
	@echo "🚀 CI pipeline completed"

ci-full: install lint test build
	@echo "🚀 Full CI pipeline completed"

# Docker commands for testing
docker-test:
	@echo "🐳 Running tests in Docker..."
	docker run --rm -v $(PWD):/workspace -w /workspace \
		quay.io/ansible/molecule:latest \
		bash -c "pip install molecule[docker] && cd tests/molecule/default && molecule test"

# Documentation
docs:
	@echo "📚 Generating documentation..."
	@echo "✅ Documentation would be generated here"

# Deployment (placeholder)
deploy:
	@echo "🚀 Deployment would happen here"
	@echo "This would integrate with your deployment system"

# Quick development workflow
dev: clean setup validate
	@echo "🚀 Development environment ready"

# Production readiness check
prod-check: lint test validate
	@echo "✅ Production readiness check completed"

# Show current status
status:
	@echo "📊 RFE Automation Tool Status:"
	@echo "📁 Working Directory: $(PWD)"
	@echo "🐍 Python Version: $(shell python3 --version)"
	@echo "🔧 Ansible Version: $(shell ansible --version | head -1)"
	@echo "🧪 Molecule Version: $(shell molecule --version 2>/dev/null || echo 'Not installed')"
	@echo "📋 Available Customers:"
	@grep -E "^  [a-zA-Z_]+:" vars/accounts.yml | sed 's/^  /  - /' | sed 's/:$$//' || echo "  No customers configured"
