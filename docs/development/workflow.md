# Development Workflow
ID: IP-DOC-005 | Version: 1.0 | Status: Approved principles

Use GitHub Flow: issue → focused branch → implementation → tests → PR → review → merge. Main must remain releasable. Example branch: `feature/IP-001-auth`. Use Conventional Commits, e.g. `feat(auth): implement JWT authentication`.

Board: Backlog → Ready → In Progress → Review → Testing → Done. An issue is Ready when scope, dependencies and acceptance criteria are clear.

## Task template
Task ID; title; context; objective; functional requirements; technical requirements; scope; out of scope; acceptance criteria; testing; documentation; deliverables; verification commands.

## Definition of Done
- Requirements and acceptance criteria satisfied.
- Relevant unit and integration tests written and passed.
- Ruff and mypy checks passed when configured.
- Authorization and security reviewed.
- Documentation updated.
- CI passed; human review completed; PR merged into main.

## Review discipline
Record material decisions as ADRs with context, options, decision and consequences. Do not treat a proposed ADR as approved. Report test evidence and unresolved issues. Actual GitHub settings, CI commands and branch protections will be established in Stage 04.
