# Hotwire Lazy Loading

Use lazy frames when the content is optional, expensive, or secondary to the first paint.

## Good Fits

- dashboards with side panels
- activity feeds or notifications
- infinite scroll pagination
- modals or drawers loaded on demand

## Pattern

```erb
<%= turbo_frame_tag "notifications",
                    src: notifications_path,
                    loading: :lazy do %>
  <%= render "shared/skeleton_rows" %>
<% end %>
```

## Rules

- Render a meaningful placeholder while the frame loads.
- Keep the lazy endpoint frame-safe and cheap.
- Preserve pagination state explicitly for infinite scroll.
- Break out with `_top` when the response should leave the frame context.
