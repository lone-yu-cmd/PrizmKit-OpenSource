# Structural Sync — Capacity-Safe Detailed Steps

## 1. Validate supplied changed files

Use only the caller-supplied `change_paths`. Normalize each repository-relative path, reject paths outside the checkout or under `.prizmkit/`, and verify its current added/modified/deleted/renamed state with exact pathspecs.

Do not expand the path set through repository-wide status or diff discovery. Never run an unconditional repository-wide documentation rewrite. If the validated list is empty, structural sync is not needed.

## 2. Map exact changes to a bounded target set

Read `.prizmkit/prizm-docs/root.prizm` only as the project map, then map each exact changed path through its MODULE_INDEX or MODULE_GROUPS pointer to the most specific existing documentation owner.

The writable set contains only:

- the most specific detail targets that own eligible changed paths;
- their necessary direct parent summary or pointer at each affected level;
- a new detail target only when the eligible source change proves meaningful durable behavior and deterministic identity;
- root only when module structure or its resolving module/group pointer changes.

Affected docs may be read to reconcile current content and resolve pointers, but they cannot independently add source facts or pull sibling docs into the writable set. Do not clean unrelated targets merely because they are stale or near a limit.

If a changed source path maps to no module, evaluate only that path and narrowly required directory context to determine whether its directory is a real logical module with entry/config/interface files or cross-module dependency use. Do not perform a repository scan to manufacture a module.

## 3. Classify eligible structural changes

- `A` added: update navigation only when the file passes the Value Gate; check source-established public/wire contracts.
- `D` deleted: remove stale owned navigation and source-invalidated knowledge.
- `M` modified: check non-obvious public/wire interfaces, dependencies, data flow, behavior, traps, rules, and decisions.
- `R` renamed: update only implicated ownership and resolving paths.

Skip structural writes for comments, whitespace, formatting, internal implementation detail with no durable contract/behavior impact, and test-only changes that reveal no durable boundary. Do not skip a bug or test change when its exact source evidence changes durable behavior or constraints.

## 4. Select the most specific detail identity

### Mirrored source identity

When identities compete, mirrored source identity takes precedence.

A real source submodule uses its mirrored detail path. Mirrored source identity takes precedence over a semantic concern with the same path or meaning. Update an existing mirrored detail before considering a semantic split.

A new mirrored detail uses these required sections:

```text
MODULE
FILES
RESPONSIBILITY
INTERFACES
KEY_FILES
DEPENDENCIES
TRAPS
```

Add `DATA_FLOW`, `RULES`, `DECISIONS`, rejected alternatives, or domain sections only for facts that pass the Value Gate.

### Deterministic semantic concern identity

For a flat source module, create a semantic concern detail only when current eligible source proves multiple stable product/domain behavior concerns and protected durable knowledge cannot fit one 5120B detail after safe cleanup. A semantic concern is not another documentation level.

Derive one deterministic concern slug:

1. Choose a concise stable product/domain concern name from current source responsibility; task, change, file-count, or temporary initiative labels are invalid.
2. Normalize the name with Unicode NFKC.
3. Apply Unicode lowercase.
4. Replace each maximal run of characters that is neither a Unicode letter nor a Unicode decimal digit with one ASCII hyphen.
5. Trim leading/trailing hyphens and require one non-empty, unambiguous lowercase kebab-case result.
6. Compare it with sibling semantic concerns, sibling `DETAILS` entries, and mirrored submodule paths. Task IDs, numeric suffixes, timestamps, and branch names are prohibited as collision workarounds.

The detail path is `.prizmkit/prizm-docs/<module>/<concern-slug>.prizm`. It has `MODULE`, `CONCERN`, `FILES`, `RESPONSIBILITY`, `INTERFACES`, `DATA_FLOW`, `KEY_FILES`, `DEPENDENCIES`, `RULES`, `TRAPS`, and `DECISIONS`; use `<SECTION>: none` rather than invented filler when a required behavioral section has no qualifying fact.

`FILES` is a non-empty exhaustive normalized source-file ownership list for the concern. Sibling semantic details require explicit non-overlapping `FILES` ownership. The direct module parent has exactly one `DETAILS` pointer:

```text
- <concern-slug>: <concise stable behavior summary> -> .prizmkit/prizm-docs/<module>/<concern-slug>.prizm
```

The pointer path, target `MODULE`, normalized `CONCERN` slug, and `FILES` ownership must agree. Mirrored source identity takes precedence; ambiguity, collision, or overlapping ownership blocks the split. Never add a suffix or partial semantic document to guess around it.

## 5. Preflight every target before replacement

For each target in the bounded writable set:

1. Read current content and resolving parent/child pointers. For an existing target, preserve its exact pre-write bytes; for a new target, record that no pre-write file exists.
2. Measure the current target before replacement using exact raw UTF-8 bytes, never characters, lines, rounded kilobytes, or locale-dependent encoding.
3. Establish a protected set before cleanup. It includes every still-valid public or wire contract, CRITICAL/HIGH trap, data-flow or data-integrity constraint, security/concurrency/transaction/compatibility rule, cross-module rule, non-obvious dependency, side effect, and durable decision with necessary rationale.
4. Build the complete candidate result before replacement. Match existing and candidate facts by meaning; update the canonical entry in place, merge synonyms, remove equivalent, stale, derivable, conflicting, duplicate, or parent-copied material, and never append another version of the same knowledge.
5. Measure the candidate as exact raw UTF-8 bytes and classify both current and candidate against the target's level.

Capacity limits and bands:

- Exact root project map: hard limit 4096B.
- Direct module index: hard limit 4096B.
- Nested mirrored or semantic detail: hard limit 5120B.
- normal: `size * 100 < limit * 80`.
- warning: `size * 100 >= limit * 80` and `size * 100 < limit * 90`.
- strong-warning: `size * 100 >= limit * 90` and `size <= limit`.
- error: `size > limit`.

When the current or candidate reaches at least 80%, perform the minimum safe cleanup or semantic split before final replacement:

1. trim stale, source-derivable, procedural, historical, transient, and low-value wording;
2. merge synonymous facts and remove duplicate meanings;
3. move child-owned behavior from the root/module index into the existing or newly justified resolving detail;
4. if one detail still cannot retain protected durable knowledge within 5120B, use the deterministic semantic split only when its stable identity and non-overlapping ownership are unambiguous.

Aim for 3277–3686B for a root/module index and 4096–4607B for a detail document, preserving approximately 10% headroom. Do not pad naturally concise output and do not trim merely to one byte below a hard limit. A post-remediation warning-range result is valid; do not force a needless split when the minimum safe cleanup establishes the target range.

Never remove protected knowledge solely to pass capacity validation. If it cannot fit after concise wording, safe movement, or an unambiguous split, do not replace that target.

## 6. Write bottom-up

Prepare all candidates before the first replacement and write only after each candidate passes its local format, identity, protected-set, and capacity preflight.

1. Create or update the most specific detail first.
2. Re-read and validate that detail before modifying its parent.
3. Update the direct module index only as concise summaries and resolving pointers, using `SUBDIRS` or `DETAILS` as applicable.
4. Update the root project map last and only when module structure or its concise resolving pointer changed.

Complete `INTERFACES`, `DATA_FLOW`, `TRAPS`, `DECISIONS`, and full RULES owned by a child must not be copied into the module index or root project map. Parent docs retain the shortest useful summary and pointer. Preserve any root `PROJECT_BRIEF:` line because it is managed separately.

Before each replacement, compare candidate bytes with current bytes. A byte-identical candidate is not written, reordered, or reported as an update.

## 7. Re-read and validate the actual final files

After every write:

1. Re-read the actual bytes from disk and recompute exact raw UTF-8 size.
2. Reapply the 4096B/4096B/5120B hard limit and 80%/90% band formulas.
3. Validate required KEY/value format and memory hygiene.
4. Resolve every affected `MODULE_INDEX`, `MODULE_GROUPS`, `SUBDIRS`, and `DETAILS` pointer; validate both each changed target and its affected direct parent/child.
5. Confirm semantic `MODULE`, `CONCERN`, path, slug, and `FILES` ownership agree and do not collide or overlap.
6. Review only the targeted documentation diff for duplicate meanings, copied child behavior, unstable reorder, and unintended paths.

If any post-write check fails, restore every replaced target from its preserved exact pre-write bytes and remove any invalid newly created target. Re-read the restored affected set and ensure no invalid oversized final document remains. Restoration is a bounded file operation; never use Git reset, checkout, or stash.

## 8. Capacity blocker evidence

When no safe compression or stable split exists, stop with no invalid candidate left in place. The blocked result's `reason` must include:

- exact target path;
- measured current bytes and/or candidate bytes, hard limit, and band;
- protected knowledge that prevented trimming;
- why attempted cleanup, movement, or identity/ownership checks could not establish a safe split;
- a concrete recommended split boundary that a future manual decision can evaluate.

Its `validation` contains only checks actually attempted. Its `documentation_paths` follows the result schema and never invents a change. `RETRO_COMPLETE` is prohibited after any unresolved capacity, pointer, format, or restoration check.

## 9. Bounded TRAPS staleness check

Run only for an affected detail target whose `TRAPS` section has more than 10 entries. Process at most five oldest traps:

1. Delete a trap only when eligible source evidence proves it stale, including a `STALE_IF` path that no longer exists within the exact scope.
2. If a `REF` cannot be validated from eligible evidence, retain the trap or mark it `[REVIEW]`; do not mine repository history or unrelated source to decide.
3. Never remove a still-valid CRITICAL/HIGH trap merely for capacity.
