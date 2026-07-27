---
name: rails-lint
description: "Run and fix Rails code-quality checks across Ruby, ERB, and security tooling. Use before pushing Rails changes, when CI reports RuboCop or ERB Lint violations, or when Brakeman reports security warnings."
---

# Rails Lint

Run the project's configured quality checks, fix violations without changing behavior, and verify the final diff.

## Workflow

### 1. Inspect Project Configuration

Read the files that define the project's actual lint contract before running or changing anything:

- `.rubocop.yml`
- `.rubocop_todo.yml`
- `.erb-lint.yml`
- `Gemfile`
- `bin/ci` or the relevant CI workflow

Use project-provided commands when they differ from the defaults below. Do not replace local conventions with generic style preferences.

### 2. Scope The Check

```bash
# Unstaged changes
git diff --name-only

# Staged changes
git diff --cached --name-only
```

Use focused checks while fixing a small change. Run the full configured checks before declaring success.

### 3. Run Checks

**RuboCop:**

```bash
# Full check
bundle exec rubocop

# Focused file or directory
bundle exec rubocop app/models/user.rb

# Specific cop
bundle exec rubocop --only Style/StringLiterals
```

**ERB Lint:**

```bash
bundle exec erblint --lint-all
```

**Brakeman:**

```bash
bin/brakeman --no-pager
```

If a tool is not configured in the project, report that instead of adding it without approval.

### 4. Apply Corrections

Start with safe automatic corrections:

```bash
bundle exec rubocop -a
bundle exec erblint --lint-all --autocorrect
```

Inspect the resulting diff. Use RuboCop's unsafe correction mode only when every semantic change will be reviewed:

```bash
bundle exec rubocop -A
```

Do not run `-A` by default. Do not mix unrelated formatting changes into the requested work.

### 5. Resolve Remaining Violations

Read the cop documentation before making non-obvious manual changes:

```bash
bundle exec rubocop --show-cops Style/StringLiterals
```

Follow these rules:

- Fix the code when the cop identifies a real issue.
- Respect project configuration when style choices are intentional.
- Use inline disables only for a justified exception, with the narrowest possible scope.
- Do not generate or expand `.rubocop_todo.yml` unless the user explicitly requests a baseline.
- Do not change public behavior merely to satisfy a metric cop.

Common fixes:

| Violation | Preferred response |
| --- | --- |
| `Layout/LineLength` | Break the expression at a readable boundary. |
| `Metrics/MethodLength` | Simplify or extract only when responsibility becomes clearer. |
| `Metrics/AbcSize` | Reduce branching or assignments without hiding logic. |
| `Rails/HasManyOrHasOneDependent` | Choose an explicit lifecycle matching domain behavior. |
| `Rails/InverseOf` | Add the inverse when the association supports it. |
| `Style/FrozenStringLiteralComment` | Add the required file header. |

### 6. Verify

Rerun every applicable check and inspect the final diff:

```bash
bundle exec rubocop
bundle exec erblint --lint-all
bin/brakeman --no-pager
git diff --check
git diff
```

Do not stage or commit automatically.

## Output

Report:

1. Checks run and their results
2. Automatic corrections applied
3. Manual fixes with cop names and file locations
4. Remaining warnings or unavailable tools
5. Final pass or needs-attention verdict
