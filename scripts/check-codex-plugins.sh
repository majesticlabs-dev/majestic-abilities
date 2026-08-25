#!/usr/bin/env bash
# Verify Codex manifests and marketplace wiring with repository-owned validation.
# An optional external validator may be provided via CODEX_PLUGIN_VALIDATOR.
set -euo pipefail

cd "$(dirname "$0")/.."

marketplace=".agents/plugins/marketplace.json"
status=0

fail() {
  echo "FAIL: $1"
  status=1
}

if [ ! -f "$marketplace" ]; then
  fail "$marketplace is required for the repo Codex marketplace"
fi

python3 - "$marketplace" <<'PY' || status=1
import json
import os
import sys

marketplace_path = sys.argv[1]
errors = []


def fail(message):
    errors.append(message)


REQUIRED_NATIVE = {
    "name",
    "version",
    "description",
    "author",
    "license",
    "keywords",
    "skills",
    "interface",
}
REQUIRED_INTERFACE = {
    "displayName",
    "shortDescription",
    "longDescription",
    "developerName",
    "category",
    "capabilities",
    "defaultPrompt",
}
INSTALLATION_POLICIES = {"NOT_AVAILABLE", "AVAILABLE", "INSTALLED_BY_DEFAULT"}
AUTHENTICATION_POLICIES = {"ON_INSTALL", "ON_USE"}


def load_json(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


if not os.path.isfile(marketplace_path):
    fail(f"{marketplace_path} is required")
    for message in errors:
        print(f"FAIL: {message}")
    raise SystemExit(1)

marketplace = load_json(marketplace_path)
plugins = marketplace.get("plugins")
if not isinstance(plugins, list):
    fail("marketplace 'plugins' must be an array")
    plugins = []

listed = {}
for entry in plugins:
    if not isinstance(entry, dict):
        fail(f"marketplace entry {entry!r} must be an object")
        continue
    name = entry.get("name")
    source = entry.get("source")
    policy = entry.get("policy")
    category = entry.get("category")

    if not isinstance(name, str) or not name:
        fail(f"marketplace entry {entry!r} needs a non-empty 'name'")
        continue
    if not isinstance(source, dict) or source.get("source") != "local":
        fail(f"marketplace entry '{name}' needs a local source object")
        continue
    source_path = source.get("path")
    if not isinstance(source_path, str) or not source_path.startswith("./plugins/"):
        fail(f"marketplace entry '{name}' source path must start with './plugins/'")
        continue
    if not isinstance(policy, dict):
        fail(f"marketplace entry '{name}' needs a policy object")
    else:
        if policy.get("installation") not in INSTALLATION_POLICIES:
            fail(f"marketplace entry '{name}' has invalid installation policy")
        if policy.get("authentication") not in AUTHENTICATION_POLICIES:
            fail(f"marketplace entry '{name}' has invalid authentication policy")
    if not isinstance(category, str) or not category:
        fail(f"marketplace entry '{name}' needs a non-empty category")

    plugin_path = source_path[2:]
    if name in listed:
        fail(f"marketplace lists plugin '{name}' more than once")
    listed[name] = plugin_path

    manifest_path = os.path.join(plugin_path, ".codex-plugin", "plugin.json")
    if not os.path.isfile(manifest_path):
        fail(f"marketplace entry '{name}' has no Codex manifest at {manifest_path}")

for category in sorted(os.listdir("plugins")):
    plugin_path = os.path.join("plugins", category)
    if not os.path.isdir(plugin_path):
        continue
    manifest_path = os.path.join(plugin_path, ".codex-plugin", "plugin.json")
    if not os.path.isfile(manifest_path):
        fail(f"{plugin_path} has no Codex manifest at {manifest_path}")
        continue

    try:
        manifest = load_json(manifest_path)
    except (OSError, json.JSONDecodeError) as error:
        fail(f"{manifest_path} is not valid JSON: {error}")
        continue
    if not isinstance(manifest, dict):
        fail(f"{manifest_path} must contain a JSON object")
        continue

    missing = sorted(REQUIRED_NATIVE - set(manifest))
    if missing:
        fail(f"{manifest_path} missing required fields: {', '.join(missing)}")

    name = manifest.get("name")
    if not isinstance(name, str) or not name:
        fail(f"{manifest_path} needs a non-empty name")
    for field in ("version", "description", "license", "skills"):
        if field in manifest and not isinstance(manifest[field], str):
            fail(f"{manifest_path} field {field!r} must be a string")
    if manifest.get("skills") != "./skills/":
        fail(f"{manifest_path} field 'skills' must be './skills/'")

    author = manifest.get("author")
    if author is not None and not isinstance(author, dict):
        fail(f"{manifest_path} field 'author' must be an object")
    keywords = manifest.get("keywords")
    if keywords is not None and (
        not isinstance(keywords, list) or any(not isinstance(item, str) for item in keywords)
    ):
        fail(f"{manifest_path} field 'keywords' must be an array of strings")

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        fail(f"{manifest_path} field 'interface' must be an object")
    else:
        missing_interface = sorted(REQUIRED_INTERFACE - set(interface))
        if missing_interface:
            fail(
                f"{manifest_path} interface missing fields: {', '.join(missing_interface)}"
            )
        for field in (
            "displayName",
            "shortDescription",
            "longDescription",
            "developerName",
            "category",
        ):
            if field in interface and not isinstance(interface[field], str):
                fail(f"{manifest_path} interface.{field} must be a string")
        capabilities = interface.get("capabilities")
        if not isinstance(capabilities, list) or any(
            not isinstance(item, str) for item in capabilities
        ):
            fail(f"{manifest_path} interface.capabilities must be an array of strings")
        default_prompt = interface.get("defaultPrompt")
        if not isinstance(default_prompt, list) or any(
            not isinstance(item, str) for item in default_prompt
        ):
            fail(f"{manifest_path} interface.defaultPrompt must be an array of strings")

    skills_dir = os.path.join(plugin_path, "skills")
    if not os.path.isdir(skills_dir):
        fail(f"{skills_dir} must exist for Codex skills path ./skills/")
    elif not any(os.path.isdir(os.path.join(skills_dir, name)) for name in os.listdir(skills_dir)):
        fail(f"{skills_dir} must contain at least one skill directory")

    if name not in listed:
        fail(f"{plugin_path} manifest '{name}' is not listed in {marketplace_path}")
    elif listed[name] != plugin_path:
        fail(
            f"marketplace entry '{name}' points to {listed[name]}, expected {plugin_path}"
        )

for message in errors:
    print(f"FAIL: {message}")
raise SystemExit(1 if errors else 0)
PY

if [ -n "${CODEX_PLUGIN_VALIDATOR:-}" ]; then
  if [ -f "$CODEX_PLUGIN_VALIDATOR" ]; then
    for plugin in plugins/*; do
      [ -d "$plugin" ] || continue
      if ! python3 "$CODEX_PLUGIN_VALIDATOR" "$plugin"; then
        status=1
      fi
    done
  else
    fail "CODEX_PLUGIN_VALIDATOR is set but not found: $CODEX_PLUGIN_VALIDATOR"
  fi
fi

if [ "$status" -eq 0 ]; then
  echo "OK: Codex manifests, marketplace entries, and skill trees all resolve"
fi
exit "$status"
