# Contributing to Gmail AI Assistant

Thank you for your interest in contributing to Gmail AI Assistant! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Set up the development environment:
   ```bash
   python setup.py
   ```
4. Create a new branch for your feature/fix
5. Make your changes
6. Test your changes thoroughly
7. Submit a pull request

## Development Setup

### Python Backend
- Ensure you have Python 3.7+ installed
- Install dependencies: `pip install -r requirements.txt`
- Create `config.py` from `config.example.py`
- Add your API keys to `config.py`
- Run the server: `python start.py`

### Chrome Extension
- Load the `gmail-extension` folder in Chrome
- Test functionality in Gmail
- Check browser console for any errors

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and small

## Testing

- Test both the Python backend and Chrome extension
- Verify email processing works correctly
- Test error handling scenarios
- Ensure the extension works in different Gmail layouts

## Pull Request Guidelines

1. **Clear Description**: Provide a clear description of what your PR does
2. **Testing**: Explain how you tested your changes
3. **Screenshots**: Include screenshots for UI changes
4. **Breaking Changes**: Note any breaking changes
5. **Documentation**: Update documentation if needed

## Security

- Never commit API keys or credentials
- Use environment variables or config files for sensitive data
- Follow security best practices for Chrome extensions

## Issues

When reporting issues, please include:
- Operating system and browser version
- Python version
- Steps to reproduce
- Expected vs actual behavior
- Error messages (if any)

## Questions?

Feel free to open an issue for questions or discussions about the project.
