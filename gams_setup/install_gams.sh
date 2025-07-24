#!/bin/bash
# GAMS Installation Script for Linux
# Run this script after placing GAMS installer in install/ directory

set -e  # Exit on any error

echo "🚀 GAMS Installation Script"
echo "=========================="

# Check if running as root (not recommended for GAMS)
if [ "$EUID" -eq 0 ]; then
    echo "⚠️  Warning: Running as root. GAMS installation is recommended for regular users."
fi

# Create directories
echo "📁 Creating directories..."
mkdir -p install downloads

# Check for existing GAMS installation
if command -v gams &> /dev/null; then
    echo "✅ GAMS already installed at: $(which gams)"
    gams --version
    echo "Do you want to proceed with new installation? (y/N)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "Exiting..."
        exit 0
    fi
fi

# Look for GAMS installer
INSTALLER=""
if [ -f "install/linux_x64_64_sfx.exe" ]; then
    INSTALLER="install/linux_x64_64_sfx.exe"
elif [ -f "install/gams_linux_x64.exe" ]; then
    INSTALLER="install/gams_linux_x64.exe"
else
    echo "❌ GAMS installer not found in install/ directory"
    echo "Please download GAMS installer from: https://www.gams.com/download/"
    echo "Place it in the install/ directory and run this script again"
    echo ""
    echo "Expected filename: linux_x64_64_sfx.exe or gams_linux_x64.exe"
    exit 1
fi

echo "📦 Found GAMS installer: $INSTALLER"

# Make installer executable
chmod +x "$INSTALLER"

# Install GAMS
echo "🔧 Installing GAMS..."
GAMS_DIR="$HOME/gams"
mkdir -p "$GAMS_DIR"

# Run installer (typically extracts to current directory)
echo "Running GAMS installer..."
./"$INSTALLER" -d "$GAMS_DIR"

# Find GAMS installation directory
GAMS_SYSTEM_DIR=$(find "$GAMS_DIR" -name "gams" -type f | head -1 | xargs dirname)

if [ -z "$GAMS_SYSTEM_DIR" ]; then
    echo "❌ GAMS installation failed or directory not found"
    exit 1
fi

echo "✅ GAMS installed to: $GAMS_SYSTEM_DIR"

# Add to PATH
echo "🔧 Configuring PATH..."
echo "" >> ~/.bashrc
echo "# GAMS Configuration" >> ~/.bashrc
echo "export GAMS_PATH=\"$GAMS_SYSTEM_DIR\"" >> ~/.bashrc
echo "export PATH=\"\$GAMS_PATH:\$PATH\"" >> ~/.bashrc

# Also add to current session
export GAMS_PATH="$GAMS_SYSTEM_DIR"
export PATH="$GAMS_PATH:$PATH"

# Verify installation
echo "🧪 Verifying GAMS installation..."
if command -v gams &> /dev/null; then
    echo "✅ GAMS successfully installed!"
    gams --version
else
    echo "❌ GAMS installation verification failed"
    echo "Try running: source ~/.bashrc"
    exit 1
fi

# Install Python API
echo "🐍 Installing GAMS Python API..."
pip install gamsapi || echo "⚠️  Warning: Failed to install gamsapi. You may need to install it manually."

# Install additional optimization libraries
echo "📚 Installing additional optimization libraries..."
pip install pyomo || echo "⚠️  Pyomo installation failed"

# Create test model
echo "📝 Creating test model..."
cat > gams_setup/models/test_model.gms << 'EOF'
$title Simple Test Model

Sets
    i   'supply points'  / seattle, san-diego /
    j   'demand points'  / new-york, chicago, topeka /;

Parameters
    a(i)  'capacity of plant i in cases'
          / seattle     350
            san-diego   600 /

    b(j)  'demand at market j in cases'
          / new-york    325
            chicago     300
            topeka      275 /;

Table d(i,j)  'distance in thousands of miles'
                  new-york       chicago      topeka
    seattle          2.5           1.7          1.8
    san-diego        2.5           1.8          1.4  ;

Scalar f  'freight in dollars per case per thousand miles'  /90/ ;

Parameter c(i,j)  'transport cost in thousands of dollars per case';
          c(i,j) = f * d(i,j) / 1000;

Variables
    x(i,j)  'shipment quantities in cases'
    z       'total transportation costs in thousands of dollars';

Positive Variable x;

Equations
    cost        'define objective function'
    supply(i)   'observe supply limit at plant i'
    demand(j)   'satisfy demand at market j';

cost ..        z  =e=  sum((i,j), c(i,j)*x(i,j));
supply(i) ..   sum(j, x(i,j))  =l=  a(i);
demand(j) ..   sum(i, x(i,j))  =g=  b(j);

Model transport /all/;
Solve transport using lp minimizing z;

Display x.l, x.m;
EOF

# Test GAMS installation
echo "🧪 Testing GAMS with sample model..."
cd gams_setup/models
if gams test_model.gms; then
    echo "✅ GAMS test successful!"
else
    echo "❌ GAMS test failed"
fi
cd ../..

echo ""
echo "🎉 GAMS Setup Complete!"
echo "====================="
echo ""
echo "📍 GAMS installed at: $GAMS_SYSTEM_DIR"
echo "🔧 Configuration added to ~/.bashrc"
echo "📝 Test model created at: gams_setup/models/test_model.gms"
echo ""
echo "🚀 Next Steps:"
echo "1. Restart your terminal or run: source ~/.bashrc"
echo "2. Add reference materials to gams_setup/references/"
echo "3. Add model examples to gams_setup/examples/"
echo "4. Start creating optimized models!"
echo ""
echo "💡 Tip: You may need a GAMS license for full functionality"
echo "   Free demo license available at: https://www.gams.com/download/"