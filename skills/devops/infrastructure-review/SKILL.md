---
name: infrastructure-review
description: "Review infrastructure changes for correctness, maintainability, simplicity, provider fit, and deployment risk. Use when reviewing or preparing to ship OpenTofu, Ansible, cloud-init, network, compute, storage, or platform configuration changes."
---

# Infrastructure Review

Review evidence, not arbitrary file-count scores. A large infrastructure repository is not automatically overengineered, and a small one is not automatically safe.

## Workflow

### 1. Discover the Infrastructure Surface

Load [discovery.md](references/discovery.md), then identify:

- OpenTofu or Terraform roots and state backends
- Ansible inventories, playbooks, and roles
- cloud-init and bootstrap files
- providers, environments, and deployment tooling
- the exact diff and resources affected

### 2. Run Repository-Native Checks

Prefer commands already documented in the repository. Typical OpenTofu checks are:

```sh
tofu fmt -check -recursive
tofu validate
tofu plan -out=tfplan
tofu show tfplan
```

For Ansible, run the configured syntax, lint, and inventory checks. Do not invent commands that the project cannot reproduce.

### 3. Review Correctness and Provider Fit

Confirm:

- resource relationships and ordering match the intended topology
- imports, moves, and replacements preserve state ownership
- provider-specific behavior is verified against current documentation
- network, DNS, certificate, storage, and database changes have explicit rollout effects
- region, quota, availability, and cost assumptions are visible

Load [provider-checks.md](references/provider-checks.md) for focused platform questions.

### 4. Review Maintainability and Simplicity

Load [quality.md](references/quality.md). Challenge:

- abstraction without demonstrated reuse
- duplicated environment trees that drift
- hidden values and unclear naming
- broad modules or roles with unrelated responsibilities
- imperative scripts replacing declarative resources without a reason

Do not demand flattening when isolation, reuse, ownership, or provider constraints justify structure.

### 5. Review Security Separately

Apply `infrastructure-security-review` when changes affect state, secrets, identity, public exposure, compute bootstrap, databases, or storage.

Security findings are not averaged away by a good maintainability score.

### 6. Review Deployment Safety

Use [verification-checklist.md](references/verification-checklist.md). Confirm:

- the plan was generated from the intended workspace and variable set
- destructive and replacement actions are understood
- backups, rollback, and recovery paths exist where needed
- staged rollout or maintenance-window requirements are explicit
- documentation and runbooks change with operational behavior

## Report Format

```markdown
# Infrastructure Review

## Verdict
APPROVED | NEEDS CHANGES

## Blocking Findings
- [severity] `path:line` - problem, impact, smallest correction

## Non-Blocking Risks
- risk and owner

## Validation
- commands run
- providers and environments reviewed
- plan summary
- unresolved assumptions
```

Use `NEEDS CHANGES` for correctness, security, destructive-change, or unrecoverable rollout blockers. Do not pad the report with praise.
