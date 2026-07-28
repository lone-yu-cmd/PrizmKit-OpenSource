---
name: "prizmkit-retrospective"
description: "Synchronize durable Prizm documentation for one caller-supplied project change, or record that no documentation update is warranted. Writes retrospective-result.json and returns RETRO_COMPLETE or RETRO_BLOCKED. (project)"
---

# PrizmKit Retrospective

`/prizmkit-retrospective` synchronizes durable project documentation for one explicitly supplied project change. It performs targeted structural synchronization and durable knowledge injection, or records `NO_DOC_CHANGE` when no update passes the Value Gate.

For first-time documentation setup, validation, rebuild, migration, or out-of-band repair after docs drift, use `/prizmkit-prizm-docs` independently. Retrospective consumes the established Prizm documentation policy but never invokes that Skill.

## Input

| Parameter | Required | Description |
|---|---|---|
| `artifact_dir` | Yes | Exact caller-supplied directory in which to write `retrospective-result.json`. |
| `change_paths` | Yes | Exact caller-supplied non-`.prizmkit/` `change_paths` whose current project changes are the only authoritative documentation input. An explicit empty list is allowed only for a caller-requested no-change determination. |
| `change_summary` | No | Supporting context only; it cannot establish a fact that the supplied project paths do not establish. |

Do not discover a different artifact directory, expand the path set, or infer prerequisite work.

## Atomic Boundary

`prizmkit-retrospective` owns only targeted structural documentation synchronization, durable knowledge injection, and `{artifact_dir}/retrospective-result.json` for the supplied paths. It does not invoke another Skill, does not read or mutate caller or checkpoint state, and does not choose stage order or routing.

It does not stage, commit, force-add, reset, checkout, or stash; it does not add, remove, or interpret `.gitignore` entries; and it does not directly edit generated platform outputs. `.prizmkit/**` is the PrizmKit framework directory, and this Skill owns only its exact documentation/result writes. The project controls whether those paths are ignored, untracked, or tracked; retrospective behavior is otherwise identical and never requires Git history. Capacity maintenance does not add a capacity state machine, fact scoring system, routing field, caller-state field, or fourth documentation level. The stage returns `RETRO_COMPLETE` or `RETRO_BLOCKED` and stops.

## When to Use

- A caller supplies exact project change paths that may affect durable documentation.
- A previously interrupted synchronization is resumed with the same exact inputs.
- The user explicitly requests a retrospective for one named project change.

## When NOT to Use

- Required paths are missing, unsafe, contradictory, outside the checkout, under `.prizmkit/`, or cannot be inspected.
- The caller asks this Skill to discover what work should be documented.
- First-time initialization or repository-wide out-of-band drift repair is needed.

## Exact Input Scope and Candidate Authority

Treat only the exact caller-supplied non-`.prizmkit/` `change_paths` as authoritative project-change input.

1. Normalize `artifact_dir` and every path exactly as supplied without broadening the set.
2. Reject paths outside the checkout, paths under `.prizmkit/`, and paths that do not belong to the supplied project change.
3. Inspect the current change only through exact pathspecs for the validated paths. Use narrowly required source context only when one eligible change raises a concrete ambiguity about its interface, caller, dependent, data flow, or behavior.
4. Generated artifacts, lifecycle records, caller metadata, `change_summary`, repository-wide discovery, and existing Prizm text must not independently establish a candidate fact or expand the input scope. Existing Prizm documents are target/current-state evidence only.
5. Map exact changes to only the affected targets and their necessary direct parent summaries or pointers. Never perform an unconditional repository-wide documentation rewrite.
6. If exact inputs cannot safely establish candidate or target scope, prepare `RETRO_BLOCKED` with the exact blocker.

Only targeted `.prizmkit/prizm-docs/` changes and `{artifact_dir}/retrospective-result.json` are outputs.

## Value and Cleanup Gates

Before retaining any candidate from an eligible source change, ask:

> Could a future AI that lacks this fact make an incorrect modification?

Retain a fact only when the answer is yes and the fact is current, durable, non-obvious, actionable, source-established, and placed at its lowest owning documentation level. Preserve rejected alternatives that future sessions are likely to propose again only when their durable reasons remain source-established.

Reject source-derivable structure or signatures, transient conclusions, historical/task/change material, duplicate meanings, stale or conflicting statements, test inventories, long procedures, parent-copied behavior, and low-value file lists or wording.

For every existing target:

1. Read each complete existing target before preparing its replacement, including every complete resolving parent/child pointer document necessary for that target.
2. Establish the protected set of still-valid contracts, constraints, traps, rules, data flow, dependencies, decisions, side effects, and safety/integrity knowledge.
3. Match existing and candidate facts by semantic meaning; update the canonical entry in place, merge synonymous facts, and remove obsolete, stale, derivable, duplicate, conflicting, or parent-copied material.
4. Add only genuinely new facts that pass the Value Gate and have no equivalent canonical entry. Append-only synchronization is prohibited.

Read `${SKILL_DIR}/references/knowledge-injection-steps.md` for candidate extraction and injection details.

## Capacity Preflight and Structural Sync

Read `${SKILL_DIR}/references/structural-sync-steps.md` and run its preflight for every target before replacement:

1. Measure the existing target's exact raw UTF-8 bytes.
2. Build the complete candidate result, including cleanup, before replacement and measure its exact raw UTF-8 bytes.
3. Apply path-classified hard limits: exact `.prizmkit/prizm-docs/root.prizm` uses 4096B, every other direct `.prizm` child uses 4096B, and every nested `.prizm` document uses 5120B. Classify normal below 80%, warning from 80% to below 90%, strong-warning from 90% through the hard limit, and error above the hard limit.
4. If current or candidate content reaches at least 80%, perform the minimum safe cleanup or semantic split before final replacement. Aim for 3277–3686B for a root/module index or 4096–4607B for a detail document, preserving approximately 10% headroom; never pad naturally concise output.
5. Never delete protected knowledge merely to satisfy a byte check. If protected knowledge cannot fit, use an unambiguous stable semantic boundary or block safely.

Plan and write bottom-up: create or update the most specific detail first, then synchronize its direct module index and the root project map only as concise summaries and resolving pointers. Complete `INTERFACES`, `DATA_FLOW`, `TRAPS`, `DECISIONS`, and full `RULES` remain in the owning detail rather than being copied into parents.

A real source submodule uses mirrored detail identity. An eligible flat module may use a deterministic semantic concern detail and direct-module `DETAILS` pointer only when the structural reference's identity, ownership, collision, and complete-terminal-shape checks pass.

## Safe Write, Verification, and Idempotency

1. Before the first write, preserve exact pre-write bytes for every existing target in the bounded affected set and record which candidates are new.
2. Do not replace a target whose candidate already violates format, identity, pointer, protected-knowledge, or capacity checks.
3. Write the validated affected set bottom-up. After each write, re-read the actual file rather than trusting the proposed content.
4. Re-read every written `.prizm` file as raw bytes, recompute its raw UTF-8 byte length, apply its exact hard limit and warning band, validate its format, and resolve every affected pointer in both directions. Validate all affected parent and child documents, not only the last file written.
5. Review the final targeted documentation diff. Never report `RETRO_COMPLETE` after a failed check.
6. If any post-write check fails, restore every replaced target to its exact pre-write bytes and remove any invalid newly created target so no invalid oversized final document remains. Do not use Git reset, checkout, or stash for restoration.
7. Compare each validated candidate with current target bytes before replacement. If byte-identical, do not rewrite or reorder the document. With identical source changes and inputs and no intervening project change, a second run produces no `.prizm` content diff and returns `NO_DOC_CHANGE` with an already-synchronized reason.

When `.prizmkit/prizm-docs/` does not exist, record `NO_DOC_CHANGE` with reason `PRIZM_DOCS_NOT_INITIALIZED` and recommend initialization as a separate action.

## Capacity Blocker Contract

If protected knowledge cannot be compressed safely and no unambiguous stable split exists, do not leave the oversized candidate as final content. Restore any earlier writes from this attempt and write `RETRO_BLOCKED` with `result: null`.

The existing seven fields carry all evidence; add no new field. Put the exact target path, measured current or candidate bytes, applicable limit/band, protected knowledge that prevented trimming, and concrete recommended split boundary in `reason`. Put only checks actually attempted, including candidate capacity or pointer checks, in `validation`. Preserve the exact supplied `change_paths`; `documentation_paths` follows the schema and lists only documentation paths actually changed during the attempt. Never invent validation or claim success after restoration/validation failure.

## Result Artifact

Read `${SKILL_DIR}/references/retrospective-result-schema.json` and atomically write `{artifact_dir}/retrospective-result.json` with exactly these seven keys:

```json
{
  "schema_version": 1,
  "outcome": "RETRO_COMPLETE",
  "result": "DOCS_UPDATED",
  "reason": "Durable module contract changed and affected documentation passed validation",
  "change_paths": ["src/example.py"],
  "documentation_paths": [".prizmkit/prizm-docs/example/module.prizm"],
  "validation": ["python3 core/templates/hooks/validate-prizm-docs.py --all"]
}
```

Every retrospective artifact has exactly these seven keys: `schema_version`, `outcome`, `result`, `reason`, `change_paths`, `documentation_paths`, and `validation`.

A capacity or validation blocker uses the same shape without adding state:

```json
{
  "schema_version": 1,
  "outcome": "RETRO_BLOCKED",
  "result": null,
  "reason": "Target .prizmkit/prizm-docs/example/module.prizm candidate=5200B limit=5120B; protected public contract prevents trimming; ownership check could not prove a stable split; recommended boundary: separate transport from persistence behavior",
  "change_paths": ["src/example.py"],
  "documentation_paths": [],
  "validation": ["candidate raw UTF-8 capacity check: 5200B > 5120B", "semantic ownership check: ambiguous"]
}
```

- `RETRO_COMPLETE` pairs only with `DOCS_UPDATED` or `NO_DOC_CHANGE`.
- `DOCS_UPDATED` requires non-empty documentation and validation lists.
- `NO_DOC_CHANGE` uses a concrete reason and truthful empty or unchanged path evidence.
- `RETRO_BLOCKED` uses `result: null`, a non-empty exact reason, the exact input paths, only truthful documentation paths, and only checks actually attempted.

Do not add checkpoint, routing, capacity-state, caller-state, evidence-manifest, hash, or attestation fields.

## Output

Return only:

- `artifact_dir` and `retrospective-result.json` path;
- `RETRO_COMPLETE` with `DOCS_UPDATED` or `NO_DOC_CHANGE`, or `RETRO_BLOCKED` with the exact blocker;
- documentation paths updated or intentionally unchanged;
- durable knowledge decisions and validation evidence.

Return only the listed retrospective outputs. Do not invoke another Skill.
