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

The independent budget does not replace, reduce, or extend the Main-Agent loop. Create at most one Reviewer for this Code Review stage. Never reuse it in another stage.

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
├── manifest: input identity, response number, exact changed paths, states, and consistency markers
├── context: requirement, plan decisions, applicable rules, and prior adjudication on resume
└── payload: complete captured current change plus targeted supporting material
```

The Code payload contains a logical representation of:

- staged tracked changes;
- unstaged tracked changes;
- untracked files;
- deleted and renamed files;
- the exact changed-file manifest;
- requirement goals and acceptance criteria;
- relevant plan decisions;
- applicable project rules and Prizm traps;
- targeted unchanged callers, dependents, contracts, schemas, or tests implicated by changed interfaces.

The Main Agent captures authoritative workspace state. The Reviewer does not run Git commands. Do not provide broad repository access as a substitute for complete current-change capture. The representation may use host-native immutable content or a read-only temporary payload outside the project change set; the protocol does not require a particular temporary path or command.

Before ordinary review, the Reviewer verifies that manifest, context, and payload agree. Missing paths, unexplained changed files, stale content, or mixed-round input produces `REVIEW_BLOCKED`, never partial success.

## Initial Reviewer Prompt

Instantiate the bracketed fields and retain every boundary below.

```text
You are the sole independent Code Reviewer for this PrizmKit Code Review stage.

Purpose:
Objectively determine whether the Main Agent's complete current implementation correctly satisfies the confirmed requirement and plan. You are not an adversary and are not required to disagree. Return NO_CORRECTION_NEEDED when the current implementation is correct.

Response:
This is response [RESPONSE_NUMBER] of a maximum five responses.
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

First validate input consistency. Then review requirement and acceptance-criteria alignment, implementation completeness, concrete failure scenarios, error handling, security, authorization, data integrity, transaction/concurrency/state-transition behavior, public and internal contracts, compatibility and regression risk, test-boundary or evidence defects that can conceal incorrect behavior, and applicable project-rule compliance.

Do not rewrite the plan, modify code, execute tests, or perform broad exploratory repository discovery.

Return exactly one result using the Reviewer Output Protocol.
```

## Resume Prompt

Resume the exact same Reviewer; do not create a new Reviewer with this text. Instantiate the bracketed fields.

```text
Continue as the same independent Code Reviewer.

Response:
This is response [RESPONSE_NUMBER] of a maximum five responses.
New review-input identity: [INPUT_ID]
New manifest: [MANIFEST]
Current context: [CONTEXT]
Current payload: [PAYLOAD]
Previously accepted corrections: [ACCEPTED_CORRECTIONS_OR_NONE]
Repairs actually made: [REPAIRS_OR_NONE]
Main-Agent targeted verification: [VERIFICATION]
Previously rejected corrections and rejection evidence: [REJECTIONS_OR_NONE]
Unresolved items: [UNRESOLVED_OR_NONE]

All initial execution boundaries and the Reviewer Output Protocol remain mandatory. Review the complete current state, not only the repair and not the superseded payload. Do not repeat a rejected correction unless the new state invalidates the recorded rejection evidence. Validate the new input before ordinary review and return exactly one result.
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

`REVIEW_BLOCKED` is an internal independent-review result, not a lifecycle verdict.

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
7. If one or more responses remain, capture the complete fresh current change and resume the exact same Reviewer with the Resume Prompt. Do not restart the complete ten-round Main-Agent loop after every ordinary independent correction.
8. If the fifth response causes a repair, no sixth response is allowed. Run targeted verification, inspect the complete final change, record final-budget handling and `Final State Independently Rechecked: no`, and do not exceed the response budget.
9. End the Reviewer when review converges, reaches the response limit, fails irrecoverably, or the stage becomes blocked. Explicitly terminate it when the host safely supports that operation; otherwise stop sending messages.
10. Complete the existing final verification and append exactly one `## Final Result` with `PASS` or `NEEDS_FIXES`.

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
5. When resume fails after an accepted repair, Never create a replacement Reviewer; rerun the Main-Agent review over the repair, within the existing ten-round safety fuse, record the downgrade and fallback, and return `NEEDS_FIXES` if review cannot establish convergence.
6. Reviewer input problems may be corrected and sent to the same Reviewer only while response budget and native continuation remain available. Otherwise downgrade.
7. Report temporary input-cleanup failures honestly; cleanup failure does not change an otherwise verified review result.

Strict downgrade is visible reduced assurance, not a new lifecycle verdict and not permission to weaken the gate.

## Report Recording

Use the existing append-only `review-report.md` lifecycle and renderer events:

- `independent-review-round`: response number `1..5`, result, correction count, adjudication counts, and next action;
- `independent-adjudication`: correction summary, `accepted | rejected | unresolved`, evidence, and actual modification;
- `independent-review-downgrade`: reason, Main-Agent fallback, and whether the final state was independently rechecked.

The report remains the only persisted Code Review artifact. It ends with exactly one `## Final Result`; valid final verdicts remain `PASS | NEEDS_FIXES`.
