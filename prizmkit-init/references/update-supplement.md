# Update Supplement — Post-Merge Gap-Fill Procedure

Runs after tech stack merge in Update mode:

1. **Bounded module scan**: Re-scan only the registered top-level source modules and concrete structural gaps using the same two-tier model. Exclude the complete `.prizmkit/` framework directory, including installed `.prizmkit/dev-pipeline/`, but do not exclude a repository's canonical top-level `dev-pipeline/` source module.
2. **Missing L1 check**: For a discovered top-level module with no direct-child L1, build one complete Value-Gate-filtered structural candidate at `.prizmkit/prizm-docs/<M>.prizm` and add a resolving root pointer only after the candidate validates.
3. **Missing L2 context**: For an affected source submodule with no nested L2, inspect only the bounded source files and narrowly implicated contracts needed to determine the gap. Do not create a placeholder. A complete L2 may be created only when current durable facts pass the Value Gate and mirrored/semantic identity, ownership, pointer, format, and capacity checks all pass.
4. **Existing target reconciliation**: Read every complete affected target and complete resolving parent/child pointer document. Apply Cleanup by semantic meaning, preserve protected knowledge, build candidates bottom-up, skip byte-identical replacements, and re-read actual bytes after writes.
5. **Failure and report**: If any post-write check fails, restore exact pre-write bytes and remove invalid new targets before reporting a blocker. Report modules/details added, skipped source fallbacks, stale summaries reconciled, and capacity/pointer validation. Never stage, commit, force-add, change or interpret `.gitignore`, require Git history, or classify tracking state as documentation health.
