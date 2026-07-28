# Planning Artifact Identity

Use one stable, project-relative artifact directory for the entire planning invocation.

## Generated Directory

When the caller does not provide `artifact_dir`:

1. Inspect only direct child directories of `.prizmkit/specs/` whose basenames match `<number>-<slug>`, where `<number>` is at least three decimal digits.
2. Choose one greater than the highest valid number, starting at `001`, and zero-pad to at least three digits. Numbers above `999` retain all digits.
3. Derive `<slug>` from the concise requirement title:
   - normalize text with Unicode NFKC and lowercase where the script has a lowercase form;
   - retain Unicode letters and decimal digits;
   - replace every run of other characters with one ASCII hyphen;
   - trim leading/trailing hyphens;
   - truncate without splitting a Unicode code point until the slug is at most 64 code points and the complete `<number>-<slug>` basename is at most 200 UTF-8 bytes, then trim a trailing hyphen;
   - use `requirement` if no letter or digit remains.
4. Create `.prizmkit/specs/<number>-<slug>/` without overwriting an existing path. If it appeared concurrently, rescan and retry with the next number; after three collisions, return `PLAN_BLOCKED`.

Examples:

```text
.prizmkit/specs/001-user-login/
.prizmkit/specs/070-skill-generated-artifact-contracts/
.prizmkit/specs/1000-支付回调/
```

## Caller-Supplied Directory

An explicit `artifact_dir` is preserved exactly; never slugify or relocate it. Before writing:

- require a project-relative path that resolves inside the active checkout;
- reject `.`/`..` components, control characters, symlink escape, and an empty basename;
- require a basename of 1-96 Unicode code points and at most 200 UTF-8 bytes, containing only letters, decimal digits, ASCII hyphens, or ASCII underscores, with a letter or digit at both ends;
- if existing `spec.md` or `plan.md` belongs to a different requirement, return `PLAN_BLOCKED` rather than overwrite it;
- if the directory already contains the same requirement, reuse it and preserve its identity.

The directory basename is the requirement identity exposed to callers. `spec.md` and `plan.md` are the only planning filenames in that directory.
