# Minitest Coder Detailed Reference

## Test Coverage Standards

| Type | Test For |
|------|----------|
| Models | Validations, associations, scopes, callbacks, methods |
| Services | Happy path, sad path, edge cases, external integrations |
| Controllers | Status codes, redirects, parameter handling |
| Jobs | Execution, retry logic, error handling |

### Coverage Example

```ruby
class UserTest < ActiveSupport::TestCase
  # Validations
  test "validates presence of name" do
    user = User.new(email: "test@example.com")
    assert_not user.valid?
    assert_includes user.errors[:name], "can't be blank"
  end

  # Methods
  describe "#full_name" do
    subject { user.full_name }
    let(:user) { User.new(first_name: "Alice", last_name: "Smith") }

    it "returns full name" do
      assert_equal "Alice Smith", subject
    end

    describe "without last name" do
      let(:user) { User.new(first_name: "Alice") }

      it "returns first name only" do
        assert_equal "Alice", subject
      end
    end
  end
end
```

## Advanced Patterns

See [references/advanced-patterns.md](advanced-patterns.md) for production-tested patterns from 37signals.

| Pattern | Problem Solved |
|---------|----------------|
| Current.account fixtures | Multi-tenant URL isolation |
| Assertion-validating helpers | Early failure with clear messages |
| Deterministic UUIDs | Predictable fixture ordering |
| VCR timestamp filtering | Reusable API cassettes |
| Thread-based concurrency | Race condition detection |
| Adapter-aware helpers | SQLite/MySQL compatibility |

## Anti-Patterns

See [references/anti-patterns.md](anti-patterns.md) for detailed examples.

| Anti-Pattern | Why Bad |
|--------------|---------|
| `require 'test_helper'` | Auto-imported |
| >3 nesting levels | Unreadable output |
| `@ivars` instead of `let` | State leakage |
| Missing `subject` | Repetitive code |
| `assert x.include?(y)` | Use `assert_includes` |
| Testing private methods | Implementation coupling |
| Not using fixtures | Slow tests |

## Best Practices Checklist

**Organization**:
- [ ] Files mirror app structure
- [ ] NOT adding `require 'test_helper'`
- [ ] Using fully qualified namespace

**Style Choice**:
- [ ] Traditional for simple tests
- [ ] Spec for complex contexts
- [ ] Max 3 nesting levels

**Test Data**:
- [ ] Using fixtures (not factories)
- [ ] Using `let` for shared data
- [ ] Using `subject` for method under test

**Assertions**:
- [ ] Correct assertion methods
- [ ] Rails helpers (`assert_changes`, `assert_difference`)
- [ ] Testing behavior, not implementation

**Coverage**:
- [ ] Happy path tested
- [ ] Sad path tested
- [ ] Edge cases covered

## When to Choose Style

**Traditional**: Simple validations, straightforward tests, no shared setup

**Spec**: Multiple contexts, lazy evaluation needed, nested scenarios, reusable subject

**Can mix both** in the same file if it improves clarity.
