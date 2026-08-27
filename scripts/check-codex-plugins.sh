#!/usr/bin/env bash
# Verify Codex manifests, marketplace wiring, and shared skill trees.
set -euo pipefail

cd "$(dirname "$0")/.."

marketplace=".agents/plugins/marketplace.json"
validator="${CODEX_PLUGIN_VALIDATOR:-scripts/vendor/codex-plugin-validator/validate_plugin.py}"
status=0

fail() {
  echo "FAIL: $1"
  status=1
}

if [ ! -f "$marketplace" ]; then
  fail "$marketplace is required for the repo Codex marketplace"
else
  if ! python3 - "$marketplace" <<'PY'
import json
import os
import sys

marketplace_path = sys.argv[1]
with open(marketplace_path, encoding="utf-8") as file:
    marketplace = json.load(file)

plugins = marketplace.get("plugins")
if not isinstance(plugins, list):
    raise SystemExit("marketplace 'plugins' must be an array")

listed = {}
status = 0

for entry in plugins:
    name = entry.get("name")
    source = entry.get("source")
    policy = entry.get("policy")
    category = entry.get("category")

    if not isinstance(name, str) or not name:
        print(f"FAIL: marketplace entry {entry!r} needs a non-empty 'name'")
        status = 1
        continue
    if not isinstance(source, dict) or source.get("source") != "local":
        print(f"FAIL: marketplace entry '{name}' needs a local source object")
        status = 1
        continue
    source_path = source.get("path")
    if not isinstance(source_path, str) or not source_path.startswith("./plugins/"):
        print(f"FAIL: marketplace entry '{name}' source path must start with './plugins/'")
        status = 1
        continue
    if not isinstance(policy, dict):
        print(f"FAIL: marketplace entry '{name}' needs a policy object")
        status = 1
    elif policy.get("installation") not in {"NOT_AVAILABLE", "AVAILABLE", "INSTALLED_BY_DEFAULT"}:
        print(f"FAIL: marketplace entry '{name}' has invalid installation policy")
        status = 1
    elif policy.get("authentication") not in {"ON_INSTALL", "ON_USE"}:
        print(f"FAIL: marketplace entry '{name}' has invalid authentication policy")
        status = 1
    if not isinstance(category, str) or not category:
        print(f"FAIL: marketplace entry '{name}' needs a non-empty category")
        status = 1

    plugin_path = source_path[2:]
    if name in listed:
        print(f"FAIL: marketplace lists plugin '{name}' more than once")
        status = 1
    listed[name] = plugin_path

    manifest_path = os.path.join(plugin_path, ".codex-plugin", "plugin.json")
    if not os.path.isfile(manifest_path):
        print(f"FAIL: marketplace entry '{name}' has no Codex manifest at {manifest_path}")
        status = 1

for category in sorted(os.listdir("plugins")):
    plugin_path = os.path.join("plugins", category)
    if not os.path.isdir(plugin_path):
        continue
    manifest_path = os.path.join(plugin_path, ".codex-plugin", "plugin.json")
    if not os.path.isfile(manifest_path):
        print(f"FAIL: {plugin_path} has no Codex manifest at {manifest_path}")
        status = 1
        continue
    with open(manifest_path, encoding="utf-8") as file:
        manifest = json.load(file)
    name = manifest.get("name")
    claude_manifest_path = os.path.join(plugin_path, ".claude-plugin", "plugin.json")
    if not os.path.isfile(claude_manifest_path):
        print(f"FAIL: {plugin_path} has no Claude manifest at {claude_manifest_path}")
        status = 1
    else:
        with open(claude_manifest_path, encoding="utf-8") as file:
            claude_manifest = json.load(file)
        if claude_manifest.get("name") != name:
            print(f"FAIL: {plugin_path} Claude and Codex manifest names do not match")
            status = 1
    if name not in listed:
        print(f"FAIL: {plugin_path} manifest '{name}' is not listed in {marketplace_path}")
        status = 1
    elif listed[name] != plugin_path:
        print(f"FAIL: marketplace entry '{name}' points to {listed[name]}, expected {plugin_path}")
        status = 1

sys.exit(status)
PY
  then
    status=1
  fi
fi

if [ ! -f "$validator" ]; then
  fail "Codex plugin validator not found at $validator"
else
  for plugin in plugins/*; do
    [ -d "$plugin" ] || continue
    if ! python3 "$validator" "$plugin"; then
      status=1
    fi
  done
fi

if [ "$status" -eq 0 ]; then
  echo "OK: Codex manifests, marketplace entries, and skill trees all resolve"
fi
exit "$status"
