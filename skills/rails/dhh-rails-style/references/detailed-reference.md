# DHH Ruby/Rails Style Guide Detailed Reference

### Architecture Preferences

| Traditional | DHH Way |
|-------------|---------|
| PostgreSQL | SQLite (for single-tenant) |
| Redis + Sidekiq | Solid Queue |
| Redis cache | Solid Cache |
| Kubernetes | Single Docker container |
| Service objects | Fat models |
| Policy objects (Pundit) | Authorization on User model |
| FactoryBot | Fixtures |
| Boolean state columns | State as records |


## Detailed References

For comprehensive patterns and examples, see:

### Core Patterns
- `patterns.md` - Complete code patterns with explanations
- `palkan-patterns.md` - Namespaced model classes, counter caches, model organization order, PostgreSQL enums
- `concerns-organization.md` - Model-specific vs common concerns, facade pattern
- `delegated-types.md` - Polymorphism without STI problems
- `recording-pattern.md` - Unifying abstraction for diverse content types
- `filter-objects.md` - PORO filter objects, URL-based state, testable query building
- `database-patterns.md` - UUIDv7, hard deletes, state as records, counter caches, indexing

### Rails Components
- `activerecord-tips.md` - ActiveRecord query patterns, validations, associations
- `controllers-tips.md` - Controller patterns, routing, rate limiting, form objects
- `activestorage-tips.md` - File uploads, attachments, blob handling

### Hotwire
- `hotwire-tips.md` - Turbo Frames, Turbo Streams, ViewComponents
- `turbo-morphing.md` - Turbo 8 page refresh with morphing patterns
- `stimulus-catalog.md` - Copy-paste-ready Stimulus controllers (clipboard, dialog, hotkey, etc.)
- **Also see:** `hotwire-coder`, `stimulus-coder`, `viewcomponent-coder` skills for detailed patterns

### Frontend
- `css-architecture.md` - Native CSS patterns (layers, OKLCH, nesting, dark mode)

### Authentication & Multi-Tenancy
- `passwordless-auth.md` - Magic link authentication, sessions, identity model
- `multi-tenancy.md` - Path-based tenancy, cookie scoping, tenant-aware jobs

### Infrastructure & Integrations
- `webhooks.md` - Secure webhook delivery, SSRF protection, retry strategies
- `caching-strategies.md` - Russian Doll caching, Solid Cache, cache analysis
- `config-tips.md` - Configuration, logging, deployment patterns
- `structured-events.md` - Rails 8.1 `Rails.event` API for structured observability
- `resources.md` - Links to source material and further reading

## Philosophy Summary

1. **REST purity**: 7 actions only; new controllers for variations
2. **Fat models**: Authorization, broadcasting, business logic in models
3. **Thin controllers**: 1-5 line actions; extract complexity
4. **Convention over configuration**: Empty methods, implicit rendering
5. **Minimal abstractions**: No service objects for simple cases
6. **Current attributes**: Thread-local request context everywhere
7. **Hotwire-first**: Model-level broadcasting, Turbo Streams, Stimulus
8. **Readable code**: Semantic naming, small methods, no comments needed

## Success Indicators

Code aligns with DHH style when:

- [ ] Controllers map CRUD verbs to resources (no custom actions)
- [ ] Models use concerns for horizontal behavior sharing
- [ ] State uses records instead of boolean columns
- [ ] Abstractions remain minimal (no unnecessary service objects)
- [ ] Database backs solutions (Solid Queue/Cache, not Redis)
- [ ] Turbo/Stimulus handle all interactivity
- [ ] Authorization lives on User model (`can_*?` methods)
- [ ] Current attributes provide request context
- [ ] Scopes follow naming conventions (`chronologically`, `with_*`, etc.)
- [ ] Uses `pluck` over `map` for attribute extraction
- [ ] Current user resources use `My::` namespace
- [ ] Data computed at write time, not presentation
