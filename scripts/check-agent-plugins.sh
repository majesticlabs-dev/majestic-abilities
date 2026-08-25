#!/usr/bin/env bash
# Verify portable Agent Plugins manifests, shared metadata, skill discovery, and package containment.
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
REQUIRED_CANONICAL = {
    "name",
    "version",
    "description",
    "author",
    "license",
    "keywords",
}
OPTIONAL_CANONICAL = {"homepage", "repository"}
CLAUDE_MARKETPLACE_FIELDS = {"name", "version", "description"}
CODEX_MARKETPLACE_FIELDS = {"name"}
ADAPTER_DIR_NAMES = {".claude-plugin", ".codex-plugin", ".opencode", ".cursor-plugin"}
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

    missing = sorted(REQUIRED_CANONICAL - set(manifest))
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


def validate_skill(skill_file):
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

    unknown = sorted(str(field) for field in set(fields) - ALLOWED_SKILL_FIELDS)
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


def compare_native_metadata(manifest_path, manifest, native_path, native):
    for field in REQUIRED_CANONICAL:
        if field not in native:
            fail(f"{native_path} is missing required shared field {field!r}")
        elif native.get(field) != manifest.get(field):
            fail(f"{native_path} field {field!r} does not match {manifest_path}")

    for field in OPTIONAL_CANONICAL:
        if field in manifest:
            if native.get(field) != manifest[field]:
                fail(f"{native_path} field {field!r} does not match {manifest_path}")
        elif field in native:
            fail(f"{native_path} field {field!r} must be absent when omitted by {manifest_path}")


def compare_marketplace_entry(manifest_path, manifest, marketplace_path, entry, fields):
    for field in fields:
        if field not in entry:
            fail(f"{marketplace_path} entry for {manifest_path} is missing required field {field!r}")
        elif entry.get(field) != manifest.get(field):
            fail(f"{marketplace_path} field {field!r} for {manifest_path} does not match")


root = Path.cwd().resolve()
plugins_root = root / "plugins"
claude_marketplace_path = root / ".claude-plugin" / "marketplace.json"
codex_marketplace_path = root / ".agents" / "plugins" / "marketplace.json"
claude_marketplace = marketplace_entries(
    claude_marketplace_path,
    lambda entry: entry.get("source"),
)
codex_marketplace = marketplace_entries(
    codex_marketplace_path,
    lambda entry: entry.get("source", {}).get("path")
    if isinstance(entry.get("source"), dict)
    else None,
)

if not plugins_root.is_dir():
    fail("plugins/ must contain at least one plugin directory")
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
    fail("plugins/ must contain at least one plugin directory")

plugin_sources = {f"./plugins/{path.name}" for path, _ in plugin_dirs}
for marketplace_path, entries in (
    (claude_marketplace_path, claude_marketplace),
    (codex_marketplace_path, codex_marketplace),
):
    for source in sorted(set(entries) - plugin_sources):
        fail(f"{marketplace_path} lists missing plugin directory {source}")

skill_owners = {}

for plugin_dir, category_real in plugin_dirs:
    source = f"./plugins/{plugin_dir.name}"
    manifest_path = plugin_dir / "plugin.json"

    try:
        manifest_real = manifest_path.resolve()
    except OSError as error:
        fail(f"cannot resolve {manifest_path}: {error}")
        continue
    if not manifest_real.is_relative_to(category_real):
        fail(f"{manifest_path} resolves outside its plugin root")
        continue

    manifest = validate_portable_manifest(manifest_path)

    native_manifests = []
    for client in (".claude-plugin", ".codex-plugin"):
        path = plugin_dir / client / "plugin.json"
        try:
            if path.exists() and not path.resolve().is_relative_to(category_real):
                fail(f"{path} resolves outside its plugin root")
                continue
        except OSError as error:
            fail(f"cannot resolve {path}: {error}")
            continue
        native = load_object(path)
        if native is not None:
            native_manifests.append((path, native))

    if manifest is not None:
        expected_name = f"majestic-{plugin_dir.name}"
        if manifest.get("name") != expected_name:
            fail(f"{manifest_path} declares {manifest.get('name')!r}, expected {expected_name!r}")

        for native_path, native in native_manifests:
            compare_native_metadata(manifest_path, manifest, native_path, native)

        claude_entry = claude_marketplace.get(source)
        if claude_entry is None:
            fail(f"{claude_marketplace_path} does not list {source}")
        else:
            compare_marketplace_entry(
                manifest_path,
                manifest,
                claude_marketplace_path,
                claude_entry,
                CLAUDE_MARKETPLACE_FIELDS,
            )

        codex_entry = codex_marketplace.get(source)
        if codex_entry is None:
            fail(f"{codex_marketplace_path} does not list {source}")
        else:
            compare_marketplace_entry(
                manifest_path,
                manifest,
                codex_marketplace_path,
                codex_entry,
                CODEX_MARKETPLACE_FIELDS,
            )

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

    immediate_skills = []
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
        immediate_skills.append(skill_file)
        validate_skill(skill_file)
        owners = skill_owners.setdefault(child.name, [])
        owners.append(str(skill_file))

    if not immediate_skills:
        fail(f"{skills_dir} must contain at least one immediate skill")

    discovered = set(immediate_skills)
    for nested in skills_dir.glob("**/SKILL.md"):
        if nested not in discovered:
            fail(f"{nested} is nested too deeply for Agent Plugins discovery")

    for directory, subdirs, filenames in os.walk(plugin_dir, followlinks=False):
        rel_parts = Path(directory).relative_to(plugin_dir).parts
        if rel_parts and rel_parts[0] in ADAPTER_DIR_NAMES and "SKILL.md" in filenames:
            fail(f"{Path(directory) / 'SKILL.md'} must not exist under an adapter directory")
        for name in [*subdirs, *filenames]:
            path = Path(directory) / name
            if not path.is_symlink():
                continue
            try:
                if not path.resolve().is_relative_to(category_real):
                    fail(f"{path} is a symlink that resolves outside its plugin root")
            except OSError as error:
                fail(f"cannot resolve symlink {path}: {error}")

for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
    rel = Path(dirpath).relative_to(root)
    if rel.parts and rel.parts[0] == ".git":
        dirnames[:] = []
        continue
    if "SKILL.md" in filenames and any(part in ADAPTER_DIR_NAMES for part in rel.parts):
        fail(f"{rel / 'SKILL.md'} must not exist under an adapter directory")

for name, owners in sorted(skill_owners.items()):
    if len(owners) > 1:
        fail(f"duplicate skill name {name!r}: {', '.join(owners)}")

if errors:
    for error in errors:
        print(f"FAIL: {error}")
    sys.exit(1)

print(
    f"OK: {len(plugin_dirs)} Agent Plugins manifests, portable metadata, "
    "skill trees, and package paths all validate"
)
PY
