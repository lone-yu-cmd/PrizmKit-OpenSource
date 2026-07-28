# Independent Plan Review

## Purpose

Run one optional independent correctness review after the mandatory Main-Agent Plan/Spec review has converged. The Reviewer checks whether the current `spec.md` and `plan.md` correctly express the requirement and are ready for implementation. It is not required to disagree and must return `NO_CORRECTION_NEEDED` when no correction is justified.

This reference is complete within `prizmkit-plan`. Do not depend on another skill's prompt or a platform-generated Reviewer role.

## Required Ordering and Budget

```text
Draft spec.md and plan.md
→ mandatory Main-Agent Plan/Spec review: maximum two rounds
→ optional independent Plan Reviewer: maximum two responses
→ PLAN_READY or PLAN_BLOCKED
```

The independent budget does not replace, reduce, or extend the local review budget. Keep at most one Reviewer active, permit at most one replacement for the Plan stage, and never reuse either unit in another stage.

## Host Capability Gate

The gate is all-or-nothing. Before creating a Reviewer, inspect the current host's actual execution-unit configuration and prove this semantic contract without relying on platform identity or implementation-specific parameters:

```yaml
execution_unit:
  concurrency: at-most-one-active-reviewer
  workspace_access: planning-input-read-only
  mutation: structurally-unavailable
  command_execution: structurally-unavailable
  network_access: structurally-unavailable
  external_process_execution: structurally-unavailable
  downstream_execution: structurally-unavailable
  model_configuration: inherit-current-session
  continuation: prefer-same-unit
  replacement: compliant-replacement-allowed
```

Rules:

- Prompt instructions cannot satisfy a missing structural capability.
- The decision must not branch on platform identity, provider, tool name, command name, execution-unit type name, adapter output, CLI parameter, or an allowlist.
- The Reviewer cannot create, modify, delete, rename, stage, or commit files; execute shell, Git, tests, builds, network calls, or external processes; or create, invoke, resume, or coordinate downstream execution units.
- If any capability is missing or cannot be proven, do not create a Reviewer. Use Strict Downgrade.
- A general execution unit that merely promises to stay read-only is ineligible while prohibited capabilities remain available.
- The Reviewer inherits the current session's model configuration. Do not add a separate model-selection contract.

## Review Input

Resolve and provide exact requirement identity on every response:

```text
artifact_dir: [EXACT_ARTIFACT_DIR]
spec_path: [EXACT_SPEC_PATH]
plan_path: [EXACT_PLAN_PATH]
```

The caller supplies these exact paths as planning-stage input even when ignored by Git. Never ask the Reviewer to discover a latest artifact or guess among multiple `spec.md` and `plan.md` files.

The Plan Reviewer receives only:

- original requirement and confirmed clarifications;
- exact artifact, spec, and plan paths;
- current `spec.md` content;
- current `plan.md` content, including tasks;
- response number and total response budget;
- prior planning adjudication and actual planning modifications on continuation or replacement.

It does not receive or inspect implementation diffs, production changes, test results, or unrelated checkout content. Missing or inconsistent required content produces `REVIEW_BLOCKED`, never partial success.

## Initial Reviewer Prompt

Instantiate the bracketed fields and retain every boundary below.

```text
You are the sole independent Plan Reviewer for this PrizmKit Plan stage.

Purpose:
Objectively determine whether the Main Agent's current specification and implementation plan correctly represent the confirmed requirement and are ready for implementation. You are not an adversary and are not required to disagree. Return NO_CORRECTION_NEEDED when the current artifacts are correct.

Response:
This is response [RESPONSE_NUMBER] of a maximum two responses.
Artifact directory: [ARTIFACT_DIR]
Specification path: [SPEC_PATH]
Plan path: [PLAN_PATH]
Original requirement and confirmed clarifications: [REQUIREMENT_CONTEXT]
Current specification: [SPEC_CONTENT]
Current plan: [PLAN_CONTENT]

Execution boundaries:
- Complete this review personally.
- Do not create, schedule, resume, continue, request, or coordinate another execution unit.
- Do not ask the Main Agent to create a helper.
- Do not re-enter delegation or another review process.
- Do not modify, create, delete, rename, stage, commit, or otherwise mutate files.
- Do not execute shell, Git, tests, builds, network calls, external processes, or any operation that can change state.
- Read only the supplied planning input at the exact paths and contents identified above.
- Do not inspect implementation code or perform repository discovery.
- Report only corrections supported by a concrete target and evidence.
- Do not invent an issue merely to return feedback.
- Return REVIEW_BLOCKED rather than delegate or provide an incomplete success result.
- Do not expose private reasoning traces. Return only the required output.

First validate input consistency. Then review requirement and scope correctness, terminology and non-goals, acceptance criteria, goal-to-plan coverage, relevant data/interface/security/compatibility/performance/deployment/migration constraints, dependency evidence, task prerequisites and safe parallel markers, task actionability/testability/resumability, and unjustified scope expansion or overengineering.

Do not review implementation code, execute tests, or redesign the requirement beyond a necessary correction.

Return exactly one result using the Reviewer Output Protocol.
```

## Resume Prompt

Prefer native continuation of the same Reviewer. If unavailable, use this complete prompt to create one compliant replacement under the replacement rules below. Instantiate the bracketed fields.

```text
Continue as the same independent Plan Reviewer.

Response:
This is response [RESPONSE_NUMBER] of a maximum two responses.
Continuation mode: [NATIVE_OR_REPLACEMENT]
Artifact directory: [ARTIFACT_DIR]
Specification path: [SPEC_PATH]
Plan path: [PLAN_PATH]
Original requirement and confirmed clarifications: [REQUIREMENT_CONTEXT]
Current specification: [SPEC_CONTENT]
Current plan: [PLAN_CONTENT]
Previously accepted corrections: [ACCEPTED_CORRECTIONS_OR_NONE]
Modifications actually made: [MODIFICATIONS_OR_NONE]
Previously rejected corrections and rejection evidence: [REJECTIONS_OR_NONE]
Unresolved items: [UNRESOLVED_OR_NONE]

All initial execution boundaries and the Reviewer Output Protocol remain mandatory. Review the current state, not the superseded payload. Do not repeat a rejected correction unless the new state invalidates the recorded rejection evidence. Validate the new input before ordinary review and return exactly one result.
```

## Reviewer Output Protocol

Return exactly one of these forms. Do not add severity, confidence, dimension, caller-routing impact, or acceptance fields.

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
- Target: <spec.md or plan.md location, section, or task>
- Problem: <what is currently incorrect>
- Evidence: <concrete basis>
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

`REVIEW_BLOCKED` is an internal independent-review result, not the planning-stage result.

## Main-Agent Adjudication

The Main Agent verifies each proposed correction and records exactly one decision:

| Decision | Meaning | Action |
|---|---|---|
| `accepted` | Evidence proves an in-scope planning correction is needed. | Main Agent modifies `spec.md` and/or `plan.md` and performs targeted verification. |
| `rejected` | Current artifacts, source, contracts, or rules disprove the proposed problem. | Record concrete rejection evidence and make no change for it. |
| `unresolved` | Correctness or a safe correction cannot be established. | Record the item and return `PLAN_BLOCKED`. |

The Reviewer never modifies artifacts and cannot overrule adjudication.

Independent review converges normally when:

1. the Reviewer returns `NO_CORRECTION_NEEDED`; or
2. every correction in the current response is rejected with concrete evidence and no unresolved item remains.

## Response Algorithm

1. Run only after the Main-Agent Plan/Spec review converges with no unresolved `BLOCKER`.
2. Apply the Host Capability Gate.
3. If eligible, capture response 1 input and create exactly one Reviewer with the Initial Reviewer Prompt.
4. Validate the result against the Reviewer Output Protocol.
5. Adjudicate every correction. Any unresolved item returns `PLAN_BLOCKED`.
6. For accepted corrections, the Main Agent modifies `spec.md` and/or `plan.md` and applies the relevant part of the existing verification checklist.
7. If one response remains, prepare the complete latest Plan input and prefer native continuation. If native continuation is unavailable or fails and no replacement has been used in this stage, create one compliant replacement only after the prior Reviewer is no longer active; reapply the full gate and continue with the next response number.
8. A replacement receives complete current content and all prior adjudication, never only a conversation summary. Replacement does not reset the two-response budget. At most one replacement may be created in the stage, and only one Reviewer may be active.
9. If the second response causes a modification, no third response is allowed. Perform targeted Plan/Spec verification, record final-budget handling, and set `Final State Independently Rechecked` to `no`.
10. Append the terminal `## Independent Plan Review` record. Appending the record itself never triggers another response.
11. End the Reviewer when review converges, reaches the response limit, fails irrecoverably, or the stage becomes blocked. Explicitly terminate it when the host safely supports that operation; otherwise stop sending messages.

## Strict Downgrade

Use strict downgrade when a required capability is unavailable or unproven, creation fails before a valid response, prohibited capability appears, the previous Reviewer may still be active, or no compliant continuation/replacement can be established.

Behavior:

1. Never create a weaker Reviewer whose prohibited capabilities remain available.
2. Prefer native continuation, but permit a fresh compliant replacement with the complete latest input and prior adjudication; a summary alone is insufficient.
3. When no Reviewer is created, record the downgrade and continue from the completed Main-Agent review if it remains valid.
4. Creation failure without a response does not consume response budget; a produced malformed response follows the existing response-budget rule.
5. When continuation and compliant replacement both fail after a modification, rerun the local Plan/Spec review over that modification, record the downgrade and fallback, and return `PLAN_BLOCKED` if readiness cannot be established.
6. Report temporary input-cleanup failures honestly; cleanup failure does not change an otherwise verified planning result.

Strict downgrade is visible reduced assurance, not an error verdict and not permission to weaken the gate.

## Terminal Record

Append the terminal record shape from `${SKILL_DIR}/assets/plan-template.md` after review or downgrade. Include:

- `Capability Gate: ENABLED | DOWNGRADED`;
- a concrete downgrade reason or `none`;
- Reviewer responses used, from `0` through `2`;
- continuation mode (`native`, `replacement`, `mixed`, or `not-applicable`) and replacement count;
- convergence or fallback mode;
- whether the final state received an independent recheck;
- every proposed correction, Main-Agent decision, evidence, and actual modification;
- unresolved items, which must be absent for `PLAN_READY`.

This section is audit metadata, not an implementation task and not input that requires another Reviewer response.
