# Operation: Update — Out-of-Band Repair/Resync

Repair `.prizmkit/prizm-docs/` after docs drifted outside the normal development loop.

PRECONDITION: `.prizmkit/prizm-docs/` exists with `root.prizm`.

Use this operation for manual edits, merges, rebases, branch switches, generated code movement, or other changes that did not pass through `/prizmkit-retrospective`. During ordinary feature/bugfix/refactor work, use `/prizmkit-retrospective` instead.

STEPS:
1. Identify drift source from explicit user context when supplied; otherwise run a bounded source/document rescan over registered modules and concrete missing/stale pointers. Do not require Git history, inspect tracking state, or change behavior because managed files are ignored, untracked, or tracked.
2. Map changed files to modules through MODULE_INDEX or MODULE_GROUPS in `root.prizm`, then resolve mirrored SUBDIRS or flat-module DETAILS ownership from the relevant L1.
3. Classify each source change as A, D, M, or R, but do not mechanically turn changes into documentation. Treat every possible file, interface, dependency, flow, trap, decision, rule, and summary as a candidate and apply the future-incorrect-modification Value Gate.
4. Before writing any existing L2, L1, or L0 target, read that complete target and complete resolving parent/child pointer documents. Build a protected set of still-valid public/wire contracts, cross-module constraints, non-obvious dependencies, traps, decisions with necessary rationale, likely-to-recur rejected alternatives, side effects, and security/data-integrity/concurrency/transaction/compatibility rules.
5. Apply the Cleanup Gate by semantic meaning:
   - update an equivalent entry in place rather than appending alternate wording
   - merge synonymous entries into one shortest complete meaning
   - remove stale, duplicate, source-derivable, low-value, and parent-copied material
   - add only a genuinely new durable fact with no semantic equivalent
   Append-only repair is prohibited.
6. Reconcile bottom-up. L2 owns Value-Gate-qualified INTERFACES/DATA_FLOW/DEPENDENCIES/RULES/TRAPS/DECISIONS. L1 owns concise FILES/KEY_FILES/SUBDIRS/DETAILS/DEPENDENCIES summaries. L0 changes only for project-map structure. When L2 has complete behavior, L0/L1 retain only a concise summary and resolving pointer, never copied interfaces, data flow, traps, decisions, or full RULES.
7. Preserve `PROJECT_BRIEF:` in `root.prizm`; it is managed by `/prizmkit-init`. Do not write prohibited history, date, workflow, branch, absolute-path, or runtime-artifact metadata.
8. Skip comments/whitespace/formatting-only changes, `.prizm`-only changes, and test-only changes that reveal no durable behavior boundary or fact passing the Value Gate.
9. If a new top-level directory qualifies as a module, create its direct-child L1 and add a concise pointer to MODULE_INDEX or MODULE_GROUPS. Use MODULE_GROUPS whenever MODULE_INDEX cannot fit within 4096B; never raise the limit for project size.
10. Create L2 only for durable behavioral knowledge:
   - a real source submodule always uses its mirrored `.prizmkit/prizm-docs/<module>/<submodule>.prizm` path
   - a flat module may use `.prizmkit/prizm-docs/<module>/<concern-slug>.prizm` only when multiple stable concerns cannot safely fit one 5120B L2 after cleanup
   - semantic details require the complete CONCERN terminal shape, explicit non-empty/non-overlapping FILES ownership, and one resolving L1 DETAILS entry
   - ambiguous concern identity, empty normalization, mirrored-path/slug collision, or overlapping ownership blocks creation and reports the manual decision; never use task IDs or numeric suffixes
11. Measure all affected targets by exact raw UTF-8 bytes with L0/L1 4096B and L2 5120B limits. Natural content below 80% remains unchanged; warning-range content is valid and reported. Clean, move, or safely split rewritten targets at 90% or above toward 3277-3686B for L0/L1 or 4096-4607B for L2. If a hard-limit error or repeated pressure cannot be resolved without deleting protected knowledge, block the write.
12. Preflight complete candidate bytes, write validated targets bottom-up, compare each candidate with current bytes, and skip byte-identical replacements.
13. Re-read actual bytes and validate Value/Cleanup compliance, parent-summary boundaries, semantic ownership/identity, pointers in both directions, hierarchy, capacity, memory hygiene, and format. Warning-only capacity results pass; hard-limit or format errors fail.
14. If any post-write check fails, restore every existing target to its exact pre-write bytes and remove invalid new targets before returning a blocker.
15. Report updated, created, removed, merged, protected, and skipped facts/docs with reasons plus capacity diagnostics ordered by descending utilization. Do not stage, commit, force-add, modify or interpret ignore policy, or require Git history.

OUTPUT: List updated, created, removed, merged, protected, and skipped docs/facts with reasons; sorted capacity diagnostics; ambiguity blockers; and an explicit statement that this was out-of-band repair/resync, not a normal development retrospective.
