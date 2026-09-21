# 03 — Trade-offs & Performance

| Field    | Value                                               |
| -------- | --------------------------------------------------- |
| Document | Trade-off explanations + performance considerations |
| Version  | 1.0                                                 |
| Date     | 2026-09-21                                          |
| Status   | Approved for build                                  |

## 1. Trade-offs

| Choice                    | Why                                   | Cost & mitigation                                        |
| ------------------------- | ------------------------------------- | -------------------------------------------------------- |
| SQLite vs Postgres        | Zero-ops, single file, enough for 10k | Single-writer; repo abstraction + Alembic seam, DSN swap |
| Monolith vs microservices | One persona/team; avoids ops overhead | Split later by bounded context if needed                 |
| FastAPI vs Django         | Speed + OpenAPI + role fit            | No admin panel; React admin covers it                    |
| Vite SPA vs Next.js       | No SSR/SEO need for HR tool           | Add Next.js only if public pages arise                   |
| Mantine vs MUI/Bootstrap  | Least code for tables/modals/filters  | Smaller ecosystem; swap is UI-local                      |
| No auth v1                | Assessor: not required; saves ~2h     | `require_hr()` + `TODO(auth)` seam                       |
| Static rates vs live FX   | Deterministic, testable, no keys      | `FxService` interface for live provider                  |

## 2. Performance (10k rows)

- Pagination mandatory (`LIMIT/OFFSET`, max 100); never full-table JSON.
- Indexes on `status, department, country, base_salary, email, name`.
- Analytics in SQL (`SUM/AVG/COUNT/GROUP BY`), 1–2 queries per summary.
- Seed bulk batches of 1000 in one transaction, target < 10s, seed=42.
- Frontend: debounced search, memoized filters, charts on buckets only.
- Gate: p95 `GET /employees` < 300ms locally; seed determinism asserted.

## 3. Not optimized (on purpose)

No Redis, replicas, or sharding — 10k rows needs none. Added complexity
would hurt clarity scores. Revisit beyond ~1M rows with Postgres + cache.
