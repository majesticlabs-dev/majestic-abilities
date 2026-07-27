# Rails Business Logic SOP

Use this SOP to decide whether Rails business logic belongs in a typed operation, a state machine, a model, or another layer.

## Routing

| Need | Use | When |
| --- | --- | --- |
| Typed operation | `active-interaction-coder` | One-time business operation with typed inputs and validations |
| State machine | `aasm-coder` | Entity lifecycle with explicit states and transitions |
| Layer extraction | `layered-rails` | Business logic is leaking across controller, model, service, and callback boundaries |
| Event history | `event-sourcing-coder` | State transitions need durable event records or audit trails |

## ActiveInteraction

Use for operations that happen once:

- User registration
- Order placement
- Payment processing
- Data imports
- Report generation

```ruby
outcome = Users::Create.run(email: email, name: name)
```

## AASM

Use for stateful entities with a lifecycle:

- Order status: pending, paid, shipped
- Subscription state: trial, active, cancelled
- Document workflow: draft, review, published
- Task status: todo, in_progress, done

```ruby
order.pay!
order.ship!
```

## Combined Pattern

Interactions can trigger state transitions when the operation owns the transaction boundary.

```ruby
module Orders
  class Process < ActiveInteraction::Base
    object :order, class: Order

    def execute
      order.process!
      fulfill_order(order)
      order
    end
  end
end
```

## Transaction Boundaries

Multi-step database changes need explicit transaction boundaries.

```ruby
def transfer_funds(from, to, amount)
  ActiveRecord::Base.transaction do
    from.lock!
    to.lock!
    from.update!(balance: from.balance - amount)
    to.update!(balance: to.balance + amount)
  end
end
```

Rules:

1. Lock records in a consistent order.
2. Keep transactions short.
3. Do not wait for user input inside transactions.
4. Do not call external APIs inside transactions.
5. Validate first, transact last.

## Nested Transactions

Use `requires_new: true` when an inner failure must roll back only the inner unit.

```ruby
transaction do
  create_order!
  transaction(requires_new: true) do
    charge_card!
  end
end
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
| --- | --- | --- |
| Long transactions | Lock contention | Split into smaller units |
| API calls inside transactions | Timeouts block database locks | Call outside, then persist results |
| User input inside transactions | Indefinite locks | Validate before transaction |
| Nested transactions by accident | Savepoint confusion | Use explicit transaction semantics |
| Services accepting controller objects | HTTP concerns leak into domain layer | Pass typed inputs or model objects |

## Success Checklist

- Lower layers do not reference higher layers.
- Models do not access request-local state.
- Services do not accept request or controller objects.
- Controllers contain only HTTP concerns.
- Domain logic lives in the right domain object or operation.
- Callback-heavy flows are extracted or justified.
- Each abstraction belongs to exactly one layer.
