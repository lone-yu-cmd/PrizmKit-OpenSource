---
name: "prizmkit-test"
description: "AI-led project-native testing for the complete affected business module and its Regression Ring. Adds comprehensive behavior, boundary, error, state, side-effect, permission, concurrency, idempotency, time, dependency, and consumer tests; repairs valid failures in a bounded loop; performs mandatory Main-Agent review plus one optional strict independent Test Reviewer; and returns TEST_PASS, TEST_NEEDS_FIXES, or TEST_BLOCKED with a human report and minimal terminal result. (project)"
---

# PrizmKit Test

`/prizmkit-test` is the independent testing stage for the current workspace. It understands the affected business behavior, fills project-native test gaps, executes the tests, repairs valid failures, reviews the final tests, and reports a truthful testing-domain result.

It does not build an evidence package, prove historical TDD order, validate a previous checkout, or manage pipeline/session state.

## Atomic Skill Boundary

The Main Agent owns this invocation from analysis through final report:

```text
resolve current change and requirement context
→ discover affected module and Regression Ring
→ model observable behavior and applicable risks
→ inspect and add project-native tests
→ execute and repair valid failures: maximum three rounds
→ mandatory Main-Agent test review: maximum ten completed rounds
→ optional independent Test Reviewer: one unit, maximum five responses
→ final native regression on the exact final state
→ write test-report.md and test-result.json
→ return TEST_PASS | TEST_NEEDS_FIXES | TEST_BLOCKED
```

After writing its result, this skill returns control to its caller. It must not:

- invoke implementation, Code Review, retrospective, or committer;
- update a workflow checkpoint or pipeline runtime state;
- classify an AI CLI session as success, crash, retry, or continuation;
- decide whether a workflow terminates or resumes;
- call a testing-domain non-pass result a runtime failure.

## Inputs and Outputs

| Parameter | Required | Description |
|---|---|---|
| `scope` | No | `full-project`, `module:<name>`, `feature:<slug>`, or `this-change`. Defaults to `this-change` when current change context exists, otherwise `full-project`. |
| `artifact_dir` | No | Active requirement directory containing available specification, plan, and prior review context. Reuse the caller-provided path. |
| `changed_files` | No | Explicit current changed paths. Highest-priority scope locator. |
| `diff_base` | No | Git comparison base when explicit changed paths are absent. |
| `test_commands` | No | Project-native commands when repository conventions are ambiguous. |

Write exactly two terminal artifacts in `artifact_dir` when it is available; otherwise use a clearly reported caller-visible artifact directory selected from the active request context:

```text
{artifact_dir}/
├── test-report.md
└── test-result.json
```

Do not create `.prizmkit/test/evidence/`, manifests, hashes, attestations, package lifecycle records, or test-internal checkpoints.

## Context Loading and Scope Resolution

1. Reuse current requirement and workspace context already loaded by the Main Agent.
2. Load `root.prizm`, the relevant module indexes, and the applicable detail docs before modifying source or tests.
3. Inspect current staged, unstaged, untracked, deleted, and renamed paths. Changed lines locate impact but never define completeness.
4. Read the available specification, acceptance criteria, plan, and prior review only as needed to establish expected behavior.
5. Inspect manifests, runner configuration, CI conventions, existing test assertions, fixtures, fakes, mocks, contracts, and coverage support.
6. If necessary scope cannot be determined safely, report the precise missing input and return `TEST_BLOCKED`.

Do not infer the active requirement solely from the name of an old artifact directory. Do not use a historical worktree, second checkout, mutation proof, baseline-failure proof, or test overlay.

## Coverage Model

Read `${SKILL_DIR}/references/test-coverage-model.md` before designing or reviewing tests.

### Affected Business Module

Prefer an explicit project module. If none exists, derive one cohesive boundary from files that jointly implement the same observable responsibility. Cover every discoverable observable behavior of that module, including relevant legacy behavior whose tests are incomplete.

### Regression Ring

Expand only along concrete coupling evidence:

- direct callers;
- consumers of values, errors, events, files, or ordering;
- shared schemas, types, protocols, generated assets, and adapters;
- persistence, cache, lock, queue, transaction, and other shared state dependencies.

Do not perform an unconditional repository-wide sweep.

### Behavior and Risks

Model outside-in from business capability or acceptance criterion to public entry point, rules, invariants, state, side effects, low-level logic, dependencies, and consumers. For each behavior, assess applicable:

```text
functional | boundary | error | state | side-effect | permission
concurrency | idempotency | time | dependency | consumer
```

A dimension may be omitted only with a concise behavior-specific reason. Coverage percentages are diagnostic signals, never a completion threshold.

### Test Layers

Use the lowest layer that proves a property without losing relevant composition, then add higher layers for composition risk:

```text
focused/unit
→ module/component
→ contract/integration
→ code-level E2E when applicable
→ complete affected-module regression
→ Regression Ring verification
```

Do not mechanically test every private function. Add direct focused tests for critical low-level logic when complexity, boundaries, risk, or failure localization justify them; otherwise prove it through public behavior.

## Test Construction

Read `${SKILL_DIR}/references/test-coverage-model.md` and, when external or cross-module contracts apply, `${SKILL_DIR}/references/external-contract-mock-guidance.md`.

Expected behavior follows this precedence:

1. confirmed specification;
2. machine-readable contract;
3. acceptance criteria;
4. trusted existing tests;
5. callers and consumers;
6. current implementation.

Conflicting higher-precedence truth that cannot be resolved is `TEST_BLOCKED`; do not preserve a possible implementation defect as a characterization test.

Tests must:

- assert observable outputs, errors, state transitions, side effects, ordering, counts, and absence of partial effects;
- isolate only dependencies irrelevant to the property being proved;
- follow project-native naming, location, framework, fixture, and helper conventions;
- control clocks, randomness, concurrency, synchronization, and fixtures deterministically;
- verify failure cleanup and useful diagnostics;
- avoid vacuous assertions and assertions that merely duplicate implementation steps;
- never delete or weaken a valid existing test just to obtain green output.

Reuse an adequate existing framework. Add only the smallest necessary project-native infrastructure when a required property cannot otherwise be expressed.

Minimal behavior-preserving testability seams are allowed, including dependency injection through an existing abstraction, pure-function extraction, an internal adapter, or controllable clock/randomness/state. Classify any production change under the repair boundary below.

## Native Execution and Failure Repair

The target project owns its runner, command, working directory, timeout, concurrency, retry behavior already encoded by the project, coverage tooling, and isolated integration environment. Do not impose an ecosystem-specific command policy.

During construction and repair, run the smallest relevant tests first. Before a pass decision, run all required layers, the complete affected-module regression, the Regression Ring, and project-wide regression when concrete coupling or project convention requires it.

A nonzero execution is development feedback, not an immediate workflow stop. Classify it:

| Classification | Action |
|---|---|
| `test-defect` | Repair the test, fixture, mock, import, syntax, or test infrastructure. |
| `local-production-defect` | Repair the proven internal implementation defect when public and cross-module contracts remain unchanged. |
| `high-risk-production-defect` | Repair only when safe, then require delta Code Review and return `TEST_NEEDS_FIXES`. |
| `environment-unavailable` | Return `TEST_BLOCKED` with the unavailable safe prerequisite. |
| `truth-unresolved` | Return `TEST_BLOCKED`; never guess the assertion. |
| `flaky-or-unreliable` | Diagnose within budget; otherwise return `TEST_BLOCKED`. |

Use at most three execution-failure repair rounds. One round is reproduce → establish truth → repair → focused verification → affected-module and Regression Ring verification. Initial test construction is not a repair round. After the third unsuccessful round:

- known remaining correction → `TEST_NEEDS_FIXES`;
- unresolved truth, reliability, safety, or environment → `TEST_BLOCKED`.

Never retry until green or weaken scope/assertions to manufacture a pass.

## Production Repair Boundary

A repair may close inside this skill only when evidence establishes that it is limited to private/internal implementation, a behavior-preserving algorithm correction, test infrastructure, a behavior-preserving testability seam, or local error handling with unchanged public obligations.

Set `review_required=true` and `review_scope=delta` when a repair affects or may affect:

- public API or observable public behavior;
- schema, migration, serialization, or generated protocol shape;
- dependency or lockfile;
- authorization, identity, secrets, permissions, or tenant isolation;
- persistence, transaction, data integrity, or concurrency semantics;
- cross-module contracts or consumer obligations;
- compatibility guarantees;
- any change whose locality cannot be established confidently.

Record completed repairs and test results, return `TEST_NEEDS_FIXES`, and stop. Do not invoke Code Review or prescribe caller routing from this skill.

## Mandatory Main-Agent Test Review

The Main Agent must personally review the complete current production-and-test state after construction and required execution. This responsibility may not be delegated.

Use at most ten completed rounds. Track report facts:

```yaml
main_review_rounds: 0
accepted_findings: 0
fixed_findings: 0
rejected_findings: 0
unresolved_findings: 0
```

Every complete round checks:

- missing behavior, acceptance criteria, Regression Ring edges, and applicable risk dimensions;
- critical low-level boundary logic;
- incorrect truth precedence or expected behavior;
- weak, vacuous, implementation-only, nondeterministic, or flaky assertions;
- over-mocking, invented contracts, and missing negative side-effect assertions;
- unjustified layer omissions or tests absent from actual native execution;
- production repairs outside this skill's safe boundary.

For each candidate finding record exactly one decision:

```text
accepted | rejected | unresolved
```

Round behavior:

```text
accepted = 0 and unresolved = 0
→ Main-Agent review converged

accepted > 0 and rounds remain
→ repair directly
→ targeted native verification
→ next complete review round

known correction remains after round ten
→ TEST_NEEDS_FIXES

truth, safety, input, or environment remains unresolved
→ TEST_BLOCKED
```

All evidence-based rejections with no unresolved item are normal convergence. Any mutation invalidates prior review and execution of that content.

## Optional Independent Test Reviewer

Only after Main-Agent review converges, read `${SKILL_DIR}/references/independent-test-review.md` and follow its complete contract.

- Create at most one Reviewer for this invocation.
- Permit at most five responses.
- Use native continuation of the exact same Reviewer after an accepted correction.
- The Reviewer is optional and available only when every structural capability in the reference is proven.
- If capability is unavailable or unproven, create no weaker replacement; record a visible strict downgrade and preserve the converged mandatory Main-Agent review.
- The Main Agent retains adjudication, mutation, execution, final result, and reporting authority.
- If response five still contains an accepted correction, return `TEST_NEEDS_FIXES`.
- If response five still contains unresolved truth, input, or safety, return `TEST_BLOCKED`.
- Never claim `TEST_PASS` for a final mutation that was not independently rechecked when independent review had already begun, unless the reference's strict downgrade rule establishes the permitted Main-Agent fallback.

## External Services and Safety

Read `${SKILL_DIR}/references/external-contract-mock-guidance.md` whenever an external service, persistence boundary, queue, filesystem, generated client, or cross-module endpoint affects the tested property.

- Prefer project-owned schemas, generated types, SDK interfaces, fixtures, and documentation.
- Use approved retrieval of public official documentation only when project artifacts are insufficient.
- Never expose secrets, private source, proprietary payloads, or repository-private data during retrieval.
- Never use production credentials, production databases/APIs/queues/storage, real user data, or destructive external operations.
- If an endpoint cannot be proven non-production, do not connect to it.
- Use contract-backed local fakes, mocks, fixtures, mock servers, containers, or project-owned isolated services.
- Record necessary unverified external behavior as a remaining risk or `TEST_BLOCKED` when it prevents the verdict.

## Final Verification

Before writing `TEST_PASS`:

1. Main-Agent review converged on the exact final state.
2. Independent review converged or was strictly and visibly downgraded under its capability contract.
3. Every required focused, module, contract/integration, applicable E2E, affected-module, and Regression Ring test passes reliably.
4. Any required project-wide regression passes.
5. No accepted correction, unresolved finding, verdict-capable scope edge, or required environment check remains.
6. No high-risk production repair awaits delta Code Review.
7. No mutation occurred after the final applicable review and execution.

## Terminal Results

Only these testing-domain outcomes are valid:

```text
TEST_PASS | TEST_NEEDS_FIXES | TEST_BLOCKED
```

- `TEST_PASS`: final reviewed state passes every required native test and no high-risk repair awaits review.
- `TEST_NEEDS_FIXES`: a known correction remains, a review/repair budget did not converge, or a completed high-risk repair requires delta Code Review.
- `TEST_BLOCKED`: expected truth, safe input, environment, execution reliability, external-target safety, or required review input prevents a safe verdict.

No conditional pass exists.

## Terminal Report and Result

Read `${SKILL_DIR}/references/test-report-template.md` before finalization. Write `test-report.md` and `test-result.json` together for every terminal outcome. The report must use the exact canonical `## Final Result` section and `- Result: <TEST_*>` marker from that template; do not rename it to `Terminal Result`, `Final Decision`, or another heading.

`test-result.json` is a terminal projection, not a checkpoint:

```json
{
  "schema_version": 1,
  "result": "TEST_PASS",
  "report": "test-report.md",
  "main_review_rounds": 3,
  "independent_review": {
    "status": "completed",
    "responses": 2,
    "downgrade_reason": null,
    "final_state_rechecked": true
  },
  "repair_rounds": 1,
  "production_changed": false,
  "review_required": false,
  "review_scope": null,
  "unresolved_items": []
}
```

Allowed `independent_review.status` values are `completed`, `downgraded`, and `not_applicable`. `completed` requires one through five responses and `final_state_rechecked=true`; `downgraded` requires zero responses, a non-empty reason, and `final_state_rechecked=false`; `not_applicable` requires zero responses, no reason, and `final_state_rechecked=false`. `review_scope` is `delta` only when `review_required=true`; otherwise it is null. The report and JSON must agree on result, review requirement, and unresolved items. If consistency cannot be established, write a truthful `TEST_BLOCKED` result rather than fabricating pass.

**HANDOFF:** Return the testing result plus `test-report.md` and `test-result.json` paths to the caller, then stop.
