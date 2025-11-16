# CI/CD Setup - Code Quality & Security Checks

This document describes the continuous integration and code quality checks configured for the Mail Scheduler project.

## Overview

The project uses a comprehensive quality assurance pipeline that includes:
- **Code Formatting**: Black & isort
- **Linting**: Flake8 with plugins
- **Type Checking**: MyPy
- **Security Scanning**: Bandit & Safety
- **Unit Testing**: Pytest with coverage
- **Integration Testing**: Docker Compose tests

## Running Checks Locally

### Prerequisites

Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

### Quick Run All Checks

Execute the quality check script:
```bash
./scripts/quality-check.sh
```

This runs all checks in sequence and provides a summary.

### Individual Checks

#### 1. Code Formatting

**Black** (auto-format):
```bash
black app tests
```

Check only (no changes):
```bash
black --check app tests
```

**isort** (sort imports):
```bash
isort app tests
```

Check only:
```bash
isort --check-only app tests
```

#### 2. Linting

**Flake8**:
```bash
flake8 app tests
```

With specific rules:
```bash
flake8 app tests --max-line-length=100 --exclude=migrations
```

#### 3. Type Checking

**MyPy**:
```bash
mypy app --ignore-missing-imports
```

#### 4. Security Scanning

**Bandit** (static security analysis):
```bash
bandit -r app -ll
```

Generate JSON report:
```bash
bandit -r app -f json -o bandit-report.json
```

**Safety** (dependency vulnerabilities):
```bash
safety check
```

JSON output:
```bash
safety check --json
```

#### 5. Testing

**Run all tests**:
```bash
pytest tests/ -v
```

**With coverage**:
```bash
pytest tests/ --cov=app --cov-report=html --cov-report=term-missing
```

View HTML coverage report:
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

**Run specific test types**:
```bash
pytest tests/ -m unit          # Unit tests only
pytest tests/ -m integration   # Integration tests only
pytest tests/ -m "not slow"    # Exclude slow tests
```

## GitHub Actions Workflow

The CI/CD pipeline runs automatically on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Manual trigger via GitHub UI

### Workflow Jobs

#### 1. Lint & Format
- Checks code formatting with Black
- Validates import sorting with isort
- Lints code with Flake8
- **Status**: Required to pass

#### 2. Type Check
- Runs MyPy type checking
- **Status**: Advisory (continues on error)

#### 3. Security Scan
- Runs Bandit for security issues
- Checks dependencies with Safety
- Uploads security reports as artifacts
- **Status**: Required to pass

#### 4. Unit Tests
- Runs pytest on all unit tests
- Generates coverage report
- Uploads to Codecov
- **Status**: Required to pass (with 40% coverage minimum)

#### 5. Integration Tests
- Builds Docker Compose stack using `docker-compose.ci.yml`
- Runs integration tests in containerized environment
- Tests API health endpoints
- Verifies service startup and connectivity
- **Status**: Advisory (may fail if infrastructure issues)

**Note**: Integration tests use a separate `docker-compose.ci.yml` file (instead of `docker-compose.yml`) to avoid permission issues in CI. This CI-specific configuration excludes volume mounts since the application code is baked into the Docker image during build.

#### 6. Quality Summary
- Aggregates results from all jobs
- Fails if critical checks fail
- **Status**: Final gate-keeper

### Viewing Results

1. Go to GitHub repository → Actions tab
2. Select the workflow run
3. View individual job results
4. Download artifacts (coverage reports, security scans)

## Configuration Files

- `.flake8` - Flake8 linter configuration
- `pyproject.toml` - Black, isort, MyPy, pytest, coverage config
- `.github/workflows/quality-checks.yml` - GitHub Actions workflow
- `scripts/quality-check.sh` - Local check runner script
- `docker-compose.yml` - Local development Docker configuration (with volume mounts)
- `docker-compose.ci.yml` - CI/CD Docker configuration (without volume mounts)

### Docker Compose Configuration

The project uses two Docker Compose configurations:

**`docker-compose.yml` (Local Development)**
- Includes volume mounts for hot-reload during development
- Mounts local code directory into containers: `volumes: - .:/var/www/mail-scheduler`
- Allows real-time code changes without rebuilding containers
- Used for local development with `docker-compose up -d`

**`docker-compose.ci.yml` (CI/CD)**
- Excludes volume mounts to avoid permission conflicts in CI environments
- Application code is baked into the Docker image during build
- Prevents permission errors when non-root user creates directories
- Used by GitHub Actions integration tests: `docker compose -f docker-compose.ci.yml up -d`

**Why Two Files?**
In CI environments, volume mounts can cause permission issues because:
1. The GitHub Actions runner mounts its working directory
2. The mounted directory may have different ownership/permissions
3. The non-root user (`appuser`) in containers cannot create required directories
4. By baking code into the image (no volume mounts), we avoid these permission conflicts

## Quality Standards

### Code Style
- Line length: 100 characters (Black/Flake8)
- Import sorting: Black-compatible (isort)
- Docstring style: Google format

### Testing
- Minimum coverage: 40%
- All new features must have tests
- Integration tests for API endpoints

### Security
- No high-severity Bandit issues
- All dependency vulnerabilities reviewed
- Secrets must not be committed

## Badges

Add to README.md:

```markdown
![Code Quality](https://github.com/yourusername/mail-scheduler/workflows/Code%20Quality%20&%20Security%20Checks/badge.svg)
![Coverage](https://codecov.io/gh/yourusername/mail-scheduler/branch/main/graph/badge.svg)
```

## Troubleshooting

### Black/isort conflicts
Run both tools in sequence:
```bash
isort app tests && black app tests
```

### Flake8 line too long
Increase limit in `.flake8` or break long lines:
```python
# Instead of:
very_long_function_name_with_many_parameters(param1, param2, param3, param4)

# Use:
very_long_function_name_with_many_parameters(
    param1, param2, param3, param4
)
```

### Coverage too low
Add more tests or exclude non-critical files in `pyproject.toml`:
```toml
[tool.coverage.run]
omit = ["*/migrations/*", "*/tests/*"]
```

### Security false positives
Suppress specific Bandit warnings with comments:
```python
# nosec B101
assert value is True
```

## Pre-commit Hooks (Optional)

Install pre-commit to run checks before each commit:

```bash
pip install pre-commit
pre-commit install
```

Create `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.10.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 7.1.1
    hooks:
      - id: flake8
```

## Additional Resources

- [Black Documentation](https://black.readthedocs.io/)
- [isort Documentation](https://pycqa.github.io/isort/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [MyPy Documentation](https://mypy.readthedocs.io/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
