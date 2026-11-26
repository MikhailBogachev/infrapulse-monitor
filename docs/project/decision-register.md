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

## Proposed technology candidates

The [charter's candidate list](charter.md#proposed-technology-candidates) records technologies proposed for evaluation at later stage gates.

## Pending architectural decisions

- Dependency versions.
- Worker concurrency and asynchronous execution strategy.
- Database schema, partitioning and retention implementation.
- Use of a transactional outbox and delivery guarantees.
- API contracts and deployment provider.

Resolve these through subsequent stage gates and ADRs.

## Approved Product Decisions

IP-002 is approved. The product owner approved the following scope decisions for IP-003. Derived requirements await validation in IP-004. Values explicitly identified as proposed remain open.

| ID | Title | Release | Status | Approved scope and proposal boundaries |
|---|---|---|---|---|
| <a id="pd-001"></a> PD-001 | Configurable Registration | MVP; invitations in Beta | APPROVED | The installation operator can enable or disable public registration. Public signup is disabled by default after initial setup. The first account has a separate operator-authorized bootstrap path. Workspace ownership does not confer installation authority. Team invitations are Beta. |
| <a id="pd-002"></a> PD-002 | HTTP Methods | MVP | APPROVED | HTTP and HTTPS monitors accept GET and HEAD. POST, PUT, PATCH, DELETE and arbitrary request bodies are outside MVP. GET is the proposed default. |
| <a id="pd-003"></a> PD-003 | Monitoring Interval | MVP | APPROVED | The configurable minimum interval is 30 seconds. The proposed default is 60 seconds. A 30-second interval for all 1,000 monitors carries no performance guarantee. |
| <a id="pd-004"></a> PD-004 | Incident Thresholds | MVP | APPROVED | Configurable opening and recovery thresholds default to three consecutive qualifying failures and two consecutive qualifying successes respectively. Internal platform faults do not establish target unavailability. |
| <a id="pd-005"></a> PD-005 | Manual Monitor Execution | MVP | APPROVED | Run Check Now is authorized, rate-limited, asynchronous, duplicate-safe, visible to the requester and retained in history. Its lifecycle, scheduling and metric eligibility details require validation. |
| <a id="pd-006"></a> PD-006 | Network Security and SSRF | MVP baseline; inherited later | APPROVED | Eligible public HTTP and HTTPS targets are permitted. Private access is denied by default and only the installation operator may allow explicitly selected eligible internal destinations. Always-denied sensitive targets remain blocked. Apply policy to all actual connections and redirects, DNS and both address families. Protect credentials and restrict the demo to controlled targets. |
| <a id="pd-007"></a> PD-007 | Workspace Authorization | MVP and Beta | APPROVED | MVP isolates workspaces and provides scoped Owner authority. Beta adds invitations, membership management and role-based authorization. Owner, Admin, Member and Viewer permissions are candidates. Installation authority is separate. |
| <a id="pd-008"></a> PD-008 | UI Data Updates | MVP and Beta | APPROVED | MVP uses polling and Beta uses Server-Sent Events. Views distinguish loading, stale data, failed refresh and recovery. Refresh intervals and live-update operating details require validation. |
| <a id="pd-009"></a> PD-009 | Additional Monitoring Types | Beta | APPROVED | Beta adds TCP, certificate expiry, HTTP keyword and JSON assertion monitoring. HTTP and HTTPS remain in MVP. User scripts, executable expressions, DNS, ICMP and heartbeat monitoring are outside scope. |
| <a id="pd-010"></a> PD-010 | Interactive Isolated Demo | v1.0.0 | APPROVED | The public demo is interactive and isolated, uses controlled synthetic targets, restricts network access, bounds resources, prevents scanning and real notification delivery, and has a reset and cleanup lifecycle. |
| <a id="pd-011"></a> PD-011 | Uptime and Latency | MVP and Beta | APPROVED | Uptime is qualifying successes divided by qualifying completed checks. Qualifying target failures and timeouts enter the denominator. Platform errors, skipped work, pauses and missing observations are distinguishable from unavailability. Latency uses qualifying successes. MVP includes basic metrics and Beta adds analytics. |
| <a id="pd-012"></a> PD-012 | Performance Measurement | MVP baseline; v1.0.0 release evidence | APPROVED | Use repeatable measurement. Baseline targets are 1,000 active monitors at 60 seconds, API p95 at most 200 ms under a defined load, backend coverage of at least 80% and 30 days of history. The 30-second profile is for capacity exploration. |
| <a id="pd-013"></a> PD-013 | Dark Theme Only | MVP; inherited later | APPROVED | All UI uses Dark Only with contrast, keyboard access, visible focus and status distinctions beyond color. Light and system themes, theme settings, pickers and automatic theme switching are outside scope. |
| <a id="pd-014"></a> PD-014 | Responsive Interface | MVP; inherited later | APPROVED | Use a desktop-first responsive web interface, preserving principal navigation, dashboard, monitor, incident and account journeys on mobile. Stage 03 defines breakpoints and layouts. Native mobile apps are outside scope. |
| <a id="pd-015"></a> PD-015 | English Language | MVP; inherited later | APPROVED | UI, repository documentation, source identifiers, technical messages and source comments use English. Discussions, Codex CLI tasks and Codex reports use Russian. Localization and multilingual UI are outside scope. |

## Product Discovery disposition

| Topic | Disposition | Pending details |
|---|---|---|
| Manual execution | Approved for MVP | Rate policy, collisions, paused behavior and calculation eligibility. |
| Incident and recovery thresholds | Configurability and 3/2 defaults resolved | Range, streak ordering and lifecycle edge cases. |
| Network targets and SSRF | Restrictive installation policy resolved | Exact classification, allowlist and port edges. |
| Workspace authorization | MVP ownership and Beta role-based scope resolved | Beta permissions, invitation and membership lifecycle. |
| Performance measurement | Targets and capacity distinction resolved | Reference workload, environment, coverage and pass inputs. |
| Uptime and latency | Observation eligibility and basic formulas resolved | Time windows, estimator, sample sizes, rounding and aggregation. |

Other pending product matters include bootstrap, HTTP defaults, retention boundaries, notification behavior, refresh tolerances, accessibility evidence, typed check details, Beta and release feature details and the demo lifecycle. The [PRD open questions](../product/prd.md#open-questions) record the owner validation agenda.

## Other pending decisions

- Branding clearance.
