# Interactive Workflow Artifact Identity

The interactive workflow derives state identity from the exact caller/planning artifact directory; it never generates a second slug.

## Derivation

1. Resolve `artifact_dir` as a project-relative path inside the active checkout.
2. Take its final path component unchanged as `<requirement-identity>`.
3. Require 1-96 Unicode code points and at most 200 UTF-8 bytes, containing only letters, decimal digits, ASCII hyphens, or ASCII underscores, with a letter or digit at both ends. Reject control characters, separators, `.`/`..`, symlink escape, and empty identity. The byte limit leaves portable filename space for the `.json` suffix.
4. Use exactly:

```text
.prizmkit/state/workflows/<requirement-identity>.json
```

Examples:

```text
.prizmkit/specs/070-skill-generated-artifact-contracts/
→ .prizmkit/state/workflows/070-skill-generated-artifact-contracts.json

.prizmkit/bugfix/B-001/
→ .prizmkit/state/workflows/B-001.json
```

## Collision and Resume Safety

- Store the exact normalized project-relative `artifact_dir` in state.
- Before creating state, if the target file already exists, read it and require its `artifact_dir` to equal the active artifact directory exactly.
- A state file naming collision with a different artifact directory is blocking. Do not overwrite, merge, suffix, or silently select a recent state; require the caller to resolve the conflicting record explicitly.
- When `resume` supplies a state path, require it to equal the derived path, remain under `.prizmkit/state/workflows/`, and point to the exact artifact directory recorded inside it.
- Continue using the same state path and artifact directory for every stage and repair round.

External checkpoints use their own identity and are never derived from or merged into this path.
