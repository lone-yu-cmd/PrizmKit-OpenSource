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

## When to Use

- After `/prizmkit-test` returns `TEST_PASS` for a formal requirement.
- When workflow state resumes a previously interrupted retrospective.
- When the user explicitly requests a retrospective or documentation synchronization outside a formal requirement.

## When NOT to Use

- The requirement has not passed code review and testing.
- `TEST_FAIL` or `TEST_BLOCKED` remains unresolved.
- The request is a direct edit outside the formal requirement lifecycle, unless the user explicitly asks for documentation maintenance.
- First-time docs initialization or out-of-band docs repair; use `/prizmkit-prizm-docs` instead.

## Preconditions and Artifact Identity

1. Reuse the caller's `artifact_dir`; do not select another requirement.
2. Confirm the latest review result is `PASS`.
3. Confirm the latest testing result is `TEST_PASS`.
4. Read the final diff, `spec.md`, `plan.md`, final `review-report.md`, final test evidence, and affected Prizm docs when present.
5. If the workflow state is missing or stale, reconstruct it from those authoritative artifacts and report the reconstruction.

## Job 1: Structural Sync

When `.prizmkit/prizm-docs/` exists, read `${SKILL_DIR}/references/structural-sync-steps.md` and synchronize documentation with the final codebase changes.

Review:

- added, modified, deleted, and renamed source files;
- L1 file counts and module mappings;
- L2 `KEY_FILES`, `INTERFACES`, `DEPENDENCIES`, and durable traps for affected modules;
- stale pointers and stale traps;
- format, pointer, size, and memory-hygiene constraints.

When `.prizmkit/prizm-docs/` does not exist, do not pretend structural sync occurred. Record `NO_DOC_CHANGE` with reason `PRIZM_DOCS_NOT_INITIALIZED` and recommend `/prizmkit-init` or `/prizmkit-prizm-docs` for a future setup. The formal lifecycle may still continue because initialization is a soft prerequisite.

Do not create an L2 document merely because one was missing during implementation. Create it only when the final change contains meaningful durable module knowledge.

## Job 2: Knowledge Injection

When the final change reveals durable knowledge, read `${SKILL_DIR}/references/knowledge-injection-steps.md` and inject only stable product/domain knowledge into Prizm docs.

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

## Workflow State and Handoff

Before reading or updating workflow state, read `${SKILL_DIR}/references/workflow-state-protocol.md`.

On successful completion, update `.prizmkit/state/workflows/<requirement-slug>.json`:

```json
{
  "stage": "retrospective",
  "status": "RETRO_COMPLETE",
  "completed_stages": ["plan", "implement", "code-review", "test", "retrospective"],
  "next_stage": "committer",
  "resume_from": "prizmkit-committer"
}
```

Use `status=DOCS_UPDATED` when durable docs changed, or `status=NO_DOC_CHANGE` when the stage completed without a docs update. Both are successful retrospective outcomes and permit the commit stage.

If documentation validation or synchronization cannot safely complete, return `RETRO_BLOCKED`, do not commit, and provide the exact recovery entry.

## Output and Handoff

Report:

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

If semantic handoff is supported, continue automatically. Otherwise provide the deterministic next invocation.
