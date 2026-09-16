#!/usr/bin/env python3
"""Validate skill names, descriptions, invocation, and install-scope collisions."""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Set, Tuple

try:
    import yaml
except ModuleNotFoundError:
    sys.exit("FAIL: PyYAML is required; install requirements-dev.txt")


TRIGGER_PATTERN = re.compile(
    r"\bUse (?:proactively )?(?:only )?(?:when|before|after|for)\b"
)
TOKEN_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
STOP_WORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "be",
    "before",
    "by",
    "for",
    "from",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "the",
    "their",
    "then",
    "this",
    "to",
    "use",
    "when",
    "with",
    "without",
}


class UniqueKeyLoader(yaml.SafeLoader):
    """YAML loader that rejects duplicate mapping keys."""


def construct_unique_mapping(
    loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> Dict[Any, Any]:
    mapping: Dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    construct_unique_mapping,
)


@dataclass(frozen=True)
class Skill:
    path: Path
    name: str
    description: str
    kind: str
    native_scope: str
    aggregate_scope: str
    model_invoked: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--inventory",
        action="store_true",
        help="print a tab-separated inventory after validation",
    )
    parser.add_argument(
        "--overlaps",
        type=int,
        default=0,
        metavar="COUNT",
        help="print the strongest description-overlap candidates",
    )
    return parser.parse_args()


def classify(path: Path) -> Tuple[str, str, str]:
    parts = path.parts
    if len(parts) == 5 and parts[0] == "plugins" and parts[2] == "skills":
        return "plugin", f"plugin:{parts[1]}", "combined-catalog"
    if len(parts) == 4 and parts[:2] == (".agents", "skills"):
        return "repository", "repository", "combined-catalog"
    if len(parts) == 3 and parts[0] == "tools":
        return "tool", f"tool:{parts[1]}", f"tool:{parts[1]}"
    return "unclassified", "unclassified", "unclassified"


def frontmatter(path: Path) -> Dict[str, Any]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("must start with YAML frontmatter")
    try:
        closing = lines.index("---", 1)
    except ValueError as error:
        raise ValueError("has no closing YAML frontmatter delimiter") from error

    try:
        fields = yaml.load("\n".join(lines[1:closing]), Loader=UniqueKeyLoader)
    except yaml.YAMLError as error:
        raise ValueError(f"has invalid YAML frontmatter: {error}") from error
    if not isinstance(fields, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return fields


def load_skills(root: Path) -> Tuple[List[Skill], List[str]]:
    skills: List[Skill] = []
    errors: List[str] = []

    for absolute_path in sorted(root.glob("**/SKILL.md")):
        path = absolute_path.relative_to(root)
        kind, native_scope, aggregate_scope = classify(path)
        if kind == "unclassified":
            errors.append(f"{path}: is outside a recognized skill runtime scope")

        try:
            fields = frontmatter(absolute_path)
        except (OSError, ValueError) as error:
            errors.append(f"{path}: {error}")
            continue

        name = fields.get("name")
        description = fields.get("description")
        disabled = fields.get("disable-model-invocation", False)

        if not isinstance(name, str) or not name.strip():
            errors.append(f"{path}: name must be a non-empty string")
            continue
        if name != path.parent.name:
            errors.append(
                f"{path}: declares name {name!r}, expected directory name {path.parent.name!r}"
            )
        if not isinstance(description, str) or not description.strip():
            errors.append(f"{path}: description must be a non-empty string")
            continue
        if description != description.strip():
            errors.append(f"{path}: description has leading or trailing whitespace")
        if "\n" in description:
            errors.append(f"{path}: description must be one line")
        if not isinstance(disabled, bool):
            errors.append(f"{path}: disable-model-invocation must be a boolean")
            continue

        model_invoked = not disabled
        if model_invoked and not TRIGGER_PATTERN.search(description):
            errors.append(
                f"{path}: model-invoked description needs an explicit Use when/before/after/for trigger"
            )
        if not model_invoked and TRIGGER_PATTERN.search(description):
            errors.append(
                f"{path}: user-invoked description must summarize behavior, not advertise a model trigger"
            )

        skills.append(
            Skill(
                path=path,
                name=name,
                description=description,
                kind=kind,
                native_scope=native_scope,
                aggregate_scope=aggregate_scope,
                model_invoked=model_invoked,
            )
        )

    return skills, errors


def normalized_description(description: str) -> str:
    return " ".join(description.casefold().split())


def collision_errors(skills: Sequence[Skill]) -> List[str]:
    errors: List[str] = []
    by_name: Dict[Tuple[str, str], List[Skill]] = defaultdict(list)
    by_description: Dict[Tuple[str, str], List[Skill]] = defaultdict(list)

    for skill in skills:
        by_name[(skill.aggregate_scope, skill.name)].append(skill)
        if skill.model_invoked:
            key = (skill.aggregate_scope, normalized_description(skill.description))
            by_description[key].append(skill)

    for (scope, name), matches in sorted(by_name.items()):
        if len(matches) > 1:
            paths = ", ".join(str(match.path) for match in matches)
            errors.append(f"{scope}: duplicate skill name {name!r}: {paths}")

    for (scope, _description), matches in sorted(by_description.items()):
        if len(matches) > 1:
            paths = ", ".join(str(match.path) for match in matches)
            errors.append(f"{scope}: duplicate model-facing description: {paths}")

    return errors


def description_tokens(description: str) -> Set[str]:
    return {
        token
        for token in TOKEN_PATTERN.findall(description.casefold())
        if token not in STOP_WORDS and len(token) > 2
    }


def overlap_candidates(skills: Sequence[Skill]) -> Iterable[Tuple[float, Skill, Skill]]:
    model_skills = [skill for skill in skills if skill.model_invoked]
    candidates: List[Tuple[float, Skill, Skill]] = []
    for index, left in enumerate(model_skills):
        left_tokens = description_tokens(left.description)
        for right in model_skills[index + 1 :]:
            if left.aggregate_scope != right.aggregate_scope:
                continue
            right_tokens = description_tokens(right.description)
            intersection = left_tokens & right_tokens
            if len(intersection) < 3:
                continue
            union = left_tokens | right_tokens
            score = len(intersection) / len(union)
            candidates.append((score, left, right))
    return sorted(
        candidates,
        key=lambda candidate: (
            -candidate[0],
            str(candidate[1].path),
            str(candidate[2].path),
        ),
    )


def print_inventory(skills: Sequence[Skill]) -> None:
    print("path\tname\tkind\tnative_scope\taggregate_scope\tinvocation\tdescription")
    for skill in skills:
        description = skill.description.replace("\t", " ")
        invocation = "model" if skill.model_invoked else "user"
        print(
            f"{skill.path}\t{skill.name}\t{skill.kind}\t{skill.native_scope}\t"
            f"{skill.aggregate_scope}\t{invocation}\t{description}"
        )


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parent.parent
    skills, errors = load_skills(root)
    errors.extend(collision_errors(skills))

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    counts: Dict[str, int] = defaultdict(int)
    scope_counts: Dict[str, int] = defaultdict(int)
    invocation_counts: Dict[str, int] = defaultdict(int)
    for skill in skills:
        counts[skill.kind] += 1
        scope_counts[skill.native_scope] += 1
        invocation_counts["model" if skill.model_invoked else "user"] += 1
    count_summary = ", ".join(
        f"{kind}={count}" for kind, count in sorted(counts.items())
    )
    print(
        f"OK: {len(skills)} skills have unique names, valid descriptions, and explicit "
        f"invocation behavior ({count_summary})"
    )
    print(
        "Scopes: "
        + ", ".join(
            f"{scope}={count}" for scope, count in sorted(scope_counts.items())
        )
    )
    print(
        "Invocation: "
        + ", ".join(
            f"{invocation}={count}"
            for invocation, count in sorted(invocation_counts.items())
        )
    )

    if args.overlaps:
        print("\nDescription overlap candidates:")
        for score, left, right in list(overlap_candidates(skills))[: args.overlaps]:
            print(f"{score:.3f}\t{left.path}\t{right.path}")

    if args.inventory:
        print("\nInventory:")
        print_inventory(skills)

    return 0


if __name__ == "__main__":
    sys.exit(main())
