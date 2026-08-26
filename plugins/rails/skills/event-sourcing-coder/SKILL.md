---
name: event-sourcing-coder
description: "Record domain events and dispatch them to inbox handlers for integrations, asynchronous side effects, analytics, and durable processing history. Use when decoupling event creation from downstream processing, synchronizing external systems, or implementing inbox patterns. Do not use only to render an activity or audit timeline."
---

# Event Sourcing for Rails Monoliths

Record significant domain events and dispatch them to specialized handlers - a pragmatic approach to event sourcing without the complexity of full CQRS/ES infrastructure.

## When to Use This Skill

- Dispatching one domain event to multiple independent handlers
- Syncing data to external services such as CRMs, analytics, or webhooks
- Automating asynchronous workflows triggered by domain events
- Decoupling "what happened" from "what to do about it"
- Keeping durable processing history for integrations or debugging

## When NOT to Use Events

| Scenario | Better Alternative |
|----------|-------------------|
| Rendered activity or audit timeline without downstream dispatch | A dedicated activity timeline pattern |
| Simple callbacks on single model | ActiveRecord callbacks |
| Synchronous side effects only | Service objects or ActiveInteraction |
| Need full event replay/rebuilding | Dedicated event sourcing gem (Rails Event Store) |
| Single handler per event | Direct method calls |

## Core Concept

**Decouple recording from processing:**

```
User action → Record Event → Broadcast to Inboxes → Side Effects
                  ↓
              Queryable
              (audit trail)
```

## Setup

### Migration

```ruby
class CreateIssueEvents < ActiveRecord::Migration[8.0]
  def change
    create_table :issue_events do |t|
      t.references :issue, null: false, foreign_key: true
      t.references :actor, null: false, foreign_key: { to_table: :users }
      t.string :action, null: false
      t.jsonb :metadata, default: {}
      t.timestamps
    end

    add_index :issue_events, :action
    add_index :issue_events, :created_at
  end
end
```

### Event Model

```ruby
# app/models/issue/event.rb
module Issue::Event
  extend ActiveSupport::Concern

  ACTIONS = %w[
    created
    assigned
    status_changed
    commented
    closed
    reopened
  ].freeze

  included do
    belongs_to :issue
    belongs_to :actor, class_name: "User"

    validates :action, presence: true, inclusion: { in: ACTIONS }

    after_commit :broadcast_to_inboxes, on: :create
  end

  private

  def broadcast_to_inboxes
    Issue::Event::BroadcastJob.perform_later(self)
  end
end

class Issue::Event < ApplicationRecord
  include Issue::Event
end
```

### Recording Events

```ruby
# app/models/issue.rb
class Issue < ApplicationRecord
  has_many :events, class_name: "Issue::Event", dependent: :destroy

  def record_event!(action:, actor:, metadata: {}, throttle: nil)
    return if throttle && recently_recorded?(action, throttle)

    events.create!(
      action: action,
      actor: actor,
      metadata: metadata
    )
  end

  private

  def recently_recorded?(action, duration)
    events.where(action: action)
          .where("created_at > ?", duration.ago)
          .exists?
  end
end
```

### Usage in Application

```ruby
# In a controller or interaction
issue.record_event!(
  action: "status_changed",
  actor: current_user,
  metadata: { from: "open", to: "in_progress" }
)

# With throttling (prevent duplicate events within timeframe)
issue.record_event!(
  action: "viewed",
  actor: current_user,
  throttle: 5.minutes
)
```

## Detailed Reference

Load [detailed-reference.md](references/detailed-reference.md) for extended examples, templates, and advanced patterns.
