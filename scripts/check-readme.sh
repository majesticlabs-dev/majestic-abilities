#!/usr/bin/env bash
# Verify README support-matrix contract, catalog counts, workflow trigger, and banned names.
set -euo pipefail

cd "$(dirname "$0")/.."

README="README.md"
WORKFLOW=".github/workflows/validate.yml"
status=0

fail() {
  echo "FAIL: $1"
  status=1
}

if [ ! -f "$README" ]; then
  echo "FAIL: $README is required"
  exit 1
fi

if [ ! -f "$WORKFLOW" ]; then
  fail "missing workflow: $WORKFLOW"
elif ! grep -Eq 'branches:[[:space:]]*\[master\]' "$WORKFLOW"; then
  fail "$WORKFLOW must trigger on the master branch"
fi

python3 - "$README" <<'PY' || status=1
import glob
import os
import re
import sys
from pathlib import Path

readme_path = Path(sys.argv[1])
text = readme_path.read_text(encoding="utf-8")
errors = []

def fail(message):
    errors.append(message)

# Banned legacy repository names.
if re.search(r"majestic-ai-", text):
    fail("README must not reference majestic-ai- names")

# Required support headings / route markers.
required_markers = [
    ("## Install As Claude Code Plugins", "Claude Code install heading"),
    ("## Install As Codex Plugins", "Codex install heading"),
    ("## Install With `npx skills`", "Skills CLI / Pi install heading"),
    ("## Install In Cursor", "Cursor install heading"),
    ("## Install In OpenCode", "OpenCode install heading"),
    ("## Layout", "Layout heading"),
    ("## Validate", "Validate heading"),
    ("OpenCode V1", "OpenCode V1 version scope"),
    ("1.18.22", "pinned OpenCode version"),
    ("OpenCode V2 is unsupported", "OpenCode V2 exclusion"),
    ("~/.cursor/plugins/local/", "Cursor local symlink destination"),
    ("Developer: Reload Window", "Cursor reload instruction"),
    ("~/.config/opencode/plugins/majestic-abilities.js", "OpenCode user symlink destination"),
    ("git -C <checkout> pull --ff-only", "shared update command"),
    ("python3 scripts/sync-plugin-metadata.py --write", "metadata write command"),
    ("python3 scripts/sync-plugin-metadata.py --check", "metadata check command"),
    ("scripts/check-agent-plugins.sh", "portable gate"),
    ("scripts/check-claude-plugins.sh", "Claude gate"),
    ("scripts/check-codex-plugins.sh", "Codex gate"),
    ("scripts/check-cookbooks.sh", "cookbooks gate"),
    ("scripts/check-cursor-plugins.sh", "Cursor gate"),
    ("scripts/check-opencode-loader.sh", "OpenCode gate"),
    ("scripts/check-readme.sh", "README gate"),
    ("Grok and Kimi have no dedicated plugin packaging", "Grok/Kimi packaging exclusion"),
    ("no Cursor-native", "no Cursor-native claim"),
]

for marker, label in required_markers:
    if marker not in text:
        fail(f"README missing required {label}: {marker!r}")

# Reject unsupported marketplace / publication claims for Cursor and OpenCode.
# Remove only the approved negative statements before searching for positive claims.
claim_text = text
for approved in (
    "no Cursor-native manifests and no Cursor marketplace files",
    "Official Cursor Marketplace submission is out of scope",
    "does not generate commands, rewrite `opencode.json`, or publish an npm package",
):
    claim_text = claim_text.replace(approved, "")

forbidden_claims = [
    (r"(?i)cursor marketplace", "Cursor Marketplace submission claim"),
    (r"(?i)publish.*(?:opencode|npm).*package", "OpenCode/npm publication claim"),
    (r"(?i)opencode\.json", "opencode.json rewrite claim"),
]
for pattern, label in forbidden_claims:
    if re.search(pattern, claim_text):
        fail(f"README must not claim supported {label}")

# Catalog skill counts from the filesystem (exclude cookbooks).
cookbook_paths = set()
for skill in list(glob.glob("plugins/*/skills/*/SKILL.md")) + list(
    glob.glob("cookbooks/*/SKILL.md")
):
    content = Path(skill).read_text(encoding="utf-8")
    if re.search(r"(?m)^## Requires\b", content):
        cookbook_paths.add(skill)

counts = {}
for skill in glob.glob("plugins/*/skills/*/SKILL.md"):
    if skill in cookbook_paths:
        continue
    category = Path(skill).parts[1]
    counts[category] = counts.get(category, 0) + 1

catalog_section = re.search(
    r"## Catalog\n(.*?)(?=\n## )",
    text,
    flags=re.S,
)
if not catalog_section:
    fail("README missing ## Catalog section")
else:
    rows = re.findall(
        r"\| ([^|]+) \| (\d+) \| \[`plugins/([^/]+)/skills/`\]",
        catalog_section.group(1),
    )
    readme_counts = {}
    for _label, count, category in rows:
        readme_counts[category] = int(count)
    if set(readme_counts) != set(counts):
        fail(
            "README catalog categories drift from plugins/: "
            f"readme={sorted(readme_counts)} actual={sorted(counts)}"
        )
    for category, actual in sorted(counts.items()):
        declared = readme_counts.get(category)
        if declared != actual:
            fail(
                f"README catalog count for {category} is {declared}, "
                f"discovered {actual}"
            )

# Cookbook count in the Cookbooks table.
cookbook_section = re.search(
    r"## Cookbooks\n(.*?)(?=\n## )",
    text,
    flags=re.S,
)
expected_cookbooks = len(cookbook_paths)
if not cookbook_section:
    fail("README missing ## Cookbooks section")
else:
    cookbook_rows = re.findall(
        r"\| \[`[^`]+`\]\([^)]+\) \|",
        cookbook_section.group(1),
    )
    if len(cookbook_rows) != expected_cookbooks:
        fail(
            f"README cookbook table has {len(cookbook_rows)} rows, "
            f"discovered {expected_cookbooks}"
        )

# Deterministic local commands referenced in README must exist.
# Skip examples that still contain OWNER/REPOSITORY placeholders.
command_candidates = set()
for match in re.finditer(r"`((?:python3 |bash |env )?scripts/[^`]+)`", text):
    command_candidates.add(match.group(1))
for match in re.finditer(r"`(python3 scripts/[^`]+)`", text):
    command_candidates.add(match.group(1))

script_paths = set()
for candidate in sorted(command_candidates):
    if "OWNER/REPOSITORY" in candidate:
        continue
    # Strip flags / args after the script path.
    parts = candidate.split()
    script = None
    for part in parts:
        if part.startswith("scripts/"):
            script = part
            break
    if script is None:
        continue
    script_paths.add(script)
    if not Path(script).exists():
        fail(f"README references missing local command path: {script}")

required_scripts = {
    "scripts/sync-plugin-metadata.py",
    "scripts/check-agent-plugins.sh",
    "scripts/check-claude-plugins.sh",
    "scripts/check-codex-plugins.sh",
    "scripts/check-cookbooks.sh",
    "scripts/check-cursor-plugins.sh",
    "scripts/check-opencode-loader.sh",
    "scripts/check-readme.sh",
}
missing_required = sorted(required_scripts - script_paths)
if missing_required:
    fail(
        "README Validate/support text must name every release-gate script; missing: "
        + ", ".join(missing_required)
    )

# Layout must document new adapter paths and must not invent .cursor-plugin/.
layout_section = re.search(r"## Layout\n(.*?)(?=\n## )", text, flags=re.S)
if not layout_section:
    fail("README missing ## Layout section")
else:
    layout = layout_section.group(1)
    for marker in (
        ".opencode/",
        "package.json",
        "requirements-dev.txt",
        "sync-plugin-metadata.py",
        "check-cursor-plugins.sh",
        "check-opencode-loader.sh",
        "check-readme.sh",
        "check-claude-plugins.sh",
    ):
        if marker not in layout:
            fail(f"README Layout missing {marker}")
    if ".cursor-plugin/" in layout:
        fail("README Layout must not document .cursor-plugin/")

if errors:
    for item in errors:
        print(f"FAIL: {item}")
    raise SystemExit(1)

print(
    f"OK: README contract matches {len(counts)} categories "
    f"({sum(counts.values())} catalog skills) and {expected_cookbooks} cookbooks"
)
PY

if [ "$status" -ne 0 ]; then
  exit 1
fi
