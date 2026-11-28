# InfraPulse — Project Charter

| Field | Value |
|---|---|
| ID | IP-DOC-001 |
| Version | 1.0 |
| Status | Approved baseline |
| Date | 2026-11-25 |
| Repository | infrapulse-monitor |

## Mission
Build an open-source, self-hosted infrastructure and API monitoring platform that demonstrates production-oriented Python backend engineering through a complete, usable web application.

## Audience and value
Backend developers, DevOps engineers, independent developers and small engineering teams need centralized health checks, incident history, performance analytics and actionable notifications without dependence on a hosted monitoring vendor.

## Product scope
| Release | Requirements |
|---|---|
| v0.1.0 MVP | F-001 Authentication (JWT and refresh tokens); F-002 workspace isolation; F-003 monitor CRUD; F-004 HTTP/HTTPS checks; F-005 scheduler; F-006 RabbitMQ/Celery tasks; F-007 check history; F-008 incidents; F-009 Telegram notifications; F-010 dashboard; F-011 SSRF protection and rate limiting; F-012 Docker Compose, migrations and GitHub Actions CI; F-029 Run Check Now; F-033 basic uptime and latency metrics |
| v0.5.0 Beta | F-013 TCP checks; F-014 SSL expiry; F-015 email; F-016 webhooks; F-017 RBAC; F-018 uptime and latency analytics; F-019 public status pages; F-020 maintenance windows; F-021 API keys; F-030 HTTP keyword monitoring; F-031 JSON assertion monitoring; F-032 workspace invitations and membership |
| v1.0.0 Release | F-022 audit log; F-023 Prometheus/Grafana; F-024 report export; F-025 interactive isolated demo mode; F-026 integration and load testing; F-027 public demo deployment; F-028 documentation |

The [PRD feature catalog](../product/prd.md#feature-catalog) records feature assignments and sources. The [Decision Register](decision-register.md#approved-product-decisions) records the detailed scope approved in PD-001–PD-016.

- **MVP.** Configurable public registration defaults to disabled after setup (PD-001). GET and HEAD checks have a 30-second minimum configurable interval (PD-002, PD-003). Configurable thresholds distinguish target failure from platform faults (PD-004). Manual execution (PD-005), scoped ownership and operator-controlled restrictive network policy (PD-006, PD-007), polling (PD-008) and basic uptime and latency (PD-011) complete the baseline. The web application is dark-only, accessible, desktop-first responsive and uses English (PD-013–PD-015).
- **Beta.** Add invitations, membership and role-based access (PD-001, PD-007), Server-Sent Events (PD-008), TCP, SSL, HTTP keyword and JSON assertion monitoring (PD-009) and expanded analytics (PD-011).
- **v1.0.0.** Extend demo mode and public deployment to a safe, interactive, isolated experience with controlled synthetic targets, resource limits and bounded data lifecycle (PD-006, PD-010). Publish repeatable performance evidence (PD-012).

Out of scope are Kubernetes, distributed agents, billing, microservices, AI, native mobile apps, full server metrics collection, arbitrary monitoring scripts and expressions, DNS/ICMP/heartbeat monitoring and multilingual UI. MVP excludes unsupported HTTP methods and arbitrary HTTP bodies. The product supports only the dark theme.

## Approved architecture and technologies
Modular monolith with separate API, scheduler and worker processes. PostgreSQL is the source of truth. Separate check and notification queues. Prefer simple designs, explicit boundaries, idempotency, bounded retries, API-first contracts and security by design.

The approved technology baseline includes FastAPI, PostgreSQL, RabbitMQ, Celery, Redis, React, Docker and Docker Compose. [D-010](decision-register.md#d-010) approves GitHub Actions as the required CI platform for MVP v0.1.0.

## Stage 02 design and verification

The owner approved the [architecture decisions](decision-register.md#approved-stage-02-architecture-decisions), the [technology stack](../architecture/technology-stack.md) and the [system design](../architecture/system-architecture.md) in IP-005. Stage 04 pinned exact dependency versions and all six mandatory technical spikes passed. The owner approved Stage 04 in [IP-007 Final Owner Acceptance](decision-register.md#ip-007-verification). Stage 07 verifies load targets and retention. See the [verification gates](../architecture/system-architecture.md#verification-gates).

## Success targets (not measured results)
- 1,000 active monitors at 60-second intervals; approximately 16.7 checks/s on average.
- API p95 at most 200 ms excluding external check duration, API server error rate below 1%, and scheduling delay p95 at most 5 seconds under the approved baseline.
- Backend line coverage target is at least 80%. Critical paths require meaningful tests.
- Initial check history retention is 30 days, equivalent to approximately 43.2 million results at full baseline load.
- The 30-second run with 1,000 monitors is a capacity stress scenario under PD-012. The [measurement protocol](../product/srs.md#performance-measurement-protocol) separates this scenario from baseline targets.
- Local startup with one documented Docker Compose command after prerequisites/configuration.
- Public demo uses controlled targets only; no arbitrary network probing.

## Governance
The owner approves scope, reviews changes and controls the repository. ChatGPT assists with requirements and design. Codex CLI is the current development assistant interface and uses repository documentation as the primary source of project context. Use the read-only sandbox for analysis and the workspace-write sandbox for approved edits. Obtain human approval before expanding task scope and human review before committing or merging. Automatic pushes to remote repositories are prohibited. See the [development workflow](../development/workflow.md).

UI, repository documentation, source identifiers, technical messages and code comments are in English. Project discussions, Codex CLI tasks and Codex reports are in Russian. The project follows GitHub Flow and uses issues, pull requests, ADRs and Conventional Commits. MIT is the intended license. The owner will add the license file during setup.

## Naming
InfraPulse is an approved working name, not a cleared trademark. Similar names have been reported in the same industry. Repository slug is infrapulse-monitor; account-level availability and legal clearance remain unverified. Reassess before public branding or commercial release.

## Approval
Stage 00 baseline approved by the project owner in conversation on 2026-11-25. Later approvals are recorded in the [decision register](decision-register.md) and [roadmap](roadmap.md).
