# PrizmKit L1 Open-Source Release Design

## 1. Purpose

This document defines the scope, lifecycle, responsibilities, handoff protocol, release boundary, and acceptance criteria for publishing the PrizmKit L1 Agent Skills as an independent open-source toolkit.

The primary audience is an independent developer who wants to complete one formal software requirement through a structured development lifecycle without requiring PrizmKit L2 orchestration skills or the PrizmKit autonomous pipeline runtime.

## 2. Understanding Summary

- The open-source package contains the L1 skills from `PrizmKit-OpenSource`.
- The core unit of work is one formal software requirement, not an entire product portfolio or batch pipeline.
- The formal requirement lifecycle is `plan -> implement -> code-review -> test -> retrospective -> committer`.
- `prizmkit-init` is a recommended, one-time project initialization skill; it is a soft prerequisite and may be skipped.
- `prizmkit` explains and routes the toolkit; `prizmkit-prizm-docs` manages the documentation system; `prizmkit-deploy` is an independent post-development deployment and operations entry point.
- The first release does not include or require `app-planner`, other L2 planners, pipeline launchers, or the autonomous runtime.
- The package is platform-agnostic at the protocol level. Platforms that support skill-to-skill handoff may continue automatically; other platforms receive a deterministic resume entry.

## 3. Scope

### Included

- Framework introduction and lifecycle navigation.
- Recommended first-time project initialization.
- Formal requirement planning, implementation, Main-Agent code review, testing, retrospective documentation, and confirmed Git commit.
- Persistent workflow state for handoff, recovery, and repair routing.
- Standalone Prizm documentation management.
- Standalone deployment and operations guidance through `prizmkit-deploy`.
- English and Simplified Chinese user-facing release documentation.

### Not Included

- L2 application planning or batch orchestration.
- Multi-requirement scheduling, queueing, parallel execution, or autonomous pipeline management.
- A universal installer or platform-specific runtime inside this skill-only repository.
- Guaranteed automatic handoff on every host platform.
- Uniform deployment automation for every cloud provider or infrastructure target.
- Automatic Git push, release publishing, or package version management.
- Control over whether a target project commits, ignores, or shares generated `.prizmkit/` files.

## 4. Skill Responsibility Map

```text
PrizmKit L1
├── prizmkit/
│   └── Framework introduction, capability map, and lifecycle navigation
│
├── prizmkit-init/
│   └── Recommended one-time project initialization
│
├── Formal requirement lifecycle/
│   ├── prizmkit-plan
│   ├── prizmkit-implement
│   ├── prizmkit-code-review
│   ├── prizmkit-test
│   ├── prizmkit-retrospective
│   └── prizmkit-committer
│
├── prizmkit-prizm-docs/
│   └── Prizm documentation initialization, validation, repair, and rebuild
│
└── prizmkit-deploy/
    └── Independent deployment and operations entry point
```

### `prizmkit`

Introduces the toolkit, explains the lifecycle, distinguishes formal requirements from direct edits, and directs users to the correct skill. It does not execute the requirement lifecycle itself.

### `prizmkit-init`

Runs when a user first enters or takes over a project. It may create project context, configuration, project brief, and Prizm documentation. It is recommended but not a hard dependency of `prizmkit-plan`.

If initialization is absent, `prizmkit-plan` must recommend `prizmkit-init`, explain the benefits, and allow the user to continue by reading the project source and available documentation as fallback context.

### `prizmkit-prizm-docs`

Owns documentation-system operations such as initialization, status, validation, migration, repair, and rebuild. It is an independent documentation skill, not an additional stage in every requirement lifecycle.

### `prizmkit-deploy`

Remains in the same repository but is not part of the six-stage requirement-development gate. Users invoke it separately after development is complete when deployment or operations work is needed.

## 5. Formal Requirement Lifecycle

The standard lifecycle is fixed:

```text
prizmkit-plan
  → prizmkit-implement
  → prizmkit-code-review
  → prizmkit-test
  → prizmkit-retrospective
  → prizmkit-committer
```

All six stages are required for a formal requirement. A stage may select a verification depth appropriate to the change, but it may not be silently omitted.

Direct edits remain available for non-requirement work such as typos, pure formatting, or other explicitly low-risk edits. Direct edits are not presented as the formal requirement lifecycle.

### Stage Contracts

| Stage | Responsibility | Successful handoff |
|---|---|---|
| Plan | Create and review `spec.md` and `plan.md` | `PLAN_READY` → `implement` |
| Implement | Execute all planned tasks and record completion | `IMPLEMENTED` → `code-review` |
| Code review | Main Agent reviews, repairs, verifies, and loops to convergence | `REVIEW_PASS` → `test` |
| Test | Validate the final reviewed implementation with project-native evidence | `TEST_PASS` → `retrospective` |
| Retrospective | Synchronize durable project documentation or explicitly record no documentation change | `RETRO_COMPLETE` → `committer` |
| Committer | Verify all gates, present commit scope and message, obtain confirmation, and commit | `COMMIT_PENDING` → user confirmation → `COMMITTED` |

`prizmkit-test` always executes a verification phase. For documentation-only or formatting-only changes, it performs deterministic lightweight validation and still returns `TEST_PASS` when successful. `TEST_NOT_APPLICABLE` is not a lifecycle terminal state.

## 6. Code Review and Test Ordering

`prizmkit-code-review` is a Main-Agent review loop. It may directly repair accepted findings, run targeted verification, and continue reviewing until it reaches `PASS` or `NEEDS_FIXES`.

The review stage precedes the full test stage because the test evidence must describe the final implementation after review repairs:

```text
implement
  → Main-Agent review and repair loop
  → final review PASS
  → complete test evidence
```

### Review Failure

- The review loop first handles accepted findings internally, within its bounded review-round limit.
- If the review still ends with `NEEDS_FIXES`, the lifecycle records the unresolved result and may return to `implement` for an outer repair round.
- After implementation repair, the flow must re-enter `code-review` before testing.
- If the unresolved result is caused by missing permissions, tools, or environment rather than code, the workflow pauses instead of creating speculative code changes.

## 7. Test Failure Routing

After a review `PASS`, `prizmkit-test` validates the final reviewed workspace.

```text
TEST_PASS
  → retrospective

TEST_FAIL
  ├── only test files, fixtures, or test-runner configuration changed
  │     → implement → test
  │
  └── production code, runtime configuration, schema, dependency,
      or public interface changed
        → implement → code-review → test

TEST_BLOCKED
  → pause without speculative code changes
  → resume from test after the environment is available
```

Any production change made after a review `PASS` must receive another review before it can be tested for final submission. A test-infrastructure-only repair may return directly to testing.

Automatic repair is bounded to three outer repair rounds. The internal Main-Agent code-review loop retains its own bounded review-round policy. After the applicable limit is reached, the workflow returns a blocked state with the current stage, evidence, completed repairs, unresolved causes, and the next resume entry.

## 8. Workflow State

Each active requirement may use a runtime state file at:

```text
.prizmkit/state/workflows/<requirement-slug>.json
```

The state file is created only when the skills are used in a target project. It is not part of this open-source skill repository, and the skills do not prescribe whether the target project commits, ignores, or shares it.

The state file is a handoff and recovery index, not the authority for requirement content.

```json
{
  "schema_version": 1,
  "artifact_dir": ".prizmkit/specs/001-login",
  "stage": "test",
  "status": "TEST_PASS",
  "completed_stages": [
    "plan",
    "implement",
    "code-review",
    "test"
  ],
  "repair_round": 0,
  "repair_scope": null,
  "next_stage": "retrospective",
  "resume_from": "prizmkit-retrospective"
}
```

Authoritative sources remain separated:

| Information | Authority |
|---|---|
| Requirement goals and acceptance criteria | `spec.md` |
| Implementation tasks and completion | `plan.md` |
| Review findings and verdict | `review-report.md` |
| Test execution and evidence | Test evidence package |
| Durable architecture knowledge | `.prizmkit/prizm-docs/` |
| Current lifecycle position and resume entry | Workflow state file |

Every stage must verify that state agrees with the artifacts and current workspace. If state is missing or stale, the skill reconstructs the safest recoverable position from available artifacts and reports the reconstruction instead of treating stale state as success.

## 9. Platform Handoff Strategy

The protocol is platform-independent:

```text
Stage completes
  → update workflow state
  → request the next semantic skill
```

If the host supports skill-to-skill handoff, the lifecycle continues automatically from `prizmkit-plan`. If it does not, the current stage reports one deterministic next skill and the persisted workflow state provides the resume context.

The release must not claim universal automatic orchestration when the host cannot provide it.

## 10. L2 Independence

The first release includes no L2 skill as a hard dependency.

`app-planner` is optional future functionality for deeper greenfield product discovery, architecture decisions, project conventions, and per-layer AI rules. It is not required by `prizmkit-init`, `prizmkit-plan`, or the six-stage requirement lifecycle.

The first release also excludes the L2 feature, bug, and refactor planners and pipeline launchers because they target batch planning and autonomous runtime execution rather than one independent requirement.

## 11. Open-Source Repository Contents

```text
PrizmKit-OpenSource/
├── README.md
├── README.zh-CN.md
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
├── .gitignore
└── skill directories
```

`README.md` is the English normative user guide. `README.zh-CN.md` is the synchronized Simplified Chinese guide.

The README must explain:

1. What PrizmKit is.
2. The responsibility map.
3. Installation with `npx skills add`.
4. Optional first-time initialization.
5. The six-stage formal requirement lifecycle.
6. Automatic handoff and deterministic manual fallback.
7. Review, test-failure, repair, and resume behavior.
8. Generated `.prizmkit/` artifacts and workflow state without prescribing Git policy.
9. Standalone documentation management.
10. Standalone deployment and operations.
11. Platform compatibility and limitations.
12. Security, authorization, contribution, support, and license information.

The package uses the MIT License.

## 12. Release Non-Functional Baseline

### Performance

- No service throughput or latency guarantee; skills are interactive procedures.
- Use progressive context loading and affected-scope verification.
- No L2 batch concurrency or autonomous queue execution in the first release.

### Scale

- Primary target: one developer, one repository, and one active formal requirement.
- Multiple artifacts may exist, but each lifecycle run must preserve one explicit `artifact_dir`.
- Multi-requirement scheduling is out of scope.

### Safety and Privacy

- Do not claim to bypass host permissions, sandboxing, credentials, or environment restrictions.
- Do not automatically push to a remote repository.
- Require user confirmation before creating the local commit.
- Make test sensitivity and mocked-versus-real environment claims visible.

### Reliability

- Use explicit stage outcomes and workflow state.
- Distinguish code failure from environment blocking.
- Bound automatic repair and report resumable blocked states.
- Never allow commit when required lifecycle gates are unresolved.

### Maintenance

- Maintain the English and Chinese README versions together.
- Validate skill references, frontmatter, lifecycle handoffs, and bundled executable tests before release.
- Keep platform-specific names as examples or adapters, not as protocol definitions.

## 13. Release Acceptance Criteria

A release is ready only when all of the following are true:

### Lifecycle Consistency

- All six core skills and both README files describe `plan → implement → code-review → test → retrospective → committer`.
- Formal requirements cannot silently skip a lifecycle stage.
- `init`, `prizmkit`, `prizmkit-prizm-docs`, and `prizmkit-deploy` retain their independent roles.

### Handoff and Recovery

- The normal six-stage success path is documented and validated.
- Review-internal repairs converge before full testing.
- Test-infrastructure-only failures route to `implement → test`.
- Production-affecting test failures route to `implement → code-review → test`.
- Environment blocks pause without speculative code changes.
- Automatic repair stops after three outer rounds.
- Unsupported automatic handoff produces a deterministic resume entry.
- Missing or stale workflow state can be reconstructed from authoritative artifacts.
- Commit confirmation occurs before a local Git commit.

### Package Integrity

- Every skill has valid frontmatter.
- All local `${SKILL_DIR}` references resolve within their owning skill.
- No hidden reference to `app-planner`, other L2 skills, pipeline launchers, or the autonomous runtime exists.
- README skill names match the published directories.
- Bundled Python tests pass.
- Generated bytecode and cache files are excluded from the release repository.

### Documentation Consistency

- `README.md` and `README.zh-CN.md` describe the same lifecycle and boundaries.
- The MIT license is present.
- Contribution, security, and support paths are clear.

## 14. Decision Log

| Decision | Rationale |
|---|---|
| Keep the first release L1-only | Preserves independent use and avoids L2 runtime dependencies. |
| Make `prizmkit-init` a soft prerequisite | Initialization improves context but should not block a user who wants to start from a requirement. |
| Keep `prizmkit` as an introduction and router | Prevents the framework index from becoming an execution coordinator. |
| Keep `prizmkit-prizm-docs` independent | Documentation maintenance is a separate concern from each requirement stage. |
| Keep `prizmkit-deploy` in the repository as an independent entry point | Makes deployment discoverable without redefining it as a requirement gate. |
| Order review before full test | Final test evidence must represent the workspace after Main-Agent review repairs. |
| Keep Main-Agent review repairs | Matches the existing bounded review implementation and avoids splitting review ownership. |
| Re-review production changes after test failure | Prevents final production changes from bypassing review. |
| Allow test-only repairs to return directly to test | Avoids redundant review when production behavior did not change. |
| Use `TEST_PASS` for lightweight validation | Keeps the six-stage protocol complete while allowing scope-appropriate verification. |
| Use a workflow state file | Enables handoff, repair routing, and recovery without adding an L2 coordinator. |
| Keep Git policy user-controlled | Skills run inside user projects and cannot prescribe whether generated state is committed or ignored. |
| Use automatic handoff when supported and deterministic manual fallback otherwise | Preserves platform independence without overstating automation. |
| Use English README plus synchronized Chinese README | Supports international discovery and the current user workflow. |
| Use MIT License | Provides simple commercial and non-commercial reuse with minimal integration friction. |

## 15. Implementation Handoff

The design is ready for implementation. The implementation should first align the six existing `SKILL.md` files and their references with this protocol, then add the repository-level release documentation and release validation checks.
