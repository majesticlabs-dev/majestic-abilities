#!/usr/bin/env bash
# Verify cookbook placement, dependency declarations, install commands, and marketplace wiring.
set -euo pipefail

cd "$(dirname "$0")/.."

marketplace=".claude-plugin/marketplace.json"

status=0
found_cookbook=0

fail() {
  echo "FAIL: $1"
  status=1
}

# A cookbook is any SKILL.md that declares a '## Requires' section. Cookbooks live
# either inside the single plugin owning all their skills, or in top-level
# cookbooks/ when they span two or more plugins.
cookbooks=$(
  for skill in plugins/*/skills/*/SKILL.md cookbooks/*/SKILL.md; do
    [ -f "$skill" ] || continue
    grep -q '^## Requires' "$skill" && printf '%s\n' "$skill"
  done
)

# One "<skill-name><TAB><plugin-name>" line per catalog skill, so a cookbook can be
# checked against both install routes. Cookbooks are excluded: they are the
# composition layer, not catalog skills another cookbook may require.
skill_index=$(
  for skill in plugins/*/skills/*/SKILL.md; do
    [ -f "$skill" ] || continue
    printf '%s\n' "$cookbooks" | grep -qx "$skill" && continue
    category=$(basename "$(dirname "$(dirname "$(dirname "$skill")")")")
    name=$(grep -m1 '^name:' "$skill" \
      | sed -E 's/^name:[[:space:]]*"?([^"]*)"?[[:space:]]*$/\1/')
    printf '%s\tmajestic-%s\n' "$name" "$category"
  done
)
skill_names=$(printf '%s\n' "$skill_index" | cut -f1)

if [ ! -f "$marketplace" ]; then
  fail "$marketplace is required so each category installs as a separate plugin"
elif ! python3 - "$marketplace" <<'PY'
import json
import os
import sys

with open(sys.argv[1]) as file:
    data = json.load(file)

entries = data.get("plugins")
if not isinstance(entries, list):
    sys.exit("marketplace 'plugins' must be an array")

status = 0
listed = {}

for entry in entries:
    name, source = entry.get("name"), entry.get("source")
    if not isinstance(name, str) or not isinstance(source, str):
        print(f"FAIL: marketplace entry {entry!r} needs a string 'name' and 'source'")
        status = 1
        continue
    if not source.startswith("./plugins/"):
        print(f"FAIL: marketplace entry '{name}' source '{source}' is outside plugins/")
        status = 1
        continue

    path = source[len("./"):]
    listed[path] = name

    manifest = os.path.join(path, ".claude-plugin", "plugin.json")
    if not os.path.isfile(manifest):
        print(f"FAIL: marketplace entry '{name}' has no plugin manifest at {manifest}")
        status = 1
        continue
    with open(manifest) as file:
        declared = json.load(file).get("name")
    if declared != name:
        print(f"FAIL: {manifest} declares name '{declared}' but the marketplace lists '{name}'")
        status = 1

for directory in sorted(os.listdir("plugins")):
    path = os.path.join("plugins", directory)
    if os.path.isdir(path) and path not in listed:
        print(f"FAIL: {path} is not listed in {sys.argv[1]} and cannot be installed")
        status = 1

sys.exit(status)
PY
then
  status=1
fi

for cookbook in $cookbooks; do
  found_cookbook=1

  cookbook_dir=$(basename "$(dirname "$cookbook")")
  cookbook_name=$(grep -m1 '^name:' "$cookbook" | sed -E 's/^name:[[:space:]]*"?([^"]*)"?[[:space:]]*$/\1/' || true)

  # Empty for a top-level cookbook, otherwise the plugin shipping it.
  host_plugin=""
  case "$cookbook" in
    plugins/*)
      host_plugin="majestic-$(basename "$(dirname "$(dirname "$(dirname "$cookbook")")")")"
      ;;
  esac

  if [ -z "$cookbook_name" ]; then
    fail "$cookbook has no name in frontmatter"
  elif [ "$cookbook_name" != "$cookbook_dir" ]; then
    fail "$cookbook name '$cookbook_name' does not match directory '$cookbook_dir'"
  elif echo "$skill_names" | grep -qx "$cookbook_name"; then
    fail "$cookbook name '$cookbook_name' collides with a catalog skill"
  fi

  # Requires entries look like: - `skill-name` - reason
  requires=$(awk '/^## Requires/{flag=1; next} /^## /{flag=0} flag' "$cookbook" \
    | grep -E '^- `' | sed -E 's/^- `([^`]+)`.*/\1/' || true)

  if [ -z "$requires" ]; then
    fail "$cookbook has no '## Requires' entries"
    continue
  fi

  required_plugins=""
  for name in $requires; do
    if ! echo "$skill_names" | grep -qx "$name"; then
      fail "$cookbook requires '$name' but no skill with that name exists"
      continue
    fi
    required_plugins="$required_plugins
$(printf '%s\n' "$skill_index" | awk -F'\t' -v n="$name" '$1 == n {print $2; exit}')"
  done
  required_plugins=$(printf '%s\n' "$required_plugins" | grep -v '^$' | sort -u)
  plugin_count=$(printf '%s\n' "$required_plugins" | grep -c . || true)

  # Placement rule: a single-plugin cookbook ships inside that plugin, a
  # cross-plugin cookbook stays in cookbooks/ and installs via the Skills CLI only.
  if [ "$plugin_count" -eq 1 ]; then
    if [ -z "$host_plugin" ]; then
      fail "$cookbook needs only '$required_plugins' and belongs in plugins/${required_plugins#majestic-}/skills/"
    elif [ "$host_plugin" != "$required_plugins" ]; then
      fail "$cookbook ships in '$host_plugin' but its skills all live in '$required_plugins'"
    fi
  elif [ -n "$host_plugin" ]; then
    fail "$cookbook spans $plugin_count plugins ($(printf '%s' "$required_plugins" | tr '\n' ' ')) and belongs in cookbooks/"
  fi

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
        fail "$cookbook install command omits skill '$name'"
      fi
    done
    if [ -n "$host_plugin" ]; then
      if ! printf '%s\n' "$install_block" | grep -Fq "${host_plugin}@"; then
        fail "$cookbook install command omits plugin '$host_plugin'"
      fi
    elif printf '%s\n' "$install_block" | grep -Fq "/plugin install"; then
      fail "$cookbook spans plugins and must not advertise a /plugin install route"
    fi
  fi
done

if [ "$found_cookbook" -eq 0 ]; then
  fail "no cookbooks found in cookbooks/ or under plugins/*/skills/"
fi

if [ "$status" -eq 0 ]; then
  echo "OK: cookbook placement, dependencies, install commands, and marketplace entries all resolve"
fi
exit "$status"
