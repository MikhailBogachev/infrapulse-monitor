# Development Workflow
ID: IP-DOC-005 | Version: 1.0 | Status: Approved principles

For tasks that change the repository, use GitHub Flow with an issue, a focused branch, task-specific checks, a pull request and human review. Main must remain releasable. Use Conventional Commits such as `feat(auth): implement JWT authentication`.

Board: Backlog → Ready → In Progress → Review → Testing → Done. An issue is Ready when scope, dependencies and acceptance criteria are clear.

## Codex CLI workflow

- Codex CLI is the current development assistant interface. Repository documentation is the primary source of project context.
- Use the read-only sandbox for analysis tasks and the workspace-write sandbox for approved editing tasks.
- Obtain human approval before expanding task scope.
- Obtain human review before committing or merging changes.
- Never push automatically to remote repositories.

## Task template
Task ID; title; context; objective; functional requirements; technical requirements; scope; out of scope; acceptance criteria; testing; documentation; deliverables; verification commands.

## Definition of Done

### Analysis and read-only tasks

- The report addresses the task and its acceptance criteria, cites evidence and records unresolved findings.
- A human reviews and accepts the report. Acceptance may occur without repository changes, commits or a pull request.

### Documentation tasks

- The documentation meets the acceptance criteria and passes relevant consistency checks and local link validation.
- The changes have a pull request and completed human review.

### Implementation tasks

- Requirements and acceptance criteria satisfied.
- Relevant unit and integration tests written and passed.
- Ruff and mypy checks passed when configured.
- Authorization and security reviewed.
- Documentation updated.
- CI passed; human review completed; PR merged into main.

## Review discipline
Record material decisions as ADRs with context, options, decision and consequences. Do not treat a proposed ADR as approved. Report test evidence and unresolved issues. [D-010](../project/decision-register.md#d-010) requires GitHub Actions for MVP CI. Stage 04 establishes the pipeline and its verification commands. GitHub settings and branch protections remain pending.
