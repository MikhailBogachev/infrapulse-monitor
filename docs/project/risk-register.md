# Risk Register
ID: IP-DOC-003 | Version: 1.0 | Status: Active

All risks initially open. H = high, M = medium, L = low. Owner reviews at each stage gate; proposed mitigations are not implemented controls.

| ID | Risk | Likelihood / impact | Mitigation / verification | Responsible role |
|---|---|---|---|---|
| R-01 | Scope creep | H/H | Release boundaries; change approval | Product owner |
| R-02 | SSRF / network abuse through internal allowlisting, supported outbound paths or additional monitor types | H/H | The pinned [HTTPX candidate](../development/technical-spikes.md#4-httpx-secure-transport) passed controlled checks. [Native Linux firewall evidence](../development/technical-spikes.md#5-ipv4ipv6-egress-enforcement) and verification on the supported deployment topology are pending, including policy readiness after replacement and the narrow control-plane exceptions. | Backend |
| R-03 | Duplicate tasks or manual and scheduled overlap | H/H | The [Celery TLS fixture](../development/technical-spikes.md#6-worker-execution-guard) observed at most one active socket after lease expiry, DB disconnect, child death and container replacement. Verify the native Linux deployment, stable lock-volume lifecycle and trusted generation-exit proof before closing the gate. | Backend |
| R-04 | Lost tasks | M/H | Verify confirms, mandatory routing, durable reconciliation and late acknowledgement with controlled broker failure. | Backend |
| R-05 | False incidents | H/M | Failure/recovery thresholds; ordered state transitions | Backend |
| R-06 | History growth | H/H | Verify six-hour partitions, ledger/index overhead, physical cleanup and representative query plans. | Backend |
| R-07 | Provider outage | H/M | Timeouts, bounded retries for eligible confirmed failures, no blind resend after an indeterminate outcome, rate limits and failure visibility | Backend |
| R-08 | AI-generated defects | H/H | Small PRs, human review, tests, no unverified claims | Owner |
| R-09 | Frontend effort | H/M | Reusable components and limited MVP screens | Frontend |
| R-10 | Naming conflict | H/M | Working name only; clearance or rename before public branding | Owner |
| R-11 | Tenant data leakage | M/H | Workspace-scoped authorization and cross-tenant tests | Backend |
| R-12 | Public demo abuse or data leakage | H/H | Controlled synthetic targets, bounded resources, isolation from real and foreign session data, simulated notification behavior and verified cleanup. | Operations |
| R-13 | Dependency/concurrency mismatch | M/H | Validate Python and Celery execution model; pin versions | Backend |
| R-14 | Credential exposure | M/H | Secret handling, redaction, secret scanning | Operations |
| R-15 | Abuse of configurable registration or initial setup | M/H | Disable public registration by default after setup. Verify operator control, one-time bootstrap eligibility and rate policy. | Backend |
| R-16 | Check bursts from Run Check Now | M/H | Verify the per-monitor 30-second acceptance limit and prevention of overlap. Test ordinary traffic and scheduling under controlled concurrent requests. | Backend |
| R-17 | Stale or unauthorized live updates and reconnect bursts | M/H | Verify Beta workspace-scoped SSE, recovery of authoritative display state and resource behavior under controlled reconnects. | Frontend and Backend |

All risks remain open. Roles describe responsibilities of the solo developer. Review residual risk and evidence before release.

Stage 04 experiment evidence and residual risks for R-02, R-03, R-04, R-06, R-13 and R-14 are tracked in the [IP-007 technical spike reports](../development/technical-spikes.md).
