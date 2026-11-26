# ADR-005 · Outbound Security and Compose Enforcement

**Status:** APPROVED · AD-010 and AD-012–AD-016 · owner approval in IP-005.

## Context

Actual socket destinations must meet current policy. Compose networking cannot express these destination rules by itself. Pause and non-overlap must hold across DB disconnect and expired leases.

## Decision

Retain the approved Compose service model, security checks and health boundaries. Use a one-connection HTTPX transport pinned to a validated numeric peer. The [deployment design](../deployment-design.md) defines runtime boundaries and traffic rules.

<a id="ad-013"></a>
### AD-013 — Linux Deployment Environment

Production runs on a single Linux host with Docker Engine and Docker Compose. Local development uses macOS and Docker Desktop. Run production-specific network verification on Linux.

<a id="ad-014"></a>
### AD-014 — Check Worker Execution Guard

Use one check-worker container with multiple prefork processes and shared OS execution and start locks. A subsequent execution requires proof that the previous execution has ended. For a marked attempt, confirm socket closure or exact process exit before recovery. Lease expiry alone cannot authorize execution. The mandatory Stage 04 [execution guard spike](../backend-design.md#execution-guard-spike) is pending.

<a id="ad-015"></a>
### AD-015 — Host-managed Network Egress

Pair application-level destination verification with Linux host-managed IPv4 and IPv6 outbound restrictions. The mandatory Stage 04 [HTTPX transport and IPv4/IPv6 egress spikes](../security-design.md#mandatory-outbound-spike) are pending.

<a id="ad-016"></a>
### AD-016 — Scheduler & Control Worker

Place Celery Beat and the control worker in one scheduler container as separate supervised processes. Handle process failures, support graceful shutdown and prevent duplicate Beat instances. See the [scheduler process lifecycle](../deployment-design.md#scheduler-process-lifecycle).

## Alternatives

Compose-only isolation cannot enforce destination eligibility. An unrestricted HTTP client may resolve a hostname again after policy validation. Database leases and connection-scoped locks cannot exclude an active request after expiry or disconnection. A dedicated outbound gateway or distributed fencing would introduce a larger deployment change and would need independent approval and verification.

## Consequences

Production startup depends on verified host setup, one probe-worker host and fail-closed readiness. Supporting multiple hosts requires a new execution guard decision. Transport, kernel networking and process guarantees remain implementation gates. Failed verification requires a revised design and owner review before engine work.
