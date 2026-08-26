---
name: hotwire-coder
description: "Use when implementing Hotwire features with Turbo Drive, Turbo Frames, and Turbo Streams. Applies Rails 8 conventions, morphing, broadcasts, lazy loading, and real-time update patterns."
---

# Hotwire Coder

## Hotwire Philosophy

Hotwire sends HTML over the wire instead of JSON:

- **Turbo Drive** - Accelerates navigation by replacing `<body>` without full page reloads
- **Turbo Frames** - Decompose pages into independent contexts that update on request
- **Turbo Streams** - Deliver partial page updates from server (HTTP or WebSocket)

## Turbo Drive

### Selective Opt-Out

```erb
<%= link_to "Download PDF", report_path(format: :pdf), data: { turbo: false } %>
<%= form_with model: @legacy, data: { turbo: false } do |f| %>
```

### Form Submissions

```ruby
def create
  @post = Post.new(post_params)
  @post.save ? redirect_to(@post, notice: "Created!") : render(:new, status: :unprocessable_entity)
end
```

## Turbo Frames

### Basic Frame

```erb
<turbo-frame id="comments">
  <%= render @post.comments %>
  <%= link_to "Load More", post_comments_path(@post, page: 2) %>
</turbo-frame>
```

### Lazy Loading

```erb
<turbo-frame id="notifications" src="<%= notifications_path %>" loading="lazy">
  <p>Loading...</p>
</turbo-frame>
```

See `references/lazy-loading.md` for skeleton UI patterns, infinite scroll, and Stimulus loading controllers.

### Breaking Out of Frames

```erb
<%= link_to "View Post", post_path(@post), data: { turbo_frame: "_top" } %>
<%= link_to "Results", search_path, data: { turbo_frame: "results" } %>
```

### Inline Editing Pattern

```erb
<turbo-frame id="<%= dom_id(post) %>">
  <article>
    <h2><%= post.title %></h2>
    <%= link_to "Edit", edit_post_path(post) %>
  </article>
</turbo-frame>
```

## Turbo Streams

### Stream Actions

```erb
<%= turbo_stream.append "comments" do %><%= render @comment %><% end %>
<%= turbo_stream.replace dom_id(@post) do %><%= render @post %><% end %>
<%= turbo_stream.remove dom_id(@comment) %>
```

### HTTP Stream Responses

```ruby
def create
  @comment = @post.comments.create(comment_params)
  respond_to do |format|
    format.turbo_stream  # renders create.turbo_stream.erb
    format.html { redirect_to @post }
  end
end
```

### Real-Time Broadcasts

```ruby
class Comment < ApplicationRecord
  after_create_commit -> {
    broadcast_append_to post, target: "comments", partial: "comments/comment"
  }
  after_update_commit -> { broadcast_replace_to post }
  after_destroy_commit -> { broadcast_remove_to post }
end
```

```erb
<%= turbo_stream_from @post %>
<div id="comments"><%= render @post.comments %></div>
```

> **Note:** For LLM streaming or features requiring message delivery guarantees, see `anycable-coder` skill. Action Cable provides at-most-once delivery which can lose chunks on reconnection.

## Turbo 8 Morphing

```erb
<head>
  <meta name="turbo-refresh-method" content="morph">
  <meta name="turbo-refresh-scroll" content="preserve">
</head>
```

```ruby
class Post < ApplicationRecord
  after_update_commit -> { broadcast_refresh_to self }
end
```

Use morphing refreshes for broad CRUD-ish pages where a server-rendered page refresh is simpler than manually coordinating many stream targets. For small, localized updates, targeted stream actions are still clearer.

## Realtime Architecture

Default to Turbo Streams for DOM changes. Add custom Action Cable channels only for small ephemeral signals such as presence, typing, or unread pings where rendering HTML would be wasteful.

Every stream name is an authorization boundary. Scope broadcasts by the tenant, account, room, or user that is allowed to see the update:

```ruby
broadcast_replace_to [ account, :cards ], target: dom_id(card)
broadcast_append_to [ user, :notifications ], target: "notifications"
```

Broadcast callbacks run outside the request context. Pass explicit locals to partials and avoid helpers that depend on controller instance variables or request-only state.

## Common Patterns

### Dialogs and Overlays

When the primary outcome is a modal, confirmation, toast, or slideover in a server-rendered Rails application, use `dialog-patterns`. Apply this skill only to the Turbo Frame or Turbo Stream mechanics that the dialog workflow needs.

### Infinite Scroll

```erb
<div id="posts"><%= render @posts %></div>
<% if @posts.next_page? %>
  <turbo-frame id="pagination" src="<%= posts_path(page: @posts.next_page) %>" loading="lazy">
    <p>Loading more...</p>
  </turbo-frame>
<% end %>
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Mismatched frame IDs | Silent failures | Validate IDs match |
| Missing status codes | Turbo ignores response | Use 422/303 correctly |
| Implicit locals in broadcasts | Runtime errors | Always pass `request_id: nil` |
| Tenant-unscoped stream names | Cross-account data leaks | Include tenant/user context in stream names |
| Action Cable for rendered HTML | Duplicates Turbo Streams | Broadcast server-rendered streams instead |
| Stimulus selectors for dynamic content | Misses broadcast-inserted elements | Use targets, values, and target callbacks |

## Debugging

```javascript
Turbo.setDebug(true)
document.addEventListener("turbo:frame-missing", (e) => console.error("Frame not found:", e.detail.response))
```

## Output Format

When implementing Hotwire features, provide:

1. **Controller** - Actions with proper response handling
2. **Views** - HTML/ERB with frames and streams
3. **Model** - Broadcast callbacks if real-time needed
4. **JavaScript** - Stimulus controllers if needed
