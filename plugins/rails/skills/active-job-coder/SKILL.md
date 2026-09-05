---
name: active-job-coder
description: "Use when creating or refactoring Active Job background jobs."
---

# Active Job Coder

## Job Design Principles

### 1. Single Responsibility

```ruby
# Good: Focused job that delegates domain work
class SendWelcomeEmailJob < ApplicationJob
  queue_as :default

  def perform(user)
    user.send_welcome_email
  end
end
```

Keep job bodies shallow. The job should restore context, choose queue/retry behavior, and call a model or domain method that owns the actual work.

### 2. Pass Stable Payloads

```ruby
# Good: pass identifiers for external boundaries or very stale-sensitive work
class ProcessOrderJob < ApplicationJob
  def perform(order_id)
    order = Order.find(order_id)
    order.process
  end
end
```

Passing Active Record instances is also valid in Rails when GlobalID semantics are the right contract. Avoid large object graphs, hashes of denormalized state, or relying on `Current` inside `perform`.

### 3. Queue Configuration

```ruby
class CriticalNotificationJob < ApplicationJob
  queue_as :critical
  queue_with_priority 1  # Lower = higher priority
end

class ReportGenerationJob < ApplicationJob
  queue_as :low_priority
  queue_with_priority 50
end
```

The queue also selects the execution model when the backend runs mixed workers, since Solid Queue supports `fibers:` alongside `threads:`. Route by workload shape: I/O-bound jobs such as LLM calls, HTTP requests, and Turbo broadcasts belong on a fiber queue; CPU-bound work and jobs holding a transaction for their whole run belong on a thread queue. See `solid-queue-coder` for the worker config and pool sizing.

## Error Handling & Retry Strategies

```ruby
class ExternalApiJob < ApplicationJob
  queue_as :default

  retry_on Net::OpenTimeout, wait: :polynomially_longer, attempts: 5
  retry_on ActiveRecord::Deadlocked, wait: 5.seconds, attempts: 3
  discard_on ActiveJob::DeserializationError

  def perform(record_id)
    record = Record.find(record_id)
    ExternalApi.sync(record)
  end
end
```

### Custom Error Handling

```ruby
class ImportantJob < ApplicationJob
  rescue_from StandardError do |exception|
    Rails.logger.error("Job failed: #{exception.message}")
    ErrorNotifier.notify(exception, job: self.class.name)
    raise # Re-raise to trigger retry
  end
end
```

## Concurrency Control (Solid Queue)

```ruby
class ProcessUserDataJob < ApplicationJob
  limits_concurrency key: ->(user_id) { user_id }, duration: 15.minutes

  def perform(user_id)
    user = User.find(user_id)
    # Process user data safely
  end
end

class ContactActionJob < ApplicationJob
  limits_concurrency key: ->(contact) { contact.id },
                     duration: 10.minutes,
                     group: "ContactActions"
end
```

## Scheduling & Delayed Execution

```ruby
SendReminderJob.perform_later(user)                              # Immediate
SendReminderJob.set(wait: 1.hour).perform_later(user)            # Delayed
SendReminderJob.set(wait_until: Date.tomorrow.noon).perform_later(user)  # Scheduled

# Bulk enqueue
ActiveJob.perform_all_later(users.map { |u| SendReminderJob.new(u.id) })
```

Set `ActiveJob::Base.enqueue_after_transaction_commit = true` at the application level when jobs depend on records created or changed in the same transaction. That fixes job-before-commit races at the source.

For multi-tenant apps, serialize tenant context at enqueue time and restore it around `perform`; do not infer the tenant from a bare record ID later.

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Fat jobs | Hard to test and maintain | Extract logic to model classes |
| Large serialized payloads | Expensive, stale data | Pass IDs or GlobalID records with clear freshness semantics |
| No retry strategy | Silent failures | Use `retry_on` with backoff |
| Synchronous calls | Blocks request | Always use `perform_later` |
| No idempotency | Duplicate processing | Design jobs to be re-runnable |
| Ignoring errors | Silent failures | Use `rescue_from` with logging |
| Monolithic steps | Can't resume after failure | Use Continuable pattern with state |
| `Current.user` inside `perform` | Request context is gone | Pass actor or tenant context at enqueue |
| CPU-heavy or long-transaction job on a fiber queue | Blocks the reactor for every other fiber, or pins a connection for the job's lifetime | Route it to a thread worker queue |

## Output Format

When creating or refactoring jobs, provide:

1. **Job Class** - The complete job implementation
2. **Queue Strategy** - Recommended queue and priority
3. **Error Handling** - Retry and failure strategies
4. **Testing** - Example test cases
5. **Considerations** - Concurrency, idempotency notes
