"""Regression checks for catalog validation using disposable skill trees."""

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

import yaml

spec = importlib.util.spec_from_file_location(
    "skill_collisions", Path(__file__).with_name("check-skill-collisions.py")
)
checker = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = checker
spec.loader.exec_module(checker)


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def skill(self, directory, description, **fields):
        path = self.root / directory / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        metadata = dict(name=path.parent.name, description=description, **fields)
        path.write_text("---\n" + yaml.safe_dump(metadata) + "---\n", encoding="utf-8")
        return path

    def errors(self):
        skills, errors = checker.load_skills(self.root)
        return errors + checker.collision_errors(skills)

    def test_natural_trigger_does_not_require_magic_phrase(self):
        self.skill("plugins/rails/skills/tests", "Write Minitest tests for Ruby applications.")
        self.assertEqual([], self.errors())

    def test_manual_skill_can_describe_when_to_invoke_it(self):
        self.skill(".agents/skills/release", "Use when publishing an approved release.",
                   **{"disable-model-invocation": True})
        self.assertEqual([], self.errors())

    def test_tool_can_collide_with_installed_plugin(self):
        self.skill("tools/finder", "Find project skills.")
        self.skill("plugins/core/skills/finder", "Select project skills.")
        self.assertTrue(any("duplicate skill name" in e for e in self.errors()))

    def test_manual_metadata_does_not_hide_description_collision(self):
        self.skill(".agents/skills/release", "Publish approved releases.",
                   **{"disable-model-invocation": True})
        self.skill("plugins/core/skills/publish", "publish  approved releases.")
        self.assertTrue(any("duplicate description" in e for e in self.errors()))

    def test_duplicate_yaml_key_is_rejected(self):
        path = self.skill("plugins/core/skills/check", "Check files.")
        path.write_text("---\nname: check\nname: other\ndescription: Check files.\n---\n")
        self.assertTrue(any("duplicate key" in e for e in self.errors()))

    def test_unknown_location_is_rejected(self):
        self.skill("other/check", "Check files.")
        self.assertTrue(any("outside a recognized" in e for e in self.errors()))

    def test_invalid_invocation_type_is_rejected(self):
        self.skill(".agents/skills/check", "Check files.",
                   **{"disable-model-invocation": "false"})
        self.assertTrue(any("must be a boolean" in e for e in self.errors()))

    def test_overlap_is_advisory_not_a_semantic_verdict(self):
        self.skill("plugins/core/skills/cache", "Use when building database backed cache storage.")
        self.skill("plugins/core/skills/queue", "Use when building database backed job queues.")
        skills, errors = checker.load_skills(self.root)
        self.assertEqual([], errors + checker.collision_errors(skills))
        self.assertEqual(1, len(list(checker.overlap_candidates(skills))))


if __name__ == "__main__":
    unittest.main()
