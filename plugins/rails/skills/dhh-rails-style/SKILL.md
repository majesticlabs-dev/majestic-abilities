---
name: dhh-rails-style
description: "Write and review Ruby and Rails code using DHH and 37signals conventions. Use when implementing, refactoring, or reviewing Rails code for Rails-native simplicity, or when the user mentions DHH, 37signals, Basecamp, HEY, Fizzy, or Campfire."
---

# DHH Rails Style

Apply DHH's Rails philosophy in two modes:

- **Implementation:** Write or refactor code with clarity, convention, and Rails-native simplicity.
- **Review:** Inspect changes for unnecessary layers, non-RESTful design, anemic models, avoidable client-side complexity, and departures from the conventions below.

For reviews, report concrete deviations, explain the simpler Rails-native alternative, and finish with `APPROVED` or `NEEDS CHANGES`. Do not pad the review with praise.

## Quick Reference

### Controller Actions
- **Only 7 REST actions**: `index`, `show`, `new`, `create`, `edit`, `update`, `destroy`
- **New behavior?** Create a new controller, not a custom action
- **Action length**: 1-5 lines maximum
- **Empty actions are fine**: Let Rails convention handle rendering

```ruby
class MessagesController < ApplicationController
  before_action :set_message, only: %i[ show edit update destroy ]

  def index
    @messages = @room.messages.with_creator.last_page
    fresh_when @messages
  end

  def show
  end

  def create
    @message = @room.messages.create_with_attachment!(message_params)
    @message.broadcast_create
  end

  private
    def set_message
      @message = @room.messages.find(params[:id])
    end

    def message_params
      params.require(:message).permit(:body, :attachment)
    end
end
```

### Private Method Indentation
Indent private methods one level under `private` keyword:

```ruby
  private
    def set_message
      @message = Message.find(params[:id])
    end

    def message_params
      params.require(:message).permit(:body)
    end
```

### Model Design (Fat Models)
Models own business logic, authorization, and broadcasting:

```ruby
class Message < ApplicationRecord
  belongs_to :room
  belongs_to :creator, class_name: "User"
  has_many :mentions

  scope :with_creator, -> { includes(:creator) }
  scope :page_before, ->(cursor) { where("id < ?", cursor.id).order(id: :desc).limit(50) }

  def broadcast_create
    broadcast_append_to room, :messages, target: "messages"
  end

  def mentionees
    mentions.includes(:user).map(&:user)
  end
end

class User < ApplicationRecord
  def can_administer?(message)
    message.creator == self || admin?
  end
end
```

### Current Attributes
Use `Current` for request context, never pass `current_user` everywhere:

```ruby
class Current < ActiveSupport::CurrentAttributes
  attribute :user, :session
end

# Usage anywhere in app
Current.user.can_administer?(@message)
```

### Ruby Syntax Preferences

DHH-specific style (for general Ruby style, see `ruby-coder` skill):

```ruby
# Symbol arrays with spaces inside brackets
before_action :set_message, only: %i[ show edit update destroy ]

# Expression-less case for cleaner conditionals
case
when params[:before].present?
  @room.messages.page_before(params[:before])
when params[:after].present?
  @room.messages.page_after(params[:after])
else
  @room.messages.last_page
end
```

### Query Optimization

Prefer `pluck(:name)` over `map(&:name)` and `messages.count` over `messages.to_a.count` -- push work to the database.

### StringInquirer for Predicates

Use `.inquiry` on string enums for readable conditionals:

```ruby
class Event < ApplicationRecord
  def action
    super.inquiry
  end
end

# Clean predicate methods
event.action.completed?
event.action.pending?
event.action.failed?
```

### Controller Response Patterns

Use `head :no_content` for updates without body, `head :created` for creates. Bang methods (`create!`, `update!`) for fail-fast.

### My:: Namespace for Current User Resources

Use `My::` namespace for resources scoped to `Current.user`:

```ruby
# routes.rb
namespace :my do
  resource :profile, only: %i[ show edit update ]
  resources :notifications, only: %i[ index destroy ]
end

# app/controllers/my/profiles_controller.rb
class My::ProfilesController < ApplicationController
  def show
    @profile = Current.user
  end
end
```

No `index` or `show` with ID needed. The resource is implicit from `Current.user`.

### Compute at Write Time

Perform data manipulation during saves, not during presentation:

```ruby
# WRONG: Compute on read
def display_name
  "#{first_name} #{last_name}".titleize
end

# CORRECT: Compute on write
before_save :set_display_name

private
  def set_display_name
    self.display_name = "#{first_name} #{last_name}".titleize
  end
```

Benefits: enables pagination, caching, and reduces view complexity.

### Delegate for Lazy Loading

Use `delegate` to enable lazy loading through associations:

```ruby
class Message < ApplicationRecord
  belongs_to :session
  delegate :user, to: :session
end

# Lazy loads user through session
message.user
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Setter methods | `set_` prefix | `set_message`, `set_room` |
| Parameter methods | `{model}_params` | `message_params` |
| Association names | Semantic, not generic | `creator` not `user` |
| Scopes | Chainable, descriptive | `with_creator`, `page_before` |
| Predicates | End with `?` | `direct?`, `can_administer?` |
| Current user resources | `My::` namespace | `My::ProfilesController` |

### Hotwire/Turbo Patterns
Broadcasting is model responsibility:

```ruby
# In model
def broadcast_create
  broadcast_append_to room, :messages, target: "messages"
end
```

**For detailed Hotwire patterns, use `hotwire-coder` skill.**

### Error Handling
Rescue specific exceptions, fail fast with bang methods:

```ruby
def create
  @message = @room.messages.create_with_attachment!(message_params)
  @message.broadcast_create
rescue ActiveRecord::RecordNotFound
  render action: :room_not_found
end
```

### State as Records (Not Booleans)

Track state via database records rather than boolean columns:

```ruby
# WRONG: Boolean columns for state
class Card < ApplicationRecord
  # closed: boolean, gilded: boolean columns
end
card.update!(closed: true)
card.closed?  # Loses who/when/why

# CORRECT: State as separate records
class Card < ApplicationRecord
  has_one :closure
  has_one :gilding

  def close(by:)
    create_closure!(closed_by: by)
  end

  def closed?
    closure.present?
  end
end
card.close(by: Current.user)
card.closure.closed_by  # Full audit trail
```

### REST URL Transformations

Map custom actions to nested resource controllers:

| Custom Action | REST Resource |
|---------------|---------------|
| `POST /cards/:id/close` | `POST /cards/:id/closure` |
| `DELETE /cards/:id/close` | `DELETE /cards/:id/closure` |
| `POST /cards/:id/gild` | `POST /cards/:id/gilding` |
| `POST /posts/:id/publish` | `POST /posts/:id/publication` |
| `DELETE /posts/:id/publish` | `DELETE /posts/:id/publication` |

```ruby
# routes.rb
resources :cards do
  resource :closure, only: %i[ create destroy ]
  resource :gilding, only: %i[ create destroy ]
end

# app/controllers/cards/closures_controller.rb
class Cards::ClosuresController < ApplicationController
  def create
    @card = Card.find(params[:card_id])
    @card.close(by: Current.user)
  end

  def destroy
    @card = Card.find(params[:card_id])
    @card.closure.destroy!
  end
end
```

## Detailed Reference

Load [detailed-reference.md](references/detailed-reference.md) for extended examples, templates, and advanced patterns.
