#!/usr/bin/env bash
# Verify that every skill a cookbook references in its "## Requires" section
# exists in skills/, and that cookbook names don't collide with skill names.
set -euo pipefail

cd "$(dirname "$0")/.."

skill_names=$(grep -h '^name:' skills/*/*/SKILL.md | sed -E 's/^name:[[:space:]]*"?([^"]*)"?[[:space:]]*$/\1/')

status=0
found_cookbook=0

for cookbook in cookbooks/*/SKILL.md; do
  [ -f "$cookbook" ] || continue
  found_cookbook=1

  cookbook_name=$(grep -m1 '^name:' "$cookbook" | sed -E 's/^name:[[:space:]]*"?([^"]*)"?[[:space:]]*$/\1/')
  if [ -z "$cookbook_name" ]; then
    echo "FAIL: $cookbook has no name in frontmatter"
    status=1
  elif echo "$skill_names" | grep -qx "$cookbook_name"; then
    echo "FAIL: $cookbook name '$cookbook_name' collides with a skill in skills/"
    status=1
  fi

  # Requires entries look like: - `skill-name` — reason
  requires=$(awk '/^## Requires/{flag=1; next} /^## /{flag=0} flag' "$cookbook" \
    | grep -E '^- `' | sed -E 's/^- `([^`]+)`.*/\1/' || true)

  if [ -z "$requires" ]; then
    echo "FAIL: $cookbook has no '## Requires' entries"
    status=1
    continue
  fi

  for name in $requires; do
    if ! echo "$skill_names" | grep -qx "$name"; then
      echo "FAIL: $cookbook requires '$name' but no skill with that name exists"
      status=1
    fi
  done
done

if [ "$found_cookbook" -eq 0 ]; then
  echo "FAIL: no cookbooks found under cookbooks/"
  status=1
fi

if [ "$status" -eq 0 ]; then
  echo "OK: all cookbook skill references resolve"
fi
exit $status
