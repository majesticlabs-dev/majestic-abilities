# Rails Conventions

Use this reference for Rails convention checks that support implementation, review, and refactoring skills.

## Core Position

- Simple duplicated code beats complex abstractions.
- Controllers should stay thin and mostly RESTful.
- Business logic belongs in models, domain objects, interactions, or small services chosen deliberately.
- Rails conventions should default until application evidence is insufficient.
- Test behavior through public outcomes before adding production indirection only to make internals easier to test.
- Extract abstractions only when the new boundary removes real complexity or has multiple concrete callers.

## Controllers

- Prefer seven REST actions.
- Create dedicated controllers for meaningful custom behavior.
- Keep orchestration short.
- Use strong parameter methods before action setup.
- Use `params.expect` when the app's Rails version supports it, and make nested attribute collection shapes explicit.
- Inline simple Turbo Stream responses when a separate template adds ceremony without clarity.

```ruby
def person_params
  params.expect(person: [ :name, :age ])
end
```

```ruby
render turbo_stream: [
  turbo_stream.replace("post_#{@post.id}", partial: "posts/post", locals: { post: @post }),
  turbo_stream.remove("flash")
]
```

## Models

- Put domain rules close to the data they protect.
- Use semantic association names.
- Use scopes for common queries.
- Use concerns for shared domain behavior, not by artifact type.

```ruby
module Dispatchable
  extend ActiveSupport::Concern

  included do
    scope :available, -> { where(status: "pending") }
  end

  class_methods do
    def claim!(batch_size)
      # class-level behavior
    end
  end
end
```

## Extraction Signals

Extract when multiple signals are present:

- complex business rules
- multiple models orchestrated together
- external API interactions
- reusable cross-controller logic
- explicit transaction, retry, or idempotency ownership
- callback side effects that are not data integrity work

Avoid extracting only because a method is long. Repetition is cheaper than a service layer that only forwards arguments.

Good service boundaries usually have:

- one public method
- namespace by responsibility
- explicit constructor dependencies
- return values that match the caller's need

## Ruby Style

- Use guard clauses to reduce nesting.
- Prefer semantic predicates such as `present?`, `any?`, and domain-specific methods.
- Use keyword arguments for clarity.
- Prefer modern hash shorthand when it improves readability.
- Query directly with `pluck` when objects are not needed.

```ruby
{ id:, slug:, doc_type: kind }

created_at&.iso8601
@setting ||= SlugSetting.active.find_by!(slug:)

def extract(document_type:, subject:, filename:)
  process!(strategy: nil)
end
```

## Enum And Scope Patterns

- Use string-backed values when the value is part of the domain language.
- Validate enum values when Rails version and app style support it.
- Keep scopes chainable and guard optional filters.

```ruby
STATUSES = %w[processed needs_review].freeze
enum :status, STATUSES.index_by(&:itself), validate: true
```

```ruby
scope :by_slug, ->(slug) { where(slug:) if slug.present? }
scope :from_date, ->(date) { where(created_at: Date.parse(date).beginning_of_day..) if date.present? }
```

## Error Handling

- Prefer domain-specific errors over generic rescue blocks.
- Log useful context before re-raising exceptions that upstream code should handle.
- Do not swallow failures only to make the call path look successful.

```ruby
class InactiveSlug < StandardError; end

def handle_exception!(error:)
  log_error("Exception #{error.class}: #{error.message}", error:)
  mark_failed!(error.message)
  raise
end
```

## Testing

- Test behavior, not private implementation details.
- Use fixtures for stable setup when the app already follows Rails fixture style.
- Stub external boundaries such as object storage, payment providers, APIs, PDFs, time, and randomness.
- Reload records after operations when asserting persisted state.
- Avoid production indirection added only to make a test easier.

```ruby
test "marks the email finished after processing" do
  email = emails(:two)

  email.process

  email.reload
  assert_equal "finished", email.processing_status
end
```

## Naming

If a name cannot be understood in a few seconds, make it more specific.

```ruby
# Weak
show_in_frame
process_stuff

# Better
fact_check_modal
fact_frame
```

## JavaScript And Importmap

- Scope JavaScript dependencies to the narrowest entrypoint.
- Pin public dependencies for the public entrypoint.
- Keep admin-only imports in an admin entrypoint.
- Do not add admin-only libraries to `application.js`.

```ruby
pin "application"
pin "@hotwired/turbo-rails", to: "turbo.min.js"
pin "@hotwired/stimulus", to: "stimulus.min.js"
pin "chartkick", to: "chartkick.js"
pin "Chart.bundle", to: "Chart.bundle.js"
```

```javascript
// app/javascript/application.js
import "@hotwired/turbo-rails"
import "@hotwired/stimulus"
import "controllers"

// app/javascript/admin.js
import "application"
import "chartkick"
import "Chart.bundle"
```

## Performance

- Consider scale impact before adding infrastructure.
- Avoid premature caching.
- Add indexes when query evidence justifies the write cost.

## Review Questions

- Does this fight Rails conventions with no payoff?
- Is the abstraction reducing real complexity, or only moving code around?
- Can behavior be tested at the right level?
- Did the change preserve existing workflows?
