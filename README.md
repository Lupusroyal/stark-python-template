# Stark Python Template

<p align="center">
A professional production-ready REST API template built with Python and FastAPI.
</p>

<p align="center">

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-production-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue.svg)
![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)

</p>

<p align="center">

![CI](https://github.com/Lupusroyal/stark-python-template/actions/workflows/ci.yml/badge.svg)
![CodeQL](https://github.com/Lupusroyal/stark-python-template/actions/workflows/codeql.yml/badge.svg)

</p>

---

## Overview

Stark Python Template is a professional backend template for building modern REST APIs using Python and FastAPI.

The project provides a complete foundation with:

- Clean layered architecture;
- Authentication and authorization;
- Role-Based Access Control (RBAC);
- Permission management;
- Administrative auditing;
- Automated testing;
- Security middleware;
- Docker infrastructure;
- Continuous Integration.

The goal is to provide a reusable and production-ready starting point for backend applications.

---

# Features

## API Core

- FastAPI framework
- OpenAPI / Swagger documentation
- Layered architecture
- Dependency injection
- Environment-based configuration
- Global exception handling

## Database

- PostgreSQL 17
- SQLAlchemy ORM
- Alembic migrations
- Structured database models

## Authentication

- JWT authentication
- Bearer token authorization
- Access tokens
- Refresh tokens
- Refresh token rotation
- Token revocation
- Secure password hashing

## Authorization (RBAC)

Role-Based Access Control system:

- Users
- Roles
- Permissions
- Protected administrative routes
- Granular permission management

Example:

```text
ADMIN

├── users.read
├── users.update
├── permissions.create
└── audit.read
```

## Audit System

Administrative actions are recorded.

Examples:

- Permission creation
- Permission updates
- Permission deletion
- Role changes
- User activation/deactivation
- Administrative operations

Each audit record contains:

- Responsible user
- Executed action
- Target resource
- Details
- Timestamp

---

# Security

The application includes multiple security layers.

## Security Headers

Implemented headers:

- X-Content-Type-Options
- X-Frame-Options
- Referrer-Policy
- Permissions-Policy
- Content-Security-Policy
- Cross-Origin-Opener-Policy
- Cross-Origin-Resource-Policy

## Request Tracking

Every request receives:

X-Request-ID


Processing time is also exposed:

X-Process-Time


for request monitoring.

## Trusted Hosts

Allowed hosts can be configured for production environments.

---

# Stack

- Python 3.12+
- FastAPI
- Pydantic Settings
- SQLAlchemy
- PostgreSQL
- Alembic
- Docker
- Docker Compose
- UV
- Pytest
- Ruff
- MyPy

---

# Project Structure

```text
.
├── src/
│ └── stark/
│ ├── api/
│ │ └── routes/
│ ├── core/
│ ├── dependencies/
│ ├── middleware/
│ ├── models/
│ ├── repositories/
│ ├── schemas/
│ └── services/
│
├── tests/
├── alembic/
├── docs/
├── scripts/
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
└── README.md
```

---

# Configuration

Copy the environment example:

```bash
cp .env.example .env
```

Configure required variables:

```env
APP_NAME=Stark API
APP_VERSION=0.1.0
APP_ENV=development

DEBUG=false

DATABASE_URL=postgresql+psycopg://postgres:postgres@postgres:5432/stark_db

SECRET_KEY=your_secret_key

ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

API_PORT=8000
POSTGRES_PORT=5432
```

Never use the default secret key in production.

Ports can be changed to run multiple project instances.

Example:

Main project:

API_PORT=8000
POSTGRES_PORT=5432

Second clone:

API_PORT=8001
POSTGRES_PORT=5433

---

Install dependencies:

```bash
uv sync
```

Running the Application

The project uses Docker Compose as the main runtime environment.

Start services:

make run

or:

docker compose up -d

Services started:

FastAPI API
PostgreSQL database

Check containers:

docker compose ps
API Documentation

Application URL:

```text
http://localhost:8000
```

Swagger:

http://localhost:8000/docs

ReDoc:

http://localhost:8000/redoc

Health check:

curl http://localhost:8000/health

Expected response:

{
  "status": "healthy"
}
Database

Database migrations are managed using Alembic.

Run migrations:

alembic upgrade head

or:

make migrate

Create a migration:

alembic revision --autogenerate -m "description"
Testing

Run all tests:

make test

or:

uv run pytest

Current test coverage includes:

Authentication
Users
Permissions
RBAC
Audit system
Error handling
Security features
Code Quality
Ruff

Lint:

make lint

Format:

make format
MyPy

Type checking:

uv run mypy .
Development Commands

Install dependencies:

make install

Run application:

make run

Run tests:

make test

Lint:

make lint

Format:

make format

Clean:

make clean
CI/CD and Security Automation

The project uses GitHub automation:

GitHub Actions

Continuous Integration validates:

Ruff
MyPy
Pytest
CodeQL

Static security analysis is enabled through GitHub CodeQL.

Dependabot

Dependency updates are automatically monitored.

Updates are grouped into:

Python dependencies
GitHub Actions dependencies
Production Checklist

Before deploying:

Change SECRET_KEY
Configure environment variables
Use managed PostgreSQL
Set:
APP_ENV=production

Configure:

ALLOWED_HOSTS
CORS_ORIGINS

Review:

Logs
Monitoring
Database backups
Security settings
Contributing

Contributions are welcome.

Before submitting a Pull Request:

Run:

uv run pytest

uv run ruff check .

uv run mypy .

Please ensure:

Tests are added when necessary.
No sensitive information is committed.
CI checks pass.

# License

MIT License

Depois de colar:

```bash
git add README.md
git commit -m "docs: improve project documentation"
git push origin main
