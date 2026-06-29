# Application Plan: 3D Sales Registry (Ewidencja3D)

## 1. Application Purpose

Web application for maintaining simplified sales records for unregistered business activity (działalność nierejestrowana) in the context of 3D printing sales.

**Core Features:**
- Adding sales transactions
- Automatic quarterly limit tracking (10,813.50 PLN in 2026)
- Generating receipts (invoices) as PDF
- Transaction history view
- Export data to CSV/Excel

## 2. Architecture

### 2.1. Overview

Two-tier architecture:
- **Frontend**: Next.js 14+ (App Router) — SSR pages, UI components, API client
- **Backend**: Python FastAPI — business logic, database access, PDF generation, CSV export

Frontend calls backend via REST API. Next.js rewrites `/api/*` requests to FastAPI in `next.config.js` (both dev and prod).

### 2.2. Directory Structure

```
.
├── Dockerfile.frontend
├── Dockerfile.backend
├── docker-compose.yml
├── Makefile
├── .env.example
├── .env                          # Gitignored
├── .gitignore
├── frontend/                     # Next.js application (pnpm)
│   ├── next.config.js
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── postcss.config.js
│   ├── package.json
│   ├── drizzle.config.ts         # Drizzle ORM — used only for TypeScript type gen from DB
│   ├── app/
│   │   ├── layout.tsx            # Root layout
│   │   ├── page.tsx              # Dashboard
│   │   ├── globals.css
│   │   ├── transactions/
│   │   │   ├── page.tsx          # List (server component, fetches from backend)
│   │   │   ├── new/page.tsx      # Create form (client component)
│   │   │   └── [id]/
│   │   │       ├── page.tsx      # Detail view (server component)
│   │   │       └── edit/page.tsx # Edit form (client component)
│   │   └── invoices/
│   │       └── [id]/page.tsx     # Invoice preview + download (client component)
│   ├── components/               # Presentational UI components
│   │   ├── ui/                   # shadcn/ui primitives
│   │   ├── transactions/
│   │   ├── dashboard/
│   │   └── invoices/
│   └── lib/                      # Frontend utilities (no business logic)
│       ├── api-client.ts         # Fetch wrapper for FastAPI backend
│       ├── date.ts               # Date formatting (Polish locale)
│       ├── validation.ts         # Zod schemas (client-side validation only)
│       ├── csv.ts                # CSV generation (can be frontend-only)
│       └── config.ts             # Public env var reader (NEXT_PUBLIC_*)
├── backend/                      # Python FastAPI application (uv)
│   ├── pyproject.toml
│   ├── alembic.ini
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py               # FastAPI app, lifespan, CORS
│   │   ├── config.py             # Settings via pydantic-settings (.env)
│   │   ├── database.py           # SQLAlchemy engine + session
│   │   ├── models/               # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   ├── transaction.py
│   │   │   └── counter.py
│   │   ├── schemas/              # Pydantic request/response schemas
│   │   │   ├── __init__.py
│   │   │   ├── transaction.py
│   │   │   ├── limit.py
│   │   │   └── invoice.py
│   │   ├── routers/              # FastAPI route handlers
│   │   │   ├── __init__.py
│   │   │   ├── transactions.py
│   │   │   ├── limits.py
│   │   │   └── invoices.py
│   │   ├── services/             # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── transaction.py
│   │   │   ├── limit.py
│   │   │   └── invoice.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── date.py
│   │       └── pdf.py            # ReportLab receipt generator
│   └── alembic/                  # DB migrations
│       └── versions/
└── data/                         # SQLite DB volume (gitignored)
```

### 2.3. Orthogonality Principles

- **Frontend knows nothing about backend internals** — communicates only through REST API contracts (Pydantic schemas mirrored as TypeScript types)
- **Business logic lives only in `backend/app/services/`** — framework-agnostic, testable without FastAPI
- **Database access only through `backend/app/models/`** — switching from SQLite to PostgreSQL means changing SQLAlchemy connection string + Alembic dialect
- **UI components in `frontend/components/` are pure** — no API calls, no business logic, receive data via props
- **Page components are thin** — fetch data or parse params, delegate rendering to components

## 3. Technology Stack

### 3.1. Frontend (Next.js)

| Component | Technology | Notes |
|-----------|------------|-------|
| Framework | Next.js 14+ (App Router) | SSR pages, no API routes |
| Language | TypeScript | Strict mode |
| Package manager | pnpm | |
| UI | Tailwind CSS v3 + shadcn/ui | Style: Default, Base color: Zinc, CSS variables: yes |
| Validation (client) | Zod | Shared with TypeScript types |
| Testing | Vitest + @testing-library/react | |
| State | React Server Components + fetch | No client-state library for MVP |

### 3.2. Backend (Python)

| Component | Technology | Notes |
|-----------|------------|-------|
| Runtime | Python 3.12+ | |
| Framework | FastAPI | With uvicorn ASGI server |
| Package manager | uv | `uv add`, `uv sync`, `uv run` |
| ORM | SQLAlchemy 2.0+ | Async or sync (SQLite: sync for simplicity) |
| Migrations | Alembic | Auto-generation from model changes |
| Validation | Pydantic v2 | Request/response schemas |
| PDF generation | ReportLab | Receipt PDF |
| CSV export | Python csv (stdlib) | |
| Testing | pytest + httpx (async test client) | |
| Config | pydantic-settings | Reads from `.env` |

### 3.3. Communication

- FastAPI serves on `http://backend:8000` (Docker) or `http://localhost:8000` (dev)
- Next.js rewrites `/api/*` → `http://backend:8000/api/*` via `next.config.js` rewrites
- In development, Next.js proxies to localhost:8000
- In production Docker, proxies to backend service name

## 4. Data Models

### 4.1. Transaction (SQLAlchemy model)

```python
# backend/app/models/transaction.py
from sqlalchemy import Column, String, Float, DateTime
import uuid
from datetime import datetime

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    date = Column(String, nullable=False)              # ISO date "YYYY-MM-DD"
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)             # Gross PLN, max 2 decimals
    invoice_number = Column(String, nullable=True)     # e.g. "R/2026/001"
    notes = Column(String, nullable=True)
    deleted_at = Column(DateTime, nullable=True)       # Soft delete
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### 4.2. Counter (SQLAlchemy model)

```python
# backend/app/models/counter.py
from sqlalchemy import Column, String, Integer

class Counter(Base):
    __tablename__ = "counters"

    id = Column(String, primary_key=True)   # e.g. "receipt-2026"
    value = Column(Integer, nullable=False, default=0)
```

### 4.3. Pydantic Schemas

```python
# backend/app/schemas/transaction.py
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional

class TransactionCreate(BaseModel):
    date: date
    description: str = Field(min_length=1, max_length=500)
    amount: float = Field(gt=0, le=1000000)
    notes: Optional[str] = None

class TransactionUpdate(BaseModel):
    date: Optional[date] = None
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    amount: Optional[float] = Field(None, gt=0, le=1000000)
    notes: Optional[str] = None

class TransactionResponse(BaseModel):
    id: str
    date: str
    description: str
    amount: float
    invoice_number: Optional[str]
    notes: Optional[str]
    created_at: str
    updated_at: str
```

```python
# backend/app/schemas/limit.py
from pydantic import BaseModel

class QuarterlyLimitResponse(BaseModel):
    year: int
    quarter: int
    limit: float
    used: float
    remaining: float
    is_exceeded: bool
```

```python
# backend/app/schemas/invoice.py
from pydantic import BaseModel
from typing import List, Optional

class SellerInfo(BaseModel):
    name: str
    address: str
    nip: Optional[str] = None

class InvoiceItem(BaseModel):
    description: str
    quantity: int = 1
    unit: str = "szt."
    unit_price: float
    total: float

class InvoiceResponse(BaseModel):
    invoice_number: str
    issue_date: str
    seller: SellerInfo
    items: List[InvoiceItem]
    total: float
```

### 4.4. API Response Envelope

```python
# backend/app/schemas/common.py
from pydantic import BaseModel
from typing import Generic, TypeVar, List, Optional

T = TypeVar("T")

class PaginatedResponse(BaseModel):
    data: List[T]
    meta: dict  # {"page": 1, "limit": 10, "total": 42, "total_pages": 5}

class ErrorResponse(BaseModel):
    error: dict  # {"code": "VALIDATION_ERROR", "message": "...", "details": [...]}
```

All endpoints return:
- 200: `PaginatedResponse` (lists) or direct object (single resource)
- 400: `ErrorResponse` with `VALIDATION_ERROR` code
- 404: `ErrorResponse` with `NOT_FOUND` code
- 500: `ErrorResponse` with `INTERNAL_ERROR` code

## 5. Environment Configuration

### 5.1. `.env.example`

```
# Database
DATABASE_URL=sqlite:///./data/database.sqlite

# Seller info (receipts)
SELLER_NAME=
SELLER_ADDRESS=
SELLER_NIP=

# App config
QUARTERLY_LIMIT=10813.50
RECEIPT_PREFIX=R
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Backend config (uvicorn)
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
```

| Variable | Required | Default | Used by | Description |
|----------|----------|---------|---------|-------------|
| `DATABASE_URL` | Yes | — | Backend | SQLAlchemy connection string |
| `SELLER_NAME` | Yes | — | Backend | Seller name on receipts |
| `SELLER_ADDRESS` | Yes | — | Backend | Seller street + city on receipts |
| `SELLER_NIP` | No | — | Backend | Seller tax ID |
| `QUARTERLY_LIMIT` | No | `10813.50` | Backend | Quarterly revenue limit |
| `RECEIPT_PREFIX` | No | `R` | Backend | Receipt number prefix |
| `NEXT_PUBLIC_APP_URL` | No | `http://localhost:3000` | Frontend | Public URL |
| `BACKEND_HOST` | No | `0.0.0.0` | Backend | Uvicorn bind address |
| `BACKEND_PORT` | No | `8000` | Backend | Uvicorn port |

### 5.2. Backend Config (`backend/app/config.py`)

Uses `pydantic-settings` to load from `.env`:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    seller_name: str
    seller_address: str
    seller_nip: str | None = None
    quarterly_limit: float = 10813.50
    receipt_prefix: str = "R"

    class Config:
        env_file = "../.env"
```

## 6. Frontend Routes (Pages)

| Route | Page type | Purpose |
|-------|-----------|---------|
| `/` | Server component | Dashboard — fetches limit + recent transactions from backend |
| `/transactions` | Server component | Paginated list — fetches from backend, passes to client table component |
| `/transactions/new` | Client component | Form — POST to backend on submit |
| `/transactions/:id` | Server component | Detail view — fetches single transaction |
| `/transactions/:id/edit` | Client component | Pre-filled form — PUT to backend on submit |
| `/invoices/:id` | Client component | Fetches invoice data from backend, renders receipt preview via React + download button. PDF download hits `/api/invoices/:id/download` directly. |

**Component boundary rule**:
- Pages that only **display** data (dashboard, list, detail) = Server Components. Data fetching done directly with `fetch()`.
- Pages that have **forms/interactivity** (new, edit, invoice preview) = Client Components marked with `"use client"`.
- Presentational components in `components/` are **never** pages — they accept props, no data fetching.

## 7. API Endpoints (FastAPI)

| Method | Endpoint | Request | Response | Description |
|--------|----------|---------|----------|-------------|
| GET | `/api/transactions` | Query: `page`, `limit`, `from`, `to`, `search` | `PaginatedResponse[TransactionResponse]` | List with pagination + filters |
| POST | `/api/transactions` | Body: `TransactionCreate` | `TransactionResponse` (201) | Create transaction |
| GET | `/api/transactions/{id}` | — | `TransactionResponse` | Get single transaction |
| PUT | `/api/transactions/{id}` | Body: `TransactionUpdate` | `TransactionResponse` | Update transaction |
| DELETE | `/api/transactions/{id}` | — | `204 No Content` | Soft delete |
| GET | `/api/limits/current` | — | `QuarterlyLimitResponse` | Current quarter limit info |
| GET | `/api/invoices/{id}` | — | `InvoiceResponse` (JSON) | Invoice data (for preview) |
| GET | `/api/invoices/{id}/download` | — | `application/pdf` | Download PDF receipt |

All mutation endpoints validated with Pydantic. Soft delete sets `deleted_at` timestamp. List queries exclude soft-deleted records by default.

## 8. Features (MVP)

### 8.1. Dashboard

- Limit gauge: colored bar showing used / remaining for current quarter
- Last 10 transactions summary list
- Quick "Add Transaction" floating button → navigates to `/transactions/new`
- Red warning banner when limit exceeded

### 8.2. Transaction Management

| Operation | Implementation |
|-----------|---------------|
| Create | Form with date (default today), description, amount, optional notes. Client validation with Zod, server validation with Pydantic. |
| Read | Server-component table, 10 per page, sortable by date/amount, filter by date range + description search |
| Update | Edit form, pre-filled. `PUT /api/transactions/{id}` |
| Delete | Confirm dialog → `DELETE /api/transactions/{id}` (soft delete). Hard delete not exposed in MVP UI. |
| Receipt | Button on detail page → navigates to `/invoices/{id}` |

### 8.3. PDF Receipt Generation

- Backend generates PDF via ReportLab
- Receipt layout:
  - Header: SELLER_NAME, SELLER_ADDRESS, NIP (if set), receipt number, issue date
  - Item row: description, quantity "szt.", unit price, total
  - Footer: total gross amount, "Sprzedaż nierejestrowana — paragon bez NIP nabywcy"
- Receipt number: `{PREFIX}/{YEAR}/{SEQUENCE}` (e.g. `R/2026/001`)
- Sequence stored in `counters` table, keyed by year (`receipt-2026`, `receipt-2027`, ...). New year resets to 1.
- PDF download via `/api/invoices/{id}/download`
- Frontend preview via `/invoices/{id}` — fetches `InvoiceResponse` JSON, renders with React components (no PDF viewer, just styled HTML preview)

### 8.4. Data Export

- Button on transaction list page
- Triggers CSV download generated by backend at `/api/transactions/export?from=&to=`
- Backend endpoint returns `text/csv` with UTF-8 BOM for Excel compatibility
- Columns: date, description, amount, invoice number, notes

## 9. Database (SQLAlchemy + Alembic)

### 9.1. Migrations

```bash
cd backend
uv run alembic init alembic          # One-time setup
uv run alembic revision --autogenerate -m "add transactions table"
uv run alembic upgrade head
```

### 9.2. alembic.ini

```
sqlalchemy.url = sqlite:///./data/database.sqlite
```

### 9.3. Database session

```python
# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}  # SQLite-specific
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
```

## 10. Component Boundary Rules (Next.js)

| File type | `"use client"`? | Logic |
|-----------|----------------|-------|
| `app/page.tsx` (dashboard) | No | Server component, fetches data |
| `app/transactions/page.tsx` | No | Server component, fetches paginated data |
| `app/transactions/new/page.tsx` | Yes | Form with client state |
| `app/transactions/[id]/page.tsx` | No | Server component, fetches single item |
| `app/transactions/[id]/edit/page.tsx` | Yes | Form with client state |
| `app/invoices/[id]/page.tsx` | Yes | Fetches JSON, renders preview |
| `components/**/*.tsx` | Only if interactive | Pure presentational |
| `lib/api-client.ts` | No | Shared fetch utility |

## 11. Frontend Configuration

### 11.1. `next.config.js`

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  rewrites: async () => [
    {
      source: "/api/:path*",
      destination: `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/:path*`,
    },
  ],
};

module.exports = nextConfig;
```

### 11.2. Tailwind + shadcn/ui

- shadcn/ui style: **Default**
- Base color: **Zinc**
- CSS variables: **yes**
- Components for MVP: `button`, `card`, `dialog`, `table`, `form`, `input`, `label`, `select`, `badge`, `toast`

## 12. Deployment (Docker)

### 12.1. `docker-compose.yml`

```yaml
services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    env_file:
      - .env
    environment:
      - DATABASE_URL=sqlite:///app/data/database.sqlite
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_API_URL=http://backend:8000
      - NEXT_PUBLIC_APP_URL=http://localhost:3000
    depends_on:
      - backend
    restart: unless-stopped
```

### 12.2. `Dockerfile.backend`

```dockerfile
FROM python:3.12-slim AS base

RUN pip install uv

WORKDIR /app
COPY backend/pyproject.toml backend/uv.lock* ./
RUN uv sync --frozen --no-dev

COPY backend/ .

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 12.3. `Dockerfile.frontend`

```dockerfile
FROM node:20-alpine AS base

# pnpm setup
RUN corepack enable && corepack prepare pnpm@latest --activate

FROM base AS deps
WORKDIR /app
COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY frontend/ .
RUN pnpm build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
EXPOSE 3000
CMD ["node", "server.js"]
```

### 12.4. `Makefile`

```makefile
.PHONY: start stop build logs clean dev dev-backend dev-frontend

start:
	docker compose up -d
	@echo "✅ App at http://localhost:3000"

stop:
	docker compose down
	@echo "✅ Stopped"

build:
	docker compose build
	@echo "✅ Images built"

logs:
	docker compose logs -f

clean:
	docker compose down -v
	rm -rf ./data
	@echo "✅ Cleaned"

restart: stop start

dev-backend:
	cd backend && uv run uvicorn app.main:app --reload --port 8000

dev-frontend:
	cd frontend && pnpm dev

dev:
	@echo "Run in separate terminals:"
	@echo "  make dev-backend"
	@echo "  make dev-frontend"
```

### 12.5. Project Root

```
.
├── Dockerfile.frontend
├── Dockerfile.backend
├── docker-compose.yml
├── Makefile
├── .env.example
├── .env
├── .gitignore
├── frontend/
│   ├── next.config.js
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── postcss.config.js
│   ├── package.json
│   ├── drizzle.config.ts
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── globals.css
│   │   ├── transactions/
│   │   └── invoices/
│   ├── components/
│   │   └── ui/
│   └── lib/
│       ├── api-client.ts
│       ├── date.ts
│       ├── validation.ts
│       └── config.ts
├── backend/
│   ├── pyproject.toml
│   ├── alembic.ini
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routers/
│   │   ├── services/
│   │   └── utils/
│   └── alembic/
│       └── versions/
└── data/
```

## 13. Testing Strategy (MVP)

### 13.1. Backend (pytest)

```bash
cd backend
uv run pytest                          # All tests
uv run pytest tests/ -v               # Verbose
```

- Tests in `backend/tests/` mirror `app/` structure
- `test_routers/` — httpx AsyncClient against FastAPI test app
- `test_services/` — pure unit tests for business logic
- In-memory SQLite for test DB

### 13.2. Frontend (Vitest)

```bash
cd frontend
pnpm vitest                            # All tests
```

- `test_utils/` — date formatting, validation schemas
- `test_components/` — @testing-library/react for form components
- No API-calling tests for MVP (covered by backend tests)

## 14. Implementation Phases

| Phase | What | Depends On |
|-------|------|------------|
| **1** | Scaffold: `frontend/` (Next.js + Tailwind + shadcn/ui + pnpm), `backend/` (FastAPI + uv + SQLAlchemy + Alembic), `docker-compose.yml`, `.env.example`, configs | — |
| **2** | Backend DB: models (`Transaction`, `Counter`), database session, initial Alembic migration | Phase 1 |
| **3** | Backend API: transactions CRUD, limit endpoint, invoice data endpoint | Phase 2 |
| **4** | Frontend: API client, transaction list page, new/edit forms, detail page | Phase 1 + 3 |
| **5** | Dashboard: limit gauge component, recent transactions, quick-add | Phase 4 |
| **6** | PDF: ReportLab receipt generator, download endpoint, invoice preview page | Phase 3 |
| **7** | CSV: export endpoint, download button on list page | Phase 3 |
| **8** | Docker: Dockerfiles, production compose, Makefile polish | Phase 1 |

## 15. Key Dependencies

### 15.1. Frontend (`frontend/package.json`)

```jsonc
{
  "dependencies": {
    "next": "^14.2",
    "react": "^18",
    "react-dom": "^18",
    "zod": "^3.23",
    "date-fns": "^4",
    "date-fns/locale/pl": "^4",
    "class-variance-authority": "^0.7",
    "clsx": "^2",
    "tailwind-merge": "^2",
    "lucide-react": "^0.400"
  },
  "devDependencies": {
    "typescript": "^5",
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "tailwindcss": "^3.4",
    "postcss": "^8",
    "autoprefixer": "^10",
    "tailwindcss-animate": "^1",
    "vitest": "^2",
    "@testing-library/react": "^16",
    "eslint": "^8",
    "eslint-config-next": "^14",
    "drizzle-kit": "^0.28",
    "drizzle-orm": "^0.36",
    "@libsql/client": "^0.14"
  }
}
```

### 15.2. Backend (`backend/pyproject.toml`)

```toml
[project]
name = "ewidencja3d-backend"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115",
    "uvicorn[standard]>=0.32",
    "sqlalchemy>=2.0",
    "alembic>=1.14",
    "pydantic>=2.0",
    "pydantic-settings>=2.0",
    "reportlab>=4.2",
]

[project.optional-dependencies]
dev = [
    "pytest>=8",
    "httpx>=0.28",
    "pytest-asyncio>=0.24",
]

[tool.uv]
dev-dependencies = ["dev"]
```
