# Knowledge Injection — Exact-Scope Value and Cleanup Steps

## 1. Establish candidate fact authority

Gather candidate knowledge only from actual project changes in the exact validated non-`.prizmkit/` input paths:

- `git diff HEAD -- <exact validated change_paths>` using literal pathspecs is the source of truth for eligible changes; never broaden the diff to `.` or use repository-wide status/discovery to add paths.
- Current source content at those exact paths may clarify the diff.
- Narrowly required unchanged source context (an interface, direct caller, direct dependent, or test) may be read only when an eligible diff raises a concrete ambiguity that cannot be resolved from the changed path itself.
- Existing affected Prizm docs may be read only as update targets, pointer maps, protected-current-knowledge evidence, and duplicate/staleness checks.

Generated artifacts, caller metadata, and existing Prizm text must not independently establish a candidate fact, expand `change_paths`, or turn an unrelated document into a target. `change_summary` is supporting context only. Reuse current Main-Agent source understanding when available, but do not treat lifecycle artifacts, completion notes, task IDs, or prior narrative as source evidence.

## 2. Apply the future-incorrect-modification Value Gate

For every candidate, ask exactly:

> Could a future AI that lacks this fact make an incorrect modification?

Retain it only when the answer is yes and current eligible source proves that it is durable, non-obvious, actionable for future modification, and owned by the target level.

High-value candidate classes include:

- non-obvious public interfaces and wire contracts;
- data flow, side effects, transactions, integrity boundaries, or surprising coupling;
- cross-module constraints and non-obvious dependencies;
- security, data-integrity, concurrency, transaction, and compatibility rules;
- actual traps, race conditions, failure modes, or unsafe-looking alternatives;
- architectural rules or durable decisions with rationale;
- observable behavior boundaries whose omission could cause a regression;
- rejected alternatives that future sessions are likely to propose again.

For a likely-to-recur rejected alternative, retain the alternative and its reason only when current eligible source establishes both. Do not retain a rejected option merely as design history.

Reject candidates that are source-derivable structure or signatures, transient implementation conclusions, historical task/change narrative, duplicate meanings, stale/conflicting statements, test inventories, coverage lists, routine file inventories, long procedures, low-value wording, or behavior already complete in a more specific child.

## 3. Extract only observed durable knowledge

### TRAPS

Use `- [SEVERITY] <description> | FIX: <approach>` and include only source-established non-obvious failure risks.

- `[CRITICAL]`: data loss, security failure, financial error, or crash.
- `[HIGH]`: functional failure, silent error, data-integrity risk, or interface incompatibility.
- `[LOW]`: misleading naming, non-intuitive API, or minor quality/performance risk that still passes the Value Gate.

Optional `REF` or `STALE_IF` metadata is allowed only when it is durable and source-relevant. For an affected `[REVIEW]` trap, remove the marker only when exact eligible source proves it still valid; delete it only when that source proves it obsolete. Lack of narrow evidence is not permission to delete it.

### RULES

Use `- MUST/NEVER/PREFER: <rule>`. Keep only constraints that a future modification must obey and that eligible source establishes.

### DECISIONS and rejected alternatives

Use `- <decision> — <durable rationale>` or `- REJECTED: <likely recurring alternative> — <why it remains rejected>`. Do not record obvious implementation choices or historical deliberation.

### Interfaces and behavior

Retain only non-obvious public/wire contracts, data flow, side effects, dependencies, and observable boundaries whose absence could cause an incorrect modification. Omit signatures and structure that direct source reading makes obvious.

## 4. Reconcile the current target before insertion

For every bounded affected target:

1. Read its current content and the necessary resolving direct parent/child pointers.
2. Build the protected set defined by the structural sync procedure before removing anything.
3. Match by semantic meaning, not exact wording.
4. Update the canonical entry in place when source changes an equivalent or conflicting fact; merge synonyms into one concise meaning.
5. Remove only source-proven obsolete facts plus stale, derivable, duplicate, low-value, or parent-copied material outside the protected set.
6. Add a candidate only when it passes the Value Gate and no equivalent canonical entry remains.
7. Preserve stable section and entry order; do not reorder unchanged entries or append alternate wording merely to make a diff.

Append-only injection is prohibited. Cleanup remains limited to the exact affected targets and their necessary direct parent summaries/pointers; do not opportunistically clean siblings.

## 5. Place knowledge at the lowest owning level

- Module behavioral details, `INTERFACES`, `DATA_FLOW`, `TRAPS`, complete `RULES`, `DECISIONS`, and rejected alternatives belong in the most specific mirrored or deterministic semantic detail.
- A real source-submodule boundary uses mirrored detail identity first.
- A flat module uses a semantic concern detail only when the structural procedure proves stable deterministic identity, explicit non-overlapping source-file ownership, capacity need, complete terminal shape, and a resolving direct-module `DETAILS` pointer.
- A direct module index keeps concise structure, navigation, critical summaries, and pointers; it does not copy complete child behavior.
- The root project map keeps only concise navigation and genuinely project-wide/cross-module summaries. An exact eligible change must establish the project-wide fact; existing root text cannot create one.

When one eligible change truly spans multiple affected modules, place complete knowledge in the lowest owning details and retain only the shortest useful cross-module summary/pointers at root. Do not infer cross-module scope from unrelated existing documentation.

## 6. Hand candidate results to capacity preflight

Do not write directly from extraction. Hand the complete cleaned candidate, protected set, exact target identity, and affected direct pointers to `structural-sync-steps.md` for raw UTF-8 size measurement, minimum safe cleanup or semantic split, bottom-up replacement, re-read validation, and safe restoration.

If no candidate survives the Value Gate and structural reconciliation produces no byte change, return a truthful `NO_DOC_CHANGE`. A repeated run over identical source and inputs must preserve byte-identical documentation and must not create duplicate, reorder-only, or synonym-only churn.

## 7. Enforce memory hygiene

Before final candidate validation, remove CHANGELOG sections/files, UPDATED/date metadata, feature/bug/refactor/task/session/run/pipeline/workflow IDs, branch names, absolute worktree paths, and `.prizmkit/specs` or `.prizmkit/dev-pipeline` artifact paths. Never trade protected durable product/domain knowledge for traceability noise.
