# Changelog

All notable user-facing changes to PrizmKit will be documented in this file.

The project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and intends to use [Semantic Versioning](https://semver.org/spec/v2.0.0.html) for published releases.

## Unreleased

### Added

- Initial independent open-source L1 Agent Skills package.
- Formal requirement lifecycle: plan, implement, Main-Agent code review, test, retrospective, and confirmed commit.
- Workflow-state protocol for automatic handoff, deterministic manual fallback, repair routing, and recovery.
- English and Simplified Chinese user documentation.
- Independent project initialization, Prizm documentation management, and deployment entry points.

### Changed

- Formal requirements now execute every lifecycle stage in a fixed order.
- Full testing runs after the Main-Agent code-review repair loop so evidence describes the final reviewed workspace.
- Test failures route repairs according to whether they affect production or test infrastructure.

### Security

- Local commits require an explicit preview and user confirmation.
- Remote push remains a separate explicit action.
