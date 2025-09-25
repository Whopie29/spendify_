# Contributing to SPENDIFY

Thank you for your interest in contributing to SPENDIFY! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Issues
- Use the GitHub issue tracker to report bugs
- Include detailed information about the issue
- Provide steps to reproduce the problem
- Include your environment details (OS, Python version, etc.)

### Adding New Bank Support
To add support for a new bank:

1. **Fork the repository**
2. **Add bank configuration** in `main.py`:
   ```python
   'NEW_BANK': {
       'name': 'New Bank Name',
       'keywords': ['bank_keyword1', 'bank_keyword2'],
       'columns': {
           'date': 'Date Column Name',
           'narration': 'Description Column Name',
           'withdrawal': 'Debit Column Name',
           'deposit': 'Credit Column Name',
           'balance': 'Balance Column Name'
       }
   }
   ```
3. **Test with sample statements**
4. **Update documentation**
5. **Submit a pull request**

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add comments for complex logic
- Include docstrings for functions

### Testing
- Test your changes with different bank statements
- Ensure existing functionality still works
- Add test cases for new features

### Pull Request Process
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (`git commit -m 'Add new feature'`)
6. Push to the branch (`git push origin feature/new-feature`)
7. Open a Pull Request

## 📋 Development Setup

1. Clone the repository
2. Run `python setup.py` to set up the environment
3. Install development dependencies
4. Make your changes
5. Test locally

## 🐛 Bug Reports

When reporting bugs, please include:
- Operating system and version
- Python version
- Bank statement format (if applicable)
- Error messages
- Steps to reproduce

## 💡 Feature Requests

We welcome feature requests! Please:
- Check if the feature already exists
- Describe the use case
- Explain why it would be beneficial
- Consider implementation complexity

## 📞 Questions?

If you have questions about contributing:
- Open an issue with the "question" label
- Check existing issues and documentation
- Be specific about what you need help with

Thank you for contributing to SPENDIFY! 🎉