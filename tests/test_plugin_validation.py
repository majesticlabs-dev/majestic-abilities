#!/usr/bin/env python3
"""Fixture tests for portable, Claude, and Codex validation contracts."""

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


class PluginValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="plugin-validation-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def _copy_minimal_repo(self) -> Path:
        root = self.tmp / "repo"
        root.mkdir()
        # Copy only core category plus marketplaces for focused fixtures.
        shutil.copytree(REPO / "plugins" / "core", root / "plugins" / "core")
        shutil.copytree(REPO / ".claude-plugin", root / ".claude-plugin")
        shutil.copytree(REPO / ".agents", root / ".agents")
        # Trim marketplaces to the core entry only.
        claude = read_json(root / ".claude-plugin" / "marketplace.json")
        claude["plugins"] = [
            entry
            for entry in claude["plugins"]
            if entry.get("source") == "./plugins/core"
        ]
        write_json(root / ".claude-plugin" / "marketplace.json", claude)
        codex = read_json(root / ".agents" / "plugins" / "marketplace.json")
        codex["plugins"] = [
            entry
            for entry in codex["plugins"]
            if entry.get("source", {}).get("path") == "./plugins/core"
        ]
        write_json(root / ".agents" / "plugins" / "marketplace.json", codex)
        # Seed validators into the fixture.
        scripts = root / "scripts"
        scripts.mkdir()
        for name in (
            "check-agent-plugins.sh",
            "check-codex-plugins.sh",
            "check-claude-plugins.sh",
        ):
            shutil.copy2(REPO / "scripts" / name, scripts / name)
            os.chmod(scripts / name, 0o755)
        return root

    def _run(self, root: Path, script: str, env: dict | None = None) -> subprocess.CompletedProcess:
        merged = os.environ.copy()
        if env:
            merged.update(env)
        return subprocess.run(
            ["bash", str(root / "scripts" / script)],
            cwd=root,
            env=merged,
            capture_output=True,
            text=True,
        )

    def test_agent_plugins_rejects_omitted_native_version(self) -> None:
        root = self._copy_minimal_repo()
        path = root / "plugins" / "core" / ".claude-plugin" / "plugin.json"
        data = read_json(path)
        del data["version"]
        write_json(path, data)
        result = self._run(root, "check-agent-plugins.sh")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(str(path), result.stdout)
        self.assertIn("version", result.stdout)

    def test_agent_plugins_rejects_duplicate_skill_name(self) -> None:
        root = self._copy_minimal_repo()
        # Add a second category with a colliding skill directory name.
        other = root / "plugins" / "misc"
        shutil.copytree(root / "plugins" / "core", other)
        portable = read_json(other / "plugin.json")
        portable["name"] = "majestic-misc"
        write_json(other / "plugin.json", portable)
        for client in (".claude-plugin", ".codex-plugin"):
            native = read_json(other / client / "plugin.json")
            native["name"] = "majestic-misc"
            write_json(other / client / "plugin.json", native)
        # Marketplace entries for misc.
        claude = read_json(root / ".claude-plugin" / "marketplace.json")
        claude["plugins"].append(
            {
                "name": "majestic-misc",
                "source": "./plugins/misc",
                "description": portable["description"],
                "version": portable["version"],
                "category": "misc",
            }
        )
        write_json(root / ".claude-plugin" / "marketplace.json", claude)
        codex = read_json(root / ".agents" / "plugins" / "marketplace.json")
        codex["plugins"].append(
            {
                "name": "majestic-misc",
                "source": {"source": "local", "path": "./plugins/misc"},
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": "Developer Tools",
            }
        )
        write_json(root / ".agents" / "plugins" / "marketplace.json", codex)

        result = self._run(root, "check-agent-plugins.sh")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate skill name", result.stdout)

    def test_agent_plugins_rejects_nested_skill_and_empty_category(self) -> None:
        root = self._copy_minimal_repo()
        nested = (
            root
            / "plugins"
            / "core"
            / "skills"
            / "agent-ready-repository"
            / "nested"
            / "SKILL.md"
        )
        nested.parent.mkdir(parents=True, exist_ok=True)
        nested.write_text(
            "---\nname: nested-skill\ndescription: nested\n---\n\n# nested\n",
            encoding="utf-8",
        )
        # Empty category
        hollow = root / "plugins" / "hollow"
        hollow.mkdir()
        write_json(
            hollow / "plugin.json",
            {
                "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
                "name": "majestic-hollow",
                "version": "0.1.0",
                "description": "empty",
                "author": {"name": "Majestic Labs"},
                "license": "MIT",
                "keywords": ["x"],
            },
        )
        (hollow / "skills").mkdir()
        write_json(
            hollow / ".claude-plugin" / "plugin.json",
            {
                "name": "majestic-hollow",
                "version": "0.1.0",
                "description": "empty",
                "author": {"name": "Majestic Labs"},
                "license": "MIT",
                "keywords": ["x"],
            },
        )
        write_json(
            hollow / ".codex-plugin" / "plugin.json",
            {
                "name": "majestic-hollow",
                "version": "0.1.0",
                "description": "empty",
                "author": {"name": "Majestic Labs"},
                "license": "MIT",
                "keywords": ["x"],
                "skills": "./skills/",
                "interface": {
                    "displayName": "Hollow",
                    "shortDescription": "empty",
                    "longDescription": "empty",
                    "developerName": "Majestic Labs",
                    "category": "Developer Tools",
                    "capabilities": ["Skills"],
                    "defaultPrompt": ["help"],
                },
            },
        )
        claude = read_json(root / ".claude-plugin" / "marketplace.json")
        claude["plugins"].append(
            {
                "name": "majestic-hollow",
                "source": "./plugins/hollow",
                "description": "empty",
                "version": "0.1.0",
                "category": "hollow",
            }
        )
        write_json(root / ".claude-plugin" / "marketplace.json", claude)
        codex = read_json(root / ".agents" / "plugins" / "marketplace.json")
        codex["plugins"].append(
            {
                "name": "majestic-hollow",
                "source": {"source": "local", "path": "./plugins/hollow"},
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": "Developer Tools",
            }
        )
        write_json(root / ".agents" / "plugins" / "marketplace.json", codex)

        result = self._run(root, "check-agent-plugins.sh")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("nested too deeply", result.stdout)
        self.assertIn("must contain at least one immediate skill", result.stdout)

    def test_agent_plugins_rejects_escaping_symlink(self) -> None:
        root = self._copy_minimal_repo()
        outside = self.tmp / "outside"
        write_skill(outside / "escaped-skill", "escaped-skill", "MARKER_SKILL_ESCAPE")
        target = root / "plugins" / "core" / "skills" / "escape"
        target.symlink_to(outside / "escaped-skill")
        result = self._run(root, "check-agent-plugins.sh")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("resolves outside its plugin root", result.stdout)
        self.assertNotIn("MARKER_SKILL_ESCAPE", result.stdout)

    def test_agent_plugins_rejects_category_root_escape(self) -> None:
        root = self._copy_minimal_repo()
        outside = self.tmp / "outside-category"
        write_skill(outside / "skills" / "escaped-skill", "escaped-skill", "MARKER_CATEGORY_ESCAPE")
        # Keep marketplace entries, replace the category directory with an escape.
        core = root / "plugins" / "core"
        shutil.rmtree(core)
        core.symlink_to(outside, target_is_directory=True)
        result = self._run(root, "check-agent-plugins.sh")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(str(core), result.stdout)
        self.assertIn("resolves outside the plugins root", result.stdout)
        self.assertNotIn("MARKER_CATEGORY_ESCAPE", result.stdout)

    def test_claude_validates_marketplace_and_every_category(self) -> None:
        root = self._copy_minimal_repo()
        result = self._run(root, "check-claude-plugins.sh")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Validating Claude marketplace:", result.stdout)
        self.assertIn("plugins/core/.claude-plugin/plugin.json", result.stdout)
        self.assertIn(
            "OK: Claude marketplace and 1 category manifests validated",
            result.stdout,
        )

    def test_claude_fails_when_category_manifest_missing(self) -> None:
        root = self._copy_minimal_repo()
        missing = root / "plugins" / "core" / ".claude-plugin" / "plugin.json"
        missing.unlink()
        result = self._run(root, "check-claude-plugins.sh")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("plugins/core/.claude-plugin/plugin.json", result.stdout)
        self.assertIn("missing Claude manifest", result.stdout)
        self.assertIn("validated 0 Claude category manifests, expected exactly 1", result.stdout)

    def test_codex_rejects_wrong_skills_path_and_missing_interface(self) -> None:
        root = self._copy_minimal_repo()
        path = root / "plugins" / "core" / ".codex-plugin" / "plugin.json"
        data = read_json(path)
        data["skills"] = "./other/"
        del data["interface"]["shortDescription"]
        write_json(path, data)
        env = {"HOME": str(self.tmp / "empty-home")}
        env["CODEX_PLUGIN_VALIDATOR"] = ""
        # Ensure unset semantics for optional validator.
        result = subprocess.run(
            ["env", "-u", "CODEX_PLUGIN_VALIDATOR", "bash", str(root / "scripts" / "check-codex-plugins.sh")],
            cwd=root,
            env={**os.environ, "HOME": str(self.tmp / "empty-home")},
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("plugins/core/.codex-plugin/plugin.json", result.stdout)
        self.assertIn("skills", result.stdout)
        self.assertIn("shortDescription", result.stdout)

    def test_codex_rejects_null_required_interface_arrays(self) -> None:
        root = self._copy_minimal_repo()
        path = root / "plugins" / "core" / ".codex-plugin" / "plugin.json"
        data = read_json(path)
        data["interface"]["capabilities"] = None
        data["interface"]["defaultPrompt"] = None
        write_json(path, data)
        result = subprocess.run(
            ["env", "-u", "CODEX_PLUGIN_VALIDATOR", "bash", str(root / "scripts" / "check-codex-plugins.sh")],
            cwd=root,
            env={**os.environ, "HOME": str(self.tmp / "empty-home")},
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("interface.capabilities must be an array of strings", result.stdout)
        self.assertIn("interface.defaultPrompt must be an array of strings", result.stdout)

    def test_codex_rejects_duplicate_marketplace_entry(self) -> None:
        root = self._copy_minimal_repo()
        market = read_json(root / ".agents" / "plugins" / "marketplace.json")
        market["plugins"].append(dict(market["plugins"][0]))
        write_json(root / ".agents" / "plugins" / "marketplace.json", market)
        result = subprocess.run(
            ["env", "-u", "CODEX_PLUGIN_VALIDATOR", "bash", str(root / "scripts" / "check-codex-plugins.sh")],
            cwd=root,
            env={**os.environ, "HOME": str(self.tmp / "empty-home")},
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("more than once", result.stdout)

    def test_codex_self_contained_without_home_validator(self) -> None:
        # Use the real repository for the happy path.
        result = subprocess.run(
            [
                "env",
                "-u",
                "CODEX_PLUGIN_VALIDATOR",
                f"HOME={self.tmp / 'empty-home'}",
                "bash",
                str(REPO / "scripts" / "check-codex-plugins.sh"),
            ],
            cwd=REPO,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("OK:", result.stdout)


if __name__ == "__main__":
    unittest.main()
