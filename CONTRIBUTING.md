# Contributing to Stateset Python SDK

Thank you for your interest in contributing to the Stateset Python SDK! This document provides guidelines and information for contributors.

## 🚀 Quick Start

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/stateset-python.git
   cd stateset-python
   ```
3. **Install development dependencies**:
   ```bash
   pip install -e .[dev]
   ```
4. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```
5. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📋 Development Guidelines

### Code Style

We use automated tools to maintain consistent code style:

- **Black** for code formatting
- **isort** for import sorting
- **Ruff** for linting
- **mypy** for type checking

Run all checks before committing:
```bash
# Format code
black .
isort .

# Lint code
ruff check .

# Type check
mypy stateset

# Run all checks
pre-commit run --all-files
```

### Code Quality Standards

- **Type Hints**: All public functions must have type hints
- **Docstrings**: All public functions, classes, and modules must have docstrings
- **Test Coverage**: Aim for >85% test coverage for new code
- **Error Handling**: Proper error handling with meaningful error messages

### Example Code Style

```python
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class Example:
    """Example class demonstrating code style.
    
    Args:
        name: The name of the example
        config: Optional configuration dictionary
    """
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None) -> None:
        self.name = name
        self.config = config or {}
    
    async def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process the provided data.
        
        Args:
            data: The data to process
            
        Returns:
            The processed data
            
        Raises:
            ValueError: If data is invalid
        """
        if not data:
            raise ValueError("Data cannot be empty")
        
        logger.info(f"Processing data for {self.name}")
        # Implementation here
        return {"processed": True, **data}
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=stateset --cov-report=html

# Run specific test file
pytest tests/test_client.py

# Run with specific markers
pytest -m unit
pytest -m integration
```

### Test Structure

- **Unit tests**: Test individual functions/methods in isolation
- **Integration tests**: Test interactions between components
- **End-to-end tests**: Test complete workflows against real API

### Writing Tests

```python
import pytest
from unittest.mock import AsyncMock, patch
from stateset import Stateset

class TestOrders:
    """Test cases for order operations."""
    
    @pytest.mark.asyncio
    async def test_create_order_success(self, httpx_mock, sample_order_data):
        """Test successful order creation."""
        httpx_mock.add_response(
            method="POST",
            url="https://api.test.stateset.com/orders",
            json=sample_order_data,
            status_code=201
        )
        
        client = Stateset(api_key="test_key")
        async with client:
            order = await client.orders.create({
                "customer_id": "cust_123",
                "total_amount": 99.98
            })
            
        assert order.id == sample_order_data["id"]
        assert order.customer_id == "cust_123"
    
    @pytest.mark.asyncio
    async def test_create_order_invalid_data(self):
        """Test order creation with invalid data."""
        client = Stateset(api_key="test_key")
        async with client:
            with pytest.raises(StatesetInvalidRequestError):
                await client.orders.create({})  # Empty data
```

## 📚 Documentation

### Docstring Style

We use Google-style docstrings:

```python
def function_example(param1: str, param2: Optional[int] = None) -> Dict[str, Any]:
    """Brief description of the function.
    
    Longer description if needed. This can span multiple lines and
    provide more context about the function's purpose.
    
    Args:
        param1: Description of param1
        param2: Description of param2, defaults to None
        
    Returns:
        Description of the return value
        
    Raises:
        ValueError: Description of when this is raised
        StatesetError: Description of when this is raised
        
    Example:
        Basic usage example:
        
        ```python
        result = function_example("hello", 42)
        print(result["status"])
        ```
    """
```

### README Updates

When adding significant features:
1. Add examples to the README
2. Update the feature list
3. Add any new configuration options
4. Update installation instructions if needed

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Python version** and OS
2. **SDK version**
3. **Minimal reproduction case**
4. **Expected vs actual behavior**
5. **Error messages and stack traces**

Use our bug report template:

```markdown
## Bug Description
Brief description of the bug.

## Environment
- Python version: 3.11.0
- SDK version: 1.1.0
- OS: Ubuntu 22.04

## Reproduction Steps
1. Step one
2. Step two
3. Step three

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Code Sample
```python
# Minimal code sample that reproduces the issue
from stateset import Stateset
client = Stateset()
# ... rest of the code
```

## Error Output
```
Traceback (most recent call last):
  ...
```
```

## 💡 Feature Requests

When proposing new features:

1. **Check existing issues** to avoid duplicates
2. **Describe the use case** clearly
3. **Provide examples** of how it would work
4. **Consider backwards compatibility**
5. **Discuss implementation approach** if you have ideas

Feature request template:

```markdown
## Feature Description
Brief description of the feature.

## Use Case
Describe the problem this feature would solve.

## Proposed API
```python
# Example of how the feature would be used
client = Stateset()
result = client.new_feature.do_something()
```

## Alternatives Considered
Other approaches you've considered.

## Implementation Notes
Any thoughts on implementation approach.
```

## 🔄 Pull Request Process

### Before Submitting

1. **Create an issue** first for significant changes
2. **Write tests** for your changes
3. **Update documentation** as needed
4. **Run the full test suite**
5. **Check that CI passes**

### PR Guidelines

1. **Clear title** describing the change
2. **Detailed description** explaining what and why
3. **Link related issues** using keywords (fixes #123)
4. **Keep changes focused** - one feature/fix per PR
5. **Respond to review feedback** promptly

### PR Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Added tests for new functionality
- [ ] All tests pass locally
- [ ] Updated documentation

## Related Issues
Fixes #(issue number)

## Screenshots (if applicable)

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] Any dependent changes have been merged and published
```

## 🏗️ Development Setup

### Prerequisites

- Python 3.8+
- Git
- A GitHub account

### Environment Setup

```bash
# Clone the repository
git clone https://github.com/stateset/stateset-python.git
cd stateset-python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .[dev]

# Install pre-commit hooks
pre-commit install

# Verify setup
pytest --version
black --version
ruff --version
mypy --version
```

### IDE Configuration

#### VS Code

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": false,
    "python.linting.mypyEnabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

#### PyCharm

1. Set interpreter to `./venv/bin/python`
2. Enable Black formatter in Settings > Tools > External Tools
3. Configure mypy in Settings > Editor > Inspections
4. Set import sorting to use isort with black profile

## 📦 Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

### Release Checklist

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Run full test suite
4. Create GitHub release
5. Publish to PyPI
6. Update documentation

## 🤝 Community Guidelines

### Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:

- **Be respectful** and professional
- **Be inclusive** and considerate
- **Focus on constructive feedback**
- **Help others learn and grow**

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Discord**: Real-time chat and community support
- **Email**: Private or sensitive communications

## 🎓 Learning Resources

### Python SDK Development
- [Requests documentation](https://docs.python-requests.org/)
- [httpx documentation](https://www.python-httpx.org/)
- [Pydantic documentation](https://docs.pydantic.dev/)
- [pytest documentation](https://docs.pytest.org/)

### API Design
- [RESTful API Design](https://restfulapi.net/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [API Design Guidelines](https://github.com/microsoft/api-guidelines)

### Testing
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [pytest Good Practices](https://docs.pytest.org/en/stable/explanation/goodpractices.html)
- [Mock Testing](https://docs.python.org/3/library/unittest.mock.html)

## 📞 Getting Help

If you need help:

1. **Check the documentation** first
2. **Search existing issues** on GitHub
3. **Ask in Discord** for quick questions
4. **Create a GitHub issue** for bugs or feature requests
5. **Email the maintainers** for private concerns

Remember: No question is too small! We're here to help you contribute successfully.

---

Thank you for contributing to the Stateset Python SDK! 🎉