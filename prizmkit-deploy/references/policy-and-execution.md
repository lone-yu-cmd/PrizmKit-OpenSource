# Deployment Policy and Execution Contract

Use this contract for every deploy or mutating online operation, regardless of whether its capabilities are verified, dynamic, manual, or mixed. It also determines when an apparently read-only request must become a mutating plan.

## Side-Effect Classification

| Class | Examples by effect | Policy |
|---|---|---|
| `read_only` | Project-native file reads, non-mutating capability/version/auth identity probes, status, configured health reads, bounded logs, history, validation, bounded diagnostics | May run directly when proven project-scoped and read-only. Do not update the local record as a side effect. |
| `reversible_write` | Create a release with verified cleanup, start/restart a project unit, update sole local record, apply project-scoped target configuration with verified restore | Show one complete immutable plan and obtain explicit confirmation before any step. |
| `high_impact` | Project/source file change, privileged/global or compatibility-sensitive dependency change, shared infrastructure, traffic/data-affecting change, plan expansion, unknown-outcome replay, no reliable rollback | Obtain the complete-plan confirmation plus a dedicated confirmation at the exact boundary. |
| `destructive` | Irreversible migration, data/resource deletion, overwrite without verified restore, destructive rollback | Obtain a dedicated confirmation identifying exact data/resources and recovery; refuse when impact cannot be bounded. |

A command name, “dry-run” flag, target label, or recipe classification does not prove read-only behavior. Inspect documented effects and actual tool capability.

## Immutable Plan

The complete preview has one `plan_id` and a Secret-free digest over:

- current project root and project/revision evidence;
- target profile, endpoint/connection identity, environment, and actual observed ports;
- requested operation and release/artifact identity;
- all capability descriptors and ordered steps;
- project/user dependencies and installed versions;
- database/data analysis;
- health boundary and verification layers;
- rollback reference or explicit no-rollback state;
- retry ceilings, human checkpoints, cleanup, and residual-resource policy;
- local-record and optional project-file effects.

Do not include Secret values in the digest input or preview. Bind only Secret names and external source references.

Every ordered step contains every field below:

| Field | Required content |
|---|---|
| `capability` | Semantic capability name. |
| `availability` | `verified`, `dynamic`, `manual`, or `unsupported`. |
| `evidence` | Bounded origin/observation/method/freshness facts supporting this exact step. |
| `preconditions` | Rechecked immediately before execution. |
| `inputs` | Non-sensitive values and Secret references, with source and identity. |
| `effects` | Files, runtime units, releases, data, traffic, network, credential, cost, and residual resources affected. |
| `risk` | `read_only`, `reversible_write`, `high_impact`, or `destructive`, plus reason. |
| `confirmation` | `none`, `complete_plan`, and/or exact dedicated reason(s). |
| `execution` | Complete executable/arguments, target-native action, or human action; target and working directory are explicit. |
| `verification` | Required and optional observable postconditions. |
| `failure_handling` | Stop, cleanup, inspection, rollback offer, and manual recovery behavior. |
| `idempotency` | `proven`, `not_idempotent`, or `unknown`, with evidence. |
| `retry` | Maximum attempts, retryable conditions, backoff/stop condition, and no-retry conditions. |
| `unknown_outcome_inspection` | Proven read-only observation that distinguishes applied/not-applied/indeterminate before replay. |

An unsupported required step makes the plan non-executable. A manual step is a human checkpoint and does not disappear from the order.

Confirmation applies only to the exact digest. A changed command, argument, target identity, project revision, release input, effect, risk, dependency, migration, verification boundary, rollback state, or added step creates a new plan and invalidates prior confirmation.

## Confirmation Matrix

| Trigger | Confirmation required | Evidence shown before confirmation |
|---|---|---|
| Proven read-only and project-scoped | `none` | Target and bounded read effects |
| Ordinary reversible writes | `complete_plan` | Entire ordered plan, effects, verification, rollback/cleanup, and digest |
| Create or modify `prizmkit.deploy.json` or another project/source file | `PROJECT_FILE_CHANGE` | Exact complete file preview/diff, path, ownership, and rollback |
| Privileged/global or compatibility-sensitive install/upgrade | `PRIVILEGED_OR_GLOBAL_DEPENDENCY` | Exact dependency/version/source, privilege, compatibility, target scope, effects, and uninstall/restore path |
| Destructive or irreversible data migration | `DESTRUCTIVE_OR_IRREVERSIBLE_MIGRATION` | Exact migration, affected data, reversibility, locks/downtime, backup/restore evidence, and stop point |
| Shared infrastructure or resource | `SHARED_INFRASTRUCTURE` | Exact shared resource, owners/consumers, traffic/cost/blast radius, and restore plan |
| New scope or changed immutable plan | `PLAN_EXPANSION` | Complete replacement plan and change summary; old confirmation is void |
| Possible prior write with unknown outcome | `UNKNOWN_WRITE_REPLAY` | Read-only inspection result, duplicate/replay effects, and exact replay action |
| Deployment without verified rollback | `NO_RELIABLE_ROLLBACK` | Live-state risk, failure effects, residual resources, and manual recovery procedure |

A dedicated confirmation supplements, not replaces, complete-plan confirmation. Capture the user's actual affirmative response and exact plan/reason scope in the active interaction. For interruption recovery, persist only a non-sensitive receipt containing confirmation kind, matching plan digest, and confirmation time; never persist unrelated conversation or Secret values. A request to deploy, initial feature request, silence, elapsed time, earlier approval, or approval of a different digest is not confirmation.

If confirmation is unavailable in a non-interactive run, stop before the action with `WAITING_USER`, persist only confirmed minimal recovery context, and state the exact decision needed.

## Dependencies and Installation

1. Read project-native dependency/runtime declarations and lock/version files.
2. Distinguish project-local, user-local, target-local, global, and privileged dependencies.
3. Inspect actual installed versions and capabilities read-only.
4. Prefer the project's declared package/dependency mechanism and pinned compatibility.
5. Include every install, upgrade, source, version, scope, write, service restart, and restore path in the plan.
6. Obtain `PRIVILEGED_OR_GLOBAL_DEPENDENCY` confirmation for privileged/global or compatibility-sensitive changes.
7. Never silently install, upgrade, replace, remove, or select a guessed/wildcard version.
8. Never transfer a controller-built dependency directory across systems unless project-native evidence explicitly establishes artifact portability and the confirmed package contract includes compatibility/integrity verification. Prefer reproducible target-compatible artifacts or target-native dependency resolution.

A missing tool can make a capability `manual` or `unsupported`; it is not permission to install it.

## Secret, Log, and Diagnostic Policy

- Secret values remain in user/target-owned Secret systems. Plans contain names and source references only.
- Never print or persist credentials in URLs, authorization headers, tokens, keys, cookies, connection strings, environment assignments, command arguments, or raw diagnostic output.
- Before display, redact recognized credential syntax and user-identified sensitive patterns. Omit unnecessary lines rather than retaining masked copies.
- Logs and diagnostics specify project-owned source, purpose, time range and/or line limit, filters, and redaction. Default to the smallest useful bounded window; do not stream indefinitely.
- Do not run broad process, filesystem, network, account, or infrastructure inventory when a project-scoped observation answers the question.
- If redaction cannot be made reliable, do not display or persist the content; provide a manual inspection checkpoint.

## Database and Persistent-Data Gate

Before any migration or data-affecting release step, report:

1. exact migration identity and target data store;
2. forward and reverse operations, or why reverse is impossible;
3. tables/collections/files/queues and estimated data transformation/loss impact;
4. lock level, downtime/online behavior, duration uncertainty, and traffic sequencing;
5. compatibility window between old/new code and old/new schema;
6. backup identity, completion, restore procedure, and restoration verification;
7. expand/contract or other safer alternative when available;
8. stop conditions, unknown-outcome inspection, and recovery owner.

A migration tool reporting success does not prove data correctness. Verify schema/state and application health. Destructive or irreversible migration requires `DESTRUCTIVE_OR_IRREVERSIBLE_MIGRATION` confirmation. Never suppress a target/tool's own safety prompt.

## Network and Shared Infrastructure

Use actual observed connection and service ports. Distinguish controller-side connection endpoints from target-side application/listener endpoints. Do not infer ports from a platform label or fixed recipe.

Any routing, certificate, firewall, load-balancer, domain, shared network, shared storage, shared database, or shared runtime change lists affected consumers and requires `SHARED_INFRASTRUCTURE` confirmation when it can affect another workload. General hardening or unrelated server administration is out of scope.

## Operation Parity

Every intent uses the same capability, planning, confirmation, and verification contracts:

| Operation | Minimum behavior |
|---|---|
| `deploy` | Discover/validate; compile all build/package/transfer/configure/migrate/release/start/health dependencies that evidence requires. |
| `status` | Observe current release/runtime state read-only; report inaccessible layers. |
| `health` | Execute configured health boundary read-only and preserve required/optional distinction. |
| `logs` | Read a bounded redacted project-owned window. |
| `stop` | Observe the current project-owned unit, confirm the stop effects and rollback/start recovery, stop only that unit, and verify the intended offline/live state. |
| `restart` | Observe current unit, confirm reversible write, restart only that unit, verify runtime/health/log layers. |
| `rollback` | Verify rollback reference and current live state, confirm effects, restore, then run full applicable verification. |
| `history` | Read concise bounded local and target-native release evidence without writing event files. |
| `validate` | Check evidence, configuration, capability prerequisites, policy, and rollback without deployment writes. |
| `diagnose` | Gather bounded read-only evidence; compile a new plan before any repair. |
| `takeover` | Discover ownership/conflicts/backups/coexistence; dedicated confirmation applies to shared or non-owned changes. |
| `resume` | Rediscover and compare evidence/digest before continuing; never assume the prior process completed nothing. |
| `cancel` | Stop future actions and perform only already-confirmed safe cleanup; report residual resources. |

## Execution Algorithm

1. Revalidate project, target, authentication identity, current live state, and the step's evidence/preconditions.
2. Verify that complete-plan and applicable dedicated confirmations match the current digest.
3. Report `step N/total`, capability, action class, target boundary, and evidence being sought. Do not promise a universal duration.
4. Execute exactly the planned action. Do not improvise flags, repairs, cleanup, scope, or dependencies.
5. Capture only bounded redacted evidence and determine the immediate command/target result.
6. Run the step verification before advancing.
7. Atomically update the sole local record only at confirmed plan points; validate before and after write.
8. Stop at a human checkpoint, failure, unknown outcome, invalidated plan, cancellation, or terminal verification.

## Retry and Unknown Outcomes

- Automatic retry is permitted only for a proven read-only action or a proven idempotent action under its explicit maximum-attempt and stop-condition policy.
- Retry count is bounded in the immutable plan; never convert a bounded retry into an open loop.
- Authentication denial, invalid input, destructive failure, plan mismatch, failed required verification, and unknown write outcome are not automatic-retry conditions.
- After timeout, disconnect, or lost response during a possible write, run the planned read-only inspection. Classify the effect as applied, not applied, or indeterminate.
- `applied`: verify postconditions; do not replay.
- `not applied`: retry only if idempotency/retry policy allows and confirmation remains valid.
- `indeterminate`: stop with `BLOCKED` or `WAITING_USER`; any replay requires `UNKNOWN_WRITE_REPLAY` confirmation.

## Deterministic Policy Cases

| Case | Required outcome |
|---|---|
| Read-only project status with proven non-mutating probe | Execute directly; no local-record write |
| Ordinary reversible restart | Complete-plan confirmation before write |
| User requested deploy but has not approved compiled plan | `WAITING_USER` |
| Plan gains an unpreviewed configuration write | New plan plus `PLAN_EXPANSION`; no execution |
| Required privileged dependency is missing | Dedicated confirmation or `WAITING_USER`; no silent install |
| Migration is irreversible and impact cannot be bounded | `BLOCKED` |
| Prior write timed out and inspection is indeterminate | No replay; `BLOCKED` or `WAITING_USER` |
| Rollback is absent but exact risk is accepted | Deployment may proceed; retain explicit manual recovery |
| Required health check fails after release command succeeds | `FAILED`; command success is not operation success |
