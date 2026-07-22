# Ewidencja3D — 3D Sales Registry

Web app for simplified sales records for unregistered business activity (*działalność nierejestrowana*) in the context of 3D printing sales.

## Features

- Add/edit/delete sales transactions
- Auto quarterly limit tracking (10,813.50 PLN in 2026)
- PDF receipt generation (ReportLab)
- Transaction list with pagination, search, date filters
- CSV export with UTF-8 BOM (Excel-compatible)
- Dashboard with limit gauge + recent transactions

## Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14 (App Router), Tailwind CSS v3, shadcn/ui, TypeScript |
| Backend | Python 3.12+, FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2 |
| PDF | ReportLab |
| Database | SQLite (dev), PostgreSQL-ready (SQLAlchemy) |
| Package mgr | uv (Python), pnpm (Node) |

## Quick Start

### Prerequisites

- Docker + Docker Compose (for production build)
- OR: Python 3.12+, Node 20+, uv, pnpm (for dev)

### Setup

```bash
# 1. Clone & enter project
git clone <url> && cd 3d-sales-registry

# 2. Configure environment
cp .env.example .env
# Edit .env — set at least SELLER_NAME and SELLER_ADDRESS

# 3. Start (choose one)
make start        # Docker production build
make dev          # local dev (run in 2 terminals)
```

## Make Commands

| Command | Description |
|---------|-------------|
| `make start` | Start all services via Docker Compose (detached) |
| `make stop` | Stop all services |
| `make restart` | Stop then start |
| `make build` | Rebuild Docker images |
| `make logs` | Tail logs from all services |
| `make clean` | Remove containers, volumes, and local data |
| `make dev` | Show instructions for local dev (2 terminals) |
| `make dev-backend` | Start FastAPI dev server with hot reload on `:8000` |
| `make dev-frontend` | Start Next.js dev server on `:3000` |

### Typical dev workflow

```bash
# Terminal 1 — backend
make dev-backend

# Terminal 2 — frontend
make dev-frontend

# Open http://localhost:3000
```

## Environment Variables

See `.env.example`. Required:

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | SQLAlchemy connection string |
| `SELLER_NAME` | Seller name printed on receipts |
| `SELLER_ADDRESS` | Seller address printed on receipts |
| `SELLER_NIP` | Seller tax ID (optional) |

Optional:

| Variable | Default | Description |
|----------|---------|-------------|
| `QUARTERLY_LIMIT` | `10813.50` | Quarterly revenue limit (PLN) |
| `RECEIPT_PREFIX` | `R` | Receipt number prefix |
| `RECEIPT_UNIT` | `szt.` | Receipt unit (Polish for "pieces") |
| `NEXT_PUBLIC_APP_URL` | `http://localhost:3000` | Public app URL |
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | Backend API URL (frontend) |
| `CORS_ORIGINS` | `http://localhost:3000,http://host.docker.internal:8000` | Allowed CORS origins |
| `BACKEND_HOST` | `0.0.0.0` | Uvicorn bind address |
| `BACKEND_PORT` | `8000` | Uvicorn port |

## Project Structure

```
.
├── frontend/          # Next.js app
│   ├── app/           # Pages (RSC + client)
│   ├── components/    # UI components (shadcn + custom)
│   └── lib/           # Utilities (api-client, validation, date, format)
├── backend/           # Python FastAPI app
│   ├── app/
│   │   ├── main.py    # App entry + exception handlers
│   │   ├── config.py  # pydantic-settings
│   │   ├── database.py
│   │   ├── models/    # SQLAlchemy ORM
│   │   ├── schemas/   # Pydantic request/response
│   │   ├── routers/   # FastAPI route handlers
│   │   ├── services/  # Business logic
│   │   └── utils/     # PDF, date helpers
│   ├── alembic/       # DB migrations
│   └── tests/         # pytest tests
├── docs/plan.md       # Full application plan
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── Makefile
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/transactions` | List (paginated, filterable) |
| POST | `/api/transactions` | Create transaction |
| GET | `/api/transactions/export` | Export CSV |
| GET | `/api/transactions/{id}` | Get single |
| PUT | `/api/transactions/{id}` | Update |
| DELETE | `/api/transactions/{id}` | Soft delete |
| GET | `/api/limits/current` | Current quarter limit info |
| GET | `/api/invoices/{id}` | Invoice JSON (preview) |
| GET | `/api/invoices/{id}/download` | Invoice PDF download |

## Testing

```bash
# Backend
cd backend && uv run pytest

# Frontend
cd frontend && pnpm vitest
```

## Database Migrations

```bash
cd backend
uv run alembic upgrade head          # Apply pending
uv run alembic revision --autogenerate -m "description"  # New migration
```

## License

MIT
