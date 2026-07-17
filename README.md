# PrizmKit

[简体中文](README.zh-CN.md)

PrizmKit is a platform-agnostic collection of Agent Skills for completing one formal software requirement through a structured lifecycle:

```text
plan → implement → code-review → test → retrospective → committer
```

The toolkit gives each stage a clear responsibility, preserves handoff state, routes repairs through the correct quality gates, and requires confirmation before creating a local Git commit.

## Why PrizmKit?

AI coding sessions often blur planning, implementation, review, testing, documentation, and commit responsibilities. PrizmKit separates those responsibilities while keeping them connected:

- requirements begin with explicit goals and acceptance criteria;
- implementation follows a reviewed task plan;
- the Main Agent reviews and repairs the complete change before final testing;
- project-native testing validates the final reviewed workspace;
- durable project knowledge is synchronized before commit;
- a local commit is created only after the user confirms the exact scope and message.

## Skill Map

```text
PrizmKit
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

## Installation

Install this repository with a skills-compatible installer:

```bash
npx skills add <owner>/<repository>
```

Follow the installer prompt and select the PrizmKit skills you want. Install all six formal lifecycle skills to use the complete requirement lifecycle.

This repository publishes platform-neutral `SKILL.md` sources. The host determines where skills are installed, which tools they may use, and whether one skill can invoke the next automatically.

## Quick Start

### 1. Entering a Project for the First Time

Run `prizmkit-init` to inspect the project and create useful PrizmKit context:

```text
/prizmkit-init
```

Initialization is recommended, not mandatory. If it has not run, `prizmkit-plan` explains the benefits and can continue using the README, manifests, project rules, source tree, and relevant source files as fallback context.

### 2. Start a Formal Requirement

For the one-entry experience, invoke:

```text
/prizmkit-workflow <requirement>
```

It coordinates the same six stage skills and preserves the requirement context. You can also invoke `/prizmkit-plan` directly when you want to start or control the lifecycle manually.

The formal lifecycle is fixed:

```text
prizmkit-plan
  → prizmkit-implement
  → prizmkit-code-review
  → prizmkit-test
  → prizmkit-retrospective
  → prizmkit-committer
```

All six stages run for a formal requirement. A stage may select a scope-appropriate depth, but it is not silently skipped.

### 3. Confirm the Commit

Before changing local Git history, `prizmkit-committer` presents:

- the intended files;
- added, modified, deleted, and renamed file summaries;
- sensitive-file warnings;
- the diff summary;
- the proposed Conventional Commit message.

The commit runs only after user confirmation. Push is a separate explicit action.

### 4. Deploy Separately

Deployment is not a seventh requirement gate. Invoke it independently when needed:

```text
/prizmkit-deploy
```

## Formal Lifecycle

### Plan

`prizmkit-plan` creates and reviews:

```text
.prizmkit/specs/<requirement>/
├── spec.md
└── plan.md
```

It is the lifecycle entry point and preserves one `artifact_dir` for every later stage.

### Implement

`prizmkit-implement` executes the reviewed tasks, records checkpoints, and performs implementation-local verification. Initial implementation always proceeds to code review.

### Code Review

`prizmkit-code-review` is a bounded Main-Agent loop. The Main Agent:

1. reviews the complete current change;
2. adjudicates concrete findings;
3. directly repairs accepted findings;
4. runs targeted repair verification;
5. repeats until `PASS` or `NEEDS_FIXES`.

Full testing comes after review so the final test evidence corresponds to the final reviewed workspace.

### Test

`prizmkit-test` validates the final reviewed change with project-native tools and auditable evidence. Its valid outcomes are:

- `TEST_PASS` — required scope-appropriate verification succeeded;
- `TEST_FAIL` — reliable evidence demonstrates an implementation or resolved-contract failure;
- `TEST_BLOCKED` — environment, scope, evidence, or reliability prevents a trustworthy verdict.

Documentation-only or formatting-only requirements still execute deterministic lightweight verification and return `TEST_PASS` when successful.

### Retrospective

`prizmkit-retrospective` examines the final reviewed and tested change. It either:

- updates durable Prizm documentation; or
- records `NO_DOC_CHANGE` with a reason.

Both are successful completion of the mandatory retrospective stage. First-time documentation setup and out-of-band repair belong to `prizmkit-prizm-docs` instead.

### Committer

`prizmkit-committer` verifies all prior gates for the same requirement, previews the intended commit, obtains confirmation, stages safely, creates a Conventional Commit, and verifies it. It does not automatically push.

## Repair Routing

Repairs return through only the gates invalidated by the change:

```text
REVIEW_NEEDS_FIXES
  → implement
  → code-review

TEST_FAIL affecting only tests, fixtures, or test-runner configuration
  → implement
  → test

TEST_FAIL affecting production code, runtime configuration, schema,
dependencies, or public interfaces
  → implement
  → code-review
  → test

TEST_BLOCKED
  → pause without speculative production edits
  → resume from test when the environment is available
```

The outer lifecycle allows at most three automatic repair rounds. The internal code-review loop has its own bounded review-round policy. When a limit or external blocker prevents completion, the workflow stops with evidence and a deterministic resume entry instead of claiming success.

## Automatic Handoff and Manual Fallback

PrizmKit defines semantic handoffs, not a platform-specific orchestration API:

```text
stage completes
  → persist truthful state
  → request the next semantic skill
```

- If the host supports skill-to-skill invocation, the lifecycle can continue automatically from `prizmkit-plan`.
- If it does not, the current stage reports exactly one next skill and persists the resume context.

A host without automatic handoff can still complete the same lifecycle by invoking the reported next skill.

## Workflow State

An active requirement may create:

```text
.prizmkit/state/workflows/<requirement-slug>.json
```

The file records the current stage, terminal status, repair round, repair scope, next stage, and resume entry. It is only a workflow index:

| Information | Authority |
|---|---|
| Goals and acceptance criteria | `spec.md` |
| Tasks and completion | `plan.md` |
| Review findings and result | `review-report.md` |
| Test result and executions | Test evidence package |
| Durable architecture knowledge | `.prizmkit/prizm-docs/` |
| Current stage and resume entry | Workflow state |

See [WORKFLOW-STATE.md](WORKFLOW-STATE.md) for the protocol.

PrizmKit does not prescribe whether a target project commits, ignores, or shares generated `.prizmkit/` state.

## Independent Skills

### `prizmkit-workflow`

Provides the one-entry experience for a formal requirement. It coordinates the six existing lifecycle skills, preserves one `artifact_dir`, applies the review/test repair routes, pauses for environment blockers, and reaches commit confirmation. It is still an L1 interactive orchestrator, not an L2 batch pipeline runtime.

### `prizmkit`

Explains the framework and routes users to the correct skill. It does not coordinate or execute the formal lifecycle itself.

### `prizmkit-init`

Provides recommended first-time project initialization. It is a soft prerequisite and may be skipped.

### `prizmkit-prizm-docs`

Initializes, validates, migrates, repairs, or rebuilds Prizm documentation. It is not an extra stage inside every formal requirement.

### `prizmkit-deploy`

Provides a separate deployment and operations entry point. Deployment support varies by target and remains subject to host permissions, credentials, and infrastructure availability.

## Platform Compatibility

Compatibility has three distinct levels:

| Level | Meaning |
|---|---|
| Installable | The host can install and expose standard Agent Skills. |
| Resumable | The host can persist generated project artifacts and users can invoke the deterministic next skill. |
| Automatic handoff | The host can semantically invoke the next installed skill in the current lifecycle. |

The protocol is platform-neutral. Platform names and command forms are examples, not protocol identifiers or allowlists.

## Scope and Non-Goals

The first open-source release does **not** include or require:

- `app-planner` or another L2 planner;
- feature, bug, or refactor batch lists;
- pipeline launchers or the autonomous pipeline runtime;
- multi-requirement queueing, scheduling, or parallel orchestration;
- universal automatic handoff on every host;
- identical deployment automation for every target;
- automatic remote push, package publishing, or version management;
- permissions beyond the host's sandbox, tools, credentials, and environment.

`app-planner` may become an optional future extension for deeper greenfield product and architecture planning. It is not a hidden dependency of the L1 lifecycle.

## Repository Layout

```text
PrizmKit-OpenSource/
├── README.md
├── README.zh-CN.md
├── WORKFLOW-STATE.md
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
├── scripts/
└── <skill-name>/
    ├── SKILL.md
    ├── assets/
    ├── references/
    ├── scripts/
    └── tests/
```

Individual skill directories include only the assets they need.

## Security

Skills are instructions executed under the host's permission and safety model. They do not bypass approval requirements, sandboxes, secrets policy, or infrastructure authorization.

Report suspected security issues through the private process in [SECURITY.md](SECURITY.md). Do not publish secrets or exploitable details in a public issue.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for lifecycle invariants, validation, testing, and pull-request expectations. Community participation follows [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

PrizmKit is available under the [MIT License](LICENSE).
