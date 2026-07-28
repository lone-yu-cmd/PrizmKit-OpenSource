---
name: "prizmkit-test"
description: "Test one supplied current change with project-native affected-module and Regression Ring coverage. Use for contract testing, test-double fidelity, consumer/provider compatibility, browser and Full-stack E2E, persistence re-entry, and cross-boundary integration; returns TEST_PASS, TEST_NEEDS_FIXES, or TEST_BLOCKED with stage-owned report/result artifacts. (project)"
---

# PrizmKit Test

`/prizmkit-test` is the independent testing stage for the current workspace. It understands the affected business behavior, fills project-native test gaps, executes the tests, repairs valid failures, reviews the final tests, and reports a truthful testing-domain result.

It does not build an evidence package, prove historical TDD order, or validate a previous checkout.

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

After writing its result, this Skill stops. It owns only testing-local source/test repairs and its two terminal artifacts. It does not invoke another Skill.

## Inputs and Outputs

| Parameter | Required | Description |
|---|---|---|
| `scope` | No | `full-project`, `module:<name>`, `feature:<slug>`, or `this-change`. Defaults to `this-change` when current change context exists, otherwise `full-project`. |
| `artifact_dir` | Yes | Exact caller-supplied project-relative directory for the two terminal artifacts and any available specification, plan, and behavior context. Reuse it unchanged. |
| `changed_files` | No | Explicit current changed paths. Highest-priority scope locator. |
| `diff_base` | No | Git comparison base when explicit changed paths are absent. |
| `test_commands` | No | Project-native commands when repository conventions are ambiguous. |

Resolve `artifact_dir` before Test execution. In interactive use, ask the user to confirm an exact project-relative directory when omitted. In non-interactive use, a missing or unsafe directory is a response-only `TEST_BLOCKED` precondition failure: create no fallback directory or artifact and report that the caller must retry with `artifact_dir`. This precondition rejection is the sole case where terminal files cannot be written because their required identity is absent.

For every invocation that passes input resolution, write exactly two terminal artifacts in the supplied `artifact_dir`:

```text
{artifact_dir}/
├── test-report.md
└── test-result.json
```

Do not create `.prizmkit/test/evidence/`, manifests, hashes, attestations, package state records, or test-internal checkpoints.

## Context Loading and Scope Resolution

1. Reuse current requirement and workspace context already loaded by the Main Agent.
2. Load `root.prizm`, the relevant module indexes, and the applicable detail docs before modifying source or tests.
3. Inspect current staged, unstaged, untracked, deleted, and renamed paths. Changed lines locate impact but never define completeness.
4. Read the available specification, acceptance criteria, plan, and caller-supplied behavior context only as needed to establish expected behavior.
5. Inspect manifests, runner configuration, CI conventions, existing test assertions, fixtures, fakes, mocks, contracts, and coverage support.
6. If necessary scope cannot be determined safely, report the precise missing input and return `TEST_BLOCKED` in the resolved artifact pair.

Do not infer the active requirement solely from the name of an old artifact directory. Do not use a historical worktree, second checkout, mutation proof, baseline-failure proof, or test overlay.

## Evidence Obligation Classification

Read the verdict-relevance rules in `${SKILL_DIR}/references/test-coverage-model.md`. Before assigning verdict impact, classify every material acceptance criterion, composition check, environment prerequisite, and failed diagnostic:

- `automated-required`: the default; missing safe verdict evidence blocks `TEST_PASS`;
- `manual-external-nonblocking`: a confirmed specification, acceptance criterion, or explicit caller decision says physical, public, production-account, or human-confirmation evidence may remain pending after the automated software-change verdict;
- `out-of-scope-diagnostic`: a current-checkout failure is non-blocking only when affected-module and Regression Ring verification pass, it is outside changed paths and concrete coupling, it is deterministic, and no changed dependency, configuration, generated artifact, or shared contract caused it.

The default is `automated-required`. Difficulty, duration, cost, agent inability, or absent safely constructible local tooling or isolated services cannot downgrade an `automated-required` obligation. An explicit requirement or project rule that makes broad validation mandatory remains authoritative. Ambiguous authority or verdict relevance remains blocking. Do not claim historical or pre-existing provenance without forbidden baseline comparison.

Keep authorized deferred evidence visible without claiming it passed or authorizing release/deployment. It is not an unresolved testing-domain item; `TEST_PASS` keeps `unresolved_items` empty when all automated-required obligations pass.

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
→ module/component or UI component
→ consumer/provider contract or integration
→ Mock Browser or Full-stack E2E according to actual composition
→ complete affected-module regression
→ Regression Ring verification
```

Browser execution alone is not Full-stack E2E. Do not mechanically test every private function. Add direct focused tests for critical low-level logic when complexity, boundaries, risk, or failure localization justify them; otherwise prove it through public behavior.

## Test Construction

Read `${SKILL_DIR}/references/test-coverage-model.md` and, whenever serialization, a producer-consumer boundary, or any test double replaces a producer or consumer, `${SKILL_DIR}/references/boundary-contract-and-test-double-guidance.md`.

Expected behavior follows boundary-specific authority:

1. confirmed specification and acceptance criteria;
2. machine-readable wire contract;
3. traceably generated type, client, server stub, or fixture;
4. provider raw-wire contract evidence or authorized isolated observation;
5. provider implementation, locked SDK behavior, and matching official documentation;
6. trusted existing tests, callers and consumers, consumer-local types/fixtures/mocks, and other current implementation evidence.

Lower-authority material cannot override higher-authority truth or prove a property outside its boundary. Conflicts that cannot be resolved are `TEST_BLOCKED`; do not preserve a possible implementation defect as a characterization test.

Tests must:

- assert observable outputs, errors, state transitions, side effects, ordering, counts, and absence of partial effects;
- isolate only dependencies irrelevant to the property being proved;
- follow project-native naming, location, framework, fixture, and helper conventions;
- control clocks, randomness, concurrency, synchronization, and fixtures deterministically;
- verify failure cleanup and useful diagnostics;
- avoid vacuous assertions and assertions that merely duplicate implementation steps;
- never delete or weaken a valid existing test just to obtain green output.

## Boundary Contract and Composition Gate

A test cannot prove a property that depends on production composition it replaces. Before test construction and again before `TEST_PASS`:

1. Inventory every verdict-relevant mock, fake, fixture, route interception, mock server, container, emulator, or isolated service that crosses or replaces a producer-consumer boundary.
2. Record its producer, consumer, boundary/protocol, contract authority, fidelity proof, composition removed, property not proven, composition-preserving test, and remaining risk.
3. Treat consumer-local types, fixtures, and mocks as expectations, not provider truth, unless they are generated from or validated against the authoritative boundary contract.
4. Classify tests by actual composition. An API-intercepted browser test is a Mock Browser Test, not Full-stack E2E.
5. Require risk-relevant Provider Contract Tests to inspect raw wire payload before provider-owned deserialization.
6. For any verdict-capable serialization or multi-layer risk in removed composition, require provider/consumer contract evidence, a composition-preserving integration test, or a Full-stack path appropriate to the risk and keeping the defect-bearing boundary real.
7. For state-changing workflows, verify commit point, cancellation, pending/duplicate protection, failure recovery, reload or re-entry, retry/conflict/idempotency, and downstream consumption.

If composition-preserving evidence required by an `automated-required` obligation cannot run in a proven safe isolated environment, return `TEST_BLOCKED`. Never substitute a lower-layer green test or downgrade the proof requirement. Explicitly authorized `manual-external-nonblocking` evidence remains reported as unproven but does not become part of the current automated verdict.

Reuse an adequate existing framework. Add only the smallest necessary project-native infrastructure when a required property cannot otherwise be expressed.

Minimal behavior-preserving testability seams are allowed, including dependency injection through an existing abstraction, pure-function extraction, an internal adapter, or controllable clock/randomness/state. Classify any production change under the repair boundary below.

## Native Execution and Failure Repair

The target project owns its runner, command, working directory, timeout, concurrency, retry behavior already encoded by the project, coverage tooling, and isolated integration environment. Do not impose an ecosystem-specific command policy.

During construction and repair, run the smallest relevant tests first. Before a pass decision, run all required layers, the complete affected-module regression, the Regression Ring, and project-wide regression when concrete coupling or project convention requires it.

A nonzero execution is testing feedback, not an immediate terminal result. Classify it:

| Classification | Action |
|---|---|
| `test-defect` | Repair the test, fixture, mock, import, syntax, or test infrastructure. |
| `local-production-defect` | Repair the proven internal implementation defect when public and cross-module contracts remain unchanged. |
| `high-risk-production-defect` | Do not repair it in this invocation; record the proven defect and return `TEST_NEEDS_FIXES`. |
| `environment-unavailable` | Return `TEST_BLOCKED` when the unavailable safe prerequisite is `automated-required`; record an authorized `manual-external-nonblocking` prerequisite without treating it as an execution failure. |
| `truth-unresolved` | Return `TEST_BLOCKED`; never guess the assertion. |
| `flaky-or-unreliable` | Diagnose within budget; otherwise return `TEST_BLOCKED`. |

Use at most three execution-failure repair rounds. One round is reproduce → establish truth → repair → focused verification → affected-module and Regression Ring verification. Initial test construction is not a repair round. After the third unsuccessful round:

- known remaining correction → `TEST_NEEDS_FIXES`;
- unresolved truth, reliability, safety, or environment → `TEST_BLOCKED`.

Never retry until green or weaken scope/assertions to manufacture a pass.

## Production Repair Boundary

A repair may close inside this Skill only when evidence establishes that it is limited to private/internal implementation, a behavior-preserving algorithm correction, test infrastructure, a behavior-preserving testability seam, or local error handling with unchanged public obligations.

Do not perform the repair in this invocation when it affects or may affect:

- public API or observable public behavior;
- schema, migration, serialization, or generated protocol shape;
- dependency or lockfile;
- authorization, identity, secrets, permissions, or tenant isolation;
- persistence, transaction, data integrity, or concurrency semantics;
- cross-module contracts or consumer obligations;
- compatibility guarantees;
- any change whose locality cannot be established confidently.

Record the defect evidence and required correction, return `TEST_NEEDS_FIXES`, and stop. Do not prescribe or execute work outside this testing invocation.

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
- every evidence-obligation classification, its authority, unsupported obligation downgrade, and any deferred evidence incorrectly treated as passed or verdict-capable;
- critical low-level boundary logic;
- incorrect truth precedence or expected behavior;
- weak, vacuous, implementation-only, nondeterministic, or flaky assertions;
- complete boundary/test-double inventory, boundary-appropriate authority, fidelity proof, and consumer-authored ideal fixtures not being treated as provider truth;
- Provider raw-wire assertions, test-layer labels matching actual composition, and Browser Tests with intercepted critical APIs not being called Full-stack E2E;
- any test that would still pass with the target defect, any verdict-capable composition removed without preserving evidence, and missing negative side-effect assertions;
- state-changing workflow commit, cancellation, failure recovery, reload/re-entry, retry/conflict/idempotency, and repeated-operation coverage;
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

- Keep at most one Reviewer active for this invocation and permit at most one compliant replacement.
- Permit at most five responses.
- Prefer native continuation after an accepted correction; when unavailable, permit one compliant replacement with complete latest Test state, prior adjudication, exact artifact/spec/plan paths, and the same remaining response budget.
- The Reviewer is optional and available only when every structural capability in the reference is proven.
- If capability is unavailable or unproven, create no weaker Reviewer; record a visible strict downgrade and preserve the converged mandatory Main-Agent review.
- The Main Agent retains adjudication, mutation, execution, final result, and reporting authority.
- If response five still contains an accepted correction, return `TEST_NEEDS_FIXES`.
- If response five still contains unresolved truth, input, or safety, return `TEST_BLOCKED`.
- Never claim `TEST_PASS` for a final mutation that was not independently rechecked when independent review had already begun, unless the reference's strict downgrade rule establishes the permitted Main-Agent fallback.

## Boundary Contracts and External Safety

Read `${SKILL_DIR}/references/boundary-contract-and-test-double-guidance.md` for internal and external APIs, cross-module endpoints, persistence, queues, filesystems, caches, generated clients/servers, and any test double replacing a producer or consumer.

- Select authority for the property at the actual boundary; a database schema does not independently prove HTTP or message serialization.
- Use approved retrieval of public official documentation only when higher-authority project artifacts are insufficient.
- Never expose secrets, private source, proprietary payloads, or repository-private data during retrieval.
- Never use production credentials, production databases/APIs/queues/storage, real user data, or destructive external operations.
- If an endpoint cannot be proven non-production, do not connect to it.
- Use contract-backed local doubles or project-owned isolated services only within their stated proof boundary.
- Missing fidelity or composition evidence for an `automated-required` obligation produces `TEST_BLOCKED`, not a conditional pass; authorized deferred external/manual evidence stays visible and unproven.

## Final Verification

Before writing `TEST_PASS`:

1. Main-Agent review converged on the exact final state.
2. Independent review converged or was strictly and visibly downgraded under its capability contract.
3. Every `automated-required` focused, module/component, consumer/provider contract, integration, actual-composition E2E, affected-module, and Regression Ring test passes reliably.
4. Every automated-verdict test double has boundary-appropriate authority and fidelity proof, and every test-layer claim matches actual composition.
5. Every automated-verdict property in removed composition has composition-preserving evidence; applicable Provider Contract Tests assert raw wire output and state-changing workflows cover the required lifecycle.
6. Every regression concretely coupled to the change passes, and every project-wide command made a whole-result completion gate by a confirmed requirement or explicit project rule passes; only other broad failures may use `out-of-scope-diagnostic`.
7. No accepted correction, unresolved finding, automated-verdict scope edge, missing required fidelity/composition proof, or required environment check remains.
8. Every `manual-external-nonblocking` item is authoritatively classified, visibly unproven, and separate from release/deployment authorization.
9. No high-risk production defect or correction remains, and no mutation occurred after final review and execution.

## Terminal Results

Only these testing-domain outcomes are valid:

```text
TEST_PASS | TEST_NEEDS_FIXES | TEST_BLOCKED
```

- `TEST_PASS`: final reviewed state passes every `automated-required` obligation and no high-risk correction remains; authorized deferred external/manual evidence may remain visibly unproven.
- `TEST_NEEDS_FIXES`: a known correction remains or a testing-local review/repair budget did not converge.
- `TEST_BLOCKED`: expected truth, safe input, required automated environment, execution reliability, external-target safety, or required review input prevents a safe verdict.

No conditional pass exists. A separate project-native status such as `MANUAL_VERIFICATION_REQUIRED` describes deferred evidence, not a fourth Test result or proof that external/manual behavior passed.

## Terminal Report and Result

Read `${SKILL_DIR}/references/test-report-template.md` before finalization. After required input resolution, write `test-report.md` and `test-result.json` together for every terminal outcome. The report must use the exact canonical `## Final Result` section and `- Result: <TEST_*>` marker from that template; do not rename it to `Terminal Result`, `Final Decision`, or another heading.

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
  "unresolved_items": []
}
```

Allowed `independent_review.status` values are `completed`, `downgraded`, and `not_applicable`. `completed` requires one through five responses and `final_state_rechecked=true`; `downgraded` requires zero responses, a non-empty reason, and `final_state_rechecked=false`; `not_applicable` requires zero responses, no reason, and `final_state_rechecked=false`. `TEST_PASS` requires an empty `unresolved_items`; each non-pass result requires at least one exact unresolved correction or blocker. The report and JSON must agree on result, production-change diagnostics, and unresolved items. If consistency cannot be established, write a truthful `TEST_BLOCKED` result rather than fabricating pass.

Return only the testing result, `test-report.md`/`test-result.json` paths, execution summary, repair diagnostics, and unresolved items.
