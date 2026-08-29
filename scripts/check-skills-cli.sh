#!/usr/bin/env bash
# Verify the default Skills CLI discovery and a cross-category cookbook install.
set -euo pipefail

cd "$(dirname "$0")/.."

skills_cli_version="${SKILLS_CLI_VERSION:-1.5.23}"
source_ref="${1:-$(pwd)}"
tmp_home=$(mktemp -d -t majestic-abilities-skills-home)
tmp_project=$(mktemp -d -t majestic-abilities-skills-project)
trap 'rm -rf "$tmp_home" "$tmp_project"' EXIT

export HOME="$tmp_home"
export npm_config_cache="$tmp_home/npm-cache"
export NO_COLOR=1

list_output=$(npx --yes "skills@${skills_cli_version}" add "$source_ref" --list)
list_file="$tmp_home/skills-list.txt"
printf '%s\n' "$list_output" > "$list_file"
printf '%s\n' "$list_output"

if ! grep -Fq 'Found 174 skills' "$list_file"; then
  echo "FAIL: Skills CLI must discover exactly 174 abilities" >&2
  exit 1
fi

for skill in \
  ai-search-visibility-foundation \
  founder-launch-decision \
  founder-next-stage-decision \
  plugin-release \
  product-engineering-handoff \
  rails-feature \
  sort-hat; do
  if ! grep -Fq "$skill" "$list_file"; then
    echo "FAIL: Skills CLI did not discover $skill" >&2
    exit 1
  fi
done

(
  cd "$tmp_project"
  npx --yes "skills@${skills_cli_version}" add "$source_ref" \
    --skill plugin-release sort-hat \
    --agent codex \
    --copy \
    --yes >/dev/null
)

for skill in plugin-release sort-hat; do
  if [ ! -f "$tmp_project/.agents/skills/$skill/SKILL.md" ]; then
    echo "FAIL: Skills CLI did not install repository skill $skill for Codex" >&2
    exit 1
  fi
done

(
  cd "$tmp_project"
  npx --yes "skills@${skills_cli_version}" add "$source_ref" \
    --skill rails-feature dhh-rails-style ruby-coder minitest-coder \
      rails-lint rails-code-review test-reviewer implementation-planning \
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
  implementation-planning; do
  if [ ! -f "$tmp_project/.agents/skills/$skill/SKILL.md" ]; then
    echo "FAIL: Skills CLI did not install $skill for Codex" >&2
    exit 1
  fi
done

echo "OK: Skills CLI ${skills_cli_version} discovers 174 abilities and installs repository skills plus rails-feature dependencies"
