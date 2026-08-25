#!/usr/bin/env python3
"""Fixture tests for Cursor portable Agent Plugins validation."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_skill(path: Path, name: str, description: str = "desc") -> None:
    path.mkdir(parents=True, exist_ok=True)
    path.joinpath("SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n",
        encoding="utf-8",
    )


class CursorPluginTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="cursor-plugins-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def _copy_minimal_repo(self) -> Path:
        root = self.tmp / "repo"
        root.mkdir()
        shutil.copytree(REPO / "plugins" / "core", root / "plugins" / "core")
        scripts = root / "scripts"
        scripts.mkdir()
        for name in ("check-cursor-plugins.sh", "check-adapter-contracts.sh"):
            shutil.copy2(REPO / "scripts" / name, scripts / name)
            os.chmod(scripts / name, 0o755)
        # Structural-only mode for fixture isolation: stub adapter contracts.
        (scripts / "check-adapter-contracts.sh").write_text(
            "#!/usr/bin/env bash\nset -euo pipefail\necho OK: stubbed adapter contracts\n",
            encoding="utf-8",
        )
        os.chmod(scripts / "check-adapter-contracts.sh", 0o755)
        return root

    def _run_checker(self, root: Path) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["bash", str(root / "scripts" / "check-cursor-plugins.sh")],
            cwd=root,
            capture_output=True,
            text=True,
            env={**os.environ, "PATH": os.environ.get("PATH", "")},
        )

    def test_valid_portable_category_passes(self) -> None:
        root = self._copy_minimal_repo()
        result = self._run_checker(root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("1 portable category packages are Cursor-compatible", result.stdout)
        self.assertIn("Cursor portable package validation complete", result.stdout)
        self.assertFalse((root / ".cursor-plugin").exists())
        self.assertFalse((root / "plugins" / "core" / ".cursor-plugin").exists())

    def test_missing_manifest_fails(self) -> None:
        root = self._copy_minimal_repo()
        missing = root / "plugins" / "core" / "plugin.json"
        missing.unlink()
        result = self._run_checker(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(str(missing), result.stdout)
        self.assertIn("missing portable Agent Plugins manifest", result.stdout)

    def test_empty_skills_fails(self) -> None:
        root = self._copy_minimal_repo()
        skills = root / "plugins" / "core" / "skills"
        shutil.rmtree(skills)
        skills.mkdir()
        result = self._run_checker(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(str(skills), result.stdout)
        self.assertIn("must contain at least one immediate skill", result.stdout)

    def test_escaping_path_fails(self) -> None:
        root = self._copy_minimal_repo()
        outside = self.tmp / "outside-skill"
        write_skill(outside / "escaped-skill", "escaped-skill")
        target = root / "plugins" / "core" / "skills" / "escaped-link"
        target.symlink_to(outside / "escaped-skill", target_is_directory=True)
        result = self._run_checker(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(str(target), result.stdout)
        self.assertIn("resolves outside its plugin root", result.stdout)

    def test_cursor_native_manifest_rejected(self) -> None:
        root = self._copy_minimal_repo()
        native = root / "plugins" / "core" / ".cursor-plugin" / "plugin.json"
        write_json(native, {"name": "cursor-native"})
        result = self._run_checker(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(".cursor-plugin", result.stdout)

    def test_occupied_destination_rejected_by_adapter_contract(self) -> None:
        result = subprocess.run(
            ["bash", str(REPO / "scripts" / "check-adapter-contracts.sh"), "--invalid-fixtures"],
            cwd=REPO,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        combined = result.stdout + result.stderr
        self.assertIn("occupied destination", combined)
        self.assertIn("escaping path", combined)

    def test_metadata_sync_does_not_create_cursor_records(self) -> None:
        root = self._copy_minimal_repo()
        shutil.copytree(REPO / ".claude-plugin", root / ".claude-plugin")
        agents = root / ".agents" / "plugins"
        agents.mkdir(parents=True)
        # Keep only the core marketplace entries that match the fixture.
        claude = read_json(root / ".claude-plugin" / "marketplace.json")
        claude["plugins"] = [
            entry
            for entry in claude["plugins"]
            if entry.get("source") == "./plugins/core"
        ]
        write_json(root / ".claude-plugin" / "marketplace.json", claude)
        codex = read_json(REPO / ".agents" / "plugins" / "marketplace.json")
        codex["plugins"] = [
            entry
            for entry in codex["plugins"]
            if entry.get("source", {}).get("path") == "./plugins/core"
        ]
        write_json(agents / "marketplace.json", codex)

        before = list(root.rglob(".cursor-plugin"))
        sync = subprocess.run(
            [
                "python3",
                str(REPO / "scripts" / "sync-plugin-metadata.py"),
                "--write",
                "--root",
                str(root),
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(sync.returncode, 0, sync.stdout + sync.stderr)
        self.assertIn("OK:", sync.stdout)
        after = list(root.rglob(".cursor-plugin"))
        self.assertEqual(before, [])
        self.assertEqual(after, [])
        self.assertFalse((REPO / ".cursor-plugin").exists())

        result = self._run_checker(root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_category_root_escape_fails_without_parsing_outside(self) -> None:
        root = self._copy_minimal_repo()
        outside = self.tmp / "outside-category"
        write_skill(outside / "skills" / "escaped-skill", "escaped-skill", "MARKER_CURSOR_ESCAPE")
        # Replace category with an escaping symlink after seeding a valid tree.
        core = root / "plugins" / "core"
        shutil.rmtree(core)
        core.symlink_to(outside, target_is_directory=True)
        result = self._run_checker(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(str(core), result.stdout)
        self.assertIn("resolves outside the plugins root", result.stdout)
        self.assertNotIn("MARKER_CURSOR_ESCAPE", result.stdout)
        self.assertNotIn("escaped-skill", result.stdout)


if __name__ == "__main__":
    unittest.main()
