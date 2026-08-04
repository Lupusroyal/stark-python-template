# Stark Python Template

<p align="center">
  <a href="https://github.com/Lupusroyal/stark-python-template">
    <img src="https://img.shields.io/badge/python-3.12+-blue.svg" alt="Python Version">
    <img src="https://img.shields.io/badge/FastAPI-production-green.svg" alt="FastAPI">
    <img src="https://img.shields.io/badge/PostgreSQL-17-blue.svg" alt="PostgreSQL">
    <img src="https://img.shields.io/badge/Docker-ready-blue.svg" alt="Docker">
  </a>
</p>

<p align="center">
  <a href="https://github.com/Lupusroyal/stark-python-template/actions/workflows/ci.yml">
    <img src="https://github.com/Lupusroyal/stark-python-template/actions/workflows/ci.yml/badge.svg" alt="CI">
  </a>
  <a href="https://github.com/Lupusroyal/stark-python-template/actions/workflows/codeql.yml">
    <img src="https://github.com/Lupusroyal/stark-python-template/actions/workflows/codeql.yml/badge.svg" alt="CodeQL">
  </a>
</p>

A professional production-ready REST API template built with Python and FastAPI.

---

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Features](#features)
  - [API Core](#api-core)
  - [Database](#database)
  - [Authentication](#authentication)
  - [Authorization (RBAC)](#authorization-rbac)
  - [Audit System](#audit-system)
  - [Security](#security)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Development](#development)
- [Testing](#testing)
- [Production](#production)
- [Database Management](#database-management)
- [Authentication Flow](#authentication-flow)
- [API Documentation](#api-documentation)
- [Development Commands](#development-commands)
- [Code Quality](#code-quality)
- [CI/CD](#cicd)
- [Production Checklist](#production-checklist)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Stark Python Template is a professional backend template for building modern, scalable REST APIs using Python and FastAPI.

The project provides a complete foundation with:

- Clean layered architecture
- Authentication and authorization
- Role-Based Access Control (RBAC)
- Permission management
- Administrative auditing
- Automated testing
- Security middleware
- Docker infrastructure
- Continuous Integration

The goal is to provide a reusable, secure, and production-ready starting point for enterprise backend applications.

---

## Quick Start

Get the development environment up and running in a few simple steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Lupusroyal/stark-python-template.git
   cd stark-python-template
   ```

2. **Copy the environment configuration:**
   ```bash
   cp .env.example .env
   ```

3. **Start the development environment:**

   The default environment uses Docker Compose with PostgreSQL.

   ```bash
   docker compose up -d
   # or
   make run
   ```

4. **Access interactive API documentation:**
   Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.

---

## Features

### API Core
- **FastAPI Framework:** High-performance async REST API capabilities.
- **OpenAPI & Interactive Docs:** Automated Swagger UI and ReDoc endpoints.
- **Layered Architecture:** Clean separation between routes, services, repositories, and models.
- **Dependency Injection:** Native FastAPI dependency injection management.
- **Environment Configuration:** Type-safe settings using Pydantic Settings.
- **Global Exception Handling:** Standardized error responses across all API routes.

### Database
- **PostgreSQL 17:** Robust, relational database management system.
- **SQLAlchemy ORM:** Modern async/sync Object-Relational Mapping.
- **Alembic Migrations:** Database schema versioning and seamless migration management.
- **Structured Database Models:** Production-ready relational entities.

### Authentication
- **JWT Authentication:** JSON Web Token issuance and validation.
- **Bearer Token Authorization:** Standard Authorization header validation.
- **Dual Token Architecture:** Support for Access Tokens and Refresh Tokens.
- **Refresh Token Rotation:** Enhanced security with token rotation upon refresh.
- **Token Revocation:** Ability to invalidate active refresh tokens.
- **Secure Hashing:** Industry-standard password hashing functions.

### Authorization (RBAC)
Role-Based Access Control system for granular access management:

- **Entities:** Users, Roles, and Permissions.
- **Protected Routes:** Administrative endpoints restricted by permission requirements.
- **Granular Management:** Dynamically attach or detach permissions from roles and users.

```text
ADMIN
├── users.read
├── users.update
├── permissions.create
└── audit.read
```

### Audit System
Comprehensive logging and auditing for administrative actions:

- **Tracked Operations:** Permission creation/updates/deletion, role modifications, user activation/deactivation, and administrative actions.
- **Audit Log Metadata:**
  - Responsible User ID
  - Executed Action Name
  - Target Resource
  - Event Details / Context
  - Timestamp

### Security
Multi-layer security setup configured out-of-the-box:

- **Security Headers:**
  - `X-Content-Type-Options`
  - `X-Frame-Options`
  - `Referrer-Policy`
  - `Permissions-Policy`
  - `Content-Security-Policy`
  - `Cross-Origin-Opener-Policy`
  - `Cross-Origin-Resource-Policy`
- **Request Tracking:**
  - `X-Request-ID`: Unique tracking identifier for every request.
  - `X-Process-Time`: Execution latency metric header.
- **Trusted Hosts & CORS:** Configurable allowed hosts and CORS origins for secure production deployments.

---

## Technology Stack

- **Language:** Python 3.12+
- **Framework:** FastAPI
- **Configuration:** Pydantic Settings
- **ORM & DB:** SQLAlchemy, PostgreSQL 17
- **Migrations:** Alembic
- **Package Manager:** UV
- **Containerization:** Docker, Docker Compose
- **Quality & Testing:** Pytest, Ruff, MyPy, pre-commit

---

## Project Structure

```text
.
├── .env.example
├── .env.test
├── .env.production
├── Dockerfile
├── Makefile
├── README.md
├── alembic/
├── docker-compose.yml
├── docker-compose.test.yml
├── docker-compose.prod.yml
├── docs/
├── pyproject.toml
├── scripts/
├── src/
│   └── stark/
│       ├── api/
│       │   └── routes/
│       ├── core/
│       ├── dependencies/
│       ├── middleware/
│       ├── models/
│       ├── repositories/
│       ├── schemas/
│       └── services/
└── tests/
```

---

## Configuration

Environment variables control overall application behavior. Configure your `.env` files based on your active target environment (`.env`, `.env.test`, `.env.production`).

## Environments

The project contains three isolated environments:

| Environment | Purpose | Compose File |
|---|---|---|
| Development | Local development | docker-compose.yml |
| Testing | Automated tests | docker-compose.test.yml |
| Production | Deployment | docker-compose.prod.yml |

### Development

```bash
docker compose up -d
```

Uses:

-API port: 8000
-PostgreSQL port: 5432

Testing

```bash
docker compose -p stark-test -f docker-compose.test.yml up -d
```

Uses:

-PostgreSQL port: 5433
-Isolated database volume

Production

```bash
docker compose -p stark-prod -f docker-compose.prod.yml up -d
```

Uses:

-Production environment variables
-Isolated Docker network
-No exposed PostgreSQL port

### Key Environment Variables

| Variable | Description | Default / Example |
| :--- | :--- | :--- |
| `APP_NAME` | Name of the application | `Stark API` |
| `APP_VERSION` | Application version | `0.1.0` |
| `APP_ENV` | Application environment (`development`, `test`, `production`) | `development` |
| `DEBUG` | Enable debug mode | `false` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+psycopg://postgres:postgres@postgres:5432/stark_db` |
| `SECRET_KEY` | Secret key for JWT signature (**Change in production**) | `your_secret_key` |
| `ALGORITHM` | JWT signing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access Token longevity in minutes | `30` |
| `API_PORT` | Host port for API container | `8000` |
| `POSTGRES_PORT` | Host port for PostgreSQL container | `5432` |

> **Note:** Customize `API_PORT` and `POSTGRES_PORT` if running multiple service instances simultaneously (e.g., instance 1 on ports `8000`/`5432` and instance 2 on `8001`/`5433`).

---

## Development

Local development uses `docker-compose.yml` to spin up services seamlessly.

1. **Install dependencies locally (optional, for IDE support):**
   ```bash
   uv sync
   ```

2. **Start development containers:**
   ```bash
   docker compose up -d
   # or
   make run
   ```
   *Services started:*
   - FastAPI API server on `http://localhost:8000`
   - PostgreSQL 17 Database on port `5432`

3. **Check running containers:**
   ```bash
   docker compose ps
   ```

4. **Stop development services:**
   ```bash
   docker compose down
   ```

---

## Testing

A dedicated container configuration `docker-compose.test.yml` isolates testing from active development databases.

### Running Tests

Execute the full suite using isolated test services:

```bash
docker compose -f docker-compose.test.yml up --build --exit-code-from test
```

Alternatively, run tests locally via UV:

```bash
uv run pytest
# or
make test
```

### Test Coverage Areas
- Authentication & JWT Token management
- User CRUD & Management
- Role & Permission RBAC
- Audit Trail System
- Security Headers & Middleware
- Global Exception Handlers

---

## Production

docker compose -p stark-prod -f docker-compose.prod.yml exec stark-api alembic upgrade head

### Key Production Differences
- Reload flags are disabled and worker processes are scaled.
- `DEBUG` is set to `false`.
- Environment variables require strong secrets (`SECRET_KEY`).
- Restrictive CORS and Trusted Host settings are enforced.

### Deploying and Creating Administrative User

1. **Start production stack:**
   ```bash
   docker compose -f docker-compose.prod.yml up -d --build
   ```

2. **Execute database migrations:**
   ```bash
   docker compose -f docker-compose.prod.yml exec api alembic upgrade head
   ```

3. **Create initial Admin user:**
   Run the administrative creation script inside the container:
   ```bash
   docker compose -p stark-prod -f docker-compose.prod.yml exec stark-api \
   uv run python scripts/create_admin.py
   ```

---

## Database Management

Database migrations are managed via **Alembic**.

- **Apply pending migrations:**
  ```bash
  uv run alembic upgrade head
  # or
  make migrate
  ```

- **Generate new migration:**
  ```bash
  uv run alembic revision --autogenerate -m "describe_your_changes"
  ```

---

## Authentication Flow

The authentication flow utilizes rotating JSON Web Tokens (JWT):

```text
[ User Credentials ] ──> Login ──> Generates [ Access Token + Refresh Token ]
                                                   │
[ Protected API Requests ] <── Access Granted <────┤
                                                   │
[ Access Token Expired ] ──> Refresh Request ─────>┴──> Validates Refresh Token
                                                            ├── Issues New Access & Refresh Tokens
                                                            └── Invalidates Old Tokens (Rotation)
                                                                
[ Logout Request ] ────────> Invalidates Current Refresh Token (Revocation)
```

1. **Login:** User authenticates via `/auth/login` to receive an `Access Token` (short-lived) and `Refresh Token` (long-lived).
2. **Access Token:** Used in the `Authorization: Bearer <token>` header to access protected resources.
3. **Refresh:** When expired, `/auth/refresh` issues a new token pair using token rotation.
4. **Logout:** Calling `/auth/logout` revokes the refresh token, terminating the session.

---

## API Documentation

Interactive API documentation is automatically generated from Pydantic schemas and OpenAPI definitions:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Health Check

Verify system operational status:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

---

## Development Commands

All standard development tasks are organized via `Makefile` and `uv`:

| Action | Makefile Command | Direct Command |
| :--- | :--- | :--- |
| **Install Dependencies** | `make install` | `uv sync` |
| **Run Application** | `make run` | `docker compose up -d` |
| **Run Migrations** | `make migrate` | `uv run alembic upgrade head` |
| **Run Tests** | `make test` | `uv run pytest` |
| **Lint Code** | `make lint` | `uv run ruff check .` |
| **Format Code** | `make format` | `uv run ruff format .` |
| **Type Checking** | - | `uv run mypy .` |
| **Clean Cache** | `make clean` | `find . -type d -name "__pycache__" -exec rm -r {} +` |

---

## Docker Environment Commands

### Development

Start:

```bash
docker compose up -d
```

Stop:

docker compose down
```

Testing

Start:

```bash
docker compose -p stark-test -f docker-compose.test.yml up -d
```

Stop:

```bash
docker compose -p stark-test -f docker-compose.test.yml down
Production
```

Start:

```bash
docker compose -p stark-prod -f docker-compose.prod.yml up -d
```

Stop:

```bash
docker compose -p stark-prod -f docker-compose.prod.yml down
```

---

## Code Quality

Maintain codebase standards using integrated quality tools:

- **Ruff (Linter & Formatter):**
  ```bash
  uv run ruff check .
  uv run ruff format .
  ```

- **MyPy (Static Type Checker):**
  ```bash
  uv run mypy .
  ```

- **Pytest (Test Suite):**
  ```bash
  uv run pytest
  ```

- **pre-commit:**
  Automatically runs linter and style checks prior to git commits.
  ```bash
  uv run pre-commit run --all-files
  ```

---

## CI/CD

Automated CI/CD workflows run via **GitHub Actions**:

- **Continuous Integration (`ci.yml`):**
  - Executes code linting with **Ruff**.
  - Enforces static type checking with **MyPy**.
  - Runs automated test suite via **Pytest**.
- **CodeQL (`codeql.yml`):**
  - Performs static security scanning and vulnerability analysis on every pull request and push to primary branches.
- **Dependabot:**
  - Monitors and automates pull requests for outdated Python dependencies and GitHub Actions.

---

## Production Checklist

Before deploying to production, verify the following checklist:

- [ ] **Security Keys:** Replace default `SECRET_KEY` with a strong, randomly generated string.
- [ ] **Environment:** Set `APP_ENV=production` and `DEBUG=false`.
- [ ] **Database:** Configure a managed PostgreSQL database instance.
- [ ] **Network & CORS:** Set explicit domains in `ALLOWED_HOSTS` and `CORS_ORIGINS`.
- [ ] **Admin User:** Run `uv run python scripts/create_admin.py` to seed administrative credentials.
- [ ] **Database Migrations:** Ensure `alembic upgrade head` is executed during deployment.
- [ ] **Observability:** Verify logging output, monitoring hooks, and automated database backup routines.
- [ ] **Docker:** Verify production containers are running with isolated network.
- [ ] **Database Exposure:** PostgreSQL should not expose public ports.
- [ ] **Health Checks:** Confirm API health endpoint is responding.
---

## Contributing

Contributions are strictly welcomed! Please follow these steps before submitting a Pull Request:

1. Fork the repository and create your feature branch (`git checkout -b feature/amazing-feature`).
2. Run quality checks locally to ensure all tests and linters pass:
   ```bash
   uv run pytest
   uv run ruff check .
   uv run mypy .
   ```
3. Commit your changes without including sensitive data or secrets.
4. Push to the branch and open a Pull Request.

---

## License

This project is licensed under the [MIT License](LICENSE).
