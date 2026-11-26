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

## Approved architecture and technologies
Modular monolith with separate API, scheduler and worker processes. PostgreSQL is the source of truth. Separate check and notification queues. Prefer simple designs, explicit boundaries, idempotency, bounded retries, API-first contracts and security by design.

The approved technology baseline includes FastAPI, PostgreSQL, RabbitMQ, Celery, Redis, React, Docker and Docker Compose.

## Proposed technology candidates
Python 3.13, SQLAlchemy 2, Psycopg 3, Alembic, Pydantic 2, Celery Beat, HTTPX, TypeScript, Vite, Tailwind CSS, shadcn/ui, Recharts, Nginx, uv, pytest, Testcontainers, Ruff, mypy, structlog and GitHub Actions remain candidates. Version numbers in this list describe proposals.

## Pending architectural decisions
Dependency versions, database schema, worker concurrency and execution model, partitioning, use of a transactional outbox and delivery guarantees remain open. See the [decision register](decision-register.md) for other pending decisions and Product Discovery topics.

## Success targets (not measured results)
- 1,000 active monitors at 60-second intervals; approximately 16.7 checks/s on average.
- p95 API latency target: 200 ms for defined typical endpoints under a documented workload.
- Backend coverage target: at least 80%; critical paths require meaningful tests.
- Initial check history retention: 30 days (approximately 43.2 million checks at full target load).
- Local startup with one documented Docker Compose command after prerequisites/configuration.
- Public demo uses controlled targets only; no arbitrary network probing.

## Governance
The owner approves scope, reviews changes and controls the repository. ChatGPT assists with requirements and design. Codex CLI is the current development assistant interface and uses repository documentation as the primary source of project context. Use the read-only sandbox for analysis and the workspace-write sandbox for approved edits. Obtain human approval before expanding task scope and human review before committing or merging. Automatic pushes to remote repositories are prohibited. See the [development workflow](../development/workflow.md).

Code, UI and repository documentation are in English. Project discussions are in Russian. The project follows GitHub Flow and uses issues, pull requests, ADRs and Conventional Commits. MIT is the intended license. The owner will add the license file during setup.

## Naming
InfraPulse is an approved working name, not a cleared trademark. Similar names have been reported in the same industry. Repository slug is infrapulse-monitor; account-level availability and legal clearance remain unverified. Reassess before public branding or commercial release.

## Approval
Stage 00 baseline approved by the project owner in conversation on 2026-11-25. Detailed requirements and technical decisions remain subject to later stage approval.
