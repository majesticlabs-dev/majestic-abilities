---
name: onepassword-secrets
description: "Load and inject development, infrastructure, and deployment secrets with the 1Password CLI. Use when configuring `op run`, secret references, service accounts, CI credentials, or multi-account automation."
---

# 1Password Secrets

## Core Patterns

### Secret Reference Format

```
op://<vault>/<item>/<field>
```

Examples:
```
op://Development/AWS/access_key_id
op://Production/Database/password
op://Shared/Stripe/secret_key
```

### Item Naming Conventions

Format: `{environment}-{service}` with kebab-case. One item per environment.

| Pattern | Example | Bad Alternative |
|---------|---------|-----------------|
| `{env}-{service}` | `production-rails` | `Production Rails` |
| `{env}-{provider}` | `production-dockerhub` | `API Key` |
| `{env}-{provider}-{resource}` | `production-hetzner-s3` | Mixed env items |

### Field Naming

Use semantic field names that describe the credential type:

| Good | Bad | Why |
|------|-----|-----|
| `access_token` | `value` | Self-documenting |
| `master_key` | `secret` | Specific purpose clear |
| `secret_access_key` | `key` | Matches AWS naming |
| `api_token` | `token` | Distinguishes from other tokens |

Field naming rules:
- Match the provider's terminology when possible (AWS uses `access_key_id`, `secret_access_key`)
- Use snake_case for consistency
- Be specific: `database_password` not just `password` when item has multiple credentials

### Environment File (.op.env)

Create `.op.env` in project root:

```bash
AWS_ACCESS_KEY_ID=op://Infrastructure/AWS/access_key_id
AWS_SECRET_ACCESS_KEY=op://Infrastructure/AWS/secret_access_key
DIGITALOCEAN_TOKEN=op://Infrastructure/DigitalOcean/api_token
DATABASE_URL=op://Production/PostgreSQL/connection_string
STRIPE_SECRET_KEY=op://Production/Stripe/secret_key
```

**Critical:** Add to `.gitignore`:
```gitignore
# 1Password - NEVER commit
.op.env
*.op.env
```

### Running Commands with Secrets

```bash
op run --env-file=.op.env -- terraform plan
op run --env-file=.op.env -- rails server
```

## Integration Patterns

### Makefile Integration

```makefile
OP ?= op
OP_ENV_FILE ?= .op.env

# Prefix for all commands needing secrets
CMD = $(OP) run --env-file=$(OP_ENV_FILE) --

deploy:
	$(CMD) kamal deploy

console:
	$(CMD) rails console

migrate:
	$(CMD) rails db:migrate
```

### Docker Compose

```bash
op run --env-file=.op.env -- docker compose up
```

### Kamal Deployment

```yaml
# config/deploy.yml
env:
  secret:
    - RAILS_MASTER_KEY
    - DATABASE_URL
    - REDIS_URL
```

```bash
# .kamal/secrets
RAILS_MASTER_KEY=$(op read "op://Production/Rails/master_key")
DATABASE_URL=$(op read "op://Production/PostgreSQL/url")
REDIS_URL=$(op read "op://Production/Redis/url")
```

### CI/CD (GitHub Actions)

Before enabling the apply job, a repository administrator **must** configure the `production` GitHub environment with required reviewers and prevent self-review. Store the apply service-account token as an environment secret so it is unavailable before approval. Without those protections, remove the apply job because the workflow would deploy automatically. Reviewers must inspect the completed plan job before approving the environment gate.

Give the plan job a separate read-only cloud identity and read-only 1Password service account. Never expose the apply identity to the unprotected plan job. Treat the saved plan as a sensitive, short-lived artifact because it may contain infrastructure data.

```yaml
# .github/workflows/deploy.yml
name: Deploy infrastructure
on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  plan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: opentofu/setup-opentofu@v1
      - uses: 1password/load-secrets-action@v2
        with:
          export-env: true
        env:
          OP_SERVICE_ACCOUNT_TOKEN: ${{ secrets.OP_PLAN_SERVICE_ACCOUNT_TOKEN }}
          AWS_ACCESS_KEY_ID: op://CI-Plan/AWS/access_key_id
          AWS_SECRET_ACCESS_KEY: op://CI-Plan/AWS/secret_access_key
      - run: tofu init -input=false
      - run: tofu plan -input=false -out=tfplan
      - uses: actions/upload-artifact@v4
        with:
          name: reviewed-tfplan
          path: tfplan
          retention-days: 1

  apply:
    needs: plan
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: opentofu/setup-opentofu@v1
      - uses: actions/download-artifact@v4
        with:
          name: reviewed-tfplan
          path: .
      - uses: 1password/load-secrets-action@v2
        with:
          export-env: true
        env:
          OP_SERVICE_ACCOUNT_TOKEN: ${{ secrets.OP_APPLY_SERVICE_ACCOUNT_TOKEN }}
          AWS_ACCESS_KEY_ID: op://CI-Apply/AWS/access_key_id
          AWS_SECRET_ACCESS_KEY: op://CI-Apply/AWS/secret_access_key
      - run: tofu init -input=false
      - run: tofu apply -input=false tfplan
```

## CLI Commands

### Reading Secrets Without Printing Them

Prefer `op run` for command injection. When a command requires a secret file, create a protected random path before writing and remove it on exit:

```bash
umask 077
key_file="$(mktemp)"
trap 'rm -f "$key_file"' EXIT
op read "op://Vault/TLS/private_key" > "$key_file"
# Pass "$key_file" directly to the command that needs it.
```

### Injecting into Commands

```bash
DATABASE_URL=$(op read "op://Production/DB/url") rails db:migrate
op run --env-file=.op.env -- ./deploy.sh
op run --account my-team --env-file=.op.env -- tofu plan -out=tfplan
```

### Managing Items

```bash
op vault list
op item list --vault Infrastructure
op item get "AWS" --vault Infrastructure
op item create --category login --vault Infrastructure \
  --title "New Service" username=admin --generate-password='letters,digits,symbols,32'
```

## Project Setup

### Initial Configuration

```bash
op signin
op vault list

cat > .op.env << 'EOF'
AWS_ACCESS_KEY_ID=op://Infrastructure/AWS/access_key_id
AWS_SECRET_ACCESS_KEY=op://Infrastructure/AWS/secret_access_key
DATABASE_URL=op://Production/Database/url
REDIS_URL=op://Production/Redis/url
EOF

op run --env-file=.op.env -- sh -c '
  for name in AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY DATABASE_URL REDIS_URL; do
    test -n "$(printenv "$name")" || exit 1
  done
  echo "Secret references resolved"
'
```

### Generated Secret Workflow

Use 1Password's built-in generator so secret values never appear in command arguments or shell history:

```bash
op item create --vault myproject --category password \
  --title "production-rails-master-key" \
  --generate-password='64,letters,digits'

cat > .kamal/secrets << 'EOF'
RAILS_MASTER_KEY=$(op read "op://myproject/production-rails-master-key/password")
EOF

# Later: rotate with the same protected generator
op item edit "production-rails-master-key" --vault myproject \
  --generate-password='64,letters,digits'
```

### Vault Organization

**Single-Vault Approach (Simpler)**

Use one vault with naming conventions for environment separation:

```
Vault: myproject
Items:
  - production-rails
  - production-dockerhub
  - production-hetzner-s3
  - staging-rails
  - staging-dockerhub
  - development-rails
```

**Multi-Vault Approach (Team Scale)** -- use when teams need different access controls:

| Vault | Purpose | Access |
|-------|---------|--------|
| `Infrastructure` | Cloud provider credentials | DevOps team |
| `Production` | Production app secrets | Deploy systems |
| `Staging` | Staging environment | Dev team |
| `Development` | Local dev secrets | Individual devs |

## Security Rules

- Add `.op.env` and `*.op.env` to `.gitignore` -- never commit
- Use service accounts for CI/CD, not personal accounts
- Never pipe `op read` to logs or echo
- Never store session tokens in scripts
- Use variables for vault/item names in automation

## Troubleshooting

```bash
op signin                  # Re-authenticate expired session
op whoami                  # Check current session
op vault list              # Verify vault access
op item list --vault Infrastructure | grep -i aws   # Search for items
op item get "AWS" --vault Infrastructure --format json | jq '.fields[].label'  # Check field names
```

## Multiple Accounts

Always specify account in automation -- never rely on "last signed in":

```bash
op vault list --account acme.1password.com
export OP_ACCOUNT=acme.1password.com
op run --account acme.1password.com --env-file=.op.env -- ./deploy.sh
```

## Multi-Environment Pattern

Use per-environment env files: `.op.env.production`, `.op.env.staging`, `.op.env.development`

```makefile
ENV ?= development
OP_ENV_FILE = .op.env.$(ENV)

deploy:
	op run --env-file=$(OP_ENV_FILE) -- kamal deploy
# Usage: make deploy ENV=production
```

## References

- [references/multiple-accounts.md](references/multiple-accounts.md) - Cross-account workflows and Makefile integration
