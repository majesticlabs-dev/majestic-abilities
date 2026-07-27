---
name: minitest-coder
description: "Write Minitest tests for Ruby and Rails applications. Use when creating test files, writing test cases, or testing new features. Covers both traditional and spec styles, fixtures, mocking, and Rails integration testing patterns."
---

# Minitest Coder

## Core Philosophy

- **AAA Pattern**: Arrange-Act-Assert structure for clarity
- **Behavior over Implementation**: Test what code does, not how
- **Isolation**: Tests should be independent
- **Descriptive Names**: Clear test descriptions
- **Coverage**: Spend coverage where regressions would hurt, not where framework behavior is already proven
- **Fast Tests**: Minimize database operations
- **Fixtures**: Use fixtures for test data
- **No Test-Induced Design Damage**: Never add production indirection only to make a test easier

## Coverage Budget

- **Heavy**: model tests for domain invariants and controller/integration tests for full request flows, authorization, formats, and state changes.
- **Focused**: system tests for critical happy paths and cross-browser behavior that lower layers cannot prove.
- **Light**: jobs, mailers, broadcasts, and channels unless they contain real branching or security-sensitive behavior.
- **Avoid**: view tests, trivial delegation tests, and tests that only assert Rails framework behavior.

Do not duplicate the same behavior assertion at every layer. Pick the lowest layer that proves the behavior and add an integration test when wiring or authorization matters.

## Minitest Styles

| Style | Best For | Syntax |
|-------|----------|--------|
| Traditional | Simple unit tests | `test "description"` |
| Spec | Complex scenarios with contexts | `describe`/`it` with `let`/`subject` |

### Traditional Style

```ruby
class UserTest < ActiveSupport::TestCase
  test "validates presence of name" do
    user = User.new
    assert_not user.valid?
    assert_includes user.errors[:name], "can't be blank"
  end
end
```

### Spec Style

```ruby
class UserTest < ActiveSupport::TestCase
  describe "#full_name" do
    subject { user.full_name }
    let(:user) { User.new(first_name: "Buffy", last_name:) }

    describe "with last name" do
      let(:last_name) { "Summers" }

      it "returns full name" do
        assert_equal "Buffy Summers", subject
      end
    end
  end
end
```

## Test Organization

### File Structure

- `test/models/` - Model unit tests
- `test/services/` - Service object tests, only when the app has real service objects
- `test/integration/` - Full-stack tests
- `test/mailers/` - Mailer tests
- `test/jobs/` - Background job tests
- `test/fixtures/` - Test data
- `test/test_helper.rb` - Configuration

### Naming Conventions

- Mirror app structure: `app/models/user.rb` → `test/models/user_test.rb`
- Use fully qualified namespace: `class Users::ProfileServiceTest`
- **Don't add** `require 'test_helper'` (auto-imported)

## Spec Style Patterns

See [references/spec-patterns.md](references/spec-patterns.md) for detailed examples.

| Pattern | Use Case |
|---------|----------|
| `subject { ... }` | Method under test |
| `let(:name) { ... }` | Lazy-evaluated data |
| `describe "context"` | Group related tests (max 3 levels) |
| `before { ... }` | Complex setup |

```ruby
describe "#process" do
  subject { processor.process }
  let(:processor) { OrderProcessor.new(order) }
  let(:order) { orders(:paid_order) }

  it "succeeds" do
    assert subject.success?
  end
end
```

## Fixtures

```yaml
# test/fixtures/users.yml
alice:
  name: Alice Smith
  email: alice@example.com
  created_at: <%= 2.days.ago %>
```

```ruby
class UserTest < ActiveSupport::TestCase
  fixtures :users

  test "validates uniqueness" do
    duplicate = User.new(email: users(:alice).email)
    assert_not duplicate.valid?
  end
end
```

## Mocking and Stubbing

See [references/spec-patterns.md](references/spec-patterns.md) for detailed examples.

Stub external boundaries such as network calls, time, payment providers, object storage, and randomness. Avoid mocking internal application methods just to prove a private call happened.

| Method | Purpose |
|--------|---------|
| `Object.stub :method, value` | Stub return value |
| `Minitest::Mock.new` | Verify method calls |

```ruby
test "processes payment" do
  PaymentGateway.stub :charge, true do
    processor = OrderProcessor.new(order)
    assert processor.process
  end
end
```

## Assertions Quick Reference

### Basic Assertions

```ruby
# Boolean
assert user.valid?
assert_not user.admin?

# Equality
assert_equal "Alice", user.name
assert_nil user.deleted_at

# Collections
assert_includes users, admin_user
assert_empty order.items

# Exceptions
assert_raises ActiveRecord::RecordInvalid do
  user.save!
end
```

### Rails Assertions

```ruby
# Changes
assert_changes -> { user.reload.status }, to: "active" do
  user.activate!
end

assert_difference "User.count", 1 do
  User.create(name: "Charlie")
end

# Responses
assert_response :success
assert_redirected_to user_path(user)
```

## AAA Pattern

```ruby
test "processes refund" do
  # Arrange
  order = orders(:completed_order)
  original_balance = order.user.account_balance

  # Act
  result = order.process_refund

  # Assert
  assert result.success?
  assert_equal "refunded", order.reload.status
end
```

**Spec style with subject**:
```ruby
describe "#process_refund" do
  subject { order.process_refund }
  let(:order) { orders(:completed_order) }

  it "updates status" do
    subject
    assert_equal "refunded", order.reload.status
  end

  it "credits user" do
    assert_changes -> { order.user.reload.account_balance }, by: order.total do
      subject
    end
  end
end
```

## Detailed Reference

Load [detailed-reference.md](references/detailed-reference.md) for extended examples, templates, and advanced patterns.
