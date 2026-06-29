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

app/
├── api/ # API Layer (Next.js App Router)
│ ├── transactions/ # Transaction endpoints
│ ├── invoices/ # Invoice/receipt endpoints
│ └── limits/ # Limit checking endpoints
├── components/ # UI Components (presentational)
│ ├── transactions/ # Transaction components
│ ├── dashboard/ # Dashboard components
│ └── invoices/ # Invoice components
├── lib/ # Business Logic (framework-agnostic)
│ ├── transactions/ # Transaction services
│ ├── limits/ # Limit services
│ ├── invoices/ # PDF generation services
│ └── db/ # Data access layer
├── models/ # Data models (type/class definitions)
│ ├── transaction.ts
│ ├── limit.ts
│ └── invoice.ts
├── types/ # Shared TypeScript types
│ └── index.ts
└── utils/ # Helper functions
├── date.ts
├── validation.ts
└── pdf.ts


### 2.2. Future-Proof Modularity

- **Database**: Currently SQLite (`database.sqlite`). The `lib/db` layer abstracts database access so that switching to PostgreSQL only requires changes in this single location.
- **Framework**: Next.js App Router. UI split into "smart" (container) and "dumb" (presentational) components.
- **Validation**: Data validation on both backend and frontend (Zod or Joi).

## 3. Technology Stack

| Component | Technology | Notes |
|-----------|------------|-------|
| Framework | Next.js 14+ (App Router) | With SSR and API Routes |
| Language | TypeScript | Strict typing |
| ORM/Database | Drizzle ORM + SQLite | Lightweight, easy to migrate to PostgreSQL |
| UI | Tailwind CSS + shadcn/ui | Rapid interface building |
| PDF | @react-pdf/renderer | Receipt generation |
| Validation | Zod | Data validation |
| Deployment | Docker + Makefile | `make start` / `make stop` |

## 4. Data Models

### 4.1. Transaction

```typescript
interface Transaction {
  id: string;           // UUID
  date: Date;           // Sale date
  description: string;  // Description (e.g., "3D Print - phone holder")
  amount: number;       // Gross amount (PLN)
  invoiceNumber?: string; // Receipt number (optional)
  createdAt: Date;
  updatedAt: Date;
}

5. Features (MVP)
5.1. Dashboard
Display current quarterly limit (used / remaining)

List of last 10 transactions

Quick "Add Transaction" button

Warning if limit exceeded

5.2. Transaction Management
Create: Form with date, description, amount

Read: List with pagination (10 per page)

Update: Edit transaction

Delete: Soft or hard delete

Filter: By date, amount, description

5.3. PDF Receipt Generation
Generate receipt for selected transaction

Receipt complies with unregistered business requirements

Seller data loaded from configuration (.env)

5.4. Data Export
Export to CSV (all transactions or selected date range)

Export to Excel (can be added later)

6. API Structure (Endpoints)
Method	Endpoint	Description
GET	/api/transactions	Fetch list of transactions (with pagination)
POST	/api/transactions	Add new transaction
GET	/api/transactions/:id	Fetch single transaction
PUT	/api/transactions/:id	Update transaction
DELETE	/api/transactions/:id	Delete transaction
GET	/api/limits/current	Fetch current quarterly limit
GET	/api/invoices/:id	Generate PDF receipt for transaction


makefile to control the app:

.PHONY: start stop build logs clean

start:
	docker-compose up -d
	@echo "✅ Application started at http://localhost:3000"

stop:
	docker-compose down
	@echo "✅ Application stopped"

build:
	docker-compose build
	@echo "✅ Image built"

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	rm -rf ./data
	@echo "✅ Data and containers removed"

restart: stop start

docker compose:

version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=file:/app/data/database.sqlite
    volumes:
      - ./data:/app/data
    restart: unless-stopped

Dockefile:

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
EXPOSE 3000
CMD ["node", "server.js"]

dockerfile strucutre:

├── Dockerfile
├── docker-compose.yml
├── Makefile
├── .env
└── app/                (Next.js application directory)
