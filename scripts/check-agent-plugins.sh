#!/usr/bin/env bash
# Verify Agent Plugins, harness marketplaces, the Pi package, skill discovery, and containment.
set -euo pipefail

cd "$(dirname "$0")/.."

python3 - <<'PY'
import json
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError:
    sys.exit("FAIL: PyYAML is required; install requirements-dev.txt")

PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
ALLOWED_PLUGIN_FIELDS = {
    "$schema",
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
    "extensions",
}
PORTABLE_METADATA_FIELDS = {
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
}
REQUIRED_PROJECT_FIELDS = {
    "name",
    "version",
    "description",
    "author",
    "license",
    "keywords",
}
PLUGIN_NAME = re.compile(r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
SKILL_NAME = re.compile(r"^(?!.*--)[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")
ALLOWED_SKILL_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
REPOSITORY_SKILL_FIELDS = ALLOWED_SKILL_FIELDS | {"disable-model-invocation"}


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def construct_unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    construct_unique_mapping,
)

errors = []


def fail(message):
    errors.append(message)


def load_object(path):
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"{path} is required")
        return None
    except (OSError, json.JSONDecodeError) as error:
        fail(f"{path} is not valid JSON: {error}")
        return None
    if not isinstance(value, dict):
        fail(f"{path} must contain a JSON object")
        return None
    return value


def validate_portable_manifest(path):
    manifest = load_object(path)
    if manifest is None:
        return None

    unknown = sorted(set(manifest) - ALLOWED_PLUGIN_FIELDS)
    if unknown:
        fail(f"{path} has unsupported top-level fields: {', '.join(unknown)}")

    missing = sorted(REQUIRED_PROJECT_FIELDS - set(manifest))
    if missing:
        fail(f"{path} is missing project metadata fields: {', '.join(missing)}")

    if manifest.get("$schema") != PLUGIN_SCHEMA:
        fail(f"{path} must declare $schema as {PLUGIN_SCHEMA}")

    name = manifest.get("name")
    if not isinstance(name, str) or not 1 <= len(name) <= 64 or not PLUGIN_NAME.fullmatch(name):
        fail(f"{path} has an invalid Agent Plugins name: {name!r}")

    for field in ("version", "description", "homepage", "repository", "license"):
        if field in manifest and not isinstance(manifest[field], str):
            fail(f"{path} field {field!r} must be a string")

    author = manifest.get("author")
    if author is not None:
        if not isinstance(author, dict):
            fail(f"{path} field 'author' must be an object")
        else:
            unknown_author = sorted(set(author) - {"name", "email", "url"})
            if unknown_author:
                fail(f"{path} author has unsupported fields: {', '.join(unknown_author)}")
            for field, value in author.items():
                if not isinstance(value, str):
                    fail(f"{path} author field {field!r} must be a string")

    keywords = manifest.get("keywords")
    if keywords is not None and (
        not isinstance(keywords, list) or any(not isinstance(item, str) for item in keywords)
    ):
        fail(f"{path} field 'keywords' must be an array of strings")

    extensions = manifest.get("extensions")
    if extensions is not None and (
        not isinstance(extensions, dict)
        or any(not isinstance(value, dict) for value in extensions.values())
    ):
        fail(f"{path} field 'extensions' must map namespaces to objects")

    return manifest


def validate_skill(skill_file, allowed_fields=ALLOWED_SKILL_FIELDS):
    try:
        lines = skill_file.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        fail(f"cannot read {skill_file}: {error}")
        return

    if not lines or lines[0] != "---":
        fail(f"{skill_file} must start with YAML frontmatter")
        return

    try:
        closing = lines.index("---", 1)
    except ValueError:
        fail(f"{skill_file} has no closing YAML frontmatter delimiter")
        return

    try:
        fields = yaml.load("\n".join(lines[1:closing]), Loader=UniqueKeyLoader)
    except yaml.YAMLError as error:
        fail(f"{skill_file} has invalid YAML frontmatter: {error}")
        return

    if not isinstance(fields, dict):
        fail(f"{skill_file} frontmatter must be a YAML mapping")
        return

    unknown = sorted(str(field) for field in set(fields) - allowed_fields)
    if unknown:
        fail(f"{skill_file} has unsupported Agent Skills fields: {', '.join(unknown)}")

    name = fields.get("name")
    description = fields.get("description")

    if not isinstance(name, str) or not 1 <= len(name) <= 64 or not SKILL_NAME.fullmatch(name):
        fail(f"{skill_file} has an invalid Agent Skills name: {name!r}")
    elif name != skill_file.parent.name:
        fail(f"{skill_file} declares {name!r}, expected directory name {skill_file.parent.name!r}")

    if (
        not isinstance(description, str)
        or not description.strip()
        or not 1 <= len(description) <= 1024
    ):
        fail(f"{skill_file} must have a description between 1 and 1024 characters")

    license_value = fields.get("license")
    if license_value is not None and not isinstance(license_value, str):
        fail(f"{skill_file} license must be a string")

    compatibility = fields.get("compatibility")
    if compatibility is not None and (
        not isinstance(compatibility, str) or not 1 <= len(compatibility) <= 500
    ):
        fail(f"{skill_file} compatibility must be between 1 and 500 characters")

    metadata = fields.get("metadata")
    if metadata is not None and (
        not isinstance(metadata, dict)
        or any(not isinstance(key, str) or not isinstance(value, str) for key, value in metadata.items())
    ):
        fail(f"{skill_file} metadata must map string keys to string values")

    allowed_tools = fields.get("allowed-tools")
    if allowed_tools is not None and not isinstance(allowed_tools, str):
        fail(f"{skill_file} allowed-tools must be a string")

    return fields


def marketplace_entries(path, source_for):
    marketplace = load_object(path)
    if marketplace is None:
        return {}
    entries = marketplace.get("plugins")
    if not isinstance(entries, list):
        fail(f"{path} field 'plugins' must be an array")
        return {}

    result = {}
    for entry in entries:
        if not isinstance(entry, dict):
            fail(f"{path} contains a non-object plugin entry")
            continue
        name = entry.get("name")
        source = source_for(entry)
        if not isinstance(name, str) or not isinstance(source, str):
            fail(f"{path} entry {entry!r} needs valid name and source values")
            continue
        if source in result:
            fail(f"{path} lists source {source!r} more than once")
        result[source] = entry
    return result


root = Path.cwd().resolve()
plugins_root = root / "plugins"
claude_marketplace = marketplace_entries(
    root / ".claude-plugin" / "marketplace.json",
    lambda entry: entry.get("source"),
)
codex_marketplace = marketplace_entries(
    root / ".agents" / "plugins" / "marketplace.json",
    lambda entry: entry.get("source", {}).get("path")
    if isinstance(entry.get("source"), dict)
    else None,
)
cursor_marketplace = marketplace_entries(
    root / ".cursor-plugin" / "marketplace.json",
    lambda entry: entry.get("source"),
)

pi_package = load_object(root / "package.json")
if pi_package is not None:
    keywords = pi_package.get("keywords")
    if not isinstance(keywords, list) or "pi-package" not in keywords:
        fail("package.json must include the pi-package keyword")
    pi_manifest = pi_package.get("pi")
    expected_pi_skills = ["./plugins/*/skills"]
    if not isinstance(pi_manifest, dict) or pi_manifest.get("skills") != expected_pi_skills:
        fail(f"package.json pi.skills must equal {expected_pi_skills!r}")

plugin_dirs = sorted(path for path in plugins_root.iterdir() if path.is_dir())
if not plugin_dirs:
    fail("plugins/ must contain at least one plugin directory")

plugin_skill_files = []
plugin_cookbook_files = []

plugin_sources = {f"./plugins/{path.name}" for path in plugin_dirs}
for marketplace_path, entries in (
    (root / ".claude-plugin" / "marketplace.json", claude_marketplace),
    (root / ".agents" / "plugins" / "marketplace.json", codex_marketplace),
    (root / ".cursor-plugin" / "marketplace.json", cursor_marketplace),
):
    for source in sorted(set(entries) - plugin_sources):
        fail(f"{marketplace_path} lists missing plugin directory {source}")

for plugin_dir in plugin_dirs:
    source = f"./plugins/{plugin_dir.name}"
    manifest_path = plugin_dir / "plugin.json"
    manifest = validate_portable_manifest(manifest_path)

    try:
        if not manifest_path.resolve().is_relative_to(plugin_dir.resolve()):
            fail(f"{manifest_path} resolves outside its plugin root")
    except OSError as error:
        fail(f"cannot resolve {manifest_path}: {error}")

    native_manifests = []
    for client in (".claude-plugin", ".codex-plugin"):
        path = plugin_dir / client / "plugin.json"
        native = load_object(path)
        if native is not None:
            native_manifests.append((path, native))

    if manifest is not None:
        expected_name = f"majestic-{plugin_dir.name}"
        if manifest.get("name") != expected_name:
            fail(f"{manifest_path} declares {manifest.get('name')!r}, expected {expected_name!r}")

        for native_path, native in native_manifests:
            for field in PORTABLE_METADATA_FIELDS & set(manifest):
                if native.get(field) != manifest[field]:
                    fail(f"{native_path} field {field!r} does not match {manifest_path}")

        for marketplace_path, entries in (
            (root / ".claude-plugin" / "marketplace.json", claude_marketplace),
            (root / ".agents" / "plugins" / "marketplace.json", codex_marketplace),
            (root / ".cursor-plugin" / "marketplace.json", cursor_marketplace),
        ):
            entry = entries.get(source)
            if entry is None:
                fail(f"{marketplace_path} does not list {source}")
                continue
            if entry.get("name") != manifest.get("name"):
                fail(f"{marketplace_path} name for {source} does not match {manifest_path}")
            for field in PORTABLE_METADATA_FIELDS & set(manifest) & set(entry):
                if entry[field] != manifest[field]:
                    fail(f"{marketplace_path} field {field!r} for {source} does not match {manifest_path}")

    skills_dir = plugin_dir / "skills"
    if not skills_dir.is_dir():
        fail(f"{skills_dir} must be a directory")
        continue

    immediate_skills = []
    for child in sorted(skills_dir.iterdir()):
        if not child.is_dir():
            continue
        skill_file = child / "SKILL.md"
        if not skill_file.is_file():
            fail(f"{child} is an immediate skill directory without SKILL.md")
            continue
        immediate_skills.append(skill_file)
        plugin_skill_files.append(skill_file)
        fields = validate_skill(skill_file)
        metadata = fields.get("metadata") if isinstance(fields, dict) else None
        if isinstance(metadata, dict) and metadata.get("requires"):
            plugin_cookbook_files.append(skill_file)
        try:
            if not skill_file.resolve().is_relative_to(plugin_dir.resolve()):
                fail(f"{skill_file} resolves outside its plugin root")
        except OSError as error:
            fail(f"cannot resolve {skill_file}: {error}")

    discovered = set(immediate_skills)
    for nested in skills_dir.glob("**/SKILL.md"):
        if nested not in discovered:
            fail(f"{nested} is nested too deeply for Agent Plugins discovery")

    for directory, subdirs, filenames in os.walk(plugin_dir, followlinks=False):
        for name in [*subdirs, *filenames]:
            path = Path(directory) / name
            if not path.is_symlink():
                continue
            try:
                if not path.resolve().is_relative_to(plugin_dir.resolve()):
                    fail(f"{path} is a symlink that resolves outside its plugin root")
            except OSError as error:
                fail(f"cannot resolve symlink {path}: {error}")

standalone_count = len(plugin_skill_files) - len(plugin_cookbook_files)
if standalone_count != 167:
    fail(f"expected 167 standalone plugin skills, found {standalone_count}")
if len(plugin_cookbook_files) != 5:
    fail(f"expected 5 plugin-hosted cookbooks, found {len(plugin_cookbook_files)}")
for obsolete_directory in (root / "cookbooks", root / "skills"):
    if obsolete_directory.exists():
        fail(f"{obsolete_directory.relative_to(root)}/ is obsolete; every cookbook must live in its primary domain plugin")

repository_skill_files = sorted(root.glob(".agents/skills/*/SKILL.md"))
required_repository_skills = {"plugin-release", "sort-hat"}
found_repository_skills = {skill_file.parent.name for skill_file in repository_skill_files}
if not required_repository_skills <= found_repository_skills:
    missing = sorted(required_repository_skills - found_repository_skills)
    fail(f".agents/skills/ is missing repository skills: {', '.join(missing)}")
for skill_file in repository_skill_files:
    fields = validate_skill(skill_file, REPOSITORY_SKILL_FIELDS)
    if skill_file.parent.name == "plugin-release" and (
        not isinstance(fields, dict) or fields.get("disable-model-invocation") is not True
    ):
        fail(f"{skill_file} must be a manual command with disable-model-invocation: true")

if errors:
    for error in errors:
        print(f"FAIL: {error}")
    sys.exit(1)

print(
    f"OK: {len(plugin_dirs)} Agent Plugins manifests, harness marketplaces, "
    "the Pi package, skill trees, and package paths all validate"
)
PY
