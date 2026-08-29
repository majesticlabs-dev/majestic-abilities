import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("update_plugin_version.py")


class UpdatePluginVersionTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.category = "rails"
        self.plugin_dir = self.root / "plugins" / self.category

        self._write_json(
            self.plugin_dir / "plugin.json",
            {"name": "majestic-rails", "version": "0.1.0", "description": "Rails"},
        )
        self._write_json(
            self.plugin_dir / ".claude-plugin" / "plugin.json",
            {"name": "majestic-rails", "version": "0.1.0", "description": "Rails"},
        )
        self._write_json(
            self.plugin_dir / ".codex-plugin" / "plugin.json",
            {"name": "majestic-rails", "version": "0.1.0", "description": "Rails"},
        )
        self._write_json(
            self.root / ".claude-plugin" / "marketplace.json",
            {
                "plugins": [
                    {
                        "name": "majestic-misc",
                        "source": "./plugins/misc",
                        "version": "0.1.0",
                    },
                    {
                        "name": "majestic-rails",
                        "source": "./plugins/rails",
                        "version": "0.1.0",
                    },
                ]
            },
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_updates_all_version_bearing_plugin_metadata(self):
        before = self._contents()

        result = self._run("rails", "0.2.0")

        self.assertEqual(0, result.returncode, result.stderr)
        for path in (
            self.plugin_dir / "plugin.json",
            self.plugin_dir / ".claude-plugin" / "plugin.json",
            self.plugin_dir / ".codex-plugin" / "plugin.json",
        ):
            self.assertEqual("0.2.0", json.loads(path.read_text())["version"])

        marketplace = json.loads(
            (self.root / ".claude-plugin" / "marketplace.json").read_text()
        )
        versions = {entry["name"]: entry["version"] for entry in marketplace["plugins"]}
        self.assertEqual("0.2.0", versions["majestic-rails"])
        self.assertEqual("0.1.0", versions["majestic-misc"])

        after = self._contents()
        for path, old_text in before.items():
            expected = old_text
            if path.name == "marketplace.json":
                expected = expected.replace(
                    '"name": "majestic-rails",\n      "source": "./plugins/rails",\n      "version": "0.1.0"',
                    '"name": "majestic-rails",\n      "source": "./plugins/rails",\n      "version": "0.2.0"',
                )
            else:
                expected = expected.replace('"version": "0.1.0"', '"version": "0.2.0"')
            self.assertEqual(expected, after[path])

    def test_rejects_inconsistent_current_versions_without_writing(self):
        codex = self.plugin_dir / ".codex-plugin" / "plugin.json"
        data = json.loads(codex.read_text())
        data["version"] = "0.0.9"
        self._write_json(codex, data)
        before = self._contents()

        result = self._run("rails", "0.2.0")

        self.assertNotEqual(0, result.returncode)
        self.assertIn("current versions do not match", result.stderr)
        self.assertEqual(before, self._contents())

    def test_rejects_invalid_version(self):
        result = self._run("rails", "next")

        self.assertNotEqual(0, result.returncode)
        self.assertIn("valid semantic version", result.stderr)

    def _run(self, category, version):
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                category,
                version,
                "--root",
                str(self.root),
            ],
            text=True,
            capture_output=True,
            check=False,
        )

    def _contents(self):
        paths = [
            self.plugin_dir / "plugin.json",
            self.plugin_dir / ".claude-plugin" / "plugin.json",
            self.plugin_dir / ".codex-plugin" / "plugin.json",
            self.root / ".claude-plugin" / "marketplace.json",
        ]
        return {path: path.read_text() for path in paths}

    @staticmethod
    def _write_json(path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2) + "\n")


if __name__ == "__main__":
    unittest.main()
