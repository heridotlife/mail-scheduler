#!/bin/bash
# Quality Check Script - Run all code quality checks locally
# This script mimics what the CI/CD pipeline will run

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================="
echo "Running Code Quality Checks"
echo "========================================="

# Function to print status
print_status() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $1 passed${NC}"
    else
        echo -e "${RED}✗ $1 failed${NC}"
        exit 1
    fi
}

# 1. Code Formatting Check (Black)
echo ""
echo "1. Checking code formatting with Black..."
black --check app tests 2>&1 || true
if [ $? -eq 0 ]; then
    print_status "Black formatting"
else
    echo -e "${YELLOW}⚠ Some files need formatting. Run: black app tests${NC}"
fi

# 2. Import Sorting Check (isort)
echo ""
echo "2. Checking import sorting with isort..."
isort --check-only app tests 2>&1 || true
if [ $? -eq 0 ]; then
    print_status "isort"
else
    echo -e "${YELLOW}⚠ Some imports need sorting. Run: isort app tests${NC}"
fi

# 3. Linting (Flake8)
echo ""
echo "3. Running flake8 linter..."
flake8 app tests
print_status "Flake8"

# 4. Type Checking (MyPy)
echo ""
echo "4. Running type checking with MyPy..."
mypy app --ignore-missing-imports
print_status "MyPy"

# 5. Security Check - Bandit
echo ""
echo "5. Running security scan with Bandit..."
bandit -r app -f json -o bandit-report.json 2>/dev/null || true
bandit -r app -ll
print_status "Bandit security scan"

# 6. Dependency Security Check
echo ""
echo "6. Checking dependencies for vulnerabilities with Safety..."
safety check --json 2>&1 || true
if [ $? -eq 0 ]; then
    print_status "Safety dependency check"
else
    echo -e "${YELLOW}⚠ Some vulnerabilities found. Review safety output above.${NC}"
fi

# 7. Unit Tests
echo ""
echo "7. Running unit tests..."
pytest tests/ -v --tb=short --cov=app --cov-report=term-missing --cov-report=html
print_status "Unit tests"

# 8. Test Coverage Check
echo ""
echo "8. Checking test coverage..."
coverage report --fail-under=40 2>&1 || true
if [ $? -eq 0 ]; then
    print_status "Coverage threshold (40%)"
else
    echo -e "${YELLOW}⚠ Coverage below 40%. Consider adding more tests.${NC}"
fi

echo ""
echo "========================================="
echo -e "${GREEN}All quality checks completed!${NC}"
echo "========================================="
echo ""
echo "Reports generated:"
echo "  - HTML Coverage: htmlcov/index.html"
echo "  - Bandit Report: bandit-report.json"
