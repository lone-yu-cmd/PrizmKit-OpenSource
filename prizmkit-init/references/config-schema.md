# config.json Schema — Tech Stack Fields

## Merge Strategy

Handles re-init without losing user edits:

- Read existing `config.json` if present
- If `tech_stack` field exists AND `_auto_detected` is `false` or absent:
  → **SKIP** — user has manually configured tech stack, preserve their settings
- Always update `detected_layers` with fresh observed layer-detection results on every init run — detection is based on code that exists, never on whether the user enables custom rules. A rule-configuration choice must not erase detected project facts.
- Preserve valid `enabled_rule_profiles` entries independently from detection. Initialize `[]` only when the field is absent or the user explicitly disables every rule profile.
- If `tech_stack` field exists AND `_auto_detected` is `true`:
  → **MERGE** — overwrite auto-detected values with new detection results, but preserve any keys the user added manually (keys not in the new detection result). Overwrite `detected_layers` with new observed results and preserve `enabled_rule_profiles` independently.
- If `tech_stack` field does NOT exist:
  → **WRITE** full detected tech stack with `"_auto_detected": true`, write `detected_layers` from observed layer detection, and initialize `enabled_rule_profiles` to `[]` unless the user explicitly enabled profiles
- Only include fields that were actually detected (no empty/null values)

## Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `adoption_mode` | string | `"passive"` \| `"advisory"` \| `"active"` |
| `platform` | string | Installed payload metadata: `"codebuddy"` \| `"claude"` \| `"codex"` \| `"pi"` \| `"all"`. It records installation, not a canonical behavior allowlist. |
| `tech_stack` | object | Detected or user-provided tech stack |
| `tech_stack._auto_detected` | boolean | `true` if auto-detected, `false` if user-provided |
| `detected_layers` | string[] | Development layers observed in the project. Written by prizmkit-init Phase 4.5. Values: `frontend` / `backend` / `database` / `mobile`. Empty only when no layers are observed. Always refreshed from code and never cleared by rule-adoption choices. |
| `enabled_rule_profiles` | string[] | Rule profiles the user explicitly enabled. This is independent from `detected_layers`; an empty array means no custom profile is enabled, not that the project has no detected layers. |

Legacy manifests may still contain `both` for read-only migration compatibility. New config writes must use `codebuddy`, `claude`, `codex`, `pi`, or `all`.

## Examples

Fullstack project:
```json
{
  "adoption_mode": "passive",
  "platform": "claude",
  "detected_layers": ["frontend", "backend", "database"],
  "enabled_rule_profiles": [],
  "tech_stack": {
    "language": "TypeScript",
    "runtime": "Node.js 20",
    "frontend_framework": "React",
    "frontend_styling": "Tailwind CSS",
    "backend_framework": "Express.js",
    "database": "PostgreSQL",
    "orm": "Prisma",
    "testing": "Vitest",
    "bundler": "Vite",
    "project_type": "fullstack",
    "_auto_detected": true
  }
}
```

Pure Python backend:
```json
{
  "adoption_mode": "passive",
  "platform": "claude",
  "tech_stack": {
    "language": "Python",
    "runtime": "Python >=3.11",
    "backend_framework": "FastAPI",
    "database": "PostgreSQL",
    "orm": "SQLAlchemy",
    "testing": "pytest",
    "project_type": "backend",
    "_auto_detected": true
  },
  "detected_layers": ["backend", "database"],
  "enabled_rule_profiles": []
}
```
