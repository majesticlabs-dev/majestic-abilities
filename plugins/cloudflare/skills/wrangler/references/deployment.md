## Deployment

### Release Checks

- Use the project's pinned Wrangler version and command runner; do not upgrade solely to deploy.
- Verify the account, target environment, configuration schema, compatibility date, and bindings.
- Run the project tests and deployment dry run. Exercise changed bindings locally where supported.
- Check remote bindings before local validation to avoid unintended production writes.
- Obtain deployment authorization before remote changes.
- Capture the deployed version and inspect logs and affected application behavior.
- If behavior regresses, inspect version history and use a known rollback target instead of redeploying unknown local state.

Report the Wrangler version, environment, bindings changed, checks run, deployed version, and remaining risks.

### Deploy Worker

```bash
# Deploy to production
wrangler deploy

# Deploy specific environment
wrangler deploy --env staging

# Dry run (validate without deploying)
wrangler deploy --dry-run

# Keep dashboard-set variables
wrangler deploy --keep-vars

# Minify code
wrangler deploy --minify
```

### Manage Secrets

> **Security**: Never pass secret values as command arguments or pipe them via `echo`.
> Use the interactive prompt (preferred), pipe from a file, or use `secret bulk`.
> Never output, log, or hardcode secret values in commands.

```bash
# Set secret — interactive prompt (preferred, wrangler will ask for the value securely)
wrangler secret put API_KEY

# Set secret from a file (useful for PEM keys, CI environments)
wrangler secret put PRIVATE_KEY < path/to/private-key.pem

# List secrets
wrangler secret list

# Delete secret
wrangler secret delete API_KEY

# Bulk secrets from JSON file (do not commit this file to version control)
wrangler secret bulk secrets.json
```

### Versions and Rollback

```bash
# List recent versions
wrangler versions list

# View specific version
wrangler versions view <VERSION_ID>

# Rollback to previous version
wrangler rollback

# Rollback to specific version
wrangler rollback <VERSION_ID>
```
