#!/usr/bin/env python3

import argparse
import json
import re
import sys
from pathlib import Path


SEMVER = re.compile(
    r"^(0|[1-9][0-9]*)\."
    r"(0|[1-9][0-9]*)\."
    r"(0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
CATEGORY = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def fail(message):
    raise ValueError(message)


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"required file does not exist: {path}")
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot read valid JSON from {path}: {error}")


def replace_single_version(text, old_version, new_version, path):
    pattern = re.compile(r'^(\s*"version"\s*:\s*")([^"\n]+)(".*)$', re.MULTILINE)
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        fail(f"expected one version field in {path}, found {len(matches)}")
    if matches[0].group(2) != old_version:
        fail(
            f"version text in {path} is {matches[0].group(2)!r}, "
            f"expected {old_version!r}"
        )
    return pattern.sub(
        lambda match: f"{match.group(1)}{new_version}{match.group(3)}",
        text,
        count=1,
    )


def replace_marketplace_entry_version(
    text, plugin_name, old_version, new_version, path
):
    lines = text.splitlines(keepends=True)
    name_pattern = re.compile(
        rf'^(\s*)"name"\s*:\s*"{re.escape(plugin_name)}"\s*,?\s*$'
    )
    name_indexes = []
    field_indent = None

    for index, line in enumerate(lines):
        match = name_pattern.match(line.rstrip("\r\n"))
        if match:
            name_indexes.append(index)
            field_indent = match.group(1)

    if len(name_indexes) != 1:
        fail(f"expected one {plugin_name!r} entry in {path}, found {len(name_indexes)}")

    version_indexes = []
    for index in range(name_indexes[0] + 1, len(lines)):
        stripped = lines[index].rstrip("\r\n")
        if stripped.startswith(field_indent + '"name"'):
            break
        if stripped.startswith(field_indent + '"version"'):
            version_indexes.append(index)
        if stripped.startswith(field_indent[:-2] + "}"):
            break

    if len(version_indexes) != 1:
        fail(
            f"expected one version field for {plugin_name!r} in {path}, "
            f"found {len(version_indexes)}"
        )

    index = version_indexes[0]
    pattern = re.compile(r'("version"\s*:\s*")([^"\n]+)(")')
    match = pattern.search(lines[index])
    if match is None or match.group(2) != old_version:
        actual = match.group(2) if match else "missing"
        fail(
            f"marketplace version for {plugin_name!r} is {actual!r}, "
            f"expected {old_version!r}"
        )
    lines[index] = pattern.sub(
        lambda item: f"{item.group(1)}{new_version}{item.group(3)}",
        lines[index],
        count=1,
    )
    return "".join(lines)


def update_plugin_version(root, category, new_version):
    if not CATEGORY.fullmatch(category):
        fail(f"invalid plugin category: {category!r}")
    if not SEMVER.fullmatch(new_version):
        fail(f"target must be a valid semantic version: {new_version!r}")

    plugin_name = f"majestic-{category}"
    plugin_dir = root / "plugins" / category
    manifest_paths = [
        plugin_dir / "plugin.json",
        plugin_dir / ".claude-plugin" / "plugin.json",
        plugin_dir / ".codex-plugin" / "plugin.json",
    ]
    marketplace_path = root / ".claude-plugin" / "marketplace.json"

    manifests = [(path, load_json(path)) for path in manifest_paths]
    for path, manifest in manifests:
        if manifest.get("name") != plugin_name:
            fail(f"{path} declares {manifest.get('name')!r}, expected {plugin_name!r}")

    current_versions = {manifest.get("version") for _, manifest in manifests}
    marketplace = load_json(marketplace_path)
    entries = marketplace.get("plugins")
    if not isinstance(entries, list):
        fail(f"{marketplace_path} must contain a plugins array")
    matching_entries = [
        entry
        for entry in entries
        if isinstance(entry, dict)
        and entry.get("name") == plugin_name
        and entry.get("source") == f"./plugins/{category}"
    ]
    if len(matching_entries) != 1:
        fail(
            f"expected one marketplace entry for {plugin_name!r} in "
            f"{marketplace_path}, found {len(matching_entries)}"
        )
    current_versions.add(matching_entries[0].get("version"))

    if len(current_versions) != 1 or None in current_versions:
        displayed = sorted(repr(version) for version in current_versions)
        fail(f"current versions do not match: {', '.join(displayed)}")

    old_version = current_versions.pop()
    if old_version == new_version:
        fail(f"plugin {plugin_name!r} is already at version {new_version}")

    updates = {}
    for path, _ in manifests:
        text = path.read_text(encoding="utf-8")
        updates[path] = replace_single_version(
            text, old_version, new_version, path
        )

    marketplace_text = marketplace_path.read_text(encoding="utf-8")
    updates[marketplace_path] = replace_marketplace_entry_version(
        marketplace_text,
        plugin_name,
        old_version,
        new_version,
        marketplace_path,
    )

    for path, text in updates.items():
        path.write_text(text, encoding="utf-8")

    return old_version, list(updates)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Update one category plugin version across release metadata."
    )
    parser.add_argument("category", help="plugin directory name, for example rails")
    parser.add_argument("version", help="target semantic version")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[4],
        help="repository root, used by tests and alternate checkouts",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        old_version, paths = update_plugin_version(
            args.root.resolve(), args.category, args.version
        )
    except ValueError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1

    print(f"Updated majestic-{args.category}: {old_version} -> {args.version}")
    for path in paths:
        print(path.relative_to(args.root.resolve()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
