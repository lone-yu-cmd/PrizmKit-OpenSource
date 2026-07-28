# Operation: Status — Detailed Steps

Check freshness of all .prizm docs.

PRECONDITION: .prizmkit/prizm-docs/ exists with root.prizm.

STEPS:
1. Read exact `root.prizm` and resolve registered direct-child L1 and nested L2 pointers from current filesystem content. Status never requires Git history and never inspects whether managed paths are ignored, untracked, or tracked.
2. For each L1/L2 document, compare its filesystem modification time with current mapped source files only as an advisory freshness signal. Resolve real source submodules through SUBDIRS and flat semantic concerns through DETAILS plus authoritative FILES ownership.
3. Classify freshness as FRESH (doc not older than source), STALE (source newer), or MISSING (a required resolving pointer or Value-Gate-qualified documented concern lacks a complete target). An absent placeholder with no Value-Gate-qualified knowledge is not MISSING.
4. Measure every `.prizm` file from its actual raw UTF-8 bytes and classify the exact path: only `.prizmkit/prizm-docs/root.prizm` is L0 with 4096B; direct children are L1 with 4096B; nested mirrored or semantic documents are L2 with 5120B. Never infer capacity from project size, line count, character count, filename, source depth, or Git state.
5. Classify capacity as normal (<80%), warning (80% to <90%), strong-warning (90% through 100%), or error (>100%). Sort every non-normal capacity entry by exact descending utilization using integer ratio comparison, then repository-relative path ascending for ties.
6. For each non-normal entry report `DOC_PATH | LEVEL | BYTES | LIMIT | BAND | TARGET_RANGE | ACTIONS`. Target is 3277-3686B for L0/L1 or 4096-4607B for L2. ACTIONS include concrete level-appropriate trim, deduplicate, move-to-child, and semantic-split guidance.
7. Status is read-only. A warning or strong warning is not "oversize" and does not force a split. An error is over the hard limit. Recommend semantic split only for an eligible flat module with multiple stable concerns after Value/Cleanup filtering; otherwise recommend the applicable non-destructive actions or manual decision.
8. When inspecting representative or named documents, use their current measured bytes and detected level. Do not special-case paths or repeat stale measurements in guidance.

OUTPUT:
- Freshness table: `DOC_PATH | LEVEL | STATUS | PRIZM_FILESYSTEM_MOD | SOURCE_FILESYSTEM_MOD` (advisory; no Git-history requirement).
- Capacity table: non-normal entries in descending utilization with `DOC_PATH | LEVEL | BYTES | LIMIT | BAND | TARGET_RANGE | ACTIONS`.
- Summary counts for normal, warning, strong-warning, and error. Status reports errors but does not mutate documents.
