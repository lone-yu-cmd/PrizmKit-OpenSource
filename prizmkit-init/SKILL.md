---
name: "prizmkit-init"
description: "Recommended one-time project initialization for PrizmKit. Scans greenfield or brownfield projects, generates Prizm docs and a project brief, and prepares optional context for the formal requirement lifecycle. Use for initialize, bootstrap, take over this project, or first-time setup requests. (project)"
---

# PrizmKit Init

Recommended project initialization skill. Scans any brownfield or greenfield project, generates Prizm documentation and a project brief, and adapts to the current AI coding host when platform-specific instruction files are present.

### When to Use
- Taking over a new project (brownfield or greenfield)
- User says "initialize PrizmKit", "set up PrizmKit", "take over this project"
- First time using PrizmKit on a project
- After the PrizmKit skills are installed (for example with `npx skills add`) when the project has no `.prizmkit/prizm-docs/`

### When NOT to Use
- All artifacts exist and are up to date → skip init; use `/prizmkit-prizm-docs` Status/Validate for health checks
- Docs drifted outside the normal development loop (manual edits, merge, branch switch) → use `/prizmkit-prizm-docs` Update/Rebuild for repair
- Normal development just finished and docs need syncing → use `/prizmkit-retrospective`, not init
- User wants to start a feature on an already-initialized project → skip init, go to `/prizmkit-plan`

### Error Handling
- If artifacts already exist: idempotent status check offers regenerate/skip choices (see Phase 3: Idempotent Status Check)
- If no source files found in any directory: fall back to greenfield mode

### Artifact Ownership

`.prizmkit/**` is the PrizmKit framework directory. Initialization may read and write only its declared managed artifacts, but it does not stage, commit, force-add, change or interpret `.gitignore`, require Git history, or decide whether those paths are ignored, untracked, or tracked. The project controls Git visibility; initialization behavior is otherwise identical. Root instruction and platform-support files remain support data rather than initialization-owned commit output.

## Host-Neutral Interaction and Discovery

- Ask required questions through the current Host's available user-interaction capability. If no structured interaction capability exists, ask directly in ordinary conversation and wait for the user's answer.
- Describe required filesystem evidence and bounded discovery results semantically. Do not require a specific tool name, shell, command, or operating system.
- Platform-specific commands may be shown only as non-normative examples after the Host has established that they are available; an unavailable example never blocks an equivalent Host-native operation.

## Execution Steps

**Phase 1: Platform Detection**
1. Detect the current AI coding host through available environment signals. Platform-specific files such as `AGENTS.md`, `CLAUDE.md`, or `CODEBUDDY.md` are non-exhaustive examples, not protocol identifiers.
2. Hold detected platform value in memory — written to disk in Phase 6 along with other config fields.

**Phase 2: Mode Detection**
- If project has source code: brownfield mode
- If project is nearly empty: greenfield mode

**Phase 3: Idempotent Status Check**

Scan all init artifacts and display their status:

| Artifact | Path | Check |
|----------|------|-------|
| Prizm docs | `.prizmkit/prizm-docs/` | Directory exists + `root.prizm` present |
| Runtime config | `.prizmkit/config.json` | File exists |
| Project brief | `.prizmkit/plans/project-brief.md` | File exists |

Display status table to user:
```
Init Status Check:
  [exists]  .prizmkit/prizm-docs/          (N files)
  [exists]  .prizmkit/config.json
  [missing] .prizmkit/plans/project-brief.md
```

- **If all missing**: skip interaction, proceed to generate everything.
- **If some exist**: ask user once:
  - **[A] Regenerate all** — overwrite all existing artifacts (fresh start)
  - **[B] Only generate missing** — skip existing, fill gaps (default)
  - **[C] Pick per item** — ask for each existing artifact: regenerate or skip

Each subsequent phase checks its artifact's action before executing:
- `action == skip` → output "Skipped (exists)" and move on
- `action == generate | regenerate` → run normally
- **Special case for `.prizmkit/prizm-docs/`**:
  - `skip` = **Update** mode: preserve existing L1/L2 docs, re-scan tech stack, merge changes, check for missing docs (see `${SKILL_DIR}/references/update-supplement.md`)
  - `regenerate` = **Reinitialize**: overwrite everything

BROWNFIELD WORKFLOW (existing project):

**Phase 4: Project Scanning**
1. Detect tech stack from build files (`package.json`, `requirements.txt`, `go.mod`, `pom.xml`, `Cargo.toml`, etc.)
2. Map directory structure using a TWO-TIER model — flat structures lose the nesting relationships that AI needs to navigate the codebase:
   - TOP-LEVEL modules: directories directly under project root that contain source files or sub-directories with source files (e.g. `src/`, `internal/`, `lib/`)
   - SUB-MODULES: directories INSIDE a top-level module (e.g. `src/routes/`, `src/models/`)
   - Exact `root.prizm` is L0; top-level module M maps to direct-child `.prizmkit/prizm-docs/<M>.prizm` (L1); sub-module S maps to nested `.prizmkit/prizm-docs/<M>/<S>.prizm` (L2). Deeper source ownership remains L2 and never creates L3.
   - Exclude: `.git/`, `node_modules/`, `vendor/`, `build/`, `dist/`, `__pycache__/`, `target/`, `bin/`, `.agents/`, `.codex/`, `.claude/`, `.codebuddy/`, `.pi/`, and the complete `.prizmkit/` framework directory. This excludes installed `.prizmkit/dev-pipeline/` artifacts but not canonical top-level `dev-pipeline/` source.
   - **Bounded discovery contract** — use the current Host's available directory-listing or file-search capability to enumerate at most two directory levels, apply the exclusions above before analysis, preserve parent/child relationships, and report the resulting project-relative structure. Do not require a POSIX shell pipeline or any other operating-system-specific command.
3. Identify entry points by language convention
4. Catalog dependencies (external packages)
5. Count source files per directory
6. Detect detailed tech stack (adaptive — only include fields that apply):
   → Read `${SKILL_DIR}/references/tech-stack-catalog.md` for the full field catalog.

   **IMPORTANT**: Not all projects have all fields. A pure backend API will have no `frontend_framework` or `frontend_styling`. A library may have no database. Only record what is actually detected — never generate empty or placeholder values.

**Phase 4.5: Layer Detection**

After tech stack detection, determine which development layers exist in the project — these are code domains that may benefit from custom dev rules (frontend, backend, database, mobile). This is a quick detection step, not an interactive Q&A — rules can be configured later based on detected layers.

1. Read `${SKILL_DIR}/references/rules/layer-detection.md` for the detection signal table and AI judgment guidelines.
2. Scan the project against each signal, and supplement with your own judgment — the signal table is a guide, not exhaustive. If you see clear evidence of a layer not covered by the table, include it. If a signal matches but context is misleading, downgrade or ignore it:
   - **frontend**: React/Vue/Angular/etc. in dependencies, or `src/components/` with UI files
   - **backend**: Express/FastAPI/Gin/etc. in dependencies, or `routes/`/`controllers/` with server code
   - **database**: Prisma/TypeORM/SQLAlchemy/etc. in dependencies, or `migrations/`/`prisma/` directory
   - **mobile**: `pubspec.yaml` (Flutter), `react-native` in package.json, or simultaneous `ios/`+`android/` directories
3. For mobile signals — if ambiguous (e.g., monorepo with web + ios/android dirs), ask the user directly: "Mobile platform signals detected. Is this project a mobile app?" Offer "Yes, this is a mobile app" and "No, these are for another purpose" as clear choices, using the Host-neutral interaction contract above.
4. Assemble `detected_layers` array (e.g., `["frontend", "backend", "database"]`). If no layers detected (library/CLI project), array is empty.

**Phase 4.6: Infrastructure Quick Scan**

Detect database and deployment signals, then ask 1-2 brief questions. This phase is **optional** — users can skip and configure later.

- **BROWNFIELD**: Auto-detect infrastructure signals from existing files, then ask 1-2 brief questions (pre-filled with detection results)
- **GREENFIELD**: No auto-detection possible — ask the 2 brief questions directly (database need and deployment target)

1. **Auto-detect infrastructure signals** (no user interaction):
   - **Database signals**: ORM/database client dependencies in `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `pyproject.toml` (look for: prisma, typeorm, sequelize, mongoose, sqlalchemy, django, gorm, diesel, sqlx, pg, mysql2, etc.); directories named `migrations/`, `db/`, `schema/`, `prisma/`; environment variables `DATABASE_URL`, `DB_HOST`, `DB_NAME`, `MONGO_URI` in `.env*` files
   - **Deployment signals**: `Dockerfile`, `docker-compose.yml`, `vercel.json`, `fly.toml`, `railway.json`, `netlify.toml`, `cloudflare.json`, `.github/workflows/`, `Procfile`, `app.yaml`, `serverless.yml`, `terraform/`, `pulumi/`

2. **Brief inquiry** (ask through the Host-neutral interaction contract, max 2 questions):

   **Question 1 — Database**:
   - If database signals detected: pre-fill with detected info
   - Question: "Does your project use a database?"
   - Options:
     - "Yes — {detected ORM/DB}" (if detected, mark as Recommended)
     - "Yes — different database" (let user specify)
     - "No database needed"
     - "Skip — decide later"
   - If "Yes": follow up to confirm database type (MySQL / PostgreSQL / MongoDB / SQLite / Other) — skip this follow-up if already clear from detection

   **Question 2 — Deployment target**:
   - If deployment signals detected: pre-fill with detected info
   - Question: "Where will this project be deployed?"
   - Options:
     - "{Detected platform}" (if detected, e.g., "Vercel" from vercel.json, mark as Recommended)
     - "Own server / VPS"
     - "SaaS platform" (if no specific platform detected)
     - "Container (Docker / K8s)"
     - "Skip — decide later"
   - If "SaaS platform": follow up with platform selection (Vercel / Railway / Fly.io / Cloudflare / AWS / Other)

3. **Write results**:
   - Append `### Infrastructure` to the detected host's main instruction file when that file exists. Use the host's conventional main instruction file; examples include `AGENTS.md`, `CLAUDE.md`, and `CODEBUDDY.md`. Do not write Infrastructure to private instruction files reserved for framework protocol imports. Format:
     ```markdown
     ### Infrastructure

     #### Database
     - **Type**: [PostgreSQL / MySQL / MongoDB / SQLite / none]
     - **ORM**: [detected ORM or "none detected"]

     #### Deployment
     - **Target**: [platform name or "undecided"]
     ```
     → This is intentionally minimal (Quick Scan). Full conventions and deployment details can be added later.
   - If user selects "Skip — decide later" for BOTH topics: write deferred marker instead:
     ```markdown
     ### Infrastructure
     <!-- infrastructure: deferred -->
     ```
   - If user skips only one topic, write the answered one normally and mark the skipped one:
     ```markdown
     #### Database
     <!-- database: deferred -->
     ```

**Phase 4.7: Rules Quick Entry**

After Infrastructure Quick Scan completes, check if `detected_layers` is non-empty (from Phase 4.5). If layers were detected, offer a lightweight entry point for rules configuration.

1. If `detected_layers` is empty (library/CLI project) → skip this phase entirely, proceed to Phase 5.
2. If layers are detected, ask through the Host-neutral interaction contract:

   **Question**: "Detected **{list detected layers}** code. Would you like to set up custom development rules for AI to follow? This helps AI generate code that matches your conventions."
   - **Configure later (Recommended)** — Record layers and configure rules later
   - **Skip entirely** — no custom rules, AI uses general best practices

3. If the user picked "Skip entirely" → preserve `detected_layers` as observed project facts, set `enabled_rule_profiles` to an empty array, and proceed to Phase 5.
4. If the user picked "Configure later" → preserve `detected_layers`, keep `enabled_rule_profiles` unchanged when already configured or initialize it to an empty array, and proceed to Phase 5. Detection never implies rule adoption.

**Phase 5: Prizm Documentation Generation**
Invoke prizmkit-prizm-docs (Init operation), passing the two-tier module structure from Phase 4:
  - Create only documentation directories needed by complete documents; do not create placeholder sub-module files.
  - Generate exact `root.prizm` (L0) with `PRIZM_VERSION: 4`, project meta, and MODULE_INDEX listing only top-level modules. If module count > 15 or measured capacity requires it, use MODULE_GROUPS.
  - For each module entry in MODULE_INDEX/MODULE_GROUPS, include only high-value intent tags and a pointer to one direct-child L1 at `.prizmkit/prizm-docs/<M>.prizm`.
  - Generate one direct-child L1 structural index for each top-level module. Record source submodules structurally, but emit a SUBDIRS pointer only when its complete nested L2 exists.
  - Skip all L2 during Init. Before later source modification, read a complete existing relevant L2 and complete resolving pointer documents; if absent, inspect bounded relevant source as fallback without creating a placeholder. `/prizmkit-retrospective` may later create a complete Value-Gate-qualified L2.
  - Do not create auxiliary `changelog.prizm`, CHANGELOG sections/files, UPDATED/date metadata, feature/bug/refactor/task/session/run/pipeline/workflow IDs, branch names, absolute worktree paths, or `.prizmkit/specs` / `.prizmkit/dev-pipeline` artifact paths; temporal history is outside Prizm memory

**Phase 6: Workspace Initialization**
6a. Create `.prizmkit/` directory structure (if missing):
  - `.prizmkit/config.json` (adoption_mode, platform installation metadata, detected_layers, enabled_rule_profiles)
  - `.prizmkit/specs/` (empty)
  - `.prizmkit/plans/` (empty — needed by Phase 7 and future pipeline tasks)

6b. Write detected tech stack to `.prizmkit/config.json`:
   → Read `${SKILL_DIR}/references/config-schema.md` for merge strategy, field definitions, and examples.

6c. Write observed layers and separate rule adoption to `.prizmkit/config.json` (alongside `tech_stack`):
   - `"detected_layers": ["frontend", "backend"]` records only the observed layers from Phase 4.5 and is never cleared because the user declines rule configuration.
   - `"enabled_rule_profiles": []` records rule adoption separately. Preserve valid existing entries; initialize an empty array when no profiles are enabled.
   - For greenfield projects (Phase 4.5 skipped), write both fields as empty arrays until code exists or the user explicitly enables a rule profile.
   - Future re-detection updates observed layers without silently enabling or disabling rule profiles.

**Phase 7: Project Brief Generation**

If action for project brief == skip, output "Project brief: skipped (exists)" and proceed to Phase 8 (Report).

Otherwise, generate a project brief to capture the user's overall product vision. This file is referenced by `root.prizm` so every new AI session understands the project goals.

→ Read `${SKILL_DIR}/assets/project-brief-template.md` for the brief format rules and checklist template.

**Brownfield** (existing codebase):
1. Infer project goals from:
   - Generated `root.prizm` (tech stack, module structure, module groups)
   - `README.md` (if exists)
   - Package metadata (`package.json` description, `pyproject.toml`, etc.)
   - Quick scan of key entry points identified in L1 docs
2. Generate a draft in the checklist format defined in the template
3. Present the draft to the user and ask:
   - Is this inference correct?
   - Anything to add, remove, or modify?
4. Apply user edits and write to `.prizmkit/plans/project-brief.md`

**Greenfield** (new/empty project):
1. Use **progressive questioning** (defined in template) to fully understand the user's intent:
   - Round 1: Problem & Vision → Round 2: Scope & Features → Round 3: Technical Constraints → Round 4: Clarification (adaptive)
   - Stop when completion criteria are met: problem, users, core features, boundaries, and technical direction are all clear
   - If answers are vague, probe deeper — don't accept shallow responses
2. Generate brief from answers in checklist format
3. Present to user for confirmation/editing
4. Write to `.prizmkit/plans/project-brief.md`

**After writing the brief**:
- Check if `root.prizm` already contains a `PROJECT_BRIEF:` line
- If exact match `PROJECT_BRIEF: .prizmkit/plans/project-brief.md` exists: skip (already correct)
- If `PROJECT_BRIEF:` exists with a different path: warn user and ask to confirm update or keep old path
- If not present: add `PROJECT_BRIEF: .prizmkit/plans/project-brief.md` at the end of `root.prizm`, after all standard sections
- This ensures every AI session that loads L0 knows to read the project brief

**Phase 8: Report**
Output summary: platform detected, tech stack detected (with detail), modules discovered, L1 docs generated, project brief status, next recommended steps.

Tech stack report format (only show detected fields, adapt to project type):
```
Tech stack detected:
  Language:     TypeScript
  Runtime:      Node.js 20
  Frontend:     React + Tailwind CSS
  Backend:      Express.js
  Database:     PostgreSQL (Prisma)
  Testing:      Vitest
  Bundler:      Vite
  Project type: fullstack
```

Adapt fields to match project type — only show detected fields.

Saved to: `.prizmkit/config.json` → `tech_stack` field

Next step: "Use `/prizmkit-plan` to start your first feature"

GREENFIELD WORKFLOW (new project):
- Skip Phase 4 code scanning (no code to scan — Phase 4.5 Layer Detection and Phase 4.7 Rules Quick Entry are skipped; no layers to detect yet):
  - Ask the user about their intended tech stack:
  - "What language/framework will you use?" (e.g. React + Node.js, Python + FastAPI, etc.)
  - Record answers in `config.json` `tech_stack` with `"_auto_detected": false` (user-provided, not auto-detected)
  - If user is unsure, skip tech_stack — it can be populated later on re-init after code exists
- Phase 4.6: Run Infrastructure Quick Scan — in greenfield mode, no auto-detection is possible, so only ask the 2 brief questions (database need and deployment target). If user is unsure, skip — these can be configured later.
- Phase 5: Create minimal `.prizmkit/prizm-docs/` with just `root.prizm` skeleton (populate TECH_STACK from user answers if provided)
- Phase 7: Generate project brief (greenfield flow — ask user about project goals, see Phase 7 above)
- Phases 6, 8: Same as brownfield (Phase 8 Report recommends `/prizmkit-plan` for first feature)

## Example

**Brownfield init on a fullstack Node.js project:**
```
$ /prizmkit-init

Platform detected: Claude Code
Init Status Check:
  [missing] .prizmkit/prizm-docs/
  [missing] .prizmkit/config.json
  [missing] .prizmkit/plans/project-brief.md
→ All missing, generating everything.

Mode: Brownfield (154 source files found)

Tech stack detected:
  Language:     TypeScript
  Runtime:      Node.js 20
  Frontend:     React + Tailwind CSS
  Backend:      Express.js
  Database:     PostgreSQL (Prisma)
  Testing:      Vitest
  Bundler:      Vite
  Project type: fullstack

Layer Detection:
  Detected layers: frontend, backend, database (from dependency + directory signals)
  → Observed layers stored in config.json independently from rule-profile adoption

Infrastructure Quick Scan:
  Database: PostgreSQL (Prisma) — detected from dependencies
  Deployment: Vercel — detected from vercel.json
  → Written to the detected main platform instruction file `### Infrastructure` (not `.private.md`)

Rules Quick Entry:
  Matched layers: frontend (React), backend (Express.js), database (Prisma) → no rule profiles enabled yet

Modules discovered:
  src/            → .prizmkit/prizm-docs/src.prizm (top-level L1)
  src/routes/     → nested source submodule (no placeholder L2 during Init)
  src/models/     → nested source submodule (no placeholder L2 during Init)
  src/services/   → nested source submodule (no placeholder L2 during Init)

Project brief: inferred from codebase → confirmed by user
  → .prizmkit/plans/project-brief.md

Generated: root.prizm + 1 direct-child L1 doc
Saved: .prizmkit/config.json (tech_stack + detected_layers + enabled_rule_profiles recorded)

Next: Use /prizmkit-plan to start your first feature
```

UPDATE SUPPLEMENT (runs after tech stack merge in Update mode):
→ Read `${SKILL_DIR}/references/update-supplement.md` for the 5-step gap-fill procedure.

**Re-init after PrizmKit upgrade (existing config preserved):**
```
$ /prizmkit-init

Init Status Check:
  [exists]  .prizmkit/prizm-docs/          (12 files)
  [exists]  .prizmkit/config.json
  [missing] .prizmkit/plans/project-brief.md

Missing items will be generated.
For existing items: [A] Regenerate all  [B] Only generate missing (default)  [C] Pick per item
> B (Only generate missing)

Tech stack changes detected:
  + bundler: Vite (newly detected)
  ~ testing: Jest → Vitest (updated)
  = language: TypeScript (unchanged)
  = frontend: React (unchanged)

Documentation gap-fill:
  = app.prizm (direct-child L1) — up to date
  source fallback: app/share/[token] (nested L2 absent; no placeholder created)
  ~ app.prizm (L1) — concise source summary updated

Project brief: inferred from codebase → confirmed by user
  → .prizmkit/plans/project-brief.md (generated)

Merged into .prizmkit/config.json (2 fields updated, user overrides preserved)
```
