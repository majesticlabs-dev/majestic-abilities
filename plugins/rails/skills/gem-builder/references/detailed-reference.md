# Gem Builder Detailed Reference

## Testing Setup

```ruby
# test/test_helper.rb
$LOAD_PATH.unshift File.expand_path("../lib", __dir__)
require "my_gem"
require "minitest/autorun"
require "webmock/minitest"

module TestConfig
  def setup_config
    WebMock.reset!
    MyGem.reset_configuration!
    MyGem.configure { |c| c.api_key = "test-key" }
  end

  def teardown_config
    WebMock.reset!
    MyGem.reset_configuration!
  end
end
```

```ruby
class ClientTest < Minitest::Test
  include TestConfig
  def setup = setup_config
  def teardown = teardown_config

  def test_requires_api_key
    MyGem.config.api_key = nil
    assert_raises(ArgumentError) { MyGem::Client.new }
  end
end
```

## Documentation

### YARD Setup (`.yardopts`)

```
--markup markdown
--no-private
lib/**/*.rb
- README.md
```

### README Sections

Installation, Quick Start, Configuration, Features, Development, License.

### CHANGELOG (Keep a Changelog)

```markdown
## [1.0.0] - 2025-01-15
### Added
- Initial release
```

## Build & Release

### Rakefile

```ruby
require "bundler/gem_tasks"
require "minitest/test_task"
Minitest::TestSubtask.create

require "rubocop/rake_task"
RuboCop::RakeSubtask.new

task default: %i[test rubocop]
```

### Release Workflow

```bash
# 1. Update lib/my_gem/version.rb
# 2. Update CHANGELOG.md
# 3. Commit and release
git commit -am "Release v1.0.0"
bundle exec rake release
```

## Anti-Patterns

| Avoid | Instead |
|-------|---------|
| `method_missing` | `define_method` |
| `@@class_variables` | `class << self` with ivars |
| Requiring Rails directly | `ActiveSupport.on_load` |
| Many runtime deps | Prefer stdlib |
| Committing Gemfile.lock | Only lock in apps |
| Heavy DSLs | Explicit Ruby |
| `autoload` | `require_relative` |

## Best Practices Checklist

**Structure:**
- [ ] Standard directory layout
- [ ] Version in single location
- [ ] Frozen string literals

**Gemspec:**
- [ ] All metadata populated
- [ ] `rubygems_mfa_required` = true
- [ ] Minimal runtime deps

**Configuration:**
- [ ] Environment variable fallbacks
- [ ] Block-based DSL
- [ ] Test-friendly reset method

**Error Handling:**
- [ ] Custom hierarchy
- [ ] Descriptive messages
- [ ] Status/body preserved

**Testing:**
- [ ] Isolation between tests
- [ ] WebMock for HTTP
- [ ] Success and failure cases

**Documentation:**
- [ ] YARD on public methods
- [ ] README with quick start
- [ ] CHANGELOG

**Rails (if applicable):**
- [ ] Optional with `if defined?(Rails)`
- [ ] Isolated namespace
- [ ] `ActiveSupport.on_load` hooks

## References

- `templates.md` - Copy-paste templates (CI, gemspec, README)
- `advanced-patterns.md` - Database adapters, multi-version testing
- `engine-migrations.md` - Keep migrations in Rails engines
