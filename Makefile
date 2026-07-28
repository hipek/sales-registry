.PHONY: start stop build logs clean dev dev-backend dev-frontend test test-backend frontend-check init backend-check e2e e2e-setup e2e-clean

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

test: test-backend
	@echo "✅ All tests passed"

test-backend:
	docker compose run --rm -v ./backend/tests:/app/tests backend-dev sh -c "export UV_PROJECT_ENVIRONMENT=.venv-container && uv sync --frozen && uv run pytest -q"

ci: test backend-check frontend-check
	@echo "✅ CI checks passed"

frontend-check:
	cd frontend && pnpm run lint && ./node_modules/.bin/tsc --noEmit && pnpm run format

backend-check:
	cd backend && uv sync --frozen && uv run ruff check . && uv run ruff format . --check

e2e:	e2e-clean e2e-setup
	docker compose run --rm e2e
	@echo "✅ E2E tests done"

e2e-setup:
	docker compose up --force-recreate -d --wait backend-e2e frontend-e2e
	docker compose run --rm backend-e2e sh -c "export UV_PROJECT_ENVIRONMENT=.venv-container && uv run alembic upgrade head"
	@echo "✅ E2E environment ready"

e2e-clean:
	rm -f ./data/e2e.sqlite ./data/e2e.sqlite-wal ./data/e2e.sqlite-shm
	@echo "✅ Old e2e database cleaned"
