"""
Contributing Guide for NLP Hub

Thank you for your interest in contributing to NLP Hub!
"""

# Development Setup

## Prerequisites

- Python 3.9+
- git
- Virtual environment tool (venv or conda)

## Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/Yacine-ai-tech/my_NLP_Journey.git
cd my_NLP_Journey

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Code Standards

### Style Guide

We follow PEP 8 with some exceptions:

- **Line length**: 100 characters
- **Docstrings**: Google style
- **Type hints**: Required for all functions

### Formatting

```bash
# Format code with Black
black src/

# Sort imports
isort src/

# Lint with Flake8
flake8 src/

# Type checking
mypy src/
```

### Docstring Example

```python
def classify(self, text: str) -> Intent:
    """
    Classify intent of the given text.
    
    Args:
        text: Input text to classify
    
    Returns:
        Intent prediction result
    
    Raises:
        ProcessingError: If classification fails
    
    Example:
        >>> classifier = get_intent_classifier()
        >>> intent = classifier.classify("What's the weather?")
        >>> print(intent.name)
        question
    """
    pass
```

## Testing

### Writing Tests

- Place unit tests in `tests/unit/`
- Place integration tests in `tests/integration/`
- Use descriptive test names starting with `test_`

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/unit/test_intent.py

# Run with verbose output
pytest -v
```

### Test Example

```python
def test_classify_greeting():
    """Test classifying greeting."""
    classifier = get_intent_classifier("dummy")
    intent = classifier.classify("Hello!")
    assert intent.name == "greeting"
    assert intent.confidence > 0.8
```

## Creating a Pull Request

### Step 1: Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### Step 2: Make Changes

- Write code following code standards
- Add tests for new functionality
- Update documentation

### Step 3: Run Tests and Checks

```bash
# Format code
black src/
isort src/

# Run tests
pytest

# Check linting
flake8 src/

# Type checking
mypy src/
```

### Step 4: Commit and Push

```bash
git add .
git commit -m "feat: Add your feature description"
git push origin feature/your-feature-name
```

### Step 5: Open Pull Request

- Go to GitHub repository
- Click "New Pull Request"
- Fill in description and related issues
- Submit PR

## Commit Message Convention

Use Conventional Commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting changes
- `refactor`: Code refactoring
- `test`: Test additions/modifications
- `chore`: Build process, dependencies

### Examples

```
feat(intent): Add confidence threshold filtering

fix(entity): Handle multi-word entity extraction

docs(readme): Update installation instructions

test(rag): Add retrieval tests
```

## Code Review Process

1. **Automated Checks**: CI/CD pipeline runs tests and linting
2. **Code Review**: Maintainers review code quality
3. **Approval**: PR approved when all checks pass
4. **Merge**: Squash merge to main branch

## Reporting Issues

### Bug Reports

Include:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment (Python version, OS, etc.)
- Error logs/stack traces

### Feature Requests

Include:
- Clear use case
- Proposed solution
- Alternative approaches
- Any related discussions

## Areas for Contribution

### High Priority

- [ ] Fine-tuned models for French and Hausa
- [ ] Database persistence layer
- [ ] Advanced RAG features
- [ ] Performance optimization
- [ ] API documentation

### Medium Priority

- [ ] Additional language support
- [ ] Enhanced error handling
- [ ] Logging improvements
- [ ] Configuration management
- [ ] Deployment guides

### Low Priority

- [ ] UI/Dashboard
- [ ] Examples and tutorials
- [ ] Community models
- [ ] Blog posts

## Getting Help

- 💬 GitHub Discussions: https://github.com/Yacine-ai-tech/my_NLP_Journey/discussions
- 📧 Email: siddoyacinetech227@gmail.com
- 🐛 GitHub Issues: https://github.com/Yacine-ai-tech/my_NLP_Journey/issues
- 📚 Documentation: See [INDEX.md](INDEX.md)

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

Thank you for contributing! 🙏
