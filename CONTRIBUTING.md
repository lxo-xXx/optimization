# Contributing to Enhanced Grey Wolf Optimizer

We welcome contributions to the Enhanced Grey Wolf Optimizer project! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Issues

1. **Search existing issues** first to avoid duplicates
2. **Use clear, descriptive titles** for bug reports and feature requests
3. **Include system information** (OS, Python version, dependencies)
4. **Provide minimal reproducible examples** for bugs
5. **Describe expected vs actual behavior** clearly

### Suggesting Enhancements

1. **Check if the enhancement aligns** with the project goals
2. **Provide clear use cases** and motivation
3. **Consider backward compatibility** implications
4. **Include performance impact** estimates if relevant

### Pull Requests

1. **Fork the repository** and create a feature branch
2. **Follow the existing code style** and conventions
3. **Add tests** for new functionality
4. **Update documentation** as needed
5. **Ensure all tests pass** before submitting

## 📋 Development Setup

### Prerequisites

- Python 3.7+
- Required packages: `matplotlib`, `numpy`

### Installation

```bash
# Clone your fork
git clone https://github.com/your-username/enhanced-gwo.git
cd enhanced-gwo

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Running Tests

```bash
# Run basic tests
python test_enhancements.py

# Run performance comparison
python quick_comparison.py

# Run full demo
python demo_enhanced_gwo.py
```

## 🏗️ Code Standards

### Code Style

- Follow **PEP 8** Python style guide
- Use **descriptive variable names**
- Add **docstrings** for all functions and classes
- Keep functions focused and **under 50 lines** when possible
- Use **type hints** where appropriate

### Documentation

- Update **README.md** for new features
- Add **docstrings** with parameter descriptions
- Include **usage examples** in docstrings
- Update **CHANGELOG.md** with changes

### Testing

- Add **unit tests** for new functions
- Include **integration tests** for new features
- Test **backward compatibility**
- Verify **performance** doesn't regress

## 📝 Commit Guidelines

### Commit Messages

Use clear, concise commit messages:

```
feat: add sigma-sharing diversity control
fix: resolve hypervolume calculation edge case
docs: update API documentation
test: add unit tests for leader selection
refactor: improve archive management efficiency
```

### Commit Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions/changes
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `style`: Code style changes

## 🔧 Enhancement Areas

We welcome contributions in these areas:

### Algorithm Improvements

- **New operators**: Additional crossover/mutation operators
- **Adaptive parameters**: Dynamic F, CR, and sigma adjustment
- **Convergence criteria**: Improved stopping conditions
- **Scalability**: Support for larger problems

### Implementation Features

- **Parallel processing**: Full multiprocessing support
- **Visualization**: Advanced plotting capabilities
- **Benchmarks**: Additional test problems
- **Metrics**: More performance indicators

### Documentation

- **Tutorials**: Step-by-step guides
- **Examples**: Real-world applications
- **API reference**: Complete documentation
- **Performance analysis**: Detailed benchmarking

## 🎯 Project Goals

Keep these goals in mind when contributing:

1. **Scientific rigor**: All enhancements should be theoretically sound
2. **Performance**: Maintain or improve computational efficiency
3. **Usability**: Keep the API simple and intuitive
4. **Modularity**: Ensure features can be enabled/disabled
5. **Compatibility**: Maintain backward compatibility when possible

## 📊 Performance Considerations

When contributing:

- **Benchmark your changes** against the original implementation
- **Consider memory usage** for large-scale problems
- **Profile critical paths** for bottlenecks
- **Test with different problem sizes** and dimensions

## 🐛 Bug Reports

Include in bug reports:

```
**Environment:**
- OS: [e.g., Ubuntu 20.04]
- Python: [e.g., 3.8.5]
- Dependencies: [output of `pip freeze`]

**Problem:**
- Clear description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior

**Code:**
- Minimal example that reproduces the bug
- Relevant configuration settings
- Error messages and stack traces
```

## 🚀 Feature Requests

Include in feature requests:

```
**Use Case:**
- Description of the problem you're trying to solve
- Why existing functionality isn't sufficient

**Proposed Solution:**
- Detailed description of the desired feature
- How it would integrate with existing code
- Potential implementation approach

**Alternatives:**
- Other solutions you've considered
- Workarounds you're currently using
```

## 📚 Resources

- **Original GWO Paper**: Mirjalili et al. (2014)
- **Multi-objective GWO**: Mirjalili et al. (2016)
- **NSGA-II Reference**: Deb et al. (2002)
- **CEC 2009 Benchmarks**: Zhang et al. (2008)

## 🏆 Recognition

Contributors will be acknowledged in:

- **README.md** contributors section
- **CHANGELOG.md** for significant contributions
- **Academic papers** that result from this work (with permission)

## 📞 Contact

For questions about contributing:

- **Open an issue** for general questions
- **Start a discussion** for design decisions
- **Email maintainers** for sensitive issues

Thank you for contributing to the Enhanced Grey Wolf Optimizer! 🐺