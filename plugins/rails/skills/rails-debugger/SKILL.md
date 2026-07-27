---
name: rails-debugger
description: Diagnose Rails errors, failing tests, and unexpected behavior by reproducing the issue, tracing the failing code path, and validating the smallest fix.
---

# Rails Debugger

## Debug Workflow

1. Reproduce the failure or state why reproduction is blocked.
2. Read the stack trace and find the first application frame.
3. Inspect the relevant model, controller, job, service, or query path.
4. Check recent changes if the failure is new.
5. Prove the root cause with logs, console inspection, or a focused test.
6. Apply the smallest fix and add or update regression coverage.

## Useful Checks

### Logs And Tests

```bash
tail -100 log/development.log
bundle exec rspec --format documentation
bin/rails test
```

### Database State

```bash
bin/rails db:migrate:status
bin/rails db:schema:dump
```

### Routing And Framework State

```bash
bin/rails routes | grep users
bin/rails routes -c users
```

### Git Context

```bash
git log --oneline -20
git diff HEAD~5 -- app/
```

## Common Rails Failure Patterns

| Error | First suspicion |
|-------|-----------------|
| `NoMethodError` on nil | missing association or guard |
| `RecordNotFound` | bad id, wrong scope, deleted row |
| `RecordInvalid` | validation or callback failure |
| `ParameterMissing` | request shape mismatch |
| `NameError` | constant path, typo, autoload issue |
| `LoadError` | missing file or dependency |

## Output

Return:

1. reproduction status
2. root cause
3. evidence
4. smallest safe fix
5. regression test or verification command
6. prevention note if the issue is likely to recur
