# Operation: Init — Detailed Steps

Bootstrap .prizmkit/prizm-docs/ for the current project.

PRECONDITION: No .prizmkit/prizm-docs/ directory exists, or user confirms overwrite.

STEPS:
1. Detect project type by scanning for build system files (go.mod, package.json, requirements.txt, Cargo.toml, pom.xml, *.csproj). Identify primary language, framework, build command, test command, and entry points.
2. Discover modules using MODULE_DISCOVERY_CRITERIA:
   - A directory qualifies as a module if it contains source files forming a logical unit, contains entry/config/interface files, contains qualifying sub-modules, or is referenced by multiple modules as a dependency.
   - TOP-LEVEL modules: directories directly under project root (or under src/ for src-based layouts) that qualify.
   - SUB-MODULES: directories INSIDE a top-level module that qualify. Record them as source structure in the direct-child parent L1; if durable L2 is created later, its nested path mirrors the sub-module.
   - HIERARCHY RULE: exact `root.prizm` is L0; top-level module M maps to direct-child `.prizmkit/prizm-docs/<M>.prizm` (L1); directory X inside M maps to nested `.prizmkit/prizm-docs/<M>/<X>.prizm` (L2). Deeper source ownership remains L2 and never creates L3.
   - Exclude .git/, node_modules/, vendor/, build/, dist/, __pycache__/, target/, bin/, .claude/, .codebuddy/, .codex/, .agents/, .pi/, and the complete `.prizmkit/` framework directory. This excludes installed `.prizmkit/dev-pipeline/` artifacts but never excludes a repository's canonical top-level `dev-pipeline/` source module by basename. If total module count > 30, ask user for include/exclude patterns.
3. Apply the Value Gate from SKILL.md and the format specification to every metadata, rule, pattern, dependency, file, and summary candidate. Keep navigational structure only when needed to locate ownership. Reject source-derivable signatures, history, test inventories, temporary conclusions, stale/duplicate meanings, procedures, and low-value file lists.
4. Create `.prizmkit/prizm-docs/` and only the mirrored directories needed by documents that will exist. Do not create placeholder detail files.
5. Generate `root.prizm` (L0) with concise PROJECT, LANG, FRAMEWORK, BUILD, TEST, ENTRY, navigation pointers, and only Value-Gate-qualified global RULES/PATTERNS/CROSS_CUTTING facts. Set `PRIZM_VERSION: 4`. Keep L0 a summary/pointer map; never copy child interfaces, data flow, traps, decisions, or full rules. No CHANGELOG sections/files, UPDATED/date metadata, feature/bug/refactor/task/session/run/pipeline/workflow IDs, branch names, absolute worktree paths, or `.prizmkit/specs` / `.prizmkit/dev-pipeline` artifact paths.
   - If `.prizmkit/plans/project-brief.md` exists, add `PROJECT_BRIEF: .prizmkit/plans/project-brief.md`; otherwise skip it.
   - Use MODULE_GROUPS whenever MODULE_INDEX cannot fit the required map within 4096B. More than 15 modules is a mandatory grouping trigger. Use 3-8 stable functional domains; never raise the L0 limit for project size.
   - Generate only high-value intent-matching keyword tags; do not copy exported names or imports mechanically when they add no navigation value.
6. Generate one direct-child L1 structural index for each discovered top-level source module at `.prizmkit/prizm-docs/<module>.prizm`. Include concise MODULE, FILES navigation summary, RESPONSIBILITY, SUBDIRS, KEY_FILES, DEPENDENCIES, and at most three critical RULES. A SUBDIRS arrow is emitted only when its mirrored L2 exists, so every arrow resolves. Do not include INTERFACES, DATA_FLOW, TRAPS, DECISIONS, full rules, or a low-value file inventory.
7. Skip all L2 creation during Init. Init has no behavioral context requiring placeholder mirrored or semantic details. Later `/prizmkit-retrospective`, Update, Rebuild, or Migrate may create a complete L2 only when facts pass the Value Gate. Real source submodules use mirrored identity. Flat-module semantic details use the deterministic CONCERN/FILES/DETAILS contract and block on unstable boundaries, overlapping ownership, empty slugs, or collisions; task-named and numbered shards are prohibited.
8. Measure every generated file with the canonical raw UTF-8 capacity classifier: L0/L1 4096B, L2 5120B. Report warning-range files without failing. If a generated L0/L1 reaches 90% or above, clean or reorganize it toward 3277-3686B without deleting protected knowledge. Any unresolved hard-limit error blocks Init.
9. Configure UserPromptSubmit hook in platform settings per `${SKILL_DIR}/assets/prizm-docs-format.md` Section 11.
10. Validate all generated docs: Value Gate, size/band reporting, pointer resolution, no circular dependencies, KEY: value format, parent-summary boundary, no anti-patterns, and no prohibited metadata. Warning-only capacity results pass; hard-limit or format errors fail.
11. Write only complete validated candidates bottom-up, compare bytes before replacement, re-read actual bytes, and restore exact pre-write bytes or remove invalid new targets if a post-write check fails.
12. Report modules discovered, L1 docs generated, files/categories omitted by the Value Gate, files excluded, capacity diagnostics in descending utilization, and any required manual decisions. Do not stage, commit, force-add, change ignore policy, require history, or report tracking state as documentation health.

OUTPUT: List of generated files, module count, Value-Gate omissions by category, capacity results, and validation results.

## Post-Init Behavior

After initialization, L2 docs are created only when durable context exists:

ON_MODIFY behavior:
- Before modification, read the complete relevant L2 plus complete resolving parent/child pointer documents. When `.prizmkit/prizm-docs/<M>/<S>.prizm` does not exist, inspect only the bounded relevant source files in S and narrowly implicated contracts as fallback context, create no placeholder, and proceed.
- Do not block implementation only to create a placeholder L2 doc.
- After the change, run `/prizmkit-retrospective` when structure, interfaces, dependencies, behavior, or durable TRAPS changed; retrospective creates or updates L2 then only for facts that pass the future-incorrect-modification Value Gate.
- Preserve the mirrored source-submodule path. For a flat module with multiple stable concerns under repeated L2 capacity pressure, use deterministic semantic L2 identity and explicit non-overlapping FILES ownership; block ambiguous creation.

ON_DEEP_READ behavior:
- When an AI needs deep understanding but L2 is absent, read the relevant source files directly as fallback context.
- Create L2 through `/prizmkit-retrospective` after normal development work, or through explicit `/prizmkit-prizm-docs` repair/rebuild when fixing out-of-band doc drift.
- Do not create L2 merely because a module was read; L2 should capture durable knowledge, not transient investigation notes.
