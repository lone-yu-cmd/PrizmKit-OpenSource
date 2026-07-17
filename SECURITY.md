# Security Policy

## Supported Versions

Security fixes target the latest published version and the default branch. Older snapshots may not receive fixes.

## Reporting a Vulnerability

Please report suspected vulnerabilities privately to the project maintainers before opening a public issue. Include:

- affected skill and file;
- reproducible steps or input;
- impact and affected host/project boundary;
- suggested mitigation, if known.

Do not include real credentials, private source code, production data, or weaponized exploit details in a public issue.

If no private reporting channel is configured yet, open a minimal issue requesting a security contact without disclosing the vulnerability details.

## Scope

PrizmKit skills execute under the host platform's permissions, tools, credentials, and sandbox. A skill does not bypass those controls. Security reports should distinguish:

- a defect in the published skill instructions or bundled helper scripts;
- unsafe behavior caused by a target project's configuration;
- a host-platform permission or sandbox issue;
- an authorized deployment or infrastructure concern.

## Safe Use

- Review generated commands before executing them against sensitive environments.
- Never provide production credentials to test evidence generation.
- Treat generated evidence and workflow state according to the target project's sensitivity and retention policy.
- Require explicit authorization for production deployment and destructive operations.
