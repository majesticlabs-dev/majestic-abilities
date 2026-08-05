---
name: solid-queue-coder
description: "Use when configuring or working with Solid Queue for background jobs. Applies Rails 8 conventions, database-backed job processing, concurrency settings, recurring jobs, and production deployment patterns."
---

# Solid Queue Coder

## Overview

Solid Queue is Rails 8's default job backend, a database-backed Active Job adapter that eliminates the need for Redis. Jobs are stored in your database with ACID guarantees.

## Configuration

### Database Setup

```yaml
# config/database.yml
production:
  primary:
    <<: *default
    url: <%= ENV["DATABASE_URL"] %>
  queue:
    <<: *default
    url: <%= ENV["QUEUE_DATABASE_URL"] %>
    migrations_paths: db/queue_migrate
```

### Queue Configuration

Solid Queue reads `config/queue.yml` by default. Override with `SOLID_QUEUE_CONFIG` or `bin/jobs -c path`.

```yaml
# config/queue.yml
production:
  dispatchers:
    - polling_interval: 1
      batch_size: 500

  workers:
    - queues: [critical, default]
      threads: 5
      processes: 2
      polling_interval: 0.1
    - queues: [low_priority]
      threads: 2
      processes: 1
      polling_interval: 1
```

### Application Configuration

```ruby
# config/application.rb
config.active_job.queue_adapter = :solid_queue

# config/environments/production.rb
config.solid_queue.connects_to = { database: { writing: :queue } }
```

## Fiber vs Thread Workers

A worker declares either `threads: N` (a thread pool, one kernel thread per running job) or `fibers: N` (up to N fibers cooperatively scheduled on a single Async reactor thread). The two keys are mutually exclusive within a worker.

Fibers win on I/O-bound work because a job awaiting a network response yields instead of pinning a thread. They do nothing for computation. Published benchmarks show roughly +12% on LLM streaming and +9.5% on async HTTP, but about 0% on CPU work. The larger practical win is connection pool pressure, not throughput.

### Requirements

```ruby
# config/application.rb
config.active_support.isolation_level = :fiber
```

- `async` gem in the Gemfile (Solid Queue uses it to install Ruby's fiber scheduler)
- Solid Queue refuses to boot fiber workers while isolation is still thread-scoped

### Routing by Workload Shape

Mix modes rather than converting everything. Route I/O-bound queues to fibers and keep a thread worker for the rest.

```yaml
# config/queue.yml
production:
  workers:
    - queues: [chat]                 # LLM streaming, I/O bound
      fibers: 10
      processes: 2
    - queues: [turbo]                # broadcasts
      fibers: 10
      processes: 1
    - queues: [notifications, default]
      fibers: 5
      processes: 1
    - queues: [cpu]                  # computation, long transactions
      threads: 1
      processes: 1
```

### Connection Pool Sizing

Pool size is per worker process, and the total across processes must fit under the database `max_connections`.

| Mode | Connections per process |
|------|-------------------------|
| `threads: N` | `N + 2` (execution, plus polling and heartbeat) |
| `fibers: N` | `3` to `5` regardless of N, since queries release connections between operations |

50 execution slots across 6 processes needs roughly 312 connections in thread mode and roughly 18 in fiber mode. Treat these as estimates: long transactions and libraries that pin a connection push actual usage back toward the thread numbers.

### Caveats

- A library or C extension that does not cooperate with the fiber scheduler blocks the reactor thread, stalling every fiber in that process, not just the calling job.
- Jobs that hold a database connection for their whole run (long transactions) erase most of the pool advantage. Put them on a thread worker.
- `isolation_level = :fiber` is process-global. Running Solid Queue inside Puma via the plugin, or combining fiber and thread workers in one process under the supervisor's `async` mode, makes everything in that process fiber-scoped.

## Queue Design

### Priority Strategy

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

### Concurrency Control

```ruby
class ProcessUserDataJob < ApplicationJob
  limits_concurrency key: ->(user_id) { user_id }
end

class SyncContactJob < ApplicationJob
  limits_concurrency key: ->(contact) { contact.id },
                     duration: 15.minutes,
                     group: "ContactOperations"
end
```

## Recurring Jobs

```yaml
# config/queue.yml
recurring:
  cleanup_old_records:
    class: CleanupJob
    schedule: every day at 3am
    queue: low_priority

  sync_external_data:
    class: SyncExternalDataJob
    schedule: every 15 minutes
    queue: default
```

## Deployment

### Procfile

```yaml
web: bundle exec puma -C config/puma.rb
worker: bundle exec rake solid_queue:start
```

### Docker Compose

```yaml
services:
  web:
    command: bundle exec puma -C config/puma.rb
  worker:
    command: bundle exec rake solid_queue:start
```

## Error Handling

```ruby
class ExternalApiJob < ApplicationJob
  retry_on Net::OpenTimeout, wait: :polynomially_longer, attempts: 5
  discard_on ActiveJob::DeserializationError

  rescue_from StandardError do |exception|
    if executions >= 5
      FailedJob.create!(job_class: self.class.name, error_message: exception.message)
    else
      raise exception
    end
  end
end
```

## Database Maintenance

```ruby
namespace :queue do
  task vacuum: :environment do
    ActiveRecord::Base.connected_to(database: :queue) do
      %w[solid_queue_ready_executions solid_queue_claimed_executions].each do |table|
        ActiveRecord::Base.connection.execute("VACUUM ANALYZE #{table}")
      end
    end
  end
end
```

## Solid Queue vs Sidekiq

| Feature | Solid Queue | Sidekiq |
|---------|-------------|---------|
| Infrastructure | Database only | Requires Redis |
| ACID guarantees | Yes | No |
| Transactional enqueue | Yes | No |
| Concurrency control | Built-in | Requires sidekiq-unique-jobs |

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Wildcard queue `*` in prod | Unpredictable priority | Specify queue order |
| Single database | Contention with app | Separate queue database |
| Too many threads | Database exhaustion | Size pool at `threads + 2` per process, check the total against `max_connections` |
| Threads for I/O-bound jobs | One kernel thread and one connection per in-flight request | Use `fibers:` for LLM, HTTP, and broadcast queues |
| Fibers for CPU or long-transaction jobs | Blocks the reactor or pins a connection for the whole run | Keep a `threads:` worker for those queues |
| `fibers:` without `isolation_level = :fiber` | Worker refuses to boot | Set it in `config/application.rb` and add the `async` gem |
| Sizing the fiber pool at `fibers + 2` | Wastes connections | Start at 3 to 5 per worker process |

## Output Format

When configuring Solid Queue, provide:

1. **Database Setup** - Multi-database configuration
2. **Queue Config** - `config/queue.yml` settings
3. **Execution Mode** - Threads or fibers per queue, with the pool size that follows
4. **Worker Setup** - Procfile/Docker configuration
5. **Jobs** - Example job classes with error handling
