#!/usr/bin/env python3
"""
UBP-Core Setup Script

Installation script for the Universal Binary Principle implementation.
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Universal Binary Principle (UBP) computational framework implementation"

# Read requirements
def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_path):
        with open(req_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return ['numpy>=1.20.0', 'pyyaml>=5.4.0']

setup(
    name="ubp-core",
    version="1.0.0",
    author="Euan Craig",
    author_email="",
    description="Universal Binary Principle (UBP) computational framework implementation",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: Public Domain",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        'plotting': ['matplotlib>=3.3.0'],
        'testing': ['pytest>=6.0.0', 'pytest-cov>=2.10.0'],
        'dev': ['matplotlib>=3.3.0', 'pytest>=6.0.0', 'pytest-cov>=2.10.0'],
    },
    package_data={
        'ubp_core': ['spec/*.yaml', 'spec/*.md'],
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'ubp-run=ubp_vm.cli:main',
        ],
    },
    project_urls={
        "Documentation": "",
        "Source": "",
        "Tracker": "",
    },
    keywords=[
        "ubp", "universal binary principle", "computational physics", 
        "quantum computing", "toggle algebra", "bitfield", "nrci",
        "coherence", "resonance", "multi-realm", "simulation"
    ],
    zip_safe=False,
)

