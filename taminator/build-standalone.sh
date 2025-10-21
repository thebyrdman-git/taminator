#!/bin/bash

# TAM RFE Automation Tool - Standalone Build Script
# Creates a completely self-contained executable with all dependencies

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="tam-rfe-automation"
VERSION="1.0.0"
BUILD_DIR="$SCRIPT_DIR/build"
DIST_DIR="$SCRIPT_DIR/dist"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}"
    echo "🚀 TAM RFE Automation Tool - Standalone Build"
    echo "============================================="
    echo -e "${NC}"
    echo "📅 Build started: $(date)"
    echo "🏗️  Project: $PROJECT_NAME v$VERSION"
    echo "📁 Build directory: $BUILD_DIR"
    echo "📦 Dist directory: $DIST_DIR"
    echo ""
}

print_step() {
    echo -e "${YELLOW}🔧 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_step "Checking build prerequisites..."
    
    # Check Python
    if ! command -v python3 >/dev/null 2>&1; then
        print_error "Python 3.7+ is required for building"
        exit 1
    fi
    
    # Check PyInstaller
    if ! python3 -c "import PyInstaller" 2>/dev/null; then
        print_step "Installing PyInstaller..."
        pip3 install pyinstaller
    fi
    
    # Check other required packages
    local required_packages=("requests" "pathlib" "json" "subprocess" "datetime")
    for package in "${required_packages[@]}"; do
        if ! python3 -c "import $package" 2>/dev/null; then
            print_step "Installing $package..."
            pip3 install "$package"
        fi
    done
    
    print_success "Prerequisites checked"
}

# Create build directory
create_build_dir() {
    print_step "Creating build directory..."
    
    rm -rf "$BUILD_DIR"
    mkdir -p "$BUILD_DIR"
    
    # Copy source files
    cp -r "$SCRIPT_DIR/src" "$BUILD_DIR/"
    cp -r "$SCRIPT_DIR/config" "$BUILD_DIR/"
    cp -r "$SCRIPT_DIR/templates" "$BUILD_DIR/" 2>/dev/null || true
    cp -r "$SCRIPT_DIR/docs" "$BUILD_DIR/" 2>/dev/null || true
    
    # Copy main executable
    cp "$SCRIPT_DIR/tam-rfe-standalone.py" "$BUILD_DIR/"
    
    print_success "Build directory created"
}

# Create requirements file
create_requirements() {
    print_step "Creating requirements file..."
    
    cat > "$BUILD_DIR/requirements.txt" << EOF
# TAM RFE Automation Tool - Standalone Requirements
# Core dependencies
requests>=2.25.0
pathlib2>=2.3.0
python-dateutil>=2.8.0

# Optional dependencies (will be bundled)
pyinstaller>=4.0
setuptools>=50.0.0
wheel>=0.36.0

# Red Hat specific (if available)
# rhcase (Red Hat internal tool)
# kerberos (for Red Hat authentication)
EOF
    
    print_success "Requirements file created"
}

# Create PyInstaller spec file
create_pyinstaller_spec() {
    print_step "Creating PyInstaller specification..."
    
    cat > "$BUILD_DIR/tam-rfe-standalone.spec" << EOF
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['tam-rfe-standalone.py'],
    pathex=['$BUILD_DIR'],
    binaries=[],
    datas=[
        ('config', 'config'),
        ('src', 'src'),
        ('templates', 'templates'),
        ('docs', 'docs'),
    ],
    hiddenimports=[
        'requests',
        'pathlib',
        'json',
        'subprocess',
        'datetime',
        'argparse',
        'platform',
        'sys',
        'os',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='tam-rfe-automation',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
EOF
    
    print_success "PyInstaller specification created"
}

# Build the executable
build_executable() {
    print_step "Building standalone executable..."
    
    cd "$BUILD_DIR"
    
    # Install requirements
    pip3 install -r requirements.txt --target ./lib
    
    # Build with PyInstaller
    pyinstaller --clean --noconfirm tam-rfe-standalone.spec
    
    print_success "Executable built"
}

# Create distribution package
create_distribution() {
    print_step "Creating distribution package..."
    
    rm -rf "$DIST_DIR"
    mkdir -p "$DIST_DIR"
    
    # Copy executable
    cp "$BUILD_DIR/dist/tam-rfe-automation" "$DIST_DIR/" 2>/dev/null || \
    cp "$BUILD_DIR/dist/tam-rfe-automation.exe" "$DIST_DIR/" 2>/dev/null || \
    print_error "Executable not found in expected location"
    
    # Create README
    cat > "$DIST_DIR/README.md" << EOF
# TAM RFE Automation Tool - Standalone Version

## 🚀 Quick Start

1. **Download**: Get the executable for your platform
2. **Run**: Execute the file (no installation required)
3. **Follow**: The guided setup process
4. **Generate**: Your first report in minutes!

## 📋 What's Included

- ✅ Embedded AI assistant
- ✅ Red Hat integration
- ✅ Report generation
- ✅ Multiple choice interface
- ✅ Passion-driven TAM support
- ✅ Zero external dependencies

## 🎯 Features

- **Completely Standalone**: No installation required
- **Cross-Platform**: Works on Windows, Mac, Linux
- **Embedded AI**: Local processing, no external APIs
- **Red Hat Integration**: Built-in rhcase and portal clients
- **Passion-Driven**: Designed to help new TAMs succeed
- **Multiple Choice**: Easy-to-use interface
- **Comprehensive**: All features in one executable

## 💝 Built with Passion

This tool was created with a passion for helping new TAMs succeed in their roles.
Every feature is designed to be supportive, encouraging, and empowering.

## 🆘 Support

If you need help, the tool includes built-in assistance and guidance.
Just run the executable and ask for help!

---

**🤖 TAM Automation Assistant - Making your life easier, one report at a time**
EOF
    
    # Create version info
    echo "$VERSION" > "$DIST_DIR/VERSION"
    echo "$(date)" > "$DIST_DIR/BUILD_DATE"
    
    print_success "Distribution package created"
}

# Create platform-specific packages
create_platform_packages() {
    print_step "Creating platform-specific packages..."
    
    local platform=$(uname -s)
    local arch=$(uname -m)
    
    case $platform in
        "Linux")
            local package_name="tam-rfe-automation-linux-${arch}-${VERSION}.tar.gz"
            tar -czf "$DIST_DIR/$package_name" -C "$DIST_DIR" .
            print_success "Linux package created: $package_name"
            ;;
        "Darwin")
            local package_name="tam-rfe-automation-macos-${arch}-${VERSION}.tar.gz"
            tar -czf "$DIST_DIR/$package_name" -C "$DIST_DIR" .
            print_success "macOS package created: $package_name"
            ;;
        "MINGW"*|"CYGWIN"*|"MSYS"*)
            local package_name="tam-rfe-automation-windows-${arch}-${VERSION}.zip"
            cd "$DIST_DIR"
            zip -r "$package_name" .
            print_success "Windows package created: $package_name"
            ;;
        *)
            print_error "Unknown platform: $platform"
            ;;
    esac
}

# Clean up
cleanup() {
    print_step "Cleaning up build files..."
    
    # Keep dist directory, remove build directory
    rm -rf "$BUILD_DIR"
    
    print_success "Cleanup completed"
}

# Main build process
main() {
    print_header
    
    check_prerequisites
    create_build_dir
    create_requirements
    create_pyinstaller_spec
    build_executable
    create_distribution
    create_platform_packages
    cleanup
    
    echo ""
    print_success "🎉 Standalone build completed successfully!"
    echo ""
    echo "📦 Distribution files created in: $DIST_DIR"
    echo "🚀 Ready for deployment!"
    echo ""
    echo "💝 Built with passion for helping new TAMs succeed!"
}

# Run main function
main "$@"
