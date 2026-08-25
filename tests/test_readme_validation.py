#!/usr/bin/env python3
"""Tests for the README support-contract validator."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REQUIRED_SCRIPTS = (
    "sync-plugin-metadata.py",
    "check-agent-plugins.sh",
    "check-claude-plugins.sh",
    "check-codex-plugins.sh",
    "check-cookbooks.sh",
    "check-cursor-plugins.sh",
    "check-opencode-loader.sh",
    "check-readme.sh",
)


class ReadmeValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="readme-validation-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        shutil.copy2(REPO / "README.md", self.tmp / "README.md")
        workflow = self.tmp / ".github" / "workflows" / "validate.yml"
        workflow.parent.mkdir(parents=True)
        shutil.copy2(REPO / ".github" / "workflows" / "validate.yml", workflow)

        scripts = self.tmp / "scripts"
        scripts.mkdir()
        for name in REQUIRED_SCRIPTS:
            source = REPO / "scripts" / name
            target = scripts / name
            if source.exists():
                shutil.copy2(source, target)
            else:
                target.touch()
        os.chmod(scripts / "check-readme.sh", 0o755)

        skill_files = list(REPO.glob("plugins/*/skills/*/SKILL.md"))
        skill_files.extend(REPO.glob("cookbooks/*/SKILL.md"))
        for source in skill_files:
            target = self.tmp / source.relative_to(REPO)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

    def _run(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", "scripts/check-readme.sh"],
            cwd=self.tmp,
            capture_output=True,
            text=True,
        )

    def test_current_readme_passes(self) -> None:
        result = self._run()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_positive_unsupported_claims_fail_despite_negative_statements(self) -> None:
        readme = self.tmp / "README.md"
        readme.write_text(
            readme.read_text(encoding="utf-8")
            + "\nInstall via the Cursor Marketplace. "
            + "The loader publishes an npm package and rewrites `opencode.json`.\n",
            encoding="utf-8",
        )
        result = self._run()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Cursor Marketplace submission claim", result.stdout)
        self.assertIn("OpenCode/npm publication claim", result.stdout)
        self.assertIn("opencode.json rewrite claim", result.stdout)


if __name__ == "__main__":
    unittest.main()
