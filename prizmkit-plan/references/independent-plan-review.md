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

The independent budget does not replace, reduce, or extend the local review budget. Create at most one Reviewer for the Plan stage. Never reuse it in another stage.

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
- The decision must not branch on platform identity, tool name, execution-unit type name, adapter output, or a platform allowlist.
- If any capability is missing or cannot be proven, do not create a Reviewer. Use Strict Downgrade.
- A general execution unit with a prompt saying "do not mutate or delegate" is not eligible when those capabilities remain available.
- The Reviewer inherits the current session's model configuration. Do not add a separate model-selection contract.

## Review Input

Before each response, the Main Agent captures one bounded review input that is immutable for one response:

```text
review-input
├── manifest: input identity, response number, project-relative paths, states, and consistency markers
├── context: requirement, confirmed clarifications, relevant rules, and prior adjudication on resume
└── payload: current spec.md, current plan.md, and only targeted supporting material
```

The Plan payload contains:

- current `spec.md`;
- current `plan.md`, including tasks;
- original requirement and confirmed clarification decisions;
- relevant project rules and Prizm documentation;
- only the source or contract paths needed to verify concrete planning assumptions.

Do not provide broad repository access as a substitute for capturing input. The representation may use host-native immutable content or a read-only temporary payload outside the project change set; the protocol does not require a particular temporary path or command.

Before ordinary review, the Reviewer verifies that manifest, context, and payload agree. Missing content, unexplained entries, stale content, or mixed-round input produces `REVIEW_BLOCKED`, never partial success.

## Initial Reviewer Prompt

Instantiate the bracketed fields and retain every boundary below.

```text
You are the sole independent Plan Reviewer for this PrizmKit Plan stage.

Purpose:
Objectively determine whether the Main Agent's current specification and implementation plan correctly represent the confirmed requirement and are ready for implementation. You are not an adversary and are not required to disagree. Return NO_CORRECTION_NEEDED when the current artifacts are correct.

Response:
This is response [RESPONSE_NUMBER] of a maximum two responses.
Review-input identity: [INPUT_ID]
Manifest: [MANIFEST]
Context: [CONTEXT]
Payload: [PAYLOAD]
Permitted targeted paths, if represented separately: [TARGETED_PATHS_OR_NONE]

Execution boundaries:
- Complete this review personally.
- Do not create, schedule, resume, continue, request, or coordinate another execution unit.
- Do not ask the Main Agent to create a helper.
- Do not re-enter orchestration, delegation, another review workflow, or an equivalent process.
- Do not modify, create, delete, rename, stage, commit, or otherwise mutate files.
- Do not execute commands, tests, builds, network calls, or any operation that can change state.
- Read only the bounded review input and explicitly permitted targeted paths.
- Do not perform broad repository discovery or a full repository scan.
- Report only corrections supported by a concrete target and evidence.
- Do not invent an issue merely to return feedback.
- Return REVIEW_BLOCKED rather than delegate or provide an incomplete success result.
- Do not expose private reasoning traces. Return only the required output.

First validate input consistency. Then review requirement and scope correctness, terminology and non-goals, acceptance criteria, goal-to-plan coverage, relevant data/interface/security/compatibility/performance/deployment/migration constraints, dependency evidence, task prerequisites and safe parallel markers, task actionability/testability/resumability, and unjustified scope expansion or overengineering.

Do not review implementation code, execute tests, or redesign the requirement beyond a necessary correction.

Return exactly one result using the Reviewer Output Protocol.
```

## Resume Prompt

Resume the exact same Reviewer; do not create a new Reviewer with this text. Instantiate the bracketed fields.

```text
Continue as the same independent Plan Reviewer.

Response:
This is response [RESPONSE_NUMBER] of a maximum two responses.
New review-input identity: [INPUT_ID]
New manifest: [MANIFEST]
Current context: [CONTEXT]
Current payload: [PAYLOAD]
Previously accepted corrections: [ACCEPTED_CORRECTIONS_OR_NONE]
Modifications actually made: [MODIFICATIONS_OR_NONE]
Previously rejected corrections and rejection evidence: [REJECTIONS_OR_NONE]
Unresolved items: [UNRESOLVED_OR_NONE]

All initial execution boundaries and the Reviewer Output Protocol remain mandatory. Review the current state, not the superseded payload. Do not repeat a rejected correction unless the new state invalidates the recorded rejection evidence. Validate the new input before ordinary review and return exactly one result.
```

## Reviewer Output Protocol

Return exactly one of these forms. Do not add severity, confidence, dimension, workflow impact, or acceptance fields.

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

`REVIEW_BLOCKED` is an internal independent-review result, not a lifecycle result.

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
7. If one response remains, capture fresh input and resume the exact same Reviewer with the Resume Prompt.
8. If the second response causes a modification, no third response is allowed. Perform targeted Plan/Spec verification, record final-budget handling, and set `Final State Independently Rechecked` to `no`.
9. Append the terminal `## Independent Plan Review` record. Appending the record itself never triggers another response.
10. End the Reviewer when review converges, reaches the response limit, fails irrecoverably, or the stage becomes blocked. Explicitly terminate it when the host safely supports that operation; otherwise stop sending messages.

## Strict Downgrade

Use strict downgrade in any of these cases:

- a required capability is unavailable or unproven before creation;
- Reviewer creation fails;
- the exact same Reviewer cannot be resumed or resume fails;
- execution-unit integrity becomes uncertain.

Behavior:

1. Never create a weaker or replacement Reviewer.
2. Never create a fresh Reviewer with a summary of the prior conversation; a summary is context, not native continuation.
3. When no Reviewer is created, record the downgrade and continue from the completed Main-Agent review if it remains valid.
4. When creation fails before any response, record the failure and preserve the completed Main-Agent review.
5. When resume fails after an accepted modification, Never create a replacement Reviewer; rerun the local Plan/Spec review over the modification within its existing local semantics, record the downgrade and fallback, and return `PLAN_BLOCKED` if that verification cannot establish readiness.
6. Reviewer input problems may be corrected and sent to the same Reviewer only while response budget and native continuation remain available. Otherwise downgrade.
7. Report temporary input-cleanup failures honestly; cleanup failure does not change an otherwise verified planning result.

Strict downgrade is visible reduced assurance, not an error verdict and not permission to weaken the gate.

## Terminal Record

Append the terminal record shape from `${SKILL_DIR}/assets/plan-template.md` after review or downgrade. Include:

- `Capability Gate: ENABLED | DOWNGRADED`;
- a concrete downgrade reason or `none`;
- Reviewer responses used, from `0` through `2`;
- convergence or fallback mode;
- whether the final state received an independent recheck;
- every proposed correction, Main-Agent decision, evidence, and actual modification;
- unresolved items, which must be absent for `PLAN_READY`.

This section is audit metadata, not an implementation task and not input that requires another Reviewer response.
