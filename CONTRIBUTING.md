# Contributing to DevServer Manager

Thank you for your interest in contributing to DevServer Manager! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

Before creating an issue, please:

1. **Search existing issues** to avoid duplicates
2. **Check the documentation** in README.md and other guides
3. **Test with the latest version** to ensure the issue still exists

When creating an issue, please include:

- **Clear title** describing the problem
- **Detailed description** of the issue
- **Steps to reproduce** the problem
- **Expected vs actual behavior**
- **System information** (OS, Python version, etc.)
- **Screenshots or logs** if applicable

### Suggesting Features

We welcome feature suggestions! Please:

1. **Check existing issues** to avoid duplicates
2. **Use GitHub Discussions** for general ideas
3. **Create detailed proposals** with use cases
4. **Consider backward compatibility**

### Code Contributions

#### Getting Started

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/DevServerManager.git
   cd DevServerManager
   ```

3. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Set up development environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If available
   ```

#### Development Guidelines

##### Code Style

- **Follow PEP 8** for Python code
- **Use type hints** where appropriate
- **Write docstrings** for functions and classes
- **Use meaningful variable names**
- **Keep functions small and focused**

##### Code Structure

```
src/
├── gui/           # GUI components
├── models/        # Data models
├── services/      # Business logic
└── utils/         # Utility functions
```

##### Testing

- **Test your changes** thoroughly
- **Test on different Windows versions** if possible
- **Test with different project types** (Laravel, Node.js, etc.)
- **Verify GUI functionality** works as expected

##### Documentation

- **Update README.md** if adding new features
- **Update CHANGELOG.md** for significant changes
- **Add docstrings** for new functions
- **Update user guides** if needed

#### Submitting Changes

1. **Test your changes**:
   ```bash
   python main.py
   python build_executable.py  # Test build process
   ```

2. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add: Brief description of changes"
   ```

3. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create a Pull Request**:
   - Use the PR template
   - Provide clear description
   - Link related issues
   - Include screenshots if applicable

## 📋 Pull Request Process

### Before Submitting

- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] Changelog updated (if applicable)

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tested on Windows 10/11
- [ ] Tested with different project types
- [ ] GUI functionality verified
- [ ] Build process tested

## Screenshots (if applicable)
Add screenshots to help explain your changes

## Related Issues
Fixes #(issue number)
```

### Review Process

1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Testing** on different environments
4. **Approval** from at least one maintainer

## 🛠️ Development Setup

### Prerequisites

- Python 3.8+
- Git
- Windows 10/11 (primary development platform)

### Dependencies

```bash
pip install -r requirements.txt
```

### Development Dependencies

```bash
pip install pytest black flake8 mypy
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src

# Run specific test
python -m pytest tests/test_specific.py
```

### Code Quality

```bash
# Format code
black src/ utils/ main.py

# Lint code
flake8 src/ utils/ main.py

# Type checking
mypy src/ utils/ main.py
```

## 🎯 Areas for Contribution

### High Priority

- **Bug fixes** and stability improvements
- **Performance optimizations**
- **UI/UX improvements**
- **Documentation** improvements
- **Test coverage** improvements

### Medium Priority

- **New server templates** for additional technologies
- **Theme customization** features
- **Plugin system** for extensibility
- **Cross-platform** support improvements

### Low Priority

- **Advanced features** (monitoring, analytics)
- **Integration** with external tools
- **Mobile companion** app

## 📚 Resources

### Documentation

- [README.md](README.md) - Project overview
- [RELEASE_GUIDE.md](RELEASE_GUIDE.md) - Release process
- [DISTRIBUTION_GUIDE.md](DISTRIBUTION_GUIDE.md) - Distribution guide

### Code References

- [Python Style Guide](https://pep8.org/)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [PyInstaller Documentation](https://pyinstaller.readthedocs.io/)

### Community

- [GitHub Discussions](https://github.com/idpcks/DevServerManager/discussions)
- [Issues](https://github.com/idpcks/DevServerManager/issues)
- [Releases](https://github.com/idpcks/DevServerManager/releases)

## 🐛 Bug Reports

### Before Reporting

1. **Check existing issues**
2. **Update to latest version**
3. **Test with clean configuration**
4. **Gather relevant information**

### Bug Report Template

```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Step one
2. Step two
3. Step three

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**System Information**
- OS: Windows 10/11
- Python Version: 3.x.x
- DevServer Manager Version: x.x.x

**Screenshots/Logs**
Add screenshots or relevant log files

**Additional Context**
Any other relevant information
```

## 💡 Feature Requests

### Before Requesting

1. **Check existing feature requests**
2. **Consider if it fits project goals**
3. **Think about implementation complexity**
4. **Consider backward compatibility**

### Feature Request Template

```markdown
**Feature Description**
Clear description of the feature

**Use Case**
Why is this feature needed?

**Proposed Solution**
How should this feature work?

**Alternatives Considered**
Other ways to solve the problem

**Additional Context**
Any other relevant information
```

## 📞 Getting Help

### Community Support

- **GitHub Discussions** for general questions
- **GitHub Issues** for bugs and feature requests
- **Email** idpcks.container103@slmail.me for private matters

### Development Questions

- **Code review** questions in PR comments
- **Architecture** discussions in GitHub Discussions
- **Implementation** help in issue comments

## 🙏 Recognition

Contributors will be recognized in:

- **CONTRIBUTORS.md** file
- **Release notes** for significant contributions
- **GitHub contributors** page
- **Project documentation**

## 📄 License

By contributing to DevServer Manager, you agree that your contributions will be licensed under the [MIT License](LICENSE).

---

**Thank you for contributing to DevServer Manager!** 🚀

Your contributions help make this project better for the entire developer community.
