# PrizmKit Workflow State Protocol

`workflow-state.json` is lifecycle metadata for one formal requirement. It preserves stage handoff, orchestrator ownership, and resume information without replacing skill-owned artifacts or any host-owned execution checkpoint.

## Location and Identity

Derive the path through `${SKILL_DIR}/references/artifact-identity.md`:

```text
.prizmkit/state/workflows/<requirement-identity>.json
```

The identity is the validated artifact-directory basename. An existing state file for a different `artifact_dir` is a blocking collision and is never overwritten or suffixed automatically. The active `artifact_dir` is preserved exactly across every stage:

```text
.prizmkit/specs/<requirement-slug>/
.prizmkit/bugfix/<bug-id>/
.prizmkit/refactor/<refactor-id>/
```

Never select another recent plan when resuming. Any external execution checkpoint remains separate from this state. Never merge, substitute, or infer one schema from the other.

## Authority

The state file is an index, not the authority for stage completion:

| Information | Authority |
|---|---|
| Requirement goals and acceptance criteria | `{artifact_dir}/spec.md` |
| Implementation tasks and completion | `{artifact_dir}/plan.md` plus current workspace |
| Review findings and result | `{artifact_dir}/review-report.md` |
| Test semantics and native execution | `{artifact_dir}/test-report.md` |
| Terminal testing result | `{artifact_dir}/test-result.json` |
| Retrospective completion | `{artifact_dir}/retrospective-result.json` |
| Durable architecture knowledge | `.prizmkit/prizm-docs/` |
| Local commit | Git history and runtime- or user-verified commit identity |
| Current stage, orchestrator, and resume entry | Workflow state |
| External orchestration progress | External host checkpoint |

Every consumer compares workflow state with the skill-owned artifacts and current workspace. Missing or stale state is reconstructed from those sources and is never accepted as success by itself.

## Schema

```json
{
  "schema_version": 1,
  "artifact_dir": ".prizmkit/specs/example",
  "orchestrator": "prizmkit-workflow",
  "stage": "test",
  "status": "completed",
  "stage_result": "TEST_PASS",
  "completed_stages": ["plan", "implement", "code-review", "test"],
  "repair_scope": null,
  "repair_round": 0,
  "next_stage": "retrospective",
  "resume_from": "prizmkit-retrospective"
}
```

### Fields

| Field | Meaning |
|---|---|
| `schema_version` | State schema version. |
| `artifact_dir` | Generic requirement artifact root reused by every stage. |
| `orchestrator` | Semantic coordinator identifier, or null for direct stage use. |
| `stage` | Stage that most recently wrote state. |
| `status` | Lifecycle status: `pending`, `in_progress`, `completed`, `failed`, or `skipped`. |
| `stage_result` | Coordinator-recorded lifecycle result mapped from a validated atomic result and its required artifacts, such as `PLAN_READY`, `IMPLEMENTED`, `REVIEW_PASS`, `REVIEW_NEEDS_FIXES`, `TEST_*`, `RETRO_COMPLETE`, or `COMMITTED`. |
| `completed_stages` | Ordered stages completed for this requirement. |
| `repair_scope` | Optional caller-owned routing scope. The test skill reports high-risk repairs through `test-result.json` instead of scheduling another stage. |
| `repair_round` | Optional outer cross-stage repair round, from 0 through 3. It is not a test-internal repair counter. |
| `next_stage` | Next semantic stage, or null when stopped. |
| `resume_from` | Exact atomic skill that can resume, or null when none is selected. |

`status` and `stage_result` are deliberately separate. Lifecycle status values must never be replaced with domain result values.

## Lifecycle and Result Mappings

```text
PLAN_READY
→ IMPLEMENTED
→ REVIEW_PASS
→ TEST_PASS
→ RETRO_COMPLETE
→ COMMIT_PENDING
→ COMMITTED
```

No formal stage is silently optional. Domain artifacts map to workflow state as follows:

```text
plan PLAN_READY                  → status=completed,  stage_result=PLAN_READY
plan PLAN_BLOCKED                → status=failed,     stage_result=PLAN_BLOCKED
implementation IMPLEMENTED       → status=completed,  stage_result=IMPLEMENTED
implementation repair/block      → status=failed,     stage_result=IMPLEMENT_REPAIR or IMPLEMENT_BLOCKED
review-report PASS               → status=completed,  stage_result=REVIEW_PASS
review-report NEEDS_FIXES        → status=failed,     stage_result=REVIEW_NEEDS_FIXES
test-result TEST_PASS, production_changed=false → status=completed, stage_result=TEST_PASS
test-result TEST_PASS, production_changed=true  → bounded re-entry; clear stale stage_result before pending delta Code Review
test-result TEST_NEEDS_FIXES     → status=failed,     stage_result=TEST_NEEDS_FIXES
test-result TEST_BLOCKED         → status=failed,     stage_result=TEST_BLOCKED
retrospective outcome=RETRO_COMPLETE, result=DOCS_UPDATED   → status=completed, stage_result=RETRO_COMPLETE
retrospective outcome=RETRO_COMPLETE, result=NO_DOC_CHANGE  → status=completed, stage_result=RETRO_COMPLETE
retrospective outcome=RETRO_BLOCKED                         → status=failed,    stage_result=RETRO_BLOCKED
runtime commit preparation       → status=in_progress, stage_result=COMMIT_PENDING
local commit confirmed           → status=completed,  stage_result=COMMITTED
commit blocked                   → status=failed,     stage_result=COMMIT_BLOCKED
```

`DOCS_UPDATED` and `NO_DOC_CHANGE` remain retrospective artifact `result` values. The workflow `stage_result` is the retrospective stage result `RETRO_COMPLETE`.

`TEST_PASS` requires both `test-report.md` and a consistent `test-result.json`. Their `production_changed` diagnostics must agree. Only `production_changed=false` is final Test authority for Retrospective. No manifest, attestation, evidence package, or test-internal checkpoint is part of this contract.

## Passing Production-Repair Re-entry

When consistent Test artifacts return `TEST_PASS` with `production_changed=true`, the atomic Test result remains truthful but the prior Code Review no longer covers the final production state. If `repair_round < 3`, the coordinator:

1. preserves the Test artifacts as repair evidence;
2. increments `repair_round`;
3. removes invalidated `code-review` and `test` entries from `completed_stages` while preserving authoritative predecessors;
4. sets `stage=code-review`, `status=pending`, and `stage_result=null` so no stale result survives re-entry;
5. sets `repair_scope=production`, `next_stage=code-review`, and `resume_from=prizmkit-code-review`;
6. invokes delta Code Review and then a fresh Test.

A fresh `TEST_PASS` with `production_changed=false` may complete Test and advance. Another production-changing pass repeats this route within the same outer budget. When `repair_round >= 3`, set `WORKFLOW_BLOCKED` without Retrospective or commit progression.

## Non-Pass Results and Routing Boundary

`prizmkit-test` performs its own bounded failure repair and review loops before returning. The test skill never invokes another lifecycle stage.

```text
TEST_NEEDS_FIXES
→ a known correction remains
→ caller decides whether and how to arrange another invocation

TEST_BLOCKED
→ truth, input, safe environment, or reliable execution prevents a verdict
→ never make speculative production edits
→ caller or external host owns recovery policy
```

A test result is not an AI CLI session classification. `TEST_NEEDS_FIXES` and `TEST_BLOCKED` must not be rewritten as crash or infrastructure failure merely because they stop lifecycle progression.

Any outer repair or continuation policy is independently owned by the caller and cannot alter the test report. The Main-Agent test review limit of ten rounds, independent Test Reviewer limit of five responses, and execution-failure repair limit of three rounds are internal to one test invocation and do not update outer counters.

## Orchestrator Ownership and Handoff

1. An atomic stage performs only its own stage, writes its truthful result and artifact paths, and returns control.
2. When `orchestrator` is non-null, only that orchestrator invokes the next skill.
3. Direct atomic use returns only its local result and artifacts; it does not report or select another invocation.
4. Every handoff preserves the same `artifact_dir`.
5. External automation invokes atomic stages directly and does not nest the composite workflow.
6. Workflow state never replaces or absorbs an external host checkpoint.

## Commit Execution Ownership

Interactive execution:

```text
coordinator assembles exact intended_paths from all final Git-visible requirement paths, including justified `.prizmkit/**` output
  + separately labeled explicitly owned host support paths with one-to-one passing support_validation_evidence
→ committer validates ordinary task ownership, global Secret safety, and the exact files/message
→ waits for explicit current-user confirmation
→ stages exact pathspecs, creates, and verifies the local commit
```

The framework directory is not a blanket allowlist or denylist: a Git-visible `.prizmkit/**` path uses the same exact manifest, task justification, staged-set equality, Secret checks, and receipt verification as any other path, with no documentation-specific evidence. Ignored files remain absent and are never force-added. Exact Runtime request/checkpoint/state, installed Runtime/host payloads, sensitive, unknown, and unrelated paths remain excluded or blocking because of their semantic role. User confirmation alone is not host-support validation.

Pipeline execution:

```text
external coordinator validates its required gates and supplies exact readiness evidence
→ committer validates only that evidence and writes an exact runtime-commit-request.json
→ external coordinator maps COMMIT_REQUEST_READY to its checkpoint's in_progress/COMMIT_PENDING state
→ Python runtime validates the request, commits, verifies Git, and writes checkpoint completed/COMMITTED
→ remote publication remains separate
```

The preparation request is data for Runtime validation, not prompt-level authorization. The committer must not stage, commit, or predeclare COMMITTED in preparation mode. Safe Git-visible `.prizmkit/**` task output may appear in Runtime `intended_paths`; ignored paths remain absent, while exact Runtime bookkeeping/support and Secrets remain excluded. Runtime verifies the commit before writing its post-commit receipt/checkpoint and never retroactively inserts those writes into the committed snapshot.

## Recovery

When state is missing, stale, or inconsistent:

1. Reuse current context, then read `spec.md` and `plan.md` only when needed.
2. Inspect task markers and current workspace.
3. Read the current review report when needed to establish review authority.
4. Validate that `test-report.md` and terminal `test-result.json` exist, agree, and reflect the claimed result.
5. Validate `retrospective-result.json` when retrospective is claimed complete.
6. Verify the commit when commit is claimed complete.
7. Let an active external host validate its own checkpoint independently.
8. Reconstruct the latest safe predecessor and report the reconstruction.
9. Continue only from the first incomplete or invalid stage.

Stale state never bypasses review, testing, retrospective, commit preparation/execution, or external checkpoint enforcement.
