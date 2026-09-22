# Salary Management (ACME — 10k employees)

Web app for HR Manager to manage salaries + answer pay questions.
Replaces Excel workflow.

**Stack:** FastAPI + SQLAlchemy + SQLite · React 18 + Vite + Mantine.

## Docs (read in order, assessment artifacts only)

- `docs/01-requirements.md` — one-page scope + non-goals
- `docs/02-architecture.md` — design notes + diagrams + API/DB/UI
- `docs/03-tradeoffs-performance.md` — trade-offs + 10k perf plan
- `docs/04-ai-prompts.md` — AI workflow log (append-only)

## Run (Docker — recommended)

```bash
docker compose up --build
# seed runs first: 10,000 employees (Faker, seed=42, ~2s)
# api:  http://localhost:8000/docs (OpenAPI + Swagger try-it)
# web:  http://localhost:5173/ (Dashboard + Employees)
docker compose down  # stop; add -v to drop the seeded volume
```

## Run (local dev)

```bash
# backend
cd app/backend && python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
SALARY_DATABASE_URL="sqlite:////tmp/salary.db" \
  python -m app.seed.seed --count 10000 --fresh
uvicorn app.main:app --reload  # :8000

# frontend (second terminal)
cd app/frontend && npm install && npm run dev  # :5173
# build: npm run build | backend tests: pytest -q (from app/backend)
```

No login v1 (single HR Manager assumed, actor `hr_manager` in audit).

## Repo layout (Docker rule)

```text
pro/                        <- GitHub root
  app/                      <- ONLY this is COPY'd into images
    backend/
    frontend/
  docs/
  Dockerfile.backend Dockerfile.frontend docker-compose.yml
  README.md .gitignore
```
