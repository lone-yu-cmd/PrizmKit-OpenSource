PRIZM_SPEC_VERSION: 4
PURPOSE: AI-only documentation framework for vibe coding projects
AUDIENCE: AI agents (not humans)
FORMAT: KEY: value pairs, ALL CAPS section headers, arrow pointers
FILE_EXT: .prizm
DOC_ROOT: .prizmkit/prizm-docs/
LICENSE: MIT

---

## Table of Contents

1. Overview
2. Architecture
3. Document Format Specification
4. Format Conventions
5. Path Mapping Rules
6. Progressive Loading Protocol
7. Auto-Update Protocol
8. Anti-Patterns
9. Initialization Procedure
10. Skill Definition
11. Hook Configuration
12. Language-Specific Initialization Hints

---

# SECTION 1: OVERVIEW

WHAT: Prizm is a self-maintaining documentation system where AI reads, generates, updates, and loads project context progressively.
WHY: Reduce AI hallucinations, minimize token waste, ensure AI has accurate project knowledge at all times.
HOW: Three-level progressive loading (L0 -> L1 -> L2) with task-scoped retrospective when code changes affect structure, interfaces, dependencies, behavior, or durable project knowledge.

CORE_PRINCIPLES:
- Token efficiency over human readability
- Progressive disclosure (load only what is needed)
- Self-maintaining (framework owners reconcile managed docs without owning project Git policy)
- Universal (language and framework agnostic)
- Durable project knowledge over auxiliary history (decisions, traps, interfaces, dependencies)
- Value-gated retention: before keeping a candidate fact, ask `Could a future AI that lacks this fact make an incorrect modification?`; retain it only when yes, current, durable, non-obvious, and owned at this level
- Protected critical knowledge: preserve still-valid public/wire contracts, cross-module constraints, non-obvious dependencies, traps, decisions with necessary rationale, likely-to-recur rejected alternatives and reasons, side effects, and security/data-integrity/concurrency/transaction/compatibility rules
- Rejected low-value material: omit source-derivable structure, task/change history, test inventories, temporary conclusions, stale statements, duplicate meanings, long procedures, low-value file lists, and child-owned behavioral detail copied into parents
- Cleanup in place: Update and Rebuild read existing targets, update equivalent meanings in place, merge synonyms, remove stale/duplicate/derivable/parent-copied content, and add only genuinely new durable knowledge
- Memory hygiene over traceability noise (no CHANGELOG sections/files, UPDATED/date metadata, feature/bug/refactor/task/session/run/pipeline/workflow IDs, branch names, absolute worktree paths, or `.prizmkit/specs` / `.prizmkit/dev-pipeline` artifact paths)
- Size-enforced (hard limits per level prevent bloat; no project-size override)
- Capacity-aware (raw UTF-8 byte bands drive warnings and safe remediation; critical knowledge is never deleted merely to meet a check)
- Lazy L2 generation (detail docs created when durable knowledge exists, not as placeholders during init)
- Rules hierarchy (root.prizm RULES are authoritative, module RULES supplement only)
- Three levels only (semantic concern documents are L2, never a fourth level or memory state machine)

---

# SECTION 2: ARCHITECTURE

## 2.1 Progressive Loading Levels

LEVELS:
- L0: Root index. ALWAYS loaded at session start. Hard limit 4096 raw UTF-8 bytes.
  FILE: exact .prizmkit/prizm-docs/root.prizm only
  CONTAINS: concise project meta, module summaries with pointers, build commands, tech stack, top rules
  DOES NOT CONTAIN: child-owned interfaces, data flow, TRAPS, DECISIONS, full rules, or copied behavioral detail

- L1: Structural index. Loaded ON DEMAND when AI works in a module area. Hard limit 4096 raw UTF-8 bytes each.
  FILE: direct .prizm child of .prizmkit/prizm-docs/, excluding exact root.prizm
  CONTAINS: concise module responsibility, source submodule pointers, semantic detail pointers, key navigation files, dependency summary, critical rules summary (1-3 only)
  DOES NOT CONTAIN: interface signatures, data flow, TRAPS, DECISIONS, full rules, or content already complete in L2

- L2: Behavioral detail. Loaded completely before modifying its owned source or when deep understanding is required. Hard limit 5120 raw UTF-8 bytes each.
  FILE: every nested .prizm document below .prizmkit/prizm-docs/, whether mirrored source detail or semantic concern
  CONTAINS: Value-Gate-qualified public interfaces, data flow, rules, TRAPS, DECISIONS, domain-specific sections, and rejected approaches
  IDENTITY: a real source submodule path takes precedence; a semantic concern remains an L2 document and never adds a level

PATH_CLASSIFICATION: Classification depends only on the repository-relative document path: exact root is L0, direct document children are L1, and nested documents are L2. Source depth, filename, module size, and Git state never change the level.

## 2.2 Directory Layout

STRUCTURE: Direct L1 documents index top-level source modules; nested L2 documents mirror owned source submodules or stable semantic concerns.

EXAMPLE (Go project):
  .prizmkit/prizm-docs/
    root.prizm                            # L0
    internal.prizm                        # L1 for internal/
    internal/
      logic.prizm                         # L2 for internal/logic/
      model.prizm                         # L2 for internal/model/
      repo.prizm                          # L2 for internal/repo/
      service.prizm                       # L2 for internal/service/

EXAMPLE (JS/TS project):
  .prizmkit/prizm-docs/
    root.prizm                            # L0
    src.prizm                             # L1 for src/
    src/
      components.prizm                    # L2 for src/components/
      hooks.prizm                         # L2 for src/hooks/
      services.prizm                      # L2 for src/services/

EXAMPLE (Python project):
  .prizmkit/prizm-docs/
    root.prizm                            # L0
    app.prizm                             # L1 for app/
    app/
      models.prizm                        # L2 for app/models/
      views.prizm                         # L2 for app/views/
      services.prizm                      # L2 for app/services/

## 2.3 Framework Directory and Git Neutrality

FRAMEWORK_DIRECTORY: `.prizmkit/**` contains PrizmKit-managed capabilities and artifacts; an owning framework capability may read or write its exact managed paths.
GIT_POLICY: The project alone decides whether `.prizmkit/**` paths are ignored, untracked, or tracked. Documentation generation, reconciliation, and validation do not add, remove, force-add, stage, commit, or interpret `.gitignore` entries and do not treat tracking state as a documentation error.
CONSISTENCY: Managed documentation behavior is identical across ignored, untracked, and tracked states apart from ordinary Git visibility.

## 2.4 Capacity Classification and Remediation

MEASUREMENT: exact raw UTF-8 bytes; never characters, lines, rounded kilobytes, or locale-dependent encoding
LEVEL_LIMITS:
- L0: exact `.prizmkit/prizm-docs/root.prizm` -> 4096B
- L1: direct `.prizm` child of `.prizmkit/prizm-docs/` -> 4096B
- L2: nested `.prizm` document -> 5120B, including mirrored and semantic concern details
BANDS:
- normal: size * 100 < limit * 80
- warning: size * 100 >= limit * 80 and size * 100 < limit * 90
- strong-warning: size * 100 >= limit * 90 and size <= limit
- error: size > limit
TARGET_RANGE:
- L0/L1 automatic remediation: 3277–3686B (80% to below 90%)
- L2 automatic remediation: 4096–4607B (80% to below 90%)
- Content naturally below 80% remains normal and is never padded to the target
ACTION_ORDER:
1. trim stale, derivable, procedural, historical, and low-value wording
2. deduplicate repeated meanings and merge synonyms
3. move child-owned behavior out of L0/L1 to a resolving child pointer
4. semantic-split an eligible flat module's unrelated stable concerns into deterministic L2 documents
PRESERVATION: establish protected critical knowledge before remediation; never remove still-valid contracts, constraints, dependencies, traps, decisions, side effects, or safety/integrity rules merely to reduce bytes
COMPLETION: after automatic cleanup or split, measure every affected parent and child; each stays within its hard limit and remediation aims for the target range without padding naturally concise output; warning-range targets remain valid and visible; unresolved hard-limit errors fail validation
REPORT_ORDER: non-normal entries sort by exact descending utilization using integer ratio comparison, then repository-relative path ascending for ties
REPORT_FIELDS: path, level, current raw bytes, hard limit, utilization band, target range, and actionable trim, deduplicate, move-to-child, or semantic-split guidance
EXIT: warning and strong-warning diagnostics alone do not fail Validate; hard-limit or format errors fail and cannot be downgraded

---

# SECTION 3: DOCUMENT FORMAT SPECIFICATION

## 3.1 L0: root.prizm

TEMPLATE:

  PRIZM_VERSION: 4
  PROJECT: <name>
  LANG: <primary language>
  FRAMEWORK: <primary framework or "none">
  BUILD: <build command>
  TEST: <test command>
  ENTRY: <entry point file(s)>

  ARCHITECTURE: <layer1> -> <layer2> -> <layer3> -> ...
  LAYERS:
  - <layer-name>: <one-line description>

  TECH_STACK:
  - runtime: <list>
  - deps: <key external dependencies>
  - infra: <infrastructure: databases, queues, caches, etc.>

  MODULE_INDEX:
  - <top-level-source-module>: <file-count> files. <one-line description>. -> .prizmkit/prizm-docs/<module>.prizm
  (Every root pointer resolves to one direct-child L1. L1 then resolves only the relevant nested L2 pointers.)

  ENTRY_POINTS:
  - <name>: <file-path> (<protocol/port if applicable>)

  RULES:
  - MUST: <project-wide mandatory rule>
  - NEVER: <project-wide prohibition>
  - PREFER: <project-wide preference>

  PATTERNS:
  - <pattern-name>: <one-line description of code pattern used across project>

  CROSS_CUTTING:
  - <concern-name>: <one-line description>. Modules: <affected-module-list>.
  (Optional: -> .prizmkit/prizm-docs/cross-cutting/<name>.prizm for detailed cross-cutting doc.
   Only record concerns spanning 2+ modules. Single-module patterns go in that module's RULES.)

  DECISIONS:
  - <project-level architectural decision and rationale>
  - REJECTED: <rejected approach + why>

CONSTRAINTS:
- Hard limit 4096 raw UTF-8 bytes; project size never raises it
- Every line must be a KEY: value pair or a list item
- MODULE_INDEX must have arrow pointer (->) for every entry
- MODULE_INDEX and MODULE_GROUPS entries point to direct-child L1 documents only
- RULES limited to 5-10 most critical conventions
- No prose paragraphs
- root.prizm RULES are AUTHORITATIVE: they override any conflicting L1/L2 RULES

### MODULE_GROUPS (capacity-safe alternative to MODULE_INDEX)

When MODULE_INDEX cannot retain the required concise module map within the L0 4096B hard limit, replace it with MODULE_GROUPS. More than 15 modules is a mandatory grouping trigger, but measured L0 capacity may require grouping earlier. Group modules by stable functional domain; never raise the L0 limit or add a project-size override:

  MODULE_GROUPS:
    <domain-name>:
      - <module>: <file-count> files. <one-line description>. -> .prizmkit/prizm-docs/<module>.prizm
      - <module>: <file-count> files. <one-line description>. -> .prizmkit/prizm-docs/<module>.prizm
    <domain-name>:
      - <module>: <file-count> files. <one-line description>. -> .prizmkit/prizm-docs/<module>.prizm

CONSTRAINTS for MODULE_GROUPS:
- Exactly ONE of MODULE_INDEX or MODULE_GROUPS must be present in root.prizm (not both)
- Grouping changes navigation shape only; L0 remains a concise summary/pointer map and the 4096B hard limit is unchanged
- Domain names: lowercase, descriptive (e.g., api, frontend, infrastructure, shared, data)
- 3-8 domains is the ideal range
- Each module appears in exactly one domain
- Every entry must have an arrow pointer (->), same as MODULE_INDEX
- AI should load the relevant domain's modules when working on a task, not all domains

### Optional Keyword Tags (applies to both MODULE_INDEX and MODULE_GROUPS)

Entries may include keyword tags for AI intent matching:

  MODULE_INDEX:
    - auth [login, session, jwt, oauth]: 12 files. Authentication and authorization. -> .prizmkit/prizm-docs/auth.prizm
    - payments [stripe, billing, subscription]: 8 files. Payment processing. -> .prizmkit/prizm-docs/payments.prizm
    - users: 6 files. User management. -> .prizmkit/prizm-docs/users.prizm

Tags are optional, enclosed in square brackets after the module name. They contain lowercase keywords that describe the module's domain concepts. AI matches user requirement descriptions against tags to identify relevant modules before loading L1. Tags are auto-generated during Init from module source content (function names, imports, domain terms) and refined during Rebuild.

## 3.2 L1: module.prizm (Structural Index)

TEMPLATE:

  MODULE: <source-path>
  FILES: <count>
  RESPONSIBILITY: <one-line>

  SUBDIRS:
  - <name>/: <one-line source-submodule summary>. -> .prizmkit/prizm-docs/<child-path>.prizm

  DETAILS:
  - <concern-slug>: <one-line stable behavior summary> -> .prizmkit/prizm-docs/<module>/<concern-slug>.prizm
  (DETAILS is present only for semantic concern L2 documents in a flat module. SUBDIRS owns real source-submodule pointers.)

  KEY_FILES:
  - <filename>: <role/purpose>

  DEPENDENCIES:
  - imports: <internal modules this module uses>
  - imported-by: <internal modules that depend on this>
  - external: <third-party packages used>

  RULES:
  - MUST: <1-3 most critical module-specific rules only — full list in L2>

CONSTRAINTS:
- Hard limit 4096 raw UTF-8 bytes; project size never raises it
- L1 is a STRUCTURAL INDEX — it answers "what exists here" not "how it works"
- DOES NOT CONTAIN: INTERFACES, DATA_FLOW, TRAPS, DECISIONS, full RULES, or copied L2 behavioral content
- RULES: summary only, max 3 entries of the most critical constraints. Full rules in L2.
- DEPENDENCIES has 3 sub-categories (imports, imported-by, external)
- SUBDIRS entries point only to mirrored real source-submodule details; each pointer must resolve
- DETAILS entries use exactly `- <concern-slug>: <one-line stable behavior summary> -> .prizmkit/prizm-docs/<module>/<concern-slug>.prizm`; each pointer must resolve to one semantic L2 whose MODULE and CONCERN match
- A real source-submodule path takes precedence over the same semantic slug; ambiguity or collision blocks semantic detail creation
- KEY_FILES lists only navigation-critical files that pass the Value Gate (max 10-15, often fewer); never use it as a file inventory
- If a child L2 contains the complete rule, interface, trap, decision, or data flow, L1 keeps only the shortest useful summary and pointer
- RULES may only SUPPLEMENT root.prizm RULES with module-specific exceptions, never contradict them

TRAPS_FORMAT_REFERENCE (spec-only — do NOT include this block in generated .prizm files):
- Severity levels: CRITICAL = data loss/security/financial/crash, HIGH = functional failure/silent error, LOW = naming/minor quality
- Temporary prefix: [REVIEW] may precede severity (e.g., `[REVIEW][HIGH]`) — signals the TRAP needs re-validation. Consumed by the next retrospective: verify and either remove [REVIEW] or delete the TRAP.
- REF: first 7 chars of the commit where the trap was discovered (optional, for traceability)
- STALE_IF: glob pattern — when matched files are deleted or heavily rewritten, this trap needs re-validation (optional)
- Minimal valid format: `- [SEVERITY] <description> | FIX: <approach>`
- Full format: `- [SEVERITY] <description> | FIX: <approach> | REF: <hash> | STALE_IF: <glob>`

## 3.3 L2: detail.prizm (Behavioral Detail)

COMMON_TEMPLATE:

  MODULE: <source-submodule path for mirrored detail, or flat parent module path for semantic detail>
  CONCERN: <stable concern identity> | SLUG: <concern-slug>
  (CONCERN is required only for semantic concern details and prohibited on mirrored source-submodule details.)
  FILES: <comma-separated repository-relative source files owned by this detail>
  RESPONSIBILITY: <one-line durable behavior boundary>

  INTERFACES:
  - <non-obvious public/exported signature or wire contract>: <modification consequence>

  DATA_FLOW:
  - <numbered non-obvious step, side effect, transaction, or cross-boundary flow>

  <DOMAIN-SPECIFIC SECTIONS>
  (AI generates these only when entries pass the Value Gate.)

  KEY_FILES:
  - <repository-relative source file>: <why a future modification needs this navigation pointer>

  DEPENDENCIES:
  - uses: <external dependency>: <non-obvious contract or constraint>
  - imports: <internal module>: <consumed public contract or coupling>

  RULES:
  - MUST: <module-specific mandatory rule>
  - NEVER: <module-specific prohibition>
  - PREFER: <module-specific preference>

  TRAPS:
  - [CRITICAL|HIGH|LOW] <incorrect-looking-safe change or non-obvious side effect> | FIX: <correct approach>

  DECISIONS:
  - <durable decision> — <only the rationale needed to preserve it>
  - REJECTED: <alternative future sessions are likely to propose again> — <why it remains rejected>

REQUIRED_FIELDS:
- Mirrored source-submodule L2: MODULE, FILES, RESPONSIBILITY, INTERFACES, KEY_FILES, DEPENDENCIES, TRAPS. DATA_FLOW, RULES, DECISIONS, and domain-specific sections are present only when facts pass the Value Gate, preserving existing mirrored-document compatibility.
- Semantic concern L2 complete terminal shape: MODULE, CONCERN, FILES, RESPONSIBILITY, INTERFACES, DATA_FLOW, KEY_FILES, DEPENDENCIES, RULES, TRAPS, DECISIONS
- In a semantic concern L2, if a required behavioral section has no fact that passes the Value Gate, render the section as `<SECTION>: none`; never invent filler to populate it
- DOMAIN-SPECIFIC sections are optional and contain only Value-Gate-qualified facts

SEMANTIC_CONCERN_TERMINAL_SHAPE:
- Eligibility: a flat source module has multiple stable behavior concerns and required protected knowledge cannot fit one L2 within 5120B after Value/Cleanup filtering
- Path: `.prizmkit/prizm-docs/<module>/<concern-slug>.prizm`; it is L2, not a new documentation level
- MODULE: exact flat source module path
- CONCERN: stable source-evidenced product/domain behavior name plus its deterministic slug
- FILES: non-empty exhaustive list of repository-relative source files owned by this concern
- Ownership: sibling semantic concerns have explicit non-overlapping FILES; unclear or overlapping ownership blocks automatic creation
- Parent: exactly one L1 DETAILS entry using the Section 3.2 grammar resolves to the semantic file; the slug, path, MODULE, and CONCERN must agree
- Mirrored precedence: if a real source submodule maps to the same path, the mirrored submodule owns it and semantic creation is blocked pending a different unambiguous concern identity
- Terminal outcomes: write the complete required shape, or report the ambiguity/collision/ownership blocker and required manual decision; never emit a partial semantic file

DOMAIN_SPECIFIC_SECTION_EXAMPLES:
- For state transition logic: STATES, TRIGGERS, TRANSITIONS
- For API handlers: ENDPOINTS, REQUEST_FORMAT, RESPONSE_FORMAT, ERROR_CODES
- For data stores: TABLES, QUERIES, INDEXES, CACHE_KEYS
- For config modules: CONFIG_KEYS, ENV_VARS, DEFAULTS
- For UI components: PROPS, EVENTS, SLOTS, STYLES

CONSTRAINTS:
- Hard limit 5120 raw UTF-8 bytes; project size never raises it
- L2 is the BEHAVIORAL DETAIL — it answers only non-obvious "how it works, what can go wrong, what was decided" questions that pass the Value Gate
- INTERFACES lists only non-obvious PUBLIC/EXPORTED or wire contracts; omit source-derivable signatures as `INTERFACES: none`
- DATA_FLOW records only flows or side effects whose absence could cause an incorrect modification
- RULES contains the full retained module-specific rules list; L1 has at most a short summary
- DECISIONS records durable rationale only; keep it current by updating equivalent decisions in place and removing stale ones
- TRAPS entries MUST have severity prefix ([CRITICAL], [HIGH], or [LOW]); [REVIEW] may precede severity as a temporary staleness marker
- TRAPS optional fields: append `| REF: <7-char-hash>` for traceability, `| STALE_IF: <glob>` for auto-expiry detection
- TRAPS severity: CRITICAL = data loss/security/financial/crash, HIGH = functional failure/silent error, LOW = naming/minor quality (see TRAPS_FORMAT_REFERENCE in Section 3.2)
- REJECTED entries exist only for alternatives likely to recur and include the durable reason
- FILES is an ownership list, not a low-value repository inventory; mirrored details list files in their source boundary and semantic details list their explicitly owned files
- KEY_FILES contains only navigation-critical files and never line counts, complexity inventories, or derivable descriptions
- RULES may only SUPPLEMENT root.prizm RULES with module-specific exceptions, never contradict them

## 3.4 Metadata Policy

TEMPORAL_INFO: Change timing and edit history are outside Prizm memory; use project history when the project provides it.
AUXILIARY_FIELDS: Do not generate CHANGELOG or UPDATED fields in .prizm files.
WORKFLOW_METADATA: Do not write feature/bug/refactor/task/session/run/pipeline/workflow IDs, branch names, absolute worktree paths, or `.prizmkit/specs` / `.prizmkit/dev-pipeline` artifact paths into .prizm files.
RATIONALE: Keep project memory focused on durable architecture, interfaces, dependencies, traps, rules, and decisions.

---

# SECTION 4: FORMAT CONVENTIONS

HEADERS: ALL CAPS followed by colon (MODULE:, FILES:, RESPONSIBILITY:, etc.)
VALUES: Single space after colon, value on same line (KEY: value)
LISTS: Dash-space prefix for items within a section (- item)
POINTERS: Arrow notation (->) to reference other .prizm files
NESTING: Indent 2 spaces for sub-keys within a section
COMMENTS: None. Every line carries information. No comments in .prizm files.
TIMESTAMPS: No date/time fields in .prizm files. Temporal history is outside Prizm memory and is never required for documentation operation.

---

# SECTION 5: PATH MAPPING RULES

## 5.1 Mapping Algorithm

RULE: Root index = exact .prizmkit/prizm-docs/root.prizm (L0)
RULE: L1 for top-level source module M = direct child .prizmkit/prizm-docs/<M>.prizm
RULE: Mirrored L2 for source submodule M/S = nested .prizmkit/prizm-docs/<M>/<S>.prizm
RULE: Semantic L2 for a stable flat-module concern = nested .prizmkit/prizm-docs/<M>/<concern-slug>.prizm
RULE: Nested source depth never creates L3; the owning nested document remains L2 and uses explicit MODULE/FILES identity

## 5.2 Examples

SOURCE_PATH                   L1_PRIZM_FILE                         L2_PRIZM_FILE
internal/                     .prizmkit/prizm-docs/internal.prizm   none until durable detail exists
internal/logic/               (parent L1 SUBDIRS pointer)           .prizmkit/prizm-docs/internal/logic.prizm
src/                          .prizmkit/prizm-docs/src.prizm        none until durable detail exists
src/components/               (parent L1 SUBDIRS pointer)           .prizmkit/prizm-docs/src/components.prizm
app/                          .prizmkit/prizm-docs/app.prizm        none until durable detail exists
app/services/                 (parent L1 SUBDIRS pointer)           .prizmkit/prizm-docs/app/services.prizm

## 5.3 Discovery Rule

FOR any source file at path P:
  1. Resolve its top-level source module M through the root MODULE_INDEX or MODULE_GROUPS pointer to direct-child L1 `.prizmkit/prizm-docs/<M>.prizm`
  2. Read that complete L1 and resolve the one mirrored SUBDIRS or semantic DETAILS pointer that owns P
  3. Mirrored source-submodule identity has precedence; for a flat module, semantic FILES ownership selects the detail
  4. Before modifying P, read the complete selected L2 and complete resolving parent/child pointer documents
  5. If ownership is absent, overlaps, or disagrees with its pointer, report ambiguity instead of guessing
  6. If no relevant L2 exists, inspect only the bounded source files needed for P and proceed without creating a placeholder; documentation creation remains an owning retrospective/repair operation

## 5.4 Deterministic Semantic Concern Identity

ELIGIBILITY:
- The source module is flat: the concern is not already a real source submodule that can use mirrored identity
- Current source proves multiple stable product/domain behavior boundaries
- Required protected knowledge cannot fit one 5120B L2 after the Value Gate, Cleanup Gate, deduplication, and concise wording

SLUG_ALGORITHM:
1. Choose one concise stable product/domain behavior concern name evidenced by current source responsibility; task, feature, bug, session, workflow, branch, temporary initiative, and file-count labels are invalid identities.
2. Normalize the identity with Unicode NFKC.
3. Apply Unicode lowercase.
4. Replace each maximal run of characters that is neither a Unicode letter nor a Unicode decimal digit with one ASCII hyphen.
5. Trim leading and trailing hyphens. The result must be non-empty, lowercase kebab-case and map unambiguously to exactly one stable concern.
6. Compare the result with every sibling semantic CONCERN slug, sibling DETAILS entry, and mirrored source-submodule path before creating a file.

OWNERSHIP_RULES:
- FILES uses normalized repository-relative source paths and is non-empty.
- Each owned file belongs to exactly one sibling semantic concern. Do not silently duplicate or overlap ownership.
- Source files outside the flat module, unclear multi-concern files, unstable behavior boundaries, empty slugs, and one slug mapping to multiple concern meanings require a manual ownership/identity decision.

COLLISION_OUTCOME:
- If normalized identities collide, a semantic slug collides with a mirrored source-submodule path, or concern/FILES ownership is ambiguous, do not create or rename a detail arbitrarily.
- Report the candidate identities, colliding path or overlapping files, and the manual decision required.
- Never use task IDs, numeric suffixes (`-2`, `-003`), timestamps, branch names, or silent overlapping documents to resolve the collision.

POINTER_RESOLUTION:
- Semantic path = `.prizmkit/prizm-docs/<module>/<concern-slug>.prizm`.
- Parent L1 contains exactly one matching DETAILS entry; the target exists; target MODULE equals `<module>`; target CONCERN slug equals `<concern-slug>`; target FILES satisfies ownership rules.
- A semantic concern remains at L2. Do not create L3, a fourth level, a memory state machine, or a scoring system.

---

# SECTION 6: PROGRESSIVE LOADING PROTOCOL

## 6.1 When to Load

ON_SESSION_START:
  ALWAYS: Read exact .prizmkit/prizm-docs/root.prizm (L0) if it exists
  PURPOSE: Get the project map, understand architecture, know where to look

ON_TASK_RECEIVED:
  IF task references specific file or directory:
    LOAD_COMPLETE: direct-child L1 for the containing top-level module
    RESOLVE: the mirrored SUBDIRS pointer first; for a flat module, use the one DETAILS pointer whose semantic L2 FILES ownership contains the source file
  IF task is broad:
    LOAD_COMPLETE: only matching direct-child L1 documents from MODULE_INDEX or MODULE_GROUPS
  IF task is exploratory:
    LOAD: L0 only, then navigate through resolving pointers as needed
  IF task is cross-cutting:
    LOAD_COMPLETE: direct-child L1 documents for affected modules and only their relevant L2 details

ON_FILE_MODIFICATION:
  BEFORE editing any source file:
    1. Read the complete relevant L2 document when it exists; partial grep fragments cannot establish all traps, decisions, interfaces, and ownership constraints.
    2. Read the complete direct L1 and any complete parent/child documents needed to resolve the selected SUBDIRS or DETAILS pointer in both directions.
    3. Do not load unrelated L1/L2 documents.
    4. If relevant L2 is absent, inspect only the bounded target source files and narrowly implicated callers/contracts needed for the modification. Proceed without creating a placeholder.

ON_DEEP_READ:
  WHEN deep understanding is required without modification:
    READ_COMPLETE: the relevant L2 and resolving pointer documents
    IF L2 is absent: inspect bounded relevant source without creating documentation merely because it was read

## 6.2 Loading Rules

NEVER: Load all L1 and L2 docs at session start
NEVER: Use grep-only fragments as modification context for a relevant L2
NEVER: Load L2 for unrelated modules
NEVER: Skip exact root when it exists
NEVER: Create placeholder L2 during context loading
MUST: Read relevant L2 and resolving pointer documents completely before source modification
PREFER: Navigate root -> direct L1 -> nested L2
PREFER: Keep source fallback bounded to the target and concrete dependency ambiguity

---

# SECTION 7: AUTO-UPDATE PROTOCOL

## 7.1 Trigger

WHEN: During the normal formal lifecycle, run `/prizmkit-retrospective` after validated source changes when structure, interfaces, dependencies, behavior, or durable project knowledge changed. Use `prizmkit-prizm-docs Update` only for out-of-band repair/resync after docs drifted outside the normal development loop.
GOAL: Keep prizm docs synchronized with source code without creating multiple competing docs writers.

## 7.2 Value Gate

QUESTION: Before retaining a candidate fact, ask `Could a future AI that lacks this fact make an incorrect modification?`
PASS: yes, and the fact is current, durable, non-obvious, actionable for a future modification, and placed at the lowest owning level
KEEP:
- non-obvious public/exported interfaces and wire contracts
- cross-module constraints and non-obvious dependencies
- traps, side effects, and failure boundaries
- durable decisions with necessary rationale
- rejected alternatives likely to recur, with the reason they remain rejected
- security, data-integrity, concurrency, transaction, and compatibility rules
REJECT:
- structure/signatures directly and safely derivable from source
- task/change/session history and test inventories
- temporary investigation conclusions and future plans
- stale statements, duplicated meanings, and synonyms already represented
- long procedures, generic advice, low-value file lists, line counts, and complexity inventories
- behavioral content already complete in a child L2
APPLIES: Init, Update, Rebuild, and Migrate evaluate every candidate through this same gate

## 7.3 Cleanup Gate

TRIGGER: Before Update or Rebuild writes an existing target
STEPS:
1. Read the current target and its parent/child pointers; never use append-only synchronization or delete-first regeneration.
2. Verify every current fact against source and build the protected set of still-valid contracts, constraints, dependencies, traps, decisions, side effects, and safety/integrity rules.
3. Match candidate and existing facts by semantic meaning. Update one equivalent entry in place and merge synonyms instead of appending alternate wording.
4. Remove stale, duplicate, source-derivable, low-value, and parent-copied material.
5. Add only genuinely new durable facts that pass the Value Gate and have no equivalent entry.
6. Reconcile bottom-up: L2 owns behavior; L1 owns concise structure and SUBDIRS/DETAILS pointers; L0 owns the concise project map.
7. Measure raw UTF-8 capacity. If automatic remediation is required, follow Section 2.4 and preserve the protected set.
BLOCK: If protected knowledge cannot fit after safe movement or an unambiguous semantic split, report the blocker and required manual decision; never delete it for capacity.

## 7.4 Update Decision Logic

SUMMARY: For normal development, `/prizmkit-retrospective` gets changed files → maps modules → classifies (A/D/M/R) → applies value-aware bottom-up reconciliation (L2→L1→L0) → skips if no structural or durable-knowledge impact → enforces capacity. For out-of-band drift, `prizmkit-prizm-docs Update` applies the governing Value and Cleanup Gates after confirming the drift source.

DETAILED_STEPS: → ${SKILL_DIR}/references/op-update.md

## 7.5 Auxiliary Metadata Policy

NEVER: Add CHANGELOG sections or changelog.prizm during doc sync.
NEVER: Add UPDATED/date/time fields to .prizm files.
NEVER: Add workflow metadata such as feature/bug/refactor/task/session/run/pipeline/workflow IDs, branch names, absolute worktree paths, or `.prizmkit/specs` / `.prizmkit/dev-pipeline` artifact paths.
RATIONALE: Temporal and workflow history is outside Prizm memory; .prizm files store only durable project knowledge regardless of Git tracking policy.

---

# SECTION 8: ANTI-PATTERNS

WHAT_NOT_TO_PUT_IN_PRIZM_DOCS:

NEVER: Prose paragraphs or explanatory text (use KEY: value or bullet lists)
NEVER: Code snippets longer than 1 line (reference file_path:line_number instead)
NEVER: Human-readable formatting (emoji, ASCII art, markdown tables, horizontal rules)
NEVER: Duplicate information across levels (L0 summarizes, L1 indexes structure, L2 details behavior)
NEVER: Copy complete L2 interfaces, data flow, TRAPS, DECISIONS, or full RULES into L0/L1; keep a concise parent summary and resolving pointer
NEVER: Retain a candidate fact that fails the future-incorrect-modification Value Gate
NEVER: Append synonymous entries instead of updating one semantic meaning in place
NEVER: Implementation details or behavioral detail in L0 or L1 (INTERFACES, DATA_FLOW, TRAPS, DECISIONS belong in L2 only)
NEVER: Stale information (update or delete, never leave outdated entries)
NEVER: Full file contents or large code blocks (summarize purpose and interfaces)
NEVER: TODO items or future plans (those belong in issue trackers)
NEVER: Session-specific context or conversation history (docs are session-independent)
NEVER: Workflow metadata such as feature/bug/refactor/task/session/run/pipeline/workflow IDs, branch names, absolute worktree paths, or `.prizmkit/specs` / `.prizmkit/dev-pipeline` artifact paths
NEVER: CHANGELOG sections, changelog.prizm, or update-history sections
NEVER: Flowcharts, diagrams, mermaid blocks, or ASCII art (wastes tokens, AI cannot parse visually)
NEVER: Markdown headers (## / ###) inside .prizm files (use ALL CAPS KEY: format instead)
NEVER: Rewrite entire .prizm files on update (modify only affected sections)
NEVER: Delete still-valid critical knowledge merely to cross a capacity threshold
NEVER: Raise 4096B/4096B/5120B hard limits for project size or trim only to one byte below a limit when automatic remediation is required
NEVER: Create task-named, numbered, timestamped, colliding, ambiguous, or silently overlapping semantic concern documents
NEVER: Add L3, a fourth documentation level, a memory state machine, or a fact scoring system
NEVER: TRAPS entries without severity prefix ([CRITICAL], [HIGH], or [LOW])

---

# SECTION 9: INITIALIZATION PROCEDURE

## 9.1 Algorithm

OPERATION: Init (invoked via prizmkit-prizm-docs skill)
PRECONDITION: No .prizmkit/prizm-docs/ directory exists (or user confirms overwrite)

INPUT: Project root directory
OUTPUT: .prizmkit/prizm-docs/ with root.prizm and L1 docs for discovered modules

SUMMARY: Detect project type → discover modules (MODULE_DISCOVERY_CRITERIA) → apply Value Gate to every candidate → create mirrored directory structure → generate concise root.prizm (L0) and L1 pointer indexes → skip placeholder L2 (lazy) → configure hook → validate format/capacity/pointers → report.

DETAILED_STEPS: → ${SKILL_DIR}/references/op-init.md

KEY_CONCEPTS:

MODULE_DISCOVERY_CRITERIA — a directory qualifies as a module if ANY of the following is true:
- Contains source files that collectively form a logical unit (shared responsibility)
- Contains entry points, configuration files, or interface definitions
- Contains sub-directories that themselves qualify as modules
- Is referenced by multiple other modules as a dependency

A directory does NOT qualify if ALL of the following are true:
- Contains only generated/derived files (build output, compiled assets)
- Contains only vendored/third-party code
- Is in the EXCLUDE list

HIERARCHY RULE: if directory X lives inside top-level module M, X is a sub-module of M — NOT a separate top-level module. Its durable behavioral detail uses the mirrored L2 path. Semantic concern identity is considered only for a flat module under Section 5.4.

CAPACITY RULE: use MODULE_GROUPS whenever MODULE_INDEX cannot fit L0 within 4096B. Do not change hard limits for project size. Init does not create semantic or mirrored L2 placeholders; later Update/Rebuild/Migrate may create complete L2 documents when durable knowledge and unambiguous identity exist.

EXCLUDE: .git/, node_modules/, vendor/, build/, dist/, __pycache__/, target/, bin/, .claude/, .codebuddy/, .codex/, .agents/, .pi/, .prizmkit/
SOURCE_BOUNDARY: Excluding `.prizmkit/` excludes the installed Runtime at `.prizmkit/dev-pipeline/`; never exclude a repository's canonical top-level `dev-pipeline/` source module by basename.

## 9.2 Post-Init Behavior

After initialization, L2 docs are created incrementally by retrospective when changed source files provide meaningful behavior or durable knowledge:

ON_MODIFY trigger:
- Before editing a file in sub-module S within module M:
  IF .prizmkit/prizm-docs/<M>/<S>.prizm exists:
    AI reads the complete L2 plus complete resolving pointer documents.
  ELSE:
    AI reads bounded relevant source files as fallback, creates no placeholder, and proceeds with the modification.
- After the change, `/prizmkit-retrospective` creates L2 only when candidate interfaces, data flow, traps, or decisions pass the Value Gate.
- Real source submodules retain mirrored paths. A flat-module semantic detail follows Sections 3.3 and 5.4 and blocks on ambiguous concern identity, slug collision, or overlapping ownership.
- This keeps initialization lightweight while still capturing L2 depth when real durable context exists.

ON_DEEP_READ trigger:
- When AI needs to deeply understand a module but not modify it (e.g., code review, architecture analysis, dependency tracing, explaining complex logic):
  IF .prizmkit/prizm-docs/<M>/<S>.prizm does not exist:
    AI reads the relevant source files for the current task and may recommend a retrospective or repair pass if durable L2 knowledge should be preserved.
- Do not create placeholder L2 docs just because a module was read; create L2 only when there is meaningful behavior, interfaces, traps, or decisions to record.

---

# SECTION 10: SKILL DEFINITION

## 10.1 SKILL.md Reference

The Prizm skill is defined at: ${SKILL_DIR}/SKILL.md

OPERATIONS (all invoked via the prizmkit-prizm-docs skill):

  Init       - Bootstrap .prizmkit/prizm-docs/ for a new project. → ${SKILL_DIR}/references/op-init.md
  Update     - Repair/resync docs after out-of-band drift. → ${SKILL_DIR}/references/op-update.md
  Status     - Check freshness of all docs. → ${SKILL_DIR}/references/op-status.md
  Rebuild    - Regenerate docs for a specific module. → ${SKILL_DIR}/references/op-rebuild.md
  Validate   - Check format compliance and consistency. → ${SKILL_DIR}/references/op-validate.md
  Migrate    - Convert existing docs to .prizmkit/prizm-docs/ format. Steps inline in SKILL.md.

---

# SECTION 11: HOOK CONFIGURATION

## 11.1 Mechanism

VALIDATION_HOOK: The installed pre-commit hook invokes the canonical Python validator through host-neutral interpreter resolution only when staged Prizm documents exist.
FAILURE: If staged Prizm documents require validation, unavailable validator/interpreter and nonzero validation are fail-closed. With no staged Prizm documents, the hook is a no-op.
SNAPSHOT: `--staged` validates index blobs and complete index pointer context; it never substitutes unstaged working bytes.
MAINTENANCE_HOOK: Commit-intent and post-command hooks may remind about the owning retrospective/repair capability, but never stage, force-add, commit, modify ignore policy, require tracking, or append changelog content.
INSTALLATION: Upgrade replaces only deterministic PrizmKit-managed hook entries/blocks and preserves user-owned settings and hook behavior.

## 11.2 Host-Neutral Invocation

COMMAND: Installed settings invoke `.prizmkit/scripts/run-python-hook.cjs`, which resolves an available Python 3 launcher and propagates the real script exit status.
PORTABILITY: Platform/provider names and direct `python3` assumptions are not protocol identifiers. A missing candidate may fall through to another supported Python 3 launcher; a real validation failure is never retried as if the interpreter were missing.

## 11.3 Git Neutrality

RULE: Hooks validate only Git-visible staged documentation already selected by the project/user. They never make ignored files visible and never infer that `.prizmkit/**` must be tracked or ignored.
RULE: Commit-intent output is maintenance guidance, not staging or commit authorization.
RULE: No hook adds CHANGELOG content or invokes broad `git add .`, `git add -A`, or force-add.

---

# SECTION 12: LANGUAGE-SPECIFIC INITIALIZATION HINTS

## 12.1 Module Boundary Detection

LANGUAGE          MODULE_BOUNDARY                         ENTRY_POINT_DETECTION
Go                Directories with .go files              main.go, cmd/**/main.go
JavaScript/TS     Directories with index.ts/js/tsx/jsx    package.json main/bin
Python            Directories with __init__.py            __main__.py, manage.py, app.py, wsgi.py
Rust              Directories with mod.rs                 main.rs, lib.rs
Java              src/main/java/* package directories     *Application.java, Main.java
C#                Directories with *.cs files             Program.cs, Startup.cs

## 12.2 Interface Detection

LANGUAGE          EXPORTED_INTERFACE_PATTERN
Go                Capitalized function/type names (func Foo, type Bar)
JavaScript/TS     export/export default declarations
Python            Functions/classes without underscore prefix
Rust              pub fn, pub struct, pub enum, pub trait
Java              public class, public interface, public method
C#                public class, public interface, public method

## 12.3 Dependency Detection

LANGUAGE          IMPORT_PATTERN
Go                import "path/to/package"
JavaScript/TS     import ... from "...", require("...")
Python            import ..., from ... import ...
Rust              use crate::..., use super::..., extern crate
Java              import package.Class
C#                using Namespace
