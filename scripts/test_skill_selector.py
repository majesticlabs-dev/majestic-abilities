"""Behavior checks for the portable selector using disposable local inventories."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from tools.skill_selector.core import NONE, baseline, inventory, prepare, select
from tools.skill_selector.evaluation import evaluate
from tools.skill_selector.io import Refusal, decode_json, read_regular


class SelectorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest = self.root / "inventory.json"
        self.records = []
        self.context = {"schema_version": 1, "session_id": "session-one",
                        "request": "Review Python code for defects."}
        self.skill("review", "Review Python code for defects.")
        self.skill("write", "Write marketing copy for product pages.")

    def skill(self, name, description, manual=False, **record):
        path = self.root / name / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("---\n" + yaml.safe_dump({"name": name, "description": description,
                        "disable-model-invocation": manual}) + "---\n# Procedure\nInspect current evidence.\n")
        self.records.append(dict(id=name, name=name, path=str(path.relative_to(self.root)),
                                 agent_invocable=True, **record))
        self.save_manifest()
        return path

    def save_manifest(self):
        self.manifest.write_text(json.dumps({"schema_version": 1, "skills": self.records}))

    def prepared(self, **kwargs):
        return prepare(self.manifest, self.context, **kwargs)

    def response(self, prepared, estimates=None, none=0.1):
        if estimates is None:
            estimates = {"review": (0.7, 0.9), "write": (0.2, 0.2)}
        rows = [{"id": f"option_{i + 1:03}", "choice": estimates[s.id][0], "fit": estimates[s.id][1]}
                for i, s in enumerate(prepared.candidates)]
        return {"schema_version": 1, "request_id": prepared.state_id,
                "scores": rows + [{"id": NONE, "choice": none}]}

    def refuse(self, reason, operation):
        with self.assertRaises(Refusal) as caught:
            operation()
        self.assertEqual(reason, caught.exception.reason)

    def test_selects_only_fitting_candidate(self):
        p = self.prepared()
        output = select(p, self.response(p))
        self.assertEqual("ranked", output["decision"])
        self.assertEqual(["review"], [s["id"] for s in output["selected"]])
        self.assertEqual(1, output["selected"][0]["rank_score"])
        self.assertEqual(0.7, output["selected"][0]["choice_probability"])
        self.assertEqual(str((self.root / "review/SKILL.md").resolve()), output["selected"][0]["load_target"])
        self.assertTrue(output["advisory_only"])

    def test_none_abstains_and_ties_do_not_pass(self):
        p = self.prepared()
        output = select(p, self.response(p, {"review": (0.4, 1), "write": (0.2, 1)}, none=0.4))
        self.assertEqual("abstain", output["decision"])
        self.assertEqual("no-model-match", output["reason"])

    def test_fit_cannot_rescue_candidate_below_none(self):
        p = self.prepared()
        out = select(p, self.response(p, {"review": (0.5, 0.6), "write": (0.2, 1)}, none=0.3))
        self.assertEqual(["review"], [s["id"] for s in out["selected"]])
        removed = next(t for t in out["trace"] if t["id"] == "write")
        self.assertEqual("not-above-none", removed["stages"][-1]["outcome"])

    def test_all_low_fit_abstains(self):
        p = self.prepared()
        out = select(p, self.response(p, {"review": (0.7, 0.1), "write": (0.2, 0.1)}))
        self.assertEqual("abstain", out["decision"])

    def test_top_k_reports_omitted_mass(self):
        p = self.prepared(top_k=1)
        out = select(p, self.response(p, {"review": (0.45, 1), "write": (0.45, 1)}))
        self.assertEqual("review", out["selected"][0]["id"])
        self.assertEqual(0.5, out["omitted_mass"])
        self.assertEqual(0.5, out["selected"][0]["rank_score"])

    def test_multiple_selection_and_explicit_not_limited_by_top_k(self):
        self.context["required"] = ["write", "review"]
        out = select(self.prepared(top_k=1), None)
        self.assertEqual("explicit", out["decision"])
        self.assertEqual(["review", "write"], [s["id"] for s in out["selected"]])

    def test_explicit_manual_skill_is_not_permission_to_execute(self):
        self.skill("publish", "Publish approved releases.", manual=True)
        self.context["required"] = ["publish"]
        out = select(self.prepared(), None)
        self.assertEqual("explicit", out["decision"])
        self.assertTrue(out["selected"][0]["manual_only"])

    def test_manual_skill_never_enters_model_options(self):
        self.skill("publish", "Review Python code.", manual=True)
        p = self.prepared()
        self.assertNotIn("publish", [s.id for s in p.candidates])

    def test_exclusion_overrides_explicit(self):
        self.context.update(required=["review"], excluded=["review"])
        out = select(self.prepared(), None)
        self.assertEqual("unavailable", out["decision"])
        self.assertEqual("conflicting-explicit", out["reason"])

    def test_missing_explicit_not_replaced_by_similar_candidate(self):
        self.context["required"] = ["review-code"]
        self.assertEqual("unresolved-explicit", select(self.prepared(), None)["reason"])

    def test_quoted_text_is_not_an_explicit_directive(self):
        self.context["request"] = 'Explain the example "use write".'
        p = self.prepared()
        self.assertEqual("selection-request", p.document["kind"])

    def test_aliases_canonicalize_and_resolve(self):
        (self.root / "alias.md").symlink_to(self.root / "review/SKILL.md")
        self.records.append(dict(id="z-review", name="plugin:review", path="alias.md", agent_invocable=True))
        self.save_manifest()
        skills, _ = inventory(self.manifest)
        self.assertEqual(2, len(skills))
        self.assertEqual(("plugin:review", "review"), skills[0].aliases)
        out = select(self.prepared(required=("z-review",)), None)
        self.assertEqual("review", out["selected"][0]["id"])

    def test_alias_restrictions_combine_conservatively(self):
        self.records.append(dict(id="z-review", name="alias", path="review/SKILL.md", agent_invocable=False))
        self.save_manifest()
        self.assertNotIn("review", [s.id for s in self.prepared().candidates])

    def test_name_collisions_are_not_arbitrarily_resolved(self):
        self.records[1]["name"] = "review"
        self.save_manifest()
        self.assertEqual("unavailable", self.prepared().document["decision"])
        self.assertEqual("unresolved-explicit", self.prepared(required=("review",)).document["reason"])

    def test_duplicate_ids_rejected(self):
        self.records[1]["id"] = "review"
        self.save_manifest()
        self.refuse("duplicate-or-reserved-id", self.prepared)

    def test_loaded_reference_suppressed_only_at_matching_hash(self):
        content_hash = hashlib.sha256((self.root / "review/SKILL.md").read_bytes()).hexdigest()
        self.records[0].update(usage="reference", loaded_hash=content_hash)
        self.save_manifest()
        self.assertNotIn("review", [s.id for s in self.prepared().candidates])
        self.records[0]["loaded_hash"] = "0" * 64
        self.save_manifest()
        self.assertIn("review", [s.id for s in self.prepared().candidates])
        self.records[0].update(usage="workflow", loaded_hash=content_hash)
        self.save_manifest()
        self.assertIn("review", [s.id for s in self.prepared().candidates])

    def test_explicit_loaded_reference_still_resolves(self):
        self.records[0].update(usage="reference", loaded_hash=hashlib.sha256(
            (self.root / "review/SKILL.md").read_bytes()).hexdigest())
        self.save_manifest()
        self.assertEqual("explicit", self.prepared(required=("review",)).document["decision"])

    def test_overflow_deterministically_prefilters_but_explicit_bypasses(self):
        p = self.prepared(max_candidates=1, top_k=1)
        self.assertEqual(["review"], [s.id for s in p.candidates])
        self.assertTrue(p.document["coverage"]["retrieval_limited"])
        explicit = self.prepared(max_candidates=1, top_k=1, required=("write",))
        self.assertEqual("write", explicit.document["selected"][0]["id"])

    def test_overflow_no_match_is_not_full_roster_abstention(self):
        p = self.prepared(max_candidates=1, top_k=1)
        out = select(p, self.response(p, {"review": (0.4, 1)}, none=0.6))
        self.assertEqual("unavailable", out["decision"])
        self.context["request"] = "Biodiversity census"
        self.assertEqual("retrieval-empty", self.prepared(max_candidates=1, top_k=1).document["reason"])

    def test_context_is_bounded_and_redacted_before_truncation(self):
        secret = "sk-" + "x" * 100
        self.context["request"] = "a" * 5900 + " " + secret + " " + "z" * 5900
        p = self.prepared()
        self.assertTrue(p.context_partial)
        request = p.document["context"]["request"]
        self.assertLessEqual(len(request), 6000)
        self.assertNotIn(secret, json.dumps(p.document))
        self.assertIn("[TRUNCATED]", request)
        self.assertEqual(1, p.document["disclosure"]["context"]["request"]["redactions"])
        out = select(p, self.response(p, {"review": (0.1, 0), "write": (0.1, 0)}, none=0.8))
        self.assertEqual("unavailable", out["decision"])

    def test_roster_secrets_redacted_and_paths_not_in_request(self):
        path = self.root / "review/SKILL.md"
        path.write_text(path.read_text() + "\nBearer abcdefghijk123456\n/home/person/private/project\n")
        request = json.dumps(self.prepared().document)
        self.assertNotIn("abcdefghijk123456", request)
        self.assertNotIn("/home/person", request)
        self.assertNotIn(str(self.root), request)

    def test_tampered_or_foreign_model_output_refused(self):
        for mutate, reason in [
            (lambda r: r.update(request_id="old"), "stale-response"),
            (lambda r: r.update(command="rm -rf /"), "unknown-field"),
            (lambda r: r["scores"][0].update(id="/tmp/foreign"), "invalid-option-set"),
            (lambda r: r["scores"][0].update(choice=float("nan")), "invalid-estimate"),
            (lambda r: r["scores"][0].update(choice=True), "invalid-estimate"),
            (lambda r: r["scores"][0].update(fit=float("inf")), "invalid-estimate"),
            (lambda r: r["scores"][0].update(choice=0), "invalid-distribution"),
            (lambda r: r["scores"].pop(), "invalid-option-set"),
            (lambda r: r["scores"][1].update(id=r["scores"][0]["id"]), "invalid-option-set"),
            (lambda r: r["scores"][-1].update(fit=1), "invalid-none-fit"),
        ]:
            with self.subTest(reason=reason):
                p = self.prepared()
                response = self.response(p)
                mutate(response)
                self.refuse(reason, lambda: select(p, response))

    def test_unevaluated_fields_are_absent_from_trace(self):
        p = self.prepared(excluded=("write",))
        out = select(p, self.response(p, {"review": (0.9, 1)}))
        trace = next(t for t in out["trace"] if t["id"] == "write")
        self.assertEqual("excluded", trace["stages"][-1]["outcome"])
        self.assertNotIn("fit", json.dumps(trace))

    def test_trace_and_order_are_deterministic(self):
        p1 = self.prepared()
        self.records.reverse()
        self.save_manifest()
        p2 = self.prepared()
        output = select(p2, self.response(p2))
        # Inventory order does not alter candidate order or trace; its snapshot
        # identity changes to invalidate responses made from an older manifest.
        self.assertEqual([s.id for s in p1.candidates], [s.id for s in p2.candidates])
        self.assertEqual(p1.trace, p2.trace)
        self.assertEqual(output, select(p2, self.response(p2)))

    def test_revalidation_checks_omitted_skill_content_and_policy(self):
        p = self.prepared(max_candidates=1, top_k=1)
        path = self.root / "write/SKILL.md"
        path.write_text(path.read_text() + "changed\n")
        self.refuse("input-changed", lambda: select(p, self.response(p, {"review": (0.9, 1)})))
        p = self.prepared()
        self.records[0]["agent_invocable"] = False
        self.save_manifest()
        self.refuse("input-changed", lambda: select(p, self.response(p)))

    def test_revalidation_checks_new_roster_member_and_symlink_target(self):
        p = self.prepared()
        self.skill("test", "Test Python code.")
        self.refuse("input-changed", lambda: select(p, self.response(p)))
        self.records = self.records[:2]
        (self.root / "link.md").symlink_to(self.root / "review/SKILL.md")
        self.records[0]["path"] = "link.md"
        self.save_manifest()
        p = self.prepared()
        (self.root / "link.md").unlink()
        (self.root / "link.md").symlink_to(self.root / "write/SKILL.md")
        self.refuse("input-changed", lambda: select(p, self.response(p)))

    def test_explicit_publication_revalidates(self):
        p = self.prepared(required=("review",))
        (self.root / "review/SKILL.md").unlink()
        self.refuse("input-changed", lambda: select(p, None))

    def test_session_request_and_policy_bind_response(self):
        p = self.prepared()
        for key in ("session_id", "request"):
            original = self.context[key]
            self.context[key] = "changed"
            fresh = self.prepared()
            self.refuse("stale-response", lambda: select(fresh, self.response(p)))
            self.context[key] = original
        self.refuse("stale-response", lambda: select(self.prepared(min_fit=0.9), self.response(p)))

    def test_json_duplicate_keys_depth_and_nonfinite_rejected(self):
        for data, reason in [(b'{"x":1,"x":2}', "duplicate-key"),
                             (b'{"x":NaN}', "nonfinite-number"),
                             (b"[" * 34 + b"0" + b"]" * 34, "input-too-deep")]:
            self.refuse(reason, lambda: decode_json(data))

    def test_yaml_duplicate_alias_and_invalid_policy_rejected(self):
        path = self.root / "review/SKILL.md"
        for header, reason in [
            ("name: review\nname: other\ndescription: Test", "duplicate-key"),
            ("name: &n review\ndescription: *n", "yaml-alias-not-supported"),
            ("name: review\ndescription: Test\ndisable-model-invocation: nope", "invalid-invocation-policy"),
        ]:
            path.write_text("---\n" + header + "\n---\nBody")
            self.refuse(reason, self.prepared)

    def test_oversize_and_fifo_refused(self):
        path = self.root / "large"
        path.write_bytes(b"x" * 20)
        self.refuse("input-too-large", lambda: read_regular(path, 10))
        fifo = self.root / "pipe"
        os.mkfifo(fifo)
        self.refuse("not-regular-file", lambda: read_regular(fifo))

    def test_empty_roster_and_invalid_limits_refused(self):
        for policy in (dict(max_candidates=255), dict(top_k=0), dict(min_fit=float("nan"))):
            with self.assertRaises(Refusal):
                self.prepared(**policy)
        self.records = []
        self.save_manifest()
        self.assertEqual("empty-roster", self.prepared().document["reason"])

    def test_baseline_is_labeled_and_does_not_fabricate_fit(self):
        out = baseline(self.prepared())
        self.assertEqual("lexical-baseline", out["method"])
        self.assertIsNone(out["selected"][0]["fit"])
        self.assertEqual("review", out["selected"][0]["id"])

    def cli(self, *args):
        return subprocess.run([sys.executable, "-m", "tools.skill_selector", *args], cwd=ROOT,
                              capture_output=True, text=True, timeout=10)

    def test_real_cli_prepare_select_and_failure_with_no_writes(self):
        context_path = self.root / "context.json"
        context_path.write_text(json.dumps(self.context))
        args = ["--inventory", str(self.manifest), "--context", str(context_path)]
        before = sorted(str(p) for p in self.root.rglob("*"))
        preview = self.cli("prepare", *args)
        self.assertEqual(0, preview.returncode, preview.stderr)
        p = self.prepared()
        self.assertEqual(p.state_id, json.loads(preview.stdout)["request_id"])
        answer = self.root / "answer.json"
        answer.write_text(json.dumps(self.response(p)))
        output = self.cli("select", *args, "--response", str(answer))
        self.assertEqual(0, output.returncode, output.stderr)
        self.assertEqual("ranked", json.loads(output.stdout)["decision"])
        self.assertEqual(sorted(before + [str(answer)]),
                         sorted(str(p) for p in self.root.rglob("*")))
        answer.write_text('{"scores": "SECRET-PRIVATE-ERROR"}')
        output = self.cli("select", *args, "--response", str(answer))
        self.assertEqual(2, output.returncode)
        failed = json.loads(output.stdout)
        self.assertEqual("unavailable", failed["decision"])
        self.assertEqual(2, len(failed["trace"]))
        self.assertNotIn("SECRET-PRIVATE-ERROR", output.stdout + output.stderr)

    def test_real_cli_explicit_needs_no_model_response(self):
        context_path = self.root / "context.json"
        context_path.write_text(json.dumps(self.context))
        output = self.cli("select", "--inventory", str(self.manifest), "--context", str(context_path),
                          "--require", "review", "--response", str(self.root / "absent.json"))
        self.assertEqual(0, output.returncode, output.stderr)
        self.assertEqual("explicit", json.loads(output.stdout)["decision"])

    def dataset(self):
        return {"schema_version": 1,
                "label_provenance": {"kind": "synthetic", "assessor": "test-author", "source": "Hand-written test cases."},
                "cases": [{"id": "positive", "family": "review", "split": "holdout",
                           "context": self.context, "acceptable_ids": ["review"], "forbidden_ids": ["write"]},
                          {"id": "none", "family": "arithmetic", "split": "holdout",
                           "context": {**self.context, "request": "What is 2 plus 2?"}, "acceptable_ids": []}]}

    def test_evaluation_has_explicit_denominators_and_no_quality_claim(self):
        report = evaluate(self.manifest, self.dataset())
        metrics = report["reports"]["lexical-baseline"]
        self.assertEqual({"numerator": 1, "denominator": 1, "value": 1.0}, metrics["top_one_precision"])
        self.assertEqual(0, metrics["needless_suggestion_rate"]["numerator"])
        self.assertEqual(1, metrics["needless_suggestion_rate"]["denominator"])
        self.assertEqual("not-established", report["quality_gate"])
        self.assertFalse(report["provenance_verified"])

    def test_evaluation_keeps_failures_and_missing_responses_in_denominator(self):
        responses = {"schema_version": 1, "responses": {}}
        metrics = evaluate(self.manifest, self.dataset(), responses)["reports"]["active-model"]
        self.assertEqual(2, metrics["operational_failures"])
        self.assertEqual(2, metrics["mean_loss"]["value"])
        self.assertEqual(1, metrics["positive_case_suggestion_rate"]["denominator"])
        self.assertEqual(0, metrics["positive_case_suggestion_rate"]["numerator"])
        self.assertIsNone(metrics["top_one_precision"]["value"])

    def test_evaluation_runs_real_selection_on_recorded_scores(self):
        data = self.dataset()
        none_p = prepare(self.manifest, data["cases"][1]["context"])
        responses = {"schema_version": 1, "responses": {
            "positive": self.response(self.prepared()),
            "none": self.response(none_p, {"review": (0.1, 0), "write": (0.1, 0)}, none=0.8)}}
        metrics = evaluate(self.manifest, data, responses)["reports"]["active-model"]
        self.assertEqual(0, metrics["operational_failures"])
        self.assertEqual(0, metrics["mean_loss"]["value"])

    def test_evaluation_rejects_family_leakage_self_labels_and_unknown_ids(self):
        data = self.dataset()
        data["cases"][1].update(family="review", split="development")
        self.refuse("family-split-leakage", lambda: evaluate(self.manifest, data))
        data = self.dataset()
        data["label_provenance"]["kind"] = "selector-generated"
        self.refuse("invalid-label-provenance", lambda: evaluate(self.manifest, data))
        data = self.dataset()
        data["cases"][0]["acceptable_ids"] = ["foreign"]
        self.refuse("unknown-label-id", lambda: evaluate(self.manifest, data))

    def test_evaluation_refuses_inventory_changes_between_cases(self):
        original = baseline

        def change_after_decision(prepared):
            output = original(prepared)
            self.records[0]["agent_invocable"] = False
            self.save_manifest()
            return output

        with patch("tools.skill_selector.evaluation.baseline", side_effect=change_after_decision):
            self.refuse("input-changed", lambda: evaluate(self.manifest, self.dataset()))

    def test_254_candidates_plus_none_and_255_skill_overflow(self):
        for i in range(252):
            self.skill(f"s{i:03}", "Review Python code.")
        p = self.prepared(max_candidates=254)
        self.assertEqual(254, len(p.candidates))
        self.assertEqual(255, len(p.document["options"]))
        self.assertEqual(NONE, p.document["options"][-1]["id"])
        self.assertFalse(p.document["coverage"]["retrieval_limited"])
        self.skill("overflow", "Review Python code.")
        p = self.prepared(max_candidates=254)
        self.assertTrue(p.document["coverage"]["retrieval_limited"])
        self.assertEqual(254, len(p.candidates))
        self.assertNotIn("write", [s.id for s in p.candidates])

    def test_explicit_and_unjudged_cases_do_not_inflate_precision(self):
        data = self.dataset()
        data["cases"][0]["context"] = {**self.context, "required": ["review"]}
        data["cases"][1]["acceptable_ids"] = None
        metrics = evaluate(self.manifest, data)["reports"]["lexical-baseline"]
        self.assertEqual(1, metrics["explicit_resolution"]["numerator"])
        self.assertEqual(1, metrics["unjudged_advisory_cases"])
        self.assertEqual(0, metrics["top_one_precision"]["denominator"])
        self.assertIsNone(metrics["mean_loss"]["value"])


if __name__ == "__main__":
    unittest.main()
