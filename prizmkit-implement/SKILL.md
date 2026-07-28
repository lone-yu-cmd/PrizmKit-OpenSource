---
name: "prizmkit-implement"
description: "Execute one caller-supplied spec.md/plan.md change, including explicitly scoped repairs, focused verification, and task-marker updates. Returns IMPLEMENTED or IMPLEMENT_BLOCKED. (project)"
---

# PrizmKit Implement

`/prizmkit-implement` executes tasks from one caller-supplied `plan.md`, including concrete repair findings explicitly included in the request.

## When to Use

- A caller supplies reviewed `spec.md` and `plan.md` artifacts with incomplete tasks.
- A caller supplies an explicit repair scope and findings for implementation repair.
- `plan.md` contains unchecked or explicitly reopened tasks, or the caller requests validation of completed task markers against the current change.
- User says "implement", "build", "code it", "start coding", "develop", or "execute".

## When NOT to Use

- No `spec.md` and `plan.md` exist for the supplied change.
- All planned tasks are complete and the caller already has a valid implementation result for the unchanged current work.
- The user is still deciding scope or asking for planning.
- The request has no reviewed implementation artifact and does not need a formal plan.

## Preconditions and Artifact Identity

| Required artifact | Check | If missing |
|---|---|---|
| `plan.md` with Tasks | Exists; contains incomplete/repairable work or completed markers requiring current-change validation | Return `IMPLEMENT_BLOCKED` with the missing-input reason. |
| `spec.md` | Exists in the same artifact directory | Return `IMPLEMENT_BLOCKED` with the missing-input reason. |

Require the caller to supply or confirm `artifact_dir`. Do not discover a different recent artifact. Optional repair input must include the exact findings and `repair_scope`; do not infer them from caller state.

## Context Loading

Before editing:

1. Read `plan.md`, `spec.md`, and only relevant companion artifacts.
2. Read `.prizmkit/prizm-docs/root.prizm` when present.
3. Follow its pointers to only the relevant direct-child module index and nested detail documentation. Before modifying source, read the complete relevant detail plus the complete parent/child documents needed to resolve its pointers; grep-only fragments are insufficient modification context.
4. If relevant detail documentation is missing, inspect only bounded target source files and narrowly implicated callers/contracts as fallback, record that detailed context was unavailable, and proceed without creating a placeholder. Context loading never creates or modifies documentation.
5. Read referenced layer rules when present. If a rule conflicts with the plan, stop and ask the user unless the plan clearly supersedes the rule.

## Optional Inline Delegation

The default is direct Main-Agent implementation. If a narrow slice is delegated, use `prompt_reference: ${SKILL_DIR}/references/implementation-subagent-procedure.md` and follow its active-checkout/no-worktree constraints. Delegation is an implementation-stage detail and does not change this Skill's output contract.

## Atomic Stage Boundary

`prizmkit-implement` owns only execution of supplied plan tasks and explicitly scoped implementation repairs. It returns `IMPLEMENTED` or `IMPLEMENT_BLOCKED` and stops.

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
7. Execute focused implementation verification appropriate to the changed task; do not expand into a separate broad audit unrelated to implementation.

### Repair Scope

When the caller requests repair, require an explicit `repair_scope` and concrete findings:

- `production`, `runtime`, `schema`, `dependency`, or `public-interface`: constrain edits to the supplied production concern.
- `test-infrastructure`: constrain edits to tests, fixtures, runner configuration, or evidence setup.
- missing or `unknown`: return `IMPLEMENT_BLOCKED`; do not guess the intended repair.

## Recovery

If interrupted:

- Reuse completed task markers and the same `artifact_dir`.
- Inspect any partially edited files before continuing.
- Reconcile plan task markers with the current diff.
- Never report `IMPLEMENTED` when tasks or supplied repair findings remain unresolved.

## Output

Return only implementation-stage outputs:

- `artifact_dir`;
- implementation summary;
- completed and remaining task markers;
- changed paths;
- focused verification performed;
- `IMPLEMENTED` when all supplied work is complete, otherwise `IMPLEMENT_BLOCKED` with exact blockers.

Return only the listed implementation outputs. Do not invoke another Skill.
