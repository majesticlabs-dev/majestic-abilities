# AnyCable Coder Detailed Reference

## Configuration

### AnyCable Server

```yaml
# config/anycable.yml
production:
  broadcast_adapter: nats
  redis_url: <%= ENV.fetch("REDIS_URL") %>

  # Enable reliable streams
  streams_history_size: 100
  streams_history_ttl: 300
```

### Cable URL

```erb
<!-- app/views/layouts/application.html.erb -->
<%= action_cable_meta_tag %>
```

```javascript
// Auto-detects from meta tag, or specify explicitly
import { createCable } from "@anycable/web"
createCable("wss://cable.example.com/cable")
```

## Deployment

### Procfile

```yaml
web: bundle exec puma -C config/puma.rb
anycable: bundle exec anycable
ws: anycable-go
```

### Docker Compose

```yaml
services:
  web:
    command: bundle exec puma
  anycable:
    command: bundle exec anycable
  ws:
    image: anycable/anycable-go:1.6
    environment:
      ANYCABLE_RPC_HOST: anycable:50051
      ANYCABLE_REDIS_URL: redis://redis:6379
```

## Action Cable vs AnyCable

| Feature | Action Cable | AnyCable |
|---------|--------------|----------|
| Delivery guarantee | At-most once | At-least once |
| Message ordering | Not guaranteed | Guaranteed |
| History on reconnect | No | Yes (configurable) |
| Presence tracking | Manual | Built-in |
| Performance | Ruby threads | Go server |
| LLM streaming | Unreliable | Reliable |

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Action Cable for LLM streaming | Lost chunks on reconnect | Use AnyCable |
| Ignoring message ordering | Garbled responses | AnyCable handles automatically |
| Manual reconnection logic | Complex, error-prone | Use AnyCable client |
| No presence tracking | Unknown user state | Use built-in presence API |

## Output Format

When implementing real-time features with AnyCable:

1. **Channel** - Server-side Ruby channel with broadcasting
2. **Client** - JavaScript subscription with message handling
3. **Configuration** - anycable.yml and deployment setup
4. **Error Handling** - Graceful degradation patterns
