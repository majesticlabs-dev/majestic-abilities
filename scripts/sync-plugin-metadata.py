#!/usr/bin/env python3
"""Synchronize shared plugin metadata from category root manifests."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_CANONICAL = (
    "name",
    "version",
    "description",
    "author",
    "license",
    "keywords",
)
OPTIONAL_CANONICAL = ("homepage", "repository")
CLAUDE_MARKETPLACE_SYNC = ("name", "version", "description")
CODEX_MARKETPLACE_SYNC = ("name",)


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def dump_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def ordered_update(
    target: dict[str, Any],
    updates: dict[str, Any],
    removals: set[str],
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in target.items():
        if key in removals:
            continue
        if key in updates:
            result[key] = updates[key]
        else:
            result[key] = value
    for key, value in updates.items():
        if key not in result and key not in removals:
            result[key] = value
    return result


def validate_canonical(path: Path, manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_CANONICAL:
        if field not in manifest:
            errors.append(f"{path}: missing required canonical field {field!r}")
    return errors


def sync_native(
    canonical: dict[str, Any],
    target: dict[str, Any],
) -> tuple[dict[str, Any], list[tuple[str, str]]]:
    updates: dict[str, Any] = {}
    removals: set[str] = set()
    drifts: list[tuple[str, str]] = []

    for field in REQUIRED_CANONICAL:
        expected = canonical[field]
        if target.get(field) != expected:
            drifts.append((field, "mismatch" if field in target else "missing"))
            updates[field] = expected

    for field in OPTIONAL_CANONICAL:
        if field in canonical:
            expected = canonical[field]
            if target.get(field) != expected:
                drifts.append((field, "mismatch" if field in target else "missing"))
                updates[field] = expected
        elif field in target:
            drifts.append((field, "unexpected"))
            removals.add(field)

    if not drifts:
        return target, []
    return ordered_update(target, updates, removals), drifts


def sync_marketplace_entry(
    canonical: dict[str, Any],
    entry: dict[str, Any],
    fields: tuple[str, ...],
) -> tuple[dict[str, Any], list[tuple[str, str]]]:
    updates: dict[str, Any] = {}
    drifts: list[tuple[str, str]] = []
    for field in fields:
        expected = canonical[field]
        if entry.get(field) != expected:
            drifts.append((field, "mismatch" if field in entry else "missing"))
            updates[field] = expected
    if not drifts:
        return entry, []
    return ordered_update(entry, updates, set()), drifts


def containment_error(path: Path, boundary: Path) -> str | None:
    try:
        resolved = path.resolve(strict=True)
        boundary_resolved = boundary.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        return f"{path}: cannot resolve path: {exc}"
    if not resolved.is_relative_to(boundary_resolved):
        return f"{path}: resolves outside {boundary_resolved}"
    return None


def iter_categories(root: Path) -> tuple[list[Path], list[str]]:
    plugins = root / "plugins"
    plugins_error = containment_error(plugins, root)
    if plugins_error:
        return [], [plugins_error]

    categories: list[Path] = []
    errors: list[str] = []
    for path in sorted(plugins.iterdir()):
        if not path.is_dir():
            continue
        error = containment_error(path, plugins)
        if error:
            errors.append(error)
            continue
        categories.append(path)
    return categories, errors


def find_marketplace_index(
    marketplace: dict[str, Any],
    source: str,
    *,
    codex: bool,
) -> int | None:
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list):
        return None
    for index, entry in enumerate(plugins):
        if not isinstance(entry, dict):
            continue
        if codex:
            source_obj = entry.get("source")
            path = source_obj.get("path") if isinstance(source_obj, dict) else None
            if path == source:
                return index
        elif entry.get("source") == source:
            return index
    return None


def analyze(root: Path) -> tuple[list[str], dict[Path, dict[str, Any]], int]:
    """Return drift diagnostics, pending file writes, and category count."""
    errors: list[str] = []
    writes: dict[Path, dict[str, Any]] = {}
    categories, category_errors = iter_categories(root)
    if category_errors:
        return category_errors, {}, len(categories)
    if not categories:
        return ["plugins/ must contain at least one category directory"], {}, 0

    claude_market_path = root / ".claude-plugin" / "marketplace.json"
    codex_market_path = root / ".agents" / "plugins" / "marketplace.json"
    for marketplace_path in (claude_market_path, codex_market_path):
        error = containment_error(marketplace_path, root)
        if error:
            return [error], {}, len(categories)
    try:
        claude_market = load_json(claude_market_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"{claude_market_path}: {exc}"], {}, len(categories)
    try:
        codex_market = load_json(codex_market_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"{codex_market_path}: {exc}"], {}, len(categories)

    claude_dirty = False
    codex_dirty = False

    for category_dir in categories:
        source = f"./plugins/{category_dir.name}"
        canonical_path = category_dir / "plugin.json"
        error = containment_error(canonical_path, category_dir)
        if error:
            errors.append(error)
            continue
        try:
            canonical = load_json(canonical_path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"{canonical_path}: {exc}")
            continue

        canonical_errors = validate_canonical(canonical_path, canonical)
        errors.extend(canonical_errors)
        if canonical_errors:
            continue

        for client in (".claude-plugin", ".codex-plugin"):
            target_path = category_dir / client / "plugin.json"
            error = containment_error(target_path, category_dir)
            if error:
                errors.append(error)
                continue
            try:
                target = load_json(target_path)
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                errors.append(f"{target_path}: {exc}")
                continue
            updated, drifts = sync_native(canonical, target)
            if drifts:
                for field, reason in drifts:
                    errors.append(
                        f"{category_dir.name}: {target_path} field {field!r} ({reason})"
                    )
                writes[target_path] = updated

        index = find_marketplace_index(claude_market, source, codex=False)
        if index is None:
            errors.append(f"{claude_market_path}: missing entry for {source}")
        else:
            updated, drifts = sync_marketplace_entry(
                canonical, claude_market["plugins"][index], CLAUDE_MARKETPLACE_SYNC
            )
            if drifts:
                claude_dirty = True
                claude_market["plugins"][index] = updated
                for field, reason in drifts:
                    errors.append(
                        f"{category_dir.name}: {claude_market_path} field {field!r} ({reason})"
                    )

        index = find_marketplace_index(codex_market, source, codex=True)
        if index is None:
            errors.append(f"{codex_market_path}: missing entry for {source}")
        else:
            updated, drifts = sync_marketplace_entry(
                canonical, codex_market["plugins"][index], CODEX_MARKETPLACE_SYNC
            )
            if drifts:
                codex_dirty = True
                codex_market["plugins"][index] = updated
                for field, reason in drifts:
                    errors.append(
                        f"{category_dir.name}: {codex_market_path} field {field!r} ({reason})"
                    )

    if claude_dirty:
        writes[claude_market_path] = claude_market
    if codex_dirty:
        writes[codex_market_path] = codex_market
    return errors, writes, len(categories)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check",
        action="store_true",
        help="report drift without writing (default)",
    )
    mode.add_argument(
        "--write",
        action="store_true",
        help="repair shared metadata fields in place",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="repository root (defaults to the checkout containing this script)",
    )
    args = parser.parse_args(argv)
    write_mode = bool(args.write)

    root = (args.root or repo_root()).resolve()
    errors, writes, category_count = analyze(root)

    # Structural errors (missing files/fields) always fail.
    structural = [
        error
        for error in errors
        if " field " not in error or "missing required canonical field" in error
    ]
    drift = [error for error in errors if error not in structural]

    if structural:
        for error in structural:
            print(f"FAIL: {error}")
        return 1

    if write_mode:
        for path, data in writes.items():
            dump_json(path, data)
        after_errors, after_writes, _ = analyze(root)
        after_structural = [
            error
            for error in after_errors
            if " field " not in error or "missing required canonical field" in error
        ]
        after_drift = [error for error in after_errors if error not in after_structural]
        if after_structural or after_drift or after_writes:
            for error in after_structural + after_drift:
                print(f"FAIL: remaining after --write: {error}")
            return 1
        print(
            f"OK: wrote shared metadata for {category_count} categories; no remaining drift"
        )
        return 0

    if drift:
        for error in drift:
            print(f"FAIL: {error}")
        return 1

    print(f"OK: no metadata drift across {category_count} categories")
    return 0


if __name__ == "__main__":
    sys.exit(main())
