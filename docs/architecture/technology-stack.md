# Technology Stack

IP-005 · Stage 02 COMPLETED AND APPROVED

The project owner approved this stack in IP-005. Major version constraints are part of the selection. Stage 04 pinned exact versions and passed the mandatory [stack compatibility spike](../development/technical-spikes.md#1-technology-stack-compatibility).

| Area | Technology | Responsibility |
|---|---|---|
| Backend runtime and boundaries | Python 3.13, FastAPI, Pydantic 2 | Async request handling, OpenAPI and validated DTOs |
| Storage | SQLAlchemy 2, Psycopg 3, Alembic, PostgreSQL | Shared mappings, separate async/sync sessions, migrations and authoritative state |
| Background processing | RabbitMQ, Celery, Celery Beat | Durable queues, prefork execution and periodic ticks |
| Outbound HTTP | HTTPX | Synchronous outbound HTTP with a validated connection path |
| Rate limiting | Redis | Ephemeral atomic request counters |
| Frontend runtime and build | React, TypeScript, Vite | Browser SPA and static production bundle |
| Frontend UI | Tailwind CSS, shadcn/ui, Recharts, Lucide React | Design primitives, charts and icons |
| Frontend flow and data | React Router, TanStack Query, React Hook Form, Zod | Routing, server state, forms and client-side schemas |
| Delivery and local operation | Nginx, Docker, Docker Compose, uv | Same-origin entry point, containers and Python dependency management |
| Quality and diagnostics | pytest, Testcontainers, Ruff, mypy, structlog | Controlled backend fixtures, static checks and structured diagnostics |
| Frontend quality | Vitest, Testing Library, Playwright | Unit, interaction and browser journey checks |
| CI | GitHub Actions | Required MVP tests and quality gates under [D-010](../project/decision-register.md#d-010) |
| Operational telemetry | Prometheus and Grafana | v1.0.0 telemetry and operator dashboards |

## Stage 04 compatibility verification

- Build Python 3.13 and both Psycopg/SQLAlchemy paths on the supported Linux image architectures. Verify wheel availability, TLS trust, asynchronous transaction rollback and Alembic upgrades from the supported schema.
- Exercise prefork child initialization and shutdown, hard/soft time limits, late acknowledgements, worker loss, RabbitMQ confirm and unroutable-return behavior with the actual Celery transport. Verify Redis atomic limiter behavior and test fixture startup under Compose and CI.
- Validate frontend runtime, build and packages together, including routing fallback, production assets, test/browser binaries and type checking. Establish supported Node and browser versions using a reproducible build.
- Select and verify the minimal authentication and cryptographic support for JWT, Argon2id and authenticated secret encryption as part of Stage 04 dependency review.
- Lock the verified dependencies and image versions. Establish required GitHub Actions jobs and observable pass/fail evidence per [AC-057](../product/acceptance-criteria.md#ac-057). Testcontainers fixtures use controlled destinations.
- Prove the selected HTTPX transport and host enforcement through the [outbound spike](security-design.md#mandatory-outbound-spike). The approved stack alone provides no compatibility, performance or security test evidence.
