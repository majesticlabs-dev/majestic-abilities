# Pattern Catalog by Layer

Use this catalog to select and implement a fitting pattern without assuming another skill is installed.

## Presentation Layer

### Filter Object

Transforms raw request params into query-ready structures.

**Use when:**
- Controller has 5+ lines of param parsing/transformation
- Same filtering logic appears in multiple actions
- Params need type coercion, defaults, or sanitization

```ruby
# app/filters/posts_filter.rb
class PostsFilter
  include ActiveModel::Model
  include ActiveModel::Attributes

  attribute :status, :string, default: "published"
  attribute :category_id, :integer
  attribute :since, :date

  def apply(scope)
    scope = scope.where(status: status) if status.present?
    scope = scope.where(category_id: category_id) if category_id.present?
    scope = scope.where("created_at >= ?", since) if since.present?
    scope
  end
end

# Controller
def index
  filter = PostsFilter.new(filter_params)
  @posts = filter.apply(Post.all)
end
```

**Keep inline when:** Simple single-attribute filtering (1-2 `where` clauses).

### Presenter

View-specific logic that doesn't belong in models or helpers.

**Use when:**
- View logic combines data from multiple models
- Formatting depends on view context (locale, current_user permissions)
- Model methods exist only for display purposes

```ruby
# app/presenters/dashboard_presenter.rb
class DashboardPresenter
  def initialize(user)
    @user = user
  end

  def greeting
    hour = Time.current.hour
    period = case hour
             when 5..11 then "morning"
             when 12..17 then "afternoon"
             else "evening"
             end
    "Good #{period}, #{@user.first_name}"
  end

  def recent_activity
    @user.activities.includes(:trackable).limit(10)
  end

  def unread_count
    @user.notifications.unread.count
  end
end
```

**Prefer ViewComponent when:** The presenter needs its own template.

### Serializer

Formats domain objects for API responses.

**Use when:**
- API responses need specific field selection
- Different endpoints return different representations of the same model
- Nested associations need controlled serialization

```ruby
# app/serializers/post_serializer.rb
class PostSerializer
  def initialize(post)
    @post = post
  end

  def as_json
    {
      id: @post.id,
      title: @post.title,
      excerpt: @post.body.truncate(200),
      author: { name: @post.author.name },
      published_at: @post.published_at&.iso8601
    }
  end
end
```

### Form Object

Handles multi-model forms or complex validation scenarios.

**Use when:**
- Form spans 2+ models
- Validation rules differ from model validations (e.g., registration vs profile edit)
- Need virtual attributes that don't map to any model

```ruby
# app/forms/registration_form.rb
class RegistrationForm
  include ActiveModel::Model
  include ActiveModel::Attributes

  attribute :email, :string
  attribute :name, :string
  attribute :company_name, :string
  attribute :terms_accepted, :boolean

  validates :email, :name, :company_name, presence: true
  validates :terms_accepted, acceptance: true

  def save
    return false unless valid?

    ActiveRecord::Base.transaction do
      company = Company.create!(name: company_name)
      User.create!(email: email, name: name, company: company)
    end
  rescue ActiveRecord::RecordInvalid => e
    errors.add(:base, e.message)
    false
  end
end
```

**Keep inline when:** Form maps 1:1 to a single model's attributes.

## Application Layer

### Service Object

Orchestrates operations across multiple domain objects.

**Use when:**
- Operation touches 2+ models in a transaction
- External side-effects (emails, API calls) must be coordinated
- Operation is reused from controllers, jobs, and console

Use ActiveInteraction when the application already uses it and the operation benefits from typed inputs, validations, and a standardized outcome. Otherwise, start with a plain Ruby operation object.

```ruby
# Plain service (when ActiveInteraction is not available)
# app/services/orders/checkout.rb
module Orders
  class Checkout
    def initialize(cart:, payment_method:, user:)
      @cart = cart
      @payment_method = payment_method
      @user = user
    end

    def call
      order = create_pending_order
      charge = PaymentGateway.charge(
        @payment_method,
        amount: order.total,
        idempotency_key: "order-#{order.id}"
      )
      order.update!(payment_id: charge.id, status: "paid")
      OrderMailer.confirmation(order).deliver_later
      order
    end

    private

    def create_pending_order
      ActiveRecord::Base.transaction do
        order = Order.create!(user: @user, total: @cart.total, status: "pending")
        order.line_items.create!(@cart.line_item_attributes)
        order
      end
    end
  end
end
```

Persist the pending order before the external call so a retry can recover it. Use a stable idempotency key to prevent duplicate charges.

**Warning signs the service should be split:**
- Service > 50 lines
- Service calls other services (extract shared logic)
- Service has conditional branches for different scenarios (use separate services)

### Policy Object

Authorization decisions separated from controllers. Use the application's existing policy library, or a plain Ruby policy with one public decision method.

**Use when:**
- Authorization rules are complex (RBAC, ABAC, resource-based)
- Same authorization logic needed across controllers, channels, jobs
- Authorization needs caching for performance

## Domain Layer

### Query Object

Encapsulates complex, reusable database queries.

**Use when:**
- Query logic exceeds a simple scope (joins, subqueries, CTEs)
- Same query used in 2+ locations
- Query needs parameterization beyond simple `where`

```ruby
# app/queries/trending_posts_query.rb
class TrendingPostsQuery
  def initialize(relation = Post.all)
    @relation = relation
  end

  def call(period: 7.days, limit: 20)
    @relation
      .published
      .where(published_at: period.ago..)
      .joins(:reactions)
      .group(:id)
      .order("COUNT(reactions.id) DESC")
      .limit(limit)
  end
end

# Usage
TrendingPostsQuery.new.call(period: 30.days, limit: 10)
TrendingPostsQuery.new(current_user.posts).call  # scoped to user
```

**Keep as scope when:** Query is a simple `where`/`order` chain (1-2 methods).

### Value Object

Immutable objects defined by their attributes, not identity.

**Use when:**
- Concept has no database ID but has behavior (Money, DateRange, Address)
- Multiple attributes always travel together
- Comparison is by value, not reference

```ruby
# app/models/money.rb
class Money
  include Comparable

  attr_reader :amount, :currency

  def initialize(amount, currency = "USD")
    @amount = BigDecimal(amount.to_s)
    @currency = currency
    freeze
  end

  def +(other)
    raise "Currency mismatch" unless currency == other.currency
    self.class.new(amount + other.amount, currency)
  end

  def <=>(other)
    return nil unless currency == other.currency
    amount <=> other.amount
  end

  def to_s
    "#{currency} #{'%.2f' % amount}"
  end
end
```

### State Machine

Model explicit states, permitted transitions, and guards together. Use AASM when the application already depends on it; otherwise, plain enum-backed transition methods can be sufficient.

**Use when:**
- Object has distinct states with defined transitions
- Transitions have guards and side-effects
- Invalid state changes must be prevented at the model level

### Concern (Behavioral)

**Use when:**
- Multiple models share the same behavior (not just the same columns)
- The concern has a clear name describing the behavior
- The concern is cohesive (all methods relate to one behavior)

```ruby
# app/models/concerns/archivable.rb
module Archivable
  extend ActiveSupport::Concern

  included do
    scope :archived, -> { where.not(archived_at: nil) }
    scope :active, -> { where(archived_at: nil) }
  end

  def archive!
    update!(archived_at: Time.current)
  end

  def unarchive!
    update!(archived_at: nil)
  end

  def archived?
    archived_at.present?
  end
end
```

**Anti-pattern (code-slicing concern):** Grouping by artifact type (all validations, all scopes) rather than behavior. Each concern should represent a cohesive capability.

## Decision Summary

```
Need typed inputs and a standard outcome? → ActiveInteraction when already adopted
Need authorization? → Policy Object using the application's policy library
Need state transitions? → State Machine, with AASM when already adopted
Need typed JSON attributes? → StoreModel or a typed value object
Need typed configuration? → Configuration object using the application's existing library
Need a durable audit trail? → Persisted domain event records
Need reusable rendered UI? → ViewComponent
Everything else → Use the simplest pattern in this catalog
```
