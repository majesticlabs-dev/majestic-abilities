import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "plugins/engineer/skills/create-verification-skill/scripts/cleanup_project_creator.py"
CREATOR = "create-verification-skill"


class CreatorCleanupTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.project = self.root / "project"
        self.project.mkdir()
        self.creator = self.make_skill(self.project / ".agents/skills" / CREATOR, CREATOR)
        self.runtime = self.make_skill(self.project / ".agents/skills/check-export", "check-export")
        self.verifier = self.make_skill(self.project / ".agents/skills/verify-project", "verify-project")
        self.lock = self.project / "skills-lock.json"

    def make_skill(self, path, name):
        path.mkdir(parents=True)
        (path / "SKILL.md").write_text(f"---\nname: {name}\ndescription: Test fixture\n---\n")
        return path

    def write_lock(self, data):
        self.lock.write_text(json.dumps(data))

    def run_cleanup(self, *extra, helper=HELPER, directories=None):
        command = [sys.executable, str(helper), "--project-root", str(self.project)]
        for directory in directories or [self.creator]:
            command.extend(["--skill-dir", str(directory)])
        return subprocess.run(command + list(extra), capture_output=True, text=True)

    def test_removes_itself_and_preserves_runtime_dependencies_and_shared_records(self):
        installed_helper = self.creator / "scripts/cleanup_project_creator.py"
        installed_helper.parent.mkdir()
        shutil.copy2(HELPER, installed_helper)
        original = {
            "version": 1,
            "skills": {
                CREATOR: {"source": "catalog"},
                "check-export": {"source": "project", "hash": "unchanged"},
                "verify-project": {"source": "project"},
            },
            "project-note": {"preserve": True},
        }
        self.write_lock(original)
        result = self.run_cleanup(helper=installed_helper)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.creator.exists())
        self.assertTrue((self.runtime / "SKILL.md").is_file())
        self.assertTrue((self.verifier / "SKILL.md").is_file())
        del original["skills"][CREATOR]
        self.assertEqual(json.loads(self.lock.read_text()), original)

    def test_dry_run_changes_nothing(self):
        self.write_lock({"version": 1, "skills": {CREATOR: {"source": "catalog"}}})
        before = self.lock.read_bytes()
        result = self.run_cleanup("--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(self.creator.exists())
        self.assertEqual(self.lock.read_bytes(), before)
        self.assertTrue(json.loads(result.stdout)["would_remove_lock_entry"])

    def test_alias_cleanup_preserves_global_and_internal_symlink_targets(self):
        global_skill = self.make_skill(self.root / "shared" / CREATOR, CREATOR)
        alias = self.project / ".claude/skills" / CREATOR
        alias.parent.mkdir(parents=True)
        alias.symlink_to(global_skill, target_is_directory=True)
        protected = self.root / "shared/user-data.txt"
        protected.write_text("keep")
        (self.creator / "linked-data").symlink_to(protected)
        result = self.run_cleanup(directories=[alias, self.creator])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(alias.is_symlink())
        self.assertTrue((global_skill / "SKILL.md").is_file())
        self.assertEqual(protected.read_text(), "keep")

    def test_parent_symlink_outside_project_blocks_cleanup(self):
        outside = self.make_skill(self.root / "outside/skills" / CREATOR, CREATOR)
        parent = self.project / "redirected-skills"
        parent.symlink_to(outside.parent, target_is_directory=True)
        result = self.run_cleanup(directories=[self.creator, parent / CREATOR])
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(self.creator.exists())
        self.assertTrue(outside.exists())

    def test_catalog_source_cannot_be_removed(self):
        source = self.make_skill(self.project / "plugins/engineer/skills" / CREATOR, CREATOR)
        result = self.run_cleanup(directories=[source])
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(source.exists())

    def test_malformed_lock_blocks_before_removal(self):
        self.lock.write_text("{invalid")
        result = self.run_cleanup()
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(self.creator.exists())
        self.assertEqual(self.lock.read_text(), "{invalid")

    def test_shared_lock_symlink_is_preserved(self):
        shared_lock = self.root / "shared-lock.json"
        shared_lock.write_text(json.dumps({"skills": {CREATOR: {}}}))
        self.lock.symlink_to(shared_lock)
        before = shared_lock.read_bytes()
        result = self.run_cleanup()
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(self.creator.exists())
        self.assertTrue(self.lock.is_symlink())
        self.assertEqual(shared_lock.read_bytes(), before)

    def test_different_skill_identity_is_preserved(self):
        (self.creator / "SKILL.md").write_text("---\nname: another-skill\n---\n")
        result = self.run_cleanup()
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(self.creator.exists())

    def test_empty_owned_lock_is_removed_and_cleanup_can_repeat(self):
        self.write_lock({"version": 1, "skills": {CREATOR: {}}})
        first = self.run_cleanup()
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertFalse(self.lock.exists())
        second = self.run_cleanup()
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(json.loads(second.stdout)["removed"], [])

    def test_lock_without_creator_entry_is_not_rewritten(self):
        self.lock.write_text('{\n "skills": {"check-export": {}}, "custom": 2\n}\n')
        original = self.lock.read_bytes()
        result = self.run_cleanup()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.lock.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
