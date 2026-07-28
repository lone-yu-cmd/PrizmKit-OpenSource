# Deployment Capability Contract

Use this contract to convert current project and target evidence into semantic deployment capabilities. Capability names are protocol identifiers; product, language, framework, controller, tool, provider, and operating-system names are not.

## Capability Vocabulary

| Capability | Semantic outcome |
|---|---|
| `discover` | Establish project, target, release, configuration, dependency, and health evidence. |
| `connect` | Reach the intended target through an identified, authorized transport or control boundary. |
| `authenticate` | Establish and revalidate the operator identity and authorization needed by later actions. |
| `build` | Transform source into a verified build output using project-native instructions. |
| `package` | Produce or select a transferable/releasable artifact with identity and integrity evidence. |
| `transfer` | Move an artifact or source input across the required boundary without assuming compatibility of dependency directories. |
| `configure` | Apply project-scoped runtime, routing, environment, or target configuration. |
| `migrate` | Apply an analyzed data/schema/state transition. |
| `release` | Create, select, promote, or activate an identifiable release. |
| `start` | Start the project-owned runtime unit. |
| `stop` | Stop the project-owned runtime unit. |
| `restart` | Restart the project-owned runtime unit and verify recovery. |
| `rollback` | Restore a verified prior release/configuration/data state. |
| `status` | Observe current release and runtime state. |
| `health` | Evaluate the configured health boundary. |
| `logs` | Read bounded project-owned operational output. |
| `history` | Read concise local and target-native operation/release evidence. |
| `validate` | Check configuration, prerequisites, authorization, and plan consistency without deployment writes. |
| `diagnose` | Gather bounded project-scoped evidence for a deployment or runtime problem. |
| `takeover` | Discover ownership, coexistence, backup, and rollback boundaries before adopting an existing deployment. |

Select only capabilities applicable to the requested operation, but never omit a prerequisite merely because automation is unavailable.

## Availability

Exactly one value applies to each selected capability:

| Availability | Required basis | Permitted behavior |
|---|---|---|
| `verified` | A maintained recipe plus a complete current evidence fingerprint matching all recipe constraints. | Compile the recipe's actions, still applying current policy, confirmation, and verification. |
| `dynamic` | Current project evidence, actual installed-tool capability, and applicable official documentation agree on a safe action. | Derive explicit actions and pass them through the same policy gate as a verified recipe. |
| `manual` | Automation ends at a user-controlled, credential, approval, UI, physical, or unavailable execution boundary. | State the exact user action, expected postcondition, and revalidation; return `WAITING_USER` when reached. |
| `unsupported` | Required evidence, access, compatible capability, or a safe execution method is absent. | Report the gap and safe alternatives; do not fabricate commands, mark completion, or promise support. |

`verified` describes evidence, not low risk. `dynamic` does not authorize experimentation. `manual` does not mean complete. An operation with a required `unsupported` capability is `BLOCKED` unless the user chooses an in-scope alternative plan.

## Descriptor

Every selected capability descriptor contains all fields below. Empty lists are explicit; no field is omitted.

| Field | Contract |
|---|---|
| `name` | One capability from the vocabulary. |
| `availability` | `verified`, `dynamic`, `manual`, or `unsupported`. |
| `evidence` | Bounded observations with origin, observed fact, observation method, freshness, and relevance. No Secret values. |
| `preconditions` | Conditions that must be true immediately before execution. |
| `inputs` | Non-sensitive values/references bound into the action; Secret references identify an external source, never a value. |
| `effects` | Project, target, data, traffic, cost, credential, and residual-resource effects. |
| `risk` | `read_only`, `reversible_write`, `high_impact`, or `destructive`, with a plain-language reason. |
| `confirmation` | `none`, `complete_plan`, or one or more dedicated confirmation reasons. |
| `execution` | Exact executable plus argument array, target-native action, or human action. No incomplete shell fragment. |
| `verification` | Observable postconditions and whether each is required or optional. |
| `failure_recovery` | Stop condition, safe cleanup, inspection, rollback eligibility, and manual recovery when rollback is absent. |

Execution stays data-shaped where possible: executable and arguments are separate, the working directory is project-relative, and Secret material is injected by the user/target-owned system. Never interpolate an untrusted value into an opaque shell command.

## Evidence Precedence and Conflict

Use the strongest current evidence, in this order:

1. directly observed project-native configuration and target state;
2. real installed-tool version/help/capability/authentication output;
3. official documentation applicable to the observed version and target;
4. the validated optional project declaration;
5. the validated local record and preserved legacy evidence;
6. user-supplied statements, labeled as such.

Lower evidence may identify what to inspect but does not override a current direct observation. On conflict, show the conflicting facts and use the safer state. A conflict affecting identity, effects, authorization, command shape, migration, health, or rollback blocks execution until resolved.

Evidence expires when the target identity, project revision, tool/runtime version, authentication identity, native configuration, health boundary, or release input changes. Re-observe affected descriptors before execution or resume.

## Verified Recipe Gate

A recipe is eligible only when all of these match current evidence:

- project-native build/start/release interface and working directory;
- artifact format and controller/target compatibility;
- installed tool/runtime and relevant feature versions;
- target type, identity, transport, and authorization boundary;
- configuration ownership and actual connection/service ports;
- health boundary and required verification layers;
- rollback mechanism and release identity semantics;
- migration and persistent-data assumptions;
- declared effects and confirmation class.

The recipe records the evidence fingerprint used for the match. Partial matches, inferred defaults, stale versions, or a matching product name are not sufficient. When any required fingerprint field is missing or mismatched, reject the recipe and consider `dynamic`, `manual`, or `unsupported`.

A verified recipe never bypasses confirmation, Secret handling, data analysis, unknown-outcome inspection, or layered verification.

## Dynamic Derivation Gate

A dynamic capability is permitted only when all three evidence sources are present and consistent:

1. **Current project evidence:** native configuration or source establishes the intended command/action and inputs.
2. **Real capability evidence:** the installed tool or reachable target exposes the required function and applicable version; a filename or remembered CLI is insufficient.
3. **Official documentation:** documentation for the observed language/framework/target/tool version supports the exact action and semantics.

Then:

- construct a complete descriptor;
- classify every effect and confirmation boundary;
- use actual ports/endpoints and target identity;
- identify idempotency and unknown-outcome inspection;
- pass the step through the same immutable plan policy as a verified recipe;
- mark any remaining human boundary `manual` rather than hiding it inside a command.

If official documentation cannot be accessed, do not improvise a write. Read-only assessment may continue; the write is `manual` or `unsupported` with the missing evidence stated.

## Availability Transitions

- `manual` → `verified` or `dynamic` only after the user action is complete and its postcondition, identity, and authorization are revalidated.
- `unsupported` → another state only after new evidence is observed; user optimism alone is not evidence.
- `verified` → `dynamic`, `manual`, or `unsupported` whenever its fingerprint no longer matches.
- Any state → blocked execution when preconditions, confirmation, or required verification cannot be established.

Record transition evidence in the operation result, not as an unbounded transcript.

## Capability Dependencies by Intent

These are semantic starting points, not fixed routes:

- `deploy`: always `discover`, `validate`, `release`, and `health`; add connect/authenticate/build/package/transfer/configure/migrate/start/stop/rollback according to evidence and effects.
- `status`, `health`, `logs`, `history`: discover and connect/authenticate only when needed; remain read-only.
- `restart`, `stop`, `rollback`: discover current live/release state first, mutate only the current project's runtime/release, then verify health/live state.
- `validate`, `diagnose`: read-only by default; any repair or invasive probe becomes a separately confirmed mutating plan.
- `takeover`: discover ownership and conflicts, inspect backup/rollback/coexistence boundaries, and require a new plan before any adoption write.
- `resume`: rediscover all evidence referenced by the stored plan before continuing.

Required unavailable dependencies stay visible in the matrix. Do not collapse a partially assessable operation into a generic fallback success.
