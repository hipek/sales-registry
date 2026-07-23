# Sales Registry — Agent Guide

## Project

Web app for 3D printing sales records. Polish tax-free quarterly limit: 10,813.50 PLN (2026).

## Stack

| Layer | Tech |
|-------|------|
| Frontend | Next.js 14 App Router, Tailwind v3, shadcn/ui, TypeScript |
| Backend | Python 3.12+, FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2 |
| DB | SQLite (dev), PostgreSQL (prod) |
| Package | uv (Python), pnpm (Node) |

## Layout

```
backend/    # FastAPI app, alembic, tests
frontend/   # Next.js app, components, lib, tests
data/       # Local data files
docs/       # Documentation
```

## Key Paths

- Backend app: `backend/app/`
- Frontend pages: `frontend/app/`
- Frontend components: `frontend/components/`
- Frontend lib: `frontend/lib/`
- Tests: `backend/tests/`, `frontend/tests/`

## Commands

```bash
# Dev
make dev          # Start both backend + frontend
make backend      # Start backend only
make frontend     # Start frontend only

# Build (Docker)
make build        # Build Docker images
make deploy       # Deploy with docker-compose

# Python
uv sync           # Install deps
uv run pytest     # Run tests
uv run alembic upgrade head  # Run migrations

# Node
pnpm install      # Install deps
pnpm run build    # Build Next.js
```

## Coolify

- App ID: `yayfxgjotwlkllhdu90x3tqk`

## Rules

- Use `uv` for Python deps, `pnpm` for Node deps
- Backend uses SQLite by default, PostgreSQL for production
- Frontend uses shadcn/ui components
- Always run `make dev` to test full stack
- Tests: `uv run pytest` (backend), `pnpm test` (frontend)
