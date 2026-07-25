---
name: cloudflare-infrastructure
description: "Provision and review Cloudflare infrastructure with OpenTofu. Use when managing zones, DNS records, TLS settings, cache rules, WAF rulesets, load balancers, or scoped infrastructure API tokens."
---

# Cloudflare Infrastructure

Treat Cloudflare provider schemas as fast-moving. Retrieve the current Cloudflare Terraform documentation and inspect the installed provider schema before writing resources. Do not reuse provider v4 resource examples in provider v5 configurations.

Use `cloudflare-workers-deployment` for Wrangler configuration, Worker bindings, and Worker deployment.

## Workflow

### 1. Inspect the Existing Infrastructure

Check:

- `.terraform.lock.hcl` and the configured provider major version
- current state and imported Cloudflare resources
- account and zone boundaries
- whether the repository is migrating from provider v4
- existing DNS, TLS, WAF, cache, and load-balancer ownership

```sh
tofu version
tofu providers
tofu state list | rg '^cloudflare_'
```

If the project uses provider v4, follow Cloudflare's current v4-to-v5 migration guide before changing resource schemas or state addresses.

### 2. Use Scoped Authentication

Prefer a scoped API token over the global API key. Grant only the account and zone permissions required by the resources in the plan.

```sh
export CLOUDFLARE_API_TOKEN="$(op read 'op://Infrastructure/Cloudflare/api_token')"
```

Load [api-token-permissions.md](references/api-token-permissions.md) as a starting checklist, then verify permission names in current Cloudflare documentation.

Never place tokens in `.tf`, `.tfvars`, shell history, plans, or committed environment files.

### 3. Pin and Inspect the Provider

Use a reviewed provider constraint and commit the dependency lockfile:

```hcl
terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 5.0"
    }
  }
}
```

```sh
tofu init -upgrade
tofu providers schema -json > /tmp/cloudflare-provider-schema.json
```

Confirm every resource and attribute against the installed schema. Current provider v5 DNS resources use names such as `cloudflare_dns_record`; old `cloudflare_record` examples are not interchangeable.

### 4. Preserve Existing Resources

Import existing zones, DNS records, rulesets, certificates, and load balancers instead of recreating them. Review the plan for destructive replacement, DNS downtime, certificate changes, and ruleset ordering.

Keep concerns separate enough to review:

- zone and account lookup
- DNS records
- TLS and certificate policy
- WAF and rate limiting
- cache and redirect rulesets
- load balancing and health checks

### 5. Apply Security Defaults Deliberately

- Use `Full (strict)` when the origin presents a valid public or Cloudflare Origin CA certificate.
- Use `Full` only when the origin certificate cannot currently be validated, and document the remediation path.
- Never use Flexible SSL for an authenticated or production origin.
- Scope API tokens by environment and zone.
- Keep administrative origins and bypass rules narrow.
- Treat WAF and cache rule ordering as behavior, not formatting.

### 6. Validate Before Apply

```sh
tofu fmt -check -recursive
tofu validate
tofu plan -out=tfplan
tofu show tfplan
```

Block the apply when the plan unexpectedly deletes records, changes nameservers, weakens TLS, broadens access, or replaces rulesets without preserving ordering.

## Completion Report

Report:

- provider version and migration status
- account and zones affected
- resources created, imported, changed, or replaced
- DNS and TLS behavior changes
- WAF, cache, and load-balancer effects
- validation commands run
- unresolved security, availability, or state risks
