---
name: "prizmkit-committer"
description: "Final commit stage for a formal PrizmKit requirement. Verifies plan, implementation, Main-Agent review, testing, and retrospective gates; presents the intended commit scope and Conventional Commit message; waits for user confirmation; creates and verifies the local Git commit without automatically pushing. (project)"
---

# PrizmKit Committer

`/prizmkit-committer` is the final stage of the formal requirement lifecycle:

```text
prizmkit-plan
  → prizmkit-implement
  → prizmkit-code-review
  → prizmkit-test
  → prizmkit-retrospective
  → prizmkit-committer
```

It does not decide which formal gates can be omitted. It verifies that all five preceding stages completed for the same `artifact_dir`, then requests confirmation before creating the local commit.

## When to Use

- Workflow state reports `RETRO_COMPLETE`, `DOCS_UPDATED`, or `NO_DOC_CHANGE` for the active formal requirement.
- User confirms they want to create the local commit.
- User says "commit", "submit", "finish", or "done" after the formal gates have completed.

## When NOT to Use

- The working tree is clean and there is nothing to commit.
- Any preceding formal stage is missing, failed, blocked, or associated with a different artifact directory.
- Review has `NEEDS_FIXES` or tests have `TEST_FAIL`/`TEST_BLOCKED`.
- Retrospective has not completed, including an explicit `NO_DOC_CHANGE` result.
- User says only "ship it"; clarify commit versus deployment first.
- A merge conflict is unresolved.

## Mandatory Gate Policy

For a formal requirement, all gates are mandatory:

| Gate | Required evidence |
|---|---|
| Plan | `spec.md`, `plan.md`, and `PLAN_READY` for the same `artifact_dir` |
| Implement | All required tasks complete and `IMPLEMENTED` |
| Code review | Final `review-report.md` result `PASS` |
| Test | Final evidence result `TEST_PASS` for the final reviewed workspace |
| Retrospective | `RETRO_COMPLETE`, `DOCS_UPDATED`, or `NO_DOC_CHANGE` |

The committer must reject a state that merely claims a gate passed when the underlying artifact or current workspace contradicts it. If workflow state is missing, reconstruct it from authoritative artifacts and report the reconstruction before asking for confirmation.

## Workflow

### Step 1: Status and Gate Check

1. Read the workflow state and resolve the same `artifact_dir` used by all prior stages.
2. Verify `spec.md`, `plan.md`, final `review-report.md`, test evidence, and retrospective result.
3. Inspect:

```bash
git status
git diff --stat
git diff
```

4. Inspect modified, deleted, renamed, and untracked files.
5. Warn about sensitive-looking files such as `.env*`, credentials, secrets, private keys, and certificates.
6. Stop when any required gate is missing, stale, contradictory, failed, or blocked.

### Step 2: Generate Commit Message

Analyze the final diff and requirement context. Propose a concise Conventional Commit message:

```text
<type>(<scope>): <description>
```

Do not update `CHANGELOG.md` unless the user explicitly requests release-note work.

### Step 3: Commit Preview and Confirmation

Before any `git add` or `git commit` that changes the target project's Git state, present:

- intended files;
- added, modified, deleted, and renamed file summary;
- sensitive-file warnings;
- diff statistics and relevant summary;
- proposed commit message;
- whether any remaining changes are intentionally excluded.

Ask the user to confirm creation of this local commit. Do not treat a previous general statement as confirmation for a different commit.

### Step 4: Stage Safely After Confirmation

Never use `git add .` or `git add -A`.

1. Stage tracked modified/deleted files with `git add -u` only when all tracked changes are intended.
2. Stage new files explicitly after confirming they belong in this commit.
3. Verify staged content:

```bash
git diff --cached --stat
git diff --cached
```

If staged content differs from the confirmed change set, unstage and correct it before committing.

### Step 5: Commit and Verify

After confirmation and staged-content verification:

```bash
git commit -m "<type>(<scope>): <description>"
git log -1 --stat
git status
```

Report the commit hash and whether the working tree is clean or contains intentionally uncommitted changes.

### Step 6: Optional Push

Pushing is separate from committing. Ask explicitly:

```text
Push this commit to the remote?
```

A refusal or lack of permission means stop after the local commit. Never push automatically. Headless use must not push.

## Workflow State

Before reading or updating workflow state, read `${SKILL_DIR}/references/workflow-state-protocol.md`.

Before the confirmation preview, set:

```json
{
  "stage": "committer",
  "status": "COMMIT_PENDING",
  "completed_stages": ["plan", "implement", "code-review", "test", "retrospective"],
  "next_stage": "committer",
  "resume_from": "prizmkit-committer"
}
```

After a successful local commit, update the runtime state to:

```json
{
  "stage": "committer",
  "status": "COMMITTED",
  "completed_stages": ["plan", "implement", "code-review", "test", "retrospective", "committer"],
  "next_stage": null,
  "resume_from": null
}
```

The state file is generated in the target project under `.prizmkit/state/workflows/`; this skill does not prescribe whether the target project commits, ignores, or shares it.
