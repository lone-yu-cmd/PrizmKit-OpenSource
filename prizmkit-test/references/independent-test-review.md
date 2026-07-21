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

Create at most one Reviewer for this invocation. Reuse the exact same Reviewer through native continuation. Never reuse a Reviewer from another lifecycle stage and never create a replacement with a summary to simulate continuation.

## Host Capability Gate

The gate is all-or-nothing. Before creating a Reviewer, the host must prove this semantic execution contract:

```yaml
execution_unit:
  count: 1
  access: read-only
  mutation: unavailable
  arbitrary_command_execution: unavailable
  downstream_execution: structurally-unavailable
  context_continuation: same-unit-native-resume
  workspace_observation: bounded-active-checkout-input
  model_configuration: inherit-current-session
```

Rules:

- Prompt instructions cannot satisfy a missing structural capability.
- Do not branch on platform identity, tool name, execution-unit type name, adapter output, or an allowlist.
- A general execution unit that merely promises not to mutate, execute commands, or delegate is ineligible while those capabilities remain available.
- The Reviewer inherits the current session's model configuration.
- If any capability is missing or unproven, create no Reviewer and use Strict Downgrade.

## Bounded Immutable Review Input

Before every response, the Main Agent captures a complete input that remains immutable for that response:

```text
test-review-input
├── manifest
│   ├── response number and input identity
│   ├── exact changed production and test paths
│   ├── relevant unchanged path inventory
│   └── consistency markers
├── change context
│   ├── requirement and acceptance criteria
│   ├── current production change
│   └── applicable project rules
├── coverage context
│   ├── affected business module
│   ├── observable behaviors
│   ├── risk and boundary assessment
│   └── Regression Ring
├── test context
│   ├── existing, added, and modified tests
│   ├── fixtures, mocks, and contracts
│   ├── selected test layers
│   └── native execution results
└── targeted supporting context
    ├── relevant callers and consumers
    ├── shared schemas and contracts
    └── necessary public official contract excerpts
```

The Reviewer does not run Git, tests, builds, network calls, or broad repository discovery. The Main Agent captures authoritative current state. Do not include secrets, credentials, production data, or unrelated private repository content.

Before ordinary review, the Reviewer verifies that manifest and content agree. Missing paths, unexplained changed files, stale content, or mixed-response input produces `REVIEW_BLOCKED`, never partial success.

## Initial Reviewer Prompt

Instantiate bracketed fields and retain every execution boundary.

```text
You are the sole independent Test Reviewer for this PrizmKit Test invocation.

Purpose:
Objectively determine whether the complete current project-native tests credibly prove the affected business module and Regression Ring and whether the tests themselves are valid. You are not an adversary and are not required to disagree. Return NO_CORRECTION_NEEDED when no evidence-backed correction is justified.

Response:
This is response [RESPONSE_NUMBER] of a maximum five responses.
Review-input identity: [INPUT_ID]
Manifest: [MANIFEST]
Change context: [CHANGE_CONTEXT]
Coverage context: [COVERAGE_CONTEXT]
Test context: [TEST_CONTEXT]
Targeted supporting context: [SUPPORTING_CONTEXT]

Execution boundaries:
- Complete this review personally.
- Do not create, schedule, resume, continue, request, or coordinate another execution unit.
- Do not ask the Main Agent to create a helper.
- Do not re-enter orchestration, delegation, another review workflow, or an equivalent process.
- Do not modify, create, delete, rename, stage, commit, or otherwise mutate files.
- Do not execute commands, tests, builds, network calls, or any operation that can change state.
- Read only the bounded review input and explicitly represented targeted supporting material.
- Do not perform broad repository discovery or a full repository scan.
- Report only corrections supported by a concrete target and evidence.
- Do not invent an issue merely to return feedback.
- Return REVIEW_BLOCKED rather than delegate or provide an incomplete success result.
- Do not expose private reasoning traces. Return only the required output.

First validate input consistency. Then review:
- requirement and acceptance-criteria coverage;
- complete observable behavior of the affected module;
- critical low-level logic and exact boundaries;
- functional, boundary, error, state, side-effect, permission, concurrency, idempotency, time, dependency, and consumer risks;
- Regression Ring completeness;
- selection of focused, module, contract/integration, applicable E2E, module-regression, and Regression Ring layers;
- assertion strength and observable effect;
- vacuous or false-positive tests and tests that cannot fail for the intended defect;
- over-mocking or removal of production composition;
- mock fidelity to project or public official contracts;
- nondeterminism and flakiness risk;
- native execution results matching the declared scope;
- production repairs that require delta Code Review;
- remaining risks being stated honestly.

Do not rewrite the requirement, modify code, execute tests, or perform broad exploration.
Return exactly one result using the Reviewer Output Protocol.
```

## Resume Prompt

Resume the exact same Reviewer. Do not create a new Reviewer with this prompt.

```text
Continue as the same independent Test Reviewer.

Response:
This is response [RESPONSE_NUMBER] of a maximum five responses.
New review-input identity: [INPUT_ID]
New manifest: [MANIFEST]
Current change context: [CHANGE_CONTEXT]
Current coverage context: [COVERAGE_CONTEXT]
Current test context: [TEST_CONTEXT]
Current supporting context: [SUPPORTING_CONTEXT]
Previously accepted corrections: [ACCEPTED_CORRECTIONS_OR_NONE]
Repairs actually made: [REPAIRS_OR_NONE]
Main-Agent native verification: [VERIFICATION]
Previously rejected corrections and rejection evidence: [REJECTIONS_OR_NONE]
Unresolved items: [UNRESOLVED_OR_NONE]

All initial execution boundaries and the Reviewer Output Protocol remain mandatory. Review the complete current state, not only the repair and not the superseded input. Do not repeat a rejected correction unless the new state invalidates its rejection evidence. Validate the new input before ordinary review and return exactly one result.
```

## Reviewer Output Protocol

Return exactly one form. Do not add severity, confidence, dimension, workflow routing, or acceptance fields.

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
7. If responses remain, capture the complete fresh input and natively resume the exact same Reviewer. Never create a replacement.
8. If response five contains an accepted correction, do not repair and claim pass without independent recheck. Return `TEST_NEEDS_FIXES` with the known correction.
9. If response five contains an unresolved correction or `REVIEW_BLOCKED` that cannot be corrected safely, return `TEST_BLOCKED`.
10. Stop sending messages when the review converges, reaches its limit, or becomes blocked. Explicitly terminate the unit only when the host safely supports it.

## Strict Downgrade

Use Strict Downgrade when:

- required capability is unavailable or unproven before creation;
- creation fails before a valid response;
- a required structural capability disappears;
- exact native resume fails after mutation.

Behavior:

1. Never create a weaker or replacement Reviewer.
2. Never create a fresh Reviewer with a summary; summary context is not native continuation.
3. Before creation or before any valid response, record the downgrade and preserve the converged mandatory Main-Agent review.
4. When resume fails after mutation, the old independent result no longer describes the final state. Rerun mandatory Main-Agent review over the mutation within its remaining budget, record the downgrade, and set `final_state_rechecked=false` for independent review.
5. A semantic `REVIEW_BLOCKED` caused by incomplete or inconsistent required input is not silently downgraded. Correct the input and resume the same Reviewer within budget, or return `TEST_BLOCKED`.
6. Strict Downgrade is visible reduced assurance, not a new testing result and not permission to weaken Main-Agent review or native test execution.

## Report Recording

Record:

- capability gate outcome and downgrade reason;
- each response number `1..5`, input identity, result, and correction count;
- every Main-Agent adjudication and its evidence;
- actual repair and native verification;
- whether the exact final state was independently rechecked.

The report remains the human-readable test artifact. Do not create a separate Reviewer state machine or evidence package.
