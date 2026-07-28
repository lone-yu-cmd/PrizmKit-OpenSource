---
name: "prizmkit-deploy"
description: "Capability-driven deployment and online-operations gateway for arbitrary projects and targets. Discovers project-native evidence and real tool capabilities, classifies semantic deployment capabilities as verified, dynamic, manual, or unsupported, then compiles a risk-gated plan or collaborates at human checkpoints. Handles deploy, status, health, bounded logs, restart, rollback, history, validate, diagnose, takeover, and interrupted-session resume without promising unattended automation. If the user says only 'ship it', clarify commit versus deploy first. (project)"
---

# PrizmKit Deploy — Capability-Driven Gateway

`/prizmkit-deploy` assesses and collaborates on deployment and online operations for the current project. It does not route by language, framework, controller, provider, tool, or operating-system name. Those names are evidence only.

**Universal means truthful assessment and collaboration, not guaranteed unattended automation.** A target can require login, MFA, browser approval, a manual action, or a capability the current environment cannot perform.

## Scope

Use this Skill for:

- deploy and release requests;
- status, health, bounded logs, restart, stop, rollback, and history;
- configuration validation, diagnostics, and existing-deployment takeover;
- authentication checkpoints and interruption recovery related to the current deployment.

Do not use it for unrelated application implementation, general server administration, or resources outside the current project and its necessary deployment dependencies. Assume one operator. Make no concurrent-write or locking guarantee.

If the request is only “ship it,” clarify commit versus deployment. In a non-interactive run where that ambiguity cannot be resolved, return `BLOCKED`; never guess.

## Semantic Protocol

The capability vocabulary is:

```text
discover, connect, authenticate, build, package, transfer, configure, migrate,
release, start, stop, restart, rollback, status, health, logs, history, validate,
diagnose, takeover
```

Every applicable capability is `verified`, `dynamic`, `manual`, or `unsupported` and has evidence, preconditions, inputs, effects, risk, confirmation, execution, verification, and failure recovery. Read `${SKILL_DIR}/references/capability-contract.md` before classifying capabilities or deriving a plan.

Operation set:

```text
deploy, status, health, logs, stop, restart, rollback, history, validate,
diagnose, takeover, resume, cancel
```

Authentication, login, MFA, browser approval, and other user actions are checkpoints inside an operation, not target routes.

## Managed Artifact Boundary

Prefer existing project-native deployment configuration. PrizmKit owns at most these two new artifacts:

| Identity | Role | Write rule |
|---|---|---|
| `.prizmkit/deploy/deploy.json` | Sole local non-sensitive deployment record | Validate with `${SKILL_DIR}/references/deploy-record-schema.json` plus the semantic validator; atomically replace only after the applicable plan confirmation |
| `prizmkit.deploy.json` | Optional version-controlled non-sensitive declaration | Create or modify only after showing an exact complete file preview and receiving explicit confirmation; validate with `${SKILL_DIR}/references/deployment-declaration-schema.json` plus the semantic validator |

Do not create a PrizmKit state, config, template, document, script, pending-input file, metadata file, or history file per language, framework, target, capability, phase, release, or event. Do not create local Secret storage. Secret values stay in user- or target-owned Secret systems; the local record and optional declaration store references and presence only.

The optional declaration is advisory evidence. It never proves that a tool is installed, authentication is current, the target is authorized, a command is safe, or deployment is approved.

### Managed Artifact Validation

Before trusting an existing managed artifact or accepting a complete write candidate, require both schema validation and semantic validation:

1. validate the complete object with its matching Draft 2020-12 schema;
2. run `python3 ${SKILL_DIR}/scripts/validate-deploy-artifact.py --kind <record|declaration> <path>` against the exact regular file without following a symlink;
3. require exit zero and exactly `{"valid":true,"errors":[]}` before using managed fields or replacing/confirming the artifact;
4. on failure, retain the original/candidate evidence, report only bounded error codes and JSON paths, and return `BLOCKED` before execution or `FAILED` after a confirmed live write as applicable.

The shipped script is a read-only semantic companion, not a schema replacement. It checks duplicate keys, canonical project-relative paths, profile identity/references, the exact verification-layer set, success consistency, and forbidden sensitive/raw-output field shapes without displaying values. If either validation capability is unavailable, do not guess, drop unknown data, or accept the managed artifact.

### Sole-Record Update Policy

For every confirmed `deploy.json` write:

1. read and validate the existing record without following a symlink or dropping unknown data;
2. build one complete candidate, preserving fields not intentionally changed by the confirmed plan;
3. update `current` only from verified live/release/health/rollback evidence, set the complete `latest_result`, append one concise redacted `history` summary, retain only the newest 50 summaries, and set or clear minimal `recovery` according to the terminal state;
4. reject Secret-like values, raw command output, full logs, duplicate profile identities, and dangling profile references;
5. write the complete candidate to a temporary regular file in the same directory, run its schema and semantic validations, close it, atomically replace the record, then read back and repeat both validations against exact content;
6. if replacement or read-back validation fails, return `FAILED`, report target-live/local-record-stale when applicable, and rediscover target state before any repair.

Trimming the bounded new-record history is part of this disclosed update policy; it never deletes or alters legacy evidence. This atomic replacement contract assumes one operator and makes no concurrent-write claim.

When an existing `.prizmkit/deploy/` directory contains legacy artifacts, read `${SKILL_DIR}/references/legacy-migration.md` before any managed write. Preserve uncertain evidence and stop all legacy write patterns.

## Workflow

### 1. Normalize Intent and Boundary

1. Resolve one operation from the operation set.
2. Bind the current project root and requested target/profile. Reject traversal into unrelated projects or infrastructure.
3. Separate read-only discovery from possible writes.
4. For a real-resource test request, stop ordinary flow and apply `${SKILL_DIR}/references/real-resource-test-policy.md`.
5. If `deploy.json` exists, run its schema and semantic validations before using any field. Unknown schema versions, malformed objects, unsafe paths/references, incomplete terminal evidence, or Secret-like values block managed writes; do not “repair” by dropping unknown data.

No-argument behavior: assess a deploy if target evidence exists; otherwise perform read-only discovery and return `WAITING_USER` with the missing non-secret target decision. A no-argument invocation is not plan confirmation.

### 2. Discover Evidence Read-Only

Read only what is needed:

- project-native manifests, build/release/runtime configuration, health definitions, deployment files, and source references needed to identify commands and ports;
- the sole local record and optional declaration, if present and valid;
- target facts supplied by the user or observed through proven read-only inspection;
- installed-tool version/help/capability output and current authentication identity, using non-mutating probes;
- official documentation for the detected language, framework, target, and tool versions when dynamic derivation is needed.

Record evidence origin, observation, freshness, and whether it was read directly or user-supplied. A filename or target label alone is not proof. Respect actual connection and service ports; never substitute a conventional or fixed port.

Do not expose Secret values discovered in files, command output, environment, URLs, headers, or logs. Retain only a Secret name/reference and presence state.

### 3. Build the Capability Matrix

Use the capability contract to classify every capability required by the operation:

- prefer a verified recipe only when its complete evidence fingerprint still matches;
- otherwise derive a dynamic plan only from current project evidence, real installed-tool capability, and official documentation;
- use `manual` when a human must act, and state the exact action plus revalidation;
- use `unsupported` when evidence or executable capability is absent, and report the gap and safe alternatives.

Dynamic is not a weaker safety mode. Dynamic, verified, and mixed plans pass the same policy and confirmation gates. Never turn guidance copied from memory or an unofficial example into executable evidence.

### 4. Choose Read-Only Execution or Compile a Plan

Read-only, project-scoped discovery, status, health, bounded logs, history, validation, and diagnostics may execute directly when every selected command is proven read-only. Report their evidence without mutating the target or local record.

A diagnostic command that may write, restart, install, repair, rotate, prune, migrate, or change authentication is not read-only and must enter the plan.

For deploy or any mutating operation, read `${SKILL_DIR}/references/policy-and-execution.md` and compile the complete immutable plan. Every step must contain:

```text
capability, availability, evidence, preconditions, inputs, effects, risk,
confirmation, execution, verification, failure_handling, idempotency, retry,
unknown_outcome_inspection
```

Bind the plan to project root, target identity, release input, ordered steps, command arguments/actions, effects, and risk. Show the complete plan before requesting confirmation. A request to deploy is not itself confirmation of the compiled plan; silence, an old approval, or approval of a different plan is not confirmation.

### 5. Apply Confirmation Policy

- **Direct:** proven read-only, project-scoped actions.
- **Complete-plan confirmation:** ordinary reversible writes, including the planned atomic local-record update.
- **Dedicated confirmation:** project/source file creation or modification; privileged/global or compatibility-sensitive install/upgrade; destructive or irreversible migration; shared infrastructure; plan expansion; replay after an unknown write outcome; or deployment without reliable rollback.

A missing rollback mechanism does not automatically block deployment. Continue only after an exact dedicated risk-acceptance confirmation that identifies live-state risk and manual recovery. Store the fact and scope of confirmation, never credentials or unrelated conversation.

Any changed target, command, argument, input, effect, scope, evidence assumption, or risk invalidates confirmation. Compile and preview a new plan.

### 6. Execute with Progress and Human Checkpoints

Execute the confirmed plan in order. Before each step, recheck preconditions and confirmation validity. Report the capability, step state, and bounded evidence; do not promise a universal duration.

- Never silently install, upgrade, overwrite, delete, expand scope, or replay a write.
- Only proven read-only or idempotent operations may use the plan's bounded retry.
- On timeout/disconnect after a possible write, mark the outcome unknown and inspect before replay.
- Analyze every database migration for reversibility, locking/downtime, data impact, backup/restore evidence, sequencing, and recovery conditions.
- Bound logs by time and/or line count and redact before display or persistence.

For login, MFA, browser approval, or manual action:

1. stop before dependent execution;
2. report `WAITING_USER` and the exact non-secret action;
3. store only the plan digest, last proven step, minimal confirmation receipts, pending checkpoint, and bounded observations in `deploy.json` when that write was confirmed;
4. after the user acts, revalidate target identity, authentication/authorization, capability evidence, and the expected postcondition;
5. resume only if the immutable plan still matches; otherwise compile a new plan.

`cancel` stops future steps, performs only already-confirmed safe cleanup, records residual resources, and returns `CANCELLED`.

### 7. Verify, Recover, and Report

Read `${SKILL_DIR}/references/verification-and-recovery.md` before deciding an outcome. Check every applicable layer:

1. command or target-control result;
2. process, service, container, or release state;
3. configured health boundary;
4. external URL;
5. bounded startup logs.

Each layer is `PASSED`, `FAILED`, `INACCESSIBLE`, or `NOT_APPLICABLE`. Inaccessible and inapplicable are not passes. A required failed or inaccessible layer prevents `SUCCEEDED`; command exit alone is never sufficient.

On failure or interruption, observe current state before action. Offer rollback only when the rollback mechanism and target release are verified. Without verified rollback, report live state, residual resources, and manual recovery explicitly.

Terminal status is exactly one of:

```text
SUCCEEDED, FAILED, BLOCKED, WAITING_USER, CANCELLED
```

## Secret and Output Rules

Before display or persistence, redact credentials in URLs, authorization headers, tokens, keys, cookies, connection strings, environment assignments, and user-identified sensitive patterns. Prefer omission over masking when context is unnecessary. Do not persist raw command output or full logs.

The final result includes:

- terminal status and operation;
- target/profile and live state;
- release identity, if established;
- rollback availability;
- every verification layer and evidence boundary;
- residual resources and partial effects;
- local-record update result;
- recovery guidance and relevant next operations.

If the live change succeeded but a required health check or local-record update failed, return `FAILED` and describe the actual live state. Never label partial completion as success.

## Reference Loading

Load only what the current operation needs:

- capability assessment or dynamic derivation → `${SKILL_DIR}/references/capability-contract.md`
- local record read/write → `${SKILL_DIR}/references/deploy-record-schema.json` and `${SKILL_DIR}/scripts/validate-deploy-artifact.py`
- optional declaration preview/write → `${SKILL_DIR}/references/deployment-declaration-schema.json` and `${SKILL_DIR}/scripts/validate-deploy-artifact.py`
- first use with legacy evidence → `${SKILL_DIR}/references/legacy-migration.md`
- any mutating plan → `${SKILL_DIR}/references/policy-and-execution.md`
- verification, failure, rollback, interruption, or resume → `${SKILL_DIR}/references/verification-and-recovery.md`
- any proposed external-resource test → `${SKILL_DIR}/references/real-resource-test-policy.md`
