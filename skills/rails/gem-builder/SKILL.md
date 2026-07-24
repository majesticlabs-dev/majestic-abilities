---
name: gem-builder
description: "Build production-quality Ruby gems. Use when creating new gems, structuring gem architecture, implementing configuration patterns, setting up testing, or preparing for publishing. Covers all gem types - libraries, CLI tools, Rails engines, and API clients."
---

# Gem Builder

## Core Philosophy

- **Minimal dependencies**: Only add gems you truly need
- **Single responsibility**: Each class/module does one thing well
- **Semantic versioning**: Follow SemVer strictly (MAJOR.MINOR.PATCH)
- **Test coverage**: Every public method has tests
- **Documentation**: YARD docs, README, and CHANGELOG
- **Fail fast**: Validate inputs early, raise descriptive errors

## Gem Structure

```
my_gem/
├── lib/
│   ├── my_gem.rb              # Main entry point
│   ├── my_gem/
│   │   ├── version.rb         # VERSION constant
│   │   ├── config.rb          # Configuration class
│   │   ├── errors.rb          # Error hierarchy
│   │   └── [feature].rb       # Feature modules
├── test/                      # Test suite
├── my_gem.gemspec             # Gem specification
├── Gemfile                    # Development dependencies
├── Rakefile                   # Build tasks
├── README.md                  # User documentation
├── CHANGELOG.md               # Version history
└── LICENSE.txt                # License file
```

### Main Entry Point

```ruby
# lib/my_gem.rb
require_relative "my_gem/version"
require_relative "my_gem/config"
require_relative "my_gem/errors"

module MyGem
  class << self
    def config
      @config ||= Config.new
    end

    def configure
      yield(config)
    end

    def reset_configuration!
      @config = nil
    end
  end
end
```

## Gemspec Best Practices

```ruby
# my_gem.gemspec
require_relative "lib/my_gem/version"

Gem::Specification.new do |spec|
  spec.name          = "my_gem"
  spec.version       = MyGem::VERSION
  spec.authors       = ["Your Name"]
  spec.email         = ["you@example.com"]
  spec.summary       = "One-line description"
  spec.homepage      = "https://github.com/username/my_gem"
  spec.license       = "MIT"
  spec.required_ruby_version = ">= 3.2.0"

  spec.metadata["rubygems_mfa_required"] = "true"
  spec.metadata["changelog_uri"] = "#{spec.homepage}/blob/main/CHANGELOG.md"

  # Exclude test/CI files
  spec.files = IO.popen(%w[git ls-files -z], chdir: __dir__, err: IO::NULL) do |ls|
    ls.readlines("\x0", chomp: true).reject { |f| f.start_with?(*%w[bin/ test/ .github/]) }
  end
  spec.require_paths = ["lib"]
end
```

## Gem Types

| Type | Key Features |
|------|--------------|
| Library | Pure Ruby, no external services |
| API Client | HTTP wrapper with resource pattern |
| CLI Tool | `spec.executables`, bindir setup |
| Rails Integration | Railtie with `ActiveSupport.on_load` |

### API Client Pattern

```ruby
class Client
  def initialize(api_key: nil)
    @api_key = api_key || MyGem.config.api_key
    raise ArgumentError, "API key required" if @api_key.to_s.empty?
  end

  def users = @users ||= Resources::Users.new(self)
  def posts = @posts ||= Resources::Posts.new(self)
end
```

### Rails Integration

**Never require Rails directly.** Use lazy loading:

```ruby
# lib/my_gem/railtie.rb
class Railtie < Rails::Railtie
  initializer "my_gem.configure" do
    ActiveSupport.on_load(:active_record) do
      extend MyGem::Model
    end
  end
end

# lib/my_gem.rb
require_relative "my_gem/railtie" if defined?(Rails)
```

### Class Macro DSL

The pattern used by `searchkick`, `lockbox`:

```ruby
# Usage: mygemname word_start: [:name]
module Model
  def mygemname(**options)
    unknown = options.keys - KNOWN_OPTIONS
    raise ArgumentError, "Unknown: #{unknown.join(", ")}" if unknown.any?

    mod = Module.new
    mod.module_eval { define_method(:some_method) { options[:key] } }
    include mod
    class_variable_set(:@@mygemname_options, options.dup)
  end
end
```

## Configuration Pattern

```ruby
# lib/my_gem/config.rb
class Config
  attr_accessor :api_key, :base_url, :timeout
  attr_writer :logger

  def initialize
    @api_key = ENV.fetch("MY_GEM_API_KEY", nil)
    @base_url = ENV.fetch("MY_GEM_BASE_URL", "https://api.example.com")
    @timeout = Integer(ENV.fetch("MY_GEM_TIMEOUT", 30)) rescue 30
  end

  def logger
    @logger ||= defined?(Rails) ? Rails.logger : Logger.new($stderr)
  end
end
```

Usage:
```ruby
MyGem.configure do |config|
  config.api_key = "secret"
end
```

## Error Handling

```ruby
# lib/my_gem/errors.rb
module MyGem
  class Error < StandardError
    attr_reader :status, :body

    def initialize(message = nil, status: nil, body: nil)
      super(message)
      @status, @body = status, body
    end
  end

  class ConfigurationError < Error; end
  class AuthenticationError < Error; end  # 401
  class ClientError < Error; end          # 4xx
  class ServerError < Error; end          # 5xx
  class NetworkError < Error; end         # Connection failures
end
```

## Detailed Reference

Load [detailed-reference.md](references/detailed-reference.md) for extended examples, templates, and advanced patterns.
