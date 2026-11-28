# InfraPulse
Open-source, self-hosted infrastructure and API monitoring platform with a web interface.

## Project status

- Stage 00 — Project Initialization is approved and complete.
- Stage 01 — Product Discovery is COMPLETED AND APPROVED.
- Stage 02 — System Design is COMPLETED AND APPROVED.
- Stage 03 — UI/UX is COMPLETED AND APPROVED.
- Stage 04 — Development Setup is COMPLETED AND APPROVED.
- Stage 05 — Backend is PENDING.
- IP-000 — Project Context Initialization is accepted.
- IP-001 — Project Initialization Baseline Corrections is complete and merged.
- IP-002 — Product Discovery Decision Review is approved.
- IP-003 — Product Requirements Documentation is COMPLETED AND MERGED.
- IP-004 — Product Requirements Finalization is COMPLETED AND MERGED.
- IP-005 — System Design and Architecture is COMPLETED AND APPROVED.
- IP-006 — UI/UX Design is COMPLETED AND APPROVED.
- IP-007 — Development Environment Setup is COMPLETED AND APPROVED. See [IP-007 Final Owner Acceptance](docs/project/decision-register.md#ip-007-verification).

## Development setup

Run `make install` and `make up`, then open <http://127.0.0.1:8080/>. See the [setup guide](docs/development/setup.md) and [Stage 04 spike reports](docs/development/technical-spikes.md).

## Project documentation
- [Project Charter](docs/project/charter.md)
- [Roadmap](docs/project/roadmap.md)
- [Risk Register](docs/project/risk-register.md)
- [Glossary](docs/project/glossary.md)
- [Decision Register](docs/project/decision-register.md)
- [Development Workflow](docs/development/workflow.md)
- [Agent Instructions](AGENTS.md)

## Product Discovery documentation

Product documentation version 0.2 is the approved Stage 01 baseline. [Q-01–Q-15](docs/project/decision-register.md#ip-004-product-decisions) are approved. [PD-016](docs/project/decision-register.md#pd-016) is the approved IP-005 lifecycle refinement.

- [Product Requirements Document](docs/product/prd.md)
- [Software Requirements Specification](docs/product/srs.md)
- [User Personas](docs/product/user-personas.md)
- [User Stories](docs/product/user-stories.md)
- [User Flows and UI Screen Catalog](docs/product/user-flows.md)
- [Business Rules](docs/product/business-rules.md)
- [Acceptance Criteria](docs/product/acceptance-criteria.md)
- [Product Backlog](docs/product/product-backlog.md)
- [Requirements Traceability Matrix](docs/product/requirements-traceability-matrix.md)

## System Design documentation

- [System architecture and requirements map](docs/architecture/system-architecture.md)
- [Approved technology stack](docs/architecture/technology-stack.md)
- [Architecture decision register](docs/project/decision-register.md#approved-stage-02-architecture-decisions)

## UI/UX design documentation

The design documentation and interactive HTML prototype form the [approved design baseline](docs/project/roadmap.md#ip-006-uiux-design).

- [Design system](docs/design/design-system.md)
- [Information architecture](docs/design/information-architecture.md)
- [MVP screen specifications](docs/design/screen-specifications.md)
- [Interaction patterns](docs/design/interaction-patterns.md)
- [Responsive design](docs/design/responsive-design.md)
- [Accessibility specification](docs/design/accessibility.md)

Open [the local prototype](docs/design/prototype/index.html) directly in a browser. It starts in the reference workspace. Use **Prototype / Demo Data** in the sidebar or mobile drawer to demonstrate session and operational states or reset the fixture. It runs offline with in-memory synthetic data. Use `owner@example.com` and `infrapulse-demo` if asked to sign in.

InfraPulse is a working name; trademark clearance is not established. Intended license: MIT (license text pending setup).
