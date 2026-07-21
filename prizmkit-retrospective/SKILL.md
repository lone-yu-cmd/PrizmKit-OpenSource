---
name: "prizmkit-retrospective"
description: "Mandatory retrospective stage after a formal requirement passes code review and testing. Synchronizes durable Prizm documentation or records that no documentation change is needed, updates workflow state, and hands off to prizmkit-committer. (project)"
---

# PrizmKit Retrospective

`/prizmkit-retrospective` is the mandatory documentation and durable-knowledge stage after `prizmkit-test` returns `TEST_PASS`.

It performs two jobs:

1. **Structural Sync** — reflect changed code structure, interfaces, dependencies, and file mappings in `.prizmkit/prizm-docs/` when the documentation system exists.
2. **Knowledge Injection** — add durable TRAPS, RULES, and DECISIONS discovered during the task when such knowledge exists.

The stage must always run for a formal requirement. When no documentation update is warranted, it records `NO_DOC_CHANGE` as a successful retrospective result rather than silently skipping the stage.

For first-time documentation setup, validation, rebuild, migration, or out-of-band repair after docs drift, use `/prizmkit-prizm-docs` independently.

## Formal Lifecycle Position

```text
prizmkit-plan
  → prizmkit-implement
  → prizmkit-code-review
  → prizmkit-test
  → prizmkit-retrospective
  → prizmkit-committer
```

## Atomic Stage Boundary

`prizmkit-retrospective` owns only structural documentation synchronization, durable knowledge injection, and retrospective result recording. It writes its truthful completion status and result plus `next_stage`, then returns control. It must not invoke `prizmkit-committer` itself; the active orchestrator owns the next-stage invocation.

## When to Use

- After `/prizmkit-test` returns `TEST_PASS` for a formal requirement.
- When workflow state resumes a previously interrupted retrospective.
- When the user explicitly requests a retrospective or documentation synchronization outside a formal requirement.

## When NOT to Use

- The requirement has not passed code review and testing.
- `TEST_NEEDS_FIXES` or `TEST_BLOCKED` remains unresolved.
- The request is a direct edit outside the formal requirement lifecycle, unless the user explicitly asks for documentation maintenance.
- First-time docs initialization or out-of-band docs repair; use `/prizmkit-prizm-docs` instead.

## Preconditions and Artifact Identity

1. Reuse the caller's `artifact_dir`; do not select another requirement.
2. Confirm the latest review result is `PASS`.
3. Confirm the latest testing result is `TEST_PASS`.
4. Read the final source diff with `.prizmkit/` excluded, then use `spec.md`, `plan.md`, the final `review-report.md`, `test-report.md`, and `test-result.json` only as supporting context for the non-`.prizmkit/` changes.
5. If the workflow state is missing or stale, reconstruct it from those authoritative artifacts and report the reconstruction.

`.prizmkit/` is always excluded from retrospective project-change input scope. Do not treat any file under `.prizmkit/`—including plans, artifacts, state, evidence, or existing Prizm docs—as a changed project file from which structural or durable knowledge is inferred. Required lifecycle state/evidence writes and targeted `.prizmkit/prizm-docs/` updates remain outputs; documentation changes must be justified only by observed non-`.prizmkit/` project changes.

## Job 1: Structural Sync

When `.prizmkit/prizm-docs/` exists, read `${SKILL_DIR}/references/structural-sync-steps.md` and synchronize documentation with the final codebase changes.

Review only changed project files outside `.prizmkit/`:

- added, modified, deleted, and renamed source files;
- structural module files, configuration, interfaces, and tests when they reveal durable project behavior;
- documentation mappings affected by those non-`.prizmkit/` project changes;
- stale pointers and stale traps implicated by those project changes;
- format, pointer, size, and memory-hygiene constraints for any docs the retrospective updates.

Never use `.prizmkit/` changes themselves as structural-sync input.

When `.prizmkit/prizm-docs/` does not exist, do not pretend structural sync occurred. Record `NO_DOC_CHANGE` with reason `PRIZM_DOCS_NOT_INITIALIZED` and recommend `/prizmkit-init` or `/prizmkit-prizm-docs` for a future setup. The formal lifecycle may still continue because initialization is a soft prerequisite.

Do not create an L2 document merely because one was missing during implementation. Create it only when the final change contains meaningful durable module knowledge.

## Job 2: Knowledge Injection

When the final project change outside `.prizmkit/` reveals durable knowledge, read `${SKILL_DIR}/references/knowledge-injection-steps.md` and inject only stable product/domain knowledge into Prizm docs.

Candidate knowledge includes:

- new traps, race conditions, or surprising coupling;
- architectural rules or decisions;
- interface or contract changes;
- dependencies affecting module behavior;
- observable behavior changes;
- test-discovered boundaries or regression rules.

Do not write transient artifact paths, task IDs, branch names, dates, session/run metadata, or changelog material into Prizm docs.

When no durable structural or knowledge change exists, return `NO_DOC_CHANGE` and explain why.

## Verification and Staging

1. Validate any updated docs using the project documentation rules.
2. Review the final diff and ensure only intended documentation changes are present.
3. Do not change the target project's Git or ignore policy. If the host or project workflow stages docs, report what was staged; otherwise leave staging to `/prizmkit-committer`.
4. Never claim documentation synchronization passed if validation failed.

## Retrospective Result

Write `{artifact_dir}/retrospective-result.json` for every formal requirement:

```json
{
  "status": "completed",
  "stage_result": "RETRO_COMPLETE",
  "result": "DOCS_UPDATED",
  "reason": "Durable module interfaces and traps changed",
  "review_verdict": "PASS",
  "test_verdict": "TEST_PASS"
}
```

`status=completed` is the stable lifecycle status. `stage_result=RETRO_COMPLETE` marks successful retrospective completion; `result` must be exactly `DOCS_UPDATED` or `NO_DOC_CHANGE`. Use `result=NO_DOC_CHANGE` with a concrete reason when no documentation update is warranted. This artifact is the retrospective gate evidence consumed by the committer and external automation; workflow state alone does not prove completion.

## Workflow State and Handoff

Before reading or updating workflow state, read `${SKILL_DIR}/references/workflow-state-protocol.md`.

On successful completion, update `.prizmkit/state/workflows/<requirement-slug>.json`:

```json
{
  "stage": "retrospective",
  "status": "completed",
  "stage_result": "RETRO_COMPLETE",
  "completed_stages": ["plan", "implement", "code-review", "test", "retrospective"],
  "next_stage": "committer",
  "resume_from": "prizmkit-committer"
}
```

Use `status=completed` and `stage_result=RETRO_COMPLETE` for both successful outcomes, with `result=DOCS_UPDATED` when durable docs changed or `result=NO_DOC_CHANGE` when the stage completed without a docs update. Both result values permit the commit stage.

If documentation validation or synchronization cannot safely complete, return `RETRO_BLOCKED`, do not commit, and provide the exact recovery entry.

## Output and Handoff

Report:

- `{artifact_dir}/retrospective-result.json` with `DOCS_UPDATED` or `NO_DOC_CHANGE`;
- docs updated, created, or intentionally unchanged;
- durable knowledge decisions;
- validation evidence;
- workflow state path and status;
- the same `artifact_dir` for the next stage.

After `RETRO_COMPLETE`:

```text
RETRO_COMPLETE
  → /prizmkit-committer
```

If workflow state names an active `orchestrator`, return `RETRO_COMPLETE`, `stage_result`, the retrospective/state paths, and `next_stage=committer` to it; do not invoke the committer independently. For direct stage use, provide the deterministic `/prizmkit-committer` invocation; a host may perform that semantic handoff on the user's behalf.
