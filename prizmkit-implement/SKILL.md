---
name: "prizmkit-implement"
description: "Execute the reviewed plan for a formal PrizmKit requirement, update task checkpoints, preserve the shared workflow artifact directory, and hand off to prizmkit-code-review. Use after prizmkit-plan or when resuming implementation repair. (project)"
---

# PrizmKit Implement

`/prizmkit-implement` executes the tasks in one formal requirement's `plan.md`. It is the implementation stage, including implementation repairs requested by code review or testing.

## When to Use

- After `/prizmkit-plan` reports `PLAN_READY`.
- When workflow state routes a review or test repair back to implementation.
- When `plan.md` contains unchecked tasks for the active requirement.
- User says "implement", "build", "code it", "start coding", "develop", or "execute".

## When NOT to Use

- No `spec.md` and `plan.md` exist for the formal requirement.
- All planned tasks are complete and no repair scope is recorded.
- The user is still deciding scope or asking for planning.
- The request is a direct low-risk edit outside the formal requirement lifecycle.

## Preconditions and Artifact Identity

| Required artifact | Check | If missing |
|---|---|---|
| `plan.md` with Tasks | Exists and contains incomplete or explicitly repairable work | Return `IMPLEMENT_BLOCKED` and direct the user to `/prizmkit-plan`. |
| `spec.md` | Exists in the same artifact directory | Return `IMPLEMENT_BLOCKED` and direct the user to `/prizmkit-plan`. |
| Workflow state | Reusable or reconstructable | Reconstruct from artifacts and report the result when absent or stale. |

Accept `artifact_dir` from the preceding skill or workflow state. Do not scan for a different most-recent plan when invoked as a handoff. A single requirement must reuse the same `artifact_dir` throughout all stages.

## Context Loading

Before editing:

1. Read `plan.md`, `spec.md`, and only relevant companion artifacts.
2. Read `.prizmkit/prizm-docs/root.prizm` when present.
3. Read relevant L1 docs and relevant L2 docs when present.
4. If an affected L2 doc is missing, read the target source files as fallback and record that no L2 context was available. Do not create L2 merely because it was read; retrospective decides whether durable knowledge warrants it.
5. Read referenced layer rules when present. If a rule conflicts with the plan, stop and ask the user unless the plan clearly supersedes the rule.

## Optional Inline Delegation

The default is direct Main-Agent implementation. If a narrow slice is delegated, read `${SKILL_DIR}/references/implementation-subagent-procedure.md` and follow its active-checkout/no-worktree constraints. Delegation is optional implementation detail and does not alter lifecycle handoff or ownership.

## Execution

For each unchecked or explicitly repair-scoped task, in plan order:

1. Confirm the target scope and relevant context.
2. Apply TDD when appropriate:
   - add or update a failing test first for behavior changes;
   - use the smallest meaningful verification for docs, configuration, UI-only, or mechanical changes.
3. Cover relevant happy paths, domain edges, and errors without inventing meaningless tests.
4. Avoid unrelated edits and preserve the requirement's artifact identity.
5. Mark a task complete immediately after its implementation is complete.
6. Stop dependent tasks on failure; run `[P]` tasks in parallel only when safe.
7. Execute only local implementation verification here. The mandatory full lifecycle code review follows implementation and the mandatory auditable test stage follows code review.

### Repair Scope

When routed from a failed test or review, read `repair_scope` from workflow state and constrain edits accordingly:

- `production`: production code, runtime configuration, schema, dependency, or public interface changes. Completion must hand off to `prizmkit-code-review`.
- `test-infrastructure`: tests, fixtures, test runner configuration, or evidence setup only. Completion may hand off directly to `prizmkit-test`.
- `unknown`: stop and ask the user; do not guess which downstream gates can be skipped.

## Recovery

If interrupted:

- Reuse completed task markers and the same `artifact_dir`.
- Inspect any partially edited files before continuing.
- Reconcile workflow state with the plan and current diff.
- Never report `IMPLEMENTED` when incomplete tasks or unresolved repair work remain.

## Workflow State

Before reading or updating workflow state, read `${SKILL_DIR}/references/workflow-state-protocol.md`.

On successful implementation, update `.prizmkit/state/workflows/<requirement-slug>.json` with:

```json
{
  "stage": "implement",
  "status": "IMPLEMENTED",
  "completed_stages": ["plan", "implement"],
  "repair_round": 0,
  "repair_scope": null,
  "next_stage": "code-review",
  "resume_from": "prizmkit-code-review"
}
```

For a repair, increment `repair_round`, set `status` to `IMPLEMENT_REPAIR`, preserve the triggering failure in the state, and select the next stage according to `repair_scope`.

## Output and Handoff

Report:

- implementation summary;
- completed and remaining tasks;
- files changed;
- local verification performed;
- workflow state path and status;
- exact next stage.

On initial implementation or a production-affecting repair:

```text
IMPLEMENTED
  → /prizmkit-code-review
```

On a test-infrastructure-only repair:

```text
IMPLEMENTED
  → /prizmkit-test
```

If semantic handoff is supported, continue automatically with the same `artifact_dir`; otherwise provide the deterministic next invocation.
