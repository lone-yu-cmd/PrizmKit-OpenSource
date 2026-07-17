# PrizmKit Workflow Eval Plan

These prompts test the orchestration skill's objective behavior rather than the quality of any product implementation.

## Assertions

### Eval 1 — Full feature orchestration

- The workflow begins with `prizmkit-plan`.
- All six lifecycle skills appear in the fixed order.
- One `artifact_dir` is preserved across stages.
- Commit confirmation is required before local commit.
- Production-affecting test failures route through code review.

### Eval 2 — API/schema change routing

- API/schema changes are treated as production-affecting.
- The workflow does not stop after generating a plan.
- `TEST_PASS` and retrospective completion are required before committer.
- No success is reported before commit confirmation.

### Eval 3 — Blocked workflow resume

- Existing workflow state or artifacts are read before planning a new change.
- The original `artifact_dir` is reused.
- A resolved `TEST_BLOCKED` state resumes at `prizmkit-test`.
- No speculative production edit is made to resolve an environment blocker.

### Eval 4 — Direct-edit boundary

- A typo-only request is identified as a direct low-risk edit.
- The six-stage workflow is not forced without explicit user confirmation.
