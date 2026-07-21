---
name: "prizmkit-code-review"
description: "Review the complete current change for a formal PrizmKit requirement with a mandatory bounded Main-Agent loop and optional capability-gated independent correctness review. Directly repair accepted corrections, verify repairs, converge to PASS or stop with NEEDS_FIXES, and hand off to prizmkit-test. (project)"
---

# PrizmKit Code Review

`/prizmkit-code-review` is the mandatory review stage after implementation and before the full test stage. The current Main Agent owns the complete baseline review loop: it discovers findings, adjudicates them, directly repairs accepted findings, verifies repairs, and continues until the review converges or stops safely. After convergence, one strictly capability-gated independent Reviewer may objectively check the complete current implementation without taking mutation or final-decision authority.

## Execution Boundary

- Main-Agent review remains mandatory and must not be delegated directly or indirectly.
- After Main-Agent convergence only, this skill may create the single independent Reviewer defined by `${SKILL_DIR}/references/independent-code-review.md` when every structural capability in that reference is proven.
- Do not invoke another review skill or review workflow from inside this skill.
- Do not launch any additional review work through a general-purpose execution unit or relabel it as a finder, verifier, audit, compatibility review, verification, or gap sweep.
- The independent Reviewer cannot mutate, execute arbitrary commands, or create downstream execution units; prompt instructions never substitute for these structural guarantees.
- The Main Agent may directly read, search, edit, and run targeted verification in the active workspace.
- Review repairs occur before the full `/prizmkit-test` stage so project-native tests run against the final reviewed workspace.
- `{artifact_dir}/review-report.md` is the only persisted review artifact for this execution.

## Atomic Stage Boundary

`prizmkit-code-review` owns the complete mandatory Main-Agent review, the optional independent correctness review, accepted-correction repairs, and review verification. It writes its truthful terminal result and `next_stage`, then returns control. It must not invoke `prizmkit-test` or `prizmkit-implement` itself; the active orchestrator owns outer repair routing and the next-stage invocation.

## When to Use

- After `/prizmkit-implement` reports `IMPLEMENTED`.
- After implementation repairs that changed production code, runtime configuration, schema, dependencies, or public interfaces.
- When a caller routes a high-risk production repair reported by `prizmkit-test` back for delta review.
- When the user asks for a complete review or commit readiness decision.

## When NOT to Use

- No valid `spec.md` and `plan.md` exist for the active requirement.
- Implementation tasks or required repair work remain incomplete.
- A test-stage environment stop is caused by availability rather than a review concern; resume from test when the environment is available.
- The request is a direct low-risk edit outside the formal requirement lifecycle.

## Input and State

| Parameter | Required | Description |
|---|---|---|
| `artifact_dir` | No | Directory containing `spec.md` and `plan.md`. Reuse the caller's directory or workflow-state value. |
| `review_scope` | No | `full` for the initial review; `delta` for a production-affecting repair after a prior review pass. |

Every invocation must reuse the same `artifact_dir`. If workflow state is missing, reconstruct it from `spec.md`, `plan.md`, `review-report.md`, the current diff, and any current test report/result pair, and report the reconstruction.

## Phase 0: Initialize Report and Reuse Current Context

1. Resolve `{artifact_dir}` and `{artifact_dir}/review-report.md` from the active requirement context.
2. At the start of each execution, replace any prior report with a new execution header using `${SKILL_DIR}/references/review-report-template.md`.
3. Within that execution, append progress after every review round, repair batch, final verification, and exactly one `## Final Result`.
4. Start from the Main Agent's current requirement context and inspect the complete workspace change first: `git status --short`, the staged diff, and the unstaged diff. Include untracked, deleted, and renamed files in the review scope.
5. Do not reread `spec.md`, `plan.md`, project rules, progressive docs, or unchanged source merely to recreate context the Main Agent already holds. Load only the missing or potentially stale material required to resolve a concrete ambiguity, verify an acceptance criterion, understand a changed contract, or reconstruct missing workflow state.
6. Inspect unchanged callers, dependents, contracts, or tests only when the diff changes or may violate an interface, shared behavior, or regression boundary. Do not perform an unconditional repository-wide dependency sweep.
7. For `review_scope=delta`, focus on files and behavior affected since the prior review pass and expand only across contracts implicated by that delta.
8. If no changes exist, record final verification and `PASS` only when the current requirement context and prior implementation state prove there is nothing left to review.

## Phase 1: Main-Agent Review Loop

The Main Agent reviews the complete current change, using the active requirement context and expanding beyond the diff only when a concrete acceptance criterion, contract, dependency, or regression risk requires it.

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
  → when all candidate findings are rejected, accepted remains 0 and the review converges

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

## Phase 3: Independent Code Review

Run only after the Main-Agent review and repair loop converges with no unresolved finding. Main-Agent review remains mandatory on every host; this optional check never replaces or weakens it.

1. Read `${SKILL_DIR}/references/independent-code-review.md` and follow its complete contract.
2. Apply its all-or-nothing semantic Host Capability Gate. If any required structural capability is unavailable or unproven, create no Reviewer, append `independent-review-downgrade`, and preserve the valid completed Main-Agent review.
3. When the gate passes, capture bounded immutable input for the complete current change and create exactly one Code Reviewer with the reference's Initial Reviewer Prompt.
4. Use maximum five Reviewer responses. Append `independent-review-round` and `independent-adjudication` events. The Main Agent adjudicates every correction as `accepted`, `rejected`, or `unresolved` and retains all mutation authority.
5. For accepted corrections, repair directly in the active checkout, run targeted verification, and inspect the complete resulting change.
6. When responses remain, capture the complete fresh state and natively resume the exact same Reviewer. Never create a replacement Reviewer or simulate continuation with a fresh Reviewer plus summary.
7. If native resume fails after repair, append downgrade and rerun the Main-Agent review over that repair within the existing ten-round safety fuse.
8. If the fifth response causes a repair, run targeted verification, inspect the complete final change, record `Final State Independently Rechecked: no`, and do not send a sixth response.
9. `NO_CORRECTION_NEEDED` or all corrections rejected with evidence converges independent review. Any unresolved correction produces `NEEDS_FIXES`.

## Phase 4: Final Result

Before completing:

1. Confirm the final workspace is the complete reviewed change.
2. Confirm all accepted findings are fixed and no unresolved finding remains for `PASS`.
3. Append final verification and exactly one final result.

Valid results:

```text
PASS | NEEDS_FIXES
```

`PASS` requires review convergence, no unresolved findings, and credible targeted verification. `NEEDS_FIXES` means an outer implementation repair is required or completion must stop safely.

## Workflow State and Outer Repair Routing

Before reading or updating workflow state, read `${SKILL_DIR}/references/workflow-state-protocol.md`.

On `PASS`, update workflow state:

```json
{
  "stage": "code-review",
  "status": "completed",
  "stage_result": "REVIEW_PASS",
  "completed_stages": ["plan", "implement", "code-review"],
  "next_stage": "test",
  "resume_from": "prizmkit-test"
}
```

On `NEEDS_FIXES` caused by code findings, update workflow state:

```json
{
  "stage": "code-review",
  "status": "failed",
  "stage_result": "REVIEW_NEEDS_FIXES",
  "repair_scope": "production",
  "next_stage": "implement",
  "resume_from": "prizmkit-implement"
}
```

Increment the outer `repair_round` only when returning to implementation; the review-internal ten-round loop never increments it. The outer workflow permits at most three repair rounds and must return a truthful unresolved `NEEDS_FIXES` result instead of beginning a fourth.

## Handoff

After `PASS`:

```text
REVIEW_PASS
  → /prizmkit-test
```

If workflow state names an active `orchestrator`, return `REVIEW_PASS`, the report/state paths, and `next_stage=test` to it; do not invoke test independently. For direct stage use, report the exact `/prizmkit-test` invocation and same `artifact_dir`; a host may perform that semantic handoff on the user's behalf.

After `NEEDS_FIXES`, stop and hand off to `/prizmkit-implement`; do not test or commit the unrepaired production change.
