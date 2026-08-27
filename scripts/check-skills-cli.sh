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

if ! grep -Fq 'Found 173 skills' "$list_file"; then
  echo "FAIL: Skills CLI must discover exactly 173 public abilities" >&2
  exit 1
fi

for skill in \
  ai-search-visibility-foundation \
  founder-launch-decision \
  founder-next-stage-decision \
  product-engineering-handoff \
  rails-feature; do
  if ! grep -Fq "$skill" "$list_file"; then
    echo "FAIL: Skills CLI did not discover $skill" >&2
    exit 1
  fi
done

if grep -Fq 'sort-hat' "$list_file"; then
  echo "FAIL: internal maintainer skill sort-hat leaked into public discovery" >&2
  exit 1
fi

if (
  cd "$tmp_project"
  npx --yes "skills@${skills_cli_version}" add "$source_ref" \
    --skill sort-hat \
    --agent codex \
    --copy \
    --yes >/dev/null 2>&1
); then
  echo "FAIL: internal maintainer skill sort-hat is publicly installable" >&2
  exit 1
fi

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

echo "OK: Skills CLI ${skills_cli_version} discovers 173 public abilities and installs rails-feature with all required skills"
