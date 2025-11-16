# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

# 🚨 MANDATORY: PERSONA SELECTION PROTOCOL

**CRITICAL**: Before executing ANY task in this repository, you MUST:

1. **Select your primary persona** from the available personas below
2. **Activate triadic mode** for complex tasks (Architect → Builder → Critic cycle)
3. **Log all decisions** in `docs/SESSION_LOG.md`
4. **Follow the 12 Factor Agent Principles** defined in `core/AGENTIC_GUIDE.md`

## Available Personas

### Primary Personas

**Developer Agent** → Use for: coding, debugging, implementing features
- Tools: pytest, Flask CLI, Docker, git
- Constraints: Follow existing patterns, no new architectures without Architect review
- Responsibilities: Write clean code, add tests, maintain coverage >80%

**Reviewer Agent** → Use for: PR reviews, code quality checks, security audits
- Tools: pytest, bandit, safety, semgrep, mypy, flake8
- Constraints: SOLID principles, security best practices, no breaking changes
- Responsibilities: Ensure code quality, identify security issues, verify test coverage

**Rebaser Agent** → Use for: git history cleanup, conflict resolution
- Tools: git rebase, git cherry-pick
- Constraints: Never rewrite published history, preserve commit semantics
- Responsibilities: Clean git history, resolve merge conflicts

**Merger Agent** → Use for: branch consolidation, release management
- Tools: git merge, GitHub CLI
- Constraints: Require passing CI/CD, maintain changelog
- Responsibilities: Merge branches, create releases, manage deployments

**Planner/Multiplan Manager Agent** → Use for: orchestrating multi-agent workflows
- Tools: All available tools
- Constraints: Coordinate between personas, manage dependencies
- Responsibilities: Break down complex tasks, assign to appropriate personas, track progress

### Triadic Personas (Mandatory for Complex Tasks)

**Architect Persona** → First step in triadic cycle
- Responsibilities: Define constraints, establish structure, identify risks, set invariants
- Output: Architecture constraints document, risk assessment
- Next: Pass to Builder with explicit constraints

**Builder Persona** → Second step in triadic cycle
- Responsibilities: Implement strictly within Architect's constraints
- Constraints: Cannot modify architecture decisions, must request Architect review for changes
- Output: Working implementation with tests
- Next: Pass to Critic for validation

**Critic Persona** → Third step in triadic cycle
- Responsibilities: Validate correctness, check integrity, test edge cases, security review
- Output: Validation report, identified issues, approval/rejection
- Next: Either complete or loop back to Architect/Builder

### Context Engineer Persona (Always Active)

**Responsibilities**:
- Load maximum context first (1500 lines)
- Compress context without losing constraints
- Retrieve continuously during execution
- Distinguish short-term vs long-term context
- Follow existing patterns identified in codebase

---

## Persona Selection Decision Tree

```
Is this a complex task requiring architecture design?
├─ YES → Activate Triadic Mode (Architect → Builder → Critic)
└─ NO → Continue below

What is the primary action?
├─ Writing/fixing code → Developer Agent
├─ Reviewing code/PR → Reviewer Agent
├─ Git history work → Rebaser Agent
├─ Merging branches → Merger Agent
├─ Planning multi-step work → Planner Agent
└─ Unclear → ASK USER for clarification
```

---

## 12 Factor Agent Principles (MANDATORY)

1. **Single Responsibility Persona** - One persona per task execution
2. **Deterministic Outputs** - Same input → Same output
3. **Explicit Context Loading** - Always load context before acting
4. **Token Efficiency** - Minimize redundant context
5. **State Isolation** - Use `tmp/SESSION/*` for scratchpad work
6. **Mandatory Session Logging** - Update `docs/SESSION_LOG.md` with:
   - Persona selected
   - Decisions made
   - Constraints applied
   - Risks identified
   - Outcomes achieved
7. **Reproducibility** - All actions must be reproducible
8. **Progressive Disclosure** - Load context as needed, not all at once
9. **Tool Awareness** - Use appropriate tools for each persona
10. **Read-Then-Act** - Always read files before modifying
11. **No Silent Guessing** - Ask questions when uncertain
12. **Verifiable Outputs** - All outputs must be testable/verifiable

---

## Triadic Execution Model (For Complex Tasks)

### Step 1: Architect Persona
**Input**: Task description, current codebase state
**Actions**:
- Define structural constraints
- Identify risks and edge cases
- Establish invariants
- Document architectural decisions

**Output**: Architecture constraints document
**Example**:
```markdown
## Architecture Constraints for [Task]
- MUST use service layer pattern (no direct DB access in views)
- MUST maintain >80% test coverage
- MUST follow property decorator pattern for model fields
- RISKS: Timezone handling complexity, email validation
```

### Step 2: Builder Persona
**Input**: Architecture constraints from Architect
**Actions**:
- Implement strictly within constraints
- Write tests first (TDD approach)
- Follow existing code patterns
- Request Architect review if constraints are unclear

**Output**: Implementation + tests
**Constraints Check**:
- Can I implement this without violating Architect's constraints? → YES: proceed
- Do I need to modify the architecture? → NO: continue, YES: return to Architect

### Step 3: Critic Persona
**Input**: Implementation from Builder, constraints from Architect
**Actions**:
- Validate correctness against constraints
- Test edge cases
- Security review (XSS, SQL injection, CSRF)
- Performance analysis
- Check test coverage

**Output**: Validation report
**Decision**:
- All checks pass → APPROVED: Complete
- Issues found → REJECTED: Return to Builder or Architect (depending on issue type)

### Loop Logic
```
Architect → Builder → Critic
              ↑         ↓
              └─────────┘
           (if issues found)
```

---

## Session Logging (MANDATORY)

**File**: `docs/SESSION_LOG.md`

Every session MUST log:

```markdown
## Session [YYYY-MM-DD HH:MM] - [Task Title]

### Persona Selected
- Primary: [Developer/Reviewer/Rebaser/Merger/Planner]
- Triadic: [Architect/Builder/Critic] (if applicable)

### Context Loaded
- Files read: [list]
- Constraints identified: [list]
- Patterns observed: [list]

### Decisions Made
1. [Decision 1 with rationale]
2. [Decision 2 with rationale]

### Constraints Applied
- [Constraint 1]
- [Constraint 2]

### Risks Identified
- [Risk 1 with mitigation]
- [Risk 2 with mitigation]

### Outcomes Achieved
- [Outcome 1]
- [Outcome 2]

### Next Actions
- [Action 1]
- [Action 2]
```

---

## Project Overview

Mail Scheduler is a Flask-based asynchronous email scheduling application that sends bulk emails at scheduled times. The application uses Redis Queue (RQ) for distributed job processing, PostgreSQL for persistence, and Flask-Mail for email delivery.

**Recommended Personas for Common Tasks**:
- Adding new API endpoint → Triadic Mode (Architect + Builder + Critic)
- Fixing bug → Developer Agent
- Adding tests → Builder Persona (with Critic review)
- Code review → Reviewer Agent
- Refactoring → Triadic Mode (Architect + Builder + Critic)

## Architecture

### Layered Architecture Pattern

The codebase follows a layered architecture with clear separation of concerns:

- **Presentation Layer**: Flask views (class-based) and API endpoints (Flask-RESTX)
- **Business Logic Layer**: Service classes implementing SOLID principles
- **Data Access Layer**: SQLAlchemy ORM models with property decorators
- **Job Processing Layer**: RQ async jobs for email scheduling

### Key Design Patterns

1. **Application Factory Pattern**: `create_app()` in `app/__init__.py`
2. **Repository/Service Pattern**: Business logic abstraction in `app/services/`
3. **Template Method Pattern**: `BaseService` abstract class for common CRUD operations
4. **Class-based Views**: Flask MethodView for organized route handling
5. **Property Decorators**: Model encapsulation and validation

### Multi-Container Architecture

The application runs as a distributed system via Docker Compose:

- **app**: Flask web server (port 8080)
- **worker**: RQ job worker for async tasks
- **scheduler**: RQ scheduler for timed jobs
- **postgres**: PostgreSQL database (port 5432)
- **redis**: Job queue and state management (port 6379)

## Common Development Commands

### Local Development

```bash
# Initial setup
./setup.sh
source venv/bin/activate

# Run Flask development server
flask run

# Create database tables
flask create_db

# Start RQ worker (for processing jobs)
flask rq worker

# Start RQ scheduler (for scheduled jobs)
flask rq scheduler

# Monitor job queue
flask rq info --interval 3
```

### Docker Development

```bash
# Start all services (local development with hot-reload)
docker-compose up -d

# Create database tables
docker-compose exec app flask create_db

# View logs
docker-compose logs -f app
docker-compose logs -f worker

# Stop all services
docker-compose down
```

**Note**: Two Docker Compose configurations are available:
- `docker-compose.yml` - Local development with volume mounts for hot-reload
- `docker-compose.ci.yml` - CI/CD without volume mounts to avoid permission issues

The CI configuration is used by GitHub Actions integration tests and bakes the application code into the Docker image during build.

### Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app

# Run specific test file
pytest tests/api/test_endpoints.py

# Run specific test markers
pytest -m unit           # Unit tests only
pytest -m integration    # Integration tests only
pytest -m "not slow"     # Skip slow tests
```

### Code Quality & Security

```bash
# Code formatting
black app/ tests/
isort app/ tests/

# Linting
flake8 app/ tests/
mypy app/

# Security scanning
bandit -r app/
safety check
semgrep --config=auto app/
pylint app/ --load-plugins=pylint.extensions.security

# Run local CI simulation
./test-ci-local.sh
```

### Documentation

```bash
# Generate Sphinx documentation
./generate_docs.py

# Generate and open documentation
./generate_docs.py --open
```

## Critical Architecture Details

### Email Scheduling Flow

1. **API Request**: Client sends POST to `/api/save_emails` with subject, content, timestamp, recipients
2. **Event Creation**: `EventService.create()` creates Event record in database
3. **Job Enqueuing**: `schedule_mail()` in `event/jobs.py` schedules RQ job with timestamp
4. **Background Execution**: RQ scheduler triggers `send_mail()` at scheduled time
5. **Email Delivery**: Flask-Mail sends via SMTP
6. **Status Update**: Event marked as `is_done=True` with `done_at` timestamp

### Service Layer (SOLID Principles)

All database operations MUST go through service classes, not direct model access:

```python
# Correct - Use service layer
from app.services.event_service import EventService
events = EventService.get_all()
event = EventService.create({'name': 'Subject', 'notes': 'Content'})

# Incorrect - Do not access models directly in views
from app.database.models import Event
events = Event.query.all()  # Avoid this
```

**Available Services**:
- `EventService`: Event CRUD operations (`app/services/event_service.py`)
- `RecipientService`: Recipient management (`app/services/recipient_service.py`)
- `UserService`: User authentication operations

### Configuration Classes

Multi-environment config in `app/config.py`:

- `DevelopmentConfig`: SQLite, debug enabled
- `ProductionConfig`: PostgreSQL, secure settings
- `StagingConfig`: PostgreSQL with staging credentials
- `TestingConfig`: In-memory SQLite, testing mode

Always load config via `create_app(config_class)` in `serve.py`.

### Database Models with Property Decorators

Models use property decorators for encapsulation and validation:

```python
# Example from Event model
@property
def email_subject(self) -> str:
    return self._email_subject

@email_subject.setter
def email_subject(self, value: str) -> None:
    if not value:
        raise ValueError("Email subject cannot be empty")
    self._email_subject = value
```

When adding new model fields, follow this pattern for consistency.

### Background Job Processing

All background jobs are in `app/event/jobs.py`:

- `add_event()`: Creates event and schedules mail job
- `send_mail()`: Executes email sending (decorated with `@rq.job`)
- `add_recipients()`: Bulk recipient processing
- `dt_utc()`: Timezone-aware datetime conversion

Jobs MUST be decorated with `@rq.job` to work with RQ scheduler.

### API Endpoints (Flask-RESTX)

All API routes in `app/api/routes.py` with Swagger documentation:

- `GET /api/health`: Health check for monitoring
- `POST /api/save_emails`: Schedule new email
- `GET /api/events`: List all scheduled emails
- `GET /api/events/<id>`: Get specific event details
- Swagger UI available at `/api/doc`

When adding new endpoints, update the namespace models for proper Swagger documentation.

### Authentication & Security

- Flask-Login for session management
- Password hashing with bcrypt (15 rounds)
- CSRF protection via Flask-WTF
- Role-based access control (admin, user, guest)
- URL redirect validation in auth views
- Security scanning in CI/CD (Bandit, Safety, Semgrep, Pylint)

NEVER hardcode credentials or secrets. Use environment variables in `.env` file.

## Technology Stack

- **Python 3.11+**: Base runtime
- **Flask 2.3.2**: Web framework
- **SQLAlchemy 2.0.30**: ORM with property decorators
- **Flask-RESTX 1.3.0**: RESTful API with Swagger UI
- **RQ 1.15.1 + rq-scheduler 0.10.0**: Distributed job queue
- **Redis 5.0.1**: Job queue backend
- **PostgreSQL 16**: Production database
- **Flask-Mail 0.9.1**: SMTP email integration
- **pytest 7.0.0**: Testing framework

## Testing Infrastructure

Test structure (23 test files across 6 directories):

```
tests/
├── api/              # API endpoint testing
├── database/         # Database and model testing
├── event/            # Event/job functionality
├── jobs/             # Async job testing
├── models/           # Data model validation
└── conftest.py       # Pytest fixtures and setup
```

**Test fixtures** (in `conftest.py`):
- `app`: Flask application instance
- `db`: Database session
- `client`: Flask test client
- `session`: SQLAlchemy session

**Test markers**:
- `@pytest.mark.slow`: Long-running tests
- `@pytest.mark.integration`: Multi-component tests
- `@pytest.mark.unit`: Isolated unit tests

## CI/CD Workflows

GitHub Actions workflows in `.github/workflows/`:

1. **quality-checks.yml**: Comprehensive quality assurance pipeline (main CI/CD)
   - Linting & Formatting (Black, isort, flake8)
   - Type Checking (MyPy - advisory)
   - Security Scanning (Bandit, Safety)
   - Unit Tests (pytest with 40% coverage minimum)
   - Integration Tests (Docker Compose with `docker-compose.ci.yml`)
   - Quality Summary (aggregates all results, enforces critical checks)
   - Runs on push to `main`/`develop` and all PRs

2. **pr-checks.yml**: Additional PR validation
   - Code quality, type checking, linting, tests
   - Multi-Python version compatibility (3.9-3.12)

3. **security-sast.yml**: Security scanning with Bandit, Safety, Semgrep, Pylint
   - Weekly scheduled security audits
   - PR comment summaries

4. **ci.yml**: Integration testing with PostgreSQL/Redis containers

5. **docs.yml**: Sphinx documentation generation

Security reports stored as artifacts for 30 days with PR comment summaries.

## Code Style Guidelines

- **Type hints**: Required for all function parameters and return values
- **f-strings**: Use for string formatting (not % or .format())
- **PEP 8**: Follow strictly (enforced by flake8)
- **Docstrings**: Required for all modules, classes, and public functions
- **Line length**: 88 characters (Black standard)
- **Import sorting**: isort with Black profile
- **Test coverage**: Maintain above 80%

## Important File Locations

- **Entry point**: `serve.py`
- **Application factory**: `app/__init__.py`
- **Configuration**: `app/config.py`
- **Extensions**: `app/extensions.py` (db, mail, migrate, rq, login)
- **API routes**: `app/api/routes.py`
- **Event views**: `app/event/views.py`
- **Auth views**: `app/auth/views.py`
- **Background jobs**: `app/event/jobs.py`
- **Service layer**: `app/services/` (base.py, event_service.py, recipient_service.py)
- **Models**: `app/database/models.py`
- **Environment config**: `.env` (never commit this file)
- **Docker Compose (Local)**: `docker-compose.yml` (with volume mounts for development)
- **Docker Compose (CI)**: `docker-compose.ci.yml` (without volume mounts for CI/CD)

## Database Migrations

```bash
# Create migration
flask db migrate -m "description"

# Apply migration
flask db upgrade

# Rollback migration
flask db downgrade

# Docker environment
docker-compose exec app flask db migrate -m "description"
docker-compose exec app flask db upgrade
```

## Common Development Patterns

### Adding a New API Endpoint

1. Define request/response models in `app/api/routes.py`
2. Create endpoint with `@namespace.route('/path')`
3. Use service layer for business logic
4. Add Swagger documentation with `@namespace.doc()`
5. Write tests in `tests/api/`

### Adding a New Background Job

1. Define job function in `app/event/jobs.py`
2. Decorate with `@rq.job`
3. Schedule with `scheduler.schedule()` or `queue.enqueue_at()`
4. Test with `MockScheduler` in `tests/jobs/`

### Adding a New Service

1. Extend `BaseService` in `app/services/`
2. Implement abstract methods (get_all, get_by_id, create, update, delete)
3. Add legacy method adapters if needed for backward compatibility
4. Write unit tests in `tests/models/` or `tests/database/`

## Security Best Practices

1. **Input Validation**: Always validate user input in forms and API endpoints
2. **SQL Injection**: Use SQLAlchemy parameterized queries (never raw SQL with string formatting)
3. **XSS Prevention**: Use Jinja2 autoescaping (enabled by default)
4. **CSRF Protection**: Flask-WTF CSRF tokens on all forms
5. **Authentication**: Check `@login_required` on protected routes
6. **Secrets**: Store in `.env`, never in code
7. **Dependencies**: Run `safety check` before merging PRs

## Context Engineering Rules (MANDATORY)

As outlined in `core/AGENTIC_GUIDE.md`, follow these context management rules:

### 1. Load Maximum Context First
- Read up to 1500 lines of relevant code before making changes
- Understand existing patterns and constraints
- Identify dependencies and related modules

### 2. Compress Context Without Losing Constraints
- Extract key constraints from codebase
- Document patterns observed (e.g., "All services inherit from BaseService")
- Note architectural decisions (e.g., "Property decorators for model fields")

### 3. Retrieve Continuously
- Re-read files when changes are made elsewhere
- Check for updates to dependencies
- Monitor for constraint violations

### 4. Distinguish Short-term vs Long-term Context
**Short-term**: Current task, immediate changes, active files
**Long-term**: Architecture patterns, design principles, project conventions

### 5. Follow Existing Patterns
**Identified Patterns in This Codebase**:
- Service layer for all DB operations (never direct model access in views)
- Property decorators with validation for model fields
- Class-based views with MethodView
- TDD approach: tests first, then implementation
- Environment-based configuration (Development/Production/Staging/Testing)

---

## TOON (Token Object Oriented Notation) Examples

### Developer Persona Definition
```
[TOON:PERSONA]
name: Developer Agent
role: Implements features and fixes bugs
constraints:
  - Follow service layer pattern
  - Maintain >80% test coverage
  - Use property decorators for model fields
  - No direct DB access in views
tools:
  - pytest
  - Flask CLI
  - Docker
  - git
end
```

### Triadic Workflow for Adding API Endpoint
```
[TOON:TRIADIC]
task: Add new API endpoint for email analytics

architect:
  responsibilities:
    - Define endpoint contract (request/response models)
    - Specify data aggregation requirements
    - Identify security constraints
  constraints:
    - Must use EventService for data access
    - Must include Swagger documentation
    - Must handle pagination
  risks:
    - Performance with large datasets
    - Timezone handling in aggregations

builder:
  responsibilities:
    - Implement endpoint in app/api/routes.py
    - Add service method if needed
    - Write comprehensive tests
  constraints:
    - Follow Flask-RESTX patterns
    - Use existing authentication
    - Maintain API versioning

critic:
  responsibilities:
    - Validate endpoint behavior
    - Test edge cases (empty data, invalid params)
    - Security review (authorization, input validation)
    - Performance testing
  acceptance_criteria:
    - All tests pass
    - Coverage >80%
    - No security vulnerabilities
    - Response time <200ms
end
```

### Context Engineer Workflow
```
[TOON:CONTEXT_ENGINEER]
must:
  - Load app/api/routes.py (existing API patterns)
  - Load app/services/event_service.py (data access patterns)
  - Load tests/api/ (test patterns)
  - Identify: Flask-RESTX namespace structure
  - Identify: Request/response model patterns
  - Identify: Error handling conventions
compress:
  - Extract: "All API routes use @namespace.route decorator"
  - Extract: "Models defined with api.model()"
  - Extract: "Error responses use standard format"
end
```

## Environment Variables

Required in `.env` file:

```bash
# Email Configuration
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=sender@example.com

# Flask Configuration
SECRET_KEY=your-secret-key

# Database Configuration
POSTGRES_HOST=postgres
POSTGRES_USER=postgres
POSTGRES_PASS=postgres

# Redis Configuration
REDIS_HOST=redis
```

## Debugging

### Health Check

```bash
curl http://localhost:8080/api/health
```

### View Application Routes

```bash
# Development only
curl http://localhost:8080/debug
```

### Monitor RQ Queue

```bash
# Check job queue status
flask rq info --interval 3

# View failed jobs
flask rq info --failed

# Requeue failed job
flask rq requeue <job_id>
```

### Docker Debugging

```bash
# Check service status
docker-compose ps

# View service logs
docker-compose logs -f app
docker-compose logs -f worker
docker-compose logs -f scheduler

# Execute command in container
docker-compose exec app bash
docker-compose exec postgres psql -U postgres

# Rebuild containers
docker-compose up -d --build
```

## Project-Specific Notes

- **Legacy Adapter Methods**: Services include legacy methods (e.g., `get_all_items()` calls `get_all()`) for backward compatibility with older code. New code should use modern method names.
- **Timezone Handling**: All timestamps stored as UTC. Use `dt_utc()` in `event/jobs.py` for conversions.
- **Email Content Parsing**: BeautifulSoup4 used for HTML email content sanitization.
- **Non-root Container**: Docker runs as `appuser` (UID 1000) for security.
- **Health Checks**: Docker container has health check via `/api/health` endpoint every 30s.
