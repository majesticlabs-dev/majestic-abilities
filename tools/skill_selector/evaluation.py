"""Offline comparison against caller-supplied labels, with explicit denominators."""
from __future__ import annotations

from .core import baseline, inventory, prepare, result, select
from .io import Refusal, fields, identifier, names, require, text


def rate(numerator, denominator):
    return {"numerator": numerator, "denominator": denominator,
            "value": numerator / denominator if denominator else None}


def evaluate(manifest_path, dataset, responses=None, *, split="holdout", **policy):
    fields(dataset, ("schema_version", "label_provenance", "cases"))
    require(type(dataset["schema_version"]) is int and dataset["schema_version"] == 1,
            "unsupported-schema")
    provenance = dataset["label_provenance"]
    fields(provenance, ("kind", "assessor", "source"))
    require(provenance["kind"] in ("independent", "synthetic"), "invalid-label-provenance")
    text(provenance["assessor"])
    text(provenance["source"], 2000)
    cases = dataset["cases"]
    require(isinstance(cases, list) and 1 <= len(cases) <= 1000, "invalid-case-count")
    families, case_ids = {}, set()
    for case in cases:
        fields(case, ("id", "family", "split", "context", "acceptable_ids"), ("forbidden_ids",))
        case_id, family = identifier(case["id"]), identifier(case["family"])
        require(case_id not in case_ids, "duplicate-case")
        case_ids.add(case_id)
        require(case["split"] in ("development", "holdout"), "invalid-split")
        require(family not in families or families[family] == case["split"], "family-split-leakage")
        families[family] = case["split"]
        if case["acceptable_ids"] is not None:
            acceptable = names(case["acceptable_ids"])
            require(not set(acceptable) & set(names(case.get("forbidden_ids", []))), "conflicting-labels")
        else:
            names(case.get("forbidden_ids", []))
    if responses is not None:
        fields(responses, ("schema_version", "responses"))
        require(type(responses["schema_version"]) is int and responses["schema_version"] == 1,
                "unsupported-schema")
        require(isinstance(responses["responses"], dict) and responses["responses"].keys() <= case_ids,
                "unknown-response-case")
    chosen = [case for case in cases if case["split"] == split]
    require(bool(chosen), "empty-evaluation-split")
    methods = ["lexical-baseline"] + (["active-model"] if responses is not None else [])
    _, roster_id = inventory(manifest_path)
    reports = {}
    for method in methods:
        rows = []
        labeled = positive = no_match = emitted = correct = useful = needless = 0
        failures = violations = unknown = explicit = explicit_correct = 0
        loss = 0
        for case in chosen:
            try:
                prepared = prepare(manifest_path, case["context"], **policy)
                require(prepared.roster_id == roster_id, "input-changed")
                # Labels refer to stable canonical IDs, never provider option handles.
                known = {s.id for s in prepared.skills}
                require(set(case["acceptable_ids"] or []) <= known, "unknown-label-id")
                require(set(case.get("forbidden_ids", [])) <= known, "unknown-label-id")
                output = (baseline(prepared) if method == "lexical-baseline" else
                          select(prepared, responses["responses"].get(case["id"])))
            except Refusal as error:
                if error.reason in ("unknown-label-id", "input-changed"):
                    raise
                output = result("unavailable", error.reason)
            selected_ids = [s["id"] for s in output["selected"]]
            failed = output["decision"] == "unavailable"
            failures += failed
            violations += bool(set(selected_ids) & set(case.get("forbidden_ids", [])))
            is_explicit = bool(case["context"].get("required")) if isinstance(case["context"], dict) else False
            if is_explicit:
                explicit += 1
                explicit_correct += (output["decision"] == "explicit" and
                                     set(selected_ids) == set(case["acceptable_ids"] or []))
            elif case["acceptable_ids"] is None:
                unknown += 1
            else:
                accepted = set(case["acceptable_ids"])
                labeled += 1
                positive += bool(accepted)
                no_match += not accepted
                emitted += bool(selected_ids)
                top_correct = bool(selected_ids) and selected_ids[0] in accepted
                correct += top_correct
                useful += bool(accepted) and top_correct
                needless += not accepted and bool(selected_ids)
                # Failed attempted cases stay in the common denominator.
                loss += (2 if failed else 0 if top_correct or (not accepted and not selected_ids)
                         else 2 if selected_ids else 1)
            rows.append({"id": case["id"], "family": case["family"],
                         "decision": output["decision"], "reason": output["reason"],
                         "selected_ids": selected_ids})
        reports[method] = {
            "cases": len(chosen), "families": len({c["family"] for c in chosen}),
            "labeled_advisory_cases": labeled, "unjudged_advisory_cases": unknown,
            "operational_failures": failures, "forbidden_selection_cases": violations,
            "explicit_resolution": rate(explicit_correct, explicit),
            "top_one_precision": rate(correct, emitted),
            "positive_case_suggestion_rate": rate(useful, positive),
            "needless_suggestion_rate": rate(needless, no_match),
            "mean_loss": rate(loss, labeled), "results": rows,
        }
    require(inventory(manifest_path)[1] == roster_id, "input-changed")
    return {"schema_version": 1, "kind": "evaluation", "advisory_only": True,
            "roster_id": roster_id, "split": split, "label_provenance": provenance,
            "provenance_verified": False, "quality_gate": "not-established",
            "interpretation": "Descriptive case rates only. Related families are not independent samples. "
                              "Supplied labels and model responses are not proof of task improvement.",
            "reports": reports}
