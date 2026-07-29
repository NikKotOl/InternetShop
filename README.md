# InternetShop — Backend Project Portfolio

## Overview
Full-featured e-commerce backend built with modern Python stack. Demonstrates production-grade architecture, async patterns, and software engineering practices.

## Tech Stack
- **Framework:** FastAPI
- **Database:** PostgreSQL with SQLAlchemy 2.0 (async)
- **Migrations:** Alembic
- **Validation:** Pydantic v2
- **Logging:** Loguru
- **Containerization:** Docker Compose
- **Package Manager:** uv
- **Testing:** pytest + pytest-asyncio

## Architecture

### Core Patterns
- **Repository Pattern** — Data access abstraction layer
- **Service Layer** — Business logic and orchestration
- **Dependency Injection** — Explicit FastAPI dependencies
- **Custom Exceptions** — Typed error hierarchy with global handlers
- **Architectural Decision Records (ADR)** — Design rationale documented for every major choice

### Project Structure
```
app/
├── core/               # Shared infrastructure
│   ├── exceptions.py   # Custom exception hierarchy
│   ├── dependencies.py # FastAPI DI factories
│   └── config.py       # Configuration
├── models/             # SQLAlchemy ORM models
├── repositories/       # Data access layer
├── services/           # Business logic
└── routers/            # API endpoints

tests/                  # Unit and integration tests
migrations/              # Alembic schema versions
```

## Key Features

### Implemented Modules

#### Category Module
- Full CRUD operations
- Repository layer for data access
- Service layer for business logic
- REST API with validation
- Comprehensive error handling

#### Product Module
- Products with category relationships
- Dual-repository service pattern
- Filtering by category (`GET /categories/{id}/products`)
- Exception hierarchy (`CategoryNotFoundError`, `ProductNotFoundError`)
- Global exception handler with custom response format

### Design Highlights
- **Async/await throughout** — Non-blocking I/O for scalability
- **Type safety** — Full type hints, Pydantic validation
- **Error handling** — Typed exceptions, meaningful HTTP responses
- **Testing-ready** — Repository mocking, dependency injection

## Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL
- Docker & Docker Compose

### Installation
```bash
# Clone and install
git clone <repo>
cd InternetShop
uv sync

# Start PostgreSQL
docker-compose up -d

# Run migrations
alembic upgrade head

# Start server
uv run uvicorn app.main:application --reload
```

### Running Tests
```bash
uv run pytest
```

## API Documentation
Swagger UI available at `http://localhost:8000/docs`

## What This Project Demonstrates
- Clean architecture separation (Repository → Service → Router)
- Async SQLAlchemy patterns and best practices
- Custom exception handling and global error strategies
- Dependency injection for testability
- Architectural decision documentation
- Test-driven development mindset