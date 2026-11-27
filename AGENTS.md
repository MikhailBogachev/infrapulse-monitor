# Instructions for coding agents

## Project context
Repository documentation is the primary source of project context. Before work, read the [charter](docs/project/charter.md), [roadmap](docs/project/roadmap.md), [risk register](docs/project/risk-register.md) and [glossary](docs/project/glossary.md). Read applicable approved product specifications and ADRs when present.

- Stage 00 — Project Initialization is approved and complete.
- Stage 01 — Product Discovery is COMPLETED AND APPROVED.
- Stage 02 — System Design is COMPLETED AND APPROVED.
- Stage 03 — UI/UX is COMPLETED AND APPROVED.
- Stage 04 — Development Setup is PENDING.
- IP-000 — Project Context Initialization is accepted.
- IP-001 — Project Initialization Baseline Corrections is complete and merged.
- IP-002 — Product Discovery Decision Review is approved.
- IP-003 — Product Requirements Documentation is COMPLETED AND MERGED.
- IP-004 — Product Requirements Finalization is COMPLETED AND MERGED.
- IP-005 — System Design and Architecture is COMPLETED AND APPROVED.
- IP-006 — UI/UX Design is COMPLETED AND APPROVED.
- Next task: IP-007 — Development Environment Setup.
- Application implementation has not started. Explicit owner authorization is required before implementation.

## Product requirements

- Read [approved product decisions PD-001–PD-015](docs/project/decision-register.md#approved-product-decisions) and [approved Q-01–Q-15](docs/project/decision-register.md#ip-004-product-decisions) for Stage 01 scope. Apply [PD-016](docs/project/decision-register.md#pd-016) as the approved IP-005 refinement.
- Use the [PRD](docs/product/prd.md) for scope and catalog, the [SRS](docs/product/srs.md) for normative requirements and the [Acceptance Criteria](docs/product/acceptance-criteria.md) for expected evidence. The product documents form the approved Stage 01 baseline.
- Preserve feature IDs and release assignments. Trace requirements to their sources, verification methods and acceptance criteria in the [Requirements Traceability Matrix](docs/product/requirements-traceability-matrix.md). Link applicable stories, rules, flows and screens. Record exceptions and gaps.
- Use the decision register for approved scope and the PRD for deferred design details. For Stage 02, use the [architecture overview](docs/architecture/system-architecture.md) and [approved architecture decisions](docs/project/decision-register.md#approved-stage-02-architecture-decisions). The owner accepted Stage 02 in IP-005 Final Acceptance.
- For Stage 03, use the [approved UX decisions](docs/project/decision-register.md#approved-stage-03-ux-decisions), [design system](docs/design/design-system.md) and [MVP screen specifications](docs/design/screen-specifications.md).

## Codex CLI
- Use Codex CLI as the current development assistant interface.
- Use the read-only sandbox for analysis tasks and the workspace-write sandbox for approved editing tasks.
- Obtain human approval before expanding task scope and human review before committing or merging changes.
- Never push automatically to remote repositories.

## Lean Development workflow

Task → Implementation → Self-validation → Owner Review → Commit → Pull Request → Merge.

- Deliver one complete outcome per task. In the same session, validate the result and fix in-scope defects. Group small corrections in the original task.
- Revisit accepted areas when evidence points to regression. Use independent review as needed for material architectural, security-sensitive or release-critical changes.
- CRITICAL and material HIGH defects block acceptance. Fix MEDIUM defects within scope and document any that require material expansion. LOW defects and optional improvements do not block acceptance.
- Keep reports compact and evidence-based. Use the repository instructions directly so task prompts can focus on the task. Obtain owner approval for material product and architectural decisions.
- Preserve GitHub Flow, Conventional Commits, required CI, automated tests, security, ADRs and change control. Follow the [development workflow](docs/development/workflow.md).

## Working rules
- Follow the current issue, acceptance criteria and approved scope. Ask about contradictions or missing requirements; do not silently invent product behavior.
- Prefer a modular monolith, explicit boundaries, simple solutions and typed Python. Do not introduce dependencies or architectural changes without justification and approval where material.
- Never commit secrets, tokens, real credentials or sensitive logs. Use synthetic fixtures. Do not probe external networks without authorization; test with controlled targets.
- Preserve workspace isolation, bounded retries, idempotency and SSRF defenses. Do not weaken security or tests to make a task pass.
- Inspect existing files before editing; preserve unrelated changes. Keep diffs focused. Do not push, merge, deploy or perform destructive operations without explicit authorization.
- Write code, comments and repository documentation in English. Discuss work with the owner in Russian unless requested otherwise.
- Run relevant checks once tooling exists. Report exact commands, outcomes, skipped checks and blockers. Never claim unrun tests passed.
- Do not assume dependency versions or verification commands exist before setup. Update docs with behavioral changes.

## Task completion report
Summarize changes, affected files, requirement IDs, tests run and results, remaining risks and suggested next step. Follow the [development workflow](docs/development/workflow.md).
