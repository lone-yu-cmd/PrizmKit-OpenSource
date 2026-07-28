# Boundary Contract and Test Double Guidance

## Purpose

Apply one contract discipline to every serialized or producer-consumer boundary, whether internal or external: browser/backend APIs, cross-module endpoints, persistence, queues, filesystems, caches, generated clients/servers, SDK providers, and any test double that replaces a producer or consumer.

Mocks are test tools, not proof of provider behavior or a deployed environment. Consumer-local types, fixtures, and mocks are expectations, not provider truth. A test cannot prove a property that depends on production composition it replaces. Apply the Test coverage model's evidence-obligation classification before deciding whether that property belongs to the current automated verdict.

## Boundary-Specific Contract Authority

Choose the highest authority that actually defines the property at the tested boundary:

1. confirmed specification;
2. machine-readable wire contract, such as OpenAPI, JSON Schema, Protocol Buffers, GraphQL, or AsyncAPI;
3. type, client, server stub, or fixture that is traceably generated from that contract;
4. provider raw-wire contract test or explicitly authorized isolated provider observation;
5. provider implementation, version-locked SDK behavior, and matching public official service documentation;
6. consumer-local types, existing tests, historical fixtures, and mocks.

Lower-authority material cannot override higher-authority material. A generated artifact must retain traceable provenance. A database schema can define applicable persistence structure and constraints, but a database schema cannot independently prove network serialization. Current provider implementation is evidence, not automatic product truth when it conflicts with a higher-authority contract.

Use the current locked/provider version when behavior differs by version. Record the source path, public URL, document/version identifier, generated provenance, raw-wire test, or isolated observation used in `test-report.md`.

Never invent fields, statuses, error shapes, retry rules, pagination behavior, ordering, or timing guarantees without a traceable source. If authorities conflict and expected behavior cannot be resolved safely, return `TEST_BLOCKED`.

## Safe Documentation Retrieval

Public official service documentation retrieval may be used only to read the minimum contract material needed for tests.

- Do not send source code, repository-private content, proprietary payloads, secrets, credentials, or user data to a public endpoint.
- Prefer a project-local or vendored source when it is authoritative.
- Distinguish official provider documentation from blogs, examples, forum answers, and third-party tutorials.
- When official sources conflict with the project's pinned generated client or schema, apply the skill's truth precedence and report the conflict.
- If the required contract cannot be established, return `TEST_BLOCKED` when it prevents a safe verdict.

## Boundary and Test-Double Inventory

Inventory every test double that crosses or replaces a producer-consumer boundary, including mocks, fakes, fixtures, route interceptions, mock servers, containers, emulators, and isolated services. Record:

| Field | Required Content |
|---|---|
| Producer | Component that creates the value, message, file, state, or response. |
| Consumer | Component that parses, reads, maps, or acts on it. |
| Boundary type | Internal/external API, module, persistence, queue, filesystem, cache, generated client/server, or other boundary. |
| Serialization or protocol | JSON, HTTP, event/message, database encoding, file format, RPC, or other wire form. |
| Contract authority | Boundary-appropriate source and provenance from the authority order. |
| Test Double | Mock, fake, fixture, interception, server, container, emulator, or isolated service. |
| Fidelity proof | Generation, schema validation, shared raw-wire fixture, contract framework, or authorized isolated observation. |
| Composition removed | Serializer, adapter, network, provider, persistence, process, or other production component replaced. |
| Property not proven | Behavior that depends on the removed composition. |
| Composition-preserving test | Contract, integration, or Full-stack path that keeps the verdict-relevant combination real. |
| Remaining risk | Unproven behavior and its effect on the verdict. |

A boundary with no test double still records its authority and the composition-preserving test when that boundary affects the verdict.

## Test-Double Fidelity Proof

A cross-boundary test double is fidelity-proven only when at least one of these applies:

- generated from the authoritative contract with provenance;
- validated against the authoritative schema during tests;
- shared with a provider raw-wire contract test that validates the same fixture;
- captured through an explicitly authorized isolated provider observation with source/version provenance;
- checked by the project's consumer/provider contract framework.

A consumer-authored ideal fixture without one of these proofs may support local UI or logic tests, but it does not count as provider compatibility evidence. Record its proof boundary explicitly.

## Build the Smallest Faithful Double

Use the target project's existing fake, fixture, mock library, mock server, container, or isolated service when adequate. Model only behavior relevant to the affected module, but preserve the contract property being tested.

Applicable variants include:

- normal success;
- empty success;
- minimum, maximum, pagination, cursor, or size boundary;
- malformed or contract-invalid response;
- timeout or cancellation;
- rate limiting or quota rejection;
- authentication or authorization rejection;
- transient service failure;
- permanent service failure;
- partial response or interrupted stream;
- retry, replay, and idempotency behavior;
- transaction, constraint, rollback, or conflict behavior for stateful services.

Do not require every variant mechanically. Select variants from the actual behavior/risk model and explain material omissions.

## Assertions

Assert the application's observable handling of the contract:

- outbound request shape, required headers or metadata, and serialization;
- response mapping, nullability, enum and format handling;
- retry count and retryable versus permanent classification;
- timeout and cancellation propagation;
- pagination and cursor behavior;
- idempotency and side-effect counts;
- state transition, rollback, cleanup, and absence of partial effects;
- consumer-visible error type or result.

A mock-success-only test is insufficient when dependency failure can change observable behavior.

### Provider Raw-Wire Assertions

A Provider Contract Test for an HTTP response, message, event, file, cache value, or other serialized output must inspect the raw wire payload before any provider-owned model rehydrates it. Select risk-relevant assertions for:

- required, optional, omitted, `null`, empty, and zero values;
- field names, scalar types, enums, formats, timestamps, and default/omission behavior;
- status or result code, error envelope, required headers, and metadata;
- exact bytes or encoding when consumers depend on them.

Deserializing output back into the provider's own model is not sufficient because defaults and zero values can conceal missing fields, nullability changes, or serializer-tag drift.

## Avoid Over-Mocking

Keep production composition real when that composition is the property under test. Mock at a stable external boundary rather than mocking the method being verified or every internal collaborator.

Reject a double when it:

- repeats the current implementation instead of the external contract;
- bypasses serialization, mapping, retries, or state transitions under test;
- returns impossible provider behavior;
- asserts only that a mock was called without proving the business result;
- silently drifts from the project or official contract.

Use contract/integration or isolated infrastructure tests when a mock cannot preserve the relevant transaction, protocol, or composition property.

## Test Layer Taxonomy

Classify a test by the production composition it actually executes, not by runner or user-interface presence:

| Layer | Critical Provider Replaced? | Proof Capability |
|---|---:|---|
| Focused / Unit Test | yes | Local logic, boundaries, and deterministic errors. |
| UI Component Test | yes | Component rendering and interaction under supplied data. |
| Mock Browser Test | yes | Browser UI workflow under intercepted or fixture-backed boundaries. |
| Consumer Contract Test | contract-validated double | Consumer handling of the authoritative contract. |
| Provider Contract Test | not applicable | Provider raw wire behavior at its serialization boundary. |
| Integration Test | no for the combination under test | The named modules or infrastructure composed together. |
| Full-stack E2E | no for critical production boundaries | Complete user path across real application layers in safe isolation. |

Browser execution alone does not make a test Full-stack E2E. A browser test that intercepts a critical API is a Mock Browser Test and cannot prove browser/backend compatibility, provider serialization, persistence, or reload behavior.

## Composition-Preserving Verdict Rule

Locate each material risk in the combination where the defect can occur. Preserve that combination for risks involving consumer/provider serialization, UI/API behavior, API/persistence behavior, generated client/server compatibility, queue producer/consumer behavior, filesystem writer/reader behavior, cache producer/consumer behavior, or transaction/lock/retry/recovery state.

Lower layers may diagnose a defect, but they cannot supply verdict evidence for a property that their doubles remove. Before `TEST_PASS`:

1. identify every verdict-capable risk located in removed composition;
2. require a provider contract, consumer contract plus provider raw-wire evidence, composition-preserving integration test, or Full-stack E2E path that proves the property without replacing that composition;
3. verify the preserving test would fail while the target defect exists;
4. record the preserving evidence and remaining risk in the report.

If required composition-preserving verification cannot run in a proven safe isolated environment, return `TEST_BLOCKED`. Required composition means an `automated-required` property under the authority-driven evidence-obligation classification. Difficulty, duration, cost, agent inability, or absent safely constructible local tooling or isolated services cannot downgrade an `automated-required` obligation. Do not substitute a lower-layer green result or relabel a Mock Browser Test as E2E.

An explicitly authorized `manual-external-nonblocking` obligation may remain unexecuted for the current automated software-change verdict, but it stays visible as unproven and cannot be used to claim provider compatibility, deployed behavior, release readiness, or physical acceptance.

## Databases and Stateful Services

Prefer project-provided isolated infrastructure, a faithful local fake, or a disposable service. Derive structure and constraints from schemas, migrations, models, or official protocol contracts.

Any disposable resource must have:

- a unique non-production identity;
- bounded lifetime;
- deterministic setup;
- verified cleanup;
- no dependency on production credentials or data.

Test relevant constraints, transactions, rollback, concurrency, idempotency, and failure mapping. Cleanup failure that undermines reliability produces `TEST_BLOCKED`.

## Production and Data Prohibitions

Never use:

- production credentials or tokens;
- production databases, APIs, queues, object storage, caches, or services;
- real customer or user data;
- a target whose non-production status cannot be established;
- destructive operations against external data.

Project configuration may be reused only when it demonstrably selects a safe isolated test target. If safety cannot be proven, do not connect; report the unexecuted check and return `TEST_BLOCKED` when it is `automated-required`. A confirmed non-verdict manual/external target remains deferred and unproven rather than becoming permission to connect.

## Reporting

For every verdict-relevant boundary or test double, complete the Boundary and Test-Double Inventory fields. Distinguish local/unit, consumer-contract, provider-contract, integration, Mock Browser, and Full-stack evidence. State whether a composition-preserving test exists and whether any missing proof changes the verdict.

Also record:

- the property's `automated-required` or `manual-external-nonblocking` obligation and its authority;
- variants exercised;
- production resources used: `no`;
- unresolved fidelity or deployed-environment risk;
- authorized deferred external or manual evidence as visible unproven status, never as a conditional pass or unresolved testing-domain item.

Do not claim that a local mock, fake, contract snapshot, container, isolated service, or Mock Browser Test verifies composition it replaces or a deployed production environment.

## Generic Composition Example

For a browser reading a provider response:

1. Treat the machine-readable wire contract as the response-shape authority.
2. Add a Provider Contract Test that asserts the raw serialized response, including a risk-relevant omitted or null field.
3. Validate the Consumer Contract Test fixture against the same contract or share the provider-validated fixture.
4. Classify a route-intercepted browser flow as a Mock Browser Test; it proves UI behavior under that fixture but not live browser/provider compatibility.
5. Add a safe integration or Full-stack E2E path that keeps browser mapping, provider serialization, and required persistence real when those components contain the verdict-capable risk.

The field names and protocol vary by project; the authority, fidelity, proof-boundary, and composition reasoning remain the same.
