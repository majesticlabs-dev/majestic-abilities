#!/usr/bin/env python3
"""Remove an approved project-local creator installation and its lock entry."""

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import stat
import sys
import tempfile


CREATOR = "create-verification-skill"


def project_path(value, root):
    path = Path(value).expanduser()
    if not path.is_absolute():
        raise ValueError("installation and lock paths must be absolute")
    # Resolve parents, but leave the final symlink intact for unlinking.
    path = path.parent.resolve() / path.name
    try:
        relative = path.relative_to(root)
    except ValueError:
        raise ValueError(f"path is outside the project: {path}") from None
    if not relative.parts or "plugins" in relative.parts:
        raise ValueError(f"project roots and plugin/catalog sources cannot be removed: {path}")
    return path


def validate_creator(path):
    if path.name != CREATOR:
        raise ValueError(f"not a creator installation: {path}")
    if not path.exists() and not path.is_symlink():
        return
    if not path.is_dir():
        raise ValueError(f"creator installation is not a readable directory: {path}")
    lines = (path / "SKILL.md").read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"creator has no skill frontmatter: {path}")
    closing = lines.index("---", 1)
    names = [line for line in lines[1:closing] if line.startswith("name:")]
    pattern = rf"""name:\s*(?:{CREATOR}|"{CREATOR}"|'{CREATOR}')\s*(?:#.*)?"""
    if len(names) != 1 or not re.fullmatch(pattern, names[0]):
        raise ValueError(f"skill identity does not match the creator: {path}")


def read_lock(path):
    if path.name != "skills-lock.json" or path.is_symlink():
        raise ValueError("use the project's regular skills-lock.json, not a symlink")
    if not path.exists():
        return None, None
    original = path.read_bytes()
    data = json.loads(original)
    if not isinstance(data, dict) or not isinstance(data.get("skills"), dict):
        raise ValueError("skills-lock.json must contain an object named skills")
    return data, original


def update_lock(path, data, original):
    if data is None or CREATOR not in data["skills"]:
        return "unchanged"
    if path.is_symlink() or path.read_bytes() != original:
        raise ValueError("skills-lock.json changed during cleanup; its contents were preserved")
    del data["skills"][CREATOR]
    if not data["skills"] and set(data) <= {"version", "skills"}:
        path.unlink()
        return "removed-empty-lock"
    mode = stat.S_IMODE(path.stat().st_mode)
    fd, temporary_name = tempfile.mkstemp(prefix=".skills-lock-", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as output:
            json.dump(data, output, indent=2)
            output.write("\n")
        temporary.chmod(mode)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()
    return "removed-creator-entry"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--skill-dir", required=True, action="append")
    parser.add_argument("--lock-file")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        supplied_root = Path(args.project_root).expanduser()
        if not supplied_root.is_absolute():
            raise ValueError("project root must be absolute")
        root = supplied_root.resolve(strict=True)
        if not root.is_dir() or root == Path(root.anchor) or root == Path.home().resolve():
            raise ValueError("use a project directory, not a filesystem root or home directory")
        targets = list(dict.fromkeys(project_path(value, root) for value in args.skill_dir))
        for target in targets:
            validate_creator(target)
        lock = project_path(args.lock_file or str(root / "skills-lock.json"), root)
        data, original = read_lock(lock)
        present = [target for target in targets if target.exists() or target.is_symlink()]
        if args.dry_run:
            print(json.dumps({
                "would_remove": [str(target) for target in present],
                "would_remove_lock_entry": data is not None and CREATOR in data["skills"],
            }))
            return 0
        # Check every target and the lock before changing any project files.
        removed = []
        for target in present:
            if target.is_symlink():
                target.unlink()
            else:
                shutil.rmtree(target)
            removed.append(str(target))
        lock_result = update_lock(lock, data, original)
        print(json.dumps({"removed": removed, "lock": lock_result}))
        return 0
    except (OSError, ValueError) as error:
        print(f"creator cleanup blocked: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
