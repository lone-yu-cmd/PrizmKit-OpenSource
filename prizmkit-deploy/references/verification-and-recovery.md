# Deployment Verification and Recovery Contract

Use this contract after each planned step, after any failure or interruption, and before selecting a terminal status. Verification observes actual state; it does not infer success from a command exit, API acceptance, or user action alone.

## Layered Verification

Evaluate all five layers and record each named layer exactly once:

```text
PASSED, FAILED, INACCESSIBLE, NOT_APPLICABLE
```

| Layer | Evidence | Applicability rule |
|---|---|---|
| `command_or_platform` | Exit/result plus target-native operation identity and completion state, not merely request acceptance | Applicable to every executed automated action; manual-only operations explain `NOT_APPLICABLE`. |
| `runtime_or_release` | Intended process/service/container/release exists, has expected identity/version, and is in the required state | Applicable when the operation creates, starts, stops, restarts, promotes, or rolls back a runtime/release. |
| `configured_health` | Every configured required project health check meets its explicit expectation | Applicable when a health boundary exists; absence is reported and never replaced with an invented endpoint. |
| `external_url` | Intended externally observed endpoint reaches the expected release/behavior through the real traffic path | Applicable when an external URL is configured and accessible from the controller boundary. |
| `startup_logs` | Bounded, redacted project-owned startup window contains no planned fatal condition | Applicable when startup output exists and access is authorized; specify time and/or line bound. |

For every layer store whether it is required and a concise redacted evidence statement. `INACCESSIBLE` and `NOT_APPLICABLE` are not passes. A required layer must be `PASSED` for `SUCCEEDED`; required `FAILED`, `INACCESSIBLE`, or `NOT_APPLICABLE` prevents success. Optional inaccessible or inapplicable layers remain visible in residual risk. Before persisting or trusting the result, validate the complete record with both `${SKILL_DIR}/references/deploy-record-schema.json` and `${SKILL_DIR}/scripts/validate-deploy-artifact.py --kind record` so omitted, duplicate, or contradictory layers fail closed.

A configured required health check failing after an otherwise successful command makes the operation `FAILED`. Do not downgrade it to a warning.

## Evidence Rules

- Re-observe state after the action; do not reuse pre-action evidence as proof of a postcondition.
- Bind release/runtime observations to the intended target profile and release identity.
- Distinguish controller result, target-control-plane result, and target workload state.
- Use actual configured ports/endpoints and target-native identities.
- Bound all output. Persist only concise summaries, never raw command output or full logs.
- Redact Secret-bearing URLs, headers, environment assignments, tokens, keys, cookies, connection strings, and user-identified patterns before display or storage.
- If evidence may be sensitive and reliable redaction is unavailable, mark the layer `INACCESSIBLE` and provide a manual verification action.

## Terminal Status Decision

Exactly one terminal status is returned:

| Status | Required condition |
|---|---|
| `SUCCEEDED` | All planned steps completed, all required applicable verification layers are `PASSED`, no effect remains unknown, and the required sole-record update was verified. |
| `FAILED` | Confirmed execution occurred but a step, required verification layer, rollback attempt, cleanup required for correctness, or required local-record update failed. Report actual live state. |
| `BLOCKED` | Safe continuation cannot be established because capability/evidence/authorization is absent, input conflicts, plan validity changed, an unknown effect remains indeterminate, or destructive impact cannot be bounded. |
| `WAITING_USER` | Execution is safely paused for an exact confirmation, login, MFA, browser approval, manual action, or separately authorized test boundary. Minimal recovery is available when its write was confirmed. |
| `CANCELLED` | The operator cancelled; no further unconfirmed action ran, and confirmed safe cleanup plus residual-resource reporting completed. |

Partial completion is never `SUCCEEDED`. A release can be live while the operation is `FAILED`; say both. A control-plane “accepted,” queued, or zero-exit response is not success until required layers pass.

## Final Result

Return and, when confirmed, persist the complete terminal result defined by `${SKILL_DIR}/references/deploy-record-schema.json` and accepted by the shipped semantic validator:

- terminal status and operation;
- target profile and immutable plan identity;
- start/finish boundary and concise summary;
- observed live state and release identity;
- rollback availability: `VERIFIED`, `UNVERIFIED`, `ABSENT`, `UNKNOWN`, or `NOT_APPLICABLE`;
- every verification layer with required flag, status, and evidence;
- residual releases, processes, artifacts, locks, migrations, traffic state, and other project-owned resources;
- local-record update result;
- exact recovery guidance and relevant next operations.

Report inaccessible or inapplicable layers explicitly. Never fill missing evidence with `PASSED`.

## Failure Handling

At the first failed step or required layer:

1. stop dependent actions and plan expansion;
2. bound and redact the failure evidence;
3. observe current target/release/runtime/data/traffic state read-only;
4. classify every planned write as proven applied, proven not applied, or indeterminate;
5. perform only cleanup already authorized by the immutable plan and safe in the observed state;
6. determine rollback availability from current evidence;
7. select `FAILED`, `BLOCKED`, or `WAITING_USER` truthfully;
8. preserve residual resources needed for diagnosis unless confirmed cleanup says otherwise.

Never automatically replay an indeterminate write. Follow the `unknown_outcome_inspection` step. Only proven read-only or idempotent actions may use bounded retry.

### Failure Before Any Write

If a precondition or capability fails before execution, live state remains unchanged. Return `BLOCKED` when continuation lacks evidence/authorization or `FAILED` when confirmed execution itself failed. Do not create a misleading release/history event file.

### Failure After a Write

State the applied/unknown effects, current live release, health, traffic, data state, residual resources, and whether old/new units coexist. A healthy previous release does not erase a failed candidate operation.

### Failed Health

Required health failure always fails the operation. If traffic/live selection changed, inspect actual live state and apply only a pre-confirmed verified rollback; otherwise stop and offer the verified rollback or manual recovery.

### Local Record Failure

If the live target changed but the required `.prizmkit/deploy/deploy.json` update or read-back validation failed:

- return `FAILED`;
- report that the target may be live and local state is stale;
- preserve the candidate temporary/legacy evidence without overwriting uncertain files;
- require read-only target rediscovery before any later record repair or deployment;
- never replay the deployment to repair the record.

## Rollback

A rollback is `VERIFIED` only when current evidence establishes:

- exact prior release/configuration/data identity;
- required artifacts/state still exist and match the target;
- rollback action and authorization are available;
- compatibility with the current persistent-data state;
- rollback verification and restore-on-rollback-failure behavior.

`UNVERIFIED`, `UNKNOWN`, or `ABSENT` rollback is not offered as an automated safety guarantee.

A rollback may run automatically only when it was explicitly part of the confirmed immutable failure plan and its preconditions still match. Otherwise show the exact rollback plan/effects and obtain confirmation. Rollback itself uses all applicable verification layers. Failed rollback leaves the operation `FAILED` and reports both attempted states.

When rollback is absent, do not block a deploy that received exact `NO_RELIABLE_ROLLBACK` risk acceptance. On failure, provide live-state evidence, residual resources, the earliest safe manual stop point, and a concrete manual recovery procedure. Do not claim the old release can be restored.

## Interruption and Unknown Remote State

A process/session interruption does not reveal whether the target wrote state. On recovery:

1. validate the sole local record with both schema and semantic validation without dropping unknown data;
2. load only `plan_id`, Secret-free plan digest, operation/profile, last proven step, minimal confirmation receipts, pending checkpoint, and bounded observations from `recovery`;
3. rediscover project revision, target identity, authentication identity, tool capability/version, native configuration, actual ports, live/release/runtime/data/traffic state, health boundary, and rollback evidence affected by the plan;
4. recompile the complete candidate plan from current authoritative evidence and compare its Secret-free digest with the stored immutable digest; never reconstruct actions from history summaries;
5. inspect each possibly executed write before replay;
6. continue only from the first unproven step when earlier postconditions are proven and every required confirmation receipt matches the digest; when a receipt is absent or cannot be validated, request fresh confirmation;
7. compile and preview a new plan when identity, command/action, effect, risk, scope, or evidence assumption changed;
8. clear recovery only after a verified terminal result is safely recorded.

Do not reconstruct commands from history summaries. Do not infer “not applied” from a missing client response. Do not claim concurrent session safety; this procedure assumes one operator.

## Human Checkpoint Recovery

For login, MFA, browser approval, confirmation, or another manual action:

- record `WAITING_USER`, exact non-sensitive action, and expected postcondition;
- never store a password, token, challenge, browser cookie, one-time code, approval URL containing credentials, or raw authentication output;
- after the user reports completion, re-run the planned read-only identity/authorization/postcondition probes;
- remain `WAITING_USER` or become `BLOCKED` when revalidation fails;
- resume only when the immutable plan and target identity still match.

The user's “done” is a signal to revalidate, not verification itself.

## Bounded Retry

Retry only when the immutable plan identifies the action as proven read-only or idempotent, the error as transient, the maximum attempts as greater than the current attempt, and the stop condition as unmet. Report each attempt without a duration promise.

Never retry automatically after authentication denial, invalid input, migration uncertainty, destructive failure, required health failure, plan mismatch, or an indeterminate write.

## Deterministic Recovery Cases

| Observed case | Terminal/result behavior |
|---|---|
| Command result passed; required configured health failed | `FAILED`; report actual live state and verified rollback availability |
| External URL required but controller cannot access it | `FAILED` or `BLOCKED` according to whether execution occurred; layer is `INACCESSIBLE`, never `PASSED` |
| Startup logs do not exist for this target | Layer is `NOT_APPLICABLE` with reason |
| Login or browser approval is required | `WAITING_USER`; persist minimal checkpoint only after confirmed record write |
| Possible write timed out; inspection proves applied | Do not replay; continue verification from the proven postcondition |
| Possible write timed out; inspection proves not applied | Retry only within confirmed idempotent policy |
| Possible write timed out; inspection is indeterminate | `BLOCKED` or `WAITING_USER`; replay needs dedicated confirmation |
| Rollback is verified after failed required health | Offer or run only according to confirmed rollback policy, then verify rollback |
| Rollback is absent after partial release | `FAILED` with live state, residual resources, and manual recovery |
| Live release is healthy but sole-record write failed | `FAILED`; state target-live/local-record-stale and rediscover before repair |
