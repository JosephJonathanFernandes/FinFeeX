# Security Policy

## 🔒 Reporting Security Issues

We take security seriously. If you discover a security vulnerability, please email us directly instead of opening a public issue.

**Email**: Create a private security advisory on GitHub

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

## ✅ Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | ✅ Yes             |

## 🛡️ Security Best Practices

### For Users

- **Never share your API keys** in screenshots or reports
- **Don't upload sensitive statements** to public demos
- **Verify the source** before running the code
- **Run locally** for maximum privacy

### For Developers

- **No hardcoded secrets** in code
- **Sanitize inputs** from file uploads
- **Use environment variables** for sensitive data
- **Keep dependencies updated**

## 📋 Known Security Considerations

### Data Privacy

- ✅ Files are processed in-memory only
- ✅ No data is stored permanently
- ✅ No external API calls (except optional OpenAI)
- ⚠️ If using OpenAI, statement text is sent to their API

### Dependencies

We regularly update dependencies to patch security vulnerabilities. Run:

```powershell
pip install --upgrade -r requirements.txt
```

## 🔄 Security Updates

Check our [CHANGELOG.md](CHANGELOG.md) for security-related updates.

## ⚖️ Responsible Disclosure

We follow a 90-day disclosure policy:

1. Report received → Acknowledged within 48 hours
2. Fix developed → Released within 30 days
3. Public disclosure → After fix is deployed

Thank you for helping keep FinFeeX secure! 🙏
