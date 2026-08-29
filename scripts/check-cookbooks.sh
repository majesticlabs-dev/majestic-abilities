#!/usr/bin/env bash
# Verify cookbook placement, dependency declarations, install commands, and marketplace wiring.
set -euo pipefail

cd "$(dirname "$0")/.."

marketplace=".claude-plugin/marketplace.json"

status=0
found_cookbook=0
hosted_cookbook_count=0

fail() {
  echo "FAIL: $1"
  status=1
}

# A cookbook is any SKILL.md that declares metadata.requires. Every cookbook
# lives in the plugin that owns its primary user trigger and output. Supporting
# skills may come from other plugins and remain explicit dependencies.
cookbooks=$(
  for skill in plugins/*/skills/*/SKILL.md; do
    [ -f "$skill" ] || continue
    awk '
      NR == 1 && $0 == "---" { in_frontmatter=1; next }
      in_frontmatter && $0 == "---" { exit !found }
      in_frontmatter && $0 == "metadata:" { in_metadata=1; next }
      in_metadata && /^[^[:space:]]/ { in_metadata=0 }
      in_metadata && /^  requires:/ { found=1 }
    ' "$skill" && printf '%s\n' "$skill"
  done
  true
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

  hosted_cookbook_count=$((hosted_cookbook_count + 1))

  if [ -z "$cookbook_name" ]; then
    fail "$cookbook has no name in frontmatter"
  elif [ "$cookbook_name" != "$cookbook_dir" ]; then
    fail "$cookbook name '$cookbook_name' does not match directory '$cookbook_dir'"
  elif echo "$skill_names" | grep -qx "$cookbook_name"; then
    fail "$cookbook name '$cookbook_name' collides with a catalog skill"
  fi

  expected_plugin=""
  case "$cookbook_name" in
    ai-search-visibility-foundation) expected_plugin="seo" ;;
    founder-launch-decision|founder-next-stage-decision) expected_plugin="founder" ;;
    product-engineering-handoff) expected_plugin="product" ;;
    rails-feature) expected_plugin="rails" ;;
  esac
  if [ -n "$expected_plugin" ]; then
    expected_path="plugins/$expected_plugin/skills/$cookbook_name/SKILL.md"
    if [ "$cookbook" != "$expected_path" ]; then
      fail "$cookbook belongs at $expected_path based on its primary domain"
    fi
  fi

  if grep -Fq '$ARGUMENTS' "$cookbook"; then
    fail "$cookbook uses harness-specific \$ARGUMENTS instead of the user's request"
  fi
  if grep -Eq 'invokes /[a-z0-9][a-z0-9-]*' "$cookbook"; then
    fail "$cookbook uses harness-specific slash invocation syntax"
  fi

  metadata_requires=$(awk '
    NR == 1 && $0 == "---" { in_frontmatter=1; next }
    in_frontmatter && $0 == "---" { exit }
    in_frontmatter && $0 == "metadata:" { in_metadata=1; next }
    in_metadata && /^[^[:space:]]/ { in_metadata=0 }
    in_metadata && /^  requires:/ {
      sub(/^  requires:[[:space:]]*/, "")
      gsub(/^"|"$/, "")
      print
      exit
    }
  ' "$cookbook" | tr ',' '\n' | sed -E 's/^[[:space:]]+|[[:space:]]+$//g' | grep -v '^$' || true)

  if [ -z "$metadata_requires" ]; then
    fail "$cookbook has no metadata.requires dependencies"
    continue
  fi
  if grep -q '^## Requires$' "$cookbook"; then
    fail "$cookbook uses an obsolete ## Requires section; metadata.requires is authoritative"
  fi
  if [ "$(printf '%s\n' "$metadata_requires" | wc -l | tr -d ' ')" -ne "$(printf '%s\n' "$metadata_requires" | sort -u | wc -l | tr -d ' ')" ]; then
    fail "$cookbook metadata.requires contains duplicate dependencies"
  fi

  required_plugins=""
  for name in $metadata_requires; do
    if ! echo "$skill_names" | grep -qx "$name"; then
      fail "$cookbook requires '$name' but no skill with that name exists"
      continue
    fi
    required_plugins="$required_plugins
$(printf '%s\n' "$skill_index" | awk -F'\t' -v n="$name" '$1 == n {print $2; exit}')"
  done
  required_plugins=$(printf '%s\n' "$required_plugins" | grep -v '^$' | sort -u)
  plugin_count=$(printf '%s\n' "$required_plugins" | grep -c . || true)

  # Plugin ownership follows the cookbook's primary domain, not dependency
  # closure. Its metadata.requires can name supporting skills from any plugin.
  if [ "$plugin_count" -eq 0 ]; then
    fail "$cookbook has no resolved plugin dependencies"
  fi

  body_refs=$(grep -oE '`[a-z0-9][a-z0-9-]*`' "$cookbook" \
    | tr -d '`' | sort -u || true)
  for name in $body_refs; do
    if ! echo "$skill_names" | grep -qx "$name"; then
      fail "$cookbook references unknown skill-like name '$name'"
    elif ! printf '%s\n' "$metadata_requires" | grep -qx "$name"; then
      fail "$cookbook references skill '$name' but does not declare it in metadata.requires"
    fi
  done

  install_block=$(awk '/^## Installation/{flag=1; next} /^## /{if (flag) exit} flag' "$cookbook")
  if [ -z "$install_block" ]; then
    fail "$cookbook has no install command"
  else
    if ! printf '%s\n' "$install_block" | grep -Fq 'npx skills add majesticlabs-dev/majestic-abilities'; then
      fail "$cookbook install command must use the public Majestic Abilities Skills CLI source"
    fi
    expected_install_names=$(printf '%s\n%s\n' "$cookbook_name" "$metadata_requires" | sort -u)
    install_names=""
    for name in "$cookbook_name" $skill_names; do
      if printf '%s\n' "$install_block" \
        | grep -Eq "(^|[[:space:]])${name}([[:space:]\\\\]|$)"; then
        install_names="$install_names
$name"
      fi
    done
    install_names=$(printf '%s\n' "$install_names" | grep -v '^$' | sort -u)
    if [ "$install_names" != "$expected_install_names" ]; then
      fail "$cookbook install command and metadata.requires dependencies differ"
    fi
    if printf '%s\n' "$install_block" | grep -Eq -- '(^|[[:space:]])--agent([=[:space:]]|$)'; then
      fail "$cookbook install command must be harness-neutral and cannot use --agent"
    fi
    if printf '%s\n' "$install_block" | grep -Eq '(/plugin install|codex plugin)'; then
      fail "$cookbook install command must not use a harness-native plugin command"
    fi
  fi
done

if [ "$found_cookbook" -eq 0 ]; then
  fail "no cookbooks found under plugins/*/skills/"
fi
if [ "$hosted_cookbook_count" -ne 5 ]; then
  fail "expected 5 plugin-hosted cookbooks, found $hosted_cookbook_count"
fi
if [ -d skills ] || [ -d cookbooks ]; then
  fail "top-level skills/ and cookbooks/ are obsolete; every cookbook must live in its primary domain plugin"
fi

if [ "$status" -eq 0 ]; then
  echo "OK: cookbook placement, dependencies, install commands, and marketplace entries all resolve"
fi
exit "$status"
