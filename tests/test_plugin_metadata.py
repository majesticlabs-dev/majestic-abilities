#!/usr/bin/env python3
"""Tests for scripts/sync-plugin-metadata.py."""

from __future__ import annotations

import importlib.util
import io
import json
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location(
    "sync_plugin_metadata",
    REPO / "scripts" / "sync-plugin-metadata.py",
)
sync = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(sync)


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class SyncPluginMetadataTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="metadata-sync-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self._build_fixture()

    def _run(self, argv: list[str]) -> tuple[int, str]:
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = sync.main(argv)
        return code, buf.getvalue()

    def _canonical(self, **overrides) -> dict:
        data = {
            "name": "majestic-core",
            "version": "0.1.0",
            "description": "Core description",
            "author": {"name": "Majestic Labs"},
            "license": "MIT",
            "keywords": ["repository", "agents"],
        }
        data.update(overrides)
        return data

    def _build_fixture(self) -> None:
        canonical = self._canonical()
        write_json(self.tmp / "plugins" / "core" / "plugin.json", canonical)
        write_json(
            self.tmp / "plugins" / "core" / ".claude-plugin" / "plugin.json",
            {
                **{k: canonical[k] for k in sync.REQUIRED_CANONICAL},
                "displayName": "Majestic Core",
            },
        )
        write_json(
            self.tmp / "plugins" / "core" / ".codex-plugin" / "plugin.json",
            {
                **{k: canonical[k] for k in sync.REQUIRED_CANONICAL},
                "skills": "./skills/",
                "interface": {
                    "displayName": "Majestic Core",
                    "category": "Developer Tools",
                },
            },
        )
        write_json(
            self.tmp / ".claude-plugin" / "marketplace.json",
            {
                "name": "majestic-abilities",
                "owner": {"name": "Majestic Labs"},
                "metadata": {"version": "9.9.9"},
                "plugins": [
                    {
                        "name": "majestic-core",
                        "source": "./plugins/core",
                        "description": canonical["description"],
                        "version": canonical["version"],
                        "category": "core",
                        "keywords": ["preserve-me"],
                    }
                ],
            },
        )
        write_json(
            self.tmp / ".agents" / "plugins" / "marketplace.json",
            {
                "name": "majestic-abilities-codex",
                "interface": {"displayName": "Majestic Abilities for Codex"},
                "plugins": [
                    {
                        "name": "majestic-core",
                        "source": {"source": "local", "path": "./plugins/core"},
                        "policy": {
                            "installation": "AVAILABLE",
                            "authentication": "ON_INSTALL",
                        },
                        "category": "Developer Tools",
                    }
                ],
            },
        )

    def test_check_no_drift(self) -> None:
        code, out = self._run(["--check", "--root", str(self.tmp)])
        self.assertEqual(code, 0)
        self.assertIn("OK: no metadata drift across 1 categories", out)

    def test_changed_version_fails_check(self) -> None:
        path = self.tmp / "plugins" / "core" / ".claude-plugin" / "plugin.json"
        data = read_json(path)
        data["version"] = "9.0.0"
        write_json(path, data)
        code, out = self._run(["--check", "--root", str(self.tmp)])
        self.assertNotEqual(code, 0)
        self.assertIn("core:", out)
        self.assertIn(str(path), out)
        self.assertIn("field 'version'", out)

    def test_missing_required_target_field_fails(self) -> None:
        path = self.tmp / "plugins" / "core" / ".codex-plugin" / "plugin.json"
        data = read_json(path)
        del data["version"]
        write_json(path, data)
        code, out = self._run(["--check", "--root", str(self.tmp)])
        self.assertNotEqual(code, 0)
        self.assertIn("core:", out)
        self.assertIn(str(path), out)
        self.assertIn("field 'version'", out)

    def test_conditional_addition_and_write(self) -> None:
        canonical_path = self.tmp / "plugins" / "core" / "plugin.json"
        canonical = read_json(canonical_path)
        canonical["homepage"] = "https://example.com/core"
        write_json(canonical_path, canonical)

        code, out = self._run(["--check", "--root", str(self.tmp)])
        self.assertNotEqual(code, 0)
        self.assertIn("core:", out)
        self.assertIn("field 'homepage'", out)
        self.assertEqual(self._run(["--write", "--root", str(self.tmp)])[0], 0)

        claude = read_json(
            self.tmp / "plugins" / "core" / ".claude-plugin" / "plugin.json"
        )
        codex = read_json(
            self.tmp / "plugins" / "core" / ".codex-plugin" / "plugin.json"
        )
        self.assertEqual(claude["homepage"], "https://example.com/core")
        self.assertEqual(codex["homepage"], "https://example.com/core")
        self.assertEqual(claude["displayName"], "Majestic Core")
        self.assertEqual(codex["skills"], "./skills/")

        before = {
            path: path.read_bytes()
            for path in self.tmp.rglob("*.json")
            if path.is_file()
        }
        self.assertEqual(self._run(["--write", "--root", str(self.tmp)])[0], 0)
        after = {
            path: path.read_bytes()
            for path in self.tmp.rglob("*.json")
            if path.is_file()
        }
        self.assertEqual(before, after)

    def test_conditional_drift_repair(self) -> None:
        canonical_path = self.tmp / "plugins" / "core" / "plugin.json"
        canonical = read_json(canonical_path)
        canonical["repository"] = "https://example.com/repo"
        write_json(canonical_path, canonical)
        claude_path = self.tmp / "plugins" / "core" / ".claude-plugin" / "plugin.json"
        claude = read_json(claude_path)
        claude["repository"] = "https://wrong.example"
        write_json(claude_path, claude)

        self.assertEqual(self._run(["--write", "--root", str(self.tmp)])[0], 0)
        repaired = read_json(claude_path)
        self.assertEqual(repaired["repository"], "https://example.com/repo")

    def test_conditional_removal_when_canonical_omits(self) -> None:
        claude_path = self.tmp / "plugins" / "core" / ".claude-plugin" / "plugin.json"
        claude = read_json(claude_path)
        claude["homepage"] = "https://stale.example"
        write_json(claude_path, claude)

        self.assertEqual(self._run(["--write", "--root", str(self.tmp)])[0], 0)
        repaired = read_json(claude_path)
        self.assertNotIn("homepage", repaired)
        self.assertEqual(repaired["displayName"], "Majestic Core")

    def test_preserves_target_only_and_unsupported_marketplace_fields(self) -> None:
        market_path = self.tmp / ".claude-plugin" / "marketplace.json"
        codex_path = self.tmp / "plugins" / "core" / ".codex-plugin" / "plugin.json"
        before_codex = read_json(codex_path)

        claude_path = self.tmp / "plugins" / "core" / ".claude-plugin" / "plugin.json"
        claude = read_json(claude_path)
        claude["description"] = "stale"
        write_json(claude_path, claude)

        self.assertEqual(self._run(["--write", "--root", str(self.tmp)])[0], 0)

        after_market = read_json(market_path)
        self.assertEqual(after_market["metadata"]["version"], "9.9.9")
        self.assertEqual(after_market["plugins"][0]["keywords"], ["preserve-me"])
        self.assertEqual(after_market["plugins"][0]["category"], "core")
        after_codex = read_json(codex_path)
        self.assertEqual(after_codex["skills"], before_codex["skills"])
        self.assertEqual(after_codex["interface"], before_codex["interface"])

    def test_marketplace_description_repair(self) -> None:
        market_path = self.tmp / ".claude-plugin" / "marketplace.json"
        market = read_json(market_path)
        market["plugins"][0]["description"] = "wrong"
        write_json(market_path, market)
        code, out = self._run(["--check", "--root", str(self.tmp)])
        self.assertNotEqual(code, 0)
        self.assertIn("core:", out)
        self.assertIn(str(market_path), out)
        self.assertIn("field 'description'", out)
        self.assertEqual(self._run(["--write", "--root", str(self.tmp)])[0], 0)
        repaired = read_json(market_path)
        self.assertEqual(repaired["plugins"][0]["description"], "Core description")
        self.assertEqual(repaired["plugins"][0]["keywords"], ["preserve-me"])
        self.assertEqual(repaired["metadata"]["version"], "9.9.9")

    def test_write_rejects_category_symlink_escape(self) -> None:
        outside = Path(tempfile.mkdtemp(prefix="metadata-sync-outside-"))
        self.addCleanup(shutil.rmtree, outside, ignore_errors=True)
        outside_category = outside / "core"
        shutil.copytree(self.tmp / "plugins" / "core", outside_category)

        external_manifest = outside_category / ".claude-plugin" / "plugin.json"
        stale = read_json(external_manifest)
        stale["version"] = "9.0.0"
        write_json(external_manifest, stale)
        before = external_manifest.read_bytes()

        shutil.rmtree(self.tmp / "plugins" / "core")
        (self.tmp / "plugins" / "core").symlink_to(
            outside_category,
            target_is_directory=True,
        )

        code, out = self._run(["--write", "--root", str(self.tmp)])
        self.assertNotEqual(code, 0)
        self.assertIn("resolves outside", out)
        self.assertEqual(external_manifest.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
