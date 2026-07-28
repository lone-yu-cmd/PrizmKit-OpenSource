# Real-Resource Test Policy

Local fixtures and side-effect-free contract tests may run without a deployment confirmation. A test crosses the real-resource boundary if it connects to or authenticates against a server, remote target/control plane, real database, credential store, external URL that creates meaningful traffic, or any resource that may create state, traffic, side effects, quota use, or cost.

A “smoke test,” read-only label, sandbox label, free tier, dry-run flag, or non-production name does not bypass this boundary.

## Deterministic Local Tests

These may run normally when they use only local temporary fixtures and no external credentials or network:

- capability availability and evidence-precedence cases;
- immutable plan and confirmation-policy cases;
- operation/command/config schema parity;
- JSON schema closed-shape and terminal-status checks;
- Secret-like fixture redaction and persistence rejection;
- bounded history/log/recovery/minimal-state checks;
- failure injection for command failure, health failure, unknown write, manual checkpoint, rollback absence, and local-record failure;
- canonical source, generated bundle, and isolated temporary Host installation parity.

Use synthetic Secret values that cannot be mistaken for live credentials. Tests must not read the operator's environment, credential files, login state, browser profile, keychain, or target configuration.

## Separate Authorization Preview

Before any real-resource test, present one dedicated preview containing every field:

| Field | Required content |
|---|---|
| `target` | Exact account/project/resource/profile and environment; no Secret values. |
| `connection` | Controller boundary, endpoint reference, and actual connection/service ports. |
| `credentials` | Secret names/source references and identity to be used, never values. |
| `actions` | Exact read/write/authentication/network/database/traffic operations and commands/actions. |
| `effects` | Possible state, traffic, data, quota, billing, notification, audit-log, and rate-limit effects. |
| `duration` | Bounded test window or command timeout; state uncertainty explicitly, never promise a universal completion time. |
| `cleanup` | Exact cleanup actions, ownership, verification, and what remains if cleanup fails. |
| `rollback` | Verified rollback or explicit absence and manual recovery. |
| `logs` | Bounded sources, line/time limits, filters, redaction, and persistence policy. |
| `stop_conditions` | Authentication, cost, traffic, data, health, timeout, and unknown-outcome conditions that stop the test. |

Ask for separate explicit authorization of this exact preview. Approval of a feature, deployment plan, local test suite, or earlier smoke test is not real-resource test authorization. Any changed target, identity, action, effect, duration, cleanup, cost, or scope invalidates authorization.

In a non-interactive session without exact authorization, do not connect. Return `WAITING_USER` with the non-sensitive preview or `BLOCKED` when the target/effects cannot be bounded.

## Execution

When authorized:

1. revalidate target and authentication identity read-only;
2. apply the ordinary deployment policy and all dedicated confirmations in addition to this test authorization;
3. execute only the previewed bounded actions;
4. report progress without a universal duration promise;
5. stop on any previewed condition, plan mismatch, unknown write outcome, credential boundary change, or unexpected cost/traffic/state;
6. run layered verification and bounded redaction;
7. perform only authorized cleanup;
8. verify cleanup independently and report residual resources.

Unknown writes are inspected before replay. A test command exit is not proof that setup, traffic, state, or cleanup succeeded.

## Result and Cleanup Failure

Report the test result separately from cleanup:

- test terminal status and verification layers;
- target and identity actually used;
- effects and traffic/state/cost observed;
- created or modified resources;
- cleanup actions and verification;
- every residual resource and manual cleanup step.

If the test passes but cleanup fails or cannot be verified, do not report an unqualified success. Return `FAILED` for a required cleanup failure or `BLOCKED` for an inaccessible/indeterminate cleanup boundary, and state that resources may remain.

## This Framework Feature's Test Boundary

The deployment Skill's framework contract tests are deterministic local tests only. They must not connect to a server, remote target/control plane, real database, credential boundary, or traffic/state/cost-bearing resource. No real-resource smoke test is implied or pre-authorized by installing or invoking this Skill.
