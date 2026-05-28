# Contributing to Hyper PDF Editor

Thank you for your interest in contributing! Here's how to get started.

## Development Setup

1. Fork the repository
2. Clone your fork
3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

## Code Style

- Format code with `black`: `black src tests`
- Lint with `flake8`: `flake8 src tests`
- Type check with `mypy`: `mypy src`

## Testing

Before submitting a PR, ensure all tests pass:
```bash
pytest tests/ -v --cov=src
```

## Commit Guidelines

- Write clear, descriptive commit messages
- Use conventional commits: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`
- Reference issues when applicable: `Closes #123`

## Pull Request Process

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make your changes
3. Write tests for new functionality
4. Update documentation
5. Push to your fork
6. Open a pull request with a clear description

## Issues

Feel free to open issues for:
- Bug reports
- Feature requests
- Documentation improvements
- Questions

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
