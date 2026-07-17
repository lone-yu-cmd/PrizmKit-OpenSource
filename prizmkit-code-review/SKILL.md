---
name: "prizmkit-code-review"
description: "Review the complete current change for a formal PrizmKit requirement in a bounded Main-Agent loop. Directly repair accepted findings, verify repairs, converge to PASS or stop with NEEDS_FIXES, and hand off to prizmkit-test. (project)"
---

# PrizmKit Code Review

`/prizmkit-code-review` is the mandatory review stage after implementation and before the full test stage. The current Main Agent is the only Code Review executor. It owns the complete review loop: it discovers findings, adjudicates them, directly repairs accepted findings, verifies repairs, and continues until the review converges or stops safely.

## Execution Boundary

- Do not delegate any part of Code Review directly or indirectly.
- Do not invoke another review skill or review workflow from inside this skill.
- Do not launch review work through a general-purpose execution unit or relabel it as a finder, verifier, audit, compatibility review, verification, or gap sweep.
- The Main Agent may directly read, search, edit, and run targeted verification in the active workspace.
- Review repairs occur before the full `/prizmkit-test` stage so final test evidence represents the final reviewed workspace.
- `{artifact_dir}/review-report.md` is the only persisted review artifact for this execution.

## When to Use

- After `/prizmkit-implement` reports `IMPLEMENTED`.
- After implementation repairs that changed production code, runtime configuration, schema, dependencies, or public interfaces.
- When workflow state routes a formal requirement back to review after `TEST_FAIL`.
- When the user asks for a complete review or commit readiness decision.

## When NOT to Use

- No valid `spec.md` and `plan.md` exist for the active requirement.
- Implementation tasks or required repair work remain incomplete.
- A `TEST_BLOCKED` state is caused by environment availability rather than a review concern; resume from test when the environment is available.
- The request is a direct low-risk edit outside the formal requirement lifecycle.

## Input and State

| Parameter | Required | Description |
|---|---|---|
| `artifact_dir` | No | Directory containing `spec.md` and `plan.md`. Reuse the caller's directory or workflow-state value. |
| `review_scope` | No | `full` for the initial review; `delta` for a production-affecting repair after a prior review pass. |

Every invocation must reuse the same `artifact_dir`. If workflow state is missing, reconstruct it from `spec.md`, `plan.md`, `review-report.md`, the current diff, and any test evidence, and report the reconstruction.

## Phase 0: Initialize Report and Collect Context

1. Resolve `{artifact_dir}` and `{artifact_dir}/review-report.md`.
2. At the start of each execution, replace any prior report with a new execution header using `${SKILL_DIR}/references/review-report-template.md`.
3. Within that execution, append progress after every review round, repair batch, final verification, and exactly one `## Final Result`.
4. Read `spec.md`, `plan.md`, relevant current test evidence if present, `.prizmkit/prizm-docs/root.prizm` when present, applicable progressive docs, and project rules.
5. Inspect staged and unstaged tracked changes, untracked files, deleted and renamed files, plus relevant unchanged callers, dependents, contracts, and tests.
6. For `review_scope=delta`, focus on files and behavior affected since the prior review pass while checking their callers and contracts.
7. If no changes exist, record final verification and `PASS` only when the required requirement artifacts and prior implementation state prove there is nothing left to review.

## Phase 1: Main-Agent Review Loop

The Main Agent reviews the complete current change against goals, acceptance criteria, contracts, rules, callers, dependents, regression risks, and implementation evidence.

Use at most ten completed review rounds per execution. Track:

```yaml
main_review_rounds: 0
accepted_findings: 0
fixed_findings: 0
rejected_findings: 0
unresolved_findings: 0
```

For every candidate finding:

1. Describe a reproducible failure scenario, affected behavior, and evidence.
2. Classify exactly one of:
   - `accepted`: evidence proves an in-scope repair is needed;
   - `rejected`: evidence disproves the failure scenario;
   - `unresolved`: correctness or safe repair cannot be established.
3. Treat Missing tools, permissions, environment, or required evidence as an unresolved finding when they prevent review verification.
4. If a repair cannot be completed safely, record an unresolved finding and return `NEEDS_FIXES`.
5. Append the review round to `review-report.md`.

Round behavior:

```text
accepted = 0 and unresolved = 0
  → review converged

accepted > 0 and rounds remain
  → Main Agent directly repairs accepted findings
  → targeted verification
  → next complete review round

unresolved > 0 or safe repair impossible
  → NEEDS_FIXES

maximum ten completed rounds reached with accepted findings
  → NEEDS_FIXES
```

## Phase 2: Repair and Verification

For accepted findings while the round limit remains:

1. Repair directly in the active workspace.
2. Run targeted tests, static checks, or other verification appropriate to each repair.
3. Inspect the complete resulting diff for unrelated changes and regressions.
4. Append repair verification and continue the review loop.

Do not run the full auditable testing protocol as a substitute for this review stage. The full testing stage follows only after review `PASS`.

If a repair is unsafe, incomplete, or unverifiable, record an unresolved finding and finish with `NEEDS_FIXES`.

## Phase 3: Final Result

Before completing:

1. Confirm the final workspace is the complete reviewed change.
2. Confirm all accepted findings are fixed and no unresolved finding remains for `PASS`.
3. Append final verification and exactly one final result.

Valid results:

```text
PASS | NEEDS_FIXES
```

`PASS` requires review convergence, no unresolved findings, and credible targeted verification. `NEEDS_FIXES` means an outer implementation repair is required or the workflow is blocked.

## Workflow State and Outer Repair Routing

Before reading or updating workflow state, read `${SKILL_DIR}/references/workflow-state-protocol.md`.

On `PASS`, update workflow state:

```json
{
  "stage": "code-review",
  "status": "REVIEW_PASS",
  "completed_stages": ["plan", "implement", "code-review"],
  "review_scope": "full",
  "next_stage": "test",
  "resume_from": "prizmkit-test"
}
```

On `NEEDS_FIXES` caused by code findings:

```json
{
  "stage": "code-review",
  "status": "REVIEW_NEEDS_FIXES",
  "repair_scope": "production",
  "next_stage": "implement",
  "resume_from": "prizmkit-implement"
}
```

Increment the outer `repair_round` when returning to implementation. The outer workflow permits at most three repair rounds. If the limit is reached, return a truthful blocked state with unresolved findings and recovery instructions.

## Handoff

After `PASS`:

```text
REVIEW_PASS
  → /prizmkit-test
```

If semantic skill handoff is supported, invoke `/prizmkit-test` with the same `artifact_dir`. Otherwise report the exact next invocation and workflow-state path.

After `NEEDS_FIXES`, stop and hand off to `/prizmkit-implement`; do not test or commit the unrepaired production change.
