# Risk Register
ID: IP-DOC-003 | Version: 1.0 | Status: Active

All risks initially open. H = high, M = medium, L = low. Owner reviews at each stage gate; proposed mitigations are not implemented controls.

| ID | Risk | Likelihood / impact | Mitigation / verification | Responsible role |
|---|---|---|---|---|
| R-01 | Scope creep | H/H | Release boundaries; change approval | Product owner |
| R-02 | SSRF / network abuse through internal allowlisting, supported outbound paths or additional monitor types | H/H | Stage 04 mitigation verified in controlled HTTPX, native Linux synthetic and Compose fixtures, including dual-stack filtering, worker INPUT and Docker post-DNAT filtering. Implement and verify production destination policy and host-managed egress on all supported outbound paths. See [Spike 5](../development/technical-spikes.md#5-ipv4ipv6-egress-enforcement). | Backend |
| R-03 | Duplicate tasks or manual and scheduled overlap | H/H | Stage 04 mitigation verified in the Celery TLS fixture and native Linux Compose lifecycle, including exact prior-generation exit, stable lock identity, policy and proof refusal, and no overlap between the recorded connections. Implement and verify the production worker execution guard and trusted host-managed termination proof. See [Spike 6](../development/technical-spikes.md#6-worker-execution-guard). | Backend |
| R-04 | Lost tasks | M/H | Verify confirms, mandatory routing, durable reconciliation and late acknowledgement with controlled broker failure. | Backend |
| R-05 | False incidents | H/M | Failure/recovery thresholds; ordered state transitions | Backend |
| R-06 | History growth | H/H | Verify six-hour partitions, ledger/index overhead, physical cleanup and representative query plans. | Backend |
| R-07 | Provider outage | H/M | Timeouts, bounded retries for eligible confirmed failures, no blind resend after an indeterminate outcome, rate limits and failure visibility | Backend |
| R-08 | AI-generated defects | H/H | Small PRs, human review, tests, no unverified claims | Owner |
| R-09 | Frontend effort | H/M | Reusable components and limited MVP screens | Frontend |
| R-10 | Naming conflict | H/M | Working name only; clearance or rename before public branding | Owner |
| R-11 | Tenant data leakage | M/H | Workspace-scoped authorization and cross-tenant tests | Backend |
| R-12 | Public demo abuse or data leakage | H/H | Controlled synthetic targets, bounded resources, isolation from real and foreign session data, simulated notification behavior and verified cleanup. | Operations |
| R-13 | Dependency/concurrency mismatch | M/H | The locked Stage 04 stack and Celery prefork execution model passed on the tested matrix. Revalidate with dependency or concurrency changes. See [Spike 1](../development/technical-spikes.md#1-technology-stack-compatibility). | Backend |
| R-14 | Credential exposure | M/H | Secret handling, redaction, secret scanning | Operations |
| R-15 | Abuse of configurable registration or initial setup | M/H | Disable public registration by default after setup. Verify operator control, one-time bootstrap eligibility and rate policy. | Backend |
| R-16 | Check bursts from Run Check Now | M/H | Verify the per-monitor 30-second acceptance limit and prevention of overlap. Test ordinary traffic and scheduling under controlled concurrent requests. | Backend |
| R-17 | Stale or unauthorized live updates and reconnect bursts | M/H | Verify Beta workspace-scoped SSE, recovery of authoritative display state and resource behavior under controlled reconnects. | Frontend and Backend |

All risks remain open. Roles describe responsibilities of the solo developer. Review residual risk and evidence before release.

The owner accepted the Stage 04 evidence, closing the native Linux fixture verification gaps for R-02 and R-03. R-02 remains open pending implementation and verification of production egress enforcement. R-03 remains open pending implementation and verification of the production worker execution guard. The [IP-007 technical spike reports](../development/technical-spikes.md) track experiment evidence and residual risks for R-02, R-03, R-04, R-06, R-13 and R-14.
