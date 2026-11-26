# Development Roadmap
ID: IP-DOC-002 | Version: 1.0 | Status: Approved baseline

Eight-week planning estimate for InfraPulse alone, not a delivery guarantee. Weeks are relative to kickoff; gates take precedence over dates.

| Stage | Weeks | Deliverables / exit gate |
|---|---|---|
| 00 Initialization | 1 | Approved charter, roadmap, risks, glossary |
| 01 Product Discovery | 1 | IP-003 prepares nine draft product documents. IP-004 validates them for owner approval before the discovery gate can close. |
| 02 System Design | 1–2 | Architecture, ERD, API, queue semantics, threat model, ADRs |
| 03 UI/UX | 2 | Screen flows, design system, responsive mockups |
| 04 Development Setup | 2 | Repository, locked dependencies, CI, Compose, verified toolchain |
| 05 Backend | 3–6 | Tested vertical slices, MVP then beta scope |
| 06 Frontend | 4–6 | Usable UI integrated with API |
| 07 QA | 6–7 | Security, integration, end-to-end and load evidence |
| 08 Deployment | 7–8 | Safe demo, operational runbook, recovery verification |
| 09 Release | 8 | Release notes, README, screenshots, architecture, tagged release |

## Product Discovery deliverables

Stage 01 is **IN PROGRESS**. IP-002 is approved. IP-003 delivers the [PRD](../product/prd.md), [SRS](../product/srs.md), [personas](../product/user-personas.md), [stories](../product/user-stories.md), [flows and screen catalog](../product/user-flows.md), [business rules](../product/business-rules.md), [acceptance criteria](../product/acceptance-criteria.md), [backlog](../product/product-backlog.md) and [traceability matrix](../product/requirements-traceability-matrix.md).

## IP-004 validation gate

IP-004 is pending. The owner reviews derived behavior against PD-001–PD-015, verifies traceability and release coverage, and approves, revises or explicitly defers open decisions. Stage 01 closure requires explicit owner approval. Stage 02 is pending.

## Release gates

- **v0.1.0 MVP.** F-001–F-012, F-029 and F-033. Demonstrate create monitor → check → incident → notification → recovery, manual checks and basic metrics through the dark, responsive UI. Verify registration, isolation and destination policy.
- **v0.5.0 Beta.** F-013–F-021 and F-030–F-032. Verify integrations, additional check types, team authorization, live updates and expanded analytics.
- **v1.0.0 Release.** F-022–F-028. Publish reproducible measured results and complete documentation. Validate the isolated interactive public demo.

See the [Decision Register](decision-register.md#approved-product-decisions) for the scope sources and the [PRD release gates](../product/prd.md#release-acceptance-gates) for expected evidence.

## Change control
Record scope changes in issues; update affected requirements, risks and roadmap. Obtain owner approval before expanding release scope. Defer optional features rather than compromising security or correctness. Overlapping weeks permit preparation, not bypassing approval gates.
