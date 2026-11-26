# ADR-002 · Authoritative Storage and Check History

**Status:** APPROVED baseline · AD-003 · owner approval in IP-005. The owner accepted the detailed design in IP-005 Final Acceptance.

## Context

MVP includes a 30-day history at a theoretical 43.2M completions at baseline, scoped deletion and incident retention.

## Decision

PostgreSQL owns business state. Use UUID identities, UTC timestamps, scoped foreign keys and transactional constraints. Partition results by completion time and anchor their canonical identity to the execution ledger. Keep a minimal monitor identity after deletion for associated incident history. [Database Design](../database-design.md) defines constraints, indexing and retention.

## Alternatives

An unpartitioned history makes expiry dependent on sustained row deletes and vacuum. Redis cannot supply authoritative durable history. Separate time-series storage would add consistency and operating boundaries.

## Consequences

Partition maintenance and ledger cleanup need independent monitoring. Stage 04 verifies DDL and partition behavior on the pinned PostgreSQL version. Stage 07 verifies physical cleanup and load behavior with representative data.
