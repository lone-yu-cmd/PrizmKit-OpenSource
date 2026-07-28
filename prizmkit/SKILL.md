---
name: "prizmkit"
description: "PrizmKit framework introduction and lifecycle navigator. Explains the independent project-init, formal requirement lifecycle, documentation, and deployment skills. Use when users ask what PrizmKit is, which skill to use, how to start, or how the lifecycle works. (project)"
---

# PrizmKit — Framework Introduction and Navigator

`/prizmkit` explains the PrizmKit toolkit and directs the user to the appropriate independent skill. It does not execute a requirement lifecycle itself.

## When to Use

- User asks what PrizmKit is or which skill to use.
- User asks how to start a project or a formal requirement.
- User asks about the development lifecycle or available tools.
- User invokes `/prizmkit`.
- User uses an ambiguous phrase such as "ship it" and the intent could mean commit or deploy.

## When NOT to Use

- User already knows the required skill; invoke that skill directly.
- A formal requirement is already in progress; continue through its owning coordinator or current atomic stage.
- User wants an immediate low-risk direct edit; perform the edit and its specific verification.

## Responsibility Map

```text
PrizmKit Toolkit
├── prizmkit
│   └── Framework introduction and navigation
├── prizmkit-workflow
│   └── One-entry orchestration for the formal requirement lifecycle
├── prizmkit-init
│   └── Recommended one-time project initialization
├── Formal requirement lifecycle
│   ├── prizmkit-plan
│   ├── prizmkit-implement
│   ├── prizmkit-code-review
│   ├── prizmkit-test
│   ├── prizmkit-retrospective
│   └── prizmkit-committer
├── prizmkit-prizm-docs
│   └── Independent Prizm documentation management
└── prizmkit-deploy
    └── Independent deployment and operations entry point
```

## Formal Requirement Lifecycle

Every formal requirement follows all six stages in this order:

```text
prizmkit-plan
  → prizmkit-implement
  → prizmkit-code-review
  → prizmkit-test
  → prizmkit-retrospective
  → prizmkit-committer
```

For a one-entry experience, invoke `/prizmkit-workflow`; it owns ordering, state, repair routing, and stage invocation without replacing stage responsibilities. Atomic Skills receive explicit stage-local input, return stage-local results, and never read or write the coordinator's state. External injected Prompts may provide the same orchestration around atomic Skills.

All six stages are required for a formal requirement. A stage may choose a verification depth appropriate to the change, but it may not be silently skipped.

### Direct Edit

Typos, pure formatting, small documentation edits, and other explicitly low-risk non-requirement changes may use a direct edit. Direct edit is not the formal requirement lifecycle.

### Stage Responsibilities

| Stage | Responsibility | Stage-local success |
|---|---|---|
| `prizmkit-plan` | Clarify the requirement and create/review `spec.md` and `plan.md`. | `PLAN_READY` |
| `prizmkit-implement` | Execute supplied plan tasks and record completion. | `IMPLEMENTED` |
| `prizmkit-code-review` | Review, repair, verify, and converge on the supplied change. | `PASS` |
| `prizmkit-test` | Test the supplied change with a consistent report/result pair. | `TEST_PASS` |
| `prizmkit-retrospective` | Synchronize durable documentation or record no change. | `RETRO_COMPLETE` |
| `prizmkit-committer` | Create a confirmed interactive commit or prepare an exact Runtime request. | `COMMITTED` or `COMMIT_REQUEST_READY` |

### `prizmkit-workflow`

Use for a one-entry formal requirement workflow. It coordinates all six lifecycle skills, preserves one `artifact_dir`, routes failures, and stops for commit confirmation. It handles exactly one requirement per invocation.

### `prizmkit-init`

`/prizmkit-init` is recommended the first time PrizmKit enters a project. It can create project context, configuration, a project brief, and Prizm documentation.

Initialization is a soft prerequisite, not a hard dependency:

- If project initialization is missing, the user may still invoke `/prizmkit-init` separately or continue without it.
- Planning reads the source tree, README, manifests, and available project rules as fallback context.
- Later documentation synchronization reports when the Prizm documentation system is not initialized instead of pretending that synchronization completed.

## Independent Skills

### `prizmkit-prizm-docs`

Use for Prizm documentation initialization, status, validation, migration, repair, and rebuild. It is not an additional stage required for every formal requirement.

### `prizmkit-deploy`

Use independently after development when deployment or operations work is needed. It is not a seventh requirement stage and does not replace the six development gates.

## Failure and Repair Routing

```text
REVIEW_NEEDS_FIXES
  → prizmkit-implement
  → prizmkit-code-review

TEST_NEEDS_FIXES
  → preserve test-report.md and test-result.json
  → stop with the known correction
  → caller owns any later review/retest route

TEST_BLOCKED
  → preserve the blocker without speculative code changes
  → caller owns recovery after truth, input, safety, environment, or reliability is restored
```

Automatic outer repair is limited to three rounds. The workflow stops with a resumable blocked result when the limit is reached or a gate cannot be safely completed.

## Commit and Deployment Boundary

The active coordinator validates all required evidence before invoking `prizmkit-committer` with exact `evidence_paths` and any caller-state `excluded_paths`. Interactive use confirms and creates a local commit. Preparation use returns `COMMIT_REQUEST_READY` without Git mutation; the injected Prompt records its pending state and Python Runtime executes the request.

Pushing to a remote is a separate explicit action. Deployment is always a separate invocation of `/prizmkit-deploy`.

## Quick Start

Install the skills through the host's skills installer, for example:

```bash
npx skills add <repository>
```

Then:

```text
1. Optionally run /prizmkit-init when entering a project for the first time.
2. Start a formal requirement with /prizmkit-plan.
3. Continue through implement → code-review → test → retrospective → committer.
4. For interactive use, confirm the local commit when `/prizmkit-committer operation=interactive-commit` presents it; pipeline runtimes use preparation mode and execute Git themselves.
5. Invoke /prizmkit-deploy separately when deployment or operations work is needed.
```

## Scope Boundary

This toolkit is self-contained. External coordinators integrate through atomic stage inputs, stage-owned artifacts, and domain results; coordinator state and routing remain outside atomic Skill contracts.

The toolkit does not promise universal automatic handoff, universal deployment automation, automatic remote push, or access beyond the host platform's permissions and environment.

If the user says only "ship it", ask whether they mean:

1. Use `/prizmkit-committer operation=interactive-commit` for a user-confirmed local commit, or preparation mode when a Python pipeline runtime owns Git execution.
2. Deploy or operate the project with `/prizmkit-deploy`.

Do not route an ambiguous "ship it" directly to either action.
