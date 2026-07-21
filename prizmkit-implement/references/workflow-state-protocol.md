# PrizmKit Workflow State Protocol

`workflow-state.json` is lifecycle metadata for one formal requirement. It preserves stage handoff, orchestrator ownership, and resume information without replacing skill-owned artifacts or any host-owned execution checkpoint.

## Location and Identity

```text
.prizmkit/state/workflows/<requirement-slug>.json
```

The active `artifact_dir` is preserved exactly across every stage:

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
| Local commit | Git history and confirmed or authorized commit identity |
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
  "status": "TEST_PASS",
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
| `status` | Lifecycle progression status, distinct from `stage_result`. |
| `stage_result` | Domain result such as `PASS`, `NEEDS_FIXES`, `TEST_*`, `DOCS_UPDATED`, or `NO_DOC_CHANGE`. |
| `completed_stages` | Ordered stages completed for this requirement. |
| `repair_scope` | Optional caller-owned routing scope. The test skill reports high-risk repairs through `test-result.json` instead of scheduling another stage. |
| `repair_round` | Optional outer cross-stage repair round, from 0 through 3. It is not a test-internal repair counter. |
| `next_stage` | Next semantic stage, or null when stopped. |
| `resume_from` | Exact atomic skill that can resume, or null when none is selected. |

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

No formal stage is silently optional. Domain artifacts map as follows:

```text
review-report PASS               → status=REVIEW_PASS, stage_result=PASS
review-report NEEDS_FIXES        → status=REVIEW_NEEDS_FIXES, stage_result=NEEDS_FIXES
test-result TEST_PASS            → status=TEST_PASS, stage_result=TEST_PASS
test-result TEST_NEEDS_FIXES     → status=TEST_NEEDS_FIXES, stage_result=TEST_NEEDS_FIXES
test-result TEST_BLOCKED         → status=TEST_BLOCKED, stage_result=TEST_BLOCKED
retrospective DOCS_UPDATED       → status=RETRO_COMPLETE, stage_result=DOCS_UPDATED
retrospective NO_DOC_CHANGE      → status=RETRO_COMPLETE, stage_result=NO_DOC_CHANGE
```

`TEST_PASS` requires both `test-report.md` and a consistent `test-result.json`. No manifest, attestation, evidence package, or test-internal checkpoint is part of this contract.

## Non-Pass Results and Routing Boundary

`prizmkit-test` performs its own bounded failure repair and review loops before returning. The test skill never invokes another lifecycle stage.

```text
TEST_NEEDS_FIXES
→ known correction or required delta review remains
→ caller decides whether and how to arrange another stage

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
3. Direct stage use may report a possible next invocation but does not claim it ran.
4. Every handoff preserves the same `artifact_dir`.
5. External automation invokes atomic stages directly and does not nest the composite workflow.
6. Workflow state never replaces or absorbs an external host checkpoint.

## Commit Authorization

Interactive execution:

```text
committer previews intended files and message
→ waits for explicit current-user confirmation
→ creates the local commit
```

Trusted headless execution:

```text
trusted host explicitly authorizes the current local task commit
→ committer verifies gates and commits automatically
→ remote publication remains separate
```

A self-declared or untrusted headless context does not authorize a commit.

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

Stale state never bypasses review, testing, retrospective, commit authorization, or external checkpoint enforcement.
