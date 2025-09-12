#!/usr/bin/env python3
"""Setup script for Server Manager Application

This script provides installation and packaging functionality for the Server Manager.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = ""
try:
    readme_file = this_directory / "README.md"
    if readme_file.exists():
        long_description = readme_file.read_text(encoding='utf-8')
except Exception:
    long_description = "A GUI application for managing multiple development servers"

# Read requirements
requirements = []
try:
    req_file = this_directory / "requirements.txt"
    if req_file.exists():
        requirements = req_file.read_text().strip().split('\n')
        requirements = [req.strip() for req in requirements if req.strip() and not req.startswith('#')]
except Exception:
    # Fallback requirements
    requirements = [
        "psutil>=5.8.0",
        "watchdog>=2.1.0",
    ]

setup(
    name="DevServerManager",
    version="2.1.3",
    author="idpcks",
    author_email="idpcks.container103@slmail.me",
    description="DevServer Manager v2 - A modern GUI application for managing development servers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/idpcks/DevServerManager",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "build": [
            "pyinstaller>=4.0",
            "cx-Freeze>=6.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "devserver-manager=main:main",
        ],
        "gui_scripts": [
            "server-manager-gui=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "src": ["*.py"],
        "src.gui": ["*.py"],
        "src.services": ["*.py"],
        "src.models": ["*.py"],
        "utils": ["*.py"],
        "config": ["*.json", "*.yaml", "*.yml"],
        "assets": ["*.png", "*.ico", "*.svg"],
    },
    data_files=[
        ("config", ["config/default_config.json"] if Path("config/default_config.json").exists() else []),
        ("assets", ["assets/icon.ico"] if Path("assets/icon.ico").exists() else []),
    ],
    zip_safe=False,
    keywords="server management gui development tools",
    project_urls={
        "Bug Reports": "https://github.com/idpcks/DevServerManager/issues",
        "Source": "https://github.com/idpcks/DevServerManager",
        "Documentation": "https://github.com/idpcks/DevServerManager/wiki",
    },
)