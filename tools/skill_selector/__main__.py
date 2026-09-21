"""Run with python3 -m tools.skill_selector from the repository root."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .core import baseline, inventory, prepare, publish, result, select
from .evaluation import evaluate
from .io import Refusal, canonical, read_json, require


def parser():
    cli = argparse.ArgumentParser(description="Local advisory skill selector. No network, loading, or persistent state.")
    sub = cli.add_subparsers(dest="command", required=True)
    for name in ("inventory", "prepare", "select", "baseline", "evaluate"):
        command = sub.add_parser(name)
        command.add_argument("--inventory", type=Path, required=True,
                             help="Explicit effective runtime inventory JSON. Paths are relative to this file.")
        if name == "inventory":
            continue
        command.add_argument("--max-candidates", type=int, default=32)
        command.add_argument("--top-k", type=int, default=5)
        command.add_argument("--min-fit", type=float, default=0.5)
        if name == "evaluate":
            command.add_argument("--dataset", type=Path, required=True)
            command.add_argument("--responses", type=Path)
            command.add_argument("--split", choices=("development", "holdout"), default="holdout")
            continue
        command.add_argument("--context", type=Path, required=True)
        command.add_argument("--require", action="append", default=[])
        command.add_argument("--exclude", action="append", default=[])
        if name == "select":
            command.add_argument("--response", type=Path,
                                 help="Active-model response JSON. Not needed for explicit/local decisions.")
    return cli


def run(args):
    if args.command == "inventory":
        skills, state_id = inventory(args.inventory)
        # This listing is local. It contains paths and must not be sent as a model request.
        return {"schema_version": 1, "kind": "inventory", "state_id": state_id,
                "advisory_only": True, "skills": [
                    {"id": s.id, "ids": s.ids, "aliases": s.aliases, "path": str(s.path),
                     "content_hash": s.content_hash, "agent_invocable": s.invocable,
                     "loaded_reference": s.loaded} for s in skills]}
    policy = dict(max_candidates=args.max_candidates, top_k=args.top_k, min_fit=args.min_fit)
    if args.command == "evaluate":
        return evaluate(args.inventory, read_json(args.dataset),
                        read_json(args.responses) if args.responses else None,
                        split=args.split, **policy)
    context = read_json(args.context)
    prepared = prepare(args.inventory, context, required=args.require, excluded=args.exclude, **policy)
    if args.command == "prepare":
        output = (publish(prepared, prepared.document) if "decision" in prepared.document
                  else prepared.document)
    elif args.command == "baseline":
        output = baseline(prepared)
    else:
        # Explicit resolution never needs to read a model answer.
        try:
            response = (read_json(args.response) if args.response and "decision" not in prepared.document else None)
            output = select(prepared, response)
        except Refusal as error:
            output = result("unavailable", error.reason, prepared.trace)
    require(read_json(args.context) == context, "input-changed")
    return output


def main():
    args = parser().parse_args()
    try:
        output = run(args)
        require(len(canonical(output)) <= 2 * 1024 * 1024, "output-too-large")
    except Refusal as error:
        output = result("unavailable", error.reason)
    except (OSError, UnicodeError):
        # Error strings can contain private paths or source text.
        output = result("unavailable", "input-unavailable")
    try:
        sys.stdout.write(json.dumps(output, sort_keys=True, ensure_ascii=True, allow_nan=False) + "\n")
    except BrokenPipeError:
        return 1
    return 2 if output.get("decision") == "unavailable" else 0


if __name__ == "__main__":
    raise SystemExit(main())
