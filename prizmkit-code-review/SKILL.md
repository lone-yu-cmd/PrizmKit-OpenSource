---
name: "prizmkit-code-review"
description: "Review one supplied complete change with a bounded Main-Agent review/repair loop and optional capability-gated independent correctness review. Produces review-report.md and returns PASS or NEEDS_FIXES. (project)"
---

# PrizmKit Code Review

`/prizmkit-code-review` reviews one caller-supplied complete change. The current Main Agent owns the complete baseline review loop: it discovers findings, adjudicates them, directly repairs accepted findings, verifies repairs, and continues until the review converges or stops safely. After convergence, one strictly capability-gated independent Reviewer may objectively check the complete current implementation without taking mutation or final-decision authority.

## Execution Boundary

- Main-Agent review remains mandatory and must not be delegated directly or indirectly.
- After Main-Agent convergence only, this skill may create the single independent Reviewer defined by `${SKILL_DIR}/references/independent-code-review.md` when every structural capability in that reference is proven.
- Do not invoke another review process from inside this skill.
- Do not launch any additional review work through a general-purpose execution unit or relabel it as a finder, verifier, audit, compatibility review, verification, or gap sweep.
- The independent Reviewer cannot mutate, execute arbitrary commands, or create downstream execution units; prompt instructions never substitute for these structural guarantees.
- The Main Agent may directly read, search, edit, and run targeted verification in the active workspace.
- Review repairs use targeted verification appropriate to each accepted finding.
- `{artifact_dir}/review-report.md` is the only persisted review artifact for this execution.

## Report Renderer Contract

Use `${SKILL_DIR}/scripts/render_review_report.py` as the canonical executable writer for report initialization, validated progress append, and finalization:

```text
resolved Python 3 interpreter + render_review_report.py init <report>
resolved Python 3 interpreter + render_review_report.py append <report>  ← validated event JSON on standard input
resolved Python 3 interpreter + render_review_report.py finalize <report> ← validated final JSON on standard input
```

Resolve a compatible Python 3 interpreter through the current Host's executable capability; do not require one operating-system-specific command name. If no compatible interpreter is available, follow `${SKILL_DIR}/references/review-report-template.md` directly, record the renderer fallback in Final Verification evidence, and apply every equivalent count, ordering, field, and terminal-shape check before returning a verdict. Never silently omit renderer-owned fields or claim executable validation occurred during fallback.

## Atomic Stage Boundary

`prizmkit-code-review` owns the complete review, accepted-correction repairs, targeted verification, and `review-report.md` for one supplied change. It returns `PASS` or `NEEDS_FIXES` and stops.

## When to Use

- A caller supplies a complete implementation for review.
- A caller supplies a production-affecting repair for delta review.
- The user asks for a complete current-change correctness review.

## When NOT to Use

- No valid `spec.md` and `plan.md` exist for the active requirement.
- Implementation tasks or required repair work remain incomplete.
- The request has no review input and does not require this bounded review contract.

## Input

| Parameter | Required | Description |
|---|---|---|
| `artifact_dir` | Yes | Caller-supplied directory containing the exact `spec.md` and `plan.md` for this review. |
| `review_scope` | No | `full` for the initial review; `delta` for a production-affecting repair after a prior review pass. |

Review only the caller-supplied `artifact_dir`; never discover a different recent artifact. Missing or inconsistent stage input produces `NEEDS_FIXES` with the exact input blocker.

## Default Correctness Scope

The current requirement change outside `.prizmkit/**` is the ordinary correctness scope. Every `.prizmkit/**` path is excluded by default from correctness review, including correctness diffs, candidate findings, repairs, and verification scope. The Skill may read only exact caller-supplied `.prizmkit` artifacts such as `spec.md` and `plan.md` as evidence for the outside-framework requirement and may write its own `review-report.md`; it must not assess, report findings against, or repair their content. Neither action makes `.prizmkit` content reviewable production change. Correctness review of any framework/support artifact requires a separate explicit support-artifact review contract naming the exact artifacts and validator.

Generated host-support paths are also excluded by default, including `AGENTS.md`, `skills-lock.json`, installed platform directories, and local platform settings. An explicitly owned support change requires a separate explicit support-artifact validation contract; do not pull it into ordinary Code Review through workspace expansion. Record excluded changed paths in the report so exclusion is visible rather than mistaken for reviewed content.

## Phase 0: Initialize Report and Reuse Current Context

1. Resolve `{artifact_dir}` and `{artifact_dir}/review-report.md` from the active requirement context.
2. At the start of each execution, initialize a replacement report through the Report Renderer Contract and `${SKILL_DIR}/references/review-report-template.md`.
3. Within that execution, append every review round, repair batch, independent-review event, final verification, and exactly one `## Final Result` through the renderer or its visible equivalent fallback.
4. Start from the Main Agent's current requirement context and inspect the complete workspace inventory first: `git status --short`, the staged diff, and the unstaged diff. Include untracked, deleted, and renamed paths in classification, then remove default-excluded `.prizmkit/**` and host-support paths from the correctness scope before producing findings.
5. Append one validated `scope-classification` renderer event containing exact in-scope paths and exact default-excluded changed paths; do not describe exclusions as reviewed or silently repair them.
6. Reuse current context and load only missing or potentially stale material required to resolve a concrete ambiguity, verify an acceptance criterion, or understand a changed contract.
7. Inspect unchanged callers, dependents, contracts, or tests only when the in-scope diff changes or may violate an interface, shared behavior, or regression boundary. Do not perform an unconditional repository-wide dependency sweep.
8. For `review_scope=delta`, focus on in-scope files and behavior affected since the prior review pass and expand only across contracts implicated by that delta.
9. If no in-scope changes exist, record final verification and `PASS` only when the current requirement context and prior implementation state prove there is nothing left to review.

## Phase 1: Main-Agent Review Loop

The Main Agent reviews the complete current change, using the active requirement context and expanding beyond the diff only when a concrete acceptance criterion, contract, dependency, or regression risk requires it.

Use at most ten completed review rounds per execution. Track:

```yaml
main_review_rounds: 0
accepted_findings: 0
fixed_findings: 0
rejected_findings: 0
unresolved_findings: 0
```

For every candidate finding:

1. Describe a reproducible failure scenario, affected behavior, and evidence.
2. Classify exactly one of:
   - `accepted`: evidence proves an in-scope repair is needed;
   - `rejected`: evidence disproves the failure scenario;
   - `unresolved`: correctness or safe repair cannot be established.
3. Treat Missing tools, permissions, environment, or required evidence as an unresolved finding when they prevent review verification.
4. If a repair cannot be completed safely, record an unresolved finding and return `NEEDS_FIXES`.
5. Append the validated review-round event through the Report Renderer Contract.

Round behavior:

```text
accepted = 0 and unresolved = 0
  → review converged
  → when all candidate findings are rejected, accepted remains 0 and the review converges

accepted > 0 and rounds remain
  → Main Agent directly repairs accepted findings
  → targeted verification
  → next complete review round

unresolved > 0 or safe repair impossible
  → NEEDS_FIXES

maximum ten completed rounds reached with accepted findings
  → NEEDS_FIXES
```

## Phase 2: Repair and Verification

For accepted findings while the round limit remains:

1. Repair directly in the active workspace.
2. Run targeted tests, static checks, or other verification appropriate to each repair.
3. Inspect the complete resulting diff for unrelated changes and regressions.
4. Append validated repair-verification evidence through the Report Renderer Contract and continue the review loop.

Do not turn review verification into a broad unrelated test campaign; use targeted checks that establish each repair.

If a repair is unsafe, incomplete, or unverifiable, record an unresolved finding and finish with `NEEDS_FIXES`.

## Phase 3: Independent Code Review

Run only after the Main-Agent review and repair loop converges with no unresolved finding. Main-Agent review remains mandatory on every host; this optional check never replaces or weakens it.

1. Read `${SKILL_DIR}/references/independent-code-review.md` and follow its complete contract.
2. Apply its all-or-nothing semantic Host Capability Gate. If any required structural capability is unavailable or unproven, create no Reviewer, append `independent-review-downgrade`, and preserve the valid completed Main-Agent review.
3. When the gate passes, provide exact artifact/spec/plan paths and contents, Main-Agent-captured complete current changes, implementation context, and verification results to one active Code Reviewer with the reference's Initial Reviewer Prompt.
4. Use maximum five Reviewer responses. Append `independent-review-round` and `independent-adjudication` events. The Main Agent adjudicates every correction as `accepted`, `rejected`, or `unresolved` and retains all mutation authority.
5. For accepted corrections, repair directly in the active checkout, run targeted verification, and inspect the complete resulting change.
6. When responses remain, prepare complete latest state and prefer native continuation. If unavailable, the reference permits one compliant replacement with complete latest state, prior adjudication, and the same remaining budget.
7. If neither compliant continuation nor replacement is available after repair, append downgrade and rerun the Main-Agent review over that repair within the existing ten-round safety fuse.
8. If the fifth response causes a repair, run targeted verification, inspect the complete final change, record `Final State Independently Rechecked: no`, and do not send a sixth response.
9. `NO_CORRECTION_NEEDED` or all corrections rejected with evidence converges independent review. Any unresolved correction produces `NEEDS_FIXES`.

## Phase 4: Final Result

Before completing:

1. Confirm the final workspace is the complete reviewed change.
2. Confirm all accepted findings are fixed and no unresolved finding remains for `PASS`.
3. Append final verification and exactly one final result through the Report Renderer Contract or its visibly recorded equivalent fallback.

Valid results:

```text
PASS | NEEDS_FIXES
```

`PASS` requires review convergence, no unresolved findings, and credible targeted verification. `NEEDS_FIXES` means a concrete correction remains or safe completion was not established.

## Output

Return only review-stage outputs:

- `artifact_dir` and `review-report.md` path;
- `PASS` when review converged with all accepted findings repaired;
- `NEEDS_FIXES` when accepted or unresolved findings remain;
- finding counts, repair verification, and concrete remaining findings.

Return only the listed review outputs. Do not invoke another Skill.
