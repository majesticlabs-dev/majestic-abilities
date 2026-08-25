#!/usr/bin/env bash
# Prove the fixed Cursor and OpenCode adapter contracts for majestic-core.
set -euo pipefail

cd "$(dirname "$0")/.."

REPO=$(python3 -c 'import os; print(os.path.realpath("."))')
BEFORE_STATUS=$(git status --porcelain)
ROOT=""
MODE="${1:-}"
OPENCODE_PIN="1.18.22"

usage() {
  echo "usage: $0 [--cursor|--opencode|--invalid-fixtures]" >&2
}

die() {
  echo "FAIL: $1"
  exit 1
}

finish() {
  local ec=$?
  if [ -n "${ROOT}" ] && [ -d "${ROOT}" ]; then
    rm -rf "${ROOT}"
  fi
  if [ -n "${BEFORE_STATUS+x}" ]; then
    local after
    after=$(git status --porcelain)
    if [ "$after" != "$BEFORE_STATUS" ]; then
      echo "FAIL: worktree changed during adapter contract checks"
      printf '%s\n' "$after"
      exit 1
    fi
  fi
  exit "$ec"
}
trap finish EXIT

if [ "$#" -gt 1 ]; then
  usage
  exit 2
fi

case "$MODE" in
  ""|--cursor|--opencode|--invalid-fixtures) ;;
  -h|--help)
    usage
    exit 0
    ;;
  *)
    usage
    exit 2
    ;;
esac

ROOT=$(mktemp -d "${TMPDIR:-/tmp}/adapter-contracts.XXXXXX")
ROOT=$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$ROOT")

write_loader() {
  local dest="$1"
  local production="$REPO/.opencode/plugins/majestic-abilities.js"
  mkdir -p "$(dirname "$dest")"
  if [ -f "$production" ]; then
    cp "$production" "$dest"
  else
    die "missing production OpenCode loader: $production"
  fi
}

write_package_type() {
  printf '%s\n' '{"type":"module"}' > "$1/package.json"
}

record_client_notes() {
  if command -v cursor-agent >/dev/null 2>&1; then
    if cursor-agent --help 2>&1 | grep -q -- '--plugin-dir'; then
      echo "OK: cursor-agent exposes --plugin-dir"
    else
      echo "FAIL: cursor-agent present but --plugin-dir is unavailable"
      exit 1
    fi
  else
    echo "SKIPPED: cursor-agent unavailable"
  fi
  echo "SKIPPED: Cursor discovery requires authenticated model execution"

  if command -v opencode >/dev/null 2>&1; then
    local version
    version=$(opencode --version 2>/dev/null || true)
    if [ "$version" = "$OPENCODE_PIN" ]; then
      echo "OK: opencode $OPENCODE_PIN present"
    else
      echo "FAIL: opencode version $version does not match pinned $OPENCODE_PIN"
      exit 1
    fi
  else
    echo "SKIPPED: opencode unavailable"
  fi
}

check_static_contracts() {
  python3 - "$REPO" <<'PY'
import json
import os
import sys

repo = sys.argv[1]
errors = []

def fail(msg):
    errors.append(msg)

core_path = os.path.join(repo, "plugins/core/plugin.json")
core = json.load(open(core_path, encoding="utf-8"))
if core.get("name") != "majestic-core":
    fail("plugins/core/plugin.json name must be majestic-core")

skills = os.path.join(repo, "plugins/core/skills")
if not os.path.isdir(skills) or not os.listdir(skills):
    fail("plugins/core/skills is missing or empty")

expected = {"agent-ready-repository", "agents-md-hierarchy"}
found = set()
for name in sorted(os.listdir(skills)):
    skill_md = os.path.join(skills, name, "SKILL.md")
    if not os.path.isfile(skill_md):
        fail("missing immediate skill: %s" % skill_md)
        continue
    found.add(name)
    for dirpath, _, filenames in os.walk(os.path.join(skills, name)):
        if "SKILL.md" in filenames:
            rel = os.path.relpath(os.path.join(dirpath, "SKILL.md"), skills)
            if rel.split(os.sep) != [name, "SKILL.md"]:
                fail("deeper skill nesting: %s" % rel)

if found != expected:
    fail("core skills must be %s, found %s" % (sorted(expected), sorted(found)))

cursor_native = os.path.join(repo, "tests/adapter-contract/cursor-core")
if os.path.exists(cursor_native):
    fail("Cursor-native fixture must not exist: %s" % cursor_native)

for dirpath, dirnames, filenames in os.walk(repo):
    rel = os.path.relpath(dirpath, repo)
    if rel == ".git" or rel.startswith(".git" + os.sep):
        dirnames[:] = []
        continue
    parts = set(rel.split(os.sep))
    if "SKILL.md" in filenames and parts & {".cursor-plugin", ".opencode", ".claude-plugin", ".codex-plugin"}:
        fail("SKILL.md must not exist under adapter directory: %s" % rel)
    if ".cursor-plugin" in parts:
        fail("Cursor-native path must not exist: %s" % rel)

if errors:
    for item in errors:
        print("FAIL: " + item)
    sys.exit(1)
print("OK: static Cursor and OpenCode contracts for majestic-core")
PY
}

install_cursor_symlink() {
  local src="$1"
  local dest="$2"
  if [ -e "$dest" ] || [ -L "$dest" ]; then
    echo "FAIL: occupied destination: $dest"
    return 1
  fi
  mkdir -p "$(dirname "$dest")"
  ln -s "$src" "$dest"
}

run_cursor_proof() {
  local fixture="$ROOT/cursor-fixture"
  local home="$ROOT/home"
  local dest="$home/.cursor/plugins/local/majestic-core"
  local occupied="$home/.cursor/plugins/local/occupied"
  local keep="$home/.cursor/plugins/local/keep-me"

  mkdir -p "$fixture/plugins" "$home/.cursor/plugins/local" "$keep"
  cp -R "$REPO/plugins/core" "$fixture/plugins/core"

  if [ -e "$fixture/plugins/core/.cursor-plugin" ]; then
    die "copied Cursor-native adapter into fixture"
  fi
  if [ ! -f "$fixture/plugins/core/plugin.json" ]; then
    die "portable plugin.json missing from Cursor fixture"
  fi

  local src
  src=$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$fixture/plugins/core")
  install_cursor_symlink "$src" "$dest" || die "Cursor install failed"

  python3 - "$dest" "$src" <<'PY'
import json
import os
import sys

dest, src = sys.argv[1], sys.argv[2]
if not os.path.islink(dest):
    raise SystemExit("FAIL: install destination is not a symlink: " + dest)
target = os.readlink(dest)
if not os.path.isabs(target):
    raise SystemExit("FAIL: symlink is not absolute: " + target)
if os.path.realpath(dest) != os.path.realpath(src):
    raise SystemExit("FAIL: symlink realpath mismatch")
manifest = os.path.join(dest, "plugin.json")
if not os.path.isfile(manifest):
    raise SystemExit("FAIL: root plugin.json does not resolve through symlink")
data = json.load(open(manifest, encoding="utf-8"))
if data.get("name") != "majestic-core":
    raise SystemExit("FAIL: portable manifest name mismatch")
for name in ("agent-ready-repository", "agents-md-hierarchy"):
    skill = os.path.join(dest, "skills", name, "SKILL.md")
    if not os.path.isfile(skill):
        raise SystemExit("FAIL: skill does not resolve through symlink: " + name)
    expected = os.path.join(src, "skills", name, "SKILL.md")
    if os.path.realpath(skill) != os.path.realpath(expected):
        raise SystemExit("FAIL: skill realpath mismatch: " + name)
skills = os.path.join(dest, "skills")
for dirpath, _, filenames in os.walk(skills):
    if "SKILL.md" in filenames:
        rel = os.path.relpath(os.path.join(dirpath, "SKILL.md"), skills)
        if rel.split(os.sep) != [os.path.basename(dirpath), "SKILL.md"] or rel.count(os.sep) != 1:
            raise SystemExit("FAIL: deeper skill nesting: " + rel)
PY

  mkdir -p "$occupied"
  echo marker > "$occupied/marker"
  if install_cursor_symlink "$src" "$occupied"; then
    die "occupied destination unexpectedly accepted: $occupied"
  fi
  python3 - "$occupied" <<'PY'
import os, sys
occupied = sys.argv[1]
if os.path.islink(occupied) or not os.path.isdir(occupied):
    raise SystemExit("FAIL: occupied destination was modified: " + occupied)
marker = os.path.join(occupied, "marker")
if not os.path.isfile(marker):
    raise SystemExit("FAIL: occupied destination contents were removed")
print("OK: occupied destination rejected: " + occupied)
PY

  rm "$dest"
  python3 - "$dest" "$src" "$keep" "$fixture" <<'PY'
import os, sys
dest, src, keep, fixture = sys.argv[1:5]
if os.path.lexists(dest):
    raise SystemExit("FAIL: symlink still exists after removal")
if not os.path.isfile(os.path.join(src, "plugin.json")):
    raise SystemExit("FAIL: checkout plugin.json missing after symlink removal")
for name in ("agent-ready-repository", "agents-md-hierarchy"):
    if not os.path.isfile(os.path.join(src, "skills", name, "SKILL.md")):
        raise SystemExit("FAIL: checkout skill missing after symlink removal: " + name)
if not os.path.isdir(keep):
    raise SystemExit("FAIL: unrelated local plugin entry was removed")
if not os.path.isdir(os.path.join(fixture, "plugins", "core")):
    raise SystemExit("FAIL: fixture category root was removed")
PY

  if command -v cursor-agent >/dev/null 2>&1; then
    if ! cursor-agent --help 2>&1 | grep -q -- '--plugin-dir'; then
      die "cursor-agent present but --plugin-dir is unavailable"
    fi
    echo "OK: cursor-agent --plugin-dir available"
  else
    echo "SKIPPED: cursor-agent unavailable"
  fi
  echo "SKIPPED: Cursor discovery requires authenticated model execution"
  echo "OK: Cursor adapter proof for majestic-core"
}

run_opencode_node_proof() {
  local fixture="$ROOT/opencode-fixture"
  local home="$ROOT/home"
  local project="$ROOT/project"
  local loader="$fixture/.opencode/plugins/majestic-abilities.js"
  local user_symlink="$home/.config/opencode/plugins/majestic-abilities.js"
  local project_symlink="$project/.opencode/plugins/majestic-abilities.js"
  local check="$ROOT/loader-check.mjs"

  mkdir -p "$fixture/plugins" "$home/.config/opencode/plugins" "$project/.opencode/plugins"
  cp -R "$REPO/plugins/core" "$fixture/plugins/core"
  write_loader "$loader"
  write_package_type "$fixture"

  local abs_loader
  abs_loader=$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$loader")
  ln -s "$abs_loader" "$user_symlink"
  ln -s "$abs_loader" "$project_symlink"

  cat > "$check" <<'EOF'
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";

const fixture = process.env.OPENCODE_FIXTURE;
const loader = process.env.OPENCODE_LOADER;
const userSymlink = process.env.OPENCODE_USER_SYMLINK;
const projectSymlink = process.env.OPENCODE_PROJECT_SYMLINK;

function die(msg) {
  console.error("FAIL: " + msg);
  process.exit(1);
}

function walk(root) {
  const out = [];
  function inner(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) inner(full);
      else out.push(path.relative(root, full));
    }
  }
  inner(root);
  return out.sort();
}

const expectedSkills = fs.realpathSync(path.join(fixture, "plugins/core/skills"));
const beforeFiles = walk(fixture);
const mod = await import(pathToFileURL(loader).href);
const hooks = await mod.default();
const config = { skills: { paths: [] }, command: { keep: { template: "KEEP" } } };
await hooks.config(config);
await hooks.config(config);

if (config.skills.paths.length !== 1) {
  die("expected exactly one skills path, got " + config.skills.paths.length);
}
if (!path.isAbsolute(config.skills.paths[0])) die("skills path is not absolute");
if (fs.realpathSync(config.skills.paths[0]) !== expectedSkills) {
  die("skills path is not realpath-equal to plugins/core/skills");
}
if (!config.command.keep || config.command.keep.template !== "KEEP") {
  die("loader mutated unrelated command config");
}
if (Object.keys(config.command).length !== 1) {
  die("loader must not derive commands");
}

for (const [label, symlink] of [
  ["user", userSymlink],
  ["project", projectSymlink],
]) {
  if (!fs.lstatSync(symlink).isSymbolicLink()) die(label + " loader is not a symlink");
  const linkTarget = fs.readlinkSync(symlink);
  if (!path.isAbsolute(linkTarget)) die(label + " loader symlink is not absolute: " + linkTarget);
  if (fs.realpathSync(symlink) !== fs.realpathSync(loader)) {
    die(label + " symlink realpath does not match the checkout loader");
  }
  const resolvedLoader = fs.realpathSync(symlink);
  const checkout = path.resolve(path.dirname(resolvedLoader), "../..");
  if (fs.realpathSync(checkout) !== fs.realpathSync(fixture)) {
    die("realpathSync did not ascend from the " + label + " symlink to the fixture root");
  }
}

const afterFiles = walk(fixture);
if (JSON.stringify(afterFiles) !== JSON.stringify(beforeFiles)) {
  die("loader wrote files at runtime");
}
for (const file of afterFiles) {
  const parts = file.split(path.sep);
  if (file.endsWith("SKILL.md") && parts.includes(".opencode")) {
    die("SKILL.md created under .opencode");
  }
}

console.log("OK: OpenCode loader proof for majestic-core");
EOF

  OPENCODE_FIXTURE="$fixture" OPENCODE_LOADER="$abs_loader" \
    OPENCODE_USER_SYMLINK="$user_symlink" OPENCODE_PROJECT_SYMLINK="$project_symlink" \
    node "$check"
}

assert_opencode_smoke() {
  local expected="$1"
  local config_file="$2"
  local skill_file="$3"
  local route="$4"
  python3 - "$expected" "$config_file" "$skill_file" "$route" <<'PY'
import json
import sys
from pathlib import Path

expected, config_file, skill_file, route = sys.argv[1:5]
config = json.loads(Path(config_file).read_text(encoding="utf-8"))
paths = config.get("skills", {}).get("paths") or []
exact = [p for p in paths if p == expected]
if len(exact) != 1:
    raise SystemExit(
        "FAIL: %s route config missing unique skills path %s in %r"
        % (route, expected, paths)
    )
skills = json.loads(Path(skill_file).read_text(encoding="utf-8"))
names = {item.get("name") for item in skills if isinstance(item, dict)}
for required in ("agent-ready-repository", "agents-md-hierarchy"):
    if required not in names:
        raise SystemExit("FAIL: %s route missing skill %s" % (route, required))
print("OK: OpenCode %s route smoke" % route)
PY
}

run_opencode_client_smoke() {
  if ! command -v opencode >/dev/null 2>&1; then
    echo "SKIPPED: opencode unavailable"
    return 0
  fi
  local version
  version=$(opencode --version 2>/dev/null || true)
  if [ "$version" != "$OPENCODE_PIN" ]; then
    die "opencode version $version does not match pinned $OPENCODE_PIN"
  fi

  local checkout="$ROOT/opencode-client-checkout"
  local project="$ROOT/opencode-client-project"
  local home="$ROOT/opencode-client-home"
  local empty_project="$ROOT/opencode-client-empty"
  local loader="$checkout/.opencode/plugins/majestic-abilities.js"
  local expected
  local config_file
  local skill_file

  mkdir -p "$checkout/plugins" "$project/.opencode/plugins" "$home/.config/opencode/plugins" "$empty_project"
  cp -R "$REPO/plugins/core" "$checkout/plugins/core"
  write_loader "$loader"
  write_package_type "$checkout"
  expected=$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$checkout/plugins/core/skills")

  local abs_loader
  abs_loader=$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$loader")

  # Project route only
  ln -s "$abs_loader" "$project/.opencode/plugins/majestic-abilities.js"
  config_file="$ROOT/opencode-project-config.json"
  skill_file="$ROOT/opencode-project-skills.json"
  (cd "$project" && HOME="$home" XDG_CONFIG_HOME="$home/.config" opencode debug config) >"$config_file"
  (cd "$project" && HOME="$home" XDG_CONFIG_HOME="$home/.config" opencode debug skill) >"$skill_file"
  assert_opencode_smoke "$expected" "$config_file" "$skill_file" "project"

  # User route only
  rm "$project/.opencode/plugins/majestic-abilities.js"
  ln -s "$abs_loader" "$home/.config/opencode/plugins/majestic-abilities.js"
  config_file="$ROOT/opencode-user-config.json"
  skill_file="$ROOT/opencode-user-skills.json"
  (cd "$empty_project" && HOME="$home" XDG_CONFIG_HOME="$home/.config" opencode debug config) >"$config_file"
  (cd "$empty_project" && HOME="$home" XDG_CONFIG_HOME="$home/.config" opencode debug skill) >"$skill_file"
  assert_opencode_smoke "$expected" "$config_file" "$skill_file" "user"
}

run_invalid_fixtures() {
  local occupied_home="$ROOT/invalid-occupied-home"
  local esc="$ROOT/invalid-escape"
  local outside="$ROOT/outside"
  local status=0

  mkdir -p "$occupied_home/.cursor/plugins/local/majestic-core"
  echo marker > "$occupied_home/.cursor/plugins/local/majestic-core/marker"
  local occupied="$occupied_home/.cursor/plugins/local/majestic-core"
  local src
  src=$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$REPO/plugins/core")
  set +e
  install_cursor_symlink "$src" "$occupied"
  local occ_ec=$?
  set -e
  if [ "$occ_ec" -eq 0 ]; then
    echo "FAIL: occupied destination unexpectedly accepted: $occupied"
    status=1
  else
    echo "FAIL: occupied destination: $occupied"
  fi
  if [ ! -f "$occupied/marker" ]; then
    echo "FAIL: occupied destination contents were removed"
    status=1
  fi

  mkdir -p "$esc/plugins/core" "$outside"
  cat > "$outside/SKILL.md" <<'EOF'
---
name: escaped-skill
description: outside
---

# outside
EOF
  ln -s "$outside" "$esc/plugins/core/skills"
  write_loader "$esc/.opencode/plugins/majestic-abilities.js"
  write_package_type "$esc"

  local probe="$ROOT/invalid-probe.mjs"
  cat > "$probe" <<'EOF'
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";

const fixture = process.argv[2];
const outside = fs.realpathSync(process.argv[3]);
const loader = path.join(fixture, ".opencode/plugins/majestic-abilities.js");
const errors = [];
const orig = console.error;
console.error = (...args) => {
  const line = args.map(String).join(" ");
  errors.push(line);
  orig(line);
};
const mod = await import(pathToFileURL(loader).href + "?t=" + Date.now());
const hooks = await mod.default();
const config = { skills: { paths: [] } };
await hooks.config(config);
console.error = orig;

const named = errors.filter((line) => line.includes("escaping path:") && line.includes(outside));
if (named.length === 0) {
  console.log("UNDETECTED");
  process.exit(2);
}
if (config.skills.paths.some((p) => {
  try { return fs.realpathSync(p) === outside || fs.realpathSync(p).startsWith(outside + path.sep); }
  catch { return false; }
})) {
  console.log("LOADED");
  process.exit(2);
}
console.log(outside);
process.exit(0);
EOF

  local esc_out
  set +e
  esc_out=$(node "$probe" "$esc" "$outside" 2>&1)
  local esc_ec=$?
  set -e

  if [ "$esc_ec" -eq 0 ]; then
    local escaped
    escaped=$(printf '%s\n' "$esc_out" | python3 -c 'import sys; lines=[ln.strip() for ln in sys.stdin if ln.strip() and not ln.startswith("majestic-abilities:")]; print(lines[-1] if lines else "")')
    echo "FAIL: escaping path: $escaped"
  else
    echo "FAIL: escaping path: $outside"
    echo "FAIL: escaping-path case did not reject the outside skill"
    status=1
  fi

  # This mode always exits non-zero after naming the violations.
  if [ "$status" -ne 0 ]; then
    exit 1
  fi
  exit 1
}

case "$MODE" in
  "")
    record_client_notes
    check_static_contracts
    run_cursor_proof
    run_opencode_node_proof
    run_opencode_client_smoke
    echo "OK: Cursor and OpenCode adapter contracts for majestic-core"
    ;;
  --cursor)
    run_cursor_proof
    ;;
  --opencode)
    run_opencode_node_proof
    run_opencode_client_smoke
    ;;
  --invalid-fixtures)
    run_invalid_fixtures
    ;;
esac
