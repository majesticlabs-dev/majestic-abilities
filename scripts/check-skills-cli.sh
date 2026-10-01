#!/usr/bin/env bash
# Verify Skills CLI discovery and installs for repository skills and cookbooks.
set -euo pipefail

cd "$(dirname "$0")/.."

skills_cli_version="${SKILLS_CLI_VERSION:-1.5.23}"
source_ref="${1:-$(pwd)}"
tmp_home=$(mktemp -d "${TMPDIR:-/tmp}/majestic-abilities-skills-home.XXXXXX")
tmp_project=$(mktemp -d "${TMPDIR:-/tmp}/majestic-abilities-skills-project.XXXXXX")
trap 'rm -rf "$tmp_home" "$tmp_project"' EXIT

export HOME="$tmp_home"
export npm_config_cache="$tmp_home/npm-cache"
export NO_COLOR=1

list_output=$(npx --yes "skills@${skills_cli_version}" add "$source_ref" --list)
list_file="$tmp_home/skills-list.txt"
printf '%s\n' "$list_output" > "$list_file"
printf '%s\n' "$list_output"

if ! grep -Fq 'Found 185 skills' "$list_file"; then
  echo "FAIL: Skills CLI must discover exactly 185 abilities" >&2
  exit 1
fi

for skill in \
  engineering-workflow \
  create-verification-skill \
  maintain-verification-skill \
  codebase-investigation \
  technical-writing \
  session-recall \
  ai-search-visibility-foundation \
  seo-operator \
  company-values \
  manual-service-pilot \
  first-customers \
  marketing-plan \
  launch-decision \
  growth-stage-decision \
  plugin-release \
  product-engineering-handoff \
  rails-feature \
  session-handoff \
  sort-hat; do
  if ! grep -Fq "$skill" "$list_file"; then
    echo "FAIL: Skills CLI did not discover $skill" >&2
    exit 1
  fi
done

(
  cd "$tmp_project"
  npx --yes "skills@${skills_cli_version}" add "$source_ref" \
    --skill plugin-release session-handoff sort-hat \
      engineering-workflow code-review implementation-planning test-reviewer writing-pr \
      create-verification-skill maintain-verification-skill \
      codebase-investigation technical-writing session-recall \
    --agent codex \
    --copy \
    --yes >/dev/null
)

for skill in plugin-release session-handoff sort-hat \
  engineering-workflow code-review implementation-planning test-reviewer writing-pr \
  create-verification-skill maintain-verification-skill \
  codebase-investigation technical-writing session-recall; do
  if [ ! -f "$tmp_project/.agents/skills/$skill/SKILL.md" ]; then
    echo "FAIL: Skills CLI did not install $skill for Codex" >&2
    exit 1
  fi
done

if [ ! -f "$tmp_project/.agents/skills/engineering-workflow/agents/openai.yaml" ]; then
  echo "FAIL: Skills CLI did not copy the engineering-workflow invocation policy" >&2
  exit 1
fi

(
  cd "$tmp_project"
  npx --yes "skills@${skills_cli_version}" add "$source_ref" \
    --skill rails-feature dhh-rails-style ruby-coder minitest-coder \
      rails-lint rails-code-review test-reviewer implementation-planning \
      company-values manual-service-pilot first-customers marketing-plan \
      icp-definition go-to-market-motion outbound-prospecting pricing-strategy \
      editorial-planning social-content newsletter-editorial growth-experimentation \
    --agent codex \
    --copy \
    --yes
)

for skill in \
  rails-feature \
  dhh-rails-style \
  ruby-coder \
  minitest-coder \
  rails-lint \
  rails-code-review \
  test-reviewer \
  company-values \
  manual-service-pilot \
  first-customers \
  marketing-plan \
  icp-definition \
  go-to-market-motion \
  outbound-prospecting \
  pricing-strategy \
  editorial-planning \
  social-content \
  newsletter-editorial \
  growth-experimentation \
  implementation-planning; do
  if [ ! -f "$tmp_project/.agents/skills/$skill/SKILL.md" ]; then
    echo "FAIL: Skills CLI did not install $skill for Codex" >&2
    exit 1
  fi
done

echo "OK: Skills CLI ${skills_cli_version} discovers 185 abilities and installs verification, investigation, writing, recall, repository, and founder skills, plus engineering-workflow, rails-feature, first-customers, and marketing-plan dependencies"
