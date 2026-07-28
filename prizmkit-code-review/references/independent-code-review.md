# Independent Code Review

## Purpose

Run one optional independent correctness review after the mandatory Main-Agent review and repair loop has converged. The Reviewer determines whether the complete current implementation correctly satisfies the requirement and plan. It is not required to disagree and must return `NO_CORRECTION_NEEDED` when no correction is justified.

This reference is complete within `prizmkit-code-review`. Do not depend on another skill's prompt or a platform-generated Reviewer role.

## Required Ordering and Budget

```text
Implementation complete
→ mandatory Main-Agent review and repair loop: maximum ten rounds
→ optional independent Code Reviewer: maximum five responses
→ PASS or NEEDS_FIXES
```

The independent budget does not replace, reduce, or extend the Main-Agent loop. Keep at most one Reviewer active, permit at most one replacement for this Code Review stage, and never reuse either unit in another stage.

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
- The decision must not branch on platform identity, provider, tool name, command name, execution-unit type name, adapter output, CLI parameter, or an allowlist.
- The Reviewer cannot create, modify, delete, rename, stage, or commit files; execute shell, Git, tests, builds, network calls, or external processes; or create, invoke, resume, or coordinate downstream execution units.
- A general execution unit that merely promises to remain read-only is ineligible while prohibited capabilities remain available.
- The Reviewer inherits the current session's model configuration.
- If any capability is missing or cannot be proven, create no Reviewer and use Strict Downgrade.

## Review Input

Use the exact caller-supplied review identity on every response:

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
- current workspace status after the Main Agent classifies default exclusions;
- staged and unstaged tracked changes in the ordinary correctness scope;
- relevant in-scope untracked, deleted, and renamed content;
- exact default-excluded changed paths as visible exclusion metadata, never as reviewed content;
- implementation task completion and targeted verification results;
- response number and total budget;
- prior adjudication, actual repairs, and repair verification on continuation or replacement.

The Main Agent runs Git and captures authoritative current-change state, then applies the Skill's default `.prizmkit/**` and generated host-support exclusions before supplying the correctness change. The Reviewer may read the exact supplied spec/plan artifacts but must not inspect other `.prizmkit` content. It may use structurally read-only checkout access to inspect unchanged callers, consumers, contracts, schemas, types, configurations, fixtures, or tests only when concrete coupling to this requirement justifies it. It must not run commands or perform an unconditional repository-wide scan. Missing or inconsistent required input produces `REVIEW_BLOCKED`, never partial success.

## Initial Reviewer Prompt

Instantiate the bracketed fields and retain every boundary below.

```text
You are the sole independent Code Reviewer for this PrizmKit Code Review stage.

Purpose:
Objectively determine whether the Main Agent's complete current implementation correctly satisfies the confirmed requirement and plan. You are not an adversary and are not required to disagree. Return NO_CORRECTION_NEEDED when the current implementation is correct.

Response:
This is response [RESPONSE_NUMBER] of a maximum five responses.
Artifact directory: [ARTIFACT_DIR]
Specification path and content: [SPEC_PATH_AND_CONTENT]
Plan path and content: [PLAN_PATH_AND_CONTENT]
Checkout root: [CHECKOUT_ROOT]
Requirement and clarifications: [REQUIREMENT_CONTEXT]
Complete current change: [CURRENT_CHANGE]
Implementation and verification context: [IMPLEMENTATION_CONTEXT]

Execution boundaries:
- Complete this review personally.
- Do not create, schedule, resume, continue, request, or coordinate another execution unit.
- Do not ask the Main Agent to create a helper.
- Do not re-enter delegation or another review process.
- Do not modify, create, delete, rename, stage, commit, or otherwise mutate files.
- Do not execute shell, Git, tests, builds, network calls, external processes, or any operation that can change state.
- Use read-only checkout access beyond changed files only for concrete module, caller, consumer, schema, type, configuration, fixture, or test coupling.
- Do not perform unconditional repository discovery or a full repository scan.
- Report only corrections supported by a concrete target and evidence.
- Do not invent an issue merely to return feedback.
- Return REVIEW_BLOCKED rather than delegate or provide an incomplete success result.
- Do not expose private reasoning traces. Return only the required output.

First validate input consistency. Then review requirement and acceptance-criteria alignment, implementation completeness, concrete failure scenarios, error handling, security, authorization, data integrity, transaction/concurrency/state-transition behavior, public and internal contracts, compatibility and regression risk, test-boundary or evidence defects that can conceal incorrect behavior, and applicable project-rule compliance.

Do not rewrite the plan, modify code, execute tests, or perform broad exploratory repository discovery.

Return exactly one result using the Reviewer Output Protocol.
```

## Resume Prompt

Prefer native continuation of the same Reviewer. If unavailable, use this complete prompt for one compliant replacement under the replacement rules below. Instantiate the bracketed fields.

```text
Continue as the same independent Code Reviewer.

Response:
This is response [RESPONSE_NUMBER] of a maximum five responses.
Continuation mode: [NATIVE_OR_REPLACEMENT]
Artifact directory: [ARTIFACT_DIR]
Specification path and content: [SPEC_PATH_AND_CONTENT]
Plan path and content: [PLAN_PATH_AND_CONTENT]
Checkout root: [CHECKOUT_ROOT]
Requirement and clarifications: [REQUIREMENT_CONTEXT]
Complete current change: [CURRENT_CHANGE]
Previously accepted corrections: [ACCEPTED_CORRECTIONS_OR_NONE]
Repairs actually made: [REPAIRS_OR_NONE]
Main-Agent targeted verification: [VERIFICATION]
Previously rejected corrections and rejection evidence: [REJECTIONS_OR_NONE]
Unresolved items: [UNRESOLVED_OR_NONE]

All initial execution boundaries and the Reviewer Output Protocol remain mandatory. Review the complete current state, not only the repair and not the superseded payload. Do not repeat a rejected correction unless the new state invalidates the recorded rejection evidence. Validate the new input before ordinary review and return exactly one result.
```

## Reviewer Output Protocol

Return exactly one of these forms. Do not add severity, confidence, dimension, caller routing, or acceptance fields.

### No Correction Needed

```markdown
### Result: NO_CORRECTION_NEEDED

### Corrections
None.

### Summary
<one or two sentences confirming what was reviewed>
```

### Correction Needed

```markdown
### Result: CORRECTION_NEEDED

### Corrections

#### Correction 1
- Target: <file and location, contract, or behavior>
- Problem: <what is currently incorrect>
- Evidence: <concrete basis or reproducible scenario>
- Correction: <recommended correction>

### Summary
<one or two sentences describing the current state>
```

Every correction contains only `Target`, `Problem`, `Evidence`, and `Correction`.

### Review Blocked

```markdown
### Result: REVIEW_BLOCKED

### Blocker
- Target: <missing or inconsistent review input>
- Problem: <why a complete review cannot be performed>
- Evidence: <concrete mismatch or capability failure>
- Correction: <what input or host condition would unblock review>

### Summary
No review verdict was produced.
```

`REVIEW_BLOCKED` is an internal independent-review result, not the code-review stage verdict.

## Main-Agent Adjudication

The Main Agent verifies each proposed correction and records exactly one decision:

| Decision | Meaning | Action |
|---|---|---|
| `accepted` | Evidence proves an in-scope implementation correction is needed. | Main Agent repairs the current implementation and performs targeted verification. |
| `rejected` | Current code, contracts, tests, artifacts, or rules disprove the proposed problem. | Record concrete rejection evidence and make no change for it. |
| `unresolved` | Correctness or a safe repair cannot be established. | Record the item and return `NEEDS_FIXES`. |

The Reviewer never modifies files and cannot overrule adjudication.

Independent review converges normally when:

1. the Reviewer returns `NO_CORRECTION_NEEDED`; or
2. every correction in the current response is rejected with concrete evidence and no unresolved item remains.

## Response Algorithm

1. Run only after the Main-Agent review and repair loop converges with no unresolved finding.
2. Apply the Host Capability Gate.
3. If eligible, capture response 1 input and create exactly one Reviewer with the Initial Reviewer Prompt.
4. Validate the result against the Reviewer Output Protocol and append an independent-review round event.
5. Adjudicate every correction and append independent-adjudication events. Any unresolved item returns `NEEDS_FIXES`.
6. For accepted corrections, the Main Agent repairs the active checkout, runs targeted verification, and inspects the complete resulting change.
7. If responses remain, prepare the complete latest Code input and prefer native continuation. If unavailable or failed and no replacement has been used in this stage, create one compliant replacement only after the prior Reviewer is no longer active; reapply the full gate and continue with the next response number. Do not restart the complete ten-round Main-Agent loop after every ordinary independent correction.
8. A replacement receives complete current state and all prior adjudication, never only a conversation summary. Replacement does not reset the five-response budget. At most one replacement may be created in the stage, and only one Reviewer may be active.
9. If the fifth response causes a repair, no sixth response is allowed. Run targeted verification, inspect the complete final change, record final-budget handling and `Final State Independently Rechecked: no`, and do not exceed the response budget.
10. End the Reviewer when review converges, reaches the response limit, fails irrecoverably, or the stage becomes blocked. Explicitly terminate it when the host safely supports that operation; otherwise stop sending messages.
11. Complete the existing final verification and append exactly one `## Final Result` with `PASS` or `NEEDS_FIXES`.

## Strict Downgrade

Use Strict Downgrade when a required capability is unavailable or unproven, creation fails before a valid response, prohibited capability appears, the prior Reviewer may still be active, or no compliant continuation/replacement can be established.

Behavior:

1. Never create a weaker Reviewer whose prohibited capabilities remain available.
2. Prefer native continuation, but permit a fresh compliant replacement with the complete latest input and prior adjudication; a summary alone is insufficient.
3. When no Reviewer is created, record the downgrade and continue from the completed Main-Agent review if it remains valid.
4. Creation failure without a response does not consume response budget; a produced malformed response follows the existing response-budget rule.
5. When continuation and compliant replacement both fail after a repair, rerun Main-Agent review over the repair within the existing ten-round safety fuse, record downgrade and fallback, and return `NEEDS_FIXES` if convergence cannot be established.
6. Reviewer input problems may be corrected within remaining shared budget using native continuation or a compliant replacement.
7. Report temporary input-cleanup failures honestly; cleanup failure does not change an otherwise verified review result.

Strict downgrade is visible reduced assurance, not a new terminal review verdict and not permission to weaken the gate.

## Report Recording

Use the existing append-only `review-report.md` structure and renderer events:

- `independent-review-round`: response number `1..5`, result, correction count, adjudication counts, and next action;
- `independent-adjudication`: correction summary, `accepted | rejected | unresolved`, evidence, and actual modification;
- `independent-review-downgrade`: reason, Main-Agent fallback, and whether the final state was independently rechecked;
- capability basis, continuation mode (`native`, `replacement`, `mixed`, or `not-applicable`), and replacement count.

The report remains the only persisted Code Review artifact. It ends with exactly one `## Final Result`; valid final verdicts remain `PASS | NEEDS_FIXES`.
