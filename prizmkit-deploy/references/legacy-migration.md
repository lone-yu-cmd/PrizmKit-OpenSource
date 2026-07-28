# Legacy Deployment State Migration

Apply this procedure on first use whenever `.prizmkit/deploy/` exists, before creating or modifying `.prizmkit/deploy/deploy.json`. Legacy artifacts are evidence, not authorization and not current output formats.

## Safety Invariants

- Inventory and validation are read-only and project-scoped.
- Never print, persist, hash, compare, or copy a Secret value.
- Never delete, rename, truncate, normalize, or overwrite a legacy artifact during automatic migration.
- Never continue a legacy writer after inventory, even when conversion is blocked.
- Migrate only necessary, unambiguous, non-sensitive facts corroborated by current evidence.
- Preserve uncertain, malformed, conflicting, Secret-bearing, or unconverted evidence in place.
- A write to the sole record is an ordinary reversible write included in the complete confirmed plan. A source-artifact deletion or modification would require a separate exact dedicated confirmation and is not part of migration.
- Existing project-native deployment configuration outranks legacy PrizmKit state.

## Known Legacy Inventory

Check only project-local paths that exist; do not create missing paths:

| Legacy class | Known identity | Validation and conversion boundary |
|---|---|---|
| Configuration | `.prizmkit/deploy/deploy.config.json` and other clearly PrizmKit-owned config files in that directory | Parse without interpolation. Convert only target/profile references, environment labels, actual observed ports, native config paths, health definitions, release/rollback references, and Secret *names/source references*. Commands become evidence only and must be rediscovered before execution. |
| Pending input | `.prizmkit/deploy/pending-input.json` | Validate shape and operation identity. Carry forward only a still-relevant non-sensitive pending action after rediscovery; otherwise preserve it and ask a fresh question. Never trust it as confirmation. |
| Generated document | `.prizmkit/deploy/deploy.md` | Treat as human-readable, potentially stale evidence. Convert a fact only when corroborated by project-native or current target evidence. Never generate or update this document. |
| Per-event history | `.prizmkit/deploy/deploy-history/*.json` | Parse each bounded file independently. Convert only concise redacted summaries from valid events, newest first, then retain at most the sole-record history limit. Preserve every source file. Never write another event file. |
| Local Secret material | `.prizmkit/deploy/secrets.local.env`, `.prizmkit/deploy/secrets.local.json`, or another clearly Secret-bearing legacy path | Validate path ownership/ignore/permission metadata without displaying content. Do not import values. When safe key-name parsing is necessary and authorized, retain only names, external source reference, and presence; malformed or unsafe content stays untouched. Never create replacement local Secret storage. |
| Target metadata copy/reference | `deploy-metadata.json` or a recorded target metadata path | Treat as stale until compared with current target-native read-only state. Convert only verified release/health/rollback facts. Do not recreate the fixed metadata format. |
| Event/template/script artifact | Any per-release, per-phase, per-target, generated script, archive recipe, or template under the legacy directory | Preserve as evidence. Do not execute, regenerate, migrate as authority, or continue its naming pattern. |

Do not recursively scan unrelated project content or follow symlinks outside the project. Record a symlink escape or unreadable artifact as a conflict and preserve it untouched.

## Procedure

### 1. Inventory

1. List the existing `.prizmkit/deploy/` entries without following external symlinks.
2. Classify each path by the table above or `unknown legacy evidence`.
3. Record path, class, readability, and validation result without content excerpts that may contain Secrets.
4. If `deploy.json` already exists, validate it first. Legacy evidence discovered later does not merge automatically into an established record.

### 2. Validate Independently

- Parse structured artifacts with strict duplicate-key and type checking where the current environment supports it.
- Reject unknown legacy schema versions as conversion authority; preserve them.
- Treat free-form documents, commands, timestamps, and recorded validation flags as stale claims.
- Check project-native configuration and current read-only target observations before accepting target identity, ports, live release, health, or rollback.
- Detect Secret-like field names and values before any preview. Omit values entirely; do not mask and carry them into the new record.
- Do not resolve a conflict by choosing the newest timestamp alone.

Invalid input does not block read-only discovery, but it blocks conversion of that input and any write that would silently discard its meaning.

### 3. Build a Migration Preview

Present one bounded preview containing:

- source paths and validation statuses;
- exact non-sensitive facts proposed for `project`, `profiles`, `secret_references`, `current`, bounded `history`, or `recovery`;
- every conflict or stale/unverified claim;
- every preserved path;
- facts intentionally omitted and why;
- the exact complete resulting `.prizmkit/deploy/deploy.json`.

The preview must not contain legacy Secret values, full logs, raw command output, or unbounded event content.

### 4. Confirm and Write Once

When the user confirms the complete plan containing the migration:

1. recheck that every inventoried source path and current evidence used by the preview is unchanged;
2. validate the complete candidate against `${SKILL_DIR}/references/deploy-record-schema.json`;
3. create `.prizmkit/deploy/` only if needed and included in the plan;
4. write a temporary file in the same directory, flush/close it, validate it again, and atomically replace `deploy.json` without following a symlink;
5. read back and validate the exact written object;
6. leave every legacy source in place;
7. stop with `FAILED` if record verification fails, preserving both the live state and legacy evidence.

Do not claim that atomic replacement provides concurrent-writer safety. This contract assumes one operator.

## Conflict and Failure Outcomes

- **Unambiguous conversion:** write the fact and mark its source `MIGRATED_NON_SECRET`.
- **Secret-bearing source:** keep values untouched, store at most a reference/presence fact, mark `PRESERVED_SECRET`.
- **Malformed or unknown source:** preserve it, mark `INVALID` or `PRESERVED_UNCERTAIN`, and describe the blocker without sensitive content.
- **Conflicting current facts:** use direct current evidence for execution, preserve the legacy conflict in `legacy_migration.conflicts`, and require confirmation of the resulting plan.
- **Unknown write outcome:** inspect whether `deploy.json` exists and validates before any replay; never overwrite merely because the client timed out.
- **No confirmation:** make no managed write and return `WAITING_USER` when a migration write is necessary for continuation.

## After Migration

Subsequent operations read and update only `deploy.json` for PrizmKit local state. Legacy paths remain read-only evidence until the user separately chooses exact cleanup. Never create or update legacy configuration, pending-input, document, metadata, Secret, template, script, archive, or per-event history artifacts.
