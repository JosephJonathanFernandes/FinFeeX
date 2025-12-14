# 🤝 Contributing to FinFeeX

Thank you for your interest in contributing to FinFeeX! We appreciate all contributions, from bug reports to feature implementations.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Guidelines](#coding-guidelines)

## 📜 Code of Conduct

This project adheres to our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you're expected to uphold this code.

## 🎯 How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Description**: Clear description of the issue
- **Steps to Reproduce**: Detailed steps to reproduce the behavior
- **Expected Behavior**: What you expected to happen
- **Screenshots**: If applicable
- **Environment**: OS, Python version, browser

### 💡 Suggesting Features

Feature suggestions are welcome! Please include:

- **Use Case**: Why is this feature valuable?
- **Proposed Solution**: How should it work?
- **Alternatives**: Other solutions you've considered

### 🔧 Code Contributions

1. **Small PRs**: Keep changes focused and atomic
2. **Tests**: Add tests for new functionality
3. **Documentation**: Update docs for user-facing changes
4. **Style**: Follow existing code patterns

## 🛠️ Development Setup

### Prerequisites

- Python 3.11+
- Git

### Setup Steps

```powershell
# Clone the repository
git clone https://github.com/JosephJonathanFernandes/FinFeeX.git
cd FinFeeX

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest -v

# Start the app
streamlit run app.py
```

### Project Structure

```
FinFeeX/
├── app.py              # Main Streamlit app
├── src/                # Core logic
│   ├── costs.py        # Fee annualization
│   ├── fee_detector.py # Detection logic
│   ├── pdf_parser.py   # PDF extraction
│   └── summarizer.py   # Reports & emails
├── tests/              # Unit tests
└── pages/              # Additional Streamlit pages
```

## 🔄 Pull Request Process

1. **Fork & Branch**: Create a feature branch from `main`
   ```powershell
   git checkout -b feature/your-feature-name
   ```

2. **Commit**: Make atomic commits with clear messages
   ```powershell
   git commit -m "feat: add new fee detection pattern"
   ```

3. **Test**: Ensure all tests pass
   ```powershell
   pytest -v
   ```

4. **Push**: Push to your fork
   ```powershell
   git push origin feature/your-feature-name
   ```

5. **PR**: Open a pull request with:
   - Clear title and description
   - Reference to related issues
   - Screenshots (if UI changes)

### Commit Message Convention

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions/changes
- `refactor:` Code restructuring
- `style:` Formatting changes
- `chore:` Maintenance tasks

## 📝 Coding Guidelines

### Python Style

- Follow PEP 8
- Use type hints
- Write docstrings for functions
- Keep functions focused and small

### Testing

- Write tests for new features
- Maintain or improve test coverage
- Test edge cases

### Security

- **Never commit**: API keys, secrets, or credentials
- Use environment variables for sensitive data
- Validate user inputs

### UI/UX

- Keep interface intuitive
- Add helpful tooltips
- Ensure mobile responsiveness
- Test with sample data

## 🎨 Areas for Contribution

### High Priority

- [ ] Add support for more currencies
- [ ] Improve fee detection accuracy
- [ ] Add historical trend analysis
- [ ] Implement comparison mode

### Good First Issues

- [ ] Add more test cases
- [ ] Improve documentation
- [ ] Fix typos
- [ ] Add tooltips to UI elements

### Advanced

- [ ] Multi-language support
- [ ] OCR for scanned PDFs
- [ ] Bank API integrations
- [ ] Machine learning for detection

## ❓ Questions?

- Open a [GitHub Discussion](https://github.com/JosephJonathanFernandes/FinFeeX/discussions)
- Tag maintainers in issues
- Check existing documentation

## 🙏 Thank You!

Your contributions make FinFeeX better for everyone. We appreciate your time and effort!

---

**Made with ❤️ by the FinFeeX community**
