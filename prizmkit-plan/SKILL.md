---
name: "prizmkit-plan"
description: "Create and review spec.md and plan.md artifacts for one supplied software requirement. Covers features, bug fixes, refactors, migrations, tests, and other scoped changes; returns PLAN_READY or PLAN_BLOCKED. (project)"
---

# PrizmKit Plan

`/prizmkit-plan` converts one caller-supplied natural-language change into a reviewed change artifact: `spec.md` defines WHAT and WHY; `plan.md` defines HOW and executable tasks.

A change artifact can describe a feature, bug fix, refactor, migration, test improvement, or another scoped requirement.

## When to Use

- Starting any formal software requirement.
- A non-trivial change benefits from written scope, acceptance criteria, and task breakdown.
- No adequate current `spec.md` and `plan.md` exist for the requested work.
- User says "specify", "plan", "new task", "I want to add...", "architect", "design", or "break it down".

## When NOT to Use

- Direct edit: typo, pure formatting, small documentation edit, or another explicitly low-risk non-requirement change.
- The supplied artifact directory already has an adequate reviewed `spec.md` and `plan.md`; return the existing stage result instead of regenerating them.

## Input

| Parameter | Required | Description |
|---|---|---|
| `description` | Yes | Natural-language description of the requirement. |
| `artifact_dir` | No | Exact caller-supplied directory for the change artifact. If omitted, create a deterministic numbered directory under `.prizmkit/specs/` using `${SKILL_DIR}/references/artifact-identity.md`. |

## Atomic Stage Boundary

`prizmkit-plan` owns specification, plan, task generation, and planning-quality review for one supplied requirement. Its terminal outputs are `PLAN_READY` or `PLAN_BLOCKED`; it stops after producing that result.

## Phase 0: Initialization Check and Context

1. Check whether project context such as `.prizmkit/prizm-docs/root.prizm`, `.prizmkit/config.json`, or a project brief exists.
2. If initialization context is missing, do not block planning; load the README, manifests, project instruction files, source structure, and relevant source files as fallback.
3. If Prizm docs exist, read `root.prizm`, follow only its relevant module/detail pointers, and use source fallback when detailed documentation is absent.
4. Read `${SKILL_DIR}/references/artifact-identity.md`, validate or generate `artifact_dir` exactly once, and keep it stable throughout this planning invocation.

## Phase 1: Specify (`spec.md`)

Skip regeneration when `spec.md` already exists and still matches the requested requirement.

1. Gather the requirement description. If it is missing in an interactive run, ask the user; otherwise return a clear blocked result.
2. Determine the artifact directory through `${SKILL_DIR}/references/artifact-identity.md`:
   - validate and preserve the exact caller-provided `artifact_dir` when present;
   - otherwise derive the normalized title slug, allocate the next collision-safe number, and create `.prizmkit/specs/<number>-<slug>/`.
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
   - project-native test strategy appropriate to the requirement;
   - risks and mitigations;
   - behavior-preservation strategy for refactors.
5. Cross-check every spec goal against the plan.
6. Check alignment with project rules and available Prizm documentation.

## Phase 3: Task Generation

1. Choose an MVP-first, incremental, or safe parallel task strategy.
2. Append `## Tasks` to `plan.md` using `${SKILL_DIR}/assets/plan-template.md`.
3. Include setup, foundation, core, and polish phases only when applicable; do not manufacture empty phases for a small plan.
4. Every formal plan must contain at least one concrete risk with mitigation and at least one verification checkpoint. A small plan may use one final checkpoint instead of artificial phase checkpoints.
5. Mark `[P]` only for tasks that can safely execute independently.
6. Include appropriate implementation-local and regression verification tasks without executing them during planning.
7. Run `${SKILL_DIR}/references/verification-checklist.md` and repair plan defects.

## Phase 4: Plan/Spec Review Loop

Run every time `spec.md` or `plan.md` is created or changed. This is the mandatory Main-Agent baseline on every host.

1. Read `${SKILL_DIR}/references/review-plan-spec-loop.md`.
2. Review the current artifacts against the requirement and project context.
3. Apply all resolvable `BLOCKER` fixes and accepted `SHOULD_FIX` fixes.
4. Treat `OPTIONAL` findings as non-blocking.
5. Rerun once when fixes were applied, with a maximum of two planning-review rounds.
6. If a `BLOCKER` remains, ask targeted questions in interactive mode; otherwise record `PLAN_BLOCKED` and stop.
7. Continue only when no unresolved blocker remains.

The planning review must not modify product/source code or execute the planned verification strategy.

## Phase 5: Independent Plan Review

Run only after the Main-Agent Plan/Spec review converges. This optional check never replaces or weakens the completed local review.

1. Read `${SKILL_DIR}/references/independent-plan-review.md` and follow its complete contract.
2. Apply its all-or-nothing semantic Host Capability Gate. If any required structural capability is unavailable or unproven, create no Reviewer and record strict downgrade in `plan.md`.
3. When the gate passes, provide the original requirement, confirmed clarifications, exact `artifact_dir`/`spec_path`/`plan_path`, and current spec/plan contents to one active Plan Reviewer with the reference's Initial Reviewer Prompt.
4. Use maximum two Reviewer responses. Adjudicate every correction as `accepted`, `rejected`, or `unresolved`; the Main Agent alone modifies artifacts.
5. After an accepted correction, perform targeted Plan/Spec verification and prefer native continuation when one response remains. If unavailable, the reference permits one compliant replacement with complete latest planning state and the same remaining budget.
6. If neither compliant continuation nor replacement is available after modification, record downgrade and rerun the Main-Agent local Plan/Spec review over that modification as specified by the reference.
7. If the final allowed response causes a modification, run targeted verification, record that the final state was not independently rechecked, and do not exceed the response budget.
8. Append the terminal `## Independent Plan Review` record. Appending that audit record does not trigger another response.
9. Any unresolved correction produces `PLAN_BLOCKED`; otherwise independent convergence or strict downgrade produces `PLAN_READY`.

## Output

Return only planning-stage outputs:

- the resolved `artifact_dir`;
- `spec.md` and `plan.md` paths;
- planning depth, key decisions, and task count;
- `PLAN_READY` when artifacts pass planning review, otherwise `PLAN_BLOCKED` with unresolved planning blockers.

Return only the listed planning outputs. Do not invoke another Skill.

Read `${SKILL_DIR}/references/examples.md` only when a worked planning example is needed.
