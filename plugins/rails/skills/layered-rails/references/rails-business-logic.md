# Rails Business Logic SOP

Use this SOP to decide where Rails business logic belongs. Start with ordinary Rails objects and add a specialized pattern only when it removes demonstrated complexity.

## Selection

| Need | Pattern | When |
| --- | --- | --- |
| Invariant with one clear owner | Model method or concern | The rule depends on one domain object |
| Multi-model operation | Plain operation object | One action coordinates records or owns a transaction boundary |
| Typed inputs and validations | ActiveInteraction | The application already uses it and needs a standard outcome object |
| Explicit lifecycle | State machine | Valid states, transitions, and guards form part of the domain |
| Durable audit history | Persisted domain event record | The application must retain what happened, when, and by whom |
| Misplaced responsibility | Extract to the correct layer | HTTP, domain, orchestration, and infrastructure concerns are mixed |

Do not combine these patterns by default. For example, a state machine does not require an operation object unless transition orchestration has its own clear boundary.

## Model Behavior

Keep a rule on the model when one object owns it and the behavior protects its own valid state.

```ruby
class Order < ApplicationRecord
  def cancel!(actor:)
    raise CannotCancel unless pending?

    update!(status: "cancelled", cancelled_by: actor)
  end
end
```

Pass request context such as the current user as an explicit argument. Models must not read controller objects, request parameters, or request-local state.

## Operation Objects

Use one operation object when a user action coordinates multiple domain objects or owns one transaction boundary.

```ruby
module Orders
  class Place
    def initialize(cart:, customer:)
      @cart = cart
      @customer = customer
    end

    def call
      validate_cart!

      ActiveRecord::Base.transaction do
        order = Order.create!(customer: @customer, total: @cart.total)
        order.line_items.create!(@cart.line_item_attributes)
        order
      end
    end
  end
end
```

Use a plain Ruby object first. Use ActiveInteraction when the application already depends on it and typed inputs, validations, composition, or a standard outcome object provide a concrete benefit.

## State Machines

Use a state machine when the entity has explicit states and only specified transitions are valid.

```ruby
class Order < ApplicationRecord
  enum :status, pending: "pending", paid: "paid", shipped: "shipped"

  def mark_paid!
    raise InvalidTransition unless pending?

    update!(status: "paid")
  end
end
```

Use AASM when the application already depends on it and several transitions, guards, or callbacks make plain transition methods difficult to inspect. Keep external side effects outside transition transactions.

## Durable Event History

A state column records the current value. It does not record how the entity reached that value. Add an event record only when audit, activity, integration, or debugging requirements need durable history.

Persist the state change and its event in the same database transaction. Dispatch notifications, webhooks, and other external side effects after commit.

## Transaction Boundaries

Multi-step database changes need an explicit transaction boundary.

```ruby
ActiveRecord::Base.transaction do
  from.lock!
  to.lock!
  from.update!(balance: from.balance - amount)
  to.update!(balance: to.balance + amount)
end
```

Rules:

1. Validate inputs before opening the transaction.
2. Lock records in a consistent order.
3. Keep the transaction short.
4. Do not wait for user input inside a transaction.
5. Do not call external APIs inside a transaction.
6. Dispatch asynchronous side effects after commit.

## Nested Transactions

Use `requires_new: true` only when a database savepoint is the required behavior. An exception that escapes the inner block still rolls back the outer transaction.

```ruby
Order.transaction do
  order.update!(status: "processed")

  AuditRecord.transaction(requires_new: true) do
    AuditRecord.create!(record: order, action: "processed")
  end
end
```

Avoid nested transactions when one clear outer transaction can express the operation.

## Tests

Test observable behavior at the boundary that owns it:

- Model test for one-object invariants and invalid state changes.
- Operation test for validation, persisted results, and atomic rollback.
- State machine test for permitted and rejected transitions.
- Event-history test for state and event records committed together.
- Integration test for asynchronous side effects dispatched after commit.

## Success Checklist

- Lower layers do not reference higher layers.
- Models do not access request-local state.
- Operation objects accept domain values, not request or controller objects.
- Controllers contain only HTTP concerns.
- External calls do not hold database locks.
- Each abstraction owns one clear boundary.
- Every specialized pattern solves a demonstrated problem.
