.PHONY: start stop build logs clean dev dev-backend dev-frontend test test-backend test-frontend init

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

init:
	docker compose run --rm backend uv run alembic upgrade head
	@echo "✅ Database initialized"

restart: stop start

dev-backend:
	cd backend && uv run uvicorn app.main:app --reload --port 8000

dev-frontend:
	cd frontend && pnpm dev

dev:
	@echo "Run in separate terminals:"
	@echo "  make dev-backend"
	@echo "  make dev-frontend"

test: test-backend test-frontend
	@echo "✅ All tests passed"

test-backend:
	docker compose run --rm -v ./backend/tests:/app/tests backend sh -c "uv sync --frozen && uv run pytest"

test-frontend:
	docker compose run --rm --no-deps -v ./frontend:/app -w /app -e CI=true -e NODE_ENV=development frontend sh -c "corepack enable && corepack prepare pnpm@9 --activate && pnpm install --frozen-lockfile && pnpm vitest run"
