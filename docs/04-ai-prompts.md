# 04 — AI Prompts Log

| Field    | Value                                     |
| -------- | ----------------------------------------- |
| Document | Prompts / instructions used with AI tools |
| Version  | 1.0 (append-only)                         |
| Date     | 2026-09-21                                |
| Status   | Living document                           |

Assessment requires intentional AI use with quality. Log every meaningful
prompt: goal, key instruction, outcome, files touched.

## 2026-09-21 — requirements + architecture first

- Goal: one-page requirements + architecture without assumptions.
- Instruction: "Build architecture first from assessment + email; ask
  before assuming; HR-only; 10k seed; FastAPI + React + SQLite."
- Outcome: `01-requirements.md`, `02-architecture.md`, stack locked.
- Touched: `pro/docs/*`, `pro/README.md`, `pro/app/` layout.

## 2026-09-21 — auth clarification + currency robustness

- Goal: resolve auth scope + FX fluctuation handling + fastest stack check.
- Instruction: "Choose what suits; robust local-currency design; JWT
  options for discussion; Docker local; maintainable every direction."
- Outcome: currency read-normalization design; auth options A/B/C with
  JWT recommended; Docker rule (`app/` ships, root holds Dockerfiles).
- Touched: `pro/docs/*`, `local/README.md`.

## 2026-09-21 — assessor guidance applied + UI + docs hygiene

- Goal: apply Sandli email (auth not required); pick UI lib; keep
  `pro/docs/` to assessment artifacts in standard format.
- Instruction: "Go with Mantine; only asked artifacts in pro/docs, rest
  to local/; standard format; commit-ready; SOLID; follow assessment."
- Outcome: no-auth v1 decided + recorded; Mantine locked; docs
  consolidated to 01–04; full notes moved to `local/design-notes/`.
- Touched: `pro/docs/01–04`, `local/design-notes/*`, `pro/README.md`.

## 2026-09-21 — core BE + FE build

- Goal: layered FastAPI backend + Mantine frontend, verified green.
- Instruction: "Proceed with core BE / Go for core FE; SOLID;
  easy to understand/maintain/scale; follow assessment."
- Outcome: `app/backend` CRUD + increment + analytics + 4 tests green;
  `app/frontend` employees table + dashboard, `npm run build` green.
  Fixed: EmailStr vs `@acme.local`, logging request_id, NumberInput types.
- Touched: `pro/app/backend/*`, `pro/app/frontend/src/*`.

## 2026-09-21 — Docker + 10k seed

- Goal: step 4 (Dockerfiles + compose) + step 5 (deterministic 10k seed).
- Instruction: "Proceed to step 4 + step 5."
- Outcome: `Dockerfile.backend/frontend`, `nginx.conf` SPA fallback,
  `docker-compose.yml` (seed → api → web, shared SQLite volume),
  Faker seed=42 bulk-1000 (~2s); verified `compose up` end-to-end:
  health ok, 10k rows, analytics headcount 9496 active, web 200.
- Touched: `pro/Dockerfile.*`, `pro/docker-compose.yml`, `pro/nginx.conf`,
  `pro/.dockerignore`, `pro/app/backend/app/seed/seed.py`, `pro/README.md`.
