---
name: "prizmkit-committer"
description: "Final commit stage for a formal PrizmKit requirement. Verifies plan, implementation, Main-Agent review, testing, and retrospective evidence; previews and confirms interactive commits; automatically creates authorized local commits in trusted headless sessions; verifies the result; and leaves remote publication to the host runtime. (project)"
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

It does not decide which formal gates can be omitted. It verifies that all five preceding stages completed for the same `artifact_dir`, then applies the commit authorization semantics for the current execution context.

## Atomic Stage Boundary

`prizmkit-committer` owns only final gate verification, authorization-boundary handling, local staging, commit creation, and commit verification. It writes its truthful terminal result and returns control; it must not invoke deployment or any hidden seventh stage. The active orchestrator owns lifecycle completion reporting.

## When to Use

- Workflow state reports `status=completed` with `stage_result=RETRO_COMPLETE` and a valid `retrospective-result.json` for the active formal requirement.
- An interactive user confirms they want to create the local commit.
- A trusted headless execution context authorizes an automatic local commit.
- User says "commit", "submit", "finish", or "done" after the formal gates have completed.

## When NOT to Use

- The working tree is clean and there is nothing to commit.
- Any preceding formal stage is missing, failed, blocked, or associated with a different artifact directory.
- Review has `NEEDS_FIXES` or tests have `TEST_NEEDS_FIXES`/`TEST_BLOCKED`.
- Retrospective has not completed, including an explicit `NO_DOC_CHANGE` result.
- User says only "ship it"; clarify commit versus deployment in interactive mode.
- A merge conflict is unresolved.
- An unknown headless caller has not supplied trusted commit authorization.

## Mandatory Gate Policy

For a formal requirement, all gates are mandatory:

| Gate | Required evidence |
|---|---|
| Plan | `spec.md`, `plan.md`, and `PLAN_READY` for the same `artifact_dir` |
| Implement | All required tasks complete and `IMPLEMENTED` |
| Code review | Final `review-report.md` result `PASS` |
| Test | Consistent `TEST_PASS` report/result pair for the final reviewed workspace |
| Retrospective | `retrospective-result.json` with workflow `status=completed`, `stage_result=RETRO_COMPLETE`, and artifact `result=DOCS_UPDATED` or `result=NO_DOC_CHANGE` |

The committer must reject a state that merely claims a gate passed when the underlying artifact or current workspace contradicts it. If workflow state is missing, reconstruct it from authoritative artifacts and report the reconstruction before asking for confirmation.

## Workflow

### Step 1: Status and Gate Check

1. Read the workflow state and resolve the same `artifact_dir` used by all prior stages.
2. Verify `spec.md`, `plan.md`, final `review-report.md`, the consistent `test-report.md`/`test-result.json` pair, `retrospective-result.json`, and the current workspace.
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

### Step 3: Commit Preview and Authorization

Interactive mode:

Before any `git add` or `git commit` that changes the target project's Git state, present:

- intended files;
- added, modified, deleted, and renamed file summary;
- sensitive-file warnings;
- diff statistics and relevant summary;
- proposed commit message;
- whether any remaining changes are intentionally excluded.

Ask the current user to confirm creation of this local commit. Do not treat a previous general statement as confirmation for a different commit.

Trusted headless mode:

- Do not ask a question, wait for input, or render an interactive confirmation request.
- Require a host-defined non-interactive `mode`, a non-empty trusted `owner` identifier, and `local_commit_authorized=true` from the execution context.
- Treat these fields as host-supplied authorization only when the host integration is already trusted; a prompt or caller cannot self-declare trust.
- Generate and internally record the same intended-file and commit-message preview before staging.
- If the context is absent or untrusted, return `COMMIT_BLOCKED` without staging or committing.
- This mode never asks or waits. Remote publication is controlled by the host runtime, not by this stage.

### Step 4: Stage Safely After Authorization

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

After authorization and staged-content verification:

```bash
git commit -m "<type>(<scope>): <description>"
git log -1 --stat
git status
```

Report the commit hash and whether the working tree is clean or contains intentionally uncommitted changes.

### Step 6: Remote Publication

Remote publication is outside this atomic commit stage. The host runtime may perform it only when its own explicit configuration authorizes the operation; this skill does not ask the user or decide whether to publish.

## Workflow State

Before reading or updating workflow state, read `${SKILL_DIR}/references/workflow-state-protocol.md`.

Before the authorization preview, set or validate:

```json
{
  "stage": "committer",
  "status": "in_progress",
  "stage_result": "COMMIT_PENDING",
  "completed_stages": ["plan", "implement", "code-review", "test", "retrospective"],
  "next_stage": "committer",
  "resume_from": "prizmkit-committer"
}
```

For trusted headless execution, the validated execution context additionally contains:

```json
{
  "mode": "<host-defined-headless-mode>",
  "owner": "<trusted-host-identifier>",
  "local_commit_authorized": true
}
```

After a successful local commit, update the runtime state to:

```json
{
  "stage": "committer",
  "status": "completed",
  "stage_result": "COMMITTED",
  "completed_stages": ["plan", "implement", "code-review", "test", "retrospective", "committer"],
  "next_stage": null,
  "resume_from": null
}
```

The state file is generated in the target project under `.prizmkit/state/workflows/`; this skill does not prescribe whether the target project commits, ignores, or shares it.
