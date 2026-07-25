# Majestic Abilities

Portable agent skills organized by capability category and compatible with the Agent Skills format.

## Install

From this directory:

```sh
# List all available skills
npx skills add . --list

# Select skills interactively
npx skills add .

# Install every available skill
npx skills add . --skill '*'

# Install every Core skill directly from the category
npx skills add ./skills/core --skill '*'

# Install every DevOps skill directly from the category
npx skills add ./skills/devops --skill '*'

# Install every Cloudflare skill directly from the category
npx skills add ./skills/cloudflare --skill '*'

# Install every Engineer skill directly from the category
npx skills add ./skills/engineer --skill '*'

# Install every Frontend skill directly from the category
npx skills add ./skills/frontend --skill '*'

# Install every Rails skill directly from the category
npx skills add ./skills/rails --skill '*'

# Install every SEO skill directly from the category
npx skills add ./skills/seo --skill '*'
```

After this repository is published, replace `.` with its GitHub `owner/repo` identifier. A category can be selected with an `owner/repo/skills/<category>` source path.

## Catalog

| Category | Skills | Path |
| --- | ---: | --- |
| Cloudflare | 3 | [`skills/cloudflare/`](skills/cloudflare/) |
| Core | 2 | [`skills/core/`](skills/core/) |
| DevOps | 10 | [`skills/devops/`](skills/devops/) |
| Engineer | 4 | [`skills/engineer/`](skills/engineer/) |
| Frontend | 5 | [`skills/frontend/`](skills/frontend/) |
| Rails | 36 | [`skills/rails/`](skills/rails/) |
| SEO | 22 | [`skills/seo/`](skills/seo/) |

Core is a category for foundational repository capabilities, not a dependency required by other categories.

## Core Skills

| Skill | Description |
| --- | --- |
| [`agent-ready-repository`](skills/core/agent-ready-repository/) | Make repositories easier and safer for coding agents to navigate and modify. |
| [`agents-md-hierarchy`](skills/core/agents-md-hierarchy/) | Audit and refine nested repository guidance where local commands, rules, or boundaries differ. |

## Cloudflare Skills

| Skill | Description |
| --- | --- |
| [`cloudflare-infrastructure`](skills/cloudflare/cloudflare-infrastructure/) | Provision and review Cloudflare infrastructure with OpenTofu. |
| [`cloudflare-worker-development`](skills/cloudflare/cloudflare-worker-development/) | Build and review TypeScript applications for the Cloudflare Workers runtime. |
| [`cloudflare-workers-deployment`](skills/cloudflare/cloudflare-workers-deployment/) | Configure, validate, and deploy Cloudflare Workers with Wrangler. |

## DevOps Skills

| Skill | Description |
| --- | --- |
| [`ansible-server-configuration`](skills/devops/ansible-server-configuration/) | Configure and maintain servers with focused Ansible playbooks. |
| [`backblaze-b2-storage`](skills/devops/backblaze-b2-storage/) | Configure and operate Backblaze B2 storage. |
| [`cloud-init-provisioning`](skills/devops/cloud-init-provisioning/) | Provision virtual machines with small, testable cloud-init configurations. |
| [`digitalocean-infrastructure`](skills/devops/digitalocean-infrastructure/) | Provision and review DigitalOcean infrastructure with OpenTofu. |
| [`hetzner-infrastructure`](skills/devops/hetzner-infrastructure/) | Provision and review Hetzner Cloud infrastructure with OpenTofu. |
| [`infrastructure-review`](skills/devops/infrastructure-review/) | Review infrastructure changes for correctness, maintainability, simplicity, and deployment risk. |
| [`infrastructure-security-review`](skills/devops/infrastructure-security-review/) | Review infrastructure as code for exploitable security failures. |
| [`kamal-deploy`](skills/devops/kamal-deploy/) | Deploy and operate Rails applications with Kamal 2. |
| [`onepassword-secrets`](skills/devops/onepassword-secrets/) | Load and inject secrets with the 1Password CLI. |
| [`opentofu-iac`](skills/devops/opentofu-iac/) | Build and maintain infrastructure as code with OpenTofu and HCL. |

## Engineer Skills

| Skill | Description |
| --- | --- |
| [`complexity-reviewer`](skills/engineer/complexity-reviewer/) | Review algorithmic complexity and performance hotspots conservatively. |
| [`plan-review`](skills/engineer/plan-review/) | Challenge implementation plans before coding starts. |
| [`structured-logging`](skills/engineer/structured-logging/) | Design structured application logging for observability and incidents. |
| [`test-reviewer`](skills/engineer/test-reviewer/) | Review automated tests for behavioral coverage and reliability. |

## Frontend Skills

| Skill | Description |
| --- | --- |
| [`frontend-design`](skills/frontend/frontend-design/) | Choose a coherent visual direction and implement production-grade interfaces. |
| [`frontend-performance`](skills/frontend/frontend-performance/) | Prevent and diagnose Core Web Vitals regressions. |
| [`pr-screenshot-docs`](skills/frontend/pr-screenshot-docs/) | Capture and document visual changes for pull-request review. |
| [`ui-code-auditor`](skills/frontend/ui-code-auditor/) | Audit frontend source for accessibility, quality, and performance problems. |
| [`visual-validator`](skills/frontend/visual-validator/) | Validate rendered UI changes against their intended goals. |

## Rails Skills

| Skill | Description |
| --- | --- |
| [`aasm-coder`](skills/rails/aasm-coder/) | Implement state machines with AASM for workflow management. |
| [`action-mailer-coder`](skills/rails/action-mailer-coder/) | Create or refactor Action Mailer emails. |
| [`action-policy-coder`](skills/rails/action-policy-coder/) | Implement authorization with Action Policy. |
| [`active-interaction-coder`](skills/rails/active-interaction-coder/) | Implement typed business operations with ActiveInteraction. |
| [`active-job-coder`](skills/rails/active-job-coder/) | Create or refactor Active Job background jobs. |
| [`anycable-coder`](skills/rails/anycable-coder/) | Implement reliable real-time features with AnyCable. |
| [`anyway-config-coder`](skills/rails/anyway-config-coder/) | Implement type-safe configuration with `anyway_config`. |
| [`business-logic-coder`](skills/rails/business-logic-coder/) | Route Rails business logic to the simplest fitting home. |
| [`constraints-reviewer`](skills/rails/constraints-reviewer/) | Review data constraints and referential integrity. |
| [`dhh-rails-style`](skills/rails/dhh-rails-style/) | Write and review Rails code using DHH and 37signals conventions. |
| [`dialog-patterns`](skills/rails/dialog-patterns/) | Build native HTML dialogs with Turbo and Stimulus. |
| [`event-sourcing-coder`](skills/rails/event-sourcing-coder/) | Record domain events for side effects, audit trails, and activity feeds. |
| [`gem-builder`](skills/rails/gem-builder/) | Build production-quality Ruby gems. |
| [`graphql-architect`](skills/rails/graphql-architect/) | Design GraphQL APIs with `graphql-ruby`. |
| [`hotwire-coder`](skills/rails/hotwire-coder/) | Implement Turbo Drive, Frames, and Streams. |
| [`inertia-coder`](skills/rails/inertia-coder/) | Build Rails applications with Inertia.js and React, Vue, or Svelte. |
| [`layered-rails`](skills/rails/layered-rails/) | Design Rails applications with explicit architectural layers. |
| [`rails-lint`](skills/rails/rails-lint/) | Run and fix RuboCop, ERB Lint, and Brakeman findings in Rails projects. |
| [`litestream-coder`](skills/rails/litestream-coder/) | Configure Litestream backups for Rails SQLite databases. |
| [`mcp-oauth-setup`](skills/rails/mcp-oauth-setup/) | Implement MCP server authentication and OAuth registration. |
| [`minitest-coder`](skills/rails/minitest-coder/) | Write Minitest tests for Ruby and Rails. |
| [`performance-reviewer`](skills/rails/performance-reviewer/) | Review Rails code for query, memory, locking, and throughput problems. |
| [`pragmatic-rails-reviewer`](skills/rails/pragmatic-rails-reviewer/) | Review Rails changes for regressions, maintainability, and conventions. |
| [`privacy-reviewer`](skills/rails/privacy-reviewer/) | Review PII handling, encryption, and privacy compliance. |
| [`rails-activity-timeline`](skills/rails/rails-activity-timeline/) | Add polymorphic activity timelines with Turbo Stream updates. |
| [`rails-authentication-coder`](skills/rails/rails-authentication-coder/) | Implement Rails 8 native authentication. |
| [`rails-debugger`](skills/rails/rails-debugger/) | Diagnose Rails errors, failing tests, and unexpected behavior. |
| [`rails-refactorer`](skills/rails/rails-refactorer/) | Refactor Rails code while preserving behavior. |
| [`ruby-coder`](skills/rails/ruby-coder/) | Write modern, idiomatic Ruby. |
| [`simplicity-reviewer`](skills/rails/simplicity-reviewer/) | Review code for unnecessary complexity and YAGNI violations. |
| [`solid-cache-coder`](skills/rails/solid-cache-coder/) | Configure and use Solid Cache. |
| [`solid-queue-coder`](skills/rails/solid-queue-coder/) | Configure and use Solid Queue. |
| [`stimulus-coder`](skills/rails/stimulus-coder/) | Create or refactor Stimulus controllers. |
| [`store-model-coder`](skills/rails/store-model-coder/) | Model typed JSON attributes with `store_model`. |
| [`tailwind-coder`](skills/rails/tailwind-coder/) | Style Rails views with Tailwind CSS. |
| [`viewcomponent-coder`](skills/rails/viewcomponent-coder/) | Build component-based Rails interfaces with ViewComponent. |

## SEO Skills

| Skill | Description |
| --- | --- |
| [`aeo-scorecard`](skills/seo/aeo-scorecard/) | Measure Answer Engine Optimization visibility, share of voice, citations, and referral demand. |
| [`ai-crawler-readiness`](skills/seo/ai-crawler-readiness/) | Configure HTTP-layer signals for LLM discovery, crawling, content negotiation, and referral measurement. |
| [`analyst-positioning`](skills/seo/analyst-positioning/) | Position people as recognizable industry experts with stronger authority and citation signals. |
| [`behavioral-seo`](skills/seo/behavioral-seo/) | Improve behavioral search signals such as click-through rate, dwell time, and engagement. |
| [`bofu-keywords`](skills/seo/bofu-keywords/) | Find and prioritize bottom-of-funnel keywords with strong purchase intent. |
| [`buyer-journey-mapper`](skills/seo/buyer-journey-mapper/) | Map personas and buyer stages into an answer-focused content matrix. |
| [`eeat-analyzer`](skills/seo/eeat-analyzer/) | Audit and improve Experience, Expertise, Authority, and Trust signals. |
| [`entity-triplets`](skills/seo/entity-triplets/) | Build consistent entity relationships that search engines and LLMs can recognize. |
| [`geo-content-optimizer`](skills/seo/geo-content-optimizer/) | Structure content for extraction and citation by ChatGPT, Perplexity, Gemini, and similar systems. |
| [`keyword-research`](skills/seo/keyword-research/) | Discover and prioritize content topics without expensive SEO tools. |
| [`keyword-strategist`](skills/seo/keyword-strategist/) | Analyze keyword usage and suggest semantic variations and related terms. |
| [`llms-txt-builder`](skills/seo/llms-txt-builder/) | Generate an `llms.txt` file that helps AI systems navigate a site. |
| [`meta-optimizer`](skills/seo/meta-optimizer/) | Create optimized meta titles, descriptions, and URL suggestions. |
| [`press-release-aeo`](skills/seo/press-release-aeo/) | Frame press releases for AI citation, authority building, and newswire distribution. |
| [`query-expansion-strategy`](skills/seo/query-expansion-strategy/) | Expand content coverage across LLM sub-questions and semantic query variations. |
| [`review-management`](skills/seo/review-management/) | Improve review presence and use customer-generated content as trust and recommendation signals. |
| [`schema-architect`](skills/seo/schema-architect/) | Create and audit Schema.org JSON-LD for rich results, AI Overviews, and search indexing. |
| [`seo-audit`](skills/seo/seo-audit/) | Audit technical SEO, content quality, E-E-A-T, and AI citation readiness. |
| [`seo-content`](skills/seo/seo-content/) | Produce a search-optimized content asset from opportunity selection through auditing and tracking. |
| [`snippet-hunter`](skills/seo/snippet-hunter/) | Format content for featured snippets and other search-result features. |
| [`structure-architect`](skills/seo/structure-architect/) | Improve headings, content structure, schema markup, and internal linking. |
| [`topical-authority`](skills/seo/topical-authority/) | Plan content clusters, identify coverage gaps, and build measurable topical authority. |

## Layout

```text
skills/
  <category>/
    <skill-name>/
      SKILL.md
      references/  # optional
      scripts/     # optional
      assets/      # optional
```

Each skill is self-contained. Category directories provide catalog organization and category-scoped installation, while installed skills are flattened into each agent's native skill directory.
