# ADR-003 · Reliable Checks, Incidents and Notifications

**Status:** APPROVED baseline · AD-006 through AD-009 · owner approval in IP-005. The approved host guard and scheduler placement are in [ADR-005](adr-005-outbound-and-deployment.md).

## Context

Scheduling, target observation, incident transitions and Telegram sends cross different failure boundaries. Broker acknowledgements and provider responses cannot be committed atomically with PostgreSQL.

## Decision

Reserve checks with due-row locks and write a transactional outbox. Relay with publisher confirms and routing verification. Consume at least once with late acknowledgement, DB-backed idempotence and bounded recovery/dead-letter handling. Apply eligible observation, monitor state, incident and outbox in one transaction. Apply [PD-016](../../project/decision-register.md#pd-016) to a checked URL edit while PAUSED as defined in the [incident engine](../backend-design.md#incident-engine). Separate Telegram delivery and record UNKNOWN if acceptance is ambiguous. Use a network execution guard in addition to leases. [Backend Design](../backend-design.md) defines transactions and retry behavior.

## Alternatives

Publishing after commit without an outbox can lose work. Holding a broker acknowledgement as the only state loses durability across coupled failures. A lease alone can expire while a socket is active. Resending after an ambiguous Telegram response can duplicate a recipient receipt.

## Consequences

Duplicate envelopes are expected and require handlers to use durable identity. An interrupted started probe can leave an observation gap. Ambiguous Telegram outcomes need operator visibility. Acceptance verifies one controlled successful receipt across concurrent processing and replay.
