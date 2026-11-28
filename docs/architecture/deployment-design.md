# Deployment Design

IP-005 · Stage 02 COMPLETED AND APPROVED · [AD-012](adr/adr-005-outbound-and-deployment.md)

Production MVP runs on a single self-hosted Linux host with Docker Engine and Docker Compose. Local development uses macOS and Docker Desktop. Run production-specific network verification on Linux. See [AD-013](../project/decision-register.md#ad-013). Nginx is the only published service. API, scheduler, both workers and migrate use the same backend image and separate runtime commands. The Nginx image serves the Vite build and proxies API and health routes on the same origin.

## Compose services

| Service | Command/role | Network and state |
|---|---|---|
| `nginx` | Serve immutable SPA assets, route HTML fallback, proxy API | Published HTTP/TLS and private ingress-to-API bridge. TLS material mounted read-only. SPA fallback never rewrites API errors. |
| `api` | Async FastAPI | Ingress and control-plane bridges. Scoped DB/Redis access. Shared lifecycle lock mount. |
| `scheduler` | Celery Beat + control worker pool | Control plane only. Beat scheduler state on a small volume. Separate processes under a single PID 1 supervisor. See [scheduler process lifecycle](#scheduler-process-lifecycle). |
| `worker-checks` | One container with multiple Celery prefork processes, checks queue | Control plane and restricted check egress. Shared execution/start lock mount. |
| `worker-notifications` | Celery prefork, notifications queue | Control plane and restricted provider egress. |
| `postgres` | Authoritative storage | Internal control plane. Persistent data volume. |
| `rabbitmq` | Durable business queues, control ticks and DLQs | Internal control plane. Persistent broker state volume. |
| `redis` | Ephemeral rate limiting | Internal control plane; no business recovery dependency. |
| `migrate` | One-shot Alembic upgrade | Internal control plane, temporary privileged migration DB role. |

Scheduler and worker commands use isolated queues and credentials. Avoid publishing data-plane ports including dashboard/management interfaces. API has no general outbound route. Lock storage is a host-local directory shared by the single check-worker container and API through explicit mounts. Scale check throughput through prefork children initially. Tie new container generations to explicit prior-container quiescence and expose exact child exit evidence to guarded recovery within the current generation. Derive filenames only from validated monitor UUIDs and never unlink or replace a file during operation, including on monitor deletion. Monitor inode growth and reclaim tombstone files only offline after all participating processes stop. Lock permissions allow the service identities to open the same inode. Network filesystems and multi-host check replicas are outside this design.

## Scheduler process lifecycle

Under [AD-016](../project/decision-register.md#ad-016), the supervisor starts one Beat process and one control worker command. Run a single scheduler service instance per installation. Require exclusive ownership before Beat starts and confirm the previous Beat process has exited before a replacement starts, including during restart or service replacement.

On termination, stop Beat from emitting ticks, stop control intake, allow in-flight control work to settle within the shutdown grace period and reap child processes. If either process exits unexpectedly, report the failure, shut down and reap the other process, and exit unsuccessfully for service-level recovery. Scheduler readiness requires both processes.

## Restricted egress

Under [AD-015](../project/decision-register.md#ad-015), Linux host-managed nftables enforcement, or an equivalently verified host-managed policy, is required for probe worker startup alongside application-level destination verification. Compose bridge membership alone is insufficient. A host-controlled provisioning step installs default-deny rules in worker network namespaces and host forwarding/input hooks. It applies both IPv4 and IPv6, checks effective destinations after DNAT, and bounds access to host services and other bridges. Validate rule attachment and identity across container recreation before starting workers. Keep rule setup authority outside the containers. The runtime containers drop unnecessary capabilities and cannot change firewall or routing. Do not use host networking, privileged containers or Docker socket mounts.

- Check-worker rules allow exact control-plane DB/broker peers and the designated DNS resolver, and approved HTTP(S) port access to eligible public ranges plus operator-allowed internal CIDRs. Always-denied classes and protected endpoints take precedence on the target path. The application also rejects the exact control-plane and DNS endpoints for probes. The narrow non-probe exceptions remain necessary capabilities of the worker process.
- Notification-worker rules allow exact control-plane peers, designated DNS and a provider-only HTTPS destination set under operator control. Maintain the verified numeric provider address set with validated resolution and atomic rule updates or an equivalently constrained provider path. Keep the fixed hostname and mandatory TLS identity verification regardless of routing mechanism. Refuse egress on uncertain/expired provider policy and surface delivery diagnostics.
- Block direct host/bridge management routes, unexpected resolver traffic and address translation into denied networks. The host procedure validates that published host ports, container DNS, loopback and IPv6 cannot provide a forbidden target path. Reconcile live policy version on restart and drain before changes per [security design](security-design.md#outbound-policy-and-pinned-transport).

Kernel/routing behavior depends on Docker, firewall backend and host setup. The [Stage 04 egress spike](../development/technical-spikes.md#5-ipv4ipv6-egress-enforcement) verified both address families on the supported native Linux fixture baseline. Local tests on Docker Desktop may use disposable isolated fixtures. Stage 04 defines the host provisioning and one-command startup instructions for the verified environment.

## Startup, shutdown and health

1. Check prerequisites, secrets, disk, state volumes and versioned firewall policy. Bring up healthy PostgreSQL, RabbitMQ and Redis. Run `migrate` under a DB migration lock and gate runtime startup on successful completion. Create enough result partitions ahead of traffic. Verify queue topology, startup roles, and the schema/policy version before declaring the relevant process ready.
2. Start API, scheduler, workers and Nginx. API liveness is independent of dependencies. Readiness checks bounded PostgreSQL and Redis availability and schema compatibility. RabbitMQ failure degrades dispatch asynchronously through the durable outbox; API readiness can stay green. Keep probe payloads generic and restrict readiness details.
3. Observe service health as well as functional progress: Beat heartbeat, control tick age, outbox backlog and oldest age, queue depth/inflight/DLQ, lease age, scheduling delay, pause/busy skips, worker restarts, UNKNOWN and FAILED deliveries, partition coverage, cleanup lag and disk/WAL growth. Use structured logs and operator queries in MVP. Prometheus/Grafana are scheduled for v1.0.0.
4. On shutdown stop new ticks and intake, drain in-flight work, close sockets, settle or leave recoverable durable state, and close per-process pools. Configure stop grace above the hard task deadline plus settlement margin, and require explicit proof of quiescence before host replacement. Fail forced terminations safely through guarded execution and notification recovery.

Environment settings cover public origin, registration, signing/encryption key references, DB/RabbitMQ/Redis endpoints, queue/pool/time budgets, network and rate policies and log level. Secrets are injected via mounted files and redacted across all processes. Fail startup on missing required secrets; provisioning and migrations use separate credentials from runtime access.

## Backup and recovery

PostgreSQL backups include scoped business data, live job state and outbox. Encrypt backups, restrict access, retain required encryption key versions separately, and practice restoring into an isolated environment. Document recovery objectives after restore measurements. Stop workers and isolate egress during restore. Rebuild transport infrastructure from topology and reconcile current eligible DB work before enabling egress. A point-in-time restore can lose evidence of a Telegram send that occurred after the restored point. Quarantine restored uncertain notification work as UNKNOWN and require evidence-based review before resuming sends; do not automatically replay that interval. Fence the old deployment before activating a replacement. Restore does not reset bootstrap authorization. Verify retained data expiry, migrations, job dispositions and diagnostics after recovery. Stage 08 defines the runbook and tested recovery procedure.
