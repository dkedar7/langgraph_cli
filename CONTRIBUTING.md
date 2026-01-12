# Contributing to langgraph-utils-cli

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/langgraph-utils-cli.git
cd langgraph-utils-cli
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install in development mode**

```bash
pip install -e ".[dev]"
```

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=langgraph_utils_cli

# Run specific test file
pytest tests/test_utils.py

# Run specific test
pytest tests/test_utils.py::TestPrepareAgentInput::test_message_input
```

### Code Formatting

We use `black` for code formatting and `ruff` for linting.

```bash
# Format code
black .

# Check linting
ruff check .

# Fix auto-fixable linting issues
ruff check --fix .
```

### Type Checking

We use `mypy` for type checking (optional but recommended).

```bash
mypy langgraph_utils_cli
```

## Making Changes

1. **Create a branch**

```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes**

- Write clear, concise code
- Add tests for new functionality
- Update documentation as needed
- Follow existing code style

3. **Test your changes**

```bash
# Run tests
pytest

# Test the CLI locally
pip install -e .
langgraph-cli examples/simple_chatbot.py -m "Test"
```

4. **Commit your changes**

```bash
git add .
git commit -m "Add: brief description of changes"
```

Use conventional commit messages:
- `Add:` for new features
- `Fix:` for bug fixes
- `Update:` for changes to existing features
- `Docs:` for documentation changes
- `Test:` for test additions/changes
- `Refactor:` for code refactoring

5. **Push and create a pull request**

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Pull Request Guidelines

- **Title**: Clear, descriptive title
- **Description**: Explain what changes were made and why
- **Tests**: Ensure all tests pass
- **Documentation**: Update README or docs if needed
- **Examples**: Add examples if introducing new features

## Project Structure

```
langgraph-utils-cli/
├── langgraph_utils_cli/
│   ├── __init__.py       # Package exports
│   ├── utils.py          # Core utilities
│   └── cli.py            # CLI interface
├── examples/             # Example agents
├── tests/                # Test files
├── README.md             # Main documentation
├── CONTRIBUTING.md       # This file
├── pyproject.toml        # Package configuration
└── LICENSE               # MIT license
```

## Adding New Features

### Adding a New Utility Function

1. Add the function to `langgraph_utils_cli/utils.py`
2. Add tests to `tests/test_utils.py`
3. Export it in `langgraph_utils_cli/__init__.py`
4. Document it in the README's API Reference
5. Add an example if applicable

### Adding a New CLI Option

1. Add the option to `cli.py` using `@click.option()`
2. Update the CLI documentation in README
3. Add an example demonstrating the new option
4. Test manually with various inputs

## Testing Guidelines

- **Coverage**: Aim for >80% code coverage
- **Edge cases**: Test edge cases and error conditions
- **Integration**: Test end-to-end workflows
- **Examples**: Ensure all examples run successfully

### Writing Tests

```python
def test_my_feature():
    """Test description in present tense."""
    # Arrange
    input_data = {"test": "data"}

    # Act
    result = my_function(input_data)

    # Assert
    assert result == expected_output
```

## Documentation Guidelines

- **Docstrings**: All functions should have clear docstrings
- **Type hints**: Use type hints for function signatures
- **Examples**: Include usage examples in docstrings
- **README**: Keep README up-to-date with new features

### Docstring Format

```python
def my_function(param1: str, param2: int) -> dict:
    """
    Brief description of what the function does.

    More detailed explanation if needed. Can span
    multiple lines.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When this error occurs

    Example:
        >>> my_function("test", 42)
        {"result": "success"}
    """
    pass
```

## Code Style

- **Line length**: 100 characters (configured in pyproject.toml)
- **Imports**: Group stdlib, third-party, local
- **Naming**:
  - Functions/variables: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_CASE`
- **Comments**: Explain *why*, not *what*

## Reporting Issues

When reporting issues, please include:

1. **Environment**: Python version, OS, package version
2. **Description**: Clear description of the issue
3. **Reproduction**: Steps to reproduce the issue
4. **Expected behavior**: What you expected to happen
5. **Actual behavior**: What actually happened
6. **Error messages**: Full error messages/stack traces

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for questions or ideas
- Check existing issues/discussions first

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Your contributions make this project better for everyone. Thank you for taking the time to contribute!
