# IP-007 technical spike reports

Stage 04 is **IN PROGRESS**. The headings follow the six [architecture verification gates](../architecture/system-architecture.md#verification-gates). Each result applies to the stated experiment and platform. All experiments use synthetic endpoints, data and credentials. The spike image and Compose profile are separate from the backend runtime image.

## Reproduction environment

Local verification ran on Apple Silicon macOS with CPython 3.13.12, uv 0.11.19, Node 20.20.2, npm 10.8.2, Docker Desktop 4.47.0, Docker Engine 28.4.0 and Compose v2.39.4. Linux containers ran on arm64 through LinuxKit. The [setup guide](setup.md#prerequisites) lists the release tags. Use a fresh Compose project, secrets and port for the experiments.

```sh
export COMPOSE_PROJECT_NAME=infrapulse-ip007
export INFRAPULSE_PORT=18087
export INFRAPULSE_BASE_URL=http://127.0.0.1:18087
export INFRAPULSE_SECRETS_DIR=./.secrets/ip007
make install config up spike-runner
```

## 1. Technology Stack Compatibility

**Objective and acceptance.** Resolve the approved stack together, exercise the real data, broker and browser paths and establish the compatible Linux build and CI matrix under F-012, NFR-013–NFR-015 and AC-055–AC-057.

**Environment and command.** Python 3.13.12, Psycopg 3.3.3, SQLAlchemy 2.0.48, Celery 5.6.3, PostgreSQL 17.9, RabbitMQ 4.2.5, Redis 8.6.2, React 19.2.4, Vite 7.3.8 and Playwright 1.58.2. Run `make spike-stack`; run `make lint typecheck test` and `npm --prefix frontend run build` for the quality gates.

**Observed.** Locked installation, binary wheel provisioning, static checks, unit tests and Linux arm64 container builds and an emulated linux/amd64 backend build completed. Nginx, PostgreSQL, RabbitMQ and Redis became healthy. The migration initialized and updated the schema with its dedicated role. Readiness verified the matching revision and Redis. Synthetic messages exercised a real DB session in each prefork lane. A disposable PostgreSQL Testcontainers run confirmed both driver paths and async rollback. The Linux arm64 runtime used binary libpq 18.0 and loaded its system CA trust store. The emulated amd64 runtime also loaded the binary driver and CA trust store and executed synchronous and asynchronous PostgreSQL queries. An injected Beat process exit stopped the scheduler with exit code 1. Starting the scheduler again restored health. The fixture verified Redis atomic commands and JWT, Argon2id and AES-GCM round trips. Using SQLAlchemy's asyncio extra fixed a missing greenlet dependency on macOS. Vitest and the local and container SPA build passed. Chromium on macOS hit a Mach service permission failure. The Playwright Chromium smoke subsequently passed in a Linux arm64 fixture on the private Compose ingress bridge.

**Result — PASS.** The local toolchain, Linux containers and synthetic compatibility checks passed on the tested matrix. Actual GitHub CI execution under AC-057 and the native Linux host policy remain separate acceptance evidence. Initial migration verification covers the foundation revision.

## 2. PostgreSQL DDL and Partitioning

**Objective and acceptance.** Verify the [proposed result identity and partition DDL](../architecture/database-design.md#result-identity-and-partitioning) under AD-003, plus monitor deletion and retention evidence for AC-015 and AC-036.

**Environment and command.** PostgreSQL 17.9 Linux arm64. Run `make spike-postgres` on the disposable project.

**Observed.** PostgreSQL enforced the partition-key requirement for uniqueness, partition primary key, canonical instant and tenant foreign key, per-monitor sequence, scheduled slot and active-execution uniqueness. An uncovered future instant failed insertion. A generic prepared plan removed one subplan and used the retained partition's history index. With a concurrent ACCESS SHARE lock, ATTACH succeeded, DETACH reached lock timeout with SQLSTATE `55P03`, and DETACH plus DROP succeeded after the reader was cancelled. The experiment excluded an expired row at the UTC cutoff, removed its partition, tombstoned the monitor and removed its remaining results, ledger and epoch. The closed incident remained queryable with its execution UUID snapshot.

**Result — PASS.** Full-volume query plans, lock budgets, physical cleanup throughput, WAL and storage sizing remain Stage 07 work.

## 3. RabbitMQ Delivery Semantics

**Objective and acceptance.** Verify AD-007's mandatory confirm/return path, settlement ordering, bounded broker redelivery, dead-letter handling and durable effect deduplication with the real Celery transport.

**Environment and command.** RabbitMQ 4.2.5, Celery 5.6.3, Kombu 5.7.0, Pika 1.3.2 and PostgreSQL 17.9. Run `make spike-rabbit` on the disposable project.

**Observed.** A mandatory unroutable publish produced both a broker confirmation and the Kombu return callback. The independent Pika publish surfaced `UnroutableError`. A quorum message with delivery limit 3 reached the dead-letter queue after delivery counts 0–3 with the `delivery_limit` reason. Two prefork children were deliberately killed before transaction commit and after commit before ack, respectively. Each task was redelivered, completed, and subsequent duplicate messages left one database effect per job. A publisher SIGKILL after confirm and before DB settlement left the outbox fixture eligible. Relaying the same job again kept one database effect. The prefork test observed a soft deadline and exact child exit after the hard deadline, then completed another database task.

**Result — PASS.** This is at-least-once work delivery with database deduplication. The fixture uses broker-default at-most-once dead-letter transfer and verifies routing with the destination available. The authoritative outbox and recovery workflow will need coverage of unavailable dead-letter routes and ambiguous broker-side confirms before production use.

## 4. HTTPX Secure Transport

**Objective and acceptance.** Exercise AD-006 and AD-010's validated numeric dial and identity requirements with controlled traffic for AC-051 and AC-052.

**Environment and command.** HTTPX 0.28.1, httpcore 1.0.9, cryptography 50.0.0, dnspython 2.9.2 and private IPv4/IPv6 Compose networks. Run `make spike-httpx`.

**Observed.** Local UDP produced exact A and AAAA answers. A truncated answer failed closed. Changed and mixed answers were rejected before a new dial. The original DNS name and port appeared in Host, the DNS name in TLS SNI, and both actual TCP peers matched the selected address. Direct IPv4 and IPv6 literals verified IP SANs. Wrong DNS and IP identities failed before HTTP. Explicit proxy environment values were ignored. Redirects generated one request, and the fixture rejected a second dial on the same client with pooling disabled. A held HTTP response exhausted the two-second monotonic budget without a second dial. The always-deny conflict fixtures included loopback, mapped loopback, link-local metadata and an explicitly protected address. The metadata address was used only as an input to the local address classifier.

**Targeted follow-up.** `test_denied_direct_and_redirect_targets` passed in the private dual-stack Compose fixture. It exercised private literals denied by default, protected-address conflicts, mapped IPv4 literals, and IPv4/IPv6 redirects to a separate denied TLS listener. The initial request used one pinned dial and the denied listener received no HTTP request. Classifier-only conflicts additionally covered unspecified, multicast, broadcast, IPv6 link-local and mapped metadata addresses. The earlier retry, reconnect, pooling, proxy and valid direct-IP evidence was retained.

**Result — PASS.** The candidate relies on pinned private HTTPX/httpcore interfaces. Re-run the experiment on upgrades. End-to-end guard integration, the full production URL policy and post-routing Linux enforcement remain distinct gates.

## 5. IPv4/IPv6 Egress Enforcement

**Objective and acceptance.** Prove AD-013 and AD-015 on Linux under AC-051 and AC-052, including controlled IPv4/IPv6 allowlists, always-deny override, mapped addresses, firewall hooks after destination translation and isolation from host and control services.

**Environment and command.** Use a disposable native Linux host with a local rootful Docker Engine at `/var/run/docker.sock`, iproute2, nftables, util-linux, make and Python 3. Preload the image before entering the isolated namespaces. The workflow runs the same target on `ubuntu-24.04`.

```sh
docker pull python:3.13.12-slim-bookworm
sudo make spike-egress
```

**Harness.** Each unprivileged Docker fixture starts with `--network none`. Its workload refuses to probe before readiness. The host installs and reads back the IPv4/IPv6 nftables rules before attaching the only veth or admitting workload checks. Raw socket sentinels test denied paths across startup and attachment. The check verifies live allowed listeners, denied targets, conflicting allowlists and IPv4-mapped IPv6, with worker, gateway-input and post-DNAT drop counters. A protected service retains an exact peer/port control exception. The harness removes the first container, waits for its veth to disappear, and repeats the assertions with a fresh namespace and different IPv4 and IPv6 addresses. It uses an isolated router and disposable fixture processes. Its raw sockets bypass the application classifier by design so the kernel verdict is observable.

**Result — INCOMPLETE.** Bash syntax and the workflow passed local static checks. The native Linux job has yet to run. The synthetic router uses manually attached veth links and service stand-ins. A passing run applies to that topology. Verify the deployment's Compose bridge and firewall backend, Docker resolver, provider-only rules and policy version readiness separately. The narrow control exception remains reachable to the worker process by design. If target sockets must have zero access even to an approved control service port under an application fault, propose a separately constrained probe process with its own network boundary for owner review.

## 6. Worker Execution Guard

**Objective and acceptance.** Verify AD-014 and AC-031 using outbound dial evidence and target-observed socket lifetimes. Exercise duplicate delivery, scheduled/manual contention, lease expiry, DB loss, hard deadline, child crash, container replacement, stale persistence and pause.

**Environment and command.** Linux arm64 via Docker Desktop, PostgreSQL 17.9, RabbitMQ 4.2.5, Celery 5.6.3 with two prefork children, the pinned HTTPX transport and a controlled TLS server. Run `make spike-guard` after starting the disposable Compose project and building the spike runner. CI publishes `integration-spikes` and `linux-egress-spike` logs as artifacts.

**Observed.** Duplicate and manual contenders remained busy after lease expiry and termination of the active PostgreSQL backend. RabbitMQ redelivered the killed child's single published message with `redelivered=True` and delivery count 1. The worker confirmed the previous child incarnation had gone before retiring the interrupted attempt. A separate TLS request committed in a replacement PostgreSQL session after backend termination. Old-token and same-token post-settlement writes were rejected. A non-cooperative TLS phase remained open at the soft deadline and ended at the hard deadline. The successor verified the exact previous owner had exited before dialing.

Docker confirmed the old private-PID-namespace container had exited with status 137 and PID 0. The new generation refused a job until the host-confirmed exit proof was supplied, then dialed with the same lock device/inode (`65025:1143127`). The base check-worker and API also shared a separate test inode and could acquire it only after the holder exited. The replacement worker stopped cleanly after settlement. The execution and start locks depend on the same stable, host-local named volume. Removing the lock files, replacing that volume or moving the worker to another host invalidates inode identity. Keep the volume and lock paths stable and require verified quiescence before replacing either. The spike uses a host-driven exit marker on disposable storage. Production needs a trusted host-managed proof tied to the identified generation and its descendants.

Pause timed out while dial and initial write were held, without committing a paused state. It committed after the request write. A subsequent delivered job had neither a client dial nor a target connection. PostgreSQL recorded five successful results and three interrupted attempts.

| Target observation | TCP accept to TLS close, seconds from first accept |
|---|---:|
| Scheduled, lease expiry and child crash | 0.000000–0.814937 |
| After child crash | 0.909678–0.951843 |
| PostgreSQL reconnect | 0.991230–1.046621 |
| Hard deadline | 1.083075–13.073571 |
| After hard deadline | 13.148611–13.190775 |
| Old worker generation | 13.203766–13.368385 |
| New worker generation | 17.606358–17.650073 |
| Pause race | 17.852470–18.093865 |

The maximum was **one active socket** for the tested monitor over all eight connections. The measured hard-deadline socket lifetime was **11.990496 seconds**. These are target observations from the monotonic trace, including pre-HTTP connection time.

**Result — INCOMPLETE.** The Celery/TLS/PostgreSQL experiment passed locally. The approved gate also requires the verified native Linux deployment arrangement and the outbound egress gate. Native CI has yet to run. Stage 04 remains in progress pending those results and owner approval.
