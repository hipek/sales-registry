.PHONY: start stop build logs clean dev dev-backend dev-frontend test test-backend test-frontend init

start:
	docker compose up -d backend-dev frontend-dev
	@echo "✅ App at http://localhost:3000"

stop:
	docker compose stop backend-dev frontend-dev
	@echo "✅ Stopped"

build:
	docker compose build
	@echo "✅ Images built"

logs:
	docker compose logs -f

clean:
	docker compose down --rmi all --volumes
	rm -f ./data/*.db ./data/*.sqlite3 ./data/*.sqlite
	@echo "✅ Containers, images, and database removed"

init:
	docker compose run --rm backend-dev uv run alembic upgrade head
	@echo "✅ Database initialized"

restart: stop start
	@echo "✅ Restarted"

dev-backend:
	cd backend && uv run uvicorn app.main:app --reload

dev-frontend:
	cd frontend && pnpm dev

dev:
	@echo "Use 'make start' to run both backend + frontend in dev mode"

test: test-backend test-frontend
	@echo "✅ All tests passed"

test-backend:
	docker compose run --rm -v ./backend/tests:/app/tests backend-dev sh -c "export UV_PROJECT_ENVIRONMENT=.venv-container && uv sync --frozen && uv run pytest -q"

test-frontend:
	docker compose run --rm --no-deps -v ./frontend:/app -w /app -e CI=true -e NODE_ENV=development frontend-dev sh -c "corepack enable && corepack prepare pnpm@9 --activate && pnpm install --frozen-lockfile && pnpm vitest run --passWithNoTests"
