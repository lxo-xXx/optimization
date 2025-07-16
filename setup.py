from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="enhanced-gwo",
    version="1.0.0",
    author="Enhanced GWO Contributors",
    author_email="your-email@example.com",
    description="Enhanced Grey Wolf Optimizer for Multi-Objective Optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/enhanced-gwo",
    project_urls={
        "Bug Tracker": "https://github.com/your-username/enhanced-gwo/issues",
        "Documentation": "https://enhanced-gwo.readthedocs.io/",
        "Source Code": "https://github.com/your-username/enhanced-gwo",
        "Changelog": "https://github.com/your-username/enhanced-gwo/blob/main/CHANGELOG.md",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "isort>=5.0",
            "mypy>=0.900",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
            "sphinx-autodoc-typehints>=1.12",
        ],
        "parallel": [
            "joblib>=1.0",
            "multiprocessing-logging>=0.3",
        ],
    },
    keywords=[
        "grey wolf optimizer",
        "multi-objective optimization",
        "evolutionary algorithm",
        "metaheuristic",
        "pareto optimization",
        "swarm intelligence",
        "optimization",
        "machine learning",
    ],
    entry_points={
        "console_scripts": [
            "enhanced-gwo-demo=demo_enhanced_gwo:main",
            "enhanced-gwo-test=test_enhancements:main",
            "enhanced-gwo-compare=quick_comparison:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)