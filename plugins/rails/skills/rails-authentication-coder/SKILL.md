---
name: rails-authentication-coder
description: "Use when implementing Rails 8 built-in authentication, session management, admin sign-in, password reset, or protecting Rails controllers without Devise."
---

# Rails Authentication Coder

Implement authentication with Rails 8 native primitives, not Devise, unless the project explicitly requires another auth library.

## Default approach

1. Inspect the app first:
   - `Gemfile` for auth gems
   - `app/models`, `app/controllers`, `config/routes.rb`
   - `app/controllers/concerns/authentication.rb`, `app/models/current.rb`, `app/models/session.rb`
   - existing `User`, `Admin`, or account models
2. If no auth exists, use Rails 8 generated authentication as the base implementation.
3. For admin-only auth, prefer a separate `Admin` model when product scope says admins are distinct from visitors/users.
4. Do not add Devise.
5. Keep public visitor routes unauthenticated; protect only admin/control surfaces.
6. Use Minitest for coverage.

## Rails 8 native authentication workflow

Use the generator as the source of Rails-conventional files, then adapt names only as needed:

```bash
bin/rails generate authentication
```

If the app needs a separate `Admin` model, verify whether the current Rails generator supports model-name arguments in this app/version. If not, generate in the task worktree and rename/adapt the generated `User` model, controller helpers, routes, fixtures, and tests to `Admin` deliberately.

Expected concepts from native auth:

- password digest via `has_secure_password`
- `Session` records for browser sessions
- `Current` for request-local session/admin state
- `Authentication` controller concern
- sign-in/sign-out routes and views
- password reset flow if generated/needed

## Admin-specific pattern

For admin-only access:

- Model: `Admin`, not `User`, when the product distinguishes admins from visitors.
- Session should resolve to `Current.admin` or equivalent, not `Current.user`.
- Public controllers should opt out of authentication or avoid including admin authentication.
- Admin-only surfaces should require authentication, e.g. RailsPress admin, `/admin/*`, or dashboard controllers.
- Seed or document how the first admin is created without exposing open registration.

Avoid open public admin registration unless explicitly accepted. Prefer one of:

- seed first admin from credentials/env in development/staging
- Rails console creation documented for production
- invite-only creation behind authenticated admin UI later

## Protecting mounted engines

For a mounted engine such as RailsPress:

1. Check whether the engine offers a host auth hook/concern. Prefer that over path checks.
2. If using a path guard, scope it tightly to admin paths only, e.g. `/railspress/admin`.
3. Verify public blog/post routes remain accessible to visitors.
4. Test unauthenticated admin access redirects to sign-in.
5. Test authenticated admin access succeeds.

## Acceptance tests to add

Minimum Minitest coverage:

- admin can sign in with valid credentials
- invalid credentials do not sign in
- admin can sign out
- unauthenticated visitor cannot access protected admin/RailsPress admin path
- authenticated admin can access protected admin/RailsPress admin path
- public visitor pages remain accessible without sign-in

## Verification commands

Run the smallest relevant checks while developing, then full project checks before PR:

```bash
bin/rails test test/models/admin_test.rb test/controllers/sessions_controller_test.rb
bin/rails test
bin/ci
```

If the local Ruby/Bundler environment is not prepared, fix that first or report the exact blocker output.

## PR requirements

PR body must include:

- auth model choice and why (`Admin` vs `User`)
- whether Rails 8 generator was used directly or adapted
- how first admin is created
- protected routes/surfaces
- test commands and real results
- linked task/card

## Pitfalls

- Do not expose a public sign-up path for admins by accident.
- Do not authenticate the whole application if visitors must browse public pages.
- Do not leave mounted admin engines public.
- Do not mix `User` and `Admin` names casually; choose one model boundary and keep helpers/routes/tests consistent.
- Do not store default passwords in code.
