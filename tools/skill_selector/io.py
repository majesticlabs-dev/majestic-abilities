"""Bounded local input and disclosure helpers. No network or persistent state."""
from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat

import yaml

JSON_BYTES = 1024 * 1024
SKILL_BYTES = 256 * 1024
FRONTMATTER_BYTES = 16 * 1024
MAX_DEPTH = 32


class Refusal(ValueError):
    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise Refusal(reason)


def canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=True,
                      separators=(",", ":"), allow_nan=False).encode()


def digest(value) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def read_regular(path: Path, limit: int = JSON_BYTES) -> bytes:
    """Open only a regular file; do not block on a FIFO supplied as input."""
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
        with os.fdopen(fd, "rb") as stream:
            require(stat.S_ISREG(os.fstat(stream.fileno()).st_mode), "not-regular-file")
            data = stream.read(limit + 1)
        require(len(data) <= limit, "input-too-large")
        return data
    except OSError as error:
        raise Refusal("input-unavailable") from error


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate-key")
        result[key] = value
    return result


def check_depth(value, depth=0):
    require(depth <= MAX_DEPTH, "input-too-deep")
    if isinstance(value, dict):
        for child in value.values():
            check_depth(child, depth + 1)
    elif isinstance(value, list):
        for child in value:
            check_depth(child, depth + 1)
    elif isinstance(value, float):
        require(math.isfinite(value), "nonfinite-number")


def decode_json(data: bytes):
    require(len(data) <= JSON_BYTES, "input-too-large")
    try:
        value = json.loads(data, object_pairs_hook=unique_pairs,
                           parse_constant=lambda _: (_ for _ in ()).throw(Refusal("nonfinite-number")))
        check_depth(value)
        return value
    except (UnicodeError, json.JSONDecodeError, RecursionError) as error:
        raise Refusal("invalid-json") from error


def read_json(path: Path):
    return decode_json(read_regular(path))


def fields(value, required, optional=()):
    require(isinstance(value, dict), "expected-object")
    require(set(required) <= value.keys(), "missing-field")
    require(value.keys() <= set(required) | set(optional), "unknown-field")


def text(value, limit=256, empty=False):
    require(isinstance(value, str) and len(value) <= limit, "invalid-text")
    require(empty or bool(value.strip()), "empty-text")
    require(not any(ord(c) < 32 and c not in "\n\r\t" for c in value), "control-character")
    return value


def identifier(value):
    require(isinstance(value, str) and bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.:/-]{0,127}", value)),
            "invalid-identifier")
    return value


def names(value):
    require(isinstance(value, list) and len(value) <= 256, "invalid-name-list")
    result = [identifier(item) for item in value]
    require(len(set(result)) == len(result), "duplicate-name")
    return result


class MetadataLoader(yaml.SafeLoader):
    pass


def yaml_mapping(loader, node, deep=False):
    pairs = []
    for key, value in node.value:
        require(isinstance(key, yaml.ScalarNode) and key.tag == "tag:yaml.org,2002:str",
                "invalid-metadata-key")
        pairs.append((loader.construct_object(key, deep=deep),
                      loader.construct_object(value, deep=deep)))
    return unique_pairs(pairs)


MetadataLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, yaml_mapping)


def skill_text(data: bytes):
    try:
        source = data.decode("utf-8")
        lines = source.splitlines(keepends=True)
        require(bool(lines) and lines[0].strip() == "---", "missing-frontmatter")
        closing = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
        require(closing is not None, "missing-frontmatter-end")
        header = "".join(lines[1:closing])
        require(len(header.encode()) <= FRONTMATTER_BYTES, "frontmatter-too-large")
        depth = 0
        for token in yaml.scan(header):
            require(not isinstance(token, (yaml.AliasToken, yaml.AnchorToken)), "yaml-alias-not-supported")
            if isinstance(token, (yaml.BlockMappingStartToken, yaml.BlockSequenceStartToken,
                                  yaml.FlowMappingStartToken, yaml.FlowSequenceStartToken)):
                depth += 1
                require(depth <= MAX_DEPTH, "input-too-deep")
            elif isinstance(token, (yaml.BlockEndToken, yaml.FlowMappingEndToken, yaml.FlowSequenceEndToken)):
                depth -= 1
        metadata = yaml.load(header, Loader=MetadataLoader)
        require(isinstance(metadata, dict), "invalid-frontmatter")
        check_depth(metadata)
        text(metadata.get("name"))
        text(metadata.get("description"), FRONTMATTER_BYTES)
        require(type(metadata.get("disable-model-invocation", False)) is bool,
                "invalid-invocation-policy")
        return metadata, "".join(lines[closing + 1:])
    except (UnicodeError, yaml.YAMLError, RecursionError) as error:
        raise Refusal("invalid-frontmatter") from error


# Conservative common-pattern redaction, not a guarantee that prose is public.
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN [^-]*PRIVATE KEY-----[\s\S]*?-----END [^-]*PRIVATE KEY-----"),
    re.compile(r"\b(?:sk-|ghp_|github_pat_|xox[baprs]-)[A-Za-z0-9_-]{8,}"),
    re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
    re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/-]+=*"),
    re.compile(r"(?i)\b(?:api[_-]?key|token|password|secret)\s*[:=]\s*[\"']?[^\s\"',;]+"),
    re.compile(r"https?://[^/\s:@]+:[^/\s@]+@[^\s]+"),
    re.compile(r"(?<!\w)(?:/Users/|/home/|/private/|/tmp/)[^\s\"'<>]+"),
]


def redact(value: str):
    count = 0
    for pattern in SECRET_PATTERNS:
        value, found = pattern.subn("[REDACTED]", value)
        count += found
    # Remove control characters from untrusted skill bodies before rendering.
    value = "".join(c for c in value if ord(c) >= 32 or c in "\n\r\t")
    return value, count


def bounded_text(value: str, limit: int):
    clean, redactions = redact(value)
    truncated = len(clean) > limit
    if truncated:
        marker = "\n[TRUNCATED]\n"
        head = (limit - len(marker)) // 2
        clean = clean[:head] + marker + clean[-(limit - len(marker) - head):]
    return clean, {"truncated": truncated, "redactions": redactions}
