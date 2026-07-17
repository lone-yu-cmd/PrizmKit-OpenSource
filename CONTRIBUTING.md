# Contributing to PrizmKit

Thank you for improving PrizmKit. Contributions should preserve the platform-neutral lifecycle protocol and keep each skill independently understandable.

## Repository Structure

```text
PrizmKit-OpenSource/
├── <skill-name>/
│   ├── SKILL.md
│   ├── assets/
│   ├── references/
│   ├── scripts/
│   └── tests/
├── README.md
├── README.zh-CN.md
├── WORKFLOW-STATE.md
└── scripts/
```

## Lifecycle Invariants

Formal requirements use this fixed order:

```text
plan → implement → code-review → test → retrospective → committer
```

A pull request must not introduce a path that silently skips a formal lifecycle stage.

Additional invariants:

- `prizmkit` is framework introduction and navigation, not an execution coordinator.
- `prizmkit-init` is a recommended soft prerequisite.
- `prizmkit-prizm-docs` is independent documentation management.
- `prizmkit-deploy` is an independent post-development entry point.
- L1 skills must not require L2 planners, launchers, workflows, or the autonomous pipeline runtime.
- Main-Agent code review repairs occur before the full test stage.
- A production-affecting repair after `TEST_FAIL` returns through code review.
- A test-infrastructure-only repair may return directly to testing.
- `TEST_BLOCKED` pauses without speculative production edits.
- Outer automatic repair is limited to three rounds.
- A local commit requires a preview and user confirmation.

## Platform-Neutral Writing

Describe semantic capabilities, execution topology, resource limits, and failure boundaries. Do not use a platform-specific tool, agent, command, or workflow name as a protocol identifier, allowlist, or prohibition list.

Platform names may appear as non-exhaustive examples.

## Skill Changes

1. Edit the owning skill's `SKILL.md`, assets, references, scripts, and tests together.
2. Keep `${SKILL_DIR}` references inside the owning skill directory.
3. Update both README language versions when public behavior changes.
4. Update `WORKFLOW-STATE.md` when stage states, repair routing, or handoff fields change.
5. Add or update tests for executable scripts and lifecycle contracts.
6. Do not commit generated caches or bytecode.

## Validation

Run:

```bash
python3 scripts/validate_release.py
```

Then run the skill-specific Python tests:

```bash
python3 -m unittest discover -s prizmkit-code-review/tests -p 'test_*.py'
```

`prizmkit-test` scripts also have project-specific evidence behavior; validate them through the release validator and any test suite added under that skill.

## Pull Requests

A pull request should include:

- the behavior or documentation problem;
- the proposed semantic change;
- affected skills and handoffs;
- compatibility implications;
- validation commands and results;
- synchronized English and Chinese user documentation when applicable.

Keep changes focused. Do not bundle unrelated skill behavior changes into one pull request.

## Security Reports

Do not disclose vulnerabilities or secrets in a public issue. Follow [SECURITY.md](SECURITY.md).

## License

By contributing, you agree that your contribution is licensed under the repository's MIT License.
