---
name: "prizmkit-workflow"
description: "Coordinate one explicitly requested formal software requirement through the complete PrizmKit lifecycle from plan to confirmed commit. Use when the user invokes prizmkit-workflow or explicitly asks for the full six-stage lifecycle, a plan-to-commit workflow, or one formal requirement completed end to end. Do not trigger on generic build, implement, feature, bug, or refactor requests; those belong to the applicable individual skill or an external integration. (project)"
---

# PrizmKit Workflow

`/prizmkit-workflow` is the optional composite entry point for one interactive formal software requirement. The user describes the requirement once; this skill coordinates the six atomic lifecycle skills in order and preserves the same requirement context throughout. It does not replace or reimplement any atomic stage.

```text
prizmkit-plan
  → prizmkit-implement
  → prizmkit-code-review
  → prizmkit-test
  → prizmkit-retrospective
  → prizmkit-committer
```

The six stages are mandatory for a formal requirement. The order is not a suggestion and no stage is silently optional.

## When to Use

Use this composite entry point when the user:

- explicitly invokes `/prizmkit-workflow`;
- explicitly asks for the full six-stage PrizmKit lifecycle;
- asks for one formal requirement to be coordinated from plan through commit;
- asks for a plan-to-commit or single-requirement full lifecycle;
- wants the workflow to continue automatically after each successful stage.

Generic "implement", "build", "add feature", "fix bug", or "refactor" requests do not select this workflow by themselves. Use the applicable individual skill unless the user explicitly asks for this complete lifecycle; external integrations may also invoke individual skills through their published contracts.

Use an individual atomic stage skill when the user explicitly wants only planning, implementation, review, testing, documentation maintenance, or committing.

Do not use this skill for:

- a typo, pure formatting change, or explicitly low-risk direct edit;
- first-time project initialization only; recommend `/prizmkit-init`;
- standalone Prizm documentation repair; use `/prizmkit-prizm-docs`;
- deployment or operations; use `/prizmkit-deploy` separately;
- multiple requirements in one invocation; this composite handles one requirement only.

## Inputs

Accept:

- `description`: the natural-language formal requirement;
- `artifact_dir`: optional explicit requirement artifact root;
- `execution_mode`: `interactive` by default; headless only when a trusted host explicitly authorizes it;
- `resume`: optional workflow state path or requirement slug for recovery.

If `description` is missing and no resumable workflow is supplied, ask for the requirement before invoking `prizmkit-plan`. External automation must invoke atomic stages directly with its own execution checkpoint rather than nesting this composite workflow.

## Core Orchestration Rules

### 1. Start with Plan

Invoke `/prizmkit-plan` with the requirement and any explicit `artifact_dir`. Do not write a second plan in this orchestrator.

If initialization context is missing, allow `prizmkit-plan` to recommend initialization and continue with source fallback when the user chooses to proceed. Initialization is a soft prerequisite, not a hidden lifecycle stage.

### 2. Preserve Requirement Identity

Once `prizmkit-plan` resolves an `artifact_dir`, capture it and pass the exact same value to every later stage. The artifact root is generic and is not restricted to one directory family:

```text
.prizmkit/specs/<requirement-slug>/
.prizmkit/bugfix/<bug-id>/
.prizmkit/refactor/<refactor-id>/
```

Never select a different most-recent plan when resuming or handing off. The workflow state path is:

```text
.prizmkit/state/workflows/<requirement-slug>.json
```

Read `${SKILL_DIR}/references/workflow-state-protocol.md` for the shared state contract. This workflow state remains distinct from any external host execution checkpoint. The target project controls whether generated `.prizmkit/` files are committed, ignored, or shared; do not modify its Git policy.

### 3. Advance Only on Truthful Success

After each atomic stage:

1. Read the stage's actual output and terminal status.
2. Validate the expected authoritative artifact or evidence and workflow-state transition.
3. Preserve the same `artifact_dir`.
4. Continue only on the permitted success status.
5. Because this composite is the active orchestrator, atomic skills return terminal state and `next_stage` to it; they must not invoke the next stage recursively.
6. If the host cannot invoke another skill automatically, stop with exactly one deterministic next skill, its `artifact_dir`, and the workflow-state path.

Expected transitions:

| Stage | Required success | Next stage |
|---|---|---|
| `prizmkit-plan` | `PLAN_READY` | `prizmkit-implement` |
| `prizmkit-implement` | `IMPLEMENTED` | `prizmkit-code-review` |
| `prizmkit-code-review` | `REVIEW_PASS` | `prizmkit-test` |
| `prizmkit-test` | `TEST_PASS` | `prizmkit-retrospective` |
| `prizmkit-retrospective` | `status=RETRO_COMPLETE` with result `DOCS_UPDATED` or `NO_DOC_CHANGE` | `prizmkit-committer` |
| `prizmkit-committer` | explicit interactive confirmation, then `COMMITTED` | end |

`TEST_NOT_APPLICABLE` is not a valid lifecycle success. Lightweight changes must execute deterministic verification and return `TEST_PASS`.

### 4. Do Not Duplicate Stage Responsibilities

The composite must not:

- reinterpret a plan as implementation;
- repair production code outside `prizmkit-implement` or the Main-Agent review loop;
- claim tests passed without a consistent `test-report.md` and terminal `test-result.json`;
- reinterpret testing-domain results as runtime/session outcomes;
- perform retrospective documentation changes itself;
- stage or commit before `prizmkit-committer` applies the current execution's authorization boundary;
- invoke `prizmkit-deploy` as a hidden seventh stage.

## Failure and Repair Routing

Use the shared workflow state and authoritative stage evidence to determine routing. Do not blindly retry every failure.

### Review Failure

`REVIEW_NEEDS_FIXES` maps from the final review report result `NEEDS_FIXES`. Route to:

```text
prizmkit-implement
  → prizmkit-code-review
  → prizmkit-test
```

The Main-Agent review skill owns its internal review repairs and its internal ten-round limit before returning its terminal result. The outer workflow repair counter is separate.

### Test Non-Pass

`prizmkit-test` already performs bounded test construction, execution-failure repair, mandatory Main-Agent review, and optional independent review before returning. The composite consumes its terminal artifacts without recreating those loops.

```text
TEST_NEEDS_FIXES
  → preserve test-report.md and test-result.json
  → stop with the known remaining correction or delta-review requirement
  → caller owns any later review/retest decision

TEST_BLOCKED
  → preserve test-report.md and test-result.json
  → stop with the unresolved truth, input, safety, environment, or reliability blocker
```

The composite must not invoke implementation or Code Review automatically from inside the returned testing result unless its own explicitly authorized outer policy defines a new invocation. It must never treat either result as an AI CLI crash.

### Environment Block

`TEST_BLOCKED` means a safe testing verdict is unavailable because truth, required input, environment, permission, external-target safety, execution reliability, or required review input remains unresolved.

Interactive behavior:

```text
TEST_BLOCKED
  → persist the blocker
  → do not make speculative production edits
  → stop with a deterministic prizmkit-test resume entry
```

A trusted headless host performs its own bounded automatic environment recovery when invoking atomic stages. It does not invoke this composite workflow or silently turn a blocked result into success.

### Repair Limit

The outer orchestrator allows at most three automatic repair rounds. These are cross-stage rounds: one repair route from `implement` through all gates required by the repair scope.

```text
repair_round: 0 → 1 → 2 → 3
```

When the limit is reached:

- set workflow status to `WORKFLOW_BLOCKED`;
- preserve the latest reports and terminal results;
- report completed rounds and unresolved cause;
- report the exact skill, `artifact_dir`, and state path from which a user may resume after resolving the cause or explicitly authorizing another attempt;
- do not claim the requirement is complete.

The internal `prizmkit-code-review` limit of ten completed review rounds remains separate and does not increment `repair_round`.

## Commit Authorization Boundary

The composite may automatically reach `/prizmkit-committer`, but it must not silently create a Git commit.

Interactive execution requires the committer to:

1. verify all five preceding stage results for the same `artifact_dir`;
2. inspect the final workspace;
3. present intended files, diff summary, sensitive-file warnings, and the proposed Conventional Commit message;
4. wait for explicit user confirmation from the current user;
5. create and verify the local commit only after confirmation.

Trusted headless execution is a separate atomic-stage path. It requires a host-defined non-interactive `mode`, a trusted `owner` identifier, and `local_commit_authorized=true`; it does not ask or wait. Unknown headless contexts are blocked. Remote publication is a separate host-runtime operation and is never decided by this composite workflow.

## Automatic Handoff and Manual Fallback

When the host supports semantic skill-to-skill invocation, the active composite invokes the next atomic stage after each permitted success transition.

When it does not:

1. update or verify workflow state;
2. stop without claiming the next stage ran;
3. print one exact recovery instruction:

```text
Next stage: /prizmkit-<skill>
artifact_dir: <same resolved artifact_dir>
workflow_state: .prizmkit/state/workflows/<requirement-slug>.json
```

The user can invoke that one atomic skill and this composite can resume with `resume` later.

## Resume Protocol

On resume:

1. Read the workflow state specified by `resume` or discover the target project's active workflow state.
2. Read `${SKILL_DIR}/references/workflow-state-protocol.md`.
3. Verify `spec.md`, `plan.md`, review report, test report/result pair, retrospective result, and current workspace against state.
4. If state is missing or stale, reconstruct the safest recoverable predecessor and report the reconstruction.
5. Continue from the first incomplete stage; never bypass a required gate based only on stale state.
6. Preserve the same `artifact_dir` and repair-round count.
7. When an external host is involved, let it validate its own checkpoint independently; never merge that checkpoint into workflow state.

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
  - RETRO_COMPLETE (DOCS_UPDATED | NO_DOC_CHANGE)
  - COMMITTED
commit: <hash>
push: not performed automatically
next_action: invoke /prizmkit-deploy separately if deployment is needed
```

If the user declines interactive commit confirmation, report `COMMIT_PENDING` rather than `WORKFLOW_COMPLETE` and provide the exact `/prizmkit-committer` resume entry.

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
