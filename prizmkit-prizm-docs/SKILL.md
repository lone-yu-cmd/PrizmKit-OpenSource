---
name: "prizmkit-prizm-docs"
description: "Project documentation specification and management for AI-optimized progressive context loading. Defines the .prizmkit/prizm-docs/ L0/L1/L2 hierarchy, format rules, size limits, and loading protocol. Use this skill to bootstrap docs for new projects (init), check freshness (status), rebuild modules, validate format, migrate existing docs, or repair/resync docs after out-of-band drift such as manual edits, merges, or branch switches. For normal development updates after code changes, use /prizmkit-retrospective instead. Trigger on: 'initialize docs', 'check doc status', 'rebuild docs', 'validate docs', 'migrate docs', 'docs drifted', 'repair prizm docs'. (project)"
---

# Prizm Docs - AI Documentation Framework

Full specification: `${SKILL_DIR}/assets/prizm-docs-format.md`

## Intent Routing

This skill handles documentation system operations. Determine the user's intent and execute the matching operation:

| User Intent | Operation | Trigger Phrases |
|---|---|---|
| Bootstrap new project docs | Init | "initialize docs", "set up prizm docs", "bootstrap documentation" |
| Repair docs after out-of-band drift | Update | "docs drifted", "repair prizm docs", "resync after merge", "docs stale after branch switch" |
| Check doc freshness | Status | "check docs", "are docs up to date", "doc status" |
| Regenerate module docs | Rebuild | "rebuild docs for X", "regenerate module docs" |
| Check format compliance | Validate | "validate docs", "check doc format", "docs valid?" |
| Convert existing docs | Migrate | "migrate docs", "convert docs to prizm format" |

Do not route ordinary development-loop "update docs" or "sync docs" here. In normal feature/bugfix/refactor work, use `/prizmkit-retrospective`; it is the development docs writer.

## Role Clarification

| Aspect | `/prizmkit-prizm-docs` | `/prizmkit-retrospective` |
|--------|------------------------|---------------------------|
| Role | Documentation specification, bootstrap, health checks, migration, out-of-band repair | Normal development writer |
| When | Project setup, validation, rebuild, migration, docs drift after merges/manual edits | After implementation/review when code changes affect docs or durable knowledge |
| Writes | Initial structure, rebuilds, migrations, repair/resync operations | Incremental task-scoped updates during development |
| Reads | Source code structure and existing docs | Git diff, task artifacts, review/test results, changed source |
| Knowledge | Defines format rules and loading protocol | Extracts durable TRAPS/RULES/DECISIONS |

Key principle: `/prizmkit-prizm-docs` defines and repairs the documentation system. `/prizmkit-retrospective` keeps docs in sync during ordinary development.

## Governing Content Gates

These gates apply uniformly wherever this Skill generates, migrates, repairs, or rebuilds documentation. Operation references may add sequencing but must not weaken them.

### Value Gate

Before retaining any candidate fact, ask exactly:

> Could a future AI that lacks this fact make an incorrect modification?

Retain the fact only when the answer is yes and the fact is current, durable, non-obvious, and stated at the lowest owning level. High-value knowledge includes:

- non-obvious public interfaces and wire contracts
- cross-module constraints and non-obvious dependencies
- traps and side effects that can cause an incorrect change
- durable decisions with only the rationale necessary to preserve the choice
- rejected alternatives that future sessions are likely to propose again, with the reason for rejection
- security, data-integrity, concurrency, transaction, and compatibility rules

Reject source-derivable structure or signatures, task/change history, test inventories, temporary conclusions, stale statements, duplicate meanings, long procedures, low-value file lists, and facts already owned by a child detail document. File names, counts, and summaries remain only when needed for navigation or ownership.

Critical-knowledge rule: a still-valid public or wire contract, cross-module constraint, non-obvious dependency, critical trap, durable decision, side effect, or safety/integrity rule must survive cleanup and capacity remediation. Never delete it merely to satisfy a byte check.

### Cleanup Gate

Before Update or Rebuild writes an existing target:

1. Read the complete target and complete resolving parent/child pointer documents first.
2. Build a protected set of still-valid critical knowledge under the Value Gate.
3. Match facts by semantic meaning, not wording; update an equivalent entry in place and merge synonymous entries.
4. Remove stale, duplicate, parent-copied, source-derivable, and otherwise low-value material.
5. Add only genuinely new durable knowledge that has no equivalent entry.
6. Keep L0 and L1 as concise structural summaries and pointers; do not copy L2 interfaces, data flow, traps, decisions, or full rules into a parent.

Append-only synchronization is prohibited. If protected knowledge cannot fit after safe cleanup, movement to the owning child, or an unambiguous semantic split, report the blocker instead of deleting knowledge.

### Framework Directory and Git Neutrality

`.prizmkit/**` is the PrizmKit framework directory. This Skill may read and write only its managed documentation and recovery artifacts, but it never owns project Git policy: do not add, remove, force-add, stage, commit, or interpret `.gitignore` entries for `.prizmkit/**`, and do not require Git history or treat ignored, untracked, or tracked state as a documentation error. Generation, reconciliation, validation, capacity behavior, and failure restoration are identical in all three tracking states apart from ordinary Git visibility.

Exact path classification is mandatory: only `.prizmkit/prizm-docs/root.prizm` is L0; a direct `.prizm` child of `.prizmkit/prizm-docs/` other than root is L1; every nested `.prizm` document is L2. Before source modification, read the complete relevant L2 plus complete parent/child documents needed to resolve its pointers. If relevant L2 is absent, inspect bounded relevant source and create no placeholder as part of context loading.

### Capacity and Sharding Invariants

Use the canonical capacity classifier: exact raw UTF-8 bytes; L0 `root.prizm` limit 4096B; direct-child L1 limit 4096B; nested L2 limit 5120B. Bands are normal below 80%, warning from 80% to below 90%, strong warning from 90% through 100%, and error above 100%.

- Natural content below 80% stays unchanged; do not pad it.
- Warning-range content remains valid and is reported without failure.
- A generated or rewritten target at 90% or above requires cleanup, movement, or a safe split. After automatic remediation, measure every affected parent and child: each must be within its hard limit and the operation targets 3277–3686B for L0/L1 or 4096–4607B for L2 (80% to below 90%), not one byte below the hard limit. A naturally concise result below 80% stays unpadded.
- Any target still above its hard limit blocks completion. A warning must never downgrade another format or hard-limit error.
- When L0 navigation cannot fit, use `MODULE_GROUPS`; never raise limits for project size.
- When one L2 cannot safely retain a flat module's multiple stable behavior concerns, use the semantic L2 policy in the format specification. Preserve mirrored L2 paths for real source submodules.
- Do not add a memory state machine, scoring system, project-size override, task-named or numbered shard, or a fourth documentation level.

### When to Use
- First-time project documentation setup
- Checking whether docs are fresh or valid
- Rebuilding stale module docs after major structural changes
- Migrating existing docs to Prizm format
- Repairing docs that drifted because of manual edits, merges, branch switches, or changes made outside the normal dev loop

### When NOT to Use
- Incremental doc updates after normal code changes → use `/prizmkit-retrospective`
- User wants to edit code → use `/prizmkit-plan` and `/prizmkit-implement`
- Project has no `.prizmkit/prizm-docs/` and the user does not want to initialize docs

## Operation: Init

Bootstrap `.prizmkit/prizm-docs/` for the current project.

Precondition: no `.prizmkit/prizm-docs/` directory exists, or user confirms overwrite.

Read `${SKILL_DIR}/references/op-init.md` for detailed steps. Apply the Value Gate before retaining every generated fact.

## Operation: Update

Repair or resync `.prizmkit/prizm-docs/` after out-of-band drift.

Precondition: `.prizmkit/prizm-docs/` exists with `root.prizm`.

Use Update only when docs drifted outside the normal development loop, such as:

- manual code edits without retrospective
- merges or rebases
- branch switches
- generated code movement
- user explicitly asks to repair stale Prizm docs

During normal feature/bugfix/refactor work, do not use Update; use `/prizmkit-retrospective` to avoid duplicate writers and conflicting edits.

Read `${SKILL_DIR}/references/op-update.md` for detailed steps. Apply both the Value Gate and target-first Cleanup Gate to every written target.

## Operation: Status

Check freshness of all `.prizm` docs.

Precondition: `.prizmkit/prizm-docs/` exists with `root.prizm`.

Read `${SKILL_DIR}/references/op-status.md` for detailed steps.

## Operation: Rebuild

Regenerate docs for a specific module from scratch.

Precondition: `.prizmkit/prizm-docs/` exists and module path is valid.

Read `${SKILL_DIR}/references/op-rebuild.md` for detailed steps. Rebuild from current source analysis without delete-first loss: preserve the target-first inventory, then apply both governing gates.

## Operation: Validate

Check format compliance and consistency of all `.prizm` docs.

Precondition: `.prizmkit/prizm-docs/` exists.

Read `${SKILL_DIR}/references/op-validate.md` for detailed steps.

## Operation: Migrate

Convert existing documentation to `.prizmkit/prizm-docs/` format.

Precondition: existing `docs/`, `docs/AI_CONTEXT/`, README, or architecture docs; no `.prizmkit/prizm-docs/` unless user confirms overwrite.

Steps:
1. Discover existing docs: `docs/`, `docs/AI_CONTEXT/`, `README.md`, `ARCHITECTURE.md`, and structured documentation files.
2. Treat every extracted statement as a candidate, verify it against current source, and apply the Value Gate. Do not migrate source-derivable structure, task/history material, test inventories, temporary conclusions, stale statements, duplicate meanings, long procedures, or low-value file lists.
3. Map project-wide summaries and pointers to L0, module structure and pointers to L1, and retained behavioral knowledge to L2. When a child L2 owns complete knowledge, keep only a concise parent summary and resolving pointer.
4. Preserve source-mirrored L2 paths for real submodules. For a flat module that needs multiple stable behavior concerns to retain required knowledge within 5120B, apply the deterministic semantic-detail identity, ownership, `DETAILS` pointer, and ambiguity-blocking contract in the format specification.
5. Convert retained content to KEY: value format and strip markdown tables, diagrams, decorative formatting, and procedural prose. Merge semantically equivalent source statements before writing.
6. Generate `.prizmkit/prizm-docs/` using the Init structure seeded only with retained content; use `MODULE_GROUPS` when the L0 map cannot fit within 4096B.
7. Run the canonical capacity classifier. Warning-only results remain successful; remediate strong-warning/error generated targets toward 3277–3686B for L0/L1 or 4096–4607B for L2 without deleting protected knowledge. An unresolved hard-limit, ambiguous or unstable concern identity, ownership problem, or slug collision is blocking; never resolve it with a task-named or numbered shard.
8. Validate format, required semantic L2 fields, source-file ownership, pointer resolution, hierarchy, capacity, and critical-knowledge preservation.
9. Write complete validated candidates bottom-up, compare candidate/current bytes to avoid byte-identical rewrites, re-read actual bytes, and restore every prior target byte-for-byte or remove an invalid new target if any post-write check fails.
10. Report files processed, generated `.prizm` files, omitted low-value categories, capacity results, and manual decisions required.

## Recovery Backup Contract

Before replacing a corrupted `root.prizm`, copy its exact bytes outside the managed documentation tree:

```text
.prizmkit/backups/prizm-docs/root.prizm.bak
```

If that path exists, use the lowest available suffix `.001`, `.002`, and so on, for example `root.prizm.bak.001`. Never overwrite an earlier backup, never place backup files under `.prizmkit/prizm-docs/`, and never normalize or partially parse the backup content. Report the backup path before rebuilding. Backups are recovery copies, not Prizm documents or sources of durable knowledge.

## Error Handling

- `root.prizm` corrupted or invalid: create the byte-for-byte recovery backup above, then rebuild affected docs from source.
- Broken pointers: inspect the bounded owning source and parent context. Create a complete Value-Gate-qualified detail only through the selected documentation operation; otherwise remove a stale pointer or report the ambiguity. Never emit a placeholder merely to make a pointer resolve.
- Capacity warning or strong warning: report the exact classifier fields and clean/organize only when required by the governing capacity policy; automatic remediation targets 80% to below 90%.
- Size limit exceeded: fail validation until Value/Cleanup filtering, deduplication, movement to the owning child, or an unambiguous semantic split brings the target within its hard limit; never delete protected knowledge or raise the limit.
- Freshness checks use current source/document filesystem evidence and never require Git history or branch/tracking state.

## Key Protocols

For detailed protocol specifications, read `assets/prizm-docs-format.md`:

- Value and Cleanup Gates: Sections 1 and 7
- Semantic L2 identity and ownership: Sections 3.2, 3.3, and 5
- Capacity classification and remediation: Sections 2.1 and 7
- Progressive Loading: Section 6.1
- Update/repair protocol: Section 7
- RULES hierarchy: Section 3.1

## Examples

**Init output:**

```text
Generated .prizmkit/prizm-docs/:
  root.prizm (L0) — top-level module map
  src.prizm (L1) — direct-child source-module structure and dependencies
  (no nested L2 placeholders during Init)
```

L1 docs are structural indexes. Interface signatures, data flow, TRAPS, and DECISIONS belong in L2 docs.

**Out-of-band repair after merge:**

```text
Changed outside normal dev loop: src/routes/avatar.ts (A), src/models/user.ts (M)
Updated: .prizmkit/prizm-docs/src/routes.prizm — complete nested route detail
Updated: .prizmkit/prizm-docs/src/models.prizm — complete nested model detail
Updated: .prizmkit/prizm-docs/src.prizm — concise direct-child summaries and resolving pointers
```
