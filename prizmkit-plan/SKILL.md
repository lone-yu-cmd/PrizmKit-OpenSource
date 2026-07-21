---
name: "prizmkit-plan"
description: "Start the formal PrizmKit requirement lifecycle by turning a natural-language change into spec.md and plan.md artifacts, running mandatory Main-Agent planning review plus optional capability-gated independent correctness review, initializing workflow state, and handing off to prizmkit-implement. Works for features, bug fixes, refactors, migrations, tests, and other formal requirements. (project)"
---

# PrizmKit Plan

`/prizmkit-plan` is the entry point for one formal requirement. It converts a natural-language change into a reviewed change artifact: `spec.md` defines WHAT and WHY; `plan.md` defines HOW and executable tasks.

A change artifact can describe a feature, bug fix, refactor, migration, test improvement, or another scoped requirement.

## When to Use

- Starting any formal software requirement.
- A non-trivial change benefits from written scope, acceptance criteria, and task breakdown.
- No adequate current `spec.md` and `plan.md` exist for the requested work.
- User says "specify", "plan", "new task", "I want to add...", "architect", "design", or "break it down".

## When NOT to Use

- Direct edit: typo, pure formatting, small documentation edit, or another explicitly low-risk non-requirement change.
- The active artifact directory already has an adequate reviewed `spec.md` and `plan.md`; resume from the workflow state instead.

## Formal Lifecycle

A successful plan starts this fixed lifecycle:

```text
plan → implement → code-review → test → retrospective → committer
```

Planning depth may be concise or comprehensive, but no later formal lifecycle stage may be silently skipped.

## Input

| Parameter | Required | Description |
|---|---|---|
| `description` | Yes | Natural-language description of the requirement. |
| `artifact_dir` | No | Directory for the change artifact. If omitted, create a numbered slug under `.prizmkit/specs/`. |

## Atomic Stage Boundary

`prizmkit-plan` owns only specification, plan, task generation, and planning-quality review. It writes its truthful terminal result and `next_stage`, then returns control. It must not invoke `prizmkit-implement` itself, including when an external orchestrator is active. The active orchestrator owns the next-stage invocation.

## Phase 0: Initialization Check and Context

1. Check whether project context such as `.prizmkit/prizm-docs/root.prizm`, `.prizmkit/config.json`, or a project brief exists.
2. If initialization context is missing:
   - recommend `/prizmkit-init` and explain that it improves project context and cross-session continuity;
   - do not block planning;
   - if the user continues, load the README, manifests, project instruction files, source structure, and relevant source files as fallback.
3. If Prizm docs exist, read `root.prizm`, relevant L1 docs, relevant L2 docs when present, and source fallback when L2 is absent.
4. Resolve `artifact_dir` once and reuse it for every later lifecycle handoff. Do not re-detect another artifact during the same requirement.

## Phase 1: Specify (`spec.md`)

Skip regeneration when `spec.md` already exists and still matches the requested requirement.

1. Gather the requirement description. If it is missing in an interactive run, ask the user; otherwise return a clear blocked result.
2. Determine the artifact directory:
   - use the caller-provided `artifact_dir` when present;
   - otherwise scan `.prizmkit/specs/` for existing numbered directories and create `.prizmkit/specs/###-task-slug/`.
3. Generate `spec.md` from `${SKILL_DIR}/assets/spec-template.md`:
   - focus on WHAT and WHY, not HOW;
   - include only relevant sections;
   - give every goal acceptance criteria;
   - mark genuine ambiguity with `[NEEDS CLARIFICATION]`.
4. For persistence changes, inspect existing schemas and add a Data Model section using project conventions.
5. Resolve clarification markers:
   - interactive: use `${SKILL_DIR}/references/clarify-guide.md` and ask targeted questions;
   - non-interactive: choose conservative defaults, annotate them, and block when a safe default is impossible.

Internal ID hygiene: PrizmKit IDs, task/session/run IDs, branch names, absolute worktree paths, and internal artifact paths may exist in change artifacts but must not leak into `.prizmkit/prizm-docs/`, product UI copy, API responses, emails, notifications, or expected user-visible test strings.

## Phase 2: Design (`plan.md`)

Precondition: `spec.md` exists with no unresolved blocker.

1. Read `spec.md` and relevant project context.
2. Resolve remaining clarification markers.
3. Choose a planning depth appropriate to the requirement:
   - concise for small, well-scoped formal requirements;
   - comprehensive for multi-module, public API, data model, security, permission, payment, deployment-impacting, or ambiguous requirements.
4. Generate `plan.md` from `${SKILL_DIR}/assets/plan-template.md` with:
   - change approach;
   - component and file changes;
   - data migration approach when relevant;
   - interface/API contract design when relevant;
   - test strategy for the mandatory `/prizmkit-test` stage;
   - risks and mitigations;
   - behavior-preservation strategy for refactors.
5. Cross-check every spec goal against the plan.
6. Check alignment with project rules and available Prizm documentation.

## Phase 3: Task Generation

1. Choose an MVP-first, incremental, or safe parallel task strategy.
2. Append `## Tasks` to `plan.md` using `${SKILL_DIR}/assets/plan-template.md`.
3. Include setup, foundation, core, polish, and checkpoint tasks only when applicable.
4. Mark `[P]` only for tasks that can safely execute independently.
5. Include implementation-local verification where useful, while preserving the later full code-review and test stages.
6. Run `${SKILL_DIR}/references/verification-checklist.md` and repair plan defects.

## Phase 4: Plan/Spec Review Loop

Run every time `spec.md` or `plan.md` is created or changed. This is the mandatory Main-Agent baseline on every host.

1. Read `${SKILL_DIR}/references/review-plan-spec-loop.md`.
2. Review the current artifacts against the requirement and project context.
3. Apply all resolvable `BLOCKER` fixes and accepted `SHOULD_FIX` fixes.
4. Treat `OPTIONAL` findings as non-blocking.
5. Rerun once when fixes were applied, with a maximum of two planning-review rounds.
6. If a `BLOCKER` remains, ask targeted questions in interactive mode; otherwise record `PLAN_BLOCKED` and stop.
7. Continue only when no unresolved blocker remains.

The planning review must not implement code, run the full test stage, or launch external orchestration.

## Phase 5: Independent Plan Review

Run only after the Main-Agent Plan/Spec review converges. This optional check never replaces or weakens the completed local review.

1. Read `${SKILL_DIR}/references/independent-plan-review.md` and follow its complete contract.
2. Apply its all-or-nothing semantic Host Capability Gate. If any required structural capability is unavailable or unproven, create no Reviewer and record strict downgrade in `plan.md`.
3. When the gate passes, capture bounded immutable current-state input and create exactly one Plan Reviewer with the reference's Initial Reviewer Prompt.
4. Use maximum two Reviewer responses. Adjudicate every correction as `accepted`, `rejected`, or `unresolved`; the Main Agent alone modifies artifacts.
5. After an accepted correction, perform targeted Plan/Spec verification and, when one response remains, natively resume the exact same Reviewer. Never create a replacement Reviewer or simulate continuation with a fresh Reviewer plus summary.
6. If native resume fails after modification, record downgrade and rerun the Main-Agent local Plan/Spec review over that modification as specified by the reference.
7. If the final allowed response causes a modification, run targeted verification, record that the final state was not independently rechecked, and do not exceed the response budget.
8. Append the terminal `## Independent Plan Review` record. Appending that audit record does not trigger another response.
9. Any unresolved correction produces `PLAN_BLOCKED`; otherwise independent convergence or strict downgrade may continue to handoff from the valid completed Main-Agent review.

## Phase 6: Workflow State and Handoff

Read `${SKILL_DIR}/references/workflow-state-protocol.md` and create or update:

```text
.prizmkit/state/workflows/<requirement-slug>.json
```

Follow the bundled protocol. At minimum record:

```json
{
  "schema_version": 1,
  "artifact_dir": ".prizmkit/specs/001-example",
  "stage": "plan",
  "status": "completed",
  "stage_result": "PLAN_READY",
  "completed_stages": ["plan"],
  "repair_round": 0,
  "repair_scope": null,
  "next_stage": "implement",
  "resume_from": "prizmkit-implement"
}
```

The state file is runtime metadata. Do not change the target project's Git or ignore policy.

## Output

- `spec.md` and `plan.md` in the resolved artifact directory.
- Workflow state with `PLAN_READY` or a truthful blocked result.
- Planning depth, key decisions, task count, and checkpoint summary.
- The same `artifact_dir` for every downstream stage.

## Handoff

On `PLAN_READY`:

1. If workflow state names an active `orchestrator`, return `PLAN_READY`, `stage_result=PLAN_READY`, `next_stage=implement`, the state path, and the same `artifact_dir` to that orchestrator; do not invoke the next stage independently.
2. For direct stage use with no active orchestrator, report exactly one deterministic next action: `/prizmkit-implement`, with `stage_result=PLAN_READY`, the state-file path, and `artifact_dir`; a host may perform that semantic handoff on the user's behalf.

Read `${SKILL_DIR}/references/examples.md` only when a worked planning example is needed.
