# Decision Register
ID: IP-DOC-006 | Version: 1.0 | Status: Active

## Approved Stage 00 decisions

| ID | Decision |
|---|---|
| <a id="d-001"></a> D-001 | InfraPulse working name; infrapulse-monitor monorepo |
| <a id="d-002"></a> D-002 | Open-source self-hosted product; intended MIT license |
| <a id="d-003"></a> D-003 | Modular monolith with background workers |
| <a id="d-004"></a> D-004 | FastAPI, PostgreSQL, RabbitMQ, Celery, Redis, React, Docker and Docker Compose baseline |
| <a id="d-005"></a> D-005 | MVP → Beta → v1.0.0 release boundaries, including CI for MVP and Prometheus and Grafana for v1.0.0 |
| <a id="d-006"></a> D-006 | English repository and UI; Russian discussions |
| <a id="d-007"></a> D-007 | GitHub Flow, issues, PRs, ADRs, tests, CI |
| <a id="d-008"></a> D-008 | Eight-week indicative roadmap for InfraPulse |
| <a id="d-009"></a> D-009 | Owner approval and review, ChatGPT design support and Codex CLI as the current development assistant interface |

Under D-009, repository documentation is the primary source of project context. Codex CLI uses the read-only sandbox for analysis and the workspace-write sandbox for approved edits. Task scope changes require human approval. Commits and merges require prior human review. Automatic pushes to remote repositories are prohibited. See the [development workflow](../development/workflow.md).

## Approved technology decisions after Stage 00

| ID | Title | Status | Decision owner | Target release |
|---|---|---|---|---|
| <a id="d-010"></a> D-010 | GitHub Actions for MVP CI | APPROVED | Project owner | MVP v0.1.0 |

**Context.** [D-005](#d-005) established CI as part of MVP. GitHub Actions entered Stage 00 as a technology candidate.

**Decision.** GitHub Actions is required for InfraPulse MVP CI. Execute the required MVP automated tests and quality checks in GitHub Actions and use verifiable execution results as acceptance evidence.

**Approval source.** The project owner explicitly approved the platform in IP-003-R2.

**Rationale.** Selecting a platform gives reviewers a single required source of CI execution evidence and aligns with the GitHub Flow established in [D-007](#d-007).

**Scope.** Continuous integration, automated quality checks and tests within approved MVP scope, and observable GitHub Actions execution. The current technology dispositions are in the [approved stack](../architecture/technology-stack.md).

**Deferred implementation details.** Workflow structure, job decomposition, triggers, runner operating systems and architectures, dependency caching, matrices, branch protection, required check names, artifact retention, deployment workflows, release automation, and versions of actions and quality or test tools remain unapproved. The detailed Stage 07 measurement protocol is deferred under [Q-11](../product/prd.md#q-11).

**Related decisions and requirements.** [D-005](#d-005), [D-007](#d-007), [F-012](../product/prd.md#f-012), [NFR-015](../product/srs.md#nfr-015), [AC-057](../product/acceptance-criteria.md#ac-057).

## Approved Stage 02 Architecture Decisions

The project owner approved AD-001–AD-012 and the [technology stack](../architecture/technology-stack.md) in the IP-005 brief. These supersede the corresponding candidate and pending architecture entries in the Stage 00 charter. In IP-005 Final Acceptance the owner approved the architecture documentation and AD-013–AD-016, completing Stage 02. Exact dependency versions and mandatory technical verification are deferred to [Stage 04](../architecture/system-architecture.md#verification-gates).

| ID | Approved decision | Record |
|---|---|---|
| <a id="ad-001"></a> AD-001 | Modular Monolith | [ADR-001](../architecture/adr/adr-001-modular-runtime.md) |
| <a id="ad-002"></a> AD-002 | Execution and Concurrency Model | [ADR-001](../architecture/adr/adr-001-modular-runtime.md) |
| <a id="ad-003"></a> AD-003 | Database Architecture | [ADR-002](../architecture/adr/adr-002-postgresql-history.md) |
| <a id="ad-004"></a> AD-004 | REST API Architecture | [ADR-004](../architecture/adr/adr-004-http-identity-and-spa.md) |
| <a id="ad-005"></a> AD-005 | Authentication and Workspace Isolation | [ADR-004](../architecture/adr/adr-004-http-identity-and-spa.md) |
| <a id="ad-006"></a> AD-006 | Monitoring Engine | [ADR-003](../architecture/adr/adr-003-background-processing.md) |
| <a id="ad-007"></a> AD-007 | Reliability and Message Processing | [ADR-003](../architecture/adr/adr-003-background-processing.md) |
| <a id="ad-008"></a> AD-008 | Incident Engine | [ADR-003](../architecture/adr/adr-003-background-processing.md) |
| <a id="ad-009"></a> AD-009 | Notification Engine | [ADR-003](../architecture/adr/adr-003-background-processing.md) |
| <a id="ad-010"></a> AD-010 | Security Architecture | [ADR-005](../architecture/adr/adr-005-outbound-and-deployment.md) |
| <a id="ad-011"></a> AD-011 | Frontend Architecture | [ADR-004](../architecture/adr/adr-004-http-identity-and-spa.md) |
| <a id="ad-012"></a> AD-012 | Deployment and Infrastructure | [ADR-005](../architecture/adr/adr-005-outbound-and-deployment.md) |
| <a id="ad-013"></a> AD-013 | Linux Deployment Environment · APPROVED. Production uses Linux, Docker Engine and Docker Compose. Local development uses macOS and Docker Desktop. Run production-specific network verification on Linux. | [ADR-005](../architecture/adr/adr-005-outbound-and-deployment.md#ad-013) |
| <a id="ad-014"></a> AD-014 | Check Worker Execution Guard · APPROVED. MVP uses one check-worker container with multiple prefork processes. A subsequent execution requires proof that the previous execution has ended. Lease expiry alone cannot authorize it. The mandatory Stage 04 execution guard spike remains pending. | [ADR-005](../architecture/adr/adr-005-outbound-and-deployment.md#ad-014) |
| <a id="ad-015"></a> AD-015 | Host-managed Network Egress · APPROVED. Combine application-level destination verification with Linux host-managed outbound restrictions. The mandatory Stage 04 IPv4/IPv6 egress spike remains pending. | [ADR-005](../architecture/adr/adr-005-outbound-and-deployment.md#ad-015) |
| <a id="ad-016"></a> AD-016 | Scheduler & Control Worker · APPROVED. Run Celery Beat and the control worker as separate processes in one scheduler container. Supervise lifecycle and failures, support graceful shutdown and enforce a single Beat instance. | [ADR-005](../architecture/adr/adr-005-outbound-and-deployment.md#ad-016) |

## Approved Product Decisions

IP-002 is approved. The product owner approved PD-001–PD-015 for IP-003. The approved IP-004 decisions below resolve the product parameters. IP-005 Final Acceptance adds PD-016 within the approved feature boundaries.

| ID | Title | Release | Status | Approved scope |
|---|---|---|---|---|
| <a id="pd-001"></a> PD-001 | Configurable Registration | MVP; invitations in Beta | APPROVED | The installation operator can enable or disable public registration. Public signup is disabled by default after initial setup. The first account has a separate operator-authorized bootstrap path. Workspace ownership does not confer installation authority. Team invitations are Beta. |
| <a id="pd-002"></a> PD-002 | HTTP Methods | MVP | APPROVED | HTTP and HTTPS monitors accept GET and HEAD. POST, PUT, PATCH, DELETE and arbitrary request bodies are outside MVP. GET is the default. |
| <a id="pd-003"></a> PD-003 | Monitoring Interval | MVP | APPROVED | The configurable minimum interval is 30 seconds. The default is 60 seconds. A 30-second interval for all 1,000 monitors carries no performance guarantee. |
| <a id="pd-004"></a> PD-004 | Incident Thresholds | MVP | APPROVED | Configurable opening and recovery thresholds default to three consecutive qualifying failures and two consecutive qualifying successes respectively. Internal platform faults do not establish target unavailability. |
| <a id="pd-005"></a> PD-005 | Manual Monitor Execution | MVP | APPROVED | Run Check Now is authorized, rate-limited, asynchronous, duplicate-safe, visible to the requester and retained in history. Q-03 establishes eligibility, cadence, metric exclusions and rate. |
| <a id="pd-006"></a> PD-006 | Network Security and SSRF | MVP baseline; inherited later | APPROVED | Eligible public HTTP and HTTPS targets are permitted. Private access is denied by default and only the installation operator may allow explicitly selected eligible internal destinations. Always-denied sensitive targets remain blocked. Apply policy to all actual connections across both address families, including DNS-based paths and redirect hops where supported. Protect credentials and restrict the demo to controlled targets. |
| <a id="pd-007"></a> PD-007 | Workspace Authorization | MVP and Beta | APPROVED | MVP isolates workspaces and provides scoped Owner authority. Beta adds invitations, membership management and role-based authorization. Q-07 approves the Owner, Admin, Member and Viewer matrix. Installation authority is separate. |
| <a id="pd-008"></a> PD-008 | UI Data Updates | MVP and Beta | APPROVED | MVP uses polling and Beta uses Server-Sent Events. Views distinguish loading, stale data, failed refresh and recovery. Q-12 approves MVP refresh and stale timing. |
| <a id="pd-009"></a> PD-009 | Additional Monitoring Types | Beta | APPROVED | Beta adds TCP, certificate expiry, HTTP keyword and JSON assertion monitoring. HTTP and HTTPS remain in MVP. User scripts, executable expressions, DNS, ICMP and heartbeat monitoring are outside scope. |
| <a id="pd-010"></a> PD-010 | Interactive Isolated Demo | v1.0.0 | APPROVED | The public demo is interactive and isolated, uses controlled synthetic targets, restricts network access, bounds resources, prevents scanning and real notification delivery, and has a reset and cleanup lifecycle. |
| <a id="pd-011"></a> PD-011 | Uptime and Latency | MVP and Beta | APPROVED | Uptime is qualifying successes divided by qualifying completed checks. Qualifying target failures and timeouts enter the denominator. Platform errors, skipped work, pauses and missing observations are distinguishable from unavailability. Latency uses qualifying successes. MVP includes basic metrics and Beta adds analytics. |
| <a id="pd-012"></a> PD-012 | Performance Measurement | MVP baseline; v1.0.0 release evidence | APPROVED | Use repeatable measurement. Baseline targets are 1,000 active monitors at 60 seconds, API p95 at most 200 ms under a defined load, backend coverage of at least 80% and 30 days of history. The 30-second profile is for capacity exploration. |
| <a id="pd-013"></a> PD-013 | Dark Theme Only | MVP; inherited later | APPROVED | All UI uses Dark Only with contrast, keyboard access, visible focus and status distinctions beyond color. Light and system themes, theme settings, pickers and automatic theme switching are outside scope. |
| <a id="pd-014"></a> PD-014 | Responsive Interface | MVP; inherited later | APPROVED | Use a desktop-first responsive web interface, preserving principal navigation, dashboard, monitor, incident and account journeys on mobile. Stage 03 defines breakpoints and layouts. Native mobile apps are outside scope. |
| <a id="pd-015"></a> PD-015 | English Language | MVP; inherited later | APPROVED | UI, repository documentation, source identifiers, technical messages and source comments use English. Discussions, Codex CLI tasks and Codex reports use Russian. Localization and multilingual UI are outside scope. |
| <a id="pd-016"></a> PD-016 | Changing Target of a Paused Monitor | MVP | APPROVED | Changing the checked URL of a PAUSED monitor keeps it PAUSED, closes any open incident as Configuration Changed, resets consecutive result counters and advances the configuration version. The edit starts no automatic check. A later Resume sets PENDING. This refines [Q-04](../product/prd.md#q-04). |

Approval source for [PD-016](#pd-016): explicit project-owner approval in IP-005 Final Acceptance.

## IP-004 Product Decisions

Approval source: explicit project-owner approval in the IP-004 task. The linked PRD entries record the approved behavior and deferred design details. The project owner confirmed final Stage 01 acceptance in the IP-005 brief.

| ID | Decision | Release | Status | Scope sources |
|---|---|---|---|---|
| [Q-01](../product/prd.md#q-01) | Registration and authentication | MVP | APPROVED | [PD-001](#pd-001) |
| [Q-02](../product/prd.md#q-02) | HTTP monitor configuration | MVP | APPROVED | [PD-002](#pd-002), [PD-003](#pd-003) |
| [Q-03](../product/prd.md#q-03) | Manual checks | MVP | APPROVED | [PD-005](#pd-005) |
| [Q-04](../product/prd.md#q-04) | Monitor lifecycle and incidents | MVP | APPROVED | [PD-004](#pd-004) |
| [Q-05](../product/prd.md#q-05) | Notifications | MVP | APPROVED | [D-005](#d-005) |
| [Q-06](../product/prd.md#q-06) | Uptime and latency | MVP; Beta aggregation | APPROVED | [PD-011](#pd-011) |
| [Q-07](../product/prd.md#q-07) | RBAC, workspaces and invitations | MVP and Beta | APPROVED | [PD-001](#pd-001), [PD-007](#pd-007) |
| [Q-08](../product/prd.md#q-08) | Data retention | MVP baseline | APPROVED | [D-005](#d-005), [PD-012](#pd-012) |
| [Q-09](../product/prd.md#q-09) | Additional monitor types | Beta | APPROVED | [PD-009](#pd-009) |
| [Q-10](../product/prd.md#q-10) | Network security and SSRF | MVP baseline; inherited later | APPROVED | [PD-006](#pd-006) |
| [Q-11](../product/prd.md#q-11) | Performance and quality | MVP targets; v1.0.0 release evidence | APPROVED | [PD-012](#pd-012) |
| [Q-12](../product/prd.md#q-12) | Data freshness | MVP and Beta | APPROVED | [PD-008](#pd-008) |
| [Q-13](../product/prd.md#q-13) | Interactive demo | v1.0.0 | APPROVED | [PD-006](#pd-006), [PD-010](#pd-010) |
| [Q-14](../product/prd.md#q-14) | Accessibility and responsive design | MVP; inherited later | APPROVED | [PD-013](#pd-013), [PD-014](#pd-014), [PD-015](#pd-015) |
| [Q-15](../product/prd.md#q-15) | Beta and release contracts | Beta and v1.0.0 | APPROVED | [D-005](#d-005) |

## Other pending decisions

- Branding clearance.
