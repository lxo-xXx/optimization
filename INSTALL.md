# Installation Guide

This guide provides detailed instructions for installing the Enhanced Grey Wolf Optimizer package.

## 📋 Requirements

### System Requirements
- **Python**: 3.7 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: At least 4GB RAM (8GB recommended for large problems)
- **Storage**: Minimum 100MB free space

### Python Dependencies
- `matplotlib >= 3.3.0` - For visualization and plotting
- `numpy >= 1.19.0` - For numerical computations

## 🚀 Installation Methods

### Method 1: Install from PyPI (Recommended)

```bash
pip install enhanced-gwo
```

### Method 2: Install from Source

```bash
# Clone the repository
git clone https://github.com/your-username/enhanced-gwo.git
cd enhanced-gwo

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install .
```

### Method 3: Development Installation

For contributors and developers:

```bash
# Clone the repository
git clone https://github.com/your-username/enhanced-gwo.git
cd enhanced-gwo

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

## 🐍 Virtual Environment Setup

It's highly recommended to use a virtual environment:

### Using venv (Built-in)

```bash
# Create virtual environment
python -m venv enhanced-gwo-env

# Activate virtual environment
# On Linux/macOS:
source enhanced-gwo-env/bin/activate
# On Windows:
enhanced-gwo-env\Scripts\activate

# Install the package
pip install enhanced-gwo

# Deactivate when done
deactivate
```

### Using conda

```bash
# Create conda environment
conda create -n enhanced-gwo python=3.9
conda activate enhanced-gwo

# Install dependencies
conda install matplotlib numpy

# Install the package
pip install enhanced-gwo
```

## 🔧 Optional Dependencies

### For Parallel Processing
```bash
pip install "enhanced-gwo[parallel]"
```

### For Development
```bash
pip install "enhanced-gwo[dev]"
```

### For Documentation
```bash
pip install "enhanced-gwo[docs]"
```

### All Optional Dependencies
```bash
pip install "enhanced-gwo[parallel,dev,docs]"
```

## ✅ Verification

After installation, verify that everything works correctly:

### Basic Import Test
```python
import enhanced_gwo
print(f"Enhanced GWO version: {enhanced_gwo.__version__}")
```

### Feature Test
```python
from enhanced_gwo import GWO
from enhanced_gwo.benchmarks import UF1, get_bounds

# Quick test
bounds = get_bounds('UF1', dim=5)
gwo = GWO(func=UF1, dim=5, bounds=bounds, pop_size=10, max_iter=5)
positions, objectives, hv_history = gwo.run()
print(f"Test completed successfully! Final hypervolume: {hv_history[-1]:.4f}")
```

### Run Test Suite
```bash
# Run basic tests
python -m tests.test_enhancements

# Run examples
python -m examples.demo_enhanced_gwo
python -m examples.quick_comparison
```

## 🚨 Troubleshooting

### Common Issues

#### 1. ImportError: No module named 'enhanced_gwo'
**Solution**: Make sure the package is installed:
```bash
pip install enhanced-gwo
```

#### 2. ModuleNotFoundError: No module named 'matplotlib'
**Solution**: Install required dependencies:
```bash
pip install matplotlib numpy
```

#### 3. Python version compatibility issues
**Solution**: Ensure Python 3.7+ is installed:
```bash
python --version
```

#### 4. Permission denied errors
**Solution**: Use `--user` flag for user installation:
```bash
pip install --user enhanced-gwo
```

### Platform-Specific Issues

#### Windows
- Make sure Python is added to PATH
- Use Command Prompt or PowerShell as Administrator if needed
- Consider using Anaconda for easier dependency management

#### macOS
- Install Xcode command line tools if needed:
  ```bash
  xcode-select --install
  ```
- Use Homebrew for Python installation if needed

#### Linux
- Install Python development headers:
  ```bash
  # Ubuntu/Debian
  sudo apt-get install python3-dev
  
  # CentOS/RHEL
  sudo yum install python3-devel
  ```

## 🏃 Quick Start

After installation, try this quick example:

```python
from enhanced_gwo import GWO
from enhanced_gwo.benchmarks import UF1, get_bounds

# Setup problem
bounds = get_bounds('UF1', dim=30)

# Create enhanced GWO instance
gwo = GWO(
    func=UF1,
    dim=30,
    bounds=bounds,
    pop_size=50,
    max_iter=100,
    use_differential_mutation=True,
    use_dynamic_ref=True,
    use_smart_leader_selection=True
)

# Run optimization
print("Running Enhanced GWO...")
positions, objectives, hv_history = gwo.run()

print(f"Optimization completed!")
print(f"Final archive size: {len(objectives)}")
print(f"Final hypervolume: {hv_history[-1]:.4f}")
```

## 📊 Performance Optimization

### For Large Problems
```python
# Reduce population size for faster execution
gwo = GWO(func=UF1, dim=100, bounds=bounds, pop_size=30, max_iter=50)

# Disable features for basic functionality
gwo = GWO(
    func=UF1, dim=100, bounds=bounds,
    use_differential_mutation=False,
    use_dynamic_ref=False,
    use_smart_leader_selection=False
)
```

### For Memory-Constrained Systems
```python
# Reduce archive size
gwo = GWO(func=UF1, dim=30, bounds=bounds, archive_size=50)

# Use simpler archive management
from enhanced_gwo import Archive
archive = Archive(max_size=50, use_clustering=False)
```

## 🔄 Updating

To update to the latest version:

```bash
pip install --upgrade enhanced-gwo
```

## 🗑️ Uninstallation

To remove the package:

```bash
pip uninstall enhanced-gwo
```

## 📞 Support

If you encounter issues during installation:

1. **Check the troubleshooting section** above
2. **Search existing issues** on GitHub
3. **Create a new issue** with:
   - Your operating system and Python version
   - Complete error message
   - Steps to reproduce the problem

## 📚 Next Steps

After successful installation:

1. **Read the documentation**: Check out the [README.md](README.md)
2. **Try the examples**: Run scripts in the `examples/` directory
3. **Explore the API**: Check the docstrings and [ENHANCEMENT_SUMMARY.md](ENHANCEMENT_SUMMARY.md)
4. **Join the community**: Visit our [GitHub Discussions](https://github.com/your-username/enhanced-gwo/discussions)

---

Happy optimizing with Enhanced GWO! 🐺