# Sales Registry — Agent Guide

## Project

Web app for 3D printing sales records. Polish tax-free quarterly limit: 10,813.50 PLN (2026).

## Stack

See [README.md](README.md) for full stack details.

## Layout

```
backend/    # FastAPI app, alembic, tests
e2e/        # Playwright e2e tests
frontend/   # Next.js app, components, lib, tests
data/       # Local data files
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

# E2E
make e2e          # Run Playwright e2e tests
make e2e-clean    # Clean e2e database

# Checks
make ci           # Run lint, typecheck, format checks

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
