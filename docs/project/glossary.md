# Glossary
ID: IP-DOC-004 | Version: 1.0 | Status: Active

| Term | Definition |
|---|---|
| Workspace | Tenant boundary for monitors, users and settings. |
| Monitor | Configuration of a recurring health check. |
| Check execution | One scheduled or manually requested logical check. |
| Check result | Persisted outcome, timing and diagnostic metadata of an execution. |
| Incident | Period of confirmed service degradation or unavailability. |
| Recovery | Confirmed return to healthy state. |
| Uptime | Availability ratio over a defined observation window; unknown and maintenance semantics must be specified. |
| Latency | Measured check duration; exact measurement boundaries to be defined. |
| Scheduler | Process identifying due checks and dispatching work. |
| Broker | RabbitMQ transport for task messages. |
| Worker | Process consuming and executing background tasks. |
| Idempotency | Repeated processing of the same logical operation does not duplicate its business effects. |
| Retry | Bounded reattempt after a transient failure. |
| Outbox | Durable database record of events awaiting publication. |
| SSRF | Server-side request forgery: abuse of server-originated requests to reach unintended destinations. |
| RBAC | Role-based access control. |
| Retention | Policy for expiring historical data. |
| Status page | Public view of selected service states. |
| ADR | Architecture decision record. |
| PRD / SRS | Product requirements document / software requirements specification. |
| DoD | Definition of Done. |
| MVP | Minimum viable product, a usable end-to-end release. |
