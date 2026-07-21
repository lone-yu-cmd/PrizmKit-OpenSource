# Test Report Template

Create one human-readable report for every terminal result. Replace an older report for the same invocation context; do not append duplicate final-result sections. Use the exact `## Final Result` heading and `- Result: <TEST_*>` marker shown below. Do not rename this machine-read contract to `Terminal Result`, `Final Decision`, or another heading.

```markdown
# Test Report

## Final Result

- Result: TEST_PASS | TEST_NEEDS_FIXES | TEST_BLOCKED
- Summary: <concise testing-domain conclusion>

## Change Scope

- Scope: <this-change / module / feature / full-project>
- Production paths: <paths or none>
- Test paths: <existing, added, and modified paths>
- Requirement source: <specification, acceptance criteria, caller request, or none>

## Affected Business Module

- Boundary: <explicit module or cohesion-derived responsibility>
- Public entry points: <entries>
- Scope rationale: <why this is the complete affected boundary>

## Observable Business Behaviors

| Behavior | Truth Source | Tests | Result |
|---|---|---|---|
| <behavior> | <spec/contract/acceptance/test/caller> | <test paths or cases> | passed / needs-fixes / blocked |

## Boundary and Risk Coverage

| Behavior | Applicable Risks | Coverage | Material Omission Reason |
|---|---|---|---|
| <behavior> | <functional, boundary, error, state, side-effect, permission, concurrency, idempotency, time, dependency, consumer> | <tests and layers> | <none or behavior-specific reason> |

Coverage metrics, when available: <diagnostic values or not collected>. Percentages are not the completion basis.

## Regression Ring

| Caller / Consumer / Contract / State | Coupling | Verification | Result |
|---|---|---|---|
| <edge> | <observable dependency> | <test or command> | passed / needs-fixes / blocked |

- Unresolved verdict-capable edges: <none or list>

## Tests Added or Updated

| Path | Layer | Behaviors and Risks | Change |
|---|---|---|---|
| <path> | focused / module / contract / integration / E2E / regression | <coverage> | added / updated / existing |

- Existing native framework reused: <yes/no and framework>
- Infrastructure changes: <none or concise list>
- Testability seams: <none or behavior-preserving changes>

## Native Test Execution

| Command | Working Directory | Scope / Layer | Result | Key Output |
|---|---|---|---|---|
| <native command> | <cwd> | <tests or layer> | passed / failed / blocked | <concise output or log pointer> |

- Required affected-module regression complete: yes / no
- Required Regression Ring verification complete: yes / no
- Project-wide regression required: yes / no
- Project-wide regression result: passed / failed / not-required / blocked

## Main-Agent Review

- Rounds: <0..10>
- Accepted findings: <count>
- Fixed findings: <count>
- Rejected findings: <count with concise evidence pointers>
- Unresolved findings: <count and list>
- Converged on exact final state: yes / no

## Independent Test Review

- Status: completed / downgraded / not_applicable
- Responses: <0..5>
- Capability gate or downgrade reason: <reason or none>
- Corrections and Main-Agent adjudication: <summary or none>
- Exact final state independently rechecked: yes / no

## Repairs Performed

| Round | Failure Classification | Repair | Focused Verification | Required Regression |
|---|---|---|---|---|
| <1..3> | test-defect / local-production-defect / high-risk-production-defect / environment-unavailable / truth-unresolved / flaky-or-unreliable | <change or none> | <result> | <result> |

- Repair rounds used: <0..3>
- Assertions or scope weakened to obtain green output: no

## Production Repair Risk

- Production changed during test: yes / no
- Repair locality: <local / high-risk / none>
- Delta Code Review required: yes / no
- Review scope: delta / none
- Rationale: <contract and risk analysis>

## External Contracts and Mocks

| Dependency | Contract Source | Test Double / Isolation | Variants | Remaining Risk |
|---|---|---|---|---|
| <dependency> | <project path or public official source/version> | <mock/fake/server/container/isolated service> | <success/boundary/failure variants> | <none or risk> |

- Production credentials or resources used: no
- Real deployed environment validated: no

## Remaining Risks and Unresolved Items

- <none, or every known correction/blocker with concrete target and next required fact>
```

## Result Rendering Rules

Render `TEST_PASS` only when:

- mandatory Main-Agent review converged;
- independent review converged or was visibly downgraded under its strict capability gate;
- all required native tests pass on the exact final state;
- no accepted or unresolved finding remains;
- no high-risk production repair awaits delta Code Review;
- no mutation occurred after final applicable review and execution.

Render `TEST_NEEDS_FIXES` for a known remaining correction, exhausted review/repair budget with known work, or a completed high-risk repair requiring delta Code Review.

Render `TEST_BLOCKED` when truth, required input, safe environment, execution reliability, external-target safety, or required Reviewer input prevents a safe verdict.

No conditional pass, commit authorization, release authorization, runtime classification, target hash, manifest, attestation, or package lifecycle belongs in the report.

## Terminal Machine Projection

Write `test-result.json` together with the report:

```json
{
  "schema_version": 1,
  "result": "TEST_PASS",
  "report": "test-report.md",
  "main_review_rounds": 1,
  "independent_review": {
    "status": "downgraded",
    "responses": 0,
    "downgrade_reason": "required read-only continuation capability is unavailable",
    "final_state_rechecked": false
  },
  "repair_rounds": 0,
  "production_changed": false,
  "review_required": false,
  "review_scope": null,
  "unresolved_items": []
}
```

Constraints:

- `schema_version` is `1`.
- `result` is `TEST_PASS`, `TEST_NEEDS_FIXES`, or `TEST_BLOCKED`.
- `report` is the sibling report filename `test-report.md`.
- `main_review_rounds` is an integer from `0` through `10`; `0` is valid only when early blocking prevents a complete review round.
- `independent_review.status` is `completed`, `downgraded`, or `not_applicable`.
- `completed` requires `responses` from `1` through `5`, `downgrade_reason=null`, and `final_state_rechecked=true`.
- `downgraded` requires `responses=0`, a non-empty `downgrade_reason`, and `final_state_rechecked=false`.
- `not_applicable` requires `responses=0`, `downgrade_reason=null`, and `final_state_rechecked=false`.
- `independent_review.responses` is otherwise bounded from `0` through `5`.
- `review_scope` is `delta` exactly when `review_required=true`; otherwise it is null.
- `unresolved_items` contains concise strings and agrees with the report.
- Report and JSON agree on final result and production-review requirement.
- The JSON is terminal output only and is never updated as an internal checkpoint.
