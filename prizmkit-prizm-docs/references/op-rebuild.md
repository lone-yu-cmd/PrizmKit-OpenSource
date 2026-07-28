# Operation: Rebuild — Detailed Steps

Regenerate docs for a specific module from scratch. Requires a module path argument.

PRECONDITION: .prizmkit/prizm-docs/ exists. Module path is valid.

STEPS:
1. Read the complete existing direct-child module L1, every complete pointed nested L2, and the complete relevant root pointer context before changing anything. Do not delete first. Snapshot semantic meanings, pointers, paths, and a protected set of still-valid public/wire contracts, cross-module constraints, non-obvious dependencies, traps, decisions with necessary rationale, likely-to-recur rejected alternatives, side effects, and security/data-integrity/concurrency/transaction/compatibility rules.
2. Re-scan the current module source for files, public/wire behavior, dependencies, flows, stable concerns, and real source submodules. Treat each observation and each old entry as a candidate under the future-incorrect-modification Value Gate; source-derived, transient, historical, test-inventory, stale, duplicate, procedural, and low-value material is omitted.
3. Reconstruct the module map in memory, then apply the Cleanup Gate to each existing target: update equivalent meanings in place, merge synonyms, remove stale/derivable/parent-copied content, and add only genuinely new durable knowledge. Append-only growth and delete-first regeneration are prohibited.
4. Reconcile detail identity:
   - real source submodules preserve mirrored `.prizmkit/prizm-docs/<module>/<submodule>.prizm` paths
   - a flat module may gain deterministic semantic `.prizmkit/prizm-docs/<module>/<concern-slug>.prizm` L2 documents only when multiple stable behavior concerns cannot retain protected knowledge in one 5120B L2 after cleanup
   - each semantic L2 has the complete CONCERN terminal shape, explicit non-empty/non-overlapping FILES ownership, and one resolving L1 DETAILS pointer
   - unstable concern boundaries, empty normalized slugs, sibling or mirrored-path collisions, and overlapping ownership block arbitrary creation; report the required manual identity/ownership decision instead of task names or numeric suffixes
5. Rewrite the existing L1 as a concise structural summary and pointer index only. Preserve SUBDIRS pointers for real source-submodule L2 and DETAILS pointers for semantic L2. Never copy child interfaces, data flow, traps, decisions, or full rules into L1. Remove an obsolete detail only after all still-valid protected knowledge has been preserved in its current owner and its source/concern identity no longer exists.
6. Update only the equivalent root MODULE_INDEX or MODULE_GROUPS entry in place. Preserve concise pointer-only parent behavior, existing project-wide knowledge, and `PROJECT_BRIEF:`. Use MODULE_GROUPS whenever MODULE_INDEX cannot fit within the unchanged 4096B L0 limit; more than 15 modules is a mandatory grouping trigger, not permission for a larger root.
7. Measure exact raw UTF-8 bytes using hard limits L0/L1 4096B and L2 5120B. Report warning-range results without failing. For any rewritten target at 90% or above, trim low-value material, deduplicate, move child-owned behavior, or safely semantic-split toward 3277-3686B for L0/L1 or 4096-4607B for L2. Never delete protected knowledge for size; unresolved hard-limit or unsafe-split pressure blocks Rebuild.
8. Build and validate the complete affected candidate set before replacement, then write bottom-up. Compare candidate/current bytes and do not rewrite byte-identical targets.
9. Re-read actual bytes and validate Value/Cleanup compliance, complete semantic fields, FILES ownership, pointer resolution in both directions, hierarchy, parent-summary boundaries, capacity, and format. Warning-only results pass; hard-limit or format errors fail.
10. If any post-write check fails, restore every replaced target to exact pre-write bytes and remove invalid new targets before returning a blocker. Rebuild never stages, commits, force-adds, changes or interprets ignore policy, requires Git history, or treats tracking state as health.

OUTPUT: Rebuilt-document before/after summary listing entries updated in place, merged, removed, added, and protected; sorted capacity diagnostics; semantic identity/ownership decisions; and any blocking ambiguity.
