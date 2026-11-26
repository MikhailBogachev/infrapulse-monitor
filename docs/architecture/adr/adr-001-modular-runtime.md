# ADR-001 · Modular Backend and Execution Model

**Status:** APPROVED baseline · AD-001 and AD-002 · owner approval in IP-005.

## Context

Interactive workspace operations and slow network checks have different blocking and failure characteristics. MVP needs explicit boundaries with one Python codebase.

## Decision

Use a modular monolith with the `backend/src/infrapulse/` layout. FastAPI uses async SQLAlchemy. Celery prefork children use sync SQLAlchemy and HTTPX. Celery Beat emits dispatcher ticks. Share models and initialize connection resources separately per process. Apply the module and unit-of-work boundaries in [Backend Design](../backend-design.md#module-boundaries).

## Alternatives

One process for API and monitoring would couple latency and outages. A fully async task runtime would require a different worker execution model. Microservices, CQRS and Event Sourcing add cross-service and data coordination beyond MVP needs.

## Consequences

Modules and migrations ship together. Process resource isolation and post-fork initialization are explicit. Stage 04 verifies runtime compatibility and later measurements determine pool and concurrency budgets.
