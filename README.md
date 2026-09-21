# Salary Management (ACME — 10k employees)

Web app for HR Manager to manage salaries + answer pay questions.
Replaces Excel workflow.

**Stack:** FastAPI + SQLAlchemy + SQLite · React 18 + Vite + Mantine.

## Docs (read in order, assessment artifacts only)

- `docs/01-requirements.md` — one-page scope + non-goals
- `docs/02-architecture.md` — design notes + diagrams + API/DB/UI
- `docs/03-tradeoffs-performance.md` — trade-offs + 10k perf plan
- `docs/04-ai-prompts.md` — AI workflow log (append-only)

## Run (after scaffold)

```bash
docker compose up --build
# api: http://localhost:8000/docs, web: http://localhost:5173
```

No login v1 (single HR Manager assumed). Seed 10k via seed job.

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

Only `pro/` is pushed to GitHub. Personal/scratch stays in `../local/`.
