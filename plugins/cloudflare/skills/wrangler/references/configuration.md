## Worker Configuration

Inspect the project's Wrangler version and configuration schema before editing fields.
Use JSONC for new configuration; preserve a working TOML configuration unless migration is requested.

- Reference the installed Wrangler schema for validation.
- Keep the entry point, compatibility date, and flags consistent with the application.
- Keep binding names stable across configuration and generated types.
- Check each environment for required bindings; do not assume all fields inherit.
- Separate non-secret variables from secrets. Keep local secrets in ignored `.dev.vars` files.
- Generate binding types after configuration changes and check for drift in CI when the project supports it.

Use the project's command runner for `wrangler types` and `wrangler types --check`.
Commit generated types when the project requires them.
