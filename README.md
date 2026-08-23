# Majestic Abilities

Portable agent skills organized by capability category and compatible with the Agent Skills format.

Each category is an Agent Plugins 1.0.0 package and a separately installable native plugin for Claude Code and Codex, so you load only the categories you work in. The same skills also install individually with the Vercel Skills CLI for Claude Code, Codex, and Pi.

## Agent Plugins

Each `plugins/<category>/` directory contains a portable root `plugin.json` and discovers skills from the standard `skills/<skill-name>/SKILL.md` location. Agent Plugins defines the package format, not marketplace distribution, so the Claude Code and Codex manifests and marketplaces remain available for their native install routes.

The root `plugin.json` is authoritative for metadata shared by the portable, Claude Code, and Codex manifests. Category versions are independent. Update a category's root and native manifest versions together, plus each marketplace entry that carries the version.

Install the portable validation dependency with `python3 -m pip install -r requirements-dev.txt`, then run `scripts/check-agent-plugins.sh`.

## Install As Claude Code Plugins

This repository is a plugin marketplace. Add it once, then install one plugin per category you need:

```sh
/plugin marketplace add OWNER/REPOSITORY
/plugin install majestic-rails@majestic-abilities
/plugin install majestic-engineer@majestic-abilities
```

Replace `OWNER/REPOSITORY` with the published repository identifier. Use an absolute path instead while developing from a local checkout.

| Plugin | Skills | Contents |
| --- | ---: | --- |
| `majestic-cloudflare` | 13 | Cloudflare platform, Workers, Agents SDK, Durable Objects, Sandbox SDK, Cloudflare One, Email, Turnstile, infrastructure, and deployment |
| `majestic-core` | 2 | Agent-ready repositories and nested guidance audits |
| `majestic-data` | 8 | Pipelines, contracts, quality controls, dbt |
| `majestic-devops` | 10 | OpenTofu, Ansible, cloud-init, Kamal, secrets, infrastructure review |
| `majestic-engineer` | 9 | Minimal sufficient work, implementation planning, task decomposition, code and test review, complexity, logging |
| `majestic-founder` | 9 | Strategy, plan review, priorities, finance, technology impact, go-to-market, launch readiness |
| `majestic-frontend` | 5 | Visual direction, Core Web Vitals, accessibility, screenshots |
| `majestic-marketing` | 13 | Positioning, naming, content, campaigns, growth experiments |
| `majestic-misc` | 4 | Actionable communication, visual explanations, skill grading, and skill structure design |
| `majestic-product` | 14 | Discovery, workflow mapping, decision alignment, requirements, roadmaps, pricing, retention |
| `majestic-rails` | 36 | Rails and Ruby implementation, Hotwire, Solid, testing, review |
| `majestic-reasoning` | 4 | Decision retrospectives, devil's advocate, premortem, reasoning verification |
| `majestic-sales` | 6 | ICP, outbound, pipeline, enablement, proposals, expansion |
| `majestic-seo` | 23 | Technical SEO, content strategy, schema, AEO, plus the `ai-search-visibility-foundation` cookbook |
| `majestic-writing` | 10 | Voice capture, brand voice, copy editing, direct response, Minto |

Plugin skills are namespaced, so `dhh-rails-style` from `majestic-rails` is invoked as `/majestic-rails:dhh-rails-style`. Each plugin's skill descriptions are always in context once enabled, so installing only the categories you use keeps that cost proportional: `claude plugin details <name>` reports the projected token cost before you commit.

Manage installed plugins with `/plugin`, `claude plugin list`, and `claude plugin uninstall <name>`.

## Install As Codex Plugins

This repository also includes a repo-scoped Codex marketplace at `.agents/plugins/marketplace.json`.
From the repository root, add it to Codex and inspect the available plugins:

```sh
codex plugin marketplace add .
codex plugin list --marketplace majestic-abilities-codex --available
```

Install one category with:

```sh
codex plugin add majestic-rails@majestic-abilities-codex
codex plugin add majestic-engineer@majestic-abilities-codex
```

The Codex package for each category is declared in `plugins/<category>/.codex-plugin/plugin.json` and shares that category's existing `skills/` directory. The Claude Code manifests and marketplace remain available separately.

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
npx skills add ./plugins/engineer/skills \
  --skill '*' \
  --agent claude-code codex pi \
  --yes

# From GitHub
npx skills add https://github.com/OWNER/REPOSITORY/tree/master/plugins/engineer/skills \
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
| Cloudflare | 13 | [`plugins/cloudflare/skills/`](plugins/cloudflare/skills/) |
| Core | 2 | [`plugins/core/skills/`](plugins/core/skills/) |
| Data | 8 | [`plugins/data/skills/`](plugins/data/skills/) |
| DevOps | 10 | [`plugins/devops/skills/`](plugins/devops/skills/) |
| Engineer | 9 | [`plugins/engineer/skills/`](plugins/engineer/skills/) |
| Founder | 9 | [`plugins/founder/skills/`](plugins/founder/skills/) |
| Frontend | 5 | [`plugins/frontend/skills/`](plugins/frontend/skills/) |
| Marketing | 13 | [`plugins/marketing/skills/`](plugins/marketing/skills/) |
| Misc | 4 | [`plugins/misc/skills/`](plugins/misc/skills/) |
| Product | 14 | [`plugins/product/skills/`](plugins/product/skills/) |
| Rails | 36 | [`plugins/rails/skills/`](plugins/rails/skills/) |
| Reasoning | 4 | [`plugins/reasoning/skills/`](plugins/reasoning/skills/) |
| Sales | 6 | [`plugins/sales/skills/`](plugins/sales/skills/) |
| SEO | 22 | [`plugins/seo/skills/`](plugins/seo/skills/) |
| Writing | 10 | [`plugins/writing/skills/`](plugins/writing/skills/) |

Core is a category for foundational repository capabilities, not a dependency required by other categories. Misc is a temporary holding category for useful portable skills whose long-term domain is still undecided, not a destination for low-value leftovers.

Counts above are catalog skills only. Cookbooks are counted separately and described below; `plugins/seo/skills/` also holds one, which is why `majestic-seo` installs 23 skills.

## Core Skills

| Skill | Description |
| --- | --- |
| [`agent-ready-repository`](plugins/core/skills/agent-ready-repository/) | Make repositories easier and safer for coding agents to navigate and modify. |
| [`agents-md-hierarchy`](plugins/core/skills/agents-md-hierarchy/) | Audit and refine nested repository guidance where local commands, rules, or boundaries differ. |

## Data Skills

| Skill | Description |
| --- | --- |
| [`anomaly-detection`](plugins/data/skills/anomaly-detection/) | Design and evaluate anomaly detection using context-appropriate baselines and methods. |
| [`csv-wrangling`](plugins/data/skills/csv-wrangling/) | Recover messy delimited files without silently dropping or corrupting records. |
| [`data-pipeline-design`](plugins/data/skills/data-pipeline-design/) | Design reliable batch or incremental pipelines with explicit recovery and reconciliation behavior. |
| [`data-pipeline-testing`](plugins/data/skills/data-pipeline-testing/) | Test transformations, contracts, incrementality, replay, and failure recovery. |
| [`data-quality`](plugins/data/skills/data-quality/) | Define and operate quality controls, service levels, scorecards, and incident response. |
| [`data-source-assessment`](plugins/data/skills/data-source-assessment/) | Assess unfamiliar sources for schema, grain, change behavior, quality, and extraction constraints. |
| [`data-validation`](plugins/data/skills/data-validation/) | Design executable contracts across records, DataFrames, warehouses, and pipeline boundaries. |
| [`dbt-development`](plugins/data/skills/dbt-development/) | Build and review dbt projects, models, tests, materializations, and documentation. |

## Cloudflare Skills

| Skill | Description |
| --- | --- |
| [`agents-sdk`](plugins/cloudflare/skills/agents-sdk/) | Build AI agents on Cloudflare Workers with state, workflows, queues, MCP, chat, and real-time APIs. |
| [`cloudflare`](plugins/cloudflare/skills/cloudflare/) | Route Cloudflare platform work to the relevant product and reference guidance. |
| [`cloudflare-email-service`](plugins/cloudflare/skills/cloudflare-email-service/) | Send and receive transactional email with Cloudflare Email Service. |
| [`cloudflare-infrastructure`](plugins/cloudflare/skills/cloudflare-infrastructure/) | Provision and review Cloudflare infrastructure with OpenTofu. |
| [`cloudflare-one`](plugins/cloudflare/skills/cloudflare-one/) | Design, configure, troubleshoot, and review Cloudflare One Zero Trust deployments. |
| [`cloudflare-one-migrations`](plugins/cloudflare/skills/cloudflare-one-migrations/) | Plan migrations from Zscaler, Palo Alto, VPN, SWG, and SASE stacks to Cloudflare One. |
| [`cloudflare-worker-development`](plugins/cloudflare/skills/cloudflare-worker-development/) | Build and review TypeScript applications for the Cloudflare Workers runtime. |
| [`cloudflare-workers-deployment`](plugins/cloudflare/skills/cloudflare-workers-deployment/) | Configure, validate, and deploy Cloudflare Workers with Wrangler. |
| [`durable-objects`](plugins/cloudflare/skills/durable-objects/) | Build and review Cloudflare Durable Objects for coordinated stateful applications. |
| [`sandbox-sdk`](plugins/cloudflare/skills/sandbox-sdk/) | Build isolated code execution environments with the Cloudflare Sandbox SDK. |
| [`turnstile-spin`](plugins/cloudflare/skills/turnstile-spin/) | Set up and validate Cloudflare Turnstile protection end to end. |
| [`workers-best-practices`](plugins/cloudflare/skills/workers-best-practices/) | Review and author Cloudflare Workers code against current production practices. |
| [`wrangler`](plugins/cloudflare/skills/wrangler/) | Use the current Wrangler CLI for Cloudflare Workers, Pages, storage, AI, queues, workflows, and deployment operations. |

## DevOps Skills

| Skill | Description |
| --- | --- |
| [`ansible-server-configuration`](plugins/devops/skills/ansible-server-configuration/) | Configure and maintain servers with focused Ansible playbooks. |
| [`backblaze-b2-storage`](plugins/devops/skills/backblaze-b2-storage/) | Configure and operate Backblaze B2 storage. |
| [`cloud-init-provisioning`](plugins/devops/skills/cloud-init-provisioning/) | Provision virtual machines with small, testable cloud-init configurations. |
| [`digitalocean-infrastructure`](plugins/devops/skills/digitalocean-infrastructure/) | Provision and review DigitalOcean infrastructure with OpenTofu. |
| [`hetzner-infrastructure`](plugins/devops/skills/hetzner-infrastructure/) | Provision and review Hetzner Cloud infrastructure with OpenTofu. |
| [`infrastructure-review`](plugins/devops/skills/infrastructure-review/) | Review infrastructure changes for correctness, maintainability, simplicity, and deployment risk. |
| [`infrastructure-security-review`](plugins/devops/skills/infrastructure-security-review/) | Review infrastructure as code for exploitable security failures. |
| [`kamal-deploy`](plugins/devops/skills/kamal-deploy/) | Deploy and operate Rails applications with Kamal 2. |
| [`onepassword-secrets`](plugins/devops/skills/onepassword-secrets/) | Load and inject secrets with the 1Password CLI. |
| [`opentofu-iac`](plugins/devops/skills/opentofu-iac/) | Build and maintain infrastructure as code with OpenTofu and HCL. |

## Engineer Skills

| Skill | Description |
| --- | --- |
| [`code-review`](plugins/engineer/skills/code-review/) | Review change sets for defects, regressions, unnecessary complexity, missing tests, and release readiness. |
| [`complexity-reviewer`](plugins/engineer/skills/complexity-reviewer/) | Review algorithmic complexity and performance hotspots conservatively. |
| [`implementation-planning`](plugins/engineer/skills/implementation-planning/) | Create an executable technical plan grounded in the existing repository. |
| [`minimal-sufficient-work`](plugins/engineer/skills/minimal-sufficient-work/) | Apply the MSW deletion rule so only work necessary to satisfy or prove the requested outcome is performed. |
| [`multi-agent-architecture`](plugins/engineer/skills/multi-agent-architecture/) | Design persistent multi-agent systems with explicit roles, handoffs, state, permissions, and failure handling. |
| [`plan-review`](plugins/engineer/skills/plan-review/) | Review planning documents as whole delivery artifacts for implementation readiness and risk. |
| [`structured-logging`](plugins/engineer/skills/structured-logging/) | Design structured application logging for observability and incidents. |
| [`test-reviewer`](plugins/engineer/skills/test-reviewer/) | Review automated tests for behavioral coverage and reliability. |
| [`to-tasks`](plugins/engineer/skills/to-tasks/) | Convert settled work into dependency-aware vertical tasks for multi-session or parallel implementation. |

## Founder Skills

| Skill | Description |
| --- | --- |
| [`bootstrapped-finance`](plugins/founder/skills/bootstrapped-finance/) | Analyze cash runway, burn, unit economics, working capital, hiring ROI, and spending tradeoffs for bootstrapped companies. |
| [`company-strategy`](plugins/founder/skills/company-strategy/) | Build future-back company strategy with explicit horizons, dependencies, bets, and revisit triggers. |
| [`founder-plan-review`](plugins/founder/skills/founder-plan-review/) | Review a concrete plan for premise quality, ambition, focus, strategic leverage, user value, and execution risk. |
| [`founder-priorities`](plugins/founder/skills/founder-priorities/) | Turn competing priorities and calendar load into a stage-fit operating plan with tradeoffs and revisit criteria. |
| [`fundraising-ask-review`](plugins/founder/skills/fundraising-ask-review/) | Review an existing fundraising ask for round coherence, evidence-backed claims, and investor relevance. |
| [`go-to-market-motion`](plugins/founder/skills/go-to-market-motion/) | Choose and phase a route to market that fits buying behavior, economics, stage, and capacity. |
| [`launch-legal-checklist`](plugins/founder/skills/launch-legal-checklist/) | Identify launch legal unknowns, escalation points, and next actions without implying legal clearance. |
| [`launch-readiness`](plugins/founder/skills/launch-readiness/) | Return a blunt go, narrow, or delay recommendation for a founder-led launch. |
| [`technology-impact-assessment`](plugins/founder/skills/technology-impact-assessment/) | Assess how an external technology change affects a named company and choose action, experiment, monitoring, or no material action. |

## Frontend Skills

| Skill | Description |
| --- | --- |
| [`frontend-design`](plugins/frontend/skills/frontend-design/) | Choose a coherent visual direction and implement production-grade interfaces. |
| [`frontend-performance`](plugins/frontend/skills/frontend-performance/) | Prevent and diagnose Core Web Vitals regressions. |
| [`pr-screenshot-docs`](plugins/frontend/skills/pr-screenshot-docs/) | Capture and document visual changes for pull-request review. |
| [`ui-code-auditor`](plugins/frontend/skills/ui-code-auditor/) | Audit frontend source for accessibility, quality, and performance problems. |
| [`visual-validator`](plugins/frontend/skills/visual-validator/) | Validate rendered UI changes against their intended goals. |

## Marketing Skills

| Skill | Description |
| --- | --- |
| [`brand-naming`](plugins/marketing/skills/brand-naming/) | Generate and evaluate brand, company, product, and feature names with verification checks. |
| [`brand-positioning`](plugins/marketing/skills/brand-positioning/) | Define evidence-backed positioning, differentiation, value propositions, messaging angles, and taglines. |
| [`community-participation`](plugins/marketing/skills/community-participation/) | Plan transparent, value-first participation in online communities within current local rules. |
| [`content-repurposing`](plugins/marketing/skills/content-repurposing/) | Adapt one verified long-form asset into channel-appropriate derivative content. |
| [`customer-case-study`](plugins/marketing/skills/customer-case-study/) | Turn verified customer outcomes and approved quotations into an evidence-safe case study and proof assets. |
| [`editorial-planning`](plugins/marketing/skills/editorial-planning/) | Generate, evaluate, prioritize, and schedule audience-led content ideas and a production calendar. |
| [`growth-experimentation`](plugins/marketing/skills/growth-experimentation/) | Run marketing experiments with explicit hypotheses, guardrails, and evidence-based decisions. |
| [`market-research`](plugins/marketing/skills/market-research/) | Research markets, audiences, competitors, and customer language into a decision-ready report. |
| [`newsletter-editorial`](plugins/marketing/skills/newsletter-editorial/) | Plan and draft a recurring newsletter with a clear editorial promise and source discipline. |
| [`offer-design`](plugins/marketing/skills/offer-design/) | Design truthful commercial and lead-generation offers before final copy. |
| [`paid-search`](plugins/marketing/skills/paid-search/) | Plan paid-search campaigns using current platform behavior, measurement, and spend controls. |
| [`social-content`](plugins/marketing/skills/social-content/) | Plan and draft professional social posts and X threads without relying on algorithm folklore. |
| [`youtube-packaging`](plugins/marketing/skills/youtube-packaging/) | Analyze normalized YouTube outliers and develop ownable title and thumbnail hypotheses. |

## Misc Skills

| Skill | Description |
| --- | --- |
| [`actionable-communication`](plugins/misc/skills/actionable-communication/) | Shape responses into direct answers, bounded actions, visible progress, and one concrete next step. |
| [`show-me`](plugins/misc/skills/show-me/) | Explain the current topic with the smallest accurate visual. |
| [`skill-grader`](plugins/misc/skills/skill-grader/) | Grade skill executions against expectations using transcript and output evidence. |
| [`skill-structure`](plugins/misc/skills/skill-structure/) | Decide whether guidance should become an Agent Skill and design a compliant structure when justified. |

## Product Skills

| Skill | Description |
| --- | --- |
| [`brainstorm-product`](plugins/product/skills/brainstorm-product/) | Diagnose an existing product, pressure-test a commercial idea, or shape a non-commercial builder project. |
| [`feature-brief`](plugins/product/skills/feature-brief/) | Write a compact feature brief or decision document before a full specification. |
| [`gherkin-stories`](plugins/product/skills/gherkin-stories/) | Decompose requirements into atomic stories with testable Gherkin scenarios and traceability. |
| [`lifecycle-retention`](plugins/product/skills/lifecycle-retention/) | Design lifecycle stages, health signals, onboarding, early warnings, and retention interventions. |
| [`north-star-metric`](plugins/product/skills/north-star-metric/) | Choose and operate one stage-fit product health metric with drivers and guardrails. |
| [`pricing-strategy`](plugins/product/skills/pricing-strategy/) | Design pricing and packaging from value, evidence, costs, and expansion logic. |
| [`product-decision-alignment`](plugins/product/skills/product-decision-alignment/) | Diagnose and repair stuck, reopened, or inconsistently executed cross-functional product decisions. |
| [`product-discovery`](plugins/product/skills/product-discovery/) | Plan interviews, map assumptions, and frame Jobs-to-be-Done before defining a solution. |
| [`product-planning`](plugins/product/skills/product-planning/) | Prioritize opportunities and build an outcome-based Now, Next, Later roadmap. |
| [`product-requirements`](plugins/product/skills/product-requirements/) | Write an evidence-grounded PRD with testable requirements, scope, and success measures. |
| [`product-validation`](plugins/product/skills/product-validation/) | Pressure-test demand and define the smallest test for the riskiest product assumption. |
| [`requirements-quality`](plugins/product/skills/requirements-quality/) | Audit and repair requirements with evidence-safe status, abstraction-aware checks, and traceability. |
| [`stakeholder-conversation-roleplay`](plugins/product/skills/stakeholder-conversation-roleplay/) | Rehearse a difficult product conversation in a bounded simulation and debrief observable communication choices. |
| [`workflow-opportunity-mapping`](plugins/product/skills/workflow-opportunity-mapping/) | Map observed workflows into states, burdens, automation choices, controls, product opportunities, and exceptions. |

## Rails Skills

| Skill | Description |
| --- | --- |
| [`aasm-coder`](plugins/rails/skills/aasm-coder/) | Implement state machines with AASM for workflow management. |
| [`action-mailer-coder`](plugins/rails/skills/action-mailer-coder/) | Create or refactor Action Mailer emails. |
| [`action-policy-coder`](plugins/rails/skills/action-policy-coder/) | Implement authorization with Action Policy. |
| [`active-interaction-coder`](plugins/rails/skills/active-interaction-coder/) | Implement typed business operations with ActiveInteraction. |
| [`active-job-coder`](plugins/rails/skills/active-job-coder/) | Create or refactor Active Job background jobs. |
| [`anycable-coder`](plugins/rails/skills/anycable-coder/) | Implement reliable real-time features with AnyCable. |
| [`anyway-config-coder`](plugins/rails/skills/anyway-config-coder/) | Implement type-safe configuration with `anyway_config`. |
| [`business-logic-coder`](plugins/rails/skills/business-logic-coder/) | Route Rails business logic to the simplest fitting home. |
| [`constraints-reviewer`](plugins/rails/skills/constraints-reviewer/) | Review data constraints and referential integrity. |
| [`dhh-rails-style`](plugins/rails/skills/dhh-rails-style/) | Write and review Rails code using DHH and 37signals conventions. |
| [`dialog-patterns`](plugins/rails/skills/dialog-patterns/) | Build native HTML dialogs with Turbo and Stimulus. |
| [`event-sourcing-coder`](plugins/rails/skills/event-sourcing-coder/) | Record domain events for side effects, audit trails, and activity feeds. |
| [`gem-builder`](plugins/rails/skills/gem-builder/) | Build production-quality Ruby gems. |
| [`graphql-architect`](plugins/rails/skills/graphql-architect/) | Design GraphQL APIs with `graphql-ruby`. |
| [`hotwire-coder`](plugins/rails/skills/hotwire-coder/) | Implement Turbo Drive, Frames, and Streams. |
| [`inertia-coder`](plugins/rails/skills/inertia-coder/) | Build Rails applications with Inertia.js and React, Vue, or Svelte. |
| [`layered-rails`](plugins/rails/skills/layered-rails/) | Design Rails applications with explicit architectural layers. |
| [`rails-lint`](plugins/rails/skills/rails-lint/) | Run and fix RuboCop, ERB Lint, and Brakeman findings in Rails projects. |
| [`litestream-coder`](plugins/rails/skills/litestream-coder/) | Configure Litestream backups for Rails SQLite databases. |
| [`mcp-oauth-setup`](plugins/rails/skills/mcp-oauth-setup/) | Implement MCP server authentication and OAuth registration. |
| [`minitest-coder`](plugins/rails/skills/minitest-coder/) | Write Minitest tests for Ruby and Rails. |
| [`performance-reviewer`](plugins/rails/skills/performance-reviewer/) | Review Rails code for query, memory, locking, and throughput problems. |
| [`rails-code-review`](plugins/rails/skills/rails-code-review/) | Review Rails changes with framework-specific correctness and release gates. |
| [`privacy-reviewer`](plugins/rails/skills/privacy-reviewer/) | Review PII handling, encryption, and privacy compliance. |
| [`rails-activity-timeline`](plugins/rails/skills/rails-activity-timeline/) | Add polymorphic activity timelines with Turbo Stream updates. |
| [`rails-authentication-coder`](plugins/rails/skills/rails-authentication-coder/) | Implement Rails 8 native authentication. |
| [`rails-debugger`](plugins/rails/skills/rails-debugger/) | Diagnose Rails errors, failing tests, and unexpected behavior. |
| [`rails-refactorer`](plugins/rails/skills/rails-refactorer/) | Refactor Rails code while preserving behavior. |
| [`ruby-coder`](plugins/rails/skills/ruby-coder/) | Write modern, idiomatic Ruby. |
| [`simplicity-reviewer`](plugins/rails/skills/simplicity-reviewer/) | Review code for unnecessary complexity and YAGNI violations. |
| [`solid-cache-coder`](plugins/rails/skills/solid-cache-coder/) | Configure and use Solid Cache. |
| [`solid-queue-coder`](plugins/rails/skills/solid-queue-coder/) | Configure and use Solid Queue. |
| [`stimulus-coder`](plugins/rails/skills/stimulus-coder/) | Create or refactor Stimulus controllers. |
| [`store-model-coder`](plugins/rails/skills/store-model-coder/) | Model typed JSON attributes with `store_model`. |
| [`tailwind-coder`](plugins/rails/skills/tailwind-coder/) | Style Rails views with Tailwind CSS. |
| [`viewcomponent-coder`](plugins/rails/skills/viewcomponent-coder/) | Build component-based Rails interfaces with ViewComponent. |

## Reasoning Skills

| Skill | Description |
| --- | --- |
| [`decision-retrospective`](plugins/reasoning/skills/decision-retrospective/) | Review a completed decision by separating process quality, outcome, hindsight, and updated decision rules. |
| [`devils-advocate`](plugins/reasoning/skills/devils-advocate/) | Pressure-test a preferred approach before commitment. |
| [`premortem`](plugins/reasoning/skills/premortem/) | Convert plausible future failure stories into safeguards for a concrete plan. |
| [`reasoning-verifier`](plugins/reasoning/skills/reasoning-verifier/) | Trace requirements, evidence, and assumptions into a completed conclusion. |

## Sales Skills

| Skill | Description |
| --- | --- |
| [`account-expansion`](plugins/sales/skills/account-expansion/) | Grow existing accounts through value reviews, expansion triggers, win-back, and referral asks. |
| [`icp-definition`](plugins/sales/skills/icp-definition/) | Define and validate an Ideal Customer Profile with fit criteria, disqualifiers, and account scoring. |
| [`outbound-prospecting`](plugins/sales/skills/outbound-prospecting/) | Design and diagnose evidence-safe outbound sequences across multiple channels. |
| [`pipeline-analysis`](plugins/sales/skills/pipeline-analysis/) | Diagnose pipeline health, challenge forecasts, and assign corrective actions. |
| [`sales-enablement`](plugins/sales/skills/sales-enablement/) | Build a B2B playbook for discovery, demos, objections, competition, and closing. |
| [`sales-proposal`](plugins/sales/skills/sales-proposal/) | Write a complete evidence-based commercial proposal after qualified discovery. |

## SEO Skills

| Skill | Description |
| --- | --- |
| [`aeo-scorecard`](plugins/seo/skills/aeo-scorecard/) | Measure Answer Engine Optimization visibility, share of voice, citations, and referral demand. |
| [`ai-crawler-readiness`](plugins/seo/skills/ai-crawler-readiness/) | Configure HTTP-layer signals for LLM discovery, crawling, content negotiation, and referral measurement. |
| [`analyst-positioning`](plugins/seo/skills/analyst-positioning/) | Position people as recognizable industry experts with stronger authority and citation signals. |
| [`behavioral-seo`](plugins/seo/skills/behavioral-seo/) | Improve behavioral search signals such as click-through rate, dwell time, and engagement. |
| [`bofu-keywords`](plugins/seo/skills/bofu-keywords/) | Find and prioritize bottom-of-funnel keywords with strong purchase intent. |
| [`buyer-journey-mapper`](plugins/seo/skills/buyer-journey-mapper/) | Map personas and buyer stages into an answer-focused content matrix. |
| [`eeat-analyzer`](plugins/seo/skills/eeat-analyzer/) | Audit and improve Experience, Expertise, Authority, and Trust signals. |
| [`entity-triplets`](plugins/seo/skills/entity-triplets/) | Build consistent entity relationships that search engines and LLMs can recognize. |
| [`geo-content-optimizer`](plugins/seo/skills/geo-content-optimizer/) | Structure content for extraction and citation by ChatGPT, Perplexity, Gemini, and similar systems. |
| [`keyword-research`](plugins/seo/skills/keyword-research/) | Discover and prioritize search-led content topics against real queries without expensive SEO tools. |
| [`keyword-strategist`](plugins/seo/skills/keyword-strategist/) | Analyze keyword usage and suggest semantic variations and related terms. |
| [`llms-txt-builder`](plugins/seo/skills/llms-txt-builder/) | Generate an `llms.txt` file that helps AI systems navigate a site. |
| [`meta-optimizer`](plugins/seo/skills/meta-optimizer/) | Create optimized meta titles, descriptions, and URL suggestions. |
| [`press-release-aeo`](plugins/seo/skills/press-release-aeo/) | Frame press releases for AI citation, authority building, and newswire distribution. |
| [`query-expansion-strategy`](plugins/seo/skills/query-expansion-strategy/) | Expand content coverage across LLM sub-questions and semantic query variations. |
| [`review-management`](plugins/seo/skills/review-management/) | Improve review presence and use customer-generated content as trust and recommendation signals. |
| [`schema-architect`](plugins/seo/skills/schema-architect/) | Create and audit Schema.org JSON-LD for rich results, AI Overviews, and search indexing. |
| [`seo-audit`](plugins/seo/skills/seo-audit/) | Audit technical SEO, content quality, E-E-A-T, and AI citation readiness. |
| [`seo-content`](plugins/seo/skills/seo-content/) | Produce a search-optimized content asset from opportunity selection through auditing and tracking. |
| [`snippet-hunter`](plugins/seo/skills/snippet-hunter/) | Format content for featured snippets and other search-result features. |
| [`structure-architect`](plugins/seo/skills/structure-architect/) | Improve headings, content structure, schema markup, and internal linking. |
| [`topical-authority`](plugins/seo/skills/topical-authority/) | Plan content clusters, identify coverage gaps, and build measurable topical authority. |

## Writing Skills

| Skill | Description |
| --- | --- |
| [`brand-voice`](plugins/writing/skills/brand-voice/) | Define an aspirational organizational voice from brand strategy, audience, and desired perception. |
| [`content-writer`](plugins/writing/skills/content-writer/) | Draft source-grounded general articles and guides through a brief, outline, and section workflow. |
| [`copy-editor`](plugins/writing/skills/copy-editor/) | Diagnose and prioritize grammar, clarity, structure, attribution, voice, and style problems in existing prose. |
| [`direct-response-copy`](plugins/writing/skills/direct-response-copy/) | Create evidence-safe conversion-oriented landing pages, sales emails, CTAs, ads, and product microcopy. |
| [`headline-generator`](plugins/writing/skills/headline-generator/) | Generate and recommend fact-bound headline, title, and subject-line candidates from supplied evidence. |
| [`minto-pyramid`](plugins/writing/skills/minto-pyramid/) | Restructure complex writing around one governing answer, supporting arguments, and matched evidence. |
| [`prose-reviser`](plugins/writing/skills/prose-reviser/) | Rewrite existing prose for clarity, natural rhythm, and author fidelity while preserving facts and uncertainty. |
| [`style-forensics`](plugins/writing/skills/style-forensics/) | Measure and explain prose style with quantitative metrics and cited examples. |
| [`style-writer`](plugins/writing/skills/style-writer/) | Draft and revise prose against an existing voice profile while preserving facts and readability. |
| [`voice-dna-kit`](plugins/writing/skills/voice-dna-kit/) | Capture an existing personal or organizational writing voice as reusable guidance. |

## Cookbooks

Cookbooks are recipes: user-invoked workflow skills that sequence catalog skills by name (plan, implement, quality gates). They follow a different contract from catalog skills, which are decoupled and never reference each other, while a cookbook references the skills it orchestrates and declares them in a `## Requires` section.

Where a cookbook lives follows from what it requires. If every required skill belongs to one plugin, the cookbook ships inside that plugin and installs with it. If it spans two or more plugins, it stays in [`cookbooks/`](cookbooks/) and is not part of any plugin, so the Skills CLI is its only install route.

| Cookbook | Requires | Description |
| --- | --- | --- |
| [`ai-search-visibility-foundation`](plugins/seo/skills/ai-search-visibility-foundation/) | `majestic-seo` | Establish a site's SEO, entity, AI navigation, crawler, structured-data, and AEO measurement foundations. |
| [`founder-launch-decision`](cookbooks/founder-launch-decision/) | `majestic-founder`, `majestic-sales` | Turn a founder-led launch proposal into a defensible audience, motion, legal-unknown inventory, and launch verdict. |
| [`product-engineering-handoff`](cookbooks/product-engineering-handoff/) | `majestic-engineer`, `majestic-product` | Turn an approved product direction into a PRD, repository-grounded implementation plan, and reviewed engineering handoff. |
| [`rails-feature`](cookbooks/rails-feature/) | `majestic-engineer`, `majestic-rails` | Build a Rails feature end-to-end: plan, implement in DHH style with TDD, then pass lint, test, and review quality gates. |

Cookbooks install like any other skill, but always install their required skills alongside them; installers do not resolve these dependencies for you. Each cookbook lists a harness-neutral `npx skills` command without `--agent`. Native category-plugin installation remains documented in the harness-specific sections above. `scripts/check-cookbooks.sh` verifies placement, that every referenced skill exists, and that the install commands cover it; run it before committing cookbook changes. See [`cookbooks/README.md`](cookbooks/README.md) for the full contract and authoring guide.

## Layout

```text
.claude-plugin/
  marketplace.json          # one entry per plugin below
.agents/
  plugins/
    marketplace.json        # Codex marketplace, one entry per plugin below
plugins/
  <category>/
    plugin.json               # Agent Plugins 1.0.0 portable manifest
    .claude-plugin/
      plugin.json             # Claude Code compatibility manifest
    .codex-plugin/
      plugin.json             # Codex compatibility manifest
    skills/
      <skill-name>/
        SKILL.md
        references/  # optional
        scripts/     # optional
        assets/      # optional
      <cookbook-name>/          # only when all its skills are in this plugin
        SKILL.md
cookbooks/
  <cookbook-name>/              # cross-plugin cookbooks; not a plugin
    SKILL.md
scripts/
  check-agent-plugins.sh
  check-codex-plugins.sh
  check-cookbooks.sh
```

Each skill is self-contained. Each category directory is a complete portable Agent Plugin. The `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` files preserve the native installation routes, and all three formats discover the shared `skills/` directory. The same directories provide catalog organization and category-scoped installation for the Skills CLI, which flattens installed skills into each agent's native skill directory.

Run `scripts/check-agent-plugins.sh`, `scripts/check-codex-plugins.sh`, and `scripts/check-cookbooks.sh` before committing packaging or cookbook changes. Cookbooks are the composition layer: they may reference catalog skills by name, and the validation scripts keep those references, their placement, and their install routes honest.
