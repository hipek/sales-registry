# Application Plan: 3D Sales Registry (Ewidencja3D)

## 1. Application Purpose

Web application for maintaining simplified sales records for unregistered business activity (działalność nierejestrowana) in the context of 3D printing sales.

**Core Features:**
- Adding sales transactions
- Automatic quarterly limit tracking (10,813.50 PLN in 2026)
- Generating receipts (invoices) as PDF
- Transaction history view
- Export data to CSV/Excel

## 2. Architecture - Design Principles

### 2.1. Orthogonality (Separation of Concerns)

The directory and module structure must be **orthogonal** – each module is responsible for one specific application layer and can be replaced/adapted independently.

```
app/                          # Next.js App Router — pages + API
├── (routes)/                 # Page routes (layout groups)
│   ├── page.tsx              # Dashboard (home)
│   ├── layout.tsx            # Root layout
│   ├── transactions/
│   │   ├── page.tsx          # List all transactions
│   │   ├── new/page.tsx      # Add transaction form
│   │   └── [id]/
│   │       ├── page.tsx      # View single transaction
│   │       └── edit/page.tsx # Edit transaction form
│   └── invoices/
│       └── [id]/page.tsx     # View/download invoice
├── api/                      # API Layer
│   ├── transactions/
│   │   ├── route.ts          # GET (list), POST (create)
│   │   └── [id]/route.ts     # GET, PUT, DELETE
│   ├── invoices/
│   │   └── [id]/route.ts     # GET (generate PDF)
│   └── limits/
│       └── current/route.ts  # GET (current quarter)
├── components/               # UI Components (presentational)
│   ├── transactions/
│   │   ├── transaction-list.tsx
│   │   ├── transaction-form.tsx
│   │   └── transaction-row.tsx
│   ├── dashboard/
│   │   ├── limit-gauge.tsx
│   │   ├── recent-transactions.tsx
│   │   └── quick-add.tsx
│   └── invoices/
│       ├── receipt-preview.tsx
│       └── receipt-actions.tsx
├── lib/                      # Business Logic (framework-agnostic)
│   ├── transactions/
│   │   ├── service.ts        # Transaction CRUD operations
│   │   └── validation.ts     # Transaction-specific validation
│   ├── limits/
│   │   └── service.ts        # Limit calculation logic
│   ├── invoices/
│   │   └── service.ts        # PDF generation logic
│   └── db/
│       ├── index.ts          # Database connection & client
│       ├── schema.ts         # Drizzle schema definitions
│       └── migrate.ts        # Migration runner
├── models/                   # Data models (type/class definitions)
│   ├── transaction.ts
│   ├── limit.ts
│   └── invoice.ts
├── types/
│   └── index.ts              # Shared TypeScript types
└── utils/
    ├── date.ts               # Date formatting (Polish locale)
    ├── validation.ts         # Generic Zod schemas
    ├── pdf.ts                # PDF rendering helpers
    ├── csv.ts                # CSV generation helpers
    └── config.ts             # Environment config reader
```

### 2.2. Future-Proof Modularity

- **Database**: Currently SQLite (`database.sqlite`). The `lib/db` layer abstracts database access so that switching to PostgreSQL only requires changes in Drizzle schema dialect and connection config.
- **Framework**: Next.js App Router. UI split into "smart" (page containers) and "dumb" (presentational `components/`) — pages import components, components never import pages.
- **Validation**: Zod schemas defined in `lib/*/validation.ts`, reused by both client forms and API routes.

## 3. Technology Stack

| Component | Technology | Notes |
|-----------|------------|-------|
| Framework | Next.js 14+ (App Router) | With SSR and API Routes |
| Language | TypeScript | Strict mode, `strict: true` in tsconfig |
| ORM/Database | Drizzle ORM + SQLite (better-sqlite3) | Easy migration to PostgreSQL via drizzle-orm/pg |
| UI | Tailwind CSS + shadcn/ui | Component library (button, card, dialog, table, form) |
| PDF | @react-pdf/renderer | Receipt generation from React components |
| Validation | Zod | Shared schemas for client + server |
| Testing | Vitest + @testing-library/react | Unit + component tests (optional MVP phase) |
| Deployment | Docker + Makefile | `make start` / `make stop` |

### 3.1. Key Dependencies (package.json)

```jsonc
{
  "dependencies": {
    "next": "^14.2",
    "react": "^18",
    "react-dom": "^18",
    "drizzle-orm": "^0.36",
    "better-sqlite3": "^11",
    "@react-pdf/renderer": "^4",
    "zod": "^3.23",
    "uuid": "^10",
    "date-fns": "^4",
    "date-fns/locale/pl": "^4"
  },
  "devDependencies": {
    "typescript": "^5",
    "@types/better-sqlite3": "^7",
    "@types/uuid": "^10",
    "drizzle-kit": "^0.28",
    "tailwindcss": "^3.4",
    "postcss": "^8",
    "autoprefixer": "^10",
    "@tailwindcss/forms": "^0.5",
    "vitest": "^2",
    "@testing-library/react": "^16",
    "eslint": "^8",
    "eslint-config-next": "^14"
  }
}
```

## 4. Data Models

### 4.1. Transaction

```typescript
interface Transaction {
  id: string;            // UUID v4
  date: string;          // ISO date (YYYY-MM-DD)
  description: string;   // Item description (e.g. "3D Print - phone holder, PLA")
  amount: number;        // Gross amount in PLN (max 2 decimal places)
  invoiceNumber: string | null;  // Auto-generated receipt number (e.g. "R/2026/001")
  notes: string | null;  // Optional internal note
  createdAt: string;     // ISO datetime
  updatedAt: string;     // ISO datetime
}
```

### 4.2. Limit (calculated, not stored)

```typescript
interface QuarterlyLimit {
  year: number;           // e.g. 2026
  quarter: number;        // 1-4
  limit: number;          // Max gross amount for quarter (e.g. 10813.50)
  used: number;           // Sum of transaction amounts in this quarter
  remaining: number;      // limit - used
  isExceeded: boolean;    // used > limit
}
```

No stored model — computed from transactions at query time. Limit value read from config.

### 4.3. Invoice / Receipt (generated, not stored)

```typescript
interface ReceiptData {
  invoiceNumber: string;         // "R/2026/001"
  issueDate: string;             // ISO date
  seller: {
    name: string;
    address: string;
    nip?: string;                // Optional tax ID
  };
  buyer: {
    name: string;                // "Nabywca" (simplified receipt — no buyer details required)
  };
  items: Array<{
    description: string;
    quantity: number;            // Always 1 for MVP
    unit: string;                // "szt."
    unitPrice: number;           // amount (gross)
    total: number;               // amount (gross)
  }>;
  total: number;                 // Gross total
}
```

Receipts are generated on-demand as PDF and never stored in DB. Re-generation uses same deterministic invoice number.

## 5. Environment Configuration

All config loaded via `utils/config.ts` which reads `process.env` at runtime.

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | `file:./data/database.sqlite` | SQLite path (production: `/app/data/database.sqlite`) |
| `NEXT_PUBLIC_APP_URL` | No | `http://localhost:3000` | Public-facing app URL |
| `SELLER_NAME` | Yes | — | Seller name for receipts |
| `SELLER_ADDRESS` | Yes | — | Seller street + city for receipts |
| `SELLER_NIP` | No | — | Seller tax ID (optional, some formats require it) |
| `QUARTERLY_LIMIT` | No | `10813.50` | Quarterly revenue limit in PLN (updates yearly) |
| `RECEIPT_PREFIX` | No | `R` | Prefix for auto-generated receipt numbers |

`.env.example` file tracked in git; `.env` gitignored.

## 6. Frontend Routes (Pages)

| Route | Page | Purpose |
|-------|------|---------|
| `/` | Dashboard | Limit gauge, last 10 transactions, quick-add button |
| `/transactions` | Transaction list | Paginated table with filters; add/edit/delete actions |
| `/transactions/new` | New transaction | Form: date, description, amount, notes |
| `/transactions/:id` | Transaction detail | View single transaction, actions: edit, delete, generate receipt |
| `/transactions/:id/edit` | Edit transaction | Pre-filled form |
| `/invoices/:id` | Invoice view | Preview receipt PDF + download button |

Navigation: Top navbar with links to Dashboard, Transactions, and Add Transaction.

## 7. Features (MVP)

### 7.1. Dashboard

- Display current quarterly limit (used / remaining) — colored gauge
- List of last 10 transactions (summary)
- Quick "Add Transaction" floating button
- Warning banner if limit exceeded (red)

### 7.2. Transaction Management

| Operation | Implementation |
|-----------|---------------|
| Create | Form with date (default today), description, amount, optional notes. Validated client + server with Zod. |
| Read | Paginated table (10 per page), sortable by date/amount, filter by date range + description search. |
| Update | Edit form, pre-filled. PUT endpoint. |
| Delete | Confirm dialog → soft delete (set `deletedAt`). Hard delete option in admin view. |
| Receipt | "Generate receipt" button → opens invoice page with PDF preview. |

### 7.3. PDF Receipt Generation

- Triggered from transaction detail or list (single transaction)
- Receipt layout:
  - Header: seller info + receipt number + issue date
  - Line item: description, quantity, unit price, total
  - Footer: total gross amount, seller signature line
- Auto-incrementing receipt number format: `{PREFIX}/{YEAR}/{SEQUENCE}` (e.g. `R/2026/001`)
- Sequence persisted in a small JSON file or a separate `counters` table in SQLite
- Seller data from `.env` config
- Downloaded as PDF via browser download

### 7.4. Data Export

- Export all transactions (or filtered by date range) to CSV
- Button on transaction list page
- Columns: date, description, amount, invoice number, notes
- UTF-8 BOM for Excel compatibility (Polish characters)

## 8. Database Schema (Drizzle ORM)

### 8.1. `drizzle.config.ts`

```typescript
import { defineConfig } from "drizzle-kit";

export default defineConfig({
  dialect: "sqlite",
  schema: "./app/lib/db/schema.ts",
  out: "./drizzle",
  dbCredentials: {
    url: process.env.DATABASE_URL ?? "file:./data/database.sqlite",
  },
});
```

### 8.2. Schema (`app/lib/db/schema.ts`)

```typescript
import { sqliteTable, text, real, integer } from "drizzle-orm/sqlite-core";

export const transactions = sqliteTable("transactions", {
  id: text("id").primaryKey(),
  date: text("date").notNull(),                  // ISO date string
  description: text("description").notNull(),
  amount: real("amount").notNull(),
  invoiceNumber: text("invoice_number"),
  notes: text("notes"),
  deletedAt: text("deleted_at"),                  // Soft delete
  createdAt: text("created_at").notNull(),
  updatedAt: text("updated_at").notNull(),
});

// Simple counter table for receipt numbering
export const counters = sqliteTable("counters", {
  id: text("id").primaryKey(),                   // e.g. "receipt-2026"
  value: integer("value").notNull().default(0),
});
```

### 8.3. Migrations

- `npm run db:generate` — `drizzle-kit generate`
- `npm run db:push` — `drizzle-kit push` (dev only, auto-apply)
- `npm run db:migrate` — programmatic migration via `drizzle-orm` migrator
- Migrations run automatically on `next start` in production (`lib/db/migrate.ts`)

## 9. API Structure (Endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/transactions` | List transactions (query: `page`, `limit`, `from`, `to`, `search`) |
| POST | `/api/transactions` | Create transaction (body: date, description, amount, notes) |
| GET | `/api/transactions/:id` | Get single transaction |
| PUT | `/api/transactions/:id` | Update transaction |
| DELETE | `/api/transactions/:id` | Soft-delete transaction |
| GET | `/api/limits/current` | Current quarter limit info (used, remaining, isExceeded) |
| GET | `/api/invoices/:id` | Generate & return PDF receipt for transaction `:id` |

All endpoints return JSON (except `/api/invoices/:id` which returns `application/pdf`).

All mutation endpoints validate request body with Zod. On validation error, return `400 { error: { code: "VALIDATION_ERROR", details: [...] } }`.

## 10. Next.js Configuration

### 10.1. `next.config.js`

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",  // Required for Docker multi-stage build
  experimental: {
    serverComponentsExternalPackages: ["better-sqlite3"],
  },
};

module.exports = nextConfig;
```

### 10.2. `tsconfig.json` — strict mode

```jsonc
{
  "compilerOptions": {
    "strict": true,
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "module": "esnext",
    "moduleResolution": "bundler",
    "jsx": "preserve",
    "paths": {
      "@/*": ["./app/*"]
    }
  }
}
```

## 11. Deployment (Docker)

### 11.1. `docker-compose.yml` (Compose v2)

```yaml
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=file:/app/data/database.sqlite
      - SELLER_NAME=${SELLER_NAME}
      - SELLER_ADDRESS=${SELLER_ADDRESS}
      - SELLER_NIP=${SELLER_NIP}
      - QUARTERLY_LIMIT=${QUARTERLY_LIMIT:-10813.50}
      - RECEIPT_PREFIX=${RECEIPT_PREFIX:-R}
    env_file:
      - .env
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

### 11.2. `Dockerfile`

```dockerfile
FROM node:20-alpine AS base

# Dependencies
FROM base AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

# Builder
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Runner
FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/drizzle ./drizzle     # Migration files
EXPOSE 3000
CMD ["node", "server.js"]
```

Note: Production startup also runs DB migrations. The `server.js` entrypoint from `next start --standalone` is extended via a small wrapper or `postinstall` script to call `lib/db/migrate.ts` before starting.

### 11.3. `Makefile`

```makefile
.PHONY: start stop build logs clean

start:
	docker compose up -d
	@echo "✅ Application started at http://localhost:3000"

stop:
	docker compose down
	@echo "✅ Application stopped"

build:
	docker compose build
	@echo "✅ Image built"

logs:
	docker compose logs -f

clean:
	docker compose down -v
	rm -rf ./data
	@echo "✅ Data and containers removed"

restart: stop start

dev:
	npm run dev
	@echo "✅ Dev server at http://localhost:3000"
```

### 11.4. Project Root Structure

```
.
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── .env.example          # Tracked in git
├── .env                  # Gitignored
├── .gitignore
├── next.config.js
├── tsconfig.json
├── tailwind.config.ts
├── postcss.config.js
├── drizzle.config.ts
├── package.json
├── data/                 # SQLite DB volume (gitignored)
├── drizzle/              # Migration files (generated)
└── app/                  # Next.js application directory
    ├── layout.tsx
    ├── page.tsx
    ├── globals.css
    └── ...
```

## 12. Testing Strategy (MVP)

- **Unit tests**: Vitest for `lib/` business logic (limit calculation, validation, date utils)
- **Component tests**: @testing-library/react for form components
- **API tests**: Vitest with API route integration tests (SQLite in-memory)
- **Target**: Not blocking MVP, but test setup included from day 1 to avoid retrofitting

## 13. Implementation Order

| Phase | What | Depends On |
|-------|------|------------|
| 1 | Scaffold: Next.js + Tailwind + Drizzle + shadcn/ui setup, `.env.example`, config files | — |
| 2 | Database: schema, migrations, seed script | Phase 1 |
| 3 | API: transactions CRUD + limit endpoint | Phase 2 |
| 4 | UI: transaction list + form pages | Phase 3 |
| 5 | Dashboard: limit gauge, recent transactions | Phase 4 |
| 6 | PDF: receipt generation, invoice page | Phase 3 |
| 7 | CSV export | Phase 4 |
| 8 | Docker: compose, Dockerfile, Makefile | Phase 1 |
