---
name: infrastructure-security-review
description: "Review infrastructure as code for exploitable security failures and unsafe operational defaults. Use when auditing state, secrets, identity, network exposure, compute bootstrap, storage, databases, or supply-chain controls before deployment."
---

# Infrastructure Security Review

Review the changed infrastructure in its provider context. Do not treat the absence of AWS-specific resources, DynamoDB locking, or one provider's private-network attribute as a generic vulnerability.

## Workflow

### 1. Establish Scope

Identify:

- changed IaC, configuration-management, and bootstrap files
- providers, backends, and deployment environments
- public entry points and administrative paths
- secret sources and CI identities
- production data stores and backup paths

Review the diff first, then inspect the surrounding resources needed to understand behavior.

### 2. Run Native Validation

Use the tools already configured by the repository:

```sh
tofu fmt -check -recursive
tofu validate
tofu plan -out=tfplan
tofu show tfplan
```

Run configured scanners such as `trivy config`, `checkov`, `tfsec`, or policy tests when present. Do not introduce a scanner merely to claim coverage.

### 3. Review Security Boundaries

#### State

- remote state is access-controlled and encrypted where supported
- locking or equivalent concurrency protection is enabled when the backend supports it
- state, plans, and crash logs are excluded from version control and artifact exposure
- state migrations and imports preserve ownership

#### Secrets and Identity

- no credentials or secret defaults appear in source, plans, logs, or user data
- CI and provider identities use least privilege
- long-lived personal credentials are not used for automation
- secret rotation and revocation paths are explicit

#### Network

- administrative ports are not open to the world
- databases and internal services use private paths where supported
- firewall and security-group rules are narrow, directional, and attributable
- public exposure is intentional and documented

#### Compute and Bootstrap

- root login and password authentication are disabled unless justified
- downloaded scripts and packages have trusted, pinned sources
- bootstrap output does not leak secrets
- patching, monitoring, and recovery ownership are defined

#### Data and Storage

- public access is blocked unless explicitly required
- encryption, retention, backup, and restore behavior match the data classification
- destructive lifecycle settings are reviewed
- production databases have appropriate availability and recovery controls

Load [patterns.md](references/patterns.md) for the compact provider-neutral checklist.

### 4. Validate Findings

For every finding:

1. cite the exact file and line
2. explain the attack or failure path
3. confirm the provider semantics from current documentation
4. distinguish exploitable risk from optional hardening
5. propose the smallest safe remediation

Do not report regex matches as confirmed vulnerabilities without reading the resource context.

## Severity

- **Critical:** direct credential exposure, public sensitive data, or immediately exploitable administrative access
- **High:** practical compromise or major data-loss path requiring limited preconditions
- **Medium:** meaningful defense-in-depth, availability, or recovery gap
- **Low:** hardening improvement with limited present impact

## Report Format

```markdown
# Infrastructure Security Review

## Verdict
PASS | NEEDS CHANGES

## Findings
### [HIGH] Public SSH ingress
- Evidence: `infra/network.tf:42`
- Risk: ...
- Remediation: ...

## Validation
- Commands run: ...
- Provider documentation checked: ...
- Residual risks: ...
```

Return `NEEDS CHANGES` when any confirmed Critical or High finding remains unresolved.
