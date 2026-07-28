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

## Evidence Obligation Classification

| Property / Check | Authority | Obligation | Evidence / Status | Verdict Impact |
|---|---|---|---|---|
| <criterion, composition, prerequisite, or diagnostic> | <confirmed spec, acceptance criterion, explicit caller decision, project rule, or coupling evidence> | automated-required / manual-external-nonblocking / out-of-scope-diagnostic | <executed result, unproven status, or exact current-checkout failure> | <passed / TEST_NEEDS_FIXES correction / TEST_BLOCKED prerequisite / non-blocking> |

- Classification ambiguities: <none or blocking list>
- Unsupported obligation downgrades: none

## Deferred External and Manual Evidence

| Evidence | Authority for Deferral | Current Status | Automated Verdict Rationale |
|---|---|---|---|
| <physical/public/production-account/human evidence or none> | <confirmed source> | MANUAL_VERIFICATION_REQUIRED / other explicit unproven status | <why it may remain pending after automated software-change completion> |

Authorized deferred evidence is not an unresolved testing-domain item, does not prove the deferred behavior, and does not authorize release or deployment.

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
| <path> | focused/unit / module/component / UI component / Mock Browser / consumer contract / provider contract / integration / Full-stack E2E / regression | <coverage and proof boundary> | added / updated / existing |

- Existing native framework reused: <yes/no and framework>
- Infrastructure changes: <none or concise list>
- Testability seams: <none or behavior-preserving changes>

## Native Test Execution

| Command | Working Directory | Scope / Layer | Result | Key Output |
|---|---|---|---|---|
| <native command> | <cwd> | <tests or layer> | passed / failed / blocked | <concise output or log pointer> |

- Required affected-module regression complete: yes / no
- Required Regression Ring verification complete: yes / no
- Project-wide command executed: yes / no
- Project-wide command is a whole-result completion gate: yes / no, with authority
- Project-wide command result: passed / failed / not-run / blocked / failed-with-proven-out-of-scope-diagnostics

## Main-Agent Review

- Rounds: <0..10>
- Accepted findings: <count>
- Fixed findings: <count>
- Rejected findings: <count with concise evidence pointers>
- Unresolved findings: <count and list>
- Converged on exact final state: yes / no

## Independent Test Review

- Status: completed / downgraded / not_applicable
- Capability Gate: <ENABLED | DOWNGRADED | NOT_APPLICABLE>
- Capability Basis: <platform-neutral structural evidence or unavailable>
- Downgrade Reason: <reason or none>
- Responses: <0..5>
- Continuation Mode: <native | replacement | mixed | not-applicable>
- Reviewer Replacements: <0..1>
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

## Boundary Contracts and Test Doubles

| Boundary | Contract Authority | Fidelity Proof | Test Double | Composition Removed |
|---|---|---|---|---|
| <producer → consumer; protocol> | <boundary-appropriate source and provenance> | <generation/schema/raw-wire/shared fixture/isolated observation/contract framework> | <mock/fake/fixture/interception/server/container/service or none> | <serializer/adapter/network/provider/persistence/process or none> |

| Property Not Proven | Composition-Preserving Test | Evidence Classification | Remaining Risk / Verdict Impact |
|---|---|---|---|
| <property outside the double-backed proof boundary> | <provider/consumer contract, integration, Full-stack E2E, authorized manual/external deferral, or missing> | <local / consumer contract / provider contract / integration / Mock Browser / Full-stack / manual-external-nonblocking> | <none, informational, deferred-unproven, TEST_NEEDS_FIXES correction, or TEST_BLOCKED prerequisite> |

- Test-layer claims match actual composition: yes / no
- Every verdict-capable removed combination has preserving evidence: yes / no
- Provider raw wire asserted where serialization affects the verdict: yes / no / not-applicable
- Production credentials or resources used: no
- Real deployed environment validated: no

## Remaining Risks and Unresolved Items

- Testing-domain unresolved items: <none, or every known correction/blocker with concrete target and next required fact>
- Informational risks and proven out-of-scope diagnostics: <none or exact list; do not claim unsupported historical provenance>
- Deferred external/manual evidence is reported in its dedicated section, not repeated as an unresolved testing-domain item.
```

## Result Rendering Rules

Render `TEST_PASS` only when:

- mandatory Main-Agent review converged;
- independent review converged or was visibly downgraded under its strict capability gate;
- every `automated-required` native test and composition obligation passes on the exact final state;
- every automated-verdict test double has boundary-specific authority and fidelity proof;
- every automated-verdict property removed by a double has composition-preserving evidence, and every layer claim matches actual composition;
- applicable provider contract tests assert risk-relevant raw wire payload and state-changing workflows cover commit, cancellation, failure, re-entry, and repeated-operation semantics;
- each `manual-external-nonblocking` item has explicit authority, visible unproven status, and no false pass/release/deployment claim;
- each `out-of-scope-diagnostic` satisfies affected-module/Regression Ring, path/coupling, determinism, cause, and project-rule conditions;
- no accepted or unresolved testing-domain finding remains;
- no high-risk production defect or correction remains;
- no mutation occurred after final applicable review and execution.

Render `TEST_NEEDS_FIXES` for a known remaining correction, an exhausted testing-local review/repair budget with known work, or a proven high-risk production defect that this invocation must not repair.

Render `TEST_BLOCKED` when truth, required input, an `automated-required` safe environment, execution reliability, external-target safety, obligation authority, diagnostic independence, or required Reviewer input prevents a safe verdict. This includes unavailable required composition-preserving execution and unresolved contract authority or test-double fidelity that affects the automated verdict; lower-layer green tests cannot substitute.

Authorized `manual-external-nonblocking` evidence alone does not block an otherwise complete automated verdict, but it remains unproven. No conditional pass, commit authorization, release authorization, runtime classification, target hash, manifest, attestation, or package state belongs in the report.

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
- `TEST_PASS` keeps `unresolved_items` empty; authorized deferred evidence and proven out-of-scope diagnostics remain in their human report sections. `TEST_NEEDS_FIXES` and `TEST_BLOCKED` each require at least one concise testing-domain correction or blocker string, and the list agrees with the report.
- Report and JSON agree on final result and production-change diagnostics.
- The JSON is terminal output only and is never updated as an internal checkpoint.
