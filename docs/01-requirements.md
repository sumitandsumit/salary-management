# 01 — Requirements (One-Page)

| Field    | Value                                                                                              |
| -------- | -------------------------------------------------------------------------------------------------- |
| Document | Requirements — ACME Salary Management (10k employees)                                              |
| Version  | 1.0                                                                                                |
| Date     | 2026-09-21                                                                                         |
| Status   | Approved for build                                                                                 |
| Source   | `Salary Management Assessment — Candidates.md` + HR email + assessor guidance (Sandli, 2026-09-21) |

## 1. Goal & persona

Replace Excel-based salary tracking for 10,000 employees across multiple
countries with a web app where a single HR Manager manages pay data and
answers "how do we pay people?".

## 2. Scope v1

**Employee:** id (UUID), name, email (unique), department, job_title,
country (ISO-2), currency (ISO-4217), base_salary + bonus (Decimal
`NUMERIC(14,2)`, never float), joining_date, status (active/inactive).

**Manage:** paginated list (25/50/100), search name/email, filter
dept/country/status/salary-range, sort salary/joining/name; create, view,
single-edit, % increment with reason; soft-deactivate (no hard delete).

**Insights:** total payroll (USD-normalized + per-currency), avg/median by
dept/country, headcount by dept/country, top-10 earners, distribution
buckets — all respecting current filters.

**Robust currency:** store local amount + code; `exchange_rates` table
holds versioned `rate_to_usd`; analytics show local + USD with `rate_date`.
Deterministic seed, refreshable via endpoint. Live FX is future.

**Cross-cutting:** single assumed HR user (no login v1); audit log per
mutation (`hr_manager`, old/new, reason); JSON logs + request-id;
validation + error envelope `{code,message,details,request_id}`; 10k seed.

## 3. Deliberately out (with reason)

- **Full authN/Z:** out per assessor ("not required, assume single HR").
  Saves time, avoids over-engineering. Seam: `TODO(auth)` + `require_hr()`.
- **Salary history table:** out to ship fast; audit log captures old/new.
  Seam: `TODO(history)` for `salary_history` table later.
- **Bulk CSV:** future; single-edit + increment suffices. Seam `TODO(bulk)`.
- **Payroll/tax/payslips, live FX, hard delete, multi-role/SSO, caching:**
  compliance/complexity creep with no v1 benefit; documented upgrade paths.

## 4. NFRs

p95 list < 300ms on 10k (paginated + indexed), deterministic seed (42),
fast unit tests, Docker Compose local run, SOLID layered code.
