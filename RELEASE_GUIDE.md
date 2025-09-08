# GitHub Release Guide - DevServer Manager

## Overview

This guide explains how to create and manage GitHub releases for the DevServer Manager project using automated workflows and manual processes.

## 🚀 Quick Start

### Automated Release (Recommended)

1. **Update Version**: Edit `setup.py` and change the version number
2. **Create Release**: Run the release script:
   ```bash
   python scripts/create_release.py 1.0.0
   ```
3. **Push Changes**: Push to GitHub:
   ```bash
   git push origin main
   git push origin --tags
   ```
4. **GitHub Actions**: The workflow will automatically create the release

### Manual Release

1. **Build Executable**:
   ```bash
   python build_executable.py
   ```
2. **Create Release Package**:
   ```bash
   python scripts/create_release.py 1.0.0 --skip-tag
   ```
3. **Upload to GitHub**: Manually upload the ZIP file to GitHub Releases

## 📋 Release Process

### 1. Pre-Release Checklist

- [ ] Update version in `setup.py`
- [ ] Update `CHANGELOG.md` with new features/fixes
- [ ] Test the application thoroughly
- [ ] Ensure all tests pass
- [ ] Update documentation if needed
- [ ] Create release notes

### 2. Version Numbering

Use [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Incompatible API changes
- **MINOR** (X.Y.0): New functionality, backwards compatible
- **PATCH** (X.Y.Z): Bug fixes, backwards compatible

Examples:
- `1.0.0` - First stable release
- `1.1.0` - New features added
- `1.1.1` - Bug fixes only
- `2.0.0` - Breaking changes

### 3. Release Script Usage

```bash
# Create a new release
python scripts/create_release.py 1.0.0

# Skip building (if already built)
python scripts/create_release.py 1.0.0 --skip-build

# Skip git tagging (for testing)
python scripts/create_release.py 1.0.0 --skip-tag
```

### 4. GitHub Actions Workflow

The `.github/workflows/build-and-release.yml` workflow:

- **Triggers**: 
  - Push to tags starting with 'v'
  - Manual workflow dispatch
- **Actions**:
  - Builds executable using PyInstaller
  - Creates release package
  - Uploads artifacts
  - Creates GitHub release automatically

### 5. Release Package Contents

Each release includes:

```
DevServerManager-vX.Y.Z-Windows.zip
├── DevServerManager.exe              # Main executable
├── README.md                         # Documentation
├── PANDUAN_PENGGUNAAN.txt           # User guide (Indonesian)
├── requirements.txt                  # Dependencies info
├── server_templates.json            # Server templates
├── server_config_example.json       # Example configuration
└── CHANGELOG.md                     # Version history
```

## 🔧 Configuration

### GitHub Actions Secrets

No additional secrets required - uses `GITHUB_TOKEN` automatically.

### Build Configuration

Edit `build_executable.py` to modify:
- PyInstaller options
- Included files
- Hidden imports
- Icon and metadata

### Release Script Configuration

Edit `scripts/create_release.py` to modify:
- Version detection
- Changelog format
- Package contents
- Git operations

## 📝 Release Notes

### Template

Use `RELEASE_NOTES_TEMPLATE.md` as a starting point for release notes.

### Key Sections

1. **What's New**: New features and improvements
2. **Bug Fixes**: Issues resolved
3. **System Requirements**: Updated requirements
4. **Installation**: Step-by-step instructions
5. **Troubleshooting**: Common issues and solutions
6. **Support**: How to get help

### Examples

```markdown
## DevServer Manager v1.1.0

### ✨ New Features
- Added support for Docker containers
- Implemented server health monitoring
- Added dark theme option

### 🔧 Improvements
- Improved startup performance by 30%
- Enhanced error handling and logging
- Better memory management

### 🐛 Bug Fixes
- Fixed server status not updating correctly
- Resolved memory leak in long-running sessions
- Corrected port conflict detection
```

## 🚨 Troubleshooting

### Common Issues

**Build Fails:**
- Check Python version (3.8+ required)
- Ensure all dependencies are installed
- Verify PyInstaller is working: `pyinstaller --version`

**Release Script Fails:**
- Ensure git is configured properly
- Check that all files are committed
- Verify version format is correct

**GitHub Actions Fails:**
- Check workflow logs in GitHub Actions tab
- Ensure all required files exist
- Verify PyInstaller command works locally

**Executable Issues:**
- Test on clean Windows machine
- Check Windows Defender settings
- Verify all dependencies are included

### Debug Mode

Run build with verbose output:
```bash
python build_executable.py --verbose
```

Check PyInstaller logs:
```bash
pyinstaller --log-level DEBUG main.py
```

## 📊 Release Metrics

Track release success:

- **Download Count**: Monitor in GitHub Releases
- **Issue Reports**: Track new issues after release
- **User Feedback**: Monitor discussions and comments
- **Build Success**: Check GitHub Actions status

## 🔄 Rollback Process

If a release has critical issues:

1. **Mark as Pre-release**: Edit the release in GitHub
2. **Create Hotfix**: Create new patch version
3. **Communicate**: Update users about the issue
4. **Fix and Release**: Deploy fixed version quickly

## 📚 Additional Resources

- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyInstaller Documentation](https://pyinstaller.readthedocs.io/)

## 🤝 Contributing to Releases

### For Contributors

1. **Test Before Release**: Always test locally first
2. **Update Documentation**: Keep docs current
3. **Follow Versioning**: Use semantic versioning
4. **Write Good Commit Messages**: Clear, descriptive commits

### For Maintainers

1. **Review Changes**: Check all PRs before merging
2. **Test Releases**: Test on different Windows versions
3. **Monitor Issues**: Watch for post-release problems
4. **Update Dependencies**: Keep dependencies current

## 📞 Support

For release-related issues:

- **GitHub Issues**: [Create an issue](https://github.com/idpcks/DevServerManager/issues)
- **Discussions**: [GitHub Discussions](https://github.com/idpcks/DevServerManager/discussions)
- **Email**: idpcks.container103@slmail.me

---

**Last Updated**: 2024-01-01
**Version**: 1.0.0
