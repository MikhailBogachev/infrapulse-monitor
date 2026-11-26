# InfraPulse User Stories

| Field | Value |
|---|---|
| Document Status | DRAFT — PENDING VALIDATION |
| Version | 0.1 |
| Responsible Role | Product Analyst |
| Related Project Stage | Stage 01 — Product Discovery |
| Project Task | IP-003 |
| Validation | IP-004, pending owner review |

## Release stories

Must, Should, Could and Won't use MoSCoW semantics within each target release. Priorities and derived stories are pending validation. Product-facing workflows are represented. Platform internals and test evidence remain in the SRS and backlog.

<a id="us-001"></a>
### US-001 — Establish the first account and control public signup

As an Installation Operator, I want to establish the first account and control public signup, so that I can decide who can register on my installation.

| Field | Value |
|---|---|
| Role | Installation Operator |
| Release | v0.1.0 MVP |
| Priority | Must |
| Features | [F-001](prd.md#f-001) |
| Functional requirements | [FR-001](srs.md#fr-001), [FR-002](srs.md#fr-002), [FR-003](srs.md#fr-003), [FR-004](srs.md#fr-004) |
| Other requirements | — |
| Business rules | [BR-001](business-rules.md#br-001), [BR-002](business-rules.md#br-002) |
| Acceptance criteria | [AC-001](acceptance-criteria.md#ac-001), [AC-002](acceptance-criteria.md#ac-002), [AC-003](acceptance-criteria.md#ac-003), [AC-004](acceptance-criteria.md#ac-004) |
| Dependencies | Initial setup for authenticated use |
| Status | DERIVED DRAFT |

<a id="us-002"></a>
### US-002 — Sign up when eligible and sign in, renew and end my session

As a Visitor or account holder, I want to sign up when eligible, sign in with JWT access, renew access using my refresh token and end my session securely.

| Field | Value |
|---|---|
| Role | Visitor or account holder |
| Release | v0.1.0 MVP |
| Priority | Must |
| Features | [F-001](prd.md#f-001) |
| Functional requirements | [FR-003](srs.md#fr-003), [FR-004](srs.md#fr-004), [FR-005](srs.md#fr-005), [FR-006](srs.md#fr-006), [FR-007](srs.md#fr-007) |
| Other requirements | — |
| Business rules | [BR-001](business-rules.md#br-001), [BR-003](business-rules.md#br-003) |
| Acceptance criteria | [AC-003](acceptance-criteria.md#ac-003), [AC-004](acceptance-criteria.md#ac-004), [AC-005](acceptance-criteria.md#ac-005), [AC-006](acceptance-criteria.md#ac-006), [AC-007](acceptance-criteria.md#ac-007) |
| Dependencies | Initial setup for authenticated use. Token and session parameters remain [Q-01](prd.md#q-01). |
| Status | DERIVED DRAFT |

<a id="us-003"></a>
### US-003 — Workspace isolation

As a Workspace Owner, I want to manage my workspace settings and see only authorized resources, so that my team's information remains private.

| Field | Value |
|---|---|
| Role | Workspace Owner |
| Release | v0.1.0 MVP |
| Priority | Must |
| Features | [F-002](prd.md#f-002) |
| Functional requirements | [FR-009](srs.md#fr-009), [FR-010](srs.md#fr-010) |
| Other requirements | [NFR-001](srs.md#nfr-001) |
| Business rules | [BR-004](business-rules.md#br-004), [BR-005](business-rules.md#br-005), [BR-022](business-rules.md#br-022) |
| Acceptance criteria | [AC-009](acceptance-criteria.md#ac-009), [AC-010](acceptance-criteria.md#ac-010), [AC-011](acceptance-criteria.md#ac-011) |
| Dependencies | [F-001](prd.md#f-001) |
| Status | DERIVED DRAFT |

<a id="us-004"></a>
### US-004 — Monitor CRUD

As a Workspace Owner, I want to create, inspect, edit, pause, resume and delete monitors, so that my configured monitoring matches the services I operate.

| Field | Value |
|---|---|
| Role | Workspace Owner |
| Release | v0.1.0 MVP |
| Priority | Must |
| Features | [F-003](prd.md#f-003) |
| Functional requirements | [FR-011](srs.md#fr-011), [FR-012](srs.md#fr-012), [FR-013](srs.md#fr-013), [FR-014](srs.md#fr-014), [FR-015](srs.md#fr-015) |
| Other requirements | — |
| Business rules | [BR-006](business-rules.md#br-006), [BR-009](business-rules.md#br-009), [BR-012](business-rules.md#br-012), [BR-019](business-rules.md#br-019), [BR-020](business-rules.md#br-020) |
| Acceptance criteria | [AC-012](acceptance-criteria.md#ac-012), [AC-013](acceptance-criteria.md#ac-013), [AC-014](acceptance-criteria.md#ac-014), [AC-015](acceptance-criteria.md#ac-015), [AC-016](acceptance-criteria.md#ac-016) |
| Dependencies | [F-002](prd.md#f-002). Pause covers recurring checks. Paused manual execution remains [Q-03](prd.md#q-03). |
| Status | DERIVED DRAFT |

<a id="us-005"></a>
### US-005 — HTTP/HTTPS checks

As a Backend Developer, I want to configure GET or HEAD checks with an expected response, so that I can verify that my API is reachable.

| Field | Value |
|---|---|
| Role | Backend Developer |
| Release | v0.1.0 MVP |
| Priority | Must |
| Features | [F-004](prd.md#f-004) |
| Functional requirements | [FR-016](srs.md#fr-016), [FR-017](srs.md#fr-017), [FR-018](srs.md#fr-018), [FR-019](srs.md#fr-019) |
| Other requirements | — |
| Business rules | [BR-006](business-rules.md#br-006), [BR-008](business-rules.md#br-008), [BR-013](business-rules.md#br-013) |
| Acceptance criteria | [AC-017](acceptance-criteria.md#ac-017), [AC-018](acceptance-criteria.md#ac-018), [AC-019](acceptance-criteria.md#ac-019), [AC-020](acceptance-criteria.md#ac-020) |
| Dependencies | [F-002](prd.md#f-002) |
| Status | DERIVED DRAFT |

<a id="us-006"></a>
### US-006 — Scheduler

As a DevOps Engineer, I want to configure a recurring check interval and see its results, so that I can detect outages without checking by hand.

| Field | Value |
|---|---|
| Role | DevOps Engineer |
| Release | v0.1.0 MVP |
| Priority | Must |
| Features | [F-005](prd.md#f-005) |
| Functional requirements | [FR-020](srs.md#fr-020), [FR-021](srs.md#fr-021), [FR-022](srs.md#fr-022) |
| Other requirements | — |
| Business rules | [BR-007](business-rules.md#br-007), [BR-009](business-rules.md#br-009) |
| Acceptance criteria | [AC-021](acceptance-criteria.md#ac-021), [AC-022](acceptance-criteria.md#ac-022), [AC-023](acceptance-criteria.md#ac-023) |
| Dependencies | [F-002](prd.md#f-002) |
| Status | DERIVED DRAFT |

<a id="us-007"></a>
### US-007 — Check history

As a Backend Developer, I want to review check outcomes, times and origins, so that I can investigate intermittent behavior.

| Field | Value |
|---|---|
| Role | Backend Developer |
| Release | v0.1.0 MVP |
| Priority | Must |
| Features | [F-007](prd.md#f-007) |
| Functional requirements | [FR-024](srs.md#fr-024), [FR-030](srs.md#fr-030), [FR-035](srs.md#fr-035) |
| Other requirements | [NFR-003](srs.md#nfr-003), [NFR-006](srs.md#nfr-006) |
| Business rules | [BR-008](business-rules.md#br-008), [BR-009](business-rules.md#br-009), [BR-010](business-rules.md#br-010), [BR-013](business-rules.md#br-013), [BR-014](business-rules.md#br-014), [BR-015](business-rules.md#br-015), [BR-016](business-rules.md#br-016), [BR-022](business-rules.md#br-022), [BR-023](business-rules.md#br-023) |
| Acceptance criteria | [AC-025](acceptance-criteria.md#ac-025), [AC-028](acceptance-criteria.md#ac-028), [AC-035](acceptance-criteria.md#ac-035), [AC-036](acceptance-criteria.md#ac-036), [AC-041](acceptance-criteria.md#ac-041) |
| Dependencies | [F-002](prd.md#f-002) |
| Status | DERIVED DRAFT |

<a id="us-008"></a>
### US-008 — Incidents

As a DevOps Engineer, I want to configure detection thresholds and inspect incident and recovery evidence, so that I can distinguish persistent failures from transient ones.

| Field | Value |
|---|---|
| Role | DevOps Engineer |
| Release | v0.1.0 MVP |
| Priority | Must |
| Features | [F-008](prd.md#f-008) |
| Functional requirements | [FR-031](srs.md#fr-031), [FR-032](srs.md#fr-032), [FR-033](srs.md#fr-033), [FR-034](srs.md#fr-034), [FR-035](srs.md#fr-035), [FR-036](srs.md#fr-036), [FR-037](srs.md#fr-037) |
| Other requirements | — |
| Business rules | [BR-006](business-rules.md#br-006), [BR-008](business-rules.md#br-008), [BR-012](business-rules.md#br-012), [BR-013](business-rules.md#br-013), [BR-014](business-rules.md#br-014), [BR-015](business-rules.md#br-015), [BR-016](business-rules.md#br-016), [BR-017](business-rules.md#br-017), [BR-019](business-rules.md#br-019), [BR-020](business-rules.md#br-020), [BR-021](business-rules.md#br-021), [BR-022](business-rules.md#br-022) |
| Acceptance criteria | [AC-037](acceptance-criteria.md#ac-037), [AC-038](acceptance-criteria.md#ac-038), [AC-039](acceptance-criteria.md#ac-039), [AC-040](acceptance-criteria.md#ac-040), [AC-041](acceptance-criteria.md#ac-041), [AC-042](acceptance-criteria.md#ac-042), [AC-043](acceptance-criteria.md#ac-043) |
| Dependencies | [F-002](prd.md#f-002) |
| Status | DERIVED DRAFT |

<a id="us-009"></a>
### US-009 — Telegram notifications

As a Workspace Owner, I want the configured Telegram recipient to receive alerts for permitted incident events and want delivery failures to be visible when the provider cannot deliver.

| Field | Value |
|---|---|
| Role | Workspace Owner |
| Release | v0.1.0 MVP |
| Priority | Must |
| Features | [F-009](prd.md#f-009) |
| Functional requirements | [FR-038](srs.md#fr-038), [FR-039](srs.md#fr-039), [FR-065](srs.md#fr-065), [FR-041](srs.md#fr-041) |
| Other requirements | [NFR-007](srs.md#nfr-007) |
| Business rules | [BR-017](business-rules.md#br-017), [BR-018](business-rules.md#br-018) |
| Acceptance criteria | [AC-044](acceptance-criteria.md#ac-044), [AC-045](acceptance-criteria.md#ac-045), [AC-046](acceptance-criteria.md#ac-046), [AC-097](acceptance-criteria.md#ac-097), [AC-048](acceptance-criteria.md#ac-048) |
| Dependencies | [F-002](prd.md#f-002). Verify delivery with a permitted event and controlled available provider. Default event preferences and delivery edges remain [Q-05](prd.md#q-05). |
| Status | DERIVED DRAFT |

<a id="us-010"></a>
### US-010 — Dashboard

As a Workspace Owner, I want to see current workspace status and its freshness in a responsive dashboard, so that I can triage issues from my primary device or phone.

| Field | Value |
|---|---|
| Role | Workspace Owner |
| Release | v0.1.0 MVP |
| Priority | Must |
| Features | [F-010](prd.md#f-010) |
| Functional requirements | [FR-040](srs.md#fr-040), [FR-041](srs.md#fr-041) |
| Other requirements | [NFR-027](srs.md#nfr-027), [NFR-028](srs.md#nfr-028), [NFR-029](srs.md#nfr-029), [NFR-030](srs.md#nfr-030), [NFR-031](srs.md#nfr-031) |
| Business rules | — |
| Acceptance criteria | [AC-047](acceptance-criteria.md#ac-047), [AC-048](acceptance-criteria.md#ac-048), [AC-091](acceptance-criteria.md#ac-091), [AC-092](acceptance-criteria.md#ac-092), [AC-093](acceptance-criteria.md#ac-093), [AC-094](acceptance-criteria.md#ac-094), [AC-095](acceptance-criteria.md#ac-095) |
| Dependencies | [F-002](prd.md#f-002). Polling cadence and freshness tolerances remain [Q-12](prd.md#q-12). |
| Status | DERIVED DRAFT |

<a id="us-011"></a>
### US-011 — SSRF protection and rate limiting

As an Installation Operator, I want to control eligible internal targets and keep forbidden destinations blocked, so that I can safely monitor authorized services.

| Field | Value |
|---|---|
| Role | Installation Operator |
| Release | v0.1.0 MVP |
| Priority | Must |
| Features | [F-011](prd.md#f-011) |
| Functional requirements | — |
| Other requirements | [NFR-008](srs.md#nfr-008), [NFR-009](srs.md#nfr-009), [NFR-010](srs.md#nfr-010), [NFR-011](srs.md#nfr-011), [NFR-012](srs.md#nfr-012) |
| Verification focus | This outcome is specified by operational or security requirements. |
| Business rules | [BR-005](business-rules.md#br-005), [BR-006](business-rules.md#br-006), [BR-022](business-rules.md#br-022) |
| Acceptance criteria | [AC-050](acceptance-criteria.md#ac-050), [AC-051](acceptance-criteria.md#ac-051), [AC-052](acceptance-criteria.md#ac-052), [AC-053](acceptance-criteria.md#ac-053), [AC-054](acceptance-criteria.md#ac-054) |
| Dependencies | [F-002](prd.md#f-002). Exact installation policy parameters remain [Q-10](prd.md#q-10). |
| Status | DERIVED DRAFT |

<a id="us-012"></a>
### US-012 — Docker Compose, migrations and CI

As an Installation Operator, I want to start and upgrade an installation using documented procedures, so that I can operate my own monitoring instance.

| Field | Value |
|---|---|
| Role | Installation Operator |
| Release | v0.1.0 MVP |
| Priority | Must |
| Features | [F-012](prd.md#f-012) |
| Functional requirements | — |
| Other requirements | [NFR-013](srs.md#nfr-013), [NFR-014](srs.md#nfr-014), [NFR-033](srs.md#nfr-033) |
| Verification focus | This outcome is specified by operational or security requirements. |
| Business rules | — |
| Acceptance criteria | [AC-055](acceptance-criteria.md#ac-055), [AC-056](acceptance-criteria.md#ac-056), [AC-100](acceptance-criteria.md#ac-100) |
| Dependencies | Supported host and documented prerequisites |
| Status | DERIVED DRAFT |

<a id="us-013"></a>
### US-013 — TCP checks

As a DevOps Engineer, I want to check TCP connection availability, so that I can detect when a listener is unreachable.

| Field | Value |
|---|---|
| Role | DevOps Engineer |
| Release | v0.5.0 Beta |
| Priority | Must |
| Features | [F-013](prd.md#f-013) |
| Functional requirements | [FR-043](srs.md#fr-043) |
| Other requirements | [NFR-022](srs.md#nfr-022) |
| Business rules | [BR-006](business-rules.md#br-006), [BR-022](business-rules.md#br-022) |
| Acceptance criteria | [AC-058](acceptance-criteria.md#ac-058), [AC-082](acceptance-criteria.md#ac-082) |
| Dependencies | [F-002](prd.md#f-002) |
| Status | DERIVED DRAFT |

<a id="us-014"></a>
### US-014 — SSL expiry

As a DevOps Engineer, I want to monitor remaining certificate lifetime, so that I can renew a certificate before it expires.

| Field | Value |
|---|---|
| Role | DevOps Engineer |
| Release | v0.5.0 Beta |
| Priority | Must |
| Features | [F-014](prd.md#f-014) |
| Functional requirements | [FR-044](srs.md#fr-044), [FR-045](srs.md#fr-045) |
| Other requirements | [NFR-022](srs.md#nfr-022) |
| Business rules | [BR-006](business-rules.md#br-006), [BR-022](business-rules.md#br-022) |
| Acceptance criteria | [AC-059](acceptance-criteria.md#ac-059), [AC-060](acceptance-criteria.md#ac-060), [AC-082](acceptance-criteria.md#ac-082) |
| Dependencies | [F-002](prd.md#f-002) |
| Status | DERIVED DRAFT |

<a id="us-015"></a>
### US-015 — Email

As a Workspace Owner, I want to configure email incident notifications, so that my team can receive alerts in its inbox.

| Field | Value |
|---|---|
| Role | Workspace Owner |
| Release | v0.5.0 Beta |
| Priority | Must |
| Features | [F-015](prd.md#f-015) |
| Functional requirements | [FR-046](srs.md#fr-046) |
| Other requirements | — |
| Business rules | [BR-017](business-rules.md#br-017) |
| Acceptance criteria | [AC-061](acceptance-criteria.md#ac-061) |
| Dependencies | [F-002](prd.md#f-002) |
| Status | DERIVED DRAFT |

<a id="us-016"></a>
### US-016 — Webhooks

As a Workspace Owner, I want to configure a permitted incident webhook, so that my team can consume incident events in its tools.

| Field | Value |
|---|---|
| Role | Workspace Owner |
| Release | v0.5.0 Beta |
| Priority | Must |
| Features | [F-016](prd.md#f-016) |
| Functional requirements | [FR-047](srs.md#fr-047) |
| Other requirements | — |
| Business rules | [BR-017](business-rules.md#br-017), [BR-022](business-rules.md#br-022) |
| Acceptance criteria | [AC-062](acceptance-criteria.md#ac-062) |
| Dependencies | [F-002](prd.md#f-002) |
| Status | DERIVED DRAFT |

<a id="us-017"></a>
### US-017 — RBAC

As a Workspace Owner, I want to assign workspace roles and have their boundaries enforced, so that teammates have appropriate access.

| Field | Value |
|---|---|
| Role | Workspace Owner |
| Release | v0.5.0 Beta |
| Priority | Must |
| Features | [F-017](prd.md#f-017) |
| Functional requirements | [FR-048](srs.md#fr-048), [FR-049](srs.md#fr-049) |
| Other requirements | — |
| Business rules | [BR-005](business-rules.md#br-005) |
| Acceptance criteria | [AC-063](acceptance-criteria.md#ac-063), [AC-064](acceptance-criteria.md#ac-064) |
| Dependencies | [F-002](prd.md#f-002) |
| Status | DERIVED DRAFT |

<a id="us-018"></a>
### US-018 — Uptime and latency analytics

As a Small Engineering Team member, I want to compare uptime and latency and see live updates, so that I can investigate changes across time and monitors.

| Field | Value |
|---|---|
| Role | Small Engineering Team member |
| Release | v0.5.0 Beta |
| Priority | Must |
| Features | [F-018](prd.md#f-018) |
| Functional requirements | [FR-042](srs.md#fr-042), [FR-052](srs.md#fr-052), [FR-066](srs.md#fr-066) |
| Other requirements | — |
| Business rules | [BR-024](business-rules.md#br-024), [BR-025](business-rules.md#br-025) |
| Acceptance criteria | [AC-049](acceptance-criteria.md#ac-049), [AC-067](acceptance-criteria.md#ac-067), [AC-098](acceptance-criteria.md#ac-098) |
| Dependencies | [F-002](prd.md#f-002), [F-007](prd.md#f-007). Comparison uses supported windows. Combined metrics are conditional on [Q-06](prd.md#q-06); live-update tolerances remain [Q-12](prd.md#q-12). |
| Status | DERIVED DRAFT |

<a id="us-019"></a>
### US-019 — Publish a status page

As a Workspace Owner, I want to publish the status of selected monitors, so that service users can see availability information.

| Field | Value |
|---|---|
| Role | Workspace Owner |
| Release | v0.5.0 Beta |
| Priority | Must |
| Features | [F-019](prd.md#f-019) |
| Functional requirements | [FR-053](srs.md#fr-053) |
| Other requirements | — |
| Business rules | [BR-004](business-rules.md#br-004) |
| Acceptance criteria | [AC-068](acceptance-criteria.md#ac-068) |
| Dependencies | [F-002](prd.md#f-002) |
| Status | DERIVED DRAFT |

<a id="us-020"></a>
### US-020 — Read public status

As a Public status visitor, I want to view published service status without signing in, so that I can tell whether a selected service has an incident.

| Field | Value |
|---|---|
| Role | Public status visitor |
| Release | v0.5.0 Beta |
| Priority | Must |
| Features | [F-019](prd.md#f-019) |
| Functional requirements | [FR-053](srs.md#fr-053) |
| Other requirements | — |
| Business rules | [BR-004](business-rules.md#br-004) |
| Acceptance criteria | [AC-068](acceptance-criteria.md#ac-068) |
| Dependencies | [F-002](prd.md#f-002) |
| Status | DERIVED DRAFT |

<a id="us-021"></a>
### US-021 — Maintenance windows

As a Workspace Owner, I want to schedule and inspect maintenance windows, so that I can communicate when maintenance is planned.

| Field | Value |
|---|---|
| Role | Workspace Owner |
| Release | v0.5.0 Beta |
| Priority | Must |
| Features | [F-020](prd.md#f-020) |
| Functional requirements | [FR-054](srs.md#fr-054) |
| Other requirements | — |
| Business rules | — |
| Acceptance criteria | [AC-069](acceptance-criteria.md#ac-069) |
| Dependencies | [F-002](prd.md#f-002). Maintenance effects on availability and latency remain [Q-15](prd.md#q-15). |
| Status | DERIVED DRAFT |

<a id="us-022"></a>
### US-022 — API keys

As a Workspace Owner, I want to create and revoke a scoped API key, so that I can control access for my automation.

| Field | Value |
|---|---|
| Role | Workspace Owner |
| Release | v0.5.0 Beta |
| Priority | Must |
| Features | [F-021](prd.md#f-021) |
| Functional requirements | [FR-055](srs.md#fr-055) |
| Other requirements | — |
| Business rules | [BR-005](business-rules.md#br-005) |
| Acceptance criteria | [AC-070](acceptance-criteria.md#ac-070) |
| Dependencies | [F-002](prd.md#f-002) |
| Status | DERIVED DRAFT |

<a id="us-023"></a>
### US-023 — Audit log

As a Workspace Owner, I want to inspect my workspace audit log, so that I can identify covered changes and their actors.

| Field | Value |
|---|---|
| Role | Workspace Owner |
| Release | v1.0.0 Release |
| Priority | Must |
| Features | [F-022](prd.md#f-022) |
| Functional requirements | [FR-056](srs.md#fr-056) |
| Other requirements | — |
| Business rules | [BR-004](business-rules.md#br-004) |
| Acceptance criteria | [AC-071](acceptance-criteria.md#ac-071) |
| Dependencies | [F-002](prd.md#f-002) |
| Status | DERIVED DRAFT |

<a id="us-024"></a>
### US-024 — Prometheus/Grafana

As an Installation Operator, I want to see system health through Prometheus and Grafana, so that I can diagnose the monitoring platform itself.

| Field | Value |
|---|---|
| Role | Installation Operator |
| Release | v1.0.0 Release |
| Priority | Must |
| Features | [F-023](prd.md#f-023) |
| Functional requirements | — |
| Other requirements | [NFR-016](srs.md#nfr-016) |
| Verification focus | This outcome is specified by operational or security requirements. |
| Business rules | — |
| Acceptance criteria | [AC-072](acceptance-criteria.md#ac-072) |
| Dependencies | [F-002](prd.md#f-002) |
| Status | DERIVED DRAFT |

<a id="us-025"></a>
### US-025 — Report export

As a Small Engineering Team member, I want to export an authorized monitoring report, so that I can share measurements with my team.

| Field | Value |
|---|---|
| Role | Small Engineering Team member |
| Release | v1.0.0 Release |
| Priority | Must |
| Features | [F-024](prd.md#f-024) |
| Functional requirements | [FR-057](srs.md#fr-057) |
| Other requirements | — |
| Business rules | [BR-004](business-rules.md#br-004) |
| Acceptance criteria | [AC-073](acceptance-criteria.md#ac-073) |
| Dependencies | [F-002](prd.md#f-002) |
| Status | DERIVED DRAFT |

<a id="us-026"></a>
### US-026 — Demo mode

As a Public demo visitor, I want to try monitoring and incident workflows with synthetic targets, so that I can evaluate the product safely.

| Field | Value |
|---|---|
| Role | Public demo visitor |
| Release | v1.0.0 Release |
| Priority | Must |
| Features | [F-025](prd.md#f-025) |
| Functional requirements | [FR-058](srs.md#fr-058) |
| Other requirements | [NFR-017](srs.md#nfr-017) |
| Business rules | [BR-022](business-rules.md#br-022), [BR-026](business-rules.md#br-026) |
| Acceptance criteria | [AC-074](acceptance-criteria.md#ac-074), [AC-075](acceptance-criteria.md#ac-075) |
| Dependencies | Controlled synthetic targets and isolated sessions |
| Status | DERIVED DRAFT |

<a id="us-027"></a>
### US-027 — Public demo deployment

As a Public demo visitor, I want to use a clean isolated demo session, so that my actions and data do not affect other visitors or installations.

| Field | Value |
|---|---|
| Role | Public demo visitor |
| Release | v1.0.0 Release |
| Priority | Must |
| Features | [F-027](prd.md#f-027) |
| Functional requirements | — |
| Other requirements | [NFR-017](srs.md#nfr-017), [NFR-018](srs.md#nfr-018), [NFR-019](srs.md#nfr-019) |
| Verification focus | This outcome is specified by operational or security requirements. |
| Business rules | [BR-004](business-rules.md#br-004), [BR-022](business-rules.md#br-022), [BR-023](business-rules.md#br-023), [BR-026](business-rules.md#br-026) |
| Acceptance criteria | [AC-075](acceptance-criteria.md#ac-075), [AC-076](acceptance-criteria.md#ac-076), [AC-077](acceptance-criteria.md#ac-077) |
| Dependencies | [F-025](prd.md#f-025), [F-011](prd.md#f-011). Reset or expiry requires verified cleanup of the validated data scope under [Q-13](prd.md#q-13). |
| Status | DERIVED DRAFT |

<a id="us-028"></a>
### US-028 — Documentation

As an Installation Operator, I want to follow English installation and operation documentation, so that I can run and maintain the product independently.

| Field | Value |
|---|---|
| Role | Installation Operator |
| Release | v1.0.0 Release |
| Priority | Must |
| Features | [F-028](prd.md#f-028) |
| Functional requirements | — |
| Other requirements | [NFR-021](srs.md#nfr-021) |
| Verification focus | This outcome is specified by operational or security requirements. |
| Business rules | — |
| Acceptance criteria | [AC-079](acceptance-criteria.md#ac-079) |
| Dependencies | Verified release setup and operating behavior |
| Status | DERIVED DRAFT |

<a id="us-029"></a>
### US-029 — Run Check Now

As a Workspace Owner, I want to request an immediate authorized check and inspect its progress and result, so that I can verify a suspected change without waiting for the next due check.

| Field | Value |
|---|---|
| Role | Workspace Owner |
| Release | v0.1.0 MVP |
| Priority | Must |
| Features | [F-029](prd.md#f-029) |
| Functional requirements | [FR-023](srs.md#fr-023), [FR-024](srs.md#fr-024), [FR-025](srs.md#fr-025), [FR-026](srs.md#fr-026), [FR-027](srs.md#fr-027), [FR-028](srs.md#fr-028), [FR-029](srs.md#fr-029) |
| Other requirements | [NFR-005](srs.md#nfr-005) |
| Business rules | [BR-004](business-rules.md#br-004), [BR-005](business-rules.md#br-005), [BR-009](business-rules.md#br-009), [BR-010](business-rules.md#br-010), [BR-011](business-rules.md#br-011), [BR-016](business-rules.md#br-016), [BR-019](business-rules.md#br-019), [BR-024](business-rules.md#br-024), [BR-025](business-rules.md#br-025) |
| Acceptance criteria | [AC-027](acceptance-criteria.md#ac-027), [AC-028](acceptance-criteria.md#ac-028), [AC-029](acceptance-criteria.md#ac-029), [AC-030](acceptance-criteria.md#ac-030), [AC-031](acceptance-criteria.md#ac-031), [AC-032](acceptance-criteria.md#ac-032), [AC-033](acceptance-criteria.md#ac-033), [AC-034](acceptance-criteria.md#ac-034) |
| Dependencies | [F-002](prd.md#f-002), [F-007](prd.md#f-007). Paused manual behavior and related policy remain [Q-03](prd.md#q-03). |
| Status | DERIVED DRAFT |

<a id="us-030"></a>
### US-030 — HTTP keyword monitoring

As a Backend Developer, I want to check HTTP response content for a literal keyword, so that I can detect invalid content behind a successful status.

| Field | Value |
|---|---|
| Role | Backend Developer |
| Release | v0.5.0 Beta |
| Priority | Must |
| Features | [F-030](prd.md#f-030) |
| Functional requirements | [FR-059](srs.md#fr-059) |
| Other requirements | [NFR-022](srs.md#nfr-022) |
| Business rules | [BR-006](business-rules.md#br-006), [BR-022](business-rules.md#br-022) |
| Acceptance criteria | [AC-080](acceptance-criteria.md#ac-080), [AC-082](acceptance-criteria.md#ac-082) |
| Dependencies | [F-002](prd.md#f-002) |
| Status | DERIVED DRAFT |

<a id="us-031"></a>
### US-031 — JSON assertion monitoring

As a Backend Developer, I want to configure a declarative JSON assertion, so that I can detect an incorrect API response.

| Field | Value |
|---|---|
| Role | Backend Developer |
| Release | v0.5.0 Beta |
| Priority | Must |
| Features | [F-031](prd.md#f-031) |
| Functional requirements | [FR-060](srs.md#fr-060) |
| Other requirements | [NFR-022](srs.md#nfr-022) |
| Business rules | [BR-006](business-rules.md#br-006), [BR-022](business-rules.md#br-022) |
| Acceptance criteria | [AC-081](acceptance-criteria.md#ac-081), [AC-082](acceptance-criteria.md#ac-082), [AC-099](acceptance-criteria.md#ac-099) |
| Dependencies | [F-002](prd.md#f-002). Malformed target JSON classification is conditional on [Q-09](prd.md#q-09). |
| Status | DERIVED DRAFT |

<a id="us-032"></a>
### US-032 — Workspace invitations and membership

As a Workspace Owner, I want to invite and remove workspace participants, so that I can keep team access current.

| Field | Value |
|---|---|
| Role | Workspace Owner |
| Release | v0.5.0 Beta |
| Priority | Must |
| Features | [F-032](prd.md#f-032) |
| Functional requirements | [FR-049](srs.md#fr-049), [FR-050](srs.md#fr-050), [FR-051](srs.md#fr-051) |
| Other requirements | — |
| Business rules | [BR-001](business-rules.md#br-001), [BR-005](business-rules.md#br-005) |
| Acceptance criteria | [AC-064](acceptance-criteria.md#ac-064), [AC-065](acceptance-criteria.md#ac-065), [AC-066](acceptance-criteria.md#ac-066) |
| Dependencies | [F-002](prd.md#f-002) |
| Status | DERIVED DRAFT |

<a id="us-033"></a>
### US-033 — Basic uptime and latency metrics

As a Workspace Owner, I want to view uptime, latency and the number of qualifying observations, so that I can distinguish measured performance from missing evidence.

| Field | Value |
|---|---|
| Role | Workspace Owner |
| Release | v0.1.0 MVP |
| Priority | Must |
| Features | [F-033](prd.md#f-033) |
| Functional requirements | [FR-061](srs.md#fr-061), [FR-062](srs.md#fr-062), [FR-063](srs.md#fr-063), [FR-064](srs.md#fr-064) |
| Other requirements | — |
| Business rules | [BR-008](business-rules.md#br-008), [BR-013](business-rules.md#br-013), [BR-019](business-rules.md#br-019), [BR-024](business-rules.md#br-024), [BR-025](business-rules.md#br-025) |
| Acceptance criteria | [AC-083](acceptance-criteria.md#ac-083), [AC-084](acceptance-criteria.md#ac-084), [AC-085](acceptance-criteria.md#ac-085), [AC-086](acceptance-criteria.md#ac-086) |
| Dependencies | [F-002](prd.md#f-002), [F-007](prd.md#f-007). MVP metrics apply per monitor. Exact window and sample rules remain [Q-06](prd.md#q-06). |
| Status | DERIVED DRAFT |

<a id="us-034"></a>
### US-034 — View and update my own supported account settings

As an Account holder, I want to view and update my own supported account settings, so that I can maintain my account details.

| Field | Value |
|---|---|
| Role | Account holder |
| Release | v0.1.0 MVP |
| Priority | Should |
| Features | [F-001](prd.md#f-001) |
| Functional requirements | [FR-008](srs.md#fr-008) |
| Other requirements | — |
| Business rules | [BR-003](business-rules.md#br-003) |
| Acceptance criteria | [AC-008](acceptance-criteria.md#ac-008) |
| Dependencies | Initial setup for authenticated use |
| Status | PROPOSED |

## References

- [Product Requirements Document](prd.md)
- [Software Requirements Specification](srs.md)
- [Business Rules](business-rules.md)
- [Acceptance Criteria](acceptance-criteria.md)
- [User Flows and Screen Catalog](user-flows.md)
