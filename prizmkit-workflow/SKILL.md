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
- `execution_mode`: `interactive`; external headless automation must invoke atomic stages directly and use its Python runtime for commit execution;
- `resume`: optional workflow state path or requirement slug for recovery.

If `description` is missing and no resumable workflow is supplied, ask for the requirement before invoking `prizmkit-plan`. External automation must invoke atomic stages directly with its own execution checkpoint rather than nesting this composite workflow.

## Core Orchestration Rules

### 1. Start with Plan

Invoke `/prizmkit-plan` with the requirement and any explicit `artifact_dir`. Do not write a second plan in this orchestrator.

If initialization context is missing, let `prizmkit-plan` use its source fallback. Initialization is not a hidden lifecycle stage.

### 2. Preserve Requirement Identity

Once `prizmkit-plan` resolves an `artifact_dir`, capture it and pass the exact same value to every later stage. Read `${SKILL_DIR}/references/artifact-identity.md` before deriving or opening workflow state. The artifact root is generic and is not restricted to one directory family:

```text
.prizmkit/specs/<requirement-slug>/
.prizmkit/bugfix/<bug-id>/
.prizmkit/refactor/<refactor-id>/
```

Never select a different most-recent plan when resuming or handing off. Derive the workflow state path from the exact artifact-directory basename, validate its safe identity, and fail closed if an existing state path belongs to another artifact:

```text
.prizmkit/state/workflows/<requirement-identity>.json
```

Read `${SKILL_DIR}/references/artifact-identity.md` for path/collision rules and `${SKILL_DIR}/references/workflow-state-protocol.md` for the shared state content contract. This workflow state remains distinct from any external host execution checkpoint. The target project controls whether generated `.prizmkit/` files are committed, ignored, or shared; do not modify its Git policy.

### 3. Advance Only on Truthful Success

After each atomic stage:

1. Read the stage-local result and stage-owned artifacts.
2. Validate those artifacts independently.
3. Map the domain result to this composite's lifecycle status and update workflow state itself.
4. Preserve the same `artifact_dir`.
5. Continue only on the permitted success result.
6. Supply explicit stage-local inputs to the next invocation; atomic Skills never read this composite's state or choose routing.
7. If the host cannot invoke another Skill automatically, stop with one deterministic next invocation and caller-owned state path.

Expected transitions:

| Stage | Required success | Next stage |
|---|---|---|
| `prizmkit-plan` | `PLAN_READY` plus valid `spec.md`/`plan.md` | `prizmkit-implement` |
| `prizmkit-implement` | `IMPLEMENTED` plus completed task markers | `prizmkit-code-review` |
| `prizmkit-code-review` | `PASS` plus valid `review-report.md` | `prizmkit-test` |
| `prizmkit-test` | `TEST_PASS` plus a consistent report/result pair with `production_changed=false` | `prizmkit-retrospective` |
| `prizmkit-retrospective` | `RETRO_COMPLETE` plus an artifact whose `outcome` and `result` agree | `prizmkit-committer` |
| `prizmkit-committer` | `COMMITTED` after explicit interactive confirmation | end |

Before accepting a Test transition, require `production_changed` to be a boolean and agree between `test-report.md` and `test-result.json`. A passing result with `production_changed=true` follows the bounded production-repair route below and is not final Test authority for Retrospective.

Before invoking `prizmkit-retrospective`, derive the exact changed project paths outside `.prizmkit/` and pass them as `change_paths` with a concise `change_summary`. Do not ask that atomic Skill to infer scope from this composite's state or earlier artifacts.

`TEST_NOT_APPLICABLE` is not a valid lifecycle success. Lightweight changes must execute deterministic verification and return `TEST_PASS`.

### 4. Do Not Duplicate Stage Responsibilities

The composite must not:

- reinterpret a plan as implementation;
- repair production code itself instead of invoking the appropriate atomic stage with explicit repair input;
- claim tests passed without a consistent `test-report.md` and terminal `test-result.json`;
- reinterpret testing-domain results as runtime/session outcomes;
- perform retrospective documentation changes itself;
- stage or commit before `prizmkit-committer` completes the interactive preview and confirmation boundary;
- invoke `prizmkit-deploy` as a hidden seventh stage.

## Failure and Repair Routing

Use caller-owned workflow state and authoritative stage artifacts to determine routing. Atomic Skills never own this decision.

### Review Failure

`REVIEW_NEEDS_FIXES` maps from the final review report result `NEEDS_FIXES`. Route to:

```text
prizmkit-implement
  → prizmkit-code-review
  → prizmkit-test
```

The Main-Agent review skill owns its internal review repairs and its internal ten-round limit before returning its terminal result. The outer workflow repair counter is separate.

### Passing Test with Production Repair

A `TEST_PASS` whose consistent final artifacts report `production_changed=true` proves the Test stage repaired production code after prior Code Review. It does not authorize Retrospective or Committer.

```text
TEST_PASS + production_changed=true + repair_round < 3
  → preserve the Test artifacts as repair evidence
  → increment the outer repair round
  → invalidate prior final Code Review/Test completion in coordinator state
  → clear stale stage_result before re-entry
  → invoke prizmkit-code-review review_scope=delta
  → require a fresh prizmkit-test result

fresh TEST_PASS + production_changed=false
  → prizmkit-retrospective

TEST_PASS + production_changed=true + repair_round >= 3
  → WORKFLOW_BLOCKED
```

On re-entry, retain only stages that remain authoritative before Code Review in `completed_stages`, set `repair_scope=production`, and set the next/resume entry to delta Code Review without inventing a new atomic result. Repeated Test production repairs consume the same existing outer repair budget; they do not create an unbounded success loop.

### Test Non-Pass

`prizmkit-test` already performs bounded test construction, execution-failure repair, mandatory Main-Agent review, and optional independent review before returning. The composite consumes its terminal artifacts without recreating those loops.

```text
TEST_NEEDS_FIXES
  → preserve test-report.md and test-result.json
  → when the outer repair budget remains, supply the exact correction to prizmkit-implement
  → require fresh prizmkit-code-review and prizmkit-test results
  → otherwise stop with WORKFLOW_BLOCKED

TEST_BLOCKED
  → preserve test-report.md and test-result.json
  → stop with the unresolved truth, input, safety, environment, or reliability blocker
```

The composite's bounded outer repair policy owns that fresh invocation route; it does not recreate the testing-local repair loop. It must never treat either non-pass result as an AI CLI crash.

### Environment Block

`TEST_BLOCKED` means a safe testing verdict is unavailable because truth, required input, environment, permission, external-target safety, execution reliability, or required review input remains unresolved.

Interactive behavior:

```text
TEST_BLOCKED
  → persist the blocker
  → do not make speculative production edits
  → stop with a deterministic prizmkit-test resume entry
```

An external headless runtime may perform its own bounded environment recovery when invoking atomic stages. It does not invoke this interactive composite workflow or silently turn a blocked result into success.

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

## Interactive Commit Boundary

The composite reaches `/prizmkit-committer operation=interactive-commit` but must not silently create a Git commit.

The composite must validate all prior stage artifacts, derive exact non-`.prizmkit/` source-change paths for retrospective input, and validate its result. It then assembles one exact interactive `intended_paths` manifest from every final Git-visible requirement output, regardless of whether a justified path is under `.prizmkit/**`. Ignored paths remain naturally absent. Prizm documentation has no separate commit-ownership or retrospective-evidence admission rule.

`.prizmkit/**` remains the framework capability boundary and ordinary Code Review black box, but project Git tracking is independent. The composite must not force-add a framework path, modify or interpret ignore policy, broadly stage, or reject a Git-visible intended path solely by directory name. Exact Runtime request/checkpoint/state and installed Runtime/host payloads remain outside the manifest because of their semantic support/bookkeeping role, not a blanket framework-directory rule. Global Secret checks apply equally to every intended path.

For each explicit host/platform support path, select and execute its applicable semantic contract before invoking Committer: instruction files require readable structure, resolvable project references, consistency with the exact requirement and applicable project conventions, and Secret scanning; lockfiles require parse/schema checks plus owning-installer or deterministic-regeneration parity; any other support class requires an exact project-native semantic validator named by the spec/plan. User confirmation alone is not support validation. A path is not host support merely because it is under `.prizmkit/**`.

Invoke Committer with the same `artifact_dir`, exact `evidence_paths`, exact caller-state/bookkeeping paths in `excluded_paths`, exact `intended_paths`, conditional one-to-one host `support_validation_evidence`, and `operation=interactive-commit`. Committer validates the exact manifest and staged-set equality, presents it, waits for confirmation, and creates it only after approval.

External headless orchestration supplies explicit readiness evidence to `operation=prepare-runtime-commit`, maps `COMMIT_REQUEST_READY` to its own pending state, and lets Python Runtime validate and execute the request. Safe Git-visible `.prizmkit/**` task output may appear in Runtime `intended_paths`; exact Runtime bookkeeping/support, Secrets, unrelated paths, and ignored paths do not. Remote publication remains separate.

## Automatic Handoff and Manual Fallback

When the host supports semantic skill-to-skill invocation, the active composite invokes the next atomic stage after each permitted success transition.

When it does not:

1. update or verify workflow state;
2. stop without claiming the next stage ran;
3. print one exact recovery instruction:

```text
Next stage: /prizmkit-<skill>
artifact_dir: <same resolved artifact_dir>
workflow_state: .prizmkit/state/workflows/<requirement-identity>.json
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
  - status=completed, stage_result=PLAN_READY
  - status=completed, stage_result=IMPLEMENTED
  - status=completed, stage_result=REVIEW_PASS
  - status=completed, stage_result=TEST_PASS
  - status=completed, stage_result=RETRO_COMPLETE (result=DOCS_UPDATED | NO_DOC_CHANGE)
  - status=completed, stage_result=COMMITTED
commit: <hash>
push: not performed automatically
next_action: invoke /prizmkit-deploy separately if deployment is needed
```

If the user declines interactive commit confirmation, preserve the committer stage as pending or in progress without a workflow `stage_result`, report the atomic operation result `COMMIT_DECLINED`, and provide the exact `/prizmkit-committer operation=interactive-commit` resume entry. `COMMIT_PENDING` is reserved for a validated Runtime commit request and must not represent an interactive decline.

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
