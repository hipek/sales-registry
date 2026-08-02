# Sales Registry — Agent Guide

## Project

Web app for 3D printing sales records. Polish tax-free quarterly limit: 10,813.50 PLN (2026).

## Layout

```
backend/    # FastAPI app, alembic, tests
frontend/   # Next.js app, components, lib
e2e/        # Playwright e2e tests
data/       # Local data files
```

## Commands

```bash
# Dev
make dev-backend    # FastAPI on :8000
make dev-frontend   # Next.js on :3000

# Test / checks
make test           # Backend pytest (frontend has no unit tests)
make ci             # pytest + ruff + eslint + tsc + prettier

# E2E
make e2e            # Playwright (auto-cleans DB, starts services)
make e2e-clean      # Reset e2e DB

# Python
uv run pytest
uv run alembic upgrade head
```

## Rules

- `uv` for Python deps, `pnpm` for Node deps
- SQLite dev, PostgreSQL prod
- shadcn/ui components
- Only backend pytest tests; `make test` runs them

## Coolify

- App ID: `yayfxgjotwlkllhdu90x3tqk`
