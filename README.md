# Majestic Abilities

Portable agent skills organized by capability category and compatible with the Agent Skills format.

## Install With `npx skills`

The [Vercel Skills CLI](https://github.com/vercel-labs/skills) discovers every `SKILL.md` in this repository. You can install one skill, a whole category, or the complete catalog.

### Choose A Source

Use the local checkout while developing this repository:

```sh
# Run from the repository root
npx skills add . --list
```

After publication, use the GitHub repository identifier instead:

```sh
npx skills add OWNER/REPOSITORY --list
```

Replace `OWNER/REPOSITORY` in the examples below with the published repository identifier.

### Install Into A Project

Project scope is the default. Run the command from the project that should receive the skills.

```sh
# Install one skill for Claude Code
npx skills add OWNER/REPOSITORY --skill code-review --agent claude-code --yes

# Install one skill for Codex
npx skills add OWNER/REPOSITORY --skill code-review --agent codex --yes

# Install one skill for Pi
npx skills add OWNER/REPOSITORY --skill code-review --agent pi --yes

# Install the selected skill for all three agents
npx skills add OWNER/REPOSITORY \
  --skill code-review \
  --agent claude-code codex pi \
  --yes
```

The CLI uses these project locations:

| Agent | CLI identifier | Project directory |
| --- | --- | --- |
| Claude Code | `claude-code` | `.claude/skills/` |
| Codex | `codex` | `.agents/skills/` |
| Pi | `pi` | `.pi/skills/` |

Omit `--agent` to choose from detected agents interactively.

### Install For The Current User

Add `--global` (or `-g`) to make skills available across projects:

```sh
# Install one skill globally for Claude Code
npx skills add OWNER/REPOSITORY \
  --skill code-review \
  --agent claude-code \
  --global \
  --yes

# Install one skill globally for Codex and Pi
npx skills add OWNER/REPOSITORY \
  --skill code-review \
  --agent codex pi \
  --global \
  --yes
```

Global installations normally resolve to:

| Agent | User directory |
| --- | --- |
| Claude Code | `~/.claude/skills/` |
| Codex | `$CODEX_HOME/skills/`, normally `~/.codex/skills/` |
| Pi | `~/.pi/agent/skills/` |

### Install A Category

Point the CLI at a category directory and select every discovered skill:

```sh
# From a local checkout
npx skills add ./skills/engineer \
  --skill '*' \
  --agent claude-code codex pi \
  --yes

# From GitHub
npx skills add https://github.com/OWNER/REPOSITORY/tree/master/skills/engineer \
  --skill '*' \
  --agent claude-code codex pi \
  --yes
```

Add `--global` to either command for a user-level category installation.

### Install The Complete Catalog

```sh
# Project installation
npx skills add OWNER/REPOSITORY \
  --skill '*' \
  --agent claude-code codex pi \
  --yes

# User installation
npx skills add OWNER/REPOSITORY \
  --skill '*' \
  --agent claude-code codex pi \
  --global \
  --yes
```

### Manage Installed Skills

```sh
# List project skills for one agent
npx skills list --agent claude-code

# List global skills
npx skills list --global

# Update project or global installations
npx skills update --project --yes
npx skills update --global --yes

# Remove one skill from one agent
npx skills remove code-review --agent claude-code --yes
```

The CLI recommends symlinks so multiple agents share one canonical installation. Add `--copy` when symlinks are unavailable or the project requires materialized skill files.

## Catalog

| Category | Skills | Path |
| --- | ---: | --- |
| Cloudflare | 3 | [`skills/cloudflare/`](skills/cloudflare/) |
| Core | 2 | [`skills/core/`](skills/core/) |
| Data | 8 | [`skills/data/`](skills/data/) |
| DevOps | 10 | [`skills/devops/`](skills/devops/) |
| Engineer | 7 | [`skills/engineer/`](skills/engineer/) |
| Founder | 7 | [`skills/founder/`](skills/founder/) |
| Frontend | 5 | [`skills/frontend/`](skills/frontend/) |
| Marketing | 13 | [`skills/marketing/`](skills/marketing/) |
| Misc | 2 | [`skills/misc/`](skills/misc/) |
| Product | 8 | [`skills/product/`](skills/product/) |
| Rails | 36 | [`skills/rails/`](skills/rails/) |
| Reasoning | 3 | [`skills/reasoning/`](skills/reasoning/) |
| Sales | 6 | [`skills/sales/`](skills/sales/) |
| SEO | 22 | [`skills/seo/`](skills/seo/) |
| Writing | 10 | [`skills/writing/`](skills/writing/) |

Core is a category for foundational repository capabilities, not a dependency required by other categories. Misc is a temporary holding category for useful portable skills whose long-term domain is still undecided, not a destination for low-value leftovers.

Multi-step workflows that compose these skills live in [`cookbooks/`](cookbooks/), described below.

## Core Skills

| Skill | Description |
| --- | --- |
| [`agent-ready-repository`](skills/core/agent-ready-repository/) | Make repositories easier and safer for coding agents to navigate and modify. |
| [`agents-md-hierarchy`](skills/core/agents-md-hierarchy/) | Audit and refine nested repository guidance where local commands, rules, or boundaries differ. |

## Data Skills

| Skill | Description |
| --- | --- |
| [`anomaly-detection`](skills/data/anomaly-detection/) | Design and evaluate anomaly detection using context-appropriate baselines and methods. |
| [`csv-wrangling`](skills/data/csv-wrangling/) | Recover messy delimited files without silently dropping or corrupting records. |
| [`data-pipeline-design`](skills/data/data-pipeline-design/) | Design reliable batch or incremental pipelines with explicit recovery and reconciliation behavior. |
| [`data-pipeline-testing`](skills/data/data-pipeline-testing/) | Test transformations, contracts, incrementality, replay, and failure recovery. |
| [`data-quality`](skills/data/data-quality/) | Define and operate quality controls, service levels, scorecards, and incident response. |
| [`data-source-assessment`](skills/data/data-source-assessment/) | Assess unfamiliar sources for schema, grain, change behavior, quality, and extraction constraints. |
| [`data-validation`](skills/data/data-validation/) | Design executable contracts across records, DataFrames, warehouses, and pipeline boundaries. |
| [`dbt-development`](skills/data/dbt-development/) | Build and review dbt projects, models, tests, materializations, and documentation. |

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
| [`code-review`](skills/engineer/code-review/) | Review change sets for defects, regressions, unnecessary complexity, missing tests, and release readiness. |
| [`complexity-reviewer`](skills/engineer/complexity-reviewer/) | Review algorithmic complexity and performance hotspots conservatively. |
| [`implementation-planning`](skills/engineer/implementation-planning/) | Create an executable technical plan grounded in the existing repository. |
| [`multi-agent-architecture`](skills/engineer/multi-agent-architecture/) | Design persistent multi-agent systems with explicit roles, handoffs, state, permissions, and failure handling. |
| [`plan-review`](skills/engineer/plan-review/) | Review planning documents for readiness, implementation risk, unnecessary scope, and verification gaps. |
| [`structured-logging`](skills/engineer/structured-logging/) | Design structured application logging for observability and incidents. |
| [`test-reviewer`](skills/engineer/test-reviewer/) | Review automated tests for behavioral coverage and reliability. |

## Founder Skills

| Skill | Description |
| --- | --- |
| [`bootstrapped-finance`](skills/founder/bootstrapped-finance/) | Analyze cash runway, burn, unit economics, working capital, hiring ROI, and spending tradeoffs for bootstrapped companies. |
| [`company-strategy`](skills/founder/company-strategy/) | Build future-back company strategy with explicit horizons, dependencies, bets, and revisit triggers. |
| [`founder-priorities`](skills/founder/founder-priorities/) | Turn competing priorities and calendar load into a stage-fit operating plan with tradeoffs and revisit criteria. |
| [`fundraising-ask-review`](skills/founder/fundraising-ask-review/) | Review an existing fundraising ask for round coherence, evidence-backed claims, and investor relevance. |
| [`go-to-market-motion`](skills/founder/go-to-market-motion/) | Choose and phase a route to market that fits buying behavior, economics, stage, and capacity. |
| [`launch-legal-checklist`](skills/founder/launch-legal-checklist/) | Identify launch legal unknowns, escalation points, and next actions without implying legal clearance. |
| [`launch-readiness`](skills/founder/launch-readiness/) | Return a blunt go, narrow, or delay recommendation for a founder-led launch. |

## Frontend Skills

| Skill | Description |
| --- | --- |
| [`frontend-design`](skills/frontend/frontend-design/) | Choose a coherent visual direction and implement production-grade interfaces. |
| [`frontend-performance`](skills/frontend/frontend-performance/) | Prevent and diagnose Core Web Vitals regressions. |
| [`pr-screenshot-docs`](skills/frontend/pr-screenshot-docs/) | Capture and document visual changes for pull-request review. |
| [`ui-code-auditor`](skills/frontend/ui-code-auditor/) | Audit frontend source for accessibility, quality, and performance problems. |
| [`visual-validator`](skills/frontend/visual-validator/) | Validate rendered UI changes against their intended goals. |

## Marketing Skills

| Skill | Description |
| --- | --- |
| [`brand-naming`](skills/marketing/brand-naming/) | Generate and evaluate brand, company, product, and feature names with verification checks. |
| [`brand-positioning`](skills/marketing/brand-positioning/) | Define evidence-backed positioning, differentiation, value propositions, messaging angles, and taglines. |
| [`community-participation`](skills/marketing/community-participation/) | Plan transparent, value-first participation in online communities within current local rules. |
| [`content-repurposing`](skills/marketing/content-repurposing/) | Adapt one verified long-form asset into channel-appropriate derivative content. |
| [`customer-case-study`](skills/marketing/customer-case-study/) | Turn verified customer outcomes and approved quotations into an evidence-safe case study and proof assets. |
| [`editorial-planning`](skills/marketing/editorial-planning/) | Generate, evaluate, prioritize, and schedule audience-led content ideas and a production calendar. |
| [`growth-experimentation`](skills/marketing/growth-experimentation/) | Run marketing experiments with explicit hypotheses, guardrails, and evidence-based decisions. |
| [`market-research`](skills/marketing/market-research/) | Research markets, audiences, competitors, and customer language into a decision-ready report. |
| [`newsletter-editorial`](skills/marketing/newsletter-editorial/) | Plan and draft a recurring newsletter with a clear editorial promise and source discipline. |
| [`offer-design`](skills/marketing/offer-design/) | Design truthful commercial and lead-generation offers before final copy. |
| [`paid-search`](skills/marketing/paid-search/) | Plan paid-search campaigns using current platform behavior, measurement, and spend controls. |
| [`social-content`](skills/marketing/social-content/) | Plan and draft professional social posts and X threads without relying on algorithm folklore. |
| [`youtube-packaging`](skills/marketing/youtube-packaging/) | Analyze normalized YouTube outliers and develop ownable title and thumbnail hypotheses. |

## Misc Skills

| Skill | Description |
| --- | --- |
| [`skill-grader`](skills/misc/skill-grader/) | Grade skill executions against expectations using transcript and output evidence. |
| [`skill-structure`](skills/misc/skill-structure/) | Decide whether guidance should become an Agent Skill and design a compliant structure when justified. |

## Product Skills

| Skill | Description |
| --- | --- |
| [`feature-brief`](skills/product/feature-brief/) | Write a compact feature brief or decision document before a full specification. |
| [`lifecycle-retention`](skills/product/lifecycle-retention/) | Design lifecycle stages, health signals, onboarding, early warnings, and retention interventions. |
| [`north-star-metric`](skills/product/north-star-metric/) | Choose and operate one stage-fit product health metric with drivers and guardrails. |
| [`pricing-strategy`](skills/product/pricing-strategy/) | Design pricing and packaging from value, evidence, costs, and expansion logic. |
| [`product-discovery`](skills/product/product-discovery/) | Plan interviews, map assumptions, and frame Jobs-to-be-Done before defining a solution. |
| [`product-planning`](skills/product/product-planning/) | Prioritize opportunities and build an outcome-based Now, Next, Later roadmap. |
| [`product-requirements`](skills/product/product-requirements/) | Write an evidence-grounded PRD with testable requirements, scope, and success measures. |
| [`product-validation`](skills/product/product-validation/) | Pressure-test demand and define the smallest test for the riskiest product assumption. |

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

## Reasoning Skills

| Skill | Description |
| --- | --- |
| [`devils-advocate`](skills/reasoning/devils-advocate/) | Pressure-test a preferred approach before commitment. |
| [`premortem`](skills/reasoning/premortem/) | Convert plausible future failure stories into safeguards for a concrete plan. |
| [`reasoning-verifier`](skills/reasoning/reasoning-verifier/) | Trace requirements, evidence, and assumptions into a completed conclusion. |

## Sales Skills

| Skill | Description |
| --- | --- |
| [`account-expansion`](skills/sales/account-expansion/) | Grow existing accounts through value reviews, expansion triggers, win-back, and referral asks. |
| [`icp-definition`](skills/sales/icp-definition/) | Define and validate an Ideal Customer Profile with fit criteria, disqualifiers, and account scoring. |
| [`outbound-prospecting`](skills/sales/outbound-prospecting/) | Design and diagnose evidence-safe outbound sequences across multiple channels. |
| [`pipeline-analysis`](skills/sales/pipeline-analysis/) | Diagnose pipeline health, challenge forecasts, and assign corrective actions. |
| [`sales-enablement`](skills/sales/sales-enablement/) | Build a B2B playbook for discovery, demos, objections, competition, and closing. |
| [`sales-proposal`](skills/sales/sales-proposal/) | Write a complete evidence-based commercial proposal after qualified discovery. |

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
| [`keyword-research`](skills/seo/keyword-research/) | Discover and prioritize search-led content topics against real queries without expensive SEO tools. |
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

## Writing Skills

| Skill | Description |
| --- | --- |
| [`brand-voice`](skills/writing/brand-voice/) | Define an aspirational organizational voice from brand strategy, audience, and desired perception. |
| [`content-writer`](skills/writing/content-writer/) | Draft source-grounded general articles and guides through a brief, outline, and section workflow. |
| [`copy-editor`](skills/writing/copy-editor/) | Diagnose and prioritize grammar, clarity, structure, attribution, voice, and style problems in existing prose. |
| [`direct-response-copy`](skills/writing/direct-response-copy/) | Create evidence-safe conversion-oriented landing pages, sales emails, CTAs, ads, and product microcopy. |
| [`headline-generator`](skills/writing/headline-generator/) | Generate and recommend fact-bound headline, title, and subject-line candidates from supplied evidence. |
| [`minto-pyramid`](skills/writing/minto-pyramid/) | Restructure complex writing around one governing answer, supporting arguments, and matched evidence. |
| [`prose-reviser`](skills/writing/prose-reviser/) | Rewrite existing prose for clarity, natural rhythm, and author fidelity while preserving facts and uncertainty. |
| [`style-forensics`](skills/writing/style-forensics/) | Measure and explain prose style with quantitative metrics and cited examples. |
| [`style-writer`](skills/writing/style-writer/) | Draft and revise prose against an existing voice profile while preserving facts and readability. |
| [`voice-dna-kit`](skills/writing/voice-dna-kit/) | Capture an existing personal or organizational writing voice as reusable guidance. |

## Cookbooks

Cookbooks are recipes: user-invoked workflow skills that sequence catalog skills by name (plan, implement, quality gates). They live in [`cookbooks/`](cookbooks/) rather than `skills/` because they follow a different contract: catalog skills are decoupled and never reference each other, while cookbooks reference the skills they orchestrate and declare them in a `## Requires` section.

| Cookbook | Description |
| --- | --- |
| [`ai-search-visibility-foundation`](cookbooks/ai-search-visibility-foundation/) | Establish a site's SEO, entity, AI navigation, crawler, structured-data, and AEO measurement foundations. |
| [`founder-launch-decision`](cookbooks/founder-launch-decision/) | Turn a founder-led launch proposal into a defensible audience, motion, legal-unknown inventory, and launch verdict. |
| [`product-engineering-handoff`](cookbooks/product-engineering-handoff/) | Turn an approved product direction into a PRD, repository-grounded implementation plan, and reviewed engineering handoff. |
| [`rails-feature`](cookbooks/rails-feature/) | Build a Rails feature end-to-end: plan, implement in DHH style with TDD, then pass lint, test, and review quality gates. |

Cookbooks install like any other skill, but always install their required skills alongside them (the CLI does not resolve dependencies). Each cookbook lists its complete install command. `scripts/check-cookbooks.sh` verifies that every referenced skill exists; run it before committing cookbook changes. See [`cookbooks/README.md`](cookbooks/README.md) for the full contract and authoring guide.

## Layout

```text
skills/
  <category>/
    <skill-name>/
      SKILL.md
      references/  # optional
      scripts/     # optional
      assets/      # optional
cookbooks/
  <cookbook-name>/
    SKILL.md
scripts/
  check-cookbooks.sh
```

Each skill is self-contained. Category directories provide catalog organization and category-scoped installation, while installed skills are flattened into each agent's native skill directory. Cookbooks are the composition layer: they may reference catalog skills by name, and `scripts/check-cookbooks.sh` keeps those references honest.
