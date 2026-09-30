# Vendored Codex plugin validator

These files are based on `openai/codex` commit
`e325e3acd9ab64cd287a2c4d6cd7a7cebb639618`:

- `codex-rs/skills/src/assets/samples/plugin-creator/scripts/validate_plugin.py`
- `codex-rs/skills/src/assets/samples/plugin-creator/scripts/identifier_validation.py`

The upstream project is licensed under Apache-2.0. Its `LICENSE` and `NOTICE`
are retained in this directory. Keeping the validator in this repository makes
`scripts/check-codex-plugins.sh` reproducible without a pre-existing Codex user
installation.

## Local invocation-policy correction

`validate_plugin.py` has a local correction for this catalog's shared skill format.
It accepts a boolean `disable-model-invocation: true` (or the existing underscore
alias) only when `agents/openai.yaml` also sets
`policy.allow_implicit_invocation: false`. It rejects non-boolean flags,
conflicting aliases, and missing or implicit Codex policy for a manual-only skill.
Existing agent-manifest checks remain in place. The shared frontmatter controls
Claude Code and Pi; it is not treated as a Codex runtime control.

[Codex skill documentation](https://developers.openai.com/codex/skills/)
documents `allow_implicit_invocation: false` as preventing implicit invocation
while retaining explicit invocation. Regression fixtures in
`scripts/test_codex_plugin_validator.py` run as part of the Codex plugin check.
