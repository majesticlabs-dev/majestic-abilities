---
name: rails-refactorer
description: "Use when refactoring Rails code for conventional, maintainable Ruby."
---

# Rails Refactorer

## Refactoring Approach

### 1. Analyze Before Changing

Preserve observable behavior and supported interfaces. Inspect the affected code, consumers, and existing tests. Expand inspection when shared state or dependencies make the effect uncertain.

### 2. Apply Rails Conventions

**Controllers:**
- Keep controllers thin (orchestration only)
- Use before_action for common setup
- Limit to 7 RESTful actions; create new controllers for custom actions
- Use strong parameters

```ruby
# Before: Custom action
class MessagesController < ApplicationController
  def archive
    @message = Message.find(params[:id])
    @message.update(archived: true)
  end
end

# After: Dedicated controller
class Messages::ArchivesController < ApplicationController
  def create
    @message = Message.find(params[:message_id])
    @message.update(archived: true)
  end
end
```

**Models:**
- Keep business logic in models
- Use concerns for shared behavior
- Use scopes for common queries
- Semantic association naming

```ruby
# Before
belongs_to :user

# After
belongs_to :author, class_name: "User"
```

**Service Objects (when appropriate):**
- Use for complex multi-step operations
- Use for operations spanning multiple models
- Keep them single-purpose

### 3. Keep Abstractions Proportional

Follow project limits where configured. Extract a class or method when it clarifies a responsibility or removes concrete duplication. Do not add parameter objects or facades solely to meet generic size limits.

### 4. Idiomatic Ruby

**Prefer:**
```ruby
# Guard clauses
return unless user.active?

# Semantic methods
items.any?
email.present?

# Symbol to proc
users.map(&:name)

# Hash shorthand (Ruby 3.x)
{ name:, email: }
```

**Avoid:**
```ruby
# Nested conditionals
if user
  if user.active?
    # ...
  end
end

# Manual checks
items.length > 0
email != nil && email != ""
```

### 5. Maintain Test Coverage

Use existing behavior tests to verify the refactor. Add a regression test when coverage does not protect an affected behavior. Do not add tests solely because a method or class was extracted. Fix failures caused by the refactor and rerun affected checks; distinguish pre-existing failures.

## Migration Safety

When refactoring involves migrations, review for production safety, data preservation, and reversibility.

### Safety Tools

**Recommended gems:**

```ruby
# Gemfile
gem "strong_migrations"      # Catches dangerous operations
gem "database_consistency"   # Validates model <-> DB constraints
gem "anchor_migrations"      # DDL lock timeout protection
```

### Reversibility

```ruby
# PROBLEM: Irreversible migration
def change
  remove_column :users, :legacy_id
end

# SOLUTION: Explicit up/down with data preservation
def up
  execute "CREATE TABLE legacy_user_ids AS SELECT id, legacy_id FROM users"
  remove_column :users, :legacy_id
end

def down
  add_column :users, :legacy_id, :integer
  execute "UPDATE users SET legacy_id = (SELECT legacy_id FROM legacy_user_ids WHERE legacy_user_ids.id = users.id)"
end
```

### Safe Column Operations

```ruby
# PROBLEM: Adding NOT NULL locks table
add_column :users, :status, :string, null: false

# SOLUTION: Three-step migration
add_column :users, :status, :string
User.update_all(status: 'active')
change_column_null :users, :status, false
```

### Long-Running Operations

```ruby
# PROBLEM: Locks table during index creation
add_index :orders, :customer_id

# SOLUTION: Concurrent index (PostgreSQL)
disable_ddl_transaction!
add_index :orders, :customer_id, algorithm: :concurrently
```

### Data Loss Scenarios

| Operation | Risk | Safe Alternative |
|-----------|------|------------------|
| Change column type | Truncation | Add new column, migrate, drop old |
| Remove column | Data loss | Archive first, then remove |
| Rename column | App errors | Add + backfill + remove |
| Change precision | Data loss | Expand only, never contract |

### Migration Review Checklist

- [ ] Migration reversible or has explicit down?
- [ ] Data preserved before destructive changes?
- [ ] Long-running ops use `algorithm: :concurrently`?
- [ ] NOT NULL added safely (nullable -> backfill -> constrain)?
- [ ] strong_migrations passing?
- [ ] Lock timeouts configured for DDL?

## Output Format

Finish when the requested refactor preserves behavior and relevant checks pass, or report the concrete blocker. Do not report tests as passing without running them.

After refactoring, provide:

1. **Summary** - What was refactored and why
2. **Changes** - Files modified with key changes
3. **Test Status** - Confirmation tests still pass
4. **Warnings** - Any potential issues or follow-up needed
