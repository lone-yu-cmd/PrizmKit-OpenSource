---
name: "prizmkit-workflow"
description: "One-command orchestrator for completing a formal PrizmKit software requirement. Use whenever the user asks to implement, develop, build, or complete a feature/change end to end, or asks to run the full PrizmKit lifecycle. It coordinates prizmkit-plan → prizmkit-implement → prizmkit-code-review → prizmkit-test → prizmkit-retrospective → prizmkit-committer, preserves one artifact directory and workflow state, routes failures through the correct repair gates, pauses for environment blockers, and asks for confirmation before the local commit. (project)"
---

# PrizmKit Workflow

`/prizmkit-workflow` is the one-entry orchestrator for one formal software requirement. The user describes the desired change once; this skill coordinates the six existing lifecycle skills in order and keeps the same requirement context throughout.

```text
prizmkit-plan
  → prizmkit-implement
  → prizmkit-code-review
  → prizmkit-test
  → prizmkit-retrospective
  → prizmkit-committer
```

This skill coordinates existing skills. It does not reimplement their planning, implementation, review, testing, retrospective, or Git commit procedures.

## When to Use

Use this skill whenever the user:

- asks to implement, develop, build, or complete a feature or formal change end to end;
- asks for one-command, one-stop, full-lifecycle, or complete requirement development;
- gives a requirement and expects planning, coding, review, testing, documentation sync, and commit preparation to be coordinated;
- asks to run the complete PrizmKit lifecycle;
- wants the workflow to continue automatically after each successful stage.

Use the individual stage skill instead when the user explicitly wants only planning, implementation, review, testing, documentation maintenance, or committing.

Do not use this skill for:

- a typo, pure formatting change, or explicitly low-risk direct edit;
- first-time project initialization only; recommend `/prizmkit-init`;
- standalone Prizm documentation repair; use `/prizmkit-prizm-docs`;
- deployment or operations; use `/prizmkit-deploy` separately;
- L2 batch planning, pipeline launchers, or multi-requirement orchestration.

## Inputs

Accept:

- `description`: the user's natural-language formal requirement;
- `artifact_dir`: optional explicit requirement artifact directory;
- `execution_mode`: interactive by default; headless only when the host and user explicitly authorize it;
- `resume`: optional workflow state path or requirement slug for recovery.

If `description` is missing and no resumable workflow is supplied, ask the user for the requirement before invoking `prizmkit-plan`.

## Core Orchestration Rules

### 1. Start with Plan

Invoke `/prizmkit-plan` with the user's requirement and any explicit `artifact_dir`. Do not write a second plan in this orchestrator.

If the project has not run `/prizmkit-init`, allow `prizmkit-plan` to recommend initialization and continue with source fallback when the user chooses to proceed. Initialization is a soft prerequisite, not a hidden workflow stage.

### 2. Preserve Requirement Identity

Once `prizmkit-plan` resolves an `artifact_dir`, capture it and pass the exact same value to every later stage:

```text
.prizmkit/specs/<requirement-slug>/
```

Never select a different most-recent plan when resuming or handing off. The workflow state path is:

```text
.prizmkit/state/workflows/<requirement-slug>.json
```

Read `${SKILL_DIR}/references/workflow-state-protocol.md` for the shared state contract. The target project controls whether generated `.prizmkit/` files are committed, ignored, or shared; do not modify its Git policy.

### 3. Advance Only on Truthful Success

After each stage:

1. Read the stage's actual output and terminal status.
2. Validate the expected artifact and workflow-state transition.
3. Preserve the same `artifact_dir`.
4. Continue only on the permitted success status.
5. If the host cannot invoke another skill automatically, stop with exactly one deterministic next skill, its `artifact_dir`, and the workflow-state path.

Expected transitions:

| Stage | Required success | Next stage |
|---|---|---|
| `prizmkit-plan` | `PLAN_READY` | `prizmkit-implement` |
| `prizmkit-implement` | `IMPLEMENTED` | `prizmkit-code-review` |
| `prizmkit-code-review` | `REVIEW_PASS` | `prizmkit-test` |
| `prizmkit-test` | `TEST_PASS` | `prizmkit-retrospective` |
| `prizmkit-retrospective` | `DOCS_UPDATED` or `NO_DOC_CHANGE` | `prizmkit-committer` |
| `prizmkit-committer` | user confirms, then `COMMITTED` | end |

`TEST_NOT_APPLICABLE` is not a valid lifecycle success. Lightweight changes must execute deterministic verification and return `TEST_PASS`.

### 4. Do Not Duplicate Stage Responsibilities

The orchestrator must not:

- reinterpret a plan as implementation;
- repair production code outside `prizmkit-implement` or the Main-Agent review loop;
- claim tests passed without `prizmkit-test` evidence;
- perform retrospective documentation changes itself;
- stage or commit before `prizmkit-committer` presents a preview and receives confirmation;
- invoke `prizmkit-deploy` as a hidden seventh stage.

## Failure and Repair Routing

Use the shared workflow state and the stage evidence to determine routing. Do not blindly retry every failure.

### Review Failure

`REVIEW_NEEDS_FIXES` means review could not converge. Route to:

```text
prizmkit-implement
  → prizmkit-code-review
  → prizmkit-test
```

The Main-Agent review skill owns its internal review repairs and review-round limit before returning its terminal result.

### Test Failure

Classify the evidence-backed repair scope:

```text
TEST_FAIL affecting only tests, fixtures, test-runner configuration,
or evidence infrastructure
  → prizmkit-implement
  → prizmkit-test
```

```text
TEST_FAIL affecting production code, runtime configuration, schema,
dependencies, or public interfaces
  → prizmkit-implement
  → prizmkit-code-review
  → prizmkit-test
```

A production-affecting repair after `REVIEW_PASS` must receive another review. A test-infrastructure-only repair may return directly to testing.

### Environment Block

`TEST_BLOCKED` means that a trustworthy verdict is unavailable because of environment, permission, dependency, external-service, scope, evidence, reliability, cleanup, or budget problems.

```text
TEST_BLOCKED
  → persist the blocker
  → do not make speculative production edits
  → pause
  → resume from prizmkit-test after the blocker is resolved
```

Do not convert an environment blocker into a code change merely to keep the workflow moving.

### Repair Limit

The outer orchestrator allows at most three automatic repair rounds. A round is one repair route from `implement` through all gates required by the repair scope.

```text
repair_round: 0 → 1 → 2 → 3
```

When the limit is reached:

- set workflow status to `WORKFLOW_BLOCKED`;
- preserve the latest failure evidence;
- report the completed rounds and unresolved cause;
- report the exact skill and `artifact_dir` from which a user may resume after changing the requirement or explicitly authorizing another attempt;
- do not claim the requirement is complete.

The internal `prizmkit-code-review` review-round limit remains separate from this outer limit.

## Commit Confirmation Boundary

The orchestrator may automatically reach `/prizmkit-committer`, but it must not silently create a Git commit.

`prizmkit-committer` must:

1. verify all five preceding stage results for the same `artifact_dir`;
2. inspect the final workspace;
3. present intended files, diff summary, sensitive-file warnings, and the proposed Conventional Commit message;
4. wait for explicit user confirmation;
5. create and verify the local commit only after confirmation.

Remote push is never part of this orchestrator's automatic path. Deployment remains a separate `/prizmkit-deploy` invocation.

## Automatic Handoff and Manual Fallback

When the host supports semantic skill-to-skill invocation, continue automatically after each permitted success transition.

When it does not:

1. update or verify workflow state;
2. stop without claiming the next stage ran;
3. print one exact recovery instruction:

```text
Next stage: /prizmkit-<skill>
artifact_dir: <same resolved artifact_dir>
workflow_state: .prizmkit/state/workflows/<requirement-slug>.json
```

The user can invoke that one skill and this orchestrator can resume with `resume` later.

## Resume Protocol

On resume:

1. Read the workflow state specified by `resume` or discover the target project's active workflow state.
2. Read `${SKILL_DIR}/references/workflow-state-protocol.md`.
3. Verify `spec.md`, `plan.md`, review report, test evidence, retrospective result, and current workspace against the state.
4. If state is missing or stale, reconstruct the safest recoverable predecessor and report the reconstruction.
5. Continue from the first incomplete stage; never bypass a required gate based only on stale state.
6. Preserve the same `artifact_dir` and repair-round count.

## Completion Report

At successful completion, report:

```text
WORKFLOW_COMPLETE
artifact_dir: <path>
stages:
  - PLAN_READY
  - IMPLEMENTED
  - REVIEW_PASS
  - TEST_PASS
  - RETRO_COMPLETE
  - COMMITTED
commit: <hash>
push: not performed automatically
next_action: invoke /prizmkit-deploy separately if deployment is needed
```

If the user declines commit confirmation, report `COMMIT_PENDING` rather than `WORKFLOW_COMPLETE` and provide the exact `/prizmkit-committer` resume entry.

If blocked, report:

```text
WORKFLOW_BLOCKED
stage: <stage>
reason: <evidence-backed reason>
repair_round: <0..3>
resume_from: <skill>
artifact_dir: <same path>
```

Never report success for a stage that did not produce its required terminal result.
