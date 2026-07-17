# PrizmKit Workflow State Protocol

`workflow-state.json` is optional runtime metadata created in a target project while a formal requirement is being developed. The published skills use it to preserve stage handoffs, repair routing, and resume information.

## Location

```text
.prizmkit/state/workflows/<requirement-slug>.json
```

The skill repository only documents this protocol. It does not create this directory until a skill is invoked in a target project, and it does not prescribe whether the target project commits, ignores, or shares the generated state.

## Authority

The state file is a workflow index, not the authority for requirement content:

| Information | Authority |
|---|---|
| Requirement goals and acceptance criteria | `.prizmkit/specs/<slug>/spec.md` |
| Implementation tasks and completion | `.prizmkit/specs/<slug>/plan.md` |
| Review findings and verdict | `.prizmkit/specs/<slug>/review-report.md` |
| Test execution and evidence | The test evidence package |
| Durable architecture knowledge | `.prizmkit/prizm-docs/` |
| Current stage and resume entry | Workflow state |

Every skill must compare workflow state with the actual artifacts and current workspace. A missing or stale state file must be reconstructed from authoritative artifacts and reported; it must not be treated as a successful state by itself.

## Schema

The minimum schema is:

```json
{
  "schema_version": 1,
  "artifact_dir": ".prizmkit/specs/001-example",
  "stage": "test",
  "status": "TEST_PASS",
  "completed_stages": [
    "plan",
    "implement",
    "code-review",
    "test"
  ],
  "repair_round": 0,
  "repair_scope": null,
  "next_stage": "retrospective",
  "resume_from": "prizmkit-retrospective"
}
```

### Fields

| Field | Meaning |
|---|---|
| `schema_version` | State schema version. Current value is `1`. |
| `artifact_dir` | The single requirement artifact directory reused by every stage. |
| `stage` | The stage that most recently wrote the state. |
| `status` | The truthful result of the current stage or workflow. |
| `completed_stages` | Ordered stages completed for this requirement. |
| `repair_round` | Outer automatic repair round, from `0` through `3`. |
| `repair_scope` | `null`, `production`, or `test-infrastructure`. |
| `next_stage` | The next semantic skill, or `null` after commit. |
| `resume_from` | The exact skill name that can resume the requirement, or `null` after commit. |

## Lifecycle States

Successful states:

```text
PLAN_READY
  → IMPLEMENTED
  → REVIEW_PASS
  → TEST_PASS
  → RETRO_COMPLETE
  → COMMIT_PENDING
  → COMMITTED
```

The retrospective stage may use `DOCS_UPDATED` or `NO_DOC_CHANGE` as its local status; both map to `RETRO_COMPLETE` for lifecycle progression.

Repair and blocked states:

```text
REVIEW_NEEDS_FIXES → IMPLEMENT_REPAIR
TEST_FAIL          → IMPLEMENT_REPAIR
TEST_BLOCKED       → PAUSED_FOR_ENVIRONMENT
RETRO_BLOCKED      → WORKFLOW_BLOCKED
WORKFLOW_BLOCKED   → resume only after the recorded blocker is resolved
```

## Repair Routing

```text
REVIEW_NEEDS_FIXES
  → implement
  → code-review
  → test

TEST_FAIL with repair_scope=test-infrastructure
  → implement
  → test

TEST_FAIL with repair_scope=production
  → implement
  → code-review
  → test

TEST_BLOCKED
  → do not modify production code speculatively
  → resolve the environment blocker
  → resume from test
```

The outer workflow permits at most three automatic repair rounds. The code-review skill has its own internal review-round limit. When an outer limit is reached, set `status` to `WORKFLOW_BLOCKED`, preserve the cause, and provide the next recovery entry instead of claiming success.

## Handoff Rules

1. The producing skill writes the next semantic stage after a successful result.
2. The next skill receives the same `artifact_dir`; it must not select another recent artifact.
3. A host that supports skill-to-skill invocation may continue automatically.
4. A host without that capability reports the exact `resume_from` skill and stops without pretending that the next stage ran.
5. A user confirmation before commit is a real gate; `COMMIT_PENDING` is not `COMMITTED`.
6. After commit, `next_stage` and `resume_from` are `null`.

## Recovery

When state is missing, stale, or inconsistent:

1. Read `spec.md` and `plan.md`.
2. Inspect task markers and the current workspace diff.
3. Read the latest review report and its final result.
4. Validate the latest test evidence and verdict.
5. Check the retrospective result when present.
6. Reconstruct the latest safe predecessor stage.
7. Write corrected state only after the reconstruction is explainable.
8. Report the reconstruction and the exact next action.

Do not use a stale success state to bypass review, testing, retrospective, or commit confirmation.
