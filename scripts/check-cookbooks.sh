#!/usr/bin/env bash
# Verify cookbook names, dependency declarations, install commands, and root discovery.
set -euo pipefail

cd "$(dirname "$0")/.."

skill_names=$(grep -h '^name:' skills/*/*/SKILL.md | sed -E 's/^name:[[:space:]]*"?([^"]*)"?[[:space:]]*$/\1/')
manifest=".claude-plugin/plugin.json"

status=0
found_cookbook=0
manifest_entries=""

fail() {
  echo "FAIL: $1"
  status=1
}

if [ ! -f "$manifest" ]; then
  fail "$manifest is required so the Skills CLI discovers cookbooks from the repository root"
elif ! manifest_entries=$(python3 - "$manifest" <<'PY'
import json
import sys

with open(sys.argv[1]) as file:
    data = json.load(file)

skills = data.get("skills")
if not isinstance(skills, list) or not all(isinstance(entry, str) for entry in skills):
    raise ValueError("manifest 'skills' must be an array of strings")

for entry in skills:
    print(entry)
PY
); then
  fail "$manifest is invalid or has no string-array 'skills' property"
  manifest_entries=""
fi

for cookbook in cookbooks/*/SKILL.md; do
  [ -f "$cookbook" ] || continue
  found_cookbook=1

  cookbook_dir=$(basename "$(dirname "$cookbook")")
  cookbook_name=$(grep -m1 '^name:' "$cookbook" | sed -E 's/^name:[[:space:]]*"?([^"]*)"?[[:space:]]*$/\1/' || true)

  if [ -z "$cookbook_name" ]; then
    fail "$cookbook has no name in frontmatter"
  elif [ "$cookbook_name" != "$cookbook_dir" ]; then
    fail "$cookbook name '$cookbook_name' does not match directory '$cookbook_dir'"
  elif echo "$skill_names" | grep -qx "$cookbook_name"; then
    fail "$cookbook name '$cookbook_name' collides with a skill in skills/"
  fi

  manifest_path="./cookbooks/$cookbook_dir"
  if ! printf '%s\n' "$manifest_entries" | grep -Fxq "$manifest_path"; then
    fail "$cookbook is missing from $manifest and will not be discovered from the repository root"
  fi

  # Requires entries look like: - `skill-name` - reason
  requires=$(awk '/^## Requires/{flag=1; next} /^## /{flag=0} flag' "$cookbook" \
    | grep -E '^- `' | sed -E 's/^- `([^`]+)`.*/\1/' || true)

  if [ -z "$requires" ]; then
    fail "$cookbook has no '## Requires' entries"
    continue
  fi

  for name in $requires; do
    if ! echo "$skill_names" | grep -qx "$name"; then
      fail "$cookbook requires '$name' but no skill with that name exists"
    fi
  done

  body_refs=$(grep -oE '`[a-z0-9][a-z0-9-]*`' "$cookbook" \
    | tr -d '`' | sort -u || true)
  for name in $body_refs; do
    if ! echo "$skill_names" | grep -qx "$name"; then
      fail "$cookbook references unknown skill-like name '$name'"
    elif ! printf '%s\n' "$requires" | grep -qx "$name"; then
      fail "$cookbook references skill '$name' but does not declare it under ## Requires"
    fi
  done

  install_block=$(awk '/^Install everything:/{flag=1; next} /^## /{if (flag) exit} flag' "$cookbook")
  if [ -z "$install_block" ]; then
    fail "$cookbook has no install command"
  else
    for name in "$cookbook_name" $requires; do
      if ! printf '%s\n' "$install_block" \
        | grep -Eq "(^|[[:space:]])${name}([[:space:]\\\\]|$)"; then
        fail "$cookbook install command omits '$name'"
      fi
    done
  fi
done

if [ "$found_cookbook" -eq 0 ]; then
  fail "no cookbooks found under cookbooks/"
fi

for entry in $manifest_entries; do
  case "$entry" in
    ./cookbooks/*)
      if [ ! -f "${entry#./}/SKILL.md" ]; then
        fail "$manifest references '$entry' but no cookbook SKILL.md exists"
      fi
      ;;
    *)
      fail "$manifest entry '$entry' is outside cookbooks/"
      ;;
  esac
done

if [ "$status" -eq 0 ]; then
  echo "OK: all cookbook dependencies, install commands, and manifest entries resolve"
fi
exit "$status"
