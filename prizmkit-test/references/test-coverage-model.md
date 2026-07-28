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

Record dynamic or unprovable coupling as a remaining edge. An edge that can change the automated testing verdict prevents `TEST_PASS` until resolved; an authoritatively separate manual/external obligation remains visible under its own evidence status.

## Truth Precedence

Resolve expected business behavior from confirmed specifications and acceptance criteria before lower-authority observations. For a producer-consumer boundary, apply the boundary-specific authority in `boundary-contract-and-test-double-guidance.md`:

1. confirmed specification;
2. machine-readable wire contract;
3. traceably generated type, client, server stub, or fixture;
4. provider raw-wire contract evidence or authorized isolated observation;
5. provider implementation, locked SDK behavior, and matching official documentation;
6. trusted existing tests, callers and consumers, consumer-local types/fixtures/mocks, and other current implementation evidence.

Lower-authority material cannot override a higher-authority source or prove a property outside its boundary. Do not encode a possible implementation defect as expected behavior. Conflicting higher-precedence truth that cannot be resolved produces `TEST_BLOCKED`.

## Evidence Obligation and Verdict Relevance

Classify each material acceptance criterion, environment prerequisite, composition proof, and failing diagnostic before selecting layers or assigning verdict impact. The default is `automated-required`.

| Obligation | Authority and Meaning | Verdict Rule |
|---|---|---|
| `automated-required` | The property belongs to the current software-change verdict, including safely constructible local tooling or isolated services needed to prove it. | Missing truth, safe execution, fidelity, or composition evidence prevents `TEST_PASS`. |
| `manual-external-nonblocking` | A confirmed specification, acceptance criterion, or explicit caller decision says physical-device, public-infrastructure, production-account, or human-confirmation evidence may remain pending after the automated software-change verdict. | Record the evidence as unproven and preserve any project-native status such as `MANUAL_VERIFICATION_REQUIRED`; do not treat it as an unresolved testing-domain item. |
| `out-of-scope-diagnostic` | A current-checkout failure has no concrete path, caller, consumer, contract, configuration, dependency, generated-artifact, or shared-state coupling to this change. | It may be informational only after every condition below is proven. |

Difficulty, duration, cost, agent inability, or initial absence of safely constructible local tooling or isolated services cannot downgrade an `automated-required` obligation. A manual/external classification must be explicit at a higher authority and must separate that evidence from software implementation/commit completion; inability to access an environment is not itself authority. Ambiguous authority or verdict relevance remains blocking.

A current-checkout failure is `out-of-scope-diagnostic` only when all of these hold:

1. affected-module and Regression Ring verification pass;
2. every failure is outside changed paths and concrete coupling;
3. the failure reproduces deterministically on the current state;
4. no changed dependency, configuration, generated artifact, or shared contract caused it;
5. no explicit requirement or project rule makes that broad command a completion gate.

Do not claim historical or pre-existing provenance from a historical worktree, second checkout, test overlay, or unsupported baseline comparison. If any relationship is uncertain, keep the failure verdict-capable. These classifications affect only the current automated Test verdict: they never approve release, deployment, public readiness, signing, security review, or physical-device acceptance.

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

For every applicable state-changing user or system workflow, model and test the complete mutation lifecycle:

1. precondition;
2. input or selection;
3. explicit commit point;
4. cancel without side effects before commit;
5. pending and duplicate-action protection;
6. success visibility;
7. failure recovery and absence of partial effects;
8. reload or re-entry, including process restart when relevant;
9. retry, conflict, and idempotency behavior;
10. downstream read or consumption of the committed result.

If the confirmed specification does not establish the commit point or interaction semantics, request clarification or return `TEST_BLOCKED` when the ambiguity affects the verdict. Do not infer the expected workflow from the current implementation.

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

## Layer Selection and Proof Capability

Use the lowest layer that proves a property without removing relevant composition. Classify tests by components actually executed:

| Layer | Use For |
|---|---|
| Focused / Unit Test | Critical pure logic, exact boundaries, deterministic errors, and fast localization; dependencies may be replaced. |
| Module / Component Test | Public module behavior or UI component behavior under supplied dependencies. |
| UI Component Test | Rendering and interaction with provider compatibility explicitly out of scope. |
| Mock Browser Test | Browser workflow with an intercepted or fixture-backed critical boundary; not Full-stack evidence. |
| Consumer Contract Test | Consumer handling against a contract-validated test double. |
| Provider Contract Test | Provider raw wire payload at its serialization boundary. |
| Integration Test | A named module/infrastructure combination with that combination kept real. |
| Full-stack E2E | Complete user path with critical application boundaries not replaced. |
| Affected-module regression | Every required test for the complete affected module. |
| Regression Ring | Concrete callers, consumers, contracts, adapters, and shared state dependencies. |

Browser execution alone does not determine the layer. Every test claim must state the property proved and any property not proven because a test double removes relevant composition.

Not every behavior needs every layer. Record a concise reason for omitted higher layers, such as a pure library having no process or UI boundary. A missing layer blocks `TEST_PASS` when it is needed to preserve an `automated-required` verdict-capable combination; authorized manual/external evidence is reported as unproven rather than relabeled as an executed layer.

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

1. every discoverable `automated-required` observable behavior is represented;
2. every applicable automated-verdict risk has a credible project-native test;
3. critical low-level logic has direct focused coverage when justified;
4. every automated-verdict boundary and test double has contract authority, fidelity proof, removed-composition, proof-limit, and remaining-risk analysis;
5. selected layers preserve the property being proved and composition-preserving evidence covers every automated-verdict removed combination;
6. provider contracts inspect risk-relevant raw wire output;
7. applicable state-changing workflows cover commit, cancellation, failure, re-entry, and repeated-operation semantics;
8. complete affected-module regression passes;
9. Regression Ring verification passes;
10. concrete unresolved coupling no longer affects the verdict and every non-blocking current-checkout failure satisfies the full diagnostic gate;
11. every deferred manual/external obligation has explicit authority, visible unproven status, and no false pass claim;
12. Main-Agent review converges;
13. applicable independent review converges or is strictly downgraded;
14. no mutation follows final review and execution.

Absolute completeness cannot be guaranteed. State remaining informational risks honestly without presenting them as proven behavior.
