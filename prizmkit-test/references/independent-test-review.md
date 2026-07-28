# Independent Test Review

## Purpose

Run one optional independent semantic review after mandatory Main-Agent test construction, execution, and review have converged. The Reviewer determines whether the complete current tests credibly prove the affected business module and Regression Ring and whether the tests themselves are valid.

The Reviewer is not required to disagree. It returns `NO_CORRECTION_NEEDED` when no evidence-backed correction is justified.

This reference is complete within `prizmkit-test`. Do not depend on another skill's prompt or a platform-generated Reviewer role.

## Required Ordering and Budget

```text
Main Agent builds and executes project-native tests
→ mandatory Main-Agent test review: maximum ten completed rounds
→ optional independent Test Reviewer: maximum five responses
→ final native regression
→ TEST_PASS | TEST_NEEDS_FIXES | TEST_BLOCKED
```

Keep at most one Reviewer active for this invocation and permit at most one replacement. Prefer native continuation and never reuse a Reviewer from another invocation. A compliant replacement may continue the same shared response budget only with complete latest state, never only a conversation summary.

## Host Capability Gate

The gate is all-or-nothing. Before creating a Reviewer, inspect the current host's actual execution-unit configuration and prove this semantic contract without relying on platform identity or implementation-specific parameters:

```yaml
execution_unit:
  concurrency: at-most-one-active-reviewer
  workspace_access: read-only-active-checkout
  mutation: structurally-unavailable
  command_execution: structurally-unavailable
  network_access: structurally-unavailable
  external_process_execution: structurally-unavailable
  downstream_execution: structurally-unavailable
  model_configuration: inherit-current-session
  scope_expansion: concrete-coupling-only
  continuation: prefer-same-unit
  replacement: compliant-replacement-allowed
```

Rules:

- Prompt instructions cannot satisfy a missing structural capability.
- Do not branch on platform identity, provider, tool name, command name, execution-unit type name, adapter output, CLI parameter, or an allowlist.
- The Reviewer cannot create, modify, delete, rename, stage, or commit files; execute shell, Git, tests, builds, network calls, or external processes; or create, invoke, resume, or coordinate downstream execution units.
- A general execution unit that merely promises to stay read-only is ineligible while prohibited capabilities remain available.
- The Reviewer inherits the current session's model configuration.
- If any capability is missing or unproven, create no Reviewer and use Strict Downgrade.

## Stage-Specific Review Input

Use the exact caller-supplied testing identity on every response:

```text
artifact_dir: [EXACT_ARTIFACT_DIR]
spec_path: [EXACT_SPEC_PATH]
plan_path: [EXACT_PLAN_PATH]
checkout_root: [ACTIVE_CHECKOUT_ROOT]
```

These paths remain authoritative even when ignored by Git. Never ask the Reviewer to discover a latest artifact or guess among multiple `spec.md` and `plan.md` files.

The Main Agent supplies:

- original requirement and confirmed clarifications;
- exact artifact, spec, and plan paths plus current contents;
- complete current production-and-test change;
- affected business module, observable behaviors, applicable risks, Regression Ring, and the authority-driven evidence-obligation classification;
- existing, added, and modified tests, fixtures, mocks, schemas, contracts, selected layers, and the complete boundary/test-double inventory with authority, fidelity, removed composition, proof limits, preserving evidence, and verdict impact;
- native test commands and results executed by Main Agent;
- testing-local repairs;
- response number and total budget;
- prior adjudication and actual corrections on continuation or replacement.

The Reviewer may use structurally read-only checkout access to inspect production code, tests, fixtures, schemas, callers, consumers, and contracts only through concrete coupling evidence. It cannot run Git, tests, builds, network calls, or external processes and must not perform an unconditional repository-wide scan. Do not include secrets, credentials, production data, or unrelated private content. Missing or inconsistent required input produces `REVIEW_BLOCKED`, never partial success.

## Initial Reviewer Prompt

Instantiate bracketed fields and retain every execution boundary.

```text
You are the sole independent Test Reviewer for this PrizmKit Test invocation.

Purpose:
Objectively determine whether the complete current project-native tests credibly prove the affected business module and Regression Ring and whether the tests themselves are valid. You are not an adversary and are not required to disagree. Return NO_CORRECTION_NEEDED when no evidence-backed correction is justified.

Response:
This is response [RESPONSE_NUMBER] of a maximum five responses.
Artifact directory: [ARTIFACT_DIR]
Specification path and content: [SPEC_PATH_AND_CONTENT]
Plan path and content: [PLAN_PATH_AND_CONTENT]
Checkout root: [CHECKOUT_ROOT]
Requirement and clarifications: [REQUIREMENT_CONTEXT]
Current production-and-test change: [CURRENT_CHANGE]
Coverage context: [COVERAGE_CONTEXT]
Test context and Main-Agent execution results: [TEST_CONTEXT]

Execution boundaries:
- Complete this review personally.
- Do not create, schedule, resume, continue, request, or coordinate another execution unit.
- Do not ask the Main Agent to create a helper.
- Do not re-enter delegation or another review process.
- Do not modify, create, delete, rename, stage, commit, or otherwise mutate files.
- Do not execute shell, Git, tests, builds, network calls, external processes, or any operation that can change state.
- Use read-only checkout access only for concrete module, caller, consumer, schema, type, configuration, fixture, test, or contract coupling.
- Do not perform unconditional repository discovery or a full repository scan.
- Report only corrections supported by a concrete target and evidence.
- Do not invent an issue merely to return feedback.
- Return REVIEW_BLOCKED rather than delegate or provide an incomplete success result.
- Do not expose private reasoning traces. Return only the required output.

First validate input consistency. Then review:
- requirement and acceptance-criteria coverage;
- every evidence obligation defaulting to automated-required unless a confirmed specification, acceptance criterion, or explicit caller decision authorizes non-verdict manual/external deferral;
- any unsupported obligation downgrade based only on difficulty, duration, cost, agent inability, or unavailable safely constructible tooling;
- authorized deferred external or manual evidence remaining visible and unproven without being treated as a verdict blocker or passed behavior;
- every out-of-scope diagnostic satisfying the exact current-checkout path, coupling, determinism, cause, and project-rule gate;
- complete observable behavior of the affected module;
- critical low-level logic and exact boundaries;
- functional, boundary, error, state, side-effect, permission, concurrency, idempotency, time, dependency, and consumer risks;
- Regression Ring completeness;
- selection of focused, module, contract/integration, applicable E2E, module-regression, and Regression Ring layers;
- assertion strength and observable effect;
- vacuous or false-positive tests and tests that cannot fail for the intended defect;
- every producer-consumer boundary and test double having boundary-appropriate contract authority and fidelity proof;
- any consumer-authored ideal fixture being treated only as consumer expectation unless independently contract-validated;
- Provider Contract Tests containing raw Provider serialization evidence, including risk-relevant omitted, null, empty, zero, type, and field-name behavior;
- each Browser Test being classified from actual production composition, with intercepted critical APIs classified as Mock Browser rather than Full-stack E2E;
- no test claim exceeding the property its test double can prove and no verdict-capable composition being removed without preserving contract, integration, or Full-stack evidence;
- each relevant test being able to fail while the target defect exists;
- state-changing workflows covering commit, cancellation, failure recovery, reload or re-entry, retry/conflict/idempotency, and repeated operation semantics;
- nondeterminism and flakiness risk;
- native execution results matching the declared scope;
- production defects or attempted repairs outside the permitted testing-local repair boundary;
- remaining risks being stated honestly.

Return `CORRECTION_NEEDED` when a verdict-relevant producer-consumer combination is replaced by a test double without authoritative fidelity proof and composition-preserving evidence, when a test-layer claim exceeds the actual composition executed, when an unsupported obligation downgrade weakens required automation, or when authorized deferred external or manual evidence is the sole reason an otherwise complete automated verdict is blocked.

Do not rewrite the requirement, modify code, execute tests, or perform broad exploration.
Return exactly one result using the Reviewer Output Protocol.
```

## Resume Prompt

Prefer native continuation of the same Reviewer. If unavailable, use this complete prompt for one compliant replacement under the replacement rules below.

```text
Continue as the same independent Test Reviewer.

Response:
This is response [RESPONSE_NUMBER] of a maximum five responses.
Continuation mode: [NATIVE_OR_REPLACEMENT]
Artifact directory: [ARTIFACT_DIR]
Specification path and content: [SPEC_PATH_AND_CONTENT]
Plan path and content: [PLAN_PATH_AND_CONTENT]
Checkout root: [CHECKOUT_ROOT]
Requirement and clarifications: [REQUIREMENT_CONTEXT]
Current production-and-test change: [CURRENT_CHANGE]
Current coverage context: [COVERAGE_CONTEXT]
Current test context and Main-Agent execution results: [TEST_CONTEXT]
Previously accepted corrections: [ACCEPTED_CORRECTIONS_OR_NONE]
Repairs actually made: [REPAIRS_OR_NONE]
Main-Agent native verification: [VERIFICATION]
Previously rejected corrections and rejection evidence: [REJECTIONS_OR_NONE]
Unresolved items: [UNRESOLVED_OR_NONE]

All initial execution boundaries and the Reviewer Output Protocol remain mandatory. Review the complete current state, not only the repair and not the superseded input. Do not repeat a rejected correction unless the new state invalidates its rejection evidence. Validate the new input before ordinary review and return exactly one result.
```

## Reviewer Output Protocol

Return exactly one form. Do not add severity, confidence, dimension, caller routing, or acceptance fields.

### No Correction Needed

```markdown
### Result: NO_CORRECTION_NEEDED

### Corrections
None.

### Summary
<one or two sentences confirming the reviewed coverage and test validity>
```

### Correction Needed

```markdown
### Result: CORRECTION_NEEDED

### Corrections

#### Correction 1
- Target: <behavior, risk, test, contract, caller, or execution>
- Problem: <what is missing or invalid>
- Evidence: <concrete basis or reproducible scenario>
- Correction: <required test or coverage correction>

### Summary
<one or two sentences describing the current state>
```

Every correction contains only `Target`, `Problem`, `Evidence`, and `Correction`.

### Review Blocked

```markdown
### Result: REVIEW_BLOCKED

### Blocker
- Target: <missing or inconsistent review input>
- Problem: <why complete review cannot be performed>
- Evidence: <concrete mismatch or missing fact>
- Correction: <what would unblock review>

### Summary
No review verdict was produced.
```

`REVIEW_BLOCKED` is an internal Reviewer result, not the final testing result.

## Main-Agent Adjudication

The Main Agent verifies every proposed correction and records exactly one decision:

| Decision | Meaning | Action |
|---|---|---|
| `accepted` | Evidence proves an in-scope correction is required. | Repair tests or permitted production code, execute targeted and required regression tests, and perform a complete Main-Agent review round. |
| `rejected` | Code, contracts, tests, execution output, or rules disprove the problem. | Record concrete rejection evidence and make no change. |
| `unresolved` | Truth, correctness, input completeness, or safe repair cannot be established. | Return `TEST_BLOCKED`, or `TEST_NEEDS_FIXES` only when a known correction remains. |

The Reviewer never mutates files and cannot overrule adjudication.

Independent review converges when:

1. the Reviewer returns `NO_CORRECTION_NEEDED`; or
2. every correction in the current response is rejected with concrete evidence and no unresolved item remains.

## Response Algorithm

1. Run only after mandatory Main-Agent review converges with no unresolved finding.
2. Apply the Host Capability Gate.
3. If eligible, capture response-one input and create exactly one Reviewer with the Initial Reviewer Prompt.
4. Validate the response against the output protocol and record it in the report.
5. Adjudicate every correction and record accepted, rejected, or unresolved with evidence.
6. For accepted corrections, the Main Agent repairs the current workspace, executes focused and required regressions, then performs a complete Main-Agent review round over the new state within its ten-round budget.
7. If responses remain, prepare the complete latest Test input and prefer native continuation. If unavailable or failed and no replacement has been used in this stage, create one compliant replacement only after the prior Reviewer is no longer active; reapply the full gate and continue with the next response number.
8. A replacement receives complete current state and all prior adjudication, never only a conversation summary. Replacement does not reset the five-response budget. At most one replacement may be created in the stage, and only one Reviewer may be active.
9. If response five contains an accepted correction, do not repair and claim pass without independent recheck. Return `TEST_NEEDS_FIXES` with the known correction.
10. If response five contains an unresolved correction or `REVIEW_BLOCKED` that cannot be corrected safely, return `TEST_BLOCKED`.
11. Stop sending messages when the review converges, reaches its limit, or becomes blocked. Explicitly terminate the unit only when the host safely supports it.

## Strict Downgrade

Use Strict Downgrade when a required capability is unavailable or unproven, creation fails before a valid response, prohibited capability appears, the prior Reviewer may still be active, or no compliant continuation/replacement can be established.

Behavior:

1. Never create a weaker Reviewer whose prohibited capabilities remain available.
2. Prefer native continuation, but permit a fresh compliant replacement with complete latest input and prior adjudication; a summary alone is insufficient.
3. Before creation or before any valid response, record downgrade and preserve the converged mandatory Main-Agent review.
4. Creation failure without a response does not consume response budget; a produced malformed response follows the existing response-budget rule.
5. When continuation and compliant replacement both fail after mutation, rerun mandatory Main-Agent review over the mutation within remaining budget, record downgrade, and set `final_state_rechecked=false`.
6. A semantic `REVIEW_BLOCKED` caused by incomplete required input is not silently downgraded. Correct input within remaining shared budget using native continuation or compliant replacement, or return `TEST_BLOCKED`.
7. Strict Downgrade is visible reduced assurance, not a new testing result and not permission to weaken Main-Agent review or native execution.

## Report Recording

Record:

- capability gate outcome and downgrade reason;
- each response number `1..5`, input identity, result, and correction count;
- every Main-Agent adjudication and its evidence;
- actual repair and native verification;
- boundary authority/fidelity, evidence-obligation authority, unsupported downgrade, deferred-evidence visibility, diagnostic-gate, removed-composition, proof-limit, preserving-evidence, layer-classification, and mutation-lifecycle corrections;
- whether the exact final state was independently rechecked;
- capability basis, continuation mode (`native`, `replacement`, `mixed`, or `not-applicable`), and replacement count.

The report remains the human-readable test artifact. Do not create a separate Reviewer state machine or evidence package.
