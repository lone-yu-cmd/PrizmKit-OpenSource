---
name: "prizmkit-committer"
description: "Perform one commit stage for a caller-supplied final change. Either preview and create an explicitly confirmed interactive local commit, or validate the final diff and write an exact runtime-commit-request.json without Git mutation. Returns only commit-stage results. (project)"
---

# PrizmKit Committer

`/prizmkit-committer` handles one caller-supplied final change through one explicit operation:

- `operation=interactive-commit`: preview, confirm, stage, commit, and verify locally.
- `operation=prepare-runtime-commit`: validate the intended change and write an exact commit request without staging or committing.

Remote publication is outside this Skill.

## Input

| Parameter | Required | Description |
|---|---|---|
| `artifact_dir` | Yes | Exact caller-supplied artifact root for this commit stage. |
| `operation` | Yes | `interactive-commit` or `prepare-runtime-commit`. |
| `evidence_paths` | Yes | Exact caller-supplied project-relative artifacts that establish commit readiness. |
| `intended_paths` | Interactive only: Yes | Exact unique project-relative final paths approved by the caller for preview and staging. It is never inferred from workspace breadth. |
| `support_validation_evidence` | Interactive conditional | Required only for an explicit host/platform support path. Supply one exact record per support path with `path`, named semantic `contract`, completed `validation`, `result=PASS`, and an exact `evidence_path` also present in `evidence_paths`. A path is not support merely because it is under `.prizmkit/**`. |
| `excluded_paths` | No | Exact caller-owned operation metadata that the selected consumer also excludes. It cannot hide unrelated project changes. |
| `request_path` | Preparation only | Must equal `{artifact_dir}/runtime-commit-request.json`. |

Do not discover another artifact root or infer the operation from provider, platform, prompt style, tracking policy, or human availability.

## Stage Boundary

This Skill owns only final-change inspection and its selected commit operation. It does not invoke another Skill.

In preparation mode it must not stage, unstage, commit, amend, reset, merge, or push.

## Framework Directory and Git Policy

`.prizmkit/**` is the PrizmKit framework directory, not a blanket Git exclusion. The project alone decides which paths are ignored, untracked, or tracked. A Git-visible intended path must not be rejected, specially admitted, or require documentation-specific evidence solely because it is under `.prizmkit/**`.

Ignored paths remain naturally absent. Never force-add a path, add/remove/interpret `.gitignore` entries, or require a project to track framework artifacts. Exact Runtime request/checkpoint paths and installed Runtime/state may remain outside a task commit only because of their concrete operation-owned support/bookkeeping role. Global Secret and sensitive-content checks apply to every intended path, including framework paths; this contract creates no Secret exception.

## Step 1: Validate Supplied Evidence and Final Change

1. Resolve `artifact_dir` and every `evidence_paths` entry exactly as supplied. For interactive operation, also resolve every exact `intended_paths` entry without broadening it.
2. Reject missing, unreadable, stale, contradictory, blocked, or explicitly non-passing readiness evidence.
3. Inspect staged, unstaged, untracked, deleted, and renamed Git-visible files with bounded Git status/diff commands. Ignored files are not discovered.
4. Confirm every intended path belongs to the supplied requirement, a concrete dependency, its tests, project documentation/configuration, a framework-managed requirement output, or an explicitly caller-owned support artifact. Unknown or unrelated Git-visible changes block rather than entering or disappearing from the manifest.
5. For each explicit host/platform support path, require one unique `support_validation_evidence` record whose `path` equals that manifest entry, whose `evidence_path` is supplied and readable, and whose named contract, completed validation, and `result=PASS` agree with that evidence. Do not apply this requirement to a path merely because its prefix is `.prizmkit/` or `.prizmkit/prizm-docs/`.
6. Reject unresolved merge state and scan all intended content/diffs for real environment files, credentials, Secrets, private keys, certificates, local settings, and other sensitive material.
7. Confirm no requested task output remains to be generated after this stage.
8. Require every intended path to be Git-visible and stageable under existing project policy. If an exact path is ignored or otherwise not stageable, report its ordinary Git visibility/policy result; never force-add or change policy.

The caller decides which readiness evidence is required and how the returned stage result is used. The Skill validates supplied evidence but does not infer a larger lifecycle.

## Step 2: Classify Paths and Build the Exact Manifest

Generate one concise Conventional Commit message:

```text
<type>(<scope>): <description>
```

Classify observed changes by semantic role, not by a blanket `.prizmkit/**` prefix:

- **task-owned**: justified source, tests, documentation, configuration, dependencies, and framework-managed requirement output, including safe Git-visible `.prizmkit/**` paths when they belong to the supplied change;
- **explicit interactive support**: host instruction/lock/config support named by the exact spec/plan, validated one-to-one, labeled separately, and confirmed by the user;
- **operation-owned Runtime bookkeeping/support**: exact request/checkpoint/caller-state paths, installed `.prizmkit/dev-pipeline/**`, Runtime state, installed host payloads, and local host settings that the active consumer contract identifies as support rather than task output;
- **project transient**: data naturally absent because the project's existing ignore policy excludes it;
- **sensitive**: Secrets, credentials, private environment, private keys/certificates, or local settings;
- **unknown Git-visible**: any remaining path whose task or explicit support ownership cannot be proven.

A Prizm documentation path has no separate commit-ownership class and requires no `retrospective-result.json` authorization. Retrospective may have created it, but Committer handles a Git-visible path through the same task justification, exact manifest, Secret scan, and receipt verification as any other path.

For `operation=interactive-commit`, validate caller-supplied `intended_paths` as the complete approved manifest. Every entry must be exact, unique, project-relative, currently Git-visible, stageable without force, and task-owned or explicitly validated support. Prohibit `.git/**`, exact operation-owned Runtime bookkeeping, installed host payload/state, Secrets, temporary files, and unrelated/unknown changes. Label explicit host support separately; do not label `.prizmkit/**` specially.

For `operation=prepare-runtime-commit`, construct a unique exact set of all justified task-owned Git-visible changed paths, including safe `.prizmkit/**` task output. Exclude only consumer-recognized semantic support/bookkeeping, sensitive, unrelated, or naturally ignored data. Exact caller metadata in `excluded_paths` is valid only when the Python Runtime independently excludes that same semantic role. Unknown Git-visible changes block.

Never use wildcard pathspecs, broad `git add .`, broad `git add -A`, or force-add. Exact literal path staging may use Git's update semantics for a listed deletion, but the path set must remain exactly the manifest.

## Step 3A: Interactive Commit

For `operation=interactive-commit`:

1. Present exact `intended_paths`, change summary, Secret/sensitive warnings, diff statistics, proposed message, intentionally excluded semantic support, and separate labels only for admitted host support.
2. Ask the current user to confirm that exact local commit.
3. Only after confirmation, stage with `git add -- <exact paths>` semantics using literal exact pathspecs for tracked changes, deletions, and explicitly named Git-visible new files; never stage workspace breadth or force-add ignored content.
4. Verify the staged path set exactly equals the confirmed manifest and no hook/incidental operation added a path.
5. Re-run global Secret checks against the exact staged snapshot.
6. Create the local commit and verify its hash, message, parent, committed path set, and remaining workspace changes against the confirmed manifest.
7. Return `COMMITTED`, commit hash/message, committed paths, and intentional remaining changes.

If confirmation is declined, return `COMMIT_DECLINED` without Git mutation.

## Step 3B: Runtime Commit Request

For `operation=prepare-runtime-commit`:

1. Require `request_path={artifact_dir}/runtime-commit-request.json` and exclude that exact operation-owned request plus the caller-supplied Runtime checkpoint from `intended_paths`.
2. Read current full `HEAD` as `base_head`.
3. Write this JSON atomically without Git mutation:

```json
{
  "schema_version": 1,
  "artifact_dir": ".prizmkit/specs/example",
  "base_head": "<full current HEAD hash>",
  "commit_message": "feat(scope): concise description",
  "intended_paths": [
    ".prizmkit/prizm-docs/example.prizm",
    "src/example.py"
  ]
}
```

4. Verify:
   - `artifact_dir` equals the supplied artifact root;
   - `base_head` equals current `HEAD`;
   - `commit_message` is one non-empty line;
   - `intended_paths` is non-empty, unique, exact, project-relative, and equals the complete task-owned Git-visible change outside exact semantic support/bookkeeping;
   - no path escapes the checkout, enters `.git/**`, names exact Runtime-owned request/checkpoint data, or contains sensitive content;
   - no path was rejected solely because it is under `.prizmkit/**`;
   - every unknown Git-visible path caused a block rather than implicit exclusion.
5. Return `COMMIT_REQUEST_READY`, request path, message, intended paths, and explicit confirmation that no Git mutation occurred.
6. Stop.

The Python Runtime independently revalidates exact changed/staged/committed sets, safety, base/message/receipt, and post-commit bookkeeping order.

## Output

Interactive operation returns exactly one of:

```text
COMMITTED | COMMIT_DECLINED | COMMIT_BLOCKED
```

Preparation operation returns exactly one of:

```text
COMMIT_REQUEST_READY | COMMIT_BLOCKED
```

Every blocked result includes concrete missing evidence, unsafe paths, or validation errors. Return only the listed commit-operation outputs.
