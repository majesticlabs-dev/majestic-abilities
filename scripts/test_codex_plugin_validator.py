"""Invocation-policy regression checks using disposable skill packages."""

import importlib.util
from pathlib import Path
import tempfile
import unittest

import yaml

spec = importlib.util.spec_from_file_location(
    "codex_plugin_validator",
    Path(__file__).parent / "vendor/codex-plugin-validator/validate_plugin.py",
)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class InvocationPolicyTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.skill_root = Path(directory.name) / "skills" / "example"
        self.skill_root.mkdir(parents=True)

    def skill(self, fields=None, agent=None):
        metadata = {"name": "example", "description": "Review an approved change."}
        metadata.update(fields or {})
        (self.skill_root / "SKILL.md").write_text(
            "---\n" + yaml.safe_dump(metadata) + "---\n\nReview the change.\n"
        )
        if agent is not None:
            path = self.skill_root / "agents/openai.yaml"
            path.parent.mkdir(exist_ok=True)
            path.write_text(yaml.safe_dump(agent))

    def agent(self, policy=None):
        result = {
            "interface": {
                "display_name": "Example",
                "short_description": "Review an approved change",
            }
        }
        if policy is not None:
            result["policy"] = policy
        return result

    def errors(self):
        errors = []
        validator.validate_skill_manifest(self.skill_root, errors)
        return errors

    def test_ordinary_skill_needs_no_invocation_metadata(self):
        self.skill()
        self.assertEqual([], self.errors())

    def test_false_frontmatter_preserves_ordinary_skills(self):
        for key in ("disable-model-invocation", "disable_model_invocation"):
            with self.subTest(key=key):
                self.skill({key: False})
                self.assertEqual([], self.errors())

    def test_manual_skill_requires_explicit_codex_policy(self):
        for key in ("disable-model-invocation", "disable_model_invocation"):
            with self.subTest(key=key):
                self.skill({key: True}, self.agent({"allow_implicit_invocation": False}))
                self.assertEqual([], self.errors())

    def test_manual_skill_without_agent_metadata_is_rejected(self):
        self.skill({"disable-model-invocation": True})
        self.assertTrue(self.errors())

    def test_manual_skill_without_explicit_policy_is_rejected(self):
        for policy in (None, {}, {"allow_implicit_invocation": True}):
            with self.subTest(policy=policy):
                self.skill({"disable-model-invocation": True}, self.agent(policy))
                self.assertTrue(self.errors())

    def test_non_boolean_frontmatter_is_rejected(self):
        for key in ("disable-model-invocation", "disable_model_invocation"):
            for value in ("true", "false", 0, 1, None, [], {}):
                with self.subTest(key=key, value=value):
                    self.skill({key: value}, self.agent({"allow_implicit_invocation": False}))
                    self.assertTrue(self.errors())

    def test_conflicting_frontmatter_aliases_are_rejected(self):
        self.skill(
            {"disable-model-invocation": False, "disable_model_invocation": True},
            self.agent({"allow_implicit_invocation": False}),
        )
        self.assertTrue(self.errors())

    def test_non_boolean_codex_policy_is_rejected(self):
        for value in ("false", 0, 1):
            with self.subTest(value=value):
                self.skill(
                    {"disable-model-invocation": True},
                    self.agent({"allow_implicit_invocation": value}),
                )
                self.assertTrue(self.errors())

    def test_invalid_agent_metadata_remains_rejected(self):
        self.skill(
            {"disable-model-invocation": True},
            {"interface": {}, "policy": {"allow_implicit_invocation": False}},
        )
        self.assertTrue(self.errors())


if __name__ == "__main__":
    unittest.main()
