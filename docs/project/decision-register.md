# Decision Register
ID: IP-DOC-006 | Version: 1.0 | Status: Active

## Approved Stage 00 decisions

| ID | Decision |
|---|---|
| D-001 | InfraPulse working name; infrapulse-monitor monorepo |
| D-002 | Open-source self-hosted product; intended MIT license |
| D-003 | Modular monolith with background workers |
| D-004 | FastAPI, PostgreSQL, RabbitMQ, Celery, Redis, React, Docker and Docker Compose baseline |
| D-005 | MVP → Beta → v1.0.0 release boundaries, including CI for MVP and Prometheus and Grafana for v1.0.0 |
| D-006 | English repository and UI; Russian discussions |
| D-007 | GitHub Flow, issues, PRs, ADRs, tests, CI |
| D-008 | Eight-week indicative roadmap for InfraPulse |
| D-009 | Owner approval and review, ChatGPT design support and Codex CLI as the current development assistant interface |

Under D-009, repository documentation is the primary source of project context. Codex CLI uses the read-only sandbox for analysis and the workspace-write sandbox for approved edits. Task scope changes require human approval. Commits and merges require prior human review. Automatic pushes to remote repositories are prohibited. See the [development workflow](../development/workflow.md).

## Proposed technology candidates

The [charter's candidate list](charter.md#proposed-technology-candidates) records technologies proposed for evaluation at later stage gates.

## Pending architectural decisions

- Dependency versions.
- Worker concurrency and asynchronous execution strategy.
- Database schema, partitioning and retention implementation.
- Use of a transactional outbox and delivery guarantees.
- API contracts and deployment provider.

Resolve these through subsequent stage gates and ADRs.

## Unresolved Product Discovery topics

- Manual monitor execution (Run Check Now).
- Incident and recovery thresholds.
- Permitted network targets and SSRF policy.
- Workspace ownership and authorization rules.
- Performance measurement methodology.
- Uptime and latency definitions.

## Other pending decisions

- Branding clearance.
