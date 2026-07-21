# External Contract Mock Guidance

## Purpose

Use traceable contracts to model external services, persistence, filesystems, queues, generated clients, browser-facing backends, and cross-module endpoints without connecting tests to production targets or inventing provider behavior.

Mocks are test tools, not proof of a deployed environment.

## Contract Source Order

Use the highest available source:

1. project-owned OpenAPI, JSON Schema, Protocol Buffers, GraphQL, AsyncAPI, database schema, generated types, SDK interfaces, fixtures, and documentation;
2. vendored or lock-version-matched dependency documentation;
3. public official service documentation obtained through approved read-only web retrieval;
4. observed non-production behavior only when explicitly authorized and safely isolated.

Use the current locked/provider version when behavior differs by version. Record the source path, public URL, document/version identifier, or generated type used in `test-report.md`.

Never invent fields, statuses, error shapes, retry rules, pagination behavior, ordering, or timing guarantees without a traceable source.

## Safe Documentation Retrieval

Public official documentation retrieval may be used only to read the minimum contract material needed for tests.

- Do not send source code, repository-private content, proprietary payloads, secrets, credentials, or user data to a public endpoint.
- Prefer a project-local or vendored source when it is authoritative.
- Distinguish official provider documentation from blogs, examples, forum answers, and third-party tutorials.
- When official sources conflict with the project's pinned generated client or schema, apply the skill's truth precedence and report the conflict.
- If the required contract cannot be established, return `TEST_BLOCKED` when it prevents a safe verdict.

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

## Avoid Over-Mocking

Keep production composition real when that composition is the property under test. Mock at a stable external boundary rather than mocking the method being verified or every internal collaborator.

Reject a double when it:

- repeats the current implementation instead of the external contract;
- bypasses serialization, mapping, retries, or state transitions under test;
- returns impossible provider behavior;
- asserts only that a mock was called without proving the business result;
- silently drifts from the project or official contract.

Use contract/integration or isolated infrastructure tests when a mock cannot preserve the relevant transaction, protocol, or composition property.

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

Project configuration may be reused only when it demonstrably selects a safe isolated test target. If safety cannot be proven, do not connect; report the unexecuted check and return `TEST_BLOCKED` when it is necessary for the verdict.

## Reporting

For every material external contract, record:

- dependency and behavior under test;
- contract source and version when available;
- mock/fake/isolated-service strategy;
- variants exercised;
- production resources used: `no`;
- unresolved fidelity or deployed-environment risk.

Do not claim that a local mock, fake, contract snapshot, container, or isolated service verifies a deployed production environment.
