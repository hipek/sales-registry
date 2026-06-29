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
