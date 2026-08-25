#!/usr/bin/env bash
# Validate Cursor support against existing portable Agent Plugins category packages.
set -euo pipefail

cd "$(dirname "$0")/.."

python3 - <<'PY'
import json
import os
import sys
from pathlib import Path

root = Path.cwd().resolve()
plugins_root = root / "plugins"
errors = []


def fail(message):
    errors.append(message)


if not plugins_root.is_dir():
    fail("plugins/ must contain at least one category")
    plugins_real = None
else:
    try:
        plugins_real = plugins_root.resolve()
    except OSError as error:
        fail(f"cannot resolve plugins/: {error}")
        plugins_real = None
    else:
        if not plugins_real.is_relative_to(root):
            fail(f"plugins/ resolves outside the repository: {plugins_real}")
            plugins_real = None

plugin_dirs = []
if plugins_real is not None:
    for path in sorted(plugins_root.iterdir()):
        if not path.is_dir():
            continue
        try:
            category_real = path.resolve()
        except OSError as error:
            fail(f"cannot resolve {path}: {error}")
            continue
        if not category_real.is_relative_to(plugins_real):
            fail(f"{path} resolves outside the plugins root")
            continue
        plugin_dirs.append((path, category_real))

if plugins_real is not None and not plugin_dirs:
    fail("plugins/ must contain at least one category")

for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
    rel = Path(dirpath).relative_to(root)
    if rel.parts and rel.parts[0] == ".git":
        dirnames[:] = []
        continue
    if ".cursor-plugin" in rel.parts:
        fail(f"Cursor-native path must not exist: {rel}")
        dirnames[:] = []
        continue
    if ".cursor-plugin" in dirnames:
        fail(f"Cursor-native path must not exist: {rel / '.cursor-plugin'}")

marketplace = root / ".cursor-plugin" / "marketplace.json"
if marketplace.exists():
    fail(f"Cursor marketplace must not exist: {marketplace}")

for plugin_dir, category_real in plugin_dirs:
    manifest_path = plugin_dir / "plugin.json"
    try:
        if not manifest_path.resolve().is_relative_to(category_real):
            fail(f"{manifest_path} resolves outside its plugin root")
            continue
    except OSError as error:
        fail(f"cannot resolve {manifest_path}: {error}")
        continue

    if not manifest_path.is_file():
        fail(f"missing portable Agent Plugins manifest: {manifest_path}")
        continue

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"{manifest_path} is not valid JSON: {error}")
        continue
    if not isinstance(manifest, dict):
        fail(f"{manifest_path} must contain a JSON object")
        continue

    expected_name = f"majestic-{plugin_dir.name}"
    if manifest.get("name") != expected_name:
        fail(f"{manifest_path} declares {manifest.get('name')!r}, expected {expected_name!r}")

    cursor_native = plugin_dir / ".cursor-plugin"
    if cursor_native.exists():
        fail(f"Cursor-native path must not exist: {cursor_native}")

    skills_dir = plugin_dir / "skills"
    if not skills_dir.is_dir():
        fail(f"{skills_dir} must be a directory")
        continue
    try:
        if not skills_dir.resolve().is_relative_to(category_real):
            fail(f"{skills_dir} resolves outside its plugin root")
            continue
    except OSError as error:
        fail(f"cannot resolve {skills_dir}: {error}")
        continue

    immediate = []
    for child in sorted(skills_dir.iterdir()):
        if child.name.startswith("."):
            continue
        if not child.is_dir():
            continue
        skill_file = child / "SKILL.md"
        if not skill_file.is_file():
            fail(f"{child} is an immediate skill directory without SKILL.md")
            continue
        try:
            if not skill_file.resolve().is_relative_to(category_real):
                fail(f"{skill_file} resolves outside its plugin root")
                continue
        except OSError as error:
            fail(f"cannot resolve {skill_file}: {error}")
            continue
        immediate.append(skill_file)

    if not immediate:
        fail(f"{skills_dir} must contain at least one immediate skill")

    discovered = set(immediate)
    for nested in skills_dir.glob("**/SKILL.md"):
        if nested not in discovered:
            fail(f"{nested} is nested too deeply for Cursor/Agent Plugins discovery")

    for directory, subdirs, filenames in os.walk(plugin_dir, followlinks=False):
        for name in [*subdirs, *filenames]:
            path = Path(directory) / name
            if not path.is_symlink():
                continue
            try:
                if not path.resolve().is_relative_to(category_real):
                    fail(f"{path} is a symlink that resolves outside its plugin root")
            except OSError as error:
                fail(f"cannot resolve symlink {path}: {error}")

if errors:
    for error in errors:
        print(f"FAIL: {error}")
    sys.exit(1)

print(f"OK: {len(plugin_dirs)} portable category packages are Cursor-compatible")
PY

echo "Checking Cursor local symlink route via adapter contracts"
bash scripts/check-adapter-contracts.sh --cursor

echo "OK: Cursor portable package validation complete"
