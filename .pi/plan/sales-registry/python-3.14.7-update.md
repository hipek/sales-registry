# Python 3.14.7 backend update plan

Goal: update backend runtime docs and Docker base to require Python 3.14+ and pin runtime to Python 3.14.7. No code changes expected.

## Current state found

- `backend/pyproject.toml`: already `requires-python = ">=3.14"`.
- `backend/uv.lock`: already `requires-python = ">=3.14"`.
- `Dockerfile.backend`: currently `FROM python:3.14-slim AS base`; pin to `python:3.14.7-slim`.
- `README.md`: stack says `Python 3.14`; prerequisites say `Python 3.12+` — update to `Python 3.14.7+`.
- `docker-compose.yaml` / `deploy-compose.yaml`: use `Dockerfile.backend`, no direct Python version references.
- `AGENTS.md`: no Python version references to update.

## Proposed changes

1. Pin backend Docker runtime:
   - `Dockerfile.backend`: change `python:3.14-slim` to `python:3.14.7-slim`.

2. Update user-facing docs:
   - `README.md`: stack row -> `Python 3.14.7`.
   - `README.md`: prerequisites -> `Python 3.14.7+, Node 20+, uv, pnpm`.

3. Leave lockfile unchanged:
   - `backend/uv.lock` already enforces `>=3.14`.
   - Exact patch pin lives in Docker base image, not uv lock.

## Verification after implementation

1. Build backend image:
   - `docker compose build backend-dev`
   - or `docker build -f Dockerfile.backend .`

2. Confirm runtime:
   - `docker run --rm <backend-image> python --version`

3. Run tests:
   - `make test`
   - `make e2e`

## Acceptance criteria

- Backend Docker image uses Python 3.14.7 exactly.
- Local dev docs require Python 3.14.7+.
- `requires-python` remains `>=3.14`.
- Backend pytest and Playwright e2e pass.
