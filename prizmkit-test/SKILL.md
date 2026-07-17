---
name: "prizmkit-test"
description: "Mandatory testing stage for a formal PrizmKit requirement. Validates the final Main-Agent-reviewed workspace with auditable project-native evidence and returns TEST_PASS, TEST_FAIL, or TEST_BLOCKED. Lightweight scopes still execute deterministic verification and return TEST_PASS when successful. (project)"
---

# PrizmKit Test

`/prizmkit-test` is the mandatory test stage after `prizmkit-code-review` reaches `PASS`. It validates the final reviewed workspace and produces auditable evidence. Completeness means that affected observable behavior, contracts, boundaries, invariants, errors, state transitions, and coupling risks are represented and proven; it does not mean mechanically reaching a line-coverage threshold.

This skill orchestrates the target project's native runners and conventions. It does not install a cross-language test runtime.

## Formal Lifecycle Position

```text
prizmkit-plan
  → prizmkit-implement
  → prizmkit-code-review
  → prizmkit-test
  → prizmkit-retrospective
  → prizmkit-committer
```

`prizmkit-test` must not be silently skipped for a formal requirement.

## When to Use

- After `/prizmkit-code-review` reports `PASS`.
- When workflow state resumes a blocked or failed test stage.
- After an implementation repair that changed only tests, fixtures, test-runner configuration, or evidence infrastructure.
- When the user asks to test, verify, add complete module tests, inspect boundaries, or produce auditable evidence.

## When NOT to Use

- The active requirement has not passed code review; return to `/prizmkit-code-review` first.
- A production-affecting repair is complete but has not received the required delta review.
- The request is a direct edit outside the formal requirement lifecycle.

## Model Choice vs Fixed Evidence Mechanics

Choose project-semantic parameters from the target project: framework, commands, cwd, timeout, retry/attempt policy, concurrency, mock tools, test layers, module boundary, inventory patterns, mutation technology, and environment classification. Do not hard-code ecosystem-specific defaults when the project can decide them.

Fix only the protocol mechanisms needed for safe, replayable evidence: project/evidence/request locators, schema-shaped requests, path confinement, real process execution, complete raw capture, runner-generated chained receipts, hash binding, append-only history, differential isolation/cleanup, and resume invalidation. Read `${SKILL_DIR}/references/trusted-evidence-execution.md` before inventory, execution, differential proof, resume, or replay. Read `${SKILL_DIR}/references/evidence-request-protocol.md` when authoring requests or authoritative records.

## Preconditions and Safety

1. Reuse the caller's `artifact_dir` and workflow state. Do not re-detect a different requirement.
2. Confirm the latest review result is `PASS` and the current workspace has not received an unreviewed production change.
3. Load `root.prizm`, relevant L1/L2 docs, project manifests, runner configuration, and changed scope once.
4. Never use production credentials, production databases, production APIs, production queues/storage, or destructive operations against real data.
5. Preserve complete command/environment/output values only under the target project's sensitivity policy; expose mocked-versus-real claims and follow the target project's retention and upload policy.
6. Treat code-level dependencies as mock-first. Real deployed test-environment validation is separate authorized work.
7. Never delete existing tests.

If test infrastructure is missing, prepare only necessary project-native infrastructure and record every change. Do not turn an environment problem into speculative production edits.

## Input

| Parameter | Required | Description |
|---|---|---|
| `scope` | No | `full-project`, `module:<name>`, `feature:<slug>`, or `this-change`. Defaults to `this-change` with a valid artifact directory. |
| `artifact_dir` | No | Change artifact containing `spec.md` and `plan.md`. |
| `changed_files` | No | Explicit changed files; highest-priority scope input. |
| `diff_base` | No | Git baseline used when `changed_files` is absent. |
| `evidence_target` | No | Existing evidence ID/directory to validate and resume. |
| `execution_budget` | No | Bounded time/attempt budget. Incomplete necessary work is `TEST_BLOCKED`, never silently truncated to pass. |
| `test_commands` | No | Explicit project-native commands when discovery is ambiguous. |

For `scope=this-change`, determine changed files from explicit input, diff base, current diff, artifact plan/context, then spec mapping. Unknown scope is `TEST_BLOCKED`.

## Required State Machine

Execute in this exact order:

```text
CHANGE_CLASSIFY
  → SCOPE_DISCOVER
  → CONTRACT_MODEL
  → TEST_PLAN
  → INFRA_READY
  → TEST_BUILD
  → EXECUTE_PROVE
  → EVIDENCE_PACKAGE
  → EVIDENCE_VALIDATE
```

Do not claim a later state complete without valid applicable predecessor outputs. Use the existing authoritative references, schemas, builder, and validator shipped under this skill for the detailed mechanics.

### Lightweight Verification

Classify an exclusively documentation, comment, or formatting scope as `lightweight` only when deterministic evidence proves runtime behavior cannot change. Still execute the test protocol's classification, scope, evidence, and validation states. Validate the relevant format, links, paths, structure, generated artifacts, and changed scope. A successful lightweight run returns `TEST_PASS` with a report such as:

```text
TEST_STATUS: TEST_PASS
TEST_SCOPE: documentation-only
VERIFICATION:
- format and structure validation
- internal link/path validation
- changed-file scope review
```

Do not use `TEST_NOT_APPLICABLE` as a lifecycle result.

### Behavior Verification

For behavior or uncertain changes, use the full evidence protocol and test layers required by observable behavior, contracts, boundaries, regression rings, and coupling risks. Necessary unproven behavior, unavailable infrastructure, unreliable execution, failed cleanup, or deterministic validation failure returns `TEST_BLOCKED`.

## Terminal Verdicts

Only these testing outcomes are valid:

- `TEST_PASS`: required verification and evidence validation succeeded for the selected scope.
- `TEST_FAIL`: a valid reliable test reproduces an implementation or resolved-contract failure.
- `TEST_BLOCKED`: scope, truth, environment, evidence, cleanup, or validation prevents a trustworthy verdict.

A `TEST_FAIL` is not automatically a production defect. First classify the repair scope from the failing evidence:

```text
TEST_FAIL
  ├── test-infrastructure
  │     tests, fixtures, test-runner configuration, or evidence setup only
  │     → implement → test
  │
  └── production
        production code, runtime configuration, schema, dependency,
        or public interface
        → implement → code-review → test
```

If the failure is caused by missing environment, permissions, dependencies, external services, or unavailable authorized resources, return `TEST_BLOCKED` and pause without speculative code changes. Resume from this stage when the environment is available.

## Workflow State and Handoff

Before reading or updating workflow state, read `${SKILL_DIR}/references/workflow-state-protocol.md`.

On `TEST_PASS`, update `.prizmkit/state/workflows/<requirement-slug>.json`:

```json
{
  "stage": "test",
  "status": "TEST_PASS",
  "completed_stages": ["plan", "implement", "code-review", "test"],
  "repair_scope": null,
  "next_stage": "retrospective",
  "resume_from": "prizmkit-retrospective"
}
```

On `TEST_FAIL`, record the evidence-backed `repair_scope`, set `next_stage` to `implement`, and increment the outer repair round. The implementation stage chooses the next review/test route from that scope.

On `TEST_BLOCKED`, set `status` to `TEST_BLOCKED`, preserve the evidence and blocking reason, set `next_stage` to `test`, and do not modify production code merely to clear the block.

After `TEST_PASS`:

```text
TEST_PASS
  → /prizmkit-retrospective
```

If semantic skill handoff is supported, continue automatically with the same `artifact_dir`; otherwise provide the deterministic next invocation and state path.

## Resume and Idempotency

When interrupted or re-invoked:

1. Validate existing manifest, hashes, and stage outputs.
2. Recompute code, test, contract, dependency, environment, and plan input hashes.
3. Preserve prior executions and raw output according to the target project's retention policy.
4. Invalidate the first changed stage and downstream results.
5. Resume from the last valid predecessor.

Never silently reduce required scope.

## Handoff Boundary

Do not embed an independent AI reviewer, decide overall code quality, claim broad spec compliance, repair a validly detected business defect, authorize commit/release, or perform deployed production validation. `prizmkit-test` returns the strict testing verdict and structured evidence pointers to the next lifecycle stage.
