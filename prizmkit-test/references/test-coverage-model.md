# Test Coverage Model

## Purpose

Use this model to determine whether project-native tests adequately prove the complete affected business module and its concrete Regression Ring. It is a semantic working model and report input, not a persisted state machine or machine-attested evidence package.

## Outside-In Scope

Start with behavior observable by a user, caller, consumer, or external contract. Trace each behavior inward:

```text
business capability or acceptance criterion
├── public entry point
├── business rules and invariants
├── state transitions and side effects
├── critical low-level logic
├── dependency and external contracts
└── callers, consumers, shared contracts, and shared state
```

Changed lines locate possible impact. They do not define completeness.

## Affected Business Module

Prefer an explicit project module. If none exists, derive one cohesive boundary from files that jointly implement one observable responsibility.

Primary Scope includes every discoverable observable behavior in that module, including relevant pre-existing behavior whose tests are incomplete. Do not expand into unrelated modules merely to increase coverage.

## Regression Ring

Include only evidenced coupling:

- direct callers;
- consumers of return values, errors, events, files, or ordering;
- shared schemas, types, protocols, generated artifacts, and adapters;
- persistence, cache, lock, queue, transaction, or other shared state;
- registrations, configuration, or runtime discovery that concretely connects behavior.

Record dynamic or unprovable coupling as a remaining edge. An edge that can change the testing verdict prevents `TEST_PASS` until resolved.

## Truth Precedence

Resolve expected behavior in this order:

1. confirmed specification;
2. machine-readable contract;
3. acceptance criteria;
4. trusted existing tests;
5. callers and consumers;
6. current implementation.

Do not encode a possible implementation defect as expected behavior. Conflicting higher-precedence truth that cannot be resolved produces `TEST_BLOCKED`.

## Behavior Inventory

For each observable behavior, capture enough working context to answer:

| Concern | Questions |
|---|---|
| Preconditions | Which identity, state, configuration, or dependency state is required? |
| Inputs | Which valid, minimal, complex, empty, null, malformed, type, and format classes matter? |
| Boundaries | What happens before, at, and after exact contract limits or transitions? |
| Outputs | Which values, errors, response shapes, ordering, and identifiers are observable? |
| Side effects | Which writes, calls, events, files, messages, counts, ordering, or absences are required? |
| State | What are the valid and invalid transitions, retry behavior, and repeated-call outcomes? |
| Dependencies | Which success, empty, malformed, timeout, rate-limit, and failure responses matter? |
| Consumers | Which return shapes, errors, events, ordering, shared contracts, and invocation assumptions must remain stable? |

Working notes may be lightweight. The final report summarizes the model; no JSON matrix, IDs, hashes, or attestation records are required.

## Risk Dimensions

Assess every dimension for every behavior. A dimension can be inapplicable, but the report must give a concise behavior-specific reason when omission would otherwise be surprising.

### Functional

Cover normal, minimal, and complex valid inputs and every contract-relevant observable branch.

### Boundary

Cover empty/null, exact minimum and maximum, before/at/after transitions, malformed formats, collection limits, overflow, and truncation where relevant.

### Error

Cover validation, dependency, malformed-response, timeout, cancellation, cleanup, and partial-failure mapping. Assert both the error and the absence of forbidden partial effects.

### State and Side Effects

Cover valid and invalid transitions, retries, repeated calls, writes, events, call counts, ordering, rollback, and cleanup.

### Permission

Apply to identity, role, tenant, ownership, policy, entitlement, secret, or protected-resource behavior. Include missing/invalid identity, wrong owner or tenant, insufficient grants, and default-deny behavior.

### Concurrency

Apply when shared mutable state, locks, optimistic versions, duplicate workers or calls, race-prone caches, or transaction ordering can affect observable results. Use deterministic barriers, fakes, or synchronization; do not rely on timing sleeps.

### Idempotency

Apply to retries, deduplication keys, create/update/delete repetition, webhook or job replay, token rotation, and repeated transitions. Assert result and side-effect count.

### Time

Apply to expiry, schedules, windows, date ranges, TTL, time zones, and clock-sensitive signatures. Control the clock and test exact boundaries plus before and after.

### Dependency

Apply to databases, filesystems, queues, providers, clocks/randomness, cross-module adapters, and network clients. Assert failure mapping, retry bounds, cleanup, and absence of partial effects.

### Consumer

Apply when callers depend on return shape, errors, side effects, ordering, generated assets, shared types, contracts, state, or invocation conventions.

## Layer Selection

Use the lowest layer that proves a property without removing relevant composition.

| Layer | Use For |
|---|---|
| Focused/unit | Critical pure logic, exact boundaries, deterministic errors, fast localization. |
| Module/component | Public module behavior with internal collaborators composed as production uses them. |
| Contract/integration | Shared protocol compatibility or isolated infrastructure that mocks cannot adequately prove. |
| Code-level E2E | User-visible CLI, API, or UI composition when an applicable native harness exists. |
| Affected-module regression | Every required test for the complete affected module. |
| Regression Ring | Concrete callers, consumers, contracts, adapters, and shared state dependencies. |

Not every behavior needs every layer. Record a concise reason for omitted higher layers, such as a pure library having no process or UI boundary.

## Critical Low-Level Logic

Do not require one test per private function. Add a direct focused test when a helper has one or more of these properties:

- nontrivial business rule or algorithm;
- exact boundary or numerical behavior;
- security, permission, data-integrity, time, or concurrency risk;
- many public paths depend on it and failure localization matters;
- public-only tests would require over-mocking or would not reliably exercise the property.

Otherwise prove private logic through stable public behavior to avoid brittle implementation-coupled tests.

## Assertion Quality

A useful test can fail for the intended defect. It should:

- assert observable outcomes rather than merely that code ran;
- verify error type and relevant message or contract fields without overspecifying incidental text;
- assert state and side effects, including forbidden partial effects;
- keep the behavior under test real while isolating irrelevant dependencies;
- use deterministic time, randomness, concurrency, and fixtures;
- provide useful failure diagnostics;
- follow native test organization and naming.

Reject snapshot-only or mock-call-only tests when those assertions do not prove the behavior. Reject a mock that duplicates the implementation or bypasses the composition being tested.

## Existing-Test-First Construction

Before adding tests:

1. Inspect manifests, native commands, runner configuration, and CI conventions.
2. Read existing test assertions rather than relying on names.
3. Reuse project fixtures, fakes, helpers, mock servers, and coverage tooling.
4. Run the smallest relevant existing tests.
5. Add or update tests only for concrete behavior/risk gaps.
6. Add only the smallest native infrastructure needed for a necessary layer.

Never add a second framework when the existing one is adequate. Never delete or weaken a valid test just to make the suite pass.

## Coverage Metrics

Use existing line, branch, or function coverage to locate possibly omitted behavior. Do not:

- use a percentage as the business-completeness verdict;
- force direct tests for irrelevant private lines;
- weaken assertions to increase percentages;
- exclude difficult business behavior merely to improve a metric.

## Completion Review

Coverage is complete enough for `TEST_PASS` only when:

1. every discoverable observable behavior is represented;
2. every applicable risk has a credible project-native test;
3. critical low-level logic has direct focused coverage when justified;
4. selected layers preserve the property being proved;
5. complete affected-module regression passes;
6. Regression Ring verification passes;
7. concrete unresolved coupling no longer affects the verdict;
8. Main-Agent review converges;
9. applicable independent review converges or is strictly downgraded;
10. no mutation follows final review and execution.

Absolute completeness cannot be guaranteed. State remaining informational risks honestly without presenting them as proven behavior.
