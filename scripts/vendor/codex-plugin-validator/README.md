# Vendored Codex plugin validator

These files are copied without functional changes from `openai/codex` commit
`e325e3acd9ab64cd287a2c4d6cd7a7cebb639618`:

- `codex-rs/skills/src/assets/samples/plugin-creator/scripts/validate_plugin.py`
- `codex-rs/skills/src/assets/samples/plugin-creator/scripts/identifier_validation.py`

The upstream project is licensed under Apache-2.0. Its `LICENSE` and `NOTICE`
are retained in this directory. Keeping the validator in this repository makes
`scripts/check-codex-plugins.sh` reproducible without a pre-existing Codex user
installation.
