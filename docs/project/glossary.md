# Glossary
ID: IP-DOC-004 | Version: 1.0 | Status: Active

| Term | Definition |
|---|---|
| Workspace | Tenant boundary for authorized monitors, observations, incidents, members and workspace settings. Installation policy is outside workspace authority. |
| Installation Operator | Authorized actor responsible for installation-wide setup, registration, destination policy and operation. |
| Allowlist | Installation operator policy explicitly permitting selected eligible internal network destinations subject to always-denied rules. |
| Monitor | Configuration of a recurring health check. |
| Check execution | One logical scheduled or on-demand attempt to observe a monitored target. Delivery and processing retries can refer to the same execution. |
| Manual Check | An authorized asynchronous, rate-limited check requested through Run Check Now. |
| Check result | A recorded outcome of one execution with its timing, origin and safe diagnostic evidence. |
| Monitor State | Live summary of a monitor's condition or lifecycle. The states are PENDING, UP, DOWN and PAUSED. |
| Incident | A recorded period of confirmed target unavailability that begins when the configured qualifying failure threshold is reached. |
| Recovery | Confirmed return to a healthy state when an active incident reaches its qualifying success threshold. |
| Uptime | Percentage of qualifying completed checks that succeeded in a defined observation window. Qualifying target failures and target timeouts enter the denominator. Excluded or absent observations are shown separately. |
| Latency | Duration of a qualifying successful scheduled check. Metrics include average and nearest-rank p95 and p99 subject to their sample minimums. |
| Polling | Browser-initiated HTTP requests for current data every 10 seconds on the designated MVP screens. |
| Server-Sent Events | Server-originated browser event stream used for Beta live updates. |
| Scheduler | Process identifying due checks and dispatching work. |
| Broker | RabbitMQ transport for task messages. |
| Worker | Process consuming and executing background tasks. |
| Idempotency | Repeated processing of the same logical operation does not duplicate its business effects. |
| Retry | Bounded reattempt after an eligible confirmed failure. |
| Outbox | Durable database record of events awaiting publication. |
| Execution lease | Expiring database claim used to find work for recovery. The worker execution lock owns actual probe exclusion. |
| Execution guard | Shared host-local lock held by the probe process until its socket is closed. A separate start lock serializes lifecycle changes with outbound starts. |
| Publisher confirm | RabbitMQ acknowledgement of a publication. Route success is verified separately. |
| UNKNOWN delivery | Terminal automated disposition when provider acceptance cannot be determined safely. |
| SSRF | Server-side request forgery: abuse of server-originated requests to reach unintended destinations. |
| RBAC | Role-based access control. |
| Retention | Policy for expiring historical data. |
| Status page | Public view of selected service states. |
| ADR | Architecture decision record. |
| PRD / SRS | Product requirements document / software requirements specification. |
| DoD | Definition of Done. |
| MVP | Minimum viable product, a usable end-to-end release. |
