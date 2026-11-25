# InfraPulse — Project Charter

| Field | Value |
|---|---|
| ID | IP-DOC-001 |
| Version | 1.0 |
| Status | Approved baseline |
| Date | 2026-11-25 |
| Repository | infrapulse-monitor |

## Mission
Build a self-hosted infrastructure and API monitoring platform that demonstrates production-oriented Python backend engineering through a complete, usable web application.

## Audience and value
Backend developers, DevOps engineers, independent developers and small IT teams need centralized health checks, incident history, performance analytics and actionable notifications without dependence on a hosted monitoring vendor.

## Product scope
| Release | Requirements |
|---|---|
| v0.1.0 MVP | F-001 Authentication (JWT and refresh tokens); F-002 workspace isolation; F-003 monitor CRUD; F-004 HTTP/HTTPS checks; F-005 scheduler; F-006 RabbitMQ/Celery tasks; F-007 check history; F-008 incidents; F-009 Telegram notifications; F-010 dashboard; F-011 SSRF protection and rate limiting; F-012 Docker Compose, migrations and CI |
| v0.5.0 Beta | F-013 TCP checks; F-014 SSL expiry; F-015 email; F-016 webhooks; F-017 RBAC; F-018 uptime and latency analytics; F-019 public status pages; F-020 maintenance windows; F-021 API keys |
| v1.0.0 Release | F-022 audit log; F-023 Prometheus/Grafana; F-024 report export; F-025 demo mode; F-026 integration and load testing; F-027 public demo deployment; F-028 documentation |

Out of scope: Kubernetes, distributed agents, billing, microservices, AI, native mobile apps and full server metrics collection.

## Architecture baseline
Modular monolith with separate API, scheduler and worker processes. PostgreSQL is the source of truth. Separate check and notification queues. Prefer simple designs, explicit boundaries, idempotency, bounded retries, API-first contracts and security by design.

Proposed stack: Python 3.13, FastAPI, SQLAlchemy 2, Psycopg 3, Alembic, Pydantic 2, RabbitMQ, Celery, Celery Beat, Redis, HTTPX, React, TypeScript, Vite, Tailwind CSS, shadcn/ui, Recharts, Nginx, Docker Compose, uv, pytest, Testcontainers, Ruff, mypy, structlog, Prometheus, Grafana and GitHub Actions. Exact versions and worker concurrency model require validation at later gates.

## Success targets (not measured results)
- 1,000 active monitors at 60-second intervals; approximately 16.7 checks/s on average.
- p95 API latency target: 200 ms for defined typical endpoints under a documented workload.
- Backend coverage target: at least 80%; critical paths require meaningful tests.
- Initial check history retention: 30 days (approximately 43.2 million checks at full target load).
- Local startup with one documented Docker Compose command after prerequisites/configuration.
- Public demo uses controlled targets only; no arbitrary network probing.

## Governance
The owner approves scope, reviews changes and controls the repository. ChatGPT assists with requirements and design; Codex assists with implementation. Human review remains mandatory. English code, UI and repository documentation; Russian project discussions. GitHub Flow, issues, pull requests, ADRs and Conventional Commits. MIT license intended; actual license file to be added by owner at setup.

## Naming
InfraPulse is an approved working name, not a cleared trademark. Similar names have been reported in the same industry. Repository slug is infrapulse-monitor; account-level availability and legal clearance remain unverified. Reassess before public branding or commercial release.

## Approval
Stage 00 baseline approved by the project owner in conversation on 2026-11-25. Detailed requirements and technical decisions remain subject to later stage approval.
