#!/usr/bin/env bash
# Validate the pinned OpenCode V1 path loader with Node and real-client checks.
set -euo pipefail

cd "$(dirname "$0")/.."

OPENCODE_PIN="1.18.22"
REPO=$(python3 -c 'import os; print(os.path.realpath("."))')
BEFORE_STATUS=$(git status --porcelain)
ROOT=""

die() {
  echo "FAIL: $1"
  exit 1
}

finish() {
  local ec=$?
  if [ -n "${ROOT}" ] && [ -d "${ROOT}" ]; then
    rm -rf "${ROOT}"
  fi
  local after
  after=$(git status --porcelain)
  if [ "$after" != "$BEFORE_STATUS" ]; then
    echo "FAIL: worktree changed during OpenCode loader checks"
    printf '%s\n' "$after"
    exit 1
  fi
  exit "$ec"
}
trap finish EXIT

LOADER=".opencode/plugins/majestic-abilities.js"
if [ ! -f "$LOADER" ]; then
  die "missing production loader: $LOADER"
fi

if [ ! -f package.json ]; then
  die "missing package.json"
fi

python3 - <<'PY'
import json
from pathlib import Path

data = json.loads(Path("package.json").read_text(encoding="utf-8"))
errors = []
if data.get("name") != "majestic-abilities":
    errors.append("package.json name must be majestic-abilities")
if data.get("private") is not True:
    errors.append("package.json must set private: true")
if data.get("type") != "module":
    errors.append('package.json must set type: "module"')
for forbidden in ("version", "main", "dependencies", "devDependencies", "publishConfig"):
    if forbidden in data:
        errors.append(f"package.json must not declare {forbidden}")
if errors:
    for item in errors:
        print("FAIL: " + item)
    raise SystemExit(1)
print("OK: package.json is a minimal ESM loader manifest")
PY

echo "Running Node OpenCode loader tests"
node --test tests/opencode-loader.test.js

echo "Checking adapter OpenCode contracts"
bash scripts/check-adapter-contracts.sh --opencode

python3 - "$REPO" <<'PY'
import os
import sys
from pathlib import Path

repo = Path(sys.argv[1])
errors = []
loader = repo / ".opencode" / "plugins" / "majestic-abilities.js"
if not loader.is_file():
    errors.append("missing production loader")

for dirpath, dirnames, filenames in os.walk(repo / ".opencode", followlinks=False):
    if "SKILL.md" in filenames:
        rel = Path(dirpath).relative_to(repo) / "SKILL.md"
        errors.append(f"SKILL.md must not exist under .opencode/: {rel}")

for dirpath, dirnames, filenames in os.walk(repo, followlinks=False):
    rel = Path(dirpath).relative_to(repo)
    if rel.parts and rel.parts[0] == ".git":
        dirnames[:] = []
        continue
    if "SKILL.md" in filenames and ".opencode" in rel.parts:
        errors.append(f"SKILL.md must not exist under .opencode/: {rel / 'SKILL.md'}")

text = loader.read_text(encoding="utf-8")
for banned in ("parseFrontmatter", "unquote(", "config.command"):
    if banned in text:
        errors.append(f"production loader must not contain {banned!r}")

if errors:
    for item in errors:
        print("FAIL: " + item)
    raise SystemExit(1)
print("OK: OpenCode adapter containment")
PY

echo "Proving production loader registers all category skill paths"
OPENCODE_CHECK_REPO="$REPO" node --input-type=module <<'EOF'
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";

const repo = process.env.OPENCODE_CHECK_REPO;
const loader = path.join(repo, ".opencode/plugins/majestic-abilities.js");
const mod = await import(pathToFileURL(loader).href + "?t=" + Date.now());
const hooks = await mod.default();
const config = { skills: { paths: [] } };
await hooks.config(config);
await hooks.config(config);

const categories = fs
  .readdirSync(path.join(repo, "plugins"))
  .filter((name) => fs.statSync(path.join(repo, "plugins", name)).isDirectory())
  .sort();
if (categories.length !== 15) {
  console.error("FAIL: expected 15 categories, found " + categories.length);
  process.exit(1);
}
const expected = categories.map((name) =>
  fs.realpathSync(path.join(repo, "plugins", name, "skills")),
);
const actual = config.skills.paths.map((p) => fs.realpathSync(p));
if (JSON.stringify(actual) !== JSON.stringify(expected)) {
  console.error("FAIL: loader paths mismatch");
  console.error(JSON.stringify({ expected, actual }, null, 2));
  process.exit(1);
}
console.log("OK: production loader registered " + actual.length + " category skill paths");
EOF

run_real_client_smoke() {
  if ! command -v opencode >/dev/null 2>&1; then
    die "opencode is required for the OpenCode release gate (pinned $OPENCODE_PIN)"
  fi
  local version
  version=$(opencode --version 2>/dev/null || true)
  if [ "$version" != "$OPENCODE_PIN" ]; then
    die "opencode version $version does not match pinned $OPENCODE_PIN"
  fi

  ROOT=$(mktemp -d "${TMPDIR:-/tmp}/opencode-loader-check.XXXXXX")
  ROOT=$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$ROOT")

  local home="$ROOT/home"
  local project="$ROOT/project"
  local empty_project="$ROOT/empty-project"
  local abs_loader
  abs_loader=$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$LOADER")

  mkdir -p "$home/.config/opencode/plugins" "$project/.opencode/plugins" "$empty_project"

  local expected_core
  expected_core=$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$REPO/plugins/core/skills")

  assert_smoke() {
    local route="$1"
    local config_file="$2"
    local skill_file="$3"
    python3 - "$route" "$config_file" "$skill_file" "$expected_core" "$REPO" <<'PY'
import json
import os
import sys
from pathlib import Path

route, config_file, skill_file, expected_core, repo = sys.argv[1:6]
config = json.loads(Path(config_file).read_text(encoding="utf-8"))
paths = config.get("skills", {}).get("paths") or []
plugins = Path(repo) / "plugins"
expected = sorted(
    os.path.realpath(plugins / name / "skills")
    for name in os.listdir(plugins)
    if (plugins / name).is_dir()
)
actual = [os.path.realpath(p) for p in paths]
missing = [p for p in expected if actual.count(p) != 1]
extras = [p for p in actual if p not in expected]
dupes = sorted({p for p in actual if actual.count(p) > 1})
if missing or extras or dupes or len(actual) != len(expected):
    raise SystemExit(
        "FAIL: %s route skills.paths mismatch missing=%s extras=%s dupes=%s count=%s"
        % (route, missing, extras, dupes, len(actual))
    )
if actual.count(expected_core) != 1:
    raise SystemExit("FAIL: %s route missing unique core skills path" % route)
skills = json.loads(Path(skill_file).read_text(encoding="utf-8"))
names = {item.get("name") for item in skills if isinstance(item, dict)}
for required in ("agent-ready-repository", "agents-md-hierarchy"):
    if required not in names:
        raise SystemExit("FAIL: %s route missing skill %s" % (route, required))
print("OK: OpenCode %s route reports %s category skill paths" % (route, len(expected)))
PY
  }

  # Project route
  ln -s "$abs_loader" "$project/.opencode/plugins/majestic-abilities.js"
  local project_config="$ROOT/project-config.json"
  local project_skills="$ROOT/project-skills.json"
  (cd "$project" && HOME="$home" XDG_CONFIG_HOME="$home/.config" opencode debug config) >"$project_config"
  (cd "$project" && HOME="$home" XDG_CONFIG_HOME="$home/.config" opencode debug skill) >"$project_skills"
  assert_smoke "project" "$project_config" "$project_skills"

  # User route
  rm "$project/.opencode/plugins/majestic-abilities.js"
  ln -s "$abs_loader" "$home/.config/opencode/plugins/majestic-abilities.js"
  local user_config="$ROOT/user-config.json"
  local user_skills="$ROOT/user-skills.json"
  (cd "$empty_project" && HOME="$home" XDG_CONFIG_HOME="$home/.config" opencode debug config) >"$user_config"
  (cd "$empty_project" && HOME="$home" XDG_CONFIG_HOME="$home/.config" opencode debug skill) >"$user_skills"
  assert_smoke "user" "$user_config" "$user_skills"
}

run_real_client_smoke

echo "OK: OpenCode V1 loader validation complete"
