# DHH Rails Review Lens

Use this reference as a strict Rails simplicity lens inside `pragmatic-rails-reviewer`.

## Review Bias

- convention over configuration
- server-rendered Rails and Hotwire before SPA complexity
- ActiveRecord before repository layers
- model/domain behavior before anemic services
- fixtures before heavy factory ceremony when the app can support it
- standard Rails sessions before token machinery in ordinary Rails apps

## Common Violations

| Anti-Pattern | Rails-First Alternative |
| --- | --- |
| Custom controller actions everywhere | Dedicated RESTful controllers |
| Repository pattern over ActiveRecord | Use scopes, associations, and query objects only when needed |
| Logic-heavy partials | Helpers, ViewComponents, or clearer model methods |
| Service objects for every action | Model methods or interactions only when orchestration is real |
| GraphQL or API layer by default | Standard Rails routes and server-rendered flows |
| JavaScript state framework for basic UI | Hotwire, Stimulus, and server-rendered state |

## Output Discipline

Report problems and fixes. Do not pad reviews with praise sections when the task is code review.
