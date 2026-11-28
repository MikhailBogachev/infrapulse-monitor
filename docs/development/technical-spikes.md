# IP-007 technical spike reports

IP-007 and Stage 04 are **COMPLETED AND APPROVED**. Stage 05 is **PENDING**. All six [architecture verification gates](../architecture/system-architecture.md#verification-gates) passed in their documented experiment environments. All experiments use synthetic endpoints, data and credentials. The spike image and Compose profile are separate from the backend runtime image.

## Approved CI evidence

**Mandatory CI verification — PASS. Runtime evidence review — PASS.** The owner accepted the Spike 5 and Spike 6 runtime evidence. [GitHub Actions run 46114848041](https://github.com/MikhailBogachev/infrapulse-monitor/actions/runs/46114848041) concluded with `success` on 2026-11-28. The native Linux runner used Ubuntu 24.04.5 LTS. The PR head was `194143150dacfb0b847c7fb4da6367d8c32fd5c5`. CI checked out the PR merge SHA `85397394e68e35644badbaec7419731181d9365a`.

| Job | Result |
|---|---|
| [Backend · 140886238998](https://github.com/MikhailBogachev/infrapulse-monitor/actions/runs/46114848041/job/140886238998) | PASS |
| [Frontend · 140886238951](https://github.com/MikhailBogachev/infrapulse-monitor/actions/runs/46114848041/job/140886238951) | PASS |
| [Integration · 140886238908](https://github.com/MikhailBogachev/infrapulse-monitor/actions/runs/46114848041/job/140886238908) | PASS |
| [Linux Compose Topology · 140886238735](https://github.com/MikhailBogachev/infrapulse-monitor/actions/runs/46114848041/job/140886238735) | PASS |
| [Linux Egress Fixture · 140886238874](https://github.com/MikhailBogachev/infrapulse-monitor/actions/runs/46114848041/job/140886238874) | PASS |

**Evidence artifacts.** [linux-egress-spike · 15250079409](https://github.com/MikhailBogachev/infrapulse-monitor/actions/runs/46114848041/artifacts/15250079409) and [linux-compose-topology · 15251049015](https://github.com/MikhailBogachev/infrapulse-monitor/actions/runs/46114848041/artifacts/15251049015).

The approved run applies to the PR head recorded above. CI verification for the final acceptance commit is pending.

**Non-blocking CI technical debt.** The runner warned that `actions/upload-artifact` targets the deprecated Node.js 20 runtime and ran the action on Node.js 24. Both artifacts uploaded successfully. Updating the action is deferred.

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

**Result — PASS.** The local toolchain, Linux containers and synthetic compatibility checks passed on the tested matrix. The [approved CI run](#approved-ci-evidence) records GitHub Actions execution for AC-057. Initial migration verification covers the foundation revision.

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

**Result — PASS.** The candidate relies on pinned private HTTPX/httpcore interfaces. Re-run the experiment on upgrades. The full production URL policy and its integration with the production execution guard and Linux enforcement remain implementation and verification work.

## 5. IPv4/IPv6 Egress Enforcement

**Objective and acceptance.** Prove AD-013 and AD-015 on Linux under AC-051 and AC-052, including controlled IPv4/IPv6 allowlists, always-deny override, mapped addresses, firewall hooks after destination translation and isolation from host and control services.

**Environment and command.** Use a disposable native Linux host with a local rootful Docker Engine at `/var/run/docker.sock`, iproute2, nftables, util-linux, make and Python 3. Preload the image before entering the isolated namespaces. The workflow runs the same target on `ubuntu-24.04`.

```sh
docker pull python:3.13.12-slim-bookworm
sudo make spike-egress
```

**Synthetic harness.** Each unprivileged Docker fixture starts with `--network none`. The host validates and installs the IPv4/IPv6 rules before attaching its veth or admitting workload checks. The isolated router keeps its gateway addresses and listeners for both worker generations. Each foreground fixture owns all its sockets and reports startup, readiness, bind errors and shutdown with its PID, network namespace and run-specific identity. Readiness checks validate the exact listener identity. The harness reaps its processes and checks that the first worker's veth disappears before attaching the second worker. GitHub Actions runs the experiment twice on the same Linux runner in fresh mount and network namespaces and records separate logs.

**CI evidence.** In [run 45999938375](https://github.com/MikhailBogachev/infrapulse-monitor/actions/runs/45999938375), backend, frontend and integration passed. On Ubuntu 24.04.5 with nftables 1.0.9, the corrected rulesets installed and the first synthetic worker passed the dual-stack, mapped IPv6, host, post-DNAT, service-exception and startup checks. The replacement reached policy readiness, then both gateway listeners failed to bind port 18080 with `EADDRINUSE`. Readiness subsequently failed at `10.70.0.1:18080`.

**Cause and correction.** The old harness terminated and waited for the sole gateway process before attempting to bind the same address/port pairs in the same network namespace. The server initiated TCP close after sending the readiness payload. On Linux, a controlled replay on both address families reproduced error 98 after the listener process had exited and been reaped. The same-port entries in `/proc/net/tcp` and `tcp6` were `TIME_WAIT` with socket inode zero. The historical CI run did not capture socket-state snapshots. Keeping the gateway listeners alive avoids rebinding through those residual connections. Bind failures in the foreground now fail the process, dump relevant TCP states and close all sockets acquired during startup. The lifecycle regression also checks dual-stack identity, graceful exit and cleanup after a partial bind failure.

**CI evidence from [run 46099421887](https://github.com/MikhailBogachev/infrapulse-monitor/actions/runs/46099421887).** Backend, frontend and integration passed. In [Linux Egress Fixture](https://github.com/MikhailBogachev/infrapulse-monitor/actions/runs/46099421887/job/140838229419), generation 1 passed IPv4, IPv6 and mapped IPv6, service exceptions, host blocking and post-DNAT filtering. It recorded 54 refusal sweeps, including 18 after attachment, and gateway counters of 38 `host_drops`, 19 `translated_v4` and 18 `translated_v6` packets. Docker confirmed a graceful exit with code 0. Generation 2 acquired its own addresses and policy readiness. The original gateway listeners still answered over both address families. The replacement assertion stopped coverage because both generations reported `net:[4026532513]` despite distinct container IDs and host PIDs. The runner did not reach the second sequential invocation.

**Generation verification.** Linux recycles network namespace inode numbers after teardown. A separate component experiment in the Docker Desktop Linux VM observed reuse after a foreground namespace owner exited. The CI fixture used a private Docker sandbox and PID namespace for each worker. Its namespace lookups and `nsenter` commands held no persistent namespace descriptor, and the harness created no namespace bind mount for a worker. The historical logs show removal and disappearance of the old veth before replacement. They contain no live snapshot of Docker's mount and descriptor state. The verifier now requires Docker exit status and removal, disappearance of the old PID/start-time identity and attachment, and a distinct container ID with a live process identity. The replacement must start without a fixture policy table or readiness marker. It receives a marker tied to its full container ID only after installation, attachment and live ruleset verification. The verifier repeats the policy and process checks before coverage. Keeping a namespace descriptor open across replacement would prolong namespace and veth lifetime.

**Supported Compose topology.** On the disposable Linux host, run `sudo make spike-topology`. The verifier requires rootful Docker Engine with cgroup v2, Compose supporting `!override`, IPv6 bridges, nftables, iproute2, conntrack, util-linux, OpenSSL, curl and Python 3. It creates a fresh project with the base Compose services and a test overlay. The overlay enables dual-stack control, check and provider bridges, controlled TLS/DNS targets and real Nginx publication. The host checks nftables rules before installation, quarantines both worker addresses before startup, and validates each live ruleset before authorizing the generation. The Compose job publishes diagnostics separately from the synthetic job.

**Compose failure in [run 46099421887](https://github.com/MikhailBogachev/infrapulse-monitor/actions/runs/46099421887/job/140838229465).** The images and dependencies started, API and Nginx reported healthy, and both worker gates admitted policy revision `ip007-compose-v1` after the policy refusal checks. Quarantine was removed. Both workers remained unhealthy, and the 35-second wait for `worker-checks` to become healthy expired before coverage or guard replacement. The Docker resolver accepted queries, but the worker output chain dropped its loopback replies before reverse NAT. This prevented Celery from resolving the broker and reaching its ready signal. A controlled component replay in Docker Desktop reproduced UDP and TCP DNS timeouts with the original rules. The corrected rules accepted conntrack replies only for the DNATed Docker resolver flow, resolved the controlled peer over both protocols and still blocked unrelated live loopback listeners. Coverage now checks both service names over UDP and TCP, resolver reply counters, and loopback denial with live listeners. A readiness failure records Docker health and process state, policy state, routes, sockets, firewall counters, service probes and redacted logs before cleanup.

**Native Linux Synthetic Egress Fixture — PASS in [run 46110368724](https://github.com/MikhailBogachev/infrapulse-monitor/actions/runs/46110368724/job/140872321858).** Both sequential invocations on the same runner passed. Each covered two worker generations and reported 38 host drops, 19 translated IPv4 packets and 19 translated IPv6 packets per generation. All four generations exited with status 0 and the fixtures were reaped. The earlier nftables syntax, listener lifecycle, TIME_WAIT and reused namespace identifier failures did not recur.

**Supported Compose evidence from [run 46110368724](https://github.com/MikhailBogachev/infrapulse-monitor/actions/runs/46110368724/job/140872321824).** Backend, frontend, integration and Linux Egress Fixture passed in the same run. On Docker Engine 28.0.4, Compose verified startup quarantine, missing and stale policy, rejection of modified live rules, both workers' readiness, IPv4 and IPv6 PostgreSQL and RabbitMQ access, allowed native and mapped targets, Docker UDP and TCP DNS, denial of alternate resolvers and loopback, provider-only HTTPS and HTTP target rejection before dial. The Nginx publication responded from the host over both families. Both worker probes to the publication failed to connect, but `published_v4` and `published_v6` were zero. The live host listener on port 18081 was blocked with one packet per family (60 IPv4 bytes and 80 IPv6 bytes). The assertion stopped the job before the prefork recreation sequence.

**Packet path.** A controlled replay with Docker Engine 28.0.4 in an isolated Docker Desktop Linux environment traced both worker SYNs through NAT PREROUTING to the Docker chain. The `ip007-check` ingress rule returned before the per-port DNAT rule. Each packet kept the check bridge's host gateway and port 18080 as its destination. The host INPUT hook dropped it before the listening `docker-proxy` socket. Neither worker SYN took FORWARD or reached the Nginx edge bridge. The versioned [Docker bridge rules](https://github.com/moby/moby/blob/v28.0.4/libnetwork/drivers/bridge/setup_ip_tables_linux.go#L410-L429) document this ingress exclusion and the relation to cross-bridge isolation.

**Compose regression.** The real workers still verify gateway and host listener blocking. A separate test client in a disposable namespace reaches the same dual-stack Nginx publication over a routed veth outside Docker's bridges. It uses the stock Docker DNAT rules. The host traces the fixture SYNs at PREROUTING priority -110, ahead of DNAT at -100, and checks the translated destination and full original/reply TCP tuples in FORWARD at -5, ahead of Docker's filter priority. The permitted control must return HTTP success through Nginx, increment the translated-control counter and reach Nginx's input hook. The forbidden probe must increment both its pre-DNAT ingress and post-DNAT drop counters and leave the Nginx SYN counter unchanged. Source ports differ by verdict and address family. The job snapshots Docker NAT, filter, listener and control-flow conntrack state, and saves the bounded trace and redacted logs before teardown.

**Isolated Docker Desktop replay.** With rootful Engine 28.0.4, both host listener counters increased and both worker publication probes hit INPUT. Both routed controls returned the application's live response and delivered one SYN each to Nginx. The forbidden IPv4 and IPv6 flows each incremented the matching pre-DNAT and translated FORWARD drop counters by one. Both Nginx SYN counters stayed at one. Conntrack recorded the gateway on port 18080 in each control's original tuple and the Nginx edge address on port 8080 in its reply tuple.

**Control-plane boundary — COMPLIANT with the approved design.** [AD-015](../project/decision-register.md#ad-015) requires application destination verification and host-managed egress restrictions. The [deployment design](../architecture/deployment-design.md#restricted-egress) explicitly permits exact DB and broker peers and ports and the designated resolver as worker capabilities. [NFR-010](../product/srs.md#nfr-010), [AC-051](../product/acceptance-criteria.md#ac-051) and [AC-052](../product/acceptance-criteria.md#ac-052) require every HTTP check path to reject these protected destinations even with a conflicting allowance and to demonstrate the effective destination of every actual target connection. The approved boundary uses application policy to distinguish target dials from legitimate use of the exact service tuples. Independent network isolation of HTTP check operations from those tuples would require an additional approved architecture decision.

**Approved native Linux Synthetic Egress Fixture — PASS.** Two consecutive invocations each exercised two worker generations. All four generations exited with code 0. The runs verified IPv4, IPv6 and IPv4-mapped IPv6 filtering, default-deny and always-deny, loopback and host access blocking, post-DNAT filtering, narrow service exceptions, fail-closed startup and worker recreation. The fixture handled namespace identifier reuse and confirmed listener lifecycle and repeatability. See the [Linux Egress Fixture job](https://github.com/MikhailBogachev/infrapulse-monitor/actions/runs/46114848041/job/140886238874).

| Run | Generation | Startup refusal sweeps | After attachment |
|---|---|---:|---:|
| 1 | 1 | 58 | 17 |
| 1 | 2 | 61 | 18 |
| 2 | 1 | 59 | 17 |
| 2 | 2 | 61 | 18 |
| **Total** | | **239** | **70** |

**Approved native Linux Compose Topology — PASS.** The job verified startup quarantine, refusal of missing, stale and drifted policy, live policy verification, and worker readiness. It exercised PostgreSQL and RabbitMQ over IPv4 and IPv6, permitted IPv4, IPv6 and mapped targets, Docker resolver UDP and TCP, third-party DNS denial, loopback isolation, provider-only HTTPS, HTTP target rejection before dial, host and published-port blocking, and worker recreation. See the [Linux Compose Topology job](https://github.com/MikhailBogachev/infrapulse-monitor/actions/runs/46114848041/job/140886238735).

The worker probes to the host listener and published port were blocked at host INPUT. The separate routed-veth client exercised actual Docker DNAT. Its allowed control reached Nginx over both address families. Each forbidden SYN crossed the ingress observation point and was dropped in FORWARD after translation. The Nginx SYN counters stayed at one after the forbidden probes.

| Path | IPv4 counter | IPv6 counter | Packets |
|---|---|---|---|
| Routed-veth ingress before DNAT | `ingress_v4` | `ingress_v6` | 0 → 1 |
| Routed-veth drop after DNAT | `published_v4` | `published_v6` | 0 → 1 |
| Nginx SYNs before control, after control and after forbidden probe | `received_v4` | `received_v6` | 0 → 1 → 1 |
| Worker host-listener and published-port denials at INPUT | `host_v4` | `host_v6` | 0 → 1 → 2 |

**Result — PASS.** The synthetic fixture and supported Compose topology passed on native Linux. Production host policy provisioning and end-to-end egress verification for supported application paths remain required under AD-013 and AD-015.

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

**CI evidence.** Integration passed on Linux x86_64 in run 45990753293. The controlled target observed eight TLS connections, at most **one simultaneous connection** and a **11.998870-second** hard-deadline connection lifetime. The fixture confirmed old-container exit and preserved the lock inode across worker generation replacement. Redelivery, PostgreSQL reconnect, stale result rejection and the Pause guard also passed.

**Supported topology scenario.** The Linux Compose job runs the existing check queue with a synthetic task in a real prefork child. It holds a target-observed TLS socket and both shared locks. The host records the full container ID, private PID namespace, cgroup v2 membership and process start times, including the child that opened the connection. It reads process leaders from `cgroup.threads`, which also supports threaded cgroups. It confirms Docker exit, empty or removed cgroup, disappearance of the recorded process identities and target-observed closure. The successor refuses stale or missing policy and refuses valid current policy with missing or mismatched exit proof. After the host publishes the matching proof, the target observes the successor's first request and the API and both worker generations report matching lock device/inode pairs.

**Isolated Docker Desktop replay.** The Compose guard captured four processes, including the lock owner, verified exit status 137 and removal of the old cgroup, and observed the old socket close. It rejected stale and missing policy and missing and mismatched generation proof without a dial. After host admission, the successor completed its check. The API and both generations reported matching execution and start lock identities. The old target connection closed before the successor connected.

**Approved native Linux Compose lifecycle — PASS.** The host confirmed that the exact previous generation `77c30176e9c4` (host PID `6325`) and all five recorded processes had stopped. Its cgroup v2 was removed. The successor was `9c4b764f468c` (host PID `10428`). Both shared lock identities were preserved (execution `66305:4791818`, start `66305:4791819`). The successor refused missing and stale policy and missing and incorrect termination proof. It accepted the matching generation proof and completed a new outbound check. See the [Linux Compose Topology job](https://github.com/MikhailBogachev/infrapulse-monitor/actions/runs/46114848041/job/140886238735).

| TLS fixture event | Monotonic time (ns) |
|---|---:|
| Old accept | 148862778372 |
| Old close | 149621708396 |
| New dial | 167776695926 |
| New accept | 167778710513 |
| New close | 167781339390 |

The old connection closed before the new dial. The time from old close to new accept was approximately 18.157 seconds. These two outbound connections did not overlap.

**Result — PASS.** The approved run passed the integration and native Linux Compose lifecycle checks. Production implementation and verification of the worker execution guard, including trusted host-managed termination proof and integration with the production transport and policy, remain required under AD-014.
